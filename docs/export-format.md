# Export format (session 5)

`python3 pipeline/export.py` writes two files to `data/export/` (committed, not gitignored). The website copies them to `web/public/` (session 6). Both follow the schemas in `schema/` and are checked against them on every run.

## prompts.json

A JSON array of **63 prompts**, one prompt per line. It is read as a plain array, so the order of the file is the order of the game.

**Dives.** Dive N (counting from 0) is the prompts at positions `7N` to `7N + 6`. There are 9 dives, so positions 0 to 62. Nothing in the file marks a dive; the position is the contract. A prompt appears once in the whole file.

**Inside a dive:** 5 player prompts and 2 team prompts. The team prompts are always the 3rd and 5th prompt of the dive (positions `7N + 2` and `7N + 4`). Within the players, and within the teams, prompts run from easy to hard, so a dive starts easy. Every dive has at least one easy, one medium and one hard prompt, and never two prompts from the same template (a test checks both on the real file). At most 2 thresholds of any template are used in the whole file.

**A prompt:**

```json
{"id":"p-points-regular-50","answerType":"player","text":"Since 2001-02 (through 2025-26), name a player who scored 50 or more points in a regular-season game.","answers":[{"id":"pl-3992","name":"James Harden","tier":1,"points":10}],"difficulty":"easy"}
```

- `id`: `p-` plus the template and threshold. Stable: the same prompt always has the same id, whatever its position.
- `text`: always starts with the era. The data's season 2002 is the 2001-02 season (the first game is 2001-10-30), so the era reads "Since 2001-02 (through 2025-26)", not "Since 2002". The "(through ...)" part says where the data stops.
- `answers`: every valid answer, best known first (tier 1 to 6, then by fame rank). Players need at least 15 and at most 400; teams at least 5.
- `tier` and `points` always pair: 1 = 10, 2 = 20, 3 = 35, 4 = 55, 5 = 75, 6 = 100.
- Player answers are named by the universe name (`unique_name`: people who share a display name carry their seasons). Team answers are the franchise under its current name; a franchise that qualified only under an older name (for example the Seattle SuperSonics for the Oklahoma City Thunder) is tier 4, and under its current name tier 1.
- `difficulty`: `easy`, `medium` or `hard`, from the number of valid answers and the share of tier 4 and above answers (see `difficulty()` in `pipeline/generator.py`).

## universe.json

An object `{"players": [...], "teams": [...]}` with one entry per line, `{"id", "name", "aliases"}`:

- **players:** all 2,520 players in the data, id `pl-<athlete id>`. Two people with the same display name stay separate entries and are told apart in `name`, for example `Mike James (2002-2014)` and `Mike James (2018-2021)`; the matcher drops the bracket to ask "which one?". Aliases are other spellings of the name (the data's own spellings, `pipeline/data/aliases.csv`).
- **teams:** all 30 franchises, id `tm-<team id>`, named by the current franchise name. Aliases are the names the franchise used before, its nicknames, unique city names, abbreviations of three or more letters and the short forms in `pipeline/data/team_aliases.csv`.
- An alias is dropped if another entry claims it or it is another entry's name (for example "Hornets", which both the Charlotte and the New Orleans franchise used). The export prints how many were dropped.

## Not in the export

`pipeline/data/outside_range.csv` (about 150 famous players from before 2001-02) is only for the "outside the data range" message. It is checked against the universe on every run (no name in it may read as a universe name or alias) but it is not exported yet; the website reads the CSV in a later session.

## Checks run by `export.py`

Both files validate against the schemas; every answer id is in the universe with the same name; every point value matches its tier; ids and names are unique; no alias points at two entries; and 10 random prompts are recomputed from the processed tables by an independent brute-force query (`pipeline/bruteforce.py`) and compared answer by answer. The result is in docs/prompts-sample.md.
