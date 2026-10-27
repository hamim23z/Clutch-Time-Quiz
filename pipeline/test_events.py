import pytest

from events import (
    FOUL,
    FREE_THROW,
    MADE_SHOT,
    OTHER,
    REBOUND,
    SHOT,
    TIMEOUT,
    TURNOVER,
    classify_event,
    foul_kind,
    is_three_attempt,
    parse_free_throw,
)


@pytest.mark.parametrize(
    "type_text, shooting, scoring, expected",
    [
        ("Jump Shot", True, True, MADE_SHOT),
        ("Driving Layup Shot", True, False, SHOT),
        ("Free Throw - 1 of 2", True, True, FREE_THROW),
        ("Free Throw - Technical", True, False, FREE_THROW),
        ("Full Timeout", False, False, TIMEOUT),
        ("Short Timeout", False, False, TIMEOUT),
        ("Defensive Rebound", False, False, REBOUND),
        ("Offensive Rebound", False, False, REBOUND),
        ("Rebound", False, False, REBOUND),
        ("Bad Pass\nTurnover", False, False, TURNOVER),
        ("Shot Clock Turnover", False, False, TURNOVER),
        ("Traveling", False, False, TURNOVER),
        ("Excess Timeout Turnover", False, False, TURNOVER),
        ("Offensive Foul Turnover", False, False, TURNOVER),
        ("No Turnover", False, False, OTHER),
        ("Shooting Foul", False, False, FOUL),
        ("Personal Take Foul", False, False, FOUL),
        ("Offensive Charge", False, False, FOUL),
        ("Technical Foul", False, False, FOUL),
        ("Defensive 3-Seconds Technical", False, False, FOUL),
        ("Substitution", False, False, OTHER),
        ("End Period", False, False, OTHER),
        ("Jumpball", False, False, OTHER),
        ("Coach's Challenge (Stands)", False, False, OTHER),
    ],
)
def test_classify_event(type_text, shooting, scoring, expected):
    assert classify_event(type_text, shooting, scoring) == expected


@pytest.mark.parametrize(
    "text, event_type, expected",
    [
        ("Jaylen Brown misses 24-foot three point jumper", SHOT, True),
        ("Fred VanVleet makes 28-foot three pointer", MADE_SHOT, True),
        ("Stephon Marbury missed Three Point Jumper.", SHOT, True),  # 2002 wording
        ("Derek Fisher made 25 ft Three Point Jumper. Assisted by Shaquille O'Neal.", MADE_SHOT, True),
        ("Jordan Poole misses 26-foot step back jumpshot", SHOT, True),  # no "three point": distance fallback
        ("Kyle Lowry makes 26-foot  ", MADE_SHOT, True),
        ("Zach LaVine misses 21-foot jumper", SHOT, False),
        ("Jayson Tatum makes 23-foot pullup jump shot", MADE_SHOT, False),  # 23 ft can be a two
        ("Nikola Jokic misses two point shot", SHOT, False),
        ("Luka Doncic makes driving layup", MADE_SHOT, False),
        ("Mikal Bridges makes free throw 1 of 2", FREE_THROW, False),
        ("Boston three point rebound", REBOUND, False),  # only shots can be three-point attempts
    ],
)
def test_is_three_attempt(text, event_type, expected):
    assert is_three_attempt(text, event_type) is expected


def test_parse_free_throw():
    assert parse_free_throw("Free Throw - 1 of 2") == ("regular", 1, 2)
    assert parse_free_throw("Free Throw - 1 of 1") == ("regular", 1, 1)
    assert parse_free_throw("Free Throw - 3 of 3") == ("regular", 3, 3)
    assert parse_free_throw("Free Throw - Flagrant 2 of 2") == ("flagrant", 2, 2)
    assert parse_free_throw("Free Throw - Clear Path 1 of 2") == ("clear_path", 1, 2)
    assert parse_free_throw("Free Throw - Technical") is None
    assert parse_free_throw("Jump Shot") is None


def test_foul_kind():
    assert foul_kind("Shooting Foul") == "defensive"
    assert foul_kind("Loose Ball Foul") == "defensive"
    assert foul_kind("Flagrant Foul Type 1") == "defensive"
    assert foul_kind("Offensive Foul") == "offensive"
    assert foul_kind("Offensive Charge") == "offensive"
    assert foul_kind("Technical Foul") == "technical"
    assert foul_kind("Flopping Technical") == "technical"
    assert foul_kind("Double Personal Foul") == "double"
