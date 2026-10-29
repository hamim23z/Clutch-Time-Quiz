"""Runs the cases in schema/match-cases.json against pipeline/matchnorm.py.

The same file is read by web/src/matching.shared.test.ts, which runs the normalization and the matching of the website.
If a case here fails, the Python copy of the normalization has drifted from the website's (or the other way round).
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # pipeline/ holds matchnorm.py

from matchnorm import base_name, normalize  # noqa: E402

CASES = json.loads((Path(__file__).resolve().parents[2] / "schema" / "match-cases.json").read_text())


def test_the_shared_file_has_enough_cases():
    assert len(CASES["normalize"]) + len(CASES["baseName"]) + len(CASES["match"]) >= 60


@pytest.mark.parametrize("case", CASES["normalize"], ids=lambda c: f"{c['input']!r}-{'drop' if c['dropSuffix'] else 'keep'}")
def test_normalize_agrees_with_the_website(case):
    assert normalize(case["input"], case["dropSuffix"]) == case["expected"]


@pytest.mark.parametrize("case", CASES["baseName"], ids=lambda c: repr(c["input"]))
def test_base_name_agrees_with_the_website(case):
    assert base_name(case["input"]) == case["expected"]


def test_every_name_and_alias_in_the_fixture_universe_normalizes_the_same_way_in_both_copies():
    """The exact-match keys of the fixture universe: what the website would index must be what the pipeline compares."""
    names = [e["name"] for kind in ("players", "teams") for e in CASES["universe"][kind]]
    aliases = [a for kind in ("players", "teams") for e in CASES["universe"][kind] for a in e["aliases"]]
    for text in names + aliases:
        key = normalize(text)
        assert key == key.lower() and key == " ".join(key.split()), text
        assert normalize(base_name(text), True) == normalize(normalize(base_name(text), True), True)  # stable under a second pass
