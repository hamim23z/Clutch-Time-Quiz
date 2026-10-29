"""Raw column names, in one place. Each table keeps only the columns the pipeline uses."""
from __future__ import annotations

import pandas as pd

SCHEDULE = [
    "game_id", "season", "season_type", "game_date", "type_abbreviation", "status_type_name",
    "status_period", "home_id", "away_id", "home_score", "away_score",
]
TEAM = [
    "game_id", "season", "team_id", "team_display_name", "team_location", "team_name", "team_abbreviation",
    "team_home_away", "team_score", "opponent_team_id", "opponent_team_score", "team_winner",
    "field_goals_made", "field_goals_attempted", "three_point_field_goals_made", "three_point_field_goals_attempted",
    "free_throws_made", "free_throws_attempted", "offensive_rebounds", "defensive_rebounds", "total_rebounds",
    "assists", "steals", "blocks", "turnovers", "fouls",
]
PLAYER = [
    "game_id", "season", "athlete_id", "athlete_display_name", "athlete_short_name", "team_id", "opponent_team_id",
    "home_away", "starter", "minutes", "points", "rebounds", "offensive_rebounds", "defensive_rebounds",
    "assists", "steals", "blocks", "turnovers", "fouls", "field_goals_made", "field_goals_attempted",
    "three_point_field_goals_made", "three_point_field_goals_attempted", "free_throws_made", "free_throws_attempted",
]
OFFICIALS = ["season", "game_id", "official_full_name", "official_order"]

COLUMNS = {"schedule": SCHEDULE, "team": TEAM, "player": PLAYER, "officials": OFFICIALS}


def slim(df: pd.DataFrame, table: str) -> pd.DataFrame:
    """Keep the columns of one raw table. Fails loudly if the release changed its column names."""
    missing = [c for c in COLUMNS[table] if c not in df.columns]
    if missing:
        raise KeyError(f"raw {table} table is missing columns: {', '.join(missing)}")
    return df[COLUMNS[table]].copy()
