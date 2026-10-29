"""Small text helpers shared by the player and official stages."""
from __future__ import annotations

import unicodedata


def clean_spaces(text: str) -> str:
    """Collapse runs of whitespace (including stray CR/LF) and trim. 'Nene ' -> 'Nene'."""
    return " ".join(text.split())


def has_non_ascii(text: str) -> bool:
    return any(ord(c) > 127 for c in text)


def fold_ascii(text: str) -> str:
    """Strip accents: 'Nenê' -> 'Nene', 'Schröder' -> 'Schroder'."""
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c))


def name_key(text: str) -> str:
    """Case-insensitive key for comparing display names after whitespace cleaning."""
    return clean_spaces(text).casefold()
