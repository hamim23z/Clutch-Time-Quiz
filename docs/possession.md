# Possession, ordering and event rules (pipeline core)

How `pipeline/normalize.py` turns raw ESPN play-by-play into `data/processed/events.parquet`.
The raw data has no possession column, so possession is inferred; this page is the
specification, and `pipeline/test_possession.py` and `pipeline/test_normalize.py` check it
on hand-verified sequences.

## What is kept

- Only `period >= 4`: the 4th quarter and every overtime (quarter 5 = OT1, 6 = OT2, ...).
- Only the last 180 seconds of each of those periods (`secs_period <= 180`).
- Possession is inferred from 120 seconds earlier, so the first event in the window already
  knows who has the ball. State resets at the start of every (game, period).
- Clock: `secs_game` comes from `start_game_seconds_remaining` and `secs_period` from
  `start_quarter_seconds_remaining`. Never the `end_*` columns, which hold the clock of the
  *next* event. In overtime both are the overtime clock (300 down to 0), so `secs_game` is
  not "seconds until the end of regulation".
- The clock has whole-second precision except near 0 where tenths are lost; the buzzer
  beater at "0.2 s" shows as 0.0. Nothing here depends on tenths.

## Event types

`event_type` is derived from the raw `type_text` (kept in `detail`), plus `shooting_play` and
`scoring_play`. Timeouts are found by type (`Full Timeout`, `Short Timeout`), never by the
`*_timeout_called` columns, which are always False or missing.

| event_type | Raw plays |
| --- | --- |
| `made_shot` | any shot (`shooting_play`) that scored. Uses `scoring_play`, not the words "makes"/"made", because 2002 text has different wording |
| `shot` | any shot that did not score (includes blocked shots) |
| `free_throw` | `Free Throw - ...` (regular, flagrant, clear path, technical) |
| `foul` | any type containing `Foul`, plus `Offensive Charge` and every `... Technical` |
| `timeout` | `Full Timeout`, `Short Timeout` |
| `rebound` | any type containing `Rebound` (including team rebounds) |
| `turnover` | any type containing `Turnover`, plus `Traveling`. `No Turnover` is `other` |
| `other` | substitutions, jump balls, period markers, reviews, challenges, violations |

`Offensive Foul` is a `foul` and is followed by its own `Offensive Foul Turnover` row.

## Three-point attempts (`is_three`)

True only for `shot` and `made_shot` rows. The rule is the one from the spike, plus a fallback:

1. The play text contains "three point" (case-insensitive; also matches "three pointer" and
   2002's "Three Point Jumper").
2. **Fallback:** the text states a distance of 24 ft or more (`26-foot step back jumpshot`,
   `25 ft ...`). No two-point shot is that long (the arc is 23 ft 9 in).

Why the fallback exists: in 2024, about 1 in 8 threes never says "three point" (step-back
jumpshots are the usual wording). Measured on the 2024 file, the text rule alone flags 35.0% of
field goal attempts as threes; with the fallback 38.5%; a distance-from-the-hoop estimate from
`coordinate_x/y` gives 39.5%, which matches the league's real 3-point rate. The coordinates
are not used by the pipeline because they are unreliable in the early seasons (2002 has `y`
values up to +-92). The fallback still misses some corner threes with no distance in the text,
roughly 1 in 40, so `is_three` slightly undercounts in recent seasons and is accurate in older ones
(where the text always says "three point").

## Same-timestamp order

Events are sorted by game, period, clock (descending) and `game_play_number`; the sort is stable
so the feed's own order is kept on ties. The clock never runs backwards in the data, so this
step only matters as a safeguard. Then, inside each tick (rows sharing one period and one
`secs_game`), four documented repairs run (`pipeline/ordering.py`):

1. **Substitutions go last**, in their original order. They never change score or possession,
   and were often listed between the free throws of a trip.
2. **A defensive foul inside an unfinished free-throw trip moves before the trip.** Example:
   `FT 1 of 2, Shooting Foul, FT 2 of 2` becomes `Shooting Foul, FT 1 of 2, FT 2 of 2`. A foul
   after the trip's last free throw is left alone (it starts the next trip), and technical or
   offensive fouls never move.
3. **A rebound with no outstanding miss moves after the next miss in the same tick.** This fixes
   `Offensive Rebound, Tip Shot (miss)`. A rebound that follows its miss never moves.
4. **An offensive rebound listed right after a made shot moves in front of it, when a miss was
   still waiting for its rebound before that shot.** This fixes `Layup (miss) ... Putback (made),
   Offensive Rebound`, which otherwise leaves the offense holding the ball after its own basket.

Everything else keeps its original order. Rows that moved keep their raw score, so scores are
re-set to the running maximum per game (scores never go down). The pipeline reports how many
rows repairs 2 to 4 moved (`reordered_rows` in `summary.json`; substitutions are not counted).

## Possession rules

`possession` is the team that has the ball (or is about to inbound / shoot free throws)
**after** the event: `home`, `away`, or empty when unknown. `acting_side` is the team in the
raw `team_id`: the shooter, rebounder, or turnover committer, and for fouls the team that
**fouled**. `margin` is the score margin after the event from the point of view of the team in
`possession` (positive = the team with the ball leads); it is empty when possession is unknown.

| Event | Possession afterwards | Status |
| --- | --- | --- |
| Made shot (field goal) | other team than the shooter | certain |
| Missed shot | the shooter's team, until the rebound | **loose** |
| Rebound (offensive, defensive or team) | the rebounding team (`team_id`) | certain |
| Rebound with no `team_id` | offensive: same team as before; defensive: the other team | certain |
| Turnover (any kind, `team_id` = committer) | other team | certain |
| Defensive foul (personal, shooting, loose ball, take, away from play, flagrant, clear path) | the *fouled* team, i.e. the other team than `team_id` | certain |
| Offensive foul / offensive charge | other team than the offender | certain |
| Technical foul, double personal foul | unchanged | carried |
| Free throw, not the last of its trip (`k of n`, k < n) | the shooter's team | certain |
| Last free throw, made | other team than the shooter (flagrant and clear path: the shooter keeps the ball) | certain |
| Last free throw, missed | the shooter's team, until the rebound | **loose** |
| Technical free throw | unchanged | carried |
| Jump ball | the team in `team_id` (it is the team that gained possession) | certain |
| Kicked ball (by the defense) | the offense, i.e. the other team than `team_id` | certain |
| Defensive goaltending | the defense inbounds: other team than the one whose score rose | certain |
| Substitution, timeout, challenge, review, violation, period markers | unchanged | carried |

A missing `team_id` (about 1% of rows) falls back to the score change for made shots, and to
`unknown` for turnovers and fouls. All rules assign the team directly rather than toggling, so
paired rows (`Offensive Foul` then `Offensive Foul Turnover`) cannot undo each other.

### Statuses

- `certain`: set by a rule above, or carried unchanged through an event that cannot change it.
- `loose`: live ball after a missed shot or missed last free throw. The team shown is the
  shooter's; the rebound row that follows settles it. **Most "uncertain" events are the missed
  shot rows themselves** and are resolved on the next row.
- `unknown`: nothing decided it (a missing `team_id`, or a period whose first events are all
  substitutions or timeouts). `possession` and `margin` are empty.

Extractors that need to know who has the ball *before* a shot should use the previous row's
`possession`, and treat `loose` rows as "ball in the air".

## How it was checked

- Unit tests with hand-written sequences for every rule above.
- The 3 games from the session 1 spike (BKN at CHI, GS at OKC, NO at HOU), event by event, in
  `pipeline/test_normalize.py`.
- Small raw samples from 2002, 2013 (a double-overtime game) and 2024 run through the full
  column mapping (`pipeline/fixtures/`).
- Whole-dataset consistency check, on all 25 seasons: for events with a `certain` possession, the
  team of the next shot, turnover or non-technical free throw in the same period should be the
  team we said had the ball. Agreement is 96.8% over 902,439 events (95.8% for 2002-2012, 97.6%
  for 2013-2026). Most of the rest is expected: an and-one free throw after a made shot, the
  turnover row that follows an offensive foul, and events missing from the older feeds (a team
  "rebounds" and is then fouled as the defender with no turnover recorded). That is why
  the older seasons score lower.

## Known limits

- Possession after a jump ball depends on `team_id` being the winner. It matched the text in the
  samples checked.
- A made shot or goaltending call on the very first row of a period with no `team_id` cannot
  find the scorer; the pipeline starts inference two minutes before the window, so this does
  not reach the window in practice.
- No shot clock exists in the data, so "last possession of the game" cannot be read off the
  clock. It has to be inferred from seconds left and margin.
