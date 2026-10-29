import { TIER_POINTS } from './tiers';
import type { Prompt, PromptResult } from './types';

export interface DiveState {
  prompts: Prompt[];
  /** Index of the prompt in play; equal to prompts.length once the dive is over. */
  index: number;
  results: PromptResult[];
}

export type DiveAction = { type: 'submit'; result: PromptResult } | { type: 'next' };

export function startDive(prompts: Prompt[]): DiveState {
  return { prompts, index: 0, results: [] };
}

export const isRevealed = (state: DiveState): boolean => state.results.length > state.index;
export const isOver = (state: DiveState): boolean => state.index >= state.prompts.length;
export const currentPrompt = (state: DiveState): Prompt | undefined => state.prompts[state.index];

export function diveReducer(state: DiveState, action: DiveAction): DiveState {
  switch (action.type) {
    case 'submit':
      if (isOver(state) || isRevealed(state)) return state; // one answer per prompt
      return { ...state, results: [...state.results, action.result] };
    case 'next':
      return isRevealed(state) && !isOver(state) ? { ...state, index: state.index + 1 } : state;
  }
}

export const totalPoints = (results: readonly PromptResult[]): number => results.reduce((sum, r) => sum + r.points, 0);

/** Check that a result's points agree with the tier table. Used by tests and as a guard against bad data. */
export const pointsMatchTier = (r: PromptResult): boolean => (r.tier === null ? r.points === 0 : TIER_POINTS[r.tier] === r.points);
