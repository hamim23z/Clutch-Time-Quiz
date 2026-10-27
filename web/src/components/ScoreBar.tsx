import { formatToPar, RESULT_LABELS, totalStrokes } from '../scoring';
import type { HoleRecord } from '../types';

interface Props {
  /** 1-based number of the hole being played. */
  hole: number;
  totalHoles: number;
  records: readonly HoleRecord[];
}

export function ScoreBar({ hole, totalHoles, records }: Props) {
  const shownHole = Math.min(hole, totalHoles);
  return (
    <header className="scorebar">
      <p className="scorebar__hole">
        Hole {shownHole} of {totalHoles}
      </p>
      <ol className="scorebar__squares" aria-label="Results so far">
        {Array.from({ length: totalHoles }, (_, i) => {
          const record = records[i];
          const label = record ? RESULT_LABELS[record.result] : 'Not played yet';
          return (
            <li
              key={i}
              className={`square square--${record ? record.result : 'pending'}`}
              aria-label={`Hole ${i + 1}: ${label}`}
            />
          );
        })}
      </ol>
      <p className="scorebar__total">
        Score <strong>{formatToPar(totalStrokes(records))}</strong>
      </p>
    </header>
  );
}
