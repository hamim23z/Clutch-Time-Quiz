# Prompts sample and checks

Written by `python3 pipeline/export.py`; do not edit by hand. Tiers are in brackets: 1 is the best-known answer (10 points), 6 the rarest (100 points).

## File sizes

| file | bytes | gzipped (what a static host sends) |
|---|---|---|
| prompts.json | 300,509 | 38,482 |
| universe.json | 143,359 | 29,262 |
| both files | 443,868 | 67,744 |

## Recheck of 10 random prompts against the processed tables

10 of 10 match. Each prompt's valid answers were recomputed from the raw rows by a separately written brute-force query (`pipeline/bruteforce.py`) and compared with the exported answers, and the tiers and points were rechecked.

| prompt | valid answers (brute force) | exported answers | missing | extra | tier problems | result |
|---|---|---|---|---|---|---|
| p-points-regular-40 | 263 | 263 | 0 | 0 | 0 | ok |
| p-blocks-playoff-7 | 21 | 21 | 0 | 0 | 0 | ok |
| p-win-streak-16 | 13 | 13 | 0 | 0 | 0 | ok |
| p-losses-season-67 | 8 | 8 | 0 | 0 | 0 | ok |
| p-assists-20 | 27 | 27 | 0 | 0 | 0 | ok |
| p-franchises-9 | 35 | 35 | 0 | 0 | 0 | ok |
| p-points-bench-40 | 35 | 35 | 0 | 0 | 0 | ok |
| p-minutes-55 | 84 | 84 | 0 | 0 | 0 | ok |
| p-points-game7-35 | 23 | 23 | 0 | 0 | 0 | ok |
| p-champion | 13 | 13 | 0 | 0 | 0 | ok |

## 20 random prompts (seed 2026)

### p-points-bench-40 (dive 1, prompt 7)

> Since 2001-02 (through 2025-26), name a player who scored 40 or more points in a game he did not start.

- hard; 35 valid answers; tiers: 1: 13, 2: 14, 3: 6, 4: 2
- Best known: LeBron James (1), James Harden (1), Kobe Bryant (1)
- Rarest: Rodrigue Beaubois (4), Malachi Flynn (4), Jordan Crawford (3)

### p-points-regular-40 (dive 2, prompt 1)

> Since 2001-02 (through 2025-26), name a player who scored 40 or more points in a regular-season game.

- easy; 263 valid answers; tiers: 1: 126, 2: 105, 3: 29, 4: 2, 5: 1
- Best known: LeBron James (1), James Harden (1), Dwight Howard (1)
- Rarest: Kenneth Lofton Jr. (5), Rodrigue Beaubois (4), Malachi Flynn (4)

### p-minutes-55 (dive 3, prompt 1)

> Since 2001-02 (through 2025-26), name a player who played 55 or more minutes in a game.

- easy; 84 valid answers; tiers: 1: 53, 2: 26, 3: 5
- Best known: LeBron James (1), Kevin Durant (1), Pau Gasol (1)
- Rarest: Kerry Kittles (3), David Wesley (3), Raja Bell (3)

### p-franchises-6 (dive 3, prompt 2)

> Since 2001-02 (through 2025-26), name a player who played for 6 or more different franchises.

- medium; 284 valid answers; tiers: 1: 46, 2: 102, 3: 88, 4: 43, 5: 5
- Best known: James Harden (1), Dwight Howard (1), Chris Paul (1)
- Rarest: Jared Cunningham (5), Bobby Jones (5), Anthony Goldwire (5)

### p-blocks-playoff-7 (dive 3, prompt 7)

> Since 2001-02 (through 2025-26), name a player who blocked 7 or more shots in a playoff game.

- hard; 21 valid answers; tiers: 1: 13, 2: 4, 3: 3, 4: 1
- Best known: Dwight Howard (1), Tim Duncan (1), Ben Wallace (1)
- Rarest: Zach Edey (4), Luke Kornet (3), Isaiah Stewart (3)

### p-shots-taken-38 (dive 4, prompt 6)

> Since 2001-02 (through 2025-26), name a player who took 38 or more shots from the field in a game.

- medium; 26 valid answers; tiers: 1: 25, 2: 1
- Best known: LeBron James (1), James Harden (1), Kobe Bryant (1)
- Rarest: Dejounte Murray (2), Michael Jordan (1), Bam Adebayo (1)

### p-points-playoff-25 (dive 5, prompt 1)

> Since 2001-02 (through 2025-26), name a player who scored 25 or more points in a playoff game.

- easy; 330 valid answers; tiers: 1: 154, 2: 106, 3: 68, 4: 2
- Best known: LeBron James (1), James Harden (1), Dwight Howard (1)
- Rarest: Timothe Luwawu-Cabarrot (4), Scotty Pippen Jr. (4), Steve Smith (3)

### p-threes-playoff-8 (dive 5, prompt 4)

> Since 2001-02 (through 2025-26), name a player who made 8 or more three-pointers in a playoff game.

- medium; 32 valid answers; tiers: 1: 16, 2: 11, 3: 5
- Best known: Chris Paul (1), Stephen Curry (1), Damian Lillard (1)
- Rarest: Aaron Nesmith (3), Maxi Kleber (3), Duncan Robinson (3)

### p-win-streak-16 (dive 5, prompt 5)

> Since 2001-02 (through 2025-26), name a team that won 16 or more regular-season games in a row.

- easy; 13 valid answers; tiers: 1: 13
- Best known: Atlanta Hawks (1), Boston Celtics (1), Cleveland Cavaliers (1)
- Rarest: San Antonio Spurs (1), Phoenix Suns (1), Philadelphia 76ers (1)

### p-double-double-average (dive 6, prompt 1)

> Since 2001-02 (through 2025-26), name a player who averaged a double-double (10 or more points and 10 or more rebounds per game) in a regular season (minimum 40 games).

- easy; 79 valid answers; tiers: 1: 48, 2: 26, 3: 5
- Best known: Dwight Howard (1), Tim Duncan (1), Russell Westbrook (1)
- Rarest: Donovan Clingan (3), Danny Fortson (3), Walker Kessler (3)

### p-steals-playoff-6 (dive 6, prompt 2)

> Since 2001-02 (through 2025-26), name a player who stole the ball 6 or more times in a playoff game.

- medium; 37 valid answers; tiers: 1: 24, 2: 6, 3: 7
- Best known: LeBron James (1), James Harden (1), Russell Westbrook (1)
- Rarest: Dylan Harper (3), Javonte Green (3), Toni Kukoc (3)

### p-overtime-wins-3 (dive 6, prompt 3)

> Since 2001-02 (through 2025-26), name a team that won a game that went to 3 or more overtimes.

- easy; 22 valid answers; tiers: 1: 21, 4: 1
- Best known: Atlanta Hawks (1), Boston Celtics (1), Brooklyn Nets (1)
- Rarest: Charlotte Hornets (4), Washington Wizards (1), Utah Jazz (1)

### p-points-game7-35 (dive 6, prompt 4)

> Since 2001-02 (through 2025-26), name a player who scored 35 or more points in a Game 7.

- medium; 23 valid answers; tiers: 1: 22, 3: 1
- Best known: LeBron James (1), Kevin Durant (1), Tim Duncan (1)
- Rarest: Donte DiVincenzo (3), Jamal Murray (1), Paolo Banchero (1)

### p-champion (dive 6, prompt 5)

> Since 2001-02 (through 2025-26), name a team that won the NBA championship.

- easy; 13 valid answers; tiers: 1: 13
- Best known: Boston Celtics (1), Cleveland Cavaliers (1), Dallas Mavericks (1)
- Rarest: Toronto Raptors (1), San Antonio Spurs (1), Oklahoma City Thunder (1)

### p-assists-20 (dive 6, prompt 7)

> Since 2001-02 (through 2025-26), name a player who recorded 20 or more assists in a game.

- hard; 27 valid answers; tiers: 1: 16, 2: 8, 3: 2, 4: 1
- Best known: James Harden (1), Chris Paul (1), Russell Westbrook (1)
- Rarest: Ryan Nembhard (4), Isaiah Collier (3), Will Bynum (3)

### p-points-any-game-160 (dive 7, prompt 5)

> Since 2001-02 (through 2025-26), name a team that scored 160 or more points in a game, overtime included.

- medium; 7 valid answers; tiers: 1: 7
- Best known: Atlanta Hawks (1), Chicago Bulls (1), Denver Nuggets (1)
- Rarest: Sacramento Kings (1), Phoenix Suns (1), LA Clippers (1)

### p-triple-double-playoff (dive 8, prompt 2)

> Since 2001-02 (through 2025-26), name a player who recorded a triple-double in a playoff game.

- easy; 42 valid answers; tiers: 1: 35, 2: 7
- Best known: LeBron James (1), James Harden (1), Kevin Durant (1)
- Rarest: Andrew Bynum (2), Josh Hart (2), Steve Francis (2)

### p-offensive-rebounds-11 (dive 8, prompt 4)

> Since 2001-02 (through 2025-26), name a player who grabbed 11 or more offensive rebounds in a game.

- medium; 84 valid answers; tiers: 1: 37, 2: 30, 3: 12, 4: 4, 6: 1
- Best known: Dwight Howard (1), Tim Duncan (1), Pau Gasol (1)
- Rarest: Alex Stepheson (6), Zendon Hamilton (4), Greg Oden (4)

### p-franchises-9 (dive 8, prompt 7)

> Since 2001-02 (through 2025-26), name a player who played for 9 or more different franchises.

- hard; 35 valid answers; tiers: 1: 10, 2: 14, 3: 8, 4: 3
- Best known: Rajon Rondo (1), Andre Miller (1), Isaiah Thomas (1)
- Rarest: Steve Novak (4), Ryan Hollins (4), James Ennis III (4)

### p-losses-season-67 (dive 9, prompt 5)

> Since 2001-02 (through 2025-26), name a team that lost 67 or more regular-season games in a season.

- hard; 8 valid answers; tiers: 1: 7, 4: 1
- Best known: Atlanta Hawks (1), Detroit Pistons (1), Miami Heat (1)
- Rarest: Brooklyn Nets (4), Washington Wizards (1), Philadelphia 76ers (1)
