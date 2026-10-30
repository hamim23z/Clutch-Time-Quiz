import type { CSSProperties } from 'react';

/** "NBA DEEP CUT": the letters drop in with a bounce, then settle. The heading carries the words, the letters are decoration. */
export function Wordmark() {
  const rows = [['N', 'B', 'A'], ['D', 'E', 'E', 'P'], ['C', 'U', 'T']];
  let n = 0;
  return (
    <h1 className="wordmark" aria-label="NBA Deep Cut">
      {rows.map((letters, r) => (
        <span key={r} className={`wordmark__row wordmark__row--${r}`} aria-hidden="true">
          {letters.map((ch) => {
            const i = n++;
            return (
              <span key={i} className="wordmark__letter" style={{ '--i': i } as CSSProperties}>
                {ch}
              </span>
            );
          })}
        </span>
      ))}
    </h1>
  );
}
