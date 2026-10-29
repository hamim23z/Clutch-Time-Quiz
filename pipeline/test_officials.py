import pandas as pd
import pytest

from officials import first_names_compatible, build_officials
from testdata import kept_games, officials_box


def run(rows, games=None):
    ids = sorted({r[0] for r in rows}) if games is None else games
    return build_officials(officials_box(*rows), kept_games(*ids))


def names_in(result, game_id):
    o = result.officials
    return o[o["game_id"] == game_id].sort_values("official_order")["official_name"].tolist()


@pytest.mark.parametrize(
    "a, b, expected",
    [
        ("J.B.", "JB", True), ("J.D.", "JD", True), ("J.T.", "JT", True),  # dots do not matter
        ("Steve", "Steven", True), ("Dan", "Daniel", True),  # one is the start of the other
        ("JB", "Joe", True), ("J.B.", "Joe", True),  # initials and a name with the same first letter
        ("Jacyn", "John", False), ("Dan", "Joe", False), ("Derek", "Leroy", False),  # different names
        ("JB", "Bob", False), ("JD", "JT", False),  # initials that do not fit
        ("Al", "Alan", False),  # too short to be a prefix match
    ],
)
def test_first_name_compatibility(a, b, expected):
    assert first_names_compatible(a, b) is expected


def test_spelling_variants_of_one_referee_become_one_canonical_name():
    rows = []
    gid = 0
    for name, n in (("Joe DeRosa", 5), ("J.B. DeRosa", 3), ("JB DeRosa", 2)):  # never in the same game
        for _ in range(n):
            gid += 1
            rows += [(gid, 2018, 1, name), (gid, 2018, 2, "Tom Washington"), (gid, 2018, 3, "Bill Kennedy")]
    result = run(rows)
    assert set(result.officials["official_name"]) == {"Joe DeRosa", "Tom Washington", "Bill Kennedy"}  # the most used spelling wins
    assert result.stats["name_merges"] == 2
    (merge,) = result.merges
    assert merge["canonical"] == "Joe DeRosa"
    assert [(v["name"], v["games"]) for v in merge["variants"]] == [("Joe DeRosa", 5), ("J.B. DeRosa", 3), ("JB DeRosa", 2)]
    assert result.officials["raw_name"].isin(["J.B. DeRosa", "JB DeRosa", "Joe DeRosa"]).any()  # the original spelling is kept


@pytest.mark.parametrize("a, b", [("Steve Anderson", "Steven Anderson"), ("J.D. Ralls", "JD Ralls"), ("J.T. Orr", "JT Orr")])
def test_other_known_variant_pairs_merge(a, b):
    rows = [(1, 2015, 1, a), (2, 2016, 1, a), (3, 2017, 1, b)]
    result = run(rows)
    assert result.officials["official_name"].nunique() == 1
    assert result.stats["name_merges"] == 1


def test_extra_spaces_are_cleaned_without_counting_as_a_merge():
    result = run([(1, 2018, 1, "Nate  Green"), (2, 2018, 1, "Nate Green")])
    assert set(result.officials["official_name"]) == {"Nate Green"}
    assert result.stats["name_merges"] == 0
    assert [(w["raw"], w["clean"]) for w in result.whitespace_fixes] == [("'Nate  Green'", "Nate Green")]


def test_different_people_with_similar_names_are_not_merged_and_are_listed_for_review():
    rows = [(1, 2017, 1, "John Goble"), (1, 2017, 2, "Jacyn Goble"), (2, 2019, 1, "Dan Crawford"), (2, 2019, 2, "Joe Crawford")]
    result = run(rows)
    assert set(result.officials["official_name"]) == {"John Goble", "Jacyn Goble", "Dan Crawford", "Joe Crawford"}
    assert result.stats["name_merges"] == 0
    assert {"Jacyn Goble", "John Goble"} in [set(pair) for pair in result.kept_separate]


def test_compatible_names_seen_working_a_game_together_are_two_people():
    # "Joe Smith" and "JB Smith" sit in different slots of the same games more often than in the same slot
    rows = []
    for gid in range(1, 5):
        rows += [(gid, 2015, 1, "Joe Smith"), (gid, 2015, 2, "JB Smith"), (gid, 2015, 3, "Other Ref")]
    result = run(rows)
    assert result.stats["name_merges"] == 0
    assert {frozenset(pair) for pair in result.kept_separate} == {frozenset({"Joe Smith", "JB Smith"})}


def test_middle_initials_and_suffixes_do_not_stop_a_merge():
    result = run([(1, 2010, 1, "Eddie F. Rush"), (2, 2011, 1, "Eddie Rush"), (3, 2012, 1, "Eddie Rush Jr.")])
    assert result.officials["official_name"].nunique() == 1


def test_two_different_people_in_one_slot_flag_the_game_and_keep_both_names():
    rows = [
        (1, 2016, 1, "Kevin Scott"), (1, 2016, 3, "Byron Scott"), (1, 2016, 3, "Evan Scott"),  # slot 3 has two people
        (2, 2016, 1, "Kevin Scott"), (2, 2016, 2, "Tom Washington"), (2, 2016, 3, "Bill Kennedy"),
    ]
    result = run(rows)
    assert names_in(result, 1) == ["Kevin Scott", "Byron Scott", "Evan Scott"]
    assert result.stats["slot_conflict_games"] == 1 and result.stats["slot_conflict_unresolved"] == 1
    status = result.game_status.set_index("game_id")["officials_status"]
    assert status.to_dict() == {1: "slot_conflict", 2: "ok"}
    flagged = result.officials.set_index("game_id")["slot_conflict"]
    assert flagged.loc[1].all() and not flagged.loc[2].any()
    shared = result.officials[result.officials["game_id"] == 1].set_index("official_name")["slot_shared"]
    assert shared.to_dict() == {"Kevin Scott": False, "Byron Scott": True, "Evan Scott": True}


def test_a_conflict_that_is_one_persons_spellings_is_still_flagged_but_marked_resolved():
    rows = [
        (1, 2016, 1, "Steve Anderson"), (1, 2016, 1, "Steven Anderson"), (1, 2016, 2, "Tom Washington"),  # same slot, same person
        (2, 2016, 1, "Tom Washington"), (2, 2016, 2, "Tom Washington"),  # same name in two slots
        (3, 2016, 1, "Steve Anderson"), (4, 2016, 1, "Steven Anderson"), (5, 2016, 1, "Steven Anderson"),  # Steven is used more
    ]
    result = run(rows)
    assert names_in(result, 1) == ["Steven Anderson", "Tom Washington"]
    assert names_in(result, 2) == ["Tom Washington"]
    assert result.stats["slot_conflict_games"] == 1  # game 1 had two names in one slot, so it is flagged
    assert result.stats["slot_conflict_unresolved"] == 0  # but they were one person, so no slot is shared
    game1 = result.officials[result.officials["game_id"] == 1]
    assert game1["slot_conflict"].all() and not game1["slot_shared"].any()
    assert "Steve Anderson|Steven Anderson" in game1["raw_name"].tolist()  # both spellings are kept
    assert result.stats["same_slot_duplicates_removed"] == 1 and result.stats["same_person_two_slots_removed"] == 1


def test_games_with_no_officials_are_marked_and_unknown_games_are_ignored():
    games = kept_games(1, 2, 3)
    rows = officials_box((1, 2010, 1, "A Ref"), (1, 2010, 2, "B Ref"), (1, 2010, 3, "C Ref"), (99, 2010, 1, "Z Ref"))
    result = build_officials(rows, games)
    status = result.game_status.set_index("game_id")
    assert status["officials_status"].to_dict() == {1: "ok", 2: "none", 3: "none"}
    assert status["n_officials"].to_dict() == {1: 3, 2: 0, 3: 0}
    assert 99 not in set(result.officials["game_id"])
    assert result.stats["games_without_officials"] == 2


def test_games_with_more_than_three_officials_are_counted():
    rows = [(1, 2013, i, f"Ref {c}") for i, c in enumerate("ABCD", start=1)] + [(2, 2013, i, f"Ref {c}") for i, c in enumerate("ABC", start=1)]
    assert run(rows).stats["games_with_more_than_3"] == 1
