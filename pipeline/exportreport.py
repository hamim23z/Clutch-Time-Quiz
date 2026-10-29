"""Reports written by the export command: docs/prompts-sample.md and docs/curation-report.md."""
from __future__ import annotations

import random
from collections import Counter
from pathlib import Path

from curate import DIVE_SIZE, DIVES, Curated
from verify import Check

SAMPLE_SEED = 2026
SAMPLE_SIZE = 20
# the templates that existed after session 4; everything else was added to reach 63 prompts
SESSION_4_TEMPLATES = {
    "points-regular", "points-playoff", "points-finals", "triple-double-regular", "triple-double-playoff",
    "triple-double-finals", "rebounds", "assists", "threes", "blocks", "steals", "ppg-season", "franchises",
    "wins-season", "wins-playoff", "points-regulation", "win-margin",
}


def _table(headers: list[str], rows: list[list[object]]) -> list[str]:
    return ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"] + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]


def _names(answers: list[dict]) -> str:
    return ", ".join(f"{a['name']} ({a['tier']})" for a in answers)


def render_sample(curated: Curated, checks: list[Check], sizes: dict[str, tuple[int, int]]) -> str:
    L = ["# Prompts sample and checks", "",
         "Written by `python3 pipeline/export.py`; do not edit by hand. Tiers are in brackets: 1 is the best-known answer (10 points), 6 the rarest (100 points).", ""]
    L += ["## File sizes", ""]
    L += _table(["file", "bytes", "gzipped (what a static host sends)"], [[name, f"{raw:,}", f"{gz:,}"] for name, (raw, gz) in sizes.items()]) + [""]
    ok = sum(c.ok for c in checks)
    L += [f"## Recheck of {len(checks)} random prompts against the processed tables", "",
          f"{ok} of {len(checks)} match. Each prompt's valid answers were recomputed from the raw rows by a separately written brute-force query "
          "(`pipeline/bruteforce.py`) and compared with the exported answers, and the tiers and points were rechecked.", ""]
    L += _table(["prompt", "valid answers (brute force)", "exported answers", "missing", "extra", "tier problems", "result"],
                [[c.prompt_id, c.expected, c.exported, len(c.missing), len(c.extra), len(c.tier_problems), "ok" if c.ok else "**MISMATCH**"] for c in checks]) + [""]
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


def render_curation(curated: Curated, candidates_total: int) -> str:
    items = curated.items
    kinds = Counter(i.answer_type for i in items)
    diffs = Counter(i.difficulty for i in items)
    by_family: dict[str, list] = {}
    for i in items:
        by_family.setdefault(i.template, []).append(i)
    added = sorted(k for k in by_family if k not in SESSION_4_TEMPLATES)
    L = ["# Curation report", "",
         "Written by `python3 pipeline/export.py`; do not edit by hand. Layout of the files is in docs/export-format.md.", "",
         f"- **{len(items)} prompts** in {DIVES} dives of {DIVE_SIZE}, chosen from {candidates_total} candidates ({kinds['player']} player, {kinds['team']} team).",
         f"- By difficulty: easy {diffs['easy']}, medium {diffs['medium']}, hard {diffs['hard']}.",
         f"- {len(by_family)} template families; at most 2 thresholds from any family"
         + (f" (exceptions: {', '.join(curated.extended)})." if curated.extended else "; no family needed more than 2."),
         f"- Templates added in session 5 because the session 4 set (17 templates) gave too few families for 63 prompts: {len(added)} of the {len(by_family)} in use ({', '.join(added)}).", ""]
    L += ["## Prompts by template", ""]
    L += _table(["template", "answers", "prompts", "thresholds", "session"],
                [[k, v[0].answer_type, len(v), ", ".join("-" if i.n is None else str(i.n) for i in v), "4" if k in SESSION_4_TEMPLATES else "5"] for k, v in sorted(by_family.items())]) + [""]
    L += ["## The dives", "", "e, m, h = easy, medium, hard. Slots 3 and 5 are the team prompts.", ""]
    rows = []
    for d in range(DIVES):
        dive = curated.dive(d)
        rows.append([d + 1, "".join(i.difficulty[0] for i in dive)] + [f"{i.template}{'' if i.n is None else ' ' + str(i.n)} ({len(i.prompt['answers'])})" for i in dive])
    L += _table(["dive", "e/m/h", "1", "2", "3 (team)", "4", "5 (team)", "6", "7"], rows) + [""]
    return "\n".join(L).rstrip() + "\n"


def write_reports(curated: Curated, checks: list[Check], sizes, candidates_total: int, docs_dir: Path) -> None:
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "prompts-sample.md").write_text(render_sample(curated, checks, sizes))
    (docs_dir / "curation-report.md").write_text(render_curation(curated, candidates_total))
