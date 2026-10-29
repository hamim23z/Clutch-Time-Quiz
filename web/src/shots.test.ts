import { describe, expect, it } from 'vitest';
import { MISS_NAME, SHOT_NAMES, TIER_NAMES, shotForPoints, shotForResult } from './shots';
import { TIER_POINTS } from './tiers';
import type { PromptResult, Tier } from './types';

const result = (status: PromptResult['status'], tier: Tier | null): PromptResult => ({
  promptId: 'p', status, input: 'x', matched: null, tier, points: tier === null ? 0 : TIER_POINTS[tier], countsAsWrong: status !== 'outside_range',
});

describe('which shot each outcome gets', () => {
  it.each([
    [0, 'airball', null, 'Airball'],
    [10, 'clank', 1, 'Garbage time'],
    [20, 'rattle', 2, 'Bench mob'],
    [35, 'bank', 3, 'Starting five'],
    [55, 'swish', 4, 'All-Star'],
    [75, 'deep-swish', 5, 'Buzzer beater'],
    [100, 'dunk', 6, 'Poster dunk'],
  ] as const)('%i points -> %s (tier %s, "%s")', (points, name, tier, label) => {
    expect(shotForPoints(points)).toEqual({ name, tier, label, points });
  });

  it('covers all seven shots exactly once', () => {
    const names = [0, 10, 20, 35, 55, 75, 100].map((p) => shotForPoints(p).name);
    expect(new Set(names).size).toBe(7);
    expect([...names].sort()).toEqual([...SHOT_NAMES].sort());
  });

  it('has six different, non-empty tier names and a miss name', () => {
    const names = Object.values(TIER_NAMES);
    expect(names).toHaveLength(6);
    expect(new Set(names).size).toBe(6);
    expect(names.every((n) => n.length > 0)).toBe(true);
    expect(MISS_NAME).toBe('Airball');
  });

  it('refuses points that are not a tier value', () => {
    for (const bad of [5, 11, 99, -10, 101]) expect(() => shotForPoints(bad)).toThrow();
  });

  it('gives every miss an airball: wrong, timed out and outside the data range', () => {
    for (const status of ['invalid', 'timeout', 'outside_range'] as const) expect(shotForResult(result(status, null)).name).toBe('airball');
  });

  it('gives a valid answer the shot of its tier', () => {
    for (const tier of [1, 2, 3, 4, 5, 6] as const) expect(shotForResult(result('valid', tier))).toEqual(shotForPoints(TIER_POINTS[tier]));
  });
});
