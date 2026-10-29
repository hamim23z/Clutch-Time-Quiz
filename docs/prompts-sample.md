# Prompts sample and checks

Written by `python3 pipeline/export.py`; do not edit by hand. Tiers are in brackets: 1 is the best-known answer (10 points), 6 the rarest (100 points).

## File sizes

| file | bytes | gzipped (what a static host sends) |
|---|---|---|
| prompts.json | 2,134,446 | 357,770 |
| universe.json | 143,359 | 29,262 |
| both files | 2,277,805 | 387,032 |

The five largest prompts (valid answers, bytes in the file):

- `p-finals-appearance`: 393 answers, 24,502 bytes
- `p-points-playoff-25`: 330 answers, 20,538 bytes
- `p-franchise-regular-17`: 293 answers, 18,457 bytes
- `p-franchise-bench-17`: 287 answers, 18,078 bytes
- `p-franchise-regular-20`: 283 answers, 17,891 bytes

## Recheck of 111 prompts against the processed tables

111 of 111 match. At least 2 prompts from each of the 81 template families were recomputed from the raw rows by a separately written brute-force query (`pipeline/bruteforce.py`) and compared with the exported answers, and the tiers and points were rechecked.

<details><summary>Every prompt checked</summary>

| prompt | valid answers (brute force) | exported answers | result |
|---|---|---|---|
| p-assists-20 | 27 | 27 | ok |
| p-assists-finals-10 | 22 | 22 | ok |
| p-assists-per-game-9 | 19 | 19 | ok |
| p-assists-playoff-16 | 15 | 15 | ok |
| p-beat-in-playoffs-21 | 10 | 10 | ok |
| p-beat-in-playoffs-16 | 9 | 9 | ok |
| p-blocks-6 | 215 | 215 | ok |
| p-blocks-playoff-7 | 21 | 21 | ok |
| p-both-franchises-9-26 | 20 | 20 | ok |
| p-both-franchises-7-26 | 26 | 26 | ok |
| p-champion | 13 | 13 | ok |
| p-double-double-average | 79 | 79 | ok |
| p-finals-appearance | 393 | 393 | ok |
| p-finals-year-2007 | 23 | 23 | ok |
| p-finals-year-2009 | 22 | 22 | ok |
| p-franchise-bench-8 | 219 | 219 | ok |
| p-franchise-bench-19 | 206 | 206 | ok |
| p-franchise-playoff-3 | 83 | 83 | ok |
| p-franchise-playoff-7 | 106 | 106 | ok |
| p-franchise-playoff-season-8-2026 | 17 | 17 | ok |
| p-franchise-playoff-season-15-2023 | 15 | 15 | ok |
| p-franchise-points-20-35 | 15 | 15 | ok |
| p-franchise-points-16-30 | 40 | 40 | ok |
| p-franchise-regular-29 | 267 | 267 | ok |
| p-franchise-regular-30 | 203 | 203 | ok |
| p-franchise-season-8-2022 | 27 | 27 | ok |
| p-franchise-season-2-2026 | 21 | 21 | ok |
| p-franchise-start-4 | 151 | 151 | ok |
| p-franchise-start-18 | 168 | 168 | ok |
| p-franchise-years-3-2022-2026 | 63 | 63 | ok |
| p-franchise-years-10-2002-2006 | 57 | 57 | ok |
| p-franchises-6 | 284 | 284 | ok |
| p-free-throws-22 | 21 | 21 | ok |
| p-held-opponent-60 | 14 | 14 | ok |
| p-held-opponent-in-season-2016-75 | 11 | 11 | ok |
| p-held-opponent-in-season-2008-70 | 13 | 13 | ok |
| p-home-wins-36 | 13 | 13 | ok |
| p-home-wins-in-season-2014-30 | 7 | 7 | ok |
| p-home-wins-in-season-2007-30 | 8 | 8 | ok |
| p-losses-season-65 | 14 | 14 | ok |
| p-made-playoffs-2015 | 16 | 16 | ok |
| p-made-playoffs-2024 | 16 | 16 | ok |
| p-margin-in-season-2020-40 | 7 | 7 | ok |
| p-margin-in-season-2014-40 | 5 | 5 | ok |
| p-minutes-55 | 84 | 84 | ok |
| p-month-points-2004-3-35 | 16 | 16 | ok |
| p-month-points-2021-4-40 | 17 | 17 | ok |
| p-month-threes-2026-2-6 | 41 | 41 | ok |
| p-month-threes-2016-4-5 | 34 | 34 | ok |
| p-offensive-rebounds-11 | 84 | 84 | ok |
| p-overtime-wins-2 | 30 | 30 | ok |
| p-overtime-wins-in-season-2005-2 | 8 | 8 | ok |
| p-overtime-wins-in-season-2013-2 | 11 | 11 | ok |
| p-perfect-shooting-10 | 46 | 46 | ok |
| p-played-playoff-against-20 | 11 | 11 | ok |
| p-played-playoff-against-25 | 16 | 16 | ok |
| p-playoff-wins-in-season-2025-4 | 8 | 8 | ok |
| p-playoff-wins-in-season-2023-4 | 8 | 8 | ok |
| p-points-against-1-45 | 18 | 18 | ok |
| p-points-against-21-45 | 20 | 20 | ok |
| p-points-any-game-160 | 7 | 7 | ok |
| p-points-bench-40 | 35 | 35 | ok |
| p-points-finals-40 | 15 | 15 | ok |
| p-points-game7-35 | 23 | 23 | ok |
| p-points-loss-55 | 20 | 20 | ok |
| p-points-overtime-game-55 | 21 | 21 | ok |
| p-points-playoff-25 | 330 | 330 | ok |
| p-points-playoff-team-140 | 13 | 13 | ok |
| p-points-regular-60 | 24 | 24 | ok |
| p-points-regulation-155 | 10 | 10 | ok |
| p-points-road-55 | 22 | 22 | ok |
| p-ppg-season-26 | 46 | 46 | ok |
| p-reached-finals | 17 | 17 | ok |
| p-rebounds-24 | 52 | 52 | ok |
| p-rebounds-finals-16 | 19 | 19 | ok |
| p-rebounds-per-game-10 | 82 | 82 | ok |
| p-rebounds-playoff-22 | 17 | 17 | ok |
| p-regulation-points-in-season-2011-125 | 17 | 17 | ok |
| p-regulation-points-in-season-2014-135 | 6 | 6 | ok |
| p-road-wins-28 | 12 | 12 | ok |
| p-road-wins-in-season-2003-23 | 5 | 5 | ok |
| p-road-wins-in-season-2018-23 | 5 | 5 | ok |
| p-season-assists-2025-15 | 18 | 18 | ok |
| p-season-assists-2020-11 | 64 | 64 | ok |
| p-season-points-2016-40 | 22 | 22 | ok |
| p-season-points-2012-40 | 16 | 16 | ok |
| p-season-rebounds-2004-20 | 20 | 20 | ok |
| p-season-rebounds-2025-16 | 61 | 61 | ok |
| p-season-threes-2018-7 | 52 | 52 | ok |
| p-season-threes-2012-6 | 44 | 44 | ok |
| p-shots-taken-38 | 26 | 26 | ok |
| p-steals-per-game-2 | 41 | 41 | ok |
| p-steals-playoff-6 | 37 | 37 | ok |
| p-steals-team-20 | 19 | 19 | ok |
| p-teammate-3468 | 209 | 209 | ok |
| p-teammate-3133628 | 115 | 115 | ok |
| p-threes-11 | 21 | 21 | ok |
| p-threes-finals-6 | 21 | 21 | ok |
| p-threes-in-season-2004-14 | 8 | 8 | ok |
| p-threes-in-season-2016-17 | 16 | 16 | ok |
| p-threes-playoff-7 | 83 | 83 | ok |
| p-threes-team-28 | 5 | 5 | ok |
| p-triple-double-regular | 248 | 248 | ok |
| p-turnovers-10 | 52 | 52 | ok |
| p-win-margin-50 | 21 | 21 | ok |
| p-win-margin-playoff-40 | 11 | 11 | ok |
| p-win-streak-18 | 8 | 8 | ok |
| p-wins-in-season-2015-40 | 16 | 16 | ok |
| p-wins-in-season-2021-45 | 7 | 7 | ok |
| p-wins-playoff-15 | 14 | 14 | ok |
| p-wins-season-65 | 9 | 9 | ok |

</details>

## 25 random prompts (seed 2026)

### p-points-against-30-45 (dive 8, prompt 4)

> Since 2001-02 (through 2025-26), name a player who scored 45 or more points against the Charlotte Hornets (including its time as the Bobcats) in a game.

- medium; 18 valid answers; tiers: 1: 17, 2: 1
- Best known: LeBron James (1), James Harden (1), Dwight Howard (1)
- Rarest: Cooper Flagg (2), DeMarcus Cousins (1), Zach LaVine (1)

### p-beat-in-playoffs-15 (dive 9, prompt 5)

> Since 2001-02 (through 2025-26), name a team that won a playoff game against the Milwaukee Bucks.

- medium; 10 valid answers; tiers: 1: 10
- Best known: Atlanta Hawks (1), Boston Celtics (1), Brooklyn Nets (1)
- Rarest: Toronto Raptors (1), Phoenix Suns (1), Orlando Magic (1)

### p-beat-in-playoffs-8 (dive 17, prompt 3)

> Since 2001-02 (through 2025-26), name a team that won a playoff game against the Detroit Pistons.

- medium; 13 valid answers; tiers: 1: 12, 4: 1
- Best known: Boston Celtics (1), Chicago Bulls (1), Cleveland Cavaliers (1)
- Rarest: Brooklyn Nets (4), Toronto Raptors (1), San Antonio Spurs (1)

### p-playoff-wins-in-season-2016-4 (dive 24, prompt 3)

> Since 2001-02 (through 2025-26), name a team that won 4 or more playoff games in the 2015-16 postseason.

- medium; 8 valid answers; tiers: 1: 8
- Best known: Atlanta Hawks (1), Cleveland Cavaliers (1), Golden State Warriors (1)
- Rarest: Toronto Raptors (1), San Antonio Spurs (1), Portland Trail Blazers (1)

### p-month-threes-2016-4-5 (dive 31, prompt 6)

> Since 2001-02 (through 2025-26), name a player who made 5 or more three-pointers in a regular-season game in April 2016.

- hard; 34 valid answers; tiers: 1: 9, 2: 12, 3: 9, 4: 4
- Best known: James Harden (1), Kevin Durant (1), Kobe Bryant (1)
- Rarest: Hollis Thompson (4), Troy Daniels (4), Isaiah Canaan (2014-2019) (4)

### p-season-rebounds-2026-20 (dive 36, prompt 7)

> Since 2001-02 (through 2025-26), name a player who grabbed 20 or more rebounds in a regular-season game in the 2025-26 season.

- hard; 19 valid answers; tiers: 1: 5, 2: 5, 3: 3, 4: 3, 5: 3
- Best known: Andre Drummond (1), Giannis Antetokounmpo (1), Nikola Jokic (1)
- Rarest: Julian Reese (5), Moussa Cisse (5), Oscar Tshiebwe (5)

### p-teammate-4278073 (dive 37, prompt 6)

> Since 2001-02 (through 2025-26), name a player who played in the same game as Shai Gilgeous-Alexander for the same team.

- hard; 87 valid answers; tiers: 1: 7, 2: 16, 3: 18, 4: 23, 5: 16, 6: 7
- Best known: Chris Paul (1), Al Horford (1), Dennis Schroder (1)
- Rarest: Angel Delgado (6), Keyontae Johnson (6), Kevin Hervey (6)

### p-franchise-points-3-25 (dive 38, prompt 4)

> Since 2001-02 (through 2025-26), name a player who scored 25 or more points in a game for the New Orleans Pelicans (including its time as the Hornets).

- medium; 81 valid answers; tiers: 1: 17, 2: 25, 3: 29, 4: 9, 5: 1
- Best known: Chris Paul (1), Anthony Davis (1), Rajon Rondo (1)
- Rarest: Jamal Cain (5), Antonio Reeves (4), Kirk Snyder (4)

### p-franchise-regular-30 (dive 41, prompt 1)

> Since 2001-02 (through 2025-26), name a player who played for the Charlotte Hornets (including its time as the Bobcats) in a regular-season game.

- medium; 203 valid answers; tiers: 1: 18, 2: 43, 3: 48, 4: 50, 5: 29, 6: 15
- Best known: Dwight Howard (1), Tony Parker (1), Tyson Chandler (1)
- Rarest: Arnoldas Kulboka (6), Mike Tobey (6), Scottie Lewis (6)

### p-road-wins-in-season-2003-23 (dive 41, prompt 5)

> Since 2001-02 (through 2025-26), name a team that won 23 or more road games in the 2002-03 season.

- medium; 5 valid answers; tiers: 1: 5
- Best known: Dallas Mavericks (1), Philadelphia 76ers (1), Portland Trail Blazers (1)
- Rarest: San Antonio Spurs (1), Sacramento Kings (1), Portland Trail Blazers (1)

### p-both-franchises-5-10 (dive 42, prompt 7)

> Since 2001-02 (through 2025-26), name a player who played for both the Cleveland Cavaliers and the Houston Rockets.

- hard; 18 valid answers; tiers: 1: 3, 2: 4, 3: 4, 4: 6, 5: 1
- Best known: James Harden (1), Dennis Schroder (1), Jeff Green (1)
- Rarest: Brodric Thomas (5), Stephen Graham (4), Sam Dekker (4)

### p-month-threes-2015-10-4 (dive 44, prompt 7)

> Since 2001-02 (through 2025-26), name a player who made 4 or more three-pointers in a regular-season game in October 2015.

- medium; 18 valid answers; tiers: 1: 7, 2: 6, 3: 4, 4: 1
- Best known: Stephen Curry (1), Carmelo Anthony (1), Mike Conley (1)
- Rarest: Isaiah Canaan (2014-2019) (4), Langston Galloway (3), Nikola Mirotic (3)

### p-franchise-points-13-35 (dive 46, prompt 4)

> Since 2001-02 (through 2025-26), name a player who scored 35 or more points in a game for the Los Angeles Lakers.

- medium; 23 valid answers; tiers: 1: 12, 2: 7, 3: 3, 4: 1
- Best known: LeBron James (1), Dwight Howard (1), Kobe Bryant (1)
- Rarest: Dalton Knecht (4), Talen Horton-Tucker (3), Rui Hachimura (3)

### p-home-wins-in-season-2007-30 (dive 48, prompt 3)

> Since 2001-02 (through 2025-26), name a team that won 30 or more home games in the 2006-07 season.

- medium; 8 valid answers; tiers: 1: 8
- Best known: Chicago Bulls (1), Cleveland Cavaliers (1), Dallas Mavericks (1)
- Rarest: Utah Jazz (1), Toronto Raptors (1), San Antonio Spurs (1)

### p-season-threes-2016-8 (dive 54, prompt 4)

> Since 2001-02 (through 2025-26), name a player who made 8 or more three-pointers in a regular-season game in the 2015-16 season.

- medium; 15 valid answers; tiers: 1: 7, 2: 4, 3: 3, 4: 1
- Best known: Stephen Curry (1), Damian Lillard (1), Paul George (1)
- Rarest: Troy Daniels (4), Rodney Hood (3), Omri Casspi (3)

### p-both-franchises-18-26 (dive 55, prompt 7)

> Since 2001-02 (through 2025-26), name a player who played for both the New York Knicks and the Utah Jazz.

- hard; 16 valid answers; tiers: 1: 1, 2: 4, 3: 6, 4: 3, 5: 2
- Best known: Enes Freedom (1), Jordan Clarkson (2), Bojan Bogdanovic (2)
- Rarest: Toure' Murry (5), Norvel Pelle (5), Steve Novak (4)

### p-teammate-3244 (dive 57, prompt 2)

> Since 2001-02 (through 2025-26), name a player who played in the same game as Thaddeus Young for the same team.

- medium; 220 valid answers; tiers: 1: 34, 2: 45, 3: 51, 4: 52, 5: 27, 6: 11
- Best known: Kevin Durant (1), Allen Iverson (1), Brook Lopez (1)
- Rarest: Trey McKinney-Jones (6), Ben Moore (6), Darius Johnson-Odom (6)

### p-month-threes-2015-3-6 (dive 57, prompt 4)

> Since 2001-02 (through 2025-26), name a player who made 6 or more three-pointers in a regular-season game in March 2015.

- medium; 21 valid answers; tiers: 1: 7, 2: 11, 3: 1, 4: 2
- Best known: James Harden (1), Stephen Curry (1), Damian Lillard (1)
- Rarest: Alexey Shved (4), Isaiah Canaan (2014-2019) (4), Anthony Morrow (3)

### p-season-rebounds-2016-20 (dive 57, prompt 6)

> Since 2001-02 (through 2025-26), name a player who grabbed 20 or more rebounds in a regular-season game in the 2015-16 season.

- medium; 17 valid answers; tiers: 1: 12, 2: 4, 3: 1
- Best known: Dwight Howard (1), Anthony Davis (1), Andre Drummond (1)
- Rarest: Jared Sullinger (3), Kenneth Faried (2), Robin Lopez (2)

### p-wins-in-season-2025-45 (dive 58, prompt 3)

> Since 2001-02 (through 2025-26), name a team that won 45 or more regular-season games in the 2024-25 season.

- easy; 13 valid answers; tiers: 1: 13
- Best known: Boston Celtics (1), Cleveland Cavaliers (1), Denver Nuggets (1)
- Rarest: Oklahoma City Thunder (1), New York Knicks (1), Minnesota Timberwolves (1)

### p-played-playoff-against-20 (dive 62, prompt 5)

> Since 2001-02 (through 2025-26), name a team that played a playoff game against the Philadelphia 76ers.

- hard; 11 valid answers; tiers: 1: 10, 4: 1
- Best known: Atlanta Hawks (1), Boston Celtics (1), Brooklyn Nets (1)
- Rarest: New Orleans Pelicans (4), Washington Wizards (1), Toronto Raptors (1)

### p-franchise-playoff-season-21-2021 (dive 63, prompt 7)

> Since 2001-02 (through 2025-26), name a player who played for the Phoenix Suns in a playoff game in the 2020-21 season.

- hard; 16 valid answers; tiers: 1: 2, 2: 5, 3: 7, 4: 1, 6: 1
- Best known: Chris Paul (1), Devin Booker (1), Deandre Ayton (2)
- Rarest: Ty-Shon Alexander (6), Abdel Nader (4), Frank Kaminsky (3)

### p-margin-in-season-2002-40 (dive 65, prompt 5)

> Since 2001-02 (through 2025-26), name a team that won a game by 40 or more points in the 2001-02 season.

- hard; 6 valid answers; tiers: 1: 4, 4: 2
- Best known: Los Angeles Lakers (1), Minnesota Timberwolves (1), Orlando Magic (1)
- Rarest: New Orleans Pelicans (4), Brooklyn Nets (4), Utah Jazz (1)

### p-free-throws-22 (dive 66, prompt 4)

> Since 2001-02 (through 2025-26), name a player who made 22 or more free throws in a game.

- medium; 21 valid answers; tiers: 1: 21
- Best known: LeBron James (1), James Harden (1), Dwight Howard (1)
- Rarest: Bam Adebayo (1), Kevin Martin (1), Jimmy Butler III (1)

### p-held-opponent-in-season-2011-70 (dive 70, prompt 5)

> Since 2001-02 (through 2025-26), name a team that held an opponent to 70 or fewer points in a game in the 2010-11 season.

- hard; 7 valid answers; tiers: 1: 6, 4: 1
- Best known: Boston Celtics (1), Los Angeles Lakers (1), Memphis Grizzlies (1)
- Rarest: New Orleans Pelicans (4), Portland Trail Blazers (1), Philadelphia 76ers (1)
