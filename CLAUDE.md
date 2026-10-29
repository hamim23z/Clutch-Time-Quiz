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

- Pipeline: TBD
- Data spike 2 (Deep Cut): download per docs/data-source-boxscores.md, then `python3 pipeline/spike/boxscore_feasibility.py data/raw/boxscores` (counts and checks; output saved in docs/boxscore-feasibility-output.txt). Optional referee cross-check: `python3 pipeline/spike/referee_census.py data/raw/boxscores <out.parquet> 2002 2026`.
- Website: `cd web && npm install` once, then `npm run dev` (dev server), `npm run build` (typecheck + production build into `web/dist`), `npm run preview` (serve the build). It reads `web/public/prompts.json` and `web/public/universe.json`; the files in the repo are MOCK data (every id starts with `mock-`, every name is invented) until session 5 exports the real ones.
- Web tests: `cd web && npm test` (vitest; includes validating both JSON files against `schema/prompts.schema.json` and `schema/universe.schema.json`)

## Conventions

- Python: type hints, small functions, one module per pipeline stage, tests next to the stage they cover.
- TypeScript: strict mode, no `any`, types generated or written from the schemas.
- Scoring tiers: 10, 20, 35, 55, 75, 100 points by global fame percentile (top 3%, 3 to 10%, 10 to 25%, 25 to 50%, 50 to 75%, bottom 25%). A wrong or timed-out answer scores 0.
- Prompt validity: at least 15 valid answers for player prompts and at least 5 for team prompts.
