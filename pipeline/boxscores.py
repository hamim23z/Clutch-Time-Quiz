"""Box score stage: team_games and player_games for the kept games."""
from __future__ import annotations

import pandas as pd

from games import NBA_TEAM_IDS

TEAM_STATS = {
    "field_goals_made": "fgm", "field_goals_attempted": "fga",
    "three_point_field_goals_made": "fg3m", "three_point_field_goals_attempted": "fg3a",
    "free_throws_made": "ftm", "free_throws_attempted": "fta",
    "offensive_rebounds": "oreb", "defensive_rebounds": "dreb", "total_rebounds": "reb",
    "assists": "ast", "steals": "stl", "blocks": "blk", "turnovers": "tov", "fouls": "pf",
}
PLAYER_STATS = {
    "points": "points", "rebounds": "reb", "assists": "ast", "steals": "stl", "blocks": "blk",
    "turnovers": "tov", "fouls": "pf", "field_goals_made": "fgm", "field_goals_attempted": "fga",
    "three_point_field_goals_made": "fg3m", "three_point_field_goals_attempted": "fg3a",
    "free_throws_made": "ftm", "free_throws_attempted": "fta",
    "offensive_rebounds": "oreb", "defensive_rebounds": "dreb",
}
TEAM_GAME_COLUMNS = [
    "game_id", "season", "season_type", "team_id", "opponent_team_id", "home_away", "team_score", "opponent_score",
    "won", *TEAM_STATS.values(),
]
PLAYER_GAME_COLUMNS = [
    "game_id", "season", "season_type", "player_id", "team_id", "opponent_team_id", "home_away", "started",
    "minutes", *PLAYER_STATS.values(),
]


def build_team_games(team: pd.DataFrame, games: pd.DataFrame) -> pd.DataFrame:
    """One row per NBA team per kept game."""
    t = team[team["team_id"].isin(NBA_TEAM_IDS) & team["game_id"].isin(games["game_id"])].copy()
    t = t.merge(games[["game_id", "season_type"]], on="game_id")
    t = t.rename(columns={"team_home_away": "home_away", "opponent_team_score": "opponent_score", "team_winner": "won", **TEAM_STATS})
    for col in ("team_score", "opponent_score", *TEAM_STATS.values()):
        t[col] = t[col].astype("int16")
    t["won"] = t["won"].astype(bool)
    return t[TEAM_GAME_COLUMNS].sort_values(["game_id", "team_id"]).reset_index(drop=True)


def build_player_games(player: pd.DataFrame, games: pd.DataFrame) -> pd.DataFrame:
    """One row per player who played in a kept game.

    A player counts as having played only if the points value is present. The did_not_play flag is not
    used: it is almost never set in 2006-2012, and rows with no points are people who did not play.
    Stat lines with no athlete id are dropped.
    """
    p = player[player["points"].notna() & player["athlete_id"].notna() & player["game_id"].isin(games["game_id"])].copy()
    p = p.merge(games[["game_id", "season_type"]], on="game_id")
    p = p.rename(columns={"athlete_id": "player_id", "starter": "started", **PLAYER_STATS})
    p["player_id"] = p["player_id"].astype("int64")
    p["started"] = p["started"].fillna(False).astype(bool)
    p["minutes"] = p["minutes"].astype("float32")
    for col in PLAYER_STATS.values():
        p[col] = p[col].astype("Int16")
    p["team_id"] = p["team_id"].astype("int16")
    p["opponent_team_id"] = p["opponent_team_id"].astype("int16")
    return p[PLAYER_GAME_COLUMNS].sort_values(["game_id", "player_id"]).reset_index(drop=True)
