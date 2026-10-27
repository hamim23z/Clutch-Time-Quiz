import { describe, expect, it } from 'vitest';
import { formatStrokes, formatToPar, resultForGap, scoreHole, STROKES, totalStrokes } from './scoring';
import { scenarioWith } from './testUtils';

describe('resultForGap', () => {
  it.each([
    [0, 'birdie'],
    [0.0000000001, 'birdie'], // float noise is not a gap
    [0.1, 'par'],
    [2.9, 'par'],
    [3, 'par'], // "up to 3 points" is par
    [3.1, 'bogey'],
    [10, 'bogey'], // "3 to 10 points" is bogey
    [10.1, 'double_bogey'],
    [40, 'double_bogey'],
  ] as const)('a gap of %s points is a %s', (gap, expected) => {
    expect(resultForGap(gap)).toBe(expected);
  });
});

describe('strokes', () => {
  it('follows SPEC.md: birdie -1, par 0, bogey +1, double bogey +2', () => {
    expect(STROKES).toEqual({ birdie: -1, par: 0, bogey: 1, double_bogey: 2 });
  });
});

describe('scoreHole', () => {
  it('scores the best option as a birdie', () => {
    const record = scoreHole(scenarioWith(0.93, 0.81), 'a');
    expect(record).toMatchObject({ result: 'birdie', strokes: -1, bestKey: 'a', pickedKey: 'a', gap: 0 });
  });

  it('measures the gap in percentage points against the best option', () => {
    const record = scoreHole(scenarioWith(0.93, 0.81), 'b');
    expect(record.gap).toBeCloseTo(12, 6);
    expect(record).toMatchObject({ result: 'double_bogey', strokes: 2, bestKey: 'a' });
  });

  it('treats exactly 3 points as par even though 0.91 - 0.88 is 0.03000000000000003', () => {
    expect(scoreHole(scenarioWith(0.91, 0.88), 'b').result).toBe('par');
  });

  it('treats exactly 10 points as bogey', () => {
    expect(scoreHole(scenarioWith(0.6, 0.5), 'b').result).toBe('bogey');
  });

  it('scores every option tied for best as a birdie', () => {
    expect(scoreHole(scenarioWith(0.5, 0.5), 'a').result).toBe('birdie');
    expect(scoreHole(scenarioWith(0.5, 0.5), 'b').result).toBe('birdie');
  });

  it('works with three options', () => {
    const s = scenarioWith(0.4, 0.5);
    s.options.push({ key: 'c', label: 'Option C', winRate: 0.45, n: 50 });
    expect(scoreHole(s, 'c').result).toBe('bogey'); // 5 points behind the best (0.50 vs 0.45)
    expect(scoreHole(s, 'a').result).toBe('bogey'); // 10 points behind
  });

  it('rejects a key that is not an option', () => {
    expect(() => scoreHole(scenarioWith(0.5, 0.4), 'zzz')).toThrow(/no option "zzz"/);
  });
});

describe('totals', () => {
  it('adds strokes across holes', () => {
    const records = [
      scoreHole(scenarioWith(0.9, 0.5, 'mock-1'), 'a'), // -1
      scoreHole(scenarioWith(0.9, 0.5, 'mock-2'), 'b'), // +2
      scoreHole(scenarioWith(0.9, 0.88, 'mock-3'), 'b'), // 0
    ];
    expect(totalStrokes(records)).toBe(1);
    expect(totalStrokes([])).toBe(0);
  });

  it('formats golf style', () => {
    expect(formatToPar(0)).toBe('E');
    expect(formatToPar(-2)).toBe('−2');
    expect(formatToPar(3)).toBe('+3');
    expect(formatStrokes(0)).toBe('0');
    expect(formatStrokes(-1)).toBe('−1');
    expect(formatStrokes(2)).toBe('+2');
  });
});
