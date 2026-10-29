# Curation report

Written by `python3 pipeline/export.py`; do not edit by hand. Layout of the files is in docs/export-format.md.

- **63 prompts** in 9 dives of 7, chosen from 171 candidates (45 player, 18 team).
- By difficulty: easy 29, medium 25, hard 9.
- 49 template families; at most 2 thresholds from any family; no family needed more than 2.
- Templates added in session 5 because the session 4 set (17 templates) gave too few families for 63 prompts: 34 of the 49 in use (assists-per-game, assists-playoff, blocks-per-game, blocks-playoff, champion, double-double-average, five-by-n, free-throws, held-opponent, home-wins, losses-season, minutes, offensive-rebounds, overtime-wins, perfect-shooting, points-any-game, points-bench, points-game7, points-playoff-team, reached-finals, rebounds-finals, rebounds-per-game, rebounds-playoff, road-wins, shots-taken, steals-per-game, steals-playoff, steals-team, threes-finals, threes-playoff, threes-team, turnovers, win-margin-playoff, win-streak).

## Prompts by template

| template | answers | prompts | thresholds | session |
|---|---|---|---|---|
| assists | player | 2 | 14, 20 | 4 |
| assists-per-game | player | 1 | 9 | 5 |
| assists-playoff | player | 1 | 16 | 5 |
| blocks | player | 1 | 10 | 4 |
| blocks-per-game | player | 1 | 2 | 5 |
| blocks-playoff | player | 1 | 7 | 5 |
| champion | team | 1 | - | 5 |
| double-double-average | player | 1 | - | 5 |
| five-by-n | player | 2 | 4, 3 | 5 |
| franchises | player | 2 | 6, 9 | 4 |
| free-throws | player | 2 | 22, 18 | 5 |
| held-opponent | team | 2 | 70, 60 | 5 |
| home-wins | team | 1 | 36 | 5 |
| losses-season | team | 1 | 67 | 5 |
| minutes | player | 2 | 58, 55 | 5 |
| offensive-rebounds | player | 2 | 12, 11 | 5 |
| overtime-wins | team | 1 | 3 | 5 |
| perfect-shooting | player | 2 | 8, 11 | 5 |
| points-any-game | team | 1 | 160 | 5 |
| points-bench | player | 1 | 40 | 5 |
| points-finals | player | 1 | 20 | 4 |
| points-game7 | player | 1 | 35 | 5 |
| points-playoff | player | 1 | 25 | 4 |
| points-playoff-team | team | 1 | 130 | 5 |
| points-regular | player | 1 | 40 | 4 |
| ppg-season | player | 2 | 30, 20 | 4 |
| reached-finals | team | 1 | - | 5 |
| rebounds | player | 1 | 27 | 4 |
| rebounds-finals | player | 1 | 14 | 5 |
| rebounds-per-game | player | 1 | 12 | 5 |
| rebounds-playoff | player | 1 | 16 | 5 |
| road-wins | team | 1 | 30 | 5 |
| shots-taken | player | 2 | 38, 35 | 5 |
| steals | player | 1 | 6 | 4 |
| steals-per-game | player | 1 | 2 | 5 |
| steals-playoff | player | 2 | 6, 4 | 5 |
| steals-team | team | 1 | 20 | 5 |
| threes | player | 2 | 11, 8 | 4 |
| threes-finals | player | 1 | 6 | 5 |
| threes-playoff | player | 1 | 8 | 5 |
| threes-team | team | 1 | 28 | 5 |
| triple-double-playoff | player | 1 | - | 4 |
| triple-double-regular | player | 1 | - | 4 |
| turnovers | player | 2 | 8, 11 | 5 |
| win-margin | team | 1 | 55 | 4 |
| win-margin-playoff | team | 1 | 35 | 5 |
| win-streak | team | 1 | 16 | 5 |
| wins-playoff | team | 2 | 14, 10 | 4 |
| wins-season | team | 1 | 50 | 4 |

## The dives

e, m, h = easy, medium, hard. Slots 3 and 5 are the team prompts.

| dive | e/m/h | 1 | 2 | 3 (team) | 4 | 5 (team) | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| 1 | eememmh | assists 14 (213) | blocks-per-game 2 (56) | road-wins 30 (8) | steals-per-game 2 (41) | threes-team 28 (5) | rebounds-finals 14 (28) | points-bench 40 (35) |
| 2 | eememmh | points-regular 40 (263) | triple-double-regular (248) | steals-team 20 (19) | turnovers 8 (247) | reached-finals (17) | minutes 58 (19) | threes 11 (21) |
| 3 | emememh | minutes 55 (84) | franchises 6 (284) | held-opponent 70 (30) | perfect-shooting 8 (176) | win-margin-playoff 35 (21) | ppg-season 30 (16) | blocks-playoff 7 (21) |
| 4 | eemehmm | threes 8 (253) | ppg-season 20 (185) | wins-playoff 14 (16) | rebounds-playoff 16 (113) | held-opponent 60 (14) | shots-taken 38 (26) | free-throws 22 (21) |
| 5 | eeememh | points-playoff 25 (330) | offensive-rebounds 12 (52) | wins-season 50 (28) | threes-playoff 8 (32) | win-streak 16 (13) | assists-per-game 9 (19) | perfect-shooting 11 (22) |
| 6 | emememh | double-double-average (79) | steals-playoff 6 (37) | overtime-wins 3 (22) | points-game7 35 (23) | champion (13) | threes-finals 6 (21) | assists 20 (27) |
| 7 | eeemmmh | steals 6 (328) | points-finals 20 (98) | home-wins 36 (13) | turnovers 11 (27) | points-any-game 160 (7) | rebounds 27 (19) | blocks 10 (20) |
| 8 | eeemmmh | free-throws 18 (65) | triple-double-playoff (42) | wins-playoff 10 (22) | offensive-rebounds 11 (84) | win-margin 55 (11) | five-by-n 4 (40) | franchises 9 (35) |
| 9 | eeeehmm | steals-playoff 4 (283) | five-by-n 3 (252) | points-playoff-team 130 (26) | shots-taken 35 (54) | losses-season 67 (8) | rebounds-per-game 12 (25) | assists-playoff 16 (15) |
