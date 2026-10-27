import pandas as pd

from events import classify_event
from ordering import TickEvent, reorder_tick, sort_and_repair


def tick(*specs: tuple[str, bool]) -> list[TickEvent]:
    """specs: (type_text, scoring). event_type is derived the same way the pipeline does."""
    out = []
    for type_text, scoring in specs:
        shooting = "Shot" in type_text or "Layup" in type_text
        out.append(TickEvent(type_text, classify_event(type_text, shooting, scoring), scoring))
    return out


def names(evs: list[TickEvent], order: list[int]) -> list[str]:
    return [evs[i].type_text for i in order]


def test_substitutions_go_last_in_original_order():
    evs = tick(
        ("Free Throw - 1 of 2", True),
        ("Substitution", False),
        ("Free Throw - 2 of 2", False),
        ("Substitution", False),
        ("Full Timeout", False),
    )
    order, _ = reorder_tick(evs, open_miss=False)
    assert order == [0, 2, 4, 1, 3]


def test_foul_listed_inside_a_free_throw_trip_moves_before_the_trip():
    evs = tick(("Free Throw - 1 of 2", True), ("Shooting Foul", False), ("Free Throw - 2 of 2", True))
    order, _ = reorder_tick(evs, open_miss=False)
    assert names(evs, order) == ["Shooting Foul", "Free Throw - 1 of 2", "Free Throw - 2 of 2"]


def test_foul_after_a_finished_trip_stays_put():
    evs = tick(("Free Throw - 1 of 2", True), ("Free Throw - 2 of 2", True), ("Shooting Foul", False))
    order, _ = reorder_tick(evs, open_miss=False)
    assert order == [0, 1, 2]


def test_technical_and_offensive_fouls_never_move():
    for foul in ("Technical Foul", "Offensive Foul", "Offensive Charge"):
        evs = tick(("Free Throw - 1 of 2", True), (foul, False), ("Free Throw - 2 of 2", True))
        order, _ = reorder_tick(evs, open_miss=False)
        assert order == [0, 1, 2], foul


def test_two_trips_in_one_tick_are_left_alone():
    # intentional fouling at the end of a game: foul, 2 free throws, rebound, foul, 2 free throws
    evs = tick(
        ("Shooting Foul", False),
        ("Free Throw - 1 of 2", True),
        ("Free Throw - 2 of 2", False),
        ("Offensive Rebound", False),
        ("Shooting Foul", False),
        ("Free Throw - 1 of 2", False),
        ("Free Throw - 2 of 2", True),
    )
    order, open_miss = reorder_tick(evs, open_miss=False)
    assert order == list(range(7))
    assert open_miss is False


def test_rebound_listed_before_its_putback_miss_moves_after_it():
    evs = tick(("Offensive Rebound", False), ("Tip Shot", False))
    order, open_miss = reorder_tick(evs, open_miss=False)
    assert names(evs, order) == ["Tip Shot", "Offensive Rebound"]
    assert open_miss is False


def test_rebound_after_an_open_miss_stays_put():
    evs = tick(("Offensive Rebound", False), ("Tip Shot", False))
    order, open_miss = reorder_tick(evs, open_miss=True)
    assert order == [0, 1]
    assert open_miss is True  # the tip shot missed and is waiting for its rebound


def test_rebound_with_its_miss_in_the_same_tick_stays_put():
    evs = tick(("Jump Shot", False), ("Defensive Rebound", False))
    order, open_miss = reorder_tick(evs, open_miss=False)
    assert order == [0, 1]
    assert open_miss is False


def test_made_putback_listed_before_its_offensive_rebound_swaps_with_it():
    evs = tick(("Layup Shot Putback", True), ("Offensive Rebound", False))
    order, open_miss = reorder_tick(evs, open_miss=True)  # a miss was waiting for its rebound
    assert names(evs, order) == ["Offensive Rebound", "Layup Shot Putback"]
    assert open_miss is False


def test_offensive_rebound_after_a_made_shot_stays_when_no_miss_was_waiting():
    evs = tick(("Layup Shot", True), ("Offensive Rebound", False))
    order, _ = reorder_tick(evs, open_miss=False)
    assert order == [0, 1]


def test_defensive_rebound_after_a_made_shot_is_not_swapped():
    evs = tick(("Layup Shot", True), ("Defensive Rebound", False))
    order, _ = reorder_tick(evs, open_miss=True)
    assert order == [0, 1]


def test_sort_is_stable_by_clock_and_keeps_play_order_on_ties():
    df = pd.DataFrame(
        {
            "game_id": [1, 1, 1, 1],
            "period": [4, 4, 4, 4],
            "secs_game": [10.0, 30.0, 10.0, 30.0],
            "play_order": [3, 1, 4, 2],
            "type_text": ["Jump Shot", "Jump Shot", "Defensive Rebound", "Defensive Rebound"],
            "event_type": ["shot", "shot", "rebound", "rebound"],
            "scoring_play": [False] * 4,
        }
    )
    out, _ = sort_and_repair(df)
    assert out["play_order"].tolist() == [1, 2, 3, 4]


def test_moving_substitutions_is_not_counted_as_a_repair():
    df = pd.DataFrame(
        {
            "game_id": [1] * 3,
            "period": [4] * 3,
            "secs_game": [60.0] * 3,
            "play_order": [0, 1, 2],
            "type_text": ["Free Throw - 1 of 2", "Substitution", "Free Throw - 2 of 2"],
            "event_type": ["free_throw", "other", "free_throw"],
            "scoring_play": [True, False, True],
        }
    )
    out, moved = sort_and_repair(df)
    assert out["type_text"].tolist() == ["Free Throw - 1 of 2", "Free Throw - 2 of 2", "Substitution"]
    assert moved == 0


def test_sort_repairs_ticks_inside_each_game_and_period_separately():
    rows = []
    for game in (1, 2):
        for period in (4, 5):
            rows += [(game, period, 60.0, "Free Throw - 1 of 2"), (game, period, 60.0, "Shooting Foul"), (game, period, 60.0, "Free Throw - 2 of 2")]
    df = pd.DataFrame(rows, columns=["game_id", "period", "secs_game", "type_text"])
    df["play_order"] = range(len(df))
    df["event_type"] = [classify_event(t, False, False) for t in df.type_text]
    df["scoring_play"] = False
    out, moved = sort_and_repair(df)
    assert out["type_text"].tolist() == ["Shooting Foul", "Free Throw - 1 of 2", "Free Throw - 2 of 2"] * 4
    assert moved == 8  # two rows move in each of the four ticks
