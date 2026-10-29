import pandas as pd
import pytest

from fame import best_seasons, compute_fame


def _games(rows):
    """rows: (player_id, season, season_type, games, points_each)"""
    out = []
    for pid, season, stype, count, pts in rows:
        for i in range(count):
            out.append({"game_id": f"{pid}-{season}-{stype}-{i}", "player_id": pid, "season": season,
                        "season_type": stype, "points": pts})
    return pd.DataFrame(out).astype({"points": "Int16"})


def _players(ids):
    return pd.DataFrame({"player_id": ids, "unique_name": [f"P{i}" for i in ids]})


def test_best_season_needs_the_minimum_games():
    pg = _games([(1, 2003, "regular", 39, 40), (1, 2004, "regular", 40, 10)])
    best = best_seasons(pg, 40).set_index("player_id")
    assert best.loc[1, "best_ppg"] == 10 and best.loc[1, "best_ppg_season"] == 2004  # the 39-game season is ignored
    assert 1 not in best_seasons(_games([(1, 2003, "regular", 39, 40)]), 40)["player_id"].tolist()


def test_best_season_adds_up_games_for_all_teams_and_ignores_playoffs():
    pg = _games([(1, 2003, "regular", 25, 20), (1, 2003, "regular", 25, 30), (1, 2003, "playoffs", 20, 60)])
    best = best_seasons(pg, 40).iloc[0]
    assert best["best_ppg"] == 25 and best["best_ppg_games"] == 50


def test_best_season_tie_goes_to_the_later_season():
    pg = _games([(1, 2003, "regular", 50, 20), (1, 2005, "regular", 50, 20)])
    assert best_seasons(pg, 40).iloc[0]["best_ppg_season"] == 2005


def test_career_points_include_playoffs():
    pg = _games([(1, 2003, "regular", 10, 10), (1, 2003, "playoffs", 5, 20)])
    assert compute_fame(pg, _players([1]), 40).iloc[0]["career_points"] == 200


def test_fame_is_the_better_of_career_rank_and_ppg_rank():
    pg = _games([
        (1, 2003, "regular", 80, 20),  # career 1600, ppg 20
        (1, 2004, "regular", 80, 20),  # career 3200
        (2, 2003, "regular", 45, 30),  # short career: 1350 points, ppg 30 -> best ppg
        (3, 2003, "regular", 50, 10),  # 500 points, ppg 10
    ])
    fame = compute_fame(pg, _players([1, 2, 3]), 40).set_index("player_id")
    assert fame.loc[1, "career_rank"] == 1 and fame.loc[1, "ppg_rank"] == 2 and fame.loc[1, "fame_rank"] == 1
    assert fame.loc[2, "career_rank"] == 2 and fame.loc[2, "ppg_rank"] == 1 and fame.loc[2, "fame_rank"] == 1
    assert fame.loc[2, "fame_source"] == "ppg" and fame.loc[1, "fame_source"] == "career"
    assert fame.loc[3, "fame_rank"] == 3


def test_percentile_uses_all_players_and_rank_one_is_most_famous():
    pg = _games([(i, 2003, "regular", 10, 100 - i) for i in range(1, 11)])  # nobody reaches 40 games
    fame = compute_fame(pg, _players(range(1, 11)), 40).set_index("player_id")
    assert fame.loc[1, "career_rank"] == 1 and fame.loc[1, "career_pct"] == 10
    assert fame.loc[10, "career_rank"] == 10 and fame.loc[10, "career_pct"] == 100
    assert fame["ppg_rank"].isna().all()  # no 40-game season, no ppg rank
    assert (fame["fame_rank"] == fame["career_rank"]).all()


def test_players_without_a_40_game_season_still_get_a_tier():
    pg = _games([(1, 2003, "regular", 10, 5)])
    fame = compute_fame(pg, _players([1]), 40).iloc[0]
    assert fame["tier"] == 6 and fame["points"] == 100  # rank 1 of 1 player is the 100th percentile


def test_ties_share_the_better_rank():
    pg = _games([(1, 2003, "regular", 10, 10), (2, 2003, "regular", 10, 10), (3, 2003, "regular", 10, 1)])
    fame = compute_fame(pg, _players([1, 2, 3]), 40).set_index("player_id")
    assert fame.loc[1, "career_rank"] == 1 and fame.loc[2, "career_rank"] == 1 and fame.loc[3, "career_rank"] == 3


def test_tiers_follow_the_cutoffs_across_a_population():
    pg = _games([(i, 2003, "regular", 1, 1000 - i) for i in range(1, 101)])
    fame = compute_fame(pg, _players(range(1, 101)), 40).set_index("player_id")
    assert [int((fame["tier"] == t).sum()) for t in range(1, 7)] == [3, 7, 15, 25, 25, 25]
    assert fame.loc[3, "tier"] == 1 and fame.loc[4, "tier"] == 2 and fame.loc[100, "tier"] == 6


def test_a_player_missing_from_the_players_table_is_an_error():
    with pytest.raises(ValueError):
        compute_fame(_games([(1, 2003, "regular", 1, 5)]), _players([2]), 40)
