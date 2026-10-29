"""docs/rarity-report.md: how rare the valid answers are, before (the session 5 export) and after (this export)."""
from __future__ import annotations

import json
import random
from collections import Counter
from pathlib import Path

from curate import DIVE_SIZE, TARGET_TIER12, TARGET_TIER56, Curated
from tiers import TIER_POINTS

BASELINE_PATH = Path(__file__).resolve().parent / "data" / "rarity-baseline.json"
SAMPLE_DIVES = 5
SAMPLE_SEED = 2026


def tier_stats(prompts: list[dict]) -> dict:
    counts = Counter(a["tier"] for p in prompts for a in p["answers"])
    answers = sum(counts.values())
    points = sum(a["points"] for p in prompts for a in p["answers"])
    return {"prompts": len(prompts), "answers": answers, "tier_counts": {t: counts.get(t, 0) for t in range(1, 7)}, "total_points": points}


def targets_met(stats: dict) -> tuple[bool, bool]:
    n = stats["answers"]
    c = stats["tier_counts"]
    return (c[1] + c[2]) / n <= TARGET_TIER12, (c[5] + c[6]) / n >= TARGET_TIER56


def load_baseline(path: Path = BASELINE_PATH) -> dict:
    raw = json.loads(path.read_text())
    return {"prompts": raw["prompts"], "answers": raw["answers"], "tier_counts": {int(t): c for t, c in raw["tier_counts"].items()}, "total_points": raw["total_points"], "source": raw["source"]}


def _row(label: str, s: dict) -> list[object]:
    n = s["answers"]
    c = s["tier_counts"]
    return [label, f"{n:,}"] + [f"{c[t]:,} ({100 * c[t] / n:.1f}%)" for t in range(1, 7)] + [f"{100 * (c[1] + c[2]) / n:.1f}%", f"{100 * (c[5] + c[6]) / n:.1f}%"]


def _table(headers: list[str], rows: list[list[object]]) -> list[str]:
    return ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"] + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]


def sample_dives(curated: Curated, k: int = SAMPLE_DIVES, seed: int = SAMPLE_SEED) -> list[int]:
    return sorted(random.Random(seed).sample(range(len(curated.items) // DIVE_SIZE), k))


def dive_extremes(prompts: list[dict]) -> tuple[int, int]:
    """Points for one dive if every prompt is answered with its best-known valid answer, and with its rarest."""
    return sum(p["answers"][0]["points"] for p in prompts), sum(p["answers"][-1]["points"] for p in prompts)


def render(curated: Curated, baseline: dict, recalibrated: str = "") -> str:
    prompts = curated.prompts
    after = tier_stats(prompts)
    ok12, ok56 = targets_met(after)
    L = ["# Rarity report", "",
         "Written by `python3 pipeline/export.py`; do not edit by hand. Tiers are the fame tiers of docs/fame-report.md: tier 1 is the best-known answer (10 points), tier 6 the rarest (100 points).", ""]
    L += ["## Tier distribution of all valid answers", "",
          f"Before is the session 5 export ({baseline['source']}); after is this export. Every valid answer of every prompt is counted once per prompt.", ""]
    L += _table(["", "answers", "tier 1", "tier 2", "tier 3", "tier 4", "tier 5", "tier 6", "tiers 1-2", "tiers 5-6"], [_row("before", baseline), _row("after", after)]) + [""]
    L += [f"- Target: tiers 1 and 2 together at most {100 * TARGET_TIER12:.0f}% of valid answers: **{'met' if ok12 else 'NOT met'}** ({100 * (after['tier_counts'][1] + after['tier_counts'][2]) / after['answers']:.1f}%).",
          f"- Target: tiers 5 and 6 together at least {100 * TARGET_TIER56:.0f}%: **{'met' if ok56 else 'NOT met'}** ({100 * (after['tier_counts'][5] + after['tier_counts'][6]) / after['answers']:.1f}%).",
          f"- Tier recalibration: {recalibrated or 'not needed; the tiers are the global fame tiers of docs/fame-report.md, unchanged.'}", ""]
    L += ["## Points", ""]
    L += _table(["", "prompts", "valid answers", "average points of a random valid answer", "average points per prompt (sum of its answers' points)", "average valid answers per prompt"],
                [[name, f"{s['prompts']:,}", f"{s['answers']:,}", f"{s['total_points'] / s['answers']:.1f}", f"{s['total_points'] / s['prompts']:,.0f}", f"{s['answers'] / s['prompts']:.0f}"]
                 for name, s in (("before", baseline), ("after", after))]) + [""]
    L += ["The fourth column is what the whole answer list of a prompt is worth added up; a player scores one answer per prompt, so what a player earns is in the next section.", ""]

    L += ["## Best-known versus rarest answer, five sample dives", "",
          "For each dive: the points if the player types the single best-known valid answer on every one of the 7 prompts, against the single rarest valid answer on every prompt (the maximum for that choice of answers).", ""]
    rows = []
    for d in sample_dives(curated):
        famous, rarest = dive_extremes([i.prompt for i in curated.dive(d)])
        rows.append([d + 1, famous, rarest, f"{rarest / famous:.1f}x"])
    L += _table(["dive", "best-known answer on every prompt", "rarest answer on every prompt", "ratio"], rows) + [""]
    allf = [dive_extremes([i.prompt for i in curated.dive(d)]) for d in range(len(prompts) // DIVE_SIZE)]
    L += [f"Over all {len(allf)} dives the best-known strategy averages {sum(f for f, _ in allf) / len(allf):.0f} points a dive and the rarest {sum(r for _, r in allf) / len(allf):.0f}; "
          f"the most a dive can pay is 700 (every answer worth 100).", ""]

    L += ["## Prompts per template family", ""]
    fam = Counter(i.template for i in curated.items)
    kinds = {i.template: ("team" if i.answer_type == "team" else "broad player" if i.broad else "star-style player") for i in curated.items}
    L += _table(["family", "kind", "prompts", "share"], [[f"`{k}`", kinds[k], c, f"{100 * c / len(prompts):.1f}%"] for k, c in sorted(fam.items(), key=lambda kv: (-kv[1], kv[0]))]) + [""]
    by_kind = Counter(kinds[i.template] for i in curated.items)
    L += ["By kind: " + ", ".join(f"{k} {v}" for k, v in sorted(by_kind.items())) + f". {len(fam)} families in all.", ""]

    L += ["## Tiers by family kind", ""]
    rows = []
    for kind in ("broad player", "star-style player", "team"):
        sub = [i.prompt for i in curated.items if kinds[i.template] == kind]
        if sub:
            rows.append(_row(kind, tier_stats(sub)))
    L += _table(["", "answers", "tier 1", "tier 2", "tier 3", "tier 4", "tier 5", "tier 6", "tiers 1-2", "tiers 5-6"], rows) + [""]
    return "\n".join(L).rstrip() + "\n"
