import { useEffect, type Ref } from 'react';
import { useAnnounce } from '../announcer';
import { useReducedMotion } from '../motion';
import { shotForResult } from '../shots';
import { useSound } from '../sound';
import { TIER_RANGES } from '../tiers';
import type { Answer, Prompt, PromptResult } from '../types';
import { ShotAnimation } from './ShotAnimation';
import { ShotLabel } from './ShotLabel';

interface Props {
  prompt: Prompt;
  result: PromptResult;
  isLast: boolean;
  headingRef: Ref<HTMLHeadingElement>;
  onNext: () => void;
  /** The player tapped or pressed Enter to skip the shot. */
  skipped: boolean;
  onSkip: () => void;
}

/** The three most famous valid answers: lowest tier first, then the order of the file. */
export const mostFamous = (answers: readonly Answer[], n = 3): Answer[] =>
  answers.map((a, i) => ({ a, i })).sort((x, y) => x.a.tier - y.a.tier || x.i - y.i).slice(0, n).map((x) => x.a);

/** The rarest valid answers: highest tier first, and the later ones in the file first within a tier. */
export const rarest = (answers: readonly Answer[], n = 3): Answer[] =>
  answers.map((a, i) => ({ a, i })).sort((x, y) => y.a.tier - x.a.tier || y.i - x.i).slice(0, n).map((x) => x.a);

function headline(result: PromptResult): string {
  switch (result.status) {
    case 'valid':
      return `Tier ${result.tier}: ${result.points} points`;
    case 'timeout':
      return "Time's up: 0 points";
    case 'outside_range':
      return 'Outside the data range';
    case 'invalid':
      return 'Not a valid answer: 0 points';
  }
}

function explanation(prompt: Prompt, result: PromptResult): string {
  const n = prompt.answers.length;
  switch (result.status) {
    case 'valid':
      return `${result.matched?.name ?? result.input} is one of ${n} valid answers. ${result.tier ? TIER_RANGES[result.tier] : ''}: the more obscure the answer, the more it scores.`;
    case 'timeout':
      return result.input.trim() === '' ? 'You ran out of time before answering.' : `You ran out of time before answering. "${result.input}" was not submitted.`;
    case 'outside_range':
      return `"${result.input}" looks like a real player from before the data starts (2002), so it is outside the data range. It does not count against you.`;
    case 'invalid':
      return result.matched ? `${result.matched.name} is not a valid answer for this prompt.` : `We did not recognize "${result.input}".`;
  }
}

function AnswerList({ title, answers }: { title: string; answers: readonly Answer[] }) {
  return (
    <>
      <h4>{title}</h4>
      <ul className="answers">
        {answers.map((a) => (
          <li key={a.id} className="answers__item">
            <span className={`chip chip--t${a.tier}`} aria-hidden="true">{a.tier}</span>
            <span className="answers__name">{a.name}</span>
            <span className="answers__points">
              <span className="visually-hidden">tier {a.tier}, </span>
              {a.points}
            </span>
          </li>
        ))}
      </ul>
    </>
  );
}

export function Reveal({ prompt, result, isLast, headingRef, onNext, skipped, onSkip }: Props) {
  const byTier = [...prompt.answers].sort((a, b) => a.tier - b.tier);
  const shot = shotForResult(result);
  const reduced = useReducedMotion();
  const announce = useAnnounce();
  const { play } = useSound();

  // Say the result once, and play its sound. The page text below carries the same words for everyone else.
  useEffect(() => {
    announce(`${headline(result)}. ${shot.label}.`);
    if (!reduced) play(shot.name);
    // eslint-disable-next-line react-hooks/exhaustive-deps -- once per result
  }, [result.promptId]);

  // A tap anywhere, or Enter, skips to the end of the shot. Neither blocks anything: buttons and typing work as before.
  useEffect(() => {
    if (skipped) return;
    const onKey = (e: KeyboardEvent): void => {
      if (e.key === 'Enter') onSkip();
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [skipped, onSkip]);

  const classes = ['card', 'reveal', `reveal--${shot.name}`, skipped ? 'is-skipped' : '', reduced ? 'is-reduced' : ''].filter(Boolean).join(' ');
  return (
    <section className={classes} aria-labelledby="result-heading" onPointerDown={skipped ? undefined : onSkip}>
      <div className="reveal__stage">
        <ShotAnimation shot={shot} reduced={reduced} skipped={skipped} />
        <ShotLabel shot={shot} skipped={skipped} />
      </div>
      <p className="eyebrow">{prompt.text}</p>
      <h3
        id="result-heading"
        className={`result result--${result.status === 'valid' && result.tier ? `t${result.tier}` : result.status}${result.status === 'outside_range' ? ' shake shake--0' : ''}`}
        tabIndex={-1}
        ref={headingRef}
      >
        {headline(result)}
      </h3>
      <div className="reveal__rest">
        <p>{explanation(prompt, result)}</p>

        <AnswerList title="The most famous valid answers" answers={mostFamous(prompt.answers)} />
        <AnswerList title="The rarest valid answers" answers={rarest(prompt.answers)} />

        <details className="all-answers">
          <summary>All {prompt.answers.length} valid answers</summary>
          <ol className="answers answers--all">
            {byTier.map((a) => (
              <li key={a.id} className="answers__item">
                <span className={`chip chip--t${a.tier}`} aria-hidden="true">{a.tier}</span>
                <span className="answers__name">{a.name}</span>
                <span className="answers__points">
                  <span className="visually-hidden">tier {a.tier}, </span>
                  {a.points}
                </span>
              </li>
            ))}
          </ol>
        </details>
        <p className="caveat">
          Obscurity is estimated from how famous an answer is across the whole data set, not from what other players typed.
        </p>
        <button type="button" className="primary" onClick={onNext}>
          {isLast ? 'See results' : 'Next prompt'}
        </button>
      </div>
    </section>
  );
}
