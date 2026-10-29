"""The website's name normalization (web/src/matching.ts `normalize`), in Python, so the pipeline can check for
collisions between names and aliases the way the answer matcher will see them."""
from __future__ import annotations

import re
import unicodedata

SUFFIXES = {"jr", "sr", "ii", "iii", "iv", "v"}


def normalize(text: str, drop_suffix: bool = False) -> str:
    """Lowercase, strip accents and punctuation (apostrophes and periods vanish, other marks become spaces), join runs
    of single letters ("J. J." -> "jj"), and optionally drop a trailing suffix (Jr., III)."""
    folded = "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.category(c).startswith("M")).lower()
    folded = re.sub(r"[‘’'`]", "", folded).replace(".", "")
    folded = re.sub(r"[^a-z0-9]+", " ", folded).strip()
    tokens = folded.split(" ") if folded else []
    joined: list[str] = []
    previous_was_letter = False
    for token in tokens:
        if len(token) == 1 and previous_was_letter and joined:
            joined[-1] += token
        else:
            joined.append(token)
        previous_was_letter = len(token) == 1
    while drop_suffix and len(joined) > 1 and joined[-1] in SUFFIXES:
        joined.pop()
    return " ".join(joined)


def base_name(name: str) -> str:
    """'Mike James (2002-2014)' -> 'Mike James': drop the disambiguator the pipeline adds for shared names."""
    return re.sub(r"\s*\([^)]*\)\s*$", "", name).strip()
