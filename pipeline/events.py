"""Event vocabulary: classify a raw play into one of a few types, and read details from it."""
from __future__ import annotations

import re
from typing import NamedTuple

SHOT = "shot"  # missed field goal attempt
MADE_SHOT = "made_shot"
FREE_THROW = "free_throw"
FOUL = "foul"
TIMEOUT = "timeout"
REBOUND = "rebound"
TURNOVER = "turnover"
OTHER = "other"

SUBSTITUTION = "Substitution"
END_PERIOD_TYPES = frozenset({"End Period", "End Game"})
TIMEOUT_TYPES = frozenset({"Full Timeout", "Short Timeout"})  # never the *_timeout_called flags
# Turnovers whose type_text does not contain the word "Turnover".
TURNOVER_TYPES = frozenset({"Traveling"})

_FT_RE = re.compile(r"^Free Throw - (?:(Flagrant|Clear Path) )?(\d) of (\d)$")
_THREE_TEXT_RE = re.compile(r"three[ -]?point", re.IGNORECASE)
_DISTANCE_RE = re.compile(r"(\d+)[ -]?(?:foot|ft)\b", re.IGNORECASE)
# The longest two-point shot is a 23 ft 9 in arc, so a stated distance of 24 ft or more is a three.
MIN_THREE_FEET = 24


def classify_event(type_text: str, shooting_play: bool, scoring_play: bool) -> str:
    if type_text.startswith("Free Throw"):
        return FREE_THROW
    if shooting_play:
        return MADE_SHOT if scoring_play else SHOT
    if type_text in TIMEOUT_TYPES:
        return TIMEOUT
    if "Rebound" in type_text:
        return REBOUND
    if type_text == "No Turnover":
        return OTHER
    if "Turnover" in type_text or type_text in TURNOVER_TYPES:
        return TURNOVER
    if "Foul" in type_text or "Technical" in type_text or type_text == "Offensive Charge":
        return FOUL
    return OTHER


def is_three_attempt(text: str, event_type: str) -> bool:
    """True for a field goal attempt that was a three.

    Primary rule: the play text says "three point" (also "three pointer").
    Fallback: the text gives a distance of 24 ft or more. About 1 in 8 recent threes
    (for example "26-foot step back jumpshot") never say "three point", so the primary
    rule alone undercounts them. See docs/possession.md.
    """
    if event_type not in (SHOT, MADE_SHOT):
        return False
    if _THREE_TEXT_RE.search(text):
        return True
    m = _DISTANCE_RE.search(text)
    return m is not None and int(m.group(1)) >= MIN_THREE_FEET


class FreeThrow(NamedTuple):
    kind: str  # "regular", "flagrant" or "clear_path"
    number: int
    total: int


def parse_free_throw(type_text: str) -> FreeThrow | None:
    """Parse "Free Throw - 1 of 2". Technical free throws return None (no trip)."""
    m = _FT_RE.match(type_text)
    if m is None:
        return None
    kind = {"Flagrant": "flagrant", "Clear Path": "clear_path"}.get(m.group(1), "regular")
    return FreeThrow(kind, int(m.group(2)), int(m.group(3)))


def foul_kind(type_text: str) -> str:
    """"technical", "double", "offensive" or "defensive" (everything else)."""
    if "Technical" in type_text:
        return "technical"
    if type_text == "Double Personal Foul":
        return "double"
    if type_text in ("Offensive Foul", "Offensive Charge"):
        return "offensive"
    return "defensive"
