import { LAUNCH_DATE, TIME_ZONE } from './config';
import { PROMPTS_PER_DIVE } from './tiers';
import type { Prompt } from './types';

const DAY_MS = 86_400_000;
const DATE = /^(\d{4})-(\d{2})-(\d{2})$/;

/** The calendar date (YYYY-MM-DD) of an instant in a time zone. */
export function dateInZone(now: Date, timeZone: string = TIME_ZONE): string {
  const parts = new Intl.DateTimeFormat('en-US', { timeZone, year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(now);
  const get = (type: string): string => parts.find((p) => p.type === type)?.value ?? '';
  return `${get('year')}-${get('month')}-${get('day')}`;
}

export function isDateString(text: string): boolean {
  const m = DATE.exec(text);
  if (!m) return false;
  const [y, mo, d] = [Number(m[1]), Number(m[2]), Number(m[3])];
  const t = new Date(Date.UTC(y, mo - 1, d));
  return t.getUTCFullYear() === y && t.getUTCMonth() === mo - 1 && t.getUTCDate() === d;
}

/** Whole calendar days from one YYYY-MM-DD date to another (negative if the second is earlier). */
export function daysBetween(from: string, to: string): number {
  const parse = (s: string): number => {
    const m = DATE.exec(s);
    if (!m) throw new Error(`not a date: ${s}`);
    return Date.UTC(Number(m[1]), Number(m[2]) - 1, Number(m[3]));
  };
  return Math.round((parse(to) - parse(from)) / DAY_MS);
}

/** Dive number of a calendar date: the launch date is #1. Zero or less means the game has not launched yet. */
export function diveNumberOn(date: string, launch: string = LAUNCH_DATE): number {
  return daysBetween(launch, date) + 1;
}

/** How many complete dives (7 prompts) prompts.json holds. */
export const diveCount = (prompts: readonly unknown[]): number => Math.floor(prompts.length / PROMPTS_PER_DIVE);

/** 0-based position of a dive number in the file: dive #1 is dive 0, and the file repeats after its last dive. */
export function diveIndex(number: number, total: number): number {
  if (total < 1) throw new Error('there are no dives');
  return (((number - 1) % total) + total) % total;
}

/** The 7 prompts of a dive number: prompts 7N to 7N+6 of the file, N = (number - 1) modulo the number of dives. */
export function divePrompts(prompts: readonly Prompt[], number: number): Prompt[] {
  const n = diveIndex(number, diveCount(prompts));
  return prompts.slice(n * PROMPTS_PER_DIVE, (n + 1) * PROMPTS_PER_DIVE);
}

/** "3 November 2026" for a YYYY-MM-DD date, in English, whatever the browser's locale. */
export function longDate(date: string): string {
  const m = DATE.exec(date);
  if (!m) return date;
  return new Intl.DateTimeFormat('en-GB', { timeZone: 'UTC', day: 'numeric', month: 'long', year: 'numeric' }).format(new Date(Date.UTC(Number(m[1]), Number(m[2]) - 1, Number(m[3]))));
}
