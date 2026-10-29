import { useState, type Ref } from 'react';
import { useAnnounce } from '../announcer';
import { totalPoints } from '../dive';
import { copyText, shareLine } from '../share';
import { MAX_DIVE_POINTS, TIERS, TIER_POINTS, TIER_RANGES } from '../tiers';
import type { Prompt, PromptResult } from '../types';

interface Props {
  prompts: readonly Prompt[];
  results: readonly PromptResult[];
  diveNumber: number;
  headingRef: Ref<HTMLHeadingElement>;
  onHome: () => void;
  onArchive: () => void;
  onHowTo: () => void;
}

function describe(r: PromptResult): string {
  if (r.status === 'valid') return `tier ${r.tier}, ${r.points} points`;
  if (r.status === 'timeout') return 'time ran out, 0 points';
  if (r.status === 'outside_range') return 'outside the data range, 0 points';
  return 'not a valid answer, 0 points';
}

export function Final({ prompts, results, diveNumber, headingRef, onHome, onArchive, onHowTo }: Props) {
  const announce = useAnnounce();
  const [copyFailed, setCopyFailed] = useState(false);
  const total = totalPoints(results);
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
      <p className="final__score" aria-label={`Total ${total} out of ${MAX_DIVE_POINTS}`}>
        {total}
        <span className="final__max"> / {MAX_DIVE_POINTS}</span>
      </p>
      <ol className="squares" aria-label="Your seven answers">
        {results.map((r, i) => (
          <li key={r.promptId} className={`square square--${r.tier === null ? 'miss' : `t${r.tier}`}`} aria-label={`Prompt ${i + 1}: ${describe(r)}`}>
            <span aria-hidden="true">{r.tier ?? '×'}</span>
          </li>
        ))}
      </ol>

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
