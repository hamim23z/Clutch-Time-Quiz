import { useEffect, useMemo, useReducer, useRef, useState } from 'react';
import { Final } from './components/Final';
import { PromptScreen } from './components/PromptScreen';
import { Reveal } from './components/Reveal';
import { Scoreboard } from './components/Scoreboard';
import { useReducedMotion } from './motion';
import { currentPrompt, diveReducer, isOver, isRevealed, startDive, totalPoints } from './dive2';
import type { Index } from './matching';
import type { Prompt, PromptResult } from './types';

interface Props {
  /** The 7 prompts of the dive, in file order. */
  prompts: readonly Prompt[];
  index: Index;
  diveNumber: number;
  outsideNames?: readonly string[];
  /** Called once, when the last prompt has been answered and the results screen appears. */
  onFinish: (results: PromptResult[]) => void;
  onHome: () => void;
  onArchive: () => void;
  onHowTo: () => void;
  /** Streak shown on the results screen, and whether it just went up. */
  streak?: { value: number; increased: boolean };
}

export function Dive({ prompts, index, diveNumber, outsideNames, onFinish, onHome, onArchive, onHowTo, streak }: Props) {
  const [state, dispatch] = useReducer(diveReducer, undefined, () => startDive([...prompts]));
  const resultRef = useRef<HTMLHeadingElement>(null);
  const finalRef = useRef<HTMLHeadingElement>(null);
  const firstRender = useRef(true);
  const finished = useRef(false);
  const reduced = useReducedMotion();
  const [skippedAt, setSkippedAt] = useState(-1); // the prompt whose shot the player skipped

  const prompt = currentPrompt(state);
  const over = isOver(state);
  const revealed = isRevealed(state);
  const result = state.results[state.index];
  const points = useMemo(() => totalPoints(state.results), [state.results]);

  // Move focus to what just appeared. A new prompt focuses its own input (see AnswerInput).
  useEffect(() => {
    if (firstRender.current) {
      firstRender.current = false;
      return;
    }
    if (over) finalRef.current?.focus();
    else if (revealed) resultRef.current?.focus();
  }, [state.index, revealed, over]);

  useEffect(() => {
    if (over && !finished.current) {
      finished.current = true;
      onFinish(state.results);
    }
  }, [over, state.results, onFinish]);

  if (over || !prompt) {
    return <Final prompts={state.prompts} results={state.results} diveNumber={diveNumber} headingRef={finalRef} onHome={onHome} onArchive={onArchive} onHowTo={onHowTo} streak={streak} />;
  }
  const skipped = skippedAt === state.index;
  const before = totalPoints(state.results.slice(0, state.index));
  const board = (
    <Scoreboard
      number={state.index + 1}
      total={state.prompts.length}
      pointsBefore={revealed ? before : points}
      points={points}
      diveNumber={diveNumber}
      rollDelayMs={reduced || skipped ? 0 : 950}
      instant={reduced || skipped || !revealed}
    />
  );
  if (revealed && result) {
    return (
      <>
        {board}
        <Reveal
          key={prompt.id}
          prompt={prompt}
          result={result}
          isLast={state.index === state.prompts.length - 1}
          headingRef={resultRef}
          onNext={() => dispatch({ type: 'next' })}
          skipped={skipped}
          onSkip={() => setSkippedAt(state.index)}
        />
      </>
    );
  }
  return (
    <>
      {board}
      <PromptScreen
        key={prompt.id}
        prompt={prompt}
        index={index}
        outsideNames={outsideNames}
        onResult={(r: PromptResult) => dispatch({ type: 'submit', result: r })}
      />
    </>
  );
}
