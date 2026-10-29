# Data source: box scores, schedules, referees (Deep Cut data spike 2)

Everything Deep Cut needs for version 1 can be downloaded from this cloud session, including referees. All of it comes from the same **sportsdataverse `sportsdataverse-data` GitHub releases** that spike 1 confirmed for play-by-play. Counts below are real, from the data, produced by `pipeline/spike/boxscore_feasibility.py` (full output: `docs/boxscore-feasibility-output.txt`).

## Answers to the five questions

| # | Need | Source (release tag) | Seasons | Verdict |
| --- | --- | --- | --- | --- |
| 1 | Player box scores | `espn_nba_player_boxscores` | 1994-2027 files; use 2002-2026 | **Yes.** Points, rebounds, assists, minutes, team, game id, plus steals, blocks, threes, shooting. |
| 2 | Team box scores and final scores | `espn_nba_team_boxscores` | 1994-2027 files; use 2002-2026 | **Yes.** One row per team per game, with `team_score`, `opponent_team_score`, `team_winner`. |
| 3 | Schedule / games table | `espn_nba_schedules` | 1994-2027 files; use 2002-2026 | **Yes.** Date, home and away team, season, regular season or playoffs, status, overtime, plus playoff round labels. |
| 4 | Referees | `espn_nba_officials` | **2002-2027** | **Yes, with gaps.** Names only, no ids, no crew chief. **Every playoff game of 2009, 2010 and 2011 is missing**, and 1.4% of games overall. See "Referees". |
| 5 | Players and teams with names, spelling variants, seasons | none (no table found) | n/a | **Derivable, but no alias data.** 2,520 players and 30 franchises can be built from the box scores. Spelling variants and nicknames must be added by hand. |

The era in SPEC.md ("since 2002", meaning the 2001-02 season on) fits the data well: the box scores are complete from then (see "Completeness"), and the officials release starts in exactly 2002.

## What this session can reach

| Host | Result |
| --- | --- |
| `github.com/.../releases/download/...` (release assets) | **Works.** Fast, no auth. |
| `raw.githubusercontent.com` (any public repo) | **Works**, and supports HTTP range requests. |
| `pypi.org` (package registries) | Works. |
| ESPN site and core APIs, `stats.nba.com`, `cdn.nba.com`, Basketball-Reference, Wikipedia, Wikidata | **Blocked** (connection refused by the proxy). No live API, and no outside alias source. |
| The release listing page `github.com/.../releases/tag/<tag>` | 403, so tags cannot be listed. The tags above were found by using hoopR's naming and testing the URLs. Other tags may exist. |

## The sources

All files are parquet. The year in a file name is the year the season **ends** (`2024` = 2023-24). The same season number is also the `season` column. Use `pandas` plus `pyarrow`.

| Source | URL pattern | Files | Per-season size | 2002-2026 total |
| --- | --- | --- | --- | --- |
| Player box | `https://github.com/sportsdataverse/sportsdataverse-data/releases/download/espn_nba_player_boxscores/player_box_<YEAR>.parquet` | 1994-2027 | 546-728 KB | 16.6 MB |
| Team box | `.../espn_nba_team_boxscores/team_box_<YEAR>.parquet` | 1994-2027 | 123-152 KB | 3.5 MB |
| Schedule | `.../espn_nba_schedules/nba_schedule_<YEAR>.parquet` | 1994-2027 | 83-526 KB | 3.0 MB |
| Officials | `.../espn_nba_officials/officials_<YEAR>.parquet` | **2002-2027** | about 20-25 KB | 0.6 MB |

All four for 2002-2026 are 100 files and 23 MB, and download in about 30 seconds. `<YEAR>` 2027 is the season in progress (52 games so far) and should be left out, so that valid-answer lists stay fixed.

### Exact download command

```bash
mkdir -p data/raw/boxscores && cd data/raw/boxscores
B=https://github.com/sportsdataverse/sportsdataverse-data/releases/download
for y in $(seq 2002 2026); do
  curl -sSLf -O $B/espn_nba_team_boxscores/team_box_$y.parquet
  curl -sSLf -O $B/espn_nba_player_boxscores/player_box_$y.parquet
  curl -sSLf -O $B/espn_nba_schedules/nba_schedule_$y.parquet
  curl -sSLf -O $B/espn_nba_officials/officials_$y.parquet
done
pip install pandas pyarrow
```

Tested from an empty directory: 28 seconds, 100 files, 23 MB. `data/raw/` is gitignored.

### How to load

```python
import pandas as pd
from pathlib import Path

raw = Path("data/raw/boxscores")
def load(prefix):
    return pd.concat([pd.read_parquet(raw / f"{prefix}_{y}.parquet") for y in range(2002, 2027)], ignore_index=True)

player, team, sched, officials = load("player_box"), load("team_box"), load("nba_schedule"), load("officials")
```

### Key columns

**Player box** (about 35,000 rows per season, 57 columns). One row per player per game, including players who did not play.
`game_id`, `season`, `season_type` (2 regular, 3 playoffs, 5 play-in), `game_date`, `athlete_id`, `athlete_display_name`, `athlete_short_name`, `athlete_position_abbreviation`, `athlete_jersey`, `team_id`, `team_display_name`, `team_abbreviation`, `home_away`, `team_winner`, `team_score`, `opponent_team_id`, `opponent_team_score`, `minutes`, `points`, `rebounds`, `offensive_rebounds`, `defensive_rebounds`, `assists`, `steals`, `blocks`, `turnovers`, `fouls`, `field_goals_made/attempted`, `three_point_field_goals_made/attempted`, `free_throws_made/attempted`, `plus_minus` (string), `starter`, `did_not_play`.

**Team box** (about 2,640 rows per season, 57 columns). Two rows per game.
`game_id`, `season`, `season_type`, `game_date`, `team_id`, `team_display_name`, `team_location`, `team_name`, `team_abbreviation`, `team_home_away`, `team_score`, `opponent_team_id`, `opponent_team_display_name`, `opponent_team_score`, `team_winner`, plus team totals: `field_goals_made/attempted`, `three_point_field_goals_made/attempted`, `free_throws_made/attempted`, `total_rebounds`, `assists`, `steals`, `blocks`, `turnovers`, `fouls`. `fast_break_points`, `points_in_paint`, `turnover_points` and `largest_lead` are strings and are empty in about 7% of recent rows; `largest_lead` is empty for most 2002-2005 rows.

**Schedule** (about 1,300 rows per season, 77 columns). One row per game, including postponed games.
`game_id`, `season`, `season_type`, `date` / `game_date`, `type_abbreviation` (`STD`, `RD16`, `QTR`, `SEMI`, `FINAL`, `ALLSTAR`, `CC`), `status_type_name` (`STATUS_FINAL` or `STATUS_POSTPONED`), `status_type_detail` (`Final`, `Final/OT`, `Final/2OT`...), `status_period` (4 = decided in regulation), `home_id`, `home_display_name`, `home_score`, `away_id`, `away_display_name`, `away_score`, `venue_full_name`, `attendance`, `notes_headline` (series and game label, mostly empty before 2020), plus flags `PBP`, `team_box`, `player_box`, `game_json` and `game_json_url`.

**Officials** (about 4,000 rows per season, 7 columns). One row per official per game.
`season`, `game_id`, `official_full_name`, `official_display_name` (identical to the full name), `official_position` (always "Referee"), `official_position_id` (always 40), `official_order`.

All four join on `game_id`, which is the same ESPN id in every file and in the play-by-play.

## Rules the data needs

These came out of checking the data against known facts (league schedule sizes, Finals lengths and champions, Kobe Bryant's 81 points on 2006-01-22, the 2015-16 Warriors' 73 wins; both are in the script output). The spike script implements them.

- **Who played:** use `points` is not null. The `did_not_play` flag is unreliable: in 2006-2012 it is almost never set, and 28-31% of rows are non-players with all-null stats. With the null rule every season has a steady median of 10 players with stats per team-game.
- **Regular season:** `season_type == 2` and `type_abbreviation == 'STD'` and both teams are NBA franchises. `season_type == 2` alone also holds the All-Star game and the NBA Cup final (`CC`), and some Rising Stars and USA-versus-World games are even typed `STD`. With this rule the regular-season game counts match the league schedule exactly: 1,189 (29 teams, 2002-2004), 1,230 (30 teams), 990 in the 2012 lockout season, 1,059 in 2020 and 1,080 in 2021. The only exception is 2013 with 1,229, where the schedule itself is one game short.
- **Playoffs:** `season_type == 3`. **Play-in:** `season_type == 5` (2020 on).
- **Finals:** `type_abbreviation == 'FINAL'` only exists from 2004. For 2002 and 2003 the Finals are the series between the two teams that played the last playoff game. This reproduces all 131 labelled games, adds 4 + 6, and gives the right champion and length for all 25 years.
- **Game number in a series (Game 7):** `notes_headline` only has "Game 7" style labels from 2020 (it finds 25 Game 7s). Numbering games by date within each series finds 79 and agrees with all 554 labelled games.
- **Regulation game:** `status_period == 4` (present for every final game).
- **NBA franchises:** the 30 `team_id`s with 300 or more team-games. The team box also has 14 non-NBA sides that must be excluded: Eastern and Western Conf All-Stars, Team LeBron, Team Giannis, Team Stephen, Team Durant, Team Candace, Team Chuck, Team Kenny, Team Shaq, Team Stars, Team Stripes, USA, World.
- **Franchise identity:** `team_id` is stable across moves and renames. Four ids change name: 3 (Charlotte Hornets 2002, New Orleans Hornets, NO/Oklahoma City Hornets, New Orleans Pelicans), 17 (New Jersey Nets, Brooklyn Nets), 25 (Seattle SuperSonics, Oklahoma City Thunder), 30 (Charlotte Bobcats, Charlotte Hornets). Abbreviations change for the same three: CHA/NO, NJ/BKN, SEA/OKC.
- **Triple-double:** 10 or more in three of points, rebounds, assists, steals and blocks.

## Completeness

| Check | Result |
| --- | --- |
| Final NBA games 2002-2026 | 32,190 (30,065 regular, 2,085 playoffs including 141 Finals, 37 play-in, 3 Cup finals) |
| Games with no team box rows | 14 (2013: 5, 2014: 1, 2017: 1, 2018: 1, 2021: 6) |
| Games with no player box rows | 27 (2005: 2, 2006: 13, 2007: 2, 2011: 1, 2013: 5, 2014: 1, 2017: 1, 2018: 1, 2019: 1) |
| Team-games where player points do not add up to the team score | 81 of 64,396 (0.13%), 25 of them in 2019 |
| Playoff series found | 375, and every one has a winner with 4 wins (3 for the 2002 best-of-5 first round) |
| Finals | 25 of 25 seasons have a 4-win champion, and game counts match history (for example 7 games in 2005, 2010, 2013, 2016 and 2025) |
| Duplicates | none for (game, athlete) or (game, team) |

The 27 games without player rows could hide a few answers, but the effect is tiny: about 7.5% of those games would contain a 40-point scorer at the overall rate, which is roughly two games, and nearly all of those players have other 40-point games. The pipeline can double-check with the play-by-play (`athlete_id_1` on scoring plays) if it wants to close the gap.

Before 2001 the box scores exist back to 1994 but have holes (for example 1996 has team box rows for only 1,106 of 1,189 regular-season games), so they are not a safe extension of the era. The 2000-01 season (file `2001`) looks complete (1,189 regular-season games) but has no officials or play-by-play.

## Feasibility counts since 2002

Counts are distinct players (or franchises) with at least one qualifying game, from `boxscore_feasibility.py`. SPEC.md needs 15 or more valid answers for a player prompt and 5 or more for a team prompt; it also wants a maximum, which the generator session has to choose. Rows marked **below** fail the minimum.

### The three examples you asked about

| Question | Count |
| --- | --- |
| Players with a 40+ point game in the regular season | **263** players (2,240 games) |
| Teams with 60+ wins in a season | **16** franchises (36 team-seasons) |
| Games where a team scored 140+ | **456** games (506 team-games), by all 30 franchises. 370 games in regulation. |

### Player prompts

| Template | Distinct players | Games |
| --- | --- | --- |
| 40+ points, regular season | 263 | 2,240 |
| 50+ points, regular season | 93 | 293 |
| 60+ points, regular season | 24 | 41 |
| 70+ points, regular season | 7 (**below**) | 7 |
| 40+ points, playoffs | 73 | 264 |
| 50+ points, playoffs | 17 | 22 |
| 30+ points, Finals | 39 | 133 |
| 40+ points, Finals | 15 | 28 |
| 30+ points in a Game 7 | 46 | 65 |
| Triple-double, regular season | 248 | 1,825 |
| Triple-double, playoffs | 42 | 162 |
| Triple-double, Finals | 11 (**below**) | 25 |
| 30+ point triple-double | 76 | 434 |
| Quadruple-double | 0 (**below**) | 0 |
| 20+ rebounds | 184 | 1,199 |
| 25+ rebounds | 43 | 83 |
| 20+ assists | 27 | 67 |
| 22+ assists | 12 (**below**) | 17 |
| 10+ blocks | 20 | 31 |
| 8+ steals | 52 | 62 |
| 9+ steals | 12 (**below**) | 12 |
| 10+ threes made | 59 | 121 |
| 12+ threes made | 8 (**below**) | 16 |
| 10+ field goals with no misses | 47 | 58 |

The full threshold ladders (30 to 70 points, other cutoffs) are in the output file. Some templates give very long lists (734 players with 30+ points, 248 with a triple-double), which probably needs the maximum from the spec.

### Team prompts

| Template | Franchises | Instances |
| --- | --- | --- |
| 55+ wins in a season | 23 | 90 |
| 60+ wins in a season | 16 | 36 |
| 65+ wins in a season | 9 | 11 |
| 67+ wins in a season | 4 (**below**) | 6 |
| 60+ losses in a season | 28 | 59 |
| 65+ losses in a season | 14 | 19 |
| 68+ losses in a season | 4 (**below**) | 4 |
| 140+ points in a game | 30 | 506 team-games |
| 150+ points in a game | 25 | 67 team-games (60 games) |
| 150+ points in a regulation game | 23 | 51 team-games (48 games) |
| 160+ points in a game | 7 | 7 |
| Won by 50+ points | 21 | 43 |
| Won by 60+ points | 4 (**below**) | 4 |
| Scored under 60 points | 10 | 15 |
| 25+ threes made in a game | 23 | 74 |
| 28+ threes made in a game | 5 | 6 |
| 15+ game regular-season winning streak | 15 | 23 |
| 20+ game winning streak | 3 (**below**) | 3 |
| Won the NBA title | 13 | 25 |

Win and loss thresholds need care because 2012 (66 games), 2020 (up to 75) and 2021 (72) are short seasons. The sanity checks hold: the most wins are the 2016 Warriors with 73, then the 2025 Thunder with 68.

### Referee prompts

| Template | Distinct officials | Games |
| --- | --- | --- |
| Officiated an NBA Finals game (2009-2011 missing) | 47 | 122 |
| Officiated a Finals game, 2012 on (complete years) | 33 | 84 |
| Officiated a playoff Game 7 | 52 | 72 |
| Officiated a game with a 60+ point scorer | 78 | 40 |
| Officiated a triple-overtime or longer game | 66 | 37 |
| Officiated 1,000+ games | 39 | 29,184 |

These use the officials that exist, so the playoff and Finals rows are incomplete for 2009-2011 (see below).

## Players and teams universe

There is no player or team table in the releases. I guessed a few tags (`espn_nba_players`, `espn_nba_teams`, `espn_nba_rosters`, `espn_nba_player_stats`, `nba_players`) and none exist, though the tag list cannot be enumerated. Build the universe from the box scores instead.

**Players:** 2,520 athletes appeared since 2002 (rows with a points value), with 2,514 distinct display names. From `player_box`, per `athlete_id`, you get the display name, short name, position, jersey, the teams and seasons played, and career totals (median 4 seasons, longest 23).

**What the names look like, and what is missing for matching:**

- Names are **plain ASCII** (`Luka Doncic`, `Nikola Jokic`, `Hedo Turkoglu`). No accented display names exist, so accent stripping only matters for what the player types.
- **No aliases or nicknames.** For example there is no "Ron Artest" for Metta World Peace.
- **6 athlete ids changed display name over time:** Jimmy Butler / Jimmy Butler III, Reggie Bullock / Reggie Bullock Jr., Nigel Hayes / Nigel Hayes-Davis, Rondae Hollis Jefferson / Rondae Hollis-Jefferson, O.G. Anunoby / OG Anunoby, Omari Spellman / Omari Rasulala Spellman.
- **43 ids have more than one `athlete_short_name`,** and these hold the only accented and alternate spellings in the data: Nenê, Calderón, Felício, Hernangómez, Schröder, and a later name change ("E. Freedom" versus "Kanter" on one id, presumably Enes Kanter Freedom). They are a free source of aliases.
- **12 display names belong to 2 athlete ids:** Brandon Williams, Chris Johnson, Chris Wright, Corey Brewer, Daryl Macon, Dee Brown, Isaiah Canaan, Marcus Williams, Mike James, Tony Mitchell, Trevon Scott, Wayne Selden. Some are different people, some may be duplicate ids for one person; this was not resolved. They need disambiguation in the autocomplete.
- **Last names:** only 52.7% of players have a last name (suffix removed) that nobody else shares, so the "last name only if unique" rule from the spec will accept about half of all players.
- **Dirty strings:** `'Nene '` (trailing space), `'Mike  Harris'` and `'Chris  Smith'` (double space), and 22 stat lines with no athlete name or id (all zero points). Suffixes appear on 82 names (Jr., III), and 144 names contain `'`, `.` or `-`.

**Teams:** 30 franchises after excluding the 14 non-NBA sides. Names per season come from `team_display_name` (also `team_location`, `team_name`, `team_abbreviation`). Dirty string: one 2006 name is `"NO/Oklahoma City\r\n Hornets"`, with a carriage return and line feed inside it. The season-specific names ("Seattle SuperSonics" for 2002-2008, "New Jersey Nets" for 2002-2012) are what the spec's "defunct or renamed franchise names" tier rule needs.

## Referees

**Source:** release tag `espn_nba_officials`, files `officials_2002.parquet` to `officials_2027.parquet`. It was built from the raw ESPN game JSON (`gameInfo.officials`), which sportsdataverse also mirrors at `https://raw.githubusercontent.com/sportsdataverse/hoopR-nba-raw/main/nba/json/final/<game_id>.json`. That raw file is about 700 KB per game, but `officials` sits in the last 25 KB, so a range request (`curl -r -32768`) gets it cheaply. It appears to be built from that file: I checked about 13,000 games (all playoff games plus part of the regular season) against the release, and they agree, except for 6 games where the raw file lists the same name twice and the release lists it once, and 1 game that has officials in the raw file but none in the release. `pipeline/spike/referee_census.py` does that check. The release is the easier source and the raw JSON adds nothing.

**Columns:** `season`, `game_id`, `official_full_name`, `official_display_name`, `official_position`, `official_position_id`, `official_order`.

**What is there:** 95,682 rows, 31,776 games, **169 distinct names**, 31,129 games with 3 officials. 39 officials worked 1,000+ games, 80 worked 500+ (median 418, most 1,783), and 25 worked 10 or fewer.

**What is missing or wrong:**

- **Every playoff game of 2009, 2010 and 2011 has no officials** (248 games, including all three Finals). The regular season of 2011 is also short (92.4% of games have officials, 93 games missing).
- **Other gaps:** 184 regular-season games overall (0.6%), 1 to 3% in 2021-2024, 1 Finals game in 2023. In total 98.6% of the 32,190 NBA games have officials, and 439 do not.
- **No official id.** Names only, so the same referee under two spellings is two people. Variants seen: `J.B. DeRosa` / `JB DeRosa` / `Joe DeRosa`, `J.D. Ralls` / `JD Ralls`, `J.T. Orr` / `JT Orr`, `Steve Anderson` / `Steven Anderson`, `Nate  Green` (double space). `Jacyn Goble` and `John Goble` may be a mistake or two people.
- **No roles.** Every row says "Referee", with no crew chief, referee or umpire distinction, so "crew chief" prompts are impossible.
- **Wrong crews in 2014-2020:** 219 games have two different names in the same `official_order` slot (for example `Kevin Scott` and `Byron Scott` both in slot 3), and 4 or 5 officials listed instead of 3 in 501 games. The extra names may be wrong, so prompts should not depend on a single game's crew in those seasons.
- **Before 2002:** nothing. The release has no 2001 or earlier file.

**Verdict for the spec:** referee prompts are possible (the reserve list in SPEC.md calls them a stretch type). Use only questions that tolerate gaps and name noise, for example "officiated a Finals game since 2012" (33 officials) or "officiated a playoff Game 7" (52 officials), and label the era accordingly. The 2009-2011 playoff hole means a "since 2002" prompt about the playoffs would have an incomplete valid-answer list, which breaks the spec's own rule. Normalize names (strip dots and double spaces, `Steven`/`Steve`) before building the answer list.

## Other findings

- **Exhibition games are inside the regular season** if you only use `season_type`. See "Rules".
- **Postponed games** appear in the schedule (67 rows, mostly 2020-2022) with no box score. Filter on `STATUS_FINAL`.
- **Overtime:** `status_period` 5 or more means overtime. `status_type_detail` says `Final/OT`, `Final/2OT`, and so on.
- **The schedule has playoff round labels** in `type_abbreviation`: `RD16` (first round), `QTR`, `SEMI`, `FINAL`, but only from 2004. The 2002 and 2003 playoff games (159 games) are all typed `STD`.
- The raw per-game JSON and the play-by-play also contain player names per play, but nothing that the box scores do not already give for these prompts.

## What is missing, in one place

1. **Referee data has holes:** all 2009-2011 playoffs, about 0.6% of regular-season games, no ids, no roles, and noisy crews in 2014-2020.
2. **No alias, nickname, birth, draft or country data** for players. Aliases must be hand-written or derived from the 43 short-name variants.
3. **No player or team reference table.** Both have to be derived.
4. **27 NBA games have no player box rows and 14 have no team box rows** (listed above), plus 81 team-games whose player points do not add up.
5. **Before 2002 the data is incomplete and has no officials.**
6. **Other sites are blocked** (ESPN API, NBA stats, Basketball-Reference, Wikipedia, Wikidata). Anything not in the GitHub releases cannot be fetched.
7. **`did_not_play`, `notes_headline` and `type_abbreviation == 'FINAL'` are unreliable** in the early seasons. Use the rules above.

## For the next sessions

- The pipeline (session 2) can read exactly these four files per season. Keep a small `season`, `game_id` join and apply the rules in "Rules the data needs".
- Pin the data to 2002-2026. Excluding the in-progress 2027 files keeps every valid-answer list fixed.
- Choose each template's maximum with the counts above in mind. For example the regular-season 40-point list (263 players) is large, while 55+ (41) or 60+ (24) are tighter.
- Referee prompts should wait until the stretch list, and need name cleanup first.

## Reproduce

```bash
# download (28 s, 23 MB): see "Exact download command"
python3 pipeline/spike/boxscore_feasibility.py data/raw/boxscores        # output: docs/boxscore-feasibility-output.txt
python3 pipeline/spike/referee_census.py data/raw/boxscores /tmp/referee_census.parquet 2002 2026   # optional cross-check, about 32,000 small range requests
```
