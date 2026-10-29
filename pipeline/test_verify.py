import copy

from bruteforce import BRUTE, Rows
from curate import Item
from fame import compute_fame
from generator import generate
from templates import PLAYER, Template, stat_in_game
from tiers import TIER_POINTS
from testtables import NO_OVERRIDES, make_tables
from verify import check_prompt, verify_sample

TABLES = make_tables()
FAME = compute_fame(TABLES.player_games, TABLES.players, TABLES.min_season_games, NO_OVERRIDES)
ROWS = Rows(TABLES)


POINTS = Template("points-regular", PLAYER, "scored {n} or more points in a regular-season game", (30,), stat_in_game("points", "regular"), "points")
RESULT = generate(TABLES, FAME, [POINTS])


def points_prompt():
    return copy.deepcopy(RESULT.prompts[0])


def team_prompt(flip_tier=False):
    """A hand-built prompt for 'won 3 or more games': tier 1 if the franchise won under its current name, else 4."""
    found = BRUTE["wins-season"](ROWS, 3)
    teams = TABLES.teams.set_index("team_id")
    answers = []
    for tid in sorted({t for t, _ in found}):
        seasons = {s for t, s in found if t == tid}
        current = [e for e in teams.loc[tid, "names"] if e["name"] == teams.loc[tid, "current_name"]][0]
        tier = 1 if seasons & set(current["seasons"]) else 4
        if flip_tier and not answers:
            tier = 5 - tier
        answers.append({"id": f"tm-{tid}", "name": teams.loc[tid, "current_name"], "tier": tier, "points": TIER_POINTS[tier]})
    return {"id": "t", "answerType": "team", "text": "Since 2001-02, name a team.", "answers": answers, "difficulty": "easy"}


def test_a_correct_player_prompt_passes():
    c = check_prompt(points_prompt(), "points-regular", 30, ROWS, FAME, TABLES.teams)
    assert c.ok and c.expected == c.exported > 15


def test_a_missing_answer_is_found():
    p = points_prompt()
    dropped = p["answers"].pop()
    c = check_prompt(p, "points-regular", 30, ROWS, FAME, TABLES.teams)
    assert not c.ok and c.missing == [dropped["id"]] and not c.extra


def test_an_extra_answer_is_found():
    p = points_prompt()
    outsider = next(f"pl-{i}" for i in range(1, 41) if f"pl-{i}" not in {a["id"] for a in p["answers"]})
    by_id = FAME.set_index("player_id")
    tier = int(by_id.loc[int(outsider[3:]), "tier"])
    p["answers"].append({"id": outsider, "name": "x", "tier": tier, "points": TIER_POINTS[tier]})
    c = check_prompt(p, "points-regular", 30, ROWS, FAME, TABLES.teams)
    assert not c.ok and c.extra == [outsider] and not c.tier_problems


def test_a_wrong_tier_is_found():
    p = points_prompt()
    first = p["answers"][0]
    first["tier"], first["points"] = (6, 100) if first["tier"] != 6 else (1, 10)
    c = check_prompt(p, "points-regular", 30, ROWS, FAME, TABLES.teams)
    assert not c.ok and len(c.tier_problems) == 1 and not c.missing


def test_wrong_points_for_the_tier_are_found():
    p = points_prompt()
    p["answers"][0]["points"] += 1
    assert check_prompt(p, "points-regular", 30, ROWS, FAME, TABLES.teams).tier_problems


def test_team_answers_and_tiers_are_rechecked():
    ok = check_prompt(team_prompt(), "wins-season", 3, ROWS, FAME, TABLES.teams)
    assert ok.ok and ok.expected >= 3
    flipped = check_prompt(team_prompt(flip_tier=True), "wins-season", 3, ROWS, FAME, TABLES.teams)
    assert not flipped.ok and len(flipped.tier_problems) == 1


def test_verify_sample_checks_the_requested_number_and_no_more_than_exist():
    items = [Item(copy.deepcopy(RESULT.prompts[0]), "points-regular", 30, "points")]
    checks = verify_sample(items, TABLES, FAME, k=10)
    assert len(checks) == 1 and checks[0].ok
