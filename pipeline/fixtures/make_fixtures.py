"""Rebuild the raw-schema test fixtures from full season downloads (not needed to run tests).

    python3 pipeline/fixtures/make_fixtures.py <raw-dir>

<raw-dir> must hold play_by_play_2002/2013/2024.parquet. Each fixture keeps every raw column
but only the 4th quarter and overtimes of a few games, so tests run on a few hundred rows.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
SPIKE_GAMES_2024 = [401584092, 401584093, 401584099]  # the 3 games printed in docs/spike-sample-output.txt


def clutch_rows(raw: pd.DataFrame, game_ids: list[int]) -> pd.DataFrame:
    g = raw[raw.game_id.isin(game_ids) & (raw.period_number >= 4)]
    return g.sort_values(["game_id", "game_play_number"]).reset_index(drop=True)


def first_close_ot_game(raw: pd.DataFrame) -> int:
    ot = raw[(raw.period_number == 5) & (raw.season_type == 2)].game_id.unique()
    return int(sorted(ot)[0])


def main(raw_dir: Path) -> None:
    r2002 = pd.read_parquet(raw_dir / "play_by_play_2002.parquet")
    r2013 = pd.read_parquet(raw_dir / "play_by_play_2013.parquet")
    r2024 = pd.read_parquet(raw_dir / "play_by_play_2024.parquet")
    # 2002: one regulation game; 2013: one game that went to overtime; 2024: the 3 spike games
    first_2002 = int(sorted(r2002[r2002.season_type == 2].game_id.unique())[0])
    clutch_rows(r2002, [first_2002]).to_parquet(HERE / "raw_2002.parquet", compression="zstd", index=False)
    clutch_rows(r2013, [first_close_ot_game(r2013)]).to_parquet(HERE / "raw_2013.parquet", compression="zstd", index=False)
    clutch_rows(r2024, SPIKE_GAMES_2024).to_parquet(HERE / "raw_2024.parquet", compression="zstd", index=False)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
