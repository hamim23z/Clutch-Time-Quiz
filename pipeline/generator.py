"""Prompt generator: turn template qualifiers into candidate prompts in the exact shape of the prompts schema.

For every template and threshold it finds the qualifiers, gives each a tier (players from the fame table, teams by
the current-name rule), applies the validity rules, and records what it dropped and why. The output is a list of
candidate prompts; choosing the final set is a later session's job.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import jsonschema
import pandas as pd

from templates import PLAYER, TEAM, TEMPLATES, Tables, Template
from tiers import DEEP_TIER, TIER_POINTS, historical_names_used, team_tiers

MIN_PLAYER_ANSWERS = 15
MAX_PLAYER_ANSWERS = 400
MIN_TEAM_ANSWERS = 5
MAX_TEAM_ANSWERS = None  # the brief sets no maximum for teams (there are only 30 franchises)

PLAYER_ID_PREFIX, TEAM_ID_PREFIX = "pl-", "tm-"
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schema" / "prompts.schema.json"


def season_label(season: int) -> str:
    """The data's season number is the year the season ends: 2002 is the 2001-02 season."""
    return f"{season - 1}-{str(season)[-2:]}"


def era_text(first_season: int, last_season: int) -> str:
    """The era every prompt starts with, exactly as long as the data runs: 'Since 2001-02 (through 2025-26)'.

    It begins with 'Since' and four digits so it passes the schema pattern. SPEC.md says 'Since 2002', which would
    read as calendar 2002 and leave out the games of October to December 2001.
    """
    return f"Since {season_label(first_season)} (through {season_label(last_season)})"


def player_answer_id(player_id: int) -> str:
    return f"{PLAYER_ID_PREFIX}{int(player_id)}"


def team_answer_id(team_id: int) -> str:
    return f"{TEAM_ID_PREFIX}{int(team_id)}"


def difficulty(answer_type: str, tiers: list[int]) -> str:
    """easy, medium or hard from how many valid answers there are and how many are deep cuts (tier 4 or above).

    A short list is harder, and so is a list with many deep cuts. Each gets 0 to 2 points of hardness:
      size  - players: 100 or more answers = 0, 40 to 99 = 1, fewer than 40 = 2;
              teams: 25 or more = 0, 12 to 24 = 1, fewer than 12 = 2
      depth - share of answers in tier 4 or above; players: under 3% = 0, 3 to 10% = 1, 10% or more = 2;
              teams: under 5% = 0, 5 to 15% = 1, 15% or more = 2
    Total 0 or 1 is easy, 2 is medium, 3 or 4 is hard. The cutoffs are set to the spread of the real candidate lists
    under the five-metric fame score (session 5): lists are mostly well-known players, so even 10% deep cuts is a high share.
    """
    n = len(tiers)
    deep = sum(1 for t in tiers if t >= DEEP_TIER) / n
    if answer_type == PLAYER:
        size = 0 if n >= 100 else 1 if n >= 40 else 2
        depth = 0 if deep < 0.03 else 1 if deep < 0.10 else 2
    else:
        size = 0 if n >= 25 else 1 if n >= 12 else 2
        depth = 0 if deep < 0.05 else 1 if deep < 0.15 else 2
    total = size + depth
    return "easy" if total <= 1 else "medium" if total == 2 else "hard"


def limits_for(answer_type: str) -> tuple[int, int | None]:
    return (MIN_PLAYER_ANSWERS, MAX_PLAYER_ANSWERS) if answer_type == PLAYER else (MIN_TEAM_ANSWERS, MAX_TEAM_ANSWERS)


def check_count(answer_type: str, count: int) -> str | None:
    """None if a prompt with this many valid answers is allowed, else 'too_few' or 'too_many'."""
    low, high = limits_for(answer_type)
    if count < low:
        return "too_few"
    if high is not None and count > high:
        return "too_many"
    return None


@dataclass
class GenerationResult:
    prompts: list[dict] = field(default_factory=list)
    meta: list[dict] = field(default_factory=list)  # one per prompt: template, threshold, tier counts, ...
    attempts: list[dict] = field(default_factory=list)  # one per template and threshold, kept or dropped
    era: str = ""


def _player_answers(qualifiers: pd.DataFrame, fame: pd.DataFrame) -> list[dict]:
    """Valid answers for a player prompt, most famous first (by fame rank, then career points, then name)."""
    rows = fame[fame["player_id"].isin(qualifiers["player_id"])]
    if len(rows) != len(qualifiers):
        raise ValueError("a qualifying player is missing from the fame table")
    rows = rows.sort_values(["tier", "fame_rank", "career_points", "name"], ascending=[True, True, False, True])
    return [
        {"id": player_answer_id(r.player_id), "name": r.name, "tier": int(r.tier), "points": int(r.points)}
        for r in rows.itertuples()
    ]


def _team_answers(qualifiers: pd.DataFrame, teams: pd.DataFrame) -> list[dict]:
    """Valid answers for a team prompt: the franchise (under its current name) with the current-name tier rule."""
    tiers = team_tiers(qualifiers, teams)
    names = teams.set_index("team_id")["current_name"]
    rows = sorted(tiers.items(), key=lambda kv: (kv[1], names[kv[0]]))
    return [
        {"id": team_answer_id(tid), "name": names[tid], "tier": tier, "points": TIER_POINTS[tier]}
        for tid, tier in rows
    ]


def generate(tables: Tables, fame: pd.DataFrame, templates: list[Template] | None = None) -> GenerationResult:
    """Candidate prompts for every template and threshold, plus a record of every attempt."""
    result = GenerationResult(era=era_text(int(tables.games["season"].min()), int(tables.games["season"].max())))
    for template in templates if templates is not None else TEMPLATES:
        for n in template.thresholds:
            qualifiers = template.qualify(tables, n)
            if template.answer_type == PLAYER:
                answers = _player_answers(qualifiers, fame) if len(qualifiers) else []
            else:
                answers = _team_answers(qualifiers, tables.teams) if len(qualifiers) else []
            attempt = {"template": template.key, "n": n, "answer_type": template.answer_type, "valid_answers": len(answers)}
            problem = check_count(template.answer_type, len(answers))
            attempt["status"] = problem or "kept"
            result.attempts.append(attempt)
            if problem:
                continue
            tiers = [a["tier"] for a in answers]
            has_n = "{n}" in template.wording
            prompt_id = f"cand-{template.key}" + (f"-{n}" if has_n else "")
            prompt = {
                "id": prompt_id,
                "answerType": template.answer_type,
                "text": template.text(result.era, n),
                "answers": answers,
                "difficulty": difficulty(template.answer_type, tiers),
            }
            result.prompts.append(prompt)
            meta = {
                "id": prompt_id, "template": template.key, "n": n if has_n else None, "valid_answers": len(answers),
                "tier_counts": {str(t): tiers.count(t) for t in range(1, 7)},
            }
            if template.answer_type == TEAM:
                meta["historical_only"] = [a["name"] for a in answers if a["tier"] > 1]
                meta["historical_names"] = {
                    team_answer_id(k): v for k, v in historical_names_used(qualifiers, tables.teams).items()
                }
            result.meta.append(meta)
    return result


def validate(prompts: list[dict], schema_path: Path = SCHEMA_PATH) -> None:
    """Raise if the prompts do not follow schema/prompts.schema.json, or break a rule the schema cannot express."""
    schema = json.loads(schema_path.read_text())
    jsonschema.Draft202012Validator(schema).validate(prompts)
    ids = [p["id"] for p in prompts]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate prompt ids")
    for p in prompts:
        answer_ids = [a["id"] for a in p["answers"]]
        if len(set(answer_ids)) != len(answer_ids):
            raise ValueError(f"{p['id']}: duplicate answer ids")
        problem = check_count(p["answerType"], len(p["answers"]))
        if problem:
            raise ValueError(f"{p['id']}: {problem}")


def write_candidates(result: GenerationResult, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    validate(result.prompts)
    (out_dir / "candidates.json").write_text(json.dumps(result.prompts, indent=1, ensure_ascii=False) + "\n")
    (out_dir / "candidates_meta.json").write_text(
        json.dumps({"era": result.era, "prompts": result.meta, "attempts": result.attempts}, indent=1, ensure_ascii=False) + "\n"
    )
