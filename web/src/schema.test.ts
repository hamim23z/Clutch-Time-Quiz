import { readFileSync } from 'node:fs';
import Ajv2020 from 'ajv/dist/2020.js';
import { describe, expect, it } from 'vitest';
import { parseScenarios } from './loadScenarios';
import { bestOptionKey } from './scoring';
import { readMockJson, SCHEMA_PATH } from './testUtils';
import type { Scenario } from './types';

const schema = JSON.parse(readFileSync(SCHEMA_PATH, 'utf8')) as object;
// ajv ships CommonJS; under ESM the class can arrive as .default
const Ajv = ((Ajv2020 as unknown as { default?: typeof Ajv2020 }).default ?? Ajv2020) as typeof Ajv2020;
const validate = new Ajv({ allErrors: true, strict: true }).compile(schema);

const clone = (): Scenario[] => JSON.parse(JSON.stringify(readMockJson())) as Scenario[];

describe('mock scenarios.json', () => {
  it('validates against schema/scenarios.schema.json', () => {
    const ok = validate(readMockJson());
    expect(validate.errors ?? []).toEqual([]);
    expect(ok).toBe(true);
  });

  const scenarios = clone();

  it('has 10 scenarios covering all 3 types and mixed difficulty', () => {
    expect(scenarios).toHaveLength(10);
    expect(new Set(scenarios.map((s) => s.type))).toEqual(new Set(['foul_up_three', 'down_three', 'last_shot']));
    expect(new Set(scenarios.map((s) => s.difficulty))).toEqual(new Set(['easy', 'medium', 'hard']));
  });

  it('is marked as mock data and has unique ids', () => {
    expect(scenarios.every((s) => s.id.startsWith('mock-'))).toBe(true);
    expect(new Set(scenarios.map((s) => s.id)).size).toBe(scenarios.length);
  });

  it('follows the rules the schema cannot express', () => {
    for (const s of scenarios) {
      const keys = s.options.map((o) => o.key);
      expect(new Set(keys).size, s.id).toBe(keys.length);
      expect(keys, s.id).toContain(s.actual.choice);
      expect(Math.min(...s.options.map((o) => o.n)), s.id).toBeGreaterThanOrEqual(30);
    }
  });

  it('has a spread of gaps so every scoring result is reachable', () => {
    const gaps = scenarios.map((s) => {
      const rates = s.options.map((o) => o.winRate);
      return (Math.max(...rates) - Math.min(...rates)) * 100;
    });
    expect(gaps.some((g) => g <= 3)).toBe(true);
    expect(gaps.some((g) => g > 3 && g <= 10)).toBe(true);
    expect(gaps.some((g) => g > 10)).toBe(true);
    // the easy ones are the wide gaps and the hard ones the narrow gaps
    const avg = (d: string) => {
      const xs = scenarios.flatMap((s, i) => (s.difficulty === d ? [gaps[i] ?? 0] : []));
      return xs.reduce((a, b) => a + b, 0) / xs.length;
    };
    expect(avg('easy')).toBeGreaterThan(avg('hard'));
  });

  it('keeps every scenario answerable (a best option exists)', () => {
    for (const s of scenarios) expect(bestOptionKey(s)).toBeTruthy();
  });
});

describe('schema rejects bad data', () => {
  const bad = (change: (s: Scenario[]) => void): boolean => {
    const data = clone();
    change(data);
    return validate(data) as boolean;
  };

  it('accepts the unchanged copy (sanity check)', () => {
    expect(bad(() => undefined)).toBe(true);
  });

  it('rejects an option with fewer than 30 samples', () => {
    expect(bad((d) => void (d[0]!.options[0]!.n = 29))).toBe(false);
  });

  it('rejects a win rate above 1 or below 0', () => {
    expect(bad((d) => void (d[0]!.options[0]!.winRate = 1.2))).toBe(false);
    expect(bad((d) => void (d[0]!.options[0]!.winRate = -0.1))).toBe(false);
  });

  it('rejects an unknown type or difficulty', () => {
    expect(bad((d) => void ((d[0] as unknown as { type: string }).type = 'dunk_contest'))).toBe(false);
    expect(bad((d) => void ((d[0] as unknown as { difficulty: string }).difficulty = 'impossible'))).toBe(false);
  });

  it('rejects one option, four options, and a missing field', () => {
    expect(bad((d) => void (d[0]!.options = d[0]!.options.slice(0, 1)))).toBe(false);
    expect(bad((d) => void (d[0]!.options = [...d[0]!.options, ...d[0]!.options]))).toBe(false);
    expect(bad((d) => void delete (d[0] as unknown as Partial<Scenario>).actual)).toBe(false);
  });

  it('rejects extra properties and an empty file', () => {
    expect(bad((d) => void ((d[0] as unknown as Record<string, unknown>).extra = 1))).toBe(false);
    expect(validate([])).toBe(false);
  });
});

describe('parseScenarios (runtime check in the app)', () => {
  it('accepts the mock file', () => {
    expect(parseScenarios(readMockJson())).toHaveLength(10);
  });

  it.each([
    ['not an array', {}],
    ['an empty array', []],
    ['a missing field', [{ id: 'x' }]],
  ])('rejects %s', (_name, data) => {
    expect(() => parseScenarios(data)).toThrow();
  });

  it('rejects an actual.choice that is not an option, and duplicate option keys', () => {
    const data = clone();
    data[0]!.actual.choice = 'nope';
    expect(() => parseScenarios(data)).toThrow(/not an option/);
    const dup = clone();
    dup[0]!.options[1]!.key = dup[0]!.options[0]!.key;
    expect(() => parseScenarios(dup)).toThrow(/unique/);
  });
});
