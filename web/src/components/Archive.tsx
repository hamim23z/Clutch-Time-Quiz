import { totalPoints } from '../dive2';
import { squareFor } from '../share';
import type { History } from '../storage';
import { MAX_DIVE_POINTS } from '../tiers';
import type { PromptResult } from '../types';

interface Props {
  /** The dive number of today: the archive lists #1 up to this one. */
  today: number;
  history: History;
  saving: boolean;
  onPlay: (number: number) => void;
  onResults: (number: number) => void;
  onBack: () => void;
}

const label = (r: PromptResult, i: number): string => (r.tier === null ? `prompt ${i + 1}: no points` : `prompt ${i + 1}: tier ${r.tier}`);

export function Archive({ today, history, saving, onPlay, onResults, onBack }: Props) {
  const numbers = Array.from({ length: today }, (_, i) => today - i); // newest first
  return (
    <section className="card archive" aria-labelledby="archive-heading">
      <h2 id="archive-heading">Archive</h2>
      <p>Every past dive. Playing one here counts for the archive only, not for your streak.</p>
      {!saving && <p className="caveat">This browser is not saving anything, so the archive will only remember this visit.</p>}
      <ol className="archive__list">
        {numbers.map((n) => {
          const played = history[n];
          return (
            <li key={n} className="archive__item">
              <span className="archive__name">Dive #{n}</span>
              {played ? (
                <>
                  <span className="archive__score" role="group" aria-label={`${totalPoints(played.results)} out of ${MAX_DIVE_POINTS}`}>
                    {totalPoints(played.results)}
                  </span>
                  <ol className="mini" aria-label={`Dive ${n} answers`}>
                    {played.results.map((r, i) => (
                      <li key={r.promptId} className={`mini__square square--${r.tier === null ? 'miss' : `t${r.tier}`}`} aria-label={label(r, i)} title={squareFor(r)}>
                        <span aria-hidden="true">{r.tier ?? '×'}</span>
                      </li>
                    ))}
                  </ol>
                  <button type="button" className="secondary" onClick={() => onResults(n)} aria-label={`Results of dive ${n}`}>
                    Results
                  </button>
                </>
              ) : (
                <button type="button" className="primary" onClick={() => onPlay(n)} aria-label={`Play dive ${n}`}>
                  Play
                </button>
              )}
            </li>
          );
        })}
      </ol>
      <div className="actions">
        <button type="button" className="secondary" onClick={onBack}>
          Back
        </button>
      </div>
    </section>
  );
}
