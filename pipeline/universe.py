"""The universe: every player and team the autocomplete and the answer matcher know about.

Players are named by their `unique_name` (people who share a display name carry the seasons they played, for
example 'Mike James (2002-2014)') and keep every spelling variant and hand-written alias as aliases. Teams are named
by their current franchise name; their aliases are every other name the franchise used, its nicknames, unique
city names, abbreviations of three or more letters, and the short forms in pipeline/data/team_aliases.csv.

An alias that more than one entry claims, or that is another entry's name, is dropped from every claimant: the
matcher must never guess between two entries on an alias. The dropped ones are returned so the export can report them.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from matchnorm import base_name, normalize
from players import apply_aliases, load_aliases

PLAYER_PREFIX, TEAM_PREFIX = "pl-", "tm-"
TEAM_ALIASES_PATH = Path(__file__).resolve().parent / "data" / "team_aliases.csv"
MIN_ABBREVIATION = 3


def _clean(candidates: list[str], own_name: str) -> list[str]:
    """Distinct aliases (by the matcher's reading), none the same as the entry's own name."""
    own = normalize(base_name(own_name), True)
    seen, out = {own}, []
    for text in candidates:
        key = normalize(text, True)
        if key and key not in seen:
            seen.add(key)
            out.append(text)
    return out


def player_entries(players: pd.DataFrame, aliases: pd.DataFrame) -> list[dict]:
    """One entry per athlete id. `aliases` is the hand-written alias file; it is checked against the players."""
    attached = apply_aliases(players.drop(columns=["aliases"], errors="ignore"), aliases)
    out = []
    for r in attached.itertuples():
        variants = [v for v in r.variants if v != r.display_name]
        out.append({
            "id": f"{PLAYER_PREFIX}{int(r.player_id)}", "name": r.unique_name,
            "aliases": _clean(variants + list(r.aliases), r.unique_name),
        })
    return sorted(out, key=lambda e: e["name"])


def load_team_aliases(path: Path = TEAM_ALIASES_PATH) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str)


def team_entries(teams: pd.DataFrame, extra: pd.DataFrame) -> list[dict]:
    names = set(teams["current_name"])
    unknown = sorted(set(extra["team"]) - names)
    if unknown:
        raise ValueError(f"team_aliases.csv names franchises that are not in the data: {unknown}")
    locations: dict[str, set[int]] = {}
    for r in teams.itertuples():
        for e in r.names:
            locations.setdefault(normalize(e["location"]), set()).add(int(r.team_id))
    short = extra.groupby("team")["alias"].apply(list).to_dict()
    out = []
    for r in teams.itertuples():
        candidates: list[str] = []
        for e in r.names:
            candidates += [e["name"], e["nickname"]]
            if len(locations[normalize(e["location"])]) == 1:
                candidates.append(e["location"])
            if len(e["abbreviation"]) >= MIN_ABBREVIATION:
                candidates.append(e["abbreviation"])
        candidates += short.get(r.current_name, [])
        out.append({"id": f"{TEAM_PREFIX}{int(r.team_id)}", "name": r.current_name, "aliases": _clean(candidates, r.current_name)})
    return sorted(out, key=lambda e: e["name"])


def drop_contested_aliases(entries: list[dict]) -> list[tuple[str, str, str]]:
    """Remove aliases claimed by several entries or equal to another entry's name. Returns (entry id, alias, why)."""
    name_owner: dict[str, set[str]] = {}
    alias_owner: dict[str, set[str]] = {}
    for e in entries:
        name_owner.setdefault(normalize(base_name(e["name"]), True), set()).add(e["id"])
        for a in e["aliases"]:
            alias_owner.setdefault(normalize(a, True), set()).add(e["id"])
    dropped = []
    for e in entries:
        keep = []
        for a in e["aliases"]:
            key = normalize(a, True)
            others = (alias_owner[key] | name_owner.get(key, set())) - {e["id"]}
            if others:
                dropped.append((e["id"], a, "also claimed by " + ", ".join(sorted(others)[:3])))
            else:
                keep.append(a)
        e["aliases"] = keep
    return dropped


def build_universe(players: pd.DataFrame, teams: pd.DataFrame, aliases: pd.DataFrame, team_aliases: pd.DataFrame) -> tuple[dict, list[tuple[str, str, str]]]:
    p, t = player_entries(players, aliases), team_entries(teams, team_aliases)
    dropped = drop_contested_aliases(p + t)
    return {"players": p, "teams": t}, dropped
