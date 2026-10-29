interface Props {
  /** What went wrong, in words a person can read out when asking for help. */
  message: string;
  onRetry: () => void;
}

/** A friendly error with a retry button. It is what the player sees instead of a blank page. */
export function ErrorScreen({ message, onRetry }: Props) {
  return (
    <section className="card error-screen" role="alert">
      <h2>We couldn&rsquo;t load the game</h2>
      <p>This is usually a bad connection. Check it and try again.</p>
      <p className="error-screen__detail">Could not load the game data: {message}</p>
      <div className="actions">
        <button type="button" className="primary" onClick={onRetry}>
          Try again
        </button>
      </div>
    </section>
  );
}
