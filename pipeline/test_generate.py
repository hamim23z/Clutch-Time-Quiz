"""The one command, run end to end on the small fixture (tables written to a temporary processed directory)."""
import json
from pathlib import Path

import pandas as pd
import pytest

import generate
import generator
import pools
import templates
from templates import PLAYER, Template, stat_in_game
from testtables import make_tables


@pytest.fixture
def small_templates():
    saved = list(templates.TEMPLATES)
    saved_families = list(pools.FAMILIES)
    pools.FAMILIES[:] = [f for f in saved_families if f.key == "finals-year"]  # one family, so the run stays small
    templates.TEMPLATES[:] = [
        Template("points-low", PLAYER, "scored {n} or more points in a regular-season game", (20, 30), stat_in_game("points", "regular"), "points"),
        Template("never", PLAYER, "scored {n} or more points in a regular-season game", (500,), stat_in_game("points", "regular"), "points"),
    ]
    yield
    templates.TEMPLATES[:] = saved
    pools.FAMILIES[:] = saved_families


def _write_processed(directory: Path) -> None:
    t = make_tables()
    directory.mkdir()
    for name in generate.TABLE_NAMES:
        getattr(t, name).to_parquet(directory / f"{name}.parquet", index=False)


def test_command_writes_candidates_fame_and_both_reports(tmp_path, small_templates, capsys):
    _write_processed(tmp_path / "processed")
    (tmp_path / "overrides.csv").write_text("athlete_id,tier,reason\n1,1,test override\n")
    code = generate.main(["--overrides", str(tmp_path / "overrides.csv"), "--processed-dir", str(tmp_path / "processed"), "--out-dir", str(tmp_path / "out"),
                          "--docs-dir", str(tmp_path / "docs")])
    assert code == 0
    prompts = json.loads((tmp_path / "out" / "candidates.json").read_text())
    generator.validate(prompts)
    ids = [p["id"] for p in prompts]
    assert ids[:2] == ["cand-points-low-20", "cand-points-low-30"]
    assert ids[2:] and all(i.startswith("cand-finals-year-") for i in ids[2:])  # the one family left in this run
    fame = pd.read_parquet(tmp_path / "out" / "fame.parquet")
    assert len(fame) == 40
    assert fame.set_index("player_id").loc[1, "override_reason"] == "test override"
    assert any(a["status"] == "too_few" and a["template"] == "never" for a in json.loads((tmp_path / "out" / "candidates_meta.json").read_text())["attempts"])
    assert "Fame" in (tmp_path / "docs" / "fame-report.md").read_text()
    report = (tmp_path / "docs" / "prompt-candidates.md").read_text()
    assert "points-low" in report and "finals-year" in report and "Candidates per family" in report
    out = capsys.readouterr().out
    assert "players per tier" in out and f"candidates: {len(ids)} ({len(ids)} player, 0 team)" in out
    assert "templates with no candidates: never" in out


def test_command_explains_a_missing_processed_directory(tmp_path):
    with pytest.raises(SystemExit) as e:
        generate.main(["--processed-dir", str(tmp_path / "nothing"), "--out-dir", str(tmp_path / "o"), "--docs-dir", str(tmp_path)])
    assert "run.py" in str(e.value)


REAL = Path(__file__).resolve().parent.parent / "data" / "processed"


@pytest.mark.skipif(not (REAL / "player_games.parquet").exists(), reason="data/processed is not built")
def test_real_data_counts_match_an_independent_pandas_query():
    """Cross-check on the real tables: 40+ point and 60+ win counts, using plain pandas rather than the templates."""
    tables = generate.load_tables(REAL)
    reg = tables.player_games[tables.player_games["season_type"] == "regular"]
    expected_players = reg.loc[reg["points"] >= 40, "player_id"].nunique()
    got = next(t for t in templates.TEMPLATES if t.key == "points-regular").qualify(tables, 40)
    assert len(got) == expected_players
    tg = tables.team_games[(tables.team_games["season_type"] == "regular") & tables.team_games["won"]]
    wins = tg.groupby(["team_id", "season"]).size()
    got = next(t for t in templates.TEMPLATES if t.key == "wins-season").qualify(tables, 60)
    assert len(got) == int((wins >= 60).sum())
