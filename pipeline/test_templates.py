"""One brute-force check per template: plain Python loops over the fixture rows (bruteforce.py), written without the
template code, compared with what each template finds."""
import pytest

import templates
from bruteforce import BRUTE, Rows
from templates import PLAYER, TEMPLATES, TEAM
from testtables import make_tables

TABLES = make_tables()
ROWS = Rows(TABLES)

# template key -> thresholds that split the small fixture (the real thresholds are for 25 seasons of data)
FIXTURE_THRESHOLDS = {
    "points-regular": (20, 30, 40), "points-playoff": (20, 30, 40), "points-finals": (15, 25, 35),
    "triple-double-regular": (0,), "triple-double-playoff": (0,), "triple-double-finals": (0,),
    "rebounds": (8, 14, 18), "assists": (6, 10, 14), "threes": (3, 6, 9), "blocks": (2, 4, 6), "steals": (2, 4, 6),
    "ppg-season": (8, 11, 14, 16), "franchises": (1, 2, 3, 4),
    "wins-season": (3, 5, 7, 9), "wins-playoff": (1, 2, 3, 4), "points-regulation": (100, 130, 150, 160),
    "win-margin": (10, 30, 50, 70),
    "points-game7": (10, 25, 35), "points-overtime-game": (20, 35, 45), "points-bench": (15, 30, 40),
    "points-loss": (20, 35, 45), "points-road": (20, 30, 40),
    "rebounds-playoff": (8, 14, 18), "rebounds-finals": (8, 14, 18), "assists-playoff": (6, 10, 14),
    "assists-finals": (6, 10, 14), "threes-playoff": (3, 6, 9), "threes-finals": (3, 6, 9),
    "blocks-playoff": (2, 4, 6), "steals-playoff": (2, 4, 6), "offensive-rebounds": (3, 6, 9),
    "free-throws": (5, 8, 12), "turnovers": (3, 6, 9), "shots-taken": (10, 18, 24), "minutes": (30, 45, 55),
    "perfect-shooting": (3, 6, 9), "five-by-n": (1, 2, 3), "points-and-rebounds": (0,), "points-and-assists": (0,),
    "rebounds-per-game": (6, 8, 10), "assists-per-game": (3, 5, 7), "steals-per-game": (1, 2),
    "blocks-per-game": (1, 2), "double-double-average": (0,),
    "losses-season": (3, 5, 7), "road-wins": (1, 3, 4), "home-wins": (1, 3, 4),
    "points-playoff-team": (100, 130, 150), "points-any-game": (100, 150, 165), "win-margin-playoff": (10, 30, 45),
    "held-opponent": (90, 100, 110), "threes-team": (10, 20, 30), "steals-team": (5, 15, 22),
    "overtime-wins": (1, 2, 3), "win-streak": (2, 4, 6), "champion": (0,), "reached-finals": (0,),
}


def template(key):
    return next(t for t in TEMPLATES if t.key == key)


def pairs(df):
    return {(int(t), int(s)) for t, s in zip(df["team_id"], df["season"])}


def test_every_registered_template_has_a_brute_force_check_and_fixture_thresholds():
    keys = {t.key for t in TEMPLATES}
    assert keys == set(BRUTE) == set(FIXTURE_THRESHOLDS)


def test_every_template_names_a_stat_group():
    assert all(t.stat_group for t in TEMPLATES)
    assert len(TEMPLATES) >= 55


def _cases():
    return [(t.key, n) for t in TEMPLATES for n in FIXTURE_THRESHOLDS[t.key]]


@pytest.mark.parametrize("key,n", _cases())
def test_qualifiers_match_brute_force(key, n):
    t = template(key)
    got = t.qualify(TABLES, n)
    expected = BRUTE[key](ROWS, n)
    if t.answer_type == PLAYER:
        assert list(got.columns) == ["player_id"]
        assert got["player_id"].is_unique
        assert set(got["player_id"]) == expected
    else:
        assert pairs(got) == expected


@pytest.mark.parametrize("key", sorted(FIXTURE_THRESHOLDS))
def test_fixture_thresholds_are_not_trivial(key):
    # the check only means something if the thresholds find something and are not all the same answer
    results = [BRUTE[key](ROWS, n) for n in FIXTURE_THRESHOLDS[key]]
    assert any(results), f"{key}: the fixture finds nothing"
    if len(results) > 1:
        assert any(r != results[0] for r in results), f"{key}: every threshold gives the same answer"


def test_a_mutated_qualifier_is_caught():
    # sanity check of the check itself: ">" instead of ">=" changes the answer on the fixture
    got = template("points-regular").qualify(TABLES, 30)
    rows = [r for r in ROWS.player("player_id", "points", "season_type") if r[2] == "regular"]
    wrong = {int(p) for p, v, _ in rows if v > 30}
    assert set(got["player_id"]) != wrong


def test_triple_double_ignores_the_threshold():
    t = template("triple-double-regular")
    assert t.qualify(TABLES, 0)["player_id"].tolist() == t.qualify(TABLES, 99)["player_id"].tolist()


def test_ppg_needs_the_minimum_games():
    tables = make_tables(min_season_games=1000)
    assert len(template("ppg-season").qualify(tables, 0)) == 0
    assert len(template("rebounds-per-game").qualify(tables, 0)) == 0
    assert len(template("double-double-average").qualify(tables, 0)) == 0


def test_regular_season_wins_do_not_include_playoff_games():
    regular, total = {}, {}
    for team, season, stype, won in ROWS.team("team_id", "season", "season_type", "won"):
        key = (int(team), int(season))
        total[key] = total.get(key, 0) + (1 if won else 0)
        if stype == "regular":
            regular[key] = regular.get(key, 0) + (1 if won else 0)
    n = max(total.values())
    assert any(total[k] >= n > regular.get(k, 0) for k in total)  # a team that only reaches n with playoff wins
    assert pairs(template("wins-season").qualify(TABLES, n)) == {k for k, w in regular.items() if w >= n}


def test_overtime_games_do_not_count_for_regulation_points():
    only_ot = [r for r in ROWS.team("game_id", "team_score") if ROWS.game[r[0]]["periods"] > 4]
    assert only_ot
    top_ot = max(r[1] for r in only_ot)
    expected = BRUTE["points-regulation"](ROWS, top_ot)
    assert pairs(template("points-regulation").qualify(TABLES, top_ot)) == expected
    # but the any-game template does count the overtime game
    assert len(pairs(template("points-any-game").qualify(TABLES, top_ot))) >= len(expected)


def test_game7_scope_only_counts_series_game_7():
    game7 = {gid for gid, g in ROWS.game.items() if g["series"] == 7}
    assert game7 and len(game7) < len(ROWS.game)
    big = max(v for gid, v in ROWS.player("game_id", "points") if gid in game7)
    assert set(template("points-game7").qualify(TABLES, int(big))["player_id"]) <= {int(p) for g, p, v in ROWS.player("game_id", "player_id", "points") if g in game7 and v >= big}


def test_held_opponent_is_a_ceiling_not_a_floor():
    low, high = template("held-opponent").qualify(TABLES, 90), template("held-opponent").qualify(TABLES, 110)
    assert pairs(low) <= pairs(high)


def test_a_title_needs_four_finals_wins():
    champions = pairs(template("champion").qualify(TABLES, 0))
    finalists = pairs(template("reached-finals").qualify(TABLES, 0))
    assert champions and champions < finalists
    assert all(season in (2002, 2004, 2003, 2005) for _, season in champions)


def test_win_streaks_do_not_cross_seasons():
    # a team with a run of n in one season qualifies; two shorter runs on either side of a season change do not
    longest = {}
    by_team = {}
    for gid, team, season, stype, won in ROWS.team("game_id", "team_id", "season", "season_type", "won"):
        if stype == "regular":
            by_team.setdefault((int(team), int(season)), []).append((ROWS.game[gid]["date"], bool(won)))
    for key, games in by_team.items():
        run = best = 0
        for _, won in sorted(games):
            run = run + 1 if won else 0
            best = max(best, run)
        longest[key] = best
    n = max(longest.values())
    assert pairs(template("win-streak").qualify(TABLES, n)) == {k for k, v in longest.items() if v >= n}
    assert not pairs(template("win-streak").qualify(TABLES, n + 1))


def test_text_wording():
    t = template("points-regular")
    assert t.text("Since 2001-02 (through 2025-26)", 50) == \
        "Since 2001-02 (through 2025-26), name a player who scored 50 or more points in a regular-season game."
    team = template("wins-season")
    assert team.text("Since 2001-02", 60).startswith("Since 2001-02, name a team that won 60 or more")
    assert template("champion").text("Since 2001-02", 0) == "Since 2001-02, name a team that won the NBA championship."


def test_registering_the_same_key_twice_is_refused():
    with pytest.raises(ValueError):
        templates.register(TEMPLATES[0])


def test_a_new_template_can_be_added_and_removed():
    before = list(TEMPLATES)
    new = templates.Template("ref-test", PLAYER, "did {n} things", (1,), lambda t, n: t.players[["player_id"]], "things")
    templates.register(new)
    try:
        assert TEMPLATES[-1] is new and new.stat_group == "ref-test"
    finally:
        TEMPLATES[:] = before
    assert TEAM == "team"
