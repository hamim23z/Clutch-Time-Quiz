# Clutch Time Quiz: Spec & Build Plan

## Overview

Clutch Time Quiz is a daily basketball game where you make the coaching call in the final minute of a real NBA game, then see how that call has actually worked out historically.

- **Daily round:** 5 real late-game situations. Team names and the date stay hidden until you answer.
- **Your move:** pick one of 2 or 3 decisions, such as fouling up three or playing defense.
- **Reveal:** what the team really did, how the game ended, and the historical win rate of every option in similar situations.
- **Golf scoring:** each hole is a birdie, par, bogey or double bogey depending on how close your pick was to the best option. The round total is shown against par.
- **Shareable result:** one colored square per hole plus your score, in the style of Wordle.

**What done means for the credit window:** a public URL live by November 3 with at least 60 verified scenarios (12 days of rounds), 3 scenario types, scoring, a share button, streaks and an archive. There are no accounts and no backend, so everything runs as a static site.

## Gameplay and scoring

Each hole shows a game state and asks one question. The win rates behind the answer come from every similar situation in the historical data, not from the single game on screen.

**Scenario card shows:** score margin, seconds left, who has the ball, the quarter, and the question. Teams and date are hidden.

**Version 1 scenario types (three, all detectable from play-by-play):**

| Type | Situation | Options |
| --- | --- | --- |
| Foul up three | Defense leads by 3, opponent has the ball, 10 seconds or fewer left | Foul before the shot, or play defense |
| Down three | Offense trails by 3 with the ball, 24 seconds or fewer left | Take a three, or take a two |
| Last shot | Offense is tied or down 1, final possession, 24 seconds or fewer left | Shoot early, or hold for the last shot |

Stretch types, only if credit remains: timeout versus push the pace after a make, and intentional fouling when trailing.

**Scoring per hole**, using the win rate gap between your pick and the best option in that situation bucket:

| Result | Gap to best option | Strokes |
| --- | --- | --- |
| Birdie | 0 (you picked the best) | -1 |
| Par | up to 3 percentage points | 0 |
| Bogey | 3 to 10 points | +1 |
| Double bogey | more than 10 points | +2 |

A round is 5 holes, so scores run from -5 to +10. The share line reads like `Clutch Time #12: -2` followed by five colored squares. Streaks count consecutive days played, stored in the browser.

## Data and content pipeline

The game runs on an offline Python pipeline that turns historical play-by-play into a fixed file of scenarios. The website never touches raw data.

1. **Fetch.** Load NBA play-by-play for several seasons into `data/raw/` (gitignored). Cloud sessions usually reach only package registries and GitHub, so prefer a dataset published on GitHub, such as the sportsdataverse hoopR NBA releases. Session 1 confirms what is actually reachable.
2. **Normalize.** Convert each game into events carrying score margin, seconds remaining, possession, and event type (shot, foul, timeout, rebound, turnover).
3. **Extract situations.** For each scenario type, find every moment in the data that matches its rule and record which option the team took, by a simple pattern in the next few events (for example, a defensive foul before any shot in the last 10 seconds means the team fouled).
4. **Build win-rate buckets.** Group situations by type and coarse state (margin, seconds band, possession) and compute the win rate of the deciding team for each option. Drop any bucket where an option has fewer than 30 samples.
5. **Pick featured games.** Choose well-defined, memorable moments from the surviving buckets, balanced across the 3 types and across easy and hard calls (a wide gap between options is easy, a narrow gap is hard).
6. **Export.** Write `web/public/scenarios.json`, validated against the schema below.

**Scenario schema (the contract between pipeline and website):**

```json
{
  "id": "foul3-0042",
  "type": "foul_up_three",
  "state": { "quarter": 4, "margin": 3, "secondsLeft": 8, "possession": "opponent" },
  "question": "You lead by 3 and they have the ball. What do you do?",
  "options": [
    { "key": "foul", "label": "Foul before the shot", "winRate": 0.91, "n": 212 },
    { "key": "defend", "label": "Play straight defense", "winRate": 0.84, "n": 1480 }
  ],
  "actual": { "choice": "defend", "summary": "Short text of what happened", "final": "Final score", "game": "Teams and date" },
  "difficulty": "easy"
}
```

The numbers in the sample are placeholders to show the shape, not real statistics.

**Known weak spot:** the win rates compare similar situations, so they show what usually happens, not what would have happened in this exact game. Say so on the reveal screen and keep the buckets coarse.

## Architecture and stack

Two separate pieces joined by one JSON file: a Python pipeline that runs offline, and a static website that only reads `scenarios.json`. No server, database or accounts are needed, which keeps the build small enough for the credit.

| Piece | Choice | Why |
| --- | --- | --- |
| Pipeline | Python 3, pandas, pytest | Simple data wrangling, easy to test |
| Website | Vite, React, TypeScript | Fast to scaffold, one static build |
| State | Browser localStorage | Streaks and history without a backend |
| Hosting | GitHub Pages (or Vercel) | Free, deploys from the repo |
| Contract | `schema/scenarios.schema.json` | Lets the pipeline and website be built in parallel |

```
clutch-time-quiz/
  SPEC.md            this document
  CLAUDE.md          short rules and commands for every session
  pipeline/          fetch, normalize, extract, buckets, export, tests
  web/               the React app and public/scenarios.json
  data/raw/          gitignored raw play-by-play
  schema/            scenarios.schema.json
```

Because the site is static, the answers ship inside `scenarios.json` and a determined player could read them. That is acceptable for a casual daily game. The daily round is chosen from the launch date, so everyone sees the same 5 holes on a given day.

## Build plan

Nine small sessions, each with one goal and a checkable finish line. Merge each pull request before starting the sessions that depend on it.

| # | Goal | Done when | Depends on |
| --- | --- | --- | --- |
| 0 | You: create the GitHub repo, connect it to Claude, commit SPEC.md and CLAUDE.md | Repo exists and a cloud session can open it | none |
| 1 | Data spike: find a play-by-play source reachable from a cloud session and load it | A report names the working source, and 3 sample games load with the fields the pipeline needs | 0 |
| 2 | Pipeline core: fetch and normalize several seasons into events with margin, seconds left and possession | Tests pass on a sample season and a one-command run produces a normalized file | 1 |
| 3 | Website with mock data: scenario card, options, reveal, golf scoring, 5-hole round, mobile layout | App runs from a hand-written 10-scenario `scenarios.json` that follows the schema | 0 (parallel with 2) |
| 4 | Extractors and buckets for the 3 scenario types | Each type outputs situations with the option taken, and buckets with at least 30 samples per option | 2 |
| 5 | Scenario selection and export | `scenarios.json` has at least 60 scenarios, balanced by type and difficulty, and passes schema validation | 4 |
| 6 | Integration: real data in the site, daily rotation, streaks, share button, archive | A full round plays end to end from the real file | 3, 5 |
| 7 | Polish and deploy: accessibility, tests, README, GitHub Pages | Public URL works on a phone and a laptop | 6 |
| 8 | Review: a fresh session audits the code and 20 random scenarios, fixes what it finds | Written list of issues, all fixed or logged | 7 |

Sessions 2 and 3 can run at the same time because they only share the schema. Everything else runs in order.

**Prompt template for every session:**

```
Read SPEC.md and CLAUDE.md first. Your task is session N: <goal>.
Stay inside that goal. Do not start other sessions' work.
Done means: <done-when line>. Run the tests before finishing.
If you are blocked for more than a few attempts, stop and report what you tried.
Open a pull request with a short summary of what changed and how to check it.
```

**Session 1 written out in full**, since it decides everything else:

```
Read SPEC.md and CLAUDE.md. Task: session 1, data spike.
Find a source of NBA play-by-play data that this cloud session can actually download
(try datasets hosted on GitHub first, then package-registry libraries).
Load 3 full games and print, for the last 60 seconds of each: score margin,
seconds left, possession, and event type.
Write docs/data-source.md with the working source, the exact download command,
the columns available, and anything missing (for example possession or timeouts).
Do not build the rest of the pipeline. Open a pull request.
```

## Credit budget and timeline

The plan spends about $75 on the core build and keeps $25 in reserve, finishing a day before the November 4 expiry. The dollar figures are estimates, not measured costs, so treat the first two days as calibration.

| Day | Sessions | Budget (USD) |
| --- | --- | --- |
| Tue Oct 27 | 0 and 1: repo setup, data spike | 3 |
| Wed Oct 28 | 2 and 3 in parallel: pipeline core, website with mock data | 22 |
| Thu Oct 29 | 4: extractors and buckets | 12 |
| Fri Oct 30 | 5: scenario selection and export | 10 |
| Sat Oct 31 | 6: integration | 12 |
| Sun Nov 1 | 7: polish and deploy | 10 |
| Mon Nov 2 | 8: review and fixes | 6 |
| Tue Nov 3 | Reserve: stretch work or reruns | 25 |

**Checkpoint after Wednesday.** If sessions 1 to 3 cost more than $40 combined, cut the stretch list and keep the reserve for fixes. If they cost far less, move the surplus to stretch work.

**Keeping sessions cheap**

- Put the spec and rules in the repo so no session has to rediscover them.
- One goal per session, and tell it to stop and report when stuck instead of retrying.
- Point it at specific files and commands rather than asking it to explore.
- Merge each pull request before the next session starts, so it begins from clean code.
- Run in parallel only where the schema keeps the work independent.

**Spending the reserve, in order of value**

1. Two more scenario types: timeout versus pushing the pace, and intentional fouling when trailing.
2. A short explanation on each reveal, written from the bucket data.
3. A hard mode that hides the clock or the quarter.
4. A generated share image instead of text.

## Risks and cuts

The biggest risk is data access, and session 1 exists to find out early.

| Risk | What happens | Fallback |
| --- | --- | --- |
| No reachable data source | Cloud session cannot download play-by-play | Download a dataset locally, filter it to the last 2 minutes of each game, and commit that smaller file to the repo |
| Too few samples per bucket | Win rates are noisy | Widen the buckets, add more seasons, or drop the weakest scenario type |
| Option detection is wrong | A scenario labels a foul or a three incorrectly | Restrict to unambiguous event patterns, and spot-check 20 random scenarios by hand in session 8 |
| Credit runs short | Later sessions cannot finish | Cut in the order below |
| Branding | NBA marks and logos | Use plain team names and no logos or league branding |

**Cut order if credit runs short:** stretch types first, then the archive, then streaks, then the third scenario type. The share button stays, because it is what makes the game spread.
