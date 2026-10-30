import { render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import App from './App';
import { LAUNCH_DATE, TIME_ZONE } from './config';
import { MOCK_OUTSIDE_RANGE_NAMES } from './outsideRange';
import { PROMPTS_PATH, UNIVERSE_PATH, readJson } from './testUtils';

beforeEach(() => {
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const u = String(url);
    const body = u.endsWith('universe.json') ? readJson(UNIVERSE_PATH) : u.endsWith('outside_range.json') ? MOCK_OUTSIDE_RANGE_NAMES : readJson(PROMPTS_PATH);
    return new Response(JSON.stringify(body), { status: 200 });
  }));
});
afterEach(() => vi.unstubAllGlobals());

const show = (iso: string, search = '') => render(<App now={() => new Date(iso)} search={search} storage={null} />);

describe('launch day', () => {
  it('has one launch date, in one config file, in New York time', () => {
    expect(LAUNCH_DATE).toBe('2026-11-03');
    expect(TIME_ZONE).toBe('America/New_York');
  });

  it('shows the coming-soon screen up to the last second before midnight in New York', async () => {
    show('2026-11-03T04:59:59Z');
    expect(await screen.findByRole('heading', { name: 'Coming soon' })).toBeInTheDocument();
    expect(screen.getByText('3 November 2026')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Play' })).not.toBeInTheDocument();
  });

  it('opens dive #1 at midnight in New York', async () => {
    show('2026-11-03T05:00:00Z');
    expect(await screen.findByRole('button', { name: 'Play' })).toBeInTheDocument();
    expect(screen.getByText('#1')).toBeInTheDocument();
  });

  it('is dive #2 the next New York day, and still #1 at 11:59 pm on launch day', async () => {
    const { unmount } = show('2026-11-04T04:59:59Z');
    expect(await screen.findByText('#1')).toBeInTheDocument();
    unmount();
    show('2026-11-04T05:00:00Z');
    expect(await screen.findByText('#2')).toBeInTheDocument();
  });

  it('shows coming soon before the launch, and the preview play-test works with ?preview=1', async () => {
    const { unmount } = show('2026-10-29T12:00:00Z');
    expect(await screen.findByRole('heading', { name: 'Coming soon' })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Play-test' })).not.toBeInTheDocument();
    unmount();
    show('2026-10-29T12:00:00Z', '?preview=1');
    expect(await screen.findByRole('button', { name: 'Play-test' })).toBeInTheDocument();
  });
});
