import { useEffect, useRef, useState } from 'react';

/**
 * Counts down from totalSeconds and calls onExpire once when it reaches zero. It reads the clock instead of adding up
 * ticks, so a slow or throttled timer (a background tab) still ends on time. Returns the milliseconds left.
 */
export function useCountdown(totalSeconds: number, onExpire: () => void, elapsedMs = 0): number {
  const [remainingMs, setRemainingMs] = useState(Math.max(0, totalSeconds * 1000 - elapsedMs));
  const onExpireRef = useRef(onExpire);
  useEffect(() => {
    onExpireRef.current = onExpire;
  });
  useEffect(() => {
    const deadline = Date.now() + Math.max(0, totalSeconds * 1000 - elapsedMs);
    let expired = false;
    const id = setInterval(() => {
      const left = Math.max(0, deadline - Date.now());
      setRemainingMs(left);
      if (left === 0 && !expired) {
        expired = true;
        clearInterval(id);
        onExpireRef.current();
      }
    }, 100);
    return () => clearInterval(id);
    // elapsedMs is only the starting point: changing it later must not restart the clock
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [totalSeconds]);
  return remainingMs;
}
