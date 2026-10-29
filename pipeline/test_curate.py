import functools

import pytest

import curate as cu
from curate import Config, Item, RANK, build_items, deal, order_dive, select, shares, totals, violations

DIFFS = ["easy", "medium", "hard"]
CFG = Config(dives=12, family_cap=12, team_family_cap=4, tag_cap=5, star_style_range=(4, 14), select_steps=8000, deal_steps_per_dive=1500)


def make_item(kind, family, param, difficulty, broad, tags=(), size=40, tiers=(10, 10, 10, 4, 4, 2), group=None, dup=None):
    answers = [{"id": f"{'pl' if kind == 'player' else 'tm'}-{i}", "name": f"N{i}", "tier": 1, "points": 10} for i in range(size)]
    pid = f"cand-{family}-{'-'.join(str(p) for p in param)}"
    prompt = {"id": pid, "answerType": kind, "text": "Since 2001-02, name x.", "answers": answers, "difficulty": difficulty}
    meta = {"id": pid, "template": family, "n": None, "param": list(param), "valid_answers": size, "broad": broad, "tags": sorted(tags),
            "dup": list(dup if dup is not None else (family, *param)), "group": group or family,
            "tier_counts": {str(t + 1): c for t, c in enumerate(tiers)}}
    return prompt, meta


def make_pool(seed_families=12):
    """Broad player families keyed by franchise, star-style player families, and team families."""
    prompts, meta = [], []

    def add(pm):
        prompts.append(pm[0])
        meta.append(pm[1])

    for f in range(seed_families):  # broad, franchise-tagged: 30 franchises each
        for tid in range(1, 31):
            deep = f % 2 == 0
            add(make_item("player", f"broad{f}", (tid,), DIFFS[(f + tid) % 3], True, [f"f:{tid}"], size=60,
                          tiers=(8, 12, 14, 12, 8, 6) if deep else (20, 20, 12, 4, 2, 2)))
    for f in range(10):  # star-style: no tags, one question each
        for n in (20, 30, 40):
            add(make_item("player", f"star{f}", (), DIFFS[(f + n) % 3], False, size=50, tiers=(25, 15, 6, 2, 1, 1), dup=(f"star{f}",)))
    for f in range(8):  # teams, mostly tier 1
        for season in range(2002, 2020):
            add(make_item("team", f"team{f}", (season,), DIFFS[(f + season) % 3], False, size=12, tiers=(12, 0, 0, 0, 0, 0)))
    return prompts, meta


@functools.lru_cache(maxsize=None)
def default():
    prompts, meta = make_pool()
    return cu.curate(prompts, meta, {}, CFG), CFG


def test_hard_rules_hold_on_a_synthetic_pool():
    result, cfg = default()
    assert violations(result, cfg) == []
    assert len(result.items) == cfg.dives * 7


def test_each_dive_is_five_player_and_two_team_prompts_with_teams_in_slots_3_and_5():
    result, cfg = default()
    for d in range(cfg.dives):
        dive = result.dive(d)
        assert [i.answer_type for i in dive] == ["player", "player", "team", "player", "team", "player", "player"]
        assert sum(1 for i in dive if i.answer_type == "player" and i.broad) >= cfg.min_broad_per_dive


def test_no_repeated_family_franchise_or_star_inside_a_dive():
    result, cfg = default()
    for d in range(cfg.dives):
        dive = result.dive(d)
        assert len({i.template for i in dive}) == 7
        tags = [t for i in dive for t in i.tags]
        assert len(tags) == len(set(tags))


def test_neighbouring_dives_share_no_franchise_or_star():
    result, cfg = default()
    for d in range(cfg.dives - 1):
        assert not ({t for i in result.dive(d) for t in i.tags} & {t for i in result.dive(d + 1) for t in i.tags})


def test_every_dive_mixes_easy_medium_and_hard():
    result, cfg = default()
    for d in range(cfg.dives):
        assert {i.difficulty for i in result.dive(d)} == set(DIFFS)


def test_no_near_duplicates_and_no_repeated_prompt():
    result, _ = default()
    dups = [i.dup for i in result.items]
    assert len(set(dups)) == len(dups)
    ids = [i.prompt["id"] for i in result.items]
    assert len(set(ids)) == len(ids)


def test_a_star_style_family_is_used_once_not_at_several_thresholds():
    result, _ = default()
    star = [i.template for i in result.items if not i.broad and i.answer_type == "player"]
    assert len(star) == len(set(star))


def test_caps_are_respected():
    result, cfg = default()
    counts = {}
    tag_counts = {}
    for i in result.items:
        counts[i.template] = counts.get(i.template, 0) + 1
        for t in i.tags:
            tag_counts[t] = tag_counts.get(t, 0) + 1
    assert max(c for k, c in counts.items() if k.startswith("broad")) <= cfg.family_cap
    assert max(c for k, c in counts.items() if k.startswith("team")) <= cfg.team_family_cap
    assert max(tag_counts.values()) <= cfg.tag_cap
    star_style = sum(1 for i in result.items if i.answer_type == "player" and not i.broad)
    assert cfg.star_style_range[0] <= star_style <= cfg.star_style_range[1]


def test_the_rarity_targets_are_reached_when_the_pool_allows():
    result, _ = default()
    t12, t56 = shares(result.items)
    assert t12 <= cu.TARGET_TIER12 and t56 >= cu.TARGET_TIER56


def test_curation_prefers_rare_prompts_when_over_the_target():
    # a pool whose star-style prompts are all tier 1: the broad deep prompts must carry the rarity
    result, _ = default()
    deep = [i for i in result.items if i.broad and i.template in {f"broad{f}" for f in range(12) if f % 2 == 0}]
    assert len(deep) > 12


def test_curation_is_deterministic():
    prompts, meta = make_pool()
    again = cu.curate(prompts, meta, {}, CFG)
    assert [i.prompt["id"] for i in again.items] == [i.prompt["id"] for i in default()[0].items]


def test_too_few_distinct_prompts_is_an_error():
    prompts, meta = make_pool(seed_families=1)
    with pytest.raises(ValueError):
        cu.curate(prompts, meta, {}, CFG)


def test_violations_finds_planted_problems():
    result, cfg = default()
    broken = cu.Curated(items=list(result.items))
    broken.items[1] = Item(broken.items[0].prompt, broken.items[0].template, None, "g", True, broken.items[0].tags, ("x",), (1,) * 6)
    assert any("repeats a template family" in v or "same franchise" in v for v in violations(broken, cfg))
    short = cu.Curated(items=result.items[:-1])
    assert any("prompts, expected" in v for v in violations(short, cfg))


def test_order_dive_runs_easy_to_hard_with_teams_in_slots_3_and_5():
    prompts, meta = make_pool()
    items = build_items(prompts, meta, {})
    dive = [i for i in items if i.answer_type == "player"][:5] + [i for i in items if i.answer_type == "team"][:2]
    ordered = order_dive(dive)
    assert [i.answer_type for i in ordered] == ["player", "player", "team", "player", "team", "player", "player"]
    players = [RANK[i.difficulty] for i in ordered if i.answer_type == "player"]
    assert players == sorted(players)


def test_deal_keeps_every_prompt_exactly_once():
    prompts, meta = make_pool()
    items = build_items(prompts, meta, {})
    players, teams = select(items, CFG)
    dives = deal(players, teams, CFG)
    flat = [i.prompt["id"] for d in dives for i in d]
    assert sorted(flat) == sorted(i.prompt["id"] for i in players + teams)


def test_tier_totals():
    prompts, meta = make_pool()
    items = build_items(prompts, meta, {})
    t = totals(items[:2])
    assert t["answers"] == 120 and t["tier12"] == items[0].tier12 + items[1].tier12
