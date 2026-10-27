# CLAUDE.md

Rules for every Claude Code session on this repo. Read this and SPEC.md before doing anything.

## Project

Clutch Time Quiz: a daily basketball decision game. An offline Python pipeline turns historical NBA play-by-play into `web/public/scenarios.json`. A static Vite + React + TypeScript site reads that file. No backend, no accounts. Full details are in SPEC.md.

## Layout

- `pipeline/`: Python 3 (pandas, pytest). Fetch, normalize, extract, buckets, export, tests.
- `web/`: Vite + React + TypeScript app. Reads `public/scenarios.json` only.
- `schema/scenarios.schema.json`: the contract between pipeline and website. Do not change it unless your session's goal says so.
- `data/raw/`: raw play-by-play. Gitignored. Never commit large raw files.
- `docs/`: notes written by sessions (for example `docs/data-source.md`).

## Working rules

- Do only the session goal you were given. Do not start other sessions' work.
- Each session ends with a pull request: short summary, and how to check it.
- Run the relevant tests before finishing (`pytest` in `pipeline/`, `npm test` and `npm run build` in `web/` once they exist). Fix failures before opening the PR.
- Keep changes small and commit often with clear messages.
- If you are blocked after a few honest attempts, stop and report what you tried and what you need. Do not keep retrying or invent data.
- Never fabricate statistics. All win rates must be computed from the real data. Sample numbers in docs are placeholders only.
- Do not use NBA logos or league branding. Plain team names are fine.
- When you add a command (run the pipeline, start the site, run tests), record it in the Commands section below.

## Commands

Filled in by sessions as they are built.

- Install pipeline dependencies: `pip install -r pipeline/requirements.txt`
- Pipeline (fetch + normalize, seasons 2002-2026): `python3 pipeline/run.py` from the repo root. Downloads one season at a time, deletes each raw file after use, writes `data/processed/events.parquet`, `games.parquet` and `summary.json`. Resumes if interrupted; `--force` redoes finished seasons, `--start 2024 --end 2024` picks seasons, `--keep-raw` keeps downloads. Rules are in docs/possession.md.
- Data spike (session 1): download per docs/data-source.md, then `python3 pipeline/spike/sample_games.py data/raw/play_by_play_2024.parquet`
- Website dev server: TBD
- Tests: `cd pipeline && python3 -m pytest` (small samples in `pipeline/fixtures/`, no downloads needed)

## Conventions

- Python: type hints, small functions, one module per pipeline stage, tests next to the stage they cover.
- TypeScript: strict mode, no `any`, components small and typed from the schema.
- Scoring: birdie -1 (best option), par 0 (within 3 points), bogey +1 (3 to 10 points), double bogey +2 (more than 10 points). Win rate buckets need at least 30 samples per option.
