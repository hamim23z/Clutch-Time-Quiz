"""Normalize stage: raw season play-by-play -> compact events for the last 3 minutes.

Keeps the final WINDOW_SECONDS of the 4th quarter and of every overtime period. Possession
is inferred from LEAD_IN_SECONDS before the window, so the first events in the window
already know who has the ball.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from columns import standardize
from events import classify_event, is_three_attempt
from ordering import sort_and_repair
from possession import AWAY, CERTAIN, HOME, LOOSE, UNKNOWN, infer_possession

WINDOW_SECONDS = 180
LEAD_IN_SECONDS = 120
FIRST_CLUTCH_PERIOD = 4  # 4th quarter; 5 and up are overtimes

EVENT_COLUMNS = [
    "game_id",
    "season",
    "quarter",
    "seq",
    "play_id",
    "secs_period",
    "secs_game",
    "margin",
    "possession",
    "possession_status",
    "event_type",
    "is_three",
    "acting_side",
    "home_score",
    "away_score",
    "detail",
]
GAME_COLUMNS = [
    "game_id",
    "season",
    "season_type",
    "game_date",
    "home_team",
    "away_team",
    "home_abbrev",
    "away_abbrev",
    "final_home_score",
    "final_away_score",
    "periods",
]


@dataclass
class Normalized:
    events: pd.DataFrame
    games: pd.DataFrame
    stats: dict[str, int]


def _acting_side(df: pd.DataFrame) -> np.ndarray:
    team = df["team_id"]
    return np.select(
        [team == df["home_team_id"], team == df["away_team_id"]],
        [HOME, AWAY],
        default="",
    )


def build_games(df: pd.DataFrame) -> pd.DataFrame:
    """One row per game: teams, date and the final score (from the last play of the game)."""
    ordered = df.sort_values(["game_id", "period", "play_order"], kind="stable")
    last = ordered.groupby("game_id").tail(1).set_index("game_id")
    first = ordered.groupby("game_id").head(1).set_index("game_id")
    games = pd.DataFrame(
        {
            "season": first["season"],
            "season_type": first["season_type"],
            "game_date": first["game_date"],
            "home_team": (first["home_team_name"].fillna("") + " " + first["home_team_mascot"].fillna("")).str.strip(),
            "away_team": (first["away_team_name"].fillna("") + " " + first["away_team_mascot"].fillna("")).str.strip(),
            "home_abbrev": first["home_team_abbrev"],
            "away_abbrev": first["away_team_abbrev"],
            "final_home_score": last["home_score"],
            "final_away_score": last["away_score"],
            "periods": ordered.groupby("game_id")["period"].max(),
        }
    )
    return games.reset_index()[GAME_COLUMNS]


def normalize_season(raw: pd.DataFrame) -> Normalized:
    df = standardize(raw)
    games = build_games(df)

    missing_clock = df["secs_game"].isna() | df["secs_period"].isna()
    df = df[~missing_clock]
    df = df[(df["period"] >= FIRST_CLUTCH_PERIOD) & (df["secs_period"] <= WINDOW_SECONDS + LEAD_IN_SECONDS)].copy()
    df["event_type"] = [
        classify_event(t, s, sc) for t, s, sc in zip(df["type_text"], df["shooting_play"], df["scoring_play"])
    ]
    df, reordered = sort_and_repair(df)
    # Scores only go up, so the running maximum is the true score at every row. This matters
    # for rows the tie-break moved (a substitution listed after the free throws it was
    # recorded before still carries the older score).
    for col in ("home_score", "away_score"):
        df[col] = df.groupby("game_id")[col].cummax()

    df["side"] = _acting_side(df)
    df["side"] = df["side"].replace("", None)
    teams, statuses = infer_possession(df)
    df["possession"] = teams
    df["possession_status"] = statuses

    df = df[df["secs_period"] <= WINDOW_SECONDS].reset_index(drop=True)
    home, away = df["home_score"], df["away_score"]
    ball_home = df["possession"] == HOME
    ball_away = df["possession"] == AWAY
    margin = pd.Series(pd.NA, index=df.index, dtype="Int16")
    margin[ball_home] = (home - away)[ball_home].astype("Int16")
    margin[ball_away] = (away - home)[ball_away].astype("Int16")

    df["is_three"] = [is_three_attempt(t, e) for t, e in zip(df["text"], df["event_type"])]
    events = pd.DataFrame(
        {
            "game_id": df["game_id"].astype("int64"),
            "season": df["season"].astype("int16"),
            "quarter": df["period"].astype("int8"),
            "seq": df.groupby("game_id").cumcount().astype("int16"),
            "play_id": df["play_order"].astype("int32"),
            "secs_period": df["secs_period"].astype("float64"),
            "secs_game": df["secs_game"].astype("float64"),
            "margin": margin,
            "possession": df["possession"].astype("category"),
            "possession_status": pd.Categorical(df["possession_status"], categories=[CERTAIN, LOOSE, UNKNOWN]),
            "event_type": df["event_type"].astype("category"),
            "is_three": df["is_three"],
            "acting_side": df["side"].astype("category"),
            "home_score": home.astype("int16"),
            "away_score": away.astype("int16"),
            "detail": df["type_text"].astype("category"),
        }
    )[EVENT_COLUMNS]

    games = games[games["game_id"].isin(events["game_id"].unique())].reset_index(drop=True)
    counts = events["possession_status"].value_counts()
    stats = {
        "games": int(len(games)),
        "events": int(len(events)),
        "certain": int(counts.get(CERTAIN, 0)),
        "loose": int(counts.get(LOOSE, 0)),
        "unknown": int(counts.get(UNKNOWN, 0)),
        "reordered_rows": int(reordered),
        "dropped_no_clock": int(missing_clock.sum()),
    }
    return Normalized(events, games, stats)
