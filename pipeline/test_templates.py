"""One brute-force check per template: plain Python loops over the fixture rows, written without the template code."""
import pytest

import templates
from templates import PLAYER, TEMPLATES, TEAM
from testtables import make_tables

TABLES = make_tables()


def _rows(df):
    return df.to_dict("records")


GAMES = {g["game_id"]: g for g in _rows(TABLES.games)}
PLAYER_ROWS = _rows(TABLES.player_games)
TEAM_ROWS = _rows(TABLES.team_games)


def in_scope(row, scope):
    if scope == "finals":
        return GAMES[row["game_id"]]["is_finals"]
    return scope == "any" or row["season_type"] == scope


def stat_players(col, scope):
    return lambda n: {r["player_id"] for r in PLAYER_ROWS if in_scope(r, scope) and r[col] >= n}


def triple_double_players(scope):
    def brute(n):
        found = set()
        for r in PLAYER_ROWS:
            if in_scope(r, scope) and sum(1 for c in ("points", "reb", "ast", "stl", "blk") if r[c] >= 10) >= 3:
                found.add(r["player_id"])
        return found
    return brute


def ppg_players(n):
    total, count = {}, {}
    for r in PLAYER_ROWS:
        if r["season_type"] == "regular":
            key = (r["player_id"], r["season"])
            total[key] = total.get(key, 0) + r["points"]
            count[key] = count.get(key, 0) + 1
    return {p for (p, s), games in count.items() if games >= TABLES.min_season_games and total[(p, s)] / games >= n}


def franchise_players(n):
    teams = {}
    for r in PLAYER_ROWS:
        teams.setdefault(r["player_id"], set()).add(r["team_id"])
    return {p for p, t in teams.items() if len(t) >= n}


def season_wins(season_type):
    def brute(n):
        wins = {}
        for r in TEAM_ROWS:
            if r["season_type"] == season_type:
                wins[(r["team_id"], r["season"])] = wins.get((r["team_id"], r["season"]), 0) + (1 if r["won"] else 0)
        return {k for k, w in wins.items() if w >= n}
    return brute


def regulation_points(n):
    return {(r["team_id"], r["season"]) for r in TEAM_ROWS if GAMES[r["game_id"]]["periods"] == 4 and r["team_score"] >= n}


def win_margin(n):
    return {(r["team_id"], r["season"]) for r in TEAM_ROWS if r["team_score"] > r["opponent_score"]
            and r["team_score"] - r["opponent_score"] >= n}


# template key -> (brute-force function, thresholds that are meaningful on the small fixture)
BRUTE = {
    "points-regular": (stat_players("points", "regular"), (20, 30, 40)),
    "points-playoff": (stat_players("points", "playoffs"), (20, 30, 40)),
    "points-finals": (stat_players("points", "finals"), (15, 25, 35)),
    "triple-double-regular": (triple_double_players("regular"), (0,)),
    "triple-double-playoff": (triple_double_players("playoffs"), (0,)),
    "triple-double-finals": (triple_double_players("finals"), (0,)),
    "rebounds": (stat_players("reb", "any"), (8, 14, 18)),
    "assists": (stat_players("ast", "any"), (6, 10, 14)),
    "threes": (stat_players("fg3m", "any"), (3, 6, 9)),
    "blocks": (stat_players("blk", "any"), (2, 4, 6)),
    "steals": (stat_players("stl", "any"), (2, 4, 6)),
    "ppg-season": (ppg_players, (8, 11, 14, 16)),
    "franchises": (franchise_players, (1, 2, 3, 4)),
    "wins-season": (season_wins("regular"), (3, 5, 7, 9)),
    "wins-playoff": (season_wins("playoffs"), (1, 2, 3, 4)),
    "points-regulation": (regulation_points, (100, 130, 150, 160)),
    "win-margin": (win_margin, (10, 30, 50, 70)),
}


def test_every_registered_template_has_a_brute_force_check():
    assert {t.key for t in TEMPLATES} == set(BRUTE)


def _cases():
    return [(t.key, n) for t in TEMPLATES for n in BRUTE[t.key][1]]


@pytest.mark.parametrize("key,n", _cases())
def test_qualifiers_match_brute_force(key, n):
    template = next(t for t in TEMPLATES if t.key == key)
    got = template.qualify(TABLES, n)
    expected = BRUTE[key][0](n)
    if template.answer_type == PLAYER:
        assert list(got.columns) == ["player_id"]
        assert got["player_id"].is_unique
        assert set(got["player_id"]) == expected
    else:
        assert {(int(t), int(s)) for t, s in zip(got["team_id"], got["season"])} == expected


def test_thresholds_on_the_fixture_are_not_all_trivial():
    # each template finds some qualifiers at its lowest fixture threshold and fewer (or none) at its highest
    for t in TEMPLATES:
        low, high = BRUTE[t.key][1][0], BRUTE[t.key][1][-1]
        found_low, found_high = BRUTE[t.key][0](low), BRUTE[t.key][0](high)
        assert found_low, t.key
        assert len(found_high) <= len(found_low), t.key


def test_triple_double_ignores_the_threshold():
    t = next(t for t in TEMPLATES if t.key == "triple-double-regular")
    assert t.qualify(TABLES, 0)["player_id"].tolist() == t.qualify(TABLES, 99)["player_id"].tolist()


def test_ppg_needs_the_minimum_games_and_adds_up_teams():
    tables = make_tables(min_season_games=1000)
    assert len(next(t for t in TEMPLATES if t.key == "ppg-season").qualify(tables, 0)) == 0


def test_regular_season_wins_do_not_include_playoff_games():
    regular, total = {}, {}
    for r in TEAM_ROWS:
        key = (r["team_id"], r["season"])
        total[key] = total.get(key, 0) + (1 if r["won"] else 0)
        if r["season_type"] == "regular":
            regular[key] = regular.get(key, 0) + (1 if r["won"] else 0)
    n = max(total.values())
    assert any(total[k] >= n > regular.get(k, 0) for k in total)  # a team that only reaches n with playoff wins
    got = next(t for t in TEMPLATES if t.key == "wins-season").qualify(TABLES, n)
    assert {(int(t), int(s)) for t, s in zip(got["team_id"], got["season"])} == {k for k, w in regular.items() if w >= n}


def test_overtime_games_do_not_count_for_regulation_points():
    only_ot = [r for r in TEAM_ROWS if GAMES[r["game_id"]]["periods"] > 4]
    assert only_ot
    top_ot = max(r["team_score"] for r in only_ot)
    got = next(t for t in TEMPLATES if t.key == "points-regulation").qualify(TABLES, top_ot)
    expected = regulation_points(top_ot)
    assert {(int(t), int(s)) for t, s in zip(got["team_id"], got["season"])} == expected


def test_text_wording():
    t = next(t for t in TEMPLATES if t.key == "points-regular")
    assert t.text("Since 2001-02 (through 2025-26)", 50) == \
        "Since 2001-02 (through 2025-26), name a player who scored 50 or more points in a regular-season game."
    team = next(t for t in TEMPLATES if t.key == "wins-season")
    assert team.text("Since 2001-02", 60).startswith("Since 2001-02, name a team that won 60 or more")


def test_registering_the_same_key_twice_is_refused():
    with pytest.raises(ValueError):
        templates.register(TEMPLATES[0])


def test_a_new_template_can_be_added_and_removed():
    before = list(TEMPLATES)
    new = templates.Template("ref-test", PLAYER, "did {n} things", (1,), lambda t, n: t.players[["player_id"]], "things")
    templates.register(new)
    try:
        assert TEMPLATES[-1] is new
    finally:
        TEMPLATES[:] = before
    assert TEAM == "team"
