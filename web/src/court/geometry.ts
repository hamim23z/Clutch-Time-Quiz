import type { ShotName } from '../shots';

/** The court is drawn in an 800 x 640 picture: the hoop at the top, the floor coming toward the viewer. */
export const VIEW = { width: 800, height: 640 };
/** The pictures are drawn wider than the court (400 either side) so a wide, short strip shows more arena instead of cutting the hoop off. */
export const VIEWBOX = '-400 0 1600 640';
export const HOOP = { x: 400, y: 258 }; // the middle of the rim opening
export const NEUTRAL = { x: 400, y: 505 }; // where the shooter waits while a question is on

/** How big things look at a height on the floor: small near the hoop (far), large near the viewer. */
export function depthScale(y: number): number {
  return 0.72 + ((y - 300) / 340) * 0.78;
}

/** Where the shooter takes each shot from (feet on the floor). Low points are close to the hoop, deep cuts are far out. */
export const SPOTS: Record<ShotName, { x: number; y: number }> = {
  airball: { x: 480, y: 468 },
  clank: { x: 432, y: 352 },
  rattle: { x: 332, y: 398 },
  bank: { x: 268, y: 432 },
  swish: { x: 400, y: 486 },
  'deep-swish': { x: 214, y: 548 },
  dunk: { x: 346, y: 436 },
};

/** The ball in the shooter's hands for a pair of feet. */
export function hand(foot: { x: number; y: number }): { x: number; y: number; s: number } {
  const s = depthScale(foot.y);
  return { x: foot.x + 4 * s, y: foot.y - 84 * s, s: s * 0.95 };
}

interface Waypoint {
  /** 0 to 1 along the flight. */
  t: number;
  x: number;
  y: number;
  /** The ball's size. */
  s: number;
  ease?: 'in' | 'out';
  /** Degrees of spin at this point. */
  r?: number;
}

/** The ball's flight after it leaves the hands, for each shot. */
export const FLIGHT: Record<Exclude<ShotName, 'dunk'>, Waypoint[]> = {
  airball: [
    { t: 0, x: NaN, y: NaN, s: NaN, ease: 'out' },
    { t: 0.42, x: 350, y: 150, s: 0.72, ease: 'in' },
    { t: 0.62, x: 316, y: 236, s: 0.68, r: 200 },
    { t: 1, x: 296, y: 720, s: 1.1, r: 520 },
  ],
  clank: [
    { t: 0, x: NaN, y: NaN, s: NaN, ease: 'out' },
    { t: 0.46, x: 408, y: 150, s: 0.68, ease: 'in' },
    { t: 0.58, x: 404, y: 178, s: 0.66, ease: 'out' },
    { t: 0.74, x: 472, y: 98, s: 0.6, ease: 'in' },
    { t: 1, x: 650, y: 430, s: 1.1, r: 300 },
  ],
  rattle: [
    { t: 0, x: NaN, y: NaN, s: NaN, ease: 'out' },
    { t: 0.36, x: 400, y: 178, s: 0.68, ease: 'in' },
    { t: 0.5, x: 386, y: 246, s: 0.64, ease: 'out' },
    { t: 0.6, x: 362, y: 214, s: 0.64, ease: 'in' },
    { t: 0.7, x: 416, y: 246, s: 0.64, ease: 'out' },
    { t: 0.76, x: 420, y: 232, s: 0.64, ease: 'in' },
    { t: 0.84, x: 400, y: 262, s: 0.64 },
    { t: 1, x: 400, y: 340, s: 0.7 },
  ],
  bank: [
    { t: 0, x: NaN, y: NaN, s: NaN, ease: 'out' },
    { t: 0.42, x: 400, y: 178, s: 0.68, ease: 'in' },
    { t: 0.58, x: 400, y: 230, s: 0.65, ease: 'out' },
    { t: 0.68, x: 404, y: 240, s: 0.64, ease: 'in' },
    { t: 0.78, x: 400, y: 266, s: 0.64 },
    { t: 1, x: 400, y: 340, s: 0.7 },
  ],
  swish: [
    { t: 0, x: NaN, y: NaN, s: NaN, ease: 'out' },
    { t: 0.48, x: 400, y: 138, s: 0.68, ease: 'in' },
    { t: 0.72, x: 400, y: 256, s: 0.64 },
    { t: 1, x: 400, y: 340, s: 0.7 },
  ],
  'deep-swish': [
    { t: 0, x: NaN, y: NaN, s: NaN, ease: 'out' },
    { t: 0.46, x: 400, y: 58, s: 0.7, ease: 'in' },
    { t: 0.72, x: 400, y: 256, s: 0.64 },
    { t: 1, x: 400, y: 340, s: 0.7 },
  ],
};

/** Time spent winding up, as a share of the animation, before the ball leaves the hands. */
export const WINDUP = 0.22;

const pct = (n: number): string => `${(n * 100).toFixed(1)}%`;

/** CSS keyframes for the ball of every shot. The start comes from custom properties so each shot can start from its own spot. */
export function ballKeyframes(): string {
  const out: string[] = [];
  for (const [name, points] of Object.entries(FLIGHT)) {
    const frames: string[] = [];
    frames.push(`0% { transform: translate(var(--nx), var(--ny)) scale(var(--ns)); animation-timing-function: ease-out; }`);
    frames.push(`10% { transform: translate(var(--bx), var(--by)) scale(var(--bs)); }`);
    frames.push(`${pct(WINDUP - 0.02)} { transform: translate(var(--bx), calc(var(--by) + 5px)) scale(var(--bs)); }`);
    points.forEach((p, i) => {
      const t = WINDUP + p.t * (1 - WINDUP);
      const ease = p.ease === 'in' ? 'ease-in' : p.ease === 'out' ? 'ease-out' : 'linear';
      if (i === 0) {
        frames.push(`${pct(t)} { transform: translate(var(--bx), var(--by)) scale(var(--bs)); animation-timing-function: ease-out; }`);
      } else {
        frames.push(`${pct(t)} { transform: translate(${p.x}px, ${p.y}px) scale(${p.s}) rotate(${p.r ?? 0}deg); animation-timing-function: ${ease}; }`);
      }
    });
    out.push(`@keyframes court-ball-${name} {\n  ${frames.join('\n  ')}\n}`);
  }
  // the slam dunk: the ball stays in the shooter's hand through the drive and the jump, then goes through
  out.push(`@keyframes court-ball-dunk {
  0% { transform: translate(var(--nx), var(--ny)) scale(var(--ns)); animation-timing-function: ease-out; }
  12% { transform: translate(var(--bx), var(--by)) scale(var(--bs)); animation-timing-function: ease-in-out; }
  34% { transform: translate(372px, 352px) scale(0.72); animation-timing-function: ease-out; }
  54% { transform: translate(394px, 226px) scale(0.66); animation-timing-function: ease-in; }
  64% { transform: translate(400px, 254px) scale(0.64); }
  100% { transform: translate(400px, 342px) scale(0.7); }
}`);
  return out.join('\n\n');
}


/** CSS keyframes for the shooter: from where he waits to the spot, a small jump at the release, and for the dunk a drive and a hang. */
export function shooterKeyframes(): string {
  return `@keyframes court-shooter-shot {
  0% { transform: translate(var(--nx), var(--ny)) scale(var(--ns)); animation-timing-function: ease-out; }
  10% { transform: translate(var(--sx), var(--sy)) scale(var(--ss)); animation-timing-function: ease-in-out; }
  18% { transform: translate(var(--sx), calc(var(--sy) - 4px)) scale(var(--ss)); animation-timing-function: ease-out; }
  26% { transform: translate(var(--sx), calc(var(--sy) - 14px * var(--ss))) scale(var(--ss)); animation-timing-function: ease-in; }
  42%, 100% { transform: translate(var(--sx), var(--sy)) scale(var(--ss)); }
}

@keyframes court-shooter-dunk {
  0% { transform: translate(var(--nx), var(--ny)) scale(var(--ns)); animation-timing-function: ease-out; }
  12% { transform: translate(var(--sx), var(--sy)) scale(var(--ss)); animation-timing-function: ease-in; }
  34% { transform: translate(368px, 368px) scale(0.74); animation-timing-function: ease-out; }
  54% { transform: translate(390px, 278px) scale(0.64); }
  74% { transform: translate(392px, 282px) scale(0.64); animation-timing-function: ease-in; }
  100% { transform: translate(392px, 336px) scale(0.6); }
}`;
}
