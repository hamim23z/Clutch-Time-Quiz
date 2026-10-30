import { useEffect, useLayoutEffect, useMemo, useRef, useState, type CSSProperties } from 'react';
import { RollingNumber } from '../components/RollingNumber';
import { useReducedMotion } from '../motion';
import type { ShotInfo, ShotName } from '../shots';
import beamUrl from '../assets/pixel/beam.png';
import ballUrl from '../assets/pixel/ball.png';
import courtUrl from '../assets/pixel/court_bare.png';
import crowdAUrl from '../assets/pixel/crowd_a.png';
import crowdBUrl from '../assets/pixel/crowd_b.png';
import dunkerUrl from '../assets/pixel/dunker.png';
import net0Url from '../assets/pixel/net_0.png';
import net1Url from '../assets/pixel/net_1.png';
import net2Url from '../assets/pixel/net_2.png';
import rimBackUrl from '../assets/pixel/rim_back.png';
import rimFrontUrl from '../assets/pixel/rim_front.png';
import shootUrl from '../assets/pixel/shooter_shoot.png';
import standUrl from '../assets/pixel/shooter_stand.png';
import { useCourtState } from './courtStore';
import { BALL, DUNK_AT, HOOP, IDLE_BALL, LOW, NEUTRAL, SPOTS, SPRITE, ballKeyframes, burstVectors, netKeyframes, stageLeft, stageScale } from './geometry';
import './court.css';

export const REPLAY_STEP_MS = 480; // one shot every 480 ms in the replay of a finished dive

export { burstVectors };

/** Where the net and the rim sit on the court, in game pixels (the same box as the sprites from tools/pixel/gen_pixel.py). */
const HOOP_BOX = { x: 74, y: 66, w: 24, h: 28 };
const FALLBACK_SCALE = 4;

/** A box in game pixels: the stage multiplies every one of these by the whole-number scale. */
const box = (x: number, y: number, w?: number, h?: number): CSSProperties =>
  ({ '--x': x, '--y': y, ...(w === undefined ? {} : { '--w': w }), ...(h === undefined ? {} : { '--h': h }) }) as CSSProperties;

/** The CSS custom properties that start a shot from its own spot on the floor. */
export function shotVars(name: ShotName): CSSProperties {
  const spot = SPOTS[name];
  return { '--sx': spot.x, '--sy': spot.y, '--nx': NEUTRAL.x, '--ny': NEUTRAL.y } as CSSProperties;
}

/** The scale and the position of the stage in its pane. Measured in the browser; a still default where nothing can be measured. */
function useStage(ref: React.RefObject<HTMLDivElement | null>): { k: number; left: number } {
  const [size, setSize] = useState<{ w: number; h: number } | null>(null);
  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return;
    const measure = (): void => {
      const w = el.clientWidth;
      const h = el.clientHeight;
      if (w > 0 && h > 0) setSize((s) => (s && s.w === w && s.h === h ? s : { w, h }));
    };
    measure();
    if (typeof ResizeObserver === 'undefined') return;
    const observer = new ResizeObserver(measure);
    observer.observe(el);
    return () => observer.disconnect();
  }, [ref]);
  if (!size) return { k: FALLBACK_SCALE, left: 0 };
  const k = stageScale(size.w, size.h);
  return { k, left: stageLeft(size.w, k) };
}

function Sprite({ src, className, style }: { src: string; className: string; style?: CSSProperties }) {
  return <img src={src} alt="" aria-hidden="true" draggable={false} className={`court__sprite ${className}`} style={style} />;
}

/** The ball, a 13 x 13 sprite. */
function Ball({ className, style }: { className: string; style?: CSSProperties }) {
  return <Sprite src={ballUrl} className={className} style={{ '--w': BALL, '--h': BALL, ...style } as CSSProperties} />;
}

/** The rim (two halves, so the ball passes between them) and the net (three frames) at the hoop. */
function Hoop({ name, made }: { name: ShotName | null; made: boolean }) {
  const size = { '--w': HOOP_BOX.w, '--h': HOOP_BOX.h } as CSSProperties;
  const at = box(HOOP_BOX.x, HOOP_BOX.y);
  return (
    <>
      <div className={`court__hoop court__hoop--back${name ? ` court__hoop--${name}` : ''}`} style={{ ...at, ...size }}>
        <Sprite src={rimBackUrl} className="court__rim court__rim--back" style={size} />
      </div>
      <div className={`court__hoop court__hoop--net${name ? ` court__hoop--${name}` : ''}${made ? ' is-made' : ''}`} style={{ ...at, ...size }}>
        <Sprite src={net0Url} className="court__net court__net--0" style={size} />
        <Sprite src={net1Url} className="court__net court__net--1" style={size} />
        <Sprite src={net2Url} className="court__net court__net--2" style={size} />
      </div>
      <div className={`court__hoop court__hoop--front${name ? ` court__hoop--${name}` : ''}`} style={{ ...at, ...size }}>
        <Sprite src={rimFrontUrl} className="court__rim court__rim--front" style={size} />
      </div>
    </>
  );
}

/** Backboard-side action: `shot` null is the idle state, a ball bouncing at centre court, or the shooter waiting with the ball. */
function Action({ shot, waiting, fast, reduced, skipped }: { shot: ShotInfo | null; waiting: boolean; fast: boolean; reduced: boolean; skipped: boolean }) {
  const name = shot?.name ?? null;
  const tier = shot?.tier == null ? 'miss' : `t${shot.tier}`;
  const made = name !== null && name !== 'airball' && name !== 'clank';
  const classes = ['court__action', name ? `court__action--${name}` : waiting ? 'court__action--waiting' : 'court__action--idle', name ? `court__action--${tier}` : '', fast ? 'is-fast' : '', skipped ? 'is-skipped' : '', reduced ? 'is-reduced' : ''].filter(Boolean).join(' ');
  const vars = name ? shotVars(name) : { '--nx': NEUTRAL.x, '--ny': NEUTRAL.y };
  const spriteBox = { '--w': SPRITE.width, '--h': SPRITE.height } as CSSProperties;
  const burst = useMemo(() => burstVectors(), []);
  const stillAt = name === 'airball' ? { x: 44, y: 134 } : name === 'clank' ? { x: 120, y: 116 } : { x: HOOP.x, y: 128 };
  return (
    <div className={classes} style={vars as CSSProperties}>
      <Hoop name={name} made={made && !reduced} />
      {/* the ball dribbling at centre court (home, archive, results) and its shadow */}
      {!name && !waiting && (
        <div className="court__idle" style={box(IDLE_BALL.x - 6, IDLE_BALL.y - 6, BALL, BALL)}>
          <span className="court__idle-shadow" />
          <Ball className="court__idle-bounce" />
        </div>
      )}
      {/* the shooter, waiting with the ball while a question is on */}
      {waiting && !name && (
        <div className="court__shooter court__shooter--waiting" style={{ ...box(NEUTRAL.x - 28, NEUTRAL.y - 76), ...spriteBox }}>
          <Sprite src={standUrl} className="court__pose" style={spriteBox} />
          <div className="court__dribble" style={box(36, 30, BALL, BALL)}>
            <Ball className="court__dribble-ball" />
          </div>
        </div>
      )}
      {name && (
        <div className={`court__shooter court__shooter--${name === 'dunk' ? 'dunk' : 'shot'}`} style={spriteBox}>
          <Sprite src={standUrl} className="court__pose court__pose--stand" style={spriteBox} />
          {name !== 'dunk' && <Sprite src={shootUrl} className="court__pose court__pose--shoot" style={spriteBox} />}
        </div>
      )}
      {name === 'dunk' && <Sprite src={dunkerUrl} className="court__dunker" style={{ ...box(DUNK_AT.x, DUNK_AT.y), ...spriteBox }} />}
      {name && !reduced && <Ball className="court__ball court__ball--shot" />}
      {name === 'dunk' && !reduced && (
        <div className="court__burst" style={box(HOOP.x, HOOP.y)}>
          {burst.map((v, i) => (
            <span key={i} className={`court__particle court__particle--${i % 3}`} style={{ '--dx': v.dx, '--dy': v.dy } as CSSProperties} />
          ))}
        </div>
      )}
      {/* reduced motion: no flight, a still ball at the end of the shot */}
      {name && reduced && <Ball className="court__still-ball" style={box(stillAt.x - 6, stillAt.y - 6)} />}
    </div>
  );
}

function Hud({ phase, headline, promptNumber, total, pointsBefore, points, diveNumber, clock, rollDelay, instant }: {
  phase: string; headline: string; promptNumber: number; total: number; pointsBefore: number; points: number; diveNumber: number | null; clock: number | null; rollDelay: number; instant: boolean;
}) {
  const urgent = clock !== null && clock <= 5;
  const counting = phase === 'prompt' || phase === 'shot';
  const results = phase === 'results';
  return (
    <>
      <div className="court__jumbo" style={box(36, 3, 100, 17)}>
        {counting || results ? (
          <div className="court__jumbo-text">
            <span className="court__cell">
              <span className="court__jumbo-label">{results ? 'DIVE' : 'PROMPT'}</span>
              <span className="court__jumbo-value">{results ? `#${diveNumber ?? ''}` : `${promptNumber} / ${total}`}</span>
            </span>
            <span className="court__cell court__cell--points">
              <span className="court__jumbo-label">{results ? 'FINAL' : 'POINTS'}</span>
              <span className="court__jumbo-value court__jumbo-value--points">
                <RollingNumber value={points} from={pointsBefore} delayMs={rollDelay} instant={instant} />
              </span>
            </span>
            <span className="court__cell">
              <span className="court__jumbo-label">{results ? 'OUT OF' : 'DIVE'}</span>
              <span className="court__jumbo-value">{results ? '700' : `#${diveNumber ?? ''}`}</span>
            </span>
          </div>
        ) : (
          <div className="court__jumbo-text court__jumbo-text--idle">
            <span className="court__jumbo-value court__jumbo-value--wide">{headline}</span>
            {diveNumber !== null && <span className="court__jumbo-label">DIVE #{diveNumber}</span>}
          </div>
        )}
      </div>
      <div className={`court__clock${urgent ? ' court__clock--danger' : ''}`} style={box(75, 21, 22, 7)}>
        <span className="court__clock-digits">{clock === null ? '25' : String(clock).padStart(2, '0')}</span>
      </div>
    </>
  );
}

/** What the court says about the shot, as a quick pop near the hoop. Decoration: the panel has the same words. */
function CourtLabel({ shot }: { shot: ShotInfo }) {
  const tier = shot.tier === null ? 'miss' : `t${shot.tier}`;
  return (
    <div className={`court__label court__label--${tier}`} aria-hidden="true">
      <span className="court__label-points">{shot.points}</span>
      <span className="court__label-name">{shot.tier === null ? shot.label : `T${shot.tier} ${shot.label}`}</span>
    </div>
  );
}

/**
 * The persistent court: a pixel picture shown at a whole-number scale. It is decoration (aria-hidden): the panel on the left
 * carries every word and number. It stays mounted as the player moves between screens, and draws whatever the court store says.
 */
export default function CourtScene() {
  const state = useCourtState();
  const reduced = useReducedMotion();
  const keyframes = useMemo(() => `${ballKeyframes()}\n\n${netKeyframes()}`, []);
  const root = useRef<HTMLDivElement>(null);
  const { k, left } = useStage(root);
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

  const classes = ['court', `court--${state.phase}`, shake ? 'court--shake' : '', replaying ? 'court--replaying' : '', reduced ? 'is-reduced' : '', state.skipped ? 'is-skipped' : ''].filter(Boolean).join(' ');
  const stage = { '--k': k, '--u': `${k}px`, width: LOW.width * k, height: LOW.height * k, left } as CSSProperties;
  return (
    <div ref={root} className={classes} aria-hidden="true" data-testid="court" data-phase={state.phase} data-shot={shot?.name ?? ''} data-scale={k}>
      <style>{keyframes}</style>
      <div className="court__stage" style={stage}>
        <img src={courtUrl} alt="" aria-hidden="true" draggable={false} className="court__sprite court__floor" style={{ '--w': LOW.width, '--h': LOW.height } as CSSProperties} />
        <div className="court__crowd" style={box(0, 6, LOW.width, 74)}>
          <Sprite src={crowdAUrl} className="court__crowd-frame court__crowd-frame--a" style={{ '--w': LOW.width, '--h': 74 } as CSSProperties} />
          <Sprite src={crowdBUrl} className="court__crowd-frame court__crowd-frame--b" style={{ '--w': LOW.width, '--h': 74 } as CSSProperties} />
        </div>
        <div className="court__lights" style={box(0, 0, LOW.width, 90)}>
          <Sprite src={beamUrl} className="court__beam court__beam--a" style={{ ...box(-4, 0, 60, 90) }} />
          <Sprite src={beamUrl} className="court__beam court__beam--b" style={{ ...box(116, 0, 60, 90) }} />
        </div>
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
        {flash && shot && !state.skipped && <div key={`f${shotKey}`} className="court__flash" style={box(0, 6, LOW.width, 74)} />}
        {shot && (state.phase === 'shot' || replaying) && <CourtLabel key={`l${shotKey}`} shot={shot} />}
      </div>
      <div className="court__scan" />
    </div>
  );
}
