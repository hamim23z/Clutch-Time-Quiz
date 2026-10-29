"""Reports written by the export command: docs/prompts-sample.md and docs/curation-report.md."""
from __future__ import annotations

import random
from collections import Counter
from pathlib import Path

from curate import DIVE_SIZE, Curated
from rarity import render as render_rarity
from verify import Check

SAMPLE_SEED = 2026
SAMPLE_SIZE = 25


def _table(headers: list[str], rows: list[list[object]]) -> list[str]:
    return ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"] + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]


def _names(answers: list[dict]) -> str:
    return ", ".join(f"{a['name']} ({a['tier']})" for a in answers)


def render_sample(curated: Curated, checks: list[Check], sizes: dict[str, tuple[int, int]], largest: list[tuple[str, int, int]]) -> str:
    L = ["# Prompts sample and checks", "",
         "Written by `python3 pipeline/export.py`; do not edit by hand. Tiers are in brackets: 1 is the best-known answer (10 points), 6 the rarest (100 points).", ""]
    L += ["## File sizes", ""]
    L += _table(["file", "bytes", "gzipped (what a static host sends)"], [[name, f"{raw:,}", f"{gz:,}"] for name, (raw, gz) in sizes.items()]) + [""]
    L += ["The five largest prompts (valid answers, bytes in the file):", ""] + [f"- `{pid}`: {n} answers, {b:,} bytes" for pid, n, b in largest] + [""]
    ok = sum(c.ok for c in checks)
    families = Counter(c.template for c in checks)
    L += [f"## Recheck of {len(checks)} prompts against the processed tables", "",
          f"{ok} of {len(checks)} match. At least 2 prompts from each of the {len(families)} template families were recomputed from the raw rows by a separately written brute-force query "
          "(`pipeline/bruteforce.py`) and compared with the exported answers, and the tiers and points were rechecked.", ""]
    bad = [c for c in checks if not c.ok]
    if bad:
        L += _table(["prompt", "valid answers (brute force)", "exported answers", "missing", "extra", "tier problems"],
                    [[c.prompt_id, c.expected, c.exported, len(c.missing), len(c.extra), len(c.tier_problems)] for c in bad]) + [""]
    L += ["<details><summary>Every prompt checked</summary>", ""]
    L += _table(["prompt", "valid answers (brute force)", "exported answers", "result"], [[c.prompt_id, c.expected, c.exported, "ok" if c.ok else "**MISMATCH**"] for c in checks]) + ["", "</details>", ""]
    L += [f"## {SAMPLE_SIZE} random prompts (seed {SAMPLE_SEED})", ""]
    for item in sorted(random.Random(SAMPLE_SEED).sample(curated.items, SAMPLE_SIZE), key=lambda i: curated.items.index(i)):
        p = item.prompt
        pos = curated.items.index(item)
        answers = p["answers"]
        L += [f"### {p['id']} (dive {pos // DIVE_SIZE + 1}, prompt {pos % DIVE_SIZE + 1})", "",
              f"> {p['text']}", "",
              f"- {p['difficulty']}; {len(answers)} valid answers; tiers: " + ", ".join(f"{t}: {sum(1 for a in answers if a['tier'] == t)}" for t in range(1, 7) if any(a['tier'] == t for a in answers)),
              f"- Best known: {_names(answers[:3])}",
              f"- Rarest: {_names(list(reversed(answers[-3:])))}", ""]
    return "\n".join(L).rstrip() + "\n"


def render_curation(curated: Curated, candidates_total: int, session_4_templates: set[str]) -> str:
    items = curated.items
    dives = len(items) // DIVE_SIZE
    kinds = Counter(i.answer_type for i in items)
    diffs = Counter(i.difficulty for i in items)
    by_family: dict[str, list] = {}
    for i in items:
        by_family.setdefault(i.template, []).append(i)
    star = sum(1 for i in items if i.answer_type == "player" and not i.broad)
    L = ["# Curation report", "",
         "Written by `python3 pipeline/export.py`; do not edit by hand. Layout of the files is in docs/export-format.md; tiers and points in docs/rarity-report.md.", "",
         f"- **{len(items)} prompts** in {dives} dives of {DIVE_SIZE}, chosen from {candidates_total:,} candidates ({kinds['player']} player: {kinds['player'] - star} broad-pool and {star} star-style; {kinds['team']} team).",
         f"- By difficulty: easy {diffs['easy']}, medium {diffs['medium']}, hard {diffs['hard']}.",
         f"- {len(by_family)} template families. Each parameter set (franchise, season, month, star) is used once, and a family never appears twice with only the threshold changed.", ""]
    L += ["## Prompts by template family", ""]
    L += _table(["family", "answers", "kind", "prompts"], [[f"`{k}`", v[0].answer_type, "broad" if v[0].broad else "-", len(v)] for k, v in sorted(by_family.items(), key=lambda kv: (-len(kv[1]), kv[0]))]) + [""]
    L += ["## The dives", "", "e, m, h = easy, medium, hard. Slots 3 and 5 are the team prompts. Counts in brackets are valid answers.", ""]
    rows = []
    for d in range(dives):
        dive = curated.dive(d)
        rows.append([d + 1, "".join(i.difficulty[0] for i in dive)] + [f"{i.template}{'' if not i.param and i.n is None else ' ' + '/'.join(str(x) for x in (i.param or (i.n,)))} ({len(i.prompt['answers'])})" for i in dive])
    L += _table(["dive", "e/m/h", "1", "2", "3 (team)", "4", "5 (team)", "6", "7"], rows) + [""]
    return "\n".join(L).rstrip() + "\n"


def write_reports(curated: Curated, checks: list[Check], sizes, largest, candidates_total: int, docs_dir: Path, baseline: dict, session_4_templates: set[str], recalibrated: str = "") -> None:
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "prompts-sample.md").write_text(render_sample(curated, checks, sizes, largest))
    (docs_dir / "curation-report.md").write_text(render_curation(curated, candidates_total, session_4_templates))
    (docs_dir / "rarity-report.md").write_text(render_rarity(curated, baseline, recalibrated))
