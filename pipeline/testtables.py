"""A small seeded set of processed tables for the fame, template and generator tests (no downloads needed).

4 franchises that play (plus 2 that do not), 40 players, seasons 2002 to 2005. Each season has 12 regular-season games, 5 playoff games and one
Finals game (a playoff game with is_finals True). Franchise 2 played under a historical name until 2005 and franchise
4 until 2003, so the team tier rule has both cases. Stat lines are random with some deliberately large ones, so every
template finds qualifiers at small thresholds.
"""
from __future__ import annotations

import random

import pandas as pd

from templates import Tables

SEASONS = (2002, 2003, 2004, 2005)
N_PLAYERS = 40
STAT_COLS = ["points", "reb", "ast", "stl", "blk", "fg3m"]


def make_teams() -> pd.DataFrame:
    def entry(name: str, seasons: list[int]) -> dict:
        return {"name": name, "location": name, "nickname": name, "abbreviation": name[:3].upper(),
                "seasons": seasons, "first_season": min(seasons), "last_season": max(seasons)}

    rows = [
        (1, "Alpha", [entry("Alpha", [2002, 2003, 2004, 2005])]),
        (2, "Beta", [entry("Old Beta", [2002, 2003, 2004, 2005][:3]), entry("Beta", [2005])]),
        (3, "Gamma", [entry("Gamma", [2002, 2003, 2004, 2005])]),
        (4, "Delta", [entry("Prior Delta", [2002, 2003]), entry("Delta", [2004, 2005])]),
        # franchises 5 and 6 play no games in the fixture; they let team prompts reach the 5-answer minimum
        (5, "Epsilon", [entry("Epsilon", [2002, 2003, 2004, 2005])]),
        (6, "Zeta", [entry("Zeta", [2002, 2003, 2004, 2005])]),
    ]
    return pd.DataFrame({
        "team_id": [r[0] for r in rows], "current_name": [r[1] for r in rows],
        "abbreviation": [r[1][:3].upper() for r in rows], "first_season": 2002, "last_season": 2005,
        "names": [r[2] for r in rows],
    })


def make_players() -> pd.DataFrame:
    ids = list(range(1, N_PLAYERS + 1))
    return pd.DataFrame({"player_id": ids, "display_name": [f"Player {i}" for i in ids],
                         "unique_name": [f"Player {i}" for i in ids]})


def _stat_line(rng: random.Random) -> dict[str, int]:
    if rng.random() < 0.15:  # a big night: double digits in everything
        return {"points": rng.randint(10, 45), "reb": rng.randint(10, 22), "ast": rng.randint(10, 16),
                "stl": rng.randint(0, 8), "blk": rng.randint(0, 8), "fg3m": rng.randint(0, 10)}
    return {"points": rng.randint(0, 30), "reb": rng.randint(0, 14), "ast": rng.randint(0, 11),
            "stl": rng.randint(0, 5), "blk": rng.randint(0, 5), "fg3m": rng.randint(0, 6)}


def team_of(player_id: int, season: int) -> int:
    """Players move: players whose id is divisible by 3 change franchise every season, others stay put."""
    shift = (season - SEASONS[0]) if player_id % 3 == 0 else 0
    return (player_id + shift) % 4 + 1


def make_tables(seed: int = 7, min_season_games: int = 3) -> Tables:
    rng = random.Random(seed)
    games, team_games, player_games = [], [], []
    next_id = 1000
    for season in SEASONS:
        plan = [("regular", False)] * 12 + [("playoffs", False)] * 5 + [("playoffs", True)]
        for number, (season_type, finals) in enumerate(plan):
            gid = f"g{next_id}"
            next_id += 1
            home, away = rng.sample([1, 2, 3, 4], 2)
            scores = {home: rng.randint(80, 165), away: rng.randint(80, 165)}
            if scores[home] == scores[away]:
                scores[home] += 1
            periods = rng.choice([4, 4, 4, 5])
            games.append({"game_id": gid, "season": season, "season_type": season_type, "home_team_id": home,
                          "away_team_id": away, "home_score": scores[home], "away_score": scores[away],
                          "periods": periods, "overtime": periods > 4, "is_finals": finals})
            for team, opp, side in ((home, away, "home"), (away, home, "away")):
                team_games.append({"game_id": gid, "season": season, "season_type": season_type, "team_id": team,
                                   "opponent_team_id": opp, "home_away": side, "team_score": scores[team],
                                   "opponent_score": scores[opp], "won": scores[team] > scores[opp]})
                roster = [p for p in range(1, N_PLAYERS + 1) if team_of(p, season) == team]
                for p in rng.sample(roster, 5):
                    player_games.append({"game_id": gid, "season": season, "season_type": season_type,
                                         "player_id": p, "team_id": team, "opponent_team_id": opp, **_stat_line(rng)})
    pg = pd.DataFrame(player_games)
    pg[STAT_COLS] = pg[STAT_COLS].astype("Int16")
    return Tables(
        players=make_players(), teams=make_teams(), games=pd.DataFrame(games), player_games=pg,
        team_games=pd.DataFrame(team_games), min_season_games=min_season_games,
    )


NO_OVERRIDES = pd.DataFrame({"athlete_id": pd.Series([], dtype="int64"), "tier": pd.Series([], dtype="int64"), "reason": []})
