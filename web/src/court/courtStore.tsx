import { createContext, useContext, useMemo, useSyncExternalStore, type ReactNode } from 'react';
import type { ShotInfo } from '../shots';

/** What the court shows. The panel on the left publishes it; the court only draws it, and never carries information of its own. */
export interface CourtState {
  /** idle: home, archive, how to play. prompt: a question is on. shot: a result is on. results: the replay of the seven shots. */
  phase: 'idle' | 'prompt' | 'shot' | 'results';
  /** The jumbotron's middle line when idle ("NBA DEEP CUT", "ARCHIVE", ...). */
  headline: string;
  promptNumber: number;
  total: number;
  points: number;
  diveNumber: number | null;
  /** Seconds left on the shot clock (null: not counting). */
  clock: number | null;
  shot: ShotInfo | null;
  /** Changes for every new shot, so the court restarts its animation. */
  shotKey: number;
  /** The player skipped the shot: jump to its end. */
  skipped: boolean;
  /** The seven shots of a finished dive, replayed on the court in order. */
  replay: ShotInfo[] | null;
  replayKey: number;
}

export const INITIAL_COURT: CourtState = {
  phase: 'idle', headline: 'NBA DEEP CUT', promptNumber: 0, total: 7, points: 0, diveNumber: null, clock: null,
  shot: null, shotKey: 0, skipped: false, replay: null, replayKey: 0,
};

export interface CourtStore {
  get(): CourtState;
  set(patch: Partial<CourtState>): void;
  subscribe(listener: () => void): () => void;
}

/** A tiny store, so the court re-draws on its own (every second for the shot clock) without re-rendering the whole panel. */
export function createCourtStore(initial: CourtState = INITIAL_COURT): CourtStore {
  let state = initial;
  const listeners = new Set<() => void>();
  return {
    get: () => state,
    set(patch) {
      const next = { ...state, ...patch };
      const changed = (Object.keys(patch) as Array<keyof CourtState>).some((k) => state[k] !== next[k]);
      if (!changed) return;
      state = next;
      listeners.forEach((l) => l());
    },
    subscribe(listener) {
      listeners.add(listener);
      return () => listeners.delete(listener);
    },
  };
}

const CourtContext = createContext<CourtStore>(createCourtStore());

export function CourtProvider({ store, children }: { store?: CourtStore; children: ReactNode }) {
  const value = useMemo(() => store ?? createCourtStore(), [store]);
  return <CourtContext.Provider value={value}>{children}</CourtContext.Provider>;
}

export const useCourtStore = (): CourtStore => useContext(CourtContext);

export function useCourtState(): CourtState {
  const store = useCourtStore();
  return useSyncExternalStore(store.subscribe, store.get, store.get);
}
