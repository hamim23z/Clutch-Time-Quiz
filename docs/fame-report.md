# Fame report

Written by `python3 pipeline/generate.py`; do not edit by hand (the review notes at the end come from `pipeline/data/fame-review.md`).

## How the fame score works

- **Population:** 2,520 players with at least one game with a points value (2001-02 to the last season in the data).
- **Five metrics:** career points (regular season plus playoffs), career rebounds, career assists, career steals plus blocks, and best single-season points per game (regular season only, at least 40 games that season, games for all teams added up).
- **Ranks:** each metric is ranked across all players (rank 1 = most famous; ties share the better rank). A player's fame rank is the best (lowest) of the five, so a short-career star, a rebounder or a defender is not rated obscure. Players with no 40-game season have no points-per-game rank, and a career total of zero in rebounds, assists or steals plus blocks is not ranked. All percentiles divide by the same number of players, so they are on the same scale.
- **Tier:** from the global percentile = fame rank / players: top 3% is tier 1 (10 points), 3 to 10% tier 2 (20), 10 to 25% tier 3 (35), 25 to 50% tier 4 (55), 50 to 75% tier 5 (75), the rest tier 6 (100). A player exactly on a cutoff gets the better-known tier.
- **Hand-set tiers:** `pipeline/data/fame_overrides.csv` sets the tier for players the metrics get clearly wrong (listed below). The percentile still shows what the metrics said.
- **Only games in the data count**, so a player whose career started before 2001-02 is judged on his later years only.

## Players per tier

| tier | points | percentile band | nominal share | nominal players | actual players | actual share |
|---|---|---|---|---|---|---|
| 1 | 10 | top 3% | 3% | 76 | 187 | 7.4% |
| 2 | 20 | 3 to 10% | 7% | 176 | 284 | 11.3% |
| 3 | 35 | 10 to 25% | 15% | 378 | 429 | 17.0% |
| 4 | 55 | 25 to 50% | 25% | 630 | 556 | 22.1% |
| 5 | 75 | 50 to 75% | 25% | 630 | 573 | 22.7% |
| 6 | 100 | bottom 25% | 25% | 630 | 491 | 19.5% |

The better-known tiers are fuller than the nominal shares (187 players in tier 1 against 76). That follows from the method: taking the best of five ranks lets a player in through any of five doors, so more players than the nominal share sit in the top bands (tiers 1 and 2 together: 471).

## The 40 most famous players

| # | player | career points | best points per game | fame percentile | tier | decided by |
|---|---|---|---|---|---|---|
| 1 | LeBron James | 51,932 | 31.4 (2006, 79 g) | 0.04% | 1 | career points |
| 2 | James Harden | 33,579 | 36.1 (2019, 78 g) | 0.04% | 1 | best points per game |
| 3 | Dwight Howard | 21,351 | 22.9 (2011, 78 g) | 0.04% | 1 | career rebounds |
| 4 | Kevin Durant | 37,572 | 32.0 (2014, 81 g) | 0.08% | 1 | career points |
| 5 | Kobe Bryant | 31,731 | 35.3 (2006, 78 g) | 0.08% | 1 | best points per game |
| 6 | Chris Paul | 26,039 | 22.8 (2009, 78 g) | 0.08% | 1 | career assists |
| 7 | Tim Duncan | 24,405 | 25.5 (2002, 82 g) | 0.08% | 1 | career steals + blocks |
| 8 | Russell Westbrook | 30,190 | 31.6 (2017, 81 g) | 0.12% | 1 | career assists |
| 9 | Luka Doncic | 16,718 | 33.9 (2024, 70 g) | 0.12% | 1 | best points per game |
| 10 | Pau Gasol | 22,974 | 20.8 (2007, 59 g) | 0.16% | 1 | career rebounds |
| 11 | Joel Embiid | 15,181 | 33.1 (2023, 66 g) | 0.16% | 1 | best points per game |
| 12 | Dirk Nowitzki | 31,359 | 26.6 (2006, 81 g) | 0.20% | 1 | career points |
| 13 | Kevin Garnett | 20,015 | 24.2 (2004, 82 g) | 0.20% | 1 | career rebounds |
| 14 | Steve Nash | 16,471 | 18.8 (2006, 78 g) | 0.20% | 1 | career assists |
| 15 | Allen Iverson | 16,212 | 33.1 (2006, 71 g) | 0.20% | 1 | best points per game |
| 16 | Ben Wallace | 5,772 | 9.7 (2005, 74 g) | 0.20% | 1 | career steals + blocks |
| 17 | Stephen Curry | 30,675 | 32.0 (2021, 63 g) | 0.24% | 1 | career points |
| 18 | Anthony Davis | 20,933 | 28.1 (2018, 75 g) | 0.24% | 1 | career steals + blocks |
| 19 | Shai Gilgeous-Alexander | 15,011 | 32.7 (2025, 76 g) | 0.24% | 1 | best points per game |
| 20 | Andre Drummond | 11,905 | 17.7 (2020, 57 g) | 0.24% | 1 | career rebounds |
| 21 | Rajon Rondo | 11,006 | 13.7 (2010, 81 g) | 0.24% | 1 | career assists |
| 22 | Damian Lillard | 24,303 | 32.2 (2023, 58 g) | 0.28% | 1 | best points per game |
| 23 | Brook Lopez | 19,403 | 20.6 (2016, 73 g) | 0.28% | 1 | career steals + blocks |
| 24 | Rudy Gobert | 12,404 | 15.9 (2019, 81 g) | 0.28% | 1 | career rebounds |
| 25 | Jason Kidd | 12,347 | 18.7 (2003, 80 g) | 0.28% | 1 | career assists |
| 26 | Carmelo Anthony | 30,158 | 28.9 (2007, 65 g) | 0.32% | 1 | career points |
| 27 | Tony Parker | 23,480 | 22.0 (2009, 72 g) | 0.32% | 1 | career assists |
| 28 | Tracy McGrady | 15,092 | 32.1 (2003, 75 g) | 0.32% | 1 | best points per game |
| 29 | Josh Smith | 14,061 | 18.8 (2012, 66 g) | 0.32% | 1 | career steals + blocks |
| 30 | DeAndre Jordan | 10,105 | 12.7 (2016, 77 g) | 0.32% | 1 | career rebounds |
| 31 | DeMar DeRozan | 28,086 | 27.9 (2022, 76 g) | 0.36% | 1 | career points |
| 32 | Kyle Lowry | 18,204 | 22.4 (2017, 60 g) | 0.36% | 1 | career assists |
| 33 | Dwyane Wade | 26,847 | 30.2 (2009, 79 g) | 0.40% | 1 | career points |
| 34 | Tyson Chandler | 10,026 | 11.8 (2008, 79 g) | 0.40% | 1 | career rebounds |
| 35 | Nikola Vucevic | 17,987 | 23.4 (2021, 70 g) | 0.44% | 1 | career rebounds |
| 36 | Andre Miller | 14,926 | 17.0 (2008, 82 g) | 0.44% | 1 | career assists |
| 37 | Paul Pierce | 25,288 | 26.8 (2006, 79 g) | 0.48% | 1 | career points |
| 38 | Zach Randolph | 19,733 | 23.6 (2007, 68 g) | 0.48% | 1 | career rebounds |
| 39 | Mike Conley | 18,263 | 21.1 (2019, 70 g) | 0.48% | 1 | career assists |
| 40 | Shawn Marion | 17,158 | 21.9 (2006, 80 g) | 0.48% | 1 | career steals + blocks |

## Hand-set tiers

| player | metrics said | tier set | reason |
|---|---|---|---|
| Michael Jordan | 3.61% (tier 2) | 1 | Michael Jordan: all-time great, but only his last two seasons (2001-02 and 2002-03) are in the data. |
| Karl Malone | 4.21% (tier 2) | 1 | Karl Malone: Hall of Famer and second all-time scorer at his retirement; only 2001-02 to 2003-04 are in the data. |
| Reggie Miller | 11.90% (tier 3) | 2 | Reggie Miller: Hall of Famer and long-time three-point record holder; only 2001-02 to 2004-05 are in the data. |
| John Stockton | 12.70% (tier 3) | 2 | John Stockton: Hall of Famer and the all-time assists and steals leader; only 2001-02 and 2002-03 are in the data. |
| Scottie Pippen | 22.06% (tier 3) | 2 | Scottie Pippen: Hall of Famer and six-time champion; only 2001-02 to 2003-04 are in the data. |
| Patrick Ewing | 49.44% (tier 4) | 2 | Patrick Ewing: Hall of Famer; only his final season (2001-02, 69 games) is in the data. |

## 15 random players per tier (seed 2026)

### Tier 1 (10 points, top 3%): 187 players

| player | career points | best points per game | fame percentile |
|---|---|---|---|
| Chris Paul | 26,039 | 22.8 (2009, 78 g) | 0.08% |
| Ben Wallace | 5,772 | 9.7 (2005, 74 g) | 0.20% |
| Jason Kidd | 12,347 | 18.7 (2003, 80 g) | 0.28% |
| Deron Williams | 15,202 | 21.0 (2012, 55 g) | 0.52% |
| Jrue Holiday | 18,921 | 21.2 (2019, 67 g) | 0.56% |
| Nikola Jokic | 20,744 | 29.6 (2025, 70 g) | 0.60% |
| Draymond Green | 10,162 | 14.0 (2016, 81 g) | 0.71% |
| LaMarcus Aldridge | 22,023 | 23.4 (2015, 71 g) | 0.75% |
| Raymond Felton | 11,294 | 15.5 (2011, 75 g) | 1.15% |
| Jeff Teague | 11,049 | 16.5 (2014, 79 g) | 1.27% |
| David Lee | 11,452 | 20.2 (2010, 81 g) | 1.47% |
| Rasheed Wallace | 11,577 | 19.3 (2002, 79 g) | 2.10% |
| Nene | 11,746 | 14.6 (2009, 77 g) | 2.26% |
| Jason Richardson | 15,259 | 23.2 (2006, 75 g) | 2.86% |
| Reggie Evans | 3,454 | 5.6 (2006, 66 g) | 2.94% |

### Tier 2 (20 points, 3 to 10%): 284 players

| player | career points | best points per game | fame percentile |
|---|---|---|---|
| Kurt Thomas | 6,577 | 14.0 (2003, 81 g) | 3.57% |
| Larry Hughes | 8,273 | 22.0 (2005, 61 g) | 4.68% |
| Wesley Matthews | 11,847 | 16.4 (2014, 82 g) | 5.12% |
| Andrea Bargnani | 7,971 | 21.4 (2011, 66 g) | 5.28% |
| Mitchell Robinson | 3,235 | 9.7 (2020, 61 g) | 7.06% |
| Randy Foye | 7,850 | 16.3 (2009, 70 g) | 7.18% |
| Jeremy Lin | 5,747 | 13.4 (2013, 82 g) | 7.42% |
| T.J. Warren | 5,593 | 19.8 (2020, 67 g) | 7.54% |
| Greivis Vasquez | 3,733 | 13.9 (2013, 77 g) | 7.86% |
| Adonal Foyle | 1,935 | 5.4 (2003, 82 g) | 8.57% |
| Tony Battie | 3,632 | 7.9 (2006, 82 g) | 9.05% |
| JaMychal Green | 4,523 | 10.3 (2018, 55 g) | 9.13% |
| Chris Wilcox | 5,150 | 13.5 (2007, 82 g) | 9.52% |
| Luc Mbah a Moute | 4,562 | 9.9 (2015, 67 g) | 10.00% |
| Reggie Miller | 4,487 | 16.5 (2002, 79 g) | 11.90% |

### Tier 3 (35 points, 10 to 25%): 429 players

| player | career points | best points per game | fame percentile |
|---|---|---|---|
| Bennedict Mathurin | 4,506 | 17.6 (2026, 54 g) | 10.08% |
| Luke Walton | 3,013 | 11.4 (2007, 59 g) | 11.87% |
| Jason Maxiell | 3,644 | 7.9 (2008, 82 g) | 12.30% |
| Matt Bonner | 4,878 | 8.4 (2009, 79 g) | 13.21% |
| Nenad Krstic | 4,499 | 13.5 (2006, 80 g) | 13.97% |
| Eddie House | 5,334 | 9.9 (2006, 80 g) | 15.48% |
| Marquis Daniels | 4,595 | 13.6 (2009, 54 g) | 16.19% |
| Rondae Hollis Jefferson | 2,815 | 13.8 (2018, 67 g) | 17.62% |
| Josh Childress | 3,598 | 13.0 (2007, 55 g) | 18.69% |
| Luther Head | 2,878 | 10.9 (2007, 80 g) | 21.47% |
| Bub Carrington | 1,685 | 10.7 (2026, 82 g) | 21.87% |
| Frank Kaminsky | 3,702 | 11.7 (2017, 75 g) | 22.02% |
| Greg Buckner | 2,501 | 6.7 (2006, 73 g) | 22.62% |
| Matt Carroll | 3,017 | 12.1 (2007, 72 g) | 22.78% |
| Dahntay Jones | 3,583 | 10.2 (2010, 76 g) | 23.21% |

### Tier 4 (55 points, 25 to 50%): 556 players

| player | career points | best points per game | fame percentile |
|---|---|---|---|
| Isaiah Canaan (2014-2019) | 1,948 | 11.0 (2016, 77 g) | 26.51% |
| Facundo Campazzo | 831 | 6.1 (2021, 65 g) | 28.21% |
| Jake LaRavia | 1,642 | 8.2 (2026, 82 g) | 31.79% |
| Shawne Williams | 1,801 | 7.1 (2011, 64 g) | 31.90% |
| Duane Washington Jr. | 717 | 9.9 (2022, 48 g) | 31.98% |
| Tim Hardaway | 714 | 9.6 (2002, 68 g) | 33.69% |
| Rodney Carney | 1,808 | 7.3 (2009, 66 g) | 33.81% |
| Danny Wolf | 508 | 8.9 (2026, 57 g) | 36.59% |
| Solomon Jones | 857 | 4.0 (2010, 52 g) | 37.26% |
| Tom Gugliotta | 819 | 6.5 (2002, 44 g) | 38.13% |
| Rob Dillingham | 636 | 6.3 (2026, 65 g) | 39.96% |
| Earl Barron | 640 | 7.1 (2008, 46 g) | 43.93% |
| Terrance Ferguson | 958 | 6.9 (2019, 74 g) | 44.68% |
| Sion James | 441 | 5.4 (2026, 82 g) | 47.10% |
| Jeremy Pargo | 416 | 3.1 (2012, 41 g) | 47.78% |

### Tier 5 (75 points, 50 to 75%): 573 players

| player | career points | best points per game | fame percentile |
|---|---|---|---|
| T.J. Leaf | 485 | 3.9 (2019, 58 g) | 51.19% |
| Kam Jones | 162 | none | 51.79% |
| Lawrence Funderburke | 365 | 4.7 (2002, 56 g) | 52.06% |
| Jorge Gutierrez | 141 | none | 57.74% |
| Jahmai Mashack | 192 | none | 58.25% |
| Rob Kurz | 157 | 3.9 (2009, 40 g) | 58.57% |
| C.J. Williams | 248 | none | 58.85% |
| Justin Williams | 165 | none | 59.29% |
| Freddie Gillespie | 132 | none | 60.28% |
| David Duke Jr. | 233 | none | 63.49% |
| Chris Wright (2012-2014) | 116 | none | 64.88% |
| Willie Warren | 37 | none | 69.48% |
| Ray Spalding | 58 | none | 71.23% |
| Rakeem Christmas | 63 | none | 72.06% |
| Jack Cooley | 67 | none | 72.46% |

### Tier 6 (100 points, bottom 25%): 491 players

| player | career points | best points per game | fame percentile |
|---|---|---|---|
| Maozinha Pereira | 48 | none | 76.90% |
| RJ Nembhard Jr. | 15 | none | 77.98% |
| Carlik Jones | 24 | none | 79.05% |
| Billy Garrett Jr. | 26 | none | 82.86% |
| Elliot Perry | 11 | none | 82.86% |
| Taze Moore | 24 | none | 83.89% |
| Joe Chealey | 4 | none | 85.40% |
| Mangok Mathiang | 8 | none | 87.70% |
| Jameel Warney | 17 | none | 88.25% |
| Jack McVeigh | 14 | none | 88.77% |
| Jordan Ford | 12 | none | 90.40% |
| Javin DeLaurier | 0 | none | 91.03% |
| Charles Cooke | 6 | none | 91.03% |
| Coty Clarke | 6 | none | 93.69% |
| Arnoldas Kulboka | 0 | none | 97.66% |

## Sanity check on recognizable names

| player | why and what we expect | tier | fame percentile | career points | best points per game | verdict |
|---|---|---|---|---|---|---|
| LeBron James | all-time great; expect tier 1 or better | 1 | 0.04% | 51,932 | 31.4 (2006, 79 g) | ok |
| Kobe Bryant | all-time great; expect tier 1 or better | 1 | 0.08% | 31,731 | 35.3 (2006, 78 g) | ok |
| Tim Duncan | all-time great; expect tier 1 or better | 1 | 0.08% | 24,405 | 25.5 (2002, 82 g) | ok |
| Dirk Nowitzki | all-time great; expect tier 1 or better | 1 | 0.20% | 31,359 | 26.6 (2006, 81 g) | ok |
| Stephen Curry | superstar; expect tier 1 or better | 1 | 0.24% | 30,675 | 32.0 (2021, 63 g) | ok |
| Kevin Durant | superstar; expect tier 1 or better | 1 | 0.08% | 37,572 | 32.0 (2014, 81 g) | ok |
| Giannis Antetokounmpo | superstar; expect tier 1 or better | 1 | 0.56% | 23,801 | 31.1 (2023, 63 g) | ok |
| Nikola Jokic | superstar; expect tier 1 or better | 1 | 0.60% | 20,744 | 29.6 (2025, 70 g) | ok |
| Luka Doncic | young star; expect tier 1 or better | 1 | 0.12% | 16,718 | 33.9 (2024, 70 g) | ok |
| Shai Gilgeous-Alexander | young star; expect tier 1 or better | 1 | 0.24% | 15,011 | 32.7 (2025, 76 g) | ok |
| Victor Wembanyama | young star, few seasons; expect tier 2 or better | 1 | 2.38% | 4,762 | 25.0 (2026, 64 g) | ok |
| Anthony Edwards | young star; expect tier 2 or better | 1 | 0.87% | 12,200 | 28.8 (2026, 61 g) | ok |
| Cade Cunningham | young star; expect tier 2 or better | 1 | 1.75% | 6,663 | 26.1 (2025, 70 g) | ok |
| Jalen Brunson | young star; expect tier 2 or better | 1 | 0.91% | 12,988 | 28.7 (2024, 77 g) | ok |
| Paolo Banchero | young star; expect tier 2 or better | 1 | 1.87% | 6,551 | 25.9 (2025, 46 g) | ok |
| Chet Holmgren | young star, defensive; expect tier 2 or better | 3 | 10.63% | 3,746 | 17.1 (2026, 69 g) | **CHECK** |
| Cooper Flagg | rookie star, one season; expect tier 2 or better | 2 | 5.83% | 1,473 | 21.0 (2026, 70 g) | ok |
| Tyrese Haliburton | young star; expect tier 2 or better | 2 | 3.69% | 6,521 | 20.7 (2023, 56 g) | ok |
| Michael Jordan | most famous player ever, but only his last two seasons (2001-02 and 2002-03, Wizards) are in the data; expect tier 1 or better | 1 | 3.61% | 3,015 | 22.9 (2002, 60 g) | ok |
| Ben Wallace | four-time Defensive Player of the Year, scorer in name only; expect tier 2 or better | 1 | 0.20% | 5,772 | 9.7 (2005, 74 g) | ok |
| Brian Scalabrine | famous bench player: a deep-ish name; expect tier 4 or worse | 4 | 30.20% | 1,697 | 6.3 (2005, 54 g) | ok |
| Jason Kapono | role player; expect tier 3 or worse | 3 | 23.89% | 3,444 | 10.6 (2007, 65 g) | ok |

Names that did not come out as expected: Chet Holmgren (tier 3).

## Review notes

Written by hand after reading the numbers above (the rest of this file is generated).

**Fixed in session 5.** The score now takes the best of five ranks (career points, rebounds, assists, steals plus blocks, best points per game), so Ben Wallace (decided by steals plus blocks) moved from tier 3 to tier 1 and every other sanity name passes. Six Hall of Famers whose prime was before 2001-02 have hand-set tiers (table above): Michael Jordan and Karl Malone tier 1; John Stockton, Scottie Pippen, Reggie Miller and Patrick Ewing tier 2.

**Still wrong:**

- **Chet Holmgren is tier 3 (10.63%).** The sanity list expects tier 2 or better for a top-pick young defender. He has played few seasons (3,746 career points, 17.1 points per game at best) and none of the five metrics lifts him into the top 10%. I did not add an override because nothing in the data proves it; it needs an owner decision (add him to `fame_overrides.csv` if you agree).
- **Tier 1 is crowded: 187 players (7.4%) against a nominal 3%, and tiers 1 and 2 hold 471 (18.7%) against 10%.** Taking the best of five ranks lets a player in through any of five doors, including some who are very good at one counting stat but not household names (Andre Drummond, Josh Smith and Brook Lopez are all tier 1). The cutoffs were kept as asked. If the bands should be fuller or emptier, the cutoffs are the lever.
- **Players with a pre-2002 prime who are not in the override file are still judged on a partial career** (for example Alonzo Mourning, tier 3, whose data covers 2001-02 to 2007-08 only). I only overrode players where the gap is large and the name is beyond doubt.
- **Points per game is regular season only** (at least 40 games, games for all teams added up); career points include the playoffs.
- **Almost every valid answer is a star, so the rarity scoring has little to reward.** Across the 63 exported prompts there are 4,672 answers: 2,390 are tier 1 (51%), 1,328 tier 2 (28%), 717 tier 3 (15%), 213 tier 4 (4.6%), 20 tier 5 and 4 tier 6. A typical dive pays 10 to 20 points per answer and a deep cut worth 75 or 100 points is rare. Players who reach a stat threshold in a game are mostly well-known, and the best-of-five fame rank puts even more of them in the top bands. Of the 118 player candidates, 106 have fewer than 10% of their answers at tier 4 or above, none has 25% or more, and the highest is 19% (blocks, 6 or more). The levers are the tier cutoffs, the number of metrics in the fame score, or preferring prompts with long lists of modest players (steals per game, turnovers, minutes); the cutoffs were kept as asked.
