import type { Ref } from 'react';
import { formatPercent } from '../format';
import { formatStrokes, RESULT_LABELS } from '../scoring';
import type { HoleRecord, Scenario } from '../types';

interface Props {
  scenario: Scenario;
  record: HoleRecord;
  isLastHole: boolean;
  headingRef: Ref<HTMLHeadingElement>;
  onNext: () => void;
}

function gapSentence(record: HoleRecord): string {
  if (record.result === 'birdie') return 'You picked the best option.';
  const points = Number(record.gap.toFixed(1));
  return `Teams that made your pick won ${points} point${points === 1 ? '' : 's'} less often than with the best option.`;
}

export function Reveal({ scenario, record, isLastHole, headingRef, onNext }: Props) {
  const label = (key: string) => scenario.options.find((o) => o.key === key)?.label ?? key;
  return (
    <section className="reveal" aria-labelledby="result">
      <h3 id="result" className={`result result--${record.result}`} tabIndex={-1} ref={headingRef}>
        {RESULT_LABELS[record.result]} <span className="result__strokes">({formatStrokes(record.strokes)})</span>
      </h3>
      <p>{gapSentence(record)}</p>

      <h4>How each option has worked out</h4>
      <ul className="bars">
        {scenario.options.map((option) => {
          const tags: string[] = [];
          if (option.key === record.pickedKey) tags.push('Your pick');
          if (option.winRate >= Math.max(...scenario.options.map((o) => o.winRate)) - 1e-9) tags.push('Best');
          if (option.key === scenario.actual.choice) tags.push('What the team did');
          return (
            <li key={option.key} className="bar">
              <div className="bar__head">
                <span className="bar__label">{option.label}</span>
                <span className="bar__value">{formatPercent(option.winRate)}</span>
              </div>
              <div className="bar__track" aria-hidden="true">
                <div
                  className={`bar__fill${option.key === record.pickedKey ? ' bar__fill--picked' : ''}`}
                  style={{ width: `${option.winRate * 100}%` }}
                />
              </div>
              <p className="bar__meta">
                Won {formatPercent(option.winRate)} of {option.n.toLocaleString('en-US')} similar situations
                {tags.length > 0 && (
                  <>
                    {' · '}
                    <strong>{tags.join(' · ')}</strong>
                  </>
                )}
              </p>
            </li>
          );
        })}
      </ul>

      <h4>What really happened</h4>
      <p className="game">{scenario.actual.game}</p>
      <p>
        The team chose: <strong>{label(scenario.actual.choice)}</strong>. {scenario.actual.summary}
      </p>
      <p>
        Final: <strong>{scenario.actual.final}</strong>
      </p>

      <p className="caveat">
        Win rates compare similar situations across NBA history. They show what usually happens, not what
        would have happened in this exact game.
      </p>

      <button type="button" className="primary" onClick={onNext}>
        {isLastHole ? 'See results' : 'Next hole'}
      </button>
    </section>
  );
}
