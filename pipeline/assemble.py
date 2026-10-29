"""Build stage: combine the per-season results into the six final tables, with integrity checks."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from officials import OfficialsResult, build_officials
from players import build_players, load_aliases, shared_names
from season import SeasonTables
from teams import build_teams

TABLES = ["players", "teams", "games", "player_games", "team_games", "officials"]


@dataclass
class Tables:
    players: pd.DataFrame
    teams: pd.DataFrame
    games: pd.DataFrame
    player_games: pd.DataFrame
    team_games: pd.DataFrame
    officials: pd.DataFrame
    # material for docs/pipeline-notes.md
    skipped: pd.DataFrame
    excluded: dict[str, int]
    seasons: list[int]
    shared_names: dict[str, list[int]]
    player_names: pd.DataFrame
    aliases: pd.DataFrame
    officials_result: OfficialsResult


def _concat(seasons: list[SeasonTables], name: str) -> pd.DataFrame:
    frames = [getattr(s, name) for s in seasons if len(getattr(s, name))]
    return pd.concat(frames, ignore_index=True) if frames else getattr(seasons[0], name).iloc[0:0]


def combine(seasons: list[SeasonTables], aliases_path: Path, partial: bool = False) -> Tables:
    seasons = sorted(seasons, key=lambda s: s.season)
    games = _concat(seasons, "games").sort_values(["game_date", "game_id"]).reset_index(drop=True)
    player_games = _concat(seasons, "player_games")
    team_games = _concat(seasons, "team_games")
    player_names = _concat(seasons, "player_names")
    team_names = _concat(seasons, "team_names")

    aliases = load_aliases(aliases_path)
    players = build_players(player_names, aliases, allow_missing_aliases=partial)
    teams = build_teams(team_names)

    officials_result = build_officials(_concat(seasons, "officials_raw"), games)
    games = games.merge(officials_result.game_status, on="game_id", how="left")

    excluded: dict[str, int] = {}
    for s in seasons:
        for reason, n in s.excluded.items():
            excluded[reason] = excluded.get(reason, 0) + n

    tables = Tables(
        players=players, teams=teams, games=games, player_games=player_games, team_games=team_games,
        officials=officials_result.officials, skipped=_concat(seasons, "skipped"), excluded=excluded,
        seasons=[s.season for s in seasons], shared_names=shared_names(player_names), player_names=player_names,
        aliases=aliases, officials_result=officials_result,
    )
    check(tables)
    return tables


def check(t: Tables) -> None:
    """Fail loudly if the tables do not fit together."""
    problems = []
    if t.games["game_id"].duplicated().any():
        problems.append("duplicate game ids in games")
    if t.player_games.duplicated(["game_id", "player_id"]).any():
        problems.append("duplicate (game, player) rows in player_games")
    if t.team_games.duplicated(["game_id", "team_id"]).any():
        problems.append("duplicate (game, team) rows in team_games")
    if not (t.team_games.groupby("game_id").size() == 2).all():
        problems.append("a game does not have exactly two team_games rows")
    if set(t.team_games["game_id"]) != set(t.games["game_id"]):
        problems.append("team_games and games cover different games")
    if not set(t.player_games["game_id"]) <= set(t.games["game_id"]):
        problems.append("player_games has games that are not in games")
    if not set(t.player_games["player_id"]) <= set(t.players["player_id"]):
        problems.append("player_games has players that are not in players")
    if not set(t.team_games["team_id"]) <= set(t.teams["team_id"]):
        problems.append("team_games has teams that are not in teams")
    if not set(t.officials["game_id"]) <= set(t.games["game_id"]):
        problems.append("officials has games that are not in games")
    if t.players["player_id"].duplicated().any() or t.players["unique_name"].duplicated().any():
        problems.append("players are not unique by player_id and unique_name")
    if problems:
        raise AssertionError("; ".join(problems))
