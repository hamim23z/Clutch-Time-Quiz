import { describe, expect, it } from 'vitest';
import { suggest } from './autocomplete';
import { idOf, mockIndex, mockPrompts } from './testUtils';

const index = mockIndex();
const names = (query: string, limit?: number): string[] => suggest(index, query, limit).map((s) => s.entry.name);

describe('autocomplete', () => {
  it('suggests from the whole universe: players and teams', () => {
    const found = suggest(index, 'har', 20).map((s) => s.entry.kind);
    expect(found).toContain('team');
    expect(found).toContain('player');
  });

  it('never depends on the prompt, so it cannot give an answer away', () => {
    // Even for the prompt with the fewest valid answers, suggestions for a short query are mostly not valid answers.
    const prompt = mockPrompts().reduce((a, b) => (b.answers.length < a.answers.length ? b : a));
    const valid = new Set(prompt.answers.map((a) => a.id));
    const shown = suggest(index, 'a', 50).map((s) => s.entry.id);
    expect(shown.length).toBeGreaterThan(prompt.answers.length);
    expect(shown.some((id) => !valid.has(id))).toBe(true);
    expect(shown.some((id) => valid.has(id))).toBe(true);
  });

  it('suggests the same list for the same query on every prompt', () => {
    expect(names('mar')).toEqual(names('mar')); // the function has no prompt argument at all
    expect(suggest.length).toBeLessThanOrEqual(3);
  });

  it('puts names that start with the query first', () => {
    const list = names('ald');
    expect(list[0]).toBe('Aldric Ashgrove');
    const mixed = names('city'); // "Harbor City Gulls" only has it inside the name
    expect(mixed).toContain('Harbor City Gulls');
  });

  it('matches any word of a name, in any order of typing the words', () => {
    expect(names('ashgrove')).toContain('Aldric Ashgrove');
    expect(names('ashgrove ald')).toContain('Aldric Ashgrove');
  });

  it('finds an entry by alias and says which alias matched', () => {
    const [first] = suggest(index, 'T-Bone');
    expect(first?.entry.name).toBe('Tavish Orlander');
    expect(first?.matchedAlias).toBe('T-Bone Orlander');
  });

  it('ignores accents and case in the query', () => {
    expect(names('CORVÍN')).toContain('Corvin Larkspur');
  });

  it('shows both people who share a name, with their disambiguators', () => {
    expect(names('dex marrow')).toEqual(['Dex Marrow (2003-2009)', 'Dex Marrow (2015-2022)']);
  });

  it('limits the list and returns nothing for an empty query', () => {
    expect(suggest(index, 'a', 6)).toHaveLength(6);
    expect(suggest(index, '   ')).toEqual([]);
    expect(suggest(index, '')).toEqual([]);
    expect(names('zzzzqq')).toEqual([]);
  });

  it('lists each entry once, even when its name and alias both match', () => {
    const found = names('dex', 20);
    expect(new Set(found).size).toBe(found.length);
    expect(found).toContain('Dex Marrow (2003-2009)');
    expect(idOf('Dex Marrow (2003-2009)')).toBeTruthy();
  });
});
