/** Shown while the game data loads: a bouncing ball and a short line of text. */
export function LoadingScreen() {
  return (
    <section className="card loading" role="status" aria-live="polite">
      <div className="loading__ball" aria-hidden="true" />
      <div className="loading__shadow" aria-hidden="true" />
      <p className="loading__text">Loading the game…</p>
    </section>
  );
}
