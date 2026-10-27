"""One-command pipeline run: fetch -> normalize -> data/processed/.

    python3 pipeline/run.py                      # seasons 2002-2026
    python3 pipeline/run.py --start 2024 --end 2024
    python3 pipeline/run.py --force              # redo seasons that already have output

Each season is downloaded, normalized, and its raw file deleted before the next one starts.
Per-season output goes to data/processed/parts/, so an interrupted run resumes where it
stopped. The parts are then combined into events.parquet, games.parquet and summary.json.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

from fetch import FIRST_SEASON, LAST_SEASON, download_season, raw_path
from normalize import Normalized, normalize_season


def process_season(season: int, raw_dir: Path, parts_dir: Path, keep_raw: bool) -> dict[str, int]:
    path = raw_path(raw_dir, season)
    downloaded = not path.exists()
    if downloaded:
        path = download_season(season, raw_dir)
    try:
        result: Normalized = normalize_season(pd.read_parquet(path))
    finally:
        if downloaded and not keep_raw:
            path.unlink(missing_ok=True)
    result.events.to_parquet(parts_dir / f"events_{season}.parquet", compression="zstd", index=False)
    result.games.to_parquet(parts_dir / f"games_{season}.parquet", compression="zstd", index=False)
    stats = {"season": season, **result.stats}
    (parts_dir / f"stats_{season}.json").write_text(json.dumps(stats))
    return stats


def combine(parts_dir: Path, out_dir: Path, seasons: list[int]) -> dict:
    have = [s for s in seasons if (parts_dir / f"stats_{s}.json").exists()]
    events = pd.concat([pd.read_parquet(parts_dir / f"events_{s}.parquet") for s in have], ignore_index=True)
    games = pd.concat([pd.read_parquet(parts_dir / f"games_{s}.parquet") for s in have], ignore_index=True)
    for col in ("possession", "possession_status", "event_type", "acting_side", "detail"):
        events[col] = events[col].astype("category")
    events.to_parquet(out_dir / "events.parquet", compression="zstd", index=False)
    games.to_parquet(out_dir / "games.parquet", compression="zstd", index=False)
    per_season = [json.loads((parts_dir / f"stats_{s}.json").read_text()) for s in have]
    keys = ("games", "events", "certain", "loose", "unknown", "reordered_rows", "dropped_no_clock")
    summary = {
        "seasons": have,
        "total": {k: sum(p[k] for p in per_season) for k in keys},
        "per_season": per_season,
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=1))
    return summary


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--start", type=int, default=FIRST_SEASON)
    ap.add_argument("--end", type=int, default=LAST_SEASON)
    ap.add_argument("--raw-dir", type=Path, default=Path("data/raw"))
    ap.add_argument("--out-dir", type=Path, default=Path("data/processed"))
    ap.add_argument("--keep-raw", action="store_true", help="keep raw files that this run downloaded")
    ap.add_argument("--force", action="store_true", help="redo seasons that already have output")
    args = ap.parse_args(argv)

    parts_dir = args.out_dir / "parts"
    parts_dir.mkdir(parents=True, exist_ok=True)
    seasons = list(range(args.start, args.end + 1))
    failed: list[int] = []
    for season in seasons:
        if not args.force and (parts_dir / f"stats_{season}.json").exists():
            print(f"{season}: already processed, skipping")
            continue
        try:
            s = process_season(season, args.raw_dir, parts_dir, args.keep_raw)
        except Exception as err:  # keep going; report at the end
            print(f"{season}: FAILED: {err}", file=sys.stderr)
            failed.append(season)
            continue
        print(
            f"{season}: {s['games']} games, {s['events']} events, "
            f"{s['loose']} loose, {s['unknown']} unknown possession"
        )
    summary = combine(parts_dir, args.out_dir, seasons)
    t = summary["total"]
    print(
        f"total: {len(summary['seasons'])} seasons, {t['games']} games, {t['events']} events, "
        f"{t['loose'] + t['unknown']} uncertain possession ({t['loose']} loose, {t['unknown']} unknown)"
    )
    if failed:
        print(f"failed seasons: {failed}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
