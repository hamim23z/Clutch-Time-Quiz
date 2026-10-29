import { useEffect, useRef, useState } from 'react';

/**
 * Counts down from totalSeconds and calls onExpire once when it reaches zero. It reads the clock instead of adding up
 * ticks, so a slow or throttled timer (a background tab) still ends on time. Returns the milliseconds left.
 */
export function useCountdown(totalSeconds: number, onExpire: () => void): number {
  const [remainingMs, setRemainingMs] = useState(totalSeconds * 1000);
  const onExpireRef = useRef(onExpire);
  useEffect(() => {
    onExpireRef.current = onExpire;
  });
  useEffect(() => {
    const deadline = Date.now() + totalSeconds * 1000;
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
  }, [totalSeconds]);
  return remainingMs;
}
