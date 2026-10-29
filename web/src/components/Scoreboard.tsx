import { RollingNumber } from './RollingNumber';

interface Props {
  number: number;
  total: number;
  /** Points before and after the prompt on screen. They differ on the reveal, when the new points roll in. */
  pointsBefore: number;
  points: number;
  diveNumber: number;
  /** How long to wait before the points roll (the shot is playing). */
  rollDelayMs: number;
  instant: boolean;
}

/** The arena scoreboard: which prompt, the points so far and the dive number. */
export function Scoreboard({ number, total, pointsBefore, points, diveNumber, rollDelayMs, instant }: Props) {
  return (
    <div className="scoreboard" role="group" aria-label="Scoreboard">
      <div className="scoreboard__cell">
        <span className="scoreboard__label">Prompt</span>
        <span className="scoreboard__value">{number}<span className="scoreboard__of"> / {total}</span></span>
        <span className="visually-hidden">Prompt {number} of {total}</span>
      </div>
      <div className="scoreboard__cell scoreboard__cell--points">
        <span className="scoreboard__label">Points</span>
        <span className="scoreboard__value" data-testid="scoreboard-points"><RollingNumber value={points} from={pointsBefore} delayMs={rollDelayMs} instant={instant} /></span>
      </div>
      <div className="scoreboard__cell">
        <span className="scoreboard__label">Dive</span>
        <span className="scoreboard__value">#{diveNumber}</span>
      </div>
    </div>
  );
}
