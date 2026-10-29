"""Parameterised prompt families: one wording, many parameters (a franchise, a season, a month, a star, a threshold).

Where `templates.py` has one prompt per threshold, a family here yields one prompt per parameter set, for example
"played for the Boston Celtics in the 2007-08 season" for every franchise and season. Most player families are
*broad*: role players are valid answers, so a pool has 15 to 700 players and rarity matters. A family's `enumerate`
returns every (parameter, pool) at once, from grouped tables rather than one query per prompt; `bruteforce.py` has
a separately written query per family for the checks.

A pool is a set of player ids (player families) or a set of (team_id, season) pairs (team families, where the
season decides the franchise's tier through the current-name rule).
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from itertools import combinations
from typing import Any, Callable, Iterator

import pandas as pd

from templates import PLAYER, TEAM, Tables

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
STAR_COUNT = 100
STAR_MIN_GAMES = 400
MIN_BROAD, MAX_BROAD = 15, 700  # valid answers for a broad player prompt
MIN_TEAM, MAX_TEAM = 5, 24  # teams: at least 5; 25 or more of 30 franchises would be a giveaway


def season_label(season: int) -> str:
    return f"{season - 1}-{str(season)[-2:]}"


@dataclass
class Ctx:
    """What the wordings need: names of franchises (now and in each season) and the list of stars."""

    tables: Tables
    stars: list[int]
    current: dict[int, str] = field(default_factory=dict)
    earlier: dict[int, list[str]] = field(default_factory=dict)
    in_season: dict[tuple[int, int], str] = field(default_factory=dict)
    player_name: dict[int, str] = field(default_factory=dict)

    def franchise(self, tid: int) -> str:
        """'the Oklahoma City Thunder (including its time as the SuperSonics)' for an all-time prompt."""
        text = f"the {self.current[tid]}"
        if self.earlier[tid]:
            text += " (including its time as the " + " and the ".join(self.earlier[tid]) + ")"
        return text

    def franchise_in(self, tid: int, season: int) -> str:
        return f"the {self.in_season[(tid, season)]}"


def make_ctx(tables: Tables, fame: pd.DataFrame | None = None) -> Ctx:
    ctx = Ctx(tables=tables, stars=[])
    for row in tables.teams.itertuples():
        tid = int(row.team_id)
        ctx.current[tid] = row.current_name
        ctx.earlier[tid] = []
        current_nickname = next((e["nickname"] for e in row.names if e["name"] == row.current_name), "")
        for entry in row.names:
            for s in entry["seasons"]:
                ctx.in_season[(tid, int(s))] = entry["name"]
            # earlier nicknames only: a city move with the same nickname (the New Jersey Nets) needs no mention
            if entry["nickname"] != current_nickname and entry["nickname"] not in ctx.earlier[tid]:
                ctx.earlier[tid].append(entry["nickname"])
    ctx.player_name = dict(zip(tables.players["player_id"].astype(int), tables.players["unique_name"]))
    if fame is not None:
        games = tables.player_games.groupby("player_id").size()
        eligible = set(games[games >= STAR_MIN_GAMES].index)
        ranked = fame[fame["player_id"].isin(eligible)].sort_values(["fame_rank", "career_points"], ascending=[True, False])
        ctx.stars = [int(p) for p in ranked["player_id"].head(STAR_COUNT)]
    return ctx


@dataclass(frozen=True)
class Family:
    key: str
    answer_type: str
    broad: bool
    group: str  # what it is about, so one dive does not ask the same thing twice
    clause: Callable[[Ctx, tuple], str]  # completes "name a player who ..." / "name a team that ..."
    enumerate: Callable[[Tables, Ctx], Iterator[tuple[tuple, Any]]]
    tags: Callable[[tuple], frozenset] = lambda param: frozenset()  # franchises and stars a prompt is about
    stat: str = ""

    def text(self, era: str, ctx: Ctx, param: tuple) -> str:
        who = "a player who" if self.answer_type == PLAYER else "a team that"
        return f"{era}, name {who} {self.clause(ctx, param)}."


FAMILIES: list[Family] = []

# thresholds tried per family (a pool outside its answer window is dropped); tests replace them with fixture-sized ones
THRESHOLDS: dict[str, tuple[int, ...]] = {
    "franchise-points": (25, 30, 35, 40), "points-against": (30, 35, 40, 45),
    "month-points": (20, 25, 30, 35, 40, 45), "month-threes": (4, 5, 6, 7, 8),
    "season-points": (30, 35, 40, 45, 50), "season-threes": (6, 7, 8, 9, 10),
    "season-rebounds": (14, 16, 18, 20), "season-assists": (11, 13, 15, 17),
    "wins-in-season": (40, 45, 50, 55, 60), "home-wins-in-season": (30, 33, 35, 37), "road-wins-in-season": (20, 23, 25, 27),
    "playoff-wins-in-season": (1, 4, 8, 12), "regulation-points-in-season": (125, 130, 135, 140, 145, 150),
    "margin-in-season": (25, 30, 35, 40, 45), "threes-in-season": (14, 17, 20, 23, 26),
    "held-opponent-in-season": (65, 70, 75, 80), "overtime-wins-in-season": (1, 2, 3),
}

# where the threshold sits in a family's parameter tuple; two prompts that differ only there are near-duplicates
THRESHOLD_AT: dict[str, int] = {
    "franchise-points": 1, "points-against": 1, "month-points": 2, "month-threes": 2, "season-points": 1, "season-threes": 1,
    "season-rebounds": 1, "season-assists": 1, "wins-in-season": 1, "home-wins-in-season": 1, "road-wins-in-season": 1,
    "playoff-wins-in-season": 1, "regulation-points-in-season": 1, "margin-in-season": 1, "threes-in-season": 1,
    "held-opponent-in-season": 1, "overtime-wins-in-season": 1,
}


def threshold_of(key: str, param: tuple) -> int | None:
    at = THRESHOLD_AT.get(key)
    return None if at is None else int(param[at])


def duplicate_key(key: str, param: tuple) -> tuple:
    """The family and its parameters without the threshold: prompts sharing it ask the same question at nearby thresholds."""
    at = THRESHOLD_AT.get(key)
    return (key,) + tuple(p for i, p in enumerate(param) if i != at)


def register_family(family: Family) -> Family:
    if any(f.key == family.key for f in FAMILIES):
        raise ValueError(f"family {family.key!r} is already registered")
    FAMILIES.append(family)
    return family


# --- table helpers ----------------------------------------------------------------------------------------------

def _dated(pg: pd.DataFrame, games: pd.DataFrame) -> pd.DataFrame:
    """Player-game rows with the calendar year and month of the game."""
    dates = games[["game_id", "game_date"]].copy()
    text = dates["game_date"].astype(str)
    dates["year"], dates["month"] = text.str[:4].astype(int), text.str[5:7].astype(int)
    return pg.merge(dates[["game_id", "year", "month"]], on="game_id")


def _sets(df: pd.DataFrame, keys: list[str], value: str = "player_id") -> dict:
    out: dict = {}
    for key, ids in df.groupby(keys)[value]:
        out[key if isinstance(key, tuple) else (key,)] = {int(i) for i in ids.unique()}
    return out


def _finals_rows(t: Tables) -> pd.DataFrame:
    return t.player_games[t.player_games["game_id"].isin(t.games.loc[t.games["is_finals"], "game_id"])]


def _regular(t: Tables) -> pd.DataFrame:
    return t.player_games[t.player_games["season_type"] == "regular"]


def _f(param_index: int = 0) -> Callable[[tuple], frozenset]:
    return lambda param: frozenset({f"f:{param[param_index]}"})


# --- player families: franchises --------------------------------------------------------------------------------

def _enum_franchise(scope: str):
    def run(t: Tables, ctx: Ctx):
        pg = t.player_games if scope == "any" else t.player_games[t.player_games["season_type"] == scope]
        for param, ids in _sets(pg, ["team_id"]).items():
            yield (int(param[0]),), ids
    return run


register_family(Family("franchise-regular", PLAYER, True, "franchise", lambda c, p: f"played for {c.franchise(p[0])} in a regular-season game",
                       _enum_franchise("regular"), _f(), "franchise"))
register_family(Family("franchise-playoff", PLAYER, True, "franchise", lambda c, p: f"played for {c.franchise(p[0])} in a playoff game",
                       _enum_franchise("playoffs"), _f(), "franchise"))


def _enum_franchise_season(t: Tables, ctx: Ctx):
    for (tid, season), ids in _sets(_regular(t), ["team_id", "season"]).items():
        yield (int(tid), int(season)), ids


register_family(Family("franchise-season", PLAYER, True, "franchise-season",
                       lambda c, p: f"played for {c.franchise_in(*p)} in a regular-season game in the {season_label(p[1])} season",
                       _enum_franchise_season, _f(), "franchise and season"))


def _enum_franchise_start(t: Tables, ctx: Ctx):
    for param, ids in _sets(t.player_games[t.player_games["started"].astype(bool)], ["team_id"]).items():
        yield (int(param[0]),), ids


register_family(Family("franchise-start", PLAYER, True, "franchise", lambda c, p: f"started a game for {c.franchise(p[0])}",
                       _enum_franchise_start, _f(), "starts for a franchise"))

def _enum_franchise_bench(t: Tables, ctx: Ctx):
    for param, ids in _sets(t.player_games[~t.player_games["started"].astype(bool)], ["team_id"]).items():
        yield (int(param[0]),), ids


register_family(Family("franchise-bench", PLAYER, True, "franchise", lambda c, p: f"came off the bench in a game for {c.franchise(p[0])}",
                       _enum_franchise_bench, _f(), "bench appearances for a franchise"))

WINDOW = 5  # seasons


def _enum_franchise_years(t: Tables, ctx: Ctx):
    """Five-season windows that tile the data: 2001-02 to 2005-06, 2006-07 to 2010-11, and so on."""
    first = int(t.games["season"].min())
    reg = _regular(t)
    window = (reg["season"] - first) // WINDOW
    for (tid, w), ids in _sets(reg.assign(window=window), ["team_id", "window"]).items():
        start = first + int(w) * WINDOW
        yield (int(tid), start, min(start + WINDOW - 1, int(t.games["season"].max()))), ids


register_family(Family("franchise-years", PLAYER, True, "franchise-season",
                       lambda c, p: f"played for {c.franchise(p[0])} in a regular-season game between the {season_label(p[1])} and {season_label(p[2])} seasons",
                       _enum_franchise_years, _f(), "franchise and five seasons"))


def _enum_franchise_playoff_season(t: Tables, ctx: Ctx):
    po = t.player_games[t.player_games["season_type"] == "playoffs"]
    for (tid, season), ids in _sets(po, ["team_id", "season"]).items():
        yield (int(tid), int(season)), ids


register_family(Family("franchise-playoff-season", PLAYER, True, "franchise-season",
                       lambda c, p: f"played for {c.franchise_in(*p)} in a playoff game in the {season_label(p[1])} season",
                       _enum_franchise_playoff_season, _f(), "franchise and season (playoffs)"))

def _enum_franchise_points(t: Tables, ctx: Ctx):
    for n in THRESHOLDS["franchise-points"]:
        for param, ids in _sets(t.player_games[(t.player_games["points"] >= n).fillna(False)], ["team_id"]).items():
            yield (int(param[0]), n), ids


register_family(Family("franchise-points", PLAYER, True, "franchise-scoring", lambda c, p: f"scored {p[1]} or more points in a game for {c.franchise(p[0])}",
                       _enum_franchise_points, _f(), "points for a franchise"))


def _enum_both(t: Tables, ctx: Ctx):
    teams_of: dict[int, set[int]] = defaultdict(set)
    for pid, tid in t.player_games[["player_id", "team_id"]].drop_duplicates().itertuples(index=False):
        teams_of[int(pid)].add(int(tid))
    pools: dict[tuple[int, int], set[int]] = defaultdict(set)
    for pid, teams in teams_of.items():
        for a, b in combinations(sorted(teams), 2):
            pools[(a, b)].add(pid)
    yield from pools.items()


register_family(Family("both-franchises", PLAYER, True, "two-franchises", lambda c, p: f"played for both {c.franchise(p[0])} and {c.franchise(p[1])}",
                       _enum_both, lambda p: frozenset({f"f:{p[0]}", f"f:{p[1]}"}), "two franchises"))


def _enum_against(t: Tables, ctx: Ctx):
    for n in THRESHOLDS["points-against"]:
        for param, ids in _sets(t.player_games[(t.player_games["points"] >= n).fillna(False)], ["opponent_team_id"]).items():
            yield (int(param[0]), n), ids


register_family(Family("points-against", PLAYER, True, "franchise-scoring", lambda c, p: f"scored {p[1]} or more points against {c.franchise(p[0])} in a game",
                       _enum_against, _f(), "points against a franchise"))


# --- player families: teammates of a star -----------------------------------------------------------------------

def _enum_teammate(t: Tables, ctx: Ctx):
    pg = t.player_games[["game_id", "team_id", "player_id"]]
    for star in ctx.stars:
        mine = pg.loc[pg["player_id"] == star, ["game_id", "team_id"]]
        others = pg.merge(mine, on=["game_id", "team_id"])
        yield (star,), {int(p) for p in others["player_id"].unique()} - {star}


register_family(Family("teammate", PLAYER, True, "teammate",
                       lambda c, p: f"played in the same game as {c.player_name[p[0]]} for the same team",
                       _enum_teammate, lambda p: frozenset({f"s:{p[0]}"}), "games with a star"))


# --- player families: the Finals --------------------------------------------------------------------------------

def _single(ids: set[int]):
    yield (), ids


register_family(Family("finals-appearance", PLAYER, True, "finals", lambda c, p: "appeared in an NBA Finals game",
                       lambda t, c: _single({int(i) for i in _finals_rows(t)["player_id"].unique()}), stat="Finals appearances"))
register_family(Family("finals-three", PLAYER, True, "finals", lambda c, p: "made a three-pointer in an NBA Finals game",
                       lambda t, c: _single({int(i) for i in _finals_rows(t).loc[lambda d: d["fg3m"] >= 1, "player_id"].unique()}), stat="Finals threes"))
register_family(Family("finals-steal-block", PLAYER, True, "finals", lambda c, p: "recorded a steal or a block in an NBA Finals game",
                       lambda t, c: _single({int(i) for i in _finals_rows(t).loc[lambda d: (d["stl"] >= 1) | (d["blk"] >= 1), "player_id"].unique()}), stat="Finals steals and blocks"))


def _enum_finals_year(t: Tables, ctx: Ctx):
    for param, ids in _sets(_finals_rows(t), ["season"]).items():
        yield (int(param[0]),), ids


register_family(Family("finals-year", PLAYER, True, "finals", lambda c, p: f"appeared in the {p[0]} NBA Finals",
                       _enum_finals_year, stat="a specific Finals"))


# --- player families: a month or a season -----------------------------------------------------------------------

def _enum_month(col: str, key: str):
    def run(t: Tables, ctx: Ctx):
        dated = _dated(_regular(t), t.games)
        for n in THRESHOLDS[key]:
            for (year, month), ids in _sets(dated[(dated[col] >= n).fillna(False)], ["year", "month"]).items():
                yield (int(year), int(month), n), ids
    return run


def _enum_season(col: str, key: str):
    def run(t: Tables, ctx: Ctx):
        reg = _regular(t)
        for n in THRESHOLDS[key]:
            for (season,), ids in _sets(reg[(reg[col] >= n).fillna(False)], ["season"]).items():
                yield (int(season), n), ids
    return run


register_family(Family("month-points", PLAYER, True, "month", lambda c, p: f"scored {p[2]} or more points in a regular-season game in {MONTHS[p[1] - 1]} {p[0]}",
                       _enum_month("points", "month-points"), stat="points in a month"))
register_family(Family("month-threes", PLAYER, True, "month", lambda c, p: f"made {p[2]} or more three-pointers in a regular-season game in {MONTHS[p[1] - 1]} {p[0]}",
                       _enum_month("fg3m", "month-threes"), stat="threes in a month"))
register_family(Family("season-points", PLAYER, True, "season", lambda c, p: f"scored {p[1]} or more points in a regular-season game in the {season_label(p[0])} season",
                       _enum_season("points", "season-points"), stat="points in a season"))
register_family(Family("season-threes", PLAYER, True, "season", lambda c, p: f"made {p[1]} or more three-pointers in a regular-season game in the {season_label(p[0])} season",
                       _enum_season("fg3m", "season-threes"), stat="threes in a season"))
register_family(Family("season-rebounds", PLAYER, True, "season", lambda c, p: f"grabbed {p[1]} or more rebounds in a regular-season game in the {season_label(p[0])} season",
                       _enum_season("reb", "season-rebounds"), stat="rebounds in a season"))
register_family(Family("season-assists", PLAYER, True, "season", lambda c, p: f"recorded {p[1]} or more assists in a regular-season game in the {season_label(p[0])} season",
                       _enum_season("ast", "season-assists"), stat="assists in a season"))


# --- team families -----------------------------------------------------------------------------------------------

def _pairs(df: pd.DataFrame) -> set[tuple[int, int]]:
    return {(int(t), int(s)) for t, s in zip(df["team_id"], df["season"])}


def _tg_games(t: Tables) -> pd.DataFrame:
    return t.team_games.merge(t.games[["game_id", "periods"]], on="game_id")


def _enum_team_threshold(season_type: str | None, build: Callable[[pd.DataFrame, int], pd.DataFrame], key: str):
    def run(t: Tables, ctx: Ctx):
        tg = _tg_games(t)
        if season_type:
            tg = tg[tg["season_type"] == season_type]
        for n in THRESHOLDS[key]:
            picked = build(tg, n)
            for season, group in picked.groupby("season"):
                yield (int(season), n), _pairs(group)
    return run


def _wins_at_least(side: str | None, season_type: str):
    def build(tg: pd.DataFrame, n: int) -> pd.DataFrame:
        part = tg if side is None else tg[tg["home_away"] == side]
        wins = part.groupby(["team_id", "season"])["won"].sum().reset_index()
        return wins[wins["won"] >= n]
    return build


def _enum_made_playoffs(t: Tables, ctx: Ctx):
    po = t.team_games[t.team_games["season_type"] == "playoffs"]
    for season, group in po.groupby("season"):
        yield (int(season),), _pairs(group)


def _enum_series(kind: str):
    """Franchises that played (kind 'played') or won (kind 'won') a playoff game against a given franchise."""
    def run(t: Tables, ctx: Ctx):
        po = t.team_games[t.team_games["season_type"] == "playoffs"]
        if kind == "won":
            po = po[po["won"]]
        for opp, group in po.groupby("opponent_team_id"):
            yield (int(opp),), _pairs(group)
    return run


def _season_clause(template: str) -> Callable[[Ctx, tuple], str]:
    return lambda c, p: template.format(season=season_label(p[0]), n=p[1] if len(p) > 1 else "")


register_family(Family("made-playoffs", TEAM, False, "playoffs", lambda c, p: f"made the playoffs in the {season_label(p[0])} season",
                       _enum_made_playoffs, stat="playoff teams"))
register_family(Family("wins-in-season", TEAM, False, "wins", _season_clause("won {n} or more regular-season games in the {season} season"),
                       _enum_team_threshold("regular", _wins_at_least(None, "regular"), "wins-in-season"), stat="wins"))
register_family(Family("home-wins-in-season", TEAM, False, "wins", _season_clause("won {n} or more home games in the {season} season"),
                       _enum_team_threshold("regular", _wins_at_least("home", "regular"), "home-wins-in-season"), stat="home wins"))
register_family(Family("road-wins-in-season", TEAM, False, "wins", _season_clause("won {n} or more road games in the {season} season"),
                       _enum_team_threshold("regular", _wins_at_least("away", "regular"), "road-wins-in-season"), stat="road wins"))
register_family(Family("playoff-wins-in-season", TEAM, False, "playoff wins", _season_clause("won {n} or more playoff games in the {season} postseason"),
                       _enum_team_threshold("playoffs", _wins_at_least(None, "playoffs"), "playoff-wins-in-season"), stat="playoff wins"))
register_family(Family("regulation-points-in-season", TEAM, False, "team scoring", _season_clause("scored {n} or more points in a regulation game in the {season} season"),
                       _enum_team_threshold(None, lambda tg, n: tg[(tg["periods"] == 4) & (tg["team_score"] >= n)], "regulation-points-in-season"), stat="points"))
register_family(Family("margin-in-season", TEAM, False, "margin", _season_clause("won a game by {n} or more points in the {season} season"),
                       _enum_team_threshold(None, lambda tg, n: tg[tg["won"] & (tg["team_score"] - tg["opponent_score"] >= n)], "margin-in-season"), stat="margin"))
register_family(Family("threes-in-season", TEAM, False, "team threes", _season_clause("made {n} or more three-pointers as a team in a game in the {season} season"),
                       _enum_team_threshold(None, lambda tg, n: tg[(tg["fg3m"] >= n).fillna(False)], "threes-in-season"), stat="team threes"))
register_family(Family("held-opponent-in-season", TEAM, False, "defence", _season_clause("held an opponent to {n} or fewer points in a game in the {season} season"),
                       _enum_team_threshold(None, lambda tg, n: tg[tg["opponent_score"] <= n], "held-opponent-in-season"), stat="points allowed"))
register_family(Family("overtime-wins-in-season", TEAM, False, "overtime", _season_clause("won a game that went to {n} or more overtimes in the {season} season"),
                       _enum_team_threshold(None, lambda tg, n: tg[tg["won"] & (tg["periods"] >= 4 + n)], "overtime-wins-in-season"), stat="overtimes"))
register_family(Family("played-playoff-against", TEAM, False, "playoff opponents", lambda c, p: f"played a playoff game against {c.franchise(p[0])}",
                       _enum_series("played"), _f(), "playoff opponents"))
register_family(Family("beat-in-playoffs", TEAM, False, "playoff opponents", lambda c, p: f"won a playoff game against {c.franchise(p[0])}",
                       _enum_series("won"), _f(), "playoff wins against a franchise"))
