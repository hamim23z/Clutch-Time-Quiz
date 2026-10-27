import type { Ref } from 'react';
import { describeState } from '../format';
import { formatStrokes, formatToPar, RESULT_LABELS, totalStrokes } from '../scoring';
import type { HoleRecord, Scenario } from '../types';

interface Props {
  scenarios: readonly Scenario[];
  records: readonly HoleRecord[];
  headingRef: Ref<HTMLHeadingElement>;
  onRestart: () => void;
}

export function FinalScreen({ scenarios, records, headingRef, onRestart }: Props) {
  const total = totalStrokes(records);
  return (
    <section className="card final" aria-labelledby="final-heading">
      <h2 id="final-heading" tabIndex={-1} ref={headingRef}>
        Round complete
      </h2>
      <p className="final__score" aria-label={`Final score ${formatToPar(total)}`}>
        {formatToPar(total)}
      </p>
      <p className="final__note">E is even with par. Birdie −1, par 0, bogey +1, double bogey +2.</p>
      <ol className="holes">
        {records.map((record, i) => {
          const scenario = scenarios[i];
          return (
            <li key={record.scenarioId} className="hole">
              <span className={`square square--${record.result}`} aria-hidden="true" />
              <span className="hole__text">
                <strong>
                  Hole {i + 1}: {RESULT_LABELS[record.result]} ({formatStrokes(record.strokes)})
                </strong>
                {scenario && <span className="hole__state">{describeState(scenario.state)}</span>}
              </span>
            </li>
          );
        })}
      </ol>
      <button type="button" className="primary" onClick={onRestart}>
        Play another round
      </button>
    </section>
  );
}
