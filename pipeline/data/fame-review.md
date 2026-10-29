Written by hand after reading the numbers above (the rest of this file is generated).

**Fixed in session 5.** The score now takes the best of five ranks (career points, rebounds, assists, steals plus blocks, best points per game), so Ben Wallace (decided by steals plus blocks) moved from tier 3 to tier 1 and every other sanity name passes. Six Hall of Famers whose prime was before 2001-02 have hand-set tiers (table above): Michael Jordan and Karl Malone tier 1; John Stockton, Scottie Pippen, Reggie Miller and Patrick Ewing tier 2.

**Still wrong:**

- **Chet Holmgren is tier 3 (10.63%).** The sanity list expects tier 2 or better for a top-pick young defender. He has played few seasons (3,746 career points, 17.1 points per game at best) and none of the five metrics lifts him into the top 10%. I did not add an override because nothing in the data proves it; it needs an owner decision (add him to `fame_overrides.csv` if you agree).
- **Tier 1 is crowded: 187 players (7.4%) against a nominal 3%, and tiers 1 and 2 hold 471 (18.7%) against 10%.** Taking the best of five ranks lets a player in through any of five doors, including some who are very good at one counting stat but not household names (Andre Drummond, Josh Smith and Brook Lopez are all tier 1). The cutoffs were kept as asked. If the bands should be fuller or emptier, the cutoffs are the lever.
- **Players with a pre-2002 prime who are not in the override file are still judged on a partial career** (for example Alonzo Mourning, tier 3, whose data covers 2001-02 to 2007-08 only). I only overrode players where the gap is large and the name is beyond doubt.
- **Points per game is regular season only** (at least 40 games, games for all teams added up); career points include the playoffs.
- **Most lists are mostly well-known players.** Because tiers are global and the top bands are full, 47 of the 53 player candidates have fewer than 10% of their answers at tier 4 or above, and none has 25% or more (the highest is 19%, blocks 6 or more). Difficulty cutoffs were re-set for this (see `difficulty()` in `pipeline/generator.py`).
