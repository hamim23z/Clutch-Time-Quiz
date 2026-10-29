import copy

import pytest

from exportcheck import check_all, check_answers_in_universe, check_tier_points, validate_universe
from tiers import TIER_POINTS


def entry(i, name, aliases=()):
    return {"id": i, "name": name, "aliases": list(aliases)}


def universe():
    return {
        "players": [entry(f"pl-{n}", f"Player {n}", [f"P{n}x"]) for n in range(1, 21)],
        "teams": [entry(f"tm-{n}", f"Team {n}", [f"T{n}x"]) for n in range(1, 8)],
    }


def prompts():
    def answers(prefix, count, name):
        return [{"id": f"{prefix}-{n}", "name": f"{name} {n}", "tier": 1 + n % 6, "points": TIER_POINTS[1 + n % 6]} for n in range(1, count + 1)]
    return [
        {"id": "p-a", "answerType": "player", "text": "Since 2001-02, name a player who did a.", "answers": answers("pl", 20, "Player"), "difficulty": "easy"},
        {"id": "p-b", "answerType": "team", "text": "Since 2001-02, name a team that did b.", "answers": answers("tm", 6, "Team"), "difficulty": "medium"},
    ]


def test_a_consistent_pair_of_files_passes():
    check_all(prompts(), universe())


def test_answer_id_missing_from_the_universe_is_caught():
    p, u = prompts(), universe()
    u["players"] = [e for e in u["players"] if e["id"] != "pl-3"]
    with pytest.raises(ValueError, match="pl-3"):
        check_answers_in_universe(p, u)


def test_answer_with_a_different_name_is_caught():
    p, u = prompts(), universe()
    p[0]["answers"][0]["name"] = "Somebody Else"
    with pytest.raises(ValueError, match="universe says"):
        check_answers_in_universe(p, u)


def test_a_team_answer_must_be_in_the_teams_list():
    p, u = prompts(), universe()
    u["teams"][0]["id"], u["players"][0]["id"] = "tm-99", "tm-1"  # tm-1 now sits in the players list
    with pytest.raises(ValueError):
        check_answers_in_universe(p, u)


@pytest.mark.parametrize("tier,points", [(1, 20), (2, 10), (3, 55), (6, 75), (4, 0)])
def test_points_must_match_the_tier(tier, points):
    p = prompts()
    p[0]["answers"][0].update(tier=tier, points=points)
    with pytest.raises(ValueError, match="points"):
        check_tier_points(p)


def test_every_tier_pairs_with_its_points():
    p = prompts()
    for tier, points in TIER_POINTS.items():
        p[0]["answers"][0].update(tier=tier, points=points)
        check_tier_points(p)


def test_check_all_includes_the_schema_and_count_rules():
    p, u = prompts(), universe()
    p[0]["answers"] = p[0]["answers"][:14]  # a player prompt needs 15
    with pytest.raises(Exception):
        check_all(p, u)
    p = prompts()
    p[1]["text"] = "In 2002, name a team."
    with pytest.raises(Exception):
        check_all(p, u)


def test_two_prompts_with_the_same_text_are_refused():
    p = prompts()
    p[1]["text"] = p[0]["text"]
    p[1]["id"] = "p-c"
    p[1]["answerType"], p[1]["answers"] = "player", prompts()[0]["answers"]
    with pytest.raises(ValueError, match="same text|text"):
        check_all(p, universe())


def test_universe_schema_and_unique_ids():
    u = universe()
    validate_universe(u)
    u["players"].append(copy.deepcopy(u["players"][0]))
    with pytest.raises(ValueError):
        validate_universe(u)
    with pytest.raises(Exception):
        validate_universe({"players": universe()["players"]})


def test_people_with_the_same_name_must_carry_a_disambiguator():
    u = universe()
    u["players"][1]["name"] = u["players"][0]["name"]
    with pytest.raises(ValueError, match="named"):
        validate_universe(u)
    u["players"][0]["name"] = "Player 1 (2002-2004)"
    u["players"][1]["name"] = "Player 1 (2010-2012)"
    validate_universe(u)  # separate entries, told apart; the shared base name is allowed


def test_an_alias_claimed_by_two_entries_is_caught():
    u = universe()
    u["players"][1]["aliases"].append("Shared Nick")
    u["players"][2]["aliases"].append("shared nick")
    with pytest.raises(ValueError, match="several"):
        validate_universe(u)


def test_an_alias_that_is_another_entrys_name_is_caught():
    u = universe()
    u["teams"][0]["aliases"].append("Player 4")
    with pytest.raises(ValueError, match="several"):
        validate_universe(u)


def test_an_alias_equal_to_its_own_name_is_caught():
    u = universe()
    u["players"][0]["aliases"].append("PLAYER 1")
    with pytest.raises(ValueError, match="own name"):
        validate_universe(u)
