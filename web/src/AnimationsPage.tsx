import { useEffect, useState } from 'react';
import { ShotAnimation } from './components/ShotAnimation';
import { ShotLabel } from './components/ShotLabel';
import { SHOT_MS, SHOT_NAMES, shotForPoints, type ShotName } from './shots';

const POINTS: Record<ShotName, number> = { airball: 0, clank: 10, rattle: 20, bank: 35, swish: 55, 'deep-swish': 75, dunk: 100 };
const LOOP_MS = SHOT_MS + 1800;

/** A review page (?animations=1 in development, ?preview=1&animations=1 in a build): every shot on a loop. */
export default function AnimationsPage() {
  const [round, setRound] = useState(0);
  const [reduced, setReduced] = useState(false);
  useEffect(() => {
    const id = setInterval(() => setRound((n) => n + 1), LOOP_MS);
    return () => clearInterval(id);
  }, []);
  return (
    <main className="app animations">
      <h1 className="title">Shot animations</h1>
      <label className="animations__toggle">
        <input type="checkbox" checked={reduced} onChange={(e) => setReduced(e.target.checked)} /> Show the reduced-motion version
      </label>
      <button type="button" className="secondary" onClick={() => setRound((n) => n + 1)}>
        Replay now
      </button>
      <div className="animations__grid">
        {SHOT_NAMES.map((name) => {
          const shot = shotForPoints(POINTS[name]);
          return (
            <section key={`${name}-${round}`} className={`card reveal reveal--${name}${reduced ? ' is-reduced' : ''}`} data-testid={`demo-${name}`}>
              <div className="reveal__stage">
                <ShotAnimation shot={shot} reduced={reduced} />
                <ShotLabel shot={shot} />
              </div>
              <p className="eyebrow">
                {name} · {shot.points} points · tier {shot.tier ?? 'none'}
              </p>
            </section>
          );
        })}
      </div>
    </main>
  );
}
