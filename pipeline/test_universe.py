import pandas as pd
import pytest

from testtables import make_teams
from universe import build_universe, drop_contested_aliases, player_entries, team_entries


def players_frame(rows):
    """rows: (player_id, display_name, unique_name, variants)"""
    return pd.DataFrame({
        "player_id": [r[0] for r in rows], "display_name": [r[1] for r in rows], "unique_name": [r[2] for r in rows],
        "variants": [r[3] for r in rows], "first_season": 2002, "last_season": 2010,
    })


def alias_frame(*rows):
    return pd.DataFrame(rows, columns=["alias", "athlete_id", "canonical_name", "kind", "evidence"])


NO_TEAM_ALIASES = pd.DataFrame({"alias": pd.Series([], dtype=str), "team": pd.Series([], dtype=str), "evidence": pd.Series([], dtype=str)})


def test_players_are_named_by_unique_name_and_keep_their_spellings():
    players = players_frame([
        (1, "Mike James", "Mike James (2002-2014)", ["Mike James"]),
        (2, "Mike James", "Mike James (2018-2021)", ["Mike James"]),
        (3, "Jimmy Butler III", "Jimmy Butler III", ["Jimmy Butler III", "Jimmy Butler"]),
        (4, "Nene", "Nene", ["Nene", "Nenê"]),
    ])
    entries = {e["id"]: e for e in player_entries(players, alias_frame(("Nene Hilario", 4, "Nene", "legal name", "evidence of the name")))}
    assert entries["pl-1"]["name"] == "Mike James (2002-2014)" and entries["pl-2"]["name"] == "Mike James (2018-2021)"
    assert entries["pl-1"]["aliases"] == [] and entries["pl-2"]["aliases"] == []  # the shared name is not an alias of either
    assert entries["pl-3"]["aliases"] == []  # 'Jimmy Butler' reads the same once the suffix is dropped
    assert entries["pl-4"]["aliases"] == ["Nene Hilario"]  # 'Nenê' reads the same as 'Nene' once accents are folded


def test_an_alias_for_an_unknown_athlete_is_refused():
    players = players_frame([(1, "A Player", "A Player", ["A Player"])])
    with pytest.raises(ValueError):
        player_entries(players, alias_frame(("Ghost", 99, "Ghost", "rename", "evidence of the name")))


def test_an_alias_that_names_the_wrong_player_is_refused():
    players = players_frame([(1, "A Player", "A Player", ["A Player"]), (2, "B Player", "B Player", ["B Player"])])
    with pytest.raises(ValueError):
        player_entries(players, alias_frame(("Nick", 2, "A Player", "nickname", "evidence of the name")))


def test_team_entries_use_current_names_history_nicknames_and_long_abbreviations():
    teams = {e["name"]: e for e in team_entries(make_teams(), NO_TEAM_ALIASES)}
    assert set(teams) == {"Alpha", "Beta", "Delta", "Epsilon", "Gamma", "Zeta"}
    assert "Old Beta" in teams["Beta"]["aliases"] and "Prior Delta" in teams["Delta"]["aliases"]
    assert "Alpha" not in teams["Alpha"]["aliases"]  # never its own name
    assert "ALP" in teams["Alpha"]["aliases"]  # three letters


def test_short_abbreviations_are_not_aliases():
    teams = make_teams()
    teams["names"] = [[{**e, "abbreviation": "NO"} for e in row] for row in teams["names"]]
    assert all("NO" not in e["aliases"] for e in team_entries(teams, NO_TEAM_ALIASES))


def test_extra_team_aliases_must_name_a_real_franchise():
    extra = pd.DataFrame({"alias": ["Alphas"], "team": ["Alpha"], "evidence": ["x"]})
    assert "Alphas" in {e["name"]: e for e in team_entries(make_teams(), extra)}["Alpha"]["aliases"]
    with pytest.raises(ValueError):
        team_entries(make_teams(), pd.DataFrame({"alias": ["X"], "team": ["Nowhere"], "evidence": ["x"]}))


def test_contested_aliases_are_dropped_from_every_claimant():
    entries = [
        {"id": "pl-1", "name": "One", "aliases": ["Shared", "Mine"]},
        {"id": "pl-2", "name": "Two", "aliases": ["shared", "One"]},  # 'One' is another entry's name
    ]
    dropped = drop_contested_aliases(entries)
    assert entries[0]["aliases"] == ["Mine"] and entries[1]["aliases"] == []
    assert {(d[0], d[1]) for d in dropped} == {("pl-1", "Shared"), ("pl-2", "shared"), ("pl-2", "One")}


def test_build_universe_on_the_fixture_teams():
    players = players_frame([(1, "A Player", "A Player", ["A Player"])])
    universe, dropped = build_universe(players, make_teams(), alias_frame(), NO_TEAM_ALIASES)
    assert [e["id"] for e in universe["players"]] == ["pl-1"]
    assert sorted(e["id"] for e in universe["teams"]) == ["tm-1", "tm-2", "tm-3", "tm-4", "tm-5", "tm-6"]
    assert dropped == []
