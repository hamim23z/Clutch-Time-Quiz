# Pipeline notes

Written by `python3 pipeline/run.py`; do not edit by hand. Rules and sources are in `docs/data-source-boxscores.md`.

## Run summary

Seasons processed: 2002-2026 (25 seasons; season 2002 means 2001-02).

| table | rows |
|---|---|
| players | 2,520 |
| teams | 30 |
| games | 32,123 |
| player_games | 667,293 |
| team_games | 64,246 |
| officials | 95,290 |

## Game selection

Kept games by season type:

| season type | games |
|---|---|
| playoffs | 2,084 |
| regular | 30,039 |

Games dropped before the box scores (not counted as skipped):

| reason | games |
|---|---|
| postponed or not final | 67 |
| All-Star game | 24 |
| NBA Cup final | 3 |
| play-in game | 37 |
| exhibition with a non-NBA side (Rising Stars, USA, World, All-Star teams) | 9 |
| other game type | 0 |

Play-in games are excluded: only regular-season and playoff games are kept. The spike reported 27 games without player rows and 14 without team rows. The 27 are the games skipped below (8 of them also lack team rows, and no game lacks only team rows). The other 6 of the spike's 14 are 2021 play-in games, which are excluded as play-in.

### Skipped games: 27

Regular-season or playoff games with no usable box score rows. They are left out of every table.

**no player rows (no row with a points value): 19**

- 2005: 250126028, 250322010
- 2006: 251105011, 251120013, 251204025, 251210011, 251216011, 251225014, 251227014, 260111011, 260120014, 260126014, 260327014, 260411014, 260516014
- 2007: 261223014, 261225014
- 2011: 301222012
- 2019: 401070917

**no team rows: 0**

**no team rows and no player rows: 8**

- 2013: 400278127, 400278386, 400278387, 400278388, 400278389
- 2014: 400489088
- 2017: 400900132
- 2018: 400975285

Counts by reason in total: no_player_rows = 19, no_team_rows = 0, no_team_and_player_rows = 8

## Played or not

A player counts as having played only if the `points` value is present. `did_not_play` is not used (it is almost never set in 2006-2012). 667,293 player-game rows are kept. Stat lines with no athlete id are dropped.

## Players

2,520 players, one record per athlete id. Ids are never merged.

**Display names that changed over time: 6 players** (all kept as spelling variants):

- id 6430: Jimmy Butler III, Jimmy Butler
- id 2528779: Reggie Bullock Jr., Reggie Bullock
- id 3059409: Nigel Hayes-Davis, Nigel Hayes
- id 3064291: Rondae Hollis Jefferson, Rondae Hollis-Jefferson
- id 3934719: OG Anunoby, O.G. Anunoby
- id 4065836: Omari Rasulala Spellman, Omari Spellman

**Accented spellings kept as variants: 6 players** (from short names), for example Nene -> Nenê, Jose Calderon -> Calderón, Willy Hernangomez -> Hernangómez, Dennis Schroder -> Schröder, Cristiano Felicio -> Felício.

**Display names shared by more than one athlete id: 12.** They stay separate records, each with a `unique_name`:

- id 932 = Brandon Williams (2003); id 4397040 = Brandon Williams (2022-2026)
- id 4400 = Chris Johnson (2011-2013); id 2325975 = Chris Johnson (2013-2016)
- id 6501 = Chris Wright (2012-2014); id 6666 = Chris Wright (2013)
- id 3191 = Corey Brewer (2008-2020); id 4415554 = Corey Brewer (2019)
- id 4066243 = Daryl Macon (2019-2020); id 4610145 = Daryl Macon (2020)
- id 97 = Dee Brown (2002); id 2994 = Dee Brown (2007-2009)
- id 2490589 = Isaiah Canaan (2014-2019); id 4412182 = Isaiah Canaan (2019)
- id 3039 = Marcus Williams (2007-2010); id 3240 = Marcus Williams (2008-2009)
- id 1051 = Mike James (2002-2014); id 2528096 = Mike James (2018-2021)
- id 2489010 = Tony Mitchell (2014, id 2489010); id 2583664 = Tony Mitchell (2014, id 2583664)
- id 3934620 = Trevon Scott (2026); id 4711005 = Trevon Scott (2022)
- id 3059316 = Wayne Selden (2017-2019); id 4895499 = Wayne Selden (2022)

**Aliases applied from `pipeline/data/aliases.csv`: 52 players.**

- Metta World Peace (id 25): Ron Artest, Metta Artest, Metta Sandiford-Artest, Metta Sandiford Artest
- Chauncey Billups (id 63): Mr. Big Shot
- Kobe Bryant (id 110): Black Mamba, Mamba
- Vince Carter (id 136): Vinsanity, Air Canada
- Tim Duncan (id 215): The Big Fundamental, Big Fundamental
- Kevin Garnett (id 261): KG
- Manu Ginobili (id 272): Manu
- Richard Hamilton (id 294): Rip Hamilton
- Robert Horry (id 347): Big Shot Bob
- Allen Iverson (id 366): The Answer
- Jason Kidd (id 429): J-Kidd
- Andrei Kirilenko (id 434): AK-47
- Tracy McGrady (id 532): T-Mac
- Dirk Nowitzki (id 609): Dirk
- Shaquille O'Neal (id 614): Shaq, Shaq O'Neal, Diesel
- Paul Pierce (id 662): The Truth
- Rasheed Wallace (id 883): Sheed
- Ben Wallace (id 885): Big Ben
- Gilbert Arenas (id 974): Agent Zero
- Michael Jordan (id 1035): MJ, Air Jordan, His Airness
- Nene (id 1713): Nene Hilario
- Yao Ming (id 1722): Yao
- Amar'e Stoudemire (id 1727): STAT
- LeBron James (id 1966): King James, LBJ, Bron
- Dwyane Wade (id 1987): D-Wade, Dwayne Wade, Flash
- Dwight Howard (id 2384): D12
- Chris Paul (id 2779): CP3, The Point God
- Lou Williams (id 2799): Sweet Lou
- Kevin Durant (id 3202): KD, Slim Reaper
- Nicolas Batum (id 3416): Nic Batum
- Derrick Rose (id 3456): D-Rose
- Russell Westbrook (id 3468): Russ, Brodie
- Patrick Beverley (id 3964): Pat Bev
- Stephen Curry (id 3975): Steph Curry, Chef Curry
- James Harden (id 3992): The Beard
- Jrue Holiday (id 3995): Jrue
- Paul George (id 4251): PG13, Playoff P
- DeMarcus Cousins (id 4258): Boogie Cousins, Boogie
- Jimmy Butler III (id 6430): Jimmy Buckets
- Enes Freedom (id 6447): Enes Kanter
- Kawhi Leonard (id 6450): The Claw
- Anthony Davis (id 6583): AD
- Draymond Green (id 6589): Dray
- Damian Lillard (id 6606): Dame, Dame Lillard
- Giannis Antetokounmpo (id 3032977): Giannis, Greek Freak, The Greek Freak
- Nikola Jokic (id 3112335): Joker, The Joker
- Karl-Anthony Towns (id 3136195): KAT
- Donovan Mitchell (id 3908809): Spida, Spida Mitchell
- Shai Gilgeous-Alexander (id 4278073): SGA
- Zion Williamson (id 4395628): Zion
- Anthony Edwards (id 4594268): Ant-Man, Ant Edwards
- Victor Wembanyama (id 5104157): Wemby

Ron Artest is not in `aliases.csv` on purpose. The data only knows this player as Metta World Peace (athlete id 25, 2002-2017) and the name Artest appears nowhere in it, so the rename cannot be confirmed from the data. Add it by hand if you want it.

## Teams

30 franchises (ESPN team ids 1-30; the 14 non-NBA sides in the team box all have ids above 30). Franchises with more than one name:

- id 3: Charlotte Hornets (CHA) 2002-2002; New Orleans Hornets (NO) 2003-2013; NO/Oklahoma City Hornets (NO) 2006-2007; New Orleans Pelicans (NO) 2014-2026
- id 17: New Jersey Nets (NJ) 2002-2012; Brooklyn Nets (BKN) 2013-2026
- id 25: Seattle SuperSonics (SEA) 2002-2008; Oklahoma City Thunder (OKC) 2009-2026
- id 30: Charlotte Bobcats (CHA) 2005-2014; Charlotte Hornets (CHA) 2015-2026

## Officials

The data has names only: no ids and no crew chief (every row is a referee). Slot = `official_order`.

**Name merges: 5** (spellings folded into another spelling of the same person), across 4 people:

- **J.T. Orr** <- JT Orr (2 games, 2019-2020)
  - evidence: `J.T. Orr` and `JT Orr` appear in the same game in the same slot 1 times and in different slots 1 times
- **JD Ralls** <- J.D. Ralls (45 games, 2024-2025)
  - evidence: `J.D. Ralls` and `JD Ralls` appear in the same game in the same slot 0 times and in different slots 0 times
- **Joe DeRosa** <- J.B. DeRosa (410 games, 2018-2026); JB DeRosa (97 games, 2018-2020)
  - evidence: `J.B. DeRosa` and `JB DeRosa` appear in the same game in the same slot 0 times and in different slots 0 times
  - evidence: `J.B. DeRosa` and `Joe DeRosa` appear in the same game in the same slot 0 times and in different slots 0 times
  - evidence: `JB DeRosa` and `Joe DeRosa` appear in the same game in the same slot 0 times and in different slots 0 times
- **Steven Anderson** <- Steve Anderson (49 games, 2012-2017)
  - evidence: `Steve Anderson` and `Steven Anderson` appear in the same game in the same slot 17 times and in different slots 8 times

Whitespace-only fixes (not counted as merges): 1 spellings.

- 'Nate  Green' -> Nate Green (36 rows)

Look alike but **not** merged (different first names, or seen as two people in the same game), for review:

- Jacyn Goble / John Goble

**Slot conflicts:** 216 games have two different names in one slot in the raw data (2014-2020). The spike counted 219 over every game type; the difference is exhibition games, which are dropped. All of them are flagged: `officials_status = slot_conflict` on the game and `slot_conflict = True` on its rows, and every raw spelling is kept in `raw_name`. In 18 of them the two names turn out to be one person (spellings merged, or the same person listed twice), so 198 games still have two different people in one slot (`slot_shared = True` on those rows).

Cleanup: 18 duplicate rows for the same person in the same slot and 73 rows listing the same person in a second slot were removed.
Games with more than 3 officials listed: 385. Games with no officials: 438.

Games with no officials, by season (the data has none for any 2009, 2010 or 2011 playoff game, and few regular-season gaps):

| season | regular | playoffs |
|---|---|---|
| 2004 | 1 | 0 |
| 2009 | 8 | 85 |
| 2010 | 0 | 82 |
| 2011 | 93 | 81 |
| 2014 | 2 | 0 |
| 2015 | 1 | 0 |
| 2018 | 1 | 0 |
| 2021 | 34 | 2 |
| 2022 | 14 | 0 |
| 2023 | 12 | 4 |
| 2024 | 18 | 0 |
