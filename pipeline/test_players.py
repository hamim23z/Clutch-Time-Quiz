from pathlib import Path

import pandas as pd
import pytest

from players import ALIAS_COLUMNS, apply_aliases, build_players, load_aliases, season_player_names, shared_names
from testdata import player_box


def names(*rows):
    """Rows: (player_id, season, display_name, short_name[, games])."""
    return pd.DataFrame(
        [{"player_id": r[0], "season": r[1], "display_name": r[2], "short_name": r[3] if len(r) > 3 else "", "games": r[4] if len(r) > 4 else 10} for r in rows]
    )


def test_one_record_per_athlete_id_with_every_display_name_and_accented_short_names():
    n = names(
        (6430, 2018, "Jimmy Butler", "J. Butler"), (6430, 2019, "Jimmy Butler", "Butler"), (6430, 2022, "Jimmy Butler III", "J. Butler III"),
        (1713, 2010, "Nene ", "N. Hilario"), (1713, 2019, "Nene", "Nenê"),
    )
    p = build_players(n).set_index("player_id")
    assert len(p) == 2
    butler = p.loc[6430]
    assert butler["display_name"] == "Jimmy Butler III"  # the name used latest
    assert butler["variants"] == ["Jimmy Butler III", "Jimmy Butler"]  # abbreviations and bare surnames are not kept
    assert (butler["first_season"], butler["last_season"], butler["seasons_played"], butler["games_played"]) == (2018, 2022, 3, 30)
    nene = p.loc[1713]
    assert nene["display_name"] == "Nene"  # stray space removed
    assert nene["variants"] == ["Nene", "Nenê"]  # accented short name kept, "N. Hilario" is not
    assert not butler["name_collision"]


def test_same_name_for_two_athletes_stays_two_records_with_a_disambiguator():
    n = names((1051, 2002, "Mike James"), (1051, 2014, "Mike James"), (2528096, 2018, "Mike James"), (2528096, 2021, "Mike James"), (5, 2020, "Ann Other"))
    p = build_players(n).set_index("player_id")
    assert len(p) == 3
    assert p.loc[1051, "unique_name"] == "Mike James (2002-2014)"
    assert p.loc[2528096, "unique_name"] == "Mike James (2018-2021)"
    assert p.loc[1051, "name_collision"] and p.loc[2528096, "name_collision"]
    assert p.loc[5, "unique_name"] == "Ann Other" and not p.loc[5, "name_collision"]
    assert p["unique_name"].is_unique
    assert shared_names(n) == {"mike james": [1051, 2528096]}


def test_two_athletes_with_the_same_name_and_seasons_are_still_told_apart_by_id():
    n = names((2583664, 2014, "Tony Mitchell"), (2489010, 2014, "Tony Mitchell"))
    p = build_players(n).set_index("player_id")
    assert p.loc[2583664, "unique_name"] == "Tony Mitchell (2014, id 2583664)"
    assert p.loc[2489010, "unique_name"] == "Tony Mitchell (2014, id 2489010)"


def test_names_that_differ_only_by_whitespace_or_case_still_count_as_the_same_name():
    n = names((1, 2012, "Mike  Harris"), (2, 2015, "mike harris"))
    p = build_players(n)
    assert p["name_collision"].all()
    assert p.loc[p.player_id == 1, "display_name"].iloc[0] == "Mike Harris"


def test_a_shared_accented_surname_is_not_a_name_collision():
    n = names((1, 2017, "Willy Hernangomez", "Hernangómez"), (2, 2017, "Juancho Hernangomez", "Hernangómez"))
    p = build_players(n)
    assert not p["name_collision"].any()
    assert p["unique_name"].tolist() == ["Willy Hernangomez", "Juancho Hernangomez"]


def test_season_player_names_counts_games_for_played_rows_only():
    raw = player_box(
        {"game_id": 1, "athlete_id": 1, "athlete_display_name": "A  B", "athlete_short_name": "A. B", "points": 3.0},
        {"game_id": 2, "athlete_id": 1, "athlete_display_name": "A  B", "athlete_short_name": "A. B", "points": 4.0},
        {"game_id": 3, "athlete_id": 1, "athlete_display_name": "A  B", "athlete_short_name": "A. B", "points": None},
    )
    kept = pd.DataFrame({"game_id": [1, 2], "player_id": [1, 1]})
    out = season_player_names(kept, raw)
    assert out["display_name"].tolist() == ["A B"] and out["games"].tolist() == [2]


# --- aliases ---------------------------------------------------------------------------------------------

PLAYERS = names((6447, 2012, "Enes Freedom", "E. Freedom"), (25, 2002, "Metta World Peace", "M. World Peace"), (9, 2005, "Other Guy", "O. Guy"))


def alias_frame(*rows):
    return pd.DataFrame(rows, columns=ALIAS_COLUMNS)


def test_aliases_are_attached_to_the_right_player():
    p = build_players(PLAYERS, alias_frame(("Enes Kanter", 6447, "Enes Freedom", "rename", "short name Kanter on the same id")))
    row = p.set_index("player_id")
    assert row.loc[6447, "aliases"] == ["Enes Kanter"]
    assert row.loc[25, "aliases"] == [] and row.loc[9, "aliases"] == []


@pytest.mark.parametrize(
    "alias, athlete_id, canonical, message",
    [
        ("Ghost", 999, "Ghost Player", "not in the data"),  # unknown athlete id
        ("Ron Artest", 25, "Ron Artest", "is not a name of athlete 25"),  # canonical name does not match the data
        ("Other Guy", 25, "Metta World Peace", "already belongs to athlete 9"),  # alias is someone else's name
        ("Enes Freedom", 6447, "Enes Freedom", "already a spelling"),  # redundant alias
    ],
)
def test_bad_aliases_are_refused(alias, athlete_id, canonical, message):
    players = build_players(PLAYERS)
    with pytest.raises(ValueError, match=message):
        apply_aliases(players, alias_frame((alias, athlete_id, canonical, "rename", "x")))


def test_an_alias_cannot_be_given_to_two_players():
    players = build_players(PLAYERS)
    rows = alias_frame(("Nickname", 25, "Metta World Peace", "nickname", "x"), ("Nickname", 9, "Other Guy", "nickname", "x"))
    with pytest.raises(ValueError, match="already belongs"):
        apply_aliases(players, rows)


def test_aliases_for_players_outside_a_partial_run_can_be_skipped():
    players = build_players(PLAYERS)
    rows = alias_frame(("Ghost", 999, "Ghost Player", "rename", "x"))
    assert apply_aliases(players, rows, allow_missing=True)["aliases"].map(len).sum() == 0


def test_alias_file_is_read_and_cleaned(tmp_path):
    f = tmp_path / "aliases.csv"
    f.write_text('alias,athlete_id,canonical_name,kind,evidence\n"Enes  Kanter",6447,Enes Freedom,rename,"why"\n')
    df = load_aliases(f)
    assert df["alias"].tolist() == ["Enes Kanter"] and df["athlete_id"].tolist() == [6447]


def test_the_shipped_alias_file_is_well_formed():
    df = load_aliases(Path(__file__).parent / "data" / "aliases.csv")
    assert list(df.columns) == ALIAS_COLUMNS
    assert len(df) <= 150  # a hand-written list, not a generated one
    assert df["evidence"].str.len().gt(20).all()  # every entry says what in the data supports it
    assert not df["alias"].duplicated().any()
