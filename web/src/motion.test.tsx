import { act, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { Confetti, CONFETTI_COUNT } from './components/Confetti';
import { MAX_PARTICLES, ShotAnimation, particleStyles } from './components/ShotAnimation';
import { ShotLabel } from './components/ShotLabel';
import { RollingNumber } from './components/RollingNumber';
import { prefersReducedMotion, useReducedMotion } from './motion';
import { SHOT_NAMES, shotForPoints } from './shots';

const POINTS = [0, 10, 20, 35, 55, 75, 100];

function mockMatchMedia(reduce: boolean) {
  const listeners = new Set<() => void>();
  const query = { matches: reduce, addEventListener: (_: string, fn: () => void) => listeners.add(fn), removeEventListener: (_: string, fn: () => void) => listeners.delete(fn) };
  vi.stubGlobal('matchMedia', vi.fn(() => query));
  return { set(value: boolean) { query.matches = value; listeners.forEach((fn) => fn()); } };
}

afterEach(() => vi.unstubAllGlobals());

describe('ShotAnimation', () => {
  it.each(POINTS)('draws the shot for %i points with a ball, a hoop and a net', (points) => {
    const shot = shotForPoints(points);
    const { container } = render(<ShotAnimation shot={shot} />);
    expect(container.querySelector(`.shot--${shot.name}`)).not.toBeNull();
    expect(container.querySelector('.shot__ball')).not.toBeNull();
    expect(container.querySelector('.shot__rim')).not.toBeNull();
    expect(container.querySelector('.shot__net')).not.toBeNull();
    expect(container.querySelector('.shot__board')).not.toBeNull();
    expect(container.firstElementChild).toHaveAttribute('aria-hidden', 'true'); // decoration: the result is in the text
  });

  it('gives only the slam dunk a player and a burst of particles, capped at 40', () => {
    for (const name of SHOT_NAMES) {
      const points = POINTS[SHOT_NAMES.indexOf(name)]!;
      const { container, unmount } = render(<ShotAnimation shot={shotForPoints(points)} />);
      const particles = container.querySelectorAll('.particle').length;
      expect(container.querySelector('.shot__player') !== null).toBe(name === 'dunk');
      expect(particles).toBe(name === 'dunk' ? MAX_PARTICLES : 0);
      expect(particles).toBeLessThanOrEqual(40);
      unmount();
    }
    expect(particleStyles(500)).toHaveLength(MAX_PARTICLES);
  });

  it('gives only the deep swish a crowd flash', () => {
    for (const name of SHOT_NAMES) {
      const { container, unmount } = render(<ShotAnimation shot={shotForPoints(POINTS[SHOT_NAMES.indexOf(name)]!)} />);
      expect(container.querySelector('.shot__crowd') !== null).toBe(name === 'deep-swish');
      unmount();
    }
  });

  it('marks a skipped shot so every animation jumps to its end', () => {
    const { container } = render(<ShotAnimation shot={shotForPoints(55)} skipped />);
    expect(container.querySelector('.shot')).toHaveClass('is-skipped');
  });

  it.each(POINTS)('reduced motion (%i points): no ball, no player, no particles, no crowd: just the still hoop', (points) => {
    const { container } = render(<ShotAnimation shot={shotForPoints(points)} reduced />);
    expect(container.querySelector('.shot')).toHaveClass('is-reduced');
    for (const sel of ['.shot__ball', '.shot__player', '.particle', '.shot__crowd']) expect(container.querySelector(sel)).toBeNull();
    expect(container.querySelector('.shot__rim')).not.toBeNull();
  });

  it('uses the tier color class for every tier and a muted one for a miss', () => {
    for (const [points, cls] of [[0, 'miss'], [10, 't1'], [20, 't2'], [35, 't3'], [55, 't4'], [75, 't5'], [100, 't6']] as const) {
      const { container, unmount } = render(<><ShotAnimation shot={shotForPoints(points)} /><ShotLabel shot={shotForPoints(points)} /></>);
      expect(container.querySelector(`.shot--${cls}`)).not.toBeNull();
      expect(container.querySelector(`.shot-label--${cls}`)).not.toBeNull();
      unmount();
    }
  });
});

describe('ShotLabel', () => {
  it('shows the points and the tier name', () => {
    render(<ShotLabel shot={shotForPoints(100)} />);
    expect(screen.getByText('100')).toBeInTheDocument();
    expect(screen.getByText('Poster dunk')).toBeInTheDocument();
  });

  it('shows 0 and Airball for a miss', () => {
    render(<ShotLabel shot={shotForPoints(0)} />);
    expect(screen.getByText('0')).toBeInTheDocument();
    expect(screen.getByText('Airball')).toBeInTheDocument();
  });
});

describe('reduced motion setting', () => {
  it('reads prefers-reduced-motion, and is false where matchMedia does not exist', () => {
    vi.stubGlobal('matchMedia', undefined);
    expect(prefersReducedMotion()).toBe(false);
    mockMatchMedia(true);
    expect(prefersReducedMotion()).toBe(true);
  });

  it('follows the setting live', () => {
    const media = mockMatchMedia(false);
    function Probe() {
      return <p>{useReducedMotion() ? 'reduced' : 'full'}</p>;
    }
    render(<Probe />);
    expect(screen.getByText('full')).toBeInTheDocument();
    act(() => media.set(true));
    expect(screen.getByText('reduced')).toBeInTheDocument();
  });
});

describe('RollingNumber', () => {
  it('shows the value at once when instant', () => {
    render(<RollingNumber value={85} from={10} instant />);
    expect(screen.getByText('85')).toBeInTheDocument();
  });

  it('rolls up from the old value to the new one', async () => {
    vi.useFakeTimers();
    const { container } = render(<RollingNumber value={120} from={20} delayMs={100} durationMs={400} />);
    expect(container.textContent).toBe('20');
    await act(async () => void vi.advanceTimersByTime(300));
    const mid = Number(container.textContent);
    expect(mid).toBeGreaterThan(20);
    await act(async () => void vi.advanceTimersByTime(1000));
    expect(container.textContent).toBe('120');
    vi.useRealTimers();
  });
});

describe('Confetti', () => {
  it('has at most 40 pieces and is hidden from screen readers', () => {
    const { container } = render(<Confetti />);
    expect(container.querySelectorAll('.confetti__piece')).toHaveLength(CONFETTI_COUNT);
    expect(CONFETTI_COUNT).toBeLessThanOrEqual(40);
    expect(container.firstElementChild).toHaveAttribute('aria-hidden', 'true');
  });
});
