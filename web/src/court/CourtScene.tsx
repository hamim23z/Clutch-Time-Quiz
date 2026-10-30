import { useEffect, useMemo, useRef, useState, type CSSProperties } from 'react';
import { RollingNumber } from '../components/RollingNumber';
import { useReducedMotion } from '../motion';
import type { ShotInfo, ShotName } from '../shots';
import { Arena, Crowd, Floor, FloorGlow, Lights } from './art';
import { useCourtState } from './courtStore';
import { HOOP, NEUTRAL, SPOTS, VIEWBOX, ballKeyframes, depthScale, hand, shooterKeyframes } from './geometry';
import './court.css';

export const REPLAY_STEP_MS = 480; // one shot every 480 ms in the replay of a finished dive
const PARTICLES = 28; // capped (the brief says about 40)

/** Directions of the dunk's burst, spread evenly round the rim with a fixed jitter. */
export function burstVectors(count = PARTICLES): Array<{ dx: number; dy: number; r: number }> {
  return Array.from({ length: Math.min(count, PARTICLES) }, (_, i) => {
    const angle = (i / count) * Math.PI * 2 + (i % 3) * 0.17;
    const reach = 44 + ((i * 37) % 40);
    return { dx: Math.round(Math.cos(angle) * reach), dy: Math.round(Math.sin(angle) * reach * 0.8 - 14), r: 2.2 + (i % 3) * 1.2 };
  });
}

/** The CSS custom properties that start a shot from its own spot on the floor. */
export function shotVars(name: ShotName): CSSProperties {
  const spot = SPOTS[name];
  const release = hand(spot);
  return {
    '--sx': `${spot.x}px`, '--sy': `${spot.y}px`, '--ss': depthScale(spot.y),
    '--nx': `${NEUTRAL.x}px`, '--ny': `${NEUTRAL.y}px`, '--ns': depthScale(NEUTRAL.y),
    '--bx': `${release.x}px`, '--by': `${release.y}px`, '--bs': release.s,
  } as CSSProperties;
}

/** The ball's starting hand position for the neutral spot, used by the ball keyframes before the shooter reaches his spot. */
function ballVars(name: ShotName): CSSProperties {
  const n = hand(NEUTRAL);
  return { ...shotVars(name), '--nx': `${n.x}px`, '--ny': `${n.y}px`, '--ns': n.s } as CSSProperties;
}

function Shooter() {
  return (
    <g className="court__shooter-fig">
      <path d="M-9 -34 L-10 0 M9 -34 L11 -2" className="court__legs" />
      <path d="M-13 -74 Q0 -80 13 -74 L10 -34 L-10 -34 Z" className="court__body" />
      <circle cx="1" cy="-86" r="9" className="court__body" />
      <path d="M-12 -70 L-2 -90 M12 -70 L8 -88" className="court__arms" />
    </g>
  );
}

function Ball({ vars, className }: { vars?: CSSProperties; className: string }) {
  return (
    <g className={className} style={vars}>
      <circle r="13" className="court__ball-body" />
      <path d="M-13 0H13M0-13V13M-9.2-9.2Q0 0-9.2 9.2M9.2-9.2Q0 0 9.2 9.2" className="court__ball-seams" />
    </g>
  );
}

function Net() {
  return (
    <g className="court__net">
      <path d="M376 260 L387 306 M386 260 L393 306 M396 260 L398 306 M404 260 L402 306 M414 260 L407 306 M424 260 L413 306 M381 276 H419 M385 290 H415 M388 302 H412" className="court__net-lines" />
    </g>
  );
}

/** Backboard, rim, net, shooter and ball. `shot` null is the idle state: a ball bouncing at centre court, or the shooter waiting. */
function Action({ shot, waiting, fast, reduced, skipped }: { shot: ShotInfo | null; waiting: boolean; fast: boolean; reduced: boolean; skipped: boolean }) {
  const name = shot?.name ?? null;
  const tier = shot?.tier == null ? 'miss' : `t${shot.tier}`;
  const classes = ['court__action', name ? `court__action--${name}` : waiting ? 'court__action--waiting' : 'court__action--idle', name ? `court__action--${tier}` : '', fast ? 'is-fast' : '', skipped ? 'is-skipped' : '', reduced ? 'is-reduced' : ''].filter(Boolean).join(' ');
  const vars = name ? ballVars(name) : undefined;
  return (
    <svg className="court__layer court__action-layer" viewBox={VIEWBOX} preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">
      <g className={classes} style={vars}>
        <g className="court__board">
          <rect x="330" y="180" width="140" height="76" rx="3" className="court__board-body" />
          <rect x="372" y="212" width="56" height="38" className="court__square" />
          <rect x="395" y="250" width="10" height="9" className="court__bracket" />
        </g>
        <g className="court__rim">
          <path d="M374 258 A26 6.5 0 0 1 426 258" className="court__rim-back" />
        </g>
        {name && !reduced ? <Ball vars={vars} className="court__ball court__ball--shot" /> : null}
        <Net />
        <g className="court__rim court__rim--front">
          <path d="M374 258 A26 6.5 0 0 0 426 258" className="court__rim-front" />
        </g>
        {/* the ball dribbling at centre court (home, archive, results) and its shadow */}
        {!name && !waiting && (
          <g className="court__idle-ball" transform={`translate(${HOOP.x} 585)`}>
            <ellipse className="court__idle-shadow" cx="0" cy="14" rx="16" ry="4.5" />
            <g className="court__idle-bounce">
              <circle r="15" className="court__ball-body" />
              <path d="M-15 0H15M0-15V15M-10.6-10.6Q0 0-10.6 10.6M10.6-10.6Q0 0 10.6 10.6" className="court__ball-seams" />
            </g>
          </g>
        )}
        {/* the shooter, waiting with the ball while a question is on */}
        {waiting && !name && (
          <g className="court__shooter court__shooter--waiting" style={{ transform: `translate(${NEUTRAL.x}px, ${NEUTRAL.y}px) scale(${depthScale(NEUTRAL.y)})` }}>
            <Shooter />
            <g className="court__dribble" transform="translate(16 -26)">
              <circle r="12" className="court__ball-body" />
              <path d="M-12 0H12M0-12V12" className="court__ball-seams" />
            </g>
          </g>
        )}
        {name && (
          <g className={`court__shooter court__shooter--${name === 'dunk' ? 'dunk' : 'shot'}`}>
            <Shooter />
          </g>
        )}
        {name === 'dunk' && !reduced && (
          <g transform={`translate(${HOOP.x} ${HOOP.y})`}>
            {burstVectors().map((v, i) => (
              <circle key={i} r={v.r} className="court__particle" style={{ '--dx': `${v.dx}px`, '--dy': `${v.dy}px` } as CSSProperties} />
            ))}
          </g>
        )}
        {/* reduced motion: no flight, a still ball at the end of the shot */}
        {name && reduced && (
          <g className="court__still-ball" transform={name === 'airball' ? 'translate(300 560)' : name === 'clank' ? 'translate(560 360)' : `translate(${HOOP.x} 330)`}>
            <circle r="11" className="court__ball-body" />
          </g>
        )}
      </g>
    </svg>
  );
}

function Hud({ phase, headline, promptNumber, total, pointsBefore, points, diveNumber, clock, rollDelay, instant }: {
  phase: string; headline: string; promptNumber: number; total: number; pointsBefore: number; points: number; diveNumber: number | null; clock: number | null; rollDelay: number; instant: boolean;
}) {
  const urgent = clock !== null && clock <= 5;
  const counting = phase === 'prompt' || phase === 'shot';
  return (
    <svg className="court__layer court__hud" viewBox={VIEWBOX} preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">
      <g className="court__cables">
        <line x1="300" y1="0" x2="318" y2="46" />
        <line x1="500" y1="0" x2="482" y2="46" />
      </g>
      <rect x="236" y="44" width="328" height="94" rx="11" className="court__jumbo" />
      <rect x="244" y="52" width="312" height="78" rx="7" className="court__jumbo-screen" />
      {counting || phase === 'results' ? (
        <g className="court__jumbo-text">
          <text x="306" y="74" className="court__jumbo-label">{phase === 'results' ? 'DIVE' : 'PROMPT'}</text>
          <text x="306" y="112" className="court__jumbo-value">{phase === 'results' ? `#${diveNumber ?? ''}` : `${promptNumber} / ${total}`}</text>
          <text x="400" y="74" className="court__jumbo-label">{phase === 'results' ? 'FINAL' : 'POINTS'}</text>
          <text x="400" y="112" className="court__jumbo-value court__jumbo-value--points">
            <RollingNumber value={points} from={pointsBefore} delayMs={rollDelay} instant={instant} />
          </text>
          <text x="494" y="74" className="court__jumbo-label">{phase === 'results' ? 'OUT OF' : 'DIVE'}</text>
          <text x="494" y="112" className="court__jumbo-value">{phase === 'results' ? '700' : `#${diveNumber ?? ''}`}</text>
        </g>
      ) : (
        <g className="court__jumbo-text">
          <text x="400" y="94" className="court__jumbo-value court__jumbo-value--wide">{headline}</text>
          {diveNumber !== null && <text x="400" y="118" className="court__jumbo-label">DIVE #{diveNumber}</text>}
        </g>
      )}
      <g className={`court__clock${urgent ? ' court__clock--danger' : ''}`}>
        <rect x="364" y="146" width="72" height="30" rx="5" className="court__clock-box" />
        <text x="400" y="170" className="court__clock-digits">{clock === null ? '25' : String(clock).padStart(2, '0')}</text>
      </g>
    </svg>
  );
}

/** What the court says about the shot, as a quick pop near the hoop. Decoration: the panel has the same words. */
function CourtLabel({ shot }: { shot: ShotInfo }) {
  const tier = shot.tier === null ? 'miss' : `t${shot.tier}`;
  return (
    <div className={`court__label court__label--${tier}`} aria-hidden="true">
      <span className="court__label-points">{shot.points}</span>
      <span className="court__label-name">{shot.label}</span>
    </div>
  );
}

/**
 * The persistent court. It is decoration (aria-hidden): the panel on the left carries every word and number. It stays mounted
 * as the player moves between screens, and draws whatever the court store says.
 */
export default function CourtScene() {
  const state = useCourtState();
  const reduced = useReducedMotion();
  const keyframes = useMemo(() => `${ballKeyframes()}\n\n${shooterKeyframes()}`, []);
  const [replayIndex, setReplayIndex] = useState(-1);
  const pointsBefore = useRef(0);
  const lastPoints = useRef(0);

  // the replay of a finished dive: one shot after another, fast
  useEffect(() => {
    if (state.phase !== 'results' || !state.replay) {
      setReplayIndex(-1);
      return;
    }
    if (reduced || state.skipped) {
      setReplayIndex(state.replay.length);
      return;
    }
    setReplayIndex(0);
    const timers: ReturnType<typeof setTimeout>[] = [];
    for (let i = 1; i <= state.replay.length; i++) timers.push(setTimeout(() => setReplayIndex(i), i * REPLAY_STEP_MS));
    return () => timers.forEach(clearTimeout);
  }, [state.phase, state.replay, state.replayKey, state.skipped, reduced]);

  const replaying = state.phase === 'results' && state.replay !== null && replayIndex >= 0 && replayIndex < state.replay.length;
  const shot: ShotInfo | null = replaying ? (state.replay as ShotInfo[])[replayIndex] ?? null : state.phase === 'shot' ? state.shot : null;
  const replayPoints = state.replay ? state.replay.slice(0, Math.min(replayIndex + 1, state.replay.length)).reduce((s, x) => s + x.points, 0) : 0;
  const displayPoints = state.phase === 'results' ? (replayIndex >= (state.replay?.length ?? 0) ? state.points : replayPoints) : state.points;
  if (state.points !== lastPoints.current) {
    pointsBefore.current = lastPoints.current;
    lastPoints.current = state.points;
  }
  const shake = shot?.name === 'dunk' && !reduced && !state.skipped && !replaying;
  const flash = (shot?.name === 'deep-swish' || shot?.name === 'dunk') && !reduced && !replaying;
  const shotKey = replaying ? `r${state.replayKey}-${replayIndex}` : `s${state.shotKey}`;

  const classes = ['court', `court--${state.phase}`, shake ? 'court--shake' : '', reduced ? 'is-reduced' : '', state.skipped ? 'is-skipped' : ''].filter(Boolean).join(' ');
  return (
    <div className={classes} aria-hidden="true" data-testid="court" data-phase={state.phase} data-shot={shot?.name ?? ''}>
      <style>{keyframes}</style>
      <Arena />
      <Crowd />
      <Lights />
      <Floor />
      <FloorGlow />
      <Hud
        phase={state.phase}
        headline={state.headline}
        promptNumber={state.promptNumber}
        total={state.total}
        pointsBefore={state.phase === 'results' ? 0 : pointsBefore.current}
        points={displayPoints}
        diveNumber={state.diveNumber}
        clock={state.phase === 'prompt' ? state.clock : null}
        rollDelay={reduced || state.skipped || state.phase === 'results' ? 0 : 950}
        instant={reduced || state.skipped || state.phase === 'prompt' || state.phase === 'idle' || state.phase === 'results'}
      />
      <Action key={shotKey} shot={shot} waiting={state.phase === 'prompt'} fast={replaying} reduced={reduced} skipped={state.skipped && !replaying} />
      {flash && shot && !state.skipped && <div key={`f${shotKey}`} className="court__flash" />}
      {shot && (state.phase === 'shot' || replaying) && <CourtLabel key={`l${shotKey}`} shot={shot} />}
      <div className="court__vignette" />
    </div>
  );
}

