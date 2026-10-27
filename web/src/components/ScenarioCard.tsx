import type { Ref } from 'react';
import { describeMargin, describePossession, describeQuarter, formatClock } from '../format';
import type { Scenario } from '../types';

interface Props {
  scenario: Scenario;
  headingRef: Ref<HTMLHeadingElement>;
}

/** The situation and the question. Teams and the date are not part of this card on purpose. */
export function ScenarioCard({ scenario, headingRef }: Props) {
  const { state } = scenario;
  return (
    <section className="card" aria-labelledby="question">
      <dl className="situation">
        <div>
          <dt>Quarter</dt>
          <dd>{describeQuarter(state.quarter)}</dd>
        </div>
        <div>
          <dt>Margin</dt>
          <dd>{describeMargin(state.margin)}</dd>
        </div>
        <div>
          <dt>Time left</dt>
          <dd>{formatClock(state.secondsLeft)}</dd>
        </div>
        <div>
          <dt>Ball</dt>
          <dd>{describePossession(state.possession)}</dd>
        </div>
      </dl>
      <h2 id="question" className="question" tabIndex={-1} ref={headingRef}>
        {scenario.question}
      </h2>
    </section>
  );
}
