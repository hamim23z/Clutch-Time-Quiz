"""Notes stage: write docs/pipeline-notes.md, the review log for decisions the pipeline made.

The file is regenerated on every run, so it always matches the tables. It lists the skipped games, the name
merges for officials, players whose names are shared, and the data gaps that downstream sessions should know.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from assemble import Tables
from games import EXCLUSION_REASONS

REASON_TEXT = {
    "not_final": "postponed or not final",
    "all_star": "All-Star game",
    "cup_final": "NBA Cup final",
    "play_in": "play-in game",
    "non_nba_team": "exhibition with a non-NBA side (Rising Stars, USA, World, All-Star teams)",
    "other_type": "other game type",
}
ARTEST_NOTE = (
    "Ron Artest is not in `aliases.csv` on purpose. The data only knows this player as Metta World Peace "
    "(athlete id 25, 2002-2017) and the name Artest appears nowhere in it, so the rename cannot be confirmed from "
    "the data. Add it by hand if you want it."
)


def _md_table(headers: list[str], rows: list[list[object]]) -> list[str]:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return out


def render(t: Tables, tables_written: dict[str, int]) -> str:
    L: list[str] = ["# Pipeline notes", ""]
    L += ["Written by `python3 pipeline/run.py`; do not edit by hand. Rules and sources are in `docs/data-source-boxscores.md`.", ""]

    L += ["## Run summary", "", f"Seasons processed: {t.seasons[0]}-{t.seasons[-1]} ({len(t.seasons)} seasons; season 2002 means 2001-02).", ""]
    L += _md_table(["table", "rows"], [[name, f"{n:,}"] for name, n in tables_written.items()]) + [""]

    g = t.games
    L += ["## Game selection", "", "Kept games by season type:", ""]
    L += _md_table(["season type", "games"], [[k, f"{v:,}"] for k, v in g["season_type"].value_counts().sort_index().items()]) + [""]
    L += ["Games dropped before the box scores (not counted as skipped):", ""]
    L += _md_table(["reason", "games"], [[REASON_TEXT[r], f"{t.excluded.get(r, 0):,}"] for r in EXCLUSION_REASONS]) + [""]
    L += [
        "Play-in games are excluded: only regular-season and playoff games are kept. The spike reported 27 games without player rows and "
        "14 without team rows. The 27 are the games skipped below (8 of them also lack team rows, and no game lacks only team rows). "
        "The other 6 of the spike's 14 are 2021 play-in games, which are excluded as play-in.",
        "",
    ]

    sk = t.skipped
    L += [f"### Skipped games: {len(sk)}", "", "Regular-season or playoff games with no usable box score rows. They are left out of every table.", ""]
    for reason, title in (
        ("no_player_rows", "no player rows (no row with a points value)"),
        ("no_team_rows", "no team rows"),
        ("no_team_and_player_rows", "no team rows and no player rows"),
    ):
        part = sk[sk["reason"] == reason]
        L += [f"**{title}: {len(part)}**", ""]
        if len(part):
            for season, h in part.groupby("season"):
                L.append(f"- {season}: " + ", ".join(str(i) for i in h["game_id"]))
            L.append("")
    L += [
        "Counts by reason in total: " + ", ".join(f"{r} = {int((sk['reason'] == r).sum())}" for r in ("no_player_rows", "no_team_rows", "no_team_and_player_rows")),
        "",
        "## Played or not", "",
        "A player counts as having played only if the `points` value is present. `did_not_play` is not used (it is almost never "
        f"set in 2006-2012). {len(t.player_games):,} player-game rows are kept. Stat lines with no athlete id are dropped.", "",
    ]

    pl, names = t.players, t.player_names
    L += ["## Players", "", f"{len(pl):,} players, one record per athlete id. Ids are never merged.", ""]
    changed = names.groupby("player_id")["display_name"].nunique()
    L += [f"**Display names that changed over time: {int((changed > 1).sum())} players** (all kept as spelling variants):", ""]
    for pid in changed[changed > 1].index:
        row = pl[pl["player_id"] == pid].iloc[0]
        L.append(f"- id {pid}: " + ", ".join(row["variants"]))
    accented = pl[pl["variants"].map(lambda v: any(any(ord(c) > 127 for c in x) for x in v))]
    L += ["", f"**Accented spellings kept as variants: {len(accented)} players** (from short names), for example "
          + ", ".join(f"{r.display_name} -> {[x for x in r.variants if any(ord(c) > 127 for c in x)][0]}" for r in accented.head(5).itertuples()) + ".", ""]
    L += [f"**Display names shared by more than one athlete id: {len(t.shared_names)}.** They stay separate records, each with a `unique_name`:", ""]
    for ids in t.shared_names.values():
        rows = pl[pl["player_id"].isin(ids)]
        L.append("- " + "; ".join(f"id {r.player_id} = {r.unique_name}" for r in rows.itertuples()))
    L += ["", f"**Aliases applied from `pipeline/data/aliases.csv`: {int((pl['aliases'].map(len) > 0).sum())} players.**", ""]
    for r in pl[pl["aliases"].map(len) > 0].itertuples():
        L.append(f"- {r.display_name} (id {r.player_id}): " + ", ".join(r.aliases))
    L += ["", ARTEST_NOTE, ""]

    tm = t.teams
    L += ["## Teams", "", f"{len(tm)} franchises (ESPN team ids 1-30; the 14 non-NBA sides in the team box all have ids above 30). Franchises with more than one name:", ""]
    for r in tm.itertuples():
        if len(r.names) > 1:
            L.append(f"- id {r.team_id}: " + "; ".join(f"{n['name']} ({n['abbreviation']}) {n['first_season']}-{n['last_season']}" for n in r.names))
    L.append("")

    o = t.officials_result
    s = o.stats
    L += ["## Officials", "", "The data has names only: no ids and no crew chief (every row is a referee). Slot = `official_order`.", ""]
    L += [f"**Name merges: {s['name_merges']}** (spellings folded into another spelling of the same person), across {len(o.merges)} people:", ""]
    for m in o.merges:
        absorbed = [v for v in m["variants"] if v["name"] != m["canonical"]]
        L.append(f"- **{m['canonical']}** <- " + "; ".join(f"{v['name']} ({v['games']} games, {v['first_season']}-{v['last_season']})" for v in absorbed))
        for e in m["evidence"]:
            L.append(f"  - evidence: `{e['a']}` and `{e['b']}` appear in the same game in the same slot {e['same_slot_games']} times and in different slots {e['different_slot_games']} times")
    L += ["", f"Whitespace-only fixes (not counted as merges): {len(o.whitespace_fixes)} spellings.", ""]
    for w in o.whitespace_fixes:
        L.append(f"- {w['raw']} -> {w['clean']} ({w['rows']} rows)")
    L += ["", "Look alike but **not** merged (different first names, or seen as two people in the same game), for review:", ""]
    for a, b in o.kept_separate:
        L.append(f"- {a} / {b}")
    L += [
        "",
        f"**Slot conflicts:** {s['slot_conflict_games']} games have two different names in one slot in the raw data (2014-2020). "
        "The spike counted 219 over every game type; the difference is exhibition games, which are dropped. All of them are flagged: "
        "`officials_status = slot_conflict` on the game and `slot_conflict = True` on its rows, and every raw spelling is kept in `raw_name`. "
        f"In {s['slot_conflict_games'] - s['slot_conflict_unresolved']} of them the two names turn out to be one person (spellings merged, or the same person "
        f"listed twice), so {s['slot_conflict_unresolved']} games still have two different people in one slot (`slot_shared = True` on those rows).",
        "",
        f"Cleanup: {s['same_slot_duplicates_removed']} duplicate rows for the same person in the same slot and {s['same_person_two_slots_removed']} "
        "rows listing the same person in a second slot were removed.",
        f"Games with more than 3 officials listed: {s['games_with_more_than_3']}. Games with no officials: {s['games_without_officials']}.",
        "",
    ]
    none = g[g["officials_status"] == "none"].groupby(["season", "season_type"]).size().unstack(fill_value=0)
    L += ["Games with no officials, by season (the data has none for any 2009, 2010 or 2011 playoff game, and few regular-season gaps):", ""]
    cols = [c for c in ("regular", "playoffs") if c in none.columns]
    L += _md_table(["season"] + cols, [[int(i)] + [int(r[c]) for c in cols] for i, r in none.iterrows()]) + [""]
    return "\n".join(L).rstrip() + "\n"


def write_notes(t: Tables, tables_written: dict[str, int], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render(t, tables_written))
