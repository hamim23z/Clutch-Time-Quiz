# Export format (session 5)

`python3 pipeline/export.py` writes two files to `data/export/` (committed, not gitignored). The website copies them to `web/public/` (session 6). Both follow the schemas in `schema/` and are checked against them on every run.

## prompts.json

A JSON array of **504 prompts** (72 dives), one prompt per line. It is read as a plain array, so the order of the file is the order of the game.

**Dives.** Dive N (counting from 0) is the prompts at positions `7N` to `7N + 6`. There are 72 dives, so positions 0 to 503. Nothing in the file marks a dive; the position is the contract. A prompt appears once in the whole file, and the website can take `N modulo 72`.

**Inside a dive:** 5 player prompts and 2 team prompts. The team prompts are always the 3rd and 5th prompt of the dive (positions `7N + 2` and `7N + 4`). Rules, all checked by `violations()` in `pipeline/curate.py` and again by a test on the committed file:

- at least 2 of the 5 player prompts are broad-pool prompts (role players are valid answers; see below);
- at least one easy, one medium and one hard prompt;
- no two prompts from the same template family, and none about the same franchise or the same star;
- neighbouring dives share no franchise or star either;
- within the players, and within the teams, prompts run from easy to hard.

Across the file, a family only repeats with a clearly different parameter (another franchise, season, month or star), never the same question at a nearby threshold, and at most 30 prompts come from one family.

**A prompt** (answers cut to one for the example; the real list is every valid answer):

```json
{"id":"p-franchise-season-13-2008","answerType":"player","text":"Since 2001-02 (through 2025-26), name a player who played for the Los Angeles Lakers in a regular-season game in the 2007-08 season.","answers":[{"id":"pl-110","name":"Kobe Bryant","tier":1,"points":10}],"difficulty":"hard"}
```

- `id`: `p-` plus the template or family and its parameters (franchise id, season, month, star id, threshold). Stable: the same prompt always has the same id, whatever its position.
- `text`: always starts with the era. The data's season 2002 is the 2001-02 season (the first game is 2001-10-30), so the era reads "Since 2001-02 (through 2025-26)", not "Since 2002". The "(through ...)" part says where the data stops. A season in a prompt is written the same way (2007-08); a Finals is named by its year (the 2008 NBA Finals).
- `answers`: every valid answer, best known first (tier 1 to 6, then by fame rank). Broad-pool player prompts have 15 to 700 answers, the older star-heavy templates 15 to 400, team prompts 5 or more (the new team families at most 24 of the 30 franchises).
- `tier` and `points` always pair: 1 = 10, 2 = 20, 3 = 35, 4 = 55, 5 = 75, 6 = 100.
- Player answers are named by the universe name (`unique_name`: people who share a display name carry their seasons). Team answers are the franchise under its current name; a franchise that qualified only under an older name (for example the Seattle SuperSonics for the Oklahoma City Thunder) is tier 4, and under its current name tier 1.
- `difficulty`: `easy`, `medium` or `hard`, from the number of valid answers and the share of tier 4 and above answers (see `difficulty()` in `pipeline/generator.py`).

**Template families.** The older templates (`pipeline/templates.py`) are star-heavy: a stat threshold in a game. The families in `pipeline/pools.py` take parameters. Broad player families: played for a franchise (any time, in the playoffs, in a season, in a five-season window, as a starter, off the bench, with N points, against a franchise), played for both of two franchises, played in a game alongside one of 100 stars, appeared in the Finals (any, with a three, with a steal or block, in a given year), and points, threes, rebounds or assists in a game in a given month or season. Team families: made the playoffs, wins, home and road wins, playoff wins, regulation points, winning margin, threes, holding an opponent down and overtime wins in a given season, and playing or winning a playoff game against a given franchise. docs/curation-report.md lists the families in use; docs/prompt-candidates.md all candidates.

## universe.json

An object `{"players": [...], "teams": [...]}` with one entry per line, `{"id", "name", "aliases"}`:

- **players:** all 2,520 players in the data, id `pl-<athlete id>`. Two people with the same display name stay separate entries and are told apart in `name`, for example `Mike James (2002-2014)` and `Mike James (2018-2021)`; the matcher drops the bracket to ask "which one?". Aliases are other spellings of the name (the data's own spellings, `pipeline/data/aliases.csv`).
- **teams:** all 30 franchises, id `tm-<team id>`, named by the current franchise name. Aliases are the names the franchise used before, its nicknames, unique city names, abbreviations of three or more letters and the short forms in `pipeline/data/team_aliases.csv`.
- An alias is dropped if another entry claims it or it is another entry's name (for example "Hornets", which both the Charlotte and the New Orleans franchise used). The export prints how many were dropped.

## Not in the export

`pipeline/data/outside_range.csv` (about 150 famous players from before 2001-02) is only for the "outside the data range" message. It is checked against the universe on every run (no name in it may read as a universe name or alias) but it is not exported yet; the website reads the CSV in a later session.

## Checks run by `export.py`

Both files validate against the schemas; the rarity targets hold (tiers 1 and 2 together at most 45% of all valid answers, tiers 5 and 6 together at least 12%, see docs/rarity-report.md); every answer id is in the universe with the same name; every point value matches its tier; ids and names are unique; no alias points at two entries; and at least 60 prompts (2 from every template family) are recomputed from the processed tables by an independent brute-force query (`pipeline/bruteforce.py`) and compared answer by answer. The result is in docs/prompts-sample.md.
