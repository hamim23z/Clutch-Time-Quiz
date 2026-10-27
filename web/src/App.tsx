import { useEffect, useState } from 'react';
import { Game } from './Game';
import { loadScenarios } from './loadScenarios';
import type { Scenario } from './types';

type Load =
  | { status: 'loading' }
  | { status: 'error'; message: string }
  | { status: 'ready'; scenarios: Scenario[] };

interface Props {
  /** Random source for choosing the round; tests pass a fixed one. */
  random?: () => number;
}

export default function App({ random }: Props) {
  const [load, setLoad] = useState<Load>({ status: 'loading' });

  useEffect(() => {
    let cancelled = false;
    loadScenarios(`${import.meta.env.BASE_URL}scenarios.json`)
      .then((scenarios) => {
        if (!cancelled) setLoad({ status: 'ready', scenarios });
      })
      .catch((err: unknown) => {
        if (!cancelled) setLoad({ status: 'error', message: err instanceof Error ? err.message : String(err) });
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const isMock = load.status === 'ready' && load.scenarios.every((s) => s.id.startsWith('mock-'));

  return (
    <main className="app">
      <h1 className="title">Clutch Time Quiz</h1>
      {load.status === 'loading' && <p role="status">Loading scenarios…</p>}
      {load.status === 'error' && (
        <p role="alert" className="error">
          Could not load the scenarios: {load.message}
        </p>
      )}
      {load.status === 'ready' && <Game allScenarios={load.scenarios} random={random} />}
      {isMock && (
        <p className="mock-note">
          Demo data: these situations, teams and win rates are made up for testing the game.
        </p>
      )}
    </main>
  );
}
