# Prompt candidates

Written by `python3 pipeline/generate.py`; do not edit by hand.

- **Era wording:** every prompt starts with "Since 2001-02 (through 2025-26)". The data's season 2002 is the 2001-02 season (the first game is on 2001-10-30), so "Since 2002" would leave out three months of games. The schema requires the text to start with "Since" and four digits, which this does.
- **Valid answers:** the star-heavy templates (first table) need 15 to 400 players; broad-pool player families (second table) need 15 to 700; teams need at least 5 (parameterised team families at most 24 of the 30 franchises, so the answer is never nearly everyone).
- **Player tiers** come from the fame score (docs/fame-report.md). **Team tiers:** a team is tier 1 (10 points) if it qualified under its current name in any qualifying season, tier 4 (55 points) if only under a historical name. Every team answer is the franchise, shown by its current name; the other names it used are aliases for the answer matcher.
- **Difficulty:** from the number of valid answers and the share of tier 4 and above (see `difficulty()` in `pipeline/generator.py`).

## Totals

- Candidates: **3945** (3360 player, 585 team).
- Tried: 5652 template and threshold combinations. Dropped for too few valid answers: 1598. Dropped for too many: 109.
- By difficulty: easy 1199, hard 1508, medium 1238.

Templates that produced no candidates: `triple-double-finals`.

## Candidates per template (star-heavy templates, one prompt per threshold)

| template | answers | thresholds tried | candidates | dropped: too few | dropped: too many |
|---|---|---|---|---|---|
| `points-regular` | player | 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0 | 5 | 1 | 1 |
| `points-playoff` | player | 25.0, 30.0, 35.0, 40.0, 45.0, 50.0 | 6 | 0 | 0 |
| `points-finals` | player | 20.0, 25.0, 30.0, 35.0, 40.0 | 5 | 0 | 0 |
| `triple-double-regular` | player | - | 1 | 0 | 0 |
| `triple-double-playoff` | player | - | 1 | 0 | 0 |
| `triple-double-finals` | player | - | 0 | 1 | 0 |
| `rebounds` | player | 16.0, 18.0, 20.0, 22.0, 24.0, 25.0, 27.0 | 6 | 0 | 1 |
| `assists` | player | 14.0, 15.0, 16.0, 18.0, 20.0, 22.0 | 5 | 1 | 0 |
| `threes` | player | 8.0, 9.0, 10.0, 11.0, 12.0 | 4 | 1 | 0 |
| `blocks` | player | 6.0, 7.0, 8.0, 9.0, 10.0, 11.0 | 5 | 1 | 0 |
| `steals` | player | 5.0, 6.0, 7.0, 8.0, 9.0 | 3 | 1 | 1 |
| `ppg-season` | player | 20.0, 22.0, 24.0, 25.0, 26.0, 27.0, 28.0, 30.0, 32.0 | 8 | 1 | 0 |
| `franchises` | player | 4.0, 5.0, 6.0, 7.0, 8.0, 9.0 | 4 | 0 | 2 |
| `wins-season` | team | 50.0, 55.0, 58.0, 60.0, 62.0, 65.0, 67.0 | 6 | 1 | 0 |
| `wins-playoff` | team | 10.0, 12.0, 14.0, 15.0, 16.0 | 5 | 0 | 0 |
| `points-regulation` | team | 140.0, 145.0, 150.0, 155.0, 160.0 | 4 | 1 | 0 |
| `win-margin` | team | 40.0, 45.0, 50.0, 55.0, 60.0 | 4 | 1 | 0 |
| `points-game7` | player | 30.0, 35.0, 40.0 | 2 | 1 | 0 |
| `points-overtime-game` | player | 40.0, 45.0, 50.0, 55.0 | 4 | 0 | 0 |
| `points-bench` | player | 30.0, 35.0, 40.0, 45.0 | 3 | 1 | 0 |
| `points-loss` | player | 45.0, 50.0, 55.0, 60.0 | 3 | 1 | 0 |
| `points-road` | player | 45.0, 50.0, 55.0, 60.0 | 3 | 1 | 0 |
| `rebounds-playoff` | player | 16.0, 18.0, 20.0, 22.0 | 4 | 0 | 0 |
| `rebounds-finals` | player | 14.0, 16.0, 18.0, 20.0 | 2 | 2 | 0 |
| `assists-playoff` | player | 12.0, 14.0, 16.0, 18.0 | 3 | 1 | 0 |
| `assists-finals` | player | 10.0, 12.0, 14.0 | 1 | 2 | 0 |
| `threes-playoff` | player | 7.0, 8.0, 9.0, 10.0 | 2 | 2 | 0 |
| `threes-finals` | player | 6.0, 7.0, 8.0 | 1 | 2 | 0 |
| `blocks-playoff` | player | 5.0, 6.0, 7.0, 8.0 | 3 | 1 | 0 |
| `steals-playoff` | player | 4.0, 5.0, 6.0, 7.0 | 3 | 1 | 0 |
| `offensive-rebounds` | player | 9.0, 10.0, 11.0, 12.0, 14.0 | 4 | 1 | 0 |
| `free-throws` | player | 18.0, 20.0, 22.0, 24.0 | 3 | 1 | 0 |
| `turnovers` | player | 8.0, 9.0, 10.0, 11.0 | 4 | 0 | 0 |
| `shots-taken` | player | 35.0, 38.0, 40.0, 42.0 | 2 | 2 | 0 |
| `minutes` | player | 55.0, 58.0, 60.0 | 2 | 1 | 0 |
| `perfect-shooting` | player | 8.0, 9.0, 10.0, 11.0 | 4 | 0 | 0 |
| `five-by-n` | player | 3.0, 4.0, 5.0 | 2 | 1 | 0 |
| `points-and-rebounds` | player | - | 1 | 0 | 0 |
| `points-and-assists` | player | - | 1 | 0 | 0 |
| `rebounds-per-game` | player | 10.0, 11.0, 12.0, 13.0 | 3 | 1 | 0 |
| `assists-per-game` | player | 8.0, 9.0, 10.0, 11.0 | 2 | 2 | 0 |
| `steals-per-game` | player | 2.0, 3.0 | 1 | 1 | 0 |
| `blocks-per-game` | player | 2.0, 3.0 | 1 | 1 | 0 |
| `double-double-average` | player | - | 1 | 0 | 0 |
| `losses-season` | team | 55.0, 60.0, 62.0, 65.0, 67.0, 70.0 | 5 | 1 | 0 |
| `road-wins` | team | 26.0, 28.0, 30.0, 32.0 | 3 | 1 | 0 |
| `home-wins` | team | 36.0, 38.0, 39.0, 40.0 | 1 | 3 | 0 |
| `points-playoff-team` | team | 130.0, 135.0, 140.0, 145.0, 150.0 | 4 | 1 | 0 |
| `points-any-game` | team | 150.0, 155.0, 160.0, 165.0 | 3 | 1 | 0 |
| `win-margin-playoff` | team | 35.0, 40.0, 45.0 | 3 | 0 | 0 |
| `held-opponent` | team | 55.0, 60.0, 65.0, 70.0 | 3 | 1 | 0 |
| `threes-team` | team | 24.0, 26.0, 28.0, 30.0 | 3 | 1 | 0 |
| `steals-team` | team | 18.0, 20.0, 22.0, 24.0 | 2 | 2 | 0 |
| `overtime-wins` | team | 2.0, 3.0, 4.0 | 2 | 1 | 0 |
| `win-streak` | team | 14.0, 16.0, 18.0, 20.0, 22.0 | 3 | 2 | 0 |
| `champion` | team | - | 1 | 0 | 0 |
| `reached-finals` | team | - | 1 | 0 | 0 |

## Candidates per family (pools.py: one prompt per franchise, season, month, star or threshold)

Each family yields one candidate per parameter set that fits the answer window. 'tiers 1-2' and 'tiers 5-6' are shares of all valid answers over the family's candidates.

| family | answers | pool | parameter sets tried | candidates | too few | too many | valid answers | tiers 1-2 | tiers 5-6 |
|---|---|---|---|---|---|---|---|---|---|
| `franchise-regular` | player | broad | 30 | 30 | 0 | 0 | 198-293 | 29% | 25% |
| `franchise-playoff` | player | broad | 30 | 30 | 0 | 0 | 36-146 | 43% | 11% |
| `franchise-season` | player | broad | 747 | 707 | 40 | 0 | 15-35 | 41% | 16% |
| `franchise-start` | player | broad | 30 | 30 | 0 | 0 | 117-196 | 40% | 11% |
| `franchise-bench` | player | broad | 30 | 30 | 0 | 0 | 190-287 | 27% | 26% |
| `franchise-years` | player | broad | 150 | 150 | 0 | 0 | 26-87 | 34% | 22% |
| `franchise-playoff-season` | player | broad | 400 | 57 | 343 | 0 | 15-18 | 47% | 12% |
| `franchise-points` | player | broad | 120 | 98 | 22 | 0 | 15-84 | 65% | 2% |
| `both-franchises` | player | broad | 435 | 422 | 13 | 0 | 15-49 | 42% | 10% |
| `points-against` | player | broad | 120 | 116 | 4 | 0 | 15-237 | 91% | 0% |
| `teammate` | player | broad | 100 | 100 | 0 | 0 | 55-249 | 36% | 19% |
| `finals-appearance` | player | broad | 1 | 1 | 0 | 0 | 393-393 | 51% | 6% |
| `finals-three` | player | broad | 1 | 1 | 0 | 0 | 227-227 | 59% | 1% |
| `finals-steal-block` | player | broad | 1 | 1 | 0 | 0 | 296-296 | 63% | 1% |
| `finals-year` | player | broad | 25 | 25 | 0 | 0 | 21-33 | 59% | 4% |
| `month-points` | player | broad | 998 | 657 | 341 | 0 | 15-206 | 81% | 0% |
| `month-threes` | player | broad | 810 | 471 | 339 | 0 | 15-200 | 67% | 1% |
| `season-points` | player | broad | 125 | 84 | 41 | 0 | 15-161 | 87% | 0% |
| `season-threes` | player | broad | 120 | 66 | 54 | 0 | 15-154 | 69% | 1% |
| `season-rebounds` | player | broad | 100 | 97 | 3 | 0 | 15-110 | 77% | 1% |
| `season-assists` | player | broad | 100 | 69 | 31 | 0 | 15-91 | 85% | 0% |
| `made-playoffs` | team | - | 25 | 25 | 0 | 0 | 16-16 | 96% | 0% |
| `wins-in-season` | team | - | 119 | 77 | 42 | 0 | 5-20 | 97% | 0% |
| `home-wins-in-season` | team | - | 71 | 25 | 46 | 0 | 5-10 | 97% | 0% |
| `road-wins-in-season` | team | - | 95 | 48 | 47 | 0 | 5-15 | 98% | 0% |
| `playoff-wins-in-season` | team | - | 100 | 50 | 50 | 0 | 8-16 | 96% | 0% |
| `regulation-points-in-season` | team | - | 119 | 60 | 38 | 21 | 5-24 | 99% | 0% |
| `margin-in-season` | team | - | 123 | 81 | 23 | 19 | 5-24 | 96% | 0% |
| `threes-in-season` | team | - | 91 | 37 | 30 | 24 | 5-24 | 97% | 0% |
| `held-opponent-in-season` | team | - | 85 | 44 | 22 | 19 | 5-23 | 93% | 0% |
| `overtime-wins-in-season` | team | - | 65 | 27 | 17 | 21 | 6-24 | 93% | 0% |
| `played-playoff-against` | team | - | 30 | 29 | 1 | 0 | 7-19 | 95% | 0% |
| `beat-in-playoffs` | team | - | 30 | 29 | 1 | 0 | 7-18 | 96% | 0% |

### Examples

Three candidates per family (shortest, middle and longest list); the ten best-known and ten rarest answers of each are shown as name (tier).

#### `franchise-regular`

**Since 2001-02 (through 2025-26), name a player who played for the San Antonio Spurs in a regular-season game.**

198 valid answers, difficulty **medium**, tiers: 1: 22, 2: 34, 3: 50, 4: 41, 5: 34, 6: 17.

Best known: Chris Paul (1), Tim Duncan (1), Pau Gasol (1), Tony Parker (1), DeMar DeRozan (1), Andre Miller (1), LaMarcus Aldridge (1), Kawhi Leonard (1), Manu Ginobili (1), David Lee (1).

Rarest: Keith Langford (6), Derrick Byars (6), Eric Dawson (6), Marcus Williams (2008-2009) (6), Harrison Ingram (6), Matt Costello (6), Shane Heal (6), Riley Minix (6), Melvin Sanders (6), Justin Dentmon (6).

**Since 2001-02 (through 2025-26), name a player who played for the Los Angeles Lakers in a regular-season game.**

237 valid answers, difficulty **medium**, tiers: 1: 35, 2: 46, 3: 55, 4: 49, 5: 32, 6: 20.

Best known: LeBron James (1), Dwight Howard (1), Kobe Bryant (1), Russell Westbrook (1), Luka Doncic (1), Pau Gasol (1), Steve Nash (1), Anthony Davis (1), Andre Drummond (1), Rajon Rondo (1).

Rarest: Tony Bobbitt (6), Quincy Olivari (6), Elias Harris (6), Darius Johnson-Odom (6), Mike Penberthy (6), Sun Yue (6), Zach Norvell Jr. (6), Alex Fudge (6), D'Moi Hodge (6), Chaundee Brown Jr. (6).

**Since 2001-02 (through 2025-26), name a player who played for the Brooklyn Nets in a regular-season game.**

293 valid answers, difficulty **medium**, tiers: 1: 32, 2: 43, 3: 73, 4: 78, 5: 47, 6: 20.

Best known: James Harden (1), Kevin Durant (1), Kevin Garnett (1), Andre Drummond (1), Brook Lopez (1), Jason Kidd (1), DeAndre Jordan (1), Paul Pierce (1), Deron Williams (1), Andrei Kirilenko (1).

Rarest: Mile Ilic (6), Tahjere McCall (6), Yongxi Cui (6), Dennis Horner (6), Jacob Wiley (6), Kris Joseph (6), Andre Emmett (6), Kaniel Dickens (6), Steve Goodrich (6), Mitchell Creek (6).

#### `franchise-playoff`

**Since 2001-02 (through 2025-26), name a player who played for the Charlotte Hornets (including its time as the Bobcats) in a playoff game.**

36 valid answers, difficulty **hard**, tiers: 1: 9, 2: 10, 3: 10, 4: 5, 5: 2.

Best known: Tyson Chandler (1), Raymond Felton (1), Al Jefferson (1), Kemba Walker (1), Boris Diaw (1), Gerald Wallace (1), Nicolas Batum (1), D.J. Augustin (1), Luke Ridnour (1), Marvin Williams (2).

Rarest: Aaron Harrison (5), Jorge Gutierrez (5), D.J. White (4), Stephen Graham (4), Derrick Brown (4), Chris Douglas-Roberts (4), Troy Daniels (4), Frank Kaminsky (3), Gary Neal (3), Josh McRoberts (3).

**Since 2001-02 (through 2025-26), name a player who played for the Atlanta Hawks in a playoff game.**

97 valid answers, difficulty **hard**, tiers: 1: 19, 2: 22, 3: 30, 4: 17, 5: 6, 6: 3.

Best known: Dwight Howard (1), Tracy McGrady (1), Josh Smith (1), Al Horford (1), Trae Young (1), Joe Johnson (1), Paul Millsap (1), Elton Brand (1), Jamal Crawford (1), Jose Calderon (1).

Rarest: Pape Sy (6), Thomas Gardner (6), Othello Hunter (6), Jeremy Richardson (5), Randolph Morris (5), Lamar Patterson (5), Mario West (5), Nathan Knight (5), Asa Newell (5), John Jenkins (4).

**Since 2001-02 (through 2025-26), name a player who played for the Boston Celtics in a playoff game.**

146 valid answers, difficulty **medium**, tiers: 1: 25, 2: 29, 3: 35, 4: 34, 5: 19, 6: 4.

Best known: Kevin Garnett (1), Rajon Rondo (1), Nikola Vucevic (1), Paul Pierce (1), Al Horford (1), Jrue Holiday (1), Jayson Tatum (1), Isaiah Thomas (1), Jaylen Brown (1), Kyrie Irving (1).

Rarest: Max Shulga (6), Malik Fitts (6), John Holland (6), Amari Williams (6), Vincent Poirier (5), RJ Hunter (5), Mark Bryant (5), Ron Harper Jr. (5), Juwan Morgan (5), Luigi Datome (5).

#### `franchise-season`

**Since 2001-02 (through 2025-26), name a player who played for the Atlanta Hawks in a regular-season game in the 2005-06 season.**

15 valid answers, difficulty **hard**, tiers: 1: 3, 2: 2, 3: 3, 4: 2, 5: 4, 6: 1.

Best known: Josh Smith (1), Joe Johnson (1), Zaza Pachulia (1), Marvin Williams (2), Al Harrington (2), Tyronn Lue (3), Josh Childress (3), Tony Delk (3), Royal Ivey (4), Salim Stoudamire (4).

Rarest: Anthony Grundy (6), John Edwards (5), Donta Smith (5), John Thomas (5), Esteban Batista (5), Salim Stoudamire (4), Royal Ivey (4), Tony Delk (3), Josh Childress (3), Tyronn Lue (3).

**Since 2001-02 (through 2025-26), name a player who played for the Charlotte Bobcats in a regular-season game in the 2006-07 season.**

18 valid answers, difficulty **hard**, tiers: 1: 2, 2: 3, 3: 6, 4: 7.

Best known: Raymond Felton (1), Gerald Wallace (1), Emeka Okafor (2), Brevin Knight (2), Jeff McInnis (2), Derek Anderson (3), Primoz Brezec (3), Matt Carroll (3), Othella Harrington (3), Jake Voskuhl (3).

Rarest: Bernard Robinson (4), Sean May (4), Walter Herrmann Heinrich (4), Melvin Ely (4), Alan Anderson (4), Eric Williams (4), Ryan Hollins (4), Adam Morrison (3), Jake Voskuhl (3), Othella Harrington (3).

**Since 2001-02 (through 2025-26), name a player who played for the Memphis Grizzlies in a regular-season game in the 2023-24 season.**

35 valid answers, difficulty **hard**, tiers: 1: 3, 2: 4, 3: 5, 4: 14, 5: 5, 6: 4.

Best known: Ja Morant (1), Derrick Rose (1), Marcus Smart (1), Desmond Bane (2), Victor Oladipo (2), Jaren Jackson Jr. (2), Bismack Biyombo (2), Luke Kennard (3), GG Jackson (3), Santi Aldama (3).

Rarest: Timmy Allen (6), Matt Hurt (6), Jack White (6), Maozinha Pereira (6), Kenneth Lofton Jr. (5), Zavier Simpson (5), DeJon Jarreau (5), Tosan Evbuomwan (5), Trey Jemison III (5), Jacob Gilyard (4).

#### `franchise-start`

**Since 2001-02 (through 2025-26), name a player who started a game for the San Antonio Spurs.**

117 valid answers, difficulty **medium**, tiers: 1: 22, 2: 30, 3: 31, 4: 22, 5: 12.

Best known: Chris Paul (1), Tim Duncan (1), Pau Gasol (1), Tony Parker (1), DeMar DeRozan (1), Andre Miller (1), LaMarcus Aldridge (1), Kawhi Leonard (1), Manu Ginobili (1), David Lee (1).

Rarest: Jeremy Richardson (5), Nicolas Laprovittola (5), Mark Bryant (5), Othyus Jeffers (5), James White (5), Brandon Paul (5), Damion James (5), Luka Samanic (5), Cherokee Parks (5), Danny Ferry (5).

**Since 2001-02 (through 2025-26), name a player who started a game for the Miami Heat.**

158 valid answers, difficulty **medium**, tiers: 1: 23, 2: 41, 3: 47, 4: 30, 5: 14, 6: 3.

Best known: LeBron James (1), Kyle Lowry (1), Dwyane Wade (1), Shawn Marion (1), Kevin Love (1), Andre Iguodala (1), Joe Johnson (1), Chris Bosh (1), Ray Allen (1), Shaquille O'Neal (1).

Rarest: Zoran Dragic (6), Tang Hamilton (6), Sam Mack (6), Kasib Powell (5), Terrel Harris (5), Dexter Pittman (5), Okaro White (5), Stephane Lasme (5), Jordan Mickey (5), Luke Jackson (5).

**Since 2001-02 (through 2025-26), name a player who started a game for the Brooklyn Nets.**

196 valid answers, difficulty **medium**, tiers: 1: 29, 2: 37, 3: 62, 4: 49, 5: 18, 6: 1.

Best known: James Harden (1), Kevin Durant (1), Kevin Garnett (1), Andre Drummond (1), Brook Lopez (1), Jason Kidd (1), DeAndre Jordan (1), Paul Pierce (1), Deron Williams (1), Andrei Kirilenko (1).

Rarest: Trevon Scott (2026) (6), Maxwell Lewis (5), E.J. Liddell (5), Chaney Johnson (5), Drew Timme (5), David Duke Jr. (5), Malachi Smith (5), Tyson Etienne (5), Tyshawn Taylor (5), Damion James (5).

#### `franchise-bench`

**Since 2001-02 (through 2025-26), name a player who came off the bench in a game for the Indiana Pacers.**

190 valid answers, difficulty **medium**, tiers: 1: 16, 2: 32, 3: 49, 4: 41, 5: 37, 6: 15.

Best known: Paul George (1), Al Jefferson (1), Myles Turner (1), David West (1), Domantas Sabonis (1), Metta World Peace (1), Tristan Thompson (1), Danny Granger (1), Monta Ellis (1), Jermaine O'Neal (1).

Rarest: Trey McKinney-Jones (6), Ahmad Caver (6), Ben Moore (6), Courtney Sims (6), Tristen Newton (6), Brian Bowen II (6), Jalen Lecque (6), Norman Richardson (6), Ike Anigbogu (6), Amida Brimah (6).

**Since 2001-02 (through 2025-26), name a player who came off the bench in a game for the Los Angeles Lakers.**

231 valid answers, difficulty **medium**, tiers: 1: 32, 2: 42, 3: 55, 4: 50, 5: 32, 6: 20.

Best known: LeBron James (1), Dwight Howard (1), Kobe Bryant (1), Russell Westbrook (1), Pau Gasol (1), Steve Nash (1), Anthony Davis (1), Rajon Rondo (1), Brook Lopez (1), Carmelo Anthony (1).

Rarest: Tony Bobbitt (6), Quincy Olivari (6), Elias Harris (6), Darius Johnson-Odom (6), Mike Penberthy (6), Sun Yue (6), Zach Norvell Jr. (6), Alex Fudge (6), D'Moi Hodge (6), Chaundee Brown Jr. (6).

**Since 2001-02 (through 2025-26), name a player who came off the bench in a game for the Brooklyn Nets.**

287 valid answers, difficulty **medium**, tiers: 1: 27, 2: 42, 3: 73, 4: 78, 5: 47, 6: 20.

Best known: James Harden (1), Kevin Durant (1), Brook Lopez (1), Jason Kidd (1), DeAndre Jordan (1), Paul Pierce (1), Deron Williams (1), Andrei Kirilenko (1), LaMarcus Aldridge (1), Vince Carter (1).

Rarest: Mile Ilic (6), Tahjere McCall (6), Yongxi Cui (6), Dennis Horner (6), Jacob Wiley (6), Kris Joseph (6), Andre Emmett (6), Kaniel Dickens (6), Steve Goodrich (6), Mitchell Creek (6).

#### `franchise-years`

**Since 2001-02 (through 2025-26), name a player who played for the Charlotte Hornets (including its time as the Bobcats) in a regular-season game between the 2001-02 and 2005-06 seasons.**

26 valid answers, difficulty **hard**, tiers: 1: 2, 2: 2, 3: 10, 4: 7, 5: 5.

Best known: Raymond Felton (1), Gerald Wallace (1), Emeka Okafor (2), Brevin Knight (2), Eddie House (3), Keith Bogans (3), Primoz Brezec (3), Jumaine Jones (3), Jason Hart (3), Matt Carroll (3).

Rarest: Cory Alexander (5), Tamar Slay (5), Kevin Burleson (5), Theron Smith (5), Jamal Sampson (5), Bernard Robinson (4), Lonny Baxter (4), Sean May (4), Jahidi White (4), Kareem Rush (4).

**Since 2001-02 (through 2025-26), name a player who played for the Washington Wizards in a regular-season game between the 2006-07 and 2010-11 seasons.**

54 valid answers, difficulty **hard**, tiers: 1: 6, 2: 12, 3: 13, 4: 10, 5: 9, 6: 4.

Best known: John Wall (1), Gilbert Arenas (1), Kirk Hinrich (1), Mike Bibby (1), Antawn Jamison (1), JaVale McGee (1), Rashard Lewis (2), Brendan Haywood (2), Caron Butler (2), Shaun Livingston (2).

Rarest: Mike Hall (6), James Lang (6), Hamady Ndiaye (6), Cedric Jackson (6), Larry Owens (5), Mustafa Shakur (5), Othyus Jeffers (5), Mike Harris (5), Paul Davis (5), Lester Hudson (5).

**Since 2001-02 (through 2025-26), name a player who played for the Washington Wizards in a regular-season game between the 2021-22 and 2025-26 seasons.**

87 valid answers, difficulty **hard**, tiers: 1: 8, 2: 15, 3: 20, 4: 18, 5: 16, 6: 10.

Best known: Bradley Beal (1), Trae Young (1), Jonas Valanciunas (1), CJ McCollum (1), Deni Avdija (1), Taj Gibson (1), Marcus Smart (1), Khris Middleton (1), Kristaps Porzingis (2), Tyus Jones (2).

Rarest: Jaime Echenique (6), Erik Stevenson (6), Jordan Schakel (6), Joel Ayayi (6), Craig Sword (6), Isaiah Todd (6), Kadary Richmond (6), Keshon Gilbert (6), Alondes Williams (6), Xavier Cooks (6).

#### `franchise-playoff-season`

**Since 2001-02 (through 2025-26), name a player who played for the Atlanta Hawks in a playoff game in the 2008-09 season.**

15 valid answers, difficulty **hard**, tiers: 1: 5, 2: 1, 3: 3, 4: 2, 5: 2, 6: 2.

Best known: Josh Smith (1), Al Horford (1), Joe Johnson (1), Mike Bibby (1), Zaza Pachulia (1), Marvin Williams (2), Speedy Claxton (3), Ronald Murray (3), Maurice Evans (3), Acie Law (4).

Rarest: Thomas Gardner (6), Othello Hunter (6), Randolph Morris (5), Mario West (5), Solomon Jones (4), Acie Law (4), Maurice Evans (3), Ronald Murray (3), Speedy Claxton (3), Marvin Williams (2).

**Since 2001-02 (through 2025-26), name a player who played for the Philadelphia 76ers in a playoff game in the 2018-19 season.**

15 valid answers, difficulty **hard**, tiers: 1: 4, 2: 4, 3: 2, 4: 3, 5: 1, 6: 1.

Best known: Joel Embiid (1), Jimmy Butler III (1), Tobias Harris (1), T.J. McConnell (1), JJ Redick (2), Greg Monroe (2), Amir Johnson (2), Ben Simmons (2), Jonathon Simmons (3), Mike Scott (3).

Rarest: Zhaire Smith (6), Jonah Bolden (5), Furkan Korkmaz (4), Boban Marjanovic (4), James Ennis III (4), Mike Scott (3), Jonathon Simmons (3), Ben Simmons (2), Amir Johnson (2), Greg Monroe (2).

**Since 2001-02 (through 2025-26), name a player who played for the New York Knicks in a playoff game in the 2025-26 season.**

18 valid answers, difficulty **hard**, tiers: 1: 2, 2: 5, 3: 4, 4: 1, 5: 6.

Best known: Jalen Brunson (1), Karl-Anthony Towns (1), Jordan Clarkson (2), Josh Hart (2), Mikal Bridges (2), OG Anunoby (2), Mitchell Robinson (2), Jose Alvarado (3), Landry Shamet (3), Miles McBride (3).

Rarest: Pacome Dadiet (5), Kevin McCullar Jr. (5), Mohamed Diawara (5), Dillon Jones (5), Ariel Hukporti (5), Trey Jemison III (5), Tyler Kolek (4), Jeremy Sochan (3), Miles McBride (3), Landry Shamet (3).

#### `franchise-points`

**Since 2001-02 (through 2025-26), name a player who scored 35 or more points in a game for the Philadelphia 76ers.**

15 valid answers, difficulty **medium**, tiers: 1: 8, 2: 1, 3: 5, 4: 1.

Best known: James Harden (1), Joel Embiid (1), Allen Iverson (1), Jrue Holiday (1), Paul George (1), Tyrese Maxey (1), Jimmy Butler III (1), Tobias Harris (1), Ben Simmons (2), VJ Edgecombe (3).

Rarest: James Anderson (4), Shake Milton (3), Quentin Grimes (3), Seth Curry (3), Willie Green (3), VJ Edgecombe (3), Ben Simmons (2), Tobias Harris (1), Jimmy Butler III (1), Tyrese Maxey (1).

**Since 2001-02 (through 2025-26), name a player who scored 30 or more points in a game for the Brooklyn Nets.**

41 valid answers, difficulty **easy**, tiers: 1: 16, 2: 10, 3: 13, 4: 2.

Best known: James Harden (1), Kevin Durant (1), Brook Lopez (1), Jason Kidd (1), Paul Pierce (1), Deron Williams (1), Joe Johnson (1), Vince Carter (1), Kyrie Irving (1), Dennis Schroder (1).

Rarest: Tyrese Martin (4), Chris Douglas-Roberts (4), Yi Jianlian (3), Mirza Teletovic (3), Noah Clowney (3), Landry Shamet (3), Sean Kilpatrick (3), Allen Crabbe (3), Shabazz Napier (3), Kerry Kittles (3).

**Since 2001-02 (through 2025-26), name a player who scored 25 or more points in a game for the New York Knicks.**

84 valid answers, difficulty **medium**, tiers: 1: 17, 2: 34, 3: 21, 4: 11, 5: 1.

Best known: Carmelo Anthony (1), Tracy McGrady (1), Tyson Chandler (1), Zach Randolph (1), Chauncey Billups (1), Jalen Brunson (1), Marcus Camby (1), Karl-Anthony Towns (1), Jamal Crawford (1), Raymond Felton (1).

Rarest: Kadeem Allen (5), Henry Walker (4), Chris Copeland (4), Shawne Williams (4), Steve Novak (4), Mario Hezonja (4), Shandon Anderson (4), Landry Fields (4), Alexey Shved (4), Cam Reddish (4).

#### `both-franchises`

**Since 2001-02 (through 2025-26), name a player who played for both the Indiana Pacers and the Miami Heat.**

15 valid answers, difficulty **hard**, tiers: 1: 2, 2: 3, 3: 8, 4: 2.

Best known: Danny Granger (1), Jermaine O'Neal (1), Victor Oladipo (2), James Johnson (2), James Posey (2), Gerald Green (3), Rasual Butler (3), Thomas Bryant (3), Josh McRoberts (3), Travis Best (3).

Rarest: Shawne Williams (4), Samaki Walker (4), Solomon Hill (3), Luther Head (3), James Jones (3), Travis Best (3), Josh McRoberts (3), Thomas Bryant (3), Rasual Butler (3), Gerald Green (3).

**Since 2001-02 (through 2025-26), name a player who played for both the Brooklyn Nets and the Charlotte Hornets (including its time as the Bobcats).**

27 valid answers, difficulty **hard**, tiers: 1: 2, 2: 6, 3: 9, 4: 8, 5: 2.

Best known: Gerald Wallace (1), Mason Plumlee (1), Shaun Livingston (2), Jeremy Lin (2), Courtney Lee (2), Jeff McInnis (2), Jared Dudley (2), DeSagana Diop (2), Garrett Temple (3), Dante Cunningham (3).

Rarest: Tamar Slay (5), Jorge Gutierrez (5), Treveon Graham (4), Bernard Robinson (4), Justin Hamilton (4), Stephen Graham (4), Linton Johnson (4), Chris Douglas-Roberts (4), Alan Anderson (4), Eric Williams (4).

**Since 2001-02 (through 2025-26), name a player who played for both the Dallas Mavericks and the Brooklyn Nets.**

49 valid answers, difficulty **medium**, tiers: 1: 9, 2: 12, 3: 16, 4: 11, 5: 1.

Best known: Jason Kidd (1), DeAndre Jordan (1), Deron Williams (1), Vince Carter (1), Kyrie Irving (1), Jason Terry (1), Richard Jefferson (1), Devin Harris (1), D'Angelo Russell (1), Troy Murphy (2).

Rarest: Maurice Ager (5), Theo Pinson (4), Kessler Edwards (4), Justin Anderson (4), Sean Williams (4), Antoine Wright (4), Moses Brown (4), Donnell Harvey (4), Chris Douglas-Roberts (4), Shawne Williams (4).

#### `points-against`

**Since 2001-02 (through 2025-26), name a player who scored 45 or more points against the Cleveland Cavaliers in a game.**

15 valid answers, difficulty **medium**, tiers: 1: 12, 2: 3.

Best known: LeBron James (1), James Harden (1), Luka Doncic (1), Allen Iverson (1), Damian Lillard (1), Paul Pierce (1), Giannis Antetokounmpo (1), Jayson Tatum (1), Gilbert Arenas (1), Jalen Brunson (1).

Rarest: Jordan Poole (2), Miles Bridges (2), Victor Oladipo (2), Jamal Murray (1), Manu Ginobili (1), Jalen Brunson (1), Gilbert Arenas (1), Jayson Tatum (1), Giannis Antetokounmpo (1), Paul Pierce (1).

**Since 2001-02 (through 2025-26), name a player who scored 35 or more points against the Chicago Bulls in a game.**

90 valid answers, difficulty **easy**, tiers: 1: 62, 2: 21, 3: 7.

Best known: LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Chris Paul (1), Russell Westbrook (1), Luka Doncic (1), Joel Embiid (1), Dirk Nowitzki (1).

Rarest: Stanley Johnson (3), Juan Dixon (3), Allen Crabbe (3), Chris Boucher (3), Brice Sensabaugh (3), Taurean Prince (3), Lamond Murray (3), Will Barton (2), Wally Szczerbiak (2), Kevin Porter Jr. (2).

**Since 2001-02 (through 2025-26), name a player who scored 30 or more points against the New York Knicks in a game.**

237 valid answers, difficulty **easy**, tiers: 1: 123, 2: 85, 3: 23, 4: 6.

Best known: LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Chris Paul (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Pau Gasol (1).

Rarest: Mike Taylor (4), Justin Champagnie (4), Tre Mann (4), Alan Anderson (4), Julian Champagnie (4), Sandro Mamukelashvili (4), Hamidou Diallo (3), Isaiah Joe (3), Moritz Wagner (3), Noah Clowney (3).

#### `teammate`

**Since 2001-02 (through 2025-26), name a player who played in the same game as Anthony Edwards for the same team.**

55 valid answers, difficulty **hard**, tiers: 1: 6, 2: 8, 3: 13, 4: 15, 5: 9, 6: 4.

Best known: Rudy Gobert (1), Mike Conley (1), Karl-Anthony Towns (1), Ricky Rubio (1), Julius Randle (1), D'Angelo Russell (1), Greg Monroe (2), Joe Ingles (2), Ed Davis (2), Kyle Anderson (2).

Rarest: Jesse Edwards (6), Tristen Newton (6), Rocco Zikarsky (6), Enrique Freeman (6), Leandro Bolmaro (5), Ashton Hagans (5), McKinley Wright IV (5), Matt Ryan (5), Joan Beringer (5), Wendell Moore Jr. (5).

**Since 2001-02 (through 2025-26), name a player who played in the same game as Kevin Garnett for the same team.**

150 valid answers, difficulty **medium**, tiers: 1: 24, 2: 29, 3: 31, 4: 31, 5: 31, 6: 4.

Best known: Rajon Rondo (1), Brook Lopez (1), Andre Miller (1), Paul Pierce (1), Deron Williams (1), Andrei Kirilenko (1), Joe Johnson (1), Chauncey Billups (1), Karl-Anthony Towns (1), Ricky Rubio (1).

Rarest: Kris Joseph (6), Fab Melo (6), Ndudi Ebi (6), Marcus Landry (6), Tornike Shengelia (5), Reggie Slater (5), J.R. Giddens (5), Dean Garrett (5), JaJuan Johnson (5), Bracey Wright (5).

**Since 2001-02 (through 2025-26), name a player who played in the same game as Chris Paul for the same team.**

249 valid answers, difficulty **medium**, tiers: 1: 43, 2: 52, 3: 57, 4: 52, 5: 23, 6: 22.

Best known: James Harden (1), Kevin Durant (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Brook Lopez (1), Carmelo Anthony (1), Josh Smith (1), DeAndre Jordan (1), Tyson Chandler (1), Paul Pierce (1).

Rarest: Vincent Edwards (6), Jahmyl Telfort (6), Branden Dawson (6), Paris Bass (6), Diamond Stone (6), Patrick Ewing Jr. (6), MJ Walker (6), Aaron Jackson (6), Harrison Ingram (6), Travis Leslie (6).

#### `finals-appearance`

**Since 2001-02 (through 2025-26), name a player who appeared in an NBA Finals game.**

393 valid answers, difficulty **easy**, tiers: 1: 97, 2: 102, 3: 104, 4: 65, 5: 19, 6: 6.

Best known: LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Chris Paul (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Pau Gasol (1).

Rarest: Ty-Shon Alexander (6), Elijah Bryant (6), Malik Fitts (6), Donny Marshall (6), Alex Ducas (6), Enrique Freeman (6), Adam Flagler (5), Malcolm Miller (5), Juwan Morgan (5), Terrel Harris (5).

#### `finals-three`

**Since 2001-02 (through 2025-26), name a player who made a three-pointer in an NBA Finals game.**

227 valid answers, difficulty **easy**, tiers: 1: 72, 2: 62, 3: 65, 4: 26, 5: 1, 6: 1.

Best known: LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Chris Paul (1), Russell Westbrook (1), Luka Doncic (1), Dirk Nowitzki (1), Stephen Curry (1).

Rarest: Malik Fitts (6), Carter Bryant (5), Steve Kerr (4), Alfonzo McKinnie (4), Brian Shaw (4), Ousmane Dieng (4), Ben Sheppard (4), Patrick McCaw (4), Jordan Nwora (4), Quinn Cook (4).

#### `finals-steal-block`

**Since 2001-02 (through 2025-26), name a player who recorded a steal or a block in an NBA Finals game.**

296 valid answers, difficulty **easy**, tiers: 1: 96, 2: 90, 3: 77, 4: 30, 5: 3.

Best known: LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Chris Paul (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Pau Gasol (1).

Rarest: Carter Bryant (5), Ariel Hukporti (5), James Michael McAdoo (5), Steve Kerr (4), Brian Shaw (4), Didier Ilunga-Mbenga (4), Ousmane Dieng (4), Ben Sheppard (4), Jordan Bell (4), Patrick McCaw (4).

#### `finals-year`

**Since 2001-02 (through 2025-26), name a player who appeared in the 2011 NBA Finals.**

21 valid answers, difficulty **medium**, tiers: 1: 11, 2: 5, 3: 4, 4: 1.

Best known: LeBron James (1), Dirk Nowitzki (1), Jason Kidd (1), Dwyane Wade (1), Tyson Chandler (1), Shawn Marion (1), Chris Bosh (1), Jason Terry (1), Mike Bibby (1), Udonis Haslem (1).

Rarest: Brian Cardinal (4), Eddie House (3), Joel Anthony (3), DeShawn Stevenson (3), Ian Mahinmi (3), Juwan Howard (2), Mike Miller (2), Mario Chalmers (2), Brendan Haywood (2), J.J. Barea (2).

**Since 2001-02 (through 2025-26), name a player who appeared in the 2010 NBA Finals.**

25 valid answers, difficulty **hard**, tiers: 1: 10, 2: 5, 3: 7, 4: 3.

Best known: Kobe Bryant (1), Pau Gasol (1), Kevin Garnett (1), Rajon Rondo (1), Paul Pierce (1), Ray Allen (1), Lamar Odom (1), Metta World Peace (1), Rasheed Wallace (1), Tony Allen (1).

Rarest: Didier Ilunga-Mbenga (4), Josh Powell (4), Brian Scalabrine (4), Shannon Brown (3), Shelden Williams (3), Sasha Vujacic (3), Marquis Daniels (3), Glen Davis (3), Luke Walton (3), Jordan Farmar (3).

**Since 2001-02 (through 2025-26), name a player who appeared in the 2025 NBA Finals.**

33 valid answers, difficulty **hard**, tiers: 1: 4, 2: 5, 3: 12, 4: 5, 5: 5, 6: 2.

Best known: Shai Gilgeous-Alexander (1), Myles Turner (1), T.J. McConnell (1), Pascal Siakam (1), Tyrese Haliburton (2), Jalen Williams (2), James Johnson (2), Alex Caruso (2), Isaiah Hartenstein (2), Bennedict Mathurin (3).

Rarest: Alex Ducas (6), Enrique Freeman (6), Adam Flagler (5), RayJ Dennis (5), Dillon Jones (5), Johnny Furphy (5), Branden Carlson (5), Ousmane Dieng (4), Ben Sheppard (4), Quenton Jackson (4).

#### `month-points`

**Since 2001-02 (through 2025-26), name a player who scored 25 or more points in a regular-season game in October 2002.**

15 valid answers, difficulty **medium**, tiers: 1: 9, 2: 5, 3: 1.

Best known: Kobe Bryant (1), Pau Gasol (1), Allen Iverson (1), Tracy McGrady (1), Paul Pierce (1), Ray Allen (1), Antawn Jamison (1), Rasheed Wallace (1), Peja Stojakovic (1), Allan Houston (2).

Rarest: Gordan Giricek (3), Brent Barry (2), Ricky Davis (2), Glenn Robinson (2), Steve Francis (2), Allan Houston (2), Peja Stojakovic (1), Rasheed Wallace (1), Antawn Jamison (1), Ray Allen (1).

**Since 2001-02 (through 2025-26), name a player who scored 20 or more points in a regular-season game in October 2015.**

63 valid answers, difficulty **easy**, tiers: 1: 43, 2: 16, 3: 4.

Best known: LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Russell Westbrook (1), Stephen Curry (1), Anthony Davis (1), Andre Drummond (1), Rajon Rondo (1), Damian Lillard (1).

Rarest: Derrick Williams (3), Nikola Mirotic (3), DeMarre Carroll (3), Jahlil Okafor (3), Michael Carter-Williams (2), Terrence Ross (2), Ryan Anderson (2), Brandon Knight (2), Evan Fournier (2), Marcus Morris Sr. (2).

**Since 2001-02 (through 2025-26), name a player who scored 20 or more points in a regular-season game in March 2025.**

206 valid answers, difficulty **easy**, tiers: 1: 55, 2: 56, 3: 61, 4: 29, 5: 5.

Best known: LeBron James (1), James Harden (1), Kevin Durant (1), Russell Westbrook (1), Luka Doncic (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Andre Drummond (1), Damian Lillard (1), Brook Lopez (1).

Rarest: Jared Rhoden (5), Colby Jones (5), A.J. Lawson (5), AJ Johnson (5), Kai Jones (5), Baylor Scheierman (4), DaQuan Jeffries (4), Kessler Edwards (4), Orlando Robinson (4), Jeff Dowtin Jr. (4).

#### `month-threes`

**Since 2001-02 (through 2025-26), name a player who made 4 or more three-pointers in a regular-season game in October 2013.**

15 valid answers, difficulty **medium**, tiers: 1: 11, 2: 3, 3: 1.

Best known: LeBron James (1), Dirk Nowitzki (1), Stephen Curry (1), Damian Lillard (1), Paul George (1), Chauncey Billups (1), Klay Thompson (1), Jason Terry (1), Ray Allen (1), Trevor Ariza (1).

Rarest: Francisco Garcia (3), Michael Carter-Williams (2), Mario Chalmers (2), George Hill (2), Shane Battier (1), Trevor Ariza (1), Ray Allen (1), Jason Terry (1), Klay Thompson (1), Chauncey Billups (1).

**Since 2001-02 (through 2025-26), name a player who made 5 or more three-pointers in a regular-season game in October 2022.**

49 valid answers, difficulty **easy**, tiers: 1: 23, 2: 17, 3: 8, 4: 1.

Best known: James Harden (1), Stephen Curry (1), Damian Lillard (1), Brook Lopez (1), Kyle Lowry (1), Nikola Vucevic (1), Mike Conley (1), Jrue Holiday (1), Kevin Love (1), Jayson Tatum (1).

Rarest: Dean Wade (4), Bones Hyland (3), Chris Duarte (3), Max Strus (3), Doug McDermott (3), Davion Mitchell (3), Josh Richardson (3), Bennedict Mathurin (3), Kevin Huerter (3), Gary Trent Jr. (2).

**Since 2001-02 (through 2025-26), name a player who made 4 or more three-pointers in a regular-season game in March 2025.**

200 valid answers, difficulty **easy**, tiers: 1: 44, 2: 46, 3: 62, 4: 44, 5: 4.

Best known: LeBron James (1), James Harden (1), Kevin Durant (1), Chris Paul (1), Russell Westbrook (1), Luka Doncic (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Damian Lillard (1), DeMar DeRozan (1).

Rarest: Jalen Hood-Schifino (5), Jared Rhoden (5), Colby Jones (5), A.J. Lawson (5), Caleb Houstan (4), Baylor Scheierman (4), DaQuan Jeffries (4), Antonio Reeves (4), Jeff Dowtin Jr. (4), Jamison Battle (4).

#### `season-points`

**Since 2001-02 (through 2025-26), name a player who scored 45 or more points in a regular-season game in the 2008-09 season.**

15 valid answers, difficulty **medium**, tiers: 1: 13, 2: 2.

Best known: LeBron James (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Dirk Nowitzki (1), Carmelo Anthony (1), Tony Parker (1), Dwyane Wade (1), Jamal Crawford (1), Shaquille O'Neal (1).

Rarest: Brandon Roy (2), JR Smith (2), Kevin Martin (1), Devin Harris (1), Amar'e Stoudemire (1), Shaquille O'Neal (1), Jamal Crawford (1), Dwyane Wade (1), Tony Parker (1), Carmelo Anthony (1).

**Since 2001-02 (through 2025-26), name a player who scored 35 or more points in a regular-season game in the 2004-05 season.**

54 valid answers, difficulty **easy**, tiers: 1: 34, 2: 16, 3: 4.

Best known: LeBron James (1), Kobe Bryant (1), Tim Duncan (1), Dirk Nowitzki (1), Kevin Garnett (1), Allen Iverson (1), Jason Kidd (1), Carmelo Anthony (1), Tony Parker (1), Tracy McGrady (1).

Rarest: Bob Sura (3), Darius Miles (3), Tim Thomas (3), Morris Peterson (3), Reggie Miller (2), Donyell Marshall (2), Quentin Richardson (2), Grant Hill (2), Damon Stoudamire (2), Ricky Davis (2).

**Since 2001-02 (through 2025-26), name a player who scored 30 or more points in a regular-season game in the 2025-26 season.**

161 valid answers, difficulty **easy**, tiers: 1: 53, 2: 47, 3: 41, 4: 16, 5: 4.

Best known: LeBron James (1), James Harden (1), Kevin Durant (1), Luka Doncic (1), Joel Embiid (1), Stephen Curry (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Brook Lopez (1), DeMar DeRozan (1).

Rarest: Blake Hinson (5), Jett Howard (5), Terrence Shannon Jr. (5), Kennedy Chandler (5), Will Richard (4), Baylor Scheierman (4), Rayan Rupert (4), Ousmane Dieng (4), Nique Clifford (4), Cody Williams (4).

#### `season-threes`

**Since 2001-02 (through 2025-26), name a player who made 8 or more three-pointers in a regular-season game in the 2015-16 season.**

15 valid answers, difficulty **medium**, tiers: 1: 7, 2: 4, 3: 3, 4: 1.

Best known: Stephen Curry (1), Damian Lillard (1), Paul George (1), Klay Thompson (1), Trevor Ariza (1), D'Angelo Russell (1), Khris Middleton (1), JR Smith (2), JJ Redick (2), Wesley Matthews (2).

Rarest: Troy Daniels (4), Rodney Hood (3), Omri Casspi (3), Nikola Mirotic (3), CJ Miles (2), Wesley Matthews (2), JJ Redick (2), JR Smith (2), Khris Middleton (1), D'Angelo Russell (1).

**Since 2001-02 (through 2025-26), name a player who made 6 or more three-pointers in a regular-season game in the 2011-12 season.**

44 valid answers, difficulty **easy**, tiers: 1: 18, 2: 16, 3: 7, 4: 2, 5: 1.

Best known: Stephen Curry (1), Kyle Lowry (1), Deron Williams (1), Jrue Holiday (1), Kevin Love (1), Joe Johnson (1), Paul George (1), Chauncey Billups (1), Kyrie Irving (1), Ray Allen (1).

Rarest: Lester Hudson (5), Henry Walker (4), Steve Novak (4), Shannon Brown (3), James Jones (3), Carlos Delfino (3), Anthony Morrow (3), Jodie Meeks (3), Dorell Wright (3), Jordan Farmar (3).

**Since 2001-02 (through 2025-26), name a player who made 6 or more three-pointers in a regular-season game in the 2025-26 season.**

154 valid answers, difficulty **easy**, tiers: 1: 37, 2: 34, 3: 47, 4: 29, 5: 6, 6: 1.

Best known: James Harden (1), Kevin Durant (1), Russell Westbrook (1), Luka Doncic (1), Stephen Curry (1), Brook Lopez (1), Al Horford (1), Jrue Holiday (1), Trae Young (1), Paul George (1).

Rarest: Koby Brea (6), Adama Bal (5), John Poulakidas (5), Ron Harper Jr. (5), Dariq Whitehead (5), Tyson Etienne (5), Daeqwon Plowden (5), Devin Carter (4), Kasparas Jakucionis (4), Baylor Scheierman (4).

#### `season-rebounds`

**Since 2001-02 (through 2025-26), name a player who grabbed 20 or more rebounds in a regular-season game in the 2001-02 season.**

15 valid answers, difficulty **hard**, tiers: 1: 6, 2: 4, 3: 3, 4: 2.

Best known: Tim Duncan (1), Dirk Nowitzki (1), Kevin Garnett (1), Ben Wallace (1), Elton Brand (1), Marcus Camby (1), Kurt Thomas (2), P.J. Brown (2), Donyell Marshall (2), Dikembe Mutombo (2).

Rarest: Hakeem Olajuwon (4), Clarence Weatherspoon (4), Danny Fortson (3), Michael Olowokandi (3), Lorenzen Wright (3), Dikembe Mutombo (2), Donyell Marshall (2), P.J. Brown (2), Kurt Thomas (2), Marcus Camby (1).

**Since 2001-02 (through 2025-26), name a player who grabbed 16 or more rebounds in a regular-season game in the 2011-12 season.**

49 valid answers, difficulty **easy**, tiers: 1: 28, 2: 16, 3: 3, 4: 1, 5: 1.

Best known: Dwight Howard (1), Kevin Durant (1), Tim Duncan (1), Pau Gasol (1), Dirk Nowitzki (1), Rajon Rondo (1), Josh Smith (1), DeAndre Jordan (1), Tyson Chandler (1), Kevin Love (1).

Rarest: Solomon Alabi (5), Gustavo Alfonso Ayon (4), Glen Davis (3), Trevor Booker (3), Nikola Pekovic (3), Luc Mbah a Moute (2), Marreese Speights (2), Ryan Anderson (2), Andrew Bynum (2), Jason Thompson (2).

**Since 2001-02 (through 2025-26), name a player who grabbed 14 or more rebounds in a regular-season game in the 2024-25 season.**

110 valid answers, difficulty **easy**, tiers: 1: 32, 2: 28, 3: 26, 4: 21, 5: 3.

Best known: LeBron James (1), Russell Westbrook (1), Luka Doncic (1), Joel Embiid (1), Anthony Davis (1), Andre Drummond (1), Rudy Gobert (1), DeAndre Jordan (1), Nikola Vucevic (1), Giannis Antetokounmpo (1).

Rarest: Marcus Bagley (5), Colin Castleton (5), Oscar Tshiebwe (5), Jonathan Mogbo (4), Tidjane Salaun (4), Charles Bassey (4), Mouhamed Gueye (4), Adem Bona (4), Bol Bol (4), Trayce Jackson-Davis (4).

#### `season-assists`

**Since 2001-02 (through 2025-26), name a player who recorded 15 or more assists in a regular-season game in the 2002-03 season.**

15 valid answers, difficulty **medium**, tiers: 1: 7, 2: 7, 3: 1.

Best known: Steve Nash (1), Jason Kidd (1), Andre Miller (1), Gilbert Arenas (1), Jason Terry (1), Mike Bibby (1), Stephon Marbury (1), Jamaal Tinsley (2), Jason Williams (2), Gary Payton (2).

Rarest: Troy Hudson (3), Anthony Carter (2), Brent Barry (2), Eric Snow (2), Sam Cassell (2), Gary Payton (2), Jason Williams (2), Jamaal Tinsley (2), Stephon Marbury (1), Mike Bibby (1).

**Since 2001-02 (through 2025-26), name a player who recorded 13 or more assists in a regular-season game in the 2020-21 season.**

36 valid answers, difficulty **medium**, tiers: 1: 28, 2: 7, 4: 1.

Best known: LeBron James (1), James Harden (1), Kevin Durant (1), Chris Paul (1), Russell Westbrook (1), Luka Doncic (1), Rajon Rondo (1), Damian Lillard (1), DeMar DeRozan (1), Kyle Lowry (1).

Rarest: Facundo Campazzo (4), Lonzo Ball (2), Kevin Porter Jr. (2), Coby White (2), Cory Joseph (2), Joe Ingles (2), Tyus Jones (2), Fred VanVleet (2), D'Angelo Russell (1), T.J. McConnell (1).

**Since 2001-02 (through 2025-26), name a player who recorded 11 or more assists in a regular-season game in the 2023-24 season.**

91 valid answers, difficulty **easy**, tiers: 1: 42, 2: 30, 3: 13, 4: 6.

Best known: LeBron James (1), James Harden (1), Kevin Durant (1), Chris Paul (1), Russell Westbrook (1), Luka Doncic (1), Joel Embiid (1), Stephen Curry (1), Anthony Davis (1), Shai Gilgeous-Alexander (1).

Rarest: Skylar Mays (4), Vasilije Micic (4), Craig Porter Jr. (4), Jared Butler (4), Marcus Sasser (4), Jaylin Williams (4), Bones Hyland (3), Jevon Carter (3), Grant Williams (3), Talen Horton-Tucker (3).

#### `made-playoffs`

**Since 2001-02 (through 2025-26), name a team that made the playoffs in the 2001-02 season.**

16 valid answers, difficulty **hard**, tiers: 1: 13, 4: 3.

Best known: Boston Celtics (1), Dallas Mavericks (1), Detroit Pistons (1), Indiana Pacers (1), Los Angeles Lakers (1), Minnesota Timberwolves (1), Orlando Magic (1), Philadelphia 76ers (1), Portland Trail Blazers (1), Sacramento Kings (1).

Rarest: Oklahoma City Thunder (4), New Orleans Pelicans (4), Brooklyn Nets (4), Utah Jazz (1), Toronto Raptors (1), San Antonio Spurs (1), Sacramento Kings (1), Portland Trail Blazers (1), Philadelphia 76ers (1), Orlando Magic (1).

**Since 2001-02 (through 2025-26), name a team that made the playoffs in the 2013-14 season.**

16 valid answers, difficulty **medium**, tiers: 1: 15, 4: 1.

Best known: Atlanta Hawks (1), Brooklyn Nets (1), Chicago Bulls (1), Dallas Mavericks (1), Golden State Warriors (1), Houston Rockets (1), Indiana Pacers (1), LA Clippers (1), Memphis Grizzlies (1), Miami Heat (1).

Rarest: Charlotte Hornets (4), Washington Wizards (1), Toronto Raptors (1), San Antonio Spurs (1), Portland Trail Blazers (1), Oklahoma City Thunder (1), Miami Heat (1), Memphis Grizzlies (1), LA Clippers (1), Indiana Pacers (1).

**Since 2001-02 (through 2025-26), name a team that made the playoffs in the 2025-26 season.**

16 valid answers, difficulty **easy**, tiers: 1: 16.

Best known: Atlanta Hawks (1), Boston Celtics (1), Cleveland Cavaliers (1), Denver Nuggets (1), Detroit Pistons (1), Houston Rockets (1), Los Angeles Lakers (1), Minnesota Timberwolves (1), New York Knicks (1), Oklahoma City Thunder (1).

Rarest: Toronto Raptors (1), San Antonio Spurs (1), Portland Trail Blazers (1), Phoenix Suns (1), Philadelphia 76ers (1), Orlando Magic (1), Oklahoma City Thunder (1), New York Knicks (1), Minnesota Timberwolves (1), Los Angeles Lakers (1).

#### `wins-in-season`

**Since 2001-02 (through 2025-26), name a team that won 50 or more regular-season games in the 2005-06 season.**

5 valid answers, difficulty **medium**, tiers: 1: 5.

Best known: Cleveland Cavaliers (1), Dallas Mavericks (1), Detroit Pistons (1), Phoenix Suns (1), San Antonio Spurs (1).

Rarest: San Antonio Spurs (1), Phoenix Suns (1), Detroit Pistons (1), Dallas Mavericks (1), Cleveland Cavaliers (1).

**Since 2001-02 (through 2025-26), name a team that won 45 or more regular-season games in the 2010-11 season.**

12 valid answers, difficulty **medium**, tiers: 1: 11, 4: 1.

Best known: Boston Celtics (1), Chicago Bulls (1), Dallas Mavericks (1), Denver Nuggets (1), Los Angeles Lakers (1), Memphis Grizzlies (1), Miami Heat (1), Oklahoma City Thunder (1), Orlando Magic (1), Portland Trail Blazers (1).

Rarest: New Orleans Pelicans (4), San Antonio Spurs (1), Portland Trail Blazers (1), Orlando Magic (1), Oklahoma City Thunder (1), Miami Heat (1), Memphis Grizzlies (1), Los Angeles Lakers (1), Denver Nuggets (1), Dallas Mavericks (1).

**Since 2001-02 (through 2025-26), name a team that won 40 or more regular-season games in the 2022-23 season.**

20 valid answers, difficulty **easy**, tiers: 1: 20.

Best known: Atlanta Hawks (1), Boston Celtics (1), Brooklyn Nets (1), Chicago Bulls (1), Cleveland Cavaliers (1), Denver Nuggets (1), Golden State Warriors (1), LA Clippers (1), Los Angeles Lakers (1), Memphis Grizzlies (1).

Rarest: Toronto Raptors (1), Sacramento Kings (1), Phoenix Suns (1), Philadelphia 76ers (1), Oklahoma City Thunder (1), New York Knicks (1), New Orleans Pelicans (1), Minnesota Timberwolves (1), Milwaukee Bucks (1), Miami Heat (1).

#### `home-wins-in-season`

**Since 2001-02 (through 2025-26), name a team that won 30 or more home games in the 2023-24 season.**

5 valid answers, difficulty **medium**, tiers: 1: 5.

Best known: Boston Celtics (1), Denver Nuggets (1), Milwaukee Bucks (1), Minnesota Timberwolves (1), Oklahoma City Thunder (1).

Rarest: Oklahoma City Thunder (1), Minnesota Timberwolves (1), Milwaukee Bucks (1), Denver Nuggets (1), Boston Celtics (1).

**Since 2001-02 (through 2025-26), name a team that won 33 or more home games in the 2007-08 season.**

6 valid answers, difficulty **medium**, tiers: 1: 6.

Best known: Boston Celtics (1), Dallas Mavericks (1), Denver Nuggets (1), Detroit Pistons (1), San Antonio Spurs (1), Utah Jazz (1).

Rarest: Utah Jazz (1), San Antonio Spurs (1), Detroit Pistons (1), Denver Nuggets (1), Dallas Mavericks (1), Boston Celtics (1).

**Since 2001-02 (through 2025-26), name a team that won 30 or more home games in the 2008-09 season.**

10 valid answers, difficulty **medium**, tiers: 1: 10.

Best known: Atlanta Hawks (1), Boston Celtics (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Houston Rockets (1), Los Angeles Lakers (1), Orlando Magic (1), Portland Trail Blazers (1), Utah Jazz (1).

Rarest: Utah Jazz (1), Portland Trail Blazers (1), Orlando Magic (1), Los Angeles Lakers (1), Houston Rockets (1), Denver Nuggets (1), Dallas Mavericks (1), Cleveland Cavaliers (1), Boston Celtics (1), Atlanta Hawks (1).

#### `road-wins-in-season`

**Since 2001-02 (through 2025-26), name a team that won 23 or more road games in the 2002-03 season.**

5 valid answers, difficulty **medium**, tiers: 1: 5.

Best known: Dallas Mavericks (1), Philadelphia 76ers (1), Portland Trail Blazers (1), Sacramento Kings (1), San Antonio Spurs (1).

Rarest: San Antonio Spurs (1), Sacramento Kings (1), Portland Trail Blazers (1), Philadelphia 76ers (1), Dallas Mavericks (1).

**Since 2001-02 (through 2025-26), name a team that won 23 or more road games in the 2010-11 season.**

8 valid answers, difficulty **medium**, tiers: 1: 8.

Best known: Boston Celtics (1), Chicago Bulls (1), Dallas Mavericks (1), Los Angeles Lakers (1), Miami Heat (1), Oklahoma City Thunder (1), Orlando Magic (1), San Antonio Spurs (1).

Rarest: San Antonio Spurs (1), Orlando Magic (1), Oklahoma City Thunder (1), Miami Heat (1), Los Angeles Lakers (1), Dallas Mavericks (1), Chicago Bulls (1), Boston Celtics (1).

**Since 2001-02 (through 2025-26), name a team that won 20 or more road games in the 2025-26 season.**

15 valid answers, difficulty **easy**, tiers: 1: 15.

Best known: Atlanta Hawks (1), Boston Celtics (1), Charlotte Hornets (1), Cleveland Cavaliers (1), Denver Nuggets (1), Detroit Pistons (1), Houston Rockets (1), Los Angeles Lakers (1), Minnesota Timberwolves (1), New York Knicks (1).

Rarest: Toronto Raptors (1), San Antonio Spurs (1), Phoenix Suns (1), Philadelphia 76ers (1), Oklahoma City Thunder (1), New York Knicks (1), Minnesota Timberwolves (1), Los Angeles Lakers (1), Houston Rockets (1), Detroit Pistons (1).

#### `playoff-wins-in-season`

**Since 2001-02 (through 2025-26), name a team that won 4 or more playoff games in the 2001-02 postseason.**

8 valid answers, difficulty **hard**, tiers: 1: 6, 4: 2.

Best known: Boston Celtics (1), Dallas Mavericks (1), Detroit Pistons (1), Los Angeles Lakers (1), Sacramento Kings (1), San Antonio Spurs (1), Brooklyn Nets (4), New Orleans Pelicans (4).

Rarest: New Orleans Pelicans (4), Brooklyn Nets (4), San Antonio Spurs (1), Sacramento Kings (1), Los Angeles Lakers (1), Detroit Pistons (1), Dallas Mavericks (1), Boston Celtics (1).

**Since 2001-02 (through 2025-26), name a team that won 4 or more playoff games in the 2025-26 postseason.**

8 valid answers, difficulty **medium**, tiers: 1: 8.

Best known: Cleveland Cavaliers (1), Detroit Pistons (1), Los Angeles Lakers (1), Minnesota Timberwolves (1), New York Knicks (1), Oklahoma City Thunder (1), Philadelphia 76ers (1), San Antonio Spurs (1).

Rarest: San Antonio Spurs (1), Philadelphia 76ers (1), Oklahoma City Thunder (1), New York Knicks (1), Minnesota Timberwolves (1), Los Angeles Lakers (1), Detroit Pistons (1), Cleveland Cavaliers (1).

**Since 2001-02 (through 2025-26), name a team that won 1 or more playoff games in the 2002-03 postseason.**

16 valid answers, difficulty **medium**, tiers: 1: 14, 4: 2.

Best known: Boston Celtics (1), Dallas Mavericks (1), Detroit Pistons (1), Indiana Pacers (1), Los Angeles Lakers (1), Milwaukee Bucks (1), Minnesota Timberwolves (1), Orlando Magic (1), Philadelphia 76ers (1), Phoenix Suns (1).

Rarest: New Orleans Pelicans (4), Brooklyn Nets (4), Utah Jazz (1), San Antonio Spurs (1), Sacramento Kings (1), Portland Trail Blazers (1), Phoenix Suns (1), Philadelphia 76ers (1), Orlando Magic (1), Minnesota Timberwolves (1).

#### `regulation-points-in-season`

**Since 2001-02 (through 2025-26), name a team that scored 135 or more points in a regulation game in the 2006-07 season.**

5 valid answers, difficulty **medium**, tiers: 1: 5.

Best known: Denver Nuggets (1), Golden State Warriors (1), Memphis Grizzlies (1), Phoenix Suns (1), Sacramento Kings (1).

Rarest: Sacramento Kings (1), Phoenix Suns (1), Memphis Grizzlies (1), Golden State Warriors (1), Denver Nuggets (1).

**Since 2001-02 (through 2025-26), name a team that scored 130 or more points in a regulation game in the 2013-14 season.**

12 valid answers, difficulty **easy**, tiers: 1: 12.

Best known: Brooklyn Nets (1), Denver Nuggets (1), Golden State Warriors (1), Houston Rockets (1), LA Clippers (1), Los Angeles Lakers (1), Milwaukee Bucks (1), Minnesota Timberwolves (1), New Orleans Pelicans (1), Oklahoma City Thunder (1).

Rarest: San Antonio Spurs (1), Portland Trail Blazers (1), Oklahoma City Thunder (1), New Orleans Pelicans (1), Minnesota Timberwolves (1), Milwaukee Bucks (1), Los Angeles Lakers (1), LA Clippers (1), Houston Rockets (1), Golden State Warriors (1).

**Since 2001-02 (through 2025-26), name a team that scored 135 or more points in a regulation game in the 2024-25 season.**

24 valid answers, difficulty **easy**, tiers: 1: 24.

Best known: Atlanta Hawks (1), Boston Celtics (1), Charlotte Hornets (1), Chicago Bulls (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Detroit Pistons (1), Golden State Warriors (1), Houston Rockets (1).

Rarest: Utah Jazz (1), San Antonio Spurs (1), Sacramento Kings (1), Portland Trail Blazers (1), Oklahoma City Thunder (1), New York Knicks (1), New Orleans Pelicans (1), Minnesota Timberwolves (1), Milwaukee Bucks (1), Miami Heat (1).

#### `margin-in-season`

**Since 2001-02 (through 2025-26), name a team that won a game by 40 or more points in the 2009-10 season.**

5 valid answers, difficulty **medium**, tiers: 1: 5.

Best known: Dallas Mavericks (1), Golden State Warriors (1), Los Angeles Lakers (1), New York Knicks (1), Orlando Magic (1).

Rarest: Orlando Magic (1), New York Knicks (1), Los Angeles Lakers (1), Golden State Warriors (1), Dallas Mavericks (1).

**Since 2001-02 (through 2025-26), name a team that won a game by 35 or more points in the 2019-20 season.**

14 valid answers, difficulty **easy**, tiers: 1: 14.

Best known: Boston Celtics (1), Brooklyn Nets (1), Chicago Bulls (1), Dallas Mavericks (1), Denver Nuggets (1), Houston Rockets (1), Indiana Pacers (1), LA Clippers (1), Memphis Grizzlies (1), Milwaukee Bucks (1).

Rarest: Utah Jazz (1), Toronto Raptors (1), Phoenix Suns (1), Philadelphia 76ers (1), Milwaukee Bucks (1), Memphis Grizzlies (1), LA Clippers (1), Indiana Pacers (1), Houston Rockets (1), Denver Nuggets (1).

**Since 2001-02 (through 2025-26), name a team that won a game by 30 or more points in the 2025-26 season.**

24 valid answers, difficulty **easy**, tiers: 1: 24.

Best known: Atlanta Hawks (1), Boston Celtics (1), Brooklyn Nets (1), Charlotte Hornets (1), Chicago Bulls (1), Cleveland Cavaliers (1), Denver Nuggets (1), Detroit Pistons (1), Golden State Warriors (1), Houston Rockets (1).

Rarest: Utah Jazz (1), Toronto Raptors (1), San Antonio Spurs (1), Portland Trail Blazers (1), Phoenix Suns (1), Orlando Magic (1), Oklahoma City Thunder (1), New York Knicks (1), Minnesota Timberwolves (1), Miami Heat (1).

#### `threes-in-season`

**Since 2001-02 (through 2025-26), name a team that made 17 or more three-pointers as a team in a game in the 2004-05 season.**

5 valid answers, difficulty **hard**, tiers: 1: 4, 4: 1.

Best known: Golden State Warriors (1), New York Knicks (1), Phoenix Suns (1), Toronto Raptors (1), Oklahoma City Thunder (4).

Rarest: Oklahoma City Thunder (4), Toronto Raptors (1), Phoenix Suns (1), New York Knicks (1), Golden State Warriors (1).

**Since 2001-02 (through 2025-26), name a team that made 14 or more three-pointers as a team in a game in the 2001-02 season.**

14 valid answers, difficulty **medium**, tiers: 1: 13, 4: 1.

Best known: Boston Celtics (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Detroit Pistons (1), Houston Rockets (1), Indiana Pacers (1), LA Clippers (1), Milwaukee Bucks (1), New York Knicks (1), Orlando Magic (1).

Rarest: Brooklyn Nets (4), Toronto Raptors (1), San Antonio Spurs (1), Sacramento Kings (1), Orlando Magic (1), New York Knicks (1), Milwaukee Bucks (1), LA Clippers (1), Indiana Pacers (1), Houston Rockets (1).

**Since 2001-02 (through 2025-26), name a team that made 14 or more three-pointers as a team in a game in the 2013-14 season.**

24 valid answers, difficulty **easy**, tiers: 1: 24.

Best known: Atlanta Hawks (1), Boston Celtics (1), Brooklyn Nets (1), Chicago Bulls (1), Dallas Mavericks (1), Denver Nuggets (1), Golden State Warriors (1), Houston Rockets (1), Indiana Pacers (1), LA Clippers (1).

Rarest: Washington Wizards (1), Utah Jazz (1), Toronto Raptors (1), San Antonio Spurs (1), Sacramento Kings (1), Portland Trail Blazers (1), Phoenix Suns (1), Philadelphia 76ers (1), Orlando Magic (1), Oklahoma City Thunder (1).

#### `held-opponent-in-season`

**Since 2001-02 (through 2025-26), name a team that held an opponent to 65 or fewer points in a game in the 2001-02 season.**

5 valid answers, difficulty **medium**, tiers: 1: 5.

Best known: Boston Celtics (1), Detroit Pistons (1), New York Knicks (1), Portland Trail Blazers (1), Utah Jazz (1).

Rarest: Utah Jazz (1), Portland Trail Blazers (1), New York Knicks (1), Detroit Pistons (1), Boston Celtics (1).

**Since 2001-02 (through 2025-26), name a team that held an opponent to 65 or fewer points in a game in the 2003-04 season.**

13 valid answers, difficulty **medium**, tiers: 1: 12, 4: 1.

Best known: Boston Celtics (1), Detroit Pistons (1), Houston Rockets (1), Indiana Pacers (1), Memphis Grizzlies (1), Miami Heat (1), Milwaukee Bucks (1), Minnesota Timberwolves (1), New York Knicks (1), Sacramento Kings (1).

Rarest: Brooklyn Nets (4), Washington Wizards (1), San Antonio Spurs (1), Sacramento Kings (1), New York Knicks (1), Minnesota Timberwolves (1), Milwaukee Bucks (1), Miami Heat (1), Memphis Grizzlies (1), Indiana Pacers (1).

**Since 2001-02 (through 2025-26), name a team that held an opponent to 75 or fewer points in a game in the 2006-07 season.**

23 valid answers, difficulty **hard**, tiers: 1: 19, 4: 4.

Best known: Atlanta Hawks (1), Boston Celtics (1), Chicago Bulls (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Detroit Pistons (1), Houston Rockets (1), Indiana Pacers (1), LA Clippers (1).

Rarest: Oklahoma City Thunder (4), New Orleans Pelicans (4), Charlotte Hornets (4), Brooklyn Nets (4), Utah Jazz (1), San Antonio Spurs (1), Portland Trail Blazers (1), Philadelphia 76ers (1), Orlando Magic (1), New York Knicks (1).

#### `overtime-wins-in-season`

**Since 2001-02 (through 2025-26), name a team that won a game that went to 2 or more overtimes in the 2001-02 season.**

6 valid answers, difficulty **hard**, tiers: 1: 5, 4: 1.

Best known: Atlanta Hawks (1), Chicago Bulls (1), Dallas Mavericks (1), Miami Heat (1), Portland Trail Blazers (1), Brooklyn Nets (4).

Rarest: Brooklyn Nets (4), Portland Trail Blazers (1), Miami Heat (1), Dallas Mavericks (1), Chicago Bulls (1), Atlanta Hawks (1).

**Since 2001-02 (through 2025-26), name a team that won a game that went to 2 or more overtimes in the 2025-26 season.**

8 valid answers, difficulty **medium**, tiers: 1: 8.

Best known: Atlanta Hawks (1), Boston Celtics (1), LA Clippers (1), New York Knicks (1), Oklahoma City Thunder (1), Phoenix Suns (1), San Antonio Spurs (1), Utah Jazz (1).

Rarest: Utah Jazz (1), San Antonio Spurs (1), Phoenix Suns (1), Oklahoma City Thunder (1), New York Knicks (1), LA Clippers (1), Boston Celtics (1), Atlanta Hawks (1).

**Since 2001-02 (through 2025-26), name a team that won a game that went to 1 or more overtimes in the 2021-22 season.**

24 valid answers, difficulty **easy**, tiers: 1: 24.

Best known: Boston Celtics (1), Brooklyn Nets (1), Chicago Bulls (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Detroit Pistons (1), Houston Rockets (1), Indiana Pacers (1), Los Angeles Lakers (1).

Rarest: Washington Wizards (1), Utah Jazz (1), Toronto Raptors (1), San Antonio Spurs (1), Sacramento Kings (1), Phoenix Suns (1), Philadelphia 76ers (1), Oklahoma City Thunder (1), New York Knicks (1), New Orleans Pelicans (1).

#### `played-playoff-against`

**Since 2001-02 (through 2025-26), name a team that played a playoff game against the Sacramento Kings.**

7 valid answers, difficulty **hard**, tiers: 1: 6, 4: 1.

Best known: Dallas Mavericks (1), Golden State Warriors (1), Los Angeles Lakers (1), Minnesota Timberwolves (1), San Antonio Spurs (1), Utah Jazz (1), Oklahoma City Thunder (4).

Rarest: Oklahoma City Thunder (4), Utah Jazz (1), San Antonio Spurs (1), Minnesota Timberwolves (1), Los Angeles Lakers (1), Golden State Warriors (1), Dallas Mavericks (1).

**Since 2001-02 (through 2025-26), name a team that played a playoff game against the Portland Trail Blazers.**

11 valid answers, difficulty **medium**, tiers: 1: 11.

Best known: Dallas Mavericks (1), Denver Nuggets (1), Golden State Warriors (1), Houston Rockets (1), LA Clippers (1), Los Angeles Lakers (1), Memphis Grizzlies (1), New Orleans Pelicans (1), Oklahoma City Thunder (1), Phoenix Suns (1).

Rarest: San Antonio Spurs (1), Phoenix Suns (1), Oklahoma City Thunder (1), New Orleans Pelicans (1), Memphis Grizzlies (1), Los Angeles Lakers (1), LA Clippers (1), Houston Rockets (1), Golden State Warriors (1), Denver Nuggets (1).

**Since 2001-02 (through 2025-26), name a team that played a playoff game against the San Antonio Spurs.**

19 valid answers, difficulty **medium**, tiers: 1: 17, 4: 2.

Best known: Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Detroit Pistons (1), Golden State Warriors (1), Houston Rockets (1), LA Clippers (1), Los Angeles Lakers (1), Memphis Grizzlies (1), Miami Heat (1).

Rarest: New Orleans Pelicans (4), Brooklyn Nets (4), Utah Jazz (1), Sacramento Kings (1), Portland Trail Blazers (1), Phoenix Suns (1), Oklahoma City Thunder (1), New York Knicks (1), Minnesota Timberwolves (1), Miami Heat (1).

#### `beat-in-playoffs`

**Since 2001-02 (through 2025-26), name a team that won a playoff game against the Sacramento Kings.**

7 valid answers, difficulty **hard**, tiers: 1: 6, 4: 1.

Best known: Dallas Mavericks (1), Golden State Warriors (1), Los Angeles Lakers (1), Minnesota Timberwolves (1), San Antonio Spurs (1), Utah Jazz (1), Oklahoma City Thunder (4).

Rarest: Oklahoma City Thunder (4), Utah Jazz (1), San Antonio Spurs (1), Minnesota Timberwolves (1), Los Angeles Lakers (1), Golden State Warriors (1), Dallas Mavericks (1).

**Since 2001-02 (through 2025-26), name a team that won a playoff game against the Cleveland Cavaliers.**

11 valid answers, difficulty **hard**, tiers: 1: 10, 4: 1.

Best known: Boston Celtics (1), Chicago Bulls (1), Detroit Pistons (1), Golden State Warriors (1), Indiana Pacers (1), New York Knicks (1), Orlando Magic (1), San Antonio Spurs (1), Toronto Raptors (1), Washington Wizards (1).

Rarest: Brooklyn Nets (4), Washington Wizards (1), Toronto Raptors (1), San Antonio Spurs (1), Orlando Magic (1), New York Knicks (1), Indiana Pacers (1), Golden State Warriors (1), Detroit Pistons (1), Chicago Bulls (1).

**Since 2001-02 (through 2025-26), name a team that won a playoff game against the San Antonio Spurs.**

18 valid answers, difficulty **medium**, tiers: 1: 16, 4: 2.

Best known: Dallas Mavericks (1), Denver Nuggets (1), Detroit Pistons (1), Golden State Warriors (1), Houston Rockets (1), LA Clippers (1), Los Angeles Lakers (1), Memphis Grizzlies (1), Miami Heat (1), Minnesota Timberwolves (1).

Rarest: New Orleans Pelicans (4), Brooklyn Nets (4), Utah Jazz (1), Sacramento Kings (1), Portland Trail Blazers (1), Phoenix Suns (1), Oklahoma City Thunder (1), New York Knicks (1), Minnesota Timberwolves (1), Miami Heat (1).

## What was dropped (star-heavy templates)

- `points-regular`: n=35.0: 422 answers (too many); n=65.0: 7 answers (too few)
- `triple-double-finals`: no threshold: 11 answers (too few)
- `rebounds`: n=16.0: 452 answers (too many)
- `assists`: n=22.0: 12 answers (too few)
- `threes`: n=12.0: 8 answers (too few)
- `blocks`: n=11.0: 7 answers (too few)
- `steals`: n=5.0: 707 answers (too many); n=9.0: 12 answers (too few)
- `ppg-season`: n=32.0: 9 answers (too few)
- `franchises`: n=4.0: 766 answers (too many); n=5.0: 493 answers (too many)
- `wins-season`: n=67.0: 4 answers (too few)
- `points-regulation`: n=160.0: 2 answers (too few)
- `win-margin`: n=60.0: 4 answers (too few)
- `points-game7`: n=40.0: 10 answers (too few)
- `points-bench`: n=45.0: 14 answers (too few)
- `points-loss`: n=60.0: 9 answers (too few)
- `points-road`: n=60.0: 11 answers (too few)
- `rebounds-finals`: n=18.0: 11 answers (too few); n=20.0: 6 answers (too few)
- `assists-playoff`: n=18.0: 6 answers (too few)
- `assists-finals`: n=12.0: 10 answers (too few); n=14.0: 3 answers (too few)
- `threes-playoff`: n=9.0: 11 answers (too few); n=10.0: 2 answers (too few)
- `threes-finals`: n=7.0: 10 answers (too few); n=8.0: 2 answers (too few)
- `blocks-playoff`: n=8.0: 9 answers (too few)
- `steals-playoff`: n=7.0: 8 answers (too few)
- `offensive-rebounds`: n=14.0: 8 answers (too few)
- `free-throws`: n=24.0: 11 answers (too few)
- `shots-taken`: n=40.0: 12 answers (too few); n=42.0: 7 answers (too few)
- `minutes`: n=60.0: 8 answers (too few)
- `five-by-n`: n=5.0: 8 answers (too few)
- `rebounds-per-game`: n=13.0: 14 answers (too few)
- `assists-per-game`: n=10.0: 13 answers (too few); n=11.0: 6 answers (too few)
- `steals-per-game`: n=3.0: 1 answers (too few)
- `blocks-per-game`: n=3.0: 9 answers (too few)
- `losses-season`: n=70.0: 2 answers (too few)
- `road-wins`: n=32.0: 4 answers (too few)
- `home-wins`: n=38.0: 4 answers (too few); n=39.0: 3 answers (too few); n=40.0: 1 answers (too few)
- `points-playoff-team`: n=150.0: 2 answers (too few)
- `points-any-game`: n=165.0: 4 answers (too few)
- `held-opponent`: n=55.0: 2 answers (too few)
- `threes-team`: n=30.0: 0 answers (too few)
- `steals-team`: n=22.0: 4 answers (too few); n=24.0: 0 answers (too few)
- `overtime-wins`: n=4.0: 4 answers (too few)
- `win-streak`: n=20.0: 3 answers (too few); n=22.0: 3 answers (too few)

## Player templates: examples

Three candidates per template, from the shortest list to the longest. Each answer is shown as name (tier).

### `points-regular`

**Since 2001-02 (through 2025-26), name a player who scored 60 or more points in a regular-season game.**

24 valid answers, difficulty **medium**, tiers: 1: 24 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kobe Bryant (1), Luka Doncic (1), Joel Embiid (1), Allen Iverson (1), Stephen Curry (1), Damian Lillard (1), Carmelo Anthony (1), Tracy McGrady (1), Bradley Beal (1), Giannis Antetokounmpo (1), Nikola Jokic (1), Jayson Tatum (1), Gilbert Arenas (1), Jalen Brunson (1), Kyrie Irving (1), Karl-Anthony Towns (1), Klay Thompson (1), Donovan Mitchell (1), Devin Booker (1), De'Aaron Fox (1), Kemba Walker (1), Bam Adebayo (1)

</details>

**Since 2001-02 (through 2025-26), name a player who scored 50 or more points in a regular-season game.**

93 valid answers, difficulty **easy**, tiers: 1: 73, 2: 19, 4: 1 (1 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Joel Embiid (1), Dirk Nowitzki (1), Allen Iverson (1), Stephen Curry (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Damian Lillard (1), Carmelo Anthony (1), Tony Parker (1), Tracy McGrady (1), DeMar DeRozan (1), Dwyane Wade (1), Andre Miller (1), Paul Pierce (1), Bradley Beal (1), Deron Williams (1), Giannis Antetokounmpo (1), Jrue Holiday (1), Kevin Love (1), Nikola Jokic (1), Jayson Tatum (1), Trae Young (1), LaMarcus Aldridge (1), John Wall (1), Gilbert Arenas (1), Vince Carter (1), Isaiah Thomas (1), Anthony Edwards (1), Jalen Brunson (1), Jaylen Brown (1), Kyrie Irving (1), Karl-Anthony Towns (1), Tyrese Maxey (1), Klay Thompson (1), Donovan Mitchell (1), Jamal Crawford (1), Kawhi Leonard (1), Devin Booker (1), Ray Allen (1), Jimmy Butler III (1), Ja Morant (1), Zach LaVine (1), DeMarcus Cousins (1), CJ McCollum (1), Lauri Markkanen (1), Julius Randle (1), Michael Redd (1), De'Aaron Fox (1), Amar'e Stoudemire (1), Paolo Banchero (1), Kemba Walker (1), Mo Williams (1), Derrick Rose (1), Jermaine O'Neal (1), Jamal Murray (1), LaMelo Ball (1), Lou Williams (1), Richard Hamilton (1), Blake Griffin (1), Victor Wembanyama (1), Kevin Martin (1), Bam Adebayo (1), D'Angelo Russell (1), Pascal Siakam (1), Khris Middleton (1), Michael Jordan (1), Eric Gordon (2), Rashard Lewis (2), Austin Reaves (2), Fred VanVleet (2), Brandon Roy (2), Brandon Jennings (2), Allan Houston (2), Darius Garland (2), Aaron Gordon (2), Jamal Mashburn (2), Shareef Abdur-Rahim (2), Corey Brewer (2008-2020) (2), Cooper Flagg (2), Caris LeVert (2), Damon Stoudamire (2), T.J. Warren (2), Kevin Porter Jr. (2), Terrence Ross (2), Saddiq Bey (2), Malachi Flynn (4)

</details>

**Since 2001-02 (through 2025-26), name a player who scored 40 or more points in a regular-season game.**

263 valid answers, difficulty **easy**, tiers: 1: 126, 2: 105, 3: 29, 4: 2, 5: 1 (3 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Chris Paul (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Pau Gasol (1), Joel Embiid (1), Dirk Nowitzki (1), Kevin Garnett (1), Steve Nash (1), Allen Iverson (1), Stephen Curry (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Damian Lillard (1), Jason Kidd (1), Carmelo Anthony (1), Tony Parker (1), Tracy McGrady (1), DeMar DeRozan (1), Kyle Lowry (1), Dwyane Wade (1), Nikola Vucevic (1), Andre Miller (1), Paul Pierce (1), Zach Randolph (1), Mike Conley (1), Shawn Marion (1), Bradley Beal (1), Deron Williams (1), Giannis Antetokounmpo (1), Jrue Holiday (1), Kevin Love (1), Nikola Jokic (1), Jayson Tatum (1), Trae Young (1), Joe Johnson (1), LaMarcus Aldridge (1), John Wall (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Paul Millsap (1), Isaiah Thomas (1), Anthony Edwards (1), Elton Brand (1), Jalen Brunson (1), Jaylen Brown (1), Carlos Boozer (1), Kyrie Irving (1), Karl-Anthony Towns (1), Tyrese Maxey (1), Klay Thompson (1), Donovan Mitchell (1), Baron Davis (1), Jamal Crawford (1), Chris Bosh (1), Kawhi Leonard (1), Marc Gasol (1), Devin Booker (1), Jason Terry (1), Ray Allen (1), Al Jefferson (1), Shaquille O'Neal (1), Jimmy Butler III (1), Ja Morant (1), Zach LaVine (1), Manu Ginobili (1), Dennis Schroder (1), Myles Turner (1), Zion Williamson (1), DeMarcus Cousins (1), CJ McCollum (1), Trevor Ariza (1), Lauri Markkanen (1), Julius Randle (1), Goran Dragic (1), Michael Redd (1), De'Aaron Fox (1), David West (1), Rudy Gay (1), Domantas Sabonis (1), Amar'e Stoudemire (1), Cade Cunningham (1), Mike Bibby (1), Antawn Jamison (1), Paolo Banchero (1), Danny Granger (1), Kemba Walker (1), Mo Williams (1), Monta Ellis (1), Derrick Rose (1), Jermaine O'Neal (1), Jamal Murray (1), Gerald Wallace (1), LaMelo Ball (1), Lou Williams (1), Richard Jefferson (1), Devin Harris (1), Yao Ming (1), Richard Hamilton (1), Blake Griffin (1), Victor Wembanyama (1), Brandon Ingram (1), Kevin Martin (1), Andrew Wiggins (1), Bam Adebayo (1), Reggie Jackson (1), D'Angelo Russell (1), Collin Sexton (1), Peja Stojakovic (1), Stephon Marbury (1), Jeff Green (1), Pascal Siakam (1), Eric Bledsoe (1), Deni Avdija (1), Jason Richardson (1), Jarrett Allen (1), Khris Middleton (1), Tyler Herro (1), Michael Jordan (1), Karl Malone (1), Eric Gordon (2), Desmond Bane (2), Robert Covington (2), Keyonte George (2), Luol Deng (2), Rashard Lewis (2), Austin Reaves (2), Kristaps Porzingis (2), Fred VanVleet (2), Victor Oladipo (2), JR Smith (2), Tyrese Haliburton (2), Caron Butler (2), Spencer Dinwiddie (2), Brandon Roy (2), Anfernee Simons (2), Jordan Clarkson (2), Stephen Jackson (2), Jaren Jackson Jr. (2), Brandon Jennings (2), JJ Redick (2), Jalen Johnson (2), Allan Houston (2), Dejounte Murray (2), Gordon Hayward (2), Cam Thomas (2), Gary Payton (2), Jerami Grant (2), Tim Hardaway Jr. (2), Ben Simmons (2), Al Harrington (2), Kyle Kuzma (2), Luis Scola (2), Darius Garland (2), Antoine Walker (2), Aaron Gordon (2), Jalen Rose (2), Jalen Green (2), Tyreke Evans (2), Larry Hughes (2), Ramon Sessions (2), Danilo Gallinari (2), Norman Powell (2), Cuttino Mobley (2), Steve Francis (2), Derrick White (2), Jamal Mashburn (2), Bojan Bogdanovic (2), Jalen Williams (2), Mehmet Okur (2), Jerry Stackhouse (2), Trey Murphy III (2), Ben Gordon (2), Andrea Bargnani (2), Josh Hart (2), Shareef Abdur-Rahim (2), Mike Miller (2), Corey Brewer (2008-2020) (2), Alperen Sengun (2), Terry Rozier (2), Buddy Hield (2), Mikal Bridges (2), RJ Barrett (2), Cooper Flagg (2), Miles Bridges (2), OG Anunoby (2), Rodney Stuckey (2), Caris LeVert (2), Nickeil Alexander-Walker (2), Ricky Davis (2), Michael Finley (2), Damon Stoudamire (2), Jordan Poole (2), Coby White (2), Leandro Barbosa (2), Kelly Oubre Jr. (2), Evan Fournier (2), Dillon Brooks (2), Andrew Bynum (2), Josh Howard (2), T.J. Warren (2), Aaron Brooks (2), Quentin Richardson (2), Eddy Curry (2), Latrell Sprewell (2), Michael Beasley (2), Kevin Porter Jr. (2), Wally Szczerbiak (2), Nate Robinson (2), Malik Monk (2), Evan Mobley (2), Marcus Thornton (2), CJ Miles (2), O.J. Mayo (2), Arron Afflalo (2), Terrence Ross (2), Nick Van Exel (2), Gary Trent Jr. (2), Nick Young (2), Amen Thompson (2), Devonte' Graham (2), Bogdan Bogdanovic (2), Charlie Villanueva (2), P.J. Washington (2), Saddiq Bey (2), Donte DiVincenzo (3), Immanuel Quickley (3), Luguentz Dort (3), Austin Rivers (3), Payton Pritchard (3), C.J. Watson (3), Trey Burke (3), Stephon Castle (3), Lamond Murray (3), Grayson Allen (3), Gerald Green (3), Matas Buzelis (3), Jodie Meeks (3), Jaime Jaquez Jr. (3), Pat Connaughton (3), Keegan Murray (3), Brice Sensabaugh (3), Darius Miles (3), Jordan Crawford (3), GG Jackson (3), Quentin Grimes (3), Jeremiah Fears (3), Anthony Morrow (3), Damien Wilkins (3), Allen Crabbe (3), Talen Horton-Tucker (3), Obi Toppin (3), Linas Kleiza (3), Aaron Wiggins (3), Malachi Flynn (4), Rodrigue Beaubois (4), Kenneth Lofton Jr. (5)

</details>

### `points-playoff`

**Since 2001-02 (through 2025-26), name a player who scored 50 or more points in a playoff game.**

17 valid answers, difficulty **medium**, tiers: 1: 17 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), Kevin Durant (1), Kobe Bryant (1), Russell Westbrook (1), Joel Embiid (1), Dirk Nowitzki (1), Allen Iverson (1), Stephen Curry (1), Damian Lillard (1), Giannis Antetokounmpo (1), Nikola Jokic (1), Jayson Tatum (1), Isaiah Thomas (1), Donovan Mitchell (1), Ray Allen (1), Jimmy Butler III (1), Jamal Murray (1)

</details>

**Since 2001-02 (through 2025-26), name a player who scored 40 or more points in a playoff game.**

73 valid answers, difficulty **easy**, tiers: 1: 63, 2: 8, 3: 2 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Chris Paul (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Joel Embiid (1), Dirk Nowitzki (1), Steve Nash (1), Allen Iverson (1), Stephen Curry (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Rajon Rondo (1), Damian Lillard (1), Carmelo Anthony (1), Tony Parker (1), Tracy McGrady (1), DeMar DeRozan (1), Dwyane Wade (1), Paul Pierce (1), Giannis Antetokounmpo (1), Jrue Holiday (1), Nikola Jokic (1), Jayson Tatum (1), Trae Young (1), LaMarcus Aldridge (1), John Wall (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Paul Millsap (1), Isaiah Thomas (1), Anthony Edwards (1), Chauncey Billups (1), Elton Brand (1), Jalen Brunson (1), Jaylen Brown (1), Carlos Boozer (1), Kyrie Irving (1), Tyrese Maxey (1), Klay Thompson (1), Donovan Mitchell (1), Kawhi Leonard (1), Devin Booker (1), Ray Allen (1), Shaquille O'Neal (1), Jimmy Butler III (1), Ja Morant (1), CJ McCollum (1), Michael Redd (1), Amar'e Stoudemire (1), Cade Cunningham (1), Paolo Banchero (1), Derrick Rose (1), Jamal Murray (1), Richard Hamilton (1), Victor Wembanyama (1), Jason Richardson (1), Khris Middleton (1), Brandon Roy (2), Gordon Hayward (2), Sam Cassell (2), Norman Powell (2), Jalen Williams (2), Ben Gordon (2), Anthony Johnson (2), Nick Van Exel (2), Bonzi Wells (3), Ayo Dosunmu (3)

</details>

**Since 2001-02 (through 2025-26), name a player who scored 25 or more points in a playoff game.**

330 valid answers, difficulty **easy**, tiers: 1: 154, 2: 106, 3: 68, 4: 2 (2 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Chris Paul (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Pau Gasol (1), Joel Embiid (1), Dirk Nowitzki (1), Kevin Garnett (1), Steve Nash (1), Allen Iverson (1), Ben Wallace (1), Stephen Curry (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Rajon Rondo (1), Damian Lillard (1), Brook Lopez (1), Rudy Gobert (1), Jason Kidd (1), Carmelo Anthony (1), Tony Parker (1), Tracy McGrady (1), Josh Smith (1), DeAndre Jordan (1), DeMar DeRozan (1), Kyle Lowry (1), Dwyane Wade (1), Nikola Vucevic (1), Andre Miller (1), Paul Pierce (1), Zach Randolph (1), Mike Conley (1), Shawn Marion (1), Bradley Beal (1), Al Horford (1), Deron Williams (1), Giannis Antetokounmpo (1), Jrue Holiday (1), Kevin Love (1), Nikola Jokic (1), Jayson Tatum (1), Andre Iguodala (1), Trae Young (1), Joe Johnson (1), Draymond Green (1), LaMarcus Aldridge (1), Jonas Valanciunas (1), John Wall (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Paul Millsap (1), Isaiah Thomas (1), Serge Ibaka (1), Anthony Edwards (1), Chauncey Billups (1), Elton Brand (1), Jalen Brunson (1), Jaylen Brown (1), Carlos Boozer (1), Kyrie Irving (1), Karl-Anthony Towns (1), Tyrese Maxey (1), Klay Thompson (1), Donovan Mitchell (1), Baron Davis (1), Jamal Crawford (1), Jose Calderon (1), Chris Bosh (1), Ricky Rubio (1), Kawhi Leonard (1), Marc Gasol (1), Raymond Felton (1), Clint Capela (1), Devin Booker (1), Jason Terry (1), Ray Allen (1), Al Jefferson (1), Shaquille O'Neal (1), Jeff Teague (1), Jimmy Butler III (1), Lamar Odom (1), Ja Morant (1), Manu Ginobili (1), Dennis Schroder (1), Myles Turner (1), Jameer Nelson (1), CJ McCollum (1), Trevor Ariza (1), Julius Randle (1), Goran Dragic (1), Michael Redd (1), De'Aaron Fox (1), David West (1), Kirk Hinrich (1), Tobias Harris (1), Amar'e Stoudemire (1), Metta World Peace (1), Cade Cunningham (1), Mike Bibby (1), Antawn Jamison (1), Paolo Banchero (1), Danny Granger (1), Kemba Walker (1), Monta Ellis (1), Derrick Rose (1), Jermaine O'Neal (1), Marcin Gortat (1), Jamal Murray (1), Rasheed Wallace (1), Boris Diaw (1), Gerald Wallace (1), Lou Williams (1), Nicolas Batum (1), Richard Jefferson (1), Nene (1), Devin Harris (1), Yao Ming (1), Jarrett Jack (1), Joakim Noah (1), Richard Hamilton (1), Blake Griffin (1), Victor Wembanyama (1), Kenyon Martin (1), Brandon Ingram (1), Kevin Martin (1), Danny Green (1), Andrew Wiggins (1), Bam Adebayo (1), D.J. Augustin (1), Reggie Jackson (1), Chris Webber (1), D'Angelo Russell (1), Harrison Barnes (1), Peja Stojakovic (1), Stephon Marbury (1), Jeff Green (1), Pascal Siakam (1), Eric Bledsoe (1), Enes Freedom (1), Deni Avdija (1), Jason Richardson (1), Taj Gibson (1), Marcus Smart (1), Michael Porter Jr. (1), Franz Wagner (1), Khris Middleton (1), Tyler Herro (1), Karl Malone (1), Eric Gordon (2), Desmond Bane (2), Luol Deng (2), Rashard Lewis (2), Ty Lawson (2), Austin Reaves (2), Kristaps Porzingis (2), Fred VanVleet (2), Victor Oladipo (2), Roy Hibbert (2), JR Smith (2), Tyrese Haliburton (2), Caron Butler (2), Spencer Dinwiddie (2), Ivica Zubac (2), Brandon Roy (2), Jordan Clarkson (2), Rafer Alston (2), Stephen Jackson (2), Jaren Jackson Jr. (2), Brandon Jennings (2), JJ Redick (2), Bobby Portis (2), George Hill (2), Dejounte Murray (2), Gordon Hayward (2), Hedo Turkoglu (2), Gary Payton (2), Tayshaun Prince (2), Jerami Grant (2), Deandre Ayton (2), Tim Hardaway Jr. (2), Ben Simmons (2), Sam Cassell (2), Corey Maggette (2), Darius Garland (2), Antoine Walker (2), Aaron Gordon (2), Jalen Green (2), Larry Hughes (2), Danilo Gallinari (2), Joe Ingles (2), Norman Powell (2), Steve Francis (2), Derrick White (2), Jamal Mashburn (2), Bojan Bogdanovic (2), Mario Chalmers (2), Jalen Williams (2), Wesley Matthews (2), Jerry Stackhouse (2), Ben Gordon (2), Josh Hart (2), Matt Barnes (2), Shareef Abdur-Rahim (2), Malcolm Brogdon (2), Alperen Sengun (2), T.J. Ford (2), Terry Rozier (2), Al-Farouq Aminu (2), Buddy Hield (2), Mikal Bridges (2), RJ Barrett (2), Mike Dunleavy (2), Antonio McDyess (2), Kelly Olynyk (2), OG Anunoby (2), Marcus Morris Sr. (2), Caris LeVert (2), Jae Crowder (2), Channing Frye (2), Michael Finley (2), Jordan Poole (2), John Salmons (2), Leandro Barbosa (2), Dillon Brooks (2), Andrew Bynum (2), Brandon Bass (2), Josh Howard (2), Scottie Barnes (2), Earl Boykins (2), Aaron Brooks (2), Ryan Anderson (2), Marco Belinelli (2), Latrell Sprewell (2), Donyell Marshall (2), Wally Szczerbiak (2), Nate Robinson (2), Alec Burks (2), Alex Caruso (2), Anthony Johnson (2), Malik Monk (2), Will Barton (2), Evan Mobley (2), Cameron Johnson (2), Montrezl Harrell (2), Eddie Jones (2), Lance Stephenson (2), Nick Van Exel (2), Gary Trent Jr. (2), Amen Thompson (2), Bogdan Bogdanovic (2), Cameron Payne (2), Monte Morris (2), P.J. Washington (2), Reggie Miller (2), Kevin Huerter (3), Bennedict Mathurin (3), Donte DiVincenzo (3), Avery Bradley (3), Luguentz Dort (3), Austin Rivers (3), Jaden McDaniels (3), Bruce Bowen (3), Chet Holmgren (3), Andrew Nembhard (3), Damon Jones (3), Payton Pritchard (3), Raja Bell (3), De'Andre Hunter (3), Bonzi Wells (3), Trey Burke (3), Stephon Castle (3), Chandler Parsons (3), Dario Saric (3), DeMarre Carroll (3), Grayson Allen (3), Clifford Robinson (3), Tim Thomas (3), Bruce Brown (3), Keith Van Horn (3), Jonathan Kuminga (3), VJ Edgecombe (3), Glen Davis (3), Duncan Robinson (3), Antonio Davis (3), Malik Rose (3), Troy Hudson (3), Nikola Mirotic (3), Luke Kennard (3), Bobby Jackson (3), Andres Nocioni (3), Ayo Dosunmu (3), Timofey Mozgov (3), Nenad Krstic (3), Seth Curry (3), Anthony Parker (3), Rodney Hood (3), Rui Hachimura (3), Eddie House (3), Maxi Kleber (3), Joe Harris (3), Chris Boucher (3), Jannero Pargo (3), Voshon Lenard (3), Terance Mann (3), Scoot Henderson (3), Elden Campbell (3), Brandin Podziemski (3), Aaron Nesmith (3), Ajay Mitchell (3), Meyers Leonard (3), Mikki Moore (3), Daniel Gibson (3), James Jones (3), Gabe Vincent (3), Juan Dixon (3), Ty Jerome (3), Caleb Martin (3), Grant Williams (3), Moses Moody (3), Miles McBride (3), Dylan Harper (3), Steve Smith (3), Scotty Pippen Jr. (4), Timothe Luwawu-Cabarrot (4)

</details>

### `points-finals`

**Since 2001-02 (through 2025-26), name a player who scored 40 or more points in a Finals game.**

15 valid answers, difficulty **medium**, tiers: 1: 14, 2: 1 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), Kevin Durant (1), Kobe Bryant (1), Russell Westbrook (1), Stephen Curry (1), Dwyane Wade (1), Giannis Antetokounmpo (1), Nikola Jokic (1), Jalen Brunson (1), Kyrie Irving (1), Devin Booker (1), Shaquille O'Neal (1), Jimmy Butler III (1), Khris Middleton (1), Jalen Williams (2)

</details>

**Since 2001-02 (through 2025-26), name a player who scored 30 or more points in a Finals game.**

39 valid answers, difficulty **medium**, tiers: 1: 36, 2: 3 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), Kevin Durant (1), Kobe Bryant (1), Chris Paul (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Dirk Nowitzki (1), Stephen Curry (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Jason Kidd (1), Tony Parker (1), Dwyane Wade (1), Paul Pierce (1), Giannis Antetokounmpo (1), Nikola Jokic (1), Jayson Tatum (1), Draymond Green (1), Chauncey Billups (1), Jalen Brunson (1), Jaylen Brown (1), Kyrie Irving (1), Klay Thompson (1), Kawhi Leonard (1), Devin Booker (1), Jason Terry (1), Ray Allen (1), Shaquille O'Neal (1), Jimmy Butler III (1), Jamal Murray (1), Richard Hamilton (1), Victor Wembanyama (1), Kenyon Martin (1), Pascal Siakam (1), Khris Middleton (1), Rashard Lewis (2), Jalen Williams (2), OG Anunoby (2)

</details>

**Since 2001-02 (through 2025-26), name a player who scored 20 or more points in a Finals game.**

98 valid answers, difficulty **easy**, tiers: 1: 61, 2: 23, 3: 12, 4: 2 (2 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Chris Paul (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Pau Gasol (1), Dirk Nowitzki (1), Kevin Garnett (1), Stephen Curry (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Rajon Rondo (1), Jason Kidd (1), Tony Parker (1), Kyle Lowry (1), Dwyane Wade (1), Paul Pierce (1), Shawn Marion (1), Al Horford (1), Giannis Antetokounmpo (1), Jrue Holiday (1), Kevin Love (1), Nikola Jokic (1), Jayson Tatum (1), Andre Iguodala (1), Draymond Green (1), Serge Ibaka (1), Chauncey Billups (1), Jalen Brunson (1), Jaylen Brown (1), Kyrie Irving (1), Karl-Anthony Towns (1), Klay Thompson (1), Chris Bosh (1), Kawhi Leonard (1), Marc Gasol (1), Devin Booker (1), Jason Terry (1), Ray Allen (1), Shaquille O'Neal (1), Jimmy Butler III (1), Lamar Odom (1), Manu Ginobili (1), De'Aaron Fox (1), Metta World Peace (1), Jamal Murray (1), Rasheed Wallace (1), Richard Hamilton (1), Victor Wembanyama (1), Kenyon Martin (1), Danny Green (1), Andrew Wiggins (1), Bam Adebayo (1), Pascal Siakam (1), Marcus Smart (1), Khris Middleton (1), Tyler Herro (1), Rashard Lewis (2), Kristaps Porzingis (2), Fred VanVleet (2), JR Smith (2), Tyrese Haliburton (2), Rafer Alston (2), Hedo Turkoglu (2), Deandre Ayton (2), Antoine Walker (2), Aaron Gordon (2), Shaun Livingston (2), Derrick White (2), Mario Chalmers (2), Jalen Williams (2), Mike Miller (2), Mikal Bridges (2), Kelly Olynyk (2), OG Anunoby (2), Andrew Bynum (2), Josh Howard (2), Alex Caruso (2), Matthew Dellavedova (2), Robert Horry (2), Bennedict Mathurin (3), Chet Holmgren (3), Stephon Castle (3), Bruce Brown (3), Duncan Robinson (3), Timofey Mozgov (3), Kerry Kittles (3), Gabe Vincent (3), Sasha Vujacic (3), Obi Toppin (3), Gary Neal (3), Dylan Harper (3), Lucious Harris (4), Leon Powe (4)

</details>

### `triple-double-regular`

**Since 2001-02 (through 2025-26), name a player who recorded a triple-double in a regular-season game.**

248 valid answers, difficulty **easy**, tiers: 1: 122, 2: 79, 3: 28, 4: 15, 5: 4 (19 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Chris Paul (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Pau Gasol (1), Joel Embiid (1), Dirk Nowitzki (1), Kevin Garnett (1), Steve Nash (1), Allen Iverson (1), Ben Wallace (1), Stephen Curry (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Rajon Rondo (1), Damian Lillard (1), Jason Kidd (1), Carmelo Anthony (1), Tony Parker (1), Tracy McGrady (1), Josh Smith (1), DeMar DeRozan (1), Kyle Lowry (1), Dwyane Wade (1), Nikola Vucevic (1), Andre Miller (1), Paul Pierce (1), Zach Randolph (1), Bradley Beal (1), Al Horford (1), Giannis Antetokounmpo (1), Jrue Holiday (1), Kevin Love (1), Nikola Jokic (1), Jayson Tatum (1), Andrei Kirilenko (1), Andre Iguodala (1), Trae Young (1), Joe Johnson (1), Draymond Green (1), Jonas Valanciunas (1), John Wall (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Paul Millsap (1), Isaiah Thomas (1), Serge Ibaka (1), Chauncey Billups (1), Elton Brand (1), Jaylen Brown (1), Carlos Boozer (1), Marcus Camby (1), Kyrie Irving (1), Karl-Anthony Towns (1), Tyrese Maxey (1), Baron Davis (1), Jose Calderon (1), Ricky Rubio (1), Kawhi Leonard (1), Marc Gasol (1), Raymond Felton (1), Clint Capela (1), Jason Terry (1), Ray Allen (1), Jimmy Butler III (1), Lamar Odom (1), Ja Morant (1), Zion Williamson (1), DeMarcus Cousins (1), David Lee (1), CJ McCollum (1), Trevor Ariza (1), Julius Randle (1), Goran Dragic (1), De'Aaron Fox (1), David West (1), Domantas Sabonis (1), Kirk Hinrich (1), Tobias Harris (1), Cade Cunningham (1), Mike Bibby (1), Paolo Banchero (1), Kemba Walker (1), Mo Williams (1), Derrick Rose (1), Jermaine O'Neal (1), Jamal Murray (1), Steven Adams (1), Boris Diaw (1), LaMelo Ball (1), Lou Williams (1), T.J. McConnell (1), Nicolas Batum (1), Richard Jefferson (1), Jarrett Jack (1), Joakim Noah (1), Blake Griffin (1), Victor Wembanyama (1), Earl Watson (1), Brandon Ingram (1), Andrew Wiggins (1), Bam Adebayo (1), Reggie Jackson (1), Chris Webber (1), D'Angelo Russell (1), JaVale McGee (1), Pascal Siakam (1), Eric Bledsoe (1), Mason Plumlee (1), Darren Collison (1), Deni Avdija (1), Marcus Smart (1), Khris Middleton (1), Drew Gooden (1), Tyler Herro (1), Karl Malone (1), Steve Blake (2), Desmond Bane (2), Jamaal Tinsley (2), Jusuf Nurkic (2), Ty Lawson (2), J.J. Barea (2), Austin Reaves (2), Fred VanVleet (2), Victor Oladipo (2), Hassan Whiteside (2), Roy Hibbert (2), Tyus Jones (2), Tyrese Haliburton (2), Brad Miller (2), Caron Butler (2), Spencer Dinwiddie (2), Ivica Zubac (2), Brandon Roy (2), Jordan Clarkson (2), Rafer Alston (2), Stephen Jackson (2), Brandon Jennings (2), Jalen Johnson (2), George Hill (2), Dejounte Murray (2), Greg Monroe (2), Hedo Turkoglu (2), Elfrid Payton (2), Gary Payton (2), Ben Simmons (2), Kyle Kuzma (2), Sam Cassell (2), Darius Garland (2), Antoine Walker (2), Aaron Gordon (2), Beno Udrih (2), Jalen Rose (2), Jalen Green (2), Tyreke Evans (2), Larry Hughes (2), Ramon Sessions (2), Steve Francis (2), Chris Duhon (2), Derrick White (2), Jamal Mashburn (2), Eric Snow (2), Josh Hart (2), Matt Barnes (2), Evan Turner (2), Kyle Anderson (2), Mike Miller (2), Malcolm Brogdon (2), Alperen Sengun (2), Terry Rozier (2), RJ Barrett (2), Miles Bridges (2), Caris LeVert (2), Damon Stoudamire (2), John Salmons (2), Josh Giddey (2), Kenny Thomas (2), Jeremy Lin (2), Scottie Barnes (2), Brandon Knight (2), James Posey (2), Greivis Vasquez (2), Latrell Sprewell (2), Royce O'Neale (2), Kevin Porter Jr. (2), Chuck Hayes (2), Isaiah Hartenstein (2), Lonzo Ball (2), Lance Stephenson (2), Amen Thompson (2), Michael Carter-Williams (2), Tre Jones (2), Dikembe Mutombo (2), Nic Claxton (2), Delon Wright (2), Immanuel Quickley (3), Tomas Satoransky (3), Payton Pritchard (3), Stephon Castle (3), Bruce Brown (3), Dennis Smith Jr. (3), Robert Williams III (3), Luke Kennard (3), Jaime Jaquez Jr. (3), Ayo Dosunmu (3), Markelle Fultz (3), Tim Frazier (3), Mark Jackson (3), Jordan Crawford (3), Ryan Gomes (3), Dyson Daniels (3), Vlade Divac (3), Jalen Suggs (3), Bob Sura (3), Max Strus (3), Larry Sanders (3), Charlie Bell (3), Anfernee Hardaway (3), Shabazz Napier (3), Tony Wroten (3), John Konchar (3), Bilal Coulibaly (3), Derik Queen (3), Trendon Watford (4), Jaylin Williams (4), Scotty Pippen Jr. (4), Tre Mann (4), Jericho Sims (4), Mario Hezonja (4), Terrence Williams (4), Jay Williams (4), Aleksej Pokusevski (4), Rodney White (4), Jalen Pickett (4), Keaton Wallace (4), Jonathan Mogbo (4), Rayan Rupert (4), Theo Pinson (4), Ben Uzoh (5), Jahmai Mashack (5), Bez Mbeng (5), Lachlan Olbrich (5)

</details>

### `triple-double-playoff`

**Since 2001-02 (through 2025-26), name a player who recorded a triple-double in a playoff game.**

42 valid answers, difficulty **easy**, tiers: 1: 35, 2: 7 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Chris Paul (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Pau Gasol (1), Joel Embiid (1), Kevin Garnett (1), Steve Nash (1), Stephen Curry (1), Rajon Rondo (1), Jason Kidd (1), Paul Pierce (1), Giannis Antetokounmpo (1), Jrue Holiday (1), Nikola Jokic (1), Jayson Tatum (1), Draymond Green (1), Paul George (1), Karl-Anthony Towns (1), Baron Davis (1), Ricky Rubio (1), Devin Booker (1), Jimmy Butler III (1), Ja Morant (1), Julius Randle (1), Cade Cunningham (1), Jamal Murray (1), Blake Griffin (1), Victor Wembanyama (1), Bam Adebayo (1), Chris Webber (1), Marcus Smart (1), Victor Oladipo (2), Tyrese Haliburton (2), Gary Payton (2), Ben Simmons (2), Steve Francis (2), Josh Hart (2), Andrew Bynum (2)

</details>

### `triple-double-finals`

No candidates: every threshold gave too few or too many valid answers (see above).

### `rebounds`

**Since 2001-02 (through 2025-26), name a player who grabbed 27 or more rebounds in a game.**

19 valid answers, difficulty **medium**, tiers: 1: 15, 2: 3, 3: 1 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Dwight Howard (1), Tim Duncan (1), Ben Wallace (1), Andre Drummond (1), Rudy Gobert (1), DeAndre Jordan (1), Tyson Chandler (1), Nikola Vucevic (1), Kevin Love (1), Nikola Jokic (1), Marcus Camby (1), Karl-Anthony Towns (1), Domantas Sabonis (1), Andrew Bogut (1), Enes Freedom (1), Jusuf Nurkic (2), Ivica Zubac (2), Andrew Bynum (2), Timofey Mozgov (3)

</details>

**Since 2001-02 (through 2025-26), name a player who grabbed 24 or more rebounds in a game.**

52 valid answers, difficulty **easy**, tiers: 1: 29, 2: 17, 3: 5, 4: 1 (1 at tier 4 or above).

<details><summary>All valid answers</summary>

Dwight Howard (1), Tim Duncan (1), Kevin Garnett (1), Ben Wallace (1), Anthony Davis (1), Andre Drummond (1), Rudy Gobert (1), DeAndre Jordan (1), Tyson Chandler (1), Nikola Vucevic (1), Zach Randolph (1), Shawn Marion (1), Kevin Love (1), Nikola Jokic (1), LaMarcus Aldridge (1), Jonas Valanciunas (1), Paul Millsap (1), Marcus Camby (1), Karl-Anthony Towns (1), Clint Capela (1), Al Jefferson (1), Shaquille O'Neal (1), DeMarcus Cousins (1), Domantas Sabonis (1), Victor Wembanyama (1), Andrew Bogut (1), Enes Freedom (1), Jarrett Allen (1), Reggie Evans (1), Emeka Okafor (2), Jusuf Nurkic (2), Hassan Whiteside (2), Ivica Zubac (2), Erick Dampier (2), Bismack Biyombo (2), Anderson Varejao (2), Ersan Ilyasova (2), John Collins (2), Kenneth Faried (2), Andrew Bynum (2), Andris Biedrins (2), Scottie Barnes (2), Joel Przybilla (2), JJ Hickson (2), Donyell Marshall (2), Chris Wilcox (2), John Henson (3), Lorenzen Wright (3), Timofey Mozgov (3), Mark Williams (3), Walker Kessler (3), Clarence Weatherspoon (4)

</details>

**Since 2001-02 (through 2025-26), name a player who grabbed 18 or more rebounds in a game.**

290 valid answers, difficulty **easy**, tiers: 1: 87, 2: 98, 3: 62, 4: 34, 5: 8, 6: 1 (43 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), Dwight Howard (1), Kevin Durant (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Pau Gasol (1), Joel Embiid (1), Dirk Nowitzki (1), Kevin Garnett (1), Ben Wallace (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Andre Drummond (1), Rajon Rondo (1), Damian Lillard (1), Brook Lopez (1), Rudy Gobert (1), Jason Kidd (1), Carmelo Anthony (1), Josh Smith (1), DeAndre Jordan (1), Tyson Chandler (1), Nikola Vucevic (1), Paul Pierce (1), Zach Randolph (1), Shawn Marion (1), Al Horford (1), Giannis Antetokounmpo (1), Kevin Love (1), Nikola Jokic (1), Jayson Tatum (1), Andrei Kirilenko (1), Draymond Green (1), LaMarcus Aldridge (1), Jonas Valanciunas (1), Paul Millsap (1), Serge Ibaka (1), Elton Brand (1), Carlos Boozer (1), Marcus Camby (1), Karl-Anthony Towns (1), Chris Bosh (1), Marc Gasol (1), Clint Capela (1), Al Jefferson (1), Shaquille O'Neal (1), Jimmy Butler III (1), Lamar Odom (1), DeMarcus Cousins (1), David Lee (1), Lauri Markkanen (1), Julius Randle (1), David West (1), Domantas Sabonis (1), Tobias Harris (1), Amar'e Stoudemire (1), Tristan Thompson (1), Antawn Jamison (1), Samuel Dalembert (1), Paolo Banchero (1), Jermaine O'Neal (1), Marcin Gortat (1), Steven Adams (1), Gerald Wallace (1), Nicolas Batum (1), Richard Jefferson (1), Yao Ming (1), Joakim Noah (1), Zaza Pachulia (1), Blake Griffin (1), Victor Wembanyama (1), Kenyon Martin (1), Andrew Bogut (1), Udonis Haslem (1), Bam Adebayo (1), Chris Webber (1), JaVale McGee (1), Pascal Siakam (1), Mason Plumlee (1), Enes Freedom (1), Deni Avdija (1), Taj Gibson (1), Jarrett Allen (1), Reggie Evans (1), Drew Gooden (1), Karl Malone (1), Zydrunas Ilgauskas (2), Emeka Okafor (2), Luol Deng (2), Rashard Lewis (2), Derrick Favors (2), Jusuf Nurkic (2), Marvin Williams (2), Kristaps Porzingis (2), Brendan Haywood (2), Hassan Whiteside (2), Roy Hibbert (2), Kurt Thomas (2), Troy Murphy (2), Chris Kaman (2), Brad Miller (2), Caron Butler (2), Ivica Zubac (2), Erick Dampier (2), Bobby Portis (2), Jalen Johnson (2), Greg Monroe (2), P.J. Tucker (2), Hedo Turkoglu (2), Bismack Biyombo (2), Chris Andersen (2), Kendrick Perkins (2), Deandre Ayton (2), Amir Johnson (2), Ben Simmons (2), Al Harrington (2), Kyle Kuzma (2), Luis Scola (2), Corey Maggette (2), Antoine Walker (2), Keldon Johnson (2), Danilo Gallinari (2), Jeff Foster (2), Nick Collison (2), Anderson Varejao (2), Ersan Ilyasova (2), John Collins (2), Robin Lopez (2), Mehmet Okur (2), Ed Davis (2), Josh Hart (2), Shareef Abdur-Rahim (2), Nazr Mohammed (2), Mike Miller (2), Jakob Poeltl (2), Corey Brewer (2008-2020) (2), Alperen Sengun (2), Al-Farouq Aminu (2), Mike Dunleavy (2), Antonio McDyess (2), Kris Humphries (2), Christian Wood (2), Kelly Olynyk (2), Jamaal Magloire (2), P.J. Brown (2), Kevon Looney (2), Kenneth Faried (2), Wendell Carter Jr. (2), Jason Thompson (2), Josh Giddey (2), Mitchell Robinson (2), Andrew Bynum (2), Andris Biedrins (2), Josh Howard (2), Kenny Thomas (2), Scottie Barnes (2), Alex Len (2), Joel Przybilla (2), JJ Hickson (2), Larry Nance Jr. (2), James Posey (2), Ryan Anderson (2), Omer Asik (2), Gorgui Dieng (2), Jalen Duren (2), Donyell Marshall (2), Kwame Brown (2), Adonal Foyle (2), Evan Mobley (2), Chuck Hayes (2), Montrezl Harrell (2), Andray Blatche (2), Isaiah Hartenstein (2), Robert Horry (2), JaMychal Green (2), Amen Thompson (2), Jared Dudley (2), Chris Wilcox (2), Dikembe Mutombo (2), Matt Harpring (2), Charlie Villanueva (2), P.J. Washington (2), Marreese Speights (2), Luc Mbah a Moute (2), Nikola Pekovic (3), Trevor Booker (3), Chet Holmgren (3), John Henson (3), Trey Lyles (3), Bonzi Wells (3), Onyeka Okongwu (3), Naz Reid (3), Lorenzen Wright (3), Dorell Wright (3), Keith Van Horn (3), Mark Blount (3), Richaun Holmes (3), Jabari Smith Jr. (3), Alonzo Mourning (3), Malik Rose (3), Isaiah Stewart (3), Willie Cauley-Stein (3), Brian Skinner (3), Anthony Tolliver (3), Andres Nocioni (3), Timofey Mozgov (3), Mark Williams (3), Precious Achiuwa (3), Dale Davis (3), Brian Grant (3), Jarred Vanderbilt (3), Dan Gadzuric (3), Marvin Bagley III (3), DeJuan Blair (3), Vlade Divac (3), Chris Boucher (3), Jared Sullinger (3), Chris Mihm (3), Elden Campbell (3), Mo Bamba (3), Eddie Griffin (3), Kelvin Cato (3), Greg Ostertag (3), Thomas Bryant (3), Michael Olowokandi (3), Larry Sanders (3), Lavoy Allen (3), Walker Kessler (3), Jerome Williams (3), Noah Vonleh (3), Primoz Brezec (3), Shawn Bradley (3), Jalen Smith (3), Jim Jackson (3), Nick Richards (3), Francisco Elson (3), Danny Fortson (3), Maxime Raynaud (3), Marcus Fizer (3), David Robinson (3), Miles Plumlee (3), Donovan Clingan (3), Thomas Robinson (3), Yi Jianlian (3), Derik Queen (3), Jeremy Sochan (3), Kyle Filipowski (4), Clarence Weatherspoon (4), Anthony Mason (4), Kel'el Ware (4), Boban Marjanovic (4), Josh Boone (4), Christian Laettner (4), Cole Aldrich (4), Ervin Johnson (4), Jordan Goodwin (4), Byron Mullens (4), Aaron Gray (4), Jericho Sims (4), Moussa Diabate (4), Alan Henderson (4), Neemias Queta (4), Jabari Walker (4), Tarik Black (4), James Singleton (4), Chimezie Metu (4), Zach Edey (4), Jahidi White (4), Moses Brown (4), Cheick Diallo (4), Greg Oden (4), Dominick Barlow (4), Kris Murray (4), Hakeem Olajuwon (4), Willie Reed (4), Omer Yurtseven (4), Mouhamed Gueye (4), Joey Dorsey (4), Greg Smith (4), Earl Barron (4), Oscar Tshiebwe (5), Alize Johnson (5), Moussa Cisse (5), Jaylen Hoard (5), Andre Brown (5), Vitor Faverani (5), Julian Reese (5), Solomon Alabi (5), Adama Sanogo (6)

</details>

### `assists`

**Since 2001-02 (through 2025-26), name a player who recorded 20 or more assists in a game.**

27 valid answers, difficulty **medium**, tiers: 1: 16, 2: 8, 3: 2, 4: 1 (1 at tier 4 or above).

<details><summary>All valid answers</summary>

James Harden (1), Chris Paul (1), Russell Westbrook (1), Luka Doncic (1), Steve Nash (1), Rajon Rondo (1), Jason Kidd (1), Andre Miller (1), Deron Williams (1), Giannis Antetokounmpo (1), Nikola Jokic (1), Trae Young (1), John Wall (1), Baron Davis (1), Reggie Jackson (1), Darren Collison (1), Jamaal Tinsley (2), Fred VanVleet (2), Tyrese Haliburton (2), Brandon Jennings (2), Elfrid Payton (2), Ramon Sessions (2), Brevin Knight (2), Chris Duhon (2), Will Bynum (3), Isaiah Collier (3), Ryan Nembhard (4)

</details>

**Since 2001-02 (through 2025-26), name a player who recorded 16 or more assists in a game.**

118 valid answers, difficulty **easy**, tiers: 1: 61, 2: 40, 3: 14, 4: 3 (3 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Chris Paul (1), Russell Westbrook (1), Luka Doncic (1), Steve Nash (1), Allen Iverson (1), Stephen Curry (1), Rajon Rondo (1), Damian Lillard (1), Jason Kidd (1), Tony Parker (1), Tracy McGrady (1), Kyle Lowry (1), Dwyane Wade (1), Andre Miller (1), Bradley Beal (1), Deron Williams (1), Giannis Antetokounmpo (1), Jrue Holiday (1), Nikola Jokic (1), Andre Iguodala (1), Trae Young (1), Joe Johnson (1), Draymond Green (1), John Wall (1), Gilbert Arenas (1), Chauncey Billups (1), Jalen Brunson (1), Kyrie Irving (1), Baron Davis (1), Jose Calderon (1), Ricky Rubio (1), Raymond Felton (1), Jason Terry (1), Jeff Teague (1), Ja Morant (1), Julius Randle (1), Goran Dragic (1), De'Aaron Fox (1), Domantas Sabonis (1), Kirk Hinrich (1), Cade Cunningham (1), Mike Bibby (1), Kemba Walker (1), Monta Ellis (1), Derrick Rose (1), Jamal Murray (1), Boris Diaw (1), T.J. McConnell (1), Nicolas Batum (1), Devin Harris (1), Richard Hamilton (1), Earl Watson (1), Reggie Jackson (1), D'Angelo Russell (1), Stephon Marbury (1), Eric Bledsoe (1), Darren Collison (1), Steve Blake (2), Desmond Bane (2), Jamaal Tinsley (2), Ty Lawson (2), Austin Reaves (2), Jason Williams (2), Fred VanVleet (2), Tyus Jones (2), Tyrese Haliburton (2), Spencer Dinwiddie (2), Brandon Jennings (2), Jalen Johnson (2), Ish Smith (2), Hedo Turkoglu (2), Elfrid Payton (2), Gary Payton (2), Ben Simmons (2), Sam Cassell (2), Darius Garland (2), Beno Udrih (2), Tyreke Evans (2), Ramon Sessions (2), Brevin Knight (2), Chris Duhon (2), T.J. Ford (2), Damon Stoudamire (2), Josh Giddey (2), Antonio Daniels (2), Randy Foye (2), Aaron Brooks (2), Greivis Vasquez (2), Kris Dunn (2), Anthony Johnson (2), Chucky Atkins (2), Brent Barry (2), Lonzo Ball (2), Nick Van Exel (2), Michael Carter-Williams (2), Cameron Payne (2), John Stockton (2), Immanuel Quickley (3), Andrew Nembhard (3), Damon Jones (3), Jordan Farmar (3), Davion Mitchell (3), Will Bynum (3), Mark Jackson (3), Rod Strickland (3), Shake Milton (3), Isaiah Collier (3), Moochie Norris (3), Kendall Marshall (3), Dan Dickau (3), Brian Roberts (3), Avery Johnson (4), Vince Williams Jr. (4), Ryan Nembhard (4)

</details>

**Since 2001-02 (through 2025-26), name a player who recorded 14 or more assists in a game.**

213 valid answers, difficulty **easy**, tiers: 1: 87, 2: 77, 3: 37, 4: 10, 5: 2 (12 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Chris Paul (1), Russell Westbrook (1), Luka Doncic (1), Pau Gasol (1), Steve Nash (1), Allen Iverson (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Rajon Rondo (1), Damian Lillard (1), Jason Kidd (1), Tony Parker (1), Tracy McGrady (1), DeMar DeRozan (1), Kyle Lowry (1), Dwyane Wade (1), Andre Miller (1), Paul Pierce (1), Mike Conley (1), Bradley Beal (1), Deron Williams (1), Giannis Antetokounmpo (1), Jrue Holiday (1), Nikola Jokic (1), Andre Iguodala (1), Trae Young (1), Joe Johnson (1), Draymond Green (1), John Wall (1), Gilbert Arenas (1), Vince Carter (1), Isaiah Thomas (1), Chauncey Billups (1), Jalen Brunson (1), Kyrie Irving (1), Tyrese Maxey (1), Donovan Mitchell (1), Baron Davis (1), Jamal Crawford (1), Jose Calderon (1), Ricky Rubio (1), Marc Gasol (1), Raymond Felton (1), Devin Booker (1), Jason Terry (1), Jeff Teague (1), Jimmy Butler III (1), Ja Morant (1), Zach LaVine (1), Manu Ginobili (1), Dennis Schroder (1), Jameer Nelson (1), Julius Randle (1), Goran Dragic (1), De'Aaron Fox (1), Domantas Sabonis (1), Kirk Hinrich (1), Cade Cunningham (1), Mike Bibby (1), Kemba Walker (1), Mo Williams (1), Monta Ellis (1), Derrick Rose (1), Jamal Murray (1), Boris Diaw (1), LaMelo Ball (1), T.J. McConnell (1), Nicolas Batum (1), Devin Harris (1), Jarrett Jack (1), Joakim Noah (1), Richard Hamilton (1), Earl Watson (1), D.J. Augustin (1), Reggie Jackson (1), D'Angelo Russell (1), Luke Ridnour (1), Stephon Marbury (1), Eric Bledsoe (1), Darren Collison (1), Deni Avdija (1), Marcus Smart (1), Tyler Herro (1), Steve Blake (2), Desmond Bane (2), Jamaal Tinsley (2), Jusuf Nurkic (2), Ty Lawson (2), J.J. Barea (2), Austin Reaves (2), Jason Williams (2), Fred VanVleet (2), Victor Oladipo (2), Tyus Jones (2), Tyrese Haliburton (2), Spencer Dinwiddie (2), Anfernee Simons (2), Rafer Alston (2), Stephen Jackson (2), Brandon Jennings (2), Jalen Johnson (2), Dejounte Murray (2), Ish Smith (2), Hedo Turkoglu (2), Elfrid Payton (2), Gary Payton (2), Ben Simmons (2), Sam Cassell (2), Darius Garland (2), Antoine Walker (2), Beno Udrih (2), Jalen Rose (2), Tyreke Evans (2), Ramon Sessions (2), Joe Ingles (2), Shaun Livingston (2), Brevin Knight (2), Steve Francis (2), Chris Duhon (2), Derrick White (2), Eric Snow (2), Cory Joseph (2), Mike Miller (2), Malcolm Brogdon (2), Alperen Sengun (2), T.J. Ford (2), RJ Barrett (2), Rodney Stuckey (2), Caris LeVert (2), Damon Stoudamire (2), Josh Giddey (2), Antonio Daniels (2), Randy Foye (2), Jeremy Lin (2), Scottie Barnes (2), Brandon Knight (2), Aaron Brooks (2), Greivis Vasquez (2), Kris Dunn (2), Kevin Porter Jr. (2), Jeff McInnis (2), Nate Robinson (2), Anthony Johnson (2), Malik Monk (2), Chucky Atkins (2), Brent Barry (2), Carlos Arroyo (2), Matthew Dellavedova (2), Lonzo Ball (2), Lance Stephenson (2), Nick Van Exel (2), Amen Thompson (2), Anthony Carter (2), Devonte' Graham (2), Michael Carter-Williams (2), Cameron Payne (2), Delon Wright (2), Darrel Armstrong (2), John Stockton (2), Scottie Pippen (2), Tyronn Lue (3), Ryan Rollins (3), Immanuel Quickley (3), Tomas Satoransky (3), Andrew Nembhard (3), Damon Jones (3), Jordan Farmar (3), Trey Burke (3), Stephon Castle (3), Davion Mitchell (3), Grayson Allen (3), Dennis Smith Jr. (3), Troy Hudson (3), Ayo Dosunmu (3), Seth Curry (3), Will Bynum (3), Markelle Fultz (3), Tim Frazier (3), Alvin Williams (3), Howard Eisley (3), Mark Jackson (3), Scoot Henderson (3), Rod Strickland (3), Brandin Podziemski (3), Reed Sheppard (3), Jonny Flynn (3), Shake Milton (3), Isaiah Collier (3), Moochie Norris (3), Jamal Shead (3), Jason Hart (3), Kendall Marshall (3), Dan Dickau (3), Shane Larkin (3), Brian Roberts (3), Rick Brunson (3), Donald Sloan (3), A.J. Price (4), Theo Maledon (4), Avery Johnson (4), Vince Williams Jr. (4), Chris Childs (4), Terrence Williams (4), Daniss Jenkins (4), Ryan Nembhard (4), Walter Clayton Jr. (4), Keaton Wallace (4), Jahmai Mashack (5), Nikola Topic (5)

</details>

### `threes`

**Since 2001-02 (through 2025-26), name a player who made 11 or more three-pointers in a game.**

21 valid answers, difficulty **medium**, tiers: 1: 9, 2: 7, 3: 3, 4: 2 (2 at tier 4 or above).

<details><summary>All valid answers</summary>

Kobe Bryant (1), Stephen Curry (1), Damian Lillard (1), Deron Williams (1), Kyrie Irving (1), Klay Thompson (1), Zach LaVine (1), CJ McCollum (1), Marcus Smart (1), Robert Covington (2), Fred VanVleet (2), JR Smith (2), Bojan Bogdanovic (2), Trey Murphy III (2), Buddy Hield (2), Donyell Marshall (2), Donte DiVincenzo (3), Malik Beasley (3), Keegan Murray (3), Julian Champagnie (4), AJ Green (4)

</details>

**Since 2001-02 (through 2025-26), name a player who made 9 or more three-pointers in a game.**

122 valid answers, difficulty **easy**, tiers: 1: 43, 2: 49, 3: 24, 4: 6 (6 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kobe Bryant (1), Luka Doncic (1), Stephen Curry (1), Damian Lillard (1), Brook Lopez (1), Carmelo Anthony (1), Bradley Beal (1), Deron Williams (1), Jayson Tatum (1), Joe Johnson (1), Paul George (1), Vince Carter (1), Isaiah Thomas (1), Anthony Edwards (1), Chauncey Billups (1), Jalen Brunson (1), Jaylen Brown (1), Kyrie Irving (1), Karl-Anthony Towns (1), Tyrese Maxey (1), Klay Thompson (1), Donovan Mitchell (1), Jason Terry (1), Ray Allen (1), Zach LaVine (1), CJ McCollum (1), Trevor Ariza (1), Lauri Markkanen (1), Michael Redd (1), Mike Bibby (1), Kemba Walker (1), Jamal Murray (1), LaMelo Ball (1), Nicolas Batum (1), Blake Griffin (1), Danny Green (1), D'Angelo Russell (1), Peja Stojakovic (1), Jason Richardson (1), Marcus Smart (1), Tyler Herro (1), Robert Covington (2), Keyonte George (2), Ty Lawson (2), Austin Reaves (2), Fred VanVleet (2), JR Smith (2), Tyrese Haliburton (2), Caron Butler (2), Anfernee Simons (2), Jaren Jackson Jr. (2), JJ Redick (2), Tim Hardaway Jr. (2), Darius Garland (2), Antoine Walker (2), Aaron Gordon (2), Danilo Gallinari (2), Norman Powell (2), Derrick White (2), Bojan Bogdanovic (2), Mario Chalmers (2), Wesley Matthews (2), Trey Murphy III (2), Ben Gordon (2), Mike Miller (2), Terry Rozier (2), Buddy Hield (2), Nickeil Alexander-Walker (2), Ricky Davis (2), Channing Frye (2), Jordan Poole (2), Coby White (2), Kelly Oubre Jr. (2), Evan Fournier (2), Dillon Brooks (2), Patty Mills (2), Jeremy Lin (2), T.J. Warren (2), Quentin Richardson (2), Latrell Sprewell (2), Kevin Porter Jr. (2), Donyell Marshall (2), Malik Monk (2), Cameron Johnson (2), CJ Miles (2), Terrence Ross (2), Gary Trent Jr. (2), Devonte' Graham (2), Bogdan Bogdanovic (2), Saddiq Bey (2), Donte DiVincenzo (3), Payton Pritchard (3), Malik Beasley (3), Chandler Parsons (3), Grayson Allen (3), Dorell Wright (3), Duncan Robinson (3), Aron Baynes (3), Jodie Meeks (3), Nikola Mirotic (3), Luke Kennard (3), Davis Bertans (3), Keegan Murray (3), Omri Casspi (3), Max Strus (3), Reed Sheppard (3), Toney Douglas (3), Toumani Camara (3), Corey Kispert (3), Landry Shamet (3), Sam Merrill (3), Miles McBride (3), Isaiah Joe (3), Yogi Ferrell (3), Keon Ellis (4), Julian Champagnie (4), Sam Hauser (4), AJ Green (4), Rodrigue Beaubois (4), Dalton Knecht (4)

</details>

**Since 2001-02 (through 2025-26), name a player who made 8 or more three-pointers in a game.**

253 valid answers, difficulty **easy**, tiers: 1: 75, 2: 88, 3: 68, 4: 19, 5: 2, 6: 1 (22 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Chris Paul (1), Russell Westbrook (1), Luka Doncic (1), Dirk Nowitzki (1), Steve Nash (1), Stephen Curry (1), Damian Lillard (1), Brook Lopez (1), Carmelo Anthony (1), Tracy McGrady (1), Kyle Lowry (1), Paul Pierce (1), Mike Conley (1), Bradley Beal (1), Deron Williams (1), Jrue Holiday (1), Kevin Love (1), Jayson Tatum (1), Trae Young (1), Joe Johnson (1), Draymond Green (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Isaiah Thomas (1), Anthony Edwards (1), Chauncey Billups (1), Jalen Brunson (1), Jaylen Brown (1), Kyrie Irving (1), Karl-Anthony Towns (1), Tyrese Maxey (1), Klay Thompson (1), Donovan Mitchell (1), Jamal Crawford (1), Ricky Rubio (1), Devin Booker (1), Jason Terry (1), Ray Allen (1), Zach LaVine (1), Manu Ginobili (1), Dennis Schroder (1), Myles Turner (1), CJ McCollum (1), Trevor Ariza (1), Lauri Markkanen (1), Julius Randle (1), Michael Redd (1), De'Aaron Fox (1), Mike Bibby (1), Kemba Walker (1), Jamal Murray (1), LaMelo Ball (1), Lou Williams (1), Nicolas Batum (1), Blake Griffin (1), Victor Wembanyama (1), Brandon Ingram (1), Danny Green (1), Andrew Wiggins (1), D'Angelo Russell (1), Harrison Barnes (1), Peja Stojakovic (1), Stephon Marbury (1), Jeff Green (1), Pascal Siakam (1), Jason Richardson (1), Marcus Smart (1), Michael Porter Jr. (1), Khris Middleton (1), Tyler Herro (1), Eric Gordon (2), Desmond Bane (2), Robert Covington (2), Keyonte George (2), Ty Lawson (2), Austin Reaves (2), Kristaps Porzingis (2), Fred VanVleet (2), JR Smith (2), Kentavious Caldwell-Pope (2), Tyrese Haliburton (2), Caron Butler (2), Anfernee Simons (2), Jordan Clarkson (2), Rafer Alston (2), Stephen Jackson (2), Jaren Jackson Jr. (2), Brandon Jennings (2), JJ Redick (2), Bobby Portis (2), Dejounte Murray (2), Kyle Korver (2), Jerami Grant (2), Tim Hardaway Jr. (2), Kyle Kuzma (2), Darius Garland (2), Antoine Walker (2), Aaron Gordon (2), Jalen Green (2), Danilo Gallinari (2), Joe Ingles (2), Norman Powell (2), Chris Duhon (2), Derrick White (2), Bojan Bogdanovic (2), Mario Chalmers (2), Wesley Matthews (2), Trey Murphy III (2), Ben Gordon (2), Mike Miller (2), Terry Rozier (2), Buddy Hield (2), Mikal Bridges (2), Mike Dunleavy (2), Christian Wood (2), Nickeil Alexander-Walker (2), Ricky Davis (2), Jae Crowder (2), Channing Frye (2), Michael Finley (2), Damon Stoudamire (2), Jordan Poole (2), Coby White (2), Leandro Barbosa (2), Kelly Oubre Jr. (2), Evan Fournier (2), Dillon Brooks (2), Brandon Miller (2), Mike James (2002-2014) (2), Patty Mills (2), Randy Foye (2), Jeremy Lin (2), T.J. Warren (2), Ryan Anderson (2), Quentin Richardson (2), Devin Vassell (2), Latrell Sprewell (2), Kevin Porter Jr. (2), Donyell Marshall (2), Nate Robinson (2), Alec Burks (2), Alex Caruso (2), Malik Monk (2), Cameron Johnson (2), Marcus Thornton (2), Kon Knueppel (2), CJ Miles (2), Arron Afflalo (2), Lonzo Ball (2), Terrence Ross (2), Nick Van Exel (2), Gary Trent Jr. (2), Nick Young (2), Devonte' Graham (2), Bogdan Bogdanovic (2), Cameron Payne (2), Justin Holiday (2), Saddiq Bey (2), Kevin Huerter (3), Josh Richardson (3), Donte DiVincenzo (3), Dorian Finney-Smith (3), Avery Bradley (3), Luguentz Dort (3), Vladimir Radmanovic (3), Damon Jones (3), Payton Pritchard (3), Raja Bell (3), Jordan Farmar (3), Trey Burke (3), Onyeka Okongwu (3), David Wesley (3), Malik Beasley (3), Chandler Parsons (3), Grayson Allen (3), Dorell Wright (3), Gerald Green (3), De'Anthony Melton (3), DeShawn Stevenson (3), Duncan Robinson (3), Aron Baynes (3), Jodie Meeks (3), Nikola Mirotic (3), Luke Kennard (3), Wayne Ellington (3), Davis Bertans (3), Taurean Prince (3), Seth Curry (3), Keegan Murray (3), Omri Casspi (3), Rodney Hood (3), Eddie House (3), Quentin Grimes (3), Maxi Kleber (3), Joe Harris (3), Mickael Pietrus (3), Anthony Morrow (3), Nemanja Bjelica (3), Scoot Henderson (3), Jose Alvarado (3), Ben McLemore (3), Brandin Podziemski (3), Aaron Nesmith (3), Carlos Delfino (3), Max Strus (3), Reed Sheppard (3), Toney Douglas (3), Toumani Camara (3), Corey Kispert (3), Allen Crabbe (3), Reggie Bullock Jr. (3), Landry Shamet (3), Sam Merrill (3), Collin Gillespie (3), Bryn Forbes (3), Ty Jerome (3), Jaylen Wells (3), Jevon Carter (3), Max Christie (3), Moses Moody (3), Lonnie Walker IV (3), Aaron Wiggins (3), Miles McBride (3), Isaiah Joe (3), Steve Smith (3), Yogi Ferrell (3), Keon Ellis (4), Julian Champagnie (4), Isaiah Canaan (2014-2019) (4), Juan Carlos Navarro (4), Damyean Dotson (4), Sam Hauser (4), Jordan Goodwin (4), Cam Reddish (4), AJ Green (4), Denzel Valentine (4), Mario Hezonja (4), Troy Daniels (4), Steve Novak (4), Jake LaRavia (4), Rodrigue Beaubois (4), Vit Krejci (4), Reggie Williams (4), Dalton Knecht (4), Tyrese Martin (4), Paul Watson (5), John Poulakidas (5), Alec Peters (6)

</details>

### `blocks`

**Since 2001-02 (through 2025-26), name a player who blocked 10 or more shots in a game.**

20 valid answers, difficulty **medium**, tiers: 1: 13, 2: 5, 3: 1, 4: 1 (1 at tier 4 or above).

<details><summary>All valid answers</summary>

Dwight Howard (1), Ben Wallace (1), Anthony Davis (1), Josh Smith (1), Andrei Kirilenko (1), Serge Ibaka (1), Marcus Camby (1), Clint Capela (1), Amar'e Stoudemire (1), Jermaine O'Neal (1), Joakim Noah (1), Victor Wembanyama (1), JaVale McGee (1), Emeka Okafor (2), Hassan Whiteside (2), Roy Hibbert (2), Andrew Bynum (2), Dikembe Mutombo (2), Larry Sanders (3), Calvin Booth (4)

</details>

**Since 2001-02 (through 2025-26), name a player who blocked 8 or more shots in a game.**

65 valid answers, difficulty **easy**, tiers: 1: 25, 2: 20, 3: 14, 4: 5, 5: 1 (6 at tier 4 or above).

<details><summary>All valid answers</summary>

Dwight Howard (1), Tim Duncan (1), Pau Gasol (1), Ben Wallace (1), Anthony Davis (1), Brook Lopez (1), Rudy Gobert (1), Josh Smith (1), DeAndre Jordan (1), Andrei Kirilenko (1), Serge Ibaka (1), Elton Brand (1), Marcus Camby (1), Marc Gasol (1), Clint Capela (1), Shaquille O'Neal (1), Myles Turner (1), Amar'e Stoudemire (1), Samuel Dalembert (1), Jermaine O'Neal (1), Yao Ming (1), Joakim Noah (1), Victor Wembanyama (1), Andrew Bogut (1), JaVale McGee (1), Emeka Okafor (2), Hassan Whiteside (2), Roy Hibbert (2), Chris Kaman (2), Erick Dampier (2), Jaren Jackson Jr. (2), Chris Andersen (2), Jerami Grant (2), Robin Lopez (2), Nazr Mohammed (2), Nerlens Noel (2), Theo Ratliff (2), Mitchell Robinson (2), Andrew Bynum (2), Rasho Nesterovic (2), Joel Przybilla (2), Adonal Foyle (2), Evan Mobley (2), Daniel Gafford (2), Dikembe Mutombo (2), Stromile Swift (3), Tyrus Thomas (3), Chet Holmgren (3), Raef LaFrentz (3), Alonzo Mourning (3), Robert Williams III (3), Isaiah Stewart (3), Joel Anthony (3), Eddie Griffin (3), Greg Ostertag (3), Larry Sanders (3), Walker Kessler (3), Shawn Bradley (3), Donovan Clingan (3), Keon Clark (4), Anthony Randolph (4), Calvin Booth (4), Sean Williams (4), Hakeem Olajuwon (4), Mamadou N'diaye (5)

</details>

**Since 2001-02 (through 2025-26), name a player who blocked 6 or more shots in a game.**

215 valid answers, difficulty **easy**, tiers: 1: 63, 2: 56, 3: 56, 4: 32, 5: 7, 6: 1 (40 at tier 4 or above).

<details><summary>All valid answers</summary>

Dwight Howard (1), Kevin Durant (1), Tim Duncan (1), Pau Gasol (1), Joel Embiid (1), Dirk Nowitzki (1), Kevin Garnett (1), Ben Wallace (1), Anthony Davis (1), Andre Drummond (1), Brook Lopez (1), Rudy Gobert (1), Josh Smith (1), DeAndre Jordan (1), Tyson Chandler (1), Nikola Vucevic (1), Shawn Marion (1), Al Horford (1), Giannis Antetokounmpo (1), Jrue Holiday (1), Jayson Tatum (1), Andrei Kirilenko (1), Draymond Green (1), LaMarcus Aldridge (1), Jonas Valanciunas (1), Paul Millsap (1), Serge Ibaka (1), Elton Brand (1), Marcus Camby (1), Karl-Anthony Towns (1), Chris Bosh (1), Kawhi Leonard (1), Marc Gasol (1), Clint Capela (1), Al Jefferson (1), Shaquille O'Neal (1), Lamar Odom (1), Myles Turner (1), DeMarcus Cousins (1), David West (1), Rudy Gay (1), Amar'e Stoudemire (1), Samuel Dalembert (1), Danny Granger (1), Shane Battier (1), Jermaine O'Neal (1), Marcin Gortat (1), Steven Adams (1), Rasheed Wallace (1), Boris Diaw (1), Gerald Wallace (1), Yao Ming (1), Joakim Noah (1), Victor Wembanyama (1), Kenyon Martin (1), Andrew Bogut (1), Danny Green (1), Bam Adebayo (1), JaVale McGee (1), Mason Plumlee (1), Enes Freedom (1), Taj Gibson (1), Jarrett Allen (1), Zydrunas Ilgauskas (2), Emeka Okafor (2), Robert Covington (2), Derrick Favors (2), Jusuf Nurkic (2), Kristaps Porzingis (2), Fred VanVleet (2), Brendan Haywood (2), Hassan Whiteside (2), Roy Hibbert (2), Kurt Thomas (2), Chris Kaman (2), Ivica Zubac (2), Erick Dampier (2), Jaren Jackson Jr. (2), Bismack Biyombo (2), Chris Andersen (2), Kendrick Perkins (2), Jerami Grant (2), Amir Johnson (2), Derrick White (2), John Collins (2), Robin Lopez (2), Andrea Bargnani (2), Nazr Mohammed (2), Jakob Poeltl (2), Nerlens Noel (2), Al-Farouq Aminu (2), James Johnson (2), Christian Wood (2), Jamaal Magloire (2), Kevon Looney (2), Markieff Morris (2), Theo Ratliff (2), Spencer Hawes (2), Mitchell Robinson (2), Andrew Bynum (2), Rasho Nesterovic (2), Andris Biedrins (2), Josh Howard (2), Scottie Barnes (2), Alex Len (2), Joel Przybilla (2), Wilson Chandler (2), Gorgui Dieng (2), Jalen Duren (2), Eddy Curry (2), Kwame Brown (2), Adonal Foyle (2), Evan Mobley (2), Daniel Gafford (2), Dewayne Dedmon (2), Dikembe Mutombo (2), Nic Claxton (2), DeSagana Diop (2), P.J. Washington (2), Jahlil Okafor (3), Trevor Booker (3), Stromile Swift (3), Tyrus Thomas (3), Chet Holmgren (3), John Henson (3), Darko Milicic (3), Dorell Wright (3), Ronny Turiaf (3), Jason Maxiell (3), Alex Sarr (3), Matas Buzelis (3), Richaun Holmes (3), Raef LaFrentz (3), Alonzo Mourning (3), Robert Williams III (3), Isaiah Stewart (3), Jordan Hill (3), Brian Skinner (3), Michael Kidd-Gilchrist (3), Joel Anthony (3), Travis Outlaw (3), Dan Gadzuric (3), Peyton Watson (3), Jonathan Isaac (3), Maxi Kleber (3), Kyle O'Quinn (3), Chris Boucher (3), Chris Mihm (3), Elden Campbell (3), Mo Bamba (3), Etan Thomas (3), Brandan Wright (3), Eddie Griffin (3), Kelvin Cato (3), Ekpe Udoh (3), Zach Collins (3), Greg Ostertag (3), Michael Olowokandi (3), Larry Sanders (3), Walker Kessler (3), Luke Kornet (3), Drew Eubanks (3), Shawn Bradley (3), James Jones (3), Jaxson Hayes (3), Jumaine Jones (3), Jerome James (3), Noah Clowney (3), Steven Hunter (3), David Robinson (3), Jamario Moon (3), Donovan Clingan (3), Terrence Jones (3), Yi Jianlian (3), Scot Pollard (3), Keon Clark (4), Isaiah Jackson (4), Kel'el Ware (4), Anthony Randolph (4), Melvin Ely (4), Jock Landale (4), Michael Ruffin (4), Greg Stiemsma (4), Robert Traylor (4), Neemias Queta (4), Isaiah Roby (4), Calvin Booth (4), Jay Huff (4), Vladimir Stepania (4), Damian Jones (4), Salah Mejri (4), David Harrison (4), Dereck Lively II (4), Zach Edey (4), Aleksej Pokusevski (4), Moses Brown (4), Donte Greene (4), Greg Oden (4), Zeljko Rebraca (4), Dragan Bender (4), Jordan Bell (4), Sean Williams (4), Jonathan Bender (4), Hakeem Olajuwon (4), Charles Bassey (4), Christian Koloko (4), Arvydas Sabonis (4), Mamadou N'diaye (5), Bernard James (5), Don Reid (5), Chris Johnson (2011-2013) (5), Joan Beringer (5), Jarvis Varnado (5), Vitor Faverani (5), Edy Tavares (6)

</details>

### `steals`

**Since 2001-02 (through 2025-26), name a player who stole the ball 6 or more times in a game.**

328 valid answers, difficulty **easy**, tiers: 1: 114, 2: 97, 3: 85, 4: 30, 5: 1, 6: 1 (32 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kobe Bryant (1), Chris Paul (1), Russell Westbrook (1), Dirk Nowitzki (1), Kevin Garnett (1), Allen Iverson (1), Ben Wallace (1), Stephen Curry (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Andre Drummond (1), Rajon Rondo (1), Damian Lillard (1), Jason Kidd (1), Carmelo Anthony (1), Tony Parker (1), Tracy McGrady (1), Josh Smith (1), DeMar DeRozan (1), Kyle Lowry (1), Dwyane Wade (1), Nikola Vucevic (1), Andre Miller (1), Paul Pierce (1), Mike Conley (1), Shawn Marion (1), Bradley Beal (1), Deron Williams (1), Jrue Holiday (1), Kevin Love (1), Nikola Jokic (1), Jayson Tatum (1), Andrei Kirilenko (1), Andre Iguodala (1), Joe Johnson (1), Draymond Green (1), John Wall (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Paul Millsap (1), Anthony Edwards (1), Marcus Camby (1), Kyrie Irving (1), Tyrese Maxey (1), Donovan Mitchell (1), Baron Davis (1), Jamal Crawford (1), Chris Bosh (1), Ricky Rubio (1), Kawhi Leonard (1), Raymond Felton (1), Devin Booker (1), Jason Terry (1), Ray Allen (1), Jeff Teague (1), Jimmy Butler III (1), Lamar Odom (1), Manu Ginobili (1), Myles Turner (1), Zion Williamson (1), DeMarcus Cousins (1), Jameer Nelson (1), Thaddeus Young (1), Trevor Ariza (1), Michael Redd (1), De'Aaron Fox (1), Rudy Gay (1), Kirk Hinrich (1), Tobias Harris (1), Amar'e Stoudemire (1), Metta World Peace (1), Cade Cunningham (1), Mike Bibby (1), Antawn Jamison (1), Danny Granger (1), Kemba Walker (1), Mo Williams (1), Monta Ellis (1), Derrick Rose (1), Jamal Murray (1), Steven Adams (1), Rasheed Wallace (1), Gerald Wallace (1), Lou Williams (1), T.J. McConnell (1), Nicolas Batum (1), Nene (1), Devin Harris (1), Zaza Pachulia (1), Victor Wembanyama (1), Kenyon Martin (1), Earl Watson (1), Andrew Wiggins (1), Bam Adebayo (1), Reggie Jackson (1), Chris Webber (1), D'Angelo Russell (1), Collin Sexton (1), Luke Ridnour (1), Peja Stojakovic (1), Stephon Marbury (1), Eric Bledsoe (1), Tony Allen (1), Darren Collison (1), Jason Richardson (1), Marcus Smart (1), Jarrett Allen (1), Franz Wagner (1), Khris Middleton (1), Michael Jordan (1), Karl Malone (1), Steve Blake (2), Robert Covington (2), Luol Deng (2), Jamaal Tinsley (2), Rashard Lewis (2), Ty Lawson (2), Jason Williams (2), Fred VanVleet (2), Victor Oladipo (2), Tyus Jones (2), Derek Fisher (2), Tyrese Haliburton (2), Caron Butler (2), Brandon Roy (2), Rafer Alston (2), Stephen Jackson (2), Jaren Jackson Jr. (2), Brandon Jennings (2), Jalen Johnson (2), Dejounte Murray (2), Kyle Korver (2), P.J. Tucker (2), Ish Smith (2), Thabo Sefolosha (2), Elfrid Payton (2), Ben Simmons (2), Al Harrington (2), Sam Cassell (2), Corey Maggette (2), Aaron Gordon (2), Beno Udrih (2), Tyreke Evans (2), Larry Hughes (2), Joe Ingles (2), Shaun Livingston (2), Brevin Knight (2), Cuttino Mobley (2), Steve Francis (2), Derrick White (2), Mario Chalmers (2), Jalen Williams (2), Matt Barnes (2), Shareef Abdur-Rahim (2), Kyle Anderson (2), Corey Brewer (2008-2020) (2), Nerlens Noel (2), Terry Rozier (2), Al-Farouq Aminu (2), Mikal Bridges (2), RJ Barrett (2), Mike Dunleavy (2), Antonio McDyess (2), Patrick Beverley (2), James Johnson (2), OG Anunoby (2), Caris LeVert (2), Ricky Davis (2), Spencer Hawes (2), Jordan Poole (2), John Salmons (2), Leandro Barbosa (2), Wendell Carter Jr. (2), Kelly Oubre Jr. (2), Josh Giddey (2), Josh Howard (2), Jeremy Lin (2), Scottie Barnes (2), Grant Hill (2), Brandon Knight (2), Earl Boykins (2), Larry Nance Jr. (2), Courtney Lee (2), James Posey (2), Sebastian Telfair (2), Royce O'Neale (2), Maurice Harkless (2), Kris Dunn (2), Kent Bazemore (2), Alex Caruso (2), Marcus Thornton (2), Dwight Powell (2), Andray Blatche (2), Brent Barry (2), Eddie Jones (2), Robert Horry (2), Lonzo Ball (2), Matisse Thybulle (2), Amen Thompson (2), Anthony Carter (2), Michael Carter-Williams (2), Justin Holiday (2), Delon Wright (2), Delonte West (2), Luc Mbah a Moute (2), Darrel Armstrong (2), John Stockton (2), Scottie Pippen (2), Kevin Huerter (3), Josh Richardson (3), Gary Harris (3), Tyrus Thomas (3), Avery Bradley (3), Luguentz Dort (3), Marko Jaric (3), Tomas Satoransky (3), Otto Porter Jr. (3), Andrew Nembhard (3), C.J. Watson (3), Raja Bell (3), De'Andre Hunter (3), Jordan Farmar (3), Wesley Johnson (3), Ian Mahinmi (3), Bonzi Wells (3), Morris Peterson (3), Speedy Claxton (3), David Wesley (3), Doug Christie (3), DeMarre Carroll (3), Dorell Wright (3), Bobby Simmons (3), De'Anthony Melton (3), Dennis Smith Jr. (3), Jared Jeffries (3), Glen Davis (3), Jodie Meeks (3), Ronnie Brewer (3), Willie Cauley-Stein (3), Michael Kidd-Gilchrist (3), Jeremy Lamb (3), Killian Hayes (3), Dale Davis (3), Sergio Rodriguez (3), Eduardo Najera (3), Ronald Murray (3), Omri Casspi (3), Markelle Fultz (3), Ruben Patterson (3), Iman Shumpert (3), Howard Eisley (3), Darius Miles (3), Dyson Daniels (3), Eddie House (3), Jonathan Isaac (3), E'Twaun Moore (3), Jalen Suggs (3), Herbert Jones (3), Marquis Daniels (3), Jeremiah Fears (3), Anthony Morrow (3), Jose Alvarado (3), Toni Kukoc (3), Charlie Bell (3), Reed Sheppard (3), Damien Wilkins (3), Anfernee Hardaway (3), Keith Bogans (3), Toumani Camara (3), Jordan McLaughlin (3), Talen Horton-Tucker (3), Pablo Prigioni (3), Chris Duarte (3), Jerome Williams (3), Ausar Thompson (3), Paul Reed (3), Smush Parker (3), Juan Dixon (3), Lindsey Hunter (3), Ty Jerome (3), Charlie Ward (3), John Konchar (3), Marcus Banks (3), Greg Buckner (3), Frank Ntilikina (3), Alonzo Gee (3), Tari Eason (3), Aaron Wiggins (3), Javonte Green (3), Dahntay Jones (3), Gary Payton II (3), Dylan Harper (3), Anthony Peeler (3), Kyle Filipowski (4), Keon Ellis (4), Troy Brown Jr. (4), Jordan Goodwin (4), Theo Maledon (4), Xavier Tillman (4), Byron Mullens (4), Adrian Griffin (4), Shammond Williams (4), Ryan Bowen (4), Tre Mann (4), Danuel House Jr. (4), Moussa Diabate (4), Ziaire Williams (4), Chris Quinn (4), Chris Crawford (4), Jabari Walker (4), Junior Harrington (4), Walter McCarty (4), Andrew Harrison (4), Chuma Okeke (4), Jay Williams (4), Nique Clifford (4), Greg Anthony (4), Oso Ighodaro (4), Dru Smith (4), Hakeem Olajuwon (4), Taylor Hendricks (4), Will Richard (4), Markel Brown (4), Jahmai Mashack (5), Kadary Richmond (6)

</details>

**Since 2001-02 (through 2025-26), name a player who stole the ball 7 or more times in a game.**

127 valid answers, difficulty **easy**, tiers: 1: 55, 2: 38, 3: 30, 4: 4 (4 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kobe Bryant (1), Chris Paul (1), Russell Westbrook (1), Dirk Nowitzki (1), Kevin Garnett (1), Allen Iverson (1), Ben Wallace (1), Stephen Curry (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Rajon Rondo (1), Jason Kidd (1), Josh Smith (1), Kyle Lowry (1), Dwyane Wade (1), Andre Miller (1), Paul Pierce (1), Mike Conley (1), Shawn Marion (1), Jrue Holiday (1), Nikola Jokic (1), Andrei Kirilenko (1), Draymond Green (1), John Wall (1), Gilbert Arenas (1), Paul George (1), Paul Millsap (1), Kyrie Irving (1), Tyrese Maxey (1), Baron Davis (1), Chris Bosh (1), Ricky Rubio (1), Kawhi Leonard (1), Raymond Felton (1), Jimmy Butler III (1), Manu Ginobili (1), DeMarcus Cousins (1), Jameer Nelson (1), Thaddeus Young (1), Kirk Hinrich (1), Metta World Peace (1), Kemba Walker (1), Monta Ellis (1), Gerald Wallace (1), Lou Williams (1), T.J. McConnell (1), Kenyon Martin (1), Chris Webber (1), D'Angelo Russell (1), Eric Bledsoe (1), Tony Allen (1), Jason Richardson (1), Marcus Smart (1), Steve Blake (2), Robert Covington (2), Jamaal Tinsley (2), Rashard Lewis (2), Ty Lawson (2), Fred VanVleet (2), Victor Oladipo (2), Tyus Jones (2), Caron Butler (2), Brandon Roy (2), Rafer Alston (2), Jalen Johnson (2), Dejounte Murray (2), P.J. Tucker (2), Ish Smith (2), Thabo Sefolosha (2), Elfrid Payton (2), Ben Simmons (2), Al Harrington (2), Larry Hughes (2), Shaun Livingston (2), Brevin Knight (2), Cuttino Mobley (2), Steve Francis (2), Mario Chalmers (2), Shareef Abdur-Rahim (2), Nerlens Noel (2), Mikal Bridges (2), Antonio McDyess (2), OG Anunoby (2), Kelly Oubre Jr. (2), Josh Giddey (2), Josh Howard (2), Earl Boykins (2), Eddie Jones (2), Amen Thompson (2), Michael Carter-Williams (2), Delonte West (2), Josh Richardson (3), C.J. Watson (3), Ian Mahinmi (3), Bonzi Wells (3), Morris Peterson (3), Speedy Claxton (3), Doug Christie (3), De'Anthony Melton (3), Dennis Smith Jr. (3), Ronnie Brewer (3), Willie Cauley-Stein (3), Sergio Rodriguez (3), Ruben Patterson (3), Dyson Daniels (3), Jonathan Isaac (3), Herbert Jones (3), Marquis Daniels (3), Jeremiah Fears (3), Damien Wilkins (3), Anfernee Hardaway (3), Pablo Prigioni (3), Jerome Williams (3), Ausar Thompson (3), Smush Parker (3), Juan Dixon (3), Charlie Ward (3), Marcus Banks (3), Greg Buckner (3), Javonte Green (3), Dylan Harper (3), Adrian Griffin (4), Ryan Bowen (4), Tre Mann (4), Walter McCarty (4)

</details>

**Since 2001-02 (through 2025-26), name a player who stole the ball 8 or more times in a game.**

52 valid answers, difficulty **easy**, tiers: 1: 28, 2: 13, 3: 11 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

James Harden (1), Chris Paul (1), Russell Westbrook (1), Dirk Nowitzki (1), Allen Iverson (1), Rajon Rondo (1), Dwyane Wade (1), Andre Miller (1), Shawn Marion (1), Andrei Kirilenko (1), Draymond Green (1), John Wall (1), Gilbert Arenas (1), Paul George (1), Paul Millsap (1), Kyrie Irving (1), Tyrese Maxey (1), Ricky Rubio (1), Manu Ginobili (1), Thaddeus Young (1), Metta World Peace (1), Kemba Walker (1), Gerald Wallace (1), Lou Williams (1), T.J. McConnell (1), Tony Allen (1), Jason Richardson (1), Marcus Smart (1), Robert Covington (2), Jamaal Tinsley (2), Ty Lawson (2), Brandon Roy (2), Rafer Alston (2), Dejounte Murray (2), Brevin Knight (2), Steve Francis (2), Mario Chalmers (2), Kelly Oubre Jr. (2), Josh Giddey (2), Michael Carter-Williams (2), Delonte West (2), Bonzi Wells (3), Morris Peterson (3), Speedy Claxton (3), Doug Christie (3), Sergio Rodriguez (3), Dyson Daniels (3), Herbert Jones (3), Marquis Daniels (3), Pablo Prigioni (3), Jerome Williams (3), Juan Dixon (3)

</details>

### `ppg-season`

**Since 2001-02 (through 2025-26), name a player who averaged 30 or more points per game in a regular season (minimum 40 games).**

16 valid answers, difficulty **medium**, tiers: 1: 16 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Russell Westbrook (1), Luka Doncic (1), Joel Embiid (1), Allen Iverson (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Damian Lillard (1), Tracy McGrady (1), Dwyane Wade (1), Bradley Beal (1), Giannis Antetokounmpo (1), Jayson Tatum (1)

</details>

**Since 2001-02 (through 2025-26), name a player who averaged 25 or more points per game in a regular season (minimum 40 games).**

60 valid answers, difficulty **easy**, tiers: 1: 60 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Joel Embiid (1), Dirk Nowitzki (1), Allen Iverson (1), Stephen Curry (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Damian Lillard (1), Carmelo Anthony (1), Tracy McGrady (1), DeMar DeRozan (1), Dwyane Wade (1), Paul Pierce (1), Bradley Beal (1), Giannis Antetokounmpo (1), Kevin Love (1), Nikola Jokic (1), Jayson Tatum (1), Trae Young (1), Joe Johnson (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Isaiah Thomas (1), Anthony Edwards (1), Jalen Brunson (1), Jaylen Brown (1), Kyrie Irving (1), Karl-Anthony Towns (1), Tyrese Maxey (1), Donovan Mitchell (1), Kawhi Leonard (1), Devin Booker (1), Ray Allen (1), Shaquille O'Neal (1), Ja Morant (1), Zach LaVine (1), Zion Williamson (1), DeMarcus Cousins (1), Lauri Markkanen (1), Julius Randle (1), Michael Redd (1), De'Aaron Fox (1), Amar'e Stoudemire (1), Cade Cunningham (1), Paolo Banchero (1), Danny Granger (1), Kemba Walker (1), Monta Ellis (1), Derrick Rose (1), Jamal Murray (1), LaMelo Ball (1), Yao Ming (1), Victor Wembanyama (1)

</details>

**Since 2001-02 (through 2025-26), name a player who averaged 20 or more points per game in a regular season (minimum 40 games).**

185 valid answers, difficulty **easy**, tiers: 1: 118, 2: 67 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Chris Paul (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Pau Gasol (1), Joel Embiid (1), Dirk Nowitzki (1), Kevin Garnett (1), Allen Iverson (1), Stephen Curry (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Damian Lillard (1), Brook Lopez (1), Carmelo Anthony (1), Tony Parker (1), Tracy McGrady (1), DeMar DeRozan (1), Kyle Lowry (1), Dwyane Wade (1), Nikola Vucevic (1), Paul Pierce (1), Zach Randolph (1), Mike Conley (1), Shawn Marion (1), Bradley Beal (1), Deron Williams (1), Giannis Antetokounmpo (1), Jrue Holiday (1), Kevin Love (1), Nikola Jokic (1), Jayson Tatum (1), Trae Young (1), Joe Johnson (1), LaMarcus Aldridge (1), John Wall (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Isaiah Thomas (1), Anthony Edwards (1), Elton Brand (1), Jalen Brunson (1), Jaylen Brown (1), Carlos Boozer (1), Kyrie Irving (1), Karl-Anthony Towns (1), Tyrese Maxey (1), Klay Thompson (1), Donovan Mitchell (1), Baron Davis (1), Jamal Crawford (1), Chris Bosh (1), Kawhi Leonard (1), Devin Booker (1), Ray Allen (1), Al Jefferson (1), Shaquille O'Neal (1), Jimmy Butler III (1), Ja Morant (1), Zach LaVine (1), Zion Williamson (1), DeMarcus Cousins (1), David Lee (1), CJ McCollum (1), Lauri Markkanen (1), Julius Randle (1), Goran Dragic (1), Michael Redd (1), De'Aaron Fox (1), David West (1), Rudy Gay (1), Domantas Sabonis (1), Tobias Harris (1), Amar'e Stoudemire (1), Metta World Peace (1), Cade Cunningham (1), Mike Bibby (1), Antawn Jamison (1), Paolo Banchero (1), Danny Granger (1), Kemba Walker (1), Monta Ellis (1), Derrick Rose (1), Jermaine O'Neal (1), Jamal Murray (1), LaMelo Ball (1), Lou Williams (1), Richard Jefferson (1), Devin Harris (1), Yao Ming (1), Richard Hamilton (1), Blake Griffin (1), Victor Wembanyama (1), Brandon Ingram (1), Kevin Martin (1), Andrew Wiggins (1), Bam Adebayo (1), Chris Webber (1), D'Angelo Russell (1), Collin Sexton (1), Peja Stojakovic (1), Stephon Marbury (1), Pascal Siakam (1), Eric Bledsoe (1), Deni Avdija (1), Jason Richardson (1), Michael Porter Jr. (1), Franz Wagner (1), Khris Middleton (1), Tyler Herro (1), Michael Jordan (1), Karl Malone (1), Eric Gordon (2), Desmond Bane (2), Keyonte George (2), Rashard Lewis (2), Austin Reaves (2), Kristaps Porzingis (2), Fred VanVleet (2), Victor Oladipo (2), Tyrese Haliburton (2), Caron Butler (2), Spencer Dinwiddie (2), Brandon Roy (2), Anfernee Simons (2), Jordan Clarkson (2), Stephen Jackson (2), Jaren Jackson Jr. (2), Jalen Johnson (2), Allan Houston (2), Dejounte Murray (2), Gordon Hayward (2), Cam Thomas (2), Gary Payton (2), Jerami Grant (2), Al Harrington (2), Kyle Kuzma (2), Corey Maggette (2), Darius Garland (2), Antoine Walker (2), Jalen Rose (2), Jalen Green (2), Tyreke Evans (2), Larry Hughes (2), Keldon Johnson (2), Norman Powell (2), Cuttino Mobley (2), Steve Francis (2), Jamal Mashburn (2), Bojan Bogdanovic (2), Jalen Williams (2), John Collins (2), Jerry Stackhouse (2), Trey Murphy III (2), Ben Gordon (2), Andrea Bargnani (2), Shareef Abdur-Rahim (2), Malcolm Brogdon (2), Alperen Sengun (2), Terry Rozier (2), Buddy Hield (2), Mikal Bridges (2), RJ Barrett (2), Cooper Flagg (2), Miles Bridges (2), Christian Wood (2), Shaedon Sharpe (2), Caris LeVert (2), Nickeil Alexander-Walker (2), Glenn Robinson (2), Ricky Davis (2), Michael Finley (2), Jordan Poole (2), Coby White (2), Kelly Oubre Jr. (2), Dillon Brooks (2), Brandon Miller (2), Mike James (2002-2014) (2), Jabari Parker (2)

</details>

### `franchises`

**Since 2001-02 (through 2025-26), name a player who played for 9 or more different franchises.**

35 valid answers, difficulty **medium**, tiers: 1: 10, 2: 14, 3: 8, 4: 3 (3 at tier 4 or above).

<details><summary>All valid answers</summary>

Rajon Rondo (1), Andre Miller (1), Isaiah Thomas (1), Jamal Crawford (1), Dennis Schroder (1), Trevor Ariza (1), D.J. Augustin (1), JaVale McGee (1), Jeff Green (1), Drew Gooden (1), Caron Butler (2), Greg Monroe (2), Ish Smith (2), Shaun Livingston (2), Robin Lopez (2), Matt Barnes (2), James Johnson (2), Jae Crowder (2), Theo Ratliff (2), Mike James (2002-2014) (2), Joe Smith (2), Marco Belinelli (2), Justin Holiday (2), Delon Wright (2), Garrett Temple (3), Wayne Ellington (3), Anthony Tolliver (3), Seth Curry (3), Tim Frazier (3), Eddie House (3), Mikki Moore (3), Lou Amundson (3), James Ennis III (4), Ryan Hollins (4), Steve Novak (4)

</details>

**Since 2001-02 (through 2025-26), name a player who played for 7 or more different franchises.**

159 valid answers, difficulty **easy**, tiers: 1: 28, 2: 64, 3: 44, 4: 22, 5: 1 (23 at tier 4 or above).

<details><summary>All valid answers</summary>

Dwight Howard (1), Chris Paul (1), Russell Westbrook (1), Rajon Rondo (1), DeAndre Jordan (1), Tyson Chandler (1), Andre Miller (1), Joe Johnson (1), Vince Carter (1), Isaiah Thomas (1), Jamal Crawford (1), Jose Calderon (1), Raymond Felton (1), Dennis Schroder (1), DeMarcus Cousins (1), Thaddeus Young (1), Trevor Ariza (1), Goran Dragic (1), Mo Williams (1), Richard Jefferson (1), Jarrett Jack (1), D.J. Augustin (1), JaVale McGee (1), Jeff Green (1), Mason Plumlee (1), Taj Gibson (1), Reggie Evans (1), Drew Gooden (1), Steve Blake (2), Kurt Thomas (2), Tyus Jones (2), Caron Butler (2), Stephen Jackson (2), George Hill (2), Greg Monroe (2), P.J. Tucker (2), Ish Smith (2), Bismack Biyombo (2), Al Harrington (2), Beno Udrih (2), Larry Hughes (2), Ramon Sessions (2), Danilo Gallinari (2), Shaun Livingston (2), Brevin Knight (2), Ersan Ilyasova (2), Wesley Matthews (2), Robin Lopez (2), Jerry Stackhouse (2), Cory Joseph (2), Ed Davis (2), Matt Barnes (2), Nazr Mohammed (2), Mike Miller (2), Corey Brewer (2008-2020) (2), Patrick Beverley (2), James Johnson (2), Kris Humphries (2), Christian Wood (2), Kelly Olynyk (2), Jamaal Magloire (2), Marcus Morris Sr. (2), Jae Crowder (2), Markieff Morris (2), Theo Ratliff (2), Juwan Howard (2), Mike James (2002-2014) (2), Patty Mills (2), Randy Foye (2), Jeremy Lin (2), Earl Boykins (2), Courtney Lee (2), Aaron Brooks (2), James Posey (2), Joe Smith (2), Marco Belinelli (2), Sebastian Telfair (2), Michael Beasley (2), Nate Robinson (2), Kwame Brown (2), Alec Burks (2), Marcus Thornton (2), Chucky Atkins (2), Carlos Arroyo (2), CJ Miles (2), Lance Stephenson (2), Jared Dudley (2), Jerryd Bayless (2), Dewayne Dedmon (2), Cameron Payne (2), Justin Holiday (2), Delon Wright (2), Avery Bradley (3), Austin Rivers (3), Vladimir Radmanovic (3), Garrett Temple (3), Shelvin Mack (3), Keyon Dooling (3), Dario Saric (3), Dante Cunningham (3), DeMarre Carroll (3), Ronny Turiaf (3), Gerald Green (3), Jodie Meeks (3), Wayne Ellington (3), Kevin Ollie (3), Brian Skinner (3), Doug McDermott (3), Rasual Butler (3), Anthony Tolliver (3), Seth Curry (3), Ronald Murray (3), Omri Casspi (3), Tim Frazier (3), Eddie House (3), Jannero Pargo (3), Anthony Morrow (3), Mo Bamba (3), Brandan Wright (3), Josh McRoberts (3), Toney Douglas (3), Keith Bogans (3), Tyler Zeller (3), Mikki Moore (3), Noah Vonleh (3), Reggie Bullock Jr. (3), Mike Muscala (3), Maurice Evans (3), Jason Hart (3), Langston Galloway (3), Lou Amundson (3), Shelden Williams (3), Roger Mason Jr. (3), Dahntay Jones (3), Shannon Brown (3), Malik Allen (3), James Ennis III (4), Svi Mykhailiuk (4), Sasha Pavlovic (4), Ryan Hollins (4), Nik Stauskas (4), Dominic McGuire (4), Troy Daniels (4), Calvin Booth (4), Steve Novak (4), Shawne Williams (4), Josh Powell (4), Von Wafer (4), Damian Jones (4), Shaquille Harrison (4), Moses Brown (4), Justin Jackson (4), Mike Wilks (4), Wenyen Gabriel (4), Linton Johnson (4), Earl Barron (4), DeAndre Liggins (4), Stephen Graham (4), Anthony Goldwire (5)

</details>

**Since 2001-02 (through 2025-26), name a player who played for 6 or more different franchises.**

284 valid answers, difficulty **easy**, tiers: 1: 46, 2: 102, 3: 88, 4: 43, 5: 5 (48 at tier 4 or above).

<details><summary>All valid answers</summary>

James Harden (1), Dwight Howard (1), Chris Paul (1), Russell Westbrook (1), Andre Drummond (1), Rajon Rondo (1), Carmelo Anthony (1), Tracy McGrady (1), DeAndre Jordan (1), Tyson Chandler (1), Andre Miller (1), Joe Johnson (1), Jonas Valanciunas (1), Vince Carter (1), Isaiah Thomas (1), Jamal Crawford (1), Jose Calderon (1), Raymond Felton (1), Jason Terry (1), Dennis Schroder (1), DeMarcus Cousins (1), Jameer Nelson (1), Thaddeus Young (1), Trevor Ariza (1), Goran Dragic (1), Metta World Peace (1), Tristan Thompson (1), Antawn Jamison (1), Samuel Dalembert (1), Mo Williams (1), Derrick Rose (1), Jermaine O'Neal (1), Lou Williams (1), Richard Jefferson (1), Jarrett Jack (1), Zaza Pachulia (1), Earl Watson (1), Danny Green (1), D.J. Augustin (1), JaVale McGee (1), Jeff Green (1), Mason Plumlee (1), Darren Collison (1), Taj Gibson (1), Reggie Evans (1), Drew Gooden (1), Steve Blake (2), Kristaps Porzingis (2), Victor Oladipo (2), Kurt Thomas (2), Troy Murphy (2), Tyus Jones (2), Kentavious Caldwell-Pope (2), Caron Butler (2), Rafer Alston (2), Stephen Jackson (2), JJ Redick (2), George Hill (2), Greg Monroe (2), Kyle Korver (2), P.J. Tucker (2), Ish Smith (2), Hedo Turkoglu (2), Bismack Biyombo (2), Al Harrington (2), Beno Udrih (2), Larry Hughes (2), Ramon Sessions (2), Danilo Gallinari (2), Shaun Livingston (2), Brevin Knight (2), Ersan Ilyasova (2), Bojan Bogdanovic (2), Wesley Matthews (2), Robin Lopez (2), Jerry Stackhouse (2), Cory Joseph (2), Ed Davis (2), Matt Barnes (2), Nazr Mohammed (2), Kyle Anderson (2), Mike Miller (2), Corey Brewer (2008-2020) (2), Nerlens Noel (2), Al-Farouq Aminu (2), Buddy Hield (2), Mike Dunleavy (2), Patrick Beverley (2), James Johnson (2), Kris Humphries (2), Christian Wood (2), Kelly Olynyk (2), Jamaal Magloire (2), Marcus Morris Sr. (2), Jae Crowder (2), Channing Frye (2), Markieff Morris (2), Theo Ratliff (2), Spencer Hawes (2), John Salmons (2), Antonio Daniels (2), Juwan Howard (2), Mike James (2002-2014) (2), Patty Mills (2), Randy Foye (2), Brandon Bass (2), Jabari Parker (2), Jeremy Lin (2), Alex Len (2), Brandon Knight (2), Earl Boykins (2), Courtney Lee (2), Aaron Brooks (2), James Posey (2), Joe Smith (2), Ryan Anderson (2), Greivis Vasquez (2), Marco Belinelli (2), Sebastian Telfair (2), Maurice Harkless (2), Kris Dunn (2), Michael Beasley (2), Donyell Marshall (2), Nate Robinson (2), Kwame Brown (2), Alec Burks (2), Anthony Johnson (2), Marcus Thornton (2), Montrezl Harrell (2), Chucky Atkins (2), Isaiah Hartenstein (2), Carlos Arroyo (2), CJ Miles (2), Arron Afflalo (2), Lance Stephenson (2), Nick Young (2), Anthony Carter (2), Jared Dudley (2), Michael Carter-Williams (2), Jerryd Bayless (2), Dewayne Dedmon (2), Cameron Payne (2), Jason Collins (2), Justin Holiday (2), Delon Wright (2), Monte Morris (2), Marreese Speights (2), Luc Mbah a Moute (2), Josh Richardson (3), Tyronn Lue (3), Avery Bradley (3), Austin Rivers (3), Vladimir Radmanovic (3), Raja Bell (3), Wesley Johnson (3), Garrett Temple (3), Malik Beasley (3), Shelvin Mack (3), Keyon Dooling (3), Dario Saric (3), Dante Cunningham (3), Darko Milicic (3), DeMarre Carroll (3), Ronny Turiaf (3), Tim Thomas (3), Gerald Green (3), Derrick Jones Jr. (3), Bruce Brown (3), Dennis Smith Jr. (3), DeShawn Stevenson (3), Jodie Meeks (3), Ronnie Brewer (3), Wayne Ellington (3), Kevin Ollie (3), Brian Skinner (3), Doug McDermott (3), Rasual Butler (3), Anthony Tolliver (3), Taurean Prince (3), Seth Curry (3), Ronald Murray (3), Wesley Person (3), Omri Casspi (3), Tim Frazier (3), Rodney Hood (3), Eddie House (3), Hakim Warrick (3), Jason Smith (3), Jannero Pargo (3), Daniel Theis (3), Anthony Morrow (3), Lee Nailon (3), Torrey Craig (3), Ronnie Price (3), Mo Bamba (3), Brandan Wright (3), Thomas Bryant (3), Josh McRoberts (3), Kenny Anderson (3), Damien Wilkins (3), Toney Douglas (3), Keith Bogans (3), Shake Milton (3), Luke Kornet (3), Tyler Zeller (3), Shabazz Napier (3), Mikki Moore (3), Drew Eubanks (3), Sean Kilpatrick (3), Noah Vonleh (3), Reggie Bullock Jr. (3), Primoz Brezec (3), Landry Shamet (3), Smush Parker (3), Mike Muscala (3), Maurice Evans (3), Francisco Elson (3), Jason Hart (3), Dan Dickau (3), Derrick Williams (3), Jevon Carter (3), Gary Neal (3), Tony Snell (3), Langston Galloway (3), Lou Amundson (3), Shelden Williams (3), Alonzo Gee (3), Devin Brown (3), Roger Mason Jr. (3), Thomas Robinson (3), Dahntay Jones (3), Rick Brunson (3), Jason Kapono (3), Glenn Robinson III (3), Shannon Brown (3), Malik Allen (3), James Ennis III (4), Svi Mykhailiuk (4), Sasha Pavlovic (4), Boban Marjanovic (4), Isaiah Canaan (2014-2019) (4), Ryan Hollins (4), Eric Williams (4), Cole Aldrich (4), Nik Stauskas (4), Shammond Williams (4), Quincy Acy (4), Danuel House Jr. (4), Brian Cardinal (4), Dominic McGuire (4), Juancho Hernangomez (4), Troy Daniels (4), Calvin Booth (4), Steve Novak (4), Shawne Williams (4), Josh Powell (4), Von Wafer (4), Tony Bradley (4), Damian Jones (4), John Lucas III (4), Shaquille Harrison (4), Hilton Armstrong (4), Earl Clark (4), Moses Brown (4), Justin Jackson (4), Solomon Jones (4), Ike Diogu (4), Mike Wilks (4), Justin Anderson (4), Cartier Martin (4), Wenyen Gabriel (4), David Roddy (4), Linton Johnson (4), Eddie Gill (4), Earl Barron (4), DeAndre Liggins (4), Lonny Baxter (4), Stephen Graham (4), Andre Barrett (4), Jamaree Bouyea (5), Alize Johnson (5), Anthony Goldwire (5), Bobby Jones (5), Jared Cunningham (5)

</details>

### `points-game7`

**Since 2001-02 (through 2025-26), name a player who scored 30 or more points in a Game 7.**

46 valid answers, difficulty **easy**, tiers: 1: 40, 2: 4, 3: 2 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Tim Duncan (1), Luka Doncic (1), Joel Embiid (1), Dirk Nowitzki (1), Kevin Garnett (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Tony Parker (1), DeMar DeRozan (1), Kyle Lowry (1), Dwyane Wade (1), Paul Pierce (1), Shawn Marion (1), Bradley Beal (1), Giannis Antetokounmpo (1), Nikola Jokic (1), Jayson Tatum (1), Draymond Green (1), Paul George (1), Chauncey Billups (1), Elton Brand (1), Jaylen Brown (1), Carlos Boozer (1), Tyrese Maxey (1), Donovan Mitchell (1), Kawhi Leonard (1), Jason Terry (1), Shaquille O'Neal (1), Jimmy Butler III (1), CJ McCollum (1), Tobias Harris (1), Cade Cunningham (1), Paolo Banchero (1), Jamal Murray (1), Yao Ming (1), Khris Middleton (1), Victor Oladipo (2), Spencer Dinwiddie (2), Ben Gordon (2), Buddy Hield (2), Donte DiVincenzo (3), Luguentz Dort (3)

</details>

**Since 2001-02 (through 2025-26), name a player who scored 35 or more points in a Game 7.**

23 valid answers, difficulty **medium**, tiers: 1: 22, 3: 1 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), Kevin Durant (1), Tim Duncan (1), Luka Doncic (1), Dirk Nowitzki (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Kyle Lowry (1), Paul Pierce (1), Bradley Beal (1), Giannis Antetokounmpo (1), Jayson Tatum (1), Chauncey Billups (1), Elton Brand (1), Carlos Boozer (1), Donovan Mitchell (1), Kawhi Leonard (1), Shaquille O'Neal (1), Jimmy Butler III (1), CJ McCollum (1), Paolo Banchero (1), Jamal Murray (1), Donte DiVincenzo (3)

</details>

### `points-overtime-game`

**Since 2001-02 (through 2025-26), name a player who scored 55 or more points in a game that went to overtime.**

21 valid answers, difficulty **medium**, tiers: 1: 21 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

James Harden (1), Kobe Bryant (1), Russell Westbrook (1), Luka Doncic (1), Allen Iverson (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Damian Lillard (1), Tony Parker (1), Bradley Beal (1), Giannis Antetokounmpo (1), Nikola Jokic (1), Jayson Tatum (1), LaMarcus Aldridge (1), Gilbert Arenas (1), Jalen Brunson (1), Kyrie Irving (1), Donovan Mitchell (1), DeMarcus Cousins (1), De'Aaron Fox (1), Kemba Walker (1)

</details>

**Since 2001-02 (through 2025-26), name a player who scored 45 or more points in a game that went to overtime.**

70 valid answers, difficulty **easy**, tiers: 1: 56, 2: 13, 3: 1 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Russell Westbrook (1), Luka Doncic (1), Joel Embiid (1), Dirk Nowitzki (1), Allen Iverson (1), Stephen Curry (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Damian Lillard (1), Tony Parker (1), Tracy McGrady (1), DeMar DeRozan (1), Dwyane Wade (1), Andre Miller (1), Paul Pierce (1), Bradley Beal (1), Giannis Antetokounmpo (1), Kevin Love (1), Nikola Jokic (1), Jayson Tatum (1), Trae Young (1), LaMarcus Aldridge (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Paul Millsap (1), Isaiah Thomas (1), Jalen Brunson (1), Jaylen Brown (1), Kyrie Irving (1), Tyrese Maxey (1), Klay Thompson (1), Donovan Mitchell (1), Jamal Crawford (1), Devin Booker (1), Ray Allen (1), Jimmy Butler III (1), Zach LaVine (1), Manu Ginobili (1), DeMarcus Cousins (1), CJ McCollum (1), Lauri Markkanen (1), Michael Redd (1), De'Aaron Fox (1), Cade Cunningham (1), Kemba Walker (1), Richard Hamilton (1), Blake Griffin (1), Brandon Ingram (1), Kevin Martin (1), D'Angelo Russell (1), Victor Oladipo (2), Jerami Grant (2), Aaron Gordon (2), Danilo Gallinari (2), Jamal Mashburn (2), Ben Gordon (2), Mike Miller (2), Mikal Bridges (2), Caris LeVert (2), Ricky Davis (2), Nate Robinson (2), Malik Monk (2), Charlie Villanueva (2), Quentin Grimes (3)

</details>

**Since 2001-02 (through 2025-26), name a player who scored 40 or more points in a game that went to overtime.**

135 valid answers, difficulty **easy**, tiers: 1: 90, 2: 39, 3: 6 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Chris Paul (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Joel Embiid (1), Dirk Nowitzki (1), Steve Nash (1), Allen Iverson (1), Stephen Curry (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Rajon Rondo (1), Damian Lillard (1), Carmelo Anthony (1), Tony Parker (1), Tracy McGrady (1), DeMar DeRozan (1), Dwyane Wade (1), Andre Miller (1), Paul Pierce (1), Zach Randolph (1), Bradley Beal (1), Deron Williams (1), Giannis Antetokounmpo (1), Jrue Holiday (1), Kevin Love (1), Nikola Jokic (1), Jayson Tatum (1), Trae Young (1), Joe Johnson (1), LaMarcus Aldridge (1), John Wall (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Paul Millsap (1), Isaiah Thomas (1), Anthony Edwards (1), Jalen Brunson (1), Jaylen Brown (1), Kyrie Irving (1), Karl-Anthony Towns (1), Tyrese Maxey (1), Klay Thompson (1), Donovan Mitchell (1), Jamal Crawford (1), Chris Bosh (1), Kawhi Leonard (1), Devin Booker (1), Jason Terry (1), Ray Allen (1), Jimmy Butler III (1), Ja Morant (1), Zach LaVine (1), Manu Ginobili (1), Myles Turner (1), DeMarcus Cousins (1), CJ McCollum (1), Lauri Markkanen (1), Julius Randle (1), Michael Redd (1), De'Aaron Fox (1), David West (1), Amar'e Stoudemire (1), Cade Cunningham (1), Mike Bibby (1), Antawn Jamison (1), Paolo Banchero (1), Kemba Walker (1), Monta Ellis (1), Derrick Rose (1), Yao Ming (1), Richard Hamilton (1), Blake Griffin (1), Victor Wembanyama (1), Brandon Ingram (1), Kevin Martin (1), Andrew Wiggins (1), D'Angelo Russell (1), Collin Sexton (1), Stephon Marbury (1), Pascal Siakam (1), Khris Middleton (1), Tyler Herro (1), Michael Jordan (1), Rashard Lewis (2), Victor Oladipo (2), Caron Butler (2), Jordan Clarkson (2), Jaren Jackson Jr. (2), JJ Redick (2), Jalen Johnson (2), Dejounte Murray (2), Gary Payton (2), Jerami Grant (2), Al Harrington (2), Darius Garland (2), Aaron Gordon (2), Jalen Rose (2), Jalen Green (2), Ramon Sessions (2), Danilo Gallinari (2), Norman Powell (2), Steve Francis (2), Jamal Mashburn (2), Trey Murphy III (2), Ben Gordon (2), Mike Miller (2), Terry Rozier (2), Buddy Hield (2), Mikal Bridges (2), Cooper Flagg (2), Caris LeVert (2), Ricky Davis (2), Jordan Poole (2), Aaron Brooks (2), Eddy Curry (2), Nate Robinson (2), Malik Monk (2), Marcus Thornton (2), Arron Afflalo (2), Nick Van Exel (2), Nick Young (2), Charlie Villanueva (2), Trey Burke (3), Grayson Allen (3), Matas Buzelis (3), Pat Connaughton (3), Quentin Grimes (3), Damien Wilkins (3)

</details>

### `points-bench`

**Since 2001-02 (through 2025-26), name a player who scored 30 or more points in a game he did not start.**

313 valid answers, difficulty **easy**, tiers: 1: 73, 2: 102, 3: 95, 4: 35, 5: 7, 6: 1 (43 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Pau Gasol (1), Dirk Nowitzki (1), Steve Nash (1), Allen Iverson (1), Stephen Curry (1), Brook Lopez (1), Tracy McGrady (1), Josh Smith (1), Dwyane Wade (1), Paul Pierce (1), Zach Randolph (1), Jrue Holiday (1), Kevin Love (1), Andrei Kirilenko (1), Gilbert Arenas (1), Vince Carter (1), Isaiah Thomas (1), Chauncey Billups (1), Elton Brand (1), Jaylen Brown (1), Klay Thompson (1), Jamal Crawford (1), Ricky Rubio (1), Jason Terry (1), Shaquille O'Neal (1), Jeff Teague (1), Zach LaVine (1), Manu Ginobili (1), Dennis Schroder (1), Myles Turner (1), Jameer Nelson (1), CJ McCollum (1), Julius Randle (1), Goran Dragic (1), Michael Redd (1), Domantas Sabonis (1), Kirk Hinrich (1), Amar'e Stoudemire (1), Metta World Peace (1), Antawn Jamison (1), Samuel Dalembert (1), Mo Williams (1), Monta Ellis (1), Derrick Rose (1), Jermaine O'Neal (1), LaMelo Ball (1), Lou Williams (1), T.J. McConnell (1), Nicolas Batum (1), Richard Jefferson (1), Yao Ming (1), Jarrett Jack (1), Richard Hamilton (1), Victor Wembanyama (1), Kevin Martin (1), D.J. Augustin (1), Reggie Jackson (1), Chris Webber (1), D'Angelo Russell (1), Peja Stojakovic (1), Stephon Marbury (1), Jeff Green (1), Jason Richardson (1), Taj Gibson (1), Michael Porter Jr. (1), Khris Middleton (1), Drew Gooden (1), Tyler Herro (1), Michael Jordan (1), Eric Gordon (2), Keyonte George (2), Jamaal Tinsley (2), Rashard Lewis (2), Austin Reaves (2), Kristaps Porzingis (2), Victor Oladipo (2), Kurt Thomas (2), JR Smith (2), Kentavious Caldwell-Pope (2), Caron Butler (2), Spencer Dinwiddie (2), Anfernee Simons (2), Jordan Clarkson (2), Stephen Jackson (2), JJ Redick (2), Bobby Portis (2), George Hill (2), Allan Houston (2), Gordon Hayward (2), Cam Thomas (2), Kyle Korver (2), Ish Smith (2), Hedo Turkoglu (2), Tim Hardaway Jr. (2), Al Harrington (2), Sam Cassell (2), Corey Maggette (2), Antoine Walker (2), Jalen Rose (2), Tyreke Evans (2), Larry Hughes (2), Ramon Sessions (2), Danilo Gallinari (2), Norman Powell (2), Cuttino Mobley (2), Jerry Stackhouse (2), Trey Murphy III (2), Ben Gordon (2), Matt Barnes (2), Mike Miller (2), Malcolm Brogdon (2), Buddy Hield (2), Mike Dunleavy (2), Miles Bridges (2), Christian Wood (2), Kelly Olynyk (2), Rodney Stuckey (2), Shaedon Sharpe (2), Marcus Morris Sr. (2), Caris LeVert (2), Glenn Robinson (2), Ricky Davis (2), Jae Crowder (2), Channing Frye (2), Michael Finley (2), Jordan Poole (2), Coby White (2), Leandro Barbosa (2), Kelly Oubre Jr. (2), Juwan Howard (2), Mike James (2002-2014) (2), Patty Mills (2), Jabari Parker (2), Andris Biedrins (2), Jeremy Lin (2), Wilson Chandler (2), Brandon Knight (2), Earl Boykins (2), Joe Smith (2), Ryan Anderson (2), Quentin Richardson (2), Michael Beasley (2), Kevin Porter Jr. (2), Donyell Marshall (2), Wally Szczerbiak (2), Nate Robinson (2), Alec Burks (2), Alex Caruso (2), Anthony Johnson (2), Malik Monk (2), Will Barton (2), Cameron Johnson (2), Marcus Thornton (2), Montrezl Harrell (2), Andray Blatche (2), CJ Miles (2), Terrence Ross (2), Lance Stephenson (2), Nick Van Exel (2), Gary Trent Jr. (2), Nick Young (2), Devonte' Graham (2), Bogdan Bogdanovic (2), Jerryd Bayless (2), Matt Harpring (2), Cameron Payne (2), Charlie Villanueva (2), P.J. Washington (2), Saddiq Bey (2), Marreese Speights (2), Reggie Miller (2), Bennedict Mathurin (3), Stromile Swift (3), Desmond Mason (3), Immanuel Quickley (3), Austin Rivers (3), Damon Jones (3), Payton Pritchard (3), De'Andre Hunter (3), Jordan Farmar (3), Bonzi Wells (3), Trey Burke (3), Garrett Temple (3), Al Thornton (3), Carl Landry (3), Stephon Castle (3), Francisco Garcia (3), Malik Beasley (3), Naz Reid (3), Gerald Green (3), Cole Anthony (3), Jonathan Kuminga (3), Dion Waiters (3), Jabari Smith Jr. (3), Jodie Meeks (3), Troy Hudson (3), Nikola Mirotic (3), Luke Kennard (3), Wayne Ellington (3), Willie Green (3), Davis Bertans (3), Doug McDermott (3), Andres Nocioni (3), Jaime Jaquez Jr. (3), Jeremy Lamb (3), Ayo Dosunmu (3), Naji Marshall (3), Seth Curry (3), Will Bynum (3), Ronald Murray (3), Travis Outlaw (3), Anthony Black (3), Ruben Patterson (3), Marvin Bagley III (3), Brice Sensabaugh (3), Rashad McCants (3), Rodney Hood (3), Darius Miles (3), Rui Hachimura (3), Jordan Crawford (3), Eddie House (3), Joe Harris (3), Chris Boucher (3), Jannero Pargo (3), Anthony Morrow (3), Voshon Lenard (3), Fred Jones (3), Lee Nailon (3), Martell Webster (3), Santi Aldama (3), Scoot Henderson (3), Jose Alvarado (3), Tyler Johnson (3), Corliss Williamson (3), Max Strus (3), Reed Sheppard (3), Toney Douglas (3), Mike Scott (3), Shake Milton (3), Corey Kispert (3), Josh Jackson (3), Shabazz Napier (3), Allen Crabbe (3), Tony Wroten (3), Georges Niang (3), Daniel Gibson (3), Brandon Williams (2022-2026) (3), Landry Shamet (3), Damion Lee (3), Austin Croshere (3), Juan Dixon (3), Bryn Forbes (3), Ty Jerome (3), Obi Toppin (3), Derrick Williams (3), Luther Head (3), Jevon Carter (3), Marcus Fizer (3), Langston Galloway (3), Frank Kaminsky (3), Moritz Wagner (3), Mirza Teletovic (3), Linas Kleiza (3), Lonnie Walker IV (3), Roger Mason Jr. (3), Isaiah Joe (3), Maurice Taylor (4), Chase Budinger (4), Sandro Mamukelashvili (4), Keon Ellis (4), Allonzo Trier (4), Damyean Dotson (4), Alan Anderson (4), Shabazz Muhammad (4), Will Riley (4), Dalano Banton (4), Furkan Korkmaz (4), Kareem Rush (4), Troy Daniels (4), James Wiseman (4), Ian Clark (4), Malachi Flynn (4), Chris Douglas-Roberts (4), Courtney Alexander (4), Rodrigue Beaubois (4), Keita Bates-Diop (4), Salim Stoudamire (4), Terence Davis (4), Walt Williams (4), Reggie Williams (4), Jordan Nwora (4), Skal Labissiere (4), Tyrese Martin (4), Ike Diogu (4), Josh Christopher (4), Wayne Selden (2017-2019) (4), Sean May (4), Jeff Dowtin Jr. (4), Antonio Reeves (4), Jordan McRae (4), Mike Taylor (4), Kennedy Chandler (5), Terrence Shannon Jr. (5), Jett Howard (5), Quincy Douby (5), A.J. Lawson (5), Richie Frahm (5), Justin James (5), Alec Peters (6)

</details>

**Since 2001-02 (through 2025-26), name a player who scored 35 or more points in a game he did not start.**

98 valid answers, difficulty **medium**, tiers: 1: 29, 2: 41, 3: 18, 4: 9, 6: 1 (10 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kobe Bryant (1), Allen Iverson (1), Stephen Curry (1), Brook Lopez (1), Tracy McGrady (1), Dwyane Wade (1), Paul Pierce (1), Kevin Love (1), Gilbert Arenas (1), Vince Carter (1), Klay Thompson (1), Jamal Crawford (1), Ricky Rubio (1), Jason Terry (1), Shaquille O'Neal (1), Zach LaVine (1), Manu Ginobili (1), Michael Redd (1), Samuel Dalembert (1), Jermaine O'Neal (1), Lou Williams (1), Richard Hamilton (1), Kevin Martin (1), Stephon Marbury (1), Jason Richardson (1), Khris Middleton (1), Tyler Herro (1), Keyonte George (2), Austin Reaves (2), JR Smith (2), Kentavious Caldwell-Pope (2), Spencer Dinwiddie (2), Anfernee Simons (2), Jordan Clarkson (2), Bobby Portis (2), Gordon Hayward (2), Cam Thomas (2), Tim Hardaway Jr. (2), Al Harrington (2), Antoine Walker (2), Larry Hughes (2), Danilo Gallinari (2), Ben Gordon (2), Mike Miller (2), Buddy Hield (2), Shaedon Sharpe (2), Glenn Robinson (2), Ricky Davis (2), Coby White (2), Leandro Barbosa (2), Kelly Oubre Jr. (2), Jabari Parker (2), Wilson Chandler (2), Donyell Marshall (2), Nate Robinson (2), Anthony Johnson (2), Malik Monk (2), Will Barton (2), Cameron Johnson (2), Marcus Thornton (2), Terrence Ross (2), Nick Van Exel (2), Gary Trent Jr. (2), Nick Young (2), Devonte' Graham (2), Bogdan Bogdanovic (2), P.J. Washington (2), Reggie Miller (2), Bennedict Mathurin (3), Austin Rivers (3), Payton Pritchard (3), De'Andre Hunter (3), Cole Anthony (3), Nikola Mirotic (3), Davis Bertans (3), Ayo Dosunmu (3), Travis Outlaw (3), Brice Sensabaugh (3), Darius Miles (3), Jordan Crawford (3), Anthony Morrow (3), Santi Aldama (3), Jose Alvarado (3), Josh Jackson (3), Landry Shamet (3), Juan Dixon (3), Alan Anderson (4), Shabazz Muhammad (4), Kareem Rush (4), Ian Clark (4), Malachi Flynn (4), Rodrigue Beaubois (4), Salim Stoudamire (4), Jordan McRae (4), Mike Taylor (4), Alec Peters (6)

</details>

**Since 2001-02 (through 2025-26), name a player who scored 40 or more points in a game he did not start.**

35 valid answers, difficulty **medium**, tiers: 1: 13, 2: 14, 3: 6, 4: 2 (2 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kobe Bryant (1), Allen Iverson (1), Stephen Curry (1), Dwyane Wade (1), Gilbert Arenas (1), Vince Carter (1), Jamal Crawford (1), Manu Ginobili (1), Lou Williams (1), Kevin Martin (1), Jason Richardson (1), JR Smith (2), Jordan Clarkson (2), Cam Thomas (2), Al Harrington (2), Ben Gordon (2), Mike Miller (2), Buddy Hield (2), Nate Robinson (2), Anthony Johnson (2), Malik Monk (2), Nick Van Exel (2), Nick Young (2), Bogdan Bogdanovic (2), P.J. Washington (2), Austin Rivers (3), Payton Pritchard (3), Ayo Dosunmu (3), Brice Sensabaugh (3), Darius Miles (3), Jordan Crawford (3), Malachi Flynn (4), Rodrigue Beaubois (4)

</details>

### `points-loss`

**Since 2001-02 (through 2025-26), name a player who scored 45 or more points in a game his team lost.**

84 valid answers, difficulty **easy**, tiers: 1: 61, 2: 19, 3: 3, 4: 1 (1 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Joel Embiid (1), Dirk Nowitzki (1), Kevin Garnett (1), Steve Nash (1), Allen Iverson (1), Stephen Curry (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Damian Lillard (1), Carmelo Anthony (1), Tracy McGrady (1), DeMar DeRozan (1), Dwyane Wade (1), Paul Pierce (1), Bradley Beal (1), Giannis Antetokounmpo (1), Kevin Love (1), Nikola Jokic (1), Jayson Tatum (1), Trae Young (1), John Wall (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Paul Millsap (1), Anthony Edwards (1), Jalen Brunson (1), Jaylen Brown (1), Kyrie Irving (1), Karl-Anthony Towns (1), Donovan Mitchell (1), Jamal Crawford (1), Devin Booker (1), Jason Terry (1), Ray Allen (1), Ja Morant (1), Zach LaVine (1), DeMarcus Cousins (1), Julius Randle (1), Michael Redd (1), De'Aaron Fox (1), Antawn Jamison (1), Paolo Banchero (1), Kemba Walker (1), Monta Ellis (1), Jamal Murray (1), LaMelo Ball (1), Lou Williams (1), Richard Hamilton (1), Blake Griffin (1), Kevin Martin (1), D'Angelo Russell (1), Stephon Marbury (1), Victor Oladipo (2), Cam Thomas (2), Jerami Grant (2), Darius Garland (2), Aaron Gordon (2), Danilo Gallinari (2), Ben Gordon (2), Mike Miller (2), Mikal Bridges (2), RJ Barrett (2), Cooper Flagg (2), Miles Bridges (2), Ricky Davis (2), Damon Stoudamire (2), Jordan Poole (2), Latrell Sprewell (2), Nate Robinson (2), Terrence Ross (2), Charlie Villanueva (2), Bonzi Wells (3), Darius Miles (3), Quentin Grimes (3), Malachi Flynn (4)

</details>

**Since 2001-02 (through 2025-26), name a player who scored 50 or more points in a game his team lost.**

47 valid answers, difficulty **easy**, tiers: 1: 41, 2: 5, 4: 1 (1 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Tim Duncan (1), Russell Westbrook (1), Dirk Nowitzki (1), Allen Iverson (1), Stephen Curry (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Damian Lillard (1), Carmelo Anthony (1), Tracy McGrady (1), Dwyane Wade (1), Paul Pierce (1), Bradley Beal (1), Giannis Antetokounmpo (1), Kevin Love (1), Nikola Jokic (1), Trae Young (1), John Wall (1), Anthony Edwards (1), Jalen Brunson (1), Kyrie Irving (1), Karl-Anthony Towns (1), Donovan Mitchell (1), Jamal Crawford (1), Devin Booker (1), Ray Allen (1), Zach LaVine (1), DeMarcus Cousins (1), Julius Randle (1), Michael Redd (1), De'Aaron Fox (1), Kemba Walker (1), Jamal Murray (1), LaMelo Ball (1), Richard Hamilton (1), Kevin Martin (1), D'Angelo Russell (1), Darius Garland (2), Aaron Gordon (2), Cooper Flagg (2), Damon Stoudamire (2), Terrence Ross (2), Malachi Flynn (4)

</details>

**Since 2001-02 (through 2025-26), name a player who scored 55 or more points in a game his team lost.**

20 valid answers, difficulty **medium**, tiers: 1: 20 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Russell Westbrook (1), Stephen Curry (1), Damian Lillard (1), Bradley Beal (1), Nikola Jokic (1), Trae Young (1), Anthony Edwards (1), Jalen Brunson (1), Karl-Anthony Towns (1), Donovan Mitchell (1), Devin Booker (1), DeMarcus Cousins (1), Julius Randle (1), Michael Redd (1), De'Aaron Fox (1), Kemba Walker (1)

</details>

### `points-road`

**Since 2001-02 (through 2025-26), name a player who scored 45 or more points in a road game.**

91 valid answers, difficulty **easy**, tiers: 1: 70, 2: 17, 3: 3, 4: 1 (1 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Joel Embiid (1), Steve Nash (1), Allen Iverson (1), Stephen Curry (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Damian Lillard (1), Carmelo Anthony (1), Tony Parker (1), Tracy McGrady (1), DeMar DeRozan (1), Dwyane Wade (1), Andre Miller (1), Paul Pierce (1), Bradley Beal (1), Deron Williams (1), Giannis Antetokounmpo (1), Jrue Holiday (1), Kevin Love (1), Nikola Jokic (1), Jayson Tatum (1), Trae Young (1), LaMarcus Aldridge (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Paul Millsap (1), Anthony Edwards (1), Jalen Brunson (1), Jaylen Brown (1), Kyrie Irving (1), Karl-Anthony Towns (1), Tyrese Maxey (1), Klay Thompson (1), Donovan Mitchell (1), Jamal Crawford (1), Kawhi Leonard (1), Devin Booker (1), Ray Allen (1), Jimmy Butler III (1), Ja Morant (1), Zach LaVine (1), Manu Ginobili (1), DeMarcus Cousins (1), Lauri Markkanen (1), Julius Randle (1), Michael Redd (1), Amar'e Stoudemire (1), Paolo Banchero (1), Kemba Walker (1), Mo Williams (1), Monta Ellis (1), Jamal Murray (1), LaMelo Ball (1), Lou Williams (1), Devin Harris (1), Richard Hamilton (1), Blake Griffin (1), Kevin Martin (1), D'Angelo Russell (1), Stephon Marbury (1), Pascal Siakam (1), Eric Gordon (2), Desmond Bane (2), Rashard Lewis (2), Austin Reaves (2), Fred VanVleet (2), Anfernee Simons (2), Allan Houston (2), Aaron Gordon (2), Ben Gordon (2), Mike Miller (2), Mikal Bridges (2), Caris LeVert (2), Damon Stoudamire (2), Latrell Sprewell (2), Malik Monk (2), Charlie Villanueva (2), Saddiq Bey (2), Bonzi Wells (3), Darius Miles (3), Quentin Grimes (3), Malachi Flynn (4)

</details>

**Since 2001-02 (through 2025-26), name a player who scored 50 or more points in a road game.**

58 valid answers, difficulty **easy**, tiers: 1: 48, 2: 9, 4: 1 (1 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Russell Westbrook (1), Luka Doncic (1), Joel Embiid (1), Allen Iverson (1), Stephen Curry (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Damian Lillard (1), Carmelo Anthony (1), Tony Parker (1), Tracy McGrady (1), Dwyane Wade (1), Andre Miller (1), Bradley Beal (1), Deron Williams (1), Giannis Antetokounmpo (1), Jrue Holiday (1), Kevin Love (1), Nikola Jokic (1), Jayson Tatum (1), Trae Young (1), Gilbert Arenas (1), Vince Carter (1), Anthony Edwards (1), Jalen Brunson (1), Jaylen Brown (1), Kyrie Irving (1), Karl-Anthony Towns (1), Tyrese Maxey (1), Klay Thompson (1), Donovan Mitchell (1), Jamal Crawford (1), Devin Booker (1), Ray Allen (1), Jimmy Butler III (1), Zach LaVine (1), Mo Williams (1), Jamal Murray (1), LaMelo Ball (1), Lou Williams (1), Richard Hamilton (1), Kevin Martin (1), D'Angelo Russell (1), Pascal Siakam (1), Eric Gordon (2), Rashard Lewis (2), Austin Reaves (2), Fred VanVleet (2), Allan Houston (2), Aaron Gordon (2), Caris LeVert (2), Damon Stoudamire (2), Saddiq Bey (2), Malachi Flynn (4)

</details>

**Since 2001-02 (through 2025-26), name a player who scored 55 or more points in a road game.**

22 valid answers, difficulty **medium**, tiers: 1: 22 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Russell Westbrook (1), Luka Doncic (1), Stephen Curry (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Damian Lillard (1), Tony Parker (1), Bradley Beal (1), Deron Williams (1), Nikola Jokic (1), Trae Young (1), Gilbert Arenas (1), Anthony Edwards (1), Jalen Brunson (1), Kyrie Irving (1), Karl-Anthony Towns (1), Donovan Mitchell (1), Devin Booker (1)

</details>

### `rebounds-playoff`

**Since 2001-02 (through 2025-26), name a player who grabbed 22 or more rebounds in a playoff game.**

17 valid answers, difficulty **medium**, tiers: 1: 14, 2: 3 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Dwight Howard (1), Tim Duncan (1), Kevin Garnett (1), Ben Wallace (1), Anthony Davis (1), Rudy Gobert (1), DeAndre Jordan (1), Giannis Antetokounmpo (1), Nikola Jokic (1), Jonas Valanciunas (1), Carlos Boozer (1), Shaquille O'Neal (1), Jermaine O'Neal (1), Victor Wembanyama (1), Bismack Biyombo (2), Deandre Ayton (2), Kevon Looney (2)

</details>

**Since 2001-02 (through 2025-26), name a player who grabbed 18 or more rebounds in a playoff game.**

68 valid answers, difficulty **easy**, tiers: 1: 48, 2: 17, 3: 3 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), Dwight Howard (1), Kevin Durant (1), Tim Duncan (1), Russell Westbrook (1), Pau Gasol (1), Joel Embiid (1), Dirk Nowitzki (1), Kevin Garnett (1), Ben Wallace (1), Anthony Davis (1), Rajon Rondo (1), Rudy Gobert (1), Josh Smith (1), DeAndre Jordan (1), Tyson Chandler (1), Zach Randolph (1), Shawn Marion (1), Giannis Antetokounmpo (1), Kevin Love (1), Nikola Jokic (1), Jayson Tatum (1), Draymond Green (1), LaMarcus Aldridge (1), Jonas Valanciunas (1), Paul Millsap (1), Carlos Boozer (1), Marcus Camby (1), Chris Bosh (1), Marc Gasol (1), Clint Capela (1), Shaquille O'Neal (1), Lamar Odom (1), Amar'e Stoudemire (1), Antawn Jamison (1), Samuel Dalembert (1), Jermaine O'Neal (1), Marcin Gortat (1), Joakim Noah (1), Zaza Pachulia (1), Blake Griffin (1), Victor Wembanyama (1), Andrew Bogut (1), Udonis Haslem (1), Bam Adebayo (1), Mason Plumlee (1), Enes Freedom (1), Jarrett Allen (1), Zydrunas Ilgauskas (2), Hassan Whiteside (2), Roy Hibbert (2), Caron Butler (2), Bobby Portis (2), Bismack Biyombo (2), Kendrick Perkins (2), Deandre Ayton (2), Jeff Foster (2), Mehmet Okur (2), Josh Hart (2), Kevon Looney (2), Mitchell Robinson (2), Andrew Bynum (2), Kenny Thomas (2), James Posey (2), Robert Horry (2), Keith Van Horn (3), Andres Nocioni (3), Jim Jackson (3)

</details>

**Since 2001-02 (through 2025-26), name a player who grabbed 16 or more rebounds in a playoff game.**

113 valid answers, difficulty **easy**, tiers: 1: 71, 2: 33, 3: 8, 4: 1 (1 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), Dwight Howard (1), Kevin Durant (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Pau Gasol (1), Joel Embiid (1), Dirk Nowitzki (1), Kevin Garnett (1), Ben Wallace (1), Anthony Davis (1), Andre Drummond (1), Rajon Rondo (1), Rudy Gobert (1), Jason Kidd (1), Carmelo Anthony (1), Josh Smith (1), DeAndre Jordan (1), Tyson Chandler (1), Nikola Vucevic (1), Paul Pierce (1), Zach Randolph (1), Shawn Marion (1), Al Horford (1), Giannis Antetokounmpo (1), Kevin Love (1), Nikola Jokic (1), Jayson Tatum (1), Draymond Green (1), LaMarcus Aldridge (1), Jonas Valanciunas (1), Paul George (1), Paul Millsap (1), Serge Ibaka (1), Jaylen Brown (1), Carlos Boozer (1), Marcus Camby (1), Karl-Anthony Towns (1), Chris Bosh (1), Kawhi Leonard (1), Marc Gasol (1), Clint Capela (1), Shaquille O'Neal (1), Lamar Odom (1), Thaddeus Young (1), Domantas Sabonis (1), Tobias Harris (1), Amar'e Stoudemire (1), Tristan Thompson (1), Antawn Jamison (1), Samuel Dalembert (1), Paolo Banchero (1), Jermaine O'Neal (1), Marcin Gortat (1), Steven Adams (1), Gerald Wallace (1), Richard Jefferson (1), Joakim Noah (1), Zaza Pachulia (1), Blake Griffin (1), Victor Wembanyama (1), Kenyon Martin (1), Andrew Bogut (1), Udonis Haslem (1), Andrew Wiggins (1), Bam Adebayo (1), Mason Plumlee (1), Enes Freedom (1), Jarrett Allen (1), Drew Gooden (1), Zydrunas Ilgauskas (2), Luol Deng (2), Derrick Favors (2), Hassan Whiteside (2), Roy Hibbert (2), Chris Kaman (2), Brad Miller (2), Caron Butler (2), Ivica Zubac (2), Bobby Portis (2), P.J. Tucker (2), Bismack Biyombo (2), Kendrick Perkins (2), Deandre Ayton (2), Aaron Gordon (2), Jeff Foster (2), John Collins (2), Mehmet Okur (2), Ed Davis (2), Josh Hart (2), Alperen Sengun (2), Antonio McDyess (2), P.J. Brown (2), Kevon Looney (2), Wendell Carter Jr. (2), Mitchell Robinson (2), Andrew Bynum (2), Kenny Thomas (2), James Posey (2), Jalen Duren (2), Evan Mobley (2), Isaiah Hartenstein (2), Robert Horry (2), Chet Holmgren (3), Bonzi Wells (3), Keith Van Horn (3), Andres Nocioni (3), Brian Grant (3), Vlade Divac (3), Jim Jackson (3), David Robinson (3), Keon Clark (4)

</details>

### `rebounds-finals`

**Since 2001-02 (through 2025-26), name a player who grabbed 14 or more rebounds in a Finals game.**

28 valid answers, difficulty **medium**, tiers: 1: 23, 2: 3, 3: 2 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), Dwight Howard (1), Kobe Bryant (1), Tim Duncan (1), Pau Gasol (1), Dirk Nowitzki (1), Kevin Garnett (1), Ben Wallace (1), Anthony Davis (1), Tyson Chandler (1), Al Horford (1), Giannis Antetokounmpo (1), Kevin Love (1), Nikola Jokic (1), Draymond Green (1), Chris Bosh (1), Kawhi Leonard (1), Shaquille O'Neal (1), Lamar Odom (1), Tristan Thompson (1), Victor Wembanyama (1), Andrew Wiggins (1), Bam Adebayo (1), Zydrunas Ilgauskas (2), Deandre Ayton (2), Josh Hart (2), Chet Holmgren (3), David Robinson (3)

</details>

**Since 2001-02 (through 2025-26), name a player who grabbed 16 or more rebounds in a Finals game.**

19 valid answers, difficulty **medium**, tiers: 1: 16, 2: 2, 3: 1 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), Dwight Howard (1), Tim Duncan (1), Pau Gasol (1), Dirk Nowitzki (1), Ben Wallace (1), Tyson Chandler (1), Giannis Antetokounmpo (1), Kevin Love (1), Nikola Jokic (1), Draymond Green (1), Kawhi Leonard (1), Shaquille O'Neal (1), Tristan Thompson (1), Andrew Wiggins (1), Bam Adebayo (1), Zydrunas Ilgauskas (2), Deandre Ayton (2), David Robinson (3)

</details>

### `assists-playoff`

**Since 2001-02 (through 2025-26), name a player who recorded 12 or more assists in a playoff game.**

76 valid answers, difficulty **easy**, tiers: 1: 54, 2: 19, 3: 2, 4: 1 (1 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kobe Bryant (1), Chris Paul (1), Russell Westbrook (1), Luka Doncic (1), Steve Nash (1), Allen Iverson (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Rajon Rondo (1), Damian Lillard (1), Jason Kidd (1), Tony Parker (1), Tracy McGrady (1), Kyle Lowry (1), Dwyane Wade (1), Mike Conley (1), Deron Williams (1), Giannis Antetokounmpo (1), Jrue Holiday (1), Nikola Jokic (1), Jayson Tatum (1), Trae Young (1), Draymond Green (1), John Wall (1), Gilbert Arenas (1), Paul George (1), Isaiah Thomas (1), Anthony Edwards (1), Chauncey Billups (1), Jalen Brunson (1), Jaylen Brown (1), Donovan Mitchell (1), Baron Davis (1), Jose Calderon (1), Devin Booker (1), Jeff Teague (1), Jimmy Butler III (1), Ja Morant (1), Zach LaVine (1), Julius Randle (1), Kirk Hinrich (1), Cade Cunningham (1), Mike Bibby (1), Derrick Rose (1), Jamal Murray (1), T.J. McConnell (1), Richard Hamilton (1), Blake Griffin (1), Reggie Jackson (1), Chris Webber (1), Marcus Smart (1), Tyler Herro (1), Jamaal Tinsley (2), Ty Lawson (2), J.J. Barea (2), Tyrese Haliburton (2), Hedo Turkoglu (2), Gary Payton (2), Ben Simmons (2), Larry Hughes (2), Shaun Livingston (2), Steve Francis (2), Eric Snow (2), Cory Joseph (2), Malcolm Brogdon (2), T.J. Ford (2), Patrick Beverley (2), Caris LeVert (2), Antonio Daniels (2), Scottie Barnes (2), John Stockton (2), Andrew Nembhard (3), Stephon Castle (3), Chris Childs (4)

</details>

**Since 2001-02 (through 2025-26), name a player who recorded 14 or more assists in a playoff game.**

36 valid answers, difficulty **medium**, tiers: 1: 26, 2: 9, 4: 1 (1 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Chris Paul (1), Russell Westbrook (1), Luka Doncic (1), Steve Nash (1), Allen Iverson (1), Stephen Curry (1), Rajon Rondo (1), Jason Kidd (1), Tony Parker (1), Tracy McGrady (1), Dwyane Wade (1), Mike Conley (1), Deron Williams (1), Giannis Antetokounmpo (1), Jrue Holiday (1), Nikola Jokic (1), Trae Young (1), John Wall (1), Gilbert Arenas (1), Jalen Brunson (1), Jeff Teague (1), Ja Morant (1), Kirk Hinrich (1), Tyler Herro (1), Tyrese Haliburton (2), Hedo Turkoglu (2), Gary Payton (2), Ben Simmons (2), Shaun Livingston (2), Malcolm Brogdon (2), T.J. Ford (2), Caris LeVert (2), Scottie Barnes (2), Chris Childs (4)

</details>

**Since 2001-02 (through 2025-26), name a player who recorded 16 or more assists in a playoff game.**

15 valid answers, difficulty **medium**, tiers: 1: 14, 2: 1 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Chris Paul (1), Russell Westbrook (1), Steve Nash (1), Rajon Rondo (1), Jason Kidd (1), Tony Parker (1), Tracy McGrady (1), Deron Williams (1), Jrue Holiday (1), Nikola Jokic (1), Trae Young (1), John Wall (1), Tyrese Haliburton (2)

</details>

### `assists-finals`

**Since 2001-02 (through 2025-26), name a player who recorded 10 or more assists in a Finals game.**

22 valid answers, difficulty **medium**, tiers: 1: 21, 2: 1 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), Kevin Durant (1), Kobe Bryant (1), Chris Paul (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Rajon Rondo (1), Jason Kidd (1), Kyle Lowry (1), Dwyane Wade (1), Paul Pierce (1), Jrue Holiday (1), Nikola Jokic (1), Jayson Tatum (1), Draymond Green (1), Jimmy Butler III (1), Manu Ginobili (1), Jamal Murray (1), Tyrese Haliburton (2)

</details>

### `threes-playoff`

**Since 2001-02 (through 2025-26), name a player who made 7 or more three-pointers in a playoff game.**

83 valid answers, difficulty **easy**, tiers: 1: 37, 2: 31, 3: 15 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Chris Paul (1), Russell Westbrook (1), Luka Doncic (1), Stephen Curry (1), Damian Lillard (1), Kyle Lowry (1), Paul Pierce (1), Mike Conley (1), Al Horford (1), Deron Williams (1), Kevin Love (1), Nikola Jokic (1), Jayson Tatum (1), Draymond Green (1), Paul George (1), Vince Carter (1), Anthony Edwards (1), Chauncey Billups (1), Kyrie Irving (1), Tyrese Maxey (1), Klay Thompson (1), Donovan Mitchell (1), Kawhi Leonard (1), Devin Booker (1), Jason Terry (1), Ray Allen (1), Myles Turner (1), CJ McCollum (1), Jamal Murray (1), Danny Green (1), D'Angelo Russell (1), Jeff Green (1), Jason Richardson (1), Marcus Smart (1), Khris Middleton (1), Eric Gordon (2), Desmond Bane (2), Fred VanVleet (2), JR Smith (2), Tyrese Haliburton (2), Stephen Jackson (2), Dejounte Murray (2), Tim Hardaway Jr. (2), Sam Cassell (2), Antoine Walker (2), Jalen Green (2), Joe Ingles (2), Norman Powell (2), Derrick White (2), Bojan Bogdanovic (2), Mike Miller (2), Terry Rozier (2), Buddy Hield (2), Mike Dunleavy (2), OG Anunoby (2), Marcus Morris Sr. (2), Channing Frye (2), Michael Finley (2), Dillon Brooks (2), Marco Belinelli (2), Latrell Sprewell (2), Alex Caruso (2), Gary Trent Jr. (2), Bogdan Bogdanovic (2), Cameron Payne (2), P.J. Washington (2), Donte DiVincenzo (3), Dorian Finney-Smith (3), Bruce Bowen (3), Damon Jones (3), Raja Bell (3), Naz Reid (3), Duncan Robinson (3), Seth Curry (3), Maxi Kleber (3), Joe Harris (3), Terance Mann (3), Aaron Nesmith (3), Bryn Forbes (3), Grant Williams (3), Miles McBride (3)

</details>

**Since 2001-02 (through 2025-26), name a player who made 8 or more three-pointers in a playoff game.**

32 valid answers, difficulty **medium**, tiers: 1: 16, 2: 11, 3: 5 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Chris Paul (1), Stephen Curry (1), Damian Lillard (1), Paul Pierce (1), Kevin Love (1), Jayson Tatum (1), Draymond Green (1), Paul George (1), Chauncey Billups (1), Klay Thompson (1), Donovan Mitchell (1), Devin Booker (1), Jason Terry (1), Ray Allen (1), Jamal Murray (1), Jason Richardson (1), Desmond Bane (2), Fred VanVleet (2), JR Smith (2), Jalen Green (2), Derrick White (2), Bojan Bogdanovic (2), Buddy Hield (2), Mike Dunleavy (2), Michael Finley (2), Alex Caruso (2), Gary Trent Jr. (2), Donte DiVincenzo (3), Dorian Finney-Smith (3), Duncan Robinson (3), Maxi Kleber (3), Aaron Nesmith (3)

</details>

### `threes-finals`

**Since 2001-02 (through 2025-26), name a player who made 6 or more three-pointers in a Finals game.**

21 valid answers, difficulty **medium**, tiers: 1: 14, 2: 5, 3: 2 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), Kevin Durant (1), Kobe Bryant (1), Stephen Curry (1), Al Horford (1), Kevin Love (1), Jayson Tatum (1), Draymond Green (1), Kyrie Irving (1), Klay Thompson (1), Devin Booker (1), Ray Allen (1), Shane Battier (1), Danny Green (1), Rashard Lewis (2), JR Smith (2), Mike Miller (2), OG Anunoby (2), Jae Crowder (2), Duncan Robinson (3), Gary Neal (3)

</details>

### `blocks-playoff`

**Since 2001-02 (through 2025-26), name a player who blocked 5 or more shots in a playoff game.**

87 valid answers, difficulty **easy**, tiers: 1: 46, 2: 19, 3: 19, 4: 3 (3 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), Dwight Howard (1), Kevin Durant (1), Tim Duncan (1), Pau Gasol (1), Joel Embiid (1), Dirk Nowitzki (1), Kevin Garnett (1), Ben Wallace (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Brook Lopez (1), Rudy Gobert (1), Josh Smith (1), DeAndre Jordan (1), Dwyane Wade (1), Paul Pierce (1), Shawn Marion (1), Al Horford (1), Giannis Antetokounmpo (1), Andrei Kirilenko (1), Draymond Green (1), LaMarcus Aldridge (1), Paul Millsap (1), Serge Ibaka (1), Elton Brand (1), Marcus Camby (1), Karl-Anthony Towns (1), Kawhi Leonard (1), Marc Gasol (1), Clint Capela (1), Shaquille O'Neal (1), Myles Turner (1), David West (1), Amar'e Stoudemire (1), Jermaine O'Neal (1), Marcin Gortat (1), Steven Adams (1), Rasheed Wallace (1), Yao Ming (1), Joakim Noah (1), Victor Wembanyama (1), Andrew Bogut (1), Danny Green (1), Chris Webber (1), JaVale McGee (1), Zydrunas Ilgauskas (2), Brendan Haywood (2), Hassan Whiteside (2), Roy Hibbert (2), Erick Dampier (2), Jaren Jackson Jr. (2), Chris Andersen (2), Kendrick Perkins (2), Jamaal Magloire (2), P.J. Brown (2), Andrew Bynum (2), Joel Przybilla (2), Joe Smith (2), Jalen Duren (2), Evan Mobley (2), Robert Horry (2), Tony Battie (2), Matisse Thybulle (2), Daniel Gafford (2), Tyrus Thomas (3), Chet Holmgren (3), John Henson (3), Raef LaFrentz (3), Alonzo Mourning (3), Robert Williams III (3), Isaiah Stewart (3), Timofey Mozgov (3), Joel Anthony (3), Elden Campbell (3), Zach Collins (3), Greg Ostertag (3), Luke Kornet (3), Ausar Thompson (3), Shawn Bradley (3), James Jones (3), Andre Roberson (3), Jerome James (3), David Robinson (3), Thon Maker (4), Todd MacCulloch (4), Zach Edey (4)

</details>

**Since 2001-02 (through 2025-26), name a player who blocked 6 or more shots in a playoff game.**

37 valid answers, difficulty **medium**, tiers: 1: 22, 2: 7, 3: 7, 4: 1 (1 at tier 4 or above).

<details><summary>All valid answers</summary>

Dwight Howard (1), Tim Duncan (1), Pau Gasol (1), Joel Embiid (1), Kevin Garnett (1), Ben Wallace (1), Anthony Davis (1), Brook Lopez (1), Rudy Gobert (1), Josh Smith (1), Shawn Marion (1), Andrei Kirilenko (1), Draymond Green (1), Serge Ibaka (1), Marc Gasol (1), Clint Capela (1), Shaquille O'Neal (1), David West (1), Rasheed Wallace (1), Joakim Noah (1), Victor Wembanyama (1), JaVale McGee (1), Zydrunas Ilgauskas (2), Roy Hibbert (2), Jaren Jackson Jr. (2), Chris Andersen (2), Kendrick Perkins (2), Jamaal Magloire (2), Andrew Bynum (2), Tyrus Thomas (3), John Henson (3), Raef LaFrentz (3), Robert Williams III (3), Isaiah Stewart (3), Luke Kornet (3), James Jones (3), Zach Edey (4)

</details>

**Since 2001-02 (through 2025-26), name a player who blocked 7 or more shots in a playoff game.**

21 valid answers, difficulty **medium**, tiers: 1: 13, 2: 4, 3: 3, 4: 1 (1 at tier 4 or above).

<details><summary>All valid answers</summary>

Dwight Howard (1), Tim Duncan (1), Ben Wallace (1), Anthony Davis (1), Brook Lopez (1), Rudy Gobert (1), Josh Smith (1), Andrei Kirilenko (1), Draymond Green (1), Serge Ibaka (1), Shaquille O'Neal (1), Rasheed Wallace (1), Victor Wembanyama (1), Roy Hibbert (2), Jaren Jackson Jr. (2), Kendrick Perkins (2), Andrew Bynum (2), Robert Williams III (3), Isaiah Stewart (3), Luke Kornet (3), Zach Edey (4)

</details>

### `steals-playoff`

**Since 2001-02 (through 2025-26), name a player who stole the ball 4 or more times in a playoff game.**

283 valid answers, difficulty **easy**, tiers: 1: 113, 2: 90, 3: 70, 4: 10 (10 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Chris Paul (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Dirk Nowitzki (1), Kevin Garnett (1), Allen Iverson (1), Ben Wallace (1), Stephen Curry (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Andre Drummond (1), Rajon Rondo (1), Damian Lillard (1), Rudy Gobert (1), Jason Kidd (1), Carmelo Anthony (1), Tony Parker (1), Tracy McGrady (1), Josh Smith (1), DeAndre Jordan (1), DeMar DeRozan (1), Kyle Lowry (1), Dwyane Wade (1), Andre Miller (1), Paul Pierce (1), Mike Conley (1), Shawn Marion (1), Bradley Beal (1), Al Horford (1), Deron Williams (1), Jrue Holiday (1), Kevin Love (1), Nikola Jokic (1), Jayson Tatum (1), Andrei Kirilenko (1), Andre Iguodala (1), Joe Johnson (1), Draymond Green (1), LaMarcus Aldridge (1), John Wall (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Paul Millsap (1), Chauncey Billups (1), Jalen Brunson (1), Jaylen Brown (1), Kyrie Irving (1), Karl-Anthony Towns (1), Tyrese Maxey (1), Klay Thompson (1), Donovan Mitchell (1), Baron Davis (1), Jamal Crawford (1), Jose Calderon (1), Ricky Rubio (1), Kawhi Leonard (1), Marc Gasol (1), Raymond Felton (1), Devin Booker (1), Jason Terry (1), Ray Allen (1), Jimmy Butler III (1), Lamar Odom (1), Manu Ginobili (1), Myles Turner (1), Jameer Nelson (1), Thaddeus Young (1), CJ McCollum (1), Trevor Ariza (1), Goran Dragic (1), De'Aaron Fox (1), Kirk Hinrich (1), Tobias Harris (1), Metta World Peace (1), Cade Cunningham (1), Mike Bibby (1), Monta Ellis (1), Derrick Rose (1), Marcin Gortat (1), Jamal Murray (1), Lou Williams (1), T.J. McConnell (1), Nicolas Batum (1), Richard Jefferson (1), Devin Harris (1), Zaza Pachulia (1), Richard Hamilton (1), Blake Griffin (1), Victor Wembanyama (1), Kenyon Martin (1), Danny Green (1), Andrew Wiggins (1), Bam Adebayo (1), Chris Webber (1), Luke Ridnour (1), Pascal Siakam (1), Eric Bledsoe (1), Tony Allen (1), Mason Plumlee (1), Darren Collison (1), Jason Richardson (1), Marcus Smart (1), Jarrett Allen (1), Franz Wagner (1), Khris Middleton (1), Karl Malone (1), Steve Blake (2), Robert Covington (2), Luol Deng (2), Jamaal Tinsley (2), Rashard Lewis (2), Jusuf Nurkic (2), Austin Reaves (2), Kristaps Porzingis (2), Fred VanVleet (2), Victor Oladipo (2), Tyus Jones (2), JR Smith (2), Kentavious Caldwell-Pope (2), Derek Fisher (2), Tyrese Haliburton (2), Caron Butler (2), Anfernee Simons (2), Rafer Alston (2), Stephen Jackson (2), Brandon Jennings (2), George Hill (2), Dejounte Murray (2), Gordon Hayward (2), Kyle Korver (2), P.J. Tucker (2), Hedo Turkoglu (2), Thabo Sefolosha (2), Tayshaun Prince (2), Ben Simmons (2), Al Harrington (2), Darius Garland (2), Antoine Walker (2), Jalen Green (2), Larry Hughes (2), Joe Ingles (2), Brevin Knight (2), Cuttino Mobley (2), Anderson Varejao (2), Derrick White (2), Bojan Bogdanovic (2), Mario Chalmers (2), Jalen Williams (2), Wesley Matthews (2), Eric Snow (2), Mehmet Okur (2), Josh Hart (2), Matt Barnes (2), Evan Turner (2), Nazr Mohammed (2), Kyle Anderson (2), Alperen Sengun (2), Al-Farouq Aminu (2), Mikal Bridges (2), RJ Barrett (2), Patrick Beverley (2), OG Anunoby (2), Rodney Stuckey (2), Marcus Morris Sr. (2), Caris LeVert (2), Nickeil Alexander-Walker (2), Ricky Davis (2), P.J. Brown (2), Jae Crowder (2), Michael Finley (2), John Salmons (2), Kelly Oubre Jr. (2), Brandon Bass (2), Josh Howard (2), T.J. Warren (2), James Posey (2), Quentin Richardson (2), Devin Vassell (2), Latrell Sprewell (2), Royce O'Neale (2), Alex Caruso (2), Chuck Hayes (2), Isaiah Hartenstein (2), O.J. Mayo (2), Robert Horry (2), Matisse Thybulle (2), Gary Trent Jr. (2), Amen Thompson (2), Bogdan Bogdanovic (2), Jared Dudley (2), Cameron Payne (2), Justin Holiday (2), Delon Wright (2), Delonte West (2), Reggie Miller (2), John Stockton (2), Kevin Huerter (3), Josh Richardson (3), Donte DiVincenzo (3), Gary Harris (3), Dorian Finney-Smith (3), Tyrus Thomas (3), Avery Bradley (3), Luguentz Dort (3), Austin Rivers (3), Jaden McDaniels (3), Otto Porter Jr. (3), Bruce Bowen (3), Chet Holmgren (3), Andrew Nembhard (3), Raja Bell (3), Bonzi Wells (3), Morris Peterson (3), Speedy Claxton (3), Onyeka Okongwu (3), Dario Saric (3), Doug Christie (3), DeMarre Carroll (3), Clifford Robinson (3), Bobby Simmons (3), Tim Thomas (3), De'Anthony Melton (3), Bruce Brown (3), Keith Van Horn (3), Glen Davis (3), Duncan Robinson (3), Malik Rose (3), Christian Braun (3), Pat Connaughton (3), Seth Curry (3), Ronald Murray (3), Trenton Hassell (3), Anthony Black (3), Iman Shumpert (3), DeJuan Blair (3), Anthony Parker (3), Devean George (3), Jalen Suggs (3), Herbert Jones (3), Marquis Daniels (3), Martell Webster (3), Tiago Splitter (3), Ron Mercer (3), Brandin Podziemski (3), Toni Kukoc (3), Ajay Mitchell (3), Kerry Kittles (3), Damien Wilkins (3), Anfernee Hardaway (3), Pablo Prigioni (3), Ausar Thompson (3), Daniel Gibson (3), Paul Reed (3), Aaron McKie (3), Jim Jackson (3), Cason Wallace (3), Andre Roberson (3), Jamal Shead (3), Obi Toppin (3), Jevon Carter (3), Isaac Okoro (3), Frank Ntilikina (3), Tari Eason (3), Javonte Green (3), Tony Delk (3), Dylan Harper (3), Julian Champagnie (4), Eric Williams (4), Jaylin Williams (4), Adrian Griffin (4), Brad Wanamaker (4), Ime Udoka (4), Daniss Jenkins (4), Quincy Pondexter (4), Ja'Kobe Walter (4), Chris Chiozza (4)

</details>

**Since 2001-02 (through 2025-26), name a player who stole the ball 5 or more times in a playoff game.**

129 valid answers, difficulty **easy**, tiers: 1: 58, 2: 43, 3: 27, 4: 1 (1 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kobe Bryant (1), Chris Paul (1), Russell Westbrook (1), Luka Doncic (1), Kevin Garnett (1), Allen Iverson (1), Ben Wallace (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Rajon Rondo (1), Rudy Gobert (1), Jason Kidd (1), Carmelo Anthony (1), Tracy McGrady (1), DeMar DeRozan (1), Dwyane Wade (1), Paul Pierce (1), Mike Conley (1), Shawn Marion (1), Bradley Beal (1), Al Horford (1), Deron Williams (1), Jrue Holiday (1), Kevin Love (1), Jayson Tatum (1), Andre Iguodala (1), Joe Johnson (1), Draymond Green (1), John Wall (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Paul Millsap (1), Chauncey Billups (1), Jalen Brunson (1), Donovan Mitchell (1), Baron Davis (1), Jamal Crawford (1), Kawhi Leonard (1), Ray Allen (1), Jimmy Butler III (1), Manu Ginobili (1), Thaddeus Young (1), Metta World Peace (1), Mike Bibby (1), Jamal Murray (1), T.J. McConnell (1), Devin Harris (1), Zaza Pachulia (1), Danny Green (1), Pascal Siakam (1), Tony Allen (1), Mason Plumlee (1), Marcus Smart (1), Jarrett Allen (1), Khris Middleton (1), Robert Covington (2), Luol Deng (2), Jamaal Tinsley (2), Jusuf Nurkic (2), Fred VanVleet (2), Victor Oladipo (2), JR Smith (2), Derek Fisher (2), Caron Butler (2), Stephen Jackson (2), Brandon Jennings (2), George Hill (2), Dejounte Murray (2), Kyle Korver (2), P.J. Tucker (2), Thabo Sefolosha (2), Al Harrington (2), Antoine Walker (2), Larry Hughes (2), Joe Ingles (2), Anderson Varejao (2), Derrick White (2), Mario Chalmers (2), Jalen Williams (2), Eric Snow (2), Evan Turner (2), Kyle Anderson (2), Al-Farouq Aminu (2), Patrick Beverley (2), OG Anunoby (2), Michael Finley (2), John Salmons (2), Kelly Oubre Jr. (2), Josh Howard (2), T.J. Warren (2), James Posey (2), Latrell Sprewell (2), Alex Caruso (2), Chuck Hayes (2), Gary Trent Jr. (2), Amen Thompson (2), Justin Holiday (2), Reggie Miller (2), Josh Richardson (3), Donte DiVincenzo (3), Dorian Finney-Smith (3), Tyrus Thomas (3), Austin Rivers (3), Andrew Nembhard (3), Bonzi Wells (3), Doug Christie (3), Clifford Robinson (3), Bruce Brown (3), Glen Davis (3), Duncan Robinson (3), Trenton Hassell (3), Anthony Black (3), Toni Kukoc (3), Damien Wilkins (3), Pablo Prigioni (3), Ausar Thompson (3), Aaron McKie (3), Jim Jackson (3), Andre Roberson (3), Jamal Shead (3), Jevon Carter (3), Tari Eason (3), Javonte Green (3), Tony Delk (3), Dylan Harper (3), Brad Wanamaker (4)

</details>

**Since 2001-02 (through 2025-26), name a player who stole the ball 6 or more times in a playoff game.**

37 valid answers, difficulty **medium**, tiers: 1: 24, 2: 6, 3: 7 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Russell Westbrook (1), Kevin Garnett (1), Ben Wallace (1), Stephen Curry (1), Rajon Rondo (1), Jason Kidd (1), Dwyane Wade (1), Shawn Marion (1), Kevin Love (1), Jayson Tatum (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Donovan Mitchell (1), Baron Davis (1), Jamal Crawford (1), Kawhi Leonard (1), Jimmy Butler III (1), Manu Ginobili (1), Thaddeus Young (1), Zaza Pachulia (1), Jarrett Allen (1), Fred VanVleet (2), Derek Fisher (2), Kyle Korver (2), Thabo Sefolosha (2), Kyle Anderson (2), John Salmons (2), Josh Richardson (3), Andrew Nembhard (3), Doug Christie (3), Glen Davis (3), Toni Kukoc (3), Javonte Green (3), Dylan Harper (3)

</details>

### `offensive-rebounds`

**Since 2001-02 (through 2025-26), name a player who grabbed 12 or more offensive rebounds in a game.**

52 valid answers, difficulty **easy**, tiers: 1: 24, 2: 19, 3: 8, 6: 1 (1 at tier 4 or above).

<details><summary>All valid answers</summary>

Tim Duncan (1), Ben Wallace (1), Andre Drummond (1), Rudy Gobert (1), Carmelo Anthony (1), DeAndre Jordan (1), Tyson Chandler (1), Zach Randolph (1), Kevin Love (1), Jonas Valanciunas (1), Elton Brand (1), Clint Capela (1), Al Jefferson (1), Shaquille O'Neal (1), Lamar Odom (1), DeMarcus Cousins (1), Domantas Sabonis (1), Tristan Thompson (1), Steven Adams (1), Joakim Noah (1), Zaza Pachulia (1), JaVale McGee (1), Enes Freedom (1), Reggie Evans (1), Zydrunas Ilgauskas (2), Emeka Okafor (2), Jusuf Nurkic (2), Ivica Zubac (2), Erick Dampier (2), Amir Johnson (2), Aaron Gordon (2), Jeff Foster (2), Anderson Varejao (2), Ersan Ilyasova (2), Kevon Looney (2), Kenneth Faried (2), Mitchell Robinson (2), Kenny Thomas (2), JJ Hickson (2), Jalen Duren (2), Chuck Hayes (2), Andray Blatche (2), Isaiah Hartenstein (2), Mark Williams (3), Vlade Divac (3), Greg Ostertag (3), Walker Kessler (3), Donovan Clingan (3), Tari Eason (3), Thomas Robinson (3), Yi Jianlian (3), Alex Stepheson (6)

</details>

**Since 2001-02 (through 2025-26), name a player who grabbed 10 or more offensive rebounds in a game.**

137 valid answers, difficulty **easy**, tiers: 1: 51, 2: 47, 3: 22, 4: 13, 5: 2, 6: 2 (17 at tier 4 or above).

<details><summary>All valid answers</summary>

Dwight Howard (1), Tim Duncan (1), Pau Gasol (1), Kevin Garnett (1), Ben Wallace (1), Anthony Davis (1), Andre Drummond (1), Brook Lopez (1), Rudy Gobert (1), Carmelo Anthony (1), DeAndre Jordan (1), Tyson Chandler (1), Nikola Vucevic (1), Zach Randolph (1), Kevin Love (1), Nikola Jokic (1), Draymond Green (1), LaMarcus Aldridge (1), Jonas Valanciunas (1), Paul Millsap (1), Elton Brand (1), Carlos Boozer (1), Marcus Camby (1), Karl-Anthony Towns (1), Chris Bosh (1), Marc Gasol (1), Clint Capela (1), Al Jefferson (1), Shaquille O'Neal (1), Lamar Odom (1), DeMarcus Cousins (1), Thaddeus Young (1), Domantas Sabonis (1), Amar'e Stoudemire (1), Tristan Thompson (1), Antawn Jamison (1), Samuel Dalembert (1), Jermaine O'Neal (1), Steven Adams (1), Joakim Noah (1), Zaza Pachulia (1), Andrew Bogut (1), Bam Adebayo (1), JaVale McGee (1), Tony Allen (1), Mason Plumlee (1), Enes Freedom (1), Taj Gibson (1), Jarrett Allen (1), Reggie Evans (1), Drew Gooden (1), Zydrunas Ilgauskas (2), Emeka Okafor (2), Derrick Favors (2), Jusuf Nurkic (2), Brendan Haywood (2), Hassan Whiteside (2), Roy Hibbert (2), Kurt Thomas (2), Caron Butler (2), Ivica Zubac (2), Erick Dampier (2), Greg Monroe (2), Chris Andersen (2), Kendrick Perkins (2), Deandre Ayton (2), Amir Johnson (2), Aaron Gordon (2), Keldon Johnson (2), Jeff Foster (2), Anderson Varejao (2), Ersan Ilyasova (2), John Collins (2), Robin Lopez (2), Mehmet Okur (2), Ed Davis (2), Nazr Mohammed (2), Jakob Poeltl (2), Antonio McDyess (2), Kevon Looney (2), Kenneth Faried (2), Jason Thompson (2), Mitchell Robinson (2), Rasho Nesterovic (2), Brandon Bass (2), Andris Biedrins (2), Kenny Thomas (2), Joel Przybilla (2), JJ Hickson (2), Larry Nance Jr. (2), Ryan Anderson (2), Gorgui Dieng (2), Jalen Duren (2), Adonal Foyle (2), Chuck Hayes (2), Andray Blatche (2), Isaiah Hartenstein (2), Luc Mbah a Moute (2), Nikola Pekovic (3), Trevor Booker (3), Bonzi Wells (3), Onyeka Okongwu (3), Antonio Davis (3), Alonzo Mourning (3), Robert Williams III (3), Mark Williams (3), Precious Achiuwa (3), Dale Davis (3), Marvin Bagley III (3), DeJuan Blair (3), Vlade Divac (3), Greg Ostertag (3), Lavoy Allen (3), Walker Kessler (3), Mikki Moore (3), Donovan Clingan (3), Tari Eason (3), Thomas Robinson (3), Yi Jianlian (3), Day'Ron Sharpe (3), Khem Birch (4), Michael Ruffin (4), Scott Padgett (4), Moussa Diabate (4), Neemias Queta (4), Yves Missi (4), Jahidi White (4), Moses Brown (4), Greg Oden (4), Loren Woods (4), Dominick Barlow (4), Joey Dorsey (4), Zendon Hamilton (4), Moussa Cisse (5), Julian Reese (5), Adama Sanogo (6), Alex Stepheson (6)

</details>

**Since 2001-02 (through 2025-26), name a player who grabbed 9 or more offensive rebounds in a game.**

236 valid answers, difficulty **easy**, tiers: 1: 67, 2: 74, 3: 52, 4: 35, 5: 6, 6: 2 (43 at tier 4 or above).

<details><summary>All valid answers</summary>

Dwight Howard (1), Tim Duncan (1), Pau Gasol (1), Joel Embiid (1), Kevin Garnett (1), Ben Wallace (1), Anthony Davis (1), Andre Drummond (1), Brook Lopez (1), Rudy Gobert (1), Carmelo Anthony (1), Tracy McGrady (1), Josh Smith (1), DeAndre Jordan (1), Tyson Chandler (1), Nikola Vucevic (1), Zach Randolph (1), Shawn Marion (1), Al Horford (1), Giannis Antetokounmpo (1), Kevin Love (1), Nikola Jokic (1), Draymond Green (1), LaMarcus Aldridge (1), Jonas Valanciunas (1), Paul Millsap (1), Serge Ibaka (1), Elton Brand (1), Carlos Boozer (1), Marcus Camby (1), Karl-Anthony Towns (1), Chris Bosh (1), Marc Gasol (1), Clint Capela (1), Ray Allen (1), Al Jefferson (1), Shaquille O'Neal (1), Lamar Odom (1), DeMarcus Cousins (1), David Lee (1), Thaddeus Young (1), Julius Randle (1), David West (1), Domantas Sabonis (1), Amar'e Stoudemire (1), Tristan Thompson (1), Antawn Jamison (1), Samuel Dalembert (1), Jermaine O'Neal (1), Marcin Gortat (1), Steven Adams (1), Nene (1), Yao Ming (1), Joakim Noah (1), Zaza Pachulia (1), Blake Griffin (1), Victor Wembanyama (1), Andrew Bogut (1), Bam Adebayo (1), JaVale McGee (1), Tony Allen (1), Mason Plumlee (1), Enes Freedom (1), Taj Gibson (1), Jarrett Allen (1), Reggie Evans (1), Drew Gooden (1), Zydrunas Ilgauskas (2), Emeka Okafor (2), Rashard Lewis (2), Derrick Favors (2), Jusuf Nurkic (2), Marvin Williams (2), Kristaps Porzingis (2), Brendan Haywood (2), Hassan Whiteside (2), Roy Hibbert (2), Kurt Thomas (2), Troy Murphy (2), Chris Kaman (2), Caron Butler (2), Ivica Zubac (2), Erick Dampier (2), Greg Monroe (2), Bismack Biyombo (2), Chris Andersen (2), Kendrick Perkins (2), Deandre Ayton (2), Amir Johnson (2), Al Harrington (2), Luis Scola (2), Aaron Gordon (2), Keldon Johnson (2), Jeff Foster (2), Anderson Varejao (2), Ersan Ilyasova (2), John Collins (2), Robin Lopez (2), Mehmet Okur (2), Ed Davis (2), Matt Barnes (2), Nazr Mohammed (2), Jakob Poeltl (2), Antonio McDyess (2), Kris Humphries (2), Jamaal Magloire (2), P.J. Brown (2), Kevon Looney (2), Markieff Morris (2), Kenneth Faried (2), Wendell Carter Jr. (2), Jason Thompson (2), Mitchell Robinson (2), Juwan Howard (2), Andrew Bynum (2), Rasho Nesterovic (2), Brandon Bass (2), Andris Biedrins (2), Kenny Thomas (2), Scottie Barnes (2), Alex Len (2), Joel Przybilla (2), JJ Hickson (2), Larry Nance Jr. (2), Joe Smith (2), Ryan Anderson (2), Omer Asik (2), Gorgui Dieng (2), Kosta Koufos (2), Jalen Duren (2), Donyell Marshall (2), Adonal Foyle (2), Chuck Hayes (2), Andray Blatche (2), Isaiah Hartenstein (2), JaMychal Green (2), Amen Thompson (2), Nic Claxton (2), Jason Collins (2), DeSagana Diop (2), Luc Mbah a Moute (2), Nikola Pekovic (3), Trevor Booker (3), Bonzi Wells (3), Onyeka Okongwu (3), Dario Saric (3), Lorenzen Wright (3), Jason Maxiell (3), Richaun Holmes (3), Glen Davis (3), Aron Baynes (3), Antonio Davis (3), Alonzo Mourning (3), Robert Williams III (3), Malik Rose (3), Isaiah Stewart (3), Jordan Hill (3), Timofey Mozgov (3), Mark Williams (3), Precious Achiuwa (3), Dale Davis (3), Dan Gadzuric (3), Marvin Bagley III (3), DeJuan Blair (3), Vlade Divac (3), Chris Boucher (3), Jared Sullinger (3), Darrell Arthur (3), Etan Thomas (3), Willy Hernangomez (3), Greg Ostertag (3), Tyler Hansbrough (3), Goga Bitadze (3), Lavoy Allen (3), Josh Childress (3), Walker Kessler (3), Luke Kornet (3), Mikki Moore (3), Drew Eubanks (3), Jerome Williams (3), Noah Vonleh (3), Primoz Brezec (3), Brandon Clarke (3), Nick Richards (3), Danny Fortson (3), Lou Amundson (3), Shelden Williams (3), Donovan Clingan (3), Terrence Jones (3), Tari Eason (3), Thomas Robinson (3), Yi Jianlian (3), Day'Ron Sharpe (3), Isaiah Jackson (4), Boban Marjanovic (4), Khem Birch (4), Josh Boone (4), Cole Aldrich (4), Byron Mullens (4), Michael Ruffin (4), Scott Padgett (4), Moussa Diabate (4), Alan Henderson (4), Neemias Queta (4), Ira Newble (4), Samaki Walker (4), Tarik Black (4), Yves Missi (4), Zach Edey (4), Trayce Jackson-Davis (4), Jahidi White (4), Slava Medvedenko (4), Moses Brown (4), Shawn Kemp (4), Greg Oden (4), Collin Murray-Boyles (4), Loren Woods (4), Dominick Barlow (4), Henry Sims (4), Luka Garza (4), Michael Bradley (4), Scott Williams (4), KJ McDaniels (4), Mouhamed Gueye (4), Ryan Kalkbrenner (4), Joey Dorsey (4), Zendon Hamilton (4), Dylan Cardwell (4), Oscar Tshiebwe (5), Curtis Borchardt (5), Moussa Cisse (5), Andre Brown (5), Colin Castleton (5), Julian Reese (5), Adama Sanogo (6), Alex Stepheson (6)

</details>

### `free-throws`

**Since 2001-02 (through 2025-26), name a player who made 18 or more free throws in a game.**

65 valid answers, difficulty **easy**, tiers: 1: 52, 2: 12, 3: 1 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Chris Paul (1), Russell Westbrook (1), Luka Doncic (1), Joel Embiid (1), Dirk Nowitzki (1), Allen Iverson (1), Stephen Curry (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Damian Lillard (1), Carmelo Anthony (1), Tracy McGrady (1), DeMar DeRozan (1), Dwyane Wade (1), Paul Pierce (1), Bradley Beal (1), Deron Williams (1), Giannis Antetokounmpo (1), Kevin Love (1), Nikola Jokic (1), Trae Young (1), John Wall (1), Gilbert Arenas (1), Vince Carter (1), Anthony Edwards (1), Chauncey Billups (1), Jaylen Brown (1), Donovan Mitchell (1), Chris Bosh (1), Kawhi Leonard (1), Devin Booker (1), Jimmy Butler III (1), Ja Morant (1), Manu Ginobili (1), DeMarcus Cousins (1), Michael Redd (1), Amar'e Stoudemire (1), Cade Cunningham (1), Derrick Rose (1), Jermaine O'Neal (1), Devin Harris (1), Yao Ming (1), Richard Hamilton (1), Kevin Martin (1), Bam Adebayo (1), Deni Avdija (1), Franz Wagner (1), Austin Reaves (2), Marvin Williams (2), Brandon Roy (2), Allan Houston (2), Cam Thomas (2), Jerami Grant (2), Corey Maggette (2), Ramon Sessions (2), Danilo Gallinari (2), Steve Francis (2), Ben Gordon (2), Mike James (2002-2014) (2), Travis Outlaw (3)

</details>

**Since 2001-02 (through 2025-26), name a player who made 20 or more free throws in a game.**

34 valid answers, difficulty **medium**, tiers: 1: 32, 2: 2 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Russell Westbrook (1), Joel Embiid (1), Dirk Nowitzki (1), Allen Iverson (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), DeMar DeRozan (1), Dwyane Wade (1), Paul Pierce (1), Deron Williams (1), Giannis Antetokounmpo (1), Nikola Jokic (1), Trae Young (1), Gilbert Arenas (1), Vince Carter (1), Donovan Mitchell (1), Chris Bosh (1), Devin Booker (1), Jimmy Butler III (1), Ja Morant (1), DeMarcus Cousins (1), Amar'e Stoudemire (1), Cade Cunningham (1), Devin Harris (1), Richard Hamilton (1), Kevin Martin (1), Bam Adebayo (1), Austin Reaves (2), Jerami Grant (2)

</details>

**Since 2001-02 (through 2025-26), name a player who made 22 or more free throws in a game.**

21 valid answers, difficulty **medium**, tiers: 1: 21 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Joel Embiid (1), Dirk Nowitzki (1), Allen Iverson (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), DeMar DeRozan (1), Dwyane Wade (1), Giannis Antetokounmpo (1), Nikola Jokic (1), Gilbert Arenas (1), Vince Carter (1), Chris Bosh (1), Devin Booker (1), Jimmy Butler III (1), Kevin Martin (1), Bam Adebayo (1)

</details>

### `turnovers`

**Since 2001-02 (through 2025-26), name a player who committed 11 or more turnovers in a game.**

27 valid answers, difficulty **medium**, tiers: 1: 23, 2: 2, 3: 2 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Russell Westbrook (1), Luka Doncic (1), Allen Iverson (1), Stephen Curry (1), Jason Kidd (1), Dwyane Wade (1), Paul Pierce (1), Giannis Antetokounmpo (1), Trae Young (1), John Wall (1), Gilbert Arenas (1), Karl-Anthony Towns (1), Domantas Sabonis (1), Amar'e Stoudemire (1), Mike Bibby (1), Monta Ellis (1), Derrick Rose (1), Richard Jefferson (1), Zydrunas Ilgauskas (2), Ben Simmons (2), Stephon Castle (3), Emmanuel Mudiay (3)

</details>

**Since 2001-02 (through 2025-26), name a player who committed 9 or more turnovers in a game.**

128 valid answers, difficulty **easy**, tiers: 1: 86, 2: 29, 3: 11, 4: 1, 5: 1 (2 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Pau Gasol (1), Joel Embiid (1), Steve Nash (1), Allen Iverson (1), Stephen Curry (1), Andre Drummond (1), Rajon Rondo (1), Damian Lillard (1), Jason Kidd (1), Carmelo Anthony (1), Josh Smith (1), DeAndre Jordan (1), Kyle Lowry (1), Dwyane Wade (1), Andre Miller (1), Paul Pierce (1), Bradley Beal (1), Deron Williams (1), Giannis Antetokounmpo (1), Jrue Holiday (1), Nikola Jokic (1), Jayson Tatum (1), Andre Iguodala (1), Trae Young (1), Joe Johnson (1), Draymond Green (1), John Wall (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Paul Millsap (1), Carlos Boozer (1), Kyrie Irving (1), Karl-Anthony Towns (1), Donovan Mitchell (1), Baron Davis (1), Kawhi Leonard (1), Raymond Felton (1), Devin Booker (1), Shaquille O'Neal (1), Ja Morant (1), Zach LaVine (1), Dennis Schroder (1), Zion Williamson (1), DeMarcus Cousins (1), Julius Randle (1), De'Aaron Fox (1), Domantas Sabonis (1), Kirk Hinrich (1), Amar'e Stoudemire (1), Cade Cunningham (1), Mike Bibby (1), Paolo Banchero (1), Kemba Walker (1), Mo Williams (1), Monta Ellis (1), Derrick Rose (1), Jermaine O'Neal (1), Jamal Murray (1), LaMelo Ball (1), Nicolas Batum (1), Richard Jefferson (1), Yao Ming (1), Joakim Noah (1), Blake Griffin (1), Victor Wembanyama (1), Andrew Bogut (1), Brandon Ingram (1), Chris Webber (1), D'Angelo Russell (1), Collin Sexton (1), Stephon Marbury (1), Eric Bledsoe (1), Darren Collison (1), Deni Avdija (1), Jason Richardson (1), Khris Middleton (1), Michael Jordan (1), Zydrunas Ilgauskas (2), Steve Blake (2), Robert Covington (2), Jamaal Tinsley (2), Victor Oladipo (2), Caron Butler (2), Stephen Jackson (2), Ben Simmons (2), Al Harrington (2), Antoine Walker (2), Jalen Rose (2), Steve Francis (2), Derrick White (2), Jerry Stackhouse (2), Ben Gordon (2), Evan Turner (2), Shaedon Sharpe (2), Ricky Davis (2), Coby White (2), Randy Foye (2), Jeremy Lin (2), JJ Hickson (2), Aaron Brooks (2), Eddy Curry (2), Kevin Porter Jr. (2), Jeff McInnis (2), O.J. Mayo (2), Michael Carter-Williams (2), P.J. Washington (2), Bonzi Wells (3), Al Thornton (3), Stephon Castle (3), Jaden Ivey (3), Dennis Smith Jr. (3), Emmanuel Mudiay (3), Scoot Henderson (3), Darius Bazley (3), Anfernee Hardaway (3), Josh Jackson (3), Danny Fortson (3), Isaiah Roby (4), Jahmai Mashack (5)

</details>

**Since 2001-02 (through 2025-26), name a player who committed 8 or more turnovers in a game.**

247 valid answers, difficulty **easy**, tiers: 1: 131, 2: 80, 3: 30, 4: 4, 5: 2 (6 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Chris Paul (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Pau Gasol (1), Joel Embiid (1), Dirk Nowitzki (1), Kevin Garnett (1), Steve Nash (1), Allen Iverson (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Andre Drummond (1), Rajon Rondo (1), Damian Lillard (1), Jason Kidd (1), Carmelo Anthony (1), Tony Parker (1), Tracy McGrady (1), Josh Smith (1), DeAndre Jordan (1), DeMar DeRozan (1), Kyle Lowry (1), Dwyane Wade (1), Tyson Chandler (1), Nikola Vucevic (1), Andre Miller (1), Paul Pierce (1), Bradley Beal (1), Deron Williams (1), Giannis Antetokounmpo (1), Jrue Holiday (1), Nikola Jokic (1), Jayson Tatum (1), Andre Iguodala (1), Trae Young (1), Joe Johnson (1), Draymond Green (1), LaMarcus Aldridge (1), Jonas Valanciunas (1), John Wall (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Paul Millsap (1), Anthony Edwards (1), Chauncey Billups (1), Elton Brand (1), Jaylen Brown (1), Carlos Boozer (1), Kyrie Irving (1), Karl-Anthony Towns (1), Donovan Mitchell (1), Baron Davis (1), Jose Calderon (1), Chris Bosh (1), Ricky Rubio (1), Kawhi Leonard (1), Marc Gasol (1), Raymond Felton (1), Devin Booker (1), Jason Terry (1), Al Jefferson (1), Shaquille O'Neal (1), Lamar Odom (1), Ja Morant (1), Zach LaVine (1), Manu Ginobili (1), Dennis Schroder (1), Zion Williamson (1), DeMarcus Cousins (1), CJ McCollum (1), Julius Randle (1), De'Aaron Fox (1), David West (1), Rudy Gay (1), Domantas Sabonis (1), Kirk Hinrich (1), Amar'e Stoudemire (1), Cade Cunningham (1), Mike Bibby (1), Antawn Jamison (1), Samuel Dalembert (1), Paolo Banchero (1), Kemba Walker (1), Mo Williams (1), Monta Ellis (1), Derrick Rose (1), Jermaine O'Neal (1), Jamal Murray (1), Boris Diaw (1), Gerald Wallace (1), LaMelo Ball (1), Lou Williams (1), Nicolas Batum (1), Richard Jefferson (1), Nene (1), Devin Harris (1), Yao Ming (1), Jarrett Jack (1), Joakim Noah (1), Zaza Pachulia (1), Richard Hamilton (1), Blake Griffin (1), Victor Wembanyama (1), Kenyon Martin (1), Andrew Bogut (1), Brandon Ingram (1), Bam Adebayo (1), D.J. Augustin (1), Reggie Jackson (1), Chris Webber (1), D'Angelo Russell (1), Collin Sexton (1), Luke Ridnour (1), Stephon Marbury (1), Eric Bledsoe (1), Mason Plumlee (1), Darren Collison (1), Deni Avdija (1), Jason Richardson (1), Marcus Smart (1), Khris Middleton (1), Tyler Herro (1), Michael Jordan (1), Karl Malone (1), Zydrunas Ilgauskas (2), Steve Blake (2), Eric Gordon (2), Desmond Bane (2), Robert Covington (2), Keyonte George (2), Luol Deng (2), Jamaal Tinsley (2), Jusuf Nurkic (2), Ty Lawson (2), Austin Reaves (2), Jason Williams (2), Fred VanVleet (2), Victor Oladipo (2), Caron Butler (2), Erick Dampier (2), Rafer Alston (2), Stephen Jackson (2), Brandon Jennings (2), George Hill (2), Dejounte Murray (2), Gordon Hayward (2), Hedo Turkoglu (2), Elfrid Payton (2), Gary Payton (2), Ben Simmons (2), Al Harrington (2), Kyle Kuzma (2), Luis Scola (2), Darius Garland (2), Antoine Walker (2), Aaron Gordon (2), Jalen Rose (2), Tyreke Evans (2), Larry Hughes (2), Joe Ingles (2), Brevin Knight (2), Steve Francis (2), Derrick White (2), Jerry Stackhouse (2), Ben Gordon (2), Shareef Abdur-Rahim (2), Evan Turner (2), Kyle Anderson (2), Mike Miller (2), Alperen Sengun (2), T.J. Ford (2), Terry Rozier (2), Mike Dunleavy (2), Rodney Stuckey (2), Jamaal Magloire (2), Shaedon Sharpe (2), Glenn Robinson (2), Ricky Davis (2), Jordan Poole (2), Coby White (2), Josh Giddey (2), Randy Foye (2), Andrew Bynum (2), Jeremy Lin (2), Scottie Barnes (2), JJ Hickson (2), Grant Hill (2), Brandon Knight (2), Aaron Brooks (2), Greivis Vasquez (2), Eddy Curry (2), Kris Dunn (2), Kevin Porter Jr. (2), Jeff McInnis (2), Andray Blatche (2), Carlos Arroyo (2), Eddie Jones (2), O.J. Mayo (2), Lance Stephenson (2), Amen Thompson (2), Michael Carter-Williams (2), P.J. Washington (2), Darrel Armstrong (2), John Stockton (2), Jahlil Okafor (3), Andrew Nembhard (3), Bonzi Wells (3), Al Thornton (3), Stephon Castle (3), Clifford Robinson (3), Jaden Ivey (3), Matas Buzelis (3), Dennis Smith Jr. (3), Mark Blount (3), Troy Hudson (3), Naji Marshall (3), Killian Hayes (3), Rashad McCants (3), Emmanuel Mudiay (3), Scoot Henderson (3), Darius Bazley (3), Josh McRoberts (3), Jonny Flynn (3), Damien Wilkins (3), Anfernee Hardaway (3), Josh Jackson (3), Tony Wroten (3), Smush Parker (3), Danny Fortson (3), Bub Carrington (3), Roger Mason Jr. (3), Rodney Rogers (3), Erick Strickland (3), Jarace Walker (3), Tre Mann (4), Isaiah Roby (4), Jared Butler (4), George McCloud (4), Jahmai Mashack (5), Nikola Topic (5)

</details>

### `shots-taken`

**Since 2001-02 (through 2025-26), name a player who took 35 or more shots from the field in a game.**

54 valid answers, difficulty **easy**, tiers: 1: 51, 2: 2, 3: 1 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Russell Westbrook (1), Luka Doncic (1), Joel Embiid (1), Allen Iverson (1), Stephen Curry (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Damian Lillard (1), Jason Kidd (1), Carmelo Anthony (1), Tony Parker (1), Tracy McGrady (1), DeMar DeRozan (1), Dwyane Wade (1), Paul Pierce (1), Zach Randolph (1), Bradley Beal (1), Giannis Antetokounmpo (1), Jrue Holiday (1), Nikola Jokic (1), Jayson Tatum (1), Gilbert Arenas (1), Vince Carter (1), Anthony Edwards (1), Jalen Brunson (1), Jaylen Brown (1), Kyrie Irving (1), Karl-Anthony Towns (1), Tyrese Maxey (1), Klay Thompson (1), Donovan Mitchell (1), Kawhi Leonard (1), Devin Booker (1), Zach LaVine (1), CJ McCollum (1), De'Aaron Fox (1), Rudy Gay (1), Cade Cunningham (1), Monta Ellis (1), Jamal Murray (1), LaMelo Ball (1), Yao Ming (1), Richard Hamilton (1), Blake Griffin (1), Bam Adebayo (1), D'Angelo Russell (1), Michael Jordan (1), Dejounte Murray (2), Latrell Sprewell (2), GG Jackson (3)

</details>

**Since 2001-02 (through 2025-26), name a player who took 38 or more shots from the field in a game.**

26 valid answers, difficulty **medium**, tiers: 1: 25, 2: 1 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kobe Bryant (1), Russell Westbrook (1), Joel Embiid (1), Allen Iverson (1), Stephen Curry (1), Damian Lillard (1), DeMar DeRozan (1), Dwyane Wade (1), Zach Randolph (1), Bradley Beal (1), Giannis Antetokounmpo (1), Nikola Jokic (1), Jalen Brunson (1), Tyrese Maxey (1), Klay Thompson (1), Kawhi Leonard (1), Devin Booker (1), CJ McCollum (1), Cade Cunningham (1), Monta Ellis (1), LaMelo Ball (1), Bam Adebayo (1), Michael Jordan (1), Dejounte Murray (2)

</details>

### `minutes`

**Since 2001-02 (through 2025-26), name a player who played 55 or more minutes in a game.**

84 valid answers, difficulty **easy**, tiers: 1: 53, 2: 26, 3: 5 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), Kevin Durant (1), Pau Gasol (1), Dirk Nowitzki (1), Steve Nash (1), Allen Iverson (1), Ben Wallace (1), Stephen Curry (1), Rajon Rondo (1), Damian Lillard (1), Jason Kidd (1), Carmelo Anthony (1), Tracy McGrady (1), DeMar DeRozan (1), Zach Randolph (1), Shawn Marion (1), Bradley Beal (1), Deron Williams (1), Nikola Jokic (1), Trae Young (1), Joe Johnson (1), Vince Carter (1), Chauncey Billups (1), Elton Brand (1), Klay Thompson (1), Jamal Crawford (1), Chris Bosh (1), Marc Gasol (1), Raymond Felton (1), Devin Booker (1), Jason Terry (1), Ray Allen (1), Jimmy Butler III (1), Lamar Odom (1), Zach LaVine (1), CJ McCollum (1), Trevor Ariza (1), Kirk Hinrich (1), Antawn Jamison (1), Derrick Rose (1), Jamal Murray (1), Rasheed Wallace (1), Gerald Wallace (1), Richard Jefferson (1), Devin Harris (1), Richard Hamilton (1), Kenyon Martin (1), Kevin Martin (1), Peja Stojakovic (1), Stephon Marbury (1), Pascal Siakam (1), Enes Freedom (1), Khris Middleton (1), Luol Deng (2), Jamaal Tinsley (2), Ty Lawson (2), Victor Oladipo (2), Caron Butler (2), Gordon Hayward (2), Thabo Sefolosha (2), Tayshaun Prince (2), Sam Cassell (2), Beno Udrih (2), Jalen Rose (2), Cuttino Mobley (2), Steve Francis (2), Chris Duhon (2), Shareef Abdur-Rahim (2), OG Anunoby (2), Marcus Morris Sr. (2), Ricky Davis (2), Channing Frye (2), Michael Finley (2), John Salmons (2), Scottie Barnes (2), Aaron Brooks (2), Ryan Anderson (2), Quentin Richardson (2), Gary Trent Jr. (2), Immanuel Quickley (3), Otto Porter Jr. (3), Raja Bell (3), David Wesley (3), Kerry Kittles (3)

</details>

**Since 2001-02 (through 2025-26), name a player who played 58 or more minutes in a game.**

19 valid answers, difficulty **medium**, tiers: 1: 14, 2: 4, 3: 1 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Dirk Nowitzki (1), Stephen Curry (1), Rajon Rondo (1), Damian Lillard (1), DeMar DeRozan (1), Shawn Marion (1), Deron Williams (1), Nikola Jokic (1), Jamal Crawford (1), Ray Allen (1), Jimmy Butler III (1), CJ McCollum (1), Kirk Hinrich (1), Derrick Rose (1), Cuttino Mobley (2), Steve Francis (2), John Salmons (2), Aaron Brooks (2), Raja Bell (3)

</details>

### `perfect-shooting`

**Since 2001-02 (through 2025-26), name a player who made 11 or more field goals in a game without a miss.**

22 valid answers, difficulty **medium**, tiers: 1: 11, 2: 4, 3: 5, 4: 2 (2 at tier 4 or above).

<details><summary>All valid answers</summary>

Dwight Howard (1), Chris Paul (1), Nikola Jokic (1), Serge Ibaka (1), Domantas Sabonis (1), Steven Adams (1), Nene (1), Yao Ming (1), Tony Allen (1), Enes Freedom (1), Jarrett Allen (1), Ivica Zubac (2), Kenneth Faried (2), Mitchell Robinson (2), Daniel Gafford (2), Jonathan Kuminga (3), Richaun Holmes (3), Nenad Krstic (3), Thomas Bryant (3), Paul Reed (3), Fabricio Oberto (4), Keita Bates-Diop (4)

</details>

**Since 2001-02 (through 2025-26), name a player who made 9 or more field goals in a game without a miss.**

91 valid answers, difficulty **medium**, tiers: 1: 34, 2: 23, 3: 23, 4: 10, 5: 1 (11 at tier 4 or above).

<details><summary>All valid answers</summary>

Dwight Howard (1), Chris Paul (1), Pau Gasol (1), Andre Drummond (1), Rudy Gobert (1), Tyson Chandler (1), Giannis Antetokounmpo (1), Nikola Jokic (1), Draymond Green (1), Jonas Valanciunas (1), Serge Ibaka (1), Chris Bosh (1), Clint Capela (1), Shaquille O'Neal (1), Myles Turner (1), Jameer Nelson (1), Julius Randle (1), Domantas Sabonis (1), Amar'e Stoudemire (1), Mo Williams (1), Marcin Gortat (1), Steven Adams (1), Boris Diaw (1), Nene (1), Yao Ming (1), Jarrett Jack (1), Kenyon Martin (1), JaVale McGee (1), Tony Allen (1), Mason Plumlee (1), Darren Collison (1), Enes Freedom (1), Jarrett Allen (1), Michael Porter Jr. (1), Zydrunas Ilgauskas (2), Derrick Favors (2), Ivica Zubac (2), Gordon Hayward (2), Ish Smith (2), Deandre Ayton (2), Amir Johnson (2), Anderson Varejao (2), Ersan Ilyasova (2), Kenneth Faried (2), Mitchell Robinson (2), Alex Len (2), JJ Hickson (2), Jalen Duren (2), Eddy Curry (2), Dwight Powell (2), Montrezl Harrell (2), Carlos Arroyo (2), Tony Battie (2), JaMychal Green (2), Daniel Gafford (2), Jared Dudley (2), Dikembe Mutombo (2), Desmond Mason (3), Jaden McDaniels (3), Chet Holmgren (3), Dante Cunningham (3), Matas Buzelis (3), Jonathan Kuminga (3), Jonas Jerebko (3), Richaun Holmes (3), Robert Williams III (3), Bobby Jackson (3), Nenad Krstic (3), Mark Williams (3), Brandan Wright (3), Thomas Bryant (3), Goga Bitadze (3), Walker Kessler (3), Mikki Moore (3), Paul Reed (3), Jaxson Hayes (3), Brandon Clarke (3), Nick Richards (3), Tony Snell (3), Jarron Collins (3), Keon Clark (4), Fabricio Oberto (4), Josh Boone (4), Lance Thomas (4), Keita Bates-Diop (4), Chimezie Metu (4), Andrew Nicholson (4), Dereck Lively II (4), Trayce Jackson-Davis (4), Derrick Brown (4), Kai Jones (5)

</details>

**Since 2001-02 (through 2025-26), name a player who made 8 or more field goals in a game without a miss.**

176 valid answers, difficulty **easy**, tiers: 1: 56, 2: 50, 3: 45, 4: 24, 5: 1 (25 at tier 4 or above).

<details><summary>All valid answers</summary>

Dwight Howard (1), Chris Paul (1), Tim Duncan (1), Pau Gasol (1), Joel Embiid (1), Steve Nash (1), Andre Drummond (1), Rudy Gobert (1), Tony Parker (1), DeAndre Jordan (1), Tyson Chandler (1), Mike Conley (1), Al Horford (1), Giannis Antetokounmpo (1), Nikola Jokic (1), Draymond Green (1), Jonas Valanciunas (1), Vince Carter (1), Serge Ibaka (1), Karl-Anthony Towns (1), Jamal Crawford (1), Jose Calderon (1), Chris Bosh (1), Marc Gasol (1), Clint Capela (1), Shaquille O'Neal (1), Myles Turner (1), David Lee (1), Jameer Nelson (1), Julius Randle (1), Domantas Sabonis (1), Amar'e Stoudemire (1), Samuel Dalembert (1), Mo Williams (1), Marcin Gortat (1), Steven Adams (1), Boris Diaw (1), T.J. McConnell (1), Richard Jefferson (1), Nene (1), Devin Harris (1), Yao Ming (1), Jarrett Jack (1), Kenyon Martin (1), Bam Adebayo (1), Luke Ridnour (1), JaVale McGee (1), Jeff Green (1), Tony Allen (1), Mason Plumlee (1), Darren Collison (1), Enes Freedom (1), Taj Gibson (1), Jarrett Allen (1), Michael Porter Jr. (1), Drew Gooden (1), Zydrunas Ilgauskas (2), Derrick Favors (2), J.J. Barea (2), Hassan Whiteside (2), Troy Murphy (2), Tyus Jones (2), Kentavious Caldwell-Pope (2), Ivica Zubac (2), Gordon Hayward (2), Kyle Korver (2), Ish Smith (2), Kendrick Perkins (2), Tayshaun Prince (2), Deandre Ayton (2), Amir Johnson (2), Ben Simmons (2), Anderson Varejao (2), Ersan Ilyasova (2), Bojan Bogdanovic (2), Mehmet Okur (2), Trey Murphy III (2), Ed Davis (2), Jakob Poeltl (2), Kris Humphries (2), Michael Finley (2), Kenneth Faried (2), Mitchell Robinson (2), Andrew Bynum (2), Andris Biedrins (2), Alex Len (2), T.J. Warren (2), JJ Hickson (2), Kosta Koufos (2), Jalen Duren (2), Eddy Curry (2), Nate Robinson (2), Evan Mobley (2), Dwight Powell (2), Montrezl Harrell (2), Carlos Arroyo (2), Cody Zeller (2), Tony Battie (2), JaMychal Green (2), Daniel Gafford (2), Bogdan Bogdanovic (2), Jared Dudley (2), Dikembe Mutombo (2), Nic Claxton (2), P.J. Washington (2), John Stockton (2), Stromile Swift (3), Desmond Mason (3), Patrick Patterson (3), Jaden McDaniels (3), Bruce Bowen (3), Chet Holmgren (3), Naz Reid (3), Dante Cunningham (3), Lorenzen Wright (3), Jason Maxiell (3), Matas Buzelis (3), Jonathan Kuminga (3), Jonas Jerebko (3), Richaun Holmes (3), Robert Williams III (3), Jodie Meeks (3), Isaiah Stewart (3), Luke Kennard (3), Jordan Hill (3), Bobby Jackson (3), Nenad Krstic (3), Mark Williams (3), Trenton Hassell (3), Markelle Fultz (3), Marvin Bagley III (3), Torrey Craig (3), Brandan Wright (3), Aaron Nesmith (3), Thomas Bryant (3), Goga Bitadze (3), Ajay Mitchell (3), Walker Kessler (3), Mikki Moore (3), Paul Reed (3), Jaxson Hayes (3), Brandon Clarke (3), Nick Richards (3), Tony Snell (3), Jarron Collins (3), Moritz Wagner (3), David Robinson (3), Donovan Clingan (3), Alonzo Gee (3), Gary Payton II (3), Derik Queen (3), Keon Clark (4), Isaiah Jackson (4), Fabricio Oberto (4), Josh Boone (4), Adrian Griffin (4), Ian Clark (4), Lance Thomas (4), Tony Bradley (4), Damian Jones (4), Keita Bates-Diop (4), Chimezie Metu (4), Andrew Nicholson (4), Dereck Lively II (4), Sonny Weems (4), Trayce Jackson-Davis (4), Cheick Diallo (4), Bruno Fernando (4), Jan Vesely (4), Derrick Brown (4), Popeye Jones (4), Ryan Kalkbrenner (4), Monty Williams (4), Qyntel Woods (4), Jordan Walsh (4), Kai Jones (5)

</details>

### `five-by-n`

**Since 2001-02 (through 2025-26), name a player who recorded at least 3 points, rebounds, assists, steals and blocks in the same game.**

252 valid answers, difficulty **easy**, tiers: 1: 103, 2: 79, 3: 48, 4: 20, 5: 2 (22 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Chris Paul (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Pau Gasol (1), Joel Embiid (1), Dirk Nowitzki (1), Kevin Garnett (1), Ben Wallace (1), Stephen Curry (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Andre Drummond (1), Rajon Rondo (1), Damian Lillard (1), Brook Lopez (1), Rudy Gobert (1), Jason Kidd (1), Tracy McGrady (1), Josh Smith (1), Kyle Lowry (1), Dwyane Wade (1), Tyson Chandler (1), Nikola Vucevic (1), Andre Miller (1), Paul Pierce (1), Zach Randolph (1), Shawn Marion (1), Al Horford (1), Giannis Antetokounmpo (1), Jrue Holiday (1), Nikola Jokic (1), Andrei Kirilenko (1), Andre Iguodala (1), Draymond Green (1), LaMarcus Aldridge (1), John Wall (1), Paul George (1), Vince Carter (1), Paul Millsap (1), Serge Ibaka (1), Anthony Edwards (1), Elton Brand (1), Carlos Boozer (1), Marcus Camby (1), Kyrie Irving (1), Karl-Anthony Towns (1), Tyrese Maxey (1), Donovan Mitchell (1), Baron Davis (1), Kawhi Leonard (1), Marc Gasol (1), Al Jefferson (1), Shaquille O'Neal (1), Jeff Teague (1), Jimmy Butler III (1), Lamar Odom (1), DeMarcus Cousins (1), Thaddeus Young (1), CJ McCollum (1), Julius Randle (1), De'Aaron Fox (1), David West (1), Rudy Gay (1), Tobias Harris (1), Amar'e Stoudemire (1), Metta World Peace (1), Cade Cunningham (1), Mike Bibby (1), Danny Granger (1), Kemba Walker (1), Shane Battier (1), Monta Ellis (1), Jermaine O'Neal (1), Marcin Gortat (1), Steven Adams (1), Rasheed Wallace (1), Boris Diaw (1), Gerald Wallace (1), LaMelo Ball (1), Nicolas Batum (1), Richard Jefferson (1), Nene (1), Jarrett Jack (1), Joakim Noah (1), Blake Griffin (1), Victor Wembanyama (1), Kenyon Martin (1), Andrew Bogut (1), Brandon Ingram (1), Andrew Wiggins (1), Bam Adebayo (1), Chris Webber (1), Pascal Siakam (1), Eric Bledsoe (1), Marcus Smart (1), Jarrett Allen (1), Karl Malone (1), Desmond Bane (2), Robert Covington (2), Jamaal Tinsley (2), Rashard Lewis (2), Derrick Favors (2), Jusuf Nurkic (2), Kristaps Porzingis (2), Fred VanVleet (2), Victor Oladipo (2), Hassan Whiteside (2), Kurt Thomas (2), Troy Murphy (2), Tyrese Haliburton (2), Brad Miller (2), Brandon Roy (2), Rafer Alston (2), Jaren Jackson Jr. (2), George Hill (2), Dejounte Murray (2), Kyle Korver (2), Thabo Sefolosha (2), Tayshaun Prince (2), Deandre Ayton (2), Amir Johnson (2), Ben Simmons (2), Cuttino Mobley (2), Derrick White (2), Wesley Matthews (2), Mehmet Okur (2), Josh Hart (2), Shareef Abdur-Rahim (2), Kyle Anderson (2), Jakob Poeltl (2), Alperen Sengun (2), Nerlens Noel (2), Al-Farouq Aminu (2), Buddy Hield (2), Mikal Bridges (2), Antonio McDyess (2), James Johnson (2), Kris Humphries (2), Nickeil Alexander-Walker (2), Ricky Davis (2), P.J. Brown (2), Jae Crowder (2), Michael Finley (2), Markieff Morris (2), Spencer Hawes (2), John Salmons (2), Wendell Carter Jr. (2), Kelly Oubre Jr. (2), Dillon Brooks (2), Mitchell Robinson (2), Andris Biedrins (2), Kenny Thomas (2), Scottie Barnes (2), T.J. Warren (2), Grant Hill (2), Larry Nance Jr. (2), Kosta Koufos (2), Royce O'Neale (2), Kris Dunn (2), Donyell Marshall (2), Nate Robinson (2), Alex Caruso (2), Evan Mobley (2), Andray Blatche (2), Brent Barry (2), Isaiah Hartenstein (2), Eddie Jones (2), Robert Horry (2), Lonzo Ball (2), Amen Thompson (2), Michael Carter-Williams (2), Nic Claxton (2), Delon Wright (2), Delonte West (2), P.J. Washington (2), Darrel Armstrong (2), Otto Porter Jr. (3), Chet Holmgren (3), Raja Bell (3), Wesley Johnson (3), Francisco Garcia (3), Dante Cunningham (3), Dorell Wright (3), Clifford Robinson (3), De'Anthony Melton (3), Bruce Brown (3), Jared Jeffries (3), Mark Blount (3), Raef LaFrentz (3), Glen Davis (3), Jabari Smith Jr. (3), Robert Williams III (3), Ronnie Brewer (3), Nikola Mirotic (3), Willie Cauley-Stein (3), Kyshawn George (3), Darius Miles (3), Devean George (3), Dyson Daniels (3), Vlade Divac (3), Jonathan Isaac (3), Quentin Grimes (3), Jalen Suggs (3), Herbert Jones (3), Daniel Theis (3), Josh Okogie (3), Elden Campbell (3), Kelvin Cato (3), Ekpe Udoh (3), Greg Ostertag (3), Corliss Williamson (3), Larry Sanders (3), Anfernee Hardaway (3), Luke Kornet (3), Ausar Thompson (3), Paul Reed (3), Andre Roberson (3), Brandon Clarke (3), Bilal Coulibaly (3), Brandon Rush (3), David Robinson (3), Frank Ntilikina (3), Miles McBride (3), Jarace Walker (3), Quinton Ross (4), Julian Champagnie (4), Anthony Randolph (4), Greg Stiemsma (4), George Lynch (4), Moussa Diabate (4), Will Riley (4), Dalano Banton (4), Isaiah Roby (4), Malachi Flynn (4), Craig Porter Jr. (4), Juan Toscano-Anderson (4), Collin Murray-Boyles (4), Hakeem Olajuwon (4), Jamir Watkins (4), Justin Hamilton (4), Romeo Langford (4), Arvydas Sabonis (4), Markel Brown (4), Eric Moreland (4), Wade Baldwin IV (5), Leaky Black (5)

</details>

**Since 2001-02 (through 2025-26), name a player who recorded at least 4 points, rebounds, assists, steals and blocks in the same game.**

40 valid answers, difficulty **easy**, tiers: 1: 29, 2: 4, 3: 5, 4: 2 (2 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Ben Wallace (1), Anthony Davis (1), Andre Drummond (1), Brook Lopez (1), Jason Kidd (1), Josh Smith (1), Dwyane Wade (1), Shawn Marion (1), Giannis Antetokounmpo (1), Andrei Kirilenko (1), Draymond Green (1), Paul Millsap (1), Anthony Edwards (1), Elton Brand (1), Marcus Camby (1), Kawhi Leonard (1), Shaquille O'Neal (1), DeMarcus Cousins (1), Metta World Peace (1), Gerald Wallace (1), Nicolas Batum (1), Nene (1), Victor Wembanyama (1), Pascal Siakam (1), Eric Bledsoe (1), Jamaal Tinsley (2), Jusuf Nurkic (2), Fred VanVleet (2), Delon Wright (2), Dorell Wright (3), Willie Cauley-Stein (3), Darius Miles (3), Jonathan Isaac (3), Ausar Thompson (3), Juan Toscano-Anderson (4), Eric Moreland (4)

</details>

### `points-and-rebounds`

**Since 2001-02 (through 2025-26), name a player who scored 30 or more points and grabbed 15 or more rebounds in the same game.**

138 valid answers, difficulty **easy**, tiers: 1: 81, 2: 44, 3: 10, 4: 3 (3 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Dwight Howard (1), Kevin Durant (1), Kobe Bryant (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Pau Gasol (1), Joel Embiid (1), Dirk Nowitzki (1), Kevin Garnett (1), Stephen Curry (1), Anthony Davis (1), Andre Drummond (1), Brook Lopez (1), Rudy Gobert (1), Carmelo Anthony (1), Tracy McGrady (1), Josh Smith (1), Dwyane Wade (1), Nikola Vucevic (1), Paul Pierce (1), Zach Randolph (1), Shawn Marion (1), Al Horford (1), Giannis Antetokounmpo (1), Kevin Love (1), Nikola Jokic (1), Jayson Tatum (1), Draymond Green (1), LaMarcus Aldridge (1), Jonas Valanciunas (1), Paul George (1), Vince Carter (1), Paul Millsap (1), Elton Brand (1), Jaylen Brown (1), Carlos Boozer (1), Marcus Camby (1), Karl-Anthony Towns (1), Chris Bosh (1), Kawhi Leonard (1), Al Jefferson (1), Shaquille O'Neal (1), Jimmy Butler III (1), Lamar Odom (1), Manu Ginobili (1), Myles Turner (1), Zion Williamson (1), DeMarcus Cousins (1), David Lee (1), Lauri Markkanen (1), Julius Randle (1), David West (1), Domantas Sabonis (1), Tobias Harris (1), Amar'e Stoudemire (1), Antawn Jamison (1), Paolo Banchero (1), Danny Granger (1), Jermaine O'Neal (1), Marcin Gortat (1), Rasheed Wallace (1), Gerald Wallace (1), Yao Ming (1), Joakim Noah (1), Blake Griffin (1), Victor Wembanyama (1), Andrew Bogut (1), Brandon Ingram (1), Bam Adebayo (1), Chris Webber (1), JaVale McGee (1), Pascal Siakam (1), Enes Freedom (1), Deni Avdija (1), Jarrett Allen (1), Michael Porter Jr. (1), Khris Middleton (1), Drew Gooden (1), Zydrunas Ilgauskas (2), Rashard Lewis (2), Jusuf Nurkic (2), Austin Reaves (2), Kristaps Porzingis (2), Hassan Whiteside (2), Kurt Thomas (2), Troy Murphy (2), Brad Miller (2), Caron Butler (2), Ivica Zubac (2), Jalen Johnson (2), Greg Monroe (2), Deandre Ayton (2), Ben Simmons (2), Luis Scola (2), Antoine Walker (2), Aaron Gordon (2), Anderson Varejao (2), John Collins (2), Mehmet Okur (2), Trey Murphy III (2), Shareef Abdur-Rahim (2), Nazr Mohammed (2), Mike Miller (2), Jakob Poeltl (2), Alperen Sengun (2), Miles Bridges (2), Kris Humphries (2), Christian Wood (2), Wendell Carter Jr. (2), Andrew Bynum (2), Scottie Barnes (2), Alex Len (2), JJ Hickson (2), Jalen Duren (2), Quentin Richardson (2), Donyell Marshall (2), Kwame Brown (2), Evan Mobley (2), Andray Blatche (2), Isaiah Hartenstein (2), Daniel Gafford (2), Chris Wilcox (2), Lorenzen Wright (3), Aron Baynes (3), Nikola Mirotic (3), Chris Boucher (3), Kelenna Azubuike (3), Jared Sullinger (3), Michael Olowokandi (3), Marcus Fizer (3), Moritz Wagner (3), Derik Queen (3), Kyle Filipowski (4), Boban Marjanovic (4), Zach Edey (4)

</details>

### `points-and-assists`

**Since 2001-02 (through 2025-26), name a player who scored 30 or more points and recorded 10 or more assists in the same game.**

169 valid answers, difficulty **easy**, tiers: 1: 101, 2: 51, 3: 13, 4: 4 (4 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Chris Paul (1), Russell Westbrook (1), Luka Doncic (1), Joel Embiid (1), Dirk Nowitzki (1), Kevin Garnett (1), Steve Nash (1), Allen Iverson (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Rajon Rondo (1), Damian Lillard (1), Jason Kidd (1), Carmelo Anthony (1), Tony Parker (1), Tracy McGrady (1), DeMar DeRozan (1), Kyle Lowry (1), Dwyane Wade (1), Nikola Vucevic (1), Andre Miller (1), Paul Pierce (1), Mike Conley (1), Bradley Beal (1), Deron Williams (1), Giannis Antetokounmpo (1), Jrue Holiday (1), Kevin Love (1), Nikola Jokic (1), Jayson Tatum (1), Andre Iguodala (1), Trae Young (1), Joe Johnson (1), John Wall (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Isaiah Thomas (1), Anthony Edwards (1), Chauncey Billups (1), Jalen Brunson (1), Kyrie Irving (1), Karl-Anthony Towns (1), Tyrese Maxey (1), Donovan Mitchell (1), Baron Davis (1), Jamal Crawford (1), Ricky Rubio (1), Kawhi Leonard (1), Raymond Felton (1), Devin Booker (1), Jason Terry (1), Jeff Teague (1), Jimmy Butler III (1), Lamar Odom (1), Ja Morant (1), Zach LaVine (1), Manu Ginobili (1), Dennis Schroder (1), Zion Williamson (1), DeMarcus Cousins (1), David Lee (1), Jameer Nelson (1), CJ McCollum (1), Julius Randle (1), Goran Dragic (1), De'Aaron Fox (1), Domantas Sabonis (1), Kirk Hinrich (1), Cade Cunningham (1), Mike Bibby (1), Paolo Banchero (1), Kemba Walker (1), Mo Williams (1), Monta Ellis (1), Derrick Rose (1), Jamal Murray (1), LaMelo Ball (1), Lou Williams (1), Richard Jefferson (1), Devin Harris (1), Jarrett Jack (1), Richard Hamilton (1), Blake Griffin (1), Victor Wembanyama (1), Brandon Ingram (1), Bam Adebayo (1), Reggie Jackson (1), D'Angelo Russell (1), Collin Sexton (1), Luke Ridnour (1), Stephon Marbury (1), Pascal Siakam (1), Eric Bledsoe (1), Deni Avdija (1), Franz Wagner (1), Tyler Herro (1), Desmond Bane (2), Jamaal Tinsley (2), Ty Lawson (2), J.J. Barea (2), Austin Reaves (2), Jason Williams (2), Fred VanVleet (2), Victor Oladipo (2), Tyrese Haliburton (2), Spencer Dinwiddie (2), Brandon Roy (2), Anfernee Simons (2), Stephen Jackson (2), Brandon Jennings (2), Jalen Johnson (2), Dejounte Murray (2), Hedo Turkoglu (2), Elfrid Payton (2), Gary Payton (2), Ben Simmons (2), Sam Cassell (2), Darius Garland (2), Antoine Walker (2), Jalen Rose (2), Jalen Green (2), Tyreke Evans (2), Larry Hughes (2), Ramon Sessions (2), Steve Francis (2), Derrick White (2), Jamal Mashburn (2), Malcolm Brogdon (2), Alperen Sengun (2), T.J. Ford (2), Terry Rozier (2), RJ Barrett (2), Caris LeVert (2), Ricky Davis (2), Antonio Daniels (2), Mike James (2002-2014) (2), Patty Mills (2), Randy Foye (2), Jeremy Lin (2), Scottie Barnes (2), Brandon Knight (2), Kevin Porter Jr. (2), Nate Robinson (2), Brent Barry (2), Nick Van Exel (2), Cameron Payne (2), Delonte West (2), Ryan Rollins (3), Immanuel Quickley (3), Andrew Nembhard (3), Payton Pritchard (3), Trey Burke (3), Stephon Castle (3), VJ Edgecombe (3), Troy Hudson (3), Naji Marshall (3), Talen Horton-Tucker (3), Collin Gillespie (3), Jevon Carter (3), Derik Queen (3), Scotty Pippen Jr. (4), Jared McCain (4), Ousmane Dieng (4), Rayan Rupert (4)

</details>

### `rebounds-per-game`

**Since 2001-02 (through 2025-26), name a player who averaged 10 or more rebounds per game in a regular season (minimum 40 games).**

82 valid answers, difficulty **easy**, tiers: 1: 51, 2: 26, 3: 5 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Dwight Howard (1), Tim Duncan (1), Russell Westbrook (1), Pau Gasol (1), Joel Embiid (1), Kevin Garnett (1), Ben Wallace (1), Anthony Davis (1), Andre Drummond (1), Rudy Gobert (1), DeAndre Jordan (1), Tyson Chandler (1), Nikola Vucevic (1), Zach Randolph (1), Shawn Marion (1), Al Horford (1), Giannis Antetokounmpo (1), Kevin Love (1), Nikola Jokic (1), LaMarcus Aldridge (1), Jonas Valanciunas (1), Elton Brand (1), Carlos Boozer (1), Marcus Camby (1), Karl-Anthony Towns (1), Chris Bosh (1), Clint Capela (1), Al Jefferson (1), Shaquille O'Neal (1), Lamar Odom (1), DeMarcus Cousins (1), David Lee (1), Julius Randle (1), Domantas Sabonis (1), Tristan Thompson (1), Antawn Jamison (1), Samuel Dalembert (1), Jermaine O'Neal (1), Marcin Gortat (1), Steven Adams (1), Gerald Wallace (1), Yao Ming (1), Joakim Noah (1), Blake Griffin (1), Victor Wembanyama (1), Andrew Bogut (1), Bam Adebayo (1), Chris Webber (1), Enes Freedom (1), Jarrett Allen (1), Reggie Evans (1), Emeka Okafor (2), Jusuf Nurkic (2), Hassan Whiteside (2), Kurt Thomas (2), Troy Murphy (2), Chris Kaman (2), Brad Miller (2), Ivica Zubac (2), Erick Dampier (2), Jalen Johnson (2), Greg Monroe (2), Deandre Ayton (2), John Collins (2), Alperen Sengun (2), Kris Humphries (2), Christian Wood (2), Jamaal Magloire (2), Wendell Carter Jr. (2), Andrew Bynum (2), Andris Biedrins (2), Kenny Thomas (2), JJ Hickson (2), Omer Asik (2), Jalen Duren (2), Isaiah Hartenstein (2), Dikembe Mutombo (2), Mark Williams (3), Brian Grant (3), Walker Kessler (3), Danny Fortson (3), Donovan Clingan (3)

</details>

**Since 2001-02 (through 2025-26), name a player who averaged 11 or more rebounds per game in a regular season (minimum 40 games).**

52 valid answers, difficulty **easy**, tiers: 1: 37, 2: 12, 3: 3 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Dwight Howard (1), Tim Duncan (1), Russell Westbrook (1), Pau Gasol (1), Joel Embiid (1), Kevin Garnett (1), Ben Wallace (1), Anthony Davis (1), Andre Drummond (1), Rudy Gobert (1), DeAndre Jordan (1), Tyson Chandler (1), Nikola Vucevic (1), Zach Randolph (1), Shawn Marion (1), Giannis Antetokounmpo (1), Kevin Love (1), Nikola Jokic (1), LaMarcus Aldridge (1), Jonas Valanciunas (1), Elton Brand (1), Carlos Boozer (1), Marcus Camby (1), Karl-Anthony Towns (1), Clint Capela (1), Al Jefferson (1), Shaquille O'Neal (1), DeMarcus Cousins (1), David Lee (1), Domantas Sabonis (1), Steven Adams (1), Joakim Noah (1), Blake Griffin (1), Victor Wembanyama (1), Andrew Bogut (1), Enes Freedom (1), Reggie Evans (1), Emeka Okafor (2), Jusuf Nurkic (2), Hassan Whiteside (2), Troy Murphy (2), Chris Kaman (2), Ivica Zubac (2), Erick Dampier (2), Deandre Ayton (2), Andrew Bynum (2), Andris Biedrins (2), Omer Asik (2), Jalen Duren (2), Walker Kessler (3), Danny Fortson (3), Donovan Clingan (3)

</details>

**Since 2001-02 (through 2025-26), name a player who averaged 12 or more rebounds per game in a regular season (minimum 40 games).**

25 valid answers, difficulty **medium**, tiers: 1: 21, 2: 3, 3: 1 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Dwight Howard (1), Tim Duncan (1), Joel Embiid (1), Kevin Garnett (1), Ben Wallace (1), Anthony Davis (1), Andre Drummond (1), Rudy Gobert (1), DeAndre Jordan (1), Tyson Chandler (1), Nikola Vucevic (1), Zach Randolph (1), Giannis Antetokounmpo (1), Kevin Love (1), Nikola Jokic (1), Jonas Valanciunas (1), Marcus Camby (1), Karl-Anthony Towns (1), Clint Capela (1), DeMarcus Cousins (1), Domantas Sabonis (1), Hassan Whiteside (2), Chris Kaman (2), Ivica Zubac (2), Walker Kessler (3)

</details>

### `assists-per-game`

**Since 2001-02 (through 2025-26), name a player who averaged 8 or more assists per game in a regular season (minimum 40 games).**

42 valid answers, difficulty **easy**, tiers: 1: 28, 2: 13, 3: 1 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Chris Paul (1), Russell Westbrook (1), Luka Doncic (1), Steve Nash (1), Stephen Curry (1), Rajon Rondo (1), Damian Lillard (1), Jason Kidd (1), Kyle Lowry (1), Andre Miller (1), Deron Williams (1), Jrue Holiday (1), Nikola Jokic (1), Trae Young (1), Draymond Green (1), John Wall (1), Chauncey Billups (1), Baron Davis (1), Jose Calderon (1), Ricky Rubio (1), Raymond Felton (1), Jeff Teague (1), Ja Morant (1), Domantas Sabonis (1), Cade Cunningham (1), Stephon Marbury (1), Jamaal Tinsley (2), Ty Lawson (2), Jason Williams (2), Fred VanVleet (2), Tyrese Haliburton (2), Dejounte Murray (2), Gary Payton (2), Ben Simmons (2), Darius Garland (2), Brevin Knight (2), Josh Giddey (2), Greivis Vasquez (2), John Stockton (2), Kendall Marshall (3)

</details>

**Since 2001-02 (through 2025-26), name a player who averaged 9 or more assists per game in a regular season (minimum 40 games).**

19 valid answers, difficulty **medium**, tiers: 1: 15, 2: 4 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Chris Paul (1), Russell Westbrook (1), Luka Doncic (1), Steve Nash (1), Rajon Rondo (1), Jason Kidd (1), Andre Miller (1), Deron Williams (1), Nikola Jokic (1), Trae Young (1), John Wall (1), Ricky Rubio (1), Cade Cunningham (1), Ty Lawson (2), Tyrese Haliburton (2), Dejounte Murray (2), Josh Giddey (2)

</details>

### `steals-per-game`

**Since 2001-02 (through 2025-26), name a player who averaged 2 or more steals per game in a regular season (minimum 40 games).**

41 valid answers, difficulty **easy**, tiers: 1: 30, 2: 8, 3: 3 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kobe Bryant (1), Chris Paul (1), Russell Westbrook (1), Allen Iverson (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Rajon Rondo (1), Jason Kidd (1), Kyle Lowry (1), Dwyane Wade (1), Mike Conley (1), Shawn Marion (1), Andre Iguodala (1), Draymond Green (1), John Wall (1), Gilbert Arenas (1), Paul George (1), Baron Davis (1), Ricky Rubio (1), Kawhi Leonard (1), Jimmy Butler III (1), Thaddeus Young (1), De'Aaron Fox (1), Metta World Peace (1), Monta Ellis (1), Gerald Wallace (1), Eric Bledsoe (1), Tony Allen (1), Jamaal Tinsley (2), Victor Oladipo (2), Caron Butler (2), Dejounte Murray (2), Ben Simmons (2), Larry Hughes (2), Brevin Knight (2), Kris Dunn (2), Doug Christie (3), Dyson Daniels (3), Ausar Thompson (3)

</details>

### `blocks-per-game`

**Since 2001-02 (through 2025-26), name a player who averaged 2 or more blocks per game in a regular season (minimum 40 games).**

56 valid answers, difficulty **easy**, tiers: 1: 26, 2: 19, 3: 11 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Dwight Howard (1), Tim Duncan (1), Pau Gasol (1), Kevin Garnett (1), Ben Wallace (1), Anthony Davis (1), Brook Lopez (1), Rudy Gobert (1), Josh Smith (1), DeAndre Jordan (1), Andrei Kirilenko (1), Serge Ibaka (1), Elton Brand (1), Marcus Camby (1), Clint Capela (1), Shaquille O'Neal (1), Myles Turner (1), Amar'e Stoudemire (1), Samuel Dalembert (1), Jermaine O'Neal (1), Gerald Wallace (1), Yao Ming (1), Joakim Noah (1), Victor Wembanyama (1), Andrew Bogut (1), JaVale McGee (1), Zydrunas Ilgauskas (2), Emeka Okafor (2), Kristaps Porzingis (2), Brendan Haywood (2), Hassan Whiteside (2), Roy Hibbert (2), Chris Kaman (2), Erick Dampier (2), Jaren Jackson Jr. (2), Chris Andersen (2), Nerlens Noel (2), Theo Ratliff (2), Mitchell Robinson (2), Rasho Nesterovic (2), Joel Przybilla (2), Adonal Foyle (2), Daniel Gafford (2), Dikembe Mutombo (2), Nic Claxton (2), Chet Holmgren (3), John Henson (3), Darko Milicic (3), Ronny Turiaf (3), Raef LaFrentz (3), Alonzo Mourning (3), Robert Williams III (3), Eddie Griffin (3), Larry Sanders (3), Walker Kessler (3), Shawn Bradley (3)

</details>

### `double-double-average`

**Since 2001-02 (through 2025-26), name a player who averaged a double-double (10 or more points and 10 or more rebounds per game) in a regular season (minimum 40 games).**

79 valid answers, difficulty **easy**, tiers: 1: 48, 2: 26, 3: 5 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Dwight Howard (1), Tim Duncan (1), Russell Westbrook (1), Pau Gasol (1), Joel Embiid (1), Kevin Garnett (1), Anthony Davis (1), Andre Drummond (1), Rudy Gobert (1), DeAndre Jordan (1), Tyson Chandler (1), Nikola Vucevic (1), Zach Randolph (1), Shawn Marion (1), Al Horford (1), Giannis Antetokounmpo (1), Kevin Love (1), Nikola Jokic (1), LaMarcus Aldridge (1), Jonas Valanciunas (1), Elton Brand (1), Carlos Boozer (1), Marcus Camby (1), Karl-Anthony Towns (1), Chris Bosh (1), Clint Capela (1), Al Jefferson (1), Shaquille O'Neal (1), Lamar Odom (1), DeMarcus Cousins (1), David Lee (1), Julius Randle (1), Domantas Sabonis (1), Tristan Thompson (1), Antawn Jamison (1), Samuel Dalembert (1), Jermaine O'Neal (1), Marcin Gortat (1), Gerald Wallace (1), Yao Ming (1), Joakim Noah (1), Blake Griffin (1), Victor Wembanyama (1), Andrew Bogut (1), Bam Adebayo (1), Chris Webber (1), Enes Freedom (1), Jarrett Allen (1), Emeka Okafor (2), Jusuf Nurkic (2), Hassan Whiteside (2), Kurt Thomas (2), Troy Murphy (2), Chris Kaman (2), Brad Miller (2), Ivica Zubac (2), Erick Dampier (2), Jalen Johnson (2), Greg Monroe (2), Deandre Ayton (2), John Collins (2), Alperen Sengun (2), Kris Humphries (2), Christian Wood (2), Jamaal Magloire (2), Wendell Carter Jr. (2), Andrew Bynum (2), Andris Biedrins (2), Kenny Thomas (2), JJ Hickson (2), Omer Asik (2), Jalen Duren (2), Isaiah Hartenstein (2), Dikembe Mutombo (2), Mark Williams (3), Brian Grant (3), Walker Kessler (3), Danny Fortson (3), Donovan Clingan (3)

</details>

## Team templates: examples

Three candidates per template, from the shortest list to the longest. Each answer is shown as name (tier).

### `wins-season`

**Since 2001-02 (through 2025-26), name a team that won 65 or more regular-season games in a season.**

9 valid answers, difficulty **medium**, tiers: 1: 9 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Boston Celtics (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Golden State Warriors (1), Houston Rockets (1), Los Angeles Lakers (1), Miami Heat (1), Oklahoma City Thunder (1), San Antonio Spurs (1)

</details>

**Since 2001-02 (through 2025-26), name a team that won 60 or more regular-season games in a season.**

16 valid answers, difficulty **easy**, tiers: 1: 16 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Atlanta Hawks (1), Boston Celtics (1), Chicago Bulls (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Detroit Pistons (1), Golden State Warriors (1), Houston Rockets (1), Indiana Pacers (1), Los Angeles Lakers (1), Miami Heat (1), Milwaukee Bucks (1), Oklahoma City Thunder (1), Phoenix Suns (1), Sacramento Kings (1), San Antonio Spurs (1)

</details>

**Since 2001-02 (through 2025-26), name a team that won 50 or more regular-season games in a season.**

28 valid answers, difficulty **easy**, tiers: 1: 26, 4: 2 (2 at tier 4 or above).

Qualified only under a historical name: Brooklyn Nets, New Orleans Pelicans.

<details><summary>All valid answers</summary>

Atlanta Hawks (1), Boston Celtics (1), Chicago Bulls (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Detroit Pistons (1), Golden State Warriors (1), Houston Rockets (1), Indiana Pacers (1), LA Clippers (1), Los Angeles Lakers (1), Memphis Grizzlies (1), Miami Heat (1), Milwaukee Bucks (1), Minnesota Timberwolves (1), New York Knicks (1), Oklahoma City Thunder (1), Orlando Magic (1), Philadelphia 76ers (1), Phoenix Suns (1), Portland Trail Blazers (1), Sacramento Kings (1), San Antonio Spurs (1), Toronto Raptors (1), Utah Jazz (1), Brooklyn Nets (4), New Orleans Pelicans (4)

</details>

### `wins-playoff`

**Since 2001-02 (through 2025-26), name a team that won 16 or more playoff games in a single postseason.**

13 valid answers, difficulty **easy**, tiers: 1: 13 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Boston Celtics (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Detroit Pistons (1), Golden State Warriors (1), Los Angeles Lakers (1), Miami Heat (1), Milwaukee Bucks (1), New York Knicks (1), Oklahoma City Thunder (1), San Antonio Spurs (1), Toronto Raptors (1)

</details>

**Since 2001-02 (through 2025-26), name a team that won 14 or more playoff games in a single postseason.**

16 valid answers, difficulty **medium**, tiers: 1: 15, 4: 1 (1 at tier 4 or above).

Qualified only under a historical name: Brooklyn Nets.

<details><summary>All valid answers</summary>

Boston Celtics (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Detroit Pistons (1), Golden State Warriors (1), Indiana Pacers (1), Los Angeles Lakers (1), Miami Heat (1), Milwaukee Bucks (1), New York Knicks (1), Oklahoma City Thunder (1), Phoenix Suns (1), San Antonio Spurs (1), Toronto Raptors (1), Brooklyn Nets (4)

</details>

**Since 2001-02 (through 2025-26), name a team that won 10 or more playoff games in a single postseason.**

22 valid answers, difficulty **easy**, tiers: 1: 21, 4: 1 (1 at tier 4 or above).

Qualified only under a historical name: Brooklyn Nets.

<details><summary>All valid answers</summary>

Atlanta Hawks (1), Boston Celtics (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Detroit Pistons (1), Golden State Warriors (1), Houston Rockets (1), Indiana Pacers (1), LA Clippers (1), Los Angeles Lakers (1), Miami Heat (1), Milwaukee Bucks (1), Minnesota Timberwolves (1), New York Knicks (1), Oklahoma City Thunder (1), Orlando Magic (1), Phoenix Suns (1), Sacramento Kings (1), San Antonio Spurs (1), Toronto Raptors (1), Brooklyn Nets (4)

</details>

### `points-regulation`

**Since 2001-02 (through 2025-26), name a team that scored 155 or more points in a regulation game.**

10 valid answers, difficulty **medium**, tiers: 1: 10 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Boston Celtics (1), Charlotte Hornets (1), Denver Nuggets (1), Golden State Warriors (1), Houston Rockets (1), Indiana Pacers (1), Memphis Grizzlies (1), New Orleans Pelicans (1), Philadelphia 76ers (1), Washington Wizards (1)

</details>

**Since 2001-02 (through 2025-26), name a team that scored 140 or more points in a regulation game.**

30 valid answers, difficulty **easy**, tiers: 1: 30 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Atlanta Hawks (1), Boston Celtics (1), Brooklyn Nets (1), Charlotte Hornets (1), Chicago Bulls (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Detroit Pistons (1), Golden State Warriors (1), Houston Rockets (1), Indiana Pacers (1), LA Clippers (1), Los Angeles Lakers (1), Memphis Grizzlies (1), Miami Heat (1), Milwaukee Bucks (1), Minnesota Timberwolves (1), New Orleans Pelicans (1), New York Knicks (1), Oklahoma City Thunder (1), Orlando Magic (1), Philadelphia 76ers (1), Phoenix Suns (1), Portland Trail Blazers (1), Sacramento Kings (1), San Antonio Spurs (1), Toronto Raptors (1), Utah Jazz (1), Washington Wizards (1)

</details>

**Since 2001-02 (through 2025-26), name a team that scored 145 or more points in a regulation game.**

30 valid answers, difficulty **easy**, tiers: 1: 30 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Atlanta Hawks (1), Boston Celtics (1), Brooklyn Nets (1), Charlotte Hornets (1), Chicago Bulls (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Detroit Pistons (1), Golden State Warriors (1), Houston Rockets (1), Indiana Pacers (1), LA Clippers (1), Los Angeles Lakers (1), Memphis Grizzlies (1), Miami Heat (1), Milwaukee Bucks (1), Minnesota Timberwolves (1), New Orleans Pelicans (1), New York Knicks (1), Oklahoma City Thunder (1), Orlando Magic (1), Philadelphia 76ers (1), Phoenix Suns (1), Portland Trail Blazers (1), Sacramento Kings (1), San Antonio Spurs (1), Toronto Raptors (1), Utah Jazz (1), Washington Wizards (1)

</details>

### `win-margin`

**Since 2001-02 (through 2025-26), name a team that won a game by 55 or more points.**

11 valid answers, difficulty **medium**, tiers: 1: 11 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Boston Celtics (1), Charlotte Hornets (1), Cleveland Cavaliers (1), Denver Nuggets (1), Golden State Warriors (1), Indiana Pacers (1), LA Clippers (1), Los Angeles Lakers (1), Memphis Grizzlies (1), Miami Heat (1), Oklahoma City Thunder (1)

</details>

**Since 2001-02 (through 2025-26), name a team that won a game by 45 or more points.**

28 valid answers, difficulty **easy**, tiers: 1: 28 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Atlanta Hawks (1), Boston Celtics (1), Brooklyn Nets (1), Charlotte Hornets (1), Chicago Bulls (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Detroit Pistons (1), Golden State Warriors (1), Houston Rockets (1), Indiana Pacers (1), LA Clippers (1), Los Angeles Lakers (1), Memphis Grizzlies (1), Miami Heat (1), Milwaukee Bucks (1), Minnesota Timberwolves (1), New Orleans Pelicans (1), New York Knicks (1), Oklahoma City Thunder (1), Philadelphia 76ers (1), Phoenix Suns (1), Portland Trail Blazers (1), San Antonio Spurs (1), Toronto Raptors (1), Utah Jazz (1), Washington Wizards (1)

</details>

**Since 2001-02 (through 2025-26), name a team that won a game by 40 or more points.**

30 valid answers, difficulty **easy**, tiers: 1: 30 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Atlanta Hawks (1), Boston Celtics (1), Brooklyn Nets (1), Charlotte Hornets (1), Chicago Bulls (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Detroit Pistons (1), Golden State Warriors (1), Houston Rockets (1), Indiana Pacers (1), LA Clippers (1), Los Angeles Lakers (1), Memphis Grizzlies (1), Miami Heat (1), Milwaukee Bucks (1), Minnesota Timberwolves (1), New Orleans Pelicans (1), New York Knicks (1), Oklahoma City Thunder (1), Orlando Magic (1), Philadelphia 76ers (1), Phoenix Suns (1), Portland Trail Blazers (1), Sacramento Kings (1), San Antonio Spurs (1), Toronto Raptors (1), Utah Jazz (1), Washington Wizards (1)

</details>

### `losses-season`

**Since 2001-02 (through 2025-26), name a team that lost 67 or more regular-season games in a season.**

8 valid answers, difficulty **hard**, tiers: 1: 7, 4: 1 (1 at tier 4 or above).

Qualified only under a historical name: Brooklyn Nets.

<details><summary>All valid answers</summary>

Atlanta Hawks (1), Detroit Pistons (1), Miami Heat (1), Milwaukee Bucks (1), Minnesota Timberwolves (1), Philadelphia 76ers (1), Washington Wizards (1), Brooklyn Nets (4)

</details>

**Since 2001-02 (through 2025-26), name a team that lost 62 or more regular-season games in a season.**

22 valid answers, difficulty **medium**, tiers: 1: 20, 4: 2 (2 at tier 4 or above).

Qualified only under a historical name: New Orleans Pelicans, Oklahoma City Thunder.

<details><summary>All valid answers</summary>

Atlanta Hawks (1), Brooklyn Nets (1), Charlotte Hornets (1), Cleveland Cavaliers (1), Denver Nuggets (1), Detroit Pistons (1), Houston Rockets (1), Indiana Pacers (1), LA Clippers (1), Los Angeles Lakers (1), Miami Heat (1), Milwaukee Bucks (1), Minnesota Timberwolves (1), New York Knicks (1), Orlando Magic (1), Philadelphia 76ers (1), Phoenix Suns (1), Sacramento Kings (1), Utah Jazz (1), Washington Wizards (1), New Orleans Pelicans (4), Oklahoma City Thunder (4)

</details>

**Since 2001-02 (through 2025-26), name a team that lost 55 or more regular-season games in a season.**

30 valid answers, difficulty **easy**, tiers: 1: 30 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Atlanta Hawks (1), Boston Celtics (1), Brooklyn Nets (1), Charlotte Hornets (1), Chicago Bulls (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Detroit Pistons (1), Golden State Warriors (1), Houston Rockets (1), Indiana Pacers (1), LA Clippers (1), Los Angeles Lakers (1), Memphis Grizzlies (1), Miami Heat (1), Milwaukee Bucks (1), Minnesota Timberwolves (1), New Orleans Pelicans (1), New York Knicks (1), Oklahoma City Thunder (1), Orlando Magic (1), Philadelphia 76ers (1), Phoenix Suns (1), Portland Trail Blazers (1), Sacramento Kings (1), San Antonio Spurs (1), Toronto Raptors (1), Utah Jazz (1), Washington Wizards (1)

</details>

### `road-wins`

**Since 2001-02 (through 2025-26), name a team that won 26 or more road games in a regular season.**

22 valid answers, difficulty **easy**, tiers: 1: 22 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Boston Celtics (1), Chicago Bulls (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Detroit Pistons (1), Golden State Warriors (1), Houston Rockets (1), Indiana Pacers (1), LA Clippers (1), Los Angeles Lakers (1), Memphis Grizzlies (1), Miami Heat (1), Milwaukee Bucks (1), Minnesota Timberwolves (1), New Orleans Pelicans (1), Oklahoma City Thunder (1), Orlando Magic (1), Philadelphia 76ers (1), Phoenix Suns (1), San Antonio Spurs (1), Toronto Raptors (1)

</details>

**Since 2001-02 (through 2025-26), name a team that won 28 or more road games in a regular season.**

12 valid answers, difficulty **easy**, tiers: 1: 12 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Boston Celtics (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Detroit Pistons (1), Golden State Warriors (1), Houston Rockets (1), Los Angeles Lakers (1), Miami Heat (1), New Orleans Pelicans (1), Oklahoma City Thunder (1), Phoenix Suns (1), San Antonio Spurs (1)

</details>

**Since 2001-02 (through 2025-26), name a team that won 30 or more road games in a regular season.**

8 valid answers, difficulty **medium**, tiers: 1: 8 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Boston Celtics (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Golden State Warriors (1), Houston Rockets (1), Oklahoma City Thunder (1), Phoenix Suns (1), San Antonio Spurs (1)

</details>

### `home-wins`

**Since 2001-02 (through 2025-26), name a team that won 36 or more home games in a regular season.**

13 valid answers, difficulty **easy**, tiers: 1: 13 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Boston Celtics (1), Chicago Bulls (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Detroit Pistons (1), Golden State Warriors (1), Los Angeles Lakers (1), Miami Heat (1), Oklahoma City Thunder (1), Sacramento Kings (1), San Antonio Spurs (1), Utah Jazz (1)

</details>

### `points-playoff-team`

**Since 2001-02 (through 2025-26), name a team that scored 145 or more points in a playoff game.**

5 valid answers, difficulty **medium**, tiers: 1: 5 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Denver Nuggets (1), LA Clippers (1), Oklahoma City Thunder (1), Philadelphia 76ers (1), Toronto Raptors (1)

</details>

**Since 2001-02 (through 2025-26), name a team that scored 135 or more points in a playoff game.**

20 valid answers, difficulty **easy**, tiers: 1: 20 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Brooklyn Nets (1), Chicago Bulls (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Golden State Warriors (1), Indiana Pacers (1), LA Clippers (1), Los Angeles Lakers (1), Milwaukee Bucks (1), Minnesota Timberwolves (1), New York Knicks (1), Oklahoma City Thunder (1), Philadelphia 76ers (1), Phoenix Suns (1), Portland Trail Blazers (1), Sacramento Kings (1), San Antonio Spurs (1), Toronto Raptors (1), Utah Jazz (1)

</details>

**Since 2001-02 (through 2025-26), name a team that scored 130 or more points in a playoff game.**

26 valid answers, difficulty **easy**, tiers: 1: 26 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Atlanta Hawks (1), Boston Celtics (1), Brooklyn Nets (1), Chicago Bulls (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Golden State Warriors (1), Houston Rockets (1), Indiana Pacers (1), LA Clippers (1), Los Angeles Lakers (1), Memphis Grizzlies (1), Miami Heat (1), Milwaukee Bucks (1), Minnesota Timberwolves (1), New Orleans Pelicans (1), New York Knicks (1), Oklahoma City Thunder (1), Philadelphia 76ers (1), Phoenix Suns (1), Portland Trail Blazers (1), Sacramento Kings (1), San Antonio Spurs (1), Toronto Raptors (1), Utah Jazz (1)

</details>

### `points-any-game`

**Since 2001-02 (through 2025-26), name a team that scored 150 or more points in a game, overtime included.**

25 valid answers, difficulty **easy**, tiers: 1: 25 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Atlanta Hawks (1), Boston Celtics (1), Brooklyn Nets (1), Charlotte Hornets (1), Chicago Bulls (1), Denver Nuggets (1), Golden State Warriors (1), Houston Rockets (1), Indiana Pacers (1), LA Clippers (1), Los Angeles Lakers (1), Memphis Grizzlies (1), Miami Heat (1), Milwaukee Bucks (1), Minnesota Timberwolves (1), New Orleans Pelicans (1), New York Knicks (1), Oklahoma City Thunder (1), Philadelphia 76ers (1), Phoenix Suns (1), Sacramento Kings (1), San Antonio Spurs (1), Toronto Raptors (1), Utah Jazz (1), Washington Wizards (1)

</details>

**Since 2001-02 (through 2025-26), name a team that scored 155 or more points in a game, overtime included.**

17 valid answers, difficulty **medium**, tiers: 1: 16, 4: 1 (1 at tier 4 or above).

Qualified only under a historical name: Brooklyn Nets.

<details><summary>All valid answers</summary>

Atlanta Hawks (1), Boston Celtics (1), Charlotte Hornets (1), Chicago Bulls (1), Denver Nuggets (1), Golden State Warriors (1), Houston Rockets (1), Indiana Pacers (1), LA Clippers (1), Memphis Grizzlies (1), New Orleans Pelicans (1), Philadelphia 76ers (1), Phoenix Suns (1), Sacramento Kings (1), San Antonio Spurs (1), Washington Wizards (1), Brooklyn Nets (4)

</details>

**Since 2001-02 (through 2025-26), name a team that scored 160 or more points in a game, overtime included.**

7 valid answers, difficulty **medium**, tiers: 1: 7 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Atlanta Hawks (1), Chicago Bulls (1), Denver Nuggets (1), Indiana Pacers (1), LA Clippers (1), Phoenix Suns (1), Sacramento Kings (1)

</details>

### `win-margin-playoff`

**Since 2001-02 (through 2025-26), name a team that won a playoff game by 35 or more points.**

21 valid answers, difficulty **easy**, tiers: 1: 21 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Boston Celtics (1), Brooklyn Nets (1), Chicago Bulls (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Golden State Warriors (1), LA Clippers (1), Los Angeles Lakers (1), Memphis Grizzlies (1), Miami Heat (1), Milwaukee Bucks (1), Minnesota Timberwolves (1), New York Knicks (1), Oklahoma City Thunder (1), Orlando Magic (1), Philadelphia 76ers (1), San Antonio Spurs (1), Toronto Raptors (1), Utah Jazz (1), Washington Wizards (1)

</details>

**Since 2001-02 (through 2025-26), name a team that won a playoff game by 40 or more points.**

11 valid answers, difficulty **medium**, tiers: 1: 11 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Chicago Bulls (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Golden State Warriors (1), LA Clippers (1), Los Angeles Lakers (1), Minnesota Timberwolves (1), New York Knicks (1), Oklahoma City Thunder (1), Orlando Magic (1)

</details>

**Since 2001-02 (through 2025-26), name a team that won a playoff game by 45 or more points.**

6 valid answers, difficulty **medium**, tiers: 1: 6 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Chicago Bulls (1), Cleveland Cavaliers (1), Denver Nuggets (1), Minnesota Timberwolves (1), New York Knicks (1), Oklahoma City Thunder (1)

</details>

### `held-opponent`

**Since 2001-02 (through 2025-26), name a team that held an opponent to 60 or fewer points in a game.**

14 valid answers, difficulty **hard**, tiers: 1: 11, 4: 3 (3 at tier 4 or above).

Qualified only under a historical name: Brooklyn Nets, New Orleans Pelicans, Oklahoma City Thunder.

<details><summary>All valid answers</summary>

Boston Celtics (1), Chicago Bulls (1), Dallas Mavericks (1), Detroit Pistons (1), Indiana Pacers (1), Los Angeles Lakers (1), Minnesota Timberwolves (1), Philadelphia 76ers (1), Toronto Raptors (1), Utah Jazz (1), Washington Wizards (1), Brooklyn Nets (4), New Orleans Pelicans (4), Oklahoma City Thunder (4)

</details>

**Since 2001-02 (through 2025-26), name a team that held an opponent to 65 or fewer points in a game.**

28 valid answers, difficulty **easy**, tiers: 1: 24, 4: 4 (4 at tier 4 or above).

Qualified only under a historical name: Brooklyn Nets, Charlotte Hornets, New Orleans Pelicans, Oklahoma City Thunder.

<details><summary>All valid answers</summary>

Atlanta Hawks (1), Boston Celtics (1), Chicago Bulls (1), Dallas Mavericks (1), Denver Nuggets (1), Detroit Pistons (1), Golden State Warriors (1), Houston Rockets (1), Indiana Pacers (1), LA Clippers (1), Los Angeles Lakers (1), Memphis Grizzlies (1), Miami Heat (1), Milwaukee Bucks (1), Minnesota Timberwolves (1), New York Knicks (1), Philadelphia 76ers (1), Phoenix Suns (1), Portland Trail Blazers (1), Sacramento Kings (1), San Antonio Spurs (1), Toronto Raptors (1), Utah Jazz (1), Washington Wizards (1), Brooklyn Nets (4), Charlotte Hornets (4), New Orleans Pelicans (4), Oklahoma City Thunder (4)

</details>

**Since 2001-02 (through 2025-26), name a team that held an opponent to 70 or fewer points in a game.**

30 valid answers, difficulty **easy**, tiers: 1: 28, 4: 2 (2 at tier 4 or above).

Qualified only under a historical name: Charlotte Hornets, New Orleans Pelicans.

<details><summary>All valid answers</summary>

Atlanta Hawks (1), Boston Celtics (1), Brooklyn Nets (1), Chicago Bulls (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Detroit Pistons (1), Golden State Warriors (1), Houston Rockets (1), Indiana Pacers (1), LA Clippers (1), Los Angeles Lakers (1), Memphis Grizzlies (1), Miami Heat (1), Milwaukee Bucks (1), Minnesota Timberwolves (1), New York Knicks (1), Oklahoma City Thunder (1), Orlando Magic (1), Philadelphia 76ers (1), Phoenix Suns (1), Portland Trail Blazers (1), Sacramento Kings (1), San Antonio Spurs (1), Toronto Raptors (1), Utah Jazz (1), Washington Wizards (1), Charlotte Hornets (4), New Orleans Pelicans (4)

</details>

### `threes-team`

**Since 2001-02 (through 2025-26), name a team that made 24 or more three-pointers as a team in a game.**

27 valid answers, difficulty **easy**, tiers: 1: 27 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Atlanta Hawks (1), Boston Celtics (1), Brooklyn Nets (1), Charlotte Hornets (1), Chicago Bulls (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Golden State Warriors (1), Houston Rockets (1), Indiana Pacers (1), LA Clippers (1), Memphis Grizzlies (1), Miami Heat (1), Milwaukee Bucks (1), Minnesota Timberwolves (1), New Orleans Pelicans (1), New York Knicks (1), Oklahoma City Thunder (1), Orlando Magic (1), Philadelphia 76ers (1), Phoenix Suns (1), Portland Trail Blazers (1), Sacramento Kings (1), San Antonio Spurs (1), Toronto Raptors (1), Utah Jazz (1)

</details>

**Since 2001-02 (through 2025-26), name a team that made 26 or more three-pointers as a team in a game.**

14 valid answers, difficulty **easy**, tiers: 1: 14 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Boston Celtics (1), Brooklyn Nets (1), Charlotte Hornets (1), Cleveland Cavaliers (1), Golden State Warriors (1), Houston Rockets (1), Indiana Pacers (1), LA Clippers (1), Memphis Grizzlies (1), Milwaukee Bucks (1), Minnesota Timberwolves (1), Oklahoma City Thunder (1), Orlando Magic (1), Utah Jazz (1)

</details>

**Since 2001-02 (through 2025-26), name a team that made 28 or more three-pointers as a team in a game.**

5 valid answers, difficulty **medium**, tiers: 1: 5 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Boston Celtics (1), Houston Rockets (1), Memphis Grizzlies (1), Milwaukee Bucks (1), Utah Jazz (1)

</details>

### `steals-team`

**Since 2001-02 (through 2025-26), name a team that recorded 18 or more steals as a team in a game.**

30 valid answers, difficulty **easy**, tiers: 1: 30 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Atlanta Hawks (1), Boston Celtics (1), Brooklyn Nets (1), Charlotte Hornets (1), Chicago Bulls (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Detroit Pistons (1), Golden State Warriors (1), Houston Rockets (1), Indiana Pacers (1), LA Clippers (1), Los Angeles Lakers (1), Memphis Grizzlies (1), Miami Heat (1), Milwaukee Bucks (1), Minnesota Timberwolves (1), New Orleans Pelicans (1), New York Knicks (1), Oklahoma City Thunder (1), Orlando Magic (1), Philadelphia 76ers (1), Phoenix Suns (1), Portland Trail Blazers (1), Sacramento Kings (1), San Antonio Spurs (1), Toronto Raptors (1), Utah Jazz (1), Washington Wizards (1)

</details>

**Since 2001-02 (through 2025-26), name a team that recorded 20 or more steals as a team in a game.**

19 valid answers, difficulty **medium**, tiers: 1: 18, 4: 1 (1 at tier 4 or above).

Qualified only under a historical name: Charlotte Hornets.

<details><summary>All valid answers</summary>

Atlanta Hawks (1), Boston Celtics (1), Dallas Mavericks (1), Golden State Warriors (1), Houston Rockets (1), LA Clippers (1), Memphis Grizzlies (1), Miami Heat (1), Milwaukee Bucks (1), New Orleans Pelicans (1), New York Knicks (1), Orlando Magic (1), Philadelphia 76ers (1), Portland Trail Blazers (1), Sacramento Kings (1), Toronto Raptors (1), Utah Jazz (1), Washington Wizards (1), Charlotte Hornets (4)

</details>

### `overtime-wins`

**Since 2001-02 (through 2025-26), name a team that won a game that went to 2 or more overtimes.**

30 valid answers, difficulty **easy**, tiers: 1: 30 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Atlanta Hawks (1), Boston Celtics (1), Brooklyn Nets (1), Charlotte Hornets (1), Chicago Bulls (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Detroit Pistons (1), Golden State Warriors (1), Houston Rockets (1), Indiana Pacers (1), LA Clippers (1), Los Angeles Lakers (1), Memphis Grizzlies (1), Miami Heat (1), Milwaukee Bucks (1), Minnesota Timberwolves (1), New Orleans Pelicans (1), New York Knicks (1), Oklahoma City Thunder (1), Orlando Magic (1), Philadelphia 76ers (1), Phoenix Suns (1), Portland Trail Blazers (1), Sacramento Kings (1), San Antonio Spurs (1), Toronto Raptors (1), Utah Jazz (1), Washington Wizards (1)

</details>

**Since 2001-02 (through 2025-26), name a team that won a game that went to 3 or more overtimes.**

22 valid answers, difficulty **easy**, tiers: 1: 21, 4: 1 (1 at tier 4 or above).

Qualified only under a historical name: Charlotte Hornets.

<details><summary>All valid answers</summary>

Atlanta Hawks (1), Boston Celtics (1), Brooklyn Nets (1), Chicago Bulls (1), Denver Nuggets (1), Detroit Pistons (1), Golden State Warriors (1), Houston Rockets (1), Los Angeles Lakers (1), Memphis Grizzlies (1), Miami Heat (1), Milwaukee Bucks (1), New Orleans Pelicans (1), New York Knicks (1), Oklahoma City Thunder (1), Philadelphia 76ers (1), Portland Trail Blazers (1), Sacramento Kings (1), Toronto Raptors (1), Utah Jazz (1), Washington Wizards (1), Charlotte Hornets (4)

</details>

### `win-streak`

**Since 2001-02 (through 2025-26), name a team that won 14 or more regular-season games in a row.**

16 valid answers, difficulty **medium**, tiers: 1: 15, 4: 1 (1 at tier 4 or above).

Qualified only under a historical name: Brooklyn Nets.

<details><summary>All valid answers</summary>

Atlanta Hawks (1), Boston Celtics (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Golden State Warriors (1), Houston Rockets (1), LA Clippers (1), Miami Heat (1), Milwaukee Bucks (1), Oklahoma City Thunder (1), Philadelphia 76ers (1), Phoenix Suns (1), San Antonio Spurs (1), Toronto Raptors (1), Brooklyn Nets (4)

</details>

**Since 2001-02 (through 2025-26), name a team that won 16 or more regular-season games in a row.**

13 valid answers, difficulty **easy**, tiers: 1: 13 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Atlanta Hawks (1), Boston Celtics (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Golden State Warriors (1), Houston Rockets (1), LA Clippers (1), Miami Heat (1), Milwaukee Bucks (1), Oklahoma City Thunder (1), Philadelphia 76ers (1), Phoenix Suns (1), San Antonio Spurs (1)

</details>

**Since 2001-02 (through 2025-26), name a team that won 18 or more regular-season games in a row.**

8 valid answers, difficulty **medium**, tiers: 1: 8 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Atlanta Hawks (1), Boston Celtics (1), Golden State Warriors (1), Houston Rockets (1), Miami Heat (1), Milwaukee Bucks (1), Phoenix Suns (1), San Antonio Spurs (1)

</details>

### `champion`

**Since 2001-02 (through 2025-26), name a team that won the NBA championship.**

13 valid answers, difficulty **easy**, tiers: 1: 13 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Boston Celtics (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Detroit Pistons (1), Golden State Warriors (1), Los Angeles Lakers (1), Miami Heat (1), Milwaukee Bucks (1), New York Knicks (1), Oklahoma City Thunder (1), San Antonio Spurs (1), Toronto Raptors (1)

</details>

### `reached-finals`

**Since 2001-02 (through 2025-26), name a team that reached the NBA Finals.**

17 valid answers, difficulty **medium**, tiers: 1: 16, 4: 1 (1 at tier 4 or above).

Qualified only under a historical name: Brooklyn Nets.

<details><summary>All valid answers</summary>

Boston Celtics (1), Cleveland Cavaliers (1), Dallas Mavericks (1), Denver Nuggets (1), Detroit Pistons (1), Golden State Warriors (1), Indiana Pacers (1), Los Angeles Lakers (1), Miami Heat (1), Milwaukee Bucks (1), New York Knicks (1), Oklahoma City Thunder (1), Orlando Magic (1), Phoenix Suns (1), San Antonio Spurs (1), Toronto Raptors (1), Brooklyn Nets (4)

</details>
