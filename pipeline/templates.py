"""Prompt templates: a wording, a list of thresholds to try, and a function that finds who or what qualifies.

A template's `qualify(tables, n)` returns the raw qualifiers for threshold n:
  - a player template returns a frame with one column, player_id (each player once);
  - a team template returns a frame with team_id and season (each qualifying instance; a franchise can appear in
    several seasons, which matters for the team tier).
Adding a template later (referees, for example) means writing one function and calling `register`; the generator,
the validity rules and the reports pick it up from TEMPLATES.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import pandas as pd

PLAYER, TEAM = "player", "team"
TRIPLE_DOUBLE_STATS = ["points", "reb", "ast", "stl", "blk"]
MIN_SEASON_GAMES = 40


@dataclass
class Tables:
    """The processed tables a template may read."""

    players: pd.DataFrame
    teams: pd.DataFrame
    games: pd.DataFrame
    player_games: pd.DataFrame
    team_games: pd.DataFrame
    min_season_games: int = MIN_SEASON_GAMES


Qualify = Callable[[Tables, int], pd.DataFrame]


@dataclass(frozen=True)
class Template:
    key: str  # lowercase with hyphens: it becomes part of the prompt id
    answer_type: str
    wording: str  # completes "name a player who ..." or "name a team that ...", with {n} for the threshold
    thresholds: tuple[int, ...]
    qualify: Qualify
    stat: str  # what the threshold measures, for the reports

    def text(self, era: str, n: int) -> str:
        who = "a player who" if self.answer_type == PLAYER else "a team that"
        return f"{era}, name {who} {self.wording.format(n=n)}."


TEMPLATES: list[Template] = []


def register(template: Template) -> Template:
    if any(t.key == template.key for t in TEMPLATES):
        raise ValueError(f"template {template.key!r} is already registered")
    TEMPLATES.append(template)
    return template


# --- helpers ----------------------------------------------------------------------------------------------------

def _players(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({"player_id": sorted(int(p) for p in df["player_id"].unique())})


def _instances(df: pd.DataFrame) -> pd.DataFrame:
    out = df[["team_id", "season"]].drop_duplicates().sort_values(["team_id", "season"]).reset_index(drop=True)
    return out.astype({"team_id": "int64", "season": "int64"})


def _finals_game_ids(t: Tables) -> pd.Series:
    return t.games.loc[t.games["is_finals"], "game_id"]


def stat_in_game(col: str, scope: str = "any") -> Qualify:
    """Players with at least n of a stat in one game. scope: any game, regular, playoffs or finals."""

    def qualify(t: Tables, n: int) -> pd.DataFrame:
        pg = t.player_games
        if scope == "regular":
            pg = pg[pg["season_type"] == "regular"]
        elif scope == "playoffs":
            pg = pg[pg["season_type"] == "playoffs"]
        elif scope == "finals":
            pg = pg[pg["game_id"].isin(_finals_game_ids(t))]
        return _players(pg[(pg[col] >= n).fillna(False)])

    return qualify


def triple_double(scope: str) -> Qualify:
    """Players with 10 or more in at least three of points, rebounds, assists, steals and blocks in one game.

    n is ignored (a triple-double has no threshold); the template lists a single placeholder value.
    """

    def qualify(t: Tables, n: int) -> pd.DataFrame:
        pg = t.player_games
        if scope == "regular":
            pg = pg[pg["season_type"] == "regular"]
        elif scope == "playoffs":
            pg = pg[pg["season_type"] == "playoffs"]
        elif scope == "finals":
            pg = pg[pg["game_id"].isin(_finals_game_ids(t))]
        double_digit = (pg[TRIPLE_DOUBLE_STATS] >= 10).sum(axis=1)
        return _players(pg[double_digit >= 3])

    return qualify


def ppg_in_season(t: Tables, n: int) -> pd.DataFrame:
    """Players who averaged n or more points in a regular season with at least min_season_games games."""
    reg = t.player_games[t.player_games["season_type"] == "regular"]
    seasons = reg.groupby(["player_id", "season"]).agg(games=("game_id", "size"), pts=("points", "sum")).reset_index()
    seasons["pts"] = seasons["pts"].astype("int64")
    # points / games >= n without floating point: points >= n * games
    ok = seasons[(seasons["games"] >= t.min_season_games) & (seasons["pts"] >= n * seasons["games"])]
    return _players(ok)


def franchises_played_for(t: Tables, n: int) -> pd.DataFrame:
    """Players who appeared in a game for n or more different franchises (regular season or playoffs)."""
    count = t.player_games.groupby("player_id")["team_id"].nunique()
    return _players(pd.DataFrame({"player_id": count[count >= n].index}))


def wins_in_season(season_type: str) -> Qualify:
    def qualify(t: Tables, n: int) -> pd.DataFrame:
        tg = t.team_games[t.team_games["season_type"] == season_type]
        wins = tg.groupby(["team_id", "season"])["won"].sum().reset_index()
        return _instances(wins[wins["won"] >= n])

    return qualify


def points_in_regulation_game(t: Tables, n: int) -> pd.DataFrame:
    regulation = t.games.loc[t.games["periods"] == 4, "game_id"]
    tg = t.team_games[t.team_games["game_id"].isin(regulation)]
    return _instances(tg[tg["team_score"] >= n])


def win_by_margin(t: Tables, n: int) -> pd.DataFrame:
    tg = t.team_games[t.team_games["won"]]
    return _instances(tg[(tg["team_score"] - tg["opponent_score"]) >= n])


# --- the templates ----------------------------------------------------------------------------------------------

_P, _T = PLAYER, TEAM
register(Template("points-regular", _P, "scored {n} or more points in a regular-season game", (35, 40, 45, 50, 55, 60, 65), stat_in_game("points", "regular"), "points"))
register(Template("points-playoff", _P, "scored {n} or more points in a playoff game", (25, 30, 35, 40, 45, 50), stat_in_game("points", "playoffs"), "points"))
register(Template("points-finals", _P, "scored {n} or more points in a Finals game", (20, 25, 30, 35, 40), stat_in_game("points", "finals"), "points"))
register(Template("triple-double-regular", _P, "recorded a triple-double in a regular-season game", (0,), triple_double("regular"), "triple-double"))
register(Template("triple-double-playoff", _P, "recorded a triple-double in a playoff game", (0,), triple_double("playoffs"), "triple-double"))
register(Template("triple-double-finals", _P, "recorded a triple-double in a Finals game", (0,), triple_double("finals"), "triple-double"))
register(Template("rebounds", _P, "grabbed {n} or more rebounds in a game", (16, 18, 20, 22, 24, 25, 27), stat_in_game("reb"), "rebounds"))
register(Template("assists", _P, "recorded {n} or more assists in a game", (14, 15, 16, 18, 20, 22), stat_in_game("ast"), "assists"))
register(Template("threes", _P, "made {n} or more three-pointers in a game", (8, 9, 10, 11, 12), stat_in_game("fg3m"), "threes made"))
register(Template("blocks", _P, "blocked {n} or more shots in a game", (6, 7, 8, 9, 10, 11), stat_in_game("blk"), "blocks"))
register(Template("steals", _P, "stole the ball {n} or more times in a game", (5, 6, 7, 8, 9), stat_in_game("stl"), "steals"))
register(Template("ppg-season", _P, "averaged {n} or more points per game in a regular season (minimum 40 games)", (20, 22, 24, 25, 26, 27, 28, 30, 32), ppg_in_season, "points per game"))
register(Template("franchises", _P, "played for {n} or more different franchises", (4, 5, 6, 7, 8, 9), franchises_played_for, "franchises"))

register(Template("wins-season", _T, "won {n} or more regular-season games in a season", (50, 55, 58, 60, 62, 65, 67), wins_in_season("regular"), "wins"))
register(Template("wins-playoff", _T, "won {n} or more playoff games in a single postseason", (10, 12, 14, 15, 16), wins_in_season("playoffs"), "playoff wins"))
register(Template("points-regulation", _T, "scored {n} or more points in a regulation game", (140, 145, 150, 155, 160), points_in_regulation_game, "points"))
register(Template("win-margin", _T, "won a game by {n} or more points", (40, 45, 50, 55, 60), win_by_margin, "margin"))
