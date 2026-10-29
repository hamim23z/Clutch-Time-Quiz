"""Independent brute-force answers for every template: plain Python loops over table rows, written without
looking at templates.py. Used by the tests (on the small fixture) and by the export check (on the real tables).

Each function takes (rows, n) and returns a set: player ids for a player template, (team_id, season) pairs for a
team template. `BRUTE[key]` has one function per registered template; a test fails if one is missing.
"""
from __future__ import annotations

import math
from typing import Callable

from templates import Tables

NAN = float("nan")


def _col(df, name):
    s = df[name]
    if str(s.dtype) in ("bool", "boolean", "str", "object", "string") or "str" in str(s.dtype):
        return s.tolist()
    return s.to_numpy(dtype="float64", na_value=NAN).tolist()


class Rows:
    """Row-wise access to a Tables object. Missing numbers are NaN, which fails every comparison."""

    def __init__(self, tables: Tables):
        self.tables = tables
        self.min_season_games = tables.min_season_games
        g = tables.games
        self.game = {
            gid: {"periods": per, "overtime": ot, "finals": fin, "series": ser, "date": str(d), "type": st}
            for gid, per, ot, fin, ser, d, st in zip(
                g["game_id"], _col(g, "periods"), g["overtime"], g["is_finals"], _col(g, "series_game"), g["game_date"], g["season_type"]
            )
        }
        tg = tables.team_games
        self.team_won = {(gid, t): bool(w) for gid, t, w in zip(tg["game_id"], tg["team_id"], tg["won"])}

    def player(self, *cols):
        df = self.tables.player_games
        return zip(*[_col(df, c) for c in cols])

    def team(self, *cols):
        df = self.tables.team_games
        return zip(*[_col(df, c) for c in cols])


def _in_scope(rows: Rows, scope: str, gid, season_type, started, home_away, team) -> bool:
    g = rows.game[gid]
    if scope == "any":
        return True
    if scope in ("regular", "playoffs"):
        return season_type == scope
    if scope == "finals":
        return g["finals"]
    if scope == "game7":
        return g["series"] == 7
    if scope == "overtime":
        return g["overtime"]
    if scope == "bench":
        return not started
    if scope == "road":
        return home_away == "away"
    if scope == "loss":
        return not rows.team_won[(gid, team)]
    raise ValueError(scope)


def stat_players(col: str, scope: str = "any") -> Callable:
    def brute(rows: Rows, n: int) -> set:
        found = set()
        for pid, value, gid, stype, started, side, team in rows.player("player_id", col, "game_id", "season_type", "started", "home_away", "team_id"):
            if value >= n and _in_scope(rows, scope, gid, stype, started, side, team):
                found.add(int(pid))
        return found
    return brute


def combo_players(minimums: dict[str, int]) -> Callable:
    def brute(rows: Rows, n: int) -> set:
        cols = list(minimums)
        found = set()
        for pid, *values in rows.player("player_id", *cols):
            if all(v >= minimums[c] for c, v in zip(cols, values)):
                found.add(int(pid))
        return found
    return brute


def triple_double_players(scope: str) -> Callable:
    def brute(rows: Rows, n: int) -> set:
        found = set()
        for pid, a, b, c, d, e, gid, stype, started, side, team in rows.player("player_id", "points", "reb", "ast", "stl", "blk", "game_id", "season_type", "started", "home_away", "team_id"):
            if sum(1 for v in (a, b, c, d, e) if v >= 10) >= 3 and _in_scope(rows, scope, gid, stype, started, side, team):
                found.add(int(pid))
        return found
    return brute


def five_by_n(rows: Rows, n: int) -> set:
    return {int(pid) for pid, *v in rows.player("player_id", "points", "reb", "ast", "stl", "blk") if min(v) >= n}


def perfect_shooting(rows: Rows, n: int) -> set:
    return {int(pid) for pid, made, tried in rows.player("player_id", "fgm", "fga") if made >= n and tried == made}


def _season_sums(rows: Rows, cols: list[str]) -> dict:
    sums: dict = {}
    for pid, season, stype, *values in rows.player("player_id", "season", "season_type", *cols):
        if stype != "regular":
            continue
        entry = sums.setdefault((int(pid), int(season)), [0] + [0.0] * len(cols))
        entry[0] += 1
        for i, v in enumerate(values):
            if not math.isnan(v):
                entry[i + 1] += v
    return sums


def average_players(col: str) -> Callable:
    def brute(rows: Rows, n: int) -> set:
        return {p for (p, s), (games, total) in _season_sums(rows, [col]).items()
                if games >= rows.min_season_games and total / games >= n}
    return brute


def double_double_average(rows: Rows, n: int) -> set:
    return {p for (p, s), (games, pts, reb) in _season_sums(rows, ["points", "reb"]).items()
            if games >= rows.min_season_games and pts / games >= 10 and reb / games >= 10}


def franchise_players(rows: Rows, n: int) -> set:
    teams: dict = {}
    for pid, team in rows.player("player_id", "team_id"):
        teams.setdefault(int(pid), set()).add(int(team))
    return {p for p, t in teams.items() if len(t) >= n}


# --- teams ------------------------------------------------------------------------------------------------------

def _team_counts(rows: Rows, keep: Callable, count_losses: bool = False) -> dict:
    counts: dict = {}
    for gid, team, season, stype, side, won in rows.team("game_id", "team_id", "season", "season_type", "home_away", "won"):
        if keep(stype, side):
            key = (int(team), int(season))
            counts[key] = counts.get(key, 0) + (1 if (bool(won) != count_losses) else 0)
    return counts


def season_wins(season_type: str) -> Callable:
    return lambda rows, n: {k for k, w in _team_counts(rows, lambda st, side: st == season_type).items() if w >= n}


def season_losses(rows: Rows, n: int) -> set:
    return {k for k, w in _team_counts(rows, lambda st, side: st == "regular", count_losses=True).items() if w >= n}


def venue_wins(side_wanted: str) -> Callable:
    return lambda rows, n: {k for k, w in _team_counts(rows, lambda st, side: st == "regular" and side == side_wanted).items() if w >= n}


def team_games_where(test: Callable) -> Callable:
    """Teams with a game where test(score, opponent_score, season_type, periods, won, row_stat...) is true."""
    def brute(rows: Rows, n: int) -> set:
        found = set()
        for gid, team, season, stype, score, opp, won, fg3m, stl in rows.team("game_id", "team_id", "season", "season_type", "team_score", "opponent_score", "won", "fg3m", "stl"):
            if test(n, rows.game[gid], stype, score, opp, bool(won), fg3m, stl):
                found.add((int(team), int(season)))
        return found
    return brute


def streaks(rows: Rows, n: int) -> set:
    by_team: dict = {}
    for gid, team, season, stype, won in rows.team("game_id", "team_id", "season", "season_type", "won"):
        if stype == "regular":
            by_team.setdefault((int(team), int(season)), []).append((rows.game[gid]["date"], bool(won)))
    found = set()
    for key, games in by_team.items():
        run = best = 0
        for _, won in sorted(games):
            run = run + 1 if won else 0
            best = max(best, run)
        if best >= n:
            found.add(key)
    return found


def finals_wins(rows: Rows) -> dict:
    wins: dict = {}
    for gid, team, season, won in rows.team("game_id", "team_id", "season", "won"):
        if rows.game[gid]["finals"]:
            wins[(int(team), int(season))] = wins.get((int(team), int(season)), 0) + (1 if won else 0)
    return wins


# template key -> brute-force function
BRUTE: dict[str, Callable[[Rows, int], set]] = {
    "points-regular": stat_players("points", "regular"),
    "points-playoff": stat_players("points", "playoffs"),
    "points-finals": stat_players("points", "finals"),
    "triple-double-regular": triple_double_players("regular"),
    "triple-double-playoff": triple_double_players("playoffs"),
    "triple-double-finals": triple_double_players("finals"),
    "rebounds": stat_players("reb"),
    "assists": stat_players("ast"),
    "threes": stat_players("fg3m"),
    "blocks": stat_players("blk"),
    "steals": stat_players("stl"),
    "ppg-season": average_players("points"),
    "franchises": franchise_players,
    "points-game7": stat_players("points", "game7"),
    "points-overtime-game": stat_players("points", "overtime"),
    "points-bench": stat_players("points", "bench"),
    "points-loss": stat_players("points", "loss"),
    "points-road": stat_players("points", "road"),
    "rebounds-playoff": stat_players("reb", "playoffs"),
    "rebounds-finals": stat_players("reb", "finals"),
    "assists-playoff": stat_players("ast", "playoffs"),
    "assists-finals": stat_players("ast", "finals"),
    "threes-playoff": stat_players("fg3m", "playoffs"),
    "threes-finals": stat_players("fg3m", "finals"),
    "blocks-playoff": stat_players("blk", "playoffs"),
    "steals-playoff": stat_players("stl", "playoffs"),
    "offensive-rebounds": stat_players("oreb"),
    "free-throws": stat_players("ftm"),
    "turnovers": stat_players("tov"),
    "shots-taken": stat_players("fga"),
    "minutes": stat_players("minutes"),
    "perfect-shooting": perfect_shooting,
    "five-by-n": five_by_n,
    "points-and-rebounds": combo_players({"points": 30, "reb": 15}),
    "points-and-assists": combo_players({"points": 30, "ast": 10}),
    "rebounds-per-game": average_players("reb"),
    "assists-per-game": average_players("ast"),
    "steals-per-game": average_players("stl"),
    "blocks-per-game": average_players("blk"),
    "double-double-average": double_double_average,
    "wins-season": season_wins("regular"),
    "wins-playoff": season_wins("playoffs"),
    "points-regulation": team_games_where(lambda n, g, st, score, opp, won, f3, stl: g["periods"] == 4 and score >= n),
    "win-margin": team_games_where(lambda n, g, st, score, opp, won, f3, stl: won and score - opp >= n),
    "losses-season": season_losses,
    "road-wins": venue_wins("away"),
    "home-wins": venue_wins("home"),
    "points-playoff-team": team_games_where(lambda n, g, st, score, opp, won, f3, stl: st == "playoffs" and score >= n),
    "points-any-game": team_games_where(lambda n, g, st, score, opp, won, f3, stl: score >= n),
    "win-margin-playoff": team_games_where(lambda n, g, st, score, opp, won, f3, stl: st == "playoffs" and won and score - opp >= n),
    "held-opponent": team_games_where(lambda n, g, st, score, opp, won, f3, stl: opp <= n),
    "threes-team": team_games_where(lambda n, g, st, score, opp, won, f3, stl: f3 >= n),
    "steals-team": team_games_where(lambda n, g, st, score, opp, won, f3, stl: stl >= n),
    "overtime-wins": team_games_where(lambda n, g, st, score, opp, won, f3, stl: won and g["periods"] - 4 >= n),
    "win-streak": streaks,
    "champion": lambda rows, n: {k for k, w in finals_wins(rows).items() if w >= 4},
    "reached-finals": lambda rows, n: set(finals_wins(rows)),
}


# --- parameterised families (pools.py): one query per (family, parameters), plain loops ----------------------------

def _players_where(rows: Rows, cols: tuple, test: Callable) -> set:
    """Player ids of rows where test(player_id, *values) is true."""
    return {int(pid) for pid, *values in rows.player("player_id", *cols) if test(*values)}


def _franchise_scope(scope: str) -> Callable:
    return lambda rows, p: _players_where(rows, ("team_id", "season_type"), lambda team, stype: team == p[0] and (scope == "any" or stype == scope))


def _two_franchises(rows: Rows, p: tuple) -> set:
    a, b = set(), set()
    for pid, team in rows.player("player_id", "team_id"):
        if team == p[0]:
            a.add(int(pid))
        elif team == p[1]:
            b.add(int(pid))
    return a & b


def _teammates(rows: Rows, p: tuple) -> set:
    star = p[0]
    together = {(gid, team) for pid, gid, team in rows.player("player_id", "game_id", "team_id") if pid == star}
    return {int(pid) for pid, gid, team in rows.player("player_id", "game_id", "team_id") if (gid, team) in together} - {star}


def _finals(test: Callable) -> Callable:
    return lambda rows, p: {int(pid) for pid, gid, three, stl, blk, season in rows.player("player_id", "game_id", "fg3m", "stl", "blk", "season")
                            if rows.game[gid]["finals"] and test(three, stl, blk, season, p)}


def _month(col: str) -> Callable:
    def brute(rows: Rows, p: tuple) -> set:
        year, month, n = p
        prefix = f"{year:04d}-{month:02d}-"
        return {int(pid) for pid, value, gid, stype in rows.player("player_id", col, "game_id", "season_type")
                if stype == "regular" and value >= n and rows.game[gid]["date"].startswith(prefix)}
    return brute


def _season(col: str) -> Callable:
    return lambda rows, p: _players_where(rows, (col, "season", "season_type"), lambda value, season, stype: stype == "regular" and season == p[0] and value >= p[1])


def _years(rows: Rows, p: tuple) -> set:
    return _players_where(rows, ("team_id", "season", "season_type"), lambda team, season, stype: team == p[0] and stype == "regular" and p[1] <= season <= p[2])


def _team_season_games(test: Callable) -> Callable:
    """Teams with a game of the given season where test(n, game_info, row) holds."""
    def brute(rows: Rows, p: tuple) -> set:
        season, n = p
        found = set()
        for gid, team, s, stype, side, score, opp, won, fg3m in rows.team("game_id", "team_id", "season", "season_type", "home_away", "team_score", "opponent_score", "won", "fg3m"):
            if s == season and test(n, rows.game[gid], stype, side, score, opp, bool(won), fg3m):
                found.add((int(team), int(s)))
        return found
    return brute


def _wins_threshold(side: str | None, season_type: str) -> Callable:
    def brute(rows: Rows, p: tuple) -> set:
        season, n = p
        wins: dict = {}
        for team, s, stype, hv, won in rows.team("team_id", "season", "season_type", "home_away", "won"):
            if s == season and stype == season_type and (side is None or hv == side):
                wins[int(team)] = wins.get(int(team), 0) + (1 if won else 0)
        return {(t, int(season)) for t, w in wins.items() if w >= n}
    return brute


def _made_playoffs(rows: Rows, p: tuple) -> set:
    return {(int(team), int(s)) for team, s, stype in rows.team("team_id", "season", "season_type") if s == p[0] and stype == "playoffs"}


def _against(kind: str) -> Callable:
    def brute(rows: Rows, p: tuple) -> set:
        return {(int(team), int(s)) for team, s, stype, opp, won in rows.team("team_id", "season", "season_type", "opponent_team_id", "won")
                if stype == "playoffs" and opp == p[0] and (kind == "played" or won)}
    return brute


BRUTE_FAMILY: dict[str, Callable[[Rows, tuple], set]] = {
    "franchise-regular": _franchise_scope("regular"),
    "franchise-playoff": _franchise_scope("playoffs"),
    "franchise-season": lambda rows, p: _players_where(rows, ("team_id", "season", "season_type"), lambda team, season, stype: team == p[0] and season == p[1] and stype == "regular"),
    "franchise-start": lambda rows, p: _players_where(rows, ("team_id", "started"), lambda team, started: team == p[0] and bool(started)),
    "franchise-bench": lambda rows, p: _players_where(rows, ("team_id", "started"), lambda team, started: team == p[0] and not started),
    "franchise-points": lambda rows, p: _players_where(rows, ("team_id", "points"), lambda team, pts: team == p[0] and pts >= p[1]),
    "franchise-years": _years,
    "franchise-playoff-season": lambda rows, p: _players_where(rows, ("team_id", "season", "season_type"), lambda team, season, stype: team == p[0] and season == p[1] and stype == "playoffs"),
    "both-franchises": _two_franchises,
    "points-against": lambda rows, p: _players_where(rows, ("opponent_team_id", "points"), lambda opp, pts: opp == p[0] and pts >= p[1]),
    "teammate": _teammates,
    "finals-appearance": _finals(lambda three, stl, blk, season, p: True),
    "finals-three": _finals(lambda three, stl, blk, season, p: three >= 1),
    "finals-steal-block": _finals(lambda three, stl, blk, season, p: stl >= 1 or blk >= 1),
    "finals-year": _finals(lambda three, stl, blk, season, p: season == p[0]),
    "month-points": _month("points"),
    "month-threes": _month("fg3m"),
    "season-points": _season("points"),
    "season-threes": _season("fg3m"),
    "season-rebounds": _season("reb"),
    "season-assists": _season("ast"),
    "made-playoffs": _made_playoffs,
    "wins-in-season": _wins_threshold(None, "regular"),
    "home-wins-in-season": _wins_threshold("home", "regular"),
    "road-wins-in-season": _wins_threshold("away", "regular"),
    "playoff-wins-in-season": _wins_threshold(None, "playoffs"),
    "regulation-points-in-season": _team_season_games(lambda n, g, st, side, score, opp, won, f3: g["periods"] == 4 and score >= n),
    "margin-in-season": _team_season_games(lambda n, g, st, side, score, opp, won, f3: won and score - opp >= n),
    "threes-in-season": _team_season_games(lambda n, g, st, side, score, opp, won, f3: f3 >= n),
    "held-opponent-in-season": _team_season_games(lambda n, g, st, side, score, opp, won, f3: opp <= n),
    "overtime-wins-in-season": _team_season_games(lambda n, g, st, side, score, opp, won, f3: won and g["periods"] - 4 >= n),
    "played-playoff-against": _against("played"),
    "beat-in-playoffs": _against("won"),
}
