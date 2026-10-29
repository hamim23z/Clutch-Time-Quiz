"""One command for session 4: fame score, tiers, candidate prompts and both reports.

    python3 pipeline/generate.py

Reads data/processed/ (make it with `python3 pipeline/run.py`) and writes
  data/generated/fame.parquet           the fame table: every player with career points, best points per game, percentile, tier
  data/generated/candidates.json        candidate prompts, in the exact shape of schema/prompts.schema.json
  data/generated/candidates_meta.json   per-prompt details and every template/threshold attempt (kept or dropped)
  docs/fame-report.md, docs/prompt-candidates.md
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

from fame import OVERRIDES_PATH, compute_fame, load_overrides
from generator import generate, write_candidates
from reports import write_reports
from templates import TEMPLATES, Tables

HERE = Path(__file__).resolve().parent
TABLE_NAMES = ("players", "teams", "games", "player_games", "team_games")


def load_tables(processed_dir: Path) -> Tables:
    missing = [n for n in TABLE_NAMES if not (processed_dir / f"{n}.parquet").exists()]
    if missing:
        raise SystemExit(f"missing {', '.join(missing)} in {processed_dir}: run `python3 pipeline/run.py` first")
    return Tables(*[pd.read_parquet(processed_dir / f"{n}.parquet") for n in TABLE_NAMES])


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--processed-dir", type=Path, default=Path("data/processed"))
    ap.add_argument("--out-dir", type=Path, default=Path("data/generated"))
    ap.add_argument("--overrides", type=Path, default=OVERRIDES_PATH, help="hand-set fame tiers (athlete_id,tier,reason)")
    ap.add_argument("--docs-dir", type=Path, default=HERE.parent / "docs")
    args = ap.parse_args(argv)

    tables = load_tables(args.processed_dir)
    fame = compute_fame(tables.player_games, tables.players, tables.min_season_games, load_overrides(args.overrides))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    fame.to_parquet(args.out_dir / "fame.parquet", compression="zstd", index=False)
    result = generate(tables, fame)
    write_candidates(result, args.out_dir)
    write_reports(fame, result, args.docs_dir)

    counts = fame["tier"].value_counts().sort_index()
    print("players per tier: " + ", ".join(f"tier {t}: {c}" for t, c in counts.items()) + f" (of {len(fame):,})")
    none = [t.key for t in TEMPLATES if not any(m["template"] == t.key for m in result.meta)]
    print(f"candidates: {len(result.prompts)} ({sum(1 for p in result.prompts if p['answerType'] == 'player')} player, "
          f"{sum(1 for p in result.prompts if p['answerType'] == 'team')} team); era: {result.era}")
    print("templates with no candidates: " + (", ".join(none) if none else "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
