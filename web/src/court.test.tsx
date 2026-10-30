import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { act, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { CourtProvider, INITIAL_COURT, createCourtStore } from './court/courtStore';
import CourtScene, { burstVectors, REPLAY_STEP_MS, shotVars } from './court/CourtScene';
import { FLIGHT, HOOP, NEUTRAL, SPOTS, VIEWBOX, ballKeyframes, depthScale, hand, shooterKeyframes } from './court/geometry';
import { ReducedMotionOverride } from './motion';
import { SHOT_NAMES, shotForPoints } from './shots';

const POINTS = [0, 10, 20, 35, 55, 75, 100];

function mount(patch = {}, reduced: boolean | null = null) {
  const store = createCourtStore({ ...INITIAL_COURT, ...patch });
  const view = render(
    <CourtProvider store={store}>
      <ReducedMotionOverride.Provider value={reduced}>
        <CourtScene />
      </ReducedMotionOverride.Provider>
    </CourtProvider>,
  );
  return { store, ...view, court: screen.getByTestId('court') };
}

afterEach(() => vi.useRealTimers());

describe('the court store', () => {
  it('tells listeners about a change and not about a repeat', () => {
    const store = createCourtStore();
    const listener = vi.fn();
    const off = store.subscribe(listener);
    store.set({ clock: 20 });
    store.set({ clock: 20 });
    expect(listener).toHaveBeenCalledTimes(1);
    store.set({ clock: 19, points: 10 });
    expect(listener).toHaveBeenCalledTimes(2);
    off();
    store.set({ clock: 3 });
    expect(listener).toHaveBeenCalledTimes(2);
    expect(store.get().clock).toBe(3);
  });
});

describe('the court', () => {
  it('is decoration: aria-hidden, with nothing focusable or readable by a screen reader', () => {
    const { court } = mount();
    expect(court).toHaveAttribute('aria-hidden', 'true');
    expect(court.querySelectorAll('button, a, input, [tabindex]')).toHaveLength(0);
  });

  it('is alive when idle: spotlights, shimmering crowd, a glowing floor and a ball bouncing at centre court', () => {
    const { court } = mount();
    for (const sel of ['.court__lights', '.court__fans', '.court__glow', '.court__idle-bounce']) expect(court.querySelector(sel), sel).not.toBeNull();
    expect(court.querySelector('.court__shooter')).toBeNull();
  });

  it('has the hoop, backboard, net, lane, three-point line and a jumbotron and shot clock', () => {
    const { court } = mount({ diveNumber: 5 });
    for (const sel of ['.court__board-body', '.court__rim-front', '.court__net', '.court__jumbo', '.court__clock-digits']) expect(court.querySelector(sel), sel).not.toBeNull();
    expect(court.querySelectorAll('svg').length).toBeGreaterThanOrEqual(5);
    expect(court.textContent).toContain('NBA DEEP CUT');
    expect(court.textContent).toContain('DIVE #5');
  });

  it('shows the prompt number, the points and the dive on the jumbotron, and the seconds on the shot clock', () => {
    const { court, store } = mount({ phase: 'prompt', promptNumber: 3, total: 7, points: 120, diveNumber: 12, clock: 17 });
    expect(court.querySelector('.court__jumbo-text')?.textContent).toContain('3 / 7');
    expect(court.querySelector('.court__jumbo-text')?.textContent).toContain('#12');
    expect(court.querySelector('.court__clock-digits')?.textContent).toBe('17');
    expect(court.querySelector('.court__clock')).not.toHaveClass('court__clock--danger');
    act(() => store.set({ clock: 5 }));
    expect(court.querySelector('.court__clock')).toHaveClass('court__clock--danger'); // red and pulsing in the last 5 seconds
    act(() => store.set({ clock: 0 }));
    expect(court.querySelector('.court__clock-digits')?.textContent).toBe('00');
  });

  it('has the shooter waiting with the ball while a question is on', () => {
    const { court } = mount({ phase: 'prompt', promptNumber: 1, diveNumber: 1, clock: 25 });
    expect(court.querySelector('.court__shooter--waiting')).not.toBeNull();
    expect(court.querySelector('.court__idle-bounce')).toBeNull();
  });

  it.each(POINTS)('stages the shot for %i points: a shooter and a ball, and the tier name', (points) => {
    const shot = shotForPoints(points);
    const { court } = mount({ phase: 'shot', shot, shotKey: 1, points, promptNumber: 2, diveNumber: 1 });
    expect(court).toHaveAttribute('data-shot', shot.name);
    expect(court.querySelector(`.court__action--${shot.name}`)).not.toBeNull();
    expect(court.querySelector('.court__ball--shot')).not.toBeNull();
    expect(court.querySelector(shot.name === 'dunk' ? '.court__shooter--dunk' : '.court__shooter--shot')).not.toBeNull();
    expect(court.querySelector('.court__label')?.textContent).toContain(shot.label);
    expect(court.querySelector('.court__label')?.textContent).toContain(String(points));
  });

  it('gives the dunk a burst of particles (capped at 40) and a screen shake, and the deep swish and dunk a crowd flash', () => {
    for (const name of SHOT_NAMES) {
      const shot = shotForPoints(POINTS[SHOT_NAMES.indexOf(name)]!);
      const { court, unmount } = mount({ phase: 'shot', shot, shotKey: 1 });
      const particles = court.querySelectorAll('.court__particle').length;
      expect(particles, name).toBe(name === 'dunk' ? 28 : 0);
      expect(particles).toBeLessThanOrEqual(40);
      expect(court.classList.contains('court--shake'), name).toBe(name === 'dunk');
      expect(court.querySelector('.court__flash') !== null, name).toBe(name === 'dunk' || name === 'deep-swish');
      unmount();
    }
    expect(burstVectors(500)).toHaveLength(28);
  });

  it('restarts the animation for every new shot', () => {
    const { court, store } = mount({ phase: 'shot', shot: shotForPoints(55), shotKey: 1 });
    const first = court.querySelector('.court__action');
    act(() => store.set({ shot: shotForPoints(55), shotKey: 2 }));
    expect(court.querySelector('.court__action')).not.toBe(first);
  });

  it('jumps to the end of a skipped shot', () => {
    const { court, store } = mount({ phase: 'shot', shot: shotForPoints(100), shotKey: 1 });
    expect(court).not.toHaveClass('is-skipped');
    act(() => store.set({ skipped: true }));
    expect(court).toHaveClass('is-skipped');
    expect(court.querySelector('.court__action')).toHaveClass('is-skipped');
    expect(court).not.toHaveClass('court--shake');
  });
});

describe('reduced motion', () => {
  it('draws a still court: it is marked reduced', () => {
    const { court } = mount({}, true);
    expect(court).toHaveClass('is-reduced');
  });

  it('has no flight, particles, flash or shake, only the ball at the end of the shot', () => {
    const shot = shotForPoints(100);
    const { court: shotCourt } = mount({ phase: 'shot', shot, shotKey: 1 }, true);
    for (const sel of ['.court__ball--shot', '.court__particle', '.court__flash']) expect(shotCourt.querySelector(sel), sel).toBeNull();
    expect(shotCourt.classList.contains('court--shake')).toBe(false);
    expect(shotCourt.querySelector('.court__still-ball')).not.toBeNull(); // the ball at the end of the shot, and the label, fade in
    expect(shotCourt.querySelector('.court__label')).not.toBeNull();
  });

  it('the stylesheet turns every court animation off, except a plain fade of the label and the ball', () => {
    const css = readFileSync(resolve(process.cwd(), 'src/court/court.css'), 'utf8');
    const block = css.slice(css.indexOf('@media (prefers-reduced-motion: reduce)'));
    expect(block).toMatch(/animation:\s*none !important/);
    expect(block).toMatch(/\.court__particle,\s*\.court__flash\s*{\s*display:\s*none !important/);
    expect(block).toMatch(/court-fade/);
  });

  it('shows the whole replay at once', () => {
    const shots = POINTS.map((p) => shotForPoints(p));
    const { court } = mount({ phase: 'results', replay: shots, replayKey: 1, points: 295, diveNumber: 3 }, true);
    expect(court.querySelector('.court__ball--shot')).toBeNull();
    expect(court.textContent).toContain('295');
  });
});

describe('the replay of a finished dive', () => {
  it('plays the seven shots in order on the court, quickly, then rests', () => {
    vi.useFakeTimers();
    const shots = POINTS.map((p) => shotForPoints(p));
    const { court } = mount({ phase: 'results', replay: shots, replayKey: 1, points: 295, diveNumber: 3 });
    const seen: string[] = [];
    seen.push(court.getAttribute('data-shot') ?? '');
    for (let i = 1; i < 7; i++) {
      act(() => void vi.advanceTimersByTime(REPLAY_STEP_MS));
      seen.push(court.getAttribute('data-shot') ?? '');
    }
    expect(seen).toEqual(shots.map((s) => s.name));
    expect(court.querySelector('.court__action')).toHaveClass('is-fast');
    act(() => void vi.advanceTimersByTime(REPLAY_STEP_MS * 2));
    expect(court.getAttribute('data-shot')).toBe(''); // the sequence is over: the court rests with the total on the jumbotron
    expect(court.querySelector('.court__jumbo-text')?.textContent).toContain('295');
  });

  it('is quick: seven shots in about three and a half seconds', () => {
    expect(REPLAY_STEP_MS * 7).toBeLessThanOrEqual(3600);
  });

  it('skips straight to the end', () => {
    vi.useFakeTimers();
    const shots = POINTS.map((p) => shotForPoints(p));
    const { court, store } = mount({ phase: 'results', replay: shots, replayKey: 1, points: 295, diveNumber: 3 });
    act(() => store.set({ skipped: true }));
    expect(court.getAttribute('data-shot')).toBe('');
  });
});

describe('where the shooter shoots from', () => {
  const distance = (p: { x: number; y: number }): number => Math.hypot(p.x - HOOP.x, p.y - HOOP.y);

  it('is closer for low points and deeper for high points', () => {
    const order = ['clank', 'rattle', 'bank', 'swish', 'deep-swish'] as const; // tiers 1 to 5
    const d = order.map((n) => distance(SPOTS[n]));
    expect(d).toEqual([...d].sort((a, b) => a - b));
    expect(distance(SPOTS['deep-swish'])).toBeGreaterThan(distance(SPOTS.clank) * 2.5);
  });

  it('is inside the picture, on the floor, for every shot', () => {
    for (const name of SHOT_NAMES) {
      expect(SPOTS[name].y).toBeGreaterThan(300);
      expect(SPOTS[name].y).toBeLessThan(640);
      expect(SPOTS[name].x).toBeGreaterThan(150);
      expect(SPOTS[name].x).toBeLessThan(650);
    }
  });

  it('looks bigger the nearer to the viewer', () => {
    expect(depthScale(550)).toBeGreaterThan(depthScale(350));
    expect(hand(SPOTS['deep-swish']).s).toBeGreaterThan(hand(SPOTS.clank).s);
  });

  it('starts every shot from the shooter, with the spot in custom properties', () => {
    const vars = shotVars('deep-swish') as Record<string, string | number>;
    expect(vars['--sx']).toBe(`${SPOTS['deep-swish'].x}px`);
    expect(vars['--nx']).toBe(`${NEUTRAL.x}px`);
  });

  it('draws the court in a picture wider than the court, so a wide strip keeps the hoop', () => {
    expect(VIEWBOX).toBe('-400 0 1600 640');
  });
});

describe('the keyframes', () => {
  it('give every shot a ball flight, with the airball falling off the bottom and the dunk made in the hand', () => {
    const css = ballKeyframes();
    for (const name of [...Object.keys(FLIGHT), 'dunk']) expect(css).toContain(`@keyframes court-ball-${name}`);
    expect(FLIGHT.airball.at(-1)?.y).toBeGreaterThan(640);
    expect(css).toContain('var(--bx)');
    expect(shooterKeyframes()).toContain('court-shooter-dunk');
  });

  it('send the made shots through the hoop and out of the net', () => {
    for (const name of ['rattle', 'bank', 'swish', 'deep-swish'] as const) {
      const points = FLIGHT[name];
      const through = points.find((p) => Math.abs(p.x - HOOP.x) < 8 && Math.abs(p.y - (HOOP.y + 4)) < 10);
      expect(through, name).toBeDefined();
      expect(points.at(-1)!.y).toBeGreaterThan(HOOP.y + 60);
    }
  });

  it('hit the backboard on the clank (its top) and the bank (its square)', () => {
    const clank = FLIGHT.clank.find((p) => p.y > 170 && p.y < 185);
    expect(clank).toBeDefined();
    const bank = FLIGHT.bank.find((p) => p.y >= 212 && p.y <= 250 && Math.abs(p.x - 400) < 30);
    expect(bank).toBeDefined();
  });
});
