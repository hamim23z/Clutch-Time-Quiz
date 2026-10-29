"""Checks on the two files the website reads: prompts.json and universe.json.

  - both validate against schema/*.schema.json;
  - every answer id is in the universe, with the same name and the right kind (pl- for players, tm- for teams);
  - every answer's points match its tier (1=10, 2=20, 3=35, 4=55, 5=75, 6=100);
  - ids are unique (prompts, answers within a prompt, universe entries) and no two entries share a name;
  - an alias is never the same text as another entry's name or alias, as the answer matcher would read it.
Each check raises ValueError with the first problems it finds.
"""
from __future__ import annotations

import json
from pathlib import Path

import jsonschema

from generator import PLAYER_ID_PREFIX, TEAM_ID_PREFIX, validate as validate_prompts
from matchnorm import base_name, normalize
from tiers import TIER_POINTS

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schema"
UNIVERSE_SCHEMA = SCHEMA_DIR / "universe.schema.json"
MAX_LISTED = 10


def _fail(problems: list[str]) -> None:
    if problems:
        shown = "; ".join(problems[:MAX_LISTED]) + (f"; and {len(problems) - MAX_LISTED} more" if len(problems) > MAX_LISTED else "")
        raise ValueError(shown)


def validate_universe(universe: dict, schema_path: Path = UNIVERSE_SCHEMA) -> None:
    """Schema, unique ids, no two entries with the same name, and no alias that points at two entries."""
    jsonschema.Draft202012Validator(json.loads(schema_path.read_text())).validate(universe)
    problems: list[str] = []
    entries = universe["players"] + universe["teams"]
    ids = [e["id"] for e in entries]
    problems += [f"duplicate id {i}" for i in sorted({i for i in ids if ids.count(i) > 1})]
    names = [e["name"] for e in entries]
    problems += [f"two entries are named {n!r}" for n in sorted({n for n in names if names.count(n) > 1})]
    problems += [f"{e['id']} has a player id prefix on a team or the reverse" for e in universe["players"] if not e["id"].startswith(PLAYER_ID_PREFIX)]
    problems += [f"{e['id']} is a team without the {TEAM_ID_PREFIX!r} prefix" for e in universe["teams"] if not e["id"].startswith(TEAM_ID_PREFIX)]
    claims_name: dict[str, set[str]] = {}
    claims_alias: dict[str, set[str]] = {}
    for e in entries:
        own = normalize(base_name(e["name"]), True)
        claims_name.setdefault(own, set()).add(e["id"])
        for alias in e["aliases"]:
            key = normalize(alias, True)
            if key == own:
                problems.append(f"{e['id']}: alias {alias!r} is the same as its own name")
            claims_alias.setdefault(key, set()).add(e["id"])
    # people with the same name share a base name on purpose; an alias must belong to exactly one entry and be nobody's name
    for key, aliased in claims_alias.items():
        claimers = aliased | claims_name.get(key, set())
        if len(claimers) > 1:
            problems.append(f"{key!r} is claimed by several entries: {sorted(claimers)[:4]}")
    _fail(problems)


def check_answers_in_universe(prompts: list[dict], universe: dict) -> None:
    """Every answer id exists in the universe with the same name, in the list that matches the prompt's answer type."""
    by_kind = {"player": {e["id"]: e["name"] for e in universe["players"]}, "team": {e["id"]: e["name"] for e in universe["teams"]}}
    problems = []
    for p in prompts:
        known = by_kind[p["answerType"]]
        for a in p["answers"]:
            if a["id"] not in known:
                problems.append(f"{p['id']}: answer {a['id']} ({a['name']}) is not in the universe")
            elif known[a["id"]] != a["name"]:
                problems.append(f"{p['id']}: answer {a['id']} is named {a['name']!r} but the universe says {known[a['id']]!r}")
    _fail(problems)


def check_tier_points(prompts: list[dict]) -> None:
    """Every answer's points match its tier."""
    problems = [
        f"{p['id']}: {a['id']} has tier {a['tier']} but {a['points']} points"
        for p in prompts for a in p["answers"] if TIER_POINTS.get(a["tier"]) != a["points"]
    ]
    _fail(problems)


def check_all(prompts: list[dict], universe: dict) -> None:
    validate_prompts(prompts)  # schema, unique prompt and answer ids, answer-count limits
    validate_universe(universe)
    check_answers_in_universe(prompts, universe)
    check_tier_points(prompts)
    texts = [p["text"] for p in prompts]
    _fail([f"two prompts have the text {t!r}" for t in sorted({t for t in texts if texts.count(t) > 1})])
