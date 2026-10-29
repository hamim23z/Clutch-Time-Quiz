import { describe, expect, it } from 'vitest';
import { divePrompts } from './schedule';
import { diveReducer, isOver, isRevealed, pointsMatchTier, startDive, totalPoints } from './dive2';
import { MAX_DIVE_POINTS, PROMPTS_PER_DIVE, SECONDS_PER_PROMPT, TIER_POINTS } from './tiers';
import { mockPrompts } from './testUtils';
import type { PromptResult, Tier } from './types';

const prompts = mockPrompts();
const result = (promptId: string, tier: Tier | null): PromptResult => ({
  promptId, status: tier === null ? 'invalid' : 'valid', input: 'x', matched: null, tier, points: tier === null ? 0 : TIER_POINTS[tier], countsAsWrong: true,
});

describe('the rules of a dive', () => {
  it('is 7 prompts of 25 seconds with tiers worth 10, 20, 35, 55, 75 and 100', () => {
    expect(PROMPTS_PER_DIVE).toBe(7);
    expect(SECONDS_PER_PROMPT).toBe(25);
    expect(Object.values(TIER_POINTS)).toEqual([10, 20, 35, 55, 75, 100]);
    expect(MAX_DIVE_POINTS).toBe(700);
  });
});

describe('diveReducer', () => {
  const state = () => startDive(divePrompts(prompts, 1));

  it('starts on the first prompt with nothing answered', () => {
    const s = state();
    expect(s.index).toBe(0);
    expect(s.results).toEqual([]);
    expect(isRevealed(s)).toBe(false);
  });

  it('records one answer per prompt and ignores a second', () => {
    let s = state();
    s = diveReducer(s, { type: 'submit', result: result(s.prompts[0]!.id, 3) });
    const again = diveReducer(s, { type: 'submit', result: result(s.prompts[0]!.id, 6) });
    expect(again).toBe(s);
    expect(isRevealed(s)).toBe(true);
  });

  it('only moves on once the prompt has been answered', () => {
    const s = state();
    expect(diveReducer(s, { type: 'next' })).toBe(s);
  });

  it('plays 7 prompts and ends, with the total and no more moves', () => {
    let s = state();
    const tiers: Array<Tier | null> = [1, 2, 3, 4, 5, 6, null];
    tiers.forEach((tier) => {
      s = diveReducer(s, { type: 'submit', result: result(s.prompts[s.index]!.id, tier) });
      s = diveReducer(s, { type: 'next' });
    });
    expect(isOver(s)).toBe(true);
    expect(s.results).toHaveLength(7);
    expect(totalPoints(s.results)).toBe(10 + 20 + 35 + 55 + 75 + 100 + 0);
    expect(diveReducer(s, { type: 'submit', result: result('x', 1) })).toBe(s);
    expect(diveReducer(s, { type: 'next' })).toBe(s);
  });

  it('checks that points agree with tiers', () => {
    expect(pointsMatchTier(result('p', 4))).toBe(true);
    expect(pointsMatchTier({ ...result('p', 4), points: 54 })).toBe(false);
    expect(pointsMatchTier(result('p', null))).toBe(true);
  });
});
