import { useEffect, useState, type CSSProperties, type Ref } from 'react';
import { useAnnounce } from '../announcer';
import { totalPoints } from '../dive2';
import { marksFrom, useChartStore } from '../chart/chartStore';
import { useReducedMotion } from '../motion';
import { rankFor } from '../ranks';
import { ARM_MS } from './Reveal';
import { shotForResult } from '../shots';
import { copyText, shareLine } from '../share';
import { MAX_DIVE_POINTS, TIERS, TIER_POINTS, TIER_RANGES } from '../tiers';
import type { Prompt, PromptResult } from '../types';
import { Confetti } from './Confetti';
import { RollingNumber } from './RollingNumber';
import { StreakBadge } from './StreakBadge';

interface Props {
  prompts: readonly Prompt[];
  results: readonly PromptResult[];
  diveNumber: number;
  headingRef: Ref<HTMLHeadingElement>;
  onHome: () => void;
  onArchive: () => void;
  onHowTo: () => void;
  streak?: { value: number; increased: boolean };
}

function describe(r: PromptResult): string {
  if (r.status === 'valid') return `tier ${r.tier}, ${r.points} points`;
  if (r.status === 'timeout') return 'time ran out, 0 points';
  if (r.status === 'outside_range') return 'outside the data range, 0 points';
  return 'not a valid answer, 0 points';
}

/** A total of at least this share of the maximum earns confetti. */
export const STRONG_SHARE = 0.6;
export const STEP_MS = 480; // one shot every 480 ms, in step with the replay on the chart

export function Final({ prompts, results, diveNumber, headingRef, onHome, onArchive, onHowTo, streak }: Props) {
  const announce = useAnnounce();
  const [copyFailed, setCopyFailed] = useState(false);
  const reduced = useReducedMotion();
  const chart = useChartStore();
  const [skipped, setSkipped] = useState(false);
  const [replay, setReplay] = useState(0); // bumped by the replay button to play the seven shots again
  const total = totalPoints(results);
  const strong = total >= STRONG_SHARE * MAX_DIVE_POINTS;
  const sequenceMs = reduced || skipped ? 0 : results.length * STEP_MS + 150;
  const rank = rankFor(total);

  // The chart replays the seven shots in order while the squares appear one by one. A tap or Enter skips to the total.
  useEffect(() => {
    chart.set({ phase: 'results', marks: marksFrom(results), replayKey: chart.get().replayKey + 1, points: total, diveNumber, shot: null, clock: null, skipped: false });
    // eslint-disable-next-line react-hooks/exhaustive-deps -- once per results screen
  }, [diveNumber]);
  useEffect(() => {
    if (skipped || reduced) return;
    const onKey = (e: KeyboardEvent): void => {
      if (e.key === 'Enter' && !e.repeat) skip();
    };
    const arm = setTimeout(() => document.addEventListener('keydown', onKey), ARM_MS);
    return () => {
      clearTimeout(arm);
      document.removeEventListener('keydown', onKey);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [skipped, reduced]);
  const skip = (): void => {
    setSkipped(true);
    chart.set({ skipped: true });
  };
  const replayShots = (): void => {
    setReplay((n) => n + 1);
    setSkipped(false);
    chart.set({ phase: 'results', marks: marksFrom(results), replayKey: chart.get().replayKey + 1, skipped: false });
  };
  const line = shareLine(diveNumber, results);

  const share = async (): Promise<void> => {
    const ok = await copyText(line);
    setCopyFailed(!ok);
    announce(ok ? 'Copied to the clipboard.' : 'Could not copy. Select the text and copy it yourself.');
  };

  return (
    <section className="card final" aria-labelledby="final-heading">
      <h2 id="final-heading" tabIndex={-1} ref={headingRef}>
        Dive complete
      </h2>
      <p className="final__number">Dive #{diveNumber}</p>
      <div className={`final__show${reduced ? ' is-reduced' : ''}${skipped ? ' is-skipped' : ''}`} key={replay} onPointerDown={skipped ? undefined : skip} style={{ '--after': `${sequenceMs}ms` } as CSSProperties}>
        <ol className="squares" aria-label="Your seven answers">
          {results.map((r, i) => (
            <li
              key={r.promptId}
              className={`square square--${r.tier === null ? 'miss' : `t${r.tier}`}`}
              style={{ '--i': i, '--step': `${STEP_MS}ms` } as CSSProperties}
              aria-label={`Prompt ${i + 1}: ${describe(r)}`}
              title={shotForResult(r).label}
            >
              <span className="square__tier" aria-hidden="true">{r.tier ?? '×'}</span>
            </li>
          ))}
        </ol>
        <p className="final__score" role="group" aria-label={`Total ${total} out of ${MAX_DIVE_POINTS}`}  >
          <span aria-hidden="true">
            <RollingNumber value={total} from={0} delayMs={sequenceMs} durationMs={700} instant={reduced} />
          </span>
          <span className="final__max" aria-hidden="true"> / {MAX_DIVE_POINTS}</span>
        </p>
        {strong && !reduced && <Confetti />}
      </div>
      <p className="final__rank" style={{ '--after': `${sequenceMs}ms` } as CSSProperties}>
        {rank}
      </p>
      {strong && <p className="final__praise">Strong dive: {Math.round((100 * total) / MAX_DIVE_POINTS)}% of the maximum.</p>}
      <div className="final__streak">
        {streak && (
          <p>
            Streak: <StreakBadge value={streak.value} increased={streak.increased} testId="final-streak" />
          </p>
        )}
        <button type="button" className="secondary" onClick={replayShots}>
          Replay the shots
        </button>
      </div>

      <h3>Share</h3>
      {copyFailed ? (
        <textarea className="share-text" readOnly rows={3} value={line} aria-label="Your result, ready to copy" onFocus={(e) => e.currentTarget.select()} />
      ) : (
        <pre className="share-preview" aria-label="Your result">{line}</pre>
      )}
      <button type="button" className="primary" onClick={() => void share()}>
        Copy result
      </button>
      {copyFailed && <p className="caveat">Your browser did not allow copying. Select the text above and copy it.</p>}

      <h3>Your answers</h3>
      <ol className="recap">
        {results.map((r, i) => (
          <li key={r.promptId} className="recap__item">
            <span className={`chip chip--${r.tier === null ? 'miss' : `t${r.tier}`}`} aria-hidden="true">{r.tier ?? '×'}</span>
            <span className="recap__text">
              <strong>{r.matched?.name ?? (r.input.trim() === '' ? 'No answer' : r.input)}</strong>
              <span className="recap__prompt">{prompts[i]?.text}</span>
              <span className="recap__how">{describe(r)}</span>
            </span>
          </li>
        ))}
      </ol>

      <h3>Tiers</h3>
      <ul className="legend">
        {TIERS.map((t) => (
          <li key={t}>
            <span className={`chip chip--t${t}`} aria-hidden="true">{t}</span> {TIER_POINTS[t]} points · {TIER_RANGES[t]}
          </li>
        ))}
        <li>
          <span className="chip chip--miss" aria-hidden="true">×</span> 0 points · wrong, outside the data range or out of time
        </li>
      </ul>

      <div className="actions">
        <button type="button" className="primary" onClick={onHome}>
          Home
        </button>
        <button type="button" className="secondary" onClick={onArchive}>
          Archive
        </button>
        <button type="button" className="secondary" onClick={onHowTo}>
          How to play
        </button>
      </div>
    </section>
  );
}
