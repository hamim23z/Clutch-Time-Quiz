import { describe, expect, it } from 'vitest';
import { allowedDistance, baseName, buildIndex, editDistance, matchAnswer, normalize, type MatchResult } from './matching';
import { idOf, mockIndex } from './testUtils';
import type { Universe } from './types';

const index = mockIndex();
const ids = (r: MatchResult): string[] => (r.kind === 'ambiguous' ? r.entries.map((e) => e.id).sort() : r.kind === 'match' ? [r.entry.id] : []);

describe('normalize', () => {
  it.each([
    ['Aldric ASHGROVE', 'aldric ashgrove'],
    ['  Aldric   Ashgrove ', 'aldric ashgrove'],
    ['J.J. Barea', 'jj barea'],
    ['J. J. Barea', 'jj barea'],
    ["Caelan O'Brask", 'caelan obrask'],
    ['Caelan O’Brask', 'caelan obrask'],
    ['Hollis-Jefferson', 'hollis jefferson'],
    ['Nenê', 'nene'],
    ['Schröder', 'schroder'],
    ['Mike J Smith', 'mike j smith'], // a lone middle initial is its own word
    ['', ''],
    ['  !!! ', ''],
  ])('%j -> %j', (input, expected) => {
    expect(normalize(input)).toBe(expected);
  });

  it('drops suffixes only when asked', () => {
    expect(normalize('Jaren Jackson Jr.')).toBe('jaren jackson jr');
    expect(normalize('Jaren Jackson Jr.', { dropSuffix: true })).toBe('jaren jackson');
    expect(normalize('Robert Williams III', { dropSuffix: true })).toBe('robert williams');
    expect(normalize('III', { dropSuffix: true })).toBe('iii'); // never reduce a name to nothing
  });

  it('removes a disambiguator in parentheses with baseName', () => {
    expect(baseName('Dex Marrow (2003-2009)')).toBe('Dex Marrow');
    expect(baseName('Harbor City Gulls')).toBe('Harbor City Gulls');
  });
});

describe('edit distance rules', () => {
  it('computes Levenshtein distance and stops early past the limit', () => {
    expect(editDistance('kitten', 'sitting', 3)).toBe(3);
    expect(editDistance('abc', 'abc', 2)).toBe(0);
    expect(editDistance('abc', 'abcdefgh', 2)).toBe(3); // too far apart: max + 1
    expect(editDistance('abcdef', 'uvwxyz', 2)).toBe(3);
  });

  it('allows no typos under 6 characters, 1 for 6 to 10, and 2 above 10', () => {
    expect([5, 6, 10, 11, 20].map(allowedDistance)).toEqual([0, 1, 1, 2, 2]);
  });
});

// [input, expected outcome]. Outcomes: id and how it matched, 'ambiguous', or 'none'.
const CASES: Array<[string, { name: string; via: string } | { ambiguous: string[] } | 'none']> = [
  // exact names in different cases and spacings
  ['Aldric Ashgrove', { name: 'Aldric Ashgrove', via: 'name' }],
  ['aldric ashgrove', { name: 'Aldric Ashgrove', via: 'name' }],
  ['ALDRIC ASHGROVE', { name: 'Aldric Ashgrove', via: 'name' }],
  ['  Aldric    Ashgrove  ', { name: 'Aldric Ashgrove', via: 'name' }],
  ['Corvín Larkspur', { name: 'Corvin Larkspur', via: 'name' }], // accent typed by the player
  // aliases and nicknames
  ['Al Ashgrove', { name: 'Aldric Ashgrove', via: 'alias' }],
  ['T-Bone Orlander', { name: 'Tavish Orlander', via: 'alias' }],
  ['t bone orlander', { name: 'Tavish Orlander', via: 'alias' }],
  ['Zeb Rainwater', { name: 'Zebediah Quarrelly', via: 'alias' }], // a former name
  ['Renato Silvéstre', { name: 'Renato Silvestre', via: 'name' }], // the accent is stripped, so it is the name itself
  // punctuation: apostrophes vanish, hyphens become spaces, dots vanish
  ["Caelan O'Brask", { name: "Caelan O'Brask", via: 'name' }],
  ['Caelan OBrask', { name: "Caelan O'Brask", via: 'name' }],
  ['Marlow Hart-Ellison', { name: 'Marlow Hart-Ellison', via: 'name' }],
  ['marlow hart ellison', { name: 'Marlow Hart-Ellison', via: 'name' }],
  ['J.J. Hartwell', { name: 'J.J. Hartwell', via: 'name' }],
  ['J. J. Hartwell', { name: 'J.J. Hartwell', via: 'name' }],
  ['JJ Hartwell', { name: 'J.J. Hartwell', via: 'name' }],
  // suffixes are dropped, or used to tell two people apart
  ['Tobias Rennick', { name: 'Tobias Rennick Jr.', via: 'name' }],
  ['Tobias Rennick III', { name: 'Tobias Rennick Jr.', via: 'name' }],
  ['Sol Garrowby', { name: 'Sol Garrowby III', via: 'name' }],
  ['Dex Marrow Sr.', { name: 'Dex Marrow (2003-2009)', via: 'alias' }],
  ['Dex Marrow Jr.', { name: 'Dex Marrow (2015-2022)', via: 'alias' }],
  ['Dex Marrow (2003-2009)', { name: 'Dex Marrow (2003-2009)', via: 'name' }],
  // two people with one name: ask which
  ['Dex Marrow', { ambiguous: ['Dex Marrow (2003-2009)', 'Dex Marrow (2015-2022)'] }],
  // last names, only when unique across the whole universe
  ['Ashgrove', { name: 'Aldric Ashgrove', via: 'last-name' }],
  ['Garrowby', { name: 'Sol Garrowby III', via: 'last-name' }],
  ['Brask', { name: 'Joren Brask', via: 'last-name' }], // O'Brask is a different surname ("obrask"), so Brask is unique
  ['Marrow', { ambiguous: ['Anselm Marrow', 'Dex Marrow (2003-2009)', 'Dex Marrow (2015-2022)'] }], // three players share it
  ['Rapids', { name: 'Lakeshore Rapids', via: 'alias' }], // a team alias; the player Verne Rapids does not get the bare surname
  // typos: 1 edit for 6-10 characters, 2 for longer names, none for short ones
  ['Aldric Ashgrov', { name: 'Aldric Ashgrove', via: 'typo' }],
  ['Aldrik Ashgruve', { name: 'Aldric Ashgrove', via: 'typo' }], // two edits in a 15-character name
  ['Aldrik Ashgruvx', 'none'], // three edits
  ['Yoran Fall', { name: 'Yoran Fell', via: 'typo' }], // 10 characters: one edit
  ['Yoran Fxxl', 'none'], // two edits is too many at 10 characters
  ['Ty Roh', { name: 'Ty Roe', via: 'typo' }], // 6 characters: one edit
  ['Bo Lee', 'none'], // 5 characters: no typos allowed
  ['harbor cty gulls', { name: 'Harbor City Gulls', via: 'typo' }],
  // teams
  ['Harbor City Gulls', { name: 'Harbor City Gulls', via: 'name' }],
  ['Gulls', { name: 'Harbor City Gulls', via: 'alias' }],
  ['Harbor City', { name: 'Harbor City Gulls', via: 'alias' }],
  ['Verne Rapids', { name: 'Verne Rapids', via: 'name' }],
  // things that are not in the universe
  ['Totally Unknown', 'none'],
  ['', 'none'],
  ['   ', 'none'],
  ['!!!', 'none'],
  ['123', 'none'],
];

describe('matchAnswer on the mock universe', () => {
  it.each(CASES)('%j', (input, expected) => {
    const r = matchAnswer(index, input);
    if (expected === 'none') {
      expect(r.kind).toBe('none');
    } else if ('ambiguous' in expected) {
      expect(r.kind).toBe('ambiguous');
      expect(ids(r)).toEqual(expected.ambiguous.map(idOf).sort());
    } else {
      expect(r.kind).toBe('match');
      if (r.kind === 'match') {
        expect(r.entry.id).toBe(idOf(expected.name));
        expect(r.via).toBe(expected.via);
      }
    }
  });

  it('has at least 30 test inputs', () => {
    expect(CASES.length).toBeGreaterThanOrEqual(30);
  });

  it('does not accept a last name several players share, and lists them all', () => {
    const r = matchAnswer(index, 'Marrow');
    expect(r.kind).toBe('ambiguous');
    expect(ids(r)).toEqual([idOf('Anselm Marrow'), idOf('Dex Marrow (2003-2009)'), idOf('Dex Marrow (2015-2022)')].sort());
  });

  it('does not accept a last name that is also a name or alias of another entry', () => {
    expect(index.lastNames.has('rapids')).toBe(false); // a team nickname
    expect(index.lastNames.has('ashgrove')).toBe(true);
    expect(index.lastNames.has('marrow')).toBe(false); // shared by three players
    expect(index.lastNames.has('brask')).toBe(true); // O'Brask is a different surname
  });

  it('treats a typo equally close to two entries as ambiguous instead of guessing', () => {
    const u: Universe = {
      players: [
        { id: 'a', name: 'Dorian Hale', aliases: [] },
        { id: 'b', name: 'Dorian Hall', aliases: [] },
      ],
      teams: [],
    };
    expect(matchAnswer(buildIndex(u), 'Dorian Halx').kind).toBe('ambiguous');
    expect(matchAnswer(buildIndex(u), 'Dorian Hale').kind).toBe('match');
  });

  it('prefers the closest typo match', () => {
    const u: Universe = {
      players: [
        { id: 'a', name: 'Dorian Hale', aliases: [] },
        { id: 'b', name: 'Dorian Haley', aliases: [] },
      ],
      teams: [],
    };
    const r = matchAnswer(buildIndex(u), 'Dorian Hali'); // 1 from Hale ("a"->"i" is 1), 2 from Haley
    expect(r.kind).toBe('match');
    if (r.kind === 'match') expect(r.entry.id).toBe('a');
  });

  it('applies the last-name rule across teams and players together', () => {
    const u: Universe = {
      players: [{ id: 'p', name: 'Zed Lakers', aliases: [] }],
      teams: [{ id: 't', name: 'Lakeshore Lakers', aliases: ['Lakers'] }],
    };
    const r = matchAnswer(buildIndex(u), 'Lakers');
    expect(r.kind === 'match' && r.entry.id === 't' && r.via === 'alias').toBe(true); // the team alias wins; the player's surname is not accepted
  });
});
