import { useEffect, useState } from 'react';

/** At this width and wider the game is a split screen: the panel on the left, the court on the right. */
export const SPLIT_MIN_WIDTH = 900;

export type Layout = 'split' | 'stacked';

/** split from 900 px up (desktop, tablet landscape); stacked below it (phones, narrow windows): a court strip above the panel. */
export function layoutForWidth(width: number): Layout {
  return width >= SPLIT_MIN_WIDTH ? 'split' : 'stacked';
}

const QUERY = `(min-width: ${SPLIT_MIN_WIDTH}px)`;

function current(): Layout {
  if (typeof window === 'undefined') return 'stacked';
  if (typeof window.matchMedia === 'function') return window.matchMedia(QUERY).matches ? 'split' : 'stacked';
  return layoutForWidth(window.innerWidth);
}

/** The layout now, following the window as it is resized or rotated. The CSS switches on the same 900 px breakpoint. */
export function useLayout(): Layout {
  const [layout, setLayout] = useState<Layout>(current);
  useEffect(() => {
    const update = (): void => setLayout(current());
    update();
    if (typeof window.matchMedia === 'function') {
      const query = window.matchMedia(QUERY);
      query.addEventListener('change', update);
      return () => query.removeEventListener('change', update);
    }
    window.addEventListener('resize', update);
    return () => window.removeEventListener('resize', update);
  }, []);
  return layout;
}
