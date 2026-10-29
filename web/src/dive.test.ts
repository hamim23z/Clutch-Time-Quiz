import { describe, expect, it } from 'vitest';
import { diveReducer, isOver, isRevealed, pickDive, pointsMatchTier, startDive, totalPoints } from './dive';
import { MAX_DIVE_POINTS, PROMPTS_PER_DIVE, SECONDS_PER_PROMPT, TIER_POINTS } from './tiers';
import { mockPrompts } from './testUtils';
import type { PromptResult, Tier } from './types';

const prompts = mockPrompts();
const seq = (values: number[]) => {
  let i = 0;
  return () => values[i++ % values.length] ?? 0;
};
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
  const state = () => startDive(pickDive(prompts, seq([0.3, 0.6, 0.1])));

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

describe('pickDive', () => {
  it('picks 7 different prompts with at least 2 of each answer type', () => {
    for (const values of [[0.1], [0.9], [0.5, 0.2, 0.8], [0.33, 0.66]]) {
      const dive = pickDive(prompts, seq(values));
      expect(dive).toHaveLength(7);
      expect(new Set(dive.map((p) => p.id)).size).toBe(7);
      expect(dive.filter((p) => p.answerType === 'player').length).toBeGreaterThanOrEqual(2);
      expect(dive.filter((p) => p.answerType === 'team').length).toBeGreaterThanOrEqual(2);
    }
  });

  it('is repeatable for the same random source and varies with it', () => {
    const a = pickDive(prompts, seq([0.1, 0.9, 0.5, 0.3, 0.7, 0.2])).map((p) => p.id);
    const b = pickDive(prompts, seq([0.1, 0.9, 0.5, 0.3, 0.7, 0.2])).map((p) => p.id);
    const c = pickDive(prompts, seq([0.95, 0.4, 0.15, 0.6, 0.05, 0.8])).map((p) => p.id);
    expect(a).toEqual(b);
    expect(a).not.toEqual(c);
  });

  it('returns what it has when there are fewer prompts than a dive, and leaves its input alone', () => {
    const ids = prompts.map((p) => p.id);
    expect(pickDive(prompts.slice(0, 4))).toHaveLength(4);
    pickDive(prompts);
    expect(prompts.map((p) => p.id)).toEqual(ids);
  });
});
