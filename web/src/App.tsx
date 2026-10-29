import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { AnnouncerProvider } from './announcer';
import { SoundProvider, useSound } from './sound';
import { Dive } from './Dive';
import { Archive } from './components/Archive';
import { ComingSoon } from './components/ComingSoon';
import { Final } from './components/Final';
import { Home } from './components/Home';
import { HowToPlay } from './components/HowToPlay';
import { LAUNCH_DATE, PREVIEW_STORAGE_KEY, STORAGE_KEY } from './config';
import { loadData, type GameData } from './loadData';
import { buildIndex } from './matching';
import { dateInZone, diveCount, diveNumberOn, divePrompts, isDateString } from './schedule';
import { browserStorage, loadHistory, saveHistory, type History, type StorageLike } from './storage';
import { computeStreaks } from './streaks';
import type { PromptResult } from './types';

type Load = { status: 'loading' } | { status: 'error'; message: string } | ({ status: 'ready' } & GameData);
/** daily: today's dive, counts for the streak. archive: a past dive. test: the preview play-test, never saved. */
type Mode = 'daily' | 'archive' | 'test';
type View = { name: 'home' } | { name: 'howto' } | { name: 'archive' } | { name: 'results'; number: number } | { name: 'dive'; number: number; mode: Mode };

interface Props {
  /** The clock; tests pass a fixed one. */
  now?: () => Date;
  /** Where finished dives are kept. Defaults to localStorage (or nothing, if the browser refuses it). */
  storage?: StorageLike | null;
  /** The URL's query string; ?preview=1 enables the pre-launch play-test, ?preview=1&today=YYYY-MM-DD pretends it is that day. */
  search?: string;
  launchDate?: string;
  /** Outside-range names, overriding outside_range.json (tests). */
  outsideNames?: readonly string[];
}

export default function App({ now = () => new Date(), storage, search, launchDate = LAUNCH_DATE, outsideNames }: Props) {
  const params = useMemo(() => new URLSearchParams(search ?? (typeof window === 'undefined' ? '' : window.location.search)), [search]);
  const preview = params.get('preview') === '1';
  const store = useMemo(() => (storage === undefined ? browserStorage() : storage), [storage]);
  const storageKey = preview ? PREVIEW_STORAGE_KEY : STORAGE_KEY;

  const [load, setLoad] = useState<Load>({ status: 'loading' });
  const [history, setHistory] = useState<History>(() => loadHistory(store, storageKey));
  const historyRef = useRef<History>(history);
  const [saving, setSaving] = useState<boolean>(store !== null);
  const [view, setView] = useState<View | null>(null);

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

  // Which day it is (in the game's time zone). ?preview=1&today=... lets a tester pretend.
  const override = params.get('today');
  const todayDate = preview && override && isDateString(override) ? override : dateInZone(now());
  const today = diveNumberOn(todayDate, launchDate);
  const launched = today >= 1;
  const streaks = useMemo(() => computeStreaks(history, today), [history, today]);
  const total = load.status === 'ready' ? diveCount(load.prompts) : 0;

  // The streak pops on the home screen when it has gone up since that screen was last shown.
  const streakBaseline = useRef<number | null>(null);
  const streakUp = streakBaseline.current !== null && streaks.current > streakBaseline.current;
  useEffect(() => {
    if (view?.name === 'home') streakBaseline.current = streaks.current;
  }, [view, streaks.current]);

  // Open on the results screen if today's dive is already finished on this device.
  const opened = useRef(false);
  useEffect(() => {
    if (load.status !== 'ready' || opened.current) return;
    opened.current = true;
    setView(launched && history[today] ? { name: 'results', number: today } : { name: 'home' });
  }, [load.status, launched, history, today]);

  const finish = useCallback(
    (number: number, mode: Mode, results: PromptResult[]): void => {
      if (mode === 'test' || historyRef.current[number]) return; // the first finished play of a dive is the one that counts
      const next = { ...historyRef.current, [number]: { results, daily: mode === 'daily' } };
      historyRef.current = next;
      setHistory(next);
      setSaving(saveHistory(store, storageKey, next));
    },
    [store, storageKey],
  );

  const go = (next: View): void => setView(next);
  const startDive = (number: number): void => go({ name: 'dive', number, mode: number === today ? 'daily' : 'archive' });
  const names = outsideNames ?? (load.status === 'ready' ? load.outsideNames : []);

  const nav = { onHome: () => go({ name: 'home' }), onArchive: () => go({ name: 'archive' }), onHowTo: () => go({ name: 'howto' }) };

  return (
    <AnnouncerProvider>
      <SoundProvider storage={store}>
      <main className="app">
        <header className="top">
          <h1 className="title">
            <button type="button" className="title__button" onClick={nav.onHome} aria-label="Deep Cut, home">
              Deep Cut
            </button>
          </h1>
          <SoundToggle />
        </header>
        {load.status === 'loading' && <p>Loading prompts…</p>}
        {load.status === 'error' && (
          <p role="alert" className="error">
            Could not load the game data: {load.message}
          </p>
        )}
        {load.status === 'ready' && index && view && total < 1 && (
          <p role="alert" className="error">
            Could not load the game data: prompts.json has no complete dive of 7 prompts.
          </p>
        )}
        {load.status === 'ready' && index && view && total >= 1 && (
          <>
            {view.name === 'home' && !launched && (
              <ComingSoon
                launchDate={launchDate}
                onHowTo={nav.onHowTo}
                onPlayTest={preview ? () => go({ name: 'dive', number: 1, mode: 'test' }) : undefined}
              />
            )}
            {view.name === 'home' && launched && (
              <Home
                number={today}
                played={Boolean(history[today])}
                streaks={streaks}
                streakUp={streakUp}
                saving={saving}
                onPlay={() => startDive(today)}
                onResults={() => go({ name: 'results', number: today })}
                onArchive={nav.onArchive}
                onHowTo={nav.onHowTo}
              />
            )}
            {view.name === 'howto' && <HowToPlay onPlay={launched ? () => startDive(today) : nav.onHome} onBack={nav.onHome} />}
            {view.name === 'archive' && launched && (
              <Archive today={today} history={history} saving={saving} onPlay={startDive} onResults={(number) => go({ name: 'results', number })} onBack={nav.onHome} />
            )}
            {view.name === 'archive' && !launched && <ComingSoon launchDate={launchDate} onHowTo={nav.onHowTo} />}
            {view.name === 'results' && history[view.number] && (
              <Final
                key={`results-${view.number}`}
                prompts={divePrompts(load.prompts, view.number)}
                results={history[view.number]?.results ?? []}
                diveNumber={view.number}
                headingRef={focusOnMount}
                streak={view.number === today ? { value: streaks.current, increased: false } : undefined}
                {...nav}
              />
            )}
            {view.name === 'dive' && (
              <Dive
                key={`${view.number}-${view.mode}`}
                prompts={divePrompts(load.prompts, view.number)}
                index={index}
                diveNumber={view.number}
                outsideNames={names}
                streak={view.mode === 'daily' ? { value: streaks.current, increased: true } : undefined}
                onFinish={(results) => finish(view.number, view.mode, results)}
                {...nav}
              />
            )}
          </>
        )}
        {isMock && <p className="mock-note">Test data: the players, teams and prompts in this version are made up for the tests.</p>}
      </main>
      </SoundProvider>
    </AnnouncerProvider>
  );
}

/** A ref callback that moves focus to a heading when the results screen opens straight away. */
function focusOnMount(node: HTMLHeadingElement | null): void {
  node?.focus();
}

/** Off by default; remembers its setting. Nothing plays before the visitor's first interaction. */
function SoundToggle() {
  const { enabled, toggle } = useSound();
  return (
    <button type="button" className="sound-toggle" aria-pressed={enabled} onClick={toggle}>
      <span aria-hidden="true">{enabled ? '🔊' : '🔈'}</span> Sound {enabled ? 'on' : 'off'}
    </button>
  );
}
