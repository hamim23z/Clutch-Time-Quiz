import { describe, expect, it } from 'vitest';
import { currentScenario, HOLES_PER_ROUND, isFinished, pickRound, roundReducer, startRound } from './round';
import { totalStrokes } from './scoring';
import { readMockScenarios, scenarioWith } from './testUtils';

const five = () => Array.from({ length: 5 }, (_, i) => scenarioWith(0.9, 0.5, `mock-${i}`));

describe('roundReducer', () => {
  it('starts on hole 1 with nothing picked', () => {
    const state = startRound(five());
    expect(state).toMatchObject({ index: 0, pickedKey: null, records: [] });
    expect(isFinished(state)).toBe(false);
    expect(currentScenario(state)?.id).toBe('mock-0');
  });

  it('records the score when a pick is made', () => {
    const state = roundReducer(startRound(five()), { type: 'pick', key: 'b' });
    expect(state.pickedKey).toBe('b');
    expect(state.records).toHaveLength(1);
    expect(state.records[0]).toMatchObject({ scenarioId: 'mock-0', result: 'double_bogey', strokes: 2 });
  });

  it('ignores a second pick on the same hole', () => {
    const once = roundReducer(startRound(five()), { type: 'pick', key: 'a' });
    const twice = roundReducer(once, { type: 'pick', key: 'b' });
    expect(twice).toBe(once);
  });

  it('only moves on after a pick', () => {
    const start = startRound(five());
    expect(roundReducer(start, { type: 'next' })).toBe(start);
  });

  it('plays five holes and finishes', () => {
    let state = startRound(five());
    for (let hole = 0; hole < 5; hole++) {
      expect(isFinished(state)).toBe(false);
      state = roundReducer(state, { type: 'pick', key: 'a' });
      state = roundReducer(state, { type: 'next' });
    }
    expect(isFinished(state)).toBe(true);
    expect(state.records).toHaveLength(5);
    expect(totalStrokes(state.records)).toBe(-5); // five birdies
    expect(currentScenario(state)).toBeUndefined();
    expect(roundReducer(state, { type: 'pick', key: 'a' })).toBe(state); // nothing left to pick
  });

  it('restarts with a fresh round', () => {
    const played = roundReducer(startRound(five()), { type: 'pick', key: 'a' });
    const fresh = roundReducer(played, { type: 'restart', scenarios: five() });
    expect(fresh).toMatchObject({ index: 0, pickedKey: null, records: [] });
  });
});

describe('pickRound', () => {
  const all = readMockScenarios();

  it('picks five different scenarios', () => {
    const round = pickRound(all);
    expect(round).toHaveLength(HOLES_PER_ROUND);
    expect(new Set(round.map((s) => s.id)).size).toBe(HOLES_PER_ROUND);
  });

  it('is repeatable for the same random source and varies with it', () => {
    const seq = (values: number[]) => {
      let i = 0;
      return () => values[i++ % values.length] ?? 0;
    };
    const a = pickRound(all, 5, seq([0.1, 0.9, 0.5, 0.3, 0.7]));
    const b = pickRound(all, 5, seq([0.1, 0.9, 0.5, 0.3, 0.7]));
    const c = pickRound(all, 5, seq([0.95, 0.2, 0.6, 0.0, 0.4]));
    expect(a.map((s) => s.id)).toEqual(b.map((s) => s.id));
    expect(a.map((s) => s.id)).not.toEqual(c.map((s) => s.id));
  });

  it('returns what it has when there are fewer scenarios than holes', () => {
    expect(pickRound(all.slice(0, 3))).toHaveLength(3);
  });

  it('does not change the list it was given', () => {
    const ids = all.map((s) => s.id);
    pickRound(all);
    expect(all.map((s) => s.id)).toEqual(ids);
  });
});
