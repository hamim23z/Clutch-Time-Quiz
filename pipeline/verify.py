"""Recheck exported prompts against the processed tables with the independent brute-force queries (bruteforce.py).

For a random sample of prompts it recomputes the valid answers from the raw rows and compares the answer ids with
the prompt's, then rechecks the tiers (players against the fame table; teams with a separately written current-name
rule) and the points. Nothing here calls the template qualifiers or the generator.
"""
from __future__ import annotations

import random
from dataclasses import dataclass

import pandas as pd

from bruteforce import BRUTE, BRUTE_FAMILY, Rows
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


def check_prompt(prompt: dict, template: str, n: int | None, rows: Rows, fame: pd.DataFrame, teams: pd.DataFrame, param: tuple = ()) -> Check:
    found = BRUTE_FAMILY[template](rows, tuple(param)) if template in BRUTE_FAMILY else BRUTE[template](rows, n or 0)
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


def pick_sample(items, k: int = 60, per_family: int = 2, seed: int = 2026) -> list:
    """At least `per_family` prompts from every template family (all of them if it has fewer), then random ones up to k."""
    rng = random.Random(seed)
    by_family: dict[str, list] = {}
    for i in items:
        by_family.setdefault(i.template, []).append(i)
    chosen = []
    for key in sorted(by_family):
        chosen += rng.sample(by_family[key], min(per_family, len(by_family[key])))
    rest = [i for i in items if i not in chosen]
    rng.shuffle(rest)
    return chosen + rest[:max(0, k - len(chosen))]


def verify_sample(items, tables, fame: pd.DataFrame, k: int = 60, per_family: int = 2, seed: int = 2026) -> list[Check]:
    """Check a sample of curated items (curate.Item): k prompts, at least per_family from every template family."""
    rows = Rows(tables)
    return [check_prompt(i.prompt, i.template, i.n, rows, fame, tables.teams, i.param) for i in pick_sample(list(items), k, per_family, seed)]
