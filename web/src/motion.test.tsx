import { act, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { Confetti, CONFETTI_COUNT } from './components/Confetti';
import { ShotLabel } from './components/ShotLabel';
import { RollingNumber } from './components/RollingNumber';
import { prefersReducedMotion, useReducedMotion } from './motion';
import { shotForPoints } from './shots';


function mockMatchMedia(reduce: boolean) {
  const listeners = new Set<() => void>();
  const query = { matches: reduce, addEventListener: (_: string, fn: () => void) => listeners.add(fn), removeEventListener: (_: string, fn: () => void) => listeners.delete(fn) };
  vi.stubGlobal('matchMedia', vi.fn(() => query));
  return { set(value: boolean) { query.matches = value; listeners.forEach((fn) => fn()); } };
}

afterEach(() => vi.unstubAllGlobals());

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
