from pathlib import Path

import pandas as pd

import run
from assemble import TABLES
from testdata import officials_box, player_box, schedule, team_box


def write_season(raw_dir: Path, season: int) -> dict[str, Path]:
    """A tiny season: 2 regular games, 1 playoff game, 1 All-Star game, 1 game with no player rows."""
    b = season * 100
    sched = schedule(
        {"game_id": b + 1, "season": season, "game_date": f"{season - 1}-11-01"},
        {"game_id": b + 2, "season": season, "game_date": f"{season - 1}-11-02", "status_period": 5},
        {"game_id": b + 3, "season": season, "season_type": 3, "type_abbreviation": "RD16", "game_date": f"{season}-04-20"},
        {"game_id": b + 4, "season": season, "type_abbreviation": "ALLSTAR", "home_id": 31, "away_id": 32, "game_date": f"{season}-02-15"},
        {"game_id": b + 5, "season": season, "game_date": f"{season - 1}-11-03"},
    )
    team = pd.concat(
        [team_box(b + i, season=season) for i in (1, 2, 3, 5)] + [team_box(b + 4, season=season, home=31, away=32, home_name="East All-Stars", away_name="West All-Stars")],
        ignore_index=True,
    )
    player = player_box(
        *[{"game_id": b + i, "season": season, "athlete_id": a, "athlete_display_name": n, "athlete_short_name": n, "points": 10.0}
          for i in (1, 2, 3) for a, n in ((1, "Alpha One"), (2, "Beta Two"))],
        {"game_id": b + 1, "season": season, "athlete_id": 3, "athlete_display_name": "Gamma Three", "points": None},  # did not play
    )
    officials = officials_box(*[(b + i, season, k, f"Ref {k}") for i in (1, 2, 3) for k in (1, 2, 3)])
    files = {"schedule": sched, "team": team, "player": player, "officials": officials}
    paths = run.season_paths(raw_dir, season)
    for table, df in files.items():
        df.to_parquet(paths[table], index=False)
    return paths


def fake_download(season, raw_dir):
    raw_dir.mkdir(parents=True, exist_ok=True)
    return write_season(raw_dir, season)


def args(tmp_path, *extra):
    aliases = tmp_path / "aliases.csv"
    aliases.write_text("alias,athlete_id,canonical_name,kind,evidence\n")
    return ["--start", "2023", "--end", "2024", "--raw-dir", str(tmp_path / "raw"), "--out-dir", str(tmp_path / "out"),
            "--aliases", str(aliases), "--notes", str(tmp_path / "notes.md"), *extra]


def test_one_command_produces_all_six_tables_and_the_notes(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(run, "download_season", fake_download)
    assert run.main(args(tmp_path)) == 0
    out = tmp_path / "out"
    rows = {name: len(pd.read_parquet(out / f"{name}.parquet")) for name in TABLES}
    assert set(rows) == {"players", "teams", "games", "player_games", "team_games", "officials"}
    assert rows == {"players": 2, "teams": 2, "games": 6, "player_games": 12, "team_games": 12, "officials": 18}
    games = pd.read_parquet(out / "games.parquet")
    assert sorted(games["season_type"].unique()) == ["playoffs", "regular"]
    assert not games["game_id"].isin([202304, 202404]).any()  # the All-Star games are gone
    assert "games skipped: 2" in capsys.readouterr().out

    notes = (tmp_path / "notes.md").read_text()
    for heading in ("## Run summary", "## Game selection", "### Skipped games: 2", "## Players", "## Teams", "## Officials"):
        assert heading in notes
    assert "202305" in notes and "202405" in notes  # the skipped game ids are logged
    assert "All-Star game | 2" in notes


def test_raw_files_this_run_downloaded_are_deleted_but_existing_ones_are_kept(tmp_path, monkeypatch):
    monkeypatch.setattr(run, "download_season", fake_download)
    raw = tmp_path / "raw"
    raw.mkdir()
    write_season(raw, 2023)  # already there: must survive
    assert run.main(args(tmp_path)) == 0
    assert len(list(raw.glob("*_2023.parquet"))) == 4
    assert not list(raw.glob("*_2024.parquet"))


def test_a_second_run_loads_finished_seasons_and_force_redoes_them(tmp_path, monkeypatch, capsys):
    calls = []

    def counting(season, raw_dir):
        calls.append(season)
        return fake_download(season, raw_dir)

    monkeypatch.setattr(run, "download_season", counting)
    run.main(args(tmp_path))
    run.main(args(tmp_path))
    assert calls == [2023, 2024]
    assert "already processed" in capsys.readouterr().out
    run.main(args(tmp_path, "--force"))
    assert calls == [2023, 2024, 2023, 2024]


def test_a_failed_season_is_reported_and_the_others_still_build(tmp_path, monkeypatch, capsys):
    def flaky(season, raw_dir):
        if season == 2023:
            raise RuntimeError("could not download")
        return fake_download(season, raw_dir)

    monkeypatch.setattr(run, "download_season", flaky)
    assert run.main(args(tmp_path)) == 1
    err = capsys.readouterr().err
    assert "2023: FAILED" in err and "failed seasons: [2023]" in err
    assert len(pd.read_parquet(tmp_path / "out" / "games.parquet")) == 3
