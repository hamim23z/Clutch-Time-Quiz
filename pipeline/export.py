"""One command for session 5: fame fixes, candidates, curation and the two files the website reads.

    python3 pipeline/export.py

Runs everything `pipeline/generate.py` does (fame, tiers, candidates, their reports), then
  - picks and arranges the final prompts (9 dives of 7; see pipeline/curate.py and docs/export-format.md),
  - builds the universe of every player and team with their aliases (pipeline/data/aliases.csv, team_aliases.csv),
  - checks both files: schemas, every answer id in the universe, every point value against its tier,
  - checks pipeline/data/outside_range.csv against the universe,
  - rechecks 10 random prompts against the processed tables with an independent brute-force query,
and writes data/export/prompts.json, data/export/universe.json, docs/prompts-sample.md and docs/curation-report.md.
"""
from __future__ import annotations

import argparse
import gzip
import json
import sys
from pathlib import Path

import pandas as pd

from curate import curate
from exportcheck import check_all
from exportreport import write_reports
from fame import OVERRIDES_PATH
from generate import build, summary
from matchnorm import base_name, normalize
from players import load_aliases
from templates import TEMPLATES
from universe import TEAM_ALIASES_PATH, build_universe, load_team_aliases
from verify import verify_sample

HERE = Path(__file__).resolve().parent
ALIASES_PATH = HERE / "data" / "aliases.csv"
OUTSIDE_RANGE_PATH = HERE / "data" / "outside_range.csv"
PROMPT_SLUG_PREFIX = "cand-"


def prompt_id(candidate_id: str) -> str:
    """cand-points-regular-50 -> p-points-regular-50: stable, readable, and the same on every run."""
    return "p-" + candidate_id.removeprefix(PROMPT_SLUG_PREFIX)


def check_outside_range(names: list[str], universe: dict) -> None:
    """The outside-range list must not name anyone the game knows: no entry may read as a universe name or alias."""
    known = {normalize(base_name(e["name"]), True) for e in universe["players"] + universe["teams"]}
    known |= {normalize(a, True) for e in universe["players"] + universe["teams"] for a in e["aliases"]}
    dupes = [n for n in names if names.count(n) > 1]
    clashes = [n for n in names if normalize(n, True) in known]
    if dupes or clashes:
        raise ValueError(f"outside_range.csv: duplicates {sorted(set(dupes))}, names in the universe {clashes}")


def dump_lines(items: list[dict]) -> str:
    """A JSON array with one compact item per line: small on the wire, readable in a diff."""
    return "[\n" + ",\n".join(json.dumps(i, ensure_ascii=False, separators=(",", ":")) for i in items) + "\n]"


def render_prompts(prompts: list[dict]) -> str:
    return dump_lines(prompts) + "\n"


def render_universe(universe: dict) -> str:
    return '{"players":' + dump_lines(universe["players"]) + ',\n"teams":' + dump_lines(universe["teams"]) + "}\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--processed-dir", type=Path, default=Path("data/processed"))
    ap.add_argument("--out-dir", type=Path, default=Path("data/generated"))
    ap.add_argument("--export-dir", type=Path, default=Path("data/export"))
    ap.add_argument("--docs-dir", type=Path, default=HERE.parent / "docs")
    ap.add_argument("--overrides", type=Path, default=OVERRIDES_PATH)
    ap.add_argument("--aliases", type=Path, default=ALIASES_PATH)
    ap.add_argument("--team-aliases", type=Path, default=TEAM_ALIASES_PATH)
    ap.add_argument("--outside-range", type=Path, default=OUTSIDE_RANGE_PATH)
    ap.add_argument("--check-count", type=int, default=10, help="how many random prompts to recheck against the tables")
    args = ap.parse_args(argv)

    tables, fame, result = build(args.processed_dir, args.out_dir, args.docs_dir, args.overrides)
    print("\n".join(summary(fame, result)))

    groups = {t.key: t.stat_group for t in TEMPLATES}
    curated = curate(result.prompts, result.meta, groups)
    renamed = {i.prompt["id"]: prompt_id(i.prompt["id"]) for i in curated.items}
    for item in curated.items:
        item.prompt = {**item.prompt, "id": renamed[item.prompt["id"]]}
    prompts = curated.prompts

    universe, dropped = build_universe(tables.players, tables.teams, load_aliases(args.aliases), load_team_aliases(args.team_aliases))
    check_all(prompts, universe)
    outside = pd.read_csv(args.outside_range)["name"].tolist()
    check_outside_range(outside, universe)

    checks = verify_sample(curated.items, tables, fame, k=args.check_count)

    args.export_dir.mkdir(parents=True, exist_ok=True)
    files = {"prompts.json": render_prompts(prompts), "universe.json": render_universe(universe)}
    sizes = {}
    for name, text in files.items():
        data = text.encode("utf-8")
        (args.export_dir / name).write_bytes(data)
        sizes[name] = (len(data), len(gzip.compress(data, 9)))
    sizes["both files"] = (sum(s[0] for s in sizes.values()), sum(s[1] for s in sizes.values()))
    write_reports(curated, checks, sizes, len(result.prompts), args.docs_dir)

    print(f"export: {len(prompts)} prompts, {len(universe['players']):,} players, {len(universe['teams'])} teams; "
          f"{sizes['both files'][0]:,} bytes ({sizes['both files'][1]:,} gzipped)")
    print(f"aliases dropped because another entry claims them: {len(dropped)}; outside-range names: {len(outside)}")
    bad = [c for c in checks if not c.ok]
    print(f"recheck: {len(checks) - len(bad)} of {len(checks)} random prompts match the tables")
    if bad:
        print("MISMATCH: " + ", ".join(c.prompt_id for c in bad))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
