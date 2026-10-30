import { lazy, Suspense, useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { AnnouncerProvider } from './announcer';
import { CourtProvider, useCourtStore } from './court/courtStore';
import { useLayout } from './layout';
import { SoundProvider, useSound } from './sound';
import { Dive } from './Dive';
import { Archive } from './components/Archive';
import { ComingSoon } from './components/ComingSoon';
import { Final } from './components/Final';
import { ErrorScreen } from './components/ErrorScreen';
import { Home } from './components/Home';
import { LoadingScreen } from './components/LoadingScreen';
import { HowToPlay } from './components/HowToPlay';
import { LAUNCH_DATE, PREVIEW_PROGRESS_KEY, PREVIEW_STORAGE_KEY, PROGRESS_KEY, STORAGE_KEY } from './config';
import { timeoutResult } from './answer';
import { SECONDS_PER_PROMPT } from './tiers';
import { clearDataCache, loadData, type GameData } from './loadData';
import { buildIndex } from './matching';
import { dateInZone, diveCount, diveNumberOn, divePrompts, isDateString } from './schedule';
import { browserStorage, loadHistory, loadProgress, saveHistory, saveProgress, type History, type Progress, type StorageLike } from './storage';
import { computeStreaks } from './streaks';
import type { Prompt, PromptResult } from './types';

type Load = { status: 'loading' } | { status: 'error'; message: string } | ({ status: 'ready' } & GameData);
/** daily: today's dive, counts for the streak. archive: a past dive. test: the preview play-test, never saved. */
// The court is the heavy art: it loads after the panel, so the home screen is quick.
const CourtScene = lazy(() => import('./court/CourtScene'));

type Mode = 'daily' | 'archive' | 'test';
type View = { name: 'home' } | { name: 'howto' } | { name: 'archive' } | { name: 'results'; number: number } | { name: 'dive'; number: number; mode: Mode; resume?: { results: PromptResult[]; elapsedMs: number } };

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

export default function App(props: Props) {
  return (
    <CourtProvider>
      <Game {...props} />
    </CourtProvider>
  );
}

function Game({ now = () => new Date(), storage, search, launchDate = LAUNCH_DATE, outsideNames }: Props) {
  const courtStore = useCourtStore();
  const layout = useLayout();
  const params = useMemo(() => new URLSearchParams(search ?? (typeof window === 'undefined' ? '' : window.location.search)), [search]);
  const preview = params.get('preview') === '1';
  const store = useMemo(() => (storage === undefined ? browserStorage() : storage), [storage]);
  const storageKey = preview ? PREVIEW_STORAGE_KEY : STORAGE_KEY;
  const progressKey = preview ? PREVIEW_PROGRESS_KEY : PROGRESS_KEY;

  const [load, setLoad] = useState<Load>({ status: 'loading' });
  const [attempt, setAttempt] = useState(0); // bumped by the retry button
  const [history, setHistory] = useState<History>(() => loadHistory(store, storageKey));
  const historyRef = useRef<History>(history);
  const storedProgress = useRef<Progress | null>(loadProgress(store, progressKey)); // read once, at load
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
  }, [attempt]);

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

  // The latest saved progress, kept in memory too so that leaving a dive and coming back resumes it instead of restarting it.
  const progressRef = useRef<Progress | null>(storedProgress.current);

  /** What to resume for a saved dive: its answers and elapsed time, or null if it is stale (another day, other prompts, finished). */
  const resumeFor = (saved: Progress, prompts: readonly Prompt[]): { results: PromptResult[]; elapsedMs: number } | null => {
    const sameDive = prompts.length === 7 && prompts.every((p, i) => p.id === saved.promptIds[i]);
    // a daily dive from an earlier day is discarded, and so is one whose prompts have changed or that is already finished
    const current = saved.mode === 'archive' ? saved.number <= today : saved.number === today && launched;
    if (!sameDive || !current || historyRef.current[saved.number]) return null;
    let results = saved.results;
    let elapsed = saved.startedAt === null ? 0 : Math.max(0, now().getTime() - saved.startedAt);
    // time ran out while the page was closed or the dive was left: that prompt is a timeout
    if (results.length < 7 && elapsed >= SECONDS_PER_PROMPT * 1000) {
      results = [...results, timeoutResult(prompts[results.length] as Prompt, '')];
      elapsed = 0;
    }
    return { results, elapsedMs: elapsed };
  };

  // On load: finish or resume a dive that was left half-played, else open on today's results if it is finished, else home.
  const opened = useRef(false);
  useEffect(() => {
    if (load.status !== 'ready' || opened.current) return;
    opened.current = true;
    const saved = storedProgress.current;
    storedProgress.current = null;
    if (saved) {
      const resume = resumeFor(saved, divePrompts(load.prompts, saved.number));
      if (resume && resume.results.length === 7) {
        finish(saved.number, saved.mode, resume.results);
        setView({ name: 'results', number: saved.number });
        return;
      }
      if (resume) {
        setView({ name: 'dive', number: saved.number, mode: saved.mode, resume });
        return;
      }
      progressRef.current = null;
      saveProgress(store, progressKey, null);
    }
    setView(launched && history[today] ? { name: 'results', number: today } : { name: 'home' });
    // eslint-disable-next-line react-hooks/exhaustive-deps -- once, when the data has loaded
  }, [load.status]);

  const finish = useCallback(
    (number: number, mode: Mode, results: PromptResult[]): void => {
      if (mode === 'test' || historyRef.current[number]) return; // the first finished play of a dive is the one that counts
      const next = { ...historyRef.current, [number]: { results, daily: mode === 'daily' } };
      historyRef.current = next;
      setHistory(next);
      setSaving(saveHistory(store, storageKey, next));
      progressRef.current = null;
      saveProgress(store, progressKey, null); // the dive is finished: nothing left to resume
    },
    [store, storageKey, progressKey],
  );

  const retry = (): void => {
    clearDataCache();
    setLoad({ status: 'loading' });
    setAttempt((n) => n + 1);
  };
  // The court on the right follows the screen on the left. A dive and the results publish their own state.
  useEffect(() => {
    if (!view || view.name === 'dive' || view.name === 'results') return;
    const headline = view.name === 'howto' ? 'HOW TO PLAY' : view.name === 'archive' ? 'ARCHIVE' : launched ? 'NBA DEEP CUT' : 'COMING SOON';
    courtStore.set({ phase: 'idle', headline, diveNumber: launched ? today : null, points: 0, promptNumber: 0, clock: null, shot: null, replay: null, skipped: false });
  }, [view, launched, today, courtStore]);

  const go = (next: View): void => setView(next);
  const startDive = (number: number): void => {
    const mode = number === today ? 'daily' : 'archive';
    const saved = progressRef.current;
    const resume = saved && saved.number === number && load.status === 'ready' ? resumeFor(saved, divePrompts(load.prompts, number)) : null;
    go({ name: 'dive', number, mode, resume: resume && resume.results.length < 7 ? resume : undefined });
  };
  const names = outsideNames ?? (load.status === 'ready' ? load.outsideNames : []);

  const nav = { onHome: () => go({ name: 'home' }), onArchive: () => go({ name: 'archive' }), onHowTo: () => go({ name: 'howto' }) };

  const heroHome = view?.name === 'home' && launched; // the home screen's wordmark is the page's h1
  return (
    <AnnouncerProvider>
      <SoundProvider storage={store}>
      <div className={`shell shell--${layout}`} data-layout={layout}>
      <main className="panel">
        <header className={`top${heroHome ? ' top--home' : ''}`}>
          {!heroHome && (
            <button type="button" className="brand" onClick={nav.onHome} aria-label="Deep Cut, home">
              <span className="brand__nba">NBA</span> Deep Cut
            </button>
          )}
          {!heroHome && <h1 className="visually-hidden">NBA Deep Cut</h1>}
          <SoundToggle />
        </header>
        {(load.status === 'loading' || (load.status === 'ready' && !view)) && <LoadingScreen />}
        {load.status === 'error' && <ErrorScreen message={load.message} onRetry={retry} />}
        {load.status === 'ready' && index && view && total < 1 && <ErrorScreen message="prompts.json has no complete dive of 7 prompts." onRetry={retry} />}
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
                resume={view.resume}
                clock={() => now().getTime()}
                onProgress={(results, startedAt) => {
                  if (view.mode === 'test') return;
                  const promptIds = divePrompts(load.prompts, view.number).map((p) => p.id);
                  const progress: Progress = { number: view.number, mode: view.mode, promptIds, results, startedAt };
                  progressRef.current = progress;
                  if (!saveProgress(store, progressKey, progress) && store !== null) setSaving(false);
                }}
                onFinish={(results) => finish(view.number, view.mode, results)}
                {...nav}
              />
            )}
          </>
        )}
        {isMock && <p className="mock-note">Test data: the players, teams and prompts in this version are made up for the tests.</p>}
        <footer className="fineprint">Unofficial fan game. Not affiliated with the NBA.</footer>
      </main>
      <div className="court-pane" aria-hidden="true">
        <Suspense fallback={<div className="court-fallback" />}>
          <CourtScene />
        </Suspense>
      </div>
      </div>
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
