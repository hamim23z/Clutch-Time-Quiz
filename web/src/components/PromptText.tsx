/** Splits "Since 2001-02 (through 2025-26), name a player who ..." into the era and the task. The era is shown smaller. */
export function splitEra(text: string): { era: string; task: string } | null {
  const m = /^(Since [^,]+,)\s+(.+)$/s.exec(text);
  return m && m[1] && m[2] ? { era: m[1], task: m[2] } : null;
}

/** The prompt text, with the era in a quieter style. The words are exactly the prompt's, so a screen reader reads the same sentence. */
export function PromptText({ text }: { text: string }) {
  const parts = splitEra(text);
  if (!parts) return <>{text}</>;
  return (
    <>
      <span className="prompt__era">{parts.era}</span> <span className="prompt__task">{parts.task}</span>
    </>
  );
}
