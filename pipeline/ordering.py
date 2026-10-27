"""Ordering stage: put events in a stable order and repair same-timestamp mistakes.

The raw clock is whole seconds (tenths near 0 are lost), so many events share one timestamp
("tick") and the feed sometimes lists them in the wrong order. `game_play_number` is right
almost always (the clock never runs backwards inside a period), so we keep it as the base
order and only fix three known patterns, inside one tick:

1. Substitutions go last. They never change the score or possession, and they were often
   listed between the free throws of one trip.
2. A defensive foul listed after the *start* of a free throw trip that is still unfinished
   (for example free throw 1 of 2, then the shooting foul, then 2 of 2) moves in front of
   that trip's first free throw. Technical and offensive fouls are never moved.
3. A rebound with no outstanding miss before it, when a miss comes later in the same tick
   (rebound listed before the putback it belongs to), moves to just after that miss.
4. An offensive rebound listed right after a made shot, when a miss was waiting for its
   rebound before that shot (the made putback was listed before the rebound that set it up),
   moves in front of the made shot.

Everything else keeps its original relative order. See docs/possession.md.
"""
from __future__ import annotations

from typing import NamedTuple, Sequence

import numpy as np
import pandas as pd

from events import (
    FOUL,
    FREE_THROW,
    MADE_SHOT,
    REBOUND,
    SHOT,
    SUBSTITUTION,
    TURNOVER,
    foul_kind,
    parse_free_throw,
)


class TickEvent(NamedTuple):
    type_text: str
    event_type: str
    scoring: bool


def _is_miss(e: TickEvent) -> bool:
    return e.event_type == SHOT or (e.event_type == FREE_THROW and not e.scoring)


def reorder_tick(evs: Sequence[TickEvent], open_miss: bool) -> tuple[list[int], bool]:
    """Return the new order (indices into evs) of one tick, and whether a miss is still unrebounded.

    open_miss says whether a miss before this tick is still waiting for its rebound.
    """
    body = [i for i, e in enumerate(evs) if e.type_text != SUBSTITUTION]
    subs = [i for i, e in enumerate(evs) if e.type_text == SUBSTITUTION]
    out: list[int] = []
    held: list[int] = []  # rebounds waiting for the miss that comes later in this tick
    trip_start: int | None = None  # position in `out` of the first free throw of an unfinished trip
    putback_at: int | None = None  # position in `out` of a made shot that followed an unrebounded miss

    for pos, i in enumerate(body):
        e = evs[i]
        if e.event_type == REBOUND and not open_miss and any(_is_miss(evs[j]) for j in body[pos + 1 :]):
            held.append(i)
            continue
        if e.event_type == FOUL and trip_start is not None and foul_kind(e.type_text) == "defensive":
            out.insert(trip_start, i)
            trip_start += 1
            continue
        if e.event_type == REBOUND and putback_at == len(out) - 1 and "Offensive" in e.type_text:
            out.insert(putback_at, i)  # rebound first, then the made putback
            putback_at = None
            open_miss = False
            continue
        putback_at = len(out) if e.event_type == MADE_SHOT and open_miss else None
        out.append(i)
        if e.event_type == FREE_THROW:
            ft = parse_free_throw(e.type_text)
            if ft is not None:
                if ft.number < ft.total and trip_start is None:
                    trip_start = len(out) - 1
                elif ft.number == ft.total:
                    trip_start = None
        if _is_miss(e):
            open_miss = True
            if held:
                out.extend(held)
                held = []
                open_miss = False
        elif e.event_type in (REBOUND, MADE_SHOT, TURNOVER) or (e.event_type == FREE_THROW and e.scoring):
            open_miss = False

    out.extend(held)
    out.extend(subs)
    return out, open_miss


def sort_and_repair(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Stable-sort by game, period and clock (play_order breaks ties), then repair each tick.

    Needs columns game_id, period, secs_game, play_order, type_text, event_type, scoring_play.
    Returns the reordered frame (fresh index) and how many rows the repairs moved. Substitutions
    are not counted: they always go last, which shifts the rows around them without changing
    their order.
    """
    df = df.sort_values(
        ["game_id", "period", "secs_game", "play_order"],
        ascending=[True, True, False, True],
        kind="stable",
    ).reset_index(drop=True)
    game = df["game_id"].to_numpy()
    period = df["period"].to_numpy()
    secs = df["secs_game"].to_numpy()
    types = df["type_text"].tolist()
    kinds = df["event_type"].tolist()
    scoring = df["scoring_play"].tolist()

    order = np.arange(len(df))
    n = len(df)
    start = 0
    moved = 0
    open_miss = True
    while start < n:
        end = start + 1
        while end < n and game[end] == game[start] and period[end] == period[start] and secs[end] == secs[start]:
            end += 1
        if start > 0 and (game[start] != game[start - 1] or period[start] != period[start - 1]):
            open_miss = True  # new period: don't move rebounds on the strength of earlier context
        if end - start > 1:
            tick = [TickEvent(types[k], kinds[k], scoring[k]) for k in range(start, end)]
            perm, open_miss = reorder_tick(tick, open_miss)
            order[start:end] = [start + p for p in perm]
            kept = [p for p in perm if tick[p].type_text != SUBSTITUTION]
            moved += sum(a != b for a, b in zip(kept, sorted(kept)))
        else:
            e = TickEvent(types[start], kinds[start], scoring[start])
            _, open_miss = reorder_tick([e], open_miss)
        start = end

    return df.iloc[order].reset_index(drop=True), moved
