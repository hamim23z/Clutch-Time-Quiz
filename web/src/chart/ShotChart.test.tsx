import { act, render, screen } from '@testing-library/react';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { capitalizeFirst, PromptText } from '../components/PromptText';
import { ReducedMotionOverride } from '../motion';
import { shotForPoints } from '../shots';
import { TIER_POINTS } from '../tiers';
import type { Tier } from '../types';
import { ChartProvider, INITIAL_CHART, createChartStore, type ChartMark } from './chartStore';
import { BANDS, HOOP, TIER_COLORS, TIER_INK } from './placement';
import ShotChart, { REPLAY_STEP_MS, flightMs } from './ShotChart';

const marksOf = (tiers: Array<Tier | null>): ChartMark[] => tiers.map((tier, i) => ({ id: `p-${i}`, tier }));

function mount(patch = {}, reduced: boolean | null = null) {
  const store = createChartStore({ ...INITIAL_CHART, ...patch });
  const view = render(
    <ChartProvider store={store}>
      <ReducedMotionOverride.Provider value={reduced}>
        <ShotChart />
      </ReducedMotionOverride.Provider>
    </ChartProvider>,
  );
  return { store, ...view, chart: screen.getByTestId('chart'), svg: view.container.querySelector('svg')! };
}

afterEach(() => vi.useRealTimers());

describe('the shot chart', () => {
  it('is one inline SVG in a 688 x 860 view with no raster images, hidden from assistive technology', () => {
    const { svg, container } = mount();
    expect(svg).toHaveAttribute('viewBox', '0 0 688 860');
    expect(svg).toHaveAttribute('aria-hidden', 'true');
    expect(container.querySelectorAll('img, image, foreignObject')).toHaveLength(0);
    expect(svg.textContent).toContain('SHOT CHART');
    expect(svg.textContent).toContain('Rarer answer = deeper shot.');
    expect(svg.textContent).toContain('AIRBALL ZONE');
  });

  it('draws the half court: hoop, backboard, lane, three-point line, circles and the court rectangle', () => {
    const { svg } = mount();
    expect(svg.querySelector('circle[r="8.4"][stroke="#FF6A13"]')).not.toBeNull();
    expect(svg.querySelector('line[y1="148.8"][x1="342.4"][x2="409.6"]')).toHaveAttribute('stroke-width', '5');
    expect(svg.querySelector('rect[x="96"][y="104"][width="560"][height="526.4"]')).not.toBeNull();
    expect(svg.querySelector('rect[x="286.4"][y="104"][width="179.2"][height="212.8"]')).not.toBeNull();
    expect(svg.innerHTML).toContain('M129.6 104V263A266 266 0 0 0 622.4 263V104');
    expect(svg.innerHTML).toContain('A67.2 67.2 0 0 1 443.2 316.8'); // free-throw circle, top half
    expect(svg.querySelector('path[stroke-dasharray="10 9"]')).not.toBeNull(); // bottom half dashed
  });

  it('has one zone circle and one dashed ring per tier band, centred on the hoop', () => {
    const { svg } = mount();
    for (const t of [1, 2, 3, 4, 5, 6] as Tier[]) {
      expect(svg.querySelector(`circle[cx="${HOOP.x}"][cy="${HOOP.y}"][r="${BANDS[t][1]}"][stroke-dasharray]`), `ring ${t}`).not.toBeNull();
    }
  });

  it('puts a depth gauge on the left with a tick at every band boundary, a square and the points for each tier', () => {
    const { svg } = mount();
    const gauge = svg.querySelector('.chart__gauge')!;
    const tickYs = [...gauge.querySelectorAll('line')].map((l) => Number(l.getAttribute('y1'))).filter((_, i) => i > 0);
    expect(tickYs).toEqual([0, 112, 190.4, 266, 358.4, 440, 467].map((d) => HOOP.y + d)); // a tick at every band boundary
    for (const t of [1, 2, 3, 4, 5, 6] as Tier[]) {
      const g = gauge.querySelector(`[data-tier="${t}"]`)!;
      expect(g.querySelector('rect')).toHaveAttribute('fill', TIER_COLORS[t]);
      expect(g.textContent).toContain(String(t));
      expect(g.textContent).toContain(String(TIER_POINTS[t]));
      const mid = HOOP.y + (BANDS[t][0] + BANDS[t][1]) / 2;
      const y = Number(g.querySelector('rect')!.getAttribute('y')) + 12;
      expect(y).toBeCloseTo(mid, 5); // the square sits in the middle of its band
      expect(y).toBeGreaterThan(HOOP.y + BANDS[t][0]);
      expect(y).toBeLessThan(HOOP.y + BANDS[t][1]);
    }
  });

  it('shows, on the home screen, no markers, a ball at the bottom and the dive in a box over the court', () => {
    const { svg, chart } = mount({ diveNumber: 5 });
    expect(svg.querySelectorAll('.chart__mark')).toHaveLength(0);
    expect(svg.querySelector('.chart__rest')).not.toBeNull();
    expect(svg.querySelector('.chart__idle')?.textContent).toContain("TODAY'S DIVE #5");
    expect(svg.querySelector('.chart__idle')?.textContent).toContain('7 PROMPTS');
    expect(chart).toHaveAttribute('data-phase', 'idle');
  });

  it('shows the clock and the points from the store, and nothing of its own', () => {
    const { store, svg } = mount({ phase: 'prompt', clock: 17, points: 120, promptNumber: 3 });
    expect(screen.getByTestId('chart-clock')).toHaveTextContent('17');
    expect(screen.getByTestId('chart-points')).toHaveTextContent('120');
    act(() => store.set({ clock: 4, points: 135 }));
    expect(screen.getByTestId('chart-clock')).toHaveTextContent('04');
    expect(screen.getByTestId('chart-clock')).toHaveClass('chart__value--danger');
    expect(screen.getByTestId('chart-points')).toHaveTextContent('135');
    expect(svg.querySelector('.chart__idle')).toBeNull();
  });

  it('shows one square per answer with the tier number in it, and the stats strip', () => {
    const { svg } = mount({ phase: 'prompt', marks: marksOf([3, 6, null, 1]), points: 145 });
    const squares = [...svg.querySelectorAll('.chart__mark')];
    expect(squares).toHaveLength(4);
    expect(squares.map((m) => m.getAttribute('data-tier'))).toEqual(['3', '6', 'miss', '1']);
    expect(svg.querySelectorAll('.chart__num')).toHaveLength(3);
    expect(squares[2]!.querySelector('.chart__x')).not.toBeNull();
    expect(squares[0]!.querySelectorAll('.chart__spoke')).toHaveLength(1); // a dashed line from the hoop
    expect(squares[2]!.querySelectorAll('.chart__spoke')).toHaveLength(0);
    expect(screen.getByTestId('chart-strip-shots')).toHaveTextContent('3 / 4');
    expect(screen.getByTestId('chart-strip-points')).toHaveTextContent('145');
    expect(screen.getByTestId('chart-strip-best-shot')).toHaveTextContent('T6 · 100');
  });

  it.each([1, 2, 3, 4, 5, 6] as Tier[])('plays a tier %i answer: the ball flies, the marker pops in after it lands, and the zone pulses', (tier) => {
    const shot = shotForPoints(TIER_POINTS[tier]);
    const { svg, chart } = mount({ phase: 'shot', shot, shotKey: 1, marks: marksOf([tier]), points: TIER_POINTS[tier] });
    expect(chart).toHaveAttribute('data-tier', String(tier));
    expect(svg.querySelector('.chart__fly-y')).not.toBeNull();
    expect(svg.querySelector('.chart__pulse')).not.toBeNull();
    const mark = svg.querySelector<SVGGElement>('.chart__mark')!;
    expect(mark).toHaveClass('chart__mark--in');
    expect(mark.style.getPropertyValue('--delay')).toBe(`${flightMs(tier)}ms`); // it appears when the ball arrives
    expect(svg.querySelector('.chart__ring')).not.toBeNull(); // the latest answer has the dashed ring
    expect(svg.querySelector('.chart__stamp') !== null).toBe(tier === 6);
    expect(svg.querySelector('.chart__heat') !== null).toBe(tier === 6);
    expect(TIER_INK[tier]).toBeTruthy();
  });

  it('gives a rarer tier a longer flight and a bigger pop', () => {
    const times = ([1, 2, 3, 4, 5, 6] as Tier[]).map(flightMs);
    expect(times).toEqual([...times].sort((a, b) => a - b));
    expect(flightMs(1)).toBeGreaterThanOrEqual(500);
    expect(flightMs(6)).toBeLessThanOrEqual(1000);
    const peaks = ([1, 6] as Tier[]).map((tier) => {
      const { svg, unmount } = mount({ phase: 'shot', shot: shotForPoints(TIER_POINTS[tier]), shotKey: 1, marks: marksOf([tier]) });
      const peak = Number(svg.querySelector<SVGGElement>('.chart__mark')!.style.getPropertyValue('--peak'));
      unmount();
      return peak;
    });
    expect(peaks[1]).toBeGreaterThan(peaks[0]!);
  });

  it('drops a wrong answer short: the ball bounces in the airball zone and an X appears', () => {
    const { svg, chart } = mount({ phase: 'shot', shot: shotForPoints(0), shotKey: 1, marks: marksOf([null]) });
    expect(chart).toHaveAttribute('data-tier', 'miss');
    expect(svg.querySelector('.chart__fly-y--miss')).not.toBeNull();
    expect(svg.querySelector('.chart__mark .chart__x')).not.toBeNull();
    expect(svg.querySelector('.chart__pulse')).toBeNull();
    expect(svg.querySelector('.chart__stamp')).toBeNull();
  });

  it('restarts the animation for every new shot', () => {
    const { store, svg } = mount({ phase: 'shot', shot: shotForPoints(55), shotKey: 1, marks: marksOf([4]) });
    const first = svg.querySelector('.chart__mark');
    act(() => store.set({ shotKey: 2 }));
    expect(svg.querySelector('.chart__mark')).not.toBe(first);
  });

  it('does not re-animate earlier answers when a new prompt appears', () => {
    const { store, svg } = mount({ phase: 'shot', shot: shotForPoints(55), shotKey: 1, marks: marksOf([4]) });
    act(() => store.set({ phase: 'prompt', shot: null, marks: marksOf([4]) }));
    expect(svg.querySelector('.chart__mark')).not.toHaveClass('chart__mark--in');
    expect(svg.querySelector('.chart__fly-y')).toBeNull();
    expect(svg.querySelector('.chart__ring')).toBeNull();
  });

  it('jumps to the end of a skipped shot', () => {
    const { store, chart } = mount({ phase: 'shot', shot: shotForPoints(55), shotKey: 1, marks: marksOf([4]) });
    act(() => store.set({ skipped: true }));
    expect(chart).toHaveClass('is-skipped');
  });

  it('shows all seven on the results screen, popping in one after another, and rests with the total', () => {
    const tiers: Array<Tier | null> = [1, 2, null, 4, 5, 6, 3];
    const { svg, chart } = mount({ phase: 'results', marks: marksOf(tiers), points: 195, replayKey: 1, diveNumber: 3 });
    const marks = [...svg.querySelectorAll<SVGGElement>('.chart__mark')];
    expect(marks).toHaveLength(7);
    expect(marks.map((m) => m.style.getPropertyValue('--delay'))).toEqual(tiers.map((_, i) => `${i * REPLAY_STEP_MS}ms`));
    expect(chart).toHaveAttribute('data-phase', 'results');
    expect(screen.getByTestId('chart-strip-shots')).toHaveTextContent('6 / 7');
  });
});

describe('reduced motion', () => {
  it('has no flight, pulse, flash or stamp: the marker only fades in', () => {
    const { svg, chart } = mount({ phase: 'shot', shot: shotForPoints(100), shotKey: 1, marks: marksOf([6]) }, true);
    expect(chart).toHaveClass('is-reduced');
    for (const sel of ['.chart__fly-x', '.chart__pulse', '.chart__heat', '.chart__stamp', '.chart__pts-flash']) expect(svg.querySelector(sel), sel).toBeNull();
    const mark = svg.querySelector<SVGGElement>('.chart__mark')!;
    expect(mark.style.getPropertyValue('--delay')).toBe('0ms');
    expect(svg.querySelector('.chart__rest--late')).toBeNull();
  });

  it('is set in the stylesheet too, and only transform and opacity ever animate', () => {
    const css = readFileSync(resolve(process.cwd(), 'src/chart/chart.css'), 'utf8');
    const block = css.slice(css.indexOf('@media (prefers-reduced-motion: reduce)'));
    expect(block).toMatch(/animation:\s*none !important/);
    expect(block).toMatch(/chart-fade/);
    for (const m of css.matchAll(/@keyframes [\w-]+ \{([\s\S]*?)\n\}/g)) {
      for (const prop of m[1]!.matchAll(/([\w-]+):/g)) expect(['opacity', 'transform', 'animation-timing-function']).toContain(prop[1]);
    }
  });
});

describe('what a screen reader hears', () => {
  it('says the result in a polite live region outside the picture', () => {
    const { store, svg } = mount({ phase: 'shot', shot: shotForPoints(35), shotKey: 1, marks: marksOf([3]), points: 35 });
    const live = screen.getByTestId('chart-live');
    expect(live).toHaveAttribute('aria-live', 'polite');
    expect(live).toHaveClass('visually-hidden');
    expect(svg.contains(live)).toBe(false);
    expect(live).toHaveTextContent('Tier 3, 35 points, 35 total');
    act(() => store.set({ shotKey: 2, marks: marksOf([3, null]), points: 35, shot: shotForPoints(0) }));
    expect(live).toHaveTextContent('Airball, 0 points, 35 total');
    act(() => store.set({ phase: 'prompt' }));
    expect(live).toHaveTextContent('');
  });
});

describe('the question text', () => {
  it('shows its first letter in capitals, and leaves the data and the matcher alone', () => {
    const text = 'Since 2001-02 (through 2025-26), name a player who scored 40 or more points.';
    const { container } = render(<PromptText text={text} />);
    expect(container.textContent).toBe('Since 2001-02 (through 2025-26), Name a player who scored 40 or more points.');
    expect(text).toContain('), name a player'); // the string itself is untouched
  });

  it('capitalises a text that has no era too, and never changes anything else', () => {
    expect(capitalizeFirst('name a team')).toBe('Name a team');
    expect(capitalizeFirst('Name a team')).toBe('Name a team');
    expect(capitalizeFirst('')).toBe('');
    expect(capitalizeFirst('3-point shooters')).toBe('3-point shooters');
    const { container } = render(<PromptText text="name a team that won." />);
    expect(container.textContent).toBe('Name a team that won.');
  });
});

describe('the look of the chart', () => {
  const css = readFileSync(resolve(process.cwd(), 'src/chart/chart.css'), 'utf8').replace(/\/\*[\s\S]*?\*\//g, '');
  const source = readFileSync(resolve(process.cwd(), 'src/chart/ShotChart.tsx'), 'utf8');

  it('is flat: no gradients, blur, filters, glow, shadows or rounded corners', () => {
    expect(css).not.toMatch(/gradient|blur\(|filter|drop-shadow|box-shadow|text-shadow|border-radius|backdrop|clip-path/);
    expect(source).not.toMatch(/Gradient|feGaussianBlur|filter=|rx=|ry=|clip-path: polygon/);
  });

  it('uses the palette and the two fonts, and loads no image', () => {
    expect(source).not.toMatch(/\.png|\.jpg|\.svg'|import .* from '\.\.\/assets/);
    expect(css).toMatch(/var\(--font-display\)/);
    expect(css).toMatch(/var\(--font-body\)/);
  });
});
