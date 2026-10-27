import { describe, expect, it } from 'vitest';
import { describeMargin, describePossession, describeQuarter, describeState, formatClock, formatPercent } from './format';

describe('format', () => {
  it('describes the margin from the coach’s side', () => {
    expect(describeMargin(3)).toBe('You lead by 3');
    expect(describeMargin(-3)).toBe('You trail by 3');
    expect(describeMargin(0)).toBe('Tied');
  });

  it('formats the clock as m:ss', () => {
    expect(formatClock(8)).toBe('0:08');
    expect(formatClock(22)).toBe('0:22');
    expect(formatClock(60)).toBe('1:00');
    expect(formatClock(0)).toBe('0:00');
  });

  it('names the quarter', () => {
    expect(describeQuarter(4)).toBe('4th quarter');
    expect(describeQuarter(5)).toBe('Overtime');
    expect(describeQuarter(6)).toBe('2OT');
  });

  it('says who has the ball', () => {
    expect(describePossession('team')).toBe('You have the ball');
    expect(describePossession('opponent')).toBe('They have the ball');
  });

  it('summarizes a state in one line', () => {
    expect(describeState({ quarter: 4, margin: 3, secondsLeft: 8, possession: 'opponent' })).toBe(
      '4th quarter, you lead by 3, 0:08 left, they have the ball',
    );
  });

  it('rounds win rates to whole percents', () => {
    expect(formatPercent(0.931)).toBe('93%');
    expect(formatPercent(0.5)).toBe('50%');
  });
});
