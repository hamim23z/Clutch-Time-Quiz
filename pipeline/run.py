"""One-command pipeline run: fetch -> normalize -> data/processed/ and docs/pipeline-notes.md.

    python3 pipeline/run.py                          # seasons 2002-2026
    python3 pipeline/run.py --start 2024 --end 2024
    python3 pipeline/run.py --force                  # redo seasons that already have output

Each season is downloaded, processed and its raw files deleted (if this run downloaded them) before the next
one starts. Per-season results go to data/processed/parts/, so an interrupted run resumes where it stopped.
Then the six tables are written: players, teams, games, player_games, team_games, officials.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

from assemble import TABLES, combine
from fetch import FIRST_SEASON, LAST_SEASON, download_season, season_paths
from notes import write_notes
from season import SeasonTables, load_season, process_season, save_season, season_is_saved

HERE = Path(__file__).resolve().parent
DEFAULT_ALIASES = HERE / "data" / "aliases.csv"
DEFAULT_NOTES = HERE.parent / "docs" / "pipeline-notes.md"


def run_season(season: int, raw_dir: Path, keep_raw: bool) -> SeasonTables:
    paths = season_paths(raw_dir, season)
    downloaded = [t for t, p in paths.items() if not p.exists()]
    download_season(season, raw_dir)
    try:
        raw = {table: pd.read_parquet(path) for table, path in paths.items()}
        return process_season(season, raw)
    finally:
        if not keep_raw:
            for table in downloaded:
                paths[table].unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--start", type=int, default=FIRST_SEASON)
    ap.add_argument("--end", type=int, default=LAST_SEASON)
    ap.add_argument("--raw-dir", type=Path, default=Path("data/raw/boxscores"))
    ap.add_argument("--out-dir", type=Path, default=Path("data/processed"))
    ap.add_argument("--aliases", type=Path, default=DEFAULT_ALIASES)
    ap.add_argument("--notes", type=Path, default=DEFAULT_NOTES)
    ap.add_argument("--keep-raw", action="store_true", help="keep raw files that this run downloaded")
    ap.add_argument("--force", action="store_true", help="redo seasons that already have output")
    args = ap.parse_args(argv)

    parts_dir = args.out_dir / "parts"
    parts_dir.mkdir(parents=True, exist_ok=True)
    seasons = list(range(args.start, args.end + 1))
    failed: list[int] = []
    results: list[SeasonTables] = []
    for season in seasons:
        try:
            if season_is_saved(season, parts_dir) and not args.force:
                result = load_season(season, parts_dir)
                print(f"{season}: already processed, loaded")
            else:
                result = run_season(season, args.raw_dir, args.keep_raw)
                save_season(result, parts_dir)
                print(f"{season}: {len(result.games)} games, {len(result.player_games)} player rows, {len(result.skipped)} skipped")
        except Exception as err:  # keep going; report at the end
            print(f"{season}: FAILED: {err}", file=sys.stderr)
            failed.append(season)
            continue
        results.append(result)
    if not results:
        print("nothing processed", file=sys.stderr)
        return 1

    partial = [s.season for s in results] != list(range(FIRST_SEASON, LAST_SEASON + 1))
    tables = combine(results, args.aliases, partial=partial)
    written = {}
    for name in TABLES:
        df = getattr(tables, name)
        df.to_parquet(args.out_dir / f"{name}.parquet", compression="zstd", index=False)
        written[name] = len(df)
    write_notes(tables, written, args.notes)
    (args.out_dir / "summary.json").write_text(
        json.dumps({"seasons": tables.seasons, "rows": written, "games_skipped": len(tables.skipped),
                    "excluded": tables.excluded, "name_merges": tables.officials_result.stats["name_merges"]}, indent=1)
    )
    print("rows: " + ", ".join(f"{k} {v:,}" for k, v in written.items()))
    print(f"games skipped: {len(tables.skipped)}; official name merges: {tables.officials_result.stats['name_merges']}")
    if failed:
        print(f"failed seasons: {failed}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
