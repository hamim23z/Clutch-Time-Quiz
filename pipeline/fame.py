"""Fame score: how well known a player is, from five things in the data.

  1. career points (regular season plus playoffs),
  2. career rebounds,
  3. career assists,
  4. career steals plus blocks, and
  5. best single-season points per game, over regular-season seasons with at least 40 games.

Each metric is turned into a rank across ALL players in the data (rank 1 = most famous; ties share the better
rank). A player's fame rank is the best (lowest) of the five ranks, so a short-career star, a rebounder or a
defender is not rated obscure just because his career points are low. The percentile is the rank divided by the
number of players, and the tier comes from that percentile (see tiers.py).

Players with no season of 40 games have no points-per-game rank, and a career total of zero rebounds, assists or
steals plus blocks is not ranked. All ranks use the same population (all players),
so the percentiles are on the same scale.

Only games in the data count (2001-02 on), so a player whose career began earlier is judged on his later years only.
For players the metrics get clearly wrong, `pipeline/data/fame_overrides.csv` sets the tier by hand (one line of
reason each); the override changes the tier and points only, the percentile still shows what the metrics said.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from tiers import points_for_tier, tier_for_rank

MIN_SEASON_GAMES = 40
SEASON_TYPE_FOR_PPG = "regular"
OVERRIDES_PATH = Path(__file__).resolve().parent / "data" / "fame_overrides.csv"
OVERRIDE_COLUMNS = ["athlete_id", "tier", "reason"]

# (rank column, label shown in reports). Order matters: a tie between metrics goes to the first one listed.
METRICS: list[tuple[str, str]] = [
    ("points_rank", "career points"), ("reb_rank", "career rebounds"), ("ast_rank", "career assists"),
    ("stocks_rank", "career steals + blocks"), ("ppg_rank", "best points per game"),
]
RANK_COLUMNS = [m for m, _ in METRICS]

FAME_COLUMNS = [
    "player_id", "name", "career_points", "career_reb", "career_ast", "career_stocks",
    "best_ppg", "best_ppg_season", "best_ppg_games",
    "points_rank", "reb_rank", "ast_rank", "stocks_rank", "ppg_rank",
    "fame_rank", "fame_pct", "fame_source", "override_reason", "tier", "points",
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


def load_overrides(path: Path = OVERRIDES_PATH) -> pd.DataFrame:
    """The hand-set tiers: athlete_id, tier, reason. A missing file means no overrides."""
    if not path.exists():
        return pd.DataFrame(columns=OVERRIDE_COLUMNS).astype({"athlete_id": "int64", "tier": "int64"})
    df = pd.read_csv(path, dtype={"athlete_id": "int64", "tier": "int64", "reason": "string"})
    if list(df.columns) != OVERRIDE_COLUMNS:
        raise ValueError(f"{path.name} must have the columns {OVERRIDE_COLUMNS}")
    if df["athlete_id"].duplicated().any():
        raise ValueError(f"{path.name} lists an athlete twice")
    if not df["tier"].between(1, 6).all():
        raise ValueError(f"{path.name} has a tier outside 1 to 6")
    if df["reason"].isna().any() or (df["reason"].str.strip() == "").any():
        raise ValueError(f"{path.name} has an override without a reason")
    return df


def compute_fame(
    player_games: pd.DataFrame, players: pd.DataFrame, min_games: int = MIN_SEASON_GAMES,
    overrides: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """The fame table: one row per player with at least one game with a points value."""
    pg = player_games.assign(stocks=player_games["stl"].fillna(0) + player_games["blk"].fillna(0))
    sums = pg.groupby("player_id")[["points", "reb", "ast", "stocks"]].sum().astype("int64")
    fame = sums.rename(columns={"points": "career_points", "reb": "career_reb", "ast": "career_ast", "stocks": "career_stocks"}).reset_index()
    n = len(fame)
    fame = fame.merge(best_seasons(player_games, min_games), on="player_id", how="left")
    for rank_col, source in (("points_rank", "career_points"), ("reb_rank", "career_reb"), ("ast_rank", "career_ast"),
                             ("stocks_rank", "career_stocks"), ("ppg_rank", "best_ppg")):
        values = fame[source]
        if rank_col in ("reb_rank", "ast_rank", "stocks_rank"):
            values = values.where(values > 0)  # a total of zero is not a claim to fame; points always rank, so a rank always exists
        fame[rank_col] = values.rank(method="min", ascending=False)
    # the best (lowest) of the ranks; a missing rank (no 40-game season, or a total of zero) is skipped
    fame["fame_rank"] = fame[RANK_COLUMNS].min(axis=1).astype("int64")
    fame["fame_pct"] = fame["fame_rank"] * 100 / n
    labels = dict(METRICS)
    fame["fame_source"] = fame[RANK_COLUMNS].idxmin(axis=1).map(labels)
    fame["tier"] = [tier_for_rank(int(r), n) for r in fame["fame_rank"]]
    fame["override_reason"] = ""
    overrides = load_overrides() if overrides is None else overrides
    unknown = set(overrides["athlete_id"]) - set(fame["player_id"])
    if unknown:
        raise ValueError(f"fame overrides name athletes who are not in the data: {sorted(unknown)}")
    for o in overrides.itertuples():
        row = fame["player_id"] == o.athlete_id
        fame.loc[row, "tier"] = int(o.tier)
        fame.loc[row, "override_reason"] = str(o.reason)
    fame["points"] = fame["tier"].map(points_for_tier)
    names = players.set_index("player_id")["unique_name"]
    fame["name"] = fame["player_id"].map(names)
    if fame["name"].isna().any():
        raise ValueError("some players in player_games are missing from the players table")
    fame = fame.sort_values(["fame_rank", "career_points", "name"], ascending=[True, False, True]).reset_index(drop=True)
    return fame[FAME_COLUMNS]
