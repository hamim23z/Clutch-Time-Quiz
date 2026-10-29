"""The parameterised families: every pool the family enumerates is compared with the independent brute-force query,
and the wording, limits and tags are checked on the small fixture."""
import pytest

import pools
from bruteforce import BRUTE_FAMILY, Rows
from fame import compute_fame
from generator import MAX_BROAD_ANSWERS, generate_families
from pools import FAMILIES, Family, duplicate_key, make_ctx, threshold_of
from templates import PLAYER, TEAM
from testtables import NO_OVERRIDES, make_tables

TABLES = make_tables()
FAME = compute_fame(TABLES.player_games, TABLES.players, TABLES.min_season_games, NO_OVERRIDES)
ROWS = Rows(TABLES)
ERA = "Since 2001-02 (through 2005-06)"

# the real thresholds are for 25 seasons of data; these split the 4-season fixture
FIXTURE_THRESHOLDS = {
    "franchise-points": (10, 20, 30), "points-against": (10, 20, 30), "month-points": (10, 20, 30), "month-threes": (2, 4, 6),
    "season-points": (20, 30, 40), "season-threes": (4, 6, 8), "season-rebounds": (8, 12, 16), "season-assists": (6, 9, 12),
    "wins-in-season": (3, 5, 7), "home-wins-in-season": (2, 3, 4), "road-wins-in-season": (1, 2, 3), "playoff-wins-in-season": (1, 2, 3),
    "regulation-points-in-season": (100, 130, 150), "margin-in-season": (10, 30, 50), "threes-in-season": (10, 20, 30),
    "held-opponent-in-season": (90, 100, 110), "overtime-wins-in-season": (1, 2, 3),
}


@pytest.fixture(autouse=True)
def fixture_scale(monkeypatch):
    for key, values in FIXTURE_THRESHOLDS.items():
        monkeypatch.setitem(pools.THRESHOLDS, key, values)
    monkeypatch.setattr(pools, "STAR_MIN_GAMES", 20)
    monkeypatch.setattr(pools, "STAR_COUNT", 5)


@pytest.fixture
def ctx():
    return make_ctx(TABLES, FAME)


def as_set(family: Family, pool):
    return pool if family.answer_type == PLAYER else {(int(t), int(s)) for t, s in pool}


def enumerated(family: Family):
    return list(family.enumerate(TABLES, make_ctx(TABLES, FAME)))


def test_every_family_has_a_brute_force_query():
    assert {f.key for f in FAMILIES} == set(BRUTE_FAMILY)
    assert len(FAMILIES) >= 30 and sum(f.answer_type == TEAM for f in FAMILIES) >= 12


@pytest.mark.parametrize("family", FAMILIES, ids=lambda f: f.key)
def test_every_pool_matches_brute_force(family):
    items = enumerated(family)
    assert items, f"{family.key}: the fixture gives no pools"
    for param, pool in items:
        assert as_set(family, pool) == BRUTE_FAMILY[family.key](ROWS, param), (family.key, param)


@pytest.mark.parametrize("family", FAMILIES, ids=lambda f: f.key)
def test_parameters_are_unique_and_pools_nonempty(family):
    params = [p for p, _ in enumerated(family)]
    assert len(params) == len(set(params))
    assert all(len(pool) > 0 for _, pool in enumerated(family))


def test_stars_are_the_most_famous_players_with_enough_games(ctx):
    games = TABLES.player_games.groupby("player_id").size()
    assert len(ctx.stars) == 5 and all(games[s] >= 20 for s in ctx.stars)
    order = FAME.set_index("player_id")["fame_rank"]
    eligible = FAME[FAME["player_id"].isin(games[games >= 20].index)].sort_values(["fame_rank", "career_points"], ascending=[True, False])
    assert ctx.stars == [int(p) for p in eligible["player_id"].head(5)]
    assert [order[s] for s in ctx.stars] == sorted(order[s] for s in ctx.stars)


def test_players_below_the_games_minimum_are_never_stars(monkeypatch):
    monkeypatch.setattr(pools, "STAR_MIN_GAMES", 10_000)
    assert make_ctx(TABLES, FAME).stars == []


def test_teammate_pool_excludes_the_star_and_needs_a_shared_game(ctx):
    star = ctx.stars[0]
    ctx.stars = [star]
    (param, pool), = list(next(f for f in FAMILIES if f.key == "teammate").enumerate(TABLES, ctx))
    assert star not in pool and param == (star,)
    pg = TABLES.player_games
    mine = pg[pg["player_id"] == star][["game_id", "team_id"]]
    together = pg.merge(mine, on=["game_id", "team_id"])
    assert pool == set(together["player_id"]) - {star}


def test_text_has_the_era_and_names_what_it_is_about(ctx):
    teammate = next(f for f in FAMILIES if f.key == "teammate")
    assert teammate.text(ERA, ctx, (7,)) == f"{ERA}, name a player who played in the same game as Player 7 for the same team."
    franchise = next(f for f in FAMILIES if f.key == "franchise-season")
    assert franchise.text(ERA, ctx, (2, 2004)) == f"{ERA}, name a player who played for the Old Beta in a regular-season game in the 2003-04 season."
    month = next(f for f in FAMILIES if f.key == "month-points")
    assert month.text(ERA, ctx, (2003, 12, 30)).endswith("scored 30 or more points in a regular-season game in December 2003.")
    playoffs = next(f for f in FAMILIES if f.key == "made-playoffs")
    assert playoffs.text(ERA, ctx, (2005,)) == f"{ERA}, name a team that made the playoffs in the 2004-05 season."
    finals = next(f for f in FAMILIES if f.key == "finals-year")
    assert finals.text(ERA, ctx, (2004,)).endswith("appeared in the 2004 NBA Finals.")


def test_a_franchise_with_an_earlier_nickname_says_so(ctx):
    assert ctx.franchise(2) == "the Beta (including its time as the Old Beta)"  # fixture: 'Old Beta' was its name until 2004
    assert ctx.franchise(1) == "the Alpha"
    assert ctx.franchise_in(2, 2003) == "the Old Beta" and ctx.franchise_in(2, 2005) == "the Beta"


def test_tags_name_the_franchises_and_stars_a_prompt_is_about():
    by_key = {f.key: f for f in FAMILIES}
    assert by_key["both-franchises"].tags((3, 9)) == frozenset({"f:3", "f:9"})
    assert by_key["franchise-season"].tags((3, 2004)) == frozenset({"f:3"})
    assert by_key["teammate"].tags((1966,)) == frozenset({"s:1966"})
    assert by_key["finals-year"].tags((2004,)) == frozenset()


def test_duplicate_keys_ignore_only_the_threshold():
    assert duplicate_key("month-points", (2015, 12, 30)) == duplicate_key("month-points", (2015, 12, 40))
    assert duplicate_key("month-points", (2015, 12, 30)) != duplicate_key("month-points", (2015, 11, 30))
    assert duplicate_key("franchise-season", (3, 2004)) != duplicate_key("franchise-season", (3, 2005))
    assert threshold_of("month-points", (2015, 12, 30)) == 30 and threshold_of("franchise-season", (3, 2004)) is None


def test_every_family_with_a_threshold_is_registered_for_it():
    for key, at in pools.THRESHOLD_AT.items():
        family = next(f for f in FAMILIES if f.key == key)
        param, _ = enumerated(family)[0]
        assert isinstance(param[at], int)


# --- generation: windows, ids, meta ------------------------------------------------------------------------------

def test_broad_pools_need_15_to_700_players_and_team_pools_5_to_24_franchises(ctx):
    result = generate_families(TABLES, FAME, ctx, broad_window=(15, 700), team_window=(5, 24))
    sizes = {}
    for p in result.prompts:
        n = len(p["answers"]) if p["answerType"] == PLAYER else len({a["id"] for a in p["answers"]})
        sizes[p["id"]] = (p["answerType"], n)
    assert all(15 <= n <= 700 for t, n in sizes.values() if t == PLAYER)
    assert all(5 <= n <= 24 for t, n in sizes.values() if t == TEAM)
    statuses = {a["status"] for a in result.attempts}
    assert "kept" in statuses and "too_few" in statuses


def test_window_edges_are_inclusive(ctx):
    family = next(f for f in FAMILIES if f.key == "finals-year")
    sizes = sorted(len(pool) for _, pool in enumerated(family))
    size = sizes[len(sizes) // 2]
    kept = generate_families(TABLES, FAME, ctx, [family], broad_window=(size, size))
    assert {len(p["answers"]) for p in kept.prompts} == {size}
    too_few = generate_families(TABLES, FAME, ctx, [family], broad_window=(size + 1, 700))
    assert all(a["valid_answers"] < size + 1 for a in too_few.attempts if a["status"] == "too_few")
    too_many = generate_families(TABLES, FAME, ctx, [family], broad_window=(15, size - 1))
    assert "too_many" in {a["status"] for a in too_many.attempts} or size - 1 < 15


def test_broad_limit_is_700_while_star_templates_keep_400():
    from generator import check_count, validate
    assert MAX_BROAD_ANSWERS == 700
    assert check_count(PLAYER, 450) == "too_many" and check_count(PLAYER, 450, MAX_BROAD_ANSWERS) is None
    assert check_count(PLAYER, 701, MAX_BROAD_ANSWERS) == "too_many"
    answers = lambda n: [{"id": f"pl-{i}", "name": f"P{i}", "tier": 1, "points": 10} for i in range(n)]
    prompt = lambda n: [{"id": "p-x", "answerType": "player", "text": "Since 2001-02, name a player.", "answers": answers(n), "difficulty": "easy"}]
    validate(prompt(700))
    with pytest.raises(ValueError):
        validate(prompt(701))


def test_generated_prompts_have_ids_meta_and_exact_wording(ctx):
    result = generate_families(TABLES, FAME, ctx, [next(f for f in FAMILIES if f.key == "franchise-season")], broad_window=(1, 700))
    assert result.prompts
    for p, m in zip(result.prompts, result.meta):
        tid, season = m["param"]
        assert p["id"] == f"cand-franchise-season-{tid}-{season}"
        assert p["text"].startswith(f"{result.era}, name a player who played for the ")
        assert m["broad"] and m["tags"] == [f"f:{tid}"] and m["dup"] == ["franchise-season", tid, season]
        assert sum(m["tier_counts"].values()) == len(p["answers"]) == m["valid_answers"]


def test_team_answers_are_franchises_with_the_current_name_tier_rule(ctx):
    family = next(f for f in FAMILIES if f.key == "made-playoffs")
    result = generate_families(TABLES, FAME, ctx, [family], team_window=(1, 24))
    assert result.prompts
    for p in result.prompts:
        for a in p["answers"]:
            assert a["id"].startswith("tm-") and a["tier"] in (1, 4) and a["points"] == {1: 10, 4: 55}[a["tier"]]
