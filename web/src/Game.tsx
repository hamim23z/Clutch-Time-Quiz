import { useEffect, useReducer, useRef } from 'react';
import { FinalScreen } from './components/FinalScreen';
import { OptionButtons } from './components/OptionButtons';
import { Reveal } from './components/Reveal';
import { ScenarioCard } from './components/ScenarioCard';
import { ScoreBar } from './components/ScoreBar';
import { currentScenario, HOLES_PER_ROUND, isFinished, pickRound, roundReducer, startRound } from './round';
import type { Scenario } from './types';

interface Props {
  allScenarios: readonly Scenario[];
  random?: () => number;
}

export function Game({ allScenarios, random = Math.random }: Props) {
  const [round, dispatch] = useReducer(roundReducer, undefined, () =>
    startRound(pickRound(allScenarios, HOLES_PER_ROUND, random)),
  );
  const questionRef = useRef<HTMLHeadingElement>(null);
  const resultRef = useRef<HTMLHeadingElement>(null);
  const finalRef = useRef<HTMLHeadingElement>(null);
  const firstRender = useRef(true);

  const scenario = currentScenario(round);
  const finished = isFinished(round);
  const revealed = round.pickedKey !== null;
  const record = round.records[round.index];

  // Move focus to whatever just appeared, so keyboard and screen reader users land on the new content.
  // Not on the very first render: the page should not steal focus when it loads.
  useEffect(() => {
    if (firstRender.current) {
      firstRender.current = false;
      return;
    }
    if (finished) finalRef.current?.focus();
    else if (revealed) resultRef.current?.focus();
    else questionRef.current?.focus();
  }, [round.index, revealed, finished]);

  return (
    <>
      <ScoreBar hole={round.index + 1} totalHoles={round.scenarios.length} records={round.records} />
      {finished || !scenario ? (
        <FinalScreen
          scenarios={round.scenarios}
          records={round.records}
          headingRef={finalRef}
          onRestart={() =>
            dispatch({ type: 'restart', scenarios: pickRound(allScenarios, HOLES_PER_ROUND, random) })
          }
        />
      ) : (
        <>
          <ScenarioCard scenario={scenario} headingRef={questionRef} />
          {revealed && record ? (
            <Reveal
              scenario={scenario}
              record={record}
              isLastHole={round.index === round.scenarios.length - 1}
              headingRef={resultRef}
              onNext={() => dispatch({ type: 'next' })}
            />
          ) : (
            <OptionButtons options={scenario.options} onPick={(key) => dispatch({ type: 'pick', key })} />
          )}
        </>
      )}
    </>
  );
}
