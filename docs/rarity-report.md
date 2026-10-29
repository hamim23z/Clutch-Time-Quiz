# Rarity report

Written by `python3 pipeline/export.py`; do not edit by hand. Tiers are the fame tiers of docs/fame-report.md: tier 1 is the best-known answer (10 points), tier 6 the rarest (100 points).

## Tier distribution of all valid answers

Before is the session 5 export (data/export/prompts.json as exported by session 5 (63 prompts, 9 dives)); after is this export. Every valid answer of every prompt is counted once per prompt.

|  | answers | tier 1 | tier 2 | tier 3 | tier 4 | tier 5 | tier 6 | tiers 1-2 | tiers 5-6 |
|---|---|---|---|---|---|---|---|---|---|
| before | 4,672 | 2,390 (51.2%) | 1,328 (28.4%) | 717 (15.3%) | 213 (4.6%) | 20 (0.4%) | 4 (0.1%) | 79.6% | 0.5% |
| after | 32,598 | 7,681 (23.6%) | 6,498 (19.9%) | 7,170 (22.0%) | 6,057 (18.6%) | 3,590 (11.0%) | 1,602 (4.9%) | 43.5% | 15.9% |

- Target: tiers 1 and 2 together at most 45% of valid answers: **met** (43.5%).
- Target: tiers 5 and 6 together at least 12%: **met** (15.9%).
- Tier recalibration: not needed; the tiers are the global fame tiers of docs/fame-report.md, unchanged.

## Points

|  | prompts | valid answers | average points of a random valid answer | average points per prompt (sum of its answers' points) | average valid answers per prompt |
|---|---|---|---|---|---|
| before | 63 | 4,672 | 19.1 | 1,415 | 74 |
| after | 504 | 32,598 | 37.4 | 2,421 | 65 |

The fourth column is what the whole answer list of a prompt is worth added up; a player scores one answer per prompt, so what a player earns is in the next section.

## Best-known versus rarest answer, five sample dives

For each dive: the points if the player types the single best-known valid answer on every one of the 7 prompts, against the single rarest valid answer on every prompt (the maximum for that choice of answers).

| dive | best-known answer on every prompt | rarest answer on every prompt | ratio |
|---|---|---|---|
| 14 | 70 | 475 | 6.8x |
| 16 | 70 | 410 | 5.9x |
| 41 | 70 | 430 | 6.1x |
| 65 | 70 | 405 | 5.8x |
| 66 | 70 | 405 | 5.8x |

Over all 72 dives the best-known strategy averages 70 points a dive and the rarest 412; the most a dive can pay is 700 (every answer worth 100).

## Prompts per template family

| family | kind | prompts | share |
|---|---|---|---|
| `franchise-bench` | broad player | 27 | 5.4% |
| `franchise-regular` | broad player | 25 | 5.0% |
| `teammate` | broad player | 21 | 4.2% |
| `both-franchises` | broad player | 20 | 4.0% |
| `franchise-season` | broad player | 20 | 4.0% |
| `franchise-start` | broad player | 20 | 4.0% |
| `franchise-years` | broad player | 20 | 4.0% |
| `franchise-playoff` | broad player | 19 | 3.8% |
| `franchise-playoff-season` | broad player | 18 | 3.6% |
| `finals-year` | broad player | 16 | 3.2% |
| `franchise-points` | broad player | 16 | 3.2% |
| `month-points` | broad player | 16 | 3.2% |
| `month-threes` | broad player | 16 | 3.2% |
| `points-against` | broad player | 15 | 3.0% |
| `season-rebounds` | broad player | 15 | 3.0% |
| `season-threes` | broad player | 15 | 3.0% |
| `season-assists` | broad player | 14 | 2.8% |
| `season-points` | broad player | 13 | 2.6% |
| `held-opponent-in-season` | team | 11 | 2.2% |
| `home-wins-in-season` | team | 11 | 2.2% |
| `overtime-wins-in-season` | team | 11 | 2.2% |
| `playoff-wins-in-season` | team | 11 | 2.2% |
| `regulation-points-in-season` | team | 11 | 2.2% |
| `threes-in-season` | team | 11 | 2.2% |
| `wins-in-season` | team | 11 | 2.2% |
| `beat-in-playoffs` | team | 10 | 2.0% |
| `made-playoffs` | team | 10 | 2.0% |
| `margin-in-season` | team | 10 | 2.0% |
| `played-playoff-against` | team | 10 | 2.0% |
| `road-wins-in-season` | team | 10 | 2.0% |
| `assists` | star-style player | 1 | 0.2% |
| `assists-finals` | star-style player | 1 | 0.2% |
| `assists-per-game` | star-style player | 1 | 0.2% |
| `assists-playoff` | star-style player | 1 | 0.2% |
| `blocks` | star-style player | 1 | 0.2% |
| `blocks-playoff` | star-style player | 1 | 0.2% |
| `champion` | team | 1 | 0.2% |
| `double-double-average` | star-style player | 1 | 0.2% |
| `finals-appearance` | broad player | 1 | 0.2% |
| `franchises` | star-style player | 1 | 0.2% |
| `free-throws` | star-style player | 1 | 0.2% |
| `held-opponent` | team | 1 | 0.2% |
| `home-wins` | team | 1 | 0.2% |
| `losses-season` | team | 1 | 0.2% |
| `minutes` | star-style player | 1 | 0.2% |
| `offensive-rebounds` | star-style player | 1 | 0.2% |
| `overtime-wins` | team | 1 | 0.2% |
| `perfect-shooting` | star-style player | 1 | 0.2% |
| `points-any-game` | team | 1 | 0.2% |
| `points-bench` | star-style player | 1 | 0.2% |
| `points-finals` | star-style player | 1 | 0.2% |
| `points-game7` | star-style player | 1 | 0.2% |
| `points-loss` | star-style player | 1 | 0.2% |
| `points-overtime-game` | star-style player | 1 | 0.2% |
| `points-playoff` | star-style player | 1 | 0.2% |
| `points-playoff-team` | team | 1 | 0.2% |
| `points-regular` | star-style player | 1 | 0.2% |
| `points-regulation` | team | 1 | 0.2% |
| `points-road` | star-style player | 1 | 0.2% |
| `ppg-season` | star-style player | 1 | 0.2% |
| `reached-finals` | team | 1 | 0.2% |
| `rebounds` | star-style player | 1 | 0.2% |
| `rebounds-finals` | star-style player | 1 | 0.2% |
| `rebounds-per-game` | star-style player | 1 | 0.2% |
| `rebounds-playoff` | star-style player | 1 | 0.2% |
| `road-wins` | team | 1 | 0.2% |
| `shots-taken` | star-style player | 1 | 0.2% |
| `steals-per-game` | star-style player | 1 | 0.2% |
| `steals-playoff` | star-style player | 1 | 0.2% |
| `steals-team` | team | 1 | 0.2% |
| `threes` | star-style player | 1 | 0.2% |
| `threes-finals` | star-style player | 1 | 0.2% |
| `threes-playoff` | star-style player | 1 | 0.2% |
| `threes-team` | team | 1 | 0.2% |
| `triple-double-regular` | star-style player | 1 | 0.2% |
| `turnovers` | star-style player | 1 | 0.2% |
| `win-margin` | team | 1 | 0.2% |
| `win-margin-playoff` | team | 1 | 0.2% |
| `win-streak` | team | 1 | 0.2% |
| `wins-playoff` | team | 1 | 0.2% |
| `wins-season` | team | 1 | 0.2% |

By kind: broad player 327, star-style player 33, team 144. 81 families in all.

## Tiers by family kind

|  | answers | tier 1 | tier 2 | tier 3 | tier 4 | tier 5 | tier 6 | tiers 1-2 | tiers 5-6 |
|---|---|---|---|---|---|---|---|---|---|
| broad player | 28,941 | 5,109 (17.7%) | 5,918 (20.4%) | 6,842 (23.6%) | 5,899 (20.4%) | 3,573 (12.3%) | 1,600 (5.5%) | 38.1% | 17.9% |
| star-style player | 2,152 | 1,118 (52.0%) | 580 (27.0%) | 328 (15.2%) | 107 (5.0%) | 17 (0.8%) | 2 (0.1%) | 78.9% | 0.9% |
| team | 1,505 | 1,454 (96.6%) | 0 (0.0%) | 0 (0.0%) | 51 (3.4%) | 0 (0.0%) | 0 (0.0%) | 96.6% | 0.0% |
