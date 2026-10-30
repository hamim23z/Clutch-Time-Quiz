import type { ShotName } from '../shots';

/**
 * The court is a pixel picture, drawn once at 172 x 215 "game pixels" (tools/pixel/gen_pixel.py) and shown at a whole-number
 * scale k: every game pixel is k x k screen pixels. All the numbers below are in game pixels.
 */
export const LOW = { width: 172, height: 215 };
/** The generated pictures are 4 times the game size. */
export const ART_SCALE = 4;
/** The rows from the top that every shot happens in. The stage is sized so at least this many rows are on screen. */
export const ROWS_VISIBLE = 142;
export const SPRITE = { width: 56, height: 76 };
export const BALL = 13;

/** The whole-number scale for a pane of this size: as wide as the pane allows, and no bigger than the height allows. */
export function stageScale(paneWidth: number, paneHeight: number): number {
  const byWidth = Math.round(paneWidth / LOW.width);
  const byHeight = Math.floor(paneHeight / ROWS_VISIBLE);
  return Math.max(1, Math.min(byWidth, byHeight, 8));
}

/** Where the stage's left edge goes in a pane (a whole number of screen pixels; negative crops both sides evenly). */
export function stageLeft(paneWidth: number, scale: number): number {
  return Math.floor((paneWidth - LOW.width * scale) / 2);
}

export const HOOP = { x: 86, y: 70 }; // the middle of the rim opening
export const NEUTRAL = { x: 86, y: 138 }; // where the shooter waits while a question is on
export const IDLE_BALL = { x: 86, y: 132 };

/** Where the shooter's feet are for each shot. Low points are close to the hoop, deep cuts are far out. */
export const SPOTS: Record<ShotName, { x: number; y: number }> = {
  airball: { x: 128, y: 120 },
  clank: { x: 112, y: 108 },
  rattle: { x: 58, y: 116 },
  bank: { x: 40, y: 122 },
  swish: { x: 136, y: 128 },
  'deep-swish': { x: 36, y: 140 },
  dunk: { x: 64, y: 118 },
};

/** Where the dunker sprite hangs: its hand is on the rim. */
export const DUNK_AT = { x: 44, y: 57 };

interface Waypoint {
  /** 0 to 1 along the flight (after the release). */
  t: number;
  x: number;
  y: number;
}

interface Flight {
  points: Waypoint[];
  /** When the ball goes through the rim, 0 to 1 along the flight (made shots only). */
  pass?: number;
  /** When the ball hits the rim or the board. */
  hits: number[];
}

const START: Waypoint = { t: 0, x: NaN, y: NaN };

/** The ball's flight after it leaves the hands, for each shot (centre of the ball). The first point is the release itself. */
export const FLIGHT: Record<Exclude<ShotName, 'dunk'>, Flight> = {
  airball: {
    hits: [],
    points: [START, { t: 0.38, x: 62, y: 22 }, { t: 0.7, x: 40, y: 96 }, { t: 1, x: 30, y: 208 }],
  },
  clank: {
    hits: [0.42],
    points: [START, { t: 0.3, x: 90, y: 36 }, { t: 0.42, x: 98, y: 66 }, { t: 0.6, x: 124, y: 26 }, { t: 0.82, x: 150, y: 96 }, { t: 1, x: 162, y: 208 }],
  },
  rattle: {
    hits: [0.4, 0.62],
    points: [
      START, { t: 0.3, x: 86, y: 40 }, { t: 0.4, x: 96, y: 64 }, { t: 0.5, x: 84, y: 54 },
      { t: 0.62, x: 76, y: 64 }, { t: 0.72, x: 88, y: 58 }, { t: 0.8, x: 86, y: 72 }, { t: 1, x: 86, y: 128 },
    ],
    pass: 0.8,
  },
  bank: {
    hits: [0.36],
    points: [START, { t: 0.2, x: 82, y: 40 }, { t: 0.36, x: 86, y: 50 }, { t: 0.52, x: 86, y: 62 }, { t: 0.62, x: 86, y: 72 }, { t: 1, x: 86, y: 128 }],
    pass: 0.62,
  },
  swish: {
    hits: [],
    points: [START, { t: 0.42, x: 86, y: 30 }, { t: 0.7, x: 86, y: 72 }, { t: 1, x: 86, y: 128 }],
    pass: 0.7,
  },
  'deep-swish': {
    hits: [],
    points: [START, { t: 0.4, x: 86, y: 2 }, { t: 0.74, x: 86, y: 72 }, { t: 1, x: 86, y: 128 }],
    pass: 0.74,
  },
};

/** Where in the whole animation the ball leaves the hands. */
export const LAUNCH = 0.3;
const DUNK_PASS = 0.54;

const pct = (n: number): string => `${(n * 100).toFixed(1)}%`;
const at = (x: number, y: number): string => `translate(calc(${x - 6} * var(--u)), calc(${y - 6} * var(--u)))`;
/** The number of jumps in a stepped move: about one every 7 game pixels, so the ball moves in chunky hops. */
const hops = (ax: number, ay: number, bx: number, by: number): number => Math.max(2, Math.round(Math.hypot(bx - ax, by - ay) / 7));
const carryAt = (p: 'n' | 's'): string => `translate(calc((var(--${p}x) + 2) * var(--u)), calc((var(--${p}y) - 46) * var(--u)))`;

/** CSS keyframes for the ball of every shot. The start comes from custom properties so each shot starts from its own spot. */
export function ballKeyframes(): string {
  const out: string[] = [];
  for (const [name, flight] of Object.entries(FLIGHT)) {
    const lines: string[] = [];
    lines.push(`0% { transform: ${carryAt('n')}; animation-timing-function: steps(3, end); }`);
    lines.push(`12% { transform: ${carryAt('s')}; animation-timing-function: steps(2, end); }`);
    lines.push(`${pct(LAUNCH - 0.04)} { transform: translate(calc((var(--sx) + 2) * var(--u)), calc((var(--sy) - 52) * var(--u))); animation-timing-function: steps(2, end); }`);
    let prev: Waypoint | null = null;
    flight.points.forEach((p, i) => {
      if (i === 0) {
        lines.push(`${pct(LAUNCH)} { transform: translate(calc((var(--sx) - 3) * var(--u)), calc((var(--sy) - 76) * var(--u))); animation-timing-function: steps(4, end); }`);
        return;
      }
      const time = LAUNCH + p.t * (1 - LAUNCH);
      const n = prev === null ? 4 : hops(prev.x, prev.y, p.x, p.y);
      lines.push(`${pct(time)} { transform: ${at(p.x, p.y)}; animation-timing-function: steps(${n}, end); }`);
      prev = p;
    });
    out.push(`@keyframes court-ball-${name} {\n  ${lines.join('\n  ')}\n}`);
  }
  // the slam dunk: the ball stays in the hand through the drive and the jump, then goes through
  out.push(`@keyframes court-ball-dunk {
  0% { transform: ${carryAt('n')}; animation-timing-function: steps(3, end); }
  12% { transform: ${carryAt('s')}; animation-timing-function: steps(4, end); }
  34% { transform: ${at(DUNK_AT.x + 40, DUNK_AT.y + 14)}; animation-timing-function: steps(2, end); }
  44% { transform: ${at(HOOP.x, HOOP.y - 6)}; animation-timing-function: steps(1, end); }
  ${pct(DUNK_PASS)} { transform: ${at(HOOP.x, HOOP.y + 4)}; animation-timing-function: steps(5, end); }
  72% { transform: ${at(HOOP.x, 128)}; animation-timing-function: steps(2, end); }
  80% { transform: ${at(HOOP.x, 118)}; animation-timing-function: steps(2, end); }
  100% { transform: ${at(HOOP.x, 128)}; }
}`);
  return out.join('\n\n');
}

/** The net for each made shot: stretched as the ball goes through (frame 1, then 2), then back to rest. Plain swaps, no tweening. */
export function netKeyframes(): string {
  const out: string[] = [];
  const passes: Array<[string, number]> = [
    ...Object.entries(FLIGHT).filter(([, f]) => f.pass !== undefined).map(([n, f]): [string, number] => [n, LAUNCH + (f.pass as number) * (1 - LAUNCH)]),
    ['dunk', DUNK_PASS],
  ];
  for (const [name, p] of passes) {
    const swap = (a: number, b: number, shown: number, hidden: number): string =>
      `${pct(a)} { opacity: ${shown}; animation-timing-function: step-end; } ${pct(b)} { opacity: ${hidden}; }`;
    out.push(`@keyframes court-net1-${name} { 0% { opacity: 0; animation-timing-function: step-end; } ${swap(p, p + 0.05, 1, 0)} 100% { opacity: 0; } }`);
    out.push(`@keyframes court-net2-${name} { 0% { opacity: 0; animation-timing-function: step-end; } ${swap(p + 0.05, p + 0.14, 1, 0)} 100% { opacity: 0; } }`);
    out.push(`@keyframes court-net0-${name} { 0% { opacity: 1; animation-timing-function: step-end; } ${swap(p, p + 0.14, 0, 1)} 100% { opacity: 1; } }`);
  }
  // the rim shakes a game pixel when the ball hits it
  for (const [name, f] of Object.entries(FLIGHT)) {
    if (f.hits.length === 0) continue;
    const frames = f.hits.map((h) => {
      const t = LAUNCH + h * (1 - LAUNCH);
      return `${pct(t)} { transform: translateY(calc(1 * var(--u))); animation-timing-function: step-end; } ${pct(t + 0.04)} { transform: translateY(0); }`;
    });
    out.push(`@keyframes court-rim-${name} { 0% { transform: translateY(0); } ${frames.join(' ')} 100% { transform: translateY(0); } }`);
  }
  return out.join('\n');
}

/** Directions of the dunk's burst: whole game pixels, spread round the rim. At most 28 pieces. */
export function burstVectors(count = 28): Array<{ dx: number; dy: number }> {
  const n = Math.min(count, 28);
  return Array.from({ length: n }, (_, i) => {
    const angle = (i / n) * Math.PI * 2 + (i % 3) * 0.17;
    const reach = 12 + ((i * 7) % 11);
    return { dx: Math.round(Math.cos(angle) * reach), dy: Math.round(Math.sin(angle) * reach * 0.8 - 4) };
  });
}
