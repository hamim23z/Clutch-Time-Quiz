"""Raw column names in one place.

The sportsdataverse files differ slightly from season to season (see docs/data-source.md).
Everything downstream uses the canonical names on the left; this is the only module that
knows the raw names. Add an alias here if a season spells a column differently.
"""
from __future__ import annotations

import pandas as pd

# canonical name -> raw names to try, in order
ALIASES: dict[str, tuple[str, ...]] = {
    "game_id": ("game_id",),
    "season": ("season",),
    "season_type": ("season_type",),
    "game_date": ("game_date",),
    "play_order": ("game_play_number",),
    "period": ("period_number", "period", "qtr"),
    "secs_period": ("start_quarter_seconds_remaining",),
    "secs_game": ("start_game_seconds_remaining",),
    "home_score": ("home_score",),
    "away_score": ("away_score",),
    "type_text": ("type_text",),
    "text": ("text",),
    "team_id": ("team_id",),
    "shooting_play": ("shooting_play",),
    "scoring_play": ("scoring_play",),
    "home_team_id": ("home_team_id",),
    "away_team_id": ("away_team_id",),
    "home_team_name": ("home_team_name",),
    "home_team_mascot": ("home_team_mascot",),
    "home_team_abbrev": ("home_team_abbrev",),
    "away_team_name": ("away_team_name",),
    "away_team_mascot": ("away_team_mascot",),
    "away_team_abbrev": ("away_team_abbrev",),
}


def standardize(raw: pd.DataFrame) -> pd.DataFrame:
    """Return a frame with only the canonical columns. Raises if one cannot be found."""
    picked: dict[str, pd.Series] = {}
    missing: list[str] = []
    for canonical, names in ALIASES.items():
        found = next((n for n in names if n in raw.columns), None)
        if found is None:
            missing.append(canonical)
        else:
            picked[canonical] = raw[found]
    if missing:
        raise KeyError(f"raw play-by-play is missing columns for: {', '.join(missing)}")
    out = pd.DataFrame(picked)
    out["game_date"] = out["game_date"].astype(str)
    out["text"] = out["text"].fillna("").astype(str)
    out["type_text"] = out["type_text"].fillna("").astype(str)
    out["shooting_play"] = out["shooting_play"].fillna(False).astype(bool)
    out["scoring_play"] = out["scoring_play"].fillna(False).astype(bool)
    return out
