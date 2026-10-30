import { MAX_DIVE_POINTS } from './tiers';

/** A label for a dive's total, by its share of the 700-point maximum. Plain basketball words, no league marks. */
export const RANKS: ReadonlyArray<{ from: number; label: string }> = [
  { from: 0, label: 'Benchwarmer' },
  { from: 0.1, label: 'Role player' },
  { from: 0.2, label: 'Sixth man' },
  { from: 0.3, label: 'Starter' },
  { from: 0.42, label: 'All-Star' },
  { from: 0.54, label: 'Franchise player' },
  { from: 0.66, label: 'MVP candidate' },
  { from: 0.8, label: 'Hall of Famer' },
  { from: 0.92, label: 'Greatest of all time' },
];

/** The rank of a total: the last band whose lower edge the total reaches. */
export function rankFor(total: number, max: number = MAX_DIVE_POINTS): string {
  const share = max > 0 ? total / max : 0;
  let label = RANKS[0]?.label ?? '';
  for (const band of RANKS) if (share >= band.from) label = band.label;
  return label;
}
