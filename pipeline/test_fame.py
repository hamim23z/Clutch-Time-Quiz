import pandas as pd
import pytest

from testtables import NO_OVERRIDES

from fame import best_seasons, compute_fame, load_overrides


STATS = ["points", "reb", "ast", "stl", "blk"]


def _games(rows, **extra):
    """rows: (player_id, season, season_type, games, points_each); extra: per-game reb/ast/stl/blk for every row."""
    out = []
    for pid, season, stype, count, pts in rows:
        for i in range(count):
            out.append({"game_id": f"{pid}-{season}-{stype}-{i}", "player_id": pid, "season": season,
                        "season_type": stype, "points": pts, "reb": 0, "ast": 0, "stl": 0, "blk": 0, **extra})
    return pd.DataFrame(out).astype({c: "Int16" for c in STATS})


def compute(pg, players, min_games=40, overrides=NO_OVERRIDES):
    return compute_fame(pg, players, min_games, overrides)


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
    assert compute(pg, _players([1]), 40).iloc[0]["career_points"] == 200


def test_fame_is_the_better_of_career_rank_and_ppg_rank():
    pg = _games([
        (1, 2003, "regular", 80, 20),  # career 1600, ppg 20
        (1, 2004, "regular", 80, 20),  # career 3200
        (2, 2003, "regular", 45, 30),  # short career: 1350 points, ppg 30 -> best ppg
        (3, 2003, "regular", 50, 10),  # 500 points, ppg 10
    ])
    fame = compute(pg, _players([1, 2, 3]), 40).set_index("player_id")
    assert fame.loc[1, "points_rank"] == 1 and fame.loc[1, "ppg_rank"] == 2 and fame.loc[1, "fame_rank"] == 1
    assert fame.loc[2, "points_rank"] == 2 and fame.loc[2, "ppg_rank"] == 1 and fame.loc[2, "fame_rank"] == 1
    assert fame.loc[2, "fame_source"] == "best points per game" and fame.loc[1, "fame_source"] == "career points"
    assert fame.loc[3, "fame_rank"] == 3


def test_percentile_uses_all_players_and_rank_one_is_most_famous():
    pg = _games([(i, 2003, "regular", 10, 100 - i) for i in range(1, 11)])  # nobody reaches 40 games
    fame = compute(pg, _players(range(1, 11)), 40).set_index("player_id")
    assert fame.loc[1, "points_rank"] == 1 and fame.loc[1, "fame_pct"] == 10
    assert fame.loc[10, "points_rank"] == 10 and fame.loc[10, "fame_pct"] == 100
    assert fame["ppg_rank"].isna().all()  # no 40-game season, no ppg rank
    assert (fame["fame_rank"] == fame["points_rank"]).all()


def test_players_without_a_40_game_season_still_get_a_tier():
    pg = _games([(1, 2003, "regular", 10, 5)])
    fame = compute(pg, _players([1]), 40).iloc[0]
    assert fame["tier"] == 6 and fame["points"] == 100  # rank 1 of 1 player is the 100th percentile


def test_ties_share_the_better_rank():
    pg = _games([(1, 2003, "regular", 10, 10), (2, 2003, "regular", 10, 10), (3, 2003, "regular", 10, 1)])
    fame = compute(pg, _players([1, 2, 3]), 40).set_index("player_id")
    assert fame.loc[1, "points_rank"] == 1 and fame.loc[2, "points_rank"] == 1 and fame.loc[3, "points_rank"] == 3


def test_tiers_follow_the_cutoffs_across_a_population():
    pg = _games([(i, 2003, "regular", 1, 1000 - i) for i in range(1, 101)])
    fame = compute(pg, _players(range(1, 101)), 40).set_index("player_id")
    assert [int((fame["tier"] == t).sum()) for t in range(1, 7)] == [3, 7, 15, 25, 25, 25]
    assert fame.loc[3, "tier"] == 1 and fame.loc[4, "tier"] == 2 and fame.loc[100, "tier"] == 6


def test_a_player_missing_from_the_players_table_is_an_error():
    with pytest.raises(ValueError):
        compute(_games([(1, 2003, "regular", 1, 5)]), _players([2]), 40)


def _players_named(n):
    return _players(range(1, n + 1))


def test_rebounds_assists_and_steals_plus_blocks_each_count():
    # four players with equal points; each is the leader of one other metric, a fifth leads nothing
    base = [(i, 2003, "regular", 10, 5) for i in range(1, 6)]
    pg = _games(base)
    pg.loc[pg.player_id == 1, "reb"] = 20
    pg.loc[pg.player_id == 2, "ast"] = 20
    pg.loc[pg.player_id == 3, "stl"] = 7
    pg.loc[pg.player_id == 3, "blk"] = 7
    pg.loc[pg.player_id == 4, "blk"] = 1  # a little, so steals and blocks add up for player 3 only
    fame = compute(pg, _players_named(5)).set_index("player_id")
    assert fame.loc[1, "reb_rank"] == 1 and fame.loc[2, "ast_rank"] == 1
    assert fame.loc[3, "stocks_rank"] == 1 and fame.loc[4, "stocks_rank"] == 2
    assert fame.loc[1, "fame_source"] == "career points"  # tie on points: the first metric listed wins
    assert fame.loc[1:3, "fame_rank"].tolist() == [1, 1, 1]


def test_fame_rank_is_the_lowest_of_the_five_ranks_and_names_its_metric():
    pg = _games([(1, 2003, "regular", 10, 30), (2, 2003, "regular", 10, 1), (3, 2003, "regular", 10, 2)])
    pg.loc[pg.player_id == 2, "reb"] = 15
    fame = compute(pg, _players_named(3)).set_index("player_id")
    assert fame.loc[2, "points_rank"] == 3 and fame.loc[2, "reb_rank"] == 1
    assert fame.loc[2, "fame_rank"] == 1 and fame.loc[2, "fame_source"] == "career rebounds"


def test_steals_and_blocks_are_added_together():
    pg = _games([(1, 2003, "regular", 10, 0), (2, 2003, "regular", 10, 0)])
    pg.loc[pg.player_id == 1, ["stl", "blk"]] = 3  # 6 a game
    pg.loc[pg.player_id == 2, "stl"] = 5  # 5 a game, but only steals
    fame = compute(pg, _players_named(2)).set_index("player_id")
    assert fame.loc[1, "career_stocks"] == 60 and fame.loc[2, "career_stocks"] == 50
    assert fame.loc[1, "stocks_rank"] == 1


def test_missing_steals_and_blocks_count_as_zero():
    pg = _games([(1, 2003, "regular", 3, 4)])
    pg["stl"] = pd.array([None, 2, 2], dtype="Int16")
    assert compute(pg, _players_named(1)).iloc[0]["career_stocks"] == 4


def test_an_override_sets_tier_and_points_but_not_the_percentile():
    pg = _games([(i, 2003, "regular", 1, 100 - i) for i in range(1, 11)])
    ov = pd.DataFrame({"athlete_id": [10], "tier": [1], "reason": ["a famous player with a short window"]})
    fame = compute(pg, _players_named(10), overrides=ov).set_index("player_id")
    assert fame.loc[10, "tier"] == 1 and fame.loc[10, "points"] == 10
    assert fame.loc[10, "fame_pct"] == 100 and fame.loc[10, "override_reason"] == "a famous player with a short window"
    assert fame.loc[9, "override_reason"] == "" and fame.loc[9, "tier"] == 6


def test_an_override_for_an_unknown_athlete_is_an_error():
    ov = pd.DataFrame({"athlete_id": [99], "tier": [1], "reason": ["x"]})
    with pytest.raises(ValueError):
        compute(_games([(1, 2003, "regular", 1, 5)]), _players_named(1), overrides=ov)


def test_overrides_file_rules(tmp_path):
    def load(text):
        p = tmp_path / "o.csv"
        p.write_text(text)
        return load_overrides(p)

    assert len(load("athlete_id,tier,reason\n5,2,\"Because, commas\"\n")) == 1
    for bad in ("athlete_id,tier,reason\n5,7,x\n", "athlete_id,tier,reason\n5,0,x\n", "athlete_id,tier,reason\n5,2,\n",
                "athlete_id,tier,reason\n5,2,x\n5,3,y\n", "id,tier,reason\n5,2,x\n"):
        with pytest.raises(ValueError):
            load(bad)
    assert load_overrides(tmp_path / "missing.csv").empty


def test_the_real_overrides_file_is_valid_and_short():
    overrides = load_overrides()
    assert 1 <= len(overrides) <= 15
    assert overrides["reason"].str.len().max() < 200
