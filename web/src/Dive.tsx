import { useEffect, useMemo, useReducer, useRef } from 'react';
import { Final } from './components/Final';
import { PromptScreen } from './components/PromptScreen';
import { Reveal } from './components/Reveal';
import { currentPrompt, diveReducer, isOver, isRevealed, pickDive, startDive, totalPoints } from './dive';
import type { Index } from './matching';
import type { Prompt, PromptResult } from './types';

interface Props {
  prompts: readonly Prompt[];
  index: Index;
  diveNumber: number;
  random?: () => number;
  outsideNames?: readonly string[];
  onPlayAgain: () => void;
  onHowTo: () => void;
}

export function Dive({ prompts, index, diveNumber, random = Math.random, outsideNames, onPlayAgain, onHowTo }: Props) {
  const [state, dispatch] = useReducer(diveReducer, undefined, () => startDive(pickDive(prompts, random)));
  const resultRef = useRef<HTMLHeadingElement>(null);
  const finalRef = useRef<HTMLHeadingElement>(null);
  const firstRender = useRef(true);

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

  if (over || !prompt) {
    return <Final prompts={state.prompts} results={state.results} diveNumber={diveNumber} headingRef={finalRef} onPlayAgain={onPlayAgain} onHowTo={onHowTo} />;
  }
  if (revealed && result) {
    return <Reveal prompt={prompt} result={result} isLast={state.index === state.prompts.length - 1} headingRef={resultRef} onNext={() => dispatch({ type: 'next' })} />;
  }
  return (
    <PromptScreen
      key={prompt.id}
      prompt={prompt}
      index={index}
      number={state.index + 1}
      total={state.prompts.length}
      points={points}
      outsideNames={outsideNames}
      onResult={(r: PromptResult) => dispatch({ type: 'submit', result: r })}
    />
  );
}
