import { useEffect, useMemo, useState } from 'react';
import ShotChart from './chart/ShotChart';
import { ChartProvider, createChartStore, INITIAL_CHART } from './chart/chartStore';
import { ReducedMotionOverride } from './motion';
import { shotForPoints } from './shots';
import { TIER_POINTS } from './tiers';
import type { Tier } from './types';

const OUTCOMES: Array<{ name: string; tier: Tier | null }> = [{ name: 'airball', tier: null }, { name: 'tier-1', tier: 1 }, { name: 'tier-2', tier: 2 }, { name: 'tier-3', tier: 3 }, { name: 'tier-4', tier: 4 }, { name: 'tier-5', tier: 5 }, { name: 'tier-6', tier: 6 }];
const LOOP_MS = 2600;

/**
 * A review page (?animations=1 in development, ?preview=1&animations=1 in a build): every outcome on the real chart, one after
 * another on a loop, with buttons to play one, and a switch for the reduced-motion version.
 */
export default function AnimationsPage() {
  const store = useMemo(() => createChartStore({ ...INITIAL_CHART, phase: 'prompt', promptNumber: 1, total: 7, diveNumber: 12, clock: 25 }), []);
  const [current, setCurrent] = useState(OUTCOMES[0]!.name);
  const [auto, setAuto] = useState(true);
  const [reduced, setReduced] = useState(false);

  const play = (name: string): void => {
    const outcome = OUTCOMES.find((o) => o.name === name) ?? OUTCOMES[0]!;
    const before = store.get();
    const marks = before.marks.length >= 7 ? [] : before.marks; // a fresh dive after seven
    const points = (marks.length === 0 ? 0 : before.points) + (outcome.tier === null ? 0 : TIER_POINTS[outcome.tier]);
    setCurrent(name);
    store.set({ phase: 'shot', marks: [...marks, { id: `demo-${before.shotKey + 1}`, tier: outcome.tier }], points, shot: shotForPoints(outcome.tier === null ? 0 : TIER_POINTS[outcome.tier]), shotKey: before.shotKey + 1, skipped: false, clock: null, promptNumber: marks.length + 1 });
  };

  useEffect(() => {
    play('airball');
    // eslint-disable-next-line react-hooks/exhaustive-deps -- once
  }, []);

  useEffect(() => {
    if (!auto) return;
    const id = setInterval(() => {
      setCurrent((c) => {
        const next = OUTCOMES[(OUTCOMES.findIndex((o) => o.name === c) + 1) % OUTCOMES.length]!.name;
        play(next);
        return next;
      });
    }, LOOP_MS);
    return () => clearInterval(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps -- play only uses the store
  }, [auto, store]);

  return (
    <div className="animations">
      <div className="animations__chart" data-reduced={reduced}>
        <ChartProvider store={store}>
          <ReducedMotionOverride.Provider value={reduced ? true : null}>
            <ShotChart />
          </ReducedMotionOverride.Provider>
        </ChartProvider>
      </div>
      <main className="animations__panel">
        <h1 className="title">Shot animations on the chart</h1>
        <p className="animations__now" data-testid="animation-now">
          Now: <strong>{current}</strong>
        </p>
        <label className="animations__toggle">
          <input type="checkbox" checked={auto} onChange={(e) => setAuto(e.target.checked)} /> Loop through all seven
        </label>
        <label className="animations__toggle">
          <input type="checkbox" checked={reduced} onChange={(e) => setReduced(e.target.checked)} /> Show the reduced-motion version
        </label>
        <div className="animations__buttons">
          {OUTCOMES.map((o) => (
            <button key={o.name} type="button" className="secondary" data-testid={`demo-${o.name}`} aria-pressed={current === o.name} onClick={() => { setAuto(false); play(o.name); }}>
              {o.name}
            </button>
          ))}
        </div>
      </main>
    </div>
  );
}
