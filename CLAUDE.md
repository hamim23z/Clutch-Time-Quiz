# CLAUDE.md

Rules for every Claude Code session on this repo. Read this and SPEC.md before doing anything.

## Project

Deep Cut: a daily basketball trivia game where obscure correct answers score more than obvious ones. An offline Python pipeline turns NBA box score data into `web/public/prompts.json` and `web/public/universe.json`. A static Vite + React + TypeScript site reads those files. No backend, no accounts. Full details are in SPEC.md.

The repo may contain leftover files from an earlier concept (Clutch Time Quiz). Ignore anything about play-by-play scenarios, possession, or golf scoring unless a session's goal says otherwise.

## Layout

- `pipeline/`: Python 3 (pandas, pyarrow, pytest). Fetch, normalize, fame score, prompt generator, export, tests.
- `web/`: Vite + React + TypeScript app. Reads `public/prompts.json` and `public/universe.json` only.
- `schema/`: JSON schemas for prompts and universe. They are the contract between pipeline and website. Do not change them unless your session's goal says so.
- `data/raw/`: raw downloads. Gitignored. Never commit large raw files.
- `docs/`: notes written by sessions (for example `docs/data-source-boxscores.md`).

## Working rules

- Do only the session goal you were given. Do not start other sessions' work.
- Each session ends with a pull request: short summary, and how to check it.
- Run the relevant tests before finishing (`pytest` in `pipeline/`, `npm test` and `npm run build` in `web/` once they exist). Fix failures before opening the PR.
- Keep changes small and commit often with clear messages.
- If you are blocked after a few honest attempts, stop and report what you tried and what you need. Do not keep retrying or invent data.
- Never fabricate data or statistics. Every valid answer must come from the real data. Sample values in docs are placeholders only.
- Every prompt must state its era (for example "Since 2002") so its valid-answer list is complete.
- Do not use NBA logos or league branding. Plain names are fine.
- When you add a command (run the pipeline, start the site, run tests), record it in the Commands section below.

## Commands

Filled in by sessions as they are built.

- Install pipeline dependencies: `pip install -r pipeline/requirements.txt`
- Pipeline (fetch + normalize, seasons 2002-2026): `python3 pipeline/run.py` from the repo root (about 90 s, run it as plain `python3`, not `python3 -I`). Downloads one season at a time, deletes the raw files it downloaded, writes the six tables `players`, `teams`, `games`, `player_games`, `team_games`, `officials` (parquet) and `summary.json` to `data/processed/`, and regenerates `docs/pipeline-notes.md`. Resumes if interrupted; `--force` redoes finished seasons, `--start 2024 --end 2024` picks seasons, `--keep-raw` keeps downloads. Hand-written aliases are in `pipeline/data/aliases.csv`.
- Fame, tiers and candidate prompts (session 4): `python3 pipeline/generate.py` from the repo root, after the pipeline has built `data/processed/`. Computes the fame score and tier of every player, generates candidate prompts from the templates in `pipeline/templates.py`, and writes `data/generated/{fame.parquet,candidates.json,candidates_meta.json}` (gitignored) plus `docs/fame-report.md` and `docs/prompt-candidates.md`. Prints tier counts, the candidate total and templates with no candidates. Hand-written review notes for the fame report: `pipeline/data/fame-review.md`.
- Curate and export (session 5): `python3 pipeline/export.py` from the repo root, after the pipeline has built `data/processed/`. Runs everything `generate.py` does, then picks 504 prompts into 72 dives of 7 (about 2 minutes), builds the universe, checks both files against the schemas and the rarity targets, rechecks at least 60 prompts (2 per template family) against the tables, and writes `data/export/prompts.json` and `data/export/universe.json` (committed) plus `docs/prompts-sample.md`, `docs/curation-report.md` and `docs/rarity-report.md`. Layout: docs/export-format.md. Hand-written inputs: `pipeline/data/{fame_overrides,aliases,team_aliases,outside_range}.csv`; `pipeline/data/rarity-baseline.json` is the session 5 export's tier counts, the "before" of the rarity report. If the code or those files change, rerun it and commit the new export (a test fails if `data/export/` is out of date).
- Data spike 2 (Deep Cut): download per docs/data-source-boxscores.md, then `python3 pipeline/spike/boxscore_feasibility.py data/raw/boxscores` (counts and checks; output saved in docs/boxscore-feasibility-output.txt). Optional referee cross-check: `python3 pipeline/spike/referee_census.py data/raw/boxscores <out.parquet> 2002 2026`.
- Website (session 6): `cd web && npm ci` once. `npm run dev` (dev server) and `npm run build` first run `npm run sync-data`, which copies `data/export/prompts.json` and `universe.json` into `web/public/` and turns `pipeline/data/outside_range.csv` into `web/public/outside_range.json` (the three copies are not committed). Run `python3 pipeline/export.py` first if `data/export/` is missing. Launch date and time zone are in `web/src/config.ts`; dive N = prompts 7(N-1) to 7(N-1)+6 of the file, wrapping after the last dive. QA before the launch: `/?preview=1` shows a Play-test, `/?preview=1&today=2026-11-10` pretends it is that day (own saved progress).
- Pipeline tests: `cd pipeline && python3 -m pytest` (tiny synthetic samples, no downloads needed)
- Web tests: `cd web && npm test` (fixtures in `web/src/__fixtures__/`; `realData.test.ts` reads the committed export). `schema/match-cases.json` is shared by `web/src/matching.shared.test.ts` and `pipeline/tests/test_matchnorm_shared.py`.

## Conventions

- Python: type hints, small functions, one module per pipeline stage, tests next to the stage they cover.
- TypeScript: strict mode, no `any`, types generated or written from the schemas.
- Scoring tiers: 10, 20, 35, 55, 75, 100 points by global fame percentile (top 3%, 3 to 10%, 10 to 25%, 25 to 50%, 50 to 75%, bottom 25%). A wrong or timed-out answer scores 0.
- Prompt validity: at least 15 valid answers for player prompts and at least 5 for team prompts.
