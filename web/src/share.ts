import type { PromptResult, Tier } from './types';
import { SITE_URL } from './config';
import { totalPoints } from './dive2';

/** One colored square per tier, from the common answers (white) to the deepest cuts (purple); a miss is black. */
export const TIER_SQUARES: Record<Tier, string> = { 1: '⬜', 2: '🟦', 3: '🟩', 4: '🟨', 5: '🟧', 6: '🟪' };
export const MISS_SQUARE = '⬛';

export function squareFor(result: PromptResult): string {
  return result.tier === null ? MISS_SQUARE : TIER_SQUARES[result.tier];
}

/** The text a player copies: "Deep Cut #12: 385", one square per prompt, and the address of the site. */
export function shareLine(diveNumber: number, results: readonly PromptResult[], url: string = SITE_URL): string {
  return `Deep Cut #${diveNumber}: ${totalPoints(results)}\n${results.map(squareFor).join('')}\n${url}`;
}

/** Copy text to the clipboard. Returns false when the browser does not allow it, so the page can show the text instead. */
export async function copyText(text: string): Promise<boolean> {
  try {
    if (typeof navigator !== 'undefined' && navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(text);
      return true;
    }
  } catch {
    // permission denied or not a secure context: fall through
  }
  return false;
}
