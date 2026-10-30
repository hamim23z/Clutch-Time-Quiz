// Copies the pipeline's export into public/ so the site serves real data, and turns the outside-range CSV into JSON.
//   data/export/prompts.json, data/export/universe.json  ->  web/public/
//   pipeline/data/outside_range.csv (column "name")      ->  web/public/outside_range.json (an array of names)
// Run by `npm run dev` and by hand as `npm run sync-data`. The copies in web/public/ ARE committed, so the site builds
// from web/ alone (Vercel imports the repo with Root Directory = web). This script is never part of `npm run build`, and it
// skips with a message, without failing, when ../data is not there or when it runs on Vercel.
import { copyFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const web = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const root = resolve(web, '..');
const publicDir = resolve(web, 'public');

/** The names in a one-column CSV with a header "name" (quoted fields allowed). */
export function parseNames(csv) {
  const lines = csv.split(/\r?\n/).filter((l) => l.trim() !== '');
  if (lines.length === 0 || lines[0].trim().replace(/^"|"$/g, '') !== 'name') throw new Error('outside_range.csv must start with the header "name"');
  return lines.slice(1).map((l) => l.trim().replace(/^"|"$/g, '').replace(/""/g, '"')).filter((n) => n !== '');
}

/** Why syncing is not possible here, or null if it is: no ../data (web/ alone, as on Vercel), or a Vercel build. */
export function skipReason(repo = root, env = process.env) {
  if (env.VERCEL) return 'running on Vercel: using the committed copies in web/public';
  if (!existsSync(resolve(repo, 'data/export'))) return `${resolve(repo, 'data/export')} not found: using the committed copies in web/public`;
  return null;
}

/** Copy the export from `repo` into `out`. Returns the number of outside-range names. */
export function sync(repo = root, out = publicDir) {
  mkdirSync(out, { recursive: true });
  for (const file of ['prompts.json', 'universe.json']) {
    const from = resolve(repo, 'data/export', file);
    if (!existsSync(from)) throw new Error(`${from} is missing: run python3 pipeline/export.py first`);
    copyFileSync(from, resolve(out, file));
  }
  const csv = resolve(repo, 'pipeline/data/outside_range.csv');
  const names = existsSync(csv) ? parseNames(readFileSync(csv, 'utf8')) : [];
  writeFileSync(resolve(out, 'outside_range.json'), JSON.stringify(names) + '\n');
  return names.length;
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const reason = skipReason();
  if (reason) {
    console.log(`sync-data skipped: ${reason}`);
  } else {
    const count = sync();
    console.log(`synced data/export to web/public (${count} outside-range names)`);
  }
}
