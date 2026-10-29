const days = (n: number): string => `${n} ${n === 1 ? 'day' : 'days'}`;

/** The current streak, which pops when it has just gone up. */
export function StreakBadge({ value, increased, testId = 'streak-current' }: { value: number; increased: boolean; testId?: string }) {
  return (
    <span className={`streak-badge${increased ? ' streak-badge--pop' : ''}`} data-testid={testId}>
      {days(value)}
    </span>
  );
}
