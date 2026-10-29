// Checks against the real export in ../data/export (committed), not the fixtures.
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { resolveText } from './answer';
import { suggest } from './autocomplete';
import { parsePrompts, parseUniverse } from './loadData';
import { buildIndex, matchAnswer } from './matching';
import { isOutsideRange } from './outsideRange';
import { diveCount, divePrompts } from './schedule';

const root = resolve(process.cwd(), '..');
const universe = parseUniverse(JSON.parse(readFileSync(resolve(root, 'data/export/universe.json'), 'utf8')));
const prompts = parsePrompts(JSON.parse(readFileSync(resolve(root, 'data/export/prompts.json'), 'utf8')), universe);
const index = buildIndex(universe);

/** The names column of pipeline/data/outside_range.csv. */
const outsideNames = readFileSync(resolve(root, 'pipeline/data/outside_range.csv'), 'utf8')
  .split(/\r?\n/)
  .slice(1)
  .map((l) => l.trim().replace(/^"|"$/g, ''))
  .filter((l) => l !== '');

const FAMOUS_BEFORE_2001 = [
  'Larry Bird', 'Magic Johnson', 'Kareem Abdul-Jabbar', 'Wilt Chamberlain', 'Bill Russell', 'Oscar Robertson', 'Jerry West',
  'Julius Erving', 'Moses Malone', 'Clyde Drexler', 'Dominique Wilkins', 'Kevin McHale', 'Robert Parish', 'James Worthy',
  'Dennis Rodman', 'Mark Price', 'Chris Mullin', 'Joe Dumars', 'Pete Maravich', 'George Gervin',
];

describe('the real export', () => {
  it('loads against the runtime checks and has whole dives', () => {
    expect(prompts.length).toBeGreaterThanOrEqual(63);
    expect(prompts.length % 7).toBe(0);
    for (let n = 1; n <= diveCount(prompts); n++) expect(divePrompts(prompts, n)).toHaveLength(7);
  });

  it('wraps after the last dive: dive number N+1 plays the same prompts as dive #1', () => {
    const total = diveCount(prompts);
    expect(divePrompts(prompts, total + 1).map((p) => p.id)).toEqual(divePrompts(prompts, 1).map((p) => p.id));
  });
});

describe('people who share a display name', () => {
  it('are separate rows in the autocomplete, each with its disambiguator', () => {
    const rows = suggest(index, 'Mike James', 10).map((s) => s.entry.name);
    expect(rows).toContain('Mike James (2002-2014)');
    expect(rows).toContain('Mike James (2018-2021)');
    expect(rows).not.toContain('Mike James');
    const ids = suggest(index, 'Mike James', 10).filter((s) => s.entry.name.startsWith('Mike James (')).map((s) => s.entry.id);
    expect(new Set(ids).size).toBe(2);
  });

  it('are asked "which one?" when typed without the disambiguator', () => {
    const r = matchAnswer(index, 'Mike James');
    expect(r.kind).toBe('ambiguous');
    if (r.kind === 'ambiguous') expect(r.entries.map((e) => e.name).sort()).toEqual(['Mike James (2002-2014)', 'Mike James (2018-2021)']);
  });

  it('every shared name in the universe carries a disambiguator, and nobody is listed twice under the same text', () => {
    const names = universe.players.map((e) => e.name);
    expect(new Set(names).size).toBe(names.length);
    const bases = new Map<string, number>();
    for (const n of names) bases.set(n.replace(/\s*\([^)]*\)\s*$/, ''), (bases.get(n.replace(/\s*\([^)]*\)\s*$/, '')) ?? 0) + 1);
    const shared = [...bases].filter(([, c]) => c > 1).map(([b]) => b);
    expect(shared.length).toBeGreaterThanOrEqual(10);
    for (const base of shared) expect(names.filter((n) => n.startsWith(`${base} (`)).length).toBeGreaterThan(1);
  });
});

describe('aliases and spellings', () => {
  it('"Ron Artest" is athlete id 25', () => {
    const r = matchAnswer(index, 'Ron Artest');
    expect(r.kind).toBe('match');
    if (r.kind === 'match') {
      expect(r.entry.id).toBe('pl-25');
      expect(r.entry.name).toBe('Metta World Peace');
    }
  });

  it('"Nene" and "Nenê" both match the same player', () => {
    const a = matchAnswer(index, 'Nene');
    const b = matchAnswer(index, 'Nenê');
    expect(a.kind).toBe('match');
    expect(b.kind).toBe('match');
    if (a.kind === 'match' && b.kind === 'match') expect(a.entry.id).toBe(b.entry.id);
  });

  it('a few nicknames people actually type resolve to the right player', () => {
    for (const [text, name] of [['Greek Freak', 'Giannis Antetokounmpo'], ['King James', 'LeBron James'], ['KD', 'Kevin Durant'], ['Sixers', 'Philadelphia 76ers'], ['Sonics', 'Oklahoma City Thunder']] as const) {
      const r = matchAnswer(index, text);
      expect(r.kind).toBe('match');
      if (r.kind === 'match') expect(r.entry.name).toBe(name);
    }
  });
});

describe('outside the data range', () => {
  const prompt = prompts[0]!;

  it('has the 20 famous pre-2001 names in the list', () => {
    for (const name of FAMOUS_BEFORE_2001) expect(outsideNames).toContain(name);
  });

  it.each(FAMOUS_BEFORE_2001)('%s gets the outside-the-data-range message, not a wrong answer', (name) => {
    expect(isOutsideRange(name, outsideNames)).toBe(true);
    const r = resolveText(prompt, index, name, outsideNames);
    expect(r.kind).toBe('result');
    if (r.kind === 'result') {
      expect(r.result.status).toBe('outside_range');
      expect(r.result.countsAsWrong).toBe(false);
      expect(r.result.points).toBe(0);
    }
  });

  it('no name on the list is read as anyone in the universe, so the message never hides a real answer', () => {
    const clashes = outsideNames.filter((n) => matchAnswer(index, n).kind !== 'none');
    expect(clashes).toEqual([]);
  });

  it('a name in neither place is simply not a valid answer', () => {
    const r = resolveText(prompt, index, 'Zorblax Quimby', outsideNames);
    expect(r.kind === 'result' && r.result.status).toBe('invalid');
  });
});
