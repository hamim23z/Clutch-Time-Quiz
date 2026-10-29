import { describe, expect, it } from 'vitest';
import { LAUNCH_DATE, TIME_ZONE } from './config';
import { dateInZone, daysBetween, diveCount, diveIndex, diveNumberOn, divePrompts, isDateString, longDate } from './schedule';
import { mockPrompts } from './testUtils';
import type { Prompt } from './types';

const fake = (n: number): Prompt[] => Array.from({ length: n }, (_, i) => ({ id: `p-${i}`, answerType: 'player', text: 'Since 2001-02, x', answers: [], difficulty: 'easy' }));

describe('the launch date', () => {
  it('is 3 November 2026 in New York time', () => {
    expect(LAUNCH_DATE).toBe('2026-11-03');
    expect(TIME_ZONE).toBe('America/New_York');
  });
});

describe('dateInZone', () => {
  it('gives the calendar date in New York, not in UTC', () => {
    expect(dateInZone(new Date('2026-11-03T04:59:00Z'))).toBe('2026-11-02'); // 11:59 pm on the 2nd in New York (UTC-5)
    expect(dateInZone(new Date('2026-11-03T05:00:00Z'))).toBe('2026-11-03'); // midnight in New York
    expect(dateInZone(new Date('2026-11-04T04:59:00Z'))).toBe('2026-11-03');
  });

  it('follows daylight saving time', () => {
    expect(dateInZone(new Date('2026-07-01T03:59:00Z'))).toBe('2026-06-30'); // UTC-4 in summer
    expect(dateInZone(new Date('2026-07-01T04:00:00Z'))).toBe('2026-07-01');
    expect(dateInZone(new Date('2026-11-01T05:30:00Z'))).toBe('2026-11-01'); // the night clocks go back
  });

  it('gives everyone in the same zone the same day, whatever the browser time zone', () => {
    const instant = new Date('2026-12-25T02:00:00Z');
    expect(dateInZone(instant, 'America/New_York')).toBe('2026-12-24');
    expect(dateInZone(instant, 'Asia/Tokyo')).toBe('2026-12-25');
  });
});

describe('dive numbers', () => {
  it('counts days since launch: the launch day is #1', () => {
    expect(diveNumberOn('2026-11-03')).toBe(1);
    expect(diveNumberOn('2026-11-04')).toBe(2);
    expect(diveNumberOn('2026-11-14')).toBe(12);
    expect(diveNumberOn('2027-11-03')).toBe(366);
    expect(diveNumberOn('2026-11-03', '2026-11-03')).toBe(1);
  });

  it('is zero or less before the launch', () => {
    expect(diveNumberOn('2026-11-02')).toBe(0);
    expect(diveNumberOn('2026-10-29')).toBe(-4);
  });

  it('counts calendar days across month ends, leap days and the clock change', () => {
    expect(daysBetween('2028-02-28', '2028-03-01')).toBe(2);
    expect(daysBetween('2026-10-31', '2026-11-02')).toBe(2);
    expect(daysBetween('2026-11-03', '2026-11-03')).toBe(0);
    expect(daysBetween('2026-11-05', '2026-11-03')).toBe(-2);
  });

  it('accepts only real dates', () => {
    expect(isDateString('2026-11-03')).toBe(true);
    for (const bad of ['2026-13-01', '2026-02-30', '03/11/2026', '2026-1-3', '', 'tomorrow']) expect(isDateString(bad)).toBe(false);
  });

  it('writes a date in words', () => {
    expect(longDate('2026-11-03')).toBe('3 November 2026');
  });
});

describe('which prompts a dive number plays', () => {
  it('counts whole dives of 7', () => {
    expect(diveCount(fake(63))).toBe(9);
    expect(diveCount(fake(504))).toBe(72);
    expect(diveCount(fake(10))).toBe(1);
    expect(diveCount(fake(6))).toBe(0);
  });

  it('plays prompts 7N to 7N+6 with N = (number - 1) modulo the number of dives', () => {
    const prompts = fake(63);
    expect(divePrompts(prompts, 1).map((p) => p.id)).toEqual(['p-0', 'p-1', 'p-2', 'p-3', 'p-4', 'p-5', 'p-6']);
    expect(divePrompts(prompts, 2)[0]?.id).toBe('p-7');
    expect(divePrompts(prompts, 9)[6]?.id).toBe('p-62');
    expect(divePrompts(prompts, 10).map((p) => p.id)).toEqual(divePrompts(prompts, 1).map((p) => p.id)); // wraps after the last dive
    expect(divePrompts(prompts, 19).map((p) => p.id)).toEqual(divePrompts(prompts, 1).map((p) => p.id));
    expect(divePrompts(fake(504), 73).map((p) => p.id)).toEqual(divePrompts(fake(504), 1).map((p) => p.id));
  });

  it('ignores leftover prompts that do not make a full dive', () => {
    const all = mockPrompts(); // 10 mock prompts: one dive and 3 left over
    expect(divePrompts(all, 1)).toHaveLength(7);
    expect(divePrompts(all, 2).map((p) => p.id)).toEqual(divePrompts(all, 1).map((p) => p.id));
  });

  it('computes the index for numbers before the first dive too, without going negative', () => {
    expect(diveIndex(1, 9)).toBe(0);
    expect(diveIndex(9, 9)).toBe(8);
    expect(diveIndex(10, 9)).toBe(0);
    expect(diveIndex(0, 9)).toBe(8);
    expect(() => diveIndex(1, 0)).toThrow();
  });
});
