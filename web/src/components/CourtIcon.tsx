/** A tiny half-court with a hoop, for the results squares. It takes the square's color through `currentColor`. */
export function CourtIcon({ miss }: { miss: boolean }) {
  return (
    <svg className="court-icon" viewBox="0 0 40 40" aria-hidden="true" focusable="false">
      <rect x="3" y="3" width="34" height="34" rx="4" fill="none" stroke="currentColor" strokeWidth="2" opacity="0.55" />
      <path d="M13 37V24H27V37M13 24A7 7 0 0 1 27 24" fill="none" stroke="currentColor" strokeWidth="1.6" opacity="0.55" />
      {miss ? <path d="M15 12L25 22M25 12L15 22" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" /> : <><circle cx="20" cy="14" r="5" fill="currentColor" /><path d="M16 21H24" stroke="currentColor" strokeWidth="2" strokeLinecap="round" /></>}
    </svg>
  );
}
