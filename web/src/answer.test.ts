import { describe, expect, it } from 'vitest';
import { resolveEntry, resolveText, timeoutResult } from './answer';
import { MOCK_OUTSIDE_RANGE_NAMES, isOutsideRange } from './outsideRange';
import { idOf, mockIndex, mockPrompts, mockUniverse } from './testUtils';
import { pointsMatchTier } from './dive';
import type { Prompt, PromptResult } from './types';

const index = mockIndex();
const prompts = mockPrompts();
const player = prompts.find((p) => p.id === 'mock-p-01') as Prompt; // 40+ points: 30 valid answers
const team = prompts.find((p) => p.id === 'mock-t-03') as Prompt; // a team prompt with 6 valid answers

const asResult = (r: ReturnType<typeof resolveText>): PromptResult => {
  if (r.kind !== 'result') throw new Error('expected a result');
  return r.result;
};
const someValid = (p: Prompt) => p.answers[0] as Prompt['answers'][number];
const someNotValid = (p: Prompt) => {
  const valid = new Set(p.answers.map((a) => a.id));
  const u = mockUniverse();
  const list = p.answerType === 'player' ? u.players : u.teams;
  return list.find((e) => !valid.has(e.id)) as (typeof list)[number];
};

describe('resolving typed answers', () => {
  it('scores a valid answer with its tier and points', () => {
    const a = someValid(player);
    const r = asResult(resolveText(player, index, a.name));
    expect(r).toMatchObject({ status: 'valid', tier: a.tier, points: a.points, countsAsWrong: true });
    expect(r.matched).toEqual({ id: a.id, name: a.name });
    expect(pointsMatchTier(r)).toBe(true);
  });

  it('accepts a valid answer typed with a typo, in lower case, or by alias', () => {
    const tavish = player.answers.find((a) => a.name === 'Aldric Ashgrove');
    if (!tavish) throw new Error('mock data changed: Aldric Ashgrove should be a valid answer of mock-p-01');
    expect(asResult(resolveText(player, index, 'aldrik ashgrove')).status).toBe('valid');
    expect(asResult(resolveText(player, index, 'ALDRIC ASHGROVE')).status).toBe('valid');
    expect(asResult(resolveText(player, index, 'Al Ashgrove')).points).toBe(tavish.points);
    expect(asResult(resolveText(player, index, 'Ashgrove')).status).toBe('valid'); // unique last name
  });

  it('marks a real universe entry that is not a valid answer as invalid, and keeps what it matched', () => {
    const other = someNotValid(player);
    const r = asResult(resolveText(player, index, other.name));
    expect(r).toMatchObject({ status: 'invalid', points: 0, tier: null, countsAsWrong: true });
    expect(r.matched?.id).toBe(other.id);
  });

  it('marks gibberish invalid with nothing matched', () => {
    const r = asResult(resolveText(player, index, 'qwerty zxcv'));
    expect(r).toMatchObject({ status: 'invalid', points: 0, matched: null, countsAsWrong: true });
  });

  it('does not accept a team for a player prompt or the other way round', () => {
    expect(asResult(resolveText(player, index, 'Harbor City Gulls')).status).toBe('invalid');
    expect(asResult(resolveText(team, index, 'Aldric Ashgrove')).status).toBe('invalid');
  });

  it('says "outside the data range", scores 0, and does not count it as wrong', () => {
    const r = asResult(resolveText(player, index, 'Orson Quillfeather'));
    expect(r).toMatchObject({ status: 'outside_range', points: 0, tier: null, matched: null, countsAsWrong: false });
    expect(asResult(resolveText(player, index, 'orson quilfeather')).status).toBe('outside_range'); // typos count too
  });

  it('only treats real, known out-of-range names that way', () => {
    expect(isOutsideRange('Orson Quillfeather')).toBe(true);
    expect(isOutsideRange('Somebody Else')).toBe(false);
    expect(MOCK_OUTSIDE_RANGE_NAMES.length).toBeGreaterThan(2);
    // a name inside the data range wins over the out-of-range list
    expect(asResult(resolveText(player, index, someValid(player).name, ['Aldric Ashgrove'])).status).toBe('valid');
  });

  it('asks again instead of guessing when two people share the typed name', () => {
    const r = resolveText(player, index, 'Dex Marrow');
    expect(r.kind).toBe('ambiguous');
    if (r.kind === 'ambiguous') expect(r.entries.map((e) => e.name).sort()).toEqual(['Dex Marrow (2003-2009)', 'Dex Marrow (2015-2022)']);
  });

  it('scores a picked suggestion exactly, so same-name players are told apart', () => {
    const entries = [...index.entries.values()];
    const a = entries.find((e) => e.name === 'Dex Marrow (2003-2009)');
    const b = entries.find((e) => e.name === 'Dex Marrow (2015-2022)');
    if (!a || !b) throw new Error('mock data changed');
    const prompt: Prompt = { ...player, answers: [{ id: a.id, name: a.name, tier: 4, points: 55 }, ...player.answers.slice(1, 16)] };
    expect(resolveEntry(prompt, a, 'Dex Marrow (2003-2009)').status).toBe('valid');
    expect(resolveEntry(prompt, b, 'Dex Marrow (2015-2022)').status).toBe('invalid');
    expect(idOf('Dex Marrow (2003-2009)')).toBe(a.id);
  });

  it('scores nothing for a timeout, whatever was typed', () => {
    const r = timeoutResult(player, 'Aldric Ash');
    expect(r).toMatchObject({ status: 'timeout', points: 0, tier: null, input: 'Aldric Ash', countsAsWrong: true });
  });

  it('accepts every valid answer of every mock prompt when its name is typed', () => {
    for (const p of prompts) {
      for (const a of p.answers) {
        const res = resolveText(p, index, a.name);
        expect(res.kind, `${p.id} ${a.name}`).toBe('result');
        if (res.kind === 'result') expect(res.result.status, `${p.id} ${a.name}`).toBe('valid');
      }
    }
  });
});
