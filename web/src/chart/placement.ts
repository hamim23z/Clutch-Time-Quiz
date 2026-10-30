import type { Tier } from '../types';
import type { ChartMark } from './chartStore';

/** The chart is drawn in a 688 x 860 picture: a half court seen from above, the basket at the top, 11.2 units per foot. */
export const VIEW = { width: 688, height: 860 };
export const COURT = { x: 96, y: 104, w: 560, h: 526.4 };
export const HOOP = { x: 376, y: 162.8 };

/** Distance from the hoop, in units, where each tier's zone starts and ends. Tier 6 stops just inside the half-court line. */
export const BANDS: Record<Tier, readonly [number, number]> = {
  1: [0, 112],
  2: [112, 190.4],
  3: [190.4, 266],
  4: [266, 358.4],
  5: [358.4, 440],
  6: [440, 467],
};

export const TIER_COLORS: Record<Tier, string> = { 1: '#6E6E6E', 2: '#A8A8A8', 3: '#EDEDED', 4: '#FFB020', 5: '#FF6A13', 6: '#FF3B1F' };
/** The number on a tier's square: white on the dark grey, ink on the rest, so it reads at 4.5 to 1 or better. */
export const TIER_INK: Record<Tier, string> = { 1: '#FFFFFF', 2: '#0A0A0A', 3: '#0A0A0A', 4: '#0A0A0A', 5: '#0A0A0A', 6: '#0A0A0A' };

export const MARKER = 22; // a square, in units
/** Markers are never closer than this (centre to centre). */
export const MIN_GAP = 34;
/** Where the ball waits, at the bottom centre of the court. */
export const BALL_REST = { x: 376, y: 596 };

/** The marker's centre stays this far inside the court lines: sideways far enough for the dashed ring (radius 26) to stay on the court. */
const INSET_X = 28;
const INSET_Y = 14;
const BOUNDS = { minX: COURT.x + INSET_X, maxX: COURT.x + COURT.w - INSET_X, minY: COURT.y + INSET_Y, maxY: COURT.y + COURT.h - INSET_Y };
/** Angles are measured from the hoop, 20 to 160 degrees (0 is straight right, 90 straight down the court). */
const ANGLES = { min: 20, max: 160 };

/** The distances a marker of each tier may take: inside the band, off its edges, off the hoop and inside the court. */
export const RANGES: Record<Tier, readonly [number, number]> = {
  1: [50, 106],
  2: [118, 184],
  3: [197, 259],
  4: [273, 352],
  5: [365, 434],
  6: [444, 452],
};

export interface Placed {
  id: string;
  /** null: an airball. */
  tier: Tier | null;
  x: number;
  y: number;
  /** Degrees and distance from the hoop (made shots only). */
  angle: number;
  distance: number;
  /** The slot in the airball zone (misses only), counted from 0. */
  slot: number;
}

/** A 32-bit FNV-1a hash: the same text always gives the same number, in every browser. */
export function hash(text: string): number {
  let h = 0x811c9dc5;
  for (let i = 0; i < text.length; i++) {
    h ^= text.charCodeAt(i);
    h = Math.imul(h, 0x01000193) >>> 0;
  }
  return h >>> 0;
}

const at = (distance: number, angle: number): { x: number; y: number } => {
  const r = (angle * Math.PI) / 180;
  return { x: HOOP.x + distance * Math.cos(r), y: HOOP.y + distance * Math.sin(r) };
};
const inside = (p: { x: number; y: number }): boolean => p.x >= BOUNDS.minX && p.x <= BOUNDS.maxX && p.y >= BOUNDS.minY && p.y <= BOUNDS.maxY;
const apart = (p: { x: number; y: number }, others: ReadonlyArray<{ x: number; y: number }>): number => others.reduce((m, o) => Math.min(m, Math.hypot(p.x - o.x, p.y - o.y)), Infinity);

/**
 * Where a made shot's marker goes. The angle and the distance come from a hash of the prompt id and the dive, so the same dive always
 * looks the same; the distance is inside the tier's band, the marker is inside the court, and it is at least MIN_GAP from the others
 * (and from the ball at rest). When the first choice is taken, the angle is walked on in fixed steps.
 */
export function place(id: string, tier: Tier, diveKey: string | number, taken: ReadonlyArray<{ x: number; y: number }>): { x: number; y: number; angle: number; distance: number } {
  const seed = hash(`${id}|${diveKey}`);
  const [lo, hi] = RANGES[tier];
  const span = ANGLES.max - ANGLES.min + 1;
  const start = seed % span;
  const step = 53; // coprime with 141, so the walk visits every angle once
  let best: { x: number; y: number; angle: number; distance: number; gap: number } | null = null;
  for (let pass = 0; pass < 14; pass++) {
    const u = ((hash(`${id}|${diveKey}|d`) % 1000) / 1000 + pass * 0.382) % 1;
    const distance = lo + (hi - lo) * u;
    for (let i = 0; i < span; i++) {
      const angle = ANGLES.min + ((start + i * step) % span);
      const p = at(distance, angle);
      if (!inside(p)) continue;
      const gap = apart(p, taken);
      if (gap >= MIN_GAP) return { x: p.x, y: p.y, angle, distance };
      if (!best || gap > best.gap) best = { ...p, angle, distance, gap };
    }
  }
  // crowded beyond hope (it cannot happen with seven markers): take the roomiest spot found
  const fallback = best ?? { ...at((lo + hi) / 2, 90), angle: 90, distance: (lo + hi) / 2, gap: 0 };
  return { x: fallback.x, y: fallback.y, angle: fallback.angle, distance: fallback.distance };
}

/** The slots in the airball zone: three across and two deep; more misses than that wrap round and sit a little to the right. */
export const SLOT_COLUMNS = 3;
export const SLOT_ROWS = 2;
export const AIRBALL_ZONE = { x: 96, y: 650, w: 560, h: 104 };
export function airballSlot(index: number): { x: number; y: number } {
  const n = SLOT_COLUMNS * SLOT_ROWS;
  const lap = Math.floor(index / n);
  const i = index % n;
  const column = i % SLOT_COLUMNS;
  const row = Math.floor(i / SLOT_COLUMNS);
  return {
    x: AIRBALL_ZONE.x + (AIRBALL_ZONE.w * (column + 0.5)) / SLOT_COLUMNS + lap * 16,
    y: AIRBALL_ZONE.y + 54 + row * 34,
  };
}

/** Every mark of a dive with its place on the chart, in prompt order: an earlier marker never moves when a later one is added. */
export function layoutMarks(marks: readonly ChartMark[], diveKey: string | number): Placed[] {
  const taken: Array<{ x: number; y: number }> = [BALL_REST];
  let misses = 0;
  return marks.map((m) => {
    if (m.tier === null) {
      const slot = airballSlot(misses);
      return { id: m.id, tier: null, x: slot.x, y: slot.y, angle: 0, distance: 0, slot: misses++ };
    }
    const p = place(m.id, m.tier, diveKey, taken);
    taken.push(p);
    return { id: m.id, tier: m.tier, x: p.x, y: p.y, angle: p.angle, distance: p.distance, slot: 0 };
  });
}
