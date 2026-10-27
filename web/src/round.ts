import { scoreHole } from './scoring';
import type { HoleRecord, Scenario } from './types';

export const HOLES_PER_ROUND = 5;

export interface RoundState {
  scenarios: Scenario[];
  /** Index of the hole being played. Equal to scenarios.length once the round is over. */
  index: number;
  /** The key picked on the current hole, or null while the player is still deciding. */
  pickedKey: string | null;
  records: HoleRecord[];
}

export type RoundAction =
  | { type: 'pick'; key: string }
  | { type: 'next' }
  | { type: 'restart'; scenarios: Scenario[] };

export function startRound(scenarios: Scenario[]): RoundState {
  return { scenarios, index: 0, pickedKey: null, records: [] };
}

export function isFinished(state: RoundState): boolean {
  return state.index >= state.scenarios.length;
}

export function currentScenario(state: RoundState): Scenario | undefined {
  return state.scenarios[state.index];
}

export function roundReducer(state: RoundState, action: RoundAction): RoundState {
  switch (action.type) {
    case 'pick': {
      const scenario = currentScenario(state);
      if (!scenario || state.pickedKey !== null) return state; // ignore a second pick on the same hole
      return {
        ...state,
        pickedKey: action.key,
        records: [...state.records, scoreHole(scenario, action.key)],
      };
    }
    case 'next':
      if (state.pickedKey === null || isFinished(state)) return state;
      return { ...state, index: state.index + 1, pickedKey: null };
    case 'restart':
      return startRound(action.scenarios);
  }
}

/** Pick `count` different scenarios at random (partial Fisher-Yates). rng returns [0, 1). */
export function pickRound(
  all: readonly Scenario[],
  count: number = HOLES_PER_ROUND,
  rng: () => number = Math.random,
): Scenario[] {
  const pool = [...all];
  const n = Math.min(count, pool.length);
  for (let i = 0; i < n; i++) {
    const j = i + Math.floor(rng() * (pool.length - i));
    const a = pool[i];
    const b = pool[j];
    if (a === undefined || b === undefined) continue;
    pool[i] = b;
    pool[j] = a;
  }
  return pool.slice(0, n);
}
