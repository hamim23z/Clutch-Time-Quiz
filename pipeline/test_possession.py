"""Hand-checked possession sequences. Each row: what happened, and who has the ball afterwards."""
import pandas as pd

from events import classify_event
from possession import AWAY, CERTAIN, HOME, LOOSE, UNKNOWN, infer_possession


def build(rows, game=1, period=4):
    """rows: (type_text, side, opts) where opts may hold pts (points scored), shot (bool)."""
    out, home, away = [], 0, 0
    for type_text, side, *rest in rows:
        opts = rest[0] if rest else {}
        pts = opts.get("pts", 0)
        if pts and opts.get("scorer", side) == HOME:
            home += pts
        elif pts:
            away += pts
        shooting = opts.get("shot", False)
        event_type = classify_event(type_text, shooting, pts > 0)
        out.append(
            dict(
                game_id=opts.get("game", game),
                period=opts.get("period", period),
                event_type=event_type,
                type_text=type_text,
                side=side,
                scoring_play=pts > 0,
                home_score=home,
                away_score=away,
            )
        )
    return pd.DataFrame(out)


def check(rows, expected):
    teams, statuses = infer_possession(build(rows))
    got = list(zip(teams, statuses))
    assert got == expected, "\n".join(f"{r[0]:<28} got {g} want {w}" for r, g, w in zip(rows, got, expected))


def test_miss_rebound_make_turnover_foul():
    check(
        [
            ("Jump Shot", HOME, {"shot": True}),  # miss
            ("Defensive Rebound", AWAY),
            ("Jump Shot", AWAY, {"shot": True, "pts": 2}),  # make: ball goes to home
            ("Lost Ball Turnover", HOME),  # home turns it over
            ("Personal Foul", HOME),  # home fouls away: away keeps the ball
            ("Substitution", AWAY),
        ],
        [
            (HOME, LOOSE),
            (AWAY, CERTAIN),
            (HOME, CERTAIN),
            (AWAY, CERTAIN),
            (AWAY, CERTAIN),
            (AWAY, CERTAIN),
        ],
    )


def test_two_shot_trip_then_defensive_rebound_then_offensive_foul():
    check(
        [
            ("Shooting Foul", HOME),  # home fouls away
            ("Free Throw - 1 of 2", AWAY, {"pts": 1}),
            ("Free Throw - 2 of 2", AWAY),  # missed
            ("Defensive Rebound", HOME),
            ("Full Timeout", AWAY),
            ("Offensive Foul", HOME),  # home commits it: away gets the ball
            ("Offensive Foul Turnover", HOME),  # the paired turnover row changes nothing more
        ],
        [
            (AWAY, CERTAIN),
            (AWAY, CERTAIN),  # more free throws coming: shooter keeps the ball
            (AWAY, LOOSE),  # missed last free throw: live ball
            (HOME, CERTAIN),
            (HOME, CERTAIN),
            (AWAY, CERTAIN),
            (AWAY, CERTAIN),
        ],
    )


def test_made_last_free_throw_gives_ball_to_other_team():
    check(
        [
            ("Free Throw - 1 of 2", AWAY, {"pts": 1}),
            ("Free Throw - 2 of 2", AWAY, {"pts": 1}),
            ("Free Throw - 1 of 1", HOME, {"pts": 1}),
            ("Free Throw - 3 of 3", AWAY, {"pts": 1}),
        ],
        [(AWAY, CERTAIN), (HOME, CERTAIN), (AWAY, CERTAIN), (HOME, CERTAIN)],
    )


def test_technical_foul_and_technical_free_throw_do_not_change_possession():
    check(
        [
            ("Personal Foul", AWAY),  # home has the ball
            ("Technical Foul", AWAY),
            ("Free Throw - Technical", HOME, {"pts": 1}),
            ("Double Personal Foul", HOME),
        ],
        [(HOME, CERTAIN)] * 4,
    )


def test_flagrant_trip_keeps_ball_with_the_shooting_team_even_when_made():
    check(
        [
            ("Flagrant Foul Type 1", AWAY),
            ("Free Throw - Flagrant 1 of 2", HOME, {"pts": 1}),
            ("Free Throw - Flagrant 2 of 2", HOME, {"pts": 1}),
            ("Free Throw - Clear Path 1 of 2", HOME, {"pts": 1}),
            ("Free Throw - Clear Path 2 of 2", HOME),  # missed: live ball
        ],
        [(HOME, CERTAIN)] * 4 + [(HOME, LOOSE)],
    )


def test_jump_ball_goes_to_the_team_in_team_id():
    check(
        [("Jumpball", HOME), ("Jumpball", None)],
        [(HOME, CERTAIN), (None, UNKNOWN)],
    )


def test_state_resets_at_the_start_of_each_period_and_game():
    rows = [
        ("Defensive Rebound", HOME),
        ("Substitution", None, {"period": 5}),  # new period: nothing decided yet
        ("Defensive Rebound", AWAY, {"period": 5}),
        ("Substitution", None, {"game": 2, "period": 5}),  # new game
    ]
    check(rows, [(HOME, CERTAIN), (None, UNKNOWN), (AWAY, CERTAIN), (None, UNKNOWN)])


# A score change needs a previous row to compare with, so the first row of a period has no
# "scorer"; that never matters in practice because the first row is minutes before the window.
def test_defensive_goaltending_awards_the_basket_and_the_defense_inbounds():
    # home shoots, away is called for goaltending: home is credited 2 and away gets the ball
    check(
        [("Substitution", None), ("Defensive Goaltending", AWAY, {"pts": 2, "scorer": HOME})],
        [(None, UNKNOWN), (AWAY, CERTAIN)],
    )


def test_made_shot_without_team_id_uses_the_team_whose_score_rose():
    check(
        [("Substitution", None), ("Jump Shot", None, {"shot": True, "pts": 3, "scorer": HOME})],
        [(None, UNKNOWN), (AWAY, CERTAIN)],
    )


def test_rebound_without_team_id_follows_the_rebound_type():
    check(
        [
            ("Jump Shot", HOME, {"shot": True}),
            ("Offensive Rebound", None),
            ("Jump Shot", HOME, {"shot": True}),
            ("Defensive Rebound", None),
            ("Rebound", None),
        ],
        [(HOME, LOOSE), (HOME, CERTAIN), (HOME, LOOSE), (AWAY, CERTAIN), (None, UNKNOWN)],
    )


def test_loose_ball_stays_loose_through_substitutions_and_timeouts():
    check(
        [
            ("Jump Shot", AWAY, {"shot": True}),
            ("Substitution", None),
            ("Full Timeout", HOME),
            ("Defensive Rebound", HOME),
        ],
        [(AWAY, LOOSE), (AWAY, LOOSE), (AWAY, LOOSE), (HOME, CERTAIN)],
    )


def test_kicked_ball_by_defense_keeps_ball_with_offense_and_missing_team_id_is_unknown():
    check(
        [
            ("Kicked Ball", AWAY),
            ("Bad Pass\nTurnover", None),
            ("Shooting Foul", None),
        ],
        [(HOME, CERTAIN), (None, UNKNOWN), (None, UNKNOWN)],
    )


def test_end_of_period_rows_keep_the_last_known_possession():
    check(
        [("Defensive Rebound", AWAY), ("End Period", None), ("End Game", None)],
        [(AWAY, CERTAIN)] * 3,
    )
