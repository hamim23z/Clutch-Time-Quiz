import { describe, expect, it } from 'vitest';
import { RANKS, rankFor } from './ranks';

describe('the rank label of a total', () => {
  it('has nine plain basketball ranks in order of the share of 700', () => {
    expect(RANKS).toHaveLength(9);
    expect(RANKS.map((r) => r.from)).toEqual([...RANKS.map((r) => r.from)].sort((a, b) => a - b));
    expect(new Set(RANKS.map((r) => r.label)).size).toBe(9);
  });

  it.each([
    [0, 'Benchwarmer'],
    [69, 'Benchwarmer'],
    [70, 'Role player'],
    [139, 'Role player'],
    [140, 'Sixth man'],
    [210, 'Starter'],
    [294, 'All-Star'],
    [378, 'Franchise player'],
    [462, 'MVP candidate'],
    [560, 'Hall of Famer'],
    [644, 'Greatest of all time'],
    [700, 'Greatest of all time'],
  ])('%i points is %s', (total, label) => {
    expect(rankFor(total)).toBe(label);
  });

  it('reaches the top rank only with nearly all the points', () => {
    expect(rankFor(640)).toBe('Hall of Famer');
    expect(rankFor(645)).toBe('Greatest of all time');
  });
});
