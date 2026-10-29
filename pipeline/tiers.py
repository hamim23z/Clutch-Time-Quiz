"""Tiers: how obscure an answer is, from the global fame percentile.

Tier 1 is the most famous answer and is worth the fewest points; tier 6 is the deepest cut. The percentile is global
(rank among every player in the data), not within one prompt, so a superstar is low value in every prompt.
"""
from __future__ import annotations

import pandas as pd

# (upper bound of the fame percentile in percent, tier). A percentile on the line belongs to the better-known tier.
CUTOFFS: tuple[tuple[int, int], ...] = ((3, 1), (10, 2), (25, 3), (50, 4), (75, 5))
LAST_TIER = 6
TIER_POINTS: dict[int, int] = {1: 10, 2: 20, 3: 35, 4: 55, 5: 75, 6: 100}
TIER_LABELS: dict[int, str] = {
    1: "top 3%", 2: "3 to 10%", 3: "10 to 25%", 4: "25 to 50%", 5: "50 to 75%", 6: "bottom 25%",
}
DEEP_TIER = 4  # tier 4 and above (4, 5, 6) count as deep cuts

# Teams: a team is tier 1 when it qualified under its current name, and tier 4 when only under a historical name.
TEAM_TIER_CURRENT = 1
TEAM_TIER_HISTORICAL = 4


def tier_for_rank(rank: int, n: int) -> int:
    """Tier of a player with this fame rank (1 = most famous) among n players.

    Integer arithmetic, so a player exactly on a cutoff is never moved by floating point error: rank/n <= 3% is
    tier 1, <= 10% is tier 2, <= 25% tier 3, <= 50% tier 4, <= 75% tier 5, anything lower is tier 6.
    """
    if rank < 1 or n < 1 or rank > n:
        raise ValueError(f"rank {rank} is not between 1 and {n}")
    for percent, tier in CUTOFFS:
        if rank * 100 <= percent * n:
            return tier
    return LAST_TIER


def points_for_tier(tier: int) -> int:
    return TIER_POINTS[tier]


def team_tiers(instances: pd.DataFrame, teams: pd.DataFrame) -> dict[int, int]:
    """Tier of every franchise that qualified, from the (team_id, season) instances that qualified.

    A franchise is tier 1 if in any qualifying season it played under its current name, and tier 4 if it qualified
    only under historical names. `teams` is the teams table (current_name and the list of names with their seasons).
    """
    names_by_season: dict[int, dict[int, set[str]]] = {}
    current: dict[int, str] = {}
    for row in teams.itertuples():
        current[int(row.team_id)] = row.current_name
        per_season: dict[int, set[str]] = {}
        for entry in row.names:
            for season in entry["seasons"]:
                per_season.setdefault(int(season), set()).add(entry["name"])
        names_by_season[int(row.team_id)] = per_season
    tiers: dict[int, int] = {}
    for team_id, season in zip(instances["team_id"], instances["season"]):
        tid = int(team_id)
        under_current = current[tid] in names_by_season[tid].get(int(season), set())
        if under_current:
            tiers[tid] = TEAM_TIER_CURRENT
        else:
            tiers.setdefault(tid, TEAM_TIER_HISTORICAL)
    return tiers


def historical_names_used(instances: pd.DataFrame, teams: pd.DataFrame) -> dict[int, list[str]]:
    """For franchises that qualified, the historical (non-current) names they qualified under. Used by the reports."""
    out: dict[int, set[str]] = {}
    by_id = {int(r.team_id): r for r in teams.itertuples()}
    for team_id, season in zip(instances["team_id"], instances["season"]):
        row = by_id[int(team_id)]
        for entry in row.names:
            if int(season) in {int(s) for s in entry["seasons"]} and entry["name"] != row.current_name:
                out.setdefault(int(team_id), set()).add(entry["name"])
    return {k: sorted(v) for k, v in out.items()}
