"""Games stage: decide which games the game uses.

Only final regular-season and playoff games between two NBA franchises are kept. Everything
else is counted by reason and dropped: postponed games, the All-Star game, the NBA Cup final,
play-in games, and exhibition games with a non-NBA side (Rising Stars, USA, World, All-Star teams).
Games with no usable box score rows are skipped and reported.
"""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

# ESPN team ids 1-30 are the 30 NBA franchises (ids are stable across moves and renames). The 14
# non-NBA sides in the team box (Team LeBron, USA, World, ...) all have ids above 30.
NBA_TEAM_IDS = frozenset(range(1, 31))
REGULAR, PLAYOFFS = "regular", "playoffs"

EXCLUSION_REASONS = ["not_final", "all_star", "cup_final", "play_in", "non_nba_team", "other_type"]
GAME_COLUMNS = [
    "game_id", "season", "season_type", "game_date", "home_team_id", "away_team_id", "home_score", "away_score",
    "periods", "overtime", "is_finals", "series_game",
]


@dataclass
class GameSelection:
    games: pd.DataFrame  # kept games
    skipped: pd.DataFrame  # game_id, season, season_type, game_date, reason
    excluded: dict[str, int]  # exclusion reason -> number of games


def _reason(row: pd.Series) -> str:
    """Why a schedule row is not a regular-season or playoff game, or '' if it is one."""
    if row["status_type_name"] != "STATUS_FINAL":
        return "not_final"
    if row["type_abbreviation"] == "ALLSTAR":
        return "all_star"
    if row["type_abbreviation"] == "CC":
        return "cup_final"
    if row["season_type"] == 5:
        return "play_in"
    if row["home_id"] not in NBA_TEAM_IDS or row["away_id"] not in NBA_TEAM_IDS:
        return "non_nba_team"
    if row["season_type"] == 2 and row["type_abbreviation"] == "STD":
        return ""
    if row["season_type"] == 3:
        return ""
    return "other_type"


def add_series_info(games: pd.DataFrame) -> pd.DataFrame:
    """Add is_finals and series_game (1-based game number inside the series) to playoff games.

    The schedule labels Finals games only from 2004 and its game-number notes only from 2020, so both are
    derived: the Finals are the series between the two teams in the last playoff game of the season, and
    a game's number is its order by date within the two teams' series.
    """
    out = games.copy()
    out["is_finals"] = False
    out["series_game"] = pd.array([pd.NA] * len(out), dtype="Int8")
    po = out[out["season_type"] == PLAYOFFS].sort_values(["game_date", "game_id"])
    if po.empty:
        return out
    pair = po[["home_team_id", "away_team_id"]].apply(lambda r: f"{min(r.iloc[0], r.iloc[1])}-{max(r.iloc[0], r.iloc[1])}", axis=1)
    po = po.assign(pair=pair)
    last_pair = po.groupby("season")["pair"].last()
    po["is_finals"] = po["pair"] == po["season"].map(last_pair)
    po["series_game"] = (po.groupby(["season", "pair"]).cumcount() + 1).astype("Int8")
    out.loc[po.index, "is_finals"] = po["is_finals"]
    out.loc[po.index, "series_game"] = po["series_game"]
    return out


def select_games(sched: pd.DataFrame, team: pd.DataFrame, player: pd.DataFrame) -> GameSelection:
    """Pick the games to keep from one season's raw schedule, team box and player box.

    team and player are the raw (slimmed) tables. A game is skipped, and listed, when it has no team
    rows for both NBA sides or no player rows with a points value.
    """
    s = sched.drop_duplicates("game_id").copy()
    s["reason"] = s.apply(_reason, axis=1)
    excluded = {r: int((s["reason"] == r).sum()) for r in EXCLUSION_REASONS}
    cand = s[s["reason"] == ""].copy()
    cand["season_type"] = cand["season_type"].map({2: REGULAR, 3: PLAYOFFS})
    cand["game_date"] = pd.to_datetime(cand["game_date"]).dt.date
    cand["periods"] = cand["status_period"].astype("int8")
    cand["overtime"] = cand["periods"] > 4
    cand = cand.rename(columns={"home_id": "home_team_id", "away_id": "away_team_id"})
    cand = add_series_info(cand)

    team_rows = team[team["team_id"].isin(NBA_TEAM_IDS)].groupby("game_id").size()
    played_rows = player[player["points"].notna() & player["athlete_id"].notna()].groupby("game_id").size()
    cand["_team_rows"] = cand["game_id"].map(team_rows).fillna(0)
    cand["_player_rows"] = cand["game_id"].map(played_rows).fillna(0)
    no_team, no_player = cand["_team_rows"] < 2, cand["_player_rows"] == 0
    reason = pd.Series("", index=cand.index)
    reason[no_team & ~no_player] = "no_team_rows"
    reason[no_player & ~no_team] = "no_player_rows"
    reason[no_team & no_player] = "no_team_and_player_rows"
    skipped = cand[reason != ""][["game_id", "season", "season_type", "game_date"]].assign(reason=reason[reason != ""])
    kept = cand[reason == ""]
    games = kept[GAME_COLUMNS].sort_values(["game_date", "game_id"]).reset_index(drop=True)
    return GameSelection(games, skipped.sort_values("game_id").reset_index(drop=True), excluded)
