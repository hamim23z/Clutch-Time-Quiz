import { useEffect, useMemo, type CSSProperties, type ReactElement } from 'react';
import { useReducedMotion } from '../motion';
import { TIERS, TIER_POINTS } from '../tiers';
import type { Tier } from '../types';
import { useChartState } from './chartStore';
import { AIRBALL_ZONE, BALL_REST, BANDS, COURT, HOOP, MARKER, TIER_COLORS, TIER_INK, VIEW, layoutMarks, type Placed } from './placement';
import './chart.css';

/** One shot every 480 ms when the results screen replays the dive (the squares on the left appear in step). */
export const REPLAY_STEP_MS = 480;

/** How long the ball is in the air, and how much it is worth showing: a rarer tier flies longer and higher. */
export const flightMs = (tier: Tier | null): number => (tier === null ? 900 : 520 + tier * 70);

const CREAM = '#F4EAD6';
const GREY = '#3A3A3A';
const LINE = { stroke: CREAM, strokeWidth: 3, strokeLinecap: 'square', fill: 'none' } as const;
/** Very dark warm tones, from the zone nearest the basket (warmest) to the deepest. */
const ZONE_TONES: Record<Tier, string> = { 1: '#3A210F', 2: '#2E1B0C', 3: '#241509', 4: '#1B1008', 5: '#140C07', 6: '#0F0905' };
const OUTER: Tier[] = [6, 5, 4, 3, 2, 1];
const circlePath = (cx: number, cy: number, r: number): string => `M${cx - r} ${cy}a${r} ${r} 0 1 0 ${2 * r} 0a${r} ${r} 0 1 0 ${-2 * r} 0Z`;
/** The ring between two radii around the hoop (a plain disc when the inner one is 0). */
const ring = (r0: number, r1: number): string => `${circlePath(HOOP.x, HOOP.y, r1)}${r0 > 0 ? circlePath(HOOP.x, HOOP.y, r0) : ''}`;

function Ball({ className, transform }: { className?: string; transform?: string }) {
  return (
    <g className={className} transform={transform}>
      <circle r="11" fill="#FF6A13" stroke="#0A0A0A" strokeWidth="2" />
      <path d="M-11 0H11M0-11V11M-7.8-7.8Q0 0-7.8 7.8M7.8-7.8Q0 0 7.8 7.8" fill="none" stroke="#0A0A0A" strokeWidth="1.6" />
    </g>
  );
}

function Court() {
  return (
    <>
      <defs>
        <clipPath id="chart-court">
          <rect x={COURT.x} y={COURT.y} width={COURT.w} height={COURT.h} />
        </clipPath>
      </defs>
      <g clipPath="url(#chart-court)">
        <rect x={COURT.x} y={COURT.y} width={COURT.w} height={COURT.h} fill={ZONE_TONES[6]} />
        {OUTER.slice(1).map((t) => (
          <circle key={t} cx={HOOP.x} cy={HOOP.y} r={BANDS[t][0]} fill={ZONE_TONES[t]} />
        ))}
        {[...OUTER].map((t) => (
          <circle key={`r${t}`} cx={HOOP.x} cy={HOOP.y} r={BANDS[t][1]} fill="none" stroke="#6E6E6E" strokeWidth="1.5" strokeDasharray="6 7" opacity="0.7" />
        ))}
      </g>
      <g {...LINE}>
        <rect x={COURT.x} y={COURT.y} width={COURT.w} height={COURT.h} />
        <rect x="286.4" y="104" width="179.2" height="212.8" />
        <path d="M308.8 316.8A67.2 67.2 0 0 1 443.2 316.8" />
        <path d="M308.8 316.8A67.2 67.2 0 0 0 443.2 316.8" strokeDasharray="10 9" />
        <path d="M331.2 162.8A44.8 44.8 0 0 0 420.8 162.8" />
        <path d="M129.6 104V263A266 266 0 0 0 622.4 263V104" />
        <path d="M308.8 630.4A67.2 67.2 0 0 1 443.2 630.4" />
      </g>
      <line x1="342.4" y1="148.8" x2="409.6" y2="148.8" stroke={CREAM} strokeWidth="5" strokeLinecap="square" />
      <circle cx={HOOP.x} cy={HOOP.y} r="8.4" fill="none" stroke="#FF6A13" strokeWidth="3.5" />
    </>
  );
}

/** The depth gauge on the left: a tick at every zone boundary, and each tier's square with its points. */
function Gauge() {
  const y = (d: number): number => HOOP.y + d;
  const ticks = [0, ...TIERS.map((t) => BANDS[t][1])];
  return (
    <g className="chart__gauge">
      <line x1="84" y1={y(0)} x2="84" y2={y(BANDS[6][1])} stroke="#6E6E6E" strokeWidth="2" />
      {ticks.map((d) => (
        <line key={d} x1="78" y1={y(d)} x2="90" y2={y(d)} stroke={CREAM} strokeWidth="2" />
      ))}
      {TIERS.map((t) => {
        const mid = y((BANDS[t][0] + BANDS[t][1]) / 2);
        return (
          <g key={t} data-tier={t}>
            <g className="chart__chipg">
              <rect x="26" y={mid - 12} width="24" height="24" fill={TIER_COLORS[t]} />
              <text x="38" y={mid} className="chart__chip" fill={TIER_INK[t]}>{t}</text>
            </g>
            <text x="56" y={mid + 5} className="chart__gauge-points">{TIER_POINTS[t]}</text>
          </g>
        );
      })}
    </g>
  );
}

function Marker({ p, tierColor, ring: ringed }: { p: Placed; tierColor: string; ring: boolean }) {
  const made = p.tier !== null;
  return (
    <g className="chart__pop">
      {ringed && <circle className="chart__ring" r="26" fill="none" stroke={CREAM} strokeWidth="2.5" strokeDasharray="5 5" />}
      <rect className="chart__sq chart__sq--shadow" x={-MARKER / 2 + 3} y={-MARKER / 2 + 3} width={MARKER} height={MARKER} fill="#000" />
      <rect className="chart__sq" x={-MARKER / 2} y={-MARKER / 2} width={MARKER} height={MARKER} fill={tierColor} />
      {made ? (
        <text className="chart__num" fill={TIER_INK[p.tier as Tier]}>{p.tier}</text>
      ) : (
        <path className="chart__x" d="M-6-6L6 6M6-6L-6 6" stroke="#FFFFFF" strokeWidth="3" strokeLinecap="square" />
      )}
    </g>
  );
}

/** What the right-hand side shows. Decoration (aria-hidden): the panel on the left carries every word and number. */
export default function ShotChart() {
  const state = useChartState();
  const reduced = useReducedMotion();
  const placed = useMemo(() => layoutMarks(state.marks, state.diveNumber ?? 0), [state.marks, state.diveNumber]);
  const shooting = state.phase === 'shot' && placed.length > 0;
  const replaying = state.phase === 'results';
  const latest = placed.length - 1;
  const last = shooting ? placed[latest] : undefined;
  const lastTier = last?.tier ?? null;
  const dur = flightMs(lastTier);
  const made = placed.filter((p) => p.tier !== null);
  const best = made.reduce<Tier | null>((b, p) => (b === null || (p.tier as Tier) > b ? (p.tier as Tier) : b), null);
  const animate = !reduced && !state.skipped;
  const flash = shooting && lastTier !== null ? TIER_COLORS[lastTier] : null;

  const live = shooting && last
    ? last.tier === null ? `Airball, 0 points, ${state.points} total` : `Tier ${last.tier}, ${TIER_POINTS[last.tier]} points, ${state.points} total`
    : '';

  // On a phone the chart is above the panel. When a result or the results screen appears (the panel moves focus to its heading, which
  // scrolls the page down), bring the chart back into view, so the shot is never played out of sight.
  const showing = shooting || replaying;
  useEffect(() => {
    if (!showing || typeof window === 'undefined' || typeof window.matchMedia !== 'function' || !window.matchMedia('(max-width: 899px)').matches) return;
    const id = setTimeout(() => window.scrollTo?.({ top: 0 }), 0);
    return () => clearTimeout(id);
  }, [showing, state.shotKey, state.replayKey]);

  const classes = ['chart', `chart--${state.phase}`, reduced ? 'is-reduced' : '', state.skipped ? 'is-skipped' : ''].filter(Boolean).join(' ');
  const idleTitle = state.headline === 'NBA DEEP CUT' && state.diveNumber !== null ? `TODAY'S DIVE #${state.diveNumber}` : state.headline;
  const idleSub = state.headline === 'NBA DEEP CUT' && state.diveNumber !== null ? '7 PROMPTS' : null;

  const marks: ReactElement[] = placed.map((p, i) => {
    const isShot = shooting && i === latest;
    const color = p.tier === null ? '#6E6E6E' : TIER_COLORS[p.tier];
    const delay = isShot ? (animate ? flightMs(p.tier) : 0) : replaying ? (animate ? i * REPLAY_STEP_MS : 0) : 0;
    const motion = isShot || replaying;
    const vars = { '--delay': `${delay}ms`, '--peak': 1.1 + (p.tier ?? 0) * 0.04 } as CSSProperties;
    return (
      <g key={`${p.id}-${motion ? (isShot ? state.shotKey : state.replayKey) : 'still'}`} className={`chart__mark${motion ? ' chart__mark--in' : ''}`} style={vars} data-tier={p.tier ?? 'miss'}>
        {p.tier !== null && <line className="chart__spoke" x1={HOOP.x} y1={HOOP.y} x2={p.x} y2={p.y} stroke="#A8A8A8" strokeWidth="2" strokeDasharray="6 6" />}
        <g transform={`translate(${p.x} ${p.y})`}>
          <Marker p={p} tierColor={color} ring={isShot} />
        </g>
      </g>
    );
  });

  let ball: ReactElement | null = null;
  if (shooting && last && animate) {
    const dx = last.x - BALL_REST.x;
    const dy = last.y - BALL_REST.y;
    const apex = last.tier === null ? 90 : Math.max(-dy, 0) + 50 + 8 * last.tier;
    ball = (
      <g key={`b${state.shotKey}`} transform={`translate(${BALL_REST.x} ${BALL_REST.y})`}>
        <g className="chart__out" style={{ '--dur': `${dur}ms` } as CSSProperties}>
          <g className={`chart__fly-x${last.tier === null ? ' chart__fly-x--miss' : ''}`} style={{ '--dur': `${dur}ms`, '--dx': dx } as CSSProperties}>
            <g className={`chart__fly-y${last.tier === null ? ' chart__fly-y--miss' : ''}`} style={{ '--dur': `${dur}ms`, '--dy': dy, '--apex': apex } as CSSProperties}>
              <Ball />
            </g>
          </g>
        </g>
      </g>
    );
  }
  const restHidden = shooting && animate;

  return (
    <div className={classes} data-testid="chart" data-phase={state.phase} data-tier={shooting ? (lastTier ?? 'miss') : ''}>
      <svg className="chart__svg" viewBox={`0 0 ${VIEW.width} ${VIEW.height}`} aria-hidden="true" focusable="false" role="presentation">
        <rect width={VIEW.width} height={VIEW.height} fill="#060606" />
        <text x="96" y="40" className="chart__title">SHOT CHART</text>
        <text x="96" y="72" className="chart__tagline">Rarer answer = deeper shot.</text>

        <Court />
        {shooting && lastTier !== null && animate && (
          <path key={`p${state.shotKey}`} className="chart__pulse" clipPath="url(#chart-court)" fillRule="evenodd" d={ring(BANDS[lastTier][0], BANDS[lastTier][1])} fill={TIER_COLORS[lastTier]} style={{ '--delay': `${dur}ms` } as CSSProperties} />
        )}
        <Gauge />

        <g className="chart__airball">
          <rect x={AIRBALL_ZONE.x} y={AIRBALL_ZONE.y} width={AIRBALL_ZONE.w} height={AIRBALL_ZONE.h} fill="none" stroke="#6E6E6E" strokeWidth="2" strokeDasharray="8 8" />
          <text x={AIRBALL_ZONE.x + AIRBALL_ZONE.w / 2} y={AIRBALL_ZONE.y + 24} className="chart__zone-label">AIRBALL ZONE</text>
        </g>

        {marks}
        <g className={restHidden ? 'chart__rest chart__rest--late' : 'chart__rest'} style={{ '--delay': `${dur + 150}ms` } as CSSProperties}>
          <Ball transform={`translate(${BALL_REST.x} ${BALL_REST.y})`} />
        </g>
        {ball}

        {shooting && lastTier === 6 && animate && (
          <g key={`h${state.shotKey}`} style={{ '--delay': `${dur}ms` } as CSSProperties}>
            <rect className="chart__heat" x={COURT.x} y={COURT.y} width={COURT.w} height={COURT.h} fill="#FFFFFF" />
            <g transform="translate(376 386) rotate(-8)">
              <g className="chart__stamp">
                <rect x="-132" y="-27" width="264" height="54" fill="#0A0A0A" stroke="#FF3B1F" strokeWidth="5" />
                <text className="chart__stamp-text">DEEP CUT</text>
              </g>
            </g>
          </g>
        )}

        {state.phase === 'idle' && (
          <g className="chart__idle">
            <rect x="170" y="352" width="412" height={idleSub ? 96 : 70} fill="#0A0A0A" />
            <rect x="170" y="352" width="412" height={idleSub ? 96 : 70} fill="none" stroke="#FF6A13" strokeWidth="4" />
            <text x="376" y={idleSub ? 394 : 394} className="chart__idle-title">{idleTitle}</text>
            {idleSub && <text x="376" y="428" className="chart__idle-sub">{idleSub}</text>}
          </g>
        )}

        <g className="chart__readouts">
          <g>
            <rect x="500" y="16" width="72" height="68" fill="#0A0A0A" stroke={GREY} strokeWidth="2" />
            <text x="536" y="36" className="chart__label">CLOCK</text>
            <text x="536" y="72" className={`chart__value${state.clock !== null && state.clock <= 5 ? ' chart__value--danger' : ''}`} data-testid="chart-clock">{state.clock === null ? '--' : String(state.clock).padStart(2, '0')}</text>
          </g>
          <g>
            <rect x="584" y="16" width="72" height="68" fill="#0A0A0A" stroke={GREY} strokeWidth="2" />
            {flash && animate && <rect key={`f${state.shotKey}`} className="chart__pts-flash" x="585" y="17" width="70" height="66" fill={flash} style={{ '--delay': `${dur}ms` } as CSSProperties} />}
            <text x="620" y="36" className="chart__label">PTS</text>
            <text x="620" y="72" className="chart__value chart__value--points" data-testid="chart-points">{state.points}</text>
          </g>
        </g>

        <g className="chart__strip">
          {[
            { x: 96, label: 'SHOTS', value: `${made.length} / ${placed.length}` },
            { x: 288, label: 'POINTS', value: String(state.points) },
            { x: 480, label: 'BEST SHOT', value: best === null ? '-' : `T${best} · ${TIER_POINTS[best]}` },
          ].map((b) => (
            <g key={b.label}>
              <rect x={b.x} y="772" width="176" height="76" fill="#0A0A0A" stroke={GREY} strokeWidth="2" />
              <text x={b.x + 14} y="798" className="chart__label chart__label--left">{b.label}</text>
              <text x={b.x + 14} y="836" className="chart__value chart__value--strip" data-testid={`chart-strip-${b.label.toLowerCase().replace(' ', '-')}`}>{b.value}</text>
              {b.label === 'BEST SHOT' && best !== null && <rect x={b.x + 150} y="812" width="14" height="14" fill={TIER_COLORS[best]} />}
            </g>
          ))}
        </g>
      </svg>
      <p className="visually-hidden" aria-live="polite" data-testid="chart-live">{live}</p>
    </div>
  );
}
