import { useCallback, useEffect, useRef } from 'react';
import { useAnnounce } from '../announcer';
import { resolveEntry, resolveText, timeoutResult } from '../answer';
import type { Index } from '../matching';
import { SECONDS_PER_PROMPT } from '../tiers';
import type { Entry, Prompt, PromptResult } from '../types';
import { useCountdown } from '../useCountdown';
import { AnswerInput } from './AnswerInput';

interface Props {
  prompt: Prompt;
  index: Index;
  /** 1-based number of this prompt, and how many there are. */
  number: number;
  total: number;
  points: number;
  outsideNames?: readonly string[];
  onResult: (result: PromptResult) => void;
}

const WARNINGS = [10, 5];

export function PromptScreen({ prompt, index, number, total, points, outsideNames, onResult }: Props) {
  const announce = useAnnounce();
  const typed = useRef('');
  const done = useRef(false);

  const finish = useCallback(
    (result: PromptResult) => {
      if (done.current) return;
      done.current = true;
      onResult(result);
    },
    [onResult],
  );

  const remainingMs = useCountdown(SECONDS_PER_PROMPT, () => finish(timeoutResult(prompt, typed.current)));
  const seconds = Math.ceil(remainingMs / 1000);

  useEffect(() => {
    if (WARNINGS.includes(seconds) && seconds < SECONDS_PER_PROMPT) announce(`${seconds} seconds left`);
  }, [seconds, announce]);

  const submitText = (
    text: string,
    setHint: (hint: string) => void,
    showChoices: (entries: Entry[]) => void,
  ): void => {
    if (text.trim() === '') {
      setHint('Type a name, or pick one from the list.');
      return;
    }
    const resolution = resolveText(prompt, index, text, outsideNames);
    if (resolution.kind === 'ambiguous') {
      const names = resolution.entries.map((e) => e.name);
      setHint(`That could be ${names.slice(0, -1).join(', ')} or ${names[names.length - 1]}. Pick one from the list.`);
      showChoices(resolution.entries);
      return;
    }
    finish(resolution.result);
  };

  const urgency = seconds <= 5 ? 'danger' : seconds <= 10 ? 'warning' : 'calm';
  const promptId = `prompt-text-${prompt.id}`;
  return (
    <section className="card" aria-labelledby={promptId}>
      <div className="timer">
        <p className="timer__count" role="timer" aria-live="off">
          <span className={`timer__seconds timer__seconds--${urgency}`}>{seconds}</span>
          <span className="visually-hidden"> seconds left</span>
        </p>
        <div className="timer__track" aria-hidden="true">
          <div className={`timer__fill timer__fill--${urgency}`} style={{ width: `${(remainingMs / (SECONDS_PER_PROMPT * 1000)) * 100}%` }} />
        </div>
      </div>
      <p className="eyebrow">
        Prompt {number} of {total} · {points} points so far
      </p>
      <h2 id={promptId} className="prompt">
        {prompt.text}
      </h2>
      <AnswerInput
        index={index}
        labelledBy={promptId}
        onTextChange={(t) => {
          typed.current = t;
        }}
        onSubmitText={submitText}
        onPick={(entry, text) => finish(resolveEntry(prompt, entry, text))}
      />
    </section>
  );
}
