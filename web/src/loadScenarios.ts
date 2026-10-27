import type { Difficulty, Possession, Scenario, ScenarioOption, ScenarioType } from './types';

const TYPES: readonly ScenarioType[] = ['foul_up_three', 'down_three', 'last_shot'];
const DIFFICULTIES: readonly Difficulty[] = ['easy', 'medium', 'hard'];
const POSSESSIONS: readonly Possession[] = ['team', 'opponent'];

type Obj = Record<string, unknown>;

function isObject(value: unknown): value is Obj {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function str(obj: Obj, key: string, where: string): string {
  const value = obj[key];
  if (typeof value !== 'string' || value === '') throw new Error(`${where}: "${key}" must be a non-empty string`);
  return value;
}

function num(obj: Obj, key: string, where: string): number {
  const value = obj[key];
  if (typeof value !== 'number' || !Number.isFinite(value)) throw new Error(`${where}: "${key}" must be a number`);
  return value;
}

function oneOf<T extends string>(obj: Obj, key: string, allowed: readonly T[], where: string): T {
  const value = obj[key];
  const found = allowed.find((a) => a === value);
  if (found === undefined) throw new Error(`${where}: "${key}" must be one of ${allowed.join(', ')}`);
  return found;
}

function child(obj: Obj, key: string, where: string): Obj {
  const value = obj[key];
  if (!isObject(value)) throw new Error(`${where}: "${key}" must be an object`);
  return value;
}

function parseOption(raw: unknown, where: string): ScenarioOption {
  if (!isObject(raw)) throw new Error(`${where}: option must be an object`);
  const winRate = num(raw, 'winRate', where);
  if (winRate < 0 || winRate > 1) throw new Error(`${where}: winRate must be between 0 and 1`);
  return { key: str(raw, 'key', where), label: str(raw, 'label', where), winRate, n: num(raw, 'n', where) };
}

function parseScenario(raw: unknown, index: number): Scenario {
  if (!isObject(raw)) throw new Error(`scenario ${index} must be an object`);
  const id = str(raw, 'id', `scenario ${index}`);
  const where = `scenario ${id}`;
  const state = child(raw, 'state', where);
  const actual = child(raw, 'actual', where);
  const rawOptions = raw['options'];
  if (!Array.isArray(rawOptions) || rawOptions.length < 2 || rawOptions.length > 3) {
    throw new Error(`${where}: "options" must have 2 or 3 entries`);
  }
  const options = rawOptions.map((o: unknown) => parseOption(o, where));
  if (new Set(options.map((o) => o.key)).size !== options.length) throw new Error(`${where}: option keys must be unique`);
  const choice = str(actual, 'choice', where);
  if (!options.some((o) => o.key === choice)) throw new Error(`${where}: actual.choice "${choice}" is not an option`);
  return {
    id,
    type: oneOf(raw, 'type', TYPES, where),
    state: {
      quarter: num(state, 'quarter', where),
      margin: num(state, 'margin', where),
      secondsLeft: num(state, 'secondsLeft', where),
      possession: oneOf(state, 'possession', POSSESSIONS, where),
    },
    question: str(raw, 'question', where),
    options,
    actual: {
      choice,
      summary: str(actual, 'summary', where),
      final: str(actual, 'final', where),
      game: str(actual, 'game', where),
    },
    difficulty: oneOf(raw, 'difficulty', DIFFICULTIES, where),
  };
}

/** Check the shape of scenarios.json at runtime and return typed scenarios. Throws a readable error. */
export function parseScenarios(data: unknown): Scenario[] {
  if (!Array.isArray(data) || data.length === 0) throw new Error('scenarios.json must be a non-empty array');
  return data.map((raw: unknown, i: number) => parseScenario(raw, i));
}

export async function loadScenarios(url: string): Promise<Scenario[]> {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`Could not load ${url} (${response.status})`);
  return parseScenarios((await response.json()) as unknown);
}
