import { useEffect, useMemo, useReducer, useRef, useState } from 'react';
import { marksFrom, useChartStore } from './chart/chartStore';
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
  /** Resume a dive after a reload: the answers already given, and how much of the prompt on screen has gone. */
  resume?: { results: PromptResult[]; elapsedMs: number };
  /** Called after every answer and whenever a new prompt appears, so progress can be saved. startedAt is null on a result screen. */
  onProgress?: (results: PromptResult[], startedAt: number | null) => void;
  clock?: () => number;
}

export function Dive({ prompts, index, diveNumber, outsideNames, onFinish, onHome, onArchive, onHowTo, streak, resume, onProgress, clock = Date.now }: Props) {
  const [state, dispatch] = useReducer(diveReducer, undefined, () => {
    const fresh = startDive([...prompts]);
    return resume ? { ...fresh, results: resume.results, index: resume.results.length } : fresh;
  });
  const startedAt = useRef<number | null>(null);
  const resumedElapsed = useRef(resume?.elapsedMs ?? 0);
  const resumeIndex = useRef(resume ? resume.results.length : -1);
  const resultRef = useRef<HTMLHeadingElement>(null);
  const finalRef = useRef<HTMLHeadingElement>(null);
  const firstRender = useRef(true);
  const finished = useRef(false);
  const reduced = useReducedMotion();
  const chart = useChartStore();
  const [skippedAt, setSkippedAt] = useState(-1); // the prompt whose shot the player skipped

  const prompt = currentPrompt(state);
  const over = isOver(state);
  const revealed = isRevealed(state);

  // Save after every answer, and note when each prompt appeared (a reload cannot give extra time).
  useEffect(() => {
    if (over) return;
    if (!revealed && startedAt.current === null) startedAt.current = clock() - (state.index === resumeIndex.current ? resumedElapsed.current : 0);
    if (revealed) startedAt.current = null;
    onProgress?.(state.results, revealed ? null : startedAt.current);
    // eslint-disable-next-line react-hooks/exhaustive-deps -- once per answer or new prompt
  }, [state.index, state.results.length, over]);
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

  // The chart follows the dive: which prompt, the points, the answers so far, and what is on (a question or a result).
  const dived = totalPoints(state.results);
  useEffect(() => {
    if (over) return;
    chart.set({ phase: revealed ? 'shot' : 'prompt', promptNumber: Math.min(state.index + 1, state.prompts.length), total: state.prompts.length, points: dived, diveNumber, marks: marksFrom(state.results), ...(revealed ? {} : { clock: 25, shot: null, skipped: false }) });
  }, [chart, over, revealed, state.index, state.results, state.prompts.length, dived, diveNumber]);

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
          onSkip={() => {
            setSkippedAt(state.index);
            chart.set({ skipped: true });
          }}
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
        elapsedMs={state.index === resumeIndex.current ? resumedElapsed.current : 0}
        onResult={(r: PromptResult) => dispatch({ type: 'submit', result: r })}
      />
    </>
  );
}
