/**
 * Answer matching. Everything about turning what a player typed into an entry of the universe lives here.
 *
 * Normalization: lowercase, strip accents, strip punctuation (apostrophes and periods vanish, hyphens and other marks
 * become spaces), drop suffixes such as Jr. and III, and join runs of single letters ("J. J." -> "jj").
 *
 * An input is recognized, in this order, as:
 *  1. a full name or an alias, with the suffix kept ("Dex Marrow Jr."), then with it dropped ("Tobias Rennick");
 *  2. a last name, but only if it is unique across the whole universe: no other player has it, and it is not a
 *     name or alias of any other entry (a team nickname, say). A last name several players share is not accepted;
 *     the result is "ambiguous" and lists them;
 *  3. a typo of one of those: edit distance 1 for names of 6 to 10 characters, 2 for longer names, none for
 *     shorter ones. A typo that is equally close to two different entries is ambiguous and is not guessed.
 *
 * When two entries share a name (for example "Dex Marrow (2003-2009)" and "Dex Marrow (2015-2022)"), the result is
 * "ambiguous" and lists them, so the interface can ask which one was meant.
 */
import type { Entry, Universe } from './types';

const SUFFIXES = new Set(['jr', 'sr', 'ii', 'iii', 'iv', 'v']);

export type MatchVia = 'name' | 'alias' | 'last-name' | 'typo';

export type MatchResult =
  | { kind: 'match'; entry: Entry; via: MatchVia; distance: number }
  | { kind: 'ambiguous'; entries: Entry[] }
  | { kind: 'none' };

/** Lowercase, strip accents and punctuation, join single letters. Suffixes are dropped only when asked. */
export function normalize(text: string, options: { dropSuffix?: boolean } = {}): string {
  const folded = text
    .normalize('NFKD')
    .replace(/\p{M}/gu, '')
    .toLowerCase()
    .replace(/[‘’'`]/g, '')
    .replace(/\./g, '')
    .replace(/[^a-z0-9]+/g, ' ')
    .trim();
  const tokens = folded === '' ? [] : folded.split(' ');
  // Join runs of single letters: "j j hartwell" -> "jj hartwell". A lone middle initial stays its own token.
  const joined: string[] = [];
  let previousWasLetter = false;
  for (const token of tokens) {
    if (token.length === 1 && previousWasLetter && joined.length > 0) joined[joined.length - 1] += token;
    else joined.push(token);
    previousWasLetter = token.length === 1;
  }
  while (options.dropSuffix && joined.length > 1 && SUFFIXES.has(joined[joined.length - 1] ?? '')) joined.pop();
  return joined.join(' ');
}

/** "Dex Marrow (2003-2009)" -> "Dex Marrow": the disambiguator the pipeline adds for people with the same name. */
export function baseName(name: string): string {
  return name.replace(/\s*\([^)]*\)\s*$/, '').trim();
}

/** Allowed edit distance for a name of this many characters (normalized, spaces included). */
export function allowedDistance(length: number): 0 | 1 | 2 {
  if (length < 6) return 0;
  return length <= 10 ? 1 : 2;
}

/** Levenshtein distance, giving up (returning max + 1) as soon as it must exceed max. */
export function editDistance(a: string, b: string, max: number): number {
  if (Math.abs(a.length - b.length) > max) return max + 1;
  let previous = Array.from({ length: b.length + 1 }, (_, j) => j);
  for (let i = 1; i <= a.length; i++) {
    const current = [i];
    let rowMin = i;
    for (let j = 1; j <= b.length; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      const value = Math.min((previous[j] ?? 0) + 1, (current[j - 1] ?? 0) + 1, (previous[j - 1] ?? 0) + cost);
      current.push(value);
      rowMin = Math.min(rowMin, value);
    }
    if (rowMin > max) return max + 1;
    previous = current;
  }
  return previous[b.length] ?? max + 1;
}

interface KeyHit {
  entryId: string;
  origin: 'name' | 'alias';
}

export interface Index {
  entries: Map<string, Entry>;
  /** Normalized names and aliases with suffixes kept. */
  exactKept: Map<string, KeyHit[]>;
  /** The same with suffixes dropped. */
  exactDropped: Map<string, KeyHit[]>;
  /** Last name -> the one player who has it. Only names passing the uniqueness rule are here. */
  lastNames: Map<string, string>;
  /** Last names several players share. Not accepted as an answer; the player is asked which one. */
  sharedLastNames: Map<string, string[]>;
}

function addKey(map: Map<string, KeyHit[]>, key: string, hit: KeyHit): void {
  if (key === '') return;
  const list = map.get(key) ?? [];
  if (!list.some((h) => h.entryId === hit.entryId)) list.push(hit);
  map.set(key, list);
}

export function toEntries(universe: Universe): Entry[] {
  return [
    ...universe.players.map((e) => ({ ...e, kind: 'player' as const })),
    ...universe.teams.map((e) => ({ ...e, kind: 'team' as const })),
  ];
}

export function buildIndex(universe: Universe): Index {
  const entries = new Map<string, Entry>();
  const exactKept = new Map<string, KeyHit[]>();
  const exactDropped = new Map<string, KeyHit[]>();
  const lastNameOwners = new Map<string, Set<string>>();
  for (const entry of toEntries(universe)) {
    entries.set(entry.id, entry);
    const names: Array<[string, 'name' | 'alias']> = [[entry.name, 'name'], [baseName(entry.name), 'name'], ...entry.aliases.map((a): [string, 'alias'] => [a, 'alias'])];
    for (const [text, origin] of names) {
      addKey(exactKept, normalize(text), { entryId: entry.id, origin });
      addKey(exactDropped, normalize(text, { dropSuffix: true }), { entryId: entry.id, origin });
    }
    if (entry.kind === 'player') {
      const tokens = normalize(baseName(entry.name), { dropSuffix: true }).split(' ');
      const last = tokens[tokens.length - 1];
      if (tokens.length > 1 && last) {
        const owners = lastNameOwners.get(last) ?? new Set<string>();
        owners.add(entry.id);
        lastNameOwners.set(last, owners);
      }
    }
  }
  // A last name is only accepted if one player has it and it is not already a name or alias of anyone else.
  const lastNames = new Map<string, string>();
  const sharedLastNames = new Map<string, string[]>();
  for (const [last, owners] of lastNameOwners) {
    const [only] = [...owners];
    if (owners.size === 1 && only !== undefined && !exactKept.has(last) && !exactDropped.has(last)) lastNames.set(last, only);
    if (owners.size > 1 && !exactKept.has(last) && !exactDropped.has(last)) sharedLastNames.set(last, [...owners]);
  }
  return { entries, exactKept, exactDropped, lastNames, sharedLastNames };
}

function resolveHits(index: Index, hits: KeyHit[], distance: number, via?: MatchVia): MatchResult | null {
  const entries = [...new Set(hits.map((h) => h.entryId))].map((id) => index.entries.get(id)).filter((e): e is Entry => e !== undefined);
  if (entries.length === 0) return null;
  if (entries.length > 1) return { kind: 'ambiguous', entries };
  const entry = entries[0];
  if (!entry) return null;
  const origin = hits.some((h) => h.origin === 'name') ? 'name' : 'alias';
  return { kind: 'match', entry, via: via ?? origin, distance };
}

/** Recognize what the player typed as an entry of the universe. */
export function matchAnswer(index: Index, input: string): MatchResult {
  const kept = normalize(input);
  const dropped = normalize(input, { dropSuffix: true });
  if (dropped === '') return { kind: 'none' };

  const exact = resolveHits(index, index.exactKept.get(kept) ?? [], 0) ?? resolveHits(index, index.exactDropped.get(dropped) ?? [], 0);
  if (exact) return exact;

  const lastId = index.lastNames.get(dropped);
  const lastEntry = lastId === undefined ? undefined : index.entries.get(lastId);
  if (lastEntry) return { kind: 'match', entry: lastEntry, via: 'last-name', distance: 0 };

  const sharedIds = index.sharedLastNames.get(dropped);
  if (sharedIds) {
    const entries = sharedIds.map((id) => index.entries.get(id)).filter((e): e is Entry => e !== undefined);
    return { kind: 'ambiguous', entries };
  }

  // Typos: the closest key within the allowed distance, if it points at one entry only.
  let best = Infinity;
  let bestIds = new Set<string>();
  const consider = (key: string, ids: string[]): void => {
    const allowed = allowedDistance(key.length);
    if (allowed === 0) return;
    const d = editDistance(dropped, key, allowed);
    if (d > allowed) return;
    if (d < best) {
      best = d;
      bestIds = new Set(ids);
    } else if (d === best) {
      ids.forEach((id) => bestIds.add(id));
    }
  };
  for (const [key, hits] of index.exactDropped) consider(key, hits.map((h) => h.entryId));
  for (const [key, id] of index.lastNames) consider(key, [id]);
  if (bestIds.size === 0) return { kind: 'none' };
  const entries = [...bestIds].map((id) => index.entries.get(id)).filter((e): e is Entry => e !== undefined);
  const [first] = entries;
  if (entries.length === 1 && first) return { kind: 'match', entry: first, via: 'typo', distance: best };
  return { kind: 'ambiguous', entries };
}
