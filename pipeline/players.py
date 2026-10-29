"""Players stage: one canonical record per athlete id.

The record keeps the display name plus every spelling it has had: display names over time (Jimmy Butler,
Jimmy Butler III), and short names with accents (Nenê, Calderón, Schröder). Abbreviated short names
("J. Butler") and bare surnames are not kept; the answer matcher handles last names itself.

Athlete ids are never merged. Display names that belong to more than one id (Mike James, Corey Brewer, ...)
get a `unique_name` with the seasons played, so they can be told apart and never collapse into one answer.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from textnorm import clean_spaces, has_non_ascii, name_key

NAME_COLUMNS = ["player_id", "season", "display_name", "short_name", "games"]
PLAYER_COLUMNS = [
    "player_id", "display_name", "unique_name", "name_collision", "variants", "aliases",
    "first_season", "last_season", "seasons_played", "games_played",
]
ALIAS_COLUMNS = ["alias", "athlete_id", "canonical_name", "kind", "evidence"]


def season_player_names(player_games: pd.DataFrame, raw_player: pd.DataFrame) -> pd.DataFrame:
    """Per (player, season, display name, short name): number of games played, for the kept games.

    raw_player is the slimmed raw player table; player_games decides which rows count as played.
    """
    keys = player_games[["game_id", "player_id"]].rename(columns={"player_id": "athlete_id"})
    r = raw_player.merge(keys, on=["game_id", "athlete_id"])
    r["athlete_id"] = r["athlete_id"].astype("int64")
    r["display_name"] = r["athlete_display_name"].map(lambda s: clean_spaces(s) if isinstance(s, str) else "")
    r["short_name"] = r["athlete_short_name"].map(lambda s: clean_spaces(s) if isinstance(s, str) else "")
    out = (
        r.groupby(["athlete_id", "season", "display_name", "short_name"], as_index=False)
        .size()
        .rename(columns={"athlete_id": "player_id", "size": "games"})
    )
    return out[NAME_COLUMNS]


def _canonical_name(group: pd.DataFrame) -> str:
    """The display name used latest; ties go to the one used in more games, then alphabetically."""
    g = group[group["display_name"] != ""]
    per_name = g.groupby("display_name").agg(last=("season", "max"), games=("games", "sum")).reset_index()
    per_name = per_name.sort_values(["last", "games", "display_name"], ascending=[False, False, True])
    return str(per_name.iloc[0]["display_name"])


def _variants(group: pd.DataFrame, canonical: str) -> list[str]:
    """Canonical name first, then other display names (latest first), then accented short names."""
    g = group[group["display_name"] != ""]
    per_name = g.groupby("display_name").agg(last=("season", "max"), games=("games", "sum")).reset_index()
    per_name = per_name.sort_values(["last", "games", "display_name"], ascending=[False, False, True])
    out = [canonical] + [n for n in per_name["display_name"] if n != canonical]
    for short in sorted(set(group["short_name"]) - {""}):
        if has_non_ascii(short) and short not in out:
            out.append(short)
    return out


def _disambiguate(players: pd.DataFrame, colliding_ids: set[int]) -> pd.Series:
    """unique_name per player: the display name, plus the seasons played when the name is shared."""
    unique = players["display_name"].copy()
    shared = players["player_id"].isin(colliding_ids)

    def label(row: pd.Series) -> str:
        span = str(row["first_season"]) if row["first_season"] == row["last_season"] else f"{row['first_season']}-{row['last_season']}"
        return f"{row['display_name']} ({span})"

    unique[shared] = players[shared].apply(label, axis=1)
    # Two people with the same name and the same seasons still need telling apart: add the id.
    dup = unique[shared].duplicated(keep=False)
    ids = players.loc[dup[dup].index, "player_id"].astype(str)
    unique[dup[dup].index] = unique[dup[dup].index].str[:-1] + ", id " + ids + ")"
    return unique


def build_players(names: pd.DataFrame, aliases: pd.DataFrame | None = None, allow_missing_aliases: bool = False) -> pd.DataFrame:
    """Build the players table from per-season name rows (see season_player_names)."""
    names = names.assign(display_name=names["display_name"].map(clean_spaces), short_name=names["short_name"].map(clean_spaces))
    rows = []
    for pid, g in names.groupby("player_id"):
        canonical = _canonical_name(g)
        rows.append(
            {
                "player_id": int(pid),
                "display_name": canonical,
                "variants": _variants(g, canonical),
                "first_season": int(g["season"].min()),
                "last_season": int(g["season"].max()),
                "seasons_played": int(g["season"].nunique()),
                "games_played": int(g.groupby("season")["games"].sum().sum()),
            }
        )
    players = pd.DataFrame(rows)
    colliding = {pid for ids in _display_owners(names).values() if len(ids) > 1 for pid in ids}
    players["name_collision"] = players["player_id"].isin(colliding)
    players["unique_name"] = _disambiguate(players, colliding)
    players = apply_aliases(players, aliases, allow_missing_aliases) if aliases is not None else players.assign(aliases=[[] for _ in range(len(players))])
    return players[PLAYER_COLUMNS].sort_values("player_id").reset_index(drop=True)


def _display_owners(names: pd.DataFrame) -> dict[str, set[int]]:
    """Lowercased display name -> athlete ids that have used it (any season). Short names do not count."""
    owners: dict[str, set[int]] = {}
    for pid, display in zip(names["player_id"], names["display_name"]):
        if display:
            owners.setdefault(name_key(display), set()).add(int(pid))
    return owners


def shared_names(names: pd.DataFrame) -> dict[str, list[int]]:
    """Display names (lowercased) owned by more than one athlete id, for the notes."""
    return {k: sorted(v) for k, v in sorted(_display_owners(names).items()) if len(v) > 1}


def load_aliases(path: Path) -> pd.DataFrame:
    """Read the hand-written aliases file (pipeline/data/aliases.csv)."""
    df = pd.read_csv(path, dtype={"alias": str, "canonical_name": str, "kind": str, "evidence": str})
    missing = [c for c in ALIAS_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"{path}: missing columns {missing}")
    df["alias"] = df["alias"].map(clean_spaces)
    df["canonical_name"] = df["canonical_name"].map(clean_spaces)
    return df[ALIAS_COLUMNS]


def apply_aliases(players: pd.DataFrame, aliases: pd.DataFrame, allow_missing: bool = False) -> pd.DataFrame:
    """Attach aliases to players, refusing anything that cannot be checked against the data.

    Every row must point at an athlete id that exists, name that player correctly (a display name or
    spelling in the data), and must not be a name or alias already belonging to anyone else.
    """
    out = players.copy()
    by_id = {int(r.player_id): r for r in out.itertuples()}
    taken: dict[str, int] = {}
    for r in out.itertuples():
        for v in r.variants:
            taken.setdefault(name_key(v), int(r.player_id))
    attached: dict[int, list[str]] = {}
    for row in aliases.itertuples():
        pid = int(row.athlete_id)
        if pid not in by_id:
            if allow_missing:
                continue
            raise ValueError(f"alias {row.alias!r}: athlete id {pid} is not in the data")
        known = {name_key(v) for v in by_id[pid].variants}
        if name_key(row.canonical_name) not in known:
            raise ValueError(f"alias {row.alias!r}: {row.canonical_name!r} is not a name of athlete {pid} ({by_id[pid].variants})")
        key = name_key(row.alias)
        if key in known:
            raise ValueError(f"alias {row.alias!r} is already a spelling of athlete {pid}")
        if key in taken:
            raise ValueError(f"alias {row.alias!r} already belongs to athlete {taken[key]}")
        taken[key] = pid
        attached.setdefault(pid, []).append(row.alias)
    out["aliases"] = [attached.get(int(p), []) for p in out["player_id"]]
    return out
