import { useEffect, useMemo, useState } from 'react';
import { AnnouncerProvider } from './announcer';
import { Dive } from './Dive';
import { HowToPlay } from './components/HowToPlay';
import { loadData } from './loadData';
import { buildIndex } from './matching';
import type { Prompt, Universe } from './types';

type Load = { status: 'loading' } | { status: 'error'; message: string } | { status: 'ready'; prompts: Prompt[]; universe: Universe };
type View = 'home' | 'howto' | 'dive';

interface Props {
  /** Random source for choosing the prompts of a dive; tests pass a fixed one. */
  random?: () => number;
  outsideNames?: readonly string[];
}

export default function App({ random, outsideNames }: Props) {
  const [load, setLoad] = useState<Load>({ status: 'loading' });
  const [view, setView] = useState<View>('home');
  // The dive number is a counter for this visit. Daily rotation will replace it with the number of the day.
  const [diveNumber, setDiveNumber] = useState(0);

  useEffect(() => {
    let cancelled = false;
    loadData(import.meta.env.BASE_URL)
      .then((data) => {
        if (!cancelled) setLoad({ status: 'ready', ...data });
      })
      .catch((err: unknown) => {
        if (!cancelled) setLoad({ status: 'error', message: err instanceof Error ? err.message : String(err) });
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const index = useMemo(() => (load.status === 'ready' ? buildIndex(load.universe) : null), [load]);
  const isMock = load.status === 'ready' && load.prompts.every((p) => p.id.startsWith('mock-'));

  const play = (): void => {
    setDiveNumber((n) => n + 1);
    setView('dive');
  };

  return (
    <AnnouncerProvider>
      <main className="app">
        <header className="top">
          <h1 className="title">
            <button type="button" className="title__button" onClick={() => setView('home')} aria-label="Deep Cut, home">
              Deep Cut
            </button>
          </h1>
        </header>
        {load.status === 'loading' && <p>Loading prompts…</p>}
        {load.status === 'error' && (
          <p role="alert" className="error">
            Could not load the game data: {load.message}
          </p>
        )}
        {load.status === 'ready' && index && view === 'home' && (
          <section className="card home" aria-labelledby="home-heading">
            <h2 id="home-heading">The daily trivia game where the obvious answer loses.</h2>
            <p>Seven basketball prompts, 25 seconds each. Name a valid answer, and the more obscure it is, the more it scores.</p>
            <div className="actions">
              <button type="button" className="primary" onClick={play}>
                Play
              </button>
              <button type="button" className="secondary" onClick={() => setView('howto')}>
                How to play
              </button>
            </div>
          </section>
        )}
        {load.status === 'ready' && view === 'howto' && <HowToPlay onPlay={play} onBack={() => setView('home')} />}
        {load.status === 'ready' && index && view === 'dive' && (
          <Dive
            key={diveNumber}
            prompts={load.prompts}
            index={index}
            diveNumber={diveNumber}
            random={random}
            outsideNames={outsideNames}
            onPlayAgain={play}
            onHowTo={() => setView('howto')}
          />
        )}
        {isMock && (
          <p className="mock-note">Demo data: the players, teams and prompts in this version are made up to test the game.</p>
        )}
      </main>
    </AnnouncerProvider>
  );
}
