import { createContext, useContext, useMemo, useSyncExternalStore, type ReactNode } from 'react';
import type { ShotInfo } from '../shots';
import type { PromptResult, Tier } from '../types';

/** One answered prompt, as the chart draws it: a tier (a made shot) or null (an airball: wrong, out of range or out of time). */
export interface ChartMark {
  id: string;
  tier: Tier | null;
}

export const marksFrom = (results: readonly PromptResult[]): ChartMark[] => results.map((r) => ({ id: r.promptId, tier: r.status === 'valid' ? r.tier : null }));

/** What the shot chart shows. The panel on the left publishes it; the chart only draws it, and never carries information of its own. */
export interface ChartState {
  /** idle: home, archive, how to play. prompt: a question is on. shot: a result is on. results: all seven shots on the chart. */
  phase: 'idle' | 'prompt' | 'shot' | 'results';
  /** The box over the court when idle ("NBA DEEP CUT" is the home screen, then "ARCHIVE", ...). */
  headline: string;
  promptNumber: number;
  total: number;
  points: number;
  diveNumber: number | null;
  /** Seconds left on the shot clock (null: not counting). */
  clock: number | null;
  shot: ShotInfo | null;
  /** Changes for every new shot, so the chart restarts its animation. */
  shotKey: number;
  /** The player skipped the shot: jump to its end. */
  skipped: boolean;
  /** The answers so far, in prompt order. */
  marks: ChartMark[];
  /** Changes when the results screen replays the seven shots. */
  replayKey: number;
}

export const INITIAL_CHART: ChartState = {
  phase: 'idle', headline: 'NBA DEEP CUT', promptNumber: 0, total: 7, points: 0, diveNumber: null, clock: null,
  shot: null, shotKey: 0, skipped: false, marks: [], replayKey: 0,
};

export interface ChartStore {
  get(): ChartState;
  set(patch: Partial<ChartState>): void;
  subscribe(listener: () => void): () => void;
}

/** A tiny store, so the chart re-draws on its own (every second for the shot clock) without re-rendering the whole panel. */
export function createChartStore(initial: ChartState = INITIAL_CHART): ChartStore {
  let state = initial;
  const listeners = new Set<() => void>();
  return {
    get: () => state,
    set(patch) {
      const next = { ...state, ...patch };
      const changed = (Object.keys(patch) as Array<keyof ChartState>).some((k) => state[k] !== next[k]);
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

const ChartContext = createContext<ChartStore>(createChartStore());

export function ChartProvider({ store, children }: { store?: ChartStore; children: ReactNode }) {
  const value = useMemo(() => store ?? createChartStore(), [store]);
  return <ChartContext.Provider value={value}>{children}</ChartContext.Provider>;
}

export const useChartStore = (): ChartStore => useContext(ChartContext);

export function useChartState(): ChartState {
  const store = useChartStore();
  return useSyncExternalStore(store.subscribe, store.get, store.get);
}
