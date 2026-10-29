import pandas as pd

from teams import build_teams, season_team_names
from testdata import team_box


def test_one_record_per_franchise_with_every_name_and_its_seasons():
    parts = [
        team_box(1, season=2002, home=25, away=2, home_name="Seattle SuperSonics", away_name="Boston Celtics"),
        team_box(2, season=2008, home=25, away=2, home_name="Seattle SuperSonics", away_name="Boston Celtics"),
        team_box(3, season=2009, home=25, away=2, home_name="Oklahoma City Thunder", away_name="Boston Celtics"),
        team_box(4, season=2010, home=25, away=2, home_name="Oklahoma City Thunder", away_name="Boston Celtics"),
    ]
    raw = pd.concat(parts, ignore_index=True)
    tg = raw[["game_id", "team_id"]]
    t = build_teams(season_team_names(raw, tg)).set_index("team_id")
    assert len(t) == 2
    okc = t.loc[25]
    assert okc["current_name"] == "Oklahoma City Thunder"
    assert [(n["name"], n["seasons"]) for n in okc["names"]] == [("Seattle SuperSonics", [2002, 2008]), ("Oklahoma City Thunder", [2009, 2010])]
    assert (okc["first_season"], okc["last_season"]) == (2002, 2010)
    assert len(t.loc[2]["names"]) == 1


def test_stray_line_breaks_in_a_name_are_cleaned_and_merge_with_the_clean_spelling():
    parts = [
        team_box(1, season=2006, home=3, away=2, home_name="NO/Oklahoma City\r\n Hornets"),
        team_box(2, season=2007, home=3, away=2, home_name="NO/Oklahoma City Hornets"),
    ]
    raw = pd.concat(parts, ignore_index=True)
    t = build_teams(season_team_names(raw, raw[["game_id", "team_id"]])).set_index("team_id")
    names = t.loc[3]["names"]
    assert len(names) == 1 and names[0]["name"] == "NO/Oklahoma City Hornets" and names[0]["seasons"] == [2006, 2007]


def test_non_nba_teams_are_not_franchises():
    raw = team_box(1, home=111353, away=2, home_name="Team LeBron")
    t = build_teams(season_team_names(raw, raw[["game_id", "team_id"]]))
    assert t["team_id"].tolist() == [2]
