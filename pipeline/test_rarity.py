import json

import pytest

import curate as cu
import rarity
from rarity import dive_extremes, load_baseline, render, sample_dives, targets_met, tier_stats
from test_curate import CFG, default, make_pool


def prompt(tiers):
    return {"id": "p", "answers": [{"id": f"pl-{i}", "name": "x", "tier": t, "points": {1: 10, 2: 20, 3: 35, 4: 55, 5: 75, 6: 100}[t]} for i, t in enumerate(tiers)]}


def test_tier_stats_counts_every_answer_once_per_prompt():
    s = tier_stats([prompt([1, 1, 2]), prompt([6, 5])])
    assert s["prompts"] == 2 and s["answers"] == 5 and s["tier_counts"] == {1: 2, 2: 1, 3: 0, 4: 0, 5: 1, 6: 1}
    assert s["total_points"] == 10 + 10 + 20 + 100 + 75


def test_targets_are_tiers_1_2_at_most_45_percent_and_5_6_at_least_12_percent():
    def stats(c12, c56, n=100):
        return {"answers": n, "tier_counts": {1: c12, 2: 0, 3: n - c12 - c56, 4: 0, 5: c56, 6: 0}}
    assert targets_met(stats(45, 12)) == (True, True)
    assert targets_met(stats(46, 12)) == (False, True)
    assert targets_met(stats(45, 11)) == (True, False)


def test_baseline_is_the_session_5_export():
    b = load_baseline()
    assert b["prompts"] == 63 and b["answers"] == sum(b["tier_counts"].values()) == 4672
    assert b["tier_counts"][5] + b["tier_counts"][6] == 24


def test_best_known_and_rarest_answer_points():
    assert dive_extremes([prompt([1, 3, 6]), prompt([2, 4])]) == (10 + 20, 100 + 55)


def test_sample_dives_are_five_distinct_dives_in_order():
    result, cfg = default()
    picked = sample_dives(result)
    assert len(picked) == 5 and picked == sorted(set(picked)) and all(0 <= d < cfg.dives for d in picked)


def test_report_has_the_required_sections():
    result, _ = default()
    text = render(result, load_baseline())
    for heading in ("## Tier distribution of all valid answers", "## Points", "## Best-known versus rarest answer, five sample dives", "## Prompts per template family"):
        assert heading in text
    assert "before" in text and "after" in text and "Tier recalibration: not needed" in text
    assert render(result, load_baseline(), "tiers recomputed over exported players").count("tiers recomputed over exported players") == 1
