"""Fame score: how well known a player is, from two things in the data.

  1. career points (regular season plus playoffs), and
  2. best single-season points per game, over regular-season seasons with at least 40 games.

Each metric is turned into a rank across ALL players in the data (rank 1 = most famous). A player's fame rank is the
better (lower) of the two ranks, so a short-career star is not rated obscure just because his career total is small.
The percentile is the rank divided by the number of players, and the tier comes from that percentile (see tiers.py).

Players with no season of 40 games have no points-per-game rank; they are ranked by career points alone, and for
the percentile they count as ranked below every player who has one. Both ranks use the same population (all players),
so the two percentiles are on the same scale.

Only games in the data count (2001-02 on), so a player whose career began earlier is judged on his later years only.
"""
from __future__ import annotations

import pandas as pd

from tiers import points_for_tier, tier_for_rank

MIN_SEASON_GAMES = 40
SEASON_TYPE_FOR_PPG = "regular"

FAME_COLUMNS = [
    "player_id", "name", "career_points", "career_rank", "career_pct", "best_ppg", "best_ppg_season",
    "best_ppg_games", "ppg_rank", "ppg_pct", "fame_rank", "fame_pct", "fame_source", "tier", "points",
]


def best_seasons(player_games: pd.DataFrame, min_games: int = MIN_SEASON_GAMES) -> pd.DataFrame:
    """Each player's best regular-season points per game over seasons with at least min_games games.

    Returns player_id, best_ppg, best_ppg_season, best_ppg_games. A player traded during the season has his
    games for all teams added up. Ties between seasons go to the later season.
    """
    reg = player_games[player_games["season_type"] == SEASON_TYPE_FOR_PPG]
    seasons = reg.groupby(["player_id", "season"]).agg(games=("game_id", "size"), pts=("points", "sum")).reset_index()
    seasons = seasons[seasons["games"] >= min_games].copy()
    seasons["pts"] = seasons["pts"].astype("int64")
    seasons["ppg"] = seasons["pts"] / seasons["games"]
    seasons = seasons.sort_values(["player_id", "ppg", "season"], ascending=[True, False, False])
    best = seasons.drop_duplicates("player_id")
    return best.rename(columns={"ppg": "best_ppg", "season": "best_ppg_season", "games": "best_ppg_games"})[
        ["player_id", "best_ppg", "best_ppg_season", "best_ppg_games"]
    ]


def compute_fame(player_games: pd.DataFrame, players: pd.DataFrame, min_games: int = MIN_SEASON_GAMES) -> pd.DataFrame:
    """The fame table: one row per player with at least one game with a points value."""
    career = player_games.groupby("player_id")["points"].sum().astype("int64").rename("career_points").reset_index()
    n = len(career)
    career["career_rank"] = career["career_points"].rank(method="min", ascending=False).astype("int64")
    fame = career.merge(best_seasons(player_games, min_games), on="player_id", how="left")
    fame["ppg_rank"] = fame["best_ppg"].rank(method="min", ascending=False)
    fame["career_pct"] = fame["career_rank"] * 100 / n
    fame["ppg_pct"] = fame["ppg_rank"] * 100 / n
    # the better (lower) rank of the two; a player with no ppg rank has only the career rank
    fame["fame_rank"] = fame[["career_rank", "ppg_rank"]].min(axis=1).astype("int64")
    fame["fame_pct"] = fame["fame_rank"] * 100 / n
    fame["fame_source"] = ["ppg" if (not pd.isna(p) and p < c) else "career" for c, p in zip(fame["career_rank"], fame["ppg_rank"])]
    fame["tier"] = [tier_for_rank(int(r), n) for r in fame["fame_rank"]]
    fame["points"] = fame["tier"].map(points_for_tier)
    names = players.set_index("player_id")["unique_name"]
    fame["name"] = fame["player_id"].map(names)
    if fame["name"].isna().any():
        raise ValueError("some players in player_games are missing from the players table")
    fame = fame.sort_values(["fame_rank", "career_points", "name"], ascending=[True, False, True]).reset_index(drop=True)
    return fame[FAME_COLUMNS]
