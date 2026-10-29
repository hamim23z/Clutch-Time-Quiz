"""Recheck exported prompts against the processed tables with the independent brute-force queries (bruteforce.py).

For a random sample of prompts it recomputes the valid answers from the raw rows and compares the answer ids with
the prompt's, then rechecks the tiers (players against the fame table; teams with a separately written current-name
rule) and the points. Nothing here calls the template qualifiers or the generator.
"""
from __future__ import annotations

import random
from dataclasses import dataclass

import pandas as pd

from bruteforce import BRUTE, Rows
from tiers import TIER_POINTS


@dataclass
class Check:
    prompt_id: str
    template: str
    expected: int
    exported: int
    missing: list[str]
    extra: list[str]
    tier_problems: list[str]

    @property
    def ok(self) -> bool:
        return not (self.missing or self.extra or self.tier_problems)


def _team_tier(teams: pd.DataFrame, team_id: int, seasons: set[int]) -> int:
    """1 if the franchise carried its current name in any of the seasons, else 4 (written without tiers.py)."""
    row = teams[teams["team_id"] == team_id].iloc[0]
    for entry in row["names"]:
        if entry["name"] == row["current_name"] and seasons & {int(s) for s in entry["seasons"]}:
            return 1
    return 4


def check_prompt(prompt: dict, template: str, n: int | None, rows: Rows, fame: pd.DataFrame, teams: pd.DataFrame) -> Check:
    found = BRUTE[template](rows, n or 0)
    exported = {a["id"]: a for a in prompt["answers"]}
    problems: list[str] = []
    if prompt["answerType"] == "player":
        want = {f"pl-{pid}" for pid in found}
        by_id = fame.set_index("player_id")
        for a in prompt["answers"]:
            tier = int(by_id.loc[int(a["id"][3:]), "tier"]) if a["id"][3:].isdigit() and int(a["id"][3:]) in by_id.index else None
            if tier != a["tier"] or TIER_POINTS.get(a["tier"]) != a["points"]:
                problems.append(f"{a['id']}: tier {a['tier']}/{a['points']} points, fame table says tier {tier}")
    else:
        seasons: dict[int, set[int]] = {}
        for team, season in found:
            seasons.setdefault(team, set()).add(season)
        want = {f"tm-{t}" for t in seasons}
        for t, s in seasons.items():
            a = exported.get(f"tm-{t}")
            if a and (a["tier"] != _team_tier(teams, t, s) or TIER_POINTS.get(a["tier"]) != a["points"]):
                problems.append(f"tm-{t}: tier {a['tier']}, expected {_team_tier(teams, t, s)}")
    return Check(prompt["id"], template, len(want), len(exported), sorted(want - set(exported)), sorted(set(exported) - want), problems)


def verify_sample(items, tables, fame: pd.DataFrame, k: int = 10, seed: int = 2026) -> list[Check]:
    """Check k randomly chosen curated items (curate.Item) against the tables."""
    rows = Rows(tables)
    sample = random.Random(seed).sample(list(items), min(k, len(items)))
    return [check_prompt(i.prompt, i.template, i.n, rows, fame, tables.teams) for i in sample]
