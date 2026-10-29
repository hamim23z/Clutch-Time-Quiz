import { describe, expect, it, vi } from 'vitest';
import { browserStorage, loadHistory, saveHistory, type History, type StorageLike } from './storage';
import type { PromptResult } from './types';

const result = (i: number): PromptResult => ({ promptId: `p-${i}`, status: 'valid', input: 'x', matched: null, tier: 3, points: 35, countsAsWrong: false });
const dive = (daily: boolean) => ({ results: Array.from({ length: 7 }, (_, i) => result(i)), daily });
const memory = (): StorageLike & { data: Map<string, string> } => {
  const data = new Map<string, string>();
  return { data, getItem: (k) => data.get(k) ?? null, setItem: (k, v) => void data.set(k, v) };
};

describe('saving and loading the history', () => {
  it('round-trips finished dives', () => {
    const store = memory();
    const history: History = { 1: dive(true), 4: dive(false) };
    expect(saveHistory(store, 'k', history)).toBe(true);
    expect(loadHistory(store, 'k')).toEqual(history);
  });

  it('keeps the normal and preview histories apart', () => {
    const store = memory();
    saveHistory(store, 'real', { 1: dive(true) });
    expect(loadHistory(store, 'preview')).toEqual({});
  });

  it('works with no storage at all: nothing loads, nothing saves, nothing throws', () => {
    expect(loadHistory(null, 'k')).toEqual({});
    expect(saveHistory(null, 'k', { 1: dive(true) })).toBe(false);
  });

  it('survives a storage that throws on read or write', () => {
    const broken: StorageLike = {
      getItem: () => {
        throw new Error('SecurityError');
      },
      setItem: () => {
        throw new Error('QuotaExceededError');
      },
    };
    expect(loadHistory(broken, 'k')).toEqual({});
    expect(saveHistory(broken, 'k', { 1: dive(true) })).toBe(false);
  });

  it('ignores corrupted or malformed values instead of failing', () => {
    const store = memory();
    for (const bad of ['{not json', 'null', '[]', '"text"', '{"1":5}', '{"x":{"results":[],"daily":true}}', '{"0":{"results":[],"daily":true}}']) {
      store.data.set('k', bad);
      expect(loadHistory(store, 'k')).toEqual({});
    }
    store.data.set('k', JSON.stringify({ 2: { results: [result(1)], daily: true }, 3: dive(true) })); // a short dive is dropped, a good one is kept
    expect(Object.keys(loadHistory(store, 'k'))).toEqual(['3']);
  });
});

describe('browserStorage', () => {
  it('returns null instead of throwing when localStorage is blocked', () => {
    const spy = vi.spyOn(window, 'localStorage', 'get').mockImplementation(() => {
      throw new Error('blocked');
    });
    expect(browserStorage()).toBeNull();
    spy.mockRestore();
  });

  it('returns null when writing is refused (a full or private store)', () => {
    const spy = vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
      throw new Error('QuotaExceededError');
    });
    expect(browserStorage()).toBeNull();
    spy.mockRestore();
  });

  it('returns the real localStorage when it works', () => {
    expect(browserStorage()).not.toBeNull();
  });
});
