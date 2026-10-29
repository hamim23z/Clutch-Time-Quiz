"""Fetch stage: download one season of the four box score files from the sportsdataverse releases."""
from __future__ import annotations

import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = "https://github.com/sportsdataverse/sportsdataverse-data/releases/download"
FIRST_SEASON, LAST_SEASON = 2002, 2026  # 2027 is the season in progress and is left out on purpose
BACKOFF_SECONDS = (2, 4, 8, 16)

# table -> (release tag, file prefix)
SOURCES: dict[str, tuple[str, str]] = {
    "schedule": ("espn_nba_schedules", "nba_schedule"),
    "team": ("espn_nba_team_boxscores", "team_box"),
    "player": ("espn_nba_player_boxscores", "player_box"),
    "officials": ("espn_nba_officials", "officials"),
}


def file_name(table: str, season: int) -> str:
    return f"{SOURCES[table][1]}_{season}.parquet"


def season_url(table: str, season: int) -> str:
    return f"{BASE}/{SOURCES[table][0]}/{file_name(table, season)}"


def season_paths(raw_dir: Path, season: int) -> dict[str, Path]:
    return {table: raw_dir / file_name(table, season) for table in SOURCES}


def _download(url: str, dest: Path, backoff: tuple[int, ...]) -> None:
    part = dest.with_suffix(".part")
    for attempt in range(len(backoff) + 1):
        try:
            with urllib.request.urlopen(url, timeout=120) as resp, open(part, "wb") as f:
                while chunk := resp.read(1 << 20):
                    f.write(chunk)
            with open(part, "rb") as f:
                if f.read(4) != b"PAR1":
                    raise OSError("downloaded file is not a parquet file")
            part.replace(dest)
            return
        except (urllib.error.URLError, OSError) as err:
            part.unlink(missing_ok=True)
            if attempt == len(backoff):
                raise RuntimeError(f"could not download {url}: {err}") from err
            time.sleep(backoff[attempt])


def download_season(season: int, raw_dir: Path, backoff: tuple[int, ...] = BACKOFF_SECONDS) -> dict[str, Path]:
    """Make sure all four files of a season are in raw_dir. Existing files are left alone."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    paths = season_paths(raw_dir, season)
    for table, path in paths.items():
        if not path.exists():
            _download(season_url(table, season), path, backoff)
    return paths
