import type { HoleRecord, HoleResult, Scenario } from './types';

export const STROKES: Record<HoleResult, number> = {
  birdie: -1,
  par: 0,
  bogey: 1,
  double_bogey: 2,
};

export const RESULT_LABELS: Record<HoleResult, string> = {
  birdie: 'Birdie',
  par: 'Par',
  bogey: 'Bogey',
  double_bogey: 'Double bogey',
};

// Win rates are decimals, so differences like 0.91 - 0.88 come out as 0.03000000000000003.
const EPSILON = 1e-9;

/** Par up to and including 3 points off the best option, bogey up to and including 10. */
const PAR_MAX_GAP = 3;
const BOGEY_MAX_GAP = 10;

export function resultForGap(gapPoints: number): HoleResult {
  if (gapPoints < EPSILON) return 'birdie';
  if (gapPoints <= PAR_MAX_GAP + EPSILON) return 'par';
  if (gapPoints <= BOGEY_MAX_GAP + EPSILON) return 'bogey';
  return 'double_bogey';
}

export function bestOptionKey(scenario: Scenario): string {
  let best = scenario.options[0];
  if (!best) throw new Error(`Scenario ${scenario.id} has no options`);
  for (const option of scenario.options) {
    if (option.winRate > best.winRate) best = option;
  }
  return best.key;
}

export function scoreHole(scenario: Scenario, pickedKey: string): HoleRecord {
  const picked = scenario.options.find((o) => o.key === pickedKey);
  if (!picked) throw new Error(`Scenario ${scenario.id} has no option "${pickedKey}"`);
  const bestWinRate = Math.max(...scenario.options.map((o) => o.winRate));
  // Ties for best count as best, so every tied option is a birdie.
  const gap = Math.max(0, (bestWinRate - picked.winRate) * 100);
  const result = resultForGap(gap);
  return {
    scenarioId: scenario.id,
    pickedKey,
    bestKey: bestOptionKey(scenario),
    result,
    strokes: STROKES[result],
    gap,
  };
}

export function totalStrokes(records: readonly HoleRecord[]): number {
  return records.reduce((sum, r) => sum + r.strokes, 0);
}

/** Golf style: "E" for even, "-2" and "+3" otherwise (with a real minus sign for reading). */
export function formatToPar(total: number): string {
  if (total === 0) return 'E';
  return total < 0 ? `−${Math.abs(total)}` : `+${total}`;
}

/** Strokes for one hole: "−1", "0", "+1", "+2". */
export function formatStrokes(strokes: number): string {
  if (strokes === 0) return '0';
  return strokes < 0 ? `−${Math.abs(strokes)}` : `+${strokes}`;
}
