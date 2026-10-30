import type { Streaks } from '../streaks';
import { StreakBadge } from './StreakBadge';
import { Wordmark } from './Wordmark';

interface Props {
  number: number;
  played: boolean;
  streaks: Streaks;
  /** True when the streak has gone up since the home screen was last shown: it pops. */
  streakUp: boolean;
  /** False when the browser will not keep anything, so streaks and the archive cannot last. */
  saving: boolean;
  onPlay: () => void;
  onResults: () => void;
  onArchive: () => void;
  onHowTo: () => void;
}

const days = (n: number): string => `${n} ${n === 1 ? 'day' : 'days'}`;

export function Home({ number, played, streaks, streakUp, saving, onPlay, onResults, onArchive, onHowTo }: Props) {
  return (
    <section className="home" aria-label="Home">
      <Wordmark />
      <p className="home__tagline">The daily basketball trivia game where the obvious answer loses.</p>
      <p className="home__rules">Seven prompts, 25 seconds each. Name a valid answer: the more obscure it is, the more it scores.</p>
      <p className="today">
        Today&rsquo;s dive: <strong>#{number}</strong>
      </p>
      <div className="actions actions--home">
        {played ? (
          <button type="button" className="primary primary--big" onClick={onResults}>
            View results
          </button>
        ) : (
          <button type="button" className="primary primary--big" onClick={onPlay}>
            Play today&rsquo;s dive
          </button>
        )}
        <div className="actions__row">
          <button type="button" className="secondary" onClick={onArchive}>
            Archive
          </button>
          <button type="button" className="secondary" onClick={onHowTo}>
            How to play
          </button>
        </div>
      </div>
      <dl className="streaks" aria-label="Streaks">
        <div>
          <dt>Streak</dt>
          <dd>
            <StreakBadge value={streaks.current} increased={streakUp} />
          </dd>
        </div>
        <div>
          <dt>Best streak</dt>
          <dd data-testid="streak-best">{days(streaks.best)}</dd>
        </div>
      </dl>
      {!saving && <p className="caveat">This browser is not saving anything, so your streaks and past dives will be gone when you close the page.</p>}
    </section>
  );
}
