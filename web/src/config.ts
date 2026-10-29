/** Settings that change when the game launches or moves. Everything else reads them from here. */

/** The first day of the game: dive #1 is played on this calendar date in TIME_ZONE (YYYY-MM-DD). */
export const LAUNCH_DATE = '2026-11-03';

/** Everyone in this time zone gets the same dive on the same calendar day. */
export const TIME_ZONE = 'America/New_York';

/** localStorage key for finished dives. The preview mode (?preview=1) uses its own, so test plays never touch real progress. */
export const STORAGE_KEY = 'deepcut.v1';
export const PREVIEW_STORAGE_KEY = 'deepcut.preview.v1';
