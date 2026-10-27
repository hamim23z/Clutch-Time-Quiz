"""Session 1 data spike: load 3 close games and print their last 60 seconds.

Not part of the pipeline. Possession here is a rough inference for display only.

Usage (from repo root):
    python3 pipeline/spike/sample_games.py [path/to/play_by_play_2024.parquet]
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

DEFAULT_PATH = Path("data/raw/play_by_play_2024.parquet")

# team_id is the acting team: the offense for these events, the defense for fouls.
OFFENSE_EVENTS = ("Shot", "Layup", "Dunk", "Free Throw", "Turnover", "Offensive Rebound", "Tip")
DEFENSE_EVENTS = ("Foul", "Defensive Goaltending")


def pick_close_games(df: pd.DataFrame, k: int = 3) -> list[int]:
    """First k regular-season games (by game_id) decided by 3 points or fewer in regulation."""
    last = df.sort_values("game_play_number").groupby("game_id").tail(1)
    close = last[
        (last.season_type == 2)
        & ((last.home_score - last.away_score).abs() <= 3)
        & (last.period_number == 4)
    ]
    return sorted(close.game_id)[:k]


def team_with_ball(row: pd.Series) -> str:
    """Best-guess possession after the event, from type_text and team_id. 'home'/'away'/'?'."""
    if pd.isna(row.team_id):
        return "?"
    side = "home" if int(row.team_id) == row.home_team_id else "away"
    other = "away" if side == "home" else "home"
    t = row.type_text
    if t == "Defensive Rebound":
        return side
    if any(word in t for word in DEFENSE_EVENTS):
        return other
    if any(word in t for word in OFFENSE_EVENTS):
        # A made field goal (or a final made free throw) hands the ball to the other team.
        return other if row.scoring_play else side
    return side


def last_minute(df: pd.DataFrame, game_id: int) -> pd.DataFrame:
    g = df[df.game_id == game_id].sort_values("game_play_number")
    g = g[(g.period_number == 4) & (g.start_game_seconds_remaining <= 60)].copy()
    g["margin_home"] = g.home_score - g.away_score
    g["acting_team"] = g.apply(
        lambda r: "" if pd.isna(r.team_id) else (r.home_team_abbrev if int(r.team_id) == r.home_team_id else r.away_team_abbrev),
        axis=1,
    )
    g["possession_after"] = g.apply(team_with_ball, axis=1)
    g["event"] = g.type_text.str.replace("\n", " ")
    return g[["start_game_seconds_remaining", "margin_home", "acting_team", "possession_after", "event", "text"]].rename(
        columns={"start_game_seconds_remaining": "secs_left"}
    )


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PATH
    df = pd.read_parquet(path)
    pd.set_option("display.width", 200, "display.max_colwidth", 60, "display.max_rows", 200)
    for gid in pick_close_games(df):
        first = df[df.game_id == gid].iloc[0]
        print(f"\n=== game {gid}: {first.away_team_name} at {first.home_team_name}, {first.game_date} ===")
        print("margin_home = home score minus away score; possession_after is inferred")
        print(last_minute(df, gid).to_string(index=False))


if __name__ == "__main__":
    main()
