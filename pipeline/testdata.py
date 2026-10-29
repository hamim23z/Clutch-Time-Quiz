"""Tiny raw-shaped tables for tests. Column names match the sportsdataverse releases."""
from __future__ import annotations

import numpy as np
import pandas as pd

from rawcols import OFFICIALS, PLAYER, SCHEDULE, TEAM

SCHED_DEFAULTS = {
    "season": 2024, "season_type": 2, "game_date": "2024-01-01", "type_abbreviation": "STD",
    "status_type_name": "STATUS_FINAL", "status_period": 4, "home_id": 2, "away_id": 6, "home_score": 100, "away_score": 90,
}


def schedule(*games: dict) -> pd.DataFrame:
    """One row per dict; game_id is required, everything else defaults to a regular-season final."""
    return pd.DataFrame([{**SCHED_DEFAULTS, **g} for g in games])[SCHEDULE]


def team_box(game_id: int, season: int = 2024, home: int = 2, away: int = 6, home_score: int = 100, away_score: int = 90,
             home_name: str = "Boston Celtics", away_name: str = "Dallas Mavericks") -> pd.DataFrame:
    def row(tid, side, score, opp, opp_score, name):
        stats = dict.fromkeys(TEAM[12:], 10)  # every count column after team_winner
        return {
            "game_id": game_id, "season": season, "team_id": tid, "team_display_name": name, "team_location": name.rsplit(" ", 1)[0],
            "team_name": name.rsplit(" ", 1)[-1], "team_abbreviation": name[:3].upper(), "team_home_away": side,
            "team_score": score, "opponent_team_id": opp, "opponent_team_score": opp_score, "team_winner": score > opp_score, **stats,
        }
    return pd.DataFrame([row(home, "home", home_score, away, away_score, home_name), row(away, "away", away_score, home, home_score, away_name)])[TEAM]


def player_box(*rows: dict) -> pd.DataFrame:
    """Rows need game_id and athlete_id (None for an unknown athlete). points=None means no stats.

    The did_not_play flag is included on purpose and may disagree with points: the pipeline must ignore it.
    """
    out = []
    for r in rows:
        stats = dict.fromkeys(PLAYER[10:], 1.0)  # every stat column from points on
        base = {
            "game_id": 1, "season": 2024, "athlete_display_name": "Some Player", "athlete_short_name": "S. Player", "team_id": 2,
            "opponent_team_id": 6, "home_away": "home", "starter": False, "minutes": 20.0, "did_not_play": False, **stats,
        }
        row = {**base, **r}
        if row.get("points") is None:
            row.update({k: np.nan for k in PLAYER[9:]})  # no stats at all: minutes too
        out.append(row)
    return pd.DataFrame(out)[[*PLAYER, "did_not_play"]]


def officials_box(*rows: tuple[int, int, int, str]) -> pd.DataFrame:
    """Rows are (game_id, season, order, name)."""
    return pd.DataFrame([dict(zip(OFFICIALS, (season, gid, name, order))) for gid, season, order, name in rows])[OFFICIALS]


def kept_games(*game_ids: int) -> pd.DataFrame:
    """A minimal games table, for stages that only need to know which games are kept."""
    return pd.DataFrame({"game_id": list(game_ids)})
