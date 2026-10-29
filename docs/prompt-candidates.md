# Prompt candidates

Written by `python3 pipeline/generate.py`; do not edit by hand.

- **Era wording:** every prompt starts with "Since 2001-02 (through 2025-26)". The data's season 2002 is the 2001-02 season (the first game is on 2001-10-30), so "Since 2002" would leave out three months of games. The schema requires the text to start with "Since" and four digits, which this does.
- **Valid answers:** players need 15 to 400; teams need at least 5.
- **Player tiers** come from the fame score (docs/fame-report.md). **Team tiers:** a team is tier 1 (10 points) if it qualified under its current name in any qualifying season, tier 4 (55 points) if only under a historical name. Every team answer is the franchise, shown by its current name; the other names it used are aliases for the answer matcher.
- **Difficulty:** from the number of valid answers and the share of tier 4 and above (see `difficulty()` in `pipeline/generator.py`).

## Totals

- Candidates: **72** (53 player, 19 team).
- Tried: 87 template and threshold combinations. Dropped for too few valid answers: 10. Dropped for too many: 5.
- By difficulty: easy 43, hard 5, medium 24.

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

290 valid answers, difficulty **medium**, tiers: 1: 87, 2: 98, 3: 62, 4: 34, 5: 8, 6: 1 (43 at tier 4 or above).

<details><summary>All valid answers</summary>

LeBron James (1), Dwight Howard (1), Kevin Durant (1), Tim Duncan (1), Russell Westbrook (1), Luka Doncic (1), Pau Gasol (1), Joel Embiid (1), Dirk Nowitzki (1), Kevin Garnett (1), Ben Wallace (1), Anthony Davis (1), Shai Gilgeous-Alexander (1), Andre Drummond (1), Rajon Rondo (1), Damian Lillard (1), Brook Lopez (1), Rudy Gobert (1), Jason Kidd (1), Carmelo Anthony (1), Josh Smith (1), DeAndre Jordan (1), Tyson Chandler (1), Nikola Vucevic (1), Paul Pierce (1), Zach Randolph (1), Shawn Marion (1), Al Horford (1), Giannis Antetokounmpo (1), Kevin Love (1), Nikola Jokic (1), Jayson Tatum (1), Andrei Kirilenko (1), Draymond Green (1), LaMarcus Aldridge (1), Jonas Valanciunas (1), Paul Millsap (1), Serge Ibaka (1), Elton Brand (1), Carlos Boozer (1), Marcus Camby (1), Karl-Anthony Towns (1), Chris Bosh (1), Marc Gasol (1), Clint Capela (1), Al Jefferson (1), Shaquille O'Neal (1), Jimmy Butler III (1), Lamar Odom (1), DeMarcus Cousins (1), David Lee (1), Lauri Markkanen (1), Julius Randle (1), David West (1), Domantas Sabonis (1), Tobias Harris (1), Amar'e Stoudemire (1), Tristan Thompson (1), Antawn Jamison (1), Samuel Dalembert (1), Paolo Banchero (1), Jermaine O'Neal (1), Marcin Gortat (1), Steven Adams (1), Gerald Wallace (1), Nicolas Batum (1), Richard Jefferson (1), Yao Ming (1), Joakim Noah (1), Zaza Pachulia (1), Blake Griffin (1), Victor Wembanyama (1), Kenyon Martin (1), Andrew Bogut (1), Udonis Haslem (1), Bam Adebayo (1), Chris Webber (1), JaVale McGee (1), Pascal Siakam (1), Mason Plumlee (1), Enes Freedom (1), Deni Avdija (1), Taj Gibson (1), Jarrett Allen (1), Reggie Evans (1), Drew Gooden (1), Karl Malone (1), Zydrunas Ilgauskas (2), Emeka Okafor (2), Luol Deng (2), Rashard Lewis (2), Derrick Favors (2), Jusuf Nurkic (2), Marvin Williams (2), Kristaps Porzingis (2), Brendan Haywood (2), Hassan Whiteside (2), Roy Hibbert (2), Kurt Thomas (2), Troy Murphy (2), Chris Kaman (2), Brad Miller (2), Caron Butler (2), Ivica Zubac (2), Erick Dampier (2), Bobby Portis (2), Jalen Johnson (2), Greg Monroe (2), P.J. Tucker (2), Hedo Turkoglu (2), Bismack Biyombo (2), Chris Andersen (2), Kendrick Perkins (2), Deandre Ayton (2), Amir Johnson (2), Ben Simmons (2), Al Harrington (2), Kyle Kuzma (2), Luis Scola (2), Corey Maggette (2), Antoine Walker (2), Keldon Johnson (2), Danilo Gallinari (2), Jeff Foster (2), Nick Collison (2), Anderson Varejao (2), Ersan Ilyasova (2), John Collins (2), Robin Lopez (2), Mehmet Okur (2), Ed Davis (2), Josh Hart (2), Shareef Abdur-Rahim (2), Nazr Mohammed (2), Mike Miller (2), Jakob Poeltl (2), Corey Brewer (2008-2020) (2), Alperen Sengun (2), Al-Farouq Aminu (2), Mike Dunleavy (2), Antonio McDyess (2), Kris Humphries (2), Christian Wood (2), Kelly Olynyk (2), Jamaal Magloire (2), P.J. Brown (2), Kevon Looney (2), Kenneth Faried (2), Wendell Carter Jr. (2), Jason Thompson (2), Josh Giddey (2), Mitchell Robinson (2), Andrew Bynum (2), Andris Biedrins (2), Josh Howard (2), Kenny Thomas (2), Scottie Barnes (2), Alex Len (2), Joel Przybilla (2), JJ Hickson (2), Larry Nance Jr. (2), James Posey (2), Ryan Anderson (2), Omer Asik (2), Gorgui Dieng (2), Jalen Duren (2), Donyell Marshall (2), Kwame Brown (2), Adonal Foyle (2), Evan Mobley (2), Chuck Hayes (2), Montrezl Harrell (2), Andray Blatche (2), Isaiah Hartenstein (2), Robert Horry (2), JaMychal Green (2), Amen Thompson (2), Jared Dudley (2), Chris Wilcox (2), Dikembe Mutombo (2), Matt Harpring (2), Charlie Villanueva (2), P.J. Washington (2), Marreese Speights (2), Luc Mbah a Moute (2), Nikola Pekovic (3), Trevor Booker (3), Chet Holmgren (3), John Henson (3), Trey Lyles (3), Bonzi Wells (3), Onyeka Okongwu (3), Naz Reid (3), Lorenzen Wright (3), Dorell Wright (3), Keith Van Horn (3), Mark Blount (3), Richaun Holmes (3), Jabari Smith Jr. (3), Alonzo Mourning (3), Malik Rose (3), Isaiah Stewart (3), Willie Cauley-Stein (3), Brian Skinner (3), Anthony Tolliver (3), Andres Nocioni (3), Timofey Mozgov (3), Mark Williams (3), Precious Achiuwa (3), Dale Davis (3), Brian Grant (3), Jarred Vanderbilt (3), Dan Gadzuric (3), Marvin Bagley III (3), DeJuan Blair (3), Vlade Divac (3), Chris Boucher (3), Jared Sullinger (3), Chris Mihm (3), Elden Campbell (3), Mo Bamba (3), Eddie Griffin (3), Kelvin Cato (3), Greg Ostertag (3), Thomas Bryant (3), Michael Olowokandi (3), Larry Sanders (3), Lavoy Allen (3), Walker Kessler (3), Jerome Williams (3), Noah Vonleh (3), Primoz Brezec (3), Shawn Bradley (3), Jalen Smith (3), Jim Jackson (3), Nick Richards (3), Francisco Elson (3), Danny Fortson (3), Maxime Raynaud (3), Marcus Fizer (3), David Robinson (3), Miles Plumlee (3), Donovan Clingan (3), Thomas Robinson (3), Yi Jianlian (3), Derik Queen (3), Jeremy Sochan (3), Kyle Filipowski (4), Clarence Weatherspoon (4), Anthony Mason (4), Kel'el Ware (4), Boban Marjanovic (4), Josh Boone (4), Christian Laettner (4), Cole Aldrich (4), Ervin Johnson (4), Jordan Goodwin (4), Byron Mullens (4), Aaron Gray (4), Jericho Sims (4), Moussa Diabate (4), Alan Henderson (4), Neemias Queta (4), Jabari Walker (4), Tarik Black (4), James Singleton (4), Chimezie Metu (4), Zach Edey (4), Jahidi White (4), Moses Brown (4), Cheick Diallo (4), Greg Oden (4), Dominick Barlow (4), Kris Murray (4), Hakeem Olajuwon (4), Willie Reed (4), Omer Yurtseven (4), Mouhamed Gueye (4), Joey Dorsey (4), Greg Smith (4), Earl Barron (4), Oscar Tshiebwe (5), Alize Johnson (5), Moussa Cisse (5), Jaylen Hoard (5), Andre Brown (5), Vitor Faverani (5), Julian Reese (5), Solomon Alabi (5), Adama Sanogo (6)

</details>

### `assists`

**Since 2001-02 (through 2025-26), name a player who recorded 20 or more assists in a game.**

27 valid answers, difficulty **hard**, tiers: 1: 16, 2: 8, 3: 2, 4: 1 (1 at tier 4 or above).

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

21 valid answers, difficulty **hard**, tiers: 1: 9, 2: 7, 3: 3, 4: 2 (2 at tier 4 or above).

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

20 valid answers, difficulty **hard**, tiers: 1: 13, 2: 5, 3: 1, 4: 1 (1 at tier 4 or above).

<details><summary>All valid answers</summary>

Dwight Howard (1), Ben Wallace (1), Anthony Davis (1), Josh Smith (1), Andrei Kirilenko (1), Serge Ibaka (1), Marcus Camby (1), Clint Capela (1), Amar'e Stoudemire (1), Jermaine O'Neal (1), Joakim Noah (1), Victor Wembanyama (1), JaVale McGee (1), Emeka Okafor (2), Hassan Whiteside (2), Roy Hibbert (2), Andrew Bynum (2), Dikembe Mutombo (2), Larry Sanders (3), Calvin Booth (4)

</details>

**Since 2001-02 (through 2025-26), name a player who blocked 8 or more shots in a game.**

65 valid answers, difficulty **medium**, tiers: 1: 25, 2: 20, 3: 14, 4: 5, 5: 1 (6 at tier 4 or above).

<details><summary>All valid answers</summary>

Dwight Howard (1), Tim Duncan (1), Pau Gasol (1), Ben Wallace (1), Anthony Davis (1), Brook Lopez (1), Rudy Gobert (1), Josh Smith (1), DeAndre Jordan (1), Andrei Kirilenko (1), Serge Ibaka (1), Elton Brand (1), Marcus Camby (1), Marc Gasol (1), Clint Capela (1), Shaquille O'Neal (1), Myles Turner (1), Amar'e Stoudemire (1), Samuel Dalembert (1), Jermaine O'Neal (1), Yao Ming (1), Joakim Noah (1), Victor Wembanyama (1), Andrew Bogut (1), JaVale McGee (1), Emeka Okafor (2), Hassan Whiteside (2), Roy Hibbert (2), Chris Kaman (2), Erick Dampier (2), Jaren Jackson Jr. (2), Chris Andersen (2), Jerami Grant (2), Robin Lopez (2), Nazr Mohammed (2), Nerlens Noel (2), Theo Ratliff (2), Mitchell Robinson (2), Andrew Bynum (2), Rasho Nesterovic (2), Joel Przybilla (2), Adonal Foyle (2), Evan Mobley (2), Daniel Gafford (2), Dikembe Mutombo (2), Stromile Swift (3), Tyrus Thomas (3), Chet Holmgren (3), Raef LaFrentz (3), Alonzo Mourning (3), Robert Williams III (3), Isaiah Stewart (3), Joel Anthony (3), Eddie Griffin (3), Greg Ostertag (3), Larry Sanders (3), Walker Kessler (3), Shawn Bradley (3), Donovan Clingan (3), Keon Clark (4), Anthony Randolph (4), Calvin Booth (4), Sean Williams (4), Hakeem Olajuwon (4), Mamadou N'diaye (5)

</details>

**Since 2001-02 (through 2025-26), name a player who blocked 6 or more shots in a game.**

215 valid answers, difficulty **medium**, tiers: 1: 63, 2: 56, 3: 56, 4: 32, 5: 7, 6: 1 (40 at tier 4 or above).

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

35 valid answers, difficulty **hard**, tiers: 1: 10, 2: 14, 3: 8, 4: 3 (3 at tier 4 or above).

<details><summary>All valid answers</summary>

Rajon Rondo (1), Andre Miller (1), Isaiah Thomas (1), Jamal Crawford (1), Dennis Schroder (1), Trevor Ariza (1), D.J. Augustin (1), JaVale McGee (1), Jeff Green (1), Drew Gooden (1), Caron Butler (2), Greg Monroe (2), Ish Smith (2), Shaun Livingston (2), Robin Lopez (2), Matt Barnes (2), James Johnson (2), Jae Crowder (2), Theo Ratliff (2), Mike James (2002-2014) (2), Joe Smith (2), Marco Belinelli (2), Justin Holiday (2), Delon Wright (2), Garrett Temple (3), Wayne Ellington (3), Anthony Tolliver (3), Seth Curry (3), Tim Frazier (3), Eddie House (3), Mikki Moore (3), Lou Amundson (3), James Ennis III (4), Ryan Hollins (4), Steve Novak (4)

</details>

**Since 2001-02 (through 2025-26), name a player who played for 7 or more different franchises.**

159 valid answers, difficulty **medium**, tiers: 1: 28, 2: 64, 3: 44, 4: 22, 5: 1 (23 at tier 4 or above).

<details><summary>All valid answers</summary>

Dwight Howard (1), Chris Paul (1), Russell Westbrook (1), Rajon Rondo (1), DeAndre Jordan (1), Tyson Chandler (1), Andre Miller (1), Joe Johnson (1), Vince Carter (1), Isaiah Thomas (1), Jamal Crawford (1), Jose Calderon (1), Raymond Felton (1), Dennis Schroder (1), DeMarcus Cousins (1), Thaddeus Young (1), Trevor Ariza (1), Goran Dragic (1), Mo Williams (1), Richard Jefferson (1), Jarrett Jack (1), D.J. Augustin (1), JaVale McGee (1), Jeff Green (1), Mason Plumlee (1), Taj Gibson (1), Reggie Evans (1), Drew Gooden (1), Steve Blake (2), Kurt Thomas (2), Tyus Jones (2), Caron Butler (2), Stephen Jackson (2), George Hill (2), Greg Monroe (2), P.J. Tucker (2), Ish Smith (2), Bismack Biyombo (2), Al Harrington (2), Beno Udrih (2), Larry Hughes (2), Ramon Sessions (2), Danilo Gallinari (2), Shaun Livingston (2), Brevin Knight (2), Ersan Ilyasova (2), Wesley Matthews (2), Robin Lopez (2), Jerry Stackhouse (2), Cory Joseph (2), Ed Davis (2), Matt Barnes (2), Nazr Mohammed (2), Mike Miller (2), Corey Brewer (2008-2020) (2), Patrick Beverley (2), James Johnson (2), Kris Humphries (2), Christian Wood (2), Kelly Olynyk (2), Jamaal Magloire (2), Marcus Morris Sr. (2), Jae Crowder (2), Markieff Morris (2), Theo Ratliff (2), Juwan Howard (2), Mike James (2002-2014) (2), Patty Mills (2), Randy Foye (2), Jeremy Lin (2), Earl Boykins (2), Courtney Lee (2), Aaron Brooks (2), James Posey (2), Joe Smith (2), Marco Belinelli (2), Sebastian Telfair (2), Michael Beasley (2), Nate Robinson (2), Kwame Brown (2), Alec Burks (2), Marcus Thornton (2), Chucky Atkins (2), Carlos Arroyo (2), CJ Miles (2), Lance Stephenson (2), Jared Dudley (2), Jerryd Bayless (2), Dewayne Dedmon (2), Cameron Payne (2), Justin Holiday (2), Delon Wright (2), Avery Bradley (3), Austin Rivers (3), Vladimir Radmanovic (3), Garrett Temple (3), Shelvin Mack (3), Keyon Dooling (3), Dario Saric (3), Dante Cunningham (3), DeMarre Carroll (3), Ronny Turiaf (3), Gerald Green (3), Jodie Meeks (3), Wayne Ellington (3), Kevin Ollie (3), Brian Skinner (3), Doug McDermott (3), Rasual Butler (3), Anthony Tolliver (3), Seth Curry (3), Ronald Murray (3), Omri Casspi (3), Tim Frazier (3), Eddie House (3), Jannero Pargo (3), Anthony Morrow (3), Mo Bamba (3), Brandan Wright (3), Josh McRoberts (3), Toney Douglas (3), Keith Bogans (3), Tyler Zeller (3), Mikki Moore (3), Noah Vonleh (3), Reggie Bullock Jr. (3), Mike Muscala (3), Maurice Evans (3), Jason Hart (3), Langston Galloway (3), Lou Amundson (3), Shelden Williams (3), Roger Mason Jr. (3), Dahntay Jones (3), Shannon Brown (3), Malik Allen (3), James Ennis III (4), Svi Mykhailiuk (4), Sasha Pavlovic (4), Ryan Hollins (4), Nik Stauskas (4), Dominic McGuire (4), Troy Daniels (4), Calvin Booth (4), Steve Novak (4), Shawne Williams (4), Josh Powell (4), Von Wafer (4), Damian Jones (4), Shaquille Harrison (4), Moses Brown (4), Justin Jackson (4), Mike Wilks (4), Wenyen Gabriel (4), Linton Johnson (4), Earl Barron (4), DeAndre Liggins (4), Stephen Graham (4), Anthony Goldwire (5)

</details>

**Since 2001-02 (through 2025-26), name a player who played for 6 or more different franchises.**

284 valid answers, difficulty **medium**, tiers: 1: 46, 2: 102, 3: 88, 4: 43, 5: 5 (48 at tier 4 or above).

<details><summary>All valid answers</summary>

James Harden (1), Dwight Howard (1), Chris Paul (1), Russell Westbrook (1), Andre Drummond (1), Rajon Rondo (1), Carmelo Anthony (1), Tracy McGrady (1), DeAndre Jordan (1), Tyson Chandler (1), Andre Miller (1), Joe Johnson (1), Jonas Valanciunas (1), Vince Carter (1), Isaiah Thomas (1), Jamal Crawford (1), Jose Calderon (1), Raymond Felton (1), Jason Terry (1), Dennis Schroder (1), DeMarcus Cousins (1), Jameer Nelson (1), Thaddeus Young (1), Trevor Ariza (1), Goran Dragic (1), Metta World Peace (1), Tristan Thompson (1), Antawn Jamison (1), Samuel Dalembert (1), Mo Williams (1), Derrick Rose (1), Jermaine O'Neal (1), Lou Williams (1), Richard Jefferson (1), Jarrett Jack (1), Zaza Pachulia (1), Earl Watson (1), Danny Green (1), D.J. Augustin (1), JaVale McGee (1), Jeff Green (1), Mason Plumlee (1), Darren Collison (1), Taj Gibson (1), Reggie Evans (1), Drew Gooden (1), Steve Blake (2), Kristaps Porzingis (2), Victor Oladipo (2), Kurt Thomas (2), Troy Murphy (2), Tyus Jones (2), Kentavious Caldwell-Pope (2), Caron Butler (2), Rafer Alston (2), Stephen Jackson (2), JJ Redick (2), George Hill (2), Greg Monroe (2), Kyle Korver (2), P.J. Tucker (2), Ish Smith (2), Hedo Turkoglu (2), Bismack Biyombo (2), Al Harrington (2), Beno Udrih (2), Larry Hughes (2), Ramon Sessions (2), Danilo Gallinari (2), Shaun Livingston (2), Brevin Knight (2), Ersan Ilyasova (2), Bojan Bogdanovic (2), Wesley Matthews (2), Robin Lopez (2), Jerry Stackhouse (2), Cory Joseph (2), Ed Davis (2), Matt Barnes (2), Nazr Mohammed (2), Kyle Anderson (2), Mike Miller (2), Corey Brewer (2008-2020) (2), Nerlens Noel (2), Al-Farouq Aminu (2), Buddy Hield (2), Mike Dunleavy (2), Patrick Beverley (2), James Johnson (2), Kris Humphries (2), Christian Wood (2), Kelly Olynyk (2), Jamaal Magloire (2), Marcus Morris Sr. (2), Jae Crowder (2), Channing Frye (2), Markieff Morris (2), Theo Ratliff (2), Spencer Hawes (2), John Salmons (2), Antonio Daniels (2), Juwan Howard (2), Mike James (2002-2014) (2), Patty Mills (2), Randy Foye (2), Brandon Bass (2), Jabari Parker (2), Jeremy Lin (2), Alex Len (2), Brandon Knight (2), Earl Boykins (2), Courtney Lee (2), Aaron Brooks (2), James Posey (2), Joe Smith (2), Ryan Anderson (2), Greivis Vasquez (2), Marco Belinelli (2), Sebastian Telfair (2), Maurice Harkless (2), Kris Dunn (2), Michael Beasley (2), Donyell Marshall (2), Nate Robinson (2), Kwame Brown (2), Alec Burks (2), Anthony Johnson (2), Marcus Thornton (2), Montrezl Harrell (2), Chucky Atkins (2), Isaiah Hartenstein (2), Carlos Arroyo (2), CJ Miles (2), Arron Afflalo (2), Lance Stephenson (2), Nick Young (2), Anthony Carter (2), Jared Dudley (2), Michael Carter-Williams (2), Jerryd Bayless (2), Dewayne Dedmon (2), Cameron Payne (2), Jason Collins (2), Justin Holiday (2), Delon Wright (2), Monte Morris (2), Marreese Speights (2), Luc Mbah a Moute (2), Josh Richardson (3), Tyronn Lue (3), Avery Bradley (3), Austin Rivers (3), Vladimir Radmanovic (3), Raja Bell (3), Wesley Johnson (3), Garrett Temple (3), Malik Beasley (3), Shelvin Mack (3), Keyon Dooling (3), Dario Saric (3), Dante Cunningham (3), Darko Milicic (3), DeMarre Carroll (3), Ronny Turiaf (3), Tim Thomas (3), Gerald Green (3), Derrick Jones Jr. (3), Bruce Brown (3), Dennis Smith Jr. (3), DeShawn Stevenson (3), Jodie Meeks (3), Ronnie Brewer (3), Wayne Ellington (3), Kevin Ollie (3), Brian Skinner (3), Doug McDermott (3), Rasual Butler (3), Anthony Tolliver (3), Taurean Prince (3), Seth Curry (3), Ronald Murray (3), Wesley Person (3), Omri Casspi (3), Tim Frazier (3), Rodney Hood (3), Eddie House (3), Hakim Warrick (3), Jason Smith (3), Jannero Pargo (3), Daniel Theis (3), Anthony Morrow (3), Lee Nailon (3), Torrey Craig (3), Ronnie Price (3), Mo Bamba (3), Brandan Wright (3), Thomas Bryant (3), Josh McRoberts (3), Kenny Anderson (3), Damien Wilkins (3), Toney Douglas (3), Keith Bogans (3), Shake Milton (3), Luke Kornet (3), Tyler Zeller (3), Shabazz Napier (3), Mikki Moore (3), Drew Eubanks (3), Sean Kilpatrick (3), Noah Vonleh (3), Reggie Bullock Jr. (3), Primoz Brezec (3), Landry Shamet (3), Smush Parker (3), Mike Muscala (3), Maurice Evans (3), Francisco Elson (3), Jason Hart (3), Dan Dickau (3), Derrick Williams (3), Jevon Carter (3), Gary Neal (3), Tony Snell (3), Langston Galloway (3), Lou Amundson (3), Shelden Williams (3), Alonzo Gee (3), Devin Brown (3), Roger Mason Jr. (3), Thomas Robinson (3), Dahntay Jones (3), Rick Brunson (3), Jason Kapono (3), Glenn Robinson III (3), Shannon Brown (3), Malik Allen (3), James Ennis III (4), Svi Mykhailiuk (4), Sasha Pavlovic (4), Boban Marjanovic (4), Isaiah Canaan (2014-2019) (4), Ryan Hollins (4), Eric Williams (4), Cole Aldrich (4), Nik Stauskas (4), Shammond Williams (4), Quincy Acy (4), Danuel House Jr. (4), Brian Cardinal (4), Dominic McGuire (4), Juancho Hernangomez (4), Troy Daniels (4), Calvin Booth (4), Steve Novak (4), Shawne Williams (4), Josh Powell (4), Von Wafer (4), Tony Bradley (4), Damian Jones (4), John Lucas III (4), Shaquille Harrison (4), Hilton Armstrong (4), Earl Clark (4), Moses Brown (4), Justin Jackson (4), Solomon Jones (4), Ike Diogu (4), Mike Wilks (4), Justin Anderson (4), Cartier Martin (4), Wenyen Gabriel (4), David Roddy (4), Linton Johnson (4), Eddie Gill (4), Earl Barron (4), DeAndre Liggins (4), Lonny Baxter (4), Stephen Graham (4), Andre Barrett (4), Jamaree Bouyea (5), Alize Johnson (5), Anthony Goldwire (5), Bobby Jones (5), Jared Cunningham (5)

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
