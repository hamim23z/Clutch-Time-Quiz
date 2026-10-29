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
    group: str = ""  # the stat it is about ('points', 'rebounds', ...): curation keeps one dive from asking the same stat twice

    @property
    def stat_group(self) -> str:
        return self.group or self.key

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


SCOPES = ("any", "regular", "playoffs", "finals", "game7", "overtime", "bench", "loss", "road")


def _scoped(t: Tables, scope: str) -> pd.DataFrame:
    """Player-game rows in a scope: any game, regular season, playoffs, Finals, a Game 7, an overtime game,
    games the player came off the bench in, games his team lost, or road games."""
    pg = t.player_games
    if scope == "any":
        return pg
    if scope == "regular":
        return pg[pg["season_type"] == "regular"]
    if scope == "playoffs":
        return pg[pg["season_type"] == "playoffs"]
    if scope == "finals":
        return pg[pg["game_id"].isin(_finals_game_ids(t))]
    if scope == "game7":
        return pg[pg["game_id"].isin(t.games.loc[(t.games["series_game"] == 7).fillna(False), "game_id"])]
    if scope == "overtime":
        return pg[pg["game_id"].isin(t.games.loc[t.games["overtime"], "game_id"])]
    if scope == "bench":
        return pg[~pg["started"].astype(bool)]
    if scope == "road":
        return pg[pg["home_away"] == "away"]
    if scope == "loss":
        lost = t.team_games.loc[~t.team_games["won"], ["game_id", "team_id"]]
        return pg.merge(lost, on=["game_id", "team_id"])
    raise ValueError(f"unknown scope {scope!r}")


def stat_in_game(col: str, scope: str = "any") -> Qualify:
    """Players with at least n of a stat in one game, within a scope (see SCOPES)."""

    def qualify(t: Tables, n: int) -> pd.DataFrame:
        pg = _scoped(t, scope)
        return _players(pg[(pg[col] >= n).fillna(False)])

    return qualify


def combo_in_game(minimums: dict[str, int], scope: str = "any") -> Qualify:
    """Players who reached every minimum in the same game, for example 30 points and 15 rebounds. n is ignored."""

    def qualify(t: Tables, n: int) -> pd.DataFrame:
        pg = _scoped(t, scope)
        ok = pd.Series(True, index=pg.index)
        for col, low in minimums.items():
            ok &= (pg[col] >= low).fillna(False)
        return _players(pg[ok])

    return qualify


def at_least_n_of_everything(t: Tables, n: int) -> pd.DataFrame:
    """Players with at least n points, rebounds, assists, steals and blocks in one game (5 is a '5x5')."""
    pg = t.player_games
    return _players(pg[(pg[TRIPLE_DOUBLE_STATS] >= n).all(axis=1)])


def perfect_shooting(t: Tables, n: int) -> pd.DataFrame:
    """Players with n or more field goals made in a game and no misses."""
    pg = t.player_games
    return _players(pg[((pg["fgm"] >= n) & (pg["fga"] == pg["fgm"])).fillna(False)])


def triple_double(scope: str) -> Qualify:
    """Players with 10 or more in at least three of points, rebounds, assists, steals and blocks in one game.

    n is ignored (a triple-double has no threshold); the template lists a single placeholder value.
    """

    def qualify(t: Tables, n: int) -> pd.DataFrame:
        pg = _scoped(t, scope)
        double_digit = (pg[TRIPLE_DOUBLE_STATS] >= 10).sum(axis=1)
        return _players(pg[double_digit >= 3])

    return qualify


def _regular_season_totals(t: Tables, cols: list[str]) -> pd.DataFrame:
    reg = t.player_games[t.player_games["season_type"] == "regular"]
    agg = {"games": ("game_id", "size"), **{c: (c, "sum") for c in cols}}
    seasons = reg.groupby(["player_id", "season"]).agg(**agg).reset_index()
    seasons[cols] = seasons[cols].astype("int64")
    return seasons[seasons["games"] >= t.min_season_games]


def avg_in_season(col: str) -> Qualify:
    """Players who averaged n or more of a stat in a regular season with at least min_season_games games."""

    def qualify(t: Tables, n: int) -> pd.DataFrame:
        seasons = _regular_season_totals(t, [col])
        # total / games >= n without floating point: total >= n * games
        return _players(seasons[seasons[col] >= n * seasons["games"]])

    return qualify


ppg_in_season = avg_in_season("points")


def double_double_average(t: Tables, n: int) -> pd.DataFrame:
    """Players who averaged 10 or more points and 10 or more rebounds in the same regular season. n is ignored."""
    seasons = _regular_season_totals(t, ["points", "reb"])
    return _players(seasons[(seasons["points"] >= 10 * seasons["games"]) & (seasons["reb"] >= 10 * seasons["games"])])


def franchises_played_for(t: Tables, n: int) -> pd.DataFrame:
    """Players who appeared in a game for n or more different franchises (regular season or playoffs)."""
    count = t.player_games.groupby("player_id")["team_id"].nunique()
    return _players(pd.DataFrame({"player_id": count[count >= n].index}))


def _regular(tg: pd.DataFrame) -> pd.DataFrame:
    return tg[tg["season_type"] == "regular"]


def wins_in_season(season_type: str) -> Qualify:
    def qualify(t: Tables, n: int) -> pd.DataFrame:
        tg = t.team_games[t.team_games["season_type"] == season_type]
        wins = tg.groupby(["team_id", "season"])["won"].sum().reset_index()
        return _instances(wins[wins["won"] >= n])

    return qualify


def losses_in_season(t: Tables, n: int) -> pd.DataFrame:
    tg = _regular(t.team_games).assign(lost=lambda d: ~d["won"])
    losses = tg.groupby(["team_id", "season"])["lost"].sum().reset_index()
    return _instances(losses[losses["lost"] >= n])


def wins_at(side: str) -> Qualify:
    """Franchise seasons with n or more regular-season wins at home (side 'home') or on the road (side 'away')."""

    def qualify(t: Tables, n: int) -> pd.DataFrame:
        tg = _regular(t.team_games)
        tg = tg[tg["home_away"] == side]
        wins = tg.groupby(["team_id", "season"])["won"].sum().reset_index()
        return _instances(wins[wins["won"] >= n])

    return qualify


def points_in_regulation_game(t: Tables, n: int) -> pd.DataFrame:
    regulation = t.games.loc[t.games["periods"] == 4, "game_id"]
    tg = t.team_games[t.team_games["game_id"].isin(regulation)]
    return _instances(tg[tg["team_score"] >= n])


def points_in_game(scope: str) -> Qualify:
    """Teams with n or more points in a game, overtime included, within a scope: 'any' or 'playoffs'."""

    def qualify(t: Tables, n: int) -> pd.DataFrame:
        tg = t.team_games if scope == "any" else t.team_games[t.team_games["season_type"] == scope]
        return _instances(tg[tg["team_score"] >= n])

    return qualify


def win_by_margin_in(scope: str) -> Qualify:
    def qualify(t: Tables, n: int) -> pd.DataFrame:
        tg = t.team_games if scope == "any" else t.team_games[t.team_games["season_type"] == scope]
        tg = tg[tg["won"]]
        return _instances(tg[(tg["team_score"] - tg["opponent_score"]) >= n])

    return qualify


win_by_margin = win_by_margin_in("any")


def held_opponent_to(t: Tables, n: int) -> pd.DataFrame:
    """Teams that held an opponent to n or fewer points in a game (the threshold is a ceiling, not a floor)."""
    return _instances(t.team_games[t.team_games["opponent_score"] <= n])


def team_stat_in_game(col: str) -> Qualify:
    def qualify(t: Tables, n: int) -> pd.DataFrame:
        return _instances(t.team_games[(t.team_games[col] >= n).fillna(False)])

    return qualify


def overtime_wins(t: Tables, n: int) -> pd.DataFrame:
    """Teams that won a game that went to n or more overtimes (a game of 4 + n periods or more)."""
    long_games = t.games.loc[t.games["periods"] >= 4 + n, "game_id"]
    tg = t.team_games[t.team_games["game_id"].isin(long_games) & t.team_games["won"]]
    return _instances(tg)


def win_streak(t: Tables, n: int) -> pd.DataFrame:
    """Franchise seasons with a run of n or more regular-season wins in a row (a run does not cross seasons)."""
    tg = _regular(t.team_games).merge(t.games[["game_id", "game_date"]], on="game_id").sort_values(["team_id", "season", "game_date"])
    found = []
    for (team, season), games in tg.groupby(["team_id", "season"], sort=True):
        run = best = 0
        for won in games["won"]:
            run = run + 1 if won else 0
            best = max(best, run)
        if best >= n:
            found.append((team, season))
    return _instances(pd.DataFrame(found, columns=["team_id", "season"]))


def _finals_wins(t: Tables) -> pd.DataFrame:
    tg = t.team_games[t.team_games["game_id"].isin(_finals_game_ids(t))]
    return tg.groupby(["team_id", "season"])["won"].sum().reset_index()


def won_title(t: Tables, n: int) -> pd.DataFrame:
    """Teams that won four Finals games in a season: the champions. n is ignored."""
    wins = _finals_wins(t)
    return _instances(wins[wins["won"] >= 4])


def reached_finals(t: Tables, n: int) -> pd.DataFrame:
    """Teams that played in a Finals game in a season. n is ignored."""
    return _instances(_finals_wins(t))


# --- the templates ----------------------------------------------------------------------------------------------
# The first block is the session 4 set; the second block (session 5) adds more families so a 63-prompt set can keep
# to two thresholds per family. A threshold that gives too few or too many answers is dropped by the generator.

_P, _T = PLAYER, TEAM
register(Template("points-regular", _P, "scored {n} or more points in a regular-season game", (35, 40, 45, 50, 55, 60, 65), stat_in_game("points", "regular"), "points", "points"))
register(Template("points-playoff", _P, "scored {n} or more points in a playoff game", (25, 30, 35, 40, 45, 50), stat_in_game("points", "playoffs"), "points", "points"))
register(Template("points-finals", _P, "scored {n} or more points in a Finals game", (20, 25, 30, 35, 40), stat_in_game("points", "finals"), "points", "points"))
register(Template("triple-double-regular", _P, "recorded a triple-double in a regular-season game", (0,), triple_double("regular"), "triple-double", "triple-double"))
register(Template("triple-double-playoff", _P, "recorded a triple-double in a playoff game", (0,), triple_double("playoffs"), "triple-double", "triple-double"))
register(Template("triple-double-finals", _P, "recorded a triple-double in a Finals game", (0,), triple_double("finals"), "triple-double", "triple-double"))
register(Template("rebounds", _P, "grabbed {n} or more rebounds in a game", (16, 18, 20, 22, 24, 25, 27), stat_in_game("reb"), "rebounds", "rebounds"))
register(Template("assists", _P, "recorded {n} or more assists in a game", (14, 15, 16, 18, 20, 22), stat_in_game("ast"), "assists", "assists"))
register(Template("threes", _P, "made {n} or more three-pointers in a game", (8, 9, 10, 11, 12), stat_in_game("fg3m"), "threes made", "threes"))
register(Template("blocks", _P, "blocked {n} or more shots in a game", (6, 7, 8, 9, 10, 11), stat_in_game("blk"), "blocks", "blocks"))
register(Template("steals", _P, "stole the ball {n} or more times in a game", (5, 6, 7, 8, 9), stat_in_game("stl"), "steals", "steals"))
register(Template("ppg-season", _P, "averaged {n} or more points per game in a regular season (minimum 40 games)", (20, 22, 24, 25, 26, 27, 28, 30, 32), ppg_in_season, "points per game", "points per game"))
register(Template("franchises", _P, "played for {n} or more different franchises", (4, 5, 6, 7, 8, 9), franchises_played_for, "franchises", "franchises"))

register(Template("wins-season", _T, "won {n} or more regular-season games in a season", (50, 55, 58, 60, 62, 65, 67), wins_in_season("regular"), "wins", "wins"))
register(Template("wins-playoff", _T, "won {n} or more playoff games in a single postseason", (10, 12, 14, 15, 16), wins_in_season("playoffs"), "playoff wins", "playoff wins"))
register(Template("points-regulation", _T, "scored {n} or more points in a regulation game", (140, 145, 150, 155, 160), points_in_regulation_game, "points", "team points"))
register(Template("win-margin", _T, "won a game by {n} or more points", (40, 45, 50, 55, 60), win_by_margin, "margin", "margin"))

# session 5: players, single games in other settings
register(Template("points-game7", _P, "scored {n} or more points in a Game 7", (30, 35, 40), stat_in_game("points", "game7"), "points", "points"))
register(Template("points-overtime-game", _P, "scored {n} or more points in a game that went to overtime", (40, 45, 50, 55), stat_in_game("points", "overtime"), "points", "points"))
register(Template("points-bench", _P, "scored {n} or more points in a game he did not start", (30, 35, 40, 45), stat_in_game("points", "bench"), "points", "points"))
register(Template("points-loss", _P, "scored {n} or more points in a game his team lost", (45, 50, 55, 60), stat_in_game("points", "loss"), "points", "points"))
register(Template("points-road", _P, "scored {n} or more points in a road game", (45, 50, 55, 60), stat_in_game("points", "road"), "points", "points"))
register(Template("rebounds-playoff", _P, "grabbed {n} or more rebounds in a playoff game", (16, 18, 20, 22), stat_in_game("reb", "playoffs"), "rebounds", "rebounds"))
register(Template("rebounds-finals", _P, "grabbed {n} or more rebounds in a Finals game", (14, 16, 18, 20), stat_in_game("reb", "finals"), "rebounds", "rebounds"))
register(Template("assists-playoff", _P, "recorded {n} or more assists in a playoff game", (12, 14, 16, 18), stat_in_game("ast", "playoffs"), "assists", "assists"))
register(Template("assists-finals", _P, "recorded {n} or more assists in a Finals game", (10, 12, 14), stat_in_game("ast", "finals"), "assists", "assists"))
register(Template("threes-playoff", _P, "made {n} or more three-pointers in a playoff game", (7, 8, 9, 10), stat_in_game("fg3m", "playoffs"), "threes made", "threes"))
register(Template("threes-finals", _P, "made {n} or more three-pointers in a Finals game", (6, 7, 8), stat_in_game("fg3m", "finals"), "threes made", "threes"))
register(Template("blocks-playoff", _P, "blocked {n} or more shots in a playoff game", (5, 6, 7, 8), stat_in_game("blk", "playoffs"), "blocks", "blocks"))
register(Template("steals-playoff", _P, "stole the ball {n} or more times in a playoff game", (4, 5, 6, 7), stat_in_game("stl", "playoffs"), "steals", "steals"))
register(Template("offensive-rebounds", _P, "grabbed {n} or more offensive rebounds in a game", (9, 10, 11, 12, 14), stat_in_game("oreb"), "offensive rebounds", "offensive rebounds"))
register(Template("free-throws", _P, "made {n} or more free throws in a game", (18, 20, 22, 24), stat_in_game("ftm"), "free throws made", "free throws"))
register(Template("turnovers", _P, "committed {n} or more turnovers in a game", (8, 9, 10, 11), stat_in_game("tov"), "turnovers", "turnovers"))
register(Template("shots-taken", _P, "took {n} or more shots from the field in a game", (35, 38, 40, 42), stat_in_game("fga"), "field goal attempts", "shots taken"))
register(Template("minutes", _P, "played {n} or more minutes in a game", (55, 58, 60), stat_in_game("minutes"), "minutes", "minutes"))
register(Template("perfect-shooting", _P, "made {n} or more field goals in a game without a miss", (8, 9, 10, 11), perfect_shooting, "field goals, no misses", "perfect shooting"))
register(Template("five-by-n", _P, "recorded at least {n} points, rebounds, assists, steals and blocks in the same game", (3, 4, 5), at_least_n_of_everything, "of each of five stats", "all-around"))
register(Template("points-and-rebounds", _P, "scored 30 or more points and grabbed 15 or more rebounds in the same game", (0,), combo_in_game({"points": 30, "reb": 15}), "30 points and 15 rebounds", "points"))
register(Template("points-and-assists", _P, "scored 30 or more points and recorded 10 or more assists in the same game", (0,), combo_in_game({"points": 30, "ast": 10}), "30 points and 10 assists", "points"))
# session 5: players, whole seasons
register(Template("rebounds-per-game", _P, "averaged {n} or more rebounds per game in a regular season (minimum 40 games)", (10, 11, 12, 13), avg_in_season("reb"), "rebounds per game", "rebounds"))
register(Template("assists-per-game", _P, "averaged {n} or more assists per game in a regular season (minimum 40 games)", (8, 9, 10, 11), avg_in_season("ast"), "assists per game", "assists"))
register(Template("steals-per-game", _P, "averaged {n} or more steals per game in a regular season (minimum 40 games)", (2, 3), avg_in_season("stl"), "steals per game", "steals"))
register(Template("blocks-per-game", _P, "averaged {n} or more blocks per game in a regular season (minimum 40 games)", (2, 3), avg_in_season("blk"), "blocks per game", "blocks"))
register(Template("double-double-average", _P, "averaged a double-double (10 or more points and 10 or more rebounds per game) in a regular season (minimum 40 games)", (0,), double_double_average, "double-double average", "rebounds"))

# session 5: teams
register(Template("losses-season", _T, "lost {n} or more regular-season games in a season", (55, 60, 62, 65, 67, 70), losses_in_season, "losses", "losses"))
register(Template("road-wins", _T, "won {n} or more road games in a regular season", (26, 28, 30, 32), wins_at("away"), "road wins", "venue wins"))
register(Template("home-wins", _T, "won {n} or more home games in a regular season", (36, 38, 39, 40), wins_at("home"), "home wins", "venue wins"))
register(Template("points-playoff-team", _T, "scored {n} or more points in a playoff game", (130, 135, 140, 145, 150), points_in_game("playoffs"), "points", "team points"))
register(Template("points-any-game", _T, "scored {n} or more points in a game, overtime included", (150, 155, 160, 165), points_in_game("any"), "points", "team points"))
register(Template("win-margin-playoff", _T, "won a playoff game by {n} or more points", (35, 40, 45), win_by_margin_in("playoffs"), "margin", "margin"))
register(Template("held-opponent", _T, "held an opponent to {n} or fewer points in a game", (55, 60, 65, 70), held_opponent_to, "points allowed (at most)", "points allowed"))
register(Template("threes-team", _T, "made {n} or more three-pointers as a team in a game", (24, 26, 28, 30), team_stat_in_game("fg3m"), "threes made", "team threes"))
register(Template("steals-team", _T, "recorded {n} or more steals as a team in a game", (18, 20, 22, 24), team_stat_in_game("stl"), "steals", "team steals"))
register(Template("overtime-wins", _T, "won a game that went to {n} or more overtimes", (2, 3, 4), overtime_wins, "overtimes", "overtimes"))
register(Template("win-streak", _T, "won {n} or more regular-season games in a row", (14, 16, 18, 20, 22), win_streak, "wins in a row", "streaks"))
register(Template("champion", _T, "won the NBA championship", (0,), won_title, "titles", "finals"))
register(Template("reached-finals", _T, "reached the NBA Finals", (0,), reached_finals, "Finals", "finals"))
