"""Possession stage: infer which team has the ball after each event.

There is no possession column in the data. We walk each period in order and update a small
state: (team, status). The rules are written out in docs/possession.md; the short version:
made shot / turnover / offensive foul flip it, a defensive foul gives it to the fouled team,
a rebound gives it to the rebounder, a miss leaves it "loose" until the rebound.

Statuses:
  certain  a rule set the team (or carried a certain team through an event that cannot change it)
  loose    live ball after a miss: the team is the shooter's, until the rebound says otherwise
  unknown  no team (start of a period before any deciding event, or a missing team_id)
"""
from __future__ import annotations

import pandas as pd

from events import (
    FOUL,
    FREE_THROW,
    MADE_SHOT,
    REBOUND,
    SHOT,
    TURNOVER,
    foul_kind,
    parse_free_throw,
)

HOME, AWAY = "home", "away"
CERTAIN, LOOSE, UNKNOWN = "certain", "loose", "unknown"

State = tuple[str | None, str]
NO_STATE: State = (None, UNKNOWN)


def other(side: str) -> str:
    return AWAY if side == HOME else HOME


def _team(side: str | None, status: str = CERTAIN) -> State:
    return (side, status) if side is not None else NO_STATE


def next_state(
    prev: State,
    event_type: str,
    type_text: str,
    side: str | None,
    scoring: bool,
    scorer: str | None,
) -> State:
    """State after one event.

    side is the acting team (team_id): the shooter, rebounder, turnover committer, or for
    fouls the team that fouled. scorer is the team whose score went up on this event.
    """
    prev_team = prev[0]

    if type_text in ("Jumpball", "Jump Ball"):
        return _team(side)  # team_id is the team that gained possession
    if type_text == "Kicked Ball":
        return _team(other(side)) if side else prev  # a kick by the defense: offense keeps it
    if type_text == "Defensive Goaltending" and scorer:
        return _team(other(scorer))  # basket is awarded, then the defense inbounds

    if event_type == FREE_THROW:
        ft = parse_free_throw(type_text)
        shooter = side or (scorer if scoring else prev_team)
        if ft is None or shooter is None:
            return prev if ft is None else NO_STATE  # technical free throw: ball stays where it was
        if ft.number < ft.total:
            return _team(shooter)
        if ft.kind != "regular":  # flagrant / clear path: the shooting team keeps the ball
            return _team(shooter) if scoring else _team(shooter, LOOSE)
        return _team(other(shooter)) if scoring else _team(shooter, LOOSE)

    if event_type == MADE_SHOT:
        shooter = side or scorer
        return _team(other(shooter)) if shooter else NO_STATE

    if event_type == SHOT:
        shooter = side or prev_team
        return _team(shooter, LOOSE)

    if event_type == REBOUND:
        if side:
            return _team(side)
        if prev_team is None:
            return NO_STATE
        if type_text == "Offensive Rebound":
            return _team(prev_team)
        if type_text == "Defensive Rebound":
            return _team(other(prev_team))
        return NO_STATE

    if event_type == TURNOVER:
        return _team(other(side)) if side else NO_STATE

    if event_type == FOUL:
        kind = foul_kind(type_text)
        if kind in ("technical", "double"):
            return prev
        return _team(other(side)) if side else NO_STATE  # fouled team gets the ball

    return prev  # substitutions, timeouts, reviews, violations: the ball does not change hands


def infer_possession(df: pd.DataFrame) -> tuple[list[str | None], list[str]]:
    """Possession team and status after every row.

    Rows must be in play order. Needs columns game_id, period, event_type, type_text,
    side (acting team: "home", "away" or None), scoring_play, home_score, away_score.
    State resets at the start of every (game, period).
    """
    teams: list[str | None] = []
    statuses: list[str] = []
    state = NO_STATE
    key = None
    prev_home = prev_away = None
    cols = zip(
        df["game_id"].tolist(),
        df["period"].tolist(),
        df["event_type"].tolist(),
        df["type_text"].tolist(),
        df["side"].tolist(),
        df["scoring_play"].tolist(),
        df["home_score"].tolist(),
        df["away_score"].tolist(),
    )
    for game, period, event_type, type_text, side, scoring, home, away in cols:
        if (game, period) != key:
            key = (game, period)
            state = NO_STATE
            prev_home, prev_away = home, away
        scorer = None
        if home > prev_home:
            scorer = HOME
        elif away > prev_away:
            scorer = AWAY
        prev_home, prev_away = home, away
        state = next_state(state, event_type, type_text, side if side in (HOME, AWAY) else None, scoring, scorer)
        teams.append(state[0])
        statuses.append(state[1])
    return teams, statuses
