/**
 * Real people who are not in the data (the game only covers 2001-02 on). If a player types one of these names the
 * game says "outside the data range" instead of "wrong", and it does not count against a streak.
 *
 * MOCK: the names below are invented stand-ins. The real list (famous players from before 2002) is not part of
 * universe.json yet; it has to come from the pipeline or be written by hand in a later session.
 */
import { buildIndex, matchAnswer } from './matching';
import type { Universe } from './types';

export const MOCK_OUTSIDE_RANGE_NAMES = [
  'Orson Quillfeather',
  'Bram Hatchetfield',
  'Casimir Dunwoody',
  'Lysander Pike',
  'Ezekiel Marchbanks',
];

export function outsideRangeUniverse(names: readonly string[]): Universe {
  return { players: names.map((name, i) => ({ id: `outside-${i + 1}`, name, aliases: [] })), teams: [] };
}

/** True when the input is recognized as one of the out-of-range names. */
export function isOutsideRange(input: string, names: readonly string[] = MOCK_OUTSIDE_RANGE_NAMES): boolean {
  return matchAnswer(buildIndex(outsideRangeUniverse(names)), input).kind === 'match';
}
