import type { ShotInfo } from '../shots';

/** The points and the tier name, big, in the tier's color. A miss shows 0 in a muted color. Decoration: the heading carries the text. */
export function ShotLabel({ shot, skipped = false }: { shot: ShotInfo; skipped?: boolean }) {
  const tier = shot.tier === null ? 'miss' : `t${shot.tier}`;
  return (
    <div className={`shot-label shot-label--${tier}${skipped ? ' is-skipped' : ''}`} aria-hidden="true">
      <span className="shot-label__points">{shot.points}</span>
      <span className="shot-label__name">{shot.label}</span>
    </div>
  );
}
