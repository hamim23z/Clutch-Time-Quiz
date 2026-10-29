import pandas as pd
import pytest

from tiers import CUTOFFS, TIER_POINTS, points_for_tier, team_tiers, tier_for_rank
from testtables import make_teams


def test_cutoffs_at_every_boundary_for_100_players():
    # percentile == rank for n=100; a player exactly on a line belongs to the better-known tier
    expected = {1: 1, 3: 1, 4: 2, 10: 2, 11: 3, 25: 3, 26: 4, 50: 4, 51: 5, 75: 5, 76: 6, 100: 6}
    for rank, tier in expected.items():
        assert tier_for_rank(rank, 100) == tier, rank


def test_cutoffs_do_not_depend_on_floating_point():
    # 3% of 2,520 players is exactly 75.6; 3% of 700 is exactly 21 (0.03 * 700 is not exactly 21.0 in floats)
    assert tier_for_rank(21, 700) == 1
    assert tier_for_rank(22, 700) == 2
    assert tier_for_rank(75, 2520) == 1
    assert tier_for_rank(76, 2520) == 2


def test_tier_sizes_over_a_population_follow_the_cutoffs():
    n = 1000
    tiers = [tier_for_rank(r, n) for r in range(1, n + 1)]
    assert [tiers.count(t) for t in range(1, 7)] == [30, 70, 150, 250, 250, 250]


def test_rank_outside_range_is_an_error():
    for rank, n in ((0, 10), (11, 10), (1, 0)):
        with pytest.raises(ValueError):
            tier_for_rank(rank, n)


def test_points_pair_with_tiers():
    assert [points_for_tier(t) for t in range(1, 7)] == [10, 20, 35, 55, 75, 100]
    assert [t for _, t in CUTOFFS] == [1, 2, 3, 4, 5]
    assert set(TIER_POINTS) == {1, 2, 3, 4, 5, 6}


def _inst(*pairs):
    return pd.DataFrame(pairs, columns=["team_id", "season"])


def test_team_under_current_name_is_tier_1():
    assert team_tiers(_inst((1, 2003)), make_teams()) == {1: 1}


def test_team_only_under_historical_name_is_tier_4():
    # franchise 2 was "Old Beta" in 2002-2004 and is "Beta" from 2005
    assert team_tiers(_inst((2, 2003), (2, 2004)), make_teams()) == {2: 4}


def test_team_with_any_season_under_current_name_is_tier_1():
    assert team_tiers(_inst((2, 2003), (2, 2005)), make_teams()) == {2: 1}
    assert team_tiers(_inst((2, 2005), (2, 2003)), make_teams()) == {2: 1}  # order does not matter


def test_each_franchise_is_judged_on_its_own_seasons():
    assert team_tiers(_inst((4, 2002), (3, 2002), (4, 2004)), make_teams()) == {4: 1, 3: 1}
    assert team_tiers(_inst((4, 2002), (3, 2002)), make_teams()) == {4: 4, 3: 1}
