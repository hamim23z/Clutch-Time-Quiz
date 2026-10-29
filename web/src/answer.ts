/** Turn a submission into a result: valid, invalid, outside the data range, or ambiguous (ask again). */
import { matchAnswer, type Index } from './matching';
import { isOutsideRange } from './outsideRange';
import type { Entry, Prompt, PromptResult, Tier } from './types';

export type Resolution = { kind: 'result'; result: PromptResult } | { kind: 'ambiguous'; entries: Entry[] };

function result(prompt: Prompt, status: PromptResult['status'], input: string, matched: Entry | null, tier: Tier | null, points: number): PromptResult {
  return {
    promptId: prompt.id,
    status,
    input,
    matched: matched ? { id: matched.id, name: matched.name } : null,
    tier,
    points,
    countsAsWrong: status !== 'outside_range',
  };
}

/** The result of running out of time: nothing scores, whatever was typed. */
export function timeoutResult(prompt: Prompt, input: string): PromptResult {
  return result(prompt, 'timeout', input, null, null, 0);
}

/** Score one entry that is already known (picked from the suggestions). */
export function resolveEntry(prompt: Prompt, entry: Entry, input: string): PromptResult {
  const answer = prompt.answers.find((a) => a.id === entry.id);
  return answer ? result(prompt, 'valid', input, entry, answer.tier, answer.points) : result(prompt, 'invalid', input, entry, null, 0);
}

/** Resolve typed text. `outsideNames` are real people outside the data range. */
export function resolveText(prompt: Prompt, index: Index, text: string, outsideNames?: readonly string[]): Resolution {
  const match = matchAnswer(index, text);
  if (match.kind === 'ambiguous') return { kind: 'ambiguous', entries: match.entries };
  if (match.kind === 'match') return { kind: 'result', result: resolveEntry(prompt, match.entry, text) };
  if (isOutsideRange(text, outsideNames)) return { kind: 'result', result: result(prompt, 'outside_range', text, null, null, 0) };
  return { kind: 'result', result: result(prompt, 'invalid', text, null, null, 0) };
}
