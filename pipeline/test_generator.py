import json

import pandas as pd
import pytest

import generator
from fame import compute_fame
from generator import (MAX_PLAYER_ANSWERS, MIN_PLAYER_ANSWERS, MIN_TEAM_ANSWERS, check_count, difficulty, era_text,
                       generate, season_label, validate, write_candidates)
from templates import PLAYER, TEAM, Tables, Template, stat_in_game, wins_in_season
from testtables import make_tables

TABLES = make_tables()
FAME = compute_fame(TABLES.player_games, TABLES.players, TABLES.min_season_games)


# --- validity rules ---------------------------------------------------------------------------------------------

@pytest.mark.parametrize("count,expected", [(14, "too_few"), (15, None), (400, None), (401, "too_many")])
def test_player_answer_limits(count, expected):
    assert check_count(PLAYER, count) == expected
    assert (MIN_PLAYER_ANSWERS, MAX_PLAYER_ANSWERS) == (15, 400)


@pytest.mark.parametrize("count,expected", [(0, "too_few"), (4, "too_few"), (5, None), (30, None), (500, None)])
def test_team_answer_limits(count, expected):
    assert check_count(TEAM, count) == expected
    assert MIN_TEAM_ANSWERS == 5


def _fake_tables(n_players: int) -> tuple[Tables, pd.DataFrame, Template]:
    """Tables and a fame table where a template qualifies exactly n_players players."""
    fame = pd.DataFrame({
        "player_id": range(1, n_players + 1), "name": [f"P{i}" for i in range(1, n_players + 1)],
        "career_points": range(n_players, 0, -1), "fame_rank": range(1, n_players + 1), "tier": 3, "points": 35,
    })
    games = pd.DataFrame({"season": [2002, 2026]})
    template = Template("fixed", PLAYER, "did something", (0,), lambda t, n: fame[["player_id"]], "x")
    return Tables(None, None, games, None, None), fame, template


@pytest.mark.parametrize("n,kept", [(14, False), (15, True), (400, True), (401, False)])
def test_generate_applies_the_player_limits(n, kept):
    tables, fame, template = _fake_tables(n)
    result = generate(tables, fame, [template])
    assert [p["id"] for p in result.prompts] == (["cand-fixed"] if kept else [])
    assert result.attempts[0]["status"] == ("kept" if kept else "too_few" if n < 15 else "too_many")
    assert result.attempts[0]["valid_answers"] == n


def _team_template(key: str, team_ids: list[int]) -> Template:
    qualifiers = pd.DataFrame({"team_id": team_ids, "season": 2005})
    return Template(key, TEAM, "x", (0,), lambda tb, n: qualifiers, "x")


@pytest.mark.parametrize("ids,kept", [([1, 2, 3, 4], False), ([1, 2, 3, 4, 5], True), ([1, 2, 3, 4, 5, 6], True)])
def test_generate_applies_the_team_minimum(ids, kept):
    result = generate(TABLES, FAME, [_team_template("t", ids)])
    assert len(result.prompts) == (1 if kept else 0)
    assert result.attempts[0]["status"] == ("kept" if kept else "too_few")


# --- generated prompts ------------------------------------------------------------------------------------------

def _wins_and_idle_teams(t: Tables, n: int) -> pd.DataFrame:
    """Teams with n or more wins, plus the two franchises that play no games, so the prompt has 5 or more answers."""
    got = wins_in_season("regular")(t, n)
    idle = pd.DataFrame({"team_id": [5, 6], "season": [2005, 2005]})
    return pd.concat([got, idle], ignore_index=True)


LOW = [
    Template("points-low", PLAYER, "scored {n} or more points in a regular-season game", (20, 25), stat_in_game("points", "regular"), "points"),
    Template("wins-low", TEAM, "won {n} or more games in a season", (3, 4), _wins_and_idle_teams, "wins"),
]


@pytest.fixture(scope="module")
def result():
    return generate(TABLES, FAME, LOW)


def test_prompts_pass_the_schema_and_rules(result):
    assert result.prompts
    validate(result.prompts)


def test_prompt_shape_ids_and_text(result):
    ids = [p["id"] for p in result.prompts]
    assert ids == ["cand-points-low-20", "cand-points-low-25", "cand-wins-low-3", "cand-wins-low-4"]
    for p in result.prompts:
        assert set(p) == {"id", "answerType", "text", "answers", "difficulty"}
        assert p["text"].startswith("Since 2001-02 (through 2004-05), name a ")
        assert p["difficulty"] in {"easy", "medium", "hard"}


def test_player_answers_use_unique_names_ids_and_fame_tiers(result):
    prompt = next(p for p in result.prompts if p["answerType"] == "player")
    fame = FAME.set_index("player_id")
    for a in prompt["answers"]:
        pid = int(a["id"].removeprefix("pl-"))
        assert a["name"] == fame.loc[pid, "name"] and a["tier"] == fame.loc[pid, "tier"]
        assert a["points"] == {1: 10, 2: 20, 3: 35, 4: 55, 5: 75, 6: 100}[a["tier"]]
    keys = [(a["tier"], fame.loc[int(a["id"][3:]), "fame_rank"]) for a in prompt["answers"]]
    assert keys == sorted(keys)  # best known first


def test_team_answers_use_current_names_and_the_current_name_rule():
    t = Template("beta", TEAM, "x", (0,), lambda tb, n: pd.DataFrame({"team_id": [2, 2, 1, 4], "season": [2003, 2004, 2002, 2002]}), "x")
    prompt_tiers = {a["name"]: a["tier"] for a in generator._team_answers(t.qualify(TABLES, 0), TABLES.teams)}
    assert prompt_tiers == {"Alpha": 1, "Beta": 4, "Delta": 4}  # Beta only as Old Beta, Delta only as Prior Delta


def test_team_answers_and_meta_record_historical_names():
    qualifiers = pd.DataFrame({"team_id": [1, 2, 3, 4, 4, 5], "season": [2002, 2003, 2002, 2002, 2004, 2002]})
    t = Template("hist", TEAM, "x", (0,), lambda tb, n: qualifiers, "x")
    out = generate(TABLES, FAME, [t])
    answers = {a["name"]: a["tier"] for a in out.prompts[0]["answers"]}
    assert answers == {"Alpha": 1, "Gamma": 1, "Delta": 1, "Epsilon": 1, "Beta": 4}
    assert out.meta[0]["historical_only"] == ["Beta"]
    assert out.meta[0]["historical_names"]["tm-2"] == ["Old Beta"]


def test_a_qualifier_missing_from_the_fame_table_is_an_error():
    t = Template("ghost", PLAYER, "x", (0,), lambda tb, n: pd.DataFrame({"player_id": [999]}), "x")
    with pytest.raises(ValueError):
        generate(TABLES, FAME, [t])


def test_meta_matches_prompts(result):
    assert [m["id"] for m in result.meta] == [p["id"] for p in result.prompts]
    for m, p in zip(result.meta, result.prompts):
        assert m["valid_answers"] == len(p["answers"]) == sum(m["tier_counts"].values())


def test_triple_double_style_ids_have_no_threshold():
    t = Template("no-n", PLAYER, "did it", (0,), lambda tb, n: FAME[["player_id"]], "x")
    out = generate(TABLES, FAME, [t])
    assert out.prompts[0]["id"] == "cand-no-n"


# --- schema rejection -------------------------------------------------------------------------------------------

def _good():
    return json.loads(json.dumps(generate(TABLES, FAME, LOW).prompts))


@pytest.mark.parametrize("break_it", [
    lambda ps: ps[0].update(text="In 2002, name a player"),
    lambda ps: ps[0]["answers"].__delitem__(slice(0, len(ps[0]["answers"]) - 14)),  # 14 player answers
    lambda ps: ps[0]["answers"][0].update(points=11),
    lambda ps: ps[0].update(id="cand_bad"),
    lambda ps: ps[0].update(extra=1),
    lambda ps: ps[0]["answers"].append(dict(ps[0]["answers"][0])),
    lambda ps: ps.append(dict(ps[0])),
])
def test_validate_rejects_broken_prompts(break_it):
    prompts = _good()
    assert len(prompts[0]["answers"]) > 15
    break_it(prompts)
    with pytest.raises(Exception):
        validate(prompts)


def test_validate_rejects_a_team_prompt_with_four_answers():
    prompts = _good()
    team = next(p for p in prompts if p["answerType"] == "team")
    team["answers"] = [{"id": f"tm-{i}", "name": f"T{i}", "tier": 1, "points": 10} for i in range(4)]
    with pytest.raises(Exception):
        validate(prompts)


# --- era wording and difficulty ---------------------------------------------------------------------------------

def test_season_labels_and_era_text():
    assert season_label(2002) == "2001-02" and season_label(2000) == "1999-00" and season_label(2026) == "2025-26"
    assert era_text(2002, 2026) == "Since 2001-02 (through 2025-26)"


def test_difficulty_rule_for_players():
    # size: 100+ answers = 0, 40-99 = 1, under 40 = 2.  depth (share at tier 4+): under 10% = 0, 10-25% = 1, 25%+ = 2.
    # total 0-1 easy, 2 medium, 3-4 hard
    assert difficulty(PLAYER, [1] * 100) == "easy"
    assert difficulty(PLAYER, [1] * 91 + [4] * 9) == "easy"  # 9% deep
    assert difficulty(PLAYER, [1] * 90 + [4] * 10) == "easy"  # size 0 + depth 1
    assert difficulty(PLAYER, [1] * 60 + [4] * 40) == "medium"  # size 0 + depth 2
    assert difficulty(PLAYER, [1] * 50) == "easy"  # size 1 + depth 0
    assert difficulty(PLAYER, [1] * 45 + [4] * 5) == "medium"  # size 1 + depth 1 (10% deep)
    assert difficulty(PLAYER, [1] * 20) == "medium"  # size 2 + depth 0
    assert difficulty(PLAYER, [1] * 15 + [6] * 5) == "hard"  # size 2 + depth 2
    assert difficulty(PLAYER, [1] * 30 + [3] * 5) == "medium"  # tier 3 is not a deep cut


def test_difficulty_rule_for_teams():
    assert difficulty(TEAM, [1] * 20) == "easy"
    assert difficulty(TEAM, [1] * 10) == "easy"  # size 1 + depth 0
    assert difficulty(TEAM, [1] * 8) == "medium"  # size 2
    assert difficulty(TEAM, [1] * 9 + [4]) == "medium"  # size 1 + 10% deep: depth 1
    assert difficulty(TEAM, [1] * 5 + [4] * 5) == "hard"  # size 1 + depth 2


def test_write_candidates_writes_valid_json_and_meta(tmp_path):
    out = generate(TABLES, FAME, LOW)
    write_candidates(out, tmp_path)
    assert json.loads((tmp_path / "candidates.json").read_text()) == out.prompts
    meta = json.loads((tmp_path / "candidates_meta.json").read_text())
    assert meta["era"] == out.era and len(meta["attempts"]) == 4


def test_write_candidates_refuses_an_invalid_set(tmp_path):
    bad = generate(TABLES, FAME, [_team_template("t", [1, 2, 3, 4, 5])])
    bad.prompts[0]["answers"] = bad.prompts[0]["answers"][:4]
    with pytest.raises(Exception):
        write_candidates(bad, tmp_path)
    assert not (tmp_path / "candidates.json").exists()
