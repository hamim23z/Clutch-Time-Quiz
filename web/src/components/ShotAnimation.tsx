import type { CSSProperties } from 'react';
import type { ShotInfo } from '../shots';

interface Props {
  shot: ShotInfo;
  /** Reduced motion: no ball, no particles, no crowd: a still hoop that fades in. */
  reduced?: boolean;
  /** Jump to the end at once (the player tapped or pressed Enter). */
  skipped?: boolean;
}

export const MAX_PARTICLES = 28; // the dunk's burst; the brief caps particles at about 40

/** Particle directions: spread evenly round the hoop with a deterministic jitter, so a replay looks the same. */
export function particleStyles(count = MAX_PARTICLES): CSSProperties[] {
  return Array.from({ length: Math.min(count, MAX_PARTICLES) }, (_, i) => {
    const angle = (i / count) * Math.PI * 2 + (i % 3) * 0.17;
    const reach = 46 + ((i * 37) % 38);
    return { '--dx': `${Math.round(Math.cos(angle) * reach)}px`, '--dy': `${Math.round(Math.sin(angle) * reach - 14)}px`, '--size': `${4 + (i % 3) * 2}px` } as CSSProperties;
  });
}

function Ball() {
  return (
    <g className="shot__ball">
      <circle r="9" className="shot__ball-body" />
      <path d="M-9 0H9M0-9V9M-6.4-6.4Q0 0-6.4 6.4M6.4-6.4Q0 0 6.4 6.4" className="shot__ball-seams" />
    </g>
  );
}

function Player() {
  // A plain geometric figure: no real person, no kit, no number.
  return (
    <g className="shot__player">
      <circle cx="0" cy="-30" r="7" />
      <rect x="-7" y="-22" width="14" height="26" rx="6" />
      <path d="M5-18L18-38" className="shot__arm" />
      <path d="M-4 4L-12 28M4 4L12 26" className="shot__legs" />
    </g>
  );
}

/**
 * One basketball shot for an outcome, drawn in SVG and moved with CSS transforms only. The tier decides which shot:
 * airball, clank, rattle, bank, swish, deep swish or slam dunk (see shots.ts). It is decoration; the result is also in the page text.
 */
export function ShotAnimation({ shot, reduced = false, skipped = false }: Props) {
  const tier = shot.tier === null ? 'miss' : `t${shot.tier}`;
  const classes = ['shot', `shot--${shot.name}`, `shot--${tier}`, reduced ? 'is-reduced' : '', skipped ? 'is-skipped' : ''].filter(Boolean).join(' ');
  return (
    <div className={classes} data-shot={shot.name} aria-hidden="true">
      {!reduced && shot.name === 'deep-swish' && <div className="shot__crowd" />}
      <svg className="shot__svg" viewBox="0 0 300 200" focusable="false">
        <line x1="0" y1="192" x2="300" y2="192" className="shot__floor" />
        <g className="shot__board">
          <rect x="252" y="28" width="8" height="86" rx="2" className="shot__board-body" />
          <rect x="249" y="62" width="3" height="28" className="shot__square" />
        </g>
        <g className="shot__rim">
          <line x1="214" y1="100" x2="252" y2="100" className="shot__rim-bar" />
          <circle cx="214" cy="100" r="3.2" className="shot__rim-front" />
        </g>
        <g className="shot__net">
          <path d="M216 102L224 140M224 102L228 140M232 102V140M240 102L236 140M248 102L240 140M219 114H245M222 126H242M225 138H239" className="shot__net-lines" />
        </g>
        {!reduced && shot.name === 'dunk' && <Player />}
        {!reduced && <Ball />}
      </svg>
      {!reduced && shot.name === 'dunk' && (
        <div className="shot__burst">
          {particleStyles().map((style, i) => (
            <span key={i} className="particle" style={style} />
          ))}
        </div>
      )}
    </div>
  );
}
