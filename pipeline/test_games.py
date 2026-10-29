import pandas as pd

from boxscores import build_team_games
from games import REGULAR, PLAYOFFS, add_series_info, select_games
from testdata import officials_box, player_box, schedule, team_box  # noqa: F401


def full_box(game_ids, **kw):
    team = pd.concat([team_box(g, **kw) for g in game_ids], ignore_index=True)
    player = player_box(*[{"game_id": g, "athlete_id": 1000 + g, "points": 10.0} for g in game_ids])
    return team, player


def test_exhibition_and_non_game_types_are_excluded_and_season_type_is_recorded():
    sched = schedule(
        {"game_id": 1},  # regular season
        {"game_id": 2, "season_type": 3, "type_abbreviation": "RD16", "game_date": "2024-04-20"},  # playoffs
        {"game_id": 3, "type_abbreviation": "ALLSTAR", "home_id": 31, "away_id": 32},  # All-Star game
        {"game_id": 4, "home_id": 111386, "away_id": 111387},  # USA vs World, typed STD in season_type 2
        {"game_id": 5, "type_abbreviation": "CC"},  # NBA Cup final: season_type 2, not a regular-season game
        {"game_id": 6, "season_type": 5},  # play-in
        {"game_id": 7, "status_type_name": "STATUS_POSTPONED"},
        {"game_id": 8, "season_type": 1},  # preseason
        {"game_id": 9, "home_id": 111353, "away_id": 6},  # one non-NBA side is enough
    )
    team, player = full_box([1, 2])
    sel = select_games(sched, team, player)
    assert sorted(sel.games["game_id"]) == [1, 2]
    assert dict(zip(sel.games["game_id"], sel.games["season_type"])) == {1: REGULAR, 2: PLAYOFFS}
    assert sel.excluded == {"not_final": 1, "all_star": 1, "cup_final": 1, "play_in": 1, "non_nba_team": 2, "other_type": 1}
    assert sel.skipped.empty


def test_non_nba_teams_never_reach_team_games():
    games = pd.DataFrame({"game_id": [1], "season_type": [REGULAR]})
    team = pd.concat([team_box(1), team_box(2, home=111353, away=111354)], ignore_index=True)
    tg = build_team_games(team, games)
    assert sorted(tg["team_id"]) == [2, 6]
    assert set(tg["game_id"]) == {1}


def test_games_with_no_box_rows_are_skipped_and_listed_with_a_reason():
    sched = schedule({"game_id": 1}, {"game_id": 2}, {"game_id": 3}, {"game_id": 4})
    team = pd.concat([team_box(1), team_box(2)], ignore_index=True)  # 3 and 4 have no team rows
    player = player_box(
        {"game_id": 1, "athlete_id": 11, "points": 8.0},
        {"game_id": 3, "athlete_id": 33, "points": 8.0},
        {"game_id": 4, "athlete_id": 44, "points": None},  # only a non-player row: still no player rows
    )
    sel = select_games(sched, team, player)
    assert sel.games["game_id"].tolist() == [1]
    reasons = dict(zip(sel.skipped["game_id"], sel.skipped["reason"]))
    assert reasons == {2: "no_player_rows", 3: "no_team_rows", 4: "no_team_and_player_rows"}


def test_overtime_flag_and_dates():
    sched = schedule({"game_id": 1, "status_period": 5}, {"game_id": 2, "status_period": 4})
    team, player = full_box([1, 2])
    games = select_games(sched, team, player).games.set_index("game_id")
    assert games.loc[1, "overtime"] and games.loc[1, "periods"] == 5
    assert not games.loc[2, "overtime"]
    assert str(games.loc[1, "game_date"]) == "2024-01-01"


def test_series_numbers_and_finals_are_derived_from_dates():
    def po(game_id, date, home, away):
        return {"game_id": game_id, "season_type": PLAYOFFS, "type_abbreviation": "STD", "game_date": date, "home_team_id": home, "away_team_id": away}
    rows = [
        po(1, "2024-04-20", 2, 6), po(2, "2024-04-22", 6, 2), po(3, "2024-04-25", 2, 6),  # series A
        po(4, "2024-04-21", 7, 8), po(5, "2024-04-23", 8, 7),  # series B
        po(6, "2024-06-05", 13, 14), po(7, "2024-06-08", 14, 13),  # the last playoff series: the Finals
    ]
    games = pd.DataFrame(rows).assign(season=2024)
    out = add_series_info(games).set_index("game_id")
    assert out["series_game"].tolist() == [1, 2, 3, 1, 2, 1, 2]
    assert out["is_finals"].tolist() == [False] * 5 + [True, True]


def test_regular_season_games_have_no_series_number():
    games = pd.DataFrame({"game_id": [1], "season": [2024], "season_type": [REGULAR], "game_date": ["2024-01-01"], "home_team_id": [2], "away_team_id": [6]})
    out = add_series_info(games)
    assert out["series_game"].isna().all() and not out["is_finals"].any()
