"""Normalize stage on small raw samples from an old (2002), middle (2013) and recent (2024) season."""
from pathlib import Path

import pandas as pd
import pytest

from columns import standardize
from normalize import EVENT_COLUMNS, GAME_COLUMNS, WINDOW_SECONDS, normalize_season

FIXTURES = Path(__file__).parent / "fixtures"
SEASONS = [2002, 2013, 2024]
EVENT_TYPES = {"shot", "made_shot", "free_throw", "foul", "timeout", "rebound", "turnover", "other"}


@pytest.fixture(scope="module")
def raw() -> dict[int, pd.DataFrame]:
    return {s: pd.read_parquet(FIXTURES / f"raw_{s}.parquet") for s in SEASONS}


@pytest.fixture(scope="module")
def result(raw):
    return {s: normalize_season(df) for s, df in raw.items()}


def play_text(raw_df: pd.DataFrame) -> dict[tuple[int, int], str]:
    return {(g, p): t for g, p, t in zip(raw_df.game_id, raw_df.game_play_number, raw_df.text)}


def find(result_season, raw_df, text_part, nth=0):
    """The nth event whose raw play text contains text_part (in clock order)."""
    texts = play_text(raw_df)
    e = result_season.events
    hits = e[[text_part in texts[(g, p)] for g, p in zip(e.game_id, e.play_id)]]
    assert len(hits) > nth, f"no event with text {text_part!r}"
    return hits.iloc[nth]


@pytest.mark.parametrize("season", SEASONS)
def test_each_season_normalizes_with_the_same_columns(season, result):
    r = result[season]
    assert list(r.events.columns) == EVENT_COLUMNS
    assert list(r.games.columns) == GAME_COLUMNS
    e = r.events
    assert len(e) > 20
    assert set(e.event_type.astype(str)) <= EVENT_TYPES
    assert (e.quarter >= 4).all()
    assert e.secs_period.between(0, WINDOW_SECONDS).all()
    assert (e.season == season).all()
    assert r.stats["events"] == len(e)
    assert r.stats["certain"] + r.stats["loose"] + r.stats["unknown"] == len(e)


@pytest.mark.parametrize("season", SEASONS)
def test_clock_never_runs_backwards_and_seq_counts_up(season, result):
    e = result[season].events
    for _, g in e.groupby("game_id"):
        assert g.seq.tolist() == list(range(len(g)))
        assert (g.groupby("quarter").secs_game.diff().dropna() <= 0).all()
        assert g.quarter.is_monotonic_increasing


@pytest.mark.parametrize("season", SEASONS)
def test_margin_is_from_the_view_of_the_team_with_the_ball(season, result):
    e = result[season].events
    has_ball = e.possession.notna()
    home = e[has_ball & (e.possession == "home")]
    away = e[has_ball & (e.possession == "away")]
    assert (home.margin == home.home_score - home.away_score).all()
    assert (away.margin == away.away_score - away.home_score).all()
    assert e[~has_ball].margin.isna().all()


@pytest.mark.parametrize("season", SEASONS)
def test_scores_never_go_down(season, result):
    e = result[season].events
    assert (e.groupby("game_id").home_score.diff().dropna() >= 0).all()
    assert (e.groupby("game_id").away_score.diff().dropna() >= 0).all()


def test_old_season_wording_is_understood(raw, result):
    # 2002 says "Three Point Jumper" and "made"/"missed", with no "makes" in the text
    r = result[2002]
    three = find(r, raw[2002], "Three Point Jumper")
    assert three.is_three
    assert three.event_type in ("shot", "made_shot")
    assert (r.events.event_type == "made_shot").any()
    assert (r.events.event_type == "timeout").any()


def test_overtimes_keep_their_own_last_three_minutes(result):
    e = result[2013].events
    assert sorted(e.quarter.unique()) == [4, 5, 6]
    for q in (4, 5, 6):
        g = e[e.quarter == q]
        assert g.secs_period.max() <= WINDOW_SECONDS
        assert g.secs_period.min() <= 10
    # in overtime the game clock is the overtime clock
    assert (e[e.quarter >= 5].secs_game == e[e.quarter >= 5].secs_period).all()


def test_timeouts_come_from_the_event_type_not_the_flag_columns(raw, result):
    # Short Timeout only exists in some seasons; both kinds must be found
    e = result[2013].events
    kinds = set(e[e.event_type == "timeout"].detail.astype(str))
    assert {"Full Timeout", "Short Timeout"} <= kinds
    assert not any(c.endswith("_timeout_called") for c in e.columns)


def test_seconds_left_uses_the_start_clock_not_the_end_clock(raw, result):
    # In the GS-OKC game, a substitution recorded at 16.1 s has end_game_seconds_remaining 0.0.
    r = result[2024]
    sub = find(r, raw[2024], "Moses Moody enters the game")
    assert sub.secs_game == pytest.approx(16.1)
    assert sub.secs_period == pytest.approx(16.1)


def test_games_table_has_names_final_score_and_periods(result):
    g = result[2013].games.iloc[0]
    assert (g.home_team, g.away_team) == ("Indiana Pacers", "Sacramento Kings")
    assert (g.final_home_score, g.final_away_score) == (106, 98)
    assert g.periods == 6
    assert g.season == 2013
    assert len(result[2024].games) == 3


def test_missing_columns_are_reported(raw):
    broken = raw[2024].drop(columns=["start_game_seconds_remaining"])
    with pytest.raises(KeyError, match="secs_game"):
        standardize(broken)


def test_alias_columns_are_accepted(raw):
    renamed = raw[2024].rename(columns={"period_number": "qtr"})
    pd.testing.assert_frame_equal(standardize(renamed), standardize(raw[2024]))


# --- the 3 games from the session 1 spike, checked by hand against the box of events ---------

# (raw text contains, possession after, status, margin for the team with the ball[, which match])
# The optional last number picks the nth play (in clock order) when the text occurs more than once.
GAME_1_BKN_AT_CHI = [
    ("Cam Thomas misses 32-foot three point", "away", "loose", 2),
    ("Nets offensive team rebound", "away", "certain", 2),
    ("shot clock turnover", "home", "certain", -2),  # Brooklyn turns it over, Chicago down 2
    ("Zach LaVine misses 12-foot pullup", "home", "loose", -2),
    ("Coby White offensive rebound", "home", "certain", -2),
    ("Royce O'Neale defensive rebound", "away", "certain", 2),
    ("Nikola Vucevic personal take foul", "away", "certain", 2),  # Chicago fouls, Brooklyn keeps it
    ("Mikal Bridges makes free throw 1 of 2", "away", "certain", 3),
    ("Mikal Bridges misses free throw 2 of 2", "away", "loose", 3),
    ("Alex Caruso defensive rebound", "home", "certain", -3),
    ("Ben Simmons personal foul", "home", "certain", -3),
    ("Zach LaVine makes free throw 1 of 2", "home", "certain", -2),
    ("Zach LaVine misses free throw 2 of 2", "home", "loose", -2),
    ("Zach LaVine offensive rebound", "home", "certain", -2),
    ("Day'Ron Sharpe defensive rebound", "away", "certain", 2),
]
GAME_2_GS_AT_OKC = [
    ("Stephen Curry makes driving layup", "home", "certain", 1, 0),  # first one, 55.1 s: OKC ball, up 1
    ("Jalen Williams lost ball turnover", "away", "certain", -1, 0),
    ("Klay Thompson makes free throw 1 of 2", "away", "certain", 0, 0),
    ("Klay Thompson makes free throw 2 of 2", "home", "certain", -1, 0),
    ("Chet Holmgren makes free throw 2 of 2", "away", "certain", -1, 0),
    ("Gary Payton II makes alley oop layup", "home", "certain", -1, 0),
    ("Luguentz Dort misses free throw 1 of 2", "home", "certain", -1, 0),  # more free throws to come
    ("Thunder offensive team rebound", "home", "certain", -1, 1),  # 16.1 s; an earlier one is at 140 s
    ("Luguentz Dort makes free throw 2 of 2", "away", "certain", 0, 0),
    ("Stephen Curry makes driving layup", "home", "certain", -2, 1),  # 2nd Curry layup: the buzzer beater
]
GAME_3_NO_AT_HOU = [
    ("Dyson Daniels lost ball turnover", "home", "certain", -2),
    ("Rockets offensive team rebound", "home", "certain", -2, 1),  # 55.1 s; an earlier one is at 104 s
    ("Fred VanVleet makes 28-foot three pointer", "away", "certain", -1),
    ("Brandon Ingram misses 25-foot three point", "away", "loose", -1),
    ("Alperen Sengun defensive rebound", "home", "certain", 1),
    ("Jordan Hawkins shooting foul", "home", "certain", 1),
    ("Fred VanVleet makes free throw 1 of 2", "home", "certain", 2),
    ("Fred VanVleet makes free throw 2 of 2", "away", "certain", -3),
    ("Brandon Ingram misses 24-foot three point", "away", "loose", -3),
    ("Tari Eason loose ball foul", "away", "certain", -3),
    ("Larry Nance Jr. misses free throw 1 of 2", "away", "certain", -3),
    ("Larry Nance Jr. makes free throw 2 of 2", "home", "certain", 2),
    ("Jalen Green misses free throw 1 of 2", "home", "certain", 2),
    ("Jalen Green makes free throw 2 of 2", "away", "certain", -3),
    ("Larry Nance Jr. out of bounds lost ball turnover", "home", "certain", 3),
]


def game_events(result_season, game_id):
    e = result_season.events
    return type(result_season)(e[e.game_id == game_id], result_season.games, result_season.stats)


@pytest.mark.parametrize(
    "game_id, expected",
    [(401584092, GAME_1_BKN_AT_CHI), (401584099, GAME_3_NO_AT_HOU)],
)
def test_spike_games_1_and_3(game_id, expected, raw, result):
    g = game_events(result[2024], game_id)
    for text, side, status, margin, *nth in expected:
        row = find(g, raw[2024], text, nth=nth[0] if nth else 0)
        assert (row.possession, row.possession_status, row.margin) == (side, status, margin), text


def test_spike_game_2(raw, result):
    g = game_events(result[2024], 401584093)
    for text, side, status, margin, nth in GAME_2_GS_AT_OKC:
        row = find(g, raw[2024], text, nth=nth)
        assert (row.possession, row.possession_status, row.margin) == (side, status, margin), text


def test_spike_games_have_flagged_threes(raw, result):
    g = result[2024].events
    texts = play_text(raw[2024])
    threes = [texts[(a, b)] for a, b, t in zip(g.game_id, g.play_id, g.is_three) if t]
    assert any("Cam Thomas misses 32-foot three point" in t for t in threes)
    assert any("Fred VanVleet makes 28-foot three pointer" in t for t in threes)
    assert not any("free throw" in t for t in threes)
    assert not any("21-foot jumper" in t for t in threes)


def test_next_shot_comes_from_the_team_we_said_had_the_ball(result):
    """Independent check: whoever has the ball after an event should take the next shot,
    free throw or turnover. Mismatches are and-ones and offensive foul pairs."""
    e = result[2024].events.reset_index(drop=True)
    acts = e.event_type.isin(["shot", "made_shot", "turnover"]) | (
        (e.event_type == "free_throw") & e.detail.astype(str).str.match(r"Free Throw - \d of \d")
    )
    side = e.acting_side.astype(object).where(acts)
    key = e.game_id.astype(str) + "-" + e.quarter.astype(str)
    nxt = side.groupby(key).transform(lambda s: s.bfill().shift(-1))
    sure = e[(e.possession_status == "certain") & nxt.notna() & (nxt != "")]
    agree = (nxt[sure.index] == sure.possession).mean()
    assert len(sure) > 80
    assert agree > 0.9, agree
