# Curation report

Written by `python3 pipeline/export.py`; do not edit by hand. Layout of the files is in docs/export-format.md; tiers and points in docs/rarity-report.md.

- **504 prompts** in 72 dives of 7, chosen from 3,945 candidates (360 player: 327 broad-pool and 33 star-style; 144 team).
- By difficulty: easy 94, medium 272, hard 138.
- 81 template families. Each parameter set (franchise, season, month, star) is used once, and a family never appears twice with only the threshold changed.

## Prompts by template family

| family | answers | kind | prompts |
|---|---|---|---|
| `franchise-bench` | player | broad | 27 |
| `franchise-regular` | player | broad | 25 |
| `teammate` | player | broad | 21 |
| `both-franchises` | player | broad | 20 |
| `franchise-season` | player | broad | 20 |
| `franchise-start` | player | broad | 20 |
| `franchise-years` | player | broad | 20 |
| `franchise-playoff` | player | broad | 19 |
| `franchise-playoff-season` | player | broad | 18 |
| `finals-year` | player | broad | 16 |
| `franchise-points` | player | broad | 16 |
| `month-points` | player | broad | 16 |
| `month-threes` | player | broad | 16 |
| `points-against` | player | broad | 15 |
| `season-rebounds` | player | broad | 15 |
| `season-threes` | player | broad | 15 |
| `season-assists` | player | broad | 14 |
| `season-points` | player | broad | 13 |
| `held-opponent-in-season` | team | - | 11 |
| `home-wins-in-season` | team | - | 11 |
| `overtime-wins-in-season` | team | - | 11 |
| `playoff-wins-in-season` | team | - | 11 |
| `regulation-points-in-season` | team | - | 11 |
| `threes-in-season` | team | - | 11 |
| `wins-in-season` | team | - | 11 |
| `beat-in-playoffs` | team | - | 10 |
| `made-playoffs` | team | - | 10 |
| `margin-in-season` | team | - | 10 |
| `played-playoff-against` | team | - | 10 |
| `road-wins-in-season` | team | - | 10 |
| `assists` | player | - | 1 |
| `assists-finals` | player | - | 1 |
| `assists-per-game` | player | - | 1 |
| `assists-playoff` | player | - | 1 |
| `blocks` | player | - | 1 |
| `blocks-playoff` | player | - | 1 |
| `champion` | team | - | 1 |
| `double-double-average` | player | - | 1 |
| `finals-appearance` | player | broad | 1 |
| `franchises` | player | - | 1 |
| `free-throws` | player | - | 1 |
| `held-opponent` | team | - | 1 |
| `home-wins` | team | - | 1 |
| `losses-season` | team | - | 1 |
| `minutes` | player | - | 1 |
| `offensive-rebounds` | player | - | 1 |
| `overtime-wins` | team | - | 1 |
| `perfect-shooting` | player | - | 1 |
| `points-any-game` | team | - | 1 |
| `points-bench` | player | - | 1 |
| `points-finals` | player | - | 1 |
| `points-game7` | player | - | 1 |
| `points-loss` | player | - | 1 |
| `points-overtime-game` | player | - | 1 |
| `points-playoff` | player | - | 1 |
| `points-playoff-team` | team | - | 1 |
| `points-regular` | player | - | 1 |
| `points-regulation` | team | - | 1 |
| `points-road` | player | - | 1 |
| `ppg-season` | player | - | 1 |
| `reached-finals` | team | - | 1 |
| `rebounds` | player | - | 1 |
| `rebounds-finals` | player | - | 1 |
| `rebounds-per-game` | player | - | 1 |
| `rebounds-playoff` | player | - | 1 |
| `road-wins` | team | - | 1 |
| `shots-taken` | player | - | 1 |
| `steals-per-game` | player | - | 1 |
| `steals-playoff` | player | - | 1 |
| `steals-team` | team | - | 1 |
| `threes` | player | - | 1 |
| `threes-finals` | player | - | 1 |
| `threes-playoff` | player | - | 1 |
| `threes-team` | team | - | 1 |
| `triple-double-regular` | player | - | 1 |
| `turnovers` | player | - | 1 |
| `win-margin` | team | - | 1 |
| `win-margin-playoff` | team | - | 1 |
| `win-streak` | team | - | 1 |
| `wins-playoff` | team | - | 1 |
| `wins-season` | team | - | 1 |

## The dives

e, m, h = easy, medium, hard. Slots 3 and 5 are the team prompts. Counts in brackets are valid answers.

| dive | e/m/h | 1 | 2 | 3 (team) | 4 | 5 (team) | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| 1 | emmmmmh | season-assists 2016/11 (61) | franchise-regular 15 (248) | reached-finals (17) | franchise-points 8/25 (71) | losses-season 65 (14) | month-points 2005/11/35 (18) | both-franchises 17/19 (23) |
| 2 | eemmmhh | month-threes 2024/3/6 (54) | season-points 2014/35 (53) | held-opponent-in-season 2020/80 (10) | franchise-bench 26 (211) | home-wins-in-season 2014/30 (7) | finals-year 2017 (26) | franchise-playoff-season 20/2021 (16) |
| 3 | eeemhmh | points-against 8/40 (46) | month-points 2007/4/30 (40) | beat-in-playoffs 2 (16) | franchise-playoff 7 (106) | overtime-wins-in-season 2011/2 (8) | season-assists 2008/15 (16) | both-franchises 9/16 (25) |
| 4 | mmemmmh | franchise-regular 23 (243) | teammate 6580 (170) | threes-in-season 2022/23 (13) | season-points 2024/45 (25) | wins-in-season 2005/40 (18) | points-finals 40 (15) | finals-year 2024 (30) |
| 5 | mmemmmh | franchise-start 26 (146) | franchise-points 30/25 (62) | played-playoff-against 2 (16) | season-assists 2022/15 (19) | road-wins-in-season 2014/23 (7) | month-points 2003/1/35 (18) | franchise-years 16/2002/2006 (48) |
| 6 | mmemehh | franchise-bench 18 (233) | points-against 10/45 (21) | threes-in-season 2016/17 (16) | season-points 2021/45 (16) | margin-in-season 2019/35 (15) | both-franchises 14/20 (19) | franchise-playoff-season 5/2026 (18) |
| 7 | emmmhmh | threes-playoff 7 (83) | teammate 3133628 (115) | regulation-points-in-season 2014/135 (6) | franchise-playoff 17 (111) | held-opponent-in-season 2005/65 (5) | season-rebounds 2005/20 (18) | franchise-years 1/2002/2006 (70) |
| 8 | ememmhh | season-points 2002/35 (49) | franchise-start 22 (159) | made-playoffs 2018 (16) | points-against 30/45 (18) | playoff-wins-in-season 2023/4 (8) | both-franchises 20/21 (37) | franchise-playoff-season 2/2020 (17) |
| 9 | ememmhh | steals-per-game 2 (41) | teammate 4277905 (104) | regulation-points-in-season 2013/125 (15) | threes-finals 6 (21) | beat-in-playoffs 15 (10) | franchise-playoff 19 (97) | franchise-season 1/2017 (20) |
| 10 | emmmmhh | franchise-start 18 (168) | franchise-bench 11 (190) | wins-in-season 2009/40 (16) | franchise-points 25/25 (66) | margin-in-season 2020/40 (7) | franchise-years 10/2002/2006 (57) | both-franchises 21/29 (37) |
| 11 | emhmhmh | points-against 17/40 (44) | franchise-regular 16 (231) | played-playoff-against 23 (7) | month-threes 2026/4/4 (129) | overtime-wins-in-season 2002/2 (6) | season-threes 2004/7 (18) | franchise-season 14/2005 (17) |
| 12 | emhmhmm | season-points 2006/35 (48) | teammate 3442 (242) | regulation-points-in-season 2002/125 (8) | franchise-bench 19 (206) | wins-in-season 2008/55 (7) | franchise-playoff 2 (146) | franchise-points 28/30 (48) |
| 13 | mmemhmm | franchise-regular 3 (262) | month-threes 2006/3/5 (31) | made-playoffs 2017 (16) | finals-year 2008 (23) | beat-in-playoffs 23 (7) | assists-finals 10 (22) | season-assists 2021/15 (16) |
| 14 | mmemhhh | teammate 1017 (182) | franchise-playoff 22 (107) | threes-in-season 2011/14 (16) | points-loss 55 (20) | played-playoff-against 19 (11) | franchise-years 13/2022/2026 (80) | both-franchises 24/27 (22) |
| 15 | emmmmmh | season-rebounds 2014/18 (41) | franchise-bench 20 (273) | regulation-points-in-season 2010/125 (18) | points-road 55 (22) | held-opponent-in-season 2016/75 (11) | month-points 2004/3/35 (16) | franchise-season 11/2013 (16) |
| 16 | mmemmhh | franchise-regular 10 (254) | teammate 1007 (203) | margin-in-season 2017/35 (12) | rebounds-finals 16 (19) | points-any-game 160 (7) | franchise-playoff 1 (97) | finals-year 2007 (23) |
| 17 | emmmhhh | franchise-points 14/25 (60) | franchise-start 19 (149) | beat-in-playoffs 8 (13) | season-threes 2020/8 (28) | overtime-wins-in-season 2004/2 (7) | franchise-season 28/2024 (30) | month-threes 2003/2/5 (27) |
| 18 | mmemmhh | teammate 3032979 (246) | franchise-bench 24 (196) | regulation-points-in-season 2011/125 (17) | season-points 2012/40 (16) | home-wins-in-season 2018/30 (6) | franchise-years 20/2017/2021 (76) | both-franchises 1/6 (38) |
| 19 | eemmmmh | season-assists 2003/11 (55) | month-points 2025/3/35 (42) | road-wins-in-season 2017/20 (9) | franchise-regular 18 (248) | overtime-wins-in-season 2022/2 (7) | franchise-start 14 (158) | franchise-season 17/2004 (19) |
| 20 | mmemmmh | teammate 136 (240) | franchise-bench 23 (237) | played-playoff-against 25 (16) | season-rebounds 2017/18 (25) | wins-in-season 2018/50 (6) | finals-year 2009 (22) | franchise-years 20/2022/2026 (85) |
| 21 | ememmhh | franchises 6 (284) | franchise-regular 28 (250) | margin-in-season 2015/35 (16) | season-assists 2017/15 (16) | home-wins-in-season 2015/30 (8) | both-franchises 21/22 (24) | franchise-season 3/2005 (22) |
| 22 | mmemmhh | franchise-start 20 (181) | month-points 2026/4/20 (172) | win-margin 50 (21) | franchise-points 7/35 (20) | overtime-wins-in-season 2012/2 (8) | franchise-playoff 5 (92) | franchise-years 19/2017/2021 (62) |
| 23 | mmemmhh | franchise-bench 2 (221) | season-points 2009/40 (32) | champion (13) | points-against 14/45 (18) | threes-in-season 2021/26 (5) | both-franchises 21/26 (28) | franchise-season 8/2025 (21) |
| 24 | emmmmhh | season-threes 2007/6 (58) | franchise-regular 22 (219) | playoff-wins-in-season 2016/4 (8) | teammate 6478 (171) | wins-in-season 2021/45 (7) | franchise-years 28/2022/2026 (71) | finals-year 2025 (33) |
| 25 | mmemmhh | franchise-bench 16 (221) | season-rebounds 2025/16 (61) | made-playoffs 2012 (16) | month-threes 2006/11/5 (25) | home-wins-in-season 2005/30 (6) | both-franchises 17/29 (36) | franchise-season 2/2003 (17) |
| 26 | emmmhhh | season-threes 2024/8 (41) | franchise-start 3 (173) | regulation-points-in-season 2018/140 (6) | franchise-points 20/35 (15) | threes-in-season 2003/14 (6) | franchise-years 8/2022/2026 (77) | finals-year 2022 (29) |
| 27 | ememmmh | blocks 6 (215) | franchise-bench 15 (245) | margin-in-season 2023/30 (21) | franchise-playoff 25 (105) | played-playoff-against 27 (8) | points-against 19/45 (20) | franchise-playoff-season 7/2024 (17) |
| 28 | emmmhmh | triple-double-regular (248) | franchise-start 29 (170) | win-streak 18 (8) | teammate 3975 (153) | held-opponent 60 (14) | month-threes 2011/3/6 (19) | franchise-years 17/2002/2006 (52) |
| 29 | emmmmmh | season-threes 2018/7 (52) | franchise-bench 9 (221) | playoff-wins-in-season 2025/4 (8) | shots-taken 38 (26) | held-opponent-in-season 2012/65 (5) | points-against 22/45 (20) | finals-year 2021 (25) |
| 30 | emmhmhh | turnovers 10 (52) | franchise-regular 29 (267) | played-playoff-against 15 (10) | franchise-playoff 16 (75) | regulation-points-in-season 2016/135 (5) | season-assists 2026/15 (18) | franchise-season 23/2011 (16) |
| 31 | mmehmhh | franchise-bench 21 (253) | teammate 6583 (181) | playoff-wins-in-season 2018/1 (15) | franchise-years 3/2022/2026 (63) | beat-in-playoffs 12 (10) | month-threes 2016/4/5 (34) | franchise-points 24/30 (32) |
| 32 | emmmhhh | points-against 2/40 (51) | franchise-start 30 (133) | win-margin-playoff 40 (11) | month-points 2021/4/40 (17) | held-opponent-in-season 2013/65 (5) | both-franchises 1/25 (28) | franchise-playoff-season 19/2024 (15) |
| 33 | mmehmhh | franchise-regular 21 (259) | franchise-bench 22 (213) | margin-in-season 2007/30 (13) | franchise-years 6/2022/2026 (74) | beat-in-playoffs 28 (11) | finals-year 2005 (24) | season-threes 2026/9 (22) |
| 34 | emmmhmh | franchise-points 17/30 (41) | franchise-start 11 (153) | held-opponent-in-season 2021/80 (9) | points-regular 60 (24) | playoff-wins-in-season 2006/4 (8) | month-points 2007/2/35 (20) | franchise-season 13/2026 (20) |
| 35 | mmemmmh | franchise-bench 14 (204) | teammate 3995 (201) | threes-in-season 2025/23 (16) | points-against 21/45 (20) | margin-in-season 2014/40 (5) | season-assists 2010/15 (15) | franchise-years 1/2022/2026 (70) |
| 36 | mmehmhh | franchise-start 28 (168) | franchise-playoff 8 (87) | made-playoffs 2023 (16) | finals-year 2023 (27) | home-wins-in-season 2006/30 (6) | franchise-season 30/2025 (27) | season-rebounds 2026/20 (19) |
| 37 | emmmmhh | perfect-shooting 10 (46) | franchise-bench 13 (231) | threes-in-season 2007/14 (16) | month-points 2020/3/35 (20) | played-playoff-against 16 (10) | teammate 4278073 (87) | franchise-playoff-season 25/2025 (17) |
| 38 | ememmhh | season-rebounds 2022/14 (106) | franchise-start 8 (138) | overtime-wins 2 (30) | franchise-points 3/25 (81) | steals-team 20 (19) | franchise-years 11/2012/2016 (44) | both-franchises 4/26 (18) |
| 39 | eeemmhh | points-playoff 25 (330) | points-against 9/40 (57) | made-playoffs 2021 (16) | franchise-regular 25 (210) | regulation-points-in-season 2004/125 (6) | franchise-playoff 21 (93) | month-threes 2022/1/7 (23) |
| 40 | emmmhmh | franchise-points 10/30 (51) | franchise-bench 5 (254) | playoff-wins-in-season 2010/4 (8) | threes 11 (21) | held-opponent-in-season 2006/65 (5) | season-rebounds 2011/20 (19) | franchise-playoff-season 2/2026 (15) |
| 41 | mmemmhh | franchise-regular 30 (203) | franchise-playoff 11 (107) | beat-in-playoffs 25 (14) | season-threes 2017/8 (18) | road-wins-in-season 2003/23 (5) | finals-year 2019 (27) | franchise-season 8/2022 (27) |
| 42 | eemmmmh | month-threes 2025/11/5 (103) | season-rebounds 2021/16 (48) | overtime-wins-in-season 2016/2 (8) | franchise-bench 6 (236) | playoff-wins-in-season 2026/4 (8) | franchise-points 21/25 (83) | both-franchises 5/10 (18) |
| 43 | ememmmh | month-points 2016/4/25 (67) | franchise-regular 26 (216) | wins-playoff 15 (14) | franchise-start 23 (152) | threes-team 28 (5) | points-against 15/45 (24) | franchise-years 27/2022/2026 (87) |
| 44 | eemmhmm | offensive-rebounds 11 (84) | season-rebounds 2003/16 (54) | overtime-wins-in-season 2019/2 (8) | teammate 3032976 (126) | road-wins-in-season 2008/25 (6) | franchise-playoff 20 (123) | month-threes 2015/10/4 (18) |
| 45 | eeemhhh | season-assists 2020/11 (64) | ppg-season 26 (46) | wins-in-season 2010/45 (14) | franchise-bench 3 (251) | threes-in-season 2004/14 (8) | finals-year 2002 (24) | franchise-playoff-season 9/2025 (17) |
| 46 | emmmmmh | season-rebounds 2010/18 (44) | franchise-start 10 (163) | points-regulation 155 (10) | franchise-points 13/35 (23) | margin-in-season 2010/40 (5) | month-points 2023/4/35 (20) | franchise-season 2/2026 (21) |
| 47 | mmemmhh | franchise-regular 4 (221) | teammate 841 (191) | wins-in-season 2016/40 (19) | season-assists 2002/15 (17) | played-playoff-against 1 (11) | franchise-years 29/2022/2026 (80) | both-franchises 11/12 (22) |
| 48 | emmmhmh | franchise-points 27/30 (42) | franchise-bench 17 (287) | home-wins-in-season 2007/30 (8) | points-bench 40 (35) | overtime-wins-in-season 2013/2 (11) | season-points 2016/40 (22) | franchise-playoff-season 15/2021 (17) |
| 49 | mmemmhh | franchise-regular 20 (283) | teammate 3059318 (129) | margin-in-season 2025/40 (15) | assists 20 (27) | road-wins-in-season 2016/20 (9) | both-franchises 7/26 (26) | season-rebounds 2002/20 (15) |
| 50 | ememhmh | season-assists 2018/11 (54) | franchise-playoff 13 (115) | points-playoff-team 140 (13) | franchise-points 23/30 (51) | home-wins-in-season 2003/33 (5) | month-points 2025/10/35 (21) | franchise-playoff-season 11/2024 (17) |
| 51 | emmmmmh | double-double-average (79) | franchise-regular 17 (293) | held-opponent-in-season 2024/80 (6) | season-points 2023/45 (26) | road-wins-in-season 2009/23 (5) | points-against 1/45 (18) | franchise-season 9/2011 (17) |
| 52 | mmemhhh | month-threes 2025/4/4 (136) | steals-playoff 6 (37) | wins-in-season 2022/45 (13) | season-assists 2011/15 (18) | beat-in-playoffs 18 (9) | franchise-playoff 3 (83) | franchise-years 23/2022/2026 (73) |
| 53 | emmmmmh | season-points 2026/40 (47) | franchise-bench 7 (199) | made-playoffs 2011 (16) | franchise-regular 24 (198) | home-wins-in-season 2008/33 (6) | month-points 2004/2/35 (16) | franchise-season 29/2006 (16) |
| 54 | mmemmhh | franchise-start 17 (196) | franchise-points 16/30 (40) | threes-in-season 2015/17 (12) | season-threes 2016/8 (15) | regulation-points-in-season 2023/150 (6) | month-threes 2002/12/5 (28) | franchise-playoff-season 15/2023 (15) |
| 55 | mmemmhh | franchise-regular 8 (227) | month-points 2011/1/35 (23) | made-playoffs 2024 (16) | season-assists 2025/15 (18) | road-wins-in-season 2011/25 (6) | franchise-season 11/2026 (27) | both-franchises 18/26 (16) |
| 56 | emhmhmh | franchise-playoff 14 (112) | franchise-start 27 (167) | home-wins-in-season 2010/30 (8) | season-threes 2011/7 (25) | threes-in-season 2005/17 (5) | points-overtime-game 55 (21) | franchise-years 25/2022/2026 (55) |
| 57 | mmemmmh | franchise-bench 29 (263) | teammate 3244 (220) | regulation-points-in-season 2008/130 (13) | month-threes 2015/3/6 (21) | played-playoff-against 21 (11) | season-rebounds 2016/20 (17) | franchise-playoff-season 2/2025 (15) |
| 58 | mmehmhh | season-threes 2008/7 (28) | assists-playoff 16 (15) | wins-in-season 2025/45 (13) | franchise-playoff 28 (95) | overtime-wins-in-season 2017/2 (6) | both-franchises 7/30 (20) | franchise-season 23/2005 (18) |
| 59 | ememmmh | rebounds-per-game 10 (82) | franchise-regular 9 (223) | made-playoffs 2015 (16) | franchise-bench 25 (198) | regulation-points-in-season 2020/145 (8) | season-points 2025/45 (23) | franchise-playoff-season 6/2024 (18) |
| 60 | emmmhmh | season-threes 2025/8 (46) | teammate 3468 (209) | playoff-wins-in-season 2012/4 (8) | franchise-start 4 (151) | overtime-wins-in-season 2005/2 (8) | points-against 7/45 (16) | finals-year 2010 (25) |
| 61 | ememmmh | season-points 2005/35 (54) | franchise-bench 27 (248) | home-wins 36 (13) | month-threes 2026/3/4 (178) | road-wins-in-season 2018/23 (5) | rebounds-playoff 22 (17) | franchise-playoff-season 17/2021 (15) |
| 62 | emmmhhh | season-threes 2012/6 (44) | franchise-regular 19 (212) | home-wins-in-season 2024/30 (5) | franchise-start 16 (151) | played-playoff-against 20 (11) | franchise-season 29/2024 (35) | finals-year 2003 (24) |
| 63 | eemmmhh | month-threes 2019/4/5 (48) | season-rebounds 2013/18 (41) | held-opponent-in-season 2004/65 (13) | franchise-bench 1 (253) | wins-season 65 (9) | both-franchises 3/17 (33) | franchise-playoff-season 21/2021 (16) |
| 64 | mmemmmh | franchise-regular 7 (204) | blocks-playoff 7 (21) | made-playoffs 2016 (16) | season-assists 2013/15 (16) | playoff-wins-in-season 2019/4 (8) | month-points 2023/11/40 (15) | finals-year 2004 (24) |
| 65 | emmmhhh | season-rebounds 2023/14 (105) | points-against 16/45 (24) | road-wins-in-season 2004/20 (6) | assists-per-game 9 (19) | margin-in-season 2002/40 (6) | franchise-playoff 29 (93) | franchise-season 20/2014 (23) |
| 66 | emmmhhh | season-threes 2023/8 (44) | franchise-regular 1 (259) | threes-in-season 2008/17 (6) | free-throws 22 (21) | made-playoffs 2002 (16) | franchise-years 21/2002/2006 (56) | both-franchises 9/26 (20) |
| 67 | mmemmmh | franchise-bench 10 (243) | teammate 3206 (147) | road-wins 28 (12) | month-threes 2026/2/6 (41) | beat-in-playoffs 16 (9) | points-game7 35 (23) | franchise-playoff-season 8/2026 (17) |
| 68 | emmmhmh | month-points 2002/4/25 (69) | franchise-regular 11 (201) | held-opponent-in-season 2008/70 (13) | franchise-start 25 (138) | home-wins-in-season 2002/30 (6) | franchise-playoff 23 (46) | finals-year 2026 (22) |
| 69 | eemmhmh | rebounds 24 (52) | season-threes 2006/6 (45) | wins-in-season 2017/50 (8) | franchise-bench 28 (244) | playoff-wins-in-season 2002/1 (14) | teammate 3934672 (102) | franchise-years 26/2022/2026 (78) |
| 70 | emmmhhh | minutes 55 (84) | franchise-regular 27 (259) | road-wins-in-season 2026/25 (7) | season-points 2020/45 (19) | held-opponent-in-season 2011/70 (7) | both-franchises 19/20 (37) | franchise-playoff-season 4/2017 (15) |
| 71 | emmmmmh | finals-appearance (393) | franchise-bench 8 (219) | playoff-wins-in-season 2008/1 (15) | season-rebounds 2004/20 (20) | beat-in-playoffs 21 (10) | points-against 24/45 (17) | franchise-season 25/2021 (22) |
| 72 | mmemmmh | franchise-regular 5 (261) | teammate 4258 (166) | wins-in-season 2015/40 (16) | franchise-start 1 (164) | overtime-wins-in-season 2018/2 (6) | season-threes 2014/8 (17) | franchise-playoff-season 16/2025 (17) |
