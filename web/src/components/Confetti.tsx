import type { CSSProperties } from 'react';

export const CONFETTI_COUNT = 40; // capped, as with the dunk's particles
const COLORS = ['var(--t2)', 'var(--t3)', 'var(--t4)', 'var(--t5)', 'var(--t6)', 'var(--accent)'];

/** A short burst of confetti in the tier colors, falling with CSS transforms. Decoration only. */
export function Confetti() {
  return (
    <div className="confetti" aria-hidden="true">
      {Array.from({ length: CONFETTI_COUNT }, (_, i) => (
        <span
          key={i}
          className="confetti__piece"
          style={{ '--x': `${(i * 53) % 100}%`, '--delay': `${(i % 8) * 70}ms`, '--spin': `${(i % 2 ? 1 : -1) * (180 + (i % 5) * 90)}deg`, '--drift': `${((i % 7) - 3) * 14}px`, background: COLORS[i % COLORS.length] } as CSSProperties}
        />
      ))}
    </div>
  );
}
