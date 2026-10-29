import { describe, expect, it } from 'vitest';
import type { History } from './storage';
import { computeStreaks } from './streaks';
import type { PromptResult } from './types';

const r = (tier: PromptResult['tier'], status: PromptResult['status'] = 'valid'): PromptResult => ({ promptId: 'p', status, input: '', matched: null, tier, points: 0, countsAsWrong: status !== 'outside_range' });
const played = (days: number[], daily = true): History => Object.fromEntries(days.map((d) => [d, { results: Array.from({ length: 7 }, () => r(null)), daily }]));

describe('streaks', () => {
  it('is zero with nothing played', () => {
    expect(computeStreaks({}, 5)).toEqual({ current: 0, best: 0 });
  });

  it('counts consecutive days ending today', () => {
    expect(computeStreaks(played([3, 4, 5]), 5)).toEqual({ current: 3, best: 3 });
  });

  it('keeps the streak alive until the day is over: yesterday counts when today is not played yet', () => {
    expect(computeStreaks(played([3, 4]), 5)).toEqual({ current: 2, best: 2 });
  });

  it('a day with no dive breaks it', () => {
    expect(computeStreaks(played([1, 2, 3]), 5)).toEqual({ current: 0, best: 3 });
    expect(computeStreaks(played([1, 2, 3, 5]), 5)).toEqual({ current: 1, best: 3 });
  });

  it('keeps the best streak after a break and starts again from one', () => {
    expect(computeStreaks(played([1, 2, 3, 4, 6, 7]), 7)).toEqual({ current: 2, best: 4 });
  });

  it('does not count archive plays', () => {
    const history = { ...played([2, 3, 4], false), ...played([5]) };
    expect(computeStreaks(history, 5)).toEqual({ current: 1, best: 1 });
    expect(computeStreaks(played([1, 2, 3], false), 3)).toEqual({ current: 0, best: 0 });
  });

  it('does not care whether the answers were right: wrong, timed out and outside-range answers never break it', () => {
    const history: History = {
      1: { results: Array.from({ length: 7 }, () => r(null, 'invalid')), daily: true },
      2: { results: Array.from({ length: 7 }, () => r(null, 'timeout')), daily: true },
      3: { results: Array.from({ length: 7 }, () => r(null, 'outside_range')), daily: true },
    };
    expect(computeStreaks(history, 3)).toEqual({ current: 3, best: 3 });
  });

  it('ignores a day in the future of the clock', () => {
    expect(computeStreaks(played([1, 2, 3]), 2)).toEqual({ current: 2, best: 3 });
  });
});
