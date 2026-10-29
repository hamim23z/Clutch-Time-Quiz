"""Season stage: run games, box scores and name collection for one season, and save or load the result.

Seasons are processed one at a time so the raw files never pile up. Each season's result is saved under
data/processed/parts/<season>/ and combined later (assemble.py).
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from boxscores import build_player_games, build_team_games
from games import EXCLUSION_REASONS, select_games
from players import season_player_names
from rawcols import slim
from teams import season_team_names

FRAMES = ["games", "team_games", "player_games", "player_names", "team_names", "officials_raw", "skipped"]


@dataclass
class SeasonTables:
    season: int
    games: pd.DataFrame
    team_games: pd.DataFrame
    player_games: pd.DataFrame
    player_names: pd.DataFrame
    team_names: pd.DataFrame
    officials_raw: pd.DataFrame
    skipped: pd.DataFrame
    excluded: dict[str, int]


def process_season(season: int, raw: dict[str, pd.DataFrame]) -> SeasonTables:
    """raw has the four raw tables of one season: schedule, team, player, officials."""
    sched, team, player, officials = (slim(raw[t], t) for t in ("schedule", "team", "player", "officials"))
    sel = select_games(sched, team, player)
    team_games = build_team_games(team, sel.games)
    player_games = build_player_games(player, sel.games)
    officials_raw = officials[officials["game_id"].isin(sel.games["game_id"])].reset_index(drop=True)
    return SeasonTables(
        season=season,
        games=sel.games,
        team_games=team_games,
        player_games=player_games,
        player_names=season_player_names(player_games, player),
        team_names=season_team_names(team, team_games),
        officials_raw=officials_raw,
        skipped=sel.skipped,
        excluded=sel.excluded,
    )


def save_season(t: SeasonTables, parts_dir: Path) -> None:
    d = parts_dir / str(t.season)
    d.mkdir(parents=True, exist_ok=True)
    for name in FRAMES:
        getattr(t, name).to_parquet(d / f"{name}.parquet", compression="zstd", index=False)
    (d / "excluded.json").write_text(json.dumps(t.excluded))


def season_is_saved(season: int, parts_dir: Path) -> bool:
    return (parts_dir / str(season) / "excluded.json").exists()


def load_season(season: int, parts_dir: Path) -> SeasonTables:
    d = parts_dir / str(season)
    frames = {name: pd.read_parquet(d / f"{name}.parquet") for name in FRAMES}
    excluded = {r: 0 for r in EXCLUSION_REASONS} | json.loads((d / "excluded.json").read_text())
    return SeasonTables(season=season, excluded=excluded, **frames)
