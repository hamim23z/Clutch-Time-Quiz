import { describe, expect, it } from 'vitest';
import type { Tier } from '../types';
import type { ChartMark } from './chartStore';
import { AIRBALL_ZONE, BALL_REST, BANDS, COURT, HOOP, MIN_GAP, RANGES, SLOT_COLUMNS, SLOT_ROWS, airballSlot, hash, layoutMarks } from './placement';

const TIERS: Tier[] = [1, 2, 3, 4, 5, 6];
const mark = (i: number, tier: Tier | null): ChartMark => ({ id: `p-${i}`, tier });
const seven = (tiers: Array<Tier | null>): ChartMark[] => tiers.map((t, i) => mark(i, t));

describe('the marker placement', () => {
  it('is the same for the same prompts and the same dive, every time', () => {
    const marks = seven([3, 6, null, 1, 4, 5, 2]);
    expect(layoutMarks(marks, 12)).toEqual(layoutMarks(marks, 12));
    expect(hash('p-1|12')).toBe(hash('p-1|12'));
  });

  it('differs between dives', () => {
    const marks = seven([3, 3, 3, 3, 3, 3, 3]);
    expect(layoutMarks(marks, 1)).not.toEqual(layoutMarks(marks, 2));
  });

  it('puts every marker inside its tier band, measured from the hoop', () => {
    for (let dive = 1; dive <= 60; dive++) {
      const placed = layoutMarks(seven([1, 2, 3, 4, 5, 6, 3]), dive);
      for (const p of placed) {
        const d = Math.hypot(p.x - HOOP.x, p.y - HOOP.y);
        const [lo, hi] = BANDS[p.tier as Tier];
        expect(d, `${p.id} tier ${p.tier}`).toBeGreaterThan(lo);
        expect(d).toBeLessThan(hi);
        expect(d).toBeGreaterThanOrEqual(RANGES[p.tier as Tier][0] - 0.01);
        expect(d).toBeLessThanOrEqual(RANGES[p.tier as Tier][1] + 0.01);
      }
    }
  });

  it('keeps every marker, square and all, inside the court and below the hoop, at 20 to 160 degrees', () => {
    for (let dive = 1; dive <= 80; dive++) {
      for (const tiers of [[6, 6, 6, 6, 6, 6, 6], [1, 1, 1, 1, 1, 1, 1], [5, 5, 4, 4, 3, 2, 6]] as Tier[][]) {
        for (const p of layoutMarks(seven(tiers), dive)) {
          expect(p.x - 26).toBeGreaterThanOrEqual(COURT.x); // the dashed ring round the latest marker stays on the court too
          expect(p.x + 26).toBeLessThanOrEqual(COURT.x + COURT.w);
          expect(p.y - 11).toBeGreaterThanOrEqual(COURT.y);
          expect(p.y + 11).toBeLessThanOrEqual(COURT.y + COURT.h);
          expect(p.angle).toBeGreaterThanOrEqual(20);
          expect(p.angle).toBeLessThanOrEqual(160);
        }
      }
    }
  });

  it('never puts two of seven markers (or one and the waiting ball) closer than the gap, even when all seven are the same tier', () => {
    for (let dive = 1; dive <= 200; dive++) {
      for (const tier of TIERS) {
        const placed = layoutMarks(seven(Array(7).fill(tier) as Tier[]), dive);
        const points = [BALL_REST, ...placed];
        for (let i = 0; i < points.length; i++) {
          for (let j = i + 1; j < points.length; j++) {
            expect(Math.hypot(points[i]!.x - points[j]!.x, points[i]!.y - points[j]!.y), `dive ${dive} tier ${tier}: ${i} and ${j}`).toBeGreaterThanOrEqual(MIN_GAP);
          }
        }
      }
    }
  });

  it('never moves an earlier marker when a later answer is added', () => {
    const marks = seven([2, 5, 1, 6, 3, 4, 2]);
    const full = layoutMarks(marks, 9);
    for (let n = 1; n < 7; n++) expect(layoutMarks(marks.slice(0, n), 9)).toEqual(full.slice(0, n));
  });
});

describe('the airball zone', () => {
  it('has three slots across and two deep, all inside the dashed rectangle', () => {
    for (let i = 0; i < SLOT_COLUMNS * SLOT_ROWS; i++) {
      const s = airballSlot(i);
      expect(s.x - 11).toBeGreaterThanOrEqual(AIRBALL_ZONE.x);
      expect(s.x + 11).toBeLessThanOrEqual(AIRBALL_ZONE.x + AIRBALL_ZONE.w);
      expect(s.y - 11).toBeGreaterThanOrEqual(AIRBALL_ZONE.y);
      expect(s.y + 11).toBeLessThanOrEqual(AIRBALL_ZONE.y + AIRBALL_ZONE.h);
    }
    expect(new Set(Array.from({ length: 6 }, (_, i) => `${airballSlot(i).x},${airballSlot(i).y}`)).size).toBe(6);
  });

  it('wraps round when there are more misses than slots, a little to the right so they do not hide each other', () => {
    expect(airballSlot(6).y).toBe(airballSlot(0).y);
    expect(airballSlot(6).x).toBeGreaterThan(airballSlot(0).x);
    expect(airballSlot(6).x - 11).toBeGreaterThanOrEqual(AIRBALL_ZONE.x);
    expect(airballSlot(7)).toEqual({ x: airballSlot(1).x + 16, y: airballSlot(1).y });
  });

  it('puts misses in slots in the order they happen and leaves made shots on the court', () => {
    const placed = layoutMarks(seven([null, 4, null, 2, null, 1, 6]), 5);
    expect(placed.filter((p) => p.tier === null).map((p) => p.slot)).toEqual([0, 1, 2]);
    for (const p of placed.filter((q) => q.tier === null)) expect(p.y).toBeGreaterThan(AIRBALL_ZONE.y);
    for (const p of placed.filter((q) => q.tier !== null)) expect(p.y).toBeLessThan(COURT.y + COURT.h);
  });
});
