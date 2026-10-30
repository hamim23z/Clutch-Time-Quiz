import { useEffect, useState } from 'react';
import CourtScene from './court/CourtScene';
import { CourtProvider, createCourtStore, INITIAL_COURT } from './court/courtStore';
import { SHOT_MS, SHOT_NAMES, shotForPoints, type ShotName } from './shots';
import { SPOTS } from './court/geometry';
import { ReducedMotionOverride } from './motion';
import { useMemo } from 'react';

const POINTS: Record<ShotName, number> = { airball: 0, clank: 10, rattle: 20, bank: 35, swish: 55, 'deep-swish': 75, dunk: 100 };
const LOOP_MS = SHOT_MS + 1800;

/**
 * A review page (?animations=1 in development, ?preview=1&animations=1 in a build): every shot on the real court, one after
 * another on a loop, with buttons to play one, and a switch for the reduced-motion version.
 */
export default function AnimationsPage() {
  const store = useMemo(() => createCourtStore({ ...INITIAL_COURT, phase: 'shot', promptNumber: 3, total: 7, diveNumber: 12, points: 0 }), []);
  const [current, setCurrent] = useState<ShotName>('airball');
  const [auto, setAuto] = useState(true);
  const [reduced, setReduced] = useState(false);

  const play = (name: ShotName): void => {
    setCurrent(name);
    const shot = shotForPoints(POINTS[name]);
    store.set({ phase: 'shot', shot, shotKey: store.get().shotKey + 1, skipped: false, points: store.get().points + shot.points, promptNumber: 3, diveNumber: 12 });
  };

  useEffect(() => {
    play('airball');
    // eslint-disable-next-line react-hooks/exhaustive-deps -- once
  }, []);

  useEffect(() => {
    if (!auto) return;
    const id = setInterval(() => {
      setCurrent((c) => {
        const next = SHOT_NAMES[(SHOT_NAMES.indexOf(c) + 1) % SHOT_NAMES.length] ?? 'airball';
        const shot = shotForPoints(POINTS[next]);
        store.set({ phase: 'shot', shot, shotKey: store.get().shotKey + 1, skipped: false, points: next === 'airball' ? 0 : store.get().points + shot.points });
        return next;
      });
    }, LOOP_MS);
    return () => clearInterval(id);
  }, [auto, store]);

  return (
    <div className="animations">
      <div className="animations__court" data-reduced={reduced}>
        <CourtProvider store={store}>
          <ReducedMotionOverride.Provider value={reduced ? true : null}>
            <CourtScene />
          </ReducedMotionOverride.Provider>
        </CourtProvider>
      </div>
      <main className="animations__panel">
        <h1 className="title">Shot animations on the court</h1>
        <p className="animations__now" data-testid="animation-now">
          Now: <strong>{current}</strong> ({POINTS[current]} points, shot from ({SPOTS[current].x}, {SPOTS[current].y}))
        </p>
        <label className="animations__toggle">
          <input type="checkbox" checked={auto} onChange={(e) => setAuto(e.target.checked)} /> Loop through all seven
        </label>
        <label className="animations__toggle">
          <input type="checkbox" checked={reduced} onChange={(e) => setReduced(e.target.checked)} /> Show the reduced-motion version
        </label>
        <div className="animations__buttons">
          {SHOT_NAMES.map((name) => (
            <button key={name} type="button" className="secondary" data-testid={`demo-${name}`} aria-pressed={current === name} onClick={() => { setAuto(false); play(name); }}>
              {name} · {POINTS[name]}
            </button>
          ))}
        </div>
      </main>
    </div>
  );
}
