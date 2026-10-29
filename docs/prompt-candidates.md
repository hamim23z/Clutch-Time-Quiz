# Prompt candidates

Written by `python3 pipeline/generate.py`; do not edit by hand.

- **Era wording:** every prompt starts with "Since 2001-02 (through 2025-26)". The data's season 2002 is the 2001-02 season (the first game is on 2001-10-30), so "Since 2002" would leave out three months of games. The schema requires the text to start with "Since" and four digits, which this does.
- **Valid answers:** players need 15 to 400; teams need at least 5.
- **Player tiers** come from the fame score (docs/fame-report.md). **Team tiers:** a team is tier 1 (10 points) if it qualified under its current name in any qualifying season, tier 4 (55 points) if only under a historical name. Every team answer is the franchise, shown by its current name; the other names it used are aliases for the answer matcher.
- **Difficulty:** from the number of valid answers and the share of tier 4 and above (see `difficulty()` in `pipeline/generator.py`).

## Totals

- Candidates: **72** (53 player, 19 team).
- Tried: 87 template and threshold combinations. Dropped for too few valid answers: 10. Dropped for too many: 5.
- By difficulty: easy 47, hard 4, medium 21.

Templates that produced no candidates: `triple-double-finals`.

## Candidates per template

| template | answers | thresholds tried | candidates | dropped: too few | dropped: too many |
|---|---|---|---|---|---|
| `points-regular` | player | 35, 40, 45, 50, 55, 60, 65 | 5 | 1 | 1 |
| `points-playoff` | player | 25, 30, 35, 40, 45, 50 | 6 | 0 | 0 |
| `points-finals` | player | 20, 25, 30, 35, 40 | 5 | 0 | 0 |
| `triple-double-regular` | player | - | 1 | 0 | 0 |
| `triple-double-playoff` | player | - | 1 | 0 | 0 |
| `triple-double-finals` | player | - | 0 | 1 | 0 |
| `rebounds` | player | 16, 18, 20, 22, 24, 25, 27 | 6 | 0 | 1 |
| `assists` | player | 14, 15, 16, 18, 20, 22 | 5 | 1 | 0 |
| `threes` | player | 8, 9, 10, 11, 12 | 4 | 1 | 0 |
| `blocks` | player | 6, 7, 8, 9, 10, 11 | 5 | 1 | 0 |
| `steals` | player | 5, 6, 7, 8, 9 | 3 | 1 | 1 |
| `ppg-season` | player | 20, 22, 24, 25, 26, 27, 28, 30, 32 | 8 | 1 | 0 |
| `franchises` | player | 4, 5, 6, 7, 8, 9 | 4 | 0 | 2 |
| `wins-season` | team | 50, 55, 58, 60, 62, 65, 67 | 6 | 1 | 0 |
| `wins-playoff` | team | 10, 12, 14, 15, 16 | 5 | 0 | 0 |
| `points-regulation` | team | 140, 145, 150, 155, 160 | 4 | 1 | 0 |
| `win-margin` | team | 40, 45, 50, 55, 60 | 4 | 1 | 0 |

## What was dropped

- `points-regular`: n=35: 422 answers (too many); n=65: 7 answers (too few)
- `triple-double-finals`: no threshold: 11 answers (too few)
- `rebounds`: n=16: 452 answers (too many)
- `assists`: n=22: 12 answers (too few)
- `threes`: n=12: 8 answers (too few)
- `blocks`: n=11: 7 answers (too few)
- `steals`: n=5: 707 answers (too many); n=9: 12 answers (too few)
- `ppg-season`: n=32: 9 answers (too few)
- `franchises`: n=4: 766 answers (too many); n=5: 493 answers (too many)
- `wins-season`: n=67: 4 answers (too few)
- `points-regulation`: n=160: 2 answers (too few)
- `win-margin`: n=60: 4 answers (too few)

## Player templates: examples

Three candidates per template, from the shortest list to the longest. Each answer is shown as name (tier).

### `points-regular`

**Since 2001-02 (through 2025-26), name a player who scored 60 or more points in a regular-season game.**

24 valid answers, difficulty **medium**, tiers: 1: 23, 2: 1 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kobe Bryant (1), Luka Doncic (1), Joel Embiid (1), Allen Iverson (1), Stephen Curry (1), Damian Lillard (1), Carmelo Anthony (1), Tracy McGrady (1), Bradley Beal (1), Giannis Antetokounmpo (1), Jayson Tatum (1), Nikola Jokic (1), Gilbert Arenas (1), Jalen Brunson (1), Kyrie Irving (1), Klay Thompson (1), Donovan Mitchell (1), Devin Booker (1), De'Aaron Fox (1), Karl-Anthony Towns (1), Kemba Walker (1), Bam Adebayo (2)

</details>

**Since 2001-02 (through 2025-26), name a player who scored 50 or more points in a regular-season game.**

93 valid answers, difficulty **easy**, tiers: 1: 67, 2: 23, 3: 2, 4: 1 (1 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Luka Doncic (1), Joel Embiid (1), Dirk Nowitzki (1), Allen Iverson (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Russell Westbrook (1), Damian Lillard (1), Carmelo Anthony (1), Tracy McGrady (1), DeMar DeRozan (1), Dwyane Wade (1), Paul Pierce (1), Tim Duncan (1), Bradley Beal (1), Giannis Antetokounmpo (1), Tony Parker (1), Jayson Tatum (1), Trae Young (1), Nikola Jokic (1), LaMarcus Aldridge (1), Gilbert Arenas (1), Vince Carter (1), Isaiah Thomas (1), Anthony Edwards (1), Anthony Davis (1), Jalen Brunson (1), Jaylen Brown (1), Kyrie Irving (1), Tyrese Maxey (1), Klay Thompson (1), Donovan Mitchell (1), Jamal Crawford (1), Kawhi Leonard (1), Devin Booker (1), Ray Allen (1), Jimmy Butler III (1), Ja Morant (1), Zach LaVine (1), Jrue Holiday (1), DeMarcus Cousins (1), CJ McCollum (1), Lauri Markkanen (1), Michael Redd (1), De'Aaron Fox (1), Karl-Anthony Towns (1), Kevin Love (1), Amar'e Stoudemire (1), Paolo Banchero (1), Kemba Walker (1), Jamal Murray (1), LaMelo Ball (1), Lou Williams (1), Julius Randle (1), Richard Hamilton (1), Derrick Rose (1), Victor Wembanyama (1), Kevin Martin (1), Blake Griffin (1), Jermaine O'Neal (1), Pascal Siakam (1), Deron Williams (1), Khris Middleton (1), Eric Gordon (2), Andre Miller (2), Rashard Lewis (2), Austin Reaves (2), John Wall (2), D'Angelo Russell (2), Michael Jordan (2), Brandon Roy (2), Allan Houston (2), Darius Garland (2), Jamal Mashburn (2), Bam Adebayo (2), Shareef Abdur-Rahim (2), Mo Williams (2), Aaron Gordon (2), Cooper Flagg (2), Fred VanVleet (2), Caris LeVert (2), T.J. Warren (2), Kevin Porter Jr. (2), Brandon Jennings (2), Terrence Ross (2), Saddiq Bey (2), Corey Brewer (2008-2020) (3), Damon Stoudamire (3), Malachi Flynn (4)

</details>

**Since 2001-02 (through 2025-26), name a player who scored 40 or more points in a regular-season game.**

263 valid answers, difficulty **easy**, tiers: 1: 103, 2: 116, 3: 40, 4: 3, 5: 1 (4 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Luka Doncic (1), Joel Embiid (1), Dirk Nowitzki (1), Allen Iverson (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Russell Westbrook (1), Damian Lillard (1), Carmelo Anthony (1), Tracy McGrady (1), DeMar DeRozan (1), Dwyane Wade (1), Chris Paul (1), Paul Pierce (1), Tim Duncan (1), Bradley Beal (1), Giannis Antetokounmpo (1), Tony Parker (1), Jayson Tatum (1), Pau Gasol (1), Trae Young (1), Joe Johnson (1), Nikola Jokic (1), LaMarcus Aldridge (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Isaiah Thomas (1), Dwight Howard (1), Anthony Edwards (1), Anthony Davis (1), Jalen Brunson (1), Jaylen Brown (1), Kyrie Irving (1), Tyrese Maxey (1), Klay Thompson (1), Donovan Mitchell (1), Jamal Crawford (1), Kevin Garnett (1), Zach Randolph (1), Kawhi Leonard (1), Devin Booker (1), Ray Allen (1), Shaquille O'Neal (1), Jimmy Butler III (1), Ja Morant (1), Zach LaVine (1), Jrue Holiday (1), Chris Bosh (1), Zion Williamson (1), DeMarcus Cousins (1), Jason Terry (1), CJ McCollum (1), Lauri Markkanen (1), Mike Conley (1), Michael Redd (1), Kyle Lowry (1), De'Aaron Fox (1), Nikola Vucevic (1), Rudy Gay (1), Cade Cunningham (1), Karl-Anthony Towns (1), Kevin Love (1), Amar'e Stoudemire (1), Antawn Jamison (1), Paolo Banchero (1), Danny Granger (1), Kemba Walker (1), Monta Ellis (1), Shawn Marion (1), Manu Ginobili (1), Jamal Murray (1), LaMelo Ball (1), Lou Williams (1), Julius Randle (1), Steve Nash (1), Richard Jefferson (1), Yao Ming (1), Richard Hamilton (1), Derrick Rose (1), Victor Wembanyama (1), Paul Millsap (1), Elton Brand (1), Brandon Ingram (1), Kevin Martin (1), Andrew Wiggins (1), Blake Griffin (1), Collin Sexton (1), Carlos Boozer (1), Jermaine O'Neal (1), Peja Stojakovic (1), Jeff Green (1), Pascal Siakam (1), David West (1), Deni Avdija (1), Jason Richardson (1), Deron Williams (1), Khris Middleton (1), Tyler Herro (1), Eric Gordon (2), Desmond Bane (2), Keyonte George (2), Andre Miller (2), Rashard Lewis (2), Al Jefferson (2), Austin Reaves (2), Kristaps Porzingis (2), Luol Deng (2), John Wall (2), Victor Oladipo (2), Marc Gasol (2), D'Angelo Russell (2), Michael Jordan (2), JR Smith (2), Baron Davis (2), Dennis Schroder (2), Goran Dragic (2), Brandon Roy (2), Anfernee Simons (2), Jordan Clarkson (2), Stephen Jackson (2), Jaren Jackson Jr. (2), JJ Redick (2), Jalen Johnson (2), Allan Houston (2), Caron Butler (2), Dejounte Murray (2), Gordon Hayward (2), Cam Thomas (2), Karl Malone (2), Mike Bibby (2), Jerami Grant (2), Tim Hardaway Jr. (2), Stephon Marbury (2), Al Harrington (2), Trevor Ariza (2), Kyle Kuzma (2), Antoine Walker (2), Jalen Rose (2), Jalen Green (2), Gary Payton (2), Larry Hughes (2), Jason Kidd (2), Danilo Gallinari (2), Norman Powell (2), Cuttino Mobley (2), Darius Garland (2), Steve Francis (2), Jamal Mashburn (2), Bojan Bogdanovic (2), Jalen Williams (2), Reggie Jackson (2), Jerry Stackhouse (2), Bam Adebayo (2), Trey Murphy III (2), Ben Gordon (2), Andrea Bargnani (2), Devin Harris (2), Shareef Abdur-Rahim (2), Alperen Sengun (2), Mo Williams (2), Terry Rozier (2), Buddy Hield (2), RJ Barrett (2), Aaron Gordon (2), Eric Bledsoe (2), Cooper Flagg (2), Miles Bridges (2), Domantas Sabonis (2), Myles Turner (2), Nickeil Alexander-Walker (2), Mikal Bridges (2), Mike Miller (2), Tyrese Haliburton (2), Michael Finley (2), Spencer Dinwiddie (2), Ricky Davis (2), Gerald Wallace (2), Jordan Poole (2), Coby White (2), Leandro Barbosa (2), Fred VanVleet (2), Kelly Oubre Jr. (2), Evan Fournier (2), Dillon Brooks (2), Caris LeVert (2), Tyreke Evans (2), Josh Howard (2), Luis Scola (2), T.J. Warren (2), Mehmet Okur (2), Aaron Brooks (2), Eddy Curry (2), Derrick White (2), Latrell Sprewell (2), Michael Beasley (2), Kevin Porter Jr. (2), Jarrett Allen (2), Brandon Jennings (2), Wally Szczerbiak (2), Andrew Bynum (2), Marcus Thornton (2), OG Anunoby (2), Evan Mobley (2), CJ Miles (2), Rodney Stuckey (2), O.J. Mayo (2), Arron Afflalo (2), Terrence Ross (2), Nick Van Exel (2), Gary Trent Jr. (2), Nick Young (2), Amen Thompson (2), Devonte' Graham (2), Saddiq Bey (2), Quentin Richardson (3), Bogdan Bogdanovic (3), Luguentz Dort (3), Nate Robinson (3), Malik Monk (3), Payton Pritchard (3), Corey Brewer (2008-2020) (3), Immanuel Quickley (3), Ramon Sessions (3), Ben Simmons (3), Stephon Castle (3), Lamond Murray (3), Josh Hart (3), Grayson Allen (3), Robert Covington (3), Charlie Villanueva (3), Gerald Green (3), Matas Buzelis (3), Damon Stoudamire (3), Austin Rivers (3), Jodie Meeks (3), P.J. Washington (3), Donte DiVincenzo (3), Jaime Jaquez Jr. (3), Keegan Murray (3), Brice Sensabaugh (3), Jordan Crawford (3), GG Jackson (3), Quentin Grimes (3), Jeremiah Fears (3), Anthony Morrow (3), Darius Miles (3), Trey Burke (3), C.J. Watson (3), Allen Crabbe (3), Pat Connaughton (3), Obi Toppin (3), Linas Kleiza (3), Damien Wilkins (3), Aaron Wiggins (3), Talen Horton-Tucker (4), Rodrigue Beaubois (4), Malachi Flynn (4), Kenneth Lofton Jr. (5)

</details>

### `points-playoff`

**Since 2001-02 (through 2025-26), name a player who scored 50 or more points in a playoff game.**

17 valid answers, difficulty **medium**, tiers: 1: 17 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), Kevin Durant (1), Kobe Bryant (1), Joel Embiid (1), Dirk Nowitzki (1), Allen Iverson (1), Stephen Curry (1), Russell Westbrook (1), Damian Lillard (1), Giannis Antetokounmpo (1), Jayson Tatum (1), Nikola Jokic (1), Isaiah Thomas (1), Donovan Mitchell (1), Ray Allen (1), Jimmy Butler III (1), Jamal Murray (1)

</details>

**Since 2001-02 (through 2025-26), name a player who scored 40 or more points in a playoff game.**

73 valid answers, difficulty **easy**, tiers: 1: 61, 2: 9, 3: 3 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Luka Doncic (1), Joel Embiid (1), Dirk Nowitzki (1), Allen Iverson (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Russell Westbrook (1), Damian Lillard (1), Carmelo Anthony (1), Tracy McGrady (1), DeMar DeRozan (1), Dwyane Wade (1), Chris Paul (1), Paul Pierce (1), Tim Duncan (1), Giannis Antetokounmpo (1), Tony Parker (1), Jayson Tatum (1), Trae Young (1), Nikola Jokic (1), LaMarcus Aldridge (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Isaiah Thomas (1), Dwight Howard (1), Anthony Edwards (1), Anthony Davis (1), Jalen Brunson (1), Jaylen Brown (1), Kyrie Irving (1), Tyrese Maxey (1), Klay Thompson (1), Donovan Mitchell (1), Kawhi Leonard (1), Devin Booker (1), Ray Allen (1), Shaquille O'Neal (1), Jimmy Butler III (1), Ja Morant (1), Jrue Holiday (1), CJ McCollum (1), Michael Redd (1), Cade Cunningham (1), Amar'e Stoudemire (1), Paolo Banchero (1), Jamal Murray (1), Steve Nash (1), Richard Hamilton (1), Derrick Rose (1), Victor Wembanyama (1), Paul Millsap (1), Elton Brand (1), Chauncey Billups (1), Carlos Boozer (1), Jason Richardson (1), Khris Middleton (1), John Wall (2), Brandon Roy (2), Gordon Hayward (2), Norman Powell (2), Jalen Williams (2), Ben Gordon (2), Rajon Rondo (2), Sam Cassell (2), Nick Van Exel (2), Bonzi Wells (3), Ayo Dosunmu (3), Anthony Johnson (3)

</details>

**Since 2001-02 (through 2025-26), name a player who scored 25 or more points in a playoff game.**

330 valid answers, difficulty **easy**, tiers: 1: 105, 2: 128, 3: 90, 4: 7 (7 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Luka Doncic (1), Joel Embiid (1), Dirk Nowitzki (1), Allen Iverson (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Russell Westbrook (1), Damian Lillard (1), Carmelo Anthony (1), Tracy McGrady (1), DeMar DeRozan (1), Dwyane Wade (1), Chris Paul (1), Paul Pierce (1), Tim Duncan (1), Bradley Beal (1), Giannis Antetokounmpo (1), Tony Parker (1), Jayson Tatum (1), Pau Gasol (1), Trae Young (1), Joe Johnson (1), Nikola Jokic (1), LaMarcus Aldridge (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Isaiah Thomas (1), Dwight Howard (1), Anthony Edwards (1), Anthony Davis (1), Jalen Brunson (1), Jaylen Brown (1), Kyrie Irving (1), Tyrese Maxey (1), Klay Thompson (1), Donovan Mitchell (1), Jamal Crawford (1), Kevin Garnett (1), Zach Randolph (1), Kawhi Leonard (1), Devin Booker (1), Ray Allen (1), Shaquille O'Neal (1), Brook Lopez (1), Jimmy Butler III (1), Ja Morant (1), Jrue Holiday (1), Chris Bosh (1), Jason Terry (1), CJ McCollum (1), Mike Conley (1), Michael Redd (1), Kyle Lowry (1), De'Aaron Fox (1), Nikola Vucevic (1), Tobias Harris (1), Cade Cunningham (1), Karl-Anthony Towns (1), Kevin Love (1), Amar'e Stoudemire (1), Antawn Jamison (1), Paolo Banchero (1), Danny Granger (1), Al Horford (1), Kemba Walker (1), Monta Ellis (1), Shawn Marion (1), Manu Ginobili (1), Jamal Murray (1), Lou Williams (1), Julius Randle (1), Steve Nash (1), Richard Jefferson (1), Yao Ming (1), Richard Hamilton (1), Derrick Rose (1), Victor Wembanyama (1), Paul Millsap (1), Elton Brand (1), Chauncey Billups (1), Brandon Ingram (1), Kevin Martin (1), Andrew Wiggins (1), Blake Griffin (1), Chris Webber (1), Andre Iguodala (1), Carlos Boozer (1), Jermaine O'Neal (1), Harrison Barnes (1), Peja Stojakovic (1), Jeff Green (1), Pascal Siakam (1), David West (1), Deni Avdija (1), Jason Richardson (1), Michael Porter Jr. (1), Deron Williams (1), Franz Wagner (1), Khris Middleton (1), Tyler Herro (1), Eric Gordon (2), Desmond Bane (2), Andre Miller (2), Rashard Lewis (2), Al Jefferson (2), Austin Reaves (2), Kristaps Porzingis (2), Luol Deng (2), John Wall (2), Victor Oladipo (2), Josh Smith (2), Marc Gasol (2), D'Angelo Russell (2), JR Smith (2), Jonas Valanciunas (2), Baron Davis (2), Dennis Schroder (2), Goran Dragic (2), Brandon Roy (2), Jordan Clarkson (2), Stephen Jackson (2), Jaren Jackson Jr. (2), JJ Redick (2), Caron Butler (2), Dejounte Murray (2), Gordon Hayward (2), Karl Malone (2), Mike Bibby (2), Tayshaun Prince (2), Jerami Grant (2), Tim Hardaway Jr. (2), Stephon Marbury (2), Trevor Ariza (2), Serge Ibaka (2), Corey Maggette (2), Antoine Walker (2), Metta World Peace (2), Jalen Green (2), Rudy Gobert (2), Gary Payton (2), Larry Hughes (2), Jason Kidd (2), Danilo Gallinari (2), Nicolas Batum (2), Norman Powell (2), Darius Garland (2), Steve Francis (2), Jamal Mashburn (2), Bojan Bogdanovic (2), Jalen Williams (2), Wesley Matthews (2), Reggie Jackson (2), Nene (2), Jerry Stackhouse (2), Bam Adebayo (2), Ben Gordon (2), Hedo Turkoglu (2), Lamar Odom (2), Devin Harris (2), Shareef Abdur-Rahim (2), Rasheed Wallace (2), Malcolm Brogdon (2), Alperen Sengun (2), Terry Rozier (2), Buddy Hield (2), Raymond Felton (2), RJ Barrett (2), Mike Dunleavy (2), Aaron Gordon (2), Eric Bledsoe (2), George Hill (2), Jeff Teague (2), Rajon Rondo (2), Marcus Morris Sr. (2), Myles Turner (2), Jameer Nelson (2), Mikal Bridges (2), Tyrese Haliburton (2), Kirk Hinrich (2), Michael Finley (2), Spencer Dinwiddie (2), Boris Diaw (2), Gerald Wallace (2), Jordan Poole (2), Draymond Green (2), DeAndre Jordan (2), Leandro Barbosa (2), Kenyon Martin (2), Fred VanVleet (2), Dillon Brooks (2), Caris LeVert (2), Jarrett Jack (2), D.J. Augustin (2), Bobby Portis (2), Josh Howard (2), Scottie Barnes (2), Sam Cassell (2), Taj Gibson (2), Aaron Brooks (2), Clint Capela (2), Marco Belinelli (2), Derrick White (2), Latrell Sprewell (2), Marcus Smart (2), Enes Freedom (2), Brandon Jennings (2), Kelly Olynyk (2), Wally Szczerbiak (2), Jae Crowder (2), Alec Burks (2), Cameron Johnson (2), Andrew Bynum (2), John Salmons (2), Danny Green (2), Montrezl Harrell (2), OG Anunoby (2), Evan Mobley (2), Marcin Gortat (2), Eddie Jones (2), Nick Van Exel (2), Gary Trent Jr. (2), Amen Thompson (2), Deandre Ayton (2), Ryan Anderson (2), Matt Barnes (2), Jose Calderon (2), Channing Frye (2), Will Barton (2), Ty Lawson (3), Bennedict Mathurin (3), Bogdan Bogdanovic (3), Avery Bradley (3), Luguentz Dort (3), Ricky Rubio (3), Nate Robinson (3), Malik Monk (3), Chet Holmgren (3), Payton Pritchard (3), Raja Bell (3), De'Andre Hunter (3), Bonzi Wells (3), Andrew Nembhard (3), Ben Simmons (3), Roy Hibbert (3), Ivica Zubac (3), Rafer Alston (3), Stephon Castle (3), Brandon Bass (3), Chandler Parsons (3), Josh Hart (3), Reggie Miller (3), Grayson Allen (3), Tim Thomas (3), Kevin Huerter (3), Mario Chalmers (3), Keith Van Horn (3), Jonathan Kuminga (3), VJ Edgecombe (3), Duncan Robinson (3), Joakim Noah (3), Austin Rivers (3), P.J. Washington (3), Nikola Mirotic (3), Donte DiVincenzo (3), Joe Ingles (3), Seth Curry (3), Bobby Jackson (3), T.J. Ford (3), Al-Farouq Aminu (3), Jaden McDaniels (3), Ben Wallace (3), Ayo Dosunmu (3), Donyell Marshall (3), Earl Boykins (3), DeMarre Carroll (3), Andres Nocioni (3), Rodney Hood (3), Rui Hachimura (3), Dario Saric (3), Clifford Robinson (3), Joe Harris (3), Luke Kennard (3), Antonio Davis (3), Voshon Lenard (3), Lance Stephenson (3), Eddie House (3), Troy Hudson (3), Antonio McDyess (3), Scoot Henderson (3), Bruce Brown (3), Elden Campbell (3), Brandin Podziemski (3), Aaron Nesmith (3), Chris Boucher (3), Trey Burke (3), Bruce Bowen (3), Glen Davis (3), Ajay Mitchell (3), Nenad Krstic (3), Anthony Parker (3), Monte Morris (3), Cameron Payne (3), James Jones (3), Terance Mann (3), Ty Jerome (3), Malik Rose (3), Damon Jones (3), Juan Dixon (3), Alex Caruso (3), Anthony Johnson (3), Moses Moody (3), Miles McBride (3), Dylan Harper (3), Daniel Gibson (3), Jannero Pargo (3), Steve Smith (3), Timofey Mozgov (3), Grant Williams (3), Caleb Martin (4), Maxi Kleber (4), Mikki Moore (4), Gabe Vincent (4), Meyers Leonard (4), Scotty Pippen Jr. (4), Timothe Luwawu-Cabarrot (4)

</details>

### `points-finals`

**Since 2001-02 (through 2025-26), name a player who scored 40 or more points in a Finals game.**

15 valid answers, difficulty **medium**, tiers: 1: 14, 2: 1 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), Kevin Durant (1), Kobe Bryant (1), Stephen Curry (1), Russell Westbrook (1), Dwyane Wade (1), Giannis Antetokounmpo (1), Nikola Jokic (1), Jalen Brunson (1), Kyrie Irving (1), Devin Booker (1), Shaquille O'Neal (1), Jimmy Butler III (1), Khris Middleton (1), Jalen Williams (2)

</details>

**Since 2001-02 (through 2025-26), name a player who scored 30 or more points in a Finals game.**

39 valid answers, difficulty **medium**, tiers: 1: 33, 2: 6 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), Kevin Durant (1), Kobe Bryant (1), Luka Doncic (1), Dirk Nowitzki (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Russell Westbrook (1), Dwyane Wade (1), Chris Paul (1), Paul Pierce (1), Tim Duncan (1), Giannis Antetokounmpo (1), Tony Parker (1), Jayson Tatum (1), Nikola Jokic (1), Anthony Davis (1), Jalen Brunson (1), Jaylen Brown (1), Kyrie Irving (1), Klay Thompson (1), Kawhi Leonard (1), Devin Booker (1), Ray Allen (1), Shaquille O'Neal (1), Jimmy Butler III (1), Jason Terry (1), Jamal Murray (1), Richard Hamilton (1), Victor Wembanyama (1), Chauncey Billups (1), Pascal Siakam (1), Khris Middleton (1), Rashard Lewis (2), Jason Kidd (2), Jalen Williams (2), Draymond Green (2), Kenyon Martin (2), OG Anunoby (2)

</details>

**Since 2001-02 (through 2025-26), name a player who scored 20 or more points in a Finals game.**

98 valid answers, difficulty **easy**, tiers: 1: 49, 2: 29, 3: 15, 4: 5 (5 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Luka Doncic (1), Dirk Nowitzki (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Russell Westbrook (1), Dwyane Wade (1), Chris Paul (1), Paul Pierce (1), Tim Duncan (1), Giannis Antetokounmpo (1), Tony Parker (1), Jayson Tatum (1), Pau Gasol (1), Nikola Jokic (1), Dwight Howard (1), Anthony Davis (1), Jalen Brunson (1), Jaylen Brown (1), Kyrie Irving (1), Klay Thompson (1), Kevin Garnett (1), Kawhi Leonard (1), Devin Booker (1), Ray Allen (1), Shaquille O'Neal (1), Jimmy Butler III (1), Jrue Holiday (1), Chris Bosh (1), Jason Terry (1), Kyle Lowry (1), De'Aaron Fox (1), Karl-Anthony Towns (1), Kevin Love (1), Al Horford (1), Shawn Marion (1), Manu Ginobili (1), Jamal Murray (1), Richard Hamilton (1), Victor Wembanyama (1), Chauncey Billups (1), Andrew Wiggins (1), Andre Iguodala (1), Pascal Siakam (1), Khris Middleton (1), Tyler Herro (1), Rashard Lewis (2), Kristaps Porzingis (2), Marc Gasol (2), JR Smith (2), Serge Ibaka (2), Antoine Walker (2), Metta World Peace (2), Jason Kidd (2), Jalen Williams (2), Bam Adebayo (2), Hedo Turkoglu (2), Lamar Odom (2), Rasheed Wallace (2), Aaron Gordon (2), Rajon Rondo (2), Mikal Bridges (2), Mike Miller (2), Tyrese Haliburton (2), Draymond Green (2), Kenyon Martin (2), Fred VanVleet (2), Josh Howard (2), Derrick White (2), Marcus Smart (2), Kelly Olynyk (2), Andrew Bynum (2), Danny Green (2), OG Anunoby (2), Deandre Ayton (2), Bennedict Mathurin (3), Chet Holmgren (3), Rafer Alston (3), Stephon Castle (3), Mario Chalmers (3), Duncan Robinson (3), Shaun Livingston (3), Bruce Brown (3), Kerry Kittles (3), Obi Toppin (3), Gary Neal (3), Alex Caruso (3), Dylan Harper (3), Sasha Vujacic (3), Timofey Mozgov (3), Robert Horry (4), Matthew Dellavedova (4), Gabe Vincent (4), Lucious Harris (4), Leon Powe (4)

</details>

### `triple-double-regular`

**Since 2001-02 (through 2025-26), name a player who recorded a triple-double in a regular-season game.**

248 valid answers, difficulty **easy**, tiers: 1: 80, 2: 77, 3: 61, 4: 22, 5: 7, 6: 1 (30 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Luka Doncic (1), Joel Embiid (1), Dirk Nowitzki (1), Allen Iverson (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Russell Westbrook (1), Damian Lillard (1), Carmelo Anthony (1), Tracy McGrady (1), DeMar DeRozan (1), Dwyane Wade (1), Chris Paul (1), Paul Pierce (1), Tim Duncan (1), Bradley Beal (1), Giannis Antetokounmpo (1), Tony Parker (1), Jayson Tatum (1), Pau Gasol (1), Trae Young (1), Joe Johnson (1), Nikola Jokic (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Isaiah Thomas (1), Dwight Howard (1), Anthony Davis (1), Jaylen Brown (1), Kyrie Irving (1), Tyrese Maxey (1), Kevin Garnett (1), Zach Randolph (1), Kawhi Leonard (1), Ray Allen (1), Jimmy Butler III (1), Ja Morant (1), Jrue Holiday (1), Zion Williamson (1), DeMarcus Cousins (1), Jason Terry (1), CJ McCollum (1), Kyle Lowry (1), De'Aaron Fox (1), Nikola Vucevic (1), Tobias Harris (1), Cade Cunningham (1), Karl-Anthony Towns (1), Kevin Love (1), Paolo Banchero (1), Al Horford (1), Kemba Walker (1), Jamal Murray (1), LaMelo Ball (1), Lou Williams (1), Julius Randle (1), Steve Nash (1), Richard Jefferson (1), Derrick Rose (1), Victor Wembanyama (1), Paul Millsap (1), Elton Brand (1), Chauncey Billups (1), Brandon Ingram (1), Andrew Wiggins (1), Blake Griffin (1), Chris Webber (1), Andre Iguodala (1), Carlos Boozer (1), Jermaine O'Neal (1), Pascal Siakam (1), David West (1), Deni Avdija (1), Khris Middleton (1), Tyler Herro (1), Desmond Bane (2), Andre Miller (2), Austin Reaves (2), John Wall (2), Victor Oladipo (2), Josh Smith (2), Marc Gasol (2), D'Angelo Russell (2), Jonas Valanciunas (2), Baron Davis (2), Goran Dragic (2), Brandon Roy (2), Jordan Clarkson (2), Stephen Jackson (2), Jalen Johnson (2), Caron Butler (2), Dejounte Murray (2), Karl Malone (2), Mike Bibby (2), Trevor Ariza (2), Kyle Kuzma (2), Serge Ibaka (2), Antoine Walker (2), Jalen Rose (2), Jalen Green (2), Gary Payton (2), Larry Hughes (2), Jason Kidd (2), Nicolas Batum (2), Darius Garland (2), Steve Francis (2), Jamal Mashburn (2), Reggie Jackson (2), Bam Adebayo (2), Hedo Turkoglu (2), Lamar Odom (2), Malcolm Brogdon (2), David Lee (2), Alperen Sengun (2), Mo Williams (2), Terry Rozier (2), Raymond Felton (2), RJ Barrett (2), Aaron Gordon (2), Eric Bledsoe (2), George Hill (2), Miles Bridges (2), Rajon Rondo (2), Domantas Sabonis (2), Mike Miller (2), Tyrese Haliburton (2), Kirk Hinrich (2), Spencer Dinwiddie (2), Boris Diaw (2), Draymond Green (2), Fred VanVleet (2), Andrei Kirilenko (2), Caris LeVert (2), Tyreke Evans (2), Jarrett Jack (2), Darren Collison (2), Scottie Barnes (2), Drew Gooden (2), Sam Cassell (2), Brad Miller (2), Brandon Knight (2), Clint Capela (2), Derrick White (2), Latrell Sprewell (2), Marcus Smart (2), Kevin Porter Jr. (2), Brandon Jennings (2), Greg Monroe (2), John Salmons (2), Amen Thompson (2), Matt Barnes (2), Jose Calderon (2), Ty Lawson (3), J.J. Barea (3), Ricky Rubio (3), Jusuf Nurkic (3), Payton Pritchard (3), Josh Giddey (3), Steven Adams (3), Hassan Whiteside (3), Immanuel Quickley (3), Ramon Sessions (3), Ben Simmons (3), JaVale McGee (3), Evan Turner (3), Roy Hibbert (3), Ivica Zubac (3), Mason Plumlee (3), Beno Udrih (3), Michael Carter-Williams (3), Rafer Alston (3), Stephon Castle (3), Josh Hart (3), James Posey (3), Damon Stoudamire (3), Joakim Noah (3), T.J. McConnell (3), Jamaal Tinsley (3), Jaime Jaquez Jr. (3), Marcus Camby (3), Dennis Smith Jr. (3), Steve Blake (3), Ben Wallace (3), Jeremy Lin (3), Ayo Dosunmu (3), Jordan Crawford (3), Earl Watson (3), Tyus Jones (3), Lonzo Ball (3), Kyle Anderson (3), Luke Kennard (3), Royce O'Neale (3), Lance Stephenson (3), Dyson Daniels (3), Kenny Thomas (3), Tre Jones (3), Bruce Brown (3), Elfrid Payton (3), Markelle Fultz (3), Greivis Vasquez (3), Jalen Suggs (3), Ryan Gomes (3), Charlie Bell (3), Tony Wroten (3), Eric Snow (3), Max Strus (3), Nic Claxton (3), Chris Duhon (3), Delon Wright (3), Bilal Coulibaly (3), Anfernee Hardaway (3), Isaiah Hartenstein (3), Derik Queen (3), Dikembe Mutombo (4), Vlade Divac (4), Tomas Satoransky (4), Bob Sura (4), Tre Mann (4), Shabazz Napier (4), Robert Williams III (4), Chuck Hayes (4), Trendon Watford (4), Mario Hezonja (4), Larry Sanders (4), Scotty Pippen Jr. (4), Jay Williams (4), Rodney White (4), John Konchar (4), Terrence Williams (4), Mark Jackson (4), Jaylin Williams (4), Tim Frazier (4), Aleksej Pokusevski (4), Jericho Sims (4), Jonathan Mogbo (4), Rayan Rupert (5), Jalen Pickett (5), Keaton Wallace (5), Theo Pinson (5), Ben Uzoh (5), Jahmai Mashack (5), Bez Mbeng (5), Lachlan Olbrich (6)

</details>

### `triple-double-playoff`

**Since 2001-02 (through 2025-26), name a player who recorded a triple-double in a playoff game.**

42 valid answers, difficulty **easy**, tiers: 1: 28, 2: 11, 3: 3 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Luka Doncic (1), Joel Embiid (1), Stephen Curry (1), Russell Westbrook (1), Chris Paul (1), Paul Pierce (1), Tim Duncan (1), Giannis Antetokounmpo (1), Jayson Tatum (1), Pau Gasol (1), Nikola Jokic (1), Paul George (1), Kevin Garnett (1), Devin Booker (1), Jimmy Butler III (1), Ja Morant (1), Jrue Holiday (1), Cade Cunningham (1), Karl-Anthony Towns (1), Jamal Murray (1), Julius Randle (1), Steve Nash (1), Victor Wembanyama (1), Blake Griffin (1), Chris Webber (1), Victor Oladipo (2), Baron Davis (2), Gary Payton (2), Jason Kidd (2), Steve Francis (2), Bam Adebayo (2), Rajon Rondo (2), Tyrese Haliburton (2), Draymond Green (2), Marcus Smart (2), Andrew Bynum (2), Ricky Rubio (3), Ben Simmons (3), Josh Hart (3)

</details>

### `triple-double-finals`

No candidates: every threshold gave too few or too many valid answers (see above).

### `rebounds`

**Since 2001-02 (through 2025-26), name a player who grabbed 27 or more rebounds in a game.**

19 valid answers, difficulty **medium**, tiers: 1: 6, 2: 7, 3: 6 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

Tim Duncan (1), Nikola Jokic (1), Dwight Howard (1), Nikola Vucevic (1), Karl-Anthony Towns (1), Kevin Love (1), Rudy Gobert (2), Andre Drummond (2), Domantas Sabonis (2), DeAndre Jordan (2), Tyson Chandler (2), Enes Freedom (2), Andrew Bynum (2), Jusuf Nurkic (3), Ivica Zubac (3), Andrew Bogut (3), Marcus Camby (3), Ben Wallace (3), Timofey Mozgov (3)

</details>

**Since 2001-02 (through 2025-26), name a player who grabbed 24 or more rebounds in a game.**

52 valid answers, difficulty **easy**, tiers: 1: 15, 2: 14, 3: 20, 4: 3 (3 at tier 4 or above).

<details><summary>All valid answers</summary>

Tim Duncan (1), Nikola Jokic (1), LaMarcus Aldridge (1), Dwight Howard (1), Anthony Davis (1), Kevin Garnett (1), Zach Randolph (1), Shaquille O'Neal (1), DeMarcus Cousins (1), Nikola Vucevic (1), Karl-Anthony Towns (1), Kevin Love (1), Shawn Marion (1), Victor Wembanyama (1), Paul Millsap (1), Al Jefferson (2), Jonas Valanciunas (2), Rudy Gobert (2), Andre Drummond (2), John Collins (2), Domantas Sabonis (2), DeAndre Jordan (2), Tyson Chandler (2), Scottie Barnes (2), Clint Capela (2), Enes Freedom (2), Ersan Ilyasova (2), Jarrett Allen (2), Andrew Bynum (2), Jusuf Nurkic (3), Hassan Whiteside (3), Emeka Okafor (3), Ivica Zubac (3), Andrew Bogut (3), Marcus Camby (3), Mark Williams (3), Ben Wallace (3), Donyell Marshall (3), Kenneth Faried (3), Erick Dampier (3), Chris Wilcox (3), JJ Hickson (3), Anderson Varejao (3), Bismack Biyombo (3), Lorenzen Wright (3), Andris Biedrins (3), Reggie Evans (3), John Henson (3), Timofey Mozgov (3), Walker Kessler (4), Joel Przybilla (4), Clarence Weatherspoon (4)

</details>

**Since 2001-02 (through 2025-26), name a player who grabbed 18 or more rebounds in a game.**

290 valid answers, difficulty **medium**, tiers: 1: 48, 2: 66, 3: 99, 4: 64, 5: 11, 6: 2 (77 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), Kevin Durant (1), Luka Doncic (1), Joel Embiid (1), Dirk Nowitzki (1), Shai Gilgeous-Alexander (1), Russell Westbrook (1), Damian Lillard (1), Carmelo Anthony (1), Paul Pierce (1), Tim Duncan (1), Giannis Antetokounmpo (1), Jayson Tatum (1), Pau Gasol (1), Nikola Jokic (1), LaMarcus Aldridge (1), Dwight Howard (1), Anthony Davis (1), Kevin Garnett (1), Zach Randolph (1), Shaquille O'Neal (1), Brook Lopez (1), Jimmy Butler III (1), Chris Bosh (1), DeMarcus Cousins (1), Lauri Markkanen (1), Nikola Vucevic (1), Tobias Harris (1), Karl-Anthony Towns (1), Kevin Love (1), Amar'e Stoudemire (1), Antawn Jamison (1), Paolo Banchero (1), Al Horford (1), Shawn Marion (1), Julius Randle (1), Richard Jefferson (1), Yao Ming (1), Victor Wembanyama (1), Paul Millsap (1), Elton Brand (1), Blake Griffin (1), Chris Webber (1), Carlos Boozer (1), Jermaine O'Neal (1), Pascal Siakam (1), David West (1), Deni Avdija (1), Rashard Lewis (2), Al Jefferson (2), Kristaps Porzingis (2), Luol Deng (2), Josh Smith (2), Marc Gasol (2), Jonas Valanciunas (2), Jalen Johnson (2), Caron Butler (2), Karl Malone (2), Al Harrington (2), Kyle Kuzma (2), Serge Ibaka (2), Corey Maggette (2), Antoine Walker (2), Rudy Gobert (2), Jason Kidd (2), Keldon Johnson (2), Danilo Gallinari (2), Nicolas Batum (2), Andre Drummond (2), John Collins (2), Bam Adebayo (2), Hedo Turkoglu (2), Lamar Odom (2), Shareef Abdur-Rahim (2), David Lee (2), Alperen Sengun (2), Marvin Williams (2), Mike Dunleavy (2), Rajon Rondo (2), Christian Wood (2), Domantas Sabonis (2), Mike Miller (2), Zydrunas Ilgauskas (2), Gerald Wallace (2), Draymond Green (2), DeAndre Jordan (2), Tyson Chandler (2), Kenyon Martin (2), Andrei Kirilenko (2), Bobby Portis (2), Josh Howard (2), Luis Scola (2), Scottie Barnes (2), Drew Gooden (2), Mehmet Okur (2), Brad Miller (2), Taj Gibson (2), Clint Capela (2), Jalen Duren (2), Enes Freedom (2), Ersan Ilyasova (2), Jarrett Allen (2), Derrick Favors (2), Kelly Olynyk (2), Robin Lopez (2), Andrew Bynum (2), Greg Monroe (2), Montrezl Harrell (2), Evan Mobley (2), Marcin Gortat (2), Chris Kaman (2), Amen Thompson (2), Deandre Ayton (2), Ryan Anderson (2), Troy Murphy (3), Matt Harpring (3), Nikola Pekovic (3), Zaza Pachulia (3), Jusuf Nurkic (3), Chet Holmgren (3), Tristan Thompson (3), Josh Giddey (3), Corey Brewer (2008-2020) (3), Steven Adams (3), Hassan Whiteside (3), Emeka Okafor (3), Bonzi Wells (3), Udonis Haslem (3), Ben Simmons (3), JaVale McGee (3), Andray Blatche (3), Roy Hibbert (3), Ivica Zubac (3), Mason Plumlee (3), Andrew Bogut (3), Samuel Dalembert (3), Josh Hart (3), Charlie Villanueva (3), Dorell Wright (3), Jared Dudley (3), P.J. Tucker (3), Keith Van Horn (3), Kurt Thomas (3), James Posey (3), Jabari Smith Jr. (3), Joakim Noah (3), Alonzo Mourning (3), P.J. Washington (3), Amir Johnson (3), Naz Reid (3), Marcus Camby (3), Mark Williams (3), Wendell Carter Jr. (3), Onyeka Okongwu (3), Jakob Poeltl (3), Marreese Speights (3), Brendan Haywood (3), Al-Farouq Aminu (3), Marvin Bagley III (3), Ben Wallace (3), Nick Collison (3), Donyell Marshall (3), Andres Nocioni (3), Nazr Mohammed (3), Kenneth Faried (3), Kris Humphries (3), Richaun Holmes (3), Erick Dampier (3), Antonio McDyess (3), Jason Thompson (3), Kenny Thomas (3), Chris Wilcox (3), Elden Campbell (3), JJ Hickson (3), Anderson Varejao (3), Trey Lyles (3), Kendrick Perkins (3), Jamaal Magloire (3), Chris Boucher (3), Mark Blount (3), P.J. Brown (3), Alex Len (3), Gorgui Dieng (3), Bismack Biyombo (3), Luc Mbah a Moute (3), JaMychal Green (3), Larry Nance Jr. (3), Anthony Tolliver (3), Jared Sullinger (3), Thomas Bryant (3), Ed Davis (3), Primoz Brezec (3), Jim Jackson (3), Kwame Brown (3), Willie Cauley-Stein (3), Chris Andersen (3), Maxime Raynaud (3), Malik Rose (3), Marcus Fizer (3), David Robinson (3), Trevor Booker (3), Donovan Clingan (3), Jeff Foster (3), Lorenzen Wright (3), Yi Jianlian (3), Kevon Looney (3), Isaiah Hartenstein (3), Andris Biedrins (3), Reggie Evans (3), John Henson (3), Derik Queen (3), Jeremy Sochan (3), Timofey Mozgov (3), Dikembe Mutombo (4), Robert Horry (4), Precious Achiuwa (4), Isaiah Stewart (4), Kyle Filipowski (4), Mitchell Robinson (4), Danny Fortson (4), Vlade Divac (4), Michael Olowokandi (4), Kel'el Ware (4), Walker Kessler (4), DeJuan Blair (4), Jalen Smith (4), Chris Mihm (4), Mo Bamba (4), Byron Mullens (4), Brian Skinner (4), Omer Asik (4), Brian Grant (4), Dan Gadzuric (4), Chuck Hayes (4), Neemias Queta (4), Joel Przybilla (4), Jarred Vanderbilt (4), Larry Sanders (4), Dale Davis (4), Eddie Griffin (4), Nick Richards (4), Jerome Williams (4), Boban Marjanovic (4), Anthony Mason (4), Adonal Foyle (4), Lavoy Allen (4), Kelvin Cato (4), Francisco Elson (4), Zach Edey (4), Miles Plumlee (4), Noah Vonleh (4), Chimezie Metu (4), Jabari Walker (4), Christian Laettner (4), Greg Oden (4), Clarence Weatherspoon (4), Jordan Goodwin (4), Thomas Robinson (4), Moses Brown (4), Greg Ostertag (4), Josh Boone (4), Moussa Diabate (4), Shawn Bradley (4), Dominick Barlow (4), Alan Henderson (4), Aaron Gray (4), Cole Aldrich (4), Tarik Black (4), Hakeem Olajuwon (4), Kris Murray (4), Earl Barron (4), Cheick Diallo (4), James Singleton (4), Jericho Sims (4), Jahidi White (4), Willie Reed (4), Greg Smith (4), Ervin Johnson (5), Omer Yurtseven (5), Mouhamed Gueye (5), Joey Dorsey (5), Oscar Tshiebwe (5), Jaylen Hoard (5), Alize Johnson (5), Andre Brown (5), Moussa Cisse (5), Vitor Faverani (5), Julian Reese (5), Adama Sanogo (6), Solomon Alabi (6)

</details>

### `assists`

**Since 2001-02 (through 2025-26), name a player who recorded 20 or more assists in a game.**

27 valid answers, difficulty **medium**, tiers: 1: 9, 2: 10, 3: 6, 4: 2 (2 at tier 4 or above).

<details><summary>All valid answers</summary>

James Harden (1), Luka Doncic (1), Russell Westbrook (1), Chris Paul (1), Giannis Antetokounmpo (1), Trae Young (1), Nikola Jokic (1), Steve Nash (1), Deron Williams (1), Andre Miller (2), John Wall (2), Baron Davis (2), Jason Kidd (2), Reggie Jackson (2), Rajon Rondo (2), Tyrese Haliburton (2), Fred VanVleet (2), Darren Collison (2), Brandon Jennings (2), Ramon Sessions (3), Jamaal Tinsley (3), Elfrid Payton (3), Chris Duhon (3), Brevin Knight (3), Isaiah Collier (3), Will Bynum (4), Ryan Nembhard (4)

</details>

**Since 2001-02 (through 2025-26), name a player who recorded 16 or more assists in a game.**

118 valid answers, difficulty **easy**, tiers: 1: 37, 2: 35, 3: 36, 4: 10 (10 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Luka Doncic (1), Allen Iverson (1), Stephen Curry (1), Russell Westbrook (1), Damian Lillard (1), Tracy McGrady (1), Dwyane Wade (1), Chris Paul (1), Bradley Beal (1), Giannis Antetokounmpo (1), Tony Parker (1), Trae Young (1), Joe Johnson (1), Nikola Jokic (1), Gilbert Arenas (1), Jalen Brunson (1), Kyrie Irving (1), Ja Morant (1), Jrue Holiday (1), Jason Terry (1), Kyle Lowry (1), De'Aaron Fox (1), Cade Cunningham (1), Kemba Walker (1), Monta Ellis (1), Jamal Murray (1), Julius Randle (1), Steve Nash (1), Richard Hamilton (1), Derrick Rose (1), Chauncey Billups (1), Andre Iguodala (1), Deron Williams (1), Desmond Bane (2), Andre Miller (2), Austin Reaves (2), John Wall (2), D'Angelo Russell (2), Baron Davis (2), Goran Dragic (2), Jalen Johnson (2), Mike Bibby (2), Stephon Marbury (2), Gary Payton (2), Jason Kidd (2), Nicolas Batum (2), Darius Garland (2), Reggie Jackson (2), Hedo Turkoglu (2), Devin Harris (2), Raymond Felton (2), Eric Bledsoe (2), Jeff Teague (2), Rajon Rondo (2), Domantas Sabonis (2), Tyrese Haliburton (2), Kirk Hinrich (2), Spencer Dinwiddie (2), Boris Diaw (2), Draymond Green (2), Fred VanVleet (2), Tyreke Evans (2), Darren Collison (2), Sam Cassell (2), Aaron Brooks (2), Brandon Jennings (2), Nick Van Exel (2), Jose Calderon (2), Ty Lawson (3), Randy Foye (3), Ricky Rubio (3), Josh Giddey (3), Immanuel Quickley (3), Andrew Nembhard (3), Ramon Sessions (3), Ben Simmons (3), Beno Udrih (3), Michael Carter-Williams (3), Damon Stoudamire (3), T.J. McConnell (3), Jamaal Tinsley (3), Jason Williams (3), Steve Blake (3), T.J. Ford (3), Ish Smith (3), Earl Watson (3), Tyus Jones (3), Lonzo Ball (3), Chucky Atkins (3), Brent Barry (3), Elfrid Payton (3), Antonio Daniels (3), Greivis Vasquez (3), Kris Dunn (3), John Stockton (3), Cameron Payne (3), Jordan Farmar (3), Shake Milton (3), Chris Duhon (3), Brevin Knight (3), Dan Dickau (3), Damon Jones (3), Anthony Johnson (3), Isaiah Collier (3), Davion Mitchell (4), Will Bynum (4), Rod Strickland (4), Vince Williams Jr. (4), Brian Roberts (4), Mark Jackson (4), Moochie Norris (4), Kendall Marshall (4), Avery Johnson (4), Ryan Nembhard (4)

</details>

**Since 2001-02 (through 2025-26), name a player who recorded 14 or more assists in a game.**

213 valid answers, difficulty **easy**, tiers: 1: 54, 2: 62, 3: 67, 4: 26, 5: 3, 6: 1 (30 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Luka Doncic (1), Allen Iverson (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Russell Westbrook (1), Damian Lillard (1), Tracy McGrady (1), DeMar DeRozan (1), Dwyane Wade (1), Chris Paul (1), Paul Pierce (1), Bradley Beal (1), Giannis Antetokounmpo (1), Tony Parker (1), Pau Gasol (1), Trae Young (1), Joe Johnson (1), Nikola Jokic (1), Gilbert Arenas (1), Vince Carter (1), Isaiah Thomas (1), Jalen Brunson (1), Kyrie Irving (1), Tyrese Maxey (1), Donovan Mitchell (1), Jamal Crawford (1), Devin Booker (1), Jimmy Butler III (1), Ja Morant (1), Zach LaVine (1), Jrue Holiday (1), Jason Terry (1), Mike Conley (1), Kyle Lowry (1), De'Aaron Fox (1), Cade Cunningham (1), Kemba Walker (1), Monta Ellis (1), Manu Ginobili (1), Jamal Murray (1), LaMelo Ball (1), Julius Randle (1), Steve Nash (1), Richard Hamilton (1), Derrick Rose (1), Chauncey Billups (1), Andre Iguodala (1), Deni Avdija (1), Deron Williams (1), Tyler Herro (1), Desmond Bane (2), Andre Miller (2), Austin Reaves (2), John Wall (2), Victor Oladipo (2), Marc Gasol (2), D'Angelo Russell (2), Baron Davis (2), Dennis Schroder (2), Goran Dragic (2), Anfernee Simons (2), Stephen Jackson (2), Jalen Johnson (2), Dejounte Murray (2), Mike Bibby (2), Stephon Marbury (2), Antoine Walker (2), Jalen Rose (2), Gary Payton (2), Jason Kidd (2), Nicolas Batum (2), Darius Garland (2), Steve Francis (2), Reggie Jackson (2), Hedo Turkoglu (2), Devin Harris (2), Malcolm Brogdon (2), Alperen Sengun (2), Mo Williams (2), Raymond Felton (2), RJ Barrett (2), Eric Bledsoe (2), Jeff Teague (2), Rajon Rondo (2), Domantas Sabonis (2), Jameer Nelson (2), Mike Miller (2), Tyrese Haliburton (2), Kirk Hinrich (2), Spencer Dinwiddie (2), Boris Diaw (2), Draymond Green (2), Fred VanVleet (2), Caris LeVert (2), Tyreke Evans (2), Jarrett Jack (2), D.J. Augustin (2), Darren Collison (2), Scottie Barnes (2), Sam Cassell (2), Brandon Knight (2), Aaron Brooks (2), Derrick White (2), Marcus Smart (2), Kevin Porter Jr. (2), Brandon Jennings (2), Rodney Stuckey (2), Nick Van Exel (2), Amen Thompson (2), Devonte' Graham (2), Jose Calderon (2), Luke Ridnour (2), Ty Lawson (3), Randy Foye (3), J.J. Barea (3), Ryan Rollins (3), Ricky Rubio (3), Nate Robinson (3), Malik Monk (3), Jusuf Nurkic (3), Josh Giddey (3), Immanuel Quickley (3), Andrew Nembhard (3), Ramon Sessions (3), Ben Simmons (3), Beno Udrih (3), Michael Carter-Williams (3), Rafer Alston (3), Stephon Castle (3), Grayson Allen (3), Damon Stoudamire (3), Joakim Noah (3), T.J. McConnell (3), Cory Joseph (3), Joe Ingles (3), Jamaal Tinsley (3), Jason Williams (3), Shaun Livingston (3), Seth Curry (3), Dennis Smith Jr. (3), Steve Blake (3), T.J. Ford (3), Ish Smith (3), Jeremy Lin (3), Ayo Dosunmu (3), Earl Watson (3), Jeff McInnis (3), Tyus Jones (3), Lonzo Ball (3), Chucky Atkins (3), Brent Barry (3), Lance Stephenson (3), Troy Hudson (3), Scoot Henderson (3), Elfrid Payton (3), Antonio Daniels (3), Markelle Fultz (3), Greivis Vasquez (3), Brandin Podziemski (3), Trey Burke (3), Reed Sheppard (3), Jonny Flynn (3), Kris Dunn (3), John Stockton (3), Tyronn Lue (3), Alvin Williams (3), Cameron Payne (3), Jordan Farmar (3), Shake Milton (3), Eric Snow (3), Chris Duhon (3), Carlos Arroyo (3), Brevin Knight (3), Delon Wright (3), Dan Dickau (3), Darrel Armstrong (3), Damon Jones (3), Anthony Johnson (3), Isaiah Collier (3), Davion Mitchell (4), Will Bynum (4), Scottie Pippen (4), Matthew Dellavedova (4), Tomas Satoransky (4), Rod Strickland (4), Theo Maledon (4), Vince Williams Jr. (4), Anthony Carter (4), Brian Roberts (4), Jason Hart (4), Howard Eisley (4), Daniss Jenkins (4), A.J. Price (4), Terrence Williams (4), Mark Jackson (4), Moochie Norris (4), Shane Larkin (4), Tim Frazier (4), Kendall Marshall (4), Avery Johnson (4), Walter Clayton Jr. (4), Donald Sloan (4), Jamal Shead (4), Ryan Nembhard (4), Rick Brunson (4), Chris Childs (5), Keaton Wallace (5), Jahmai Mashack (5), Nikola Topic (6)

</details>

### `threes`

**Since 2001-02 (through 2025-26), name a player who made 11 or more three-pointers in a game.**

21 valid answers, difficulty **medium**, tiers: 1: 8, 2: 6, 3: 5, 4: 2 (2 at tier 4 or above).

<details><summary>All valid answers</summary>

Kobe Bryant (1), Stephen Curry (1), Damian Lillard (1), Kyrie Irving (1), Klay Thompson (1), Zach LaVine (1), CJ McCollum (1), Deron Williams (1), JR Smith (2), Bojan Bogdanovic (2), Trey Murphy III (2), Buddy Hield (2), Fred VanVleet (2), Marcus Smart (2), Malik Beasley (3), Robert Covington (3), Donte DiVincenzo (3), Keegan Murray (3), Donyell Marshall (3), Julian Champagnie (4), AJ Green (4)

</details>

**Since 2001-02 (through 2025-26), name a player who made 9 or more three-pointers in a game.**

122 valid answers, difficulty **easy**, tiers: 1: 37, 2: 47, 3: 30, 4: 8 (8 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kobe Bryant (1), Luka Doncic (1), Stephen Curry (1), Damian Lillard (1), Carmelo Anthony (1), Bradley Beal (1), Jayson Tatum (1), Joe Johnson (1), Paul George (1), Vince Carter (1), Isaiah Thomas (1), Anthony Edwards (1), Jalen Brunson (1), Jaylen Brown (1), Kyrie Irving (1), Tyrese Maxey (1), Klay Thompson (1), Donovan Mitchell (1), Ray Allen (1), Brook Lopez (1), Zach LaVine (1), Jason Terry (1), CJ McCollum (1), Lauri Markkanen (1), Michael Redd (1), Karl-Anthony Towns (1), Kemba Walker (1), Jamal Murray (1), LaMelo Ball (1), Chauncey Billups (1), Blake Griffin (1), Peja Stojakovic (1), Jason Richardson (1), Deron Williams (1), Tyler Herro (1), Keyonte George (2), Austin Reaves (2), D'Angelo Russell (2), JR Smith (2), Anfernee Simons (2), Jaren Jackson Jr. (2), JJ Redick (2), Caron Butler (2), Mike Bibby (2), Tim Hardaway Jr. (2), Trevor Ariza (2), Antoine Walker (2), Danilo Gallinari (2), Nicolas Batum (2), Norman Powell (2), Darius Garland (2), Bojan Bogdanovic (2), Wesley Matthews (2), Trey Murphy III (2), Ben Gordon (2), Terry Rozier (2), Buddy Hield (2), Aaron Gordon (2), Nickeil Alexander-Walker (2), Mike Miller (2), Tyrese Haliburton (2), Ricky Davis (2), Jordan Poole (2), Coby White (2), Fred VanVleet (2), Kelly Oubre Jr. (2), Evan Fournier (2), Dillon Brooks (2), T.J. Warren (2), Derrick White (2), Latrell Sprewell (2), Marcus Smart (2), Kevin Porter Jr. (2), Patty Mills (2), Cameron Johnson (2), Danny Green (2), CJ Miles (2), Terrence Ross (2), Gary Trent Jr. (2), Devonte' Graham (2), Channing Frye (2), Saddiq Bey (2), Ty Lawson (3), Quentin Richardson (3), Bogdan Bogdanovic (3), Malik Monk (3), Payton Pritchard (3), Malik Beasley (3), Chandler Parsons (3), Grayson Allen (3), Robert Covington (3), Dorell Wright (3), Mario Chalmers (3), Duncan Robinson (3), Jodie Meeks (3), Nikola Mirotic (3), Donte DiVincenzo (3), Davis Bertans (3), Keegan Murray (3), Jeremy Lin (3), Donyell Marshall (3), Luke Kennard (3), Reed Sheppard (3), Omri Casspi (3), Toumani Camara (3), Corey Kispert (3), Landry Shamet (3), Sam Merrill (3), Max Strus (3), Miles McBride (3), Isaiah Joe (3), Aron Baynes (3), Julian Champagnie (4), Toney Douglas (4), Sam Hauser (4), AJ Green (4), Yogi Ferrell (4), Dalton Knecht (4), Rodrigue Beaubois (4), Keon Ellis (4)

</details>

**Since 2001-02 (through 2025-26), name a player who made 8 or more three-pointers in a game.**

253 valid answers, difficulty **easy**, tiers: 1: 64, 2: 80, 3: 82, 4: 24, 5: 2, 6: 1 (27 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Luka Doncic (1), Dirk Nowitzki (1), Stephen Curry (1), Russell Westbrook (1), Damian Lillard (1), Carmelo Anthony (1), Tracy McGrady (1), Chris Paul (1), Paul Pierce (1), Bradley Beal (1), Jayson Tatum (1), Trae Young (1), Joe Johnson (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Isaiah Thomas (1), Anthony Edwards (1), Jalen Brunson (1), Jaylen Brown (1), Kyrie Irving (1), Tyrese Maxey (1), Klay Thompson (1), Donovan Mitchell (1), Jamal Crawford (1), Devin Booker (1), Ray Allen (1), Brook Lopez (1), Zach LaVine (1), Jrue Holiday (1), Jason Terry (1), CJ McCollum (1), Lauri Markkanen (1), Mike Conley (1), Michael Redd (1), Kyle Lowry (1), De'Aaron Fox (1), Karl-Anthony Towns (1), Kevin Love (1), Kemba Walker (1), Manu Ginobili (1), Jamal Murray (1), LaMelo Ball (1), Lou Williams (1), Julius Randle (1), Steve Nash (1), Victor Wembanyama (1), Chauncey Billups (1), Brandon Ingram (1), Andrew Wiggins (1), Blake Griffin (1), Harrison Barnes (1), Peja Stojakovic (1), Jeff Green (1), Pascal Siakam (1), Jason Richardson (1), Michael Porter Jr. (1), Deron Williams (1), Khris Middleton (1), Tyler Herro (1), Eric Gordon (2), Desmond Bane (2), Keyonte George (2), Austin Reaves (2), Kristaps Porzingis (2), D'Angelo Russell (2), JR Smith (2), Dennis Schroder (2), Anfernee Simons (2), Jordan Clarkson (2), Stephen Jackson (2), Jaren Jackson Jr. (2), JJ Redick (2), Caron Butler (2), Dejounte Murray (2), Kyle Korver (2), Mike Bibby (2), Jerami Grant (2), Tim Hardaway Jr. (2), Stephon Marbury (2), Trevor Ariza (2), Kyle Kuzma (2), Antoine Walker (2), Jalen Green (2), Danilo Gallinari (2), Nicolas Batum (2), Norman Powell (2), Darius Garland (2), Bojan Bogdanovic (2), Wesley Matthews (2), Trey Murphy III (2), Ben Gordon (2), Terry Rozier (2), Buddy Hield (2), Mike Dunleavy (2), Aaron Gordon (2), Kentavious Caldwell-Pope (2), Christian Wood (2), Myles Turner (2), Nickeil Alexander-Walker (2), Mikal Bridges (2), Mike Miller (2), Tyrese Haliburton (2), Michael Finley (2), Ricky Davis (2), Jordan Poole (2), Draymond Green (2), Coby White (2), Leandro Barbosa (2), Fred VanVleet (2), Kelly Oubre Jr. (2), Evan Fournier (2), Dillon Brooks (2), Brandon Miller (2), Mike James (2002-2014) (2), Bobby Portis (2), T.J. Warren (2), Devin Vassell (2), Derrick White (2), Latrell Sprewell (2), Marcus Smart (2), Kevin Porter Jr. (2), Brandon Jennings (2), Jae Crowder (2), Alec Burks (2), Patty Mills (2), Cameron Johnson (2), Marcus Thornton (2), Danny Green (2), Kon Knueppel (2), CJ Miles (2), Arron Afflalo (2), Terrence Ross (2), Nick Van Exel (2), Gary Trent Jr. (2), Nick Young (2), Devonte' Graham (2), Ryan Anderson (2), Channing Frye (2), Saddiq Bey (2), Ty Lawson (3), Randy Foye (3), Quentin Richardson (3), Bogdan Bogdanovic (3), Avery Bradley (3), Luguentz Dort (3), Ricky Rubio (3), Nate Robinson (3), Malik Monk (3), Payton Pritchard (3), Raja Bell (3), David Wesley (3), Rafer Alston (3), Malik Beasley (3), Chandler Parsons (3), Josh Richardson (3), Grayson Allen (3), Robert Covington (3), Dorell Wright (3), Gerald Green (3), Kevin Huerter (3), Mario Chalmers (3), Duncan Robinson (3), Damon Stoudamire (3), Jodie Meeks (3), Nikola Mirotic (3), Donte DiVincenzo (3), Wayne Ellington (3), Joe Ingles (3), Davis Bertans (3), Vladimir Radmanovic (3), Taurean Prince (3), DeShawn Stevenson (3), Seth Curry (3), Keegan Murray (3), Onyeka Okongwu (3), Jeremy Lin (3), Donyell Marshall (3), Rodney Hood (3), Lonzo Ball (3), Quentin Grimes (3), Joe Harris (3), Justin Holiday (3), Luke Kennard (3), Dorian Finney-Smith (3), Anthony Morrow (3), Eddie House (3), Scoot Henderson (3), Mickael Pietrus (3), Ben McLemore (3), Brandin Podziemski (3), Aaron Nesmith (3), Trey Burke (3), Reed Sheppard (3), Omri Casspi (3), Toumani Camara (3), Corey Kispert (3), Allen Crabbe (3), Carlos Delfino (3), Reggie Bullock Jr. (3), Cameron Payne (3), Jordan Farmar (3), Landry Shamet (3), Sam Merrill (3), Max Strus (3), Collin Gillespie (3), Chris Duhon (3), Bryn Forbes (3), De'Anthony Melton (3), Ty Jerome (3), Jaylen Wells (3), Damon Jones (3), Alex Caruso (3), Max Christie (3), Moses Moody (3), Lonnie Walker IV (3), Aaron Wiggins (3), Miles McBride (3), Nemanja Bjelica (3), Isaiah Joe (3), Steve Smith (3), Aron Baynes (3), Maxi Kleber (4), Julian Champagnie (4), Toney Douglas (4), Isaiah Canaan (2014-2019) (4), Juan Carlos Navarro (4), Damyean Dotson (4), Sam Hauser (4), Cam Reddish (4), AJ Green (4), Jose Alvarado (4), Jevon Carter (4), Yogi Ferrell (4), Denzel Valentine (4), Mario Hezonja (4), Troy Daniels (4), Steve Novak (4), Reggie Williams (4), Dalton Knecht (4), Rodrigue Beaubois (4), Jake LaRavia (4), Tyrese Martin (4), Jordan Goodwin (4), Vit Krejci (4), Keon Ellis (4), Paul Watson (5), John Poulakidas (5), Alec Peters (6)

</details>

### `blocks`

**Since 2001-02 (through 2025-26), name a player who blocked 10 or more shots in a game.**

20 valid answers, difficulty **hard**, tiers: 1: 5, 2: 5, 3: 7, 4: 3 (3 at tier 4 or above).

<details><summary>All valid answers</summary>

Dwight Howard (1), Anthony Davis (1), Amar'e Stoudemire (1), Victor Wembanyama (1), Jermaine O'Neal (1), Josh Smith (2), Serge Ibaka (2), Andrei Kirilenko (2), Clint Capela (2), Andrew Bynum (2), Hassan Whiteside (3), Emeka Okafor (3), JaVale McGee (3), Roy Hibbert (3), Joakim Noah (3), Marcus Camby (3), Ben Wallace (3), Dikembe Mutombo (4), Larry Sanders (4), Calvin Booth (4)

</details>

**Since 2001-02 (through 2025-26), name a player who blocked 8 or more shots in a game.**

65 valid answers, difficulty **hard**, tiers: 1: 11, 2: 14, 3: 20, 4: 18, 5: 2 (20 at tier 4 or above).

<details><summary>All valid answers</summary>

Tim Duncan (1), Pau Gasol (1), Dwight Howard (1), Anthony Davis (1), Shaquille O'Neal (1), Brook Lopez (1), Amar'e Stoudemire (1), Yao Ming (1), Victor Wembanyama (1), Elton Brand (1), Jermaine O'Neal (1), Josh Smith (2), Marc Gasol (2), Jaren Jackson Jr. (2), Jerami Grant (2), Serge Ibaka (2), Rudy Gobert (2), Myles Turner (2), DeAndre Jordan (2), Andrei Kirilenko (2), Clint Capela (2), Robin Lopez (2), Andrew Bynum (2), Evan Mobley (2), Chris Kaman (2), Chet Holmgren (3), Hassan Whiteside (3), Emeka Okafor (3), JaVale McGee (3), Roy Hibbert (3), Andrew Bogut (3), Samuel Dalembert (3), Joakim Noah (3), Alonzo Mourning (3), Marcus Camby (3), Ben Wallace (3), Nazr Mohammed (3), Erick Dampier (3), Rasho Nesterovic (3), Raef LaFrentz (3), Daniel Gafford (3), Stromile Swift (3), Chris Andersen (3), Donovan Clingan (3), Nerlens Noel (3), Dikembe Mutombo (4), Isaiah Stewart (4), Tyrus Thomas (4), Mitchell Robinson (4), Keon Clark (4), Walker Kessler (4), Robert Williams III (4), Theo Ratliff (4), Joel Przybilla (4), Larry Sanders (4), Eddie Griffin (4), Adonal Foyle (4), Anthony Randolph (4), Greg Ostertag (4), Shawn Bradley (4), Joel Anthony (4), Hakeem Olajuwon (4), Calvin Booth (4), Sean Williams (5), Mamadou N'diaye (5)

</details>

**Since 2001-02 (through 2025-26), name a player who blocked 6 or more shots in a game.**

215 valid answers, difficulty **medium**, tiers: 1: 30, 2: 45, 3: 63, 4: 65, 5: 11, 6: 1 (77 at tier 4 or above).

<details><summary>All valid answers</summary>

Kevin Durant (1), Joel Embiid (1), Dirk Nowitzki (1), Tim Duncan (1), Giannis Antetokounmpo (1), Jayson Tatum (1), Pau Gasol (1), LaMarcus Aldridge (1), Dwight Howard (1), Anthony Davis (1), Kevin Garnett (1), Kawhi Leonard (1), Shaquille O'Neal (1), Brook Lopez (1), Jrue Holiday (1), Chris Bosh (1), DeMarcus Cousins (1), Nikola Vucevic (1), Rudy Gay (1), Karl-Anthony Towns (1), Amar'e Stoudemire (1), Danny Granger (1), Al Horford (1), Shawn Marion (1), Yao Ming (1), Victor Wembanyama (1), Paul Millsap (1), Elton Brand (1), Jermaine O'Neal (1), David West (1), Al Jefferson (2), Kristaps Porzingis (2), Josh Smith (2), Marc Gasol (2), Jonas Valanciunas (2), Jaren Jackson Jr. (2), Jerami Grant (2), Serge Ibaka (2), Rudy Gobert (2), Andre Drummond (2), John Collins (2), Bam Adebayo (2), Andrea Bargnani (2), Lamar Odom (2), Rasheed Wallace (2), Christian Wood (2), Myles Turner (2), Zydrunas Ilgauskas (2), Boris Diaw (2), Gerald Wallace (2), Draymond Green (2), DeAndre Jordan (2), Tyson Chandler (2), Kenyon Martin (2), Fred VanVleet (2), Andrei Kirilenko (2), Josh Howard (2), Scottie Barnes (2), Shane Battier (2), Taj Gibson (2), Clint Capela (2), Jalen Duren (2), Eddy Curry (2), Derrick White (2), Enes Freedom (2), Jarrett Allen (2), Derrick Favors (2), Robin Lopez (2), Wilson Chandler (2), Andrew Bynum (2), Danny Green (2), Evan Mobley (2), Marcin Gortat (2), Chris Kaman (2), Markieff Morris (2), Jahlil Okafor (3), Jusuf Nurkic (3), Chet Holmgren (3), Steven Adams (3), Hassan Whiteside (3), Emeka Okafor (3), JaVale McGee (3), Roy Hibbert (3), Ivica Zubac (3), Mason Plumlee (3), Andrew Bogut (3), Samuel Dalembert (3), Robert Covington (3), Dorell Wright (3), Alex Sarr (3), Matas Buzelis (3), Kurt Thomas (3), Joakim Noah (3), Alonzo Mourning (3), P.J. Washington (3), Amir Johnson (3), Marcus Camby (3), Spencer Hawes (3), Jakob Poeltl (3), James Johnson (3), Brendan Haywood (3), Al-Farouq Aminu (3), Ben Wallace (3), Nazr Mohammed (3), Peyton Watson (3), Richaun Holmes (3), Erick Dampier (3), Travis Outlaw (3), Elden Campbell (3), Kendrick Perkins (3), Rasho Nesterovic (3), Jamaal Magloire (3), Chris Boucher (3), Alex Len (3), Raef LaFrentz (3), Gorgui Dieng (3), Bismack Biyombo (3), Daniel Gafford (3), James Jones (3), Stromile Swift (3), Kwame Brown (3), Chris Andersen (3), Nic Claxton (3), Michael Kidd-Gilchrist (3), Noah Clowney (3), David Robinson (3), Trevor Booker (3), Donovan Clingan (3), Terrence Jones (3), Jason Maxiell (3), Jordan Hill (3), Yi Jianlian (3), Kevon Looney (3), Andris Biedrins (3), John Henson (3), Nerlens Noel (3), Dewayne Dedmon (3), Zach Collins (3), Dikembe Mutombo (4), Isaiah Stewart (4), Tyrus Thomas (4), Mitchell Robinson (4), Keon Clark (4), Maxi Kleber (4), Jaxson Hayes (4), Michael Olowokandi (4), Kel'el Ware (4), Walker Kessler (4), Brandan Wright (4), Jumaine Jones (4), Darko Milicic (4), Chris Mihm (4), Mo Bamba (4), Jock Landale (4), Brian Skinner (4), Kyle O'Quinn (4), Robert Williams III (4), Dan Gadzuric (4), Luke Kornet (4), Etan Thomas (4), Neemias Queta (4), Drew Eubanks (4), Theo Ratliff (4), Isaiah Roby (4), Ronny Turiaf (4), Jonathan Isaac (4), Joel Przybilla (4), Larry Sanders (4), Eddie Griffin (4), Melvin Ely (4), Jay Huff (4), Adonal Foyle (4), Jamario Moon (4), Steven Hunter (4), Kelvin Cato (4), Anthony Randolph (4), Zach Edey (4), Jerome James (4), Greg Oden (4), Dereck Lively II (4), Isaiah Jackson (4), Moses Brown (4), Donte Greene (4), Greg Ostertag (4), Damian Jones (4), Aleksej Pokusevski (4), Ekpe Udoh (4), Robert Traylor (4), Zeljko Rebraca (4), Jonathan Bender (4), DeSagana Diop (4), Shawn Bradley (4), Scot Pollard (4), Joel Anthony (4), Hakeem Olajuwon (4), Dragan Bender (4), David Harrison (4), Calvin Booth (4), Vladimir Stepania (4), Arvydas Sabonis (4), Salah Mejri (4), Jordan Bell (4), Greg Stiemsma (4), Sean Williams (5), Charles Bassey (5), Michael Ruffin (5), Christian Koloko (5), Joan Beringer (5), Don Reid (5), Mamadou N'diaye (5), Bernard James (5), Chris Johnson (2011-2013) (5), Vitor Faverani (5), Jarvis Varnado (5), Edy Tavares (6)

</details>

### `steals`

**Since 2001-02 (through 2025-26), name a player who stole the ball 6 or more times in a game.**

328 valid answers, difficulty **easy**, tiers: 1: 69, 2: 82, 3: 113, 4: 61, 5: 2, 6: 1 (64 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kobe Bryant (1), Dirk Nowitzki (1), Allen Iverson (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Russell Westbrook (1), Damian Lillard (1), Carmelo Anthony (1), Tracy McGrady (1), DeMar DeRozan (1), Dwyane Wade (1), Chris Paul (1), Paul Pierce (1), Bradley Beal (1), Tony Parker (1), Jayson Tatum (1), Joe Johnson (1), Nikola Jokic (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Anthony Edwards (1), Anthony Davis (1), Kyrie Irving (1), Tyrese Maxey (1), Donovan Mitchell (1), Jamal Crawford (1), Kevin Garnett (1), Kawhi Leonard (1), Devin Booker (1), Ray Allen (1), Jimmy Butler III (1), Jrue Holiday (1), Chris Bosh (1), Zion Williamson (1), DeMarcus Cousins (1), Jason Terry (1), Mike Conley (1), Michael Redd (1), Kyle Lowry (1), De'Aaron Fox (1), Nikola Vucevic (1), Rudy Gay (1), Tobias Harris (1), Cade Cunningham (1), Kevin Love (1), Amar'e Stoudemire (1), Antawn Jamison (1), Danny Granger (1), Kemba Walker (1), Monta Ellis (1), Shawn Marion (1), Manu Ginobili (1), Jamal Murray (1), Lou Williams (1), Derrick Rose (1), Victor Wembanyama (1), Paul Millsap (1), Andrew Wiggins (1), Chris Webber (1), Andre Iguodala (1), Collin Sexton (1), Peja Stojakovic (1), Jason Richardson (1), Deron Williams (1), Franz Wagner (1), Khris Middleton (1), Andre Miller (2), Rashard Lewis (2), Thaddeus Young (2), Luol Deng (2), John Wall (2), Victor Oladipo (2), Josh Smith (2), D'Angelo Russell (2), Michael Jordan (2), Baron Davis (2), Brandon Roy (2), Stephen Jackson (2), Jaren Jackson Jr. (2), Jalen Johnson (2), Caron Butler (2), Dejounte Murray (2), Kyle Korver (2), Karl Malone (2), Mike Bibby (2), Stephon Marbury (2), Al Harrington (2), Trevor Ariza (2), Corey Maggette (2), Metta World Peace (2), Larry Hughes (2), Jason Kidd (2), Nicolas Batum (2), Cuttino Mobley (2), Steve Francis (2), Andre Drummond (2), Jalen Williams (2), Reggie Jackson (2), Nene (2), Bam Adebayo (2), Lamar Odom (2), Devin Harris (2), Shareef Abdur-Rahim (2), Rasheed Wallace (2), Mo Williams (2), Terry Rozier (2), Raymond Felton (2), RJ Barrett (2), Mike Dunleavy (2), Aaron Gordon (2), Eric Bledsoe (2), Jeff Teague (2), Rajon Rondo (2), Myles Turner (2), Jameer Nelson (2), Derek Fisher (2), Mikal Bridges (2), Tyrese Haliburton (2), Kirk Hinrich (2), Ricky Davis (2), Gerald Wallace (2), Jordan Poole (2), Draymond Green (2), Leandro Barbosa (2), Kenyon Martin (2), Fred VanVleet (2), Andrei Kirilenko (2), Kelly Oubre Jr. (2), Caris LeVert (2), Tyreke Evans (2), Josh Howard (2), Darren Collison (2), Scottie Barnes (2), Sam Cassell (2), Grant Hill (2), Brandon Knight (2), Derrick White (2), Marcus Smart (2), Jarrett Allen (2), Brandon Jennings (2), John Salmons (2), Marcus Thornton (2), OG Anunoby (2), Eddie Jones (2), Amen Thompson (2), Matt Barnes (2), Courtney Lee (2), Luke Ridnour (2), Ty Lawson (3), Gary Harris (3), Zaza Pachulia (3), Avery Bradley (3), Luguentz Dort (3), Ricky Rubio (3), Raja Bell (3), Josh Giddey (3), Corey Brewer (2008-2020) (3), Steven Adams (3), De'Andre Hunter (3), Bonzi Wells (3), Andrew Nembhard (3), Ben Simmons (3), Tony Allen (3), Andray Blatche (3), Beno Udrih (3), Morris Peterson (3), Michael Carter-Williams (3), David Wesley (3), Rafer Alston (3), Josh Richardson (3), Robert Covington (3), Dorell Wright (3), Bobby Simmons (3), Kevin Huerter (3), Mario Chalmers (3), P.J. Tucker (3), James Posey (3), T.J. McConnell (3), Jodie Meeks (3), Joe Ingles (3), Jamaal Tinsley (3), Jason Williams (3), Marcus Camby (3), Spencer Hawes (3), Jeremy Lamb (3), Patrick Beverley (3), Shaun Livingston (3), Wendell Carter Jr. (3), Dennis Smith Jr. (3), James Johnson (3), Steve Blake (3), Otto Porter Jr. (3), Al-Farouq Aminu (3), Ish Smith (3), Ben Wallace (3), Jeremy Lin (3), Earl Boykins (3), DeMarre Carroll (3), Ruben Patterson (3), Kent Bazemore (3), Earl Watson (3), Tyus Jones (3), Lonzo Ball (3), Kyle Anderson (3), Justin Holiday (3), Thabo Sefolosha (3), Brent Barry (3), Royce O'Neale (3), Jeremiah Fears (3), Anthony Morrow (3), Eddie House (3), Antonio McDyess (3), Dyson Daniels (3), Darius Miles (3), Elfrid Payton (3), Ronald Murray (3), Markelle Fultz (3), Dwight Powell (3), Jalen Suggs (3), Ronnie Brewer (3), E'Twaun Moore (3), Glen Davis (3), Marquis Daniels (3), Charlie Bell (3), Reed Sheppard (3), Delonte West (3), Omri Casspi (3), Kris Dunn (3), C.J. Watson (3), John Stockton (3), Toumani Camara (3), Luc Mbah a Moute (3), Maurice Harkless (3), Larry Nance Jr. (3), Keith Bogans (3), Chris Duarte (3), Jordan Farmar (3), Wesley Johnson (3), Sebastian Telfair (3), Willie Cauley-Stein (3), Brevin Knight (3), De'Anthony Melton (3), Ty Jerome (3), Delon Wright (3), Darrel Armstrong (3), Juan Dixon (3), Michael Kidd-Gilchrist (3), Iman Shumpert (3), Alex Caruso (3), Speedy Claxton (3), Damien Wilkins (3), Tari Eason (3), Aaron Wiggins (3), Doug Christie (3), Dahntay Jones (3), Anfernee Hardaway (3), Dylan Harper (3), Ian Mahinmi (3), Nerlens Noel (3), Toni Kukoc (3), Smush Parker (3), Robert Horry (4), Kyle Filipowski (4), Tyrus Thomas (4), Marko Jaric (4), Jared Jeffries (4), Eduardo Najera (4), Herbert Jones (4), Scottie Pippen (4), Talen Horton-Tucker (4), Byron Mullens (4), Alonzo Gee (4), Tomas Satoransky (4), Danuel House Jr. (4), Tre Mann (4), Troy Brown Jr. (4), Killian Hayes (4), Jose Alvarado (4), Greg Buckner (4), Ziaire Williams (4), Chris Crawford (4), Theo Maledon (4), Ausar Thompson (4), Jonathan Isaac (4), Gary Payton II (4), Marcus Banks (4), Dale Davis (4), Anthony Carter (4), Jerome Williams (4), Anthony Peeler (4), Javonte Green (4), Matisse Thybulle (4), Paul Reed (4), Lindsey Hunter (4), Jay Williams (4), Andrew Harrison (4), Howard Eisley (4), Walter McCarty (4), Sergio Rodriguez (4), Jabari Walker (4), John Konchar (4), Jordan Goodwin (4), Chuma Okeke (4), Frank Ntilikina (4), Nique Clifford (4), Xavier Tillman (4), Adrian Griffin (4), Keon Ellis (4), Shammond Williams (4), Chris Quinn (4), Jordan McLaughlin (4), Charlie Ward (4), Greg Anthony (4), Moussa Diabate (4), Taylor Hendricks (4), Pablo Prigioni (4), Ryan Bowen (4), Hakeem Olajuwon (4), Oso Ighodaro (4), Will Richard (4), Junior Harrington (4), Markel Brown (4), Dru Smith (5), Jahmai Mashack (5), Kadary Richmond (6)

</details>

**Since 2001-02 (through 2025-26), name a player who stole the ball 7 or more times in a game.**

127 valid answers, difficulty **easy**, tiers: 1: 33, 2: 36, 3: 44, 4: 14 (14 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kobe Bryant (1), Dirk Nowitzki (1), Allen Iverson (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Russell Westbrook (1), Dwyane Wade (1), Chris Paul (1), Paul Pierce (1), Nikola Jokic (1), Gilbert Arenas (1), Paul George (1), Anthony Davis (1), Kyrie Irving (1), Tyrese Maxey (1), Kevin Garnett (1), Kawhi Leonard (1), Jimmy Butler III (1), Jrue Holiday (1), Chris Bosh (1), DeMarcus Cousins (1), Mike Conley (1), Kyle Lowry (1), Kemba Walker (1), Monta Ellis (1), Shawn Marion (1), Manu Ginobili (1), Lou Williams (1), Paul Millsap (1), Chris Webber (1), Jason Richardson (1), Andre Miller (2), Rashard Lewis (2), Thaddeus Young (2), John Wall (2), Victor Oladipo (2), Josh Smith (2), D'Angelo Russell (2), Baron Davis (2), Brandon Roy (2), Jalen Johnson (2), Caron Butler (2), Dejounte Murray (2), Al Harrington (2), Metta World Peace (2), Larry Hughes (2), Jason Kidd (2), Cuttino Mobley (2), Steve Francis (2), Shareef Abdur-Rahim (2), Raymond Felton (2), Eric Bledsoe (2), Rajon Rondo (2), Jameer Nelson (2), Mikal Bridges (2), Kirk Hinrich (2), Gerald Wallace (2), Draymond Green (2), Kenyon Martin (2), Fred VanVleet (2), Andrei Kirilenko (2), Kelly Oubre Jr. (2), Josh Howard (2), Marcus Smart (2), OG Anunoby (2), Eddie Jones (2), Amen Thompson (2), Ty Lawson (3), Ricky Rubio (3), Josh Giddey (3), Bonzi Wells (3), Ben Simmons (3), Tony Allen (3), Morris Peterson (3), Michael Carter-Williams (3), Rafer Alston (3), Josh Richardson (3), Robert Covington (3), Mario Chalmers (3), P.J. Tucker (3), T.J. McConnell (3), Jamaal Tinsley (3), Shaun Livingston (3), Dennis Smith Jr. (3), Steve Blake (3), Ish Smith (3), Ben Wallace (3), Earl Boykins (3), Ruben Patterson (3), Tyus Jones (3), Thabo Sefolosha (3), Jeremiah Fears (3), Antonio McDyess (3), Dyson Daniels (3), Elfrid Payton (3), Ronnie Brewer (3), Marquis Daniels (3), Delonte West (3), C.J. Watson (3), Willie Cauley-Stein (3), Brevin Knight (3), De'Anthony Melton (3), Juan Dixon (3), Speedy Claxton (3), Damien Wilkins (3), Doug Christie (3), Anfernee Hardaway (3), Dylan Harper (3), Ian Mahinmi (3), Nerlens Noel (3), Smush Parker (3), Herbert Jones (4), Tre Mann (4), Greg Buckner (4), Ausar Thompson (4), Jonathan Isaac (4), Marcus Banks (4), Jerome Williams (4), Javonte Green (4), Walter McCarty (4), Sergio Rodriguez (4), Adrian Griffin (4), Charlie Ward (4), Pablo Prigioni (4), Ryan Bowen (4)

</details>

**Since 2001-02 (through 2025-26), name a player who stole the ball 8 or more times in a game.**

52 valid answers, difficulty **easy**, tiers: 1: 16, 2: 13, 3: 19, 4: 4 (4 at tier 4 or above).

<details><summary>All valid answers</summary>

James Harden (1), Dirk Nowitzki (1), Allen Iverson (1), Russell Westbrook (1), Dwyane Wade (1), Chris Paul (1), Gilbert Arenas (1), Paul George (1), Kyrie Irving (1), Tyrese Maxey (1), Kemba Walker (1), Shawn Marion (1), Manu Ginobili (1), Lou Williams (1), Paul Millsap (1), Jason Richardson (1), Andre Miller (2), Thaddeus Young (2), John Wall (2), Brandon Roy (2), Dejounte Murray (2), Metta World Peace (2), Steve Francis (2), Rajon Rondo (2), Gerald Wallace (2), Draymond Green (2), Andrei Kirilenko (2), Kelly Oubre Jr. (2), Marcus Smart (2), Ty Lawson (3), Ricky Rubio (3), Josh Giddey (3), Bonzi Wells (3), Tony Allen (3), Morris Peterson (3), Michael Carter-Williams (3), Rafer Alston (3), Robert Covington (3), Mario Chalmers (3), T.J. McConnell (3), Jamaal Tinsley (3), Dyson Daniels (3), Marquis Daniels (3), Delonte West (3), Brevin Knight (3), Juan Dixon (3), Speedy Claxton (3), Doug Christie (3), Herbert Jones (4), Jerome Williams (4), Sergio Rodriguez (4), Pablo Prigioni (4)

</details>

### `ppg-season`

**Since 2001-02 (through 2025-26), name a player who averaged 30 or more points per game in a regular season (minimum 40 games).**

16 valid answers, difficulty **medium**, tiers: 1: 16 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Luka Doncic (1), Joel Embiid (1), Allen Iverson (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Russell Westbrook (1), Damian Lillard (1), Tracy McGrady (1), Dwyane Wade (1), Bradley Beal (1), Giannis Antetokounmpo (1), Jayson Tatum (1)

</details>

**Since 2001-02 (through 2025-26), name a player who averaged 25 or more points per game in a regular season (minimum 40 games).**

60 valid answers, difficulty **easy**, tiers: 1: 60 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Luka Doncic (1), Joel Embiid (1), Dirk Nowitzki (1), Allen Iverson (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Russell Westbrook (1), Damian Lillard (1), Carmelo Anthony (1), Tracy McGrady (1), DeMar DeRozan (1), Dwyane Wade (1), Paul Pierce (1), Tim Duncan (1), Bradley Beal (1), Giannis Antetokounmpo (1), Jayson Tatum (1), Trae Young (1), Joe Johnson (1), Nikola Jokic (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Isaiah Thomas (1), Anthony Edwards (1), Anthony Davis (1), Jalen Brunson (1), Jaylen Brown (1), Kyrie Irving (1), Tyrese Maxey (1), Donovan Mitchell (1), Kawhi Leonard (1), Devin Booker (1), Ray Allen (1), Shaquille O'Neal (1), Ja Morant (1), Zach LaVine (1), Zion Williamson (1), DeMarcus Cousins (1), Lauri Markkanen (1), Michael Redd (1), De'Aaron Fox (1), Cade Cunningham (1), Karl-Anthony Towns (1), Kevin Love (1), Amar'e Stoudemire (1), Paolo Banchero (1), Danny Granger (1), Kemba Walker (1), Monta Ellis (1), Jamal Murray (1), LaMelo Ball (1), Julius Randle (1), Yao Ming (1), Derrick Rose (1), Victor Wembanyama (1)

</details>

**Since 2001-02 (through 2025-26), name a player who averaged 20 or more points per game in a regular season (minimum 40 games).**

185 valid answers, difficulty **easy**, tiers: 1: 103, 2: 82 (0 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), James Harden (1), Kevin Durant (1), Kobe Bryant (1), Luka Doncic (1), Joel Embiid (1), Dirk Nowitzki (1), Allen Iverson (1), Stephen Curry (1), Shai Gilgeous-Alexander (1), Russell Westbrook (1), Damian Lillard (1), Carmelo Anthony (1), Tracy McGrady (1), DeMar DeRozan (1), Dwyane Wade (1), Chris Paul (1), Paul Pierce (1), Tim Duncan (1), Bradley Beal (1), Giannis Antetokounmpo (1), Tony Parker (1), Jayson Tatum (1), Pau Gasol (1), Trae Young (1), Joe Johnson (1), Nikola Jokic (1), LaMarcus Aldridge (1), Gilbert Arenas (1), Paul George (1), Vince Carter (1), Isaiah Thomas (1), Dwight Howard (1), Anthony Edwards (1), Anthony Davis (1), Jalen Brunson (1), Jaylen Brown (1), Kyrie Irving (1), Tyrese Maxey (1), Klay Thompson (1), Donovan Mitchell (1), Jamal Crawford (1), Kevin Garnett (1), Zach Randolph (1), Kawhi Leonard (1), Devin Booker (1), Ray Allen (1), Shaquille O'Neal (1), Brook Lopez (1), Jimmy Butler III (1), Ja Morant (1), Zach LaVine (1), Jrue Holiday (1), Chris Bosh (1), Zion Williamson (1), DeMarcus Cousins (1), CJ McCollum (1), Lauri Markkanen (1), Mike Conley (1), Michael Redd (1), Kyle Lowry (1), De'Aaron Fox (1), Nikola Vucevic (1), Rudy Gay (1), Tobias Harris (1), Cade Cunningham (1), Karl-Anthony Towns (1), Kevin Love (1), Amar'e Stoudemire (1), Antawn Jamison (1), Paolo Banchero (1), Danny Granger (1), Kemba Walker (1), Monta Ellis (1), Shawn Marion (1), Jamal Murray (1), LaMelo Ball (1), Lou Williams (1), Julius Randle (1), Richard Jefferson (1), Yao Ming (1), Richard Hamilton (1), Derrick Rose (1), Victor Wembanyama (1), Elton Brand (1), Brandon Ingram (1), Kevin Martin (1), Andrew Wiggins (1), Blake Griffin (1), Chris Webber (1), Collin Sexton (1), Carlos Boozer (1), Jermaine O'Neal (1), Peja Stojakovic (1), Pascal Siakam (1), David West (1), Deni Avdija (1), Jason Richardson (1), Michael Porter Jr. (1), Deron Williams (1), Franz Wagner (1), Khris Middleton (1), Tyler Herro (1), Eric Gordon (2), Desmond Bane (2), Keyonte George (2), Rashard Lewis (2), Al Jefferson (2), Austin Reaves (2), Kristaps Porzingis (2), John Wall (2), Victor Oladipo (2), D'Angelo Russell (2), Michael Jordan (2), Baron Davis (2), Goran Dragic (2), Brandon Roy (2), Anfernee Simons (2), Jordan Clarkson (2), Stephen Jackson (2), Jaren Jackson Jr. (2), Jalen Johnson (2), Allan Houston (2), Caron Butler (2), Dejounte Murray (2), Gordon Hayward (2), Cam Thomas (2), Karl Malone (2), Mike Bibby (2), Jerami Grant (2), Stephon Marbury (2), Al Harrington (2), Kyle Kuzma (2), Corey Maggette (2), Antoine Walker (2), Jalen Rose (2), Metta World Peace (2), Jalen Green (2), Gary Payton (2), Larry Hughes (2), Keldon Johnson (2), Norman Powell (2), Cuttino Mobley (2), Darius Garland (2), Steve Francis (2), Jamal Mashburn (2), Bojan Bogdanovic (2), Jalen Williams (2), John Collins (2), Jerry Stackhouse (2), Bam Adebayo (2), Trey Murphy III (2), Ben Gordon (2), Andrea Bargnani (2), Devin Harris (2), Shareef Abdur-Rahim (2), Malcolm Brogdon (2), David Lee (2), Alperen Sengun (2), Terry Rozier (2), Buddy Hield (2), RJ Barrett (2), Eric Bledsoe (2), Cooper Flagg (2), Miles Bridges (2), Christian Wood (2), Domantas Sabonis (2), Shaedon Sharpe (2), Nickeil Alexander-Walker (2), Glenn Robinson (2), Mikal Bridges (2), Tyrese Haliburton (2), Michael Finley (2), Spencer Dinwiddie (2), Ricky Davis (2), Jordan Poole (2), Coby White (2), Fred VanVleet (2), Kelly Oubre Jr. (2), Dillon Brooks (2), Caris LeVert (2), Brandon Miller (2), Mike James (2002-2014) (2), Tyreke Evans (2), Jabari Parker (2)

</details>

### `franchises`

**Since 2001-02 (through 2025-26), name a player who played for 9 or more different franchises.**

35 valid answers, difficulty **hard**, tiers: 1: 3, 2: 13, 3: 12, 4: 7 (7 at tier 4 or above).

<details><summary>All valid answers</summary>

Isaiah Thomas (1), Jamal Crawford (1), Jeff Green (1), Andre Miller (2), Dennis Schroder (2), Caron Butler (2), Trevor Ariza (2), Rajon Rondo (2), Mike James (2002-2014) (2), D.J. Augustin (2), Drew Gooden (2), Marco Belinelli (2), Jae Crowder (2), Robin Lopez (2), Greg Monroe (2), Matt Barnes (2), JaVale McGee (3), Wayne Ellington (3), Shaun Livingston (3), Seth Curry (3), James Johnson (3), Ish Smith (3), Justin Holiday (3), Joe Smith (3), Eddie House (3), Garrett Temple (3), Anthony Tolliver (3), Delon Wright (3), Mikki Moore (4), James Ennis III (4), Theo Ratliff (4), Steve Novak (4), Ryan Hollins (4), Lou Amundson (4), Tim Frazier (4)

</details>

**Since 2001-02 (through 2025-26), name a player who played for 7 or more different franchises.**

159 valid answers, difficulty **medium**, tiers: 1: 10, 2: 43, 3: 66, 4: 36, 5: 4 (40 at tier 4 or above).

<details><summary>All valid answers</summary>

Russell Westbrook (1), Chris Paul (1), Joe Johnson (1), Vince Carter (1), Isaiah Thomas (1), Dwight Howard (1), Jamal Crawford (1), DeMarcus Cousins (1), Richard Jefferson (1), Jeff Green (1), Andre Miller (2), Thaddeus Young (2), Dennis Schroder (2), Goran Dragic (2), Stephen Jackson (2), Caron Butler (2), Al Harrington (2), Trevor Ariza (2), Larry Hughes (2), Danilo Gallinari (2), Wesley Matthews (2), Jerry Stackhouse (2), Mo Williams (2), Raymond Felton (2), George Hill (2), Rajon Rondo (2), Christian Wood (2), Marcus Morris Sr. (2), Mike Miller (2), DeAndre Jordan (2), Tyson Chandler (2), Mike James (2002-2014) (2), Jarrett Jack (2), D.J. Augustin (2), Drew Gooden (2), Taj Gibson (2), Aaron Brooks (2), Marco Belinelli (2), Ersan Ilyasova (2), Michael Beasley (2), Kelly Olynyk (2), Jae Crowder (2), Alec Burks (2), Patty Mills (2), Robin Lopez (2), Greg Monroe (2), Marcus Thornton (2), Markieff Morris (2), CJ Miles (2), Juwan Howard (2), Matt Barnes (2), Courtney Lee (2), Jose Calderon (2), Randy Foye (3), Avery Bradley (3), Nate Robinson (3), Corey Brewer (2008-2020) (3), Ramon Sessions (3), JaVale McGee (3), Mason Plumlee (3), Beno Udrih (3), Jared Dudley (3), Gerald Green (3), P.J. Tucker (3), Kurt Thomas (3), James Posey (3), Austin Rivers (3), Jodie Meeks (3), Cory Joseph (3), Wayne Ellington (3), Doug McDermott (3), Rasual Butler (3), Vladimir Radmanovic (3), Patrick Beverley (3), Shaun Livingston (3), Seth Curry (3), James Johnson (3), Steve Blake (3), Ish Smith (3), Jeremy Lin (3), Earl Boykins (3), DeMarre Carroll (3), Nazr Mohammed (3), Dario Saric (3), Tyus Jones (3), Justin Holiday (3), Kris Humphries (3), Chucky Atkins (3), Joe Smith (3), Anthony Morrow (3), Lance Stephenson (3), Eddie House (3), Jerryd Bayless (3), Ronald Murray (3), Keyon Dooling (3), Jamaal Magloire (3), Garrett Temple (3), Omri Casspi (3), Bismack Biyombo (3), Anthony Tolliver (3), Keith Bogans (3), Ed Davis (3), Reggie Bullock Jr. (3), Cameron Payne (3), Dante Cunningham (3), Kwame Brown (3), Sebastian Telfair (3), Carlos Arroyo (3), Brevin Knight (3), Maurice Evans (3), Delon Wright (3), Langston Galloway (3), Dahntay Jones (3), Roger Mason Jr. (3), Reggie Evans (3), Shannon Brown (3), Jannero Pargo (3), Dewayne Dedmon (3), Mike Muscala (3), Shelvin Mack (4), Toney Douglas (4), Sasha Pavlovic (4), Brandan Wright (4), Tyler Zeller (4), Mikki Moore (4), James Ennis III (4), Mo Bamba (4), Brian Skinner (4), Svi Mykhailiuk (4), Josh McRoberts (4), Malik Allen (4), Theo Ratliff (4), Ronny Turiaf (4), Nik Stauskas (4), Troy Daniels (4), Steve Novak (4), Von Wafer (4), Kevin Ollie (4), Ryan Hollins (4), Jason Hart (4), Shawne Williams (4), Noah Vonleh (4), Justin Jackson (4), Lou Amundson (4), Shelden Williams (4), Moses Brown (4), Tim Frazier (4), Damian Jones (4), Josh Powell (4), Earl Barron (4), Shaquille Harrison (4), Stephen Graham (4), Dominic McGuire (4), Calvin Booth (4), Wenyen Gabriel (4), Mike Wilks (5), Linton Johnson (5), DeAndre Liggins (5), Anthony Goldwire (5)

</details>

**Since 2001-02 (through 2025-26), name a player who played for 6 or more different franchises.**

284 valid answers, difficulty **medium**, tiers: 1: 18, 2: 66, 3: 120, 4: 69, 5: 11 (80 at tier 4 or above).

<details><summary>All valid answers</summary>

James Harden (1), Russell Westbrook (1), Carmelo Anthony (1), Tracy McGrady (1), Chris Paul (1), Joe Johnson (1), Vince Carter (1), Isaiah Thomas (1), Dwight Howard (1), Jamal Crawford (1), DeMarcus Cousins (1), Jason Terry (1), Antawn Jamison (1), Lou Williams (1), Richard Jefferson (1), Derrick Rose (1), Jermaine O'Neal (1), Jeff Green (1), Andre Miller (2), Thaddeus Young (2), Kristaps Porzingis (2), Victor Oladipo (2), Jonas Valanciunas (2), Dennis Schroder (2), Goran Dragic (2), Stephen Jackson (2), JJ Redick (2), Caron Butler (2), Kyle Korver (2), Al Harrington (2), Trevor Ariza (2), Metta World Peace (2), Larry Hughes (2), Danilo Gallinari (2), Andre Drummond (2), Bojan Bogdanovic (2), Wesley Matthews (2), Jerry Stackhouse (2), Hedo Turkoglu (2), Mo Williams (2), Buddy Hield (2), Raymond Felton (2), Mike Dunleavy (2), Kentavious Caldwell-Pope (2), George Hill (2), Rajon Rondo (2), Christian Wood (2), Marcus Morris Sr. (2), Jameer Nelson (2), Mike Miller (2), DeAndre Jordan (2), Tyson Chandler (2), Mike James (2002-2014) (2), Jarrett Jack (2), D.J. Augustin (2), Jabari Parker (2), Darren Collison (2), Drew Gooden (2), Brandon Knight (2), Taj Gibson (2), Aaron Brooks (2), Marco Belinelli (2), Ersan Ilyasova (2), Michael Beasley (2), Kelly Olynyk (2), Jae Crowder (2), Alec Burks (2), Patty Mills (2), Robin Lopez (2), Greg Monroe (2), John Salmons (2), Marcus Thornton (2), Danny Green (2), Montrezl Harrell (2), Markieff Morris (2), CJ Miles (2), Arron Afflalo (2), Juwan Howard (2), Nick Young (2), Ryan Anderson (2), Matt Barnes (2), Courtney Lee (2), Jose Calderon (2), Channing Frye (2), Troy Murphy (3), Randy Foye (3), Zaza Pachulia (3), Avery Bradley (3), Nate Robinson (3), Tristan Thompson (3), Raja Bell (3), Corey Brewer (2008-2020) (3), Ramon Sessions (3), JaVale McGee (3), Mason Plumlee (3), Beno Udrih (3), Michael Carter-Williams (3), Rafer Alston (3), Brandon Bass (3), Malik Beasley (3), Josh Richardson (3), Samuel Dalembert (3), Jared Dudley (3), Tim Thomas (3), Gerald Green (3), P.J. Tucker (3), Kurt Thomas (3), James Posey (3), Austin Rivers (3), Jodie Meeks (3), Cory Joseph (3), Wayne Ellington (3), Doug McDermott (3), Rasual Butler (3), Vladimir Radmanovic (3), Taurean Prince (3), Spencer Hawes (3), Patrick Beverley (3), DeShawn Stevenson (3), Shaun Livingston (3), Seth Curry (3), Dennis Smith Jr. (3), James Johnson (3), Steve Blake (3), Marreese Speights (3), Wesley Person (3), Al-Farouq Aminu (3), Ish Smith (3), Jeremy Lin (3), Donyell Marshall (3), Earl Boykins (3), DeMarre Carroll (3), Nazr Mohammed (3), Rodney Hood (3), Earl Watson (3), Dario Saric (3), Tyus Jones (3), Kyle Anderson (3), Justin Holiday (3), Kris Humphries (3), Chucky Atkins (3), Joe Smith (3), Anthony Morrow (3), Lance Stephenson (3), Eddie House (3), Lee Nailon (3), Jerryd Bayless (3), Bruce Brown (3), Antonio Daniels (3), Ronald Murray (3), Greivis Vasquez (3), Hakim Warrick (3), Ronnie Brewer (3), Keyon Dooling (3), Jamaal Magloire (3), Garrett Temple (3), Alex Len (3), Omri Casspi (3), Bismack Biyombo (3), Kris Dunn (3), Luc Mbah a Moute (3), Maurice Harkless (3), Anthony Tolliver (3), Thomas Bryant (3), Monte Morris (3), Tyronn Lue (3), Keith Bogans (3), Sean Kilpatrick (3), Ed Davis (3), Derrick Jones Jr. (3), Reggie Bullock Jr. (3), Primoz Brezec (3), Cameron Payne (3), Shake Milton (3), Wesley Johnson (3), Dante Cunningham (3), Landry Shamet (3), Kwame Brown (3), Sebastian Telfair (3), Carlos Arroyo (3), Brevin Knight (3), Maurice Evans (3), Delon Wright (3), Dan Dickau (3), Jason Smith (3), Derrick Williams (3), Gary Neal (3), Tony Snell (3), Anthony Johnson (3), Langston Galloway (3), Damien Wilkins (3), Dahntay Jones (3), Isaiah Hartenstein (3), Devin Brown (3), Roger Mason Jr. (3), Reggie Evans (3), Jason Kapono (3), Glenn Robinson III (3), Nerlens Noel (3), Shannon Brown (3), Jannero Pargo (3), Dewayne Dedmon (3), Smush Parker (3), Mike Muscala (3), Shelvin Mack (4), Daniel Theis (4), Toney Douglas (4), Torrey Craig (4), Isaiah Canaan (2014-2019) (4), Sasha Pavlovic (4), Brandan Wright (4), Tyler Zeller (4), Jason Collins (4), Darko Milicic (4), Mikki Moore (4), James Ennis III (4), Mo Bamba (4), Alonzo Gee (4), Eric Williams (4), Brian Skinner (4), Danuel House Jr. (4), Svi Mykhailiuk (4), Jevon Carter (4), Shabazz Napier (4), Luke Kornet (4), Josh McRoberts (4), Drew Eubanks (4), Malik Allen (4), Theo Ratliff (4), Ronny Turiaf (4), Nik Stauskas (4), Troy Daniels (4), Steve Novak (4), Anthony Carter (4), Von Wafer (4), Brian Cardinal (4), Kevin Ollie (4), Ronnie Price (4), Boban Marjanovic (4), Kenny Anderson (4), Ryan Hollins (4), Jason Hart (4), Francisco Elson (4), Shawne Williams (4), Juancho Hernangomez (4), Noah Vonleh (4), Justin Jackson (4), Lou Amundson (4), Shelden Williams (4), Quincy Acy (4), Thomas Robinson (4), Moses Brown (4), Tim Frazier (4), Damian Jones (4), Justin Anderson (4), Shammond Williams (4), Ike Diogu (4), Josh Powell (4), Cartier Martin (4), John Lucas III (4), Earl Clark (4), David Roddy (4), Cole Aldrich (4), Tony Bradley (4), Earl Barron (4), Shaquille Harrison (4), Stephen Graham (4), Dominic McGuire (4), Hilton Armstrong (4), Calvin Booth (4), Solomon Jones (4), Rick Brunson (4), Wenyen Gabriel (4), Jamaree Bouyea (5), Lonny Baxter (5), Mike Wilks (5), Linton Johnson (5), Eddie Gill (5), DeAndre Liggins (5), Bobby Jones (5), Jared Cunningham (5), Andre Barrett (5), Anthony Goldwire (5), Alize Johnson (5)

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

10 valid answers, difficulty **easy**, tiers: 1: 10 (0 at tier 4 or above).

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

11 valid answers, difficulty **easy**, tiers: 1: 11 (0 at tier 4 or above).

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
