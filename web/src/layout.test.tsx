import { act, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import App from './App';
import { SPLIT_MIN_WIDTH, layoutForWidth, useLayout } from './layout';
import { MOCK_OUTSIDE_RANGE_NAMES } from './outsideRange';
import { PROMPTS_PATH, UNIVERSE_PATH, readJson } from './testUtils';

describe('which layout a width gets', () => {
  it('is split from 900 px up and stacked below it', () => {
    expect(SPLIT_MIN_WIDTH).toBe(900);
    for (const w of [900, 901, 1024, 1280, 1920, 2560]) expect(layoutForWidth(w), String(w)).toBe('split');
    for (const w of [0, 320, 360, 414, 768, 899]) expect(layoutForWidth(w), String(w)).toBe('stacked');
  });
});

function mockMedia(initial: boolean) {
  const listeners = new Set<() => void>();
  const query = { matches: initial, addEventListener: (_: string, fn: () => void) => listeners.add(fn), removeEventListener: (_: string, fn: () => void) => listeners.delete(fn) };
  vi.stubGlobal('matchMedia', vi.fn((q: string) => (q.includes('min-width: 900px') ? query : { matches: false, addEventListener: () => undefined, removeEventListener: () => undefined })));
  return (value: boolean) => {
    query.matches = value;
    listeners.forEach((fn) => fn());
  };
}

function Probe() {
  return <p data-testid="layout">{useLayout()}</p>;
}

describe('useLayout', () => {
  afterEach(() => vi.unstubAllGlobals());

  it('starts with the layout of the window and follows it when the window is resized', () => {
    const set = mockMedia(false);
    render(<Probe />);
    expect(screen.getByTestId('layout')).toHaveTextContent('stacked');
    act(() => set(true));
    expect(screen.getByTestId('layout')).toHaveTextContent('split');
    act(() => set(false));
    expect(screen.getByTestId('layout')).toHaveTextContent('stacked');
  });

  it('starts split on a wide window', () => {
    mockMedia(true);
    render(<Probe />);
    expect(screen.getByTestId('layout')).toHaveTextContent('split');
  });

  it('falls back to the window width where matchMedia does not exist', () => {
    vi.stubGlobal('matchMedia', undefined);
    vi.stubGlobal('innerWidth', 1280);
    render(<Probe />);
    expect(screen.getByTestId('layout')).toHaveTextContent('split');
    act(() => {
      vi.stubGlobal('innerWidth', 500);
      window.dispatchEvent(new Event('resize'));
    });
    expect(screen.getByTestId('layout')).toHaveTextContent('stacked');
  });
});

describe('the shell', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn(async (url: string) => {
      const u = String(url);
      return new Response(JSON.stringify(u.endsWith('universe.json') ? readJson(UNIVERSE_PATH) : u.endsWith('outside_range.json') ? MOCK_OUTSIDE_RANGE_NAMES : readJson(PROMPTS_PATH)), { status: 200 });
    }));
  });
  afterEach(() => vi.unstubAllGlobals());

  const show = () => render(<App now={() => new Date('2026-11-04T17:00:00Z')} search="" storage={null} />);

  it('marks the layout, and puts the panel before the chart in the page, so reading starts with the questions', async () => {
    mockMedia(true);
    const { container } = show();
    await screen.findByRole('button', { name: /^Play today/ });
    const shell = container.querySelector('.shell')!;
    expect(shell).toHaveAttribute('data-layout', 'split');
    expect(shell.firstElementChild).toHaveClass('panel');
    expect(shell.lastElementChild).toHaveClass('chart-pane');
  });

  it('is stacked on a phone', async () => {
    mockMedia(false);
    const { container } = show();
    await screen.findByRole('button', { name: /^Play today/ });
    expect(container.querySelector('.shell')).toHaveAttribute('data-layout', 'stacked');
  });

  it('keeps the chart mounted from the first screen: it is the same element on home, how to play and the archive', async () => {
    mockMedia(true);
    show();
    const chart = await screen.findByTestId('chart');
    const { default: userEvent } = await import('@testing-library/user-event');
    const user = userEvent.setup();
    await user.click(await screen.findByRole('button', { name: 'Archive' }));
    expect(await screen.findByRole('heading', { name: 'Archive' })).toBeInTheDocument();
    expect(screen.getByTestId('chart')).toBe(chart);
    expect(chart).toHaveAttribute('data-phase', 'idle');
    await user.click(screen.getByRole('button', { name: 'Back' }));
    await user.click(await screen.findByRole('button', { name: 'How to play' }));
    expect(screen.getByTestId('chart')).toBe(chart);
    await user.click(screen.getByRole('button', { name: 'Back' }));
    await user.click(await screen.findByRole('button', { name: /^Play today/ }));
    await screen.findByRole('combobox');
    expect(screen.getByTestId('chart')).toBe(chart);
    expect(chart).toHaveAttribute('data-phase', 'prompt');
  });

  it('hides the picture from assistive technology: it is decoration, the panel has every word (a live line says the result)', async () => {
    show();
    const chart = await screen.findByTestId('chart');
    expect(chart.querySelector('svg')).toHaveAttribute('aria-hidden', 'true');
    expect(chart.closest('.chart-pane')).not.toBeNull();
    expect(screen.queryByRole('main')?.contains(chart)).toBe(false);
  });
});
