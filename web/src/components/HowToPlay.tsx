import { PROMPTS_PER_DIVE, SECONDS_PER_PROMPT, TIERS, TIER_POINTS, TIER_RANGES } from '../tiers';

interface Props {
  onPlay: () => void;
  onBack: () => void;
}

export function HowToPlay({ onPlay, onBack }: Props) {
  return (
    <section className="card howto" aria-labelledby="howto-heading">
      <h2 id="howto-heading">How to play</h2>
      <ol className="steps">
        <li>
          A dive is <strong>{PROMPTS_PER_DIVE} prompts</strong>, with <strong>{SECONDS_PER_PROMPT} seconds</strong> each.
        </li>
        <li>Type one answer, a player or a team, or pick it from the suggestions. The suggestions list everyone, so they never give an answer away.</li>
        <li>
          The more obscure a correct answer, the more it scores. A wrong answer, or running out of time, scores <strong>0</strong>.
        </li>
        <li>After each prompt you see your tier and points, plus the most famous and the rarest valid answers.</li>
        <li>At the end, copy your score and seven colored squares to share.</li>
      </ol>
      <table className="tiers">
        <caption>Points by tier</caption>
        <thead>
          <tr>
            <th scope="col">Tier</th>
            <th scope="col">How famous</th>
            <th scope="col">Points</th>
          </tr>
        </thead>
        <tbody>
          {TIERS.map((t) => (
            <tr key={t}>
              <th scope="row">
                <span className={`chip chip--t${t}`} aria-hidden="true">{t}</span> Tier {t}
              </th>
              <td>{TIER_RANGES[t]}</td>
              <td>{TIER_POINTS[t]}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <p className="caveat">
        Obscurity comes from a fame score computed from the data. It is a stand-in for real answer frequencies, so it is an approximation.
      </p>
      <p className="caveat">
        Every prompt says which years it covers, for example &ldquo;Since 2002&rdquo;. A real player from before that gets an &ldquo;outside the data range&rdquo; message, not a miss.
      </p>
      <div className="actions">
        <button type="button" className="primary" onClick={onPlay}>
          Play
        </button>
        <button type="button" className="secondary" onClick={onBack}>
          Back
        </button>
      </div>
    </section>
  );
}
