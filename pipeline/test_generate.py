"""The one command, run end to end on the small fixture (tables written to a temporary processed directory)."""
import json
from pathlib import Path

import pandas as pd
import pytest

import generate
import generator
import templates
from templates import PLAYER, Template, stat_in_game
from testtables import make_tables


@pytest.fixture
def small_templates():
    saved = list(templates.TEMPLATES)
    templates.TEMPLATES[:] = [
        Template("points-low", PLAYER, "scored {n} or more points in a regular-season game", (20, 30), stat_in_game("points", "regular"), "points"),
        Template("never", PLAYER, "scored {n} or more points in a regular-season game", (500,), stat_in_game("points", "regular"), "points"),
    ]
    yield
    templates.TEMPLATES[:] = saved


def _write_processed(directory: Path) -> None:
    t = make_tables()
    directory.mkdir()
    for name in generate.TABLE_NAMES:
        getattr(t, name).to_parquet(directory / f"{name}.parquet", index=False)


def test_command_writes_candidates_fame_and_both_reports(tmp_path, small_templates, capsys):
    _write_processed(tmp_path / "processed")
    code = generate.main(["--processed-dir", str(tmp_path / "processed"), "--out-dir", str(tmp_path / "out"),
                          "--docs-dir", str(tmp_path / "docs")])
    assert code == 0
    prompts = json.loads((tmp_path / "out" / "candidates.json").read_text())
    generator.validate(prompts)
    assert [p["id"] for p in prompts] == ["cand-points-low-20", "cand-points-low-30"]
    assert len(pd.read_parquet(tmp_path / "out" / "fame.parquet")) == 40
    assert json.loads((tmp_path / "out" / "candidates_meta.json").read_text())["attempts"][-1]["status"] == "too_few"
    assert "Fame" in (tmp_path / "docs" / "fame-report.md").read_text()
    assert "points-low" in (tmp_path / "docs" / "prompt-candidates.md").read_text()
    out = capsys.readouterr().out
    assert "players per tier" in out and "candidates: 2 (2 player, 0 team)" in out
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
