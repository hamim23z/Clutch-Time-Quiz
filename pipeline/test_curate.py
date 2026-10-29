import functools

import pytest

import curate
from curate import DIVE_SIZE, DIVES, MAX_PER_FAMILY, PLAYER_PER_DIVE, RANK, TEAM_SLOTS, Item, build_items, curate as run_curate, deal, order_dive, pool_for, select

DIFFS = ["easy", "medium", "hard"]


def _prompt(kind, template, n, difficulty, size=20, points=10):
    answers = [{"id": f"{'pl' if kind == 'player' else 'tm'}-{i}", "name": f"N{i}", "tier": 1, "points": points} for i in range(size)]
    return {"id": f"cand-{template}-{n}", "answerType": kind, "text": "Since 2001-02, name x.", "answers": answers, "difficulty": difficulty}, {"id": f"cand-{template}-{n}", "template": template, "n": n}


MIXED = [("easy", "hard"), ("easy", "medium"), ("medium", "hard")]  # what a two-threshold family offers


def make_pool(player_families=30, team_families=12, per_family=2):
    """Families with per_family thresholds each. With 2 the difficulties are mixed so every level is available;
    with more they cycle through the three levels."""
    prompts, meta = [], []
    for kind, families in (("player", player_families), ("team", team_families)):
        for f in range(families):
            for k in range(per_family):
                difficulty = MIXED[f % 3][k] if per_family == 2 else DIFFS[(f + k) % 3]
                p, m = _prompt(kind, f"{kind}-fam{f}", k + 1, difficulty, size=10 + 7 * k)
                prompts.append(p)
                meta.append(m)
    groups = {m["template"]: f"group{int(m['template'].split('fam')[1]) % 12}" for m in meta}
    return prompts, meta, groups


@functools.lru_cache(maxsize=None)
def default_result():
    prompts, meta, groups = make_pool()
    return run_curate(prompts, meta, groups)


def test_curation_gives_63_prompts_in_9_dives_of_5_player_and_2_team_prompts():
    result = default_result()
    assert len(result.items) == DIVES * DIVE_SIZE == 63
    for d in range(DIVES):
        dive = result.dive(d)
        assert [i.answer_type for i in dive].count("team") == 2 and [i.answer_type for i in dive].count("player") == PLAYER_PER_DIVE
        assert [slot for slot, i in enumerate(dive) if i.answer_type == "team"] == list(TEAM_SLOTS)


def test_no_repeated_prompts_and_at_most_two_per_family():
    result = default_result()
    ids = [i.prompt["id"] for i in result.items]
    assert len(set(ids)) == len(ids)
    per_family = {}
    for i in result.items:
        per_family[i.template] = per_family.get(i.template, 0) + 1
    assert max(per_family.values()) <= MAX_PER_FAMILY
    assert result.extended == []


def test_a_family_keeps_its_easiest_and_hardest_prompt():
    prompts, meta, groups = make_pool(player_families=1, team_families=0, per_family=4)
    items = build_items(prompts, meta, groups)
    kept = pool_for(items)
    assert len(kept) == 2
    ranks = sorted(RANK[i.difficulty] for i in items)
    assert RANK[kept[0].difficulty] == ranks[0] and RANK[kept[1].difficulty] == ranks[-1]


def test_dives_do_not_repeat_a_template_and_mostly_not_a_stat():
    result = default_result()
    for d in range(DIVES):
        dive = result.dive(d)
        assert len({i.template for i in dive}) == DIVE_SIZE
    repeats = sum(DIVE_SIZE - len({i.group for i in result.dive(d)}) for d in range(DIVES))
    assert repeats == 0  # 12 stat groups are plenty for 7 prompts a dive


def test_each_dive_has_easy_medium_and_hard_when_the_pool_allows():
    result = default_result()
    for d in range(DIVES):
        assert {i.difficulty for i in result.dive(d)} == set(DIFFS)


def test_a_dive_runs_from_easy_to_hard():
    dive = default_result().dive(0)
    players = [RANK[i.difficulty] for i in dive if i.answer_type == "player"]
    teams = [RANK[i.difficulty] for i in dive if i.answer_type == "team"]
    assert players == sorted(players) and teams == sorted(teams)


def test_curation_is_deterministic():
    prompts, meta, groups = make_pool()
    a = [i.prompt["id"] for i in default_result().items]
    b = [i.prompt["id"] for i in run_curate(prompts, meta, groups).items]
    assert a == b


def test_more_thresholds_are_added_only_when_two_per_family_is_not_enough():
    # 20 player families x 2 = 40 < 45 player slots, so some families must give a third prompt
    prompts, meta, groups = make_pool(player_families=20, team_families=12, per_family=4)
    result = run_curate(prompts, meta, groups)
    assert len(result.items) == 63
    assert result.extended
    per_family = {}
    for i in result.items:
        per_family[i.template] = per_family.get(i.template, 0) + 1
    assert set(result.extended) == {k for k, c in per_family.items() if c > MAX_PER_FAMILY}


def test_too_few_candidates_is_an_error():
    prompts, meta, groups = make_pool(player_families=3, team_families=12, per_family=3)
    with pytest.raises(ValueError):
        run_curate(prompts, meta, groups)


def test_difficulty_quotas_follow_what_the_pool_has():
    prompts, meta, groups = make_pool()
    players, teams, _ = select(build_items(prompts, meta, groups))
    counts = {d: sum(1 for i in players if i.difficulty == d) for d in DIFFS}
    assert counts["hard"] == round(0.2 * 45) and counts["medium"] == round(0.4 * 45) and sum(counts.values()) == 45


def test_order_dive_puts_teams_in_slots_3_and_5():
    prompts, meta, groups = make_pool()
    items = build_items(prompts, meta, groups)
    dive = [i for i in items if i.answer_type == "player"][:5] + [i for i in items if i.answer_type == "team"][:2]
    ordered = order_dive(dive)
    assert [i.answer_type for i in ordered] == ["player", "player", "team", "player", "team", "player", "player"]


def test_a_shortage_of_hard_prompts_is_passed_to_the_other_levels():
    prompts, meta, groups = make_pool()
    for p in prompts:
        if p["difficulty"] == "hard":
            p["difficulty"] = "medium"
    players, teams, _ = select(build_items(prompts, meta, groups))
    assert len(players) == 45 and len(teams) == 18
    assert not any(i.difficulty == "hard" for i in players + teams)
