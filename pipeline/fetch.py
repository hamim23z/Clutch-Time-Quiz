"""Fetch stage: download one season of ESPN play-by-play from the sportsdataverse releases."""
from __future__ import annotations

import time
import urllib.error
import urllib.request
from pathlib import Path

URL = (
    "https://github.com/sportsdataverse/sportsdataverse-data/releases/download/"
    "espn_nba_pbp/play_by_play_{season}.parquet"
)
FIRST_SEASON, LAST_SEASON = 2002, 2026
BACKOFF_SECONDS = (2, 4, 8, 16)


def season_url(season: int) -> str:
    return URL.format(season=season)


def raw_path(raw_dir: Path, season: int) -> Path:
    return raw_dir / f"play_by_play_{season}.parquet"


def download_season(season: int, raw_dir: Path, backoff: tuple[int, ...] = BACKOFF_SECONDS) -> Path:
    """Download one season into raw_dir and return its path. Retries network errors with backoff."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    dest = raw_path(raw_dir, season)
    part = dest.with_suffix(".part")
    attempts = len(backoff) + 1
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(season_url(season), timeout=120) as resp, open(part, "wb") as f:
                while chunk := resp.read(1 << 20):
                    f.write(chunk)
            with open(part, "rb") as f:
                if f.read(4) != b"PAR1":
                    raise OSError("downloaded file is not a parquet file")
            part.replace(dest)
            return dest
        except (urllib.error.URLError, OSError) as err:
            part.unlink(missing_ok=True)
            if attempt == attempts - 1:
                raise RuntimeError(f"could not download season {season}: {err}") from err
            time.sleep(backoff[attempt])
    raise AssertionError("unreachable")
