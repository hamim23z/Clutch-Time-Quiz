import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { baseName, buildIndex, matchAnswer, normalize } from './matching';
import type { Universe } from './types';

// schema/match-cases.json is shared with pipeline/tests/test_matchnorm_shared.py, so the two copies of the
// normalization cannot drift apart.
interface Cases {
  universe: Universe;
  normalize: Array<{ input: string; expected: string; dropSuffix: boolean }>;
  baseName: Array<{ input: string; expected: string }>;
  match: Array<{ input: string; expect: 'match' | 'ambiguous' | 'none'; id?: string; ids?: string[]; via?: string }>;
}
const cases = JSON.parse(readFileSync(resolve(process.cwd(), '../schema/match-cases.json'), 'utf8')) as Cases;
const index = buildIndex(cases.universe);

describe('the shared match cases', () => {
  it('has at least 60 cases covering accents, suffixes, aliases, last names, duplicate names and typos', () => {
    expect(cases.normalize.length + cases.baseName.length + cases.match.length).toBeGreaterThanOrEqual(60);
    const kinds = new Set(cases.match.map((c) => c.via ?? c.expect));
    for (const k of ['name', 'alias', 'last-name', 'typo', 'ambiguous', 'none']) expect(kinds.has(k)).toBe(true);
  });

  it.each(cases.normalize.map((c) => [c.input, c.dropSuffix, c.expected] as const))('normalize(%j, dropSuffix=%s) = %j', (input, dropSuffix, expected) => {
    expect(normalize(input, { dropSuffix })).toBe(expected);
  });

  it.each(cases.baseName.map((c) => [c.input, c.expected] as const))('baseName(%j) = %j', (input, expected) => {
    expect(baseName(input)).toBe(expected);
  });

  it.each(cases.match.map((c) => [c.input, c] as const))('matchAnswer(%j)', (input, c) => {
    const result = matchAnswer(index, input);
    expect(result.kind).toBe(c.expect);
    if (result.kind === 'match') {
      expect(result.entry.id).toBe(c.id);
      expect(result.via).toBe(c.via);
    } else if (result.kind === 'ambiguous') {
      expect(result.entries.map((e) => e.id).sort()).toEqual(c.ids);
    }
  });
});
