import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { parseScenarios } from './loadScenarios';
import type { Scenario } from './types';

// Tests run from web/ (npm test), so paths are relative to that folder.
export const SCENARIOS_PATH = resolve(process.cwd(), 'public/scenarios.json');
export const SCHEMA_PATH = resolve(process.cwd(), '../schema/scenarios.schema.json');

export function readMockJson(): unknown {
  return JSON.parse(readFileSync(SCENARIOS_PATH, 'utf8')) as unknown;
}

export function readMockScenarios(): Scenario[] {
  return parseScenarios(readMockJson());
}

/** A two-option scenario with the given win rates (0 to 1) for options "a" and "b". */
export function scenarioWith(winRateA: number, winRateB: number, id = 'mock-test'): Scenario {
  return {
    id,
    type: 'foul_up_three',
    state: { quarter: 4, margin: 3, secondsLeft: 8, possession: 'opponent' },
    question: 'Test question?',
    options: [
      { key: 'a', label: 'Option A', winRate: winRateA, n: 100 },
      { key: 'b', label: 'Option B', winRate: winRateB, n: 100 },
    ],
    actual: { choice: 'a', summary: 'It happened.', final: 'A 1, B 0', game: 'Test game' },
    difficulty: 'medium',
  };
}
