# Fame report

Written by `python3 pipeline/generate.py`; do not edit by hand (the review notes at the end come from `pipeline/data/fame-review.md`).

## How the fame score works

- **Population:** 2,520 players with at least one game with a points value (2001-02 to the last season in the data).
- **Two metrics:** career points (regular season plus playoffs), and best single-season points per game (regular season only, at least 40 games that season, games for all teams added up).
- **Ranks:** each metric is ranked across all players (rank 1 = most famous; ties share the better rank). A player's fame rank is the better (lower) of the two, so a short-career star is not rated obscure. Players with no 40-game season have no points-per-game rank and are ranked by career points alone. Both percentiles divide by the same number of players, so they are on the same scale.
- **Tier:** from the global percentile = fame rank / players: top 3% is tier 1 (10 points), 3 to 10% tier 2 (20), 10 to 25% tier 3 (35), 25 to 50% tier 4 (55), 50 to 75% tier 5 (75), the rest tier 6 (100). A player exactly on a cutoff gets the better-known tier.
- **Only games in the data count**, so a player whose career started before 2001-02 is judged on his later years only.

## Players per tier

| tier | points | percentile band | nominal share | nominal players | actual players | actual share |
|---|---|---|---|---|---|---|
| 1 | 10 | top 3% | 3% | 76 | 112 | 4.4% |
| 2 | 20 | 3 to 10% | 7% | 176 | 205 | 8.1% |
| 3 | 35 | 10 to 25% | 15% | 378 | 427 | 16.9% |
| 4 | 55 | 25 to 50% | 25% | 630 | 600 | 23.8% |
| 5 | 75 | 50 to 75% | 25% | 630 | 555 | 22.0% |
| 6 | 100 | bottom 25% | 25% | 630 | 621 | 24.6% |

The better-known tiers are fuller than the nominal shares (112 players in tier 1 against 76). That follows from the method: taking the better of two ranks lets a player in through either door, so up to twice as many players can sit in the top 3% (tier 1 and 2 together: 317).

## The 40 most famous players

| # | player | career points | best points per game | fame percentile | tier | decided by |
|---|---|---|---|---|---|---|
| 1 | LeBron James | 51,932 | 31.4 (2006, 79 g) | 0.04% | 1 | career |
| 2 | James Harden | 33,579 | 36.1 (2019, 78 g) | 0.04% | 1 | ppg |
| 3 | Kevin Durant | 37,572 | 32.0 (2014, 81 g) | 0.08% | 1 | career |
| 4 | Kobe Bryant | 31,731 | 35.3 (2006, 78 g) | 0.08% | 1 | ppg |
| 5 | Luka Doncic | 16,718 | 33.9 (2024, 70 g) | 0.12% | 1 | ppg |
| 6 | Joel Embiid | 15,181 | 33.1 (2023, 66 g) | 0.16% | 1 | ppg |
| 7 | Dirk Nowitzki | 31,359 | 26.6 (2006, 81 g) | 0.20% | 1 | career |
| 8 | Allen Iverson | 16,212 | 33.1 (2006, 71 g) | 0.20% | 1 | ppg |
| 9 | Stephen Curry | 30,675 | 32.0 (2021, 63 g) | 0.24% | 1 | career |
| 10 | Shai Gilgeous-Alexander | 15,011 | 32.7 (2025, 76 g) | 0.24% | 1 | ppg |
| 11 | Russell Westbrook | 30,190 | 31.6 (2017, 81 g) | 0.28% | 1 | career |
| 12 | Damian Lillard | 24,303 | 32.2 (2023, 58 g) | 0.28% | 1 | ppg |
| 13 | Carmelo Anthony | 30,158 | 28.9 (2007, 65 g) | 0.32% | 1 | career |
| 14 | Tracy McGrady | 15,092 | 32.1 (2003, 75 g) | 0.32% | 1 | ppg |
| 15 | DeMar DeRozan | 28,086 | 27.9 (2022, 76 g) | 0.36% | 1 | career |
| 16 | Dwyane Wade | 26,847 | 30.2 (2009, 79 g) | 0.40% | 1 | career |
| 17 | Chris Paul | 26,039 | 22.8 (2009, 78 g) | 0.44% | 1 | career |
| 18 | Paul Pierce | 25,288 | 26.8 (2006, 79 g) | 0.48% | 1 | career |
| 19 | Tim Duncan | 24,405 | 25.5 (2002, 82 g) | 0.52% | 1 | career |
| 20 | Bradley Beal | 18,429 | 31.3 (2021, 60 g) | 0.52% | 1 | ppg |
| 21 | Giannis Antetokounmpo | 23,801 | 31.1 (2023, 63 g) | 0.56% | 1 | ppg |
| 22 | Tony Parker | 23,480 | 22.0 (2009, 72 g) | 0.63% | 1 | career |
| 23 | Jayson Tatum | 17,199 | 30.1 (2023, 74 g) | 0.63% | 1 | ppg |
| 24 | Pau Gasol | 22,974 | 20.8 (2007, 59 g) | 0.67% | 1 | career |
| 25 | Trae Young | 13,202 | 29.6 (2020, 60 g) | 0.67% | 1 | ppg |
| 26 | Joe Johnson | 22,235 | 25.0 (2007, 57 g) | 0.71% | 1 | career |
| 27 | Nikola Jokic | 20,744 | 29.6 (2025, 70 g) | 0.71% | 1 | ppg |
| 28 | LaMarcus Aldridge | 22,023 | 23.4 (2015, 71 g) | 0.75% | 1 | career |
| 29 | Gilbert Arenas | 11,932 | 29.3 (2006, 80 g) | 0.75% | 1 | ppg |
| 30 | Paul George | 21,919 | 28.0 (2019, 77 g) | 0.79% | 1 | career |
| 31 | Vince Carter | 21,804 | 25.2 (2007, 82 g) | 0.83% | 1 | career |
| 32 | Isaiah Thomas | 10,287 | 28.9 (2017, 76 g) | 0.83% | 1 | ppg |
| 33 | Dwight Howard | 21,351 | 22.9 (2011, 78 g) | 0.87% | 1 | career |
| 34 | Anthony Edwards | 12,200 | 28.8 (2026, 61 g) | 0.87% | 1 | ppg |
| 35 | Anthony Davis | 20,933 | 28.1 (2018, 75 g) | 0.91% | 1 | career |
| 36 | Jalen Brunson | 12,988 | 28.7 (2024, 77 g) | 0.91% | 1 | ppg |
| 37 | Jaylen Brown | 16,249 | 28.7 (2026, 71 g) | 0.95% | 1 | ppg |
| 38 | Kyrie Irving | 20,602 | 27.1 (2023, 60 g) | 0.99% | 1 | career |
| 39 | Tyrese Maxey | 9,173 | 28.3 (2026, 70 g) | 0.99% | 1 | ppg |
| 40 | Klay Thompson | 20,346 | 22.3 (2017, 78 g) | 1.03% | 1 | career |

## 15 random players per tier (seed 2026)

### Tier 1 (10 points, top 3%): 112 players

| player | career points | best points per game | fame percentile |
|---|---|---|---|
| Luka Doncic | 16,718 | 33.9 (2024, 70 g) | 0.12% |
| Russell Westbrook | 30,190 | 31.6 (2017, 81 g) | 0.28% |
| Tim Duncan | 24,405 | 25.5 (2002, 82 g) | 0.52% |
| Klay Thompson | 20,346 | 22.3 (2017, 78 g) | 1.03% |
| Kawhi Leonard | 19,679 | 27.9 (2026, 65 g) | 1.15% |
| Devin Booker | 19,520 | 27.8 (2023, 53 g) | 1.23% |
| Chris Bosh | 18,534 | 24.0 (2010, 70 g) | 1.43% |
| CJ McCollum | 18,297 | 23.1 (2021, 47 g) | 1.55% |
| Mike Conley | 18,263 | 21.1 (2019, 70 g) | 1.59% |
| De'Aaron Fox | 13,254 | 26.6 (2024, 74 g) | 1.63% |
| Lou Williams | 16,607 | 22.6 (2018, 79 g) | 2.18% |
| Richard Hamilton | 16,229 | 20.1 (2006, 80 g) | 2.34% |
| Andre Iguodala | 15,615 | 19.9 (2008, 82 g) | 2.62% |
| Jeff Green | 15,360 | 16.9 (2014, 82 g) | 2.78% |
| Khris Middleton | 15,191 | 20.9 (2020, 62 g) | 2.94% |

### Tier 2 (20 points, 3 to 10%): 205 players

| player | career points | best points per game | fame percentile |
|---|---|---|---|
| Thaddeus Young | 14,767 | 17.9 (2014, 79 g) | 3.25% |
| Michael Jordan | 3,015 | 22.9 (2002, 60 g) | 3.61% |
| Myles Turner | 10,787 | 18.0 (2023, 62 g) | 6.15% |
| Tyson Chandler | 10,026 | 11.8 (2008, 79 g) | 6.79% |
| Evan Fournier | 9,810 | 18.5 (2020, 66 g) | 6.94% |
| Brandon Miller | 3,158 | 20.2 (2026, 65 g) | 7.06% |
| Mehmet Okur | 9,118 | 17.9 (2006, 81 g) | 7.58% |
| Jalen Duren | 3,950 | 19.5 (2026, 70 g) | 7.90% |
| Derrick White | 8,845 | 16.5 (2026, 77 g) | 8.06% |
| O.J. Mayo | 7,822 | 18.5 (2009, 82 g) | 9.01% |
| Juwan Howard | 7,228 | 18.4 (2003, 77 g) | 9.09% |
| Terrence Ross | 8,396 | 15.6 (2021, 46 g) | 9.13% |
| Nick Young | 8,342 | 17.9 (2014, 64 g) | 9.25% |
| Devonte' Graham | 3,757 | 18.2 (2020, 63 g) | 9.37% |
| Matt Barnes | 8,207 | 10.3 (2013, 80 g) | 9.48% |

### Tier 3 (35 points, 10 to 25%): 427 players

| player | career points | best points per game | fame percentile |
|---|---|---|---|
| Ty Lawson | 7,408 | 17.6 (2014, 62 g) | 10.04% |
| Josh Richardson | 6,617 | 16.6 (2019, 73 g) | 11.83% |
| Matas Buzelis | 1,940 | 16.3 (2026, 77 g) | 12.46% |
| Alonzo Mourning | 3,022 | 15.7 (2002, 75 g) | 13.06% |
| Kenneth Faried | 5,578 | 13.7 (2014, 80 g) | 15.56% |
| Thabo Sefolosha | 5,420 | 7.7 (2013, 80 g) | 16.07% |
| E'Twaun Moore | 4,872 | 12.5 (2018, 82 g) | 18.06% |
| Ajay Mitchell | 1,215 | 13.6 (2026, 57 g) | 18.25% |
| Keith Bogans | 4,417 | 9.6 (2005, 74 g) | 19.52% |
| Georges Niang | 4,295 | 9.9 (2025, 79 g) | 19.76% |
| Pat Connaughton | 4,206 | 9.9 (2022, 65 g) | 20.20% |
| Cam Whitmore | 1,249 | 12.3 (2024, 47 g) | 21.83% |
| Alex Caruso | 3,779 | 10.1 (2024, 71 g) | 22.06% |
| Noah Clowney | 1,362 | 12.3 (2026, 66 g) | 22.14% |
| Jannero Pargo | 3,403 | 9.2 (2007, 82 g) | 24.37% |

### Tier 4 (55 points, 25 to 50%): 600 players

| player | career points | best points per game | fame percentile |
|---|---|---|---|
| Herbert Jones | 3,045 | 11.0 (2024, 76 g) | 26.43% |
| Egor Demin | 536 | 10.3 (2026, 52 g) | 29.48% |
| Trendon Watford | 2,071 | 10.2 (2025, 44 g) | 29.92% |
| Amir Coffey | 2,323 | 9.7 (2025, 72 g) | 30.91% |
| Oshae Brissett | 1,546 | 9.1 (2022, 67 g) | 35.56% |
| Dereck Lively II | 992 | 8.8 (2024, 55 g) | 37.18% |
| Tyrese Martin | 834 | 8.7 (2025, 60 g) | 37.42% |
| John Konchar | 1,570 | 5.1 (2023, 72 g) | 37.54% |
| Jeremiah Robinson-Earl | 1,294 | 7.5 (2022, 49 g) | 40.91% |
| Alan Williams | 413 | 7.4 (2017, 47 g) | 43.21% |
| Eddie Robinson | 969 | 6.7 (2004, 51 g) | 44.92% |
| John Crotty | 325 | 6.9 (2002, 41 g) | 45.60% |
| Allan Ray | 290 | 6.7 (2007, 43 g) | 46.31% |
| Drake Powell | 408 | 6.5 (2026, 63 g) | 47.62% |
| Dalen Terry | 780 | 4.5 (2025, 73 g) | 48.17% |

### Tier 5 (75 points, 50 to 75%): 555 players

| player | career points | best points per game | fame percentile |
|---|---|---|---|
| Jan Vesely | 590 | 4.7 (2012, 57 g) | 51.83% |
| Danny Manning | 201 | 4.0 (2002, 41 g) | 57.90% |
| Jerome Adolphus Jordan | 182 | 3.1 (2015, 44 g) | 61.39% |
| Jaylen Hoard | 271 | none | 61.67% |
| Jermaine Jackson | 259 | 2.3 (2003, 53 g) | 62.10% |
| Dominique Jones | 246 | none | 62.74% |
| Johnathan Motley | 226 | none | 63.93% |
| Mengke Bateer | 156 | none | 68.85% |
| Billy Thomas | 147 | none | 69.52% |
| Tyler Burton | 129 | none | 71.03% |
| Justin Robinson | 112 | none | 72.46% |
| Cole Swider | 110 | none | 72.62% |
| Cameron Reynolds | 110 | none | 72.62% |
| Mac McClung | 100 | none | 73.65% |
| Jeremy Richardson | 88 | none | 75.00% |

### Tier 6 (100 points, bottom 25%): 621 players

| player | career points | best points per game | fame percentile |
|---|---|---|---|
| Sergei Monia | 77 | none | 76.75% |
| Nicolas Laprovittola | 59 | none | 78.57% |
| Cassius Winston | 57 | none | 78.97% |
| Melvin Sanders | 41 | none | 82.18% |
| Jordan Hall | 28 | none | 85.52% |
| Malik Williams | 19 | none | 88.17% |
| Dereon Seabron | 18 | none | 88.41% |
| Jalen Lecque | 15 | none | 89.29% |
| Armel Traore | 14 | none | 89.84% |
| Petr Cornelie | 14 | none | 89.84% |
| Antonio Harvey | 13 | none | 90.52% |
| Charles Cooke | 6 | none | 93.69% |
| Filip Petrusev | 3 | none | 95.83% |
| Scottie Lewis | 1 | none | 97.54% |
| Ibrahim Kutluay | 0 | none | 97.66% |

## Sanity check on recognizable names

| player | why and what we expect | tier | fame percentile | career points | best points per game | verdict |
|---|---|---|---|---|---|---|
| LeBron James | all-time great; expect tier 1 or better | 1 | 0.04% | 51,932 | 31.4 (2006, 79 g) | ok |
| Kobe Bryant | all-time great; expect tier 1 or better | 1 | 0.08% | 31,731 | 35.3 (2006, 78 g) | ok |
| Tim Duncan | all-time great; expect tier 1 or better | 1 | 0.52% | 24,405 | 25.5 (2002, 82 g) | ok |
| Dirk Nowitzki | all-time great; expect tier 1 or better | 1 | 0.20% | 31,359 | 26.6 (2006, 81 g) | ok |
| Stephen Curry | superstar; expect tier 1 or better | 1 | 0.24% | 30,675 | 32.0 (2021, 63 g) | ok |
| Kevin Durant | superstar; expect tier 1 or better | 1 | 0.08% | 37,572 | 32.0 (2014, 81 g) | ok |
| Giannis Antetokounmpo | superstar; expect tier 1 or better | 1 | 0.56% | 23,801 | 31.1 (2023, 63 g) | ok |
| Nikola Jokic | superstar; expect tier 1 or better | 1 | 0.71% | 20,744 | 29.6 (2025, 70 g) | ok |
| Luka Doncic | young star; expect tier 1 or better | 1 | 0.12% | 16,718 | 33.9 (2024, 70 g) | ok |
| Shai Gilgeous-Alexander | young star; expect tier 1 or better | 1 | 0.24% | 15,011 | 32.7 (2025, 76 g) | ok |
| Victor Wembanyama | young star, few seasons; expect tier 2 or better | 1 | 2.38% | 4,762 | 25.0 (2026, 64 g) | ok |
| Anthony Edwards | young star; expect tier 2 or better | 1 | 0.87% | 12,200 | 28.8 (2026, 61 g) | ok |
| Cade Cunningham | young star; expect tier 2 or better | 1 | 1.75% | 6,663 | 26.1 (2025, 70 g) | ok |
| Jalen Brunson | young star; expect tier 2 or better | 1 | 0.91% | 12,988 | 28.7 (2024, 77 g) | ok |
| Paolo Banchero | young star; expect tier 2 or better | 1 | 1.87% | 6,551 | 25.9 (2025, 46 g) | ok |
| Chet Holmgren | young star, defensive; expect tier 2 or better | 3 | 10.63% | 3,746 | 17.1 (2026, 69 g) | **CHECK** |
| Cooper Flagg | rookie star, one season; expect tier 2 or better | 2 | 5.83% | 1,473 | 21.0 (2026, 70 g) | ok |
| Tyrese Haliburton | young star; expect tier 2 or better | 2 | 6.35% | 6,521 | 20.7 (2023, 56 g) | ok |
| Michael Jordan | most famous player ever, but only his last two seasons (2001-02 and 2002-03, Wizards) are in the data; expect tier 1 or better | 2 | 3.61% | 3,015 | 22.9 (2002, 60 g) | **CHECK** |
| Ben Wallace | four-time Defensive Player of the Year, scorer in name only; expect tier 2 or better | 3 | 14.88% | 5,772 | 9.7 (2005, 74 g) | **CHECK** |
| Brian Scalabrine | famous bench player: a deep-ish name; expect tier 4 or worse | 4 | 36.23% | 1,697 | 6.3 (2005, 54 g) | ok |
| Jason Kapono | role player; expect tier 3 or worse | 3 | 23.89% | 3,444 | 10.6 (2007, 65 g) | ok |

Names that did not come out as expected: Chet Holmgren (tier 3), Michael Jordan (tier 2), Ben Wallace (tier 3).

## Review notes

Written by hand after reading the numbers above (the rest of this file is generated). Nothing in the top 40 looks wrong. These do:

- **Defenders and rebounders are rated too low (clearly wrong for Ben Wallace and Chet Holmgren).** Both come out as tier 3 (35 points) although each is well known for defence. The fame score only knows points, so a player who matters for blocks, rebounds or defence but scores little is under-rated. This shows up in prompts: Ben Wallace is a valid answer in 15 candidates (rebounds, blocks, steals, a triple-double) and is worth 35 points in each, where a fan would expect a tier 2 name (20). It is a limit of the method in the brief, not a bug. Fixing it needs another metric (rebounds, blocks, awards) or hand-set overrides, which is a decision for the next session or the owner.
- **Michael Jordan is tier 2, not tier 1.** Only his last two seasons (2001-02 and 2002-03, Wizards) are in the data, so he is judged on 3,015 career points and a best average of 22.9. This is the data window and it affects anyone whose prime was before 2001-02. It matters for prompts: Jordan scored 51 points twice in the data, so he is a valid answer to the 40+, 45+ and 50+ regular-season points prompts (6 candidates in all), where he is worth 20 points instead of 10.
- **One great season can make a modest-career player tier 1.** The "better of the two ranks" rule does what it was asked to, but it lets volume scorers in on a single season: Isaiah Thomas, Gilbert Arenas and Tyrese Maxey are all in the top 40. They are real stars, so this is not wrong, but tier 1 is fuller than 3% (112 players, 4.4%) and tiers 1 and 2 together hold 317 players (12.6%) against a nominal 10%.
- **Points per game uses the regular season only** (at least 40 games, games for all teams added up); career points include the playoffs, as the brief says. A player who was great in the playoffs but short on regular-season games gets no credit for it in the points-per-game rank.
- **Most lists are mostly well-known players.** Because tiers are global, 35 of the 53 player candidates have fewer than 10% of their answers at tier 4 or above, and only 7 have 25% or more. Those 7 come from `blocks` (15% to 36%), `rebounds` and `franchises`. If the game needs more deep cuts per prompt, the thresholds or the tier cutoffs are the levers.
