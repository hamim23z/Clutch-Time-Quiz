import pandas as pd

from boxscores import build_player_games, build_team_games
from games import PLAYOFFS, REGULAR
from testdata import player_box, team_box


def games_table(*ids):
    return pd.DataFrame({"game_id": list(ids), "season_type": [REGULAR] * len(ids)})


def test_a_player_played_only_if_points_is_present_not_if_did_not_play_says_so():
    raw = player_box(
        {"athlete_id": 1, "points": 12.0, "did_not_play": True},  # flag says no, but there are stats: played
        {"athlete_id": 2, "points": None, "did_not_play": False},  # flag says yes, but no stats: did not play (2006-2012 style)
        {"athlete_id": 3, "points": 0.0, "minutes": 0.0, "did_not_play": False},  # zero points is still a value: played
        {"athlete_id": None, "points": 0.0},  # stat line with no athlete id
        {"athlete_id": 5, "points": None, "did_not_play": True},
    )
    pg = build_player_games(raw, games_table(1))
    assert sorted(pg["player_id"]) == [1, 3]
    assert pg.set_index("player_id").loc[1, "points"] == 12


def test_player_games_only_cover_kept_games_and_carry_the_season_type():
    raw = player_box({"game_id": 1, "athlete_id": 1, "points": 5.0}, {"game_id": 2, "athlete_id": 2, "points": 5.0})
    games = pd.DataFrame({"game_id": [1], "season_type": [PLAYOFFS]})
    pg = build_player_games(raw, games)
    assert pg["game_id"].tolist() == [1] and pg["season_type"].tolist() == [PLAYOFFS]


def test_player_stat_columns_are_renamed_and_typed():
    raw = player_box({"athlete_id": 7, "points": 41.0, "rebounds": 9.0, "assists": 10.0, "three_point_field_goals_made": 6.0, "starter": True})
    row = build_player_games(raw, games_table(1)).iloc[0]
    assert (row["points"], row["reb"], row["ast"], row["fg3m"]) == (41, 9, 10, 6)
    assert bool(row["started"]) is True and row["home_away"] == "home"


def test_team_games_have_two_rows_per_game_and_a_won_flag():
    tg = build_team_games(team_box(1, home_score=101, away_score=99), games_table(1))
    assert len(tg) == 2
    rows = tg.set_index("team_id")
    assert bool(rows.loc[2, "won"]) and not bool(rows.loc[6, "won"])
    assert rows.loc[2, "opponent_score"] == 99 and rows.loc[2, "team_score"] == 101
