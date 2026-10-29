// Copies the pipeline's export into public/ so the site serves real data, and turns the outside-range CSV into JSON.
//   data/export/prompts.json, data/export/universe.json  ->  web/public/
//   pipeline/data/outside_range.csv (column "name")      ->  web/public/outside_range.json (an array of names)
// Run by `npm run dev` and `npm run build` (and by hand as `npm run sync-data`). The copies are not committed.
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
  const count = sync();
  console.log(`synced data/export to web/public (${count} outside-range names)`);
}
