import { createContext, useCallback, useContext, useMemo, useRef, useState, type ReactNode } from 'react';

/**
 * One polite live region for the whole page. Screen readers hear a message once, without the page moving focus.
 * The timer is deliberately not announced every second: only a few warnings are sent through here.
 */
type Announce = (message: string) => void;

const AnnouncerContext = createContext<Announce>(() => undefined);

export const useAnnounce = (): Announce => useContext(AnnouncerContext);

export function AnnouncerProvider({ children }: { children: ReactNode }) {
  const [message, setMessage] = useState('');
  const flip = useRef(false);
  const announce = useCallback<Announce>((text) => {
    flip.current = !flip.current;
    // A trailing invisible character makes the same message announce again.
    setMessage(text + (flip.current ? '​' : ''));
  }, []);
  const value = useMemo(() => announce, [announce]);
  return (
    <AnnouncerContext.Provider value={value}>
      {children}
      <div className="visually-hidden" role="status" aria-live="polite" aria-atomic="true" data-testid="announcer">
        {message}
      </div>
    </AnnouncerContext.Provider>
  );
}
