import type { Streaks } from '../streaks';

interface Props {
  number: number;
  played: boolean;
  streaks: Streaks;
  /** False when the browser will not keep anything, so streaks and the archive cannot last. */
  saving: boolean;
  onPlay: () => void;
  onResults: () => void;
  onArchive: () => void;
  onHowTo: () => void;
}

const days = (n: number): string => `${n} ${n === 1 ? 'day' : 'days'}`;

export function Home({ number, played, streaks, saving, onPlay, onResults, onArchive, onHowTo }: Props) {
  return (
    <section className="card home" aria-labelledby="home-heading">
      <h2 id="home-heading">The daily trivia game where the obvious answer loses.</h2>
      <p>Seven basketball prompts, 25 seconds each. Name a valid answer, and the more obscure it is, the more it scores.</p>
      <p className="today">Today&rsquo;s dive: <strong>#{number}</strong></p>
      <dl className="streaks" aria-label="Streaks">
        <div>
          <dt>Streak</dt>
          <dd data-testid="streak-current">{days(streaks.current)}</dd>
        </div>
        <div>
          <dt>Best streak</dt>
          <dd data-testid="streak-best">{days(streaks.best)}</dd>
        </div>
      </dl>
      {!saving && <p className="caveat">This browser is not saving anything, so your streaks and past dives will be gone when you close the page.</p>}
      <div className="actions">
        {played ? (
          <button type="button" className="primary" onClick={onResults}>
            Today&rsquo;s results
          </button>
        ) : (
          <button type="button" className="primary" onClick={onPlay}>
            Play
          </button>
        )}
        <button type="button" className="secondary" onClick={onArchive}>
          Archive
        </button>
        <button type="button" className="secondary" onClick={onHowTo}>
          How to play
        </button>
      </div>
    </section>
  );
}
