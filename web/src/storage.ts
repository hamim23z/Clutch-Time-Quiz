import type { PromptResult } from './types';

/** The part of localStorage the game uses. A test can pass a plain object. */
export interface StorageLike {
  getItem(key: string): string | null;
  setItem(key: string, value: string): void;
}

/** A finished dive on this device. */
export interface PlayedDive {
  results: PromptResult[];
  /** True when it was played on its own day (counts for the streak); false for an archive play. */
  daily: boolean;
}

/** Finished dives by dive number. */
export type History = Record<number, PlayedDive>;

/** localStorage, or null when the browser refuses it (private windows, blocked site data). Never throws. */
export function browserStorage(): StorageLike | null {
  try {
    if (typeof window === 'undefined' || !window.localStorage) return null;
    const probe = '__deepcut_probe__';
    window.localStorage.setItem(probe, '1');
    window.localStorage.removeItem(probe);
    return window.localStorage;
  } catch {
    return null;
  }
}

const isResult = (r: unknown): r is PromptResult => {
  if (typeof r !== 'object' || r === null) return false;
  const o = r as Record<string, unknown>;
  return typeof o['promptId'] === 'string' && typeof o['status'] === 'string' && typeof o['points'] === 'number' && typeof o['input'] === 'string' && 'tier' in o;
};

/** Read the history. Anything unreadable or malformed is ignored, so a bad value never stops the game. */
export function loadHistory(storage: StorageLike | null, key: string): History {
  if (!storage) return {};
  try {
    const raw = storage.getItem(key);
    if (!raw) return {};
    const data = JSON.parse(raw) as unknown;
    if (typeof data !== 'object' || data === null) return {};
    const out: History = {};
    for (const [k, v] of Object.entries(data as Record<string, unknown>)) {
      const number = Number(k);
      if (!Number.isInteger(number) || number < 1 || typeof v !== 'object' || v === null) continue;
      const { results, daily } = v as { results?: unknown; daily?: unknown };
      if (Array.isArray(results) && results.length === 7 && results.every(isResult) && typeof daily === 'boolean') out[number] = { results, daily };
    }
    return out;
  } catch {
    return {};
  }
}

/** Write the history. Returns false (and does nothing else) if the browser refuses; the game carries on without saving. */
export function saveHistory(storage: StorageLike | null, key: string, history: History): boolean {
  if (!storage) return false;
  try {
    storage.setItem(key, JSON.stringify(history));
    return true;
  } catch {
    return false;
  }
}
