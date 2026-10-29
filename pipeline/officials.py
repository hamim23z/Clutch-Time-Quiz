"""Officials stage: clean referee names, merge spelling variants, and flag games with problems.

The data has names only: no ids, no crew chief. The same person appears under several spellings
(J.B. DeRosa, JB DeRosa, Joe DeRosa), so names are merged when, and only when:

  1. the last names are the same (ignoring dots, middle initials and Jr./Sr./II/III), and
  2. the first names are compatible: the same after dropping dots (J.B. = JB), one is the start of the other
     (Steve, Steven), or one is a set of initials and the other is a name starting with the same letter
     (JB, Joe), and
  3. the data does not show them as two people: if the two spellings turn up in the same game in
     different slots more often than in the same slot, they are two people. The same slot listing two spellings
     is the data's duplicate-listing glitch (one person).

Every merge, with its evidence, is returned so it can be reviewed in docs/pipeline-notes.md.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from textnorm import clean_spaces

SUFFIXES = {"jr", "sr", "ii", "iii", "iv"}
OFFICIAL_COLUMNS = ["game_id", "season", "official_order", "official_name", "raw_name", "slot_conflict", "slot_shared"]
STATUS_OK, STATUS_NONE, STATUS_CONFLICT = "ok", "none", "slot_conflict"


@dataclass
class OfficialsResult:
    officials: pd.DataFrame
    game_status: pd.DataFrame  # game_id, officials_status, n_officials
    merges: list[dict] = field(default_factory=list)  # one per person that absorbed spellings
    whitespace_fixes: list[dict] = field(default_factory=list)  # raw spellings that only differed by spaces
    kept_separate: list[tuple[str, str]] = field(default_factory=list)  # look alike, not merged
    stats: dict[str, int] = field(default_factory=dict)


def _tokens(name: str) -> tuple[str, str]:
    """(first token as written, last-name key). Middle initials and suffixes are ignored for the key."""
    parts = clean_spaces(name).split()
    core = [p for p in parts if p.replace(".", "").casefold() not in SUFFIXES]
    first = core[0] if core else ""
    last = core[-1].replace(".", "").casefold() if core else ""
    return first, last


def _is_initials(token: str) -> bool:
    bare = token.replace(".", "")
    return 2 <= len(bare) <= 3 and bare.isalpha() and bare.isupper()


def first_names_compatible(a: str, b: str) -> bool:
    """Whether two first-name tokens can be the same person's (see module docstring)."""
    ka, kb = a.replace(".", "").casefold(), b.replace(".", "").casefold()
    if not ka or not kb:
        return False
    if ka == kb:
        return True
    if len(ka) >= 3 and len(kb) >= 3 and (ka.startswith(kb) or kb.startswith(ka)):
        return True
    if _is_initials(a) != _is_initials(b):
        return ka[0] == kb[0]
    return False


class _Groups:
    """Tiny union-find over names."""

    def __init__(self, items: list[str]) -> None:
        self.parent = {i: i for i in items}

    def find(self, x: str) -> str:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: str, b: str) -> None:
        self.parent[self.find(a)] = self.find(b)


def _co_occurrence(rows: pd.DataFrame, a: str, b: str) -> tuple[int, int]:
    """(games where both spellings share a slot, games where they sit in different slots)."""
    ra = rows[rows["name"] == a][["game_id", "official_order"]]
    rb = rows[rows["name"] == b][["game_id", "official_order"]]
    both = ra.merge(rb, on="game_id", suffixes=("_a", "_b"))
    same = int((both["official_order_a"] == both["official_order_b"]).sum())
    return same, int(len(both) - same)


def _collapse(rows: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    """Keep the first row of each key, with every raw spelling of the collapsed rows joined in raw_name."""
    raw = rows.groupby(keys, sort=False)["raw_name"].agg(lambda s: "|".join(dict.fromkeys(s))).rename("raw_name_all")
    kept = rows.drop_duplicates(keys).merge(raw.reset_index(), on=keys)
    kept["raw_name"] = kept["raw_name_all"]
    return kept.drop(columns="raw_name_all")


def build_officials(rows: pd.DataFrame, games: pd.DataFrame) -> OfficialsResult:
    """rows: raw officials (game_id, season, official_order, official_full_name). games: the kept games."""
    r = rows[rows["game_id"].isin(games["game_id"])].copy()
    r["raw_name"] = r["official_full_name"].map(clean_spaces)
    changed = rows.loc[r.index][r["official_full_name"] != r["raw_name"]]
    ws = (
        changed.assign(clean=changed["official_full_name"].map(clean_spaces))
        .groupby(["official_full_name", "clean"], as_index=False).size()
    )
    whitespace_fixes = [{"raw": repr(x.official_full_name), "clean": x.clean, "rows": int(x.size)} for x in ws.itertuples()]
    r["name"] = r["raw_name"]
    r["official_order"] = r["official_order"].astype(int)
    stats = {"rows_in_kept_games": len(r)}

    per_name = r.groupby("name").agg(games=("game_id", "nunique"), first=("season", "min"), last=("season", "max"))
    names = sorted(per_name.index)
    groups = _Groups(names)
    evidence: dict[tuple[str, str], dict] = {}
    by_last: dict[str, list[str]] = {}
    for n in names:
        by_last.setdefault(_tokens(n)[1], []).append(n)
    blocked: list[tuple[str, str]] = []
    for last, group in by_last.items():
        for i, a in enumerate(group):
            for b in group[i + 1 :]:
                if not first_names_compatible(_tokens(a)[0], _tokens(b)[0]):
                    continue
                same, diff = _co_occurrence(r, a, b)
                if diff > same:
                    blocked.append((a, b))
                    continue
                groups.union(a, b)
                evidence[(a, b)] = {"a": a, "b": b, "same_slot_games": same, "different_slot_games": diff}

    components: dict[str, list[str]] = {}
    for n in names:
        components.setdefault(groups.find(n), []).append(n)

    def pick(variants: list[str]) -> str:
        return sorted(variants, key=lambda v: (-per_name.loc[v, "games"], -per_name.loc[v, "last"], v))[0]

    canon = {n: pick(vs) for vs in components.values() for n in vs}
    merges = []
    for vs in components.values():
        if len(vs) < 2:
            continue
        c = pick(vs)
        merges.append(
            {
                "canonical": c,
                "variants": [
                    {"name": v, "games": int(per_name.loc[v, "games"]), "first_season": int(per_name.loc[v, "first"]), "last_season": int(per_name.loc[v, "last"])}
                    for v in sorted(vs, key=lambda v: (-per_name.loc[v, "games"], v))
                ],
                "evidence": [e for (a, b), e in evidence.items() if a in vs and b in vs],
            }
        )
    merges.sort(key=lambda m: m["canonical"])
    stats["name_merges"] = sum(len(m["variants"]) - 1 for m in merges)

    kept_separate = []
    for last, group in by_last.items():
        for i, a in enumerate(group):
            for b in group[i + 1 :]:
                if canon[a] != canon[b] and _tokens(a)[0][:1].casefold() == _tokens(b)[0][:1].casefold():
                    kept_separate.append((a, b))
    kept_separate = sorted(set(kept_separate) | set(blocked))

    # Every game where the cleaned raw names put two different names in one slot is flagged, whether or not the
    # merge later shows both to be one person (the 219 games of the spike, fewer here: some are exhibitions).
    raw_conflicts = r.groupby(["game_id", "official_order"])["name"].nunique()
    conflict_games = set(raw_conflicts[raw_conflicts > 1].reset_index()["game_id"])
    stats["slot_conflict_games"] = len(conflict_games)

    r["official_name"] = r["name"].map(canon)
    r = r.sort_values(["game_id", "official_order", "official_name"])
    before = len(r)
    r = _collapse(r, ["game_id", "official_order", "official_name"])  # same person, same slot
    stats["same_slot_duplicates_removed"] = before - len(r)
    before = len(r)
    r = _collapse(r, ["game_id", "official_name"])  # same person listed in two slots
    stats["same_person_two_slots_removed"] = before - len(r)

    slot_counts = r.groupby(["game_id", "official_order"]).size()
    shared = slot_counts[slot_counts > 1].reset_index()
    stats["slot_conflict_unresolved"] = int(shared["game_id"].nunique())
    r = r.merge(shared[["game_id", "official_order"]].assign(slot_shared=True), on=["game_id", "official_order"], how="left")
    r["slot_shared"] = r["slot_shared"].fillna(False).astype(bool)
    r["slot_conflict"] = r["game_id"].isin(conflict_games)
    officials = r[OFFICIAL_COLUMNS].sort_values(["game_id", "official_order", "official_name"]).reset_index(drop=True)

    n = officials.groupby("game_id").size()
    status = games[["game_id"]].copy()
    status["n_officials"] = status["game_id"].map(n).fillna(0).astype("int8")
    status["officials_status"] = STATUS_OK
    status.loc[status["n_officials"] == 0, "officials_status"] = STATUS_NONE
    status.loc[status["game_id"].isin(conflict_games), "officials_status"] = STATUS_CONFLICT
    stats["games_without_officials"] = int((status["officials_status"] == STATUS_NONE).sum())
    stats["games_with_more_than_3"] = int((status["n_officials"] > 3).sum())
    stats["distinct_officials"] = int(officials["official_name"].nunique())
    return OfficialsResult(officials, status, merges, whitespace_fixes, kept_separate, stats)
