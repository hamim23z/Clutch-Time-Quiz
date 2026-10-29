/**
 * Autocomplete suggestions. They are drawn from the whole universe (every player and team), never from the valid
 * answers of the current prompt, so the list can never give an answer away.
 */
import { baseName, normalize, type Index } from './matching';
import type { Entry } from './types';

export interface Suggestion {
  entry: Entry;
  /** The alias that matched, when the name itself did not. */
  matchedAlias: string | null;
}

interface Candidate {
  text: string;
  isAlias: boolean;
}

function tokenize(text: string): string[] {
  const n = normalize(text);
  return n === '' ? [] : n.split(' ');
}

/** 0 = the name starts with the query, 1 = every query word starts a word, 2 = a word starts with each query word in order. */
function score(candidate: string[], query: string[]): number | null {
  if (query.length === 0 || candidate.length === 0) return null;
  const startsWith = query.every((q, i) => candidate[i]?.startsWith(q));
  if (startsWith) return 0;
  const everyWord = query.every((q) => candidate.some((c) => c.startsWith(q)));
  return everyWord ? 1 : null;
}

export function suggest(index: Index, query: string, limit = 6): Suggestion[] {
  const q = tokenize(query);
  if (q.length === 0) return [];
  const found: Array<{ s: Suggestion; rank: number; label: string }> = [];
  for (const entry of index.entries.values()) {
    const candidates: Candidate[] = [
      { text: entry.name, isAlias: false },
      { text: baseName(entry.name), isAlias: false },
      ...entry.aliases.map((a) => ({ text: a, isAlias: true })),
    ];
    let best: { rank: number; alias: string | null } | null = null;
    for (const c of candidates) {
      const sc = score(tokenize(c.text), q);
      if (sc === null) continue;
      const rank = sc + (c.isAlias ? 0.5 : 0);
      if (best === null || rank < best.rank) best = { rank, alias: c.isAlias ? c.text : null };
    }
    if (best) found.push({ s: { entry, matchedAlias: best.alias }, rank: best.rank, label: entry.name });
  }
  found.sort((a, b) => a.rank - b.rank || a.label.localeCompare(b.label));
  return found.slice(0, limit).map((f) => f.s);
}
