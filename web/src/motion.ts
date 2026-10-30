import { createContext, useContext, useEffect, useState } from 'react';

const QUERY = '(prefers-reduced-motion: reduce)';

/** True when the visitor asked their system for less motion. False where matchMedia does not exist. */
export function prefersReducedMotion(): boolean {
  return typeof window !== 'undefined' && typeof window.matchMedia === 'function' && window.matchMedia(QUERY).matches;
}

/** Lets a page (the animation review page) show the reduced-motion version without changing the system setting. */
export const ReducedMotionOverride = createContext<boolean | null>(null);

/** Follows the setting live, so turning it on mid-game takes effect at once. */
export function useReducedMotion(): boolean {
  const override = useContext(ReducedMotionOverride);
  const [reduced, setReduced] = useState(prefersReducedMotion);
  useEffect(() => {
    if (typeof window === 'undefined' || typeof window.matchMedia !== 'function') return;
    const query = window.matchMedia(QUERY);
    const update = (): void => setReduced(query.matches);
    update();
    query.addEventListener('change', update);
    return () => query.removeEventListener('change', update);
  }, []);
  return override ?? reduced;
}
