import Ajv2020 from 'ajv/dist/2020.js';
import { describe, expect, it } from 'vitest';
import { parsePrompts, parseUniverse } from './loadData';
import { PROMPTS_SCHEMA_PATH, readJson, PROMPTS_PATH, UNIVERSE_PATH, UNIVERSE_SCHEMA_PATH, mockPrompts, mockUniverse } from './testUtils';
import { TIER_POINTS } from './tiers';
import type { Prompt, Universe } from './types';

// ajv ships CommonJS; under ESM the class can arrive as .default
const Ajv = ((Ajv2020 as unknown as { default?: typeof Ajv2020 }).default ?? Ajv2020) as typeof Ajv2020;
const ajv = new Ajv({ allErrors: true, strict: true });
const validatePrompts = ajv.compile(readJson(PROMPTS_SCHEMA_PATH) as object);
const validateUniverse = ajv.compile(readJson(UNIVERSE_SCHEMA_PATH) as object);

const clonePrompts = (): Prompt[] => JSON.parse(JSON.stringify(readJson(PROMPTS_PATH))) as Prompt[];
const cloneUniverse = (): Universe => JSON.parse(JSON.stringify(readJson(UNIVERSE_PATH))) as Universe;

describe('the mock files are valid against the schemas', () => {
  it('prompts.json validates against schema/prompts.schema.json', () => {
    const ok = validatePrompts(readJson(PROMPTS_PATH));
    expect(validatePrompts.errors ?? []).toEqual([]);
    expect(ok).toBe(true);
  });

  it('universe.json validates against schema/universe.schema.json', () => {
    const ok = validateUniverse(readJson(UNIVERSE_PATH));
    expect(validateUniverse.errors ?? []).toEqual([]);
    expect(ok).toBe(true);
  });
});

describe('the mock prompts', () => {
  const prompts = mockPrompts();

  it('are 10 prompts: a mix of player and team, with mixed difficulty', () => {
    expect(prompts).toHaveLength(10);
    expect(new Set(prompts.map((p) => p.answerType))).toEqual(new Set(['player', 'team']));
    expect(new Set(prompts.map((p) => p.difficulty))).toEqual(new Set(['easy', 'medium', 'hard']));
    expect(prompts.filter((p) => p.answerType === 'team').length).toBeGreaterThanOrEqual(3);
  });

  it('have 15 or more valid answers per player prompt and 5 or more per team prompt', () => {
    for (const p of prompts) expect(p.answers.length, p.id).toBeGreaterThanOrEqual(p.answerType === 'player' ? 15 : 5);
  });

  it('state their era and use ids with a mock- prefix', () => {
    for (const p of prompts) {
      expect(p.text, p.id).toMatch(/^Since 20\d\d\b/);
      expect(p.id.startsWith('mock-')).toBe(true);
    }
    expect(new Set(prompts.map((p) => p.id)).size).toBe(prompts.length);
  });

  it('give each answer a tier whose points follow the table', () => {
    for (const p of prompts) for (const a of p.answers) expect(a.points, `${p.id} ${a.name}`).toBe(TIER_POINTS[a.tier]);
  });

  it('use every tier somewhere, and one tier per person across prompts', () => {
    const tiersSeen = new Set(prompts.flatMap((p) => p.answers.map((a) => a.tier)));
    expect(tiersSeen).toEqual(new Set([1, 2, 3, 4, 5, 6]));
    const byId = new Map<string, number>();
    for (const p of prompts) for (const a of p.answers) {
      expect(byId.get(a.id) ?? a.tier, `${a.name} has different tiers in different prompts`).toBe(a.tier);
      byId.set(a.id, a.tier);
    }
  });

  it('have unique answers inside a prompt, all pointing at the universe with the same name', () => {
    const u = mockUniverse();
    const names = new Map([...u.players, ...u.teams].map((e) => [e.id, e.name]));
    for (const p of prompts) {
      expect(new Set(p.answers.map((a) => a.id)).size, p.id).toBe(p.answers.length);
      for (const a of p.answers) expect(names.get(a.id), `${p.id} ${a.id}`).toBe(a.name);
      const kind = p.answerType === 'player' ? u.players : u.teams;
      const ids = new Set(kind.map((e) => e.id));
      for (const a of p.answers) expect(ids.has(a.id), `${p.id}: ${a.name} is not a ${p.answerType}`).toBe(true);
    }
  });

  it('get harder as they have fewer, more obscure answers', () => {
    const avgTier = (d: string) => {
      const xs = prompts.filter((p) => p.difficulty === d).flatMap((p) => p.answers.map((a) => a.tier));
      return xs.reduce((a, b) => a + b, 0) / xs.length;
    };
    expect(avgTier('hard')).toBeGreaterThan(avgTier('easy'));
  });
});

describe('the mock universe', () => {
  const u = mockUniverse();
  const all = [...u.players, ...u.teams];

  it('has at least 80 entries, with invented names, and covers more than any one prompt', () => {
    expect(all.length).toBeGreaterThanOrEqual(80);
    expect(all.every((e) => e.id.startsWith('mock-'))).toBe(true);
    const mostAnswers = Math.max(...mockPrompts().map((p) => p.answers.length));
    expect(all.length).toBeGreaterThan(mostAnswers * 2);
  });

  it('has unique ids and unique names, so no two entries are the same text', () => {
    expect(new Set(all.map((e) => e.id)).size).toBe(all.length);
    expect(new Set(all.map((e) => e.name)).size).toBe(all.length);
  });

  it('includes entries that are valid for no prompt', () => {
    const used = new Set(mockPrompts().flatMap((p) => p.answers.map((a) => a.id)));
    expect(all.filter((e) => !used.has(e.id)).length).toBeGreaterThan(10);
  });
});

describe('the schemas reject bad data', () => {
  const badPrompts = (change: (p: Prompt[]) => void): boolean => {
    const data = clonePrompts();
    change(data);
    return validatePrompts(data) as boolean;
  };
  const badUniverse = (change: (u: Universe) => void): boolean => {
    const data = cloneUniverse();
    change(data);
    return validateUniverse(data) as boolean;
  };
  const playerPrompt = (p: Prompt[]): Prompt => p.find((x) => x.answerType === 'player') as Prompt;
  const teamPrompt = (p: Prompt[]): Prompt => p.find((x) => x.answerType === 'team') as Prompt;

  it('accepts the unchanged copies (sanity check)', () => {
    expect(badPrompts(() => undefined)).toBe(true);
    expect(badUniverse(() => undefined)).toBe(true);
  });

  it('rejects a player prompt with fewer than 15 answers, and a team prompt with fewer than 5', () => {
    expect(badPrompts((p) => void (playerPrompt(p).answers = playerPrompt(p).answers.slice(0, 14)))).toBe(false);
    expect(badPrompts((p) => void (teamPrompt(p).answers = teamPrompt(p).answers.slice(0, 4)))).toBe(false);
  });

  it('rejects a prompt that does not state its era', () => {
    expect(badPrompts((p) => void (playerPrompt(p).text = 'Name a player who scored 40 or more points.'))).toBe(false);
  });

  it('rejects a tier whose points do not match, and unknown tiers and points', () => {
    expect(badPrompts((p) => void (playerPrompt(p).answers[0]!.points = 20 === playerPrompt(p).answers[0]!.points ? 35 : 20))).toBe(false);
    expect(badPrompts((p) => void ((playerPrompt(p).answers[0] as unknown as { tier: number }).tier = 7))).toBe(false);
    expect(badPrompts((p) => void ((playerPrompt(p).answers[0] as unknown as { points: number }).points = 99))).toBe(false);
  });

  it('rejects an unknown answer type or difficulty, and extra or missing fields', () => {
    expect(badPrompts((p) => void ((p[0] as unknown as { answerType: string }).answerType = 'coach'))).toBe(false);
    expect(badPrompts((p) => void ((p[0] as unknown as { difficulty: string }).difficulty = 'brutal'))).toBe(false);
    expect(badPrompts((p) => void ((p[0] as unknown as Record<string, unknown>).extra = 1))).toBe(false);
    expect(badPrompts((p) => void delete (p[0] as unknown as Partial<Prompt>).answers)).toBe(false);
    expect(validatePrompts([])).toBe(false);
  });

  it('rejects a universe without teams, with empty names, or with duplicate aliases', () => {
    expect(badUniverse((u) => void ((u as unknown as { teams?: unknown }).teams = []))).toBe(false);
    expect(badUniverse((u) => void (u.players[0]!.name = ''))).toBe(false);
    expect(badUniverse((u) => void (u.players[0]!.aliases = ['x', 'x']))).toBe(false);
    expect(badUniverse((u) => void delete (u.players[0] as unknown as Partial<Universe['players'][number]>).aliases)).toBe(false);
    expect(badUniverse((u) => void ((u.players[0] as unknown as Record<string, unknown>).fame = 1))).toBe(false);
  });
});

describe('the runtime checks in the app', () => {
  it('accept the mock files', () => {
    const u = parseUniverse(readJson(UNIVERSE_PATH));
    expect(parsePrompts(readJson(PROMPTS_PATH), u)).toHaveLength(10);
  });

  it('refuse an answer that is not in the universe, and malformed files', () => {
    const u = mockUniverse();
    const p = clonePrompts();
    p[0]!.answers[0]!.id = 'mock-pl-999';
    expect(() => parsePrompts(p, u)).toThrow(/not in the universe/);
    expect(() => parsePrompts([], u)).toThrow();
    expect(() => parseUniverse({ players: [] })).toThrow();
    expect(() => parseUniverse(null)).toThrow();
  });
});
