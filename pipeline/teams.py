"""Teams stage: one record per franchise with every historical name and the seasons each was used."""
from __future__ import annotations

import pandas as pd

from games import NBA_TEAM_IDS
from textnorm import clean_spaces

NAME_COLUMNS = ["team_id", "season", "name", "location", "nickname", "abbreviation", "games"]
TEAM_COLUMNS = ["team_id", "current_name", "abbreviation", "first_season", "last_season", "names"]


def season_team_names(raw_team: pd.DataFrame, team_games: pd.DataFrame) -> pd.DataFrame:
    """Per (team, season, name): games played. Names come from the raw team box, cleaned of stray whitespace
    (one 2006 name has a carriage return and line feed inside it)."""
    keys = team_games[["game_id", "team_id"]]
    r = raw_team[raw_team["team_id"].isin(NBA_TEAM_IDS)].merge(keys, on=["game_id", "team_id"])
    for src, dst in (("team_display_name", "name"), ("team_location", "location"), ("team_name", "nickname"), ("team_abbreviation", "abbreviation")):
        r[dst] = r[src].map(lambda s: clean_spaces(s) if isinstance(s, str) else "")
    out = r.groupby(["team_id", "season", "name", "location", "nickname", "abbreviation"], as_index=False).size().rename(columns={"size": "games"})
    return out[NAME_COLUMNS]


def build_teams(names: pd.DataFrame) -> pd.DataFrame:
    """Franchise table. `names` is a list of {name, location, nickname, abbreviation, seasons, first_season, last_season}."""
    rows = []
    for tid, g in names.groupby("team_id"):
        entries = []
        for (name, location, nickname, abbr), h in g.groupby(["name", "location", "nickname", "abbreviation"]):
            seasons = sorted(int(s) for s in h["season"].unique())
            entries.append(
                {"name": name, "location": location, "nickname": nickname, "abbreviation": abbr,
                 "seasons": seasons, "first_season": seasons[0], "last_season": seasons[-1]}
            )
        entries.sort(key=lambda e: (e["first_season"], e["name"]))
        latest = max(entries, key=lambda e: (e["last_season"], len(e["seasons"])))
        rows.append(
            {
                "team_id": int(tid),
                "current_name": latest["name"],
                "abbreviation": latest["abbreviation"],
                "first_season": int(g["season"].min()),
                "last_season": int(g["season"].max()),
                "names": entries,
            }
        )
    return pd.DataFrame(rows, columns=TEAM_COLUMNS).sort_values("team_id").reset_index(drop=True)
