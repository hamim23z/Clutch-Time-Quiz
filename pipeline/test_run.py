import shutil
from pathlib import Path

import pandas as pd

import run

FIXTURES = Path(__file__).parent / "fixtures"


def fake_download(season, raw_dir):
    """Stands in for the network: drops the 2024 sample where the real file would go."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    dest = raw_dir / f"play_by_play_{season}.parquet"
    shutil.copy(FIXTURES / "raw_2024.parquet", dest)
    return dest


def test_one_command_run_writes_processed_files_and_deletes_downloaded_raw(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(run, "download_season", fake_download)
    raw_dir, out_dir = tmp_path / "raw", tmp_path / "processed"
    code = run.main(["--start", "2024", "--end", "2024", "--raw-dir", str(raw_dir), "--out-dir", str(out_dir)])
    assert code == 0
    assert not list(raw_dir.glob("*.parquet"))  # nothing large stays behind
    events = pd.read_parquet(out_dir / "events.parquet")
    games = pd.read_parquet(out_dir / "games.parquet")
    assert len(games) == 3 and events.game_id.nunique() == 3
    summary = pd.read_json(out_dir / "summary.json", typ="series")
    assert summary["total"]["events"] == len(events)
    assert summary["total"]["games"] == 3
    out = capsys.readouterr().out
    assert "2024: 3 games" in out and "uncertain possession" in out


def test_second_run_skips_finished_seasons_and_force_redoes_them(tmp_path, monkeypatch, capsys):
    calls = []

    def counting_download(season, raw_dir):
        calls.append(season)
        return fake_download(season, raw_dir)

    monkeypatch.setattr(run, "download_season", counting_download)
    args = ["--start", "2024", "--end", "2024", "--raw-dir", str(tmp_path / "raw"), "--out-dir", str(tmp_path / "out")]
    run.main(args)
    run.main(args)
    assert calls == [2024]
    assert "already processed" in capsys.readouterr().out
    run.main(args + ["--force"])
    assert calls == [2024, 2024]


def test_existing_raw_file_is_used_and_kept(tmp_path, monkeypatch):
    monkeypatch.setattr(run, "download_season", lambda *a: (_ for _ in ()).throw(AssertionError("should not download")))
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    shutil.copy(FIXTURES / "raw_2024.parquet", raw_dir / "play_by_play_2024.parquet")
    run.main(["--start", "2024", "--end", "2024", "--raw-dir", str(raw_dir), "--out-dir", str(tmp_path / "out")])
    assert (raw_dir / "play_by_play_2024.parquet").exists()  # we did not download it, so we don't delete it


def test_failed_season_is_reported_and_the_rest_still_run(tmp_path, monkeypatch, capsys):
    def flaky(season, raw_dir):
        if season == 2023:
            raise RuntimeError("could not download season 2023: no route")
        return fake_download(season, raw_dir)

    monkeypatch.setattr(run, "download_season", flaky)
    code = run.main(["--start", "2023", "--end", "2024", "--raw-dir", str(tmp_path / "raw"), "--out-dir", str(tmp_path / "out")])
    captured = capsys.readouterr()
    assert code == 1
    assert "failed seasons: [2023]" in captured.err
    assert "2024: 3 games" in captured.out
