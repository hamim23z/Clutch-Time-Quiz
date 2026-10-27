# Data source (session 1 spike)

## Working source

**sportsdataverse `sportsdataverse-data` GitHub releases, tag `espn_nba_pbp`** (this is the dataset behind the hoopR R package). It holds ESPN play-by-play, one parquet file per season, and it downloads directly from this cloud session through the GitHub release CDN.

- Release page: https://github.com/sportsdataverse/sportsdataverse-data/releases/tag/espn_nba_pbp
- File pattern: `play_by_play_<YEAR>.parquet`, where `<YEAR>` is the season's **end** year (`2024` = 2023-24, games from 2023-10-24 to 2024-06-17).
- Checked reachable (HTTP 200): 2002, 2005, 2010, 2015, 2018, 2020, 2024, 2025, 2026.
- Size: about 20 MB and about 600k rows per season; 2024 has 1,320 games (regular season, playoffs and play-in).

Package-registry libraries (`nba_api`, `hoopR`) were not needed. `nba_api` calls stats.nba.com live, which is the kind of host a cloud session usually cannot reach.

## Exact download command

```bash
mkdir -p data/raw
curl -sSL -o data/raw/play_by_play_2024.parquet \
  https://github.com/sportsdataverse/sportsdataverse-data/releases/download/espn_nba_pbp/play_by_play_2024.parquet
pip install pandas pyarrow   # pyarrow is required to read parquet
```

Then print the last 60 seconds of 3 close games:

```bash
python3 pipeline/spike/sample_games.py data/raw/play_by_play_2024.parquet
```

The script picks the first 3 regular-season games (by `game_id`) that ended within 3 points in regulation: BKN at CHI (2023-11-03), GS at OKC (2023-11-03), NO at HOU (2023-11-10). Its full output is in `docs/spike-sample-output.txt`.

## Columns (2024 file, 68 columns)

The columns the pipeline needs:

| Need | Column(s) | Notes |
| --- | --- | --- |
| Game / order | `game_id`, `game_play_number` (sort key), `sequence_number` | Sort by `game_play_number`. |
| Score | `home_score`, `away_score` | Score **after** the event. Margin = `home_score - away_score`. |
| Clock | `start_game_seconds_remaining`, `period_number`, `clock_display_value`, `start_quarter_seconds_remaining` | Use `start_*` for the clock at the event. `end_*` is the clock at the *next* event, so don't use it for that. Overtime periods are 5, 6, and so on. |
| Event type | `type_text`, `type_id`, `text`, `shooting_play`, `scoring_play`, `score_value` | `type_text` has about 140 values (for example `Jump Shot`, `Shooting Foul`, `Personal Take Foul`, `Full Timeout`, `Defensive Rebound`, `Lost Ball Turnover`, `Free Throw - 1 of 2`). |
| Acting team | `team_id`, compared with `home_team_id` / `away_team_id` | For shots, free throws, rebounds and turnovers it is the team doing the action. For fouls it is the **fouling** team. It is null on period markers and reviews (about 1% of rows). |
| Teams | `home_team_name`, `home_team_mascot`, `home_team_abbrev`, and the `away_*` versions | Plain names only, for `actual.game`. |
| Date | `game_date`, `season`, `season_type` (2 = regular, 3 = playoffs, 5 = play-in) | |
| Players | `athlete_id_1..3`, `athlete_name_1..3` | |
| Other | `coordinate_x/y`, `game_spread`, `home_team_spread`, `home_favorite`, `wallclock`, `points_attempted`, `short_description`, `score_source` | |

## What's missing or unreliable

- **No possession column.** It has to be inferred from the event and `team_id`: a defensive rebound gives the ball to the rebounder's team; a made field goal or a last made free throw gives it to the other team; a turnover gives it to the other team; a foul's `team_id` is the defense. The spike script's `possession_after` column is a rough version of this, for display only. Session 2 must build and test it properly.
- **No explicit 3PT flag** on field goals (`points_attempted` is almost always null). Use `"three point"` in `text` together with `shooting_play`. Missed threes say "misses 27-foot three point ...". Spot-check this on older seasons, where the wording may differ.
- **Timeout flags are broken:** `home_timeout_called` and `away_timeout_called` are False on every 2024 row, and they are missing entirely from 2010 and 2018. Find timeouts with `type_text == "Full Timeout"` (2010 also has `"Short Timeout"`), plus `team_id`. A coach's challenge that fails can charge a timeout but only says so in `text`.
- **No shot clock.** "Hold for the last shot" and "≤24 s, final possession" have to be inferred from the game clock.
- **Sub-second clock is lost near 0.** GS at OKC: Curry's game winner was at 0.2 s according to the review text, but the row shows `0.0`.
- **Event order within one clock tick is loose.** Substitutions, fouls and free throws that share a timestamp can come out of order, so order within a tick should not be fully trusted.
- **Schema drift between seasons:** 2010 and 2018 lack `wallclock`, `points_attempted`, `short_description`, the `*_timeout_called` columns and `lag_half`/`lead_half`, and have `lag_game_half`/`lead_game_half` instead. The core columns above are present in every season checked.
- `score_source` is `rebuilt` on most rows, meaning sportsdataverse reconstructed the score. It looked correct in all 3 sample games.
