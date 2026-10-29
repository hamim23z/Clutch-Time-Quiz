"""The export command: unit tests for its helpers, and an end-to-end run on the real tables when they are present."""
import json
from pathlib import Path

import pandas as pd
import pytest

import export
from exportcheck import check_all
from generator import validate
from players import ALIAS_COLUMNS, load_aliases
from universe import load_team_aliases

ROOT = Path(__file__).resolve().parent.parent
REAL = ROOT / "data" / "processed"
needs_data = pytest.mark.skipif(not (REAL / "player_games.parquet").exists(), reason="data/processed is not built")


def test_prompt_ids_are_stable_and_readable():
    assert export.prompt_id("cand-points-regular-50") == "p-points-regular-50"
    assert export.prompt_id("cand-champion") == "p-champion"


def test_json_is_one_compact_item_per_line():
    text = export.dump_lines([{"a": 1, "b": "é"}, {"a": 2, "b": "x"}])
    assert text == '[\n{"a":1,"b":"é"},\n{"a":2,"b":"x"}\n]'
    assert json.loads(text) == [{"a": 1, "b": "é"}, {"a": 2, "b": "x"}]


def test_universe_json_round_trips():
    universe = {"players": [{"id": "pl-1", "name": "A", "aliases": []}], "teams": [{"id": "tm-1", "name": "T", "aliases": ["t"]}]}
    assert json.loads(export.render_universe(universe)) == universe


def test_outside_range_names_must_not_be_in_the_universe():
    universe = {"players": [{"id": "pl-1", "name": "Michael Jordan", "aliases": ["MJ"]}, {"id": "pl-2", "name": "Gary Payton II", "aliases": []}],
                "teams": [{"id": "tm-1", "name": "Boston Celtics", "aliases": ["Celtics"]}]}
    export.check_outside_range(["Larry Bird", "Magic Johnson"], universe)
    for bad in (["Michael Jordan"], ["michael jordan"], ["MJ"], ["Gary Payton"], ["Larry Bird", "Larry Bird"], ["Celtics"]):
        with pytest.raises(ValueError):
            export.check_outside_range(bad, universe)


def test_the_shipped_alias_file_points_only_at_real_athletes():
    df = load_aliases(ROOT / "pipeline" / "data" / "aliases.csv")
    assert list(df.columns) == ALIAS_COLUMNS
    assert not df["alias"].str.lower().duplicated().any()
    assert df["evidence"].str.len().gt(20).all()
    assert load_team_aliases()["evidence"].notna().all()


def test_the_outside_range_file_is_about_150_distinct_names():
    names = pd.read_csv(export.OUTSIDE_RANGE_PATH)["name"].tolist()
    assert 140 <= len(names) <= 170
    assert len({n.lower() for n in names}) == len(names)
    assert all(len(n.split()) >= 2 for n in names)


def family_of(prompt_id: str) -> str:
    """p-<family>[-<parameters>] back to the family key (longest key first, on a dash boundary)."""
    from pools import FAMILIES
    from templates import TEMPLATES
    keys = sorted([t.key for t in TEMPLATES] + [f.key for f in FAMILIES], key=len, reverse=True)
    body = prompt_id[2:]
    return next(k for k in keys if body == k or body.startswith(k + "-"))


def check_export_rules(prompts: list[dict], universe: dict) -> None:
    from pools import FAMILIES
    broad = {f.key for f in FAMILIES if f.broad}
    assert len(prompts) >= 504 and len(prompts) % 7 == 0
    assert len({p["id"] for p in prompts}) == len(prompts)
    assert len({p["text"] for p in prompts}) == len(prompts)
    check_all(prompts, universe)  # schemas, answer ids in the universe, points against tiers
    for d in range(len(prompts) // 7):
        dive = prompts[7 * d:7 * d + 7]
        kinds = [p["answerType"] for p in dive]
        assert kinds == ["player", "player", "team", "player", "team", "player", "player"], f"dive {d + 1}"
        assert 4 <= kinds.count("player") <= 6 and 1 <= kinds.count("team") <= 3
        families = [family_of(p["id"]) for p in dive]
        assert len(set(families)) == 7, f"dive {d + 1} repeats a template family"
        assert sum(1 for p, f in zip(dive, families) if p["answerType"] == "player" and f in broad) >= 2, f"dive {d + 1}"
        assert {p["difficulty"] for p in dive} == {"easy", "medium", "hard"}, f"dive {d + 1}"
    assert all(p["text"].startswith("Since 2001-02 (through 2025-26), name a ") for p in prompts)
    counts = {}
    for p in prompts:
        counts[family_of(p["id"])] = counts.get(family_of(p["id"]), 0) + 1
    assert max(counts.values()) <= 40  # no family dominates
    answers = [a for p in prompts for a in p["answers"]]
    low = sum(1 for a in answers if a["tier"] <= 2) / len(answers)
    deep = sum(1 for a in answers if a["tier"] >= 5) / len(answers)
    assert low <= 0.45 and deep >= 0.12, (low, deep)  # the rarity targets


@needs_data
def test_end_to_end_on_the_real_tables(tmp_path):
    code = export.main(["--processed-dir", str(REAL), "--out-dir", str(tmp_path / "gen"), "--export-dir", str(tmp_path / "export"),
                        "--docs-dir", str(tmp_path / "docs"), "--check-count", "5", "--per-family", "0"])
    assert code == 0
    prompts = json.loads((tmp_path / "export" / "prompts.json").read_text())
    universe = json.loads((tmp_path / "export" / "universe.json").read_text())
    check_export_rules(prompts, universe)
    for name in ("prompts-sample.md", "curation-report.md", "rarity-report.md"):
        assert (tmp_path / "docs" / name).exists()
    # people who share a display name stay separate entries, told apart by the seasons in their name
    names = [e["name"] for e in universe["players"]]
    assert "Mike James (2002-2014)" in names and "Mike James (2018-2021)" in names and "Mike James" not in names
    # the committed export is the one this code produces
    committed = ROOT / "data" / "export"
    for name in ("prompts.json", "universe.json"):
        assert (committed / name).read_text() == (tmp_path / "export" / name).read_text(), f"data/export/{name} is out of date: run python3 pipeline/export.py"


@needs_data
def test_committed_export_files_follow_every_rule_on_their_own():
    prompts = json.loads((ROOT / "data" / "export" / "prompts.json").read_text())
    universe = json.loads((ROOT / "data" / "export" / "universe.json").read_text())
    check_export_rules(prompts, universe)
    size = (ROOT / "data" / "export" / "prompts.json").stat().st_size + (ROOT / "data" / "export" / "universe.json").stat().st_size
    assert size < 5_000_000
