"""Spike: which games have referee data, and what does it look like?

Referees are not in the box score releases. They live in the raw per-game ESPN JSON that
sportsdataverse mirrors on GitHub (the schedule's game_json_url column points at it):

    https://raw.githubusercontent.com/sportsdataverse/hoopR-nba-raw/main/nba/json/final/<game_id>.json

Each file is about 700 KB, but `gameInfo.officials` sits within the last ~25 KB, so this script
fetches only the tail of each file with an HTTP Range request (about 32 KB per game).

Usage (from the repo root):
    python3 pipeline/spike/referee_census.py <schedule_dir> <out.parquet> [first_season] [last_season]

<schedule_dir> holds nba_schedule_<year>.parquet files. Output has one row per game with the
number of officials, their names and the outcome ("ok", "no_officials" or "unknown").
"""
from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd

URL = "https://raw.githubusercontent.com/sportsdataverse/hoopR-nba-raw/main/nba/json/final/{game_id}.json"
TAIL_BYTES = (32_768, 262_144)  # try a small tail first, then a bigger one
WORKERS = 12


def fetch_tail(game_id: int, nbytes: int) -> str:
    req = urllib.request.Request(URL.format(game_id=game_id), headers={"Range": f"bytes=-{nbytes}"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as err:
            if err.code == 404:
                return ""
            time.sleep(2 * (attempt + 1))
        except (urllib.error.URLError, TimeoutError, OSError):
            time.sleep(2 * (attempt + 1))
    return ""


def parse_officials(text: str) -> tuple[str, list[dict]]:
    """Return (status, officials). "unknown" means the tail did not reach gameInfo."""
    i = text.find('"officials"')
    if i >= 0:
        start = text.find("[", i)
        try:
            officials, _ = json.JSONDecoder().raw_decode(text[start:])
            return "ok", officials
        except ValueError:
            return "unknown", []
    # gameInfo holds venue, attendance and (when present) officials, and comes before teamInfo
    if '"attendance"' in text or '"gameInfo"' in text:
        return "no_officials", []
    return "unknown", []


def census_one(game_id: int) -> dict:
    status, officials = "unknown", []
    for nbytes in TAIL_BYTES:
        text = fetch_tail(game_id, nbytes)
        if not text:
            continue
        status, officials = parse_officials(text)
        if status != "unknown":
            break
    return {
        "game_id": game_id,
        "status": status,
        "n_officials": len(officials),
        "officials": "|".join(str(o.get("fullName", "")) for o in officials),
        "positions": "|".join(str((o.get("position") or {}).get("displayName", "")) for o in officials),
    }


def main() -> None:
    sched_dir, out = Path(sys.argv[1]), Path(sys.argv[2])
    first = int(sys.argv[3]) if len(sys.argv) > 3 else 2002
    last = int(sys.argv[4]) if len(sys.argv) > 4 else 2026
    sched = pd.concat(
        [pd.read_parquet(sched_dir / f"nba_schedule_{y}.parquet") for y in range(first, last + 1)],
        ignore_index=True,
    )
    sched = sched[(sched["status_type_name"] == "STATUS_FINAL") & sched["game_json"]]
    # playoffs first, so a partial run still answers the playoff question
    sched = sched.assign(_order=(sched["season_type"] != 3).astype(int)).sort_values(["_order", "season", "game_id"])
    ids = sched["game_id"].tolist()
    meta = sched.set_index("game_id")[["season", "season_type", "type_abbreviation"]]
    print(f"{len(ids)} games, {WORKERS} workers", flush=True)
    rows: list[dict] = []
    with ThreadPoolExecutor(WORKERS) as pool:
        for n, row in enumerate(pool.map(census_one, ids), 1):
            rows.append(row)
            if n % 1000 == 0:
                print(f"{n}/{len(ids)}", flush=True)
                pd.DataFrame(rows).to_parquet(out)
    df = pd.DataFrame(rows).join(meta, on="game_id")
    df.to_parquet(out)
    print(df.groupby("status").size().to_string())


if __name__ == "__main__":
    main()
