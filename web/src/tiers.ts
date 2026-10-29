import type { Tier } from './types';

export const TIERS: readonly Tier[] = [1, 2, 3, 4, 5, 6];

/** Points by tier. Tier 1 is the most famous answer (top 3%), tier 6 the most obscure (bottom 25%). */
export const TIER_POINTS: Record<Tier, number> = { 1: 10, 2: 20, 3: 35, 4: 55, 5: 75, 6: 100 };

export const TIER_RANGES: Record<Tier, string> = {
  1: 'Top 3% most famous',
  2: '3 to 10%',
  3: '10 to 25%',
  4: '25 to 50%',
  5: '50 to 75%',
  6: 'Bottom 25%, the deepest cuts',
};

export const PROMPTS_PER_DIVE = 7;
export const SECONDS_PER_PROMPT = 25;
/** Seven prompts, each worth at most 100. */
export const MAX_DIVE_POINTS = PROMPTS_PER_DIVE * TIER_POINTS[6];
