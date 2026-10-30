import { render, screen, within } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import App from './App';
import { Home } from './components/Home';
import { Wordmark } from './components/Wordmark';
import { MOCK_OUTSIDE_RANGE_NAMES } from './outsideRange';
import { PROMPTS_PATH, UNIVERSE_PATH, readJson } from './testUtils';

describe('the wordmark', () => {
  it('is the page heading, read as "NBA Deep Cut", with the letters as decoration', () => {
    const { container } = render(<Wordmark />);
    const h1 = screen.getByRole('heading', { level: 1, name: 'NBA Deep Cut' });
    expect(h1).toBeInTheDocument();
    const letters = container.querySelectorAll('.wordmark__letter');
    expect(letters).toHaveLength(10); // N B A D E E P C U T
    expect([...letters].map((l) => l.textContent).join('')).toBe('NBADEEPCUT');
    letters.forEach((l, i) => expect(l.getAttribute('style')).toContain(`--i: ${i}`)); // each drops a little after the one before
  });
});

describe('the home screen', () => {
  const props = { number: 12, played: false, streaks: { current: 3, best: 5 }, streakUp: false, saving: true, onPlay: vi.fn(), onResults: vi.fn(), onArchive: vi.fn(), onHowTo: vi.fn() };

  it('has the wordmark, a tagline, a big play button, archive, how to play, and both streaks', () => {
    render(<Home {...props} />);
    expect(screen.getByRole('heading', { level: 1 })).toBeInTheDocument();
    expect(screen.getByText(/daily basketball trivia game where the obvious answer loses/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^Play today.s dive$/ })).toHaveClass('primary--big');
    expect(screen.getByRole('button', { name: 'Archive' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'How to play' })).toBeInTheDocument();
    expect(screen.getByTestId('streak-current')).toHaveTextContent('3 days');
    expect(screen.getByTestId('streak-best')).toHaveTextContent('5 days');
    expect(screen.getByText('#12')).toBeInTheDocument();
  });

  it('offers View results instead of Play when today is already played', () => {
    render(<Home {...props} played />);
    expect(screen.getByRole('button', { name: 'View results' })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /^Play today/ })).not.toBeInTheDocument();
  });

  it('uses text only: no images, no logos', () => {
    const { container } = render(<Home {...props} />);
    expect(container.querySelectorAll('img, image, picture')).toHaveLength(0);
  });
});

describe('every screen', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn(async (url: string) => {
      const u = String(url);
      return new Response(JSON.stringify(u.endsWith('universe.json') ? readJson(UNIVERSE_PATH) : u.endsWith('outside_range.json') ? MOCK_OUTSIDE_RANGE_NAMES : readJson(PROMPTS_PATH)), { status: 200 });
    }));
  });
  afterEach(() => vi.unstubAllGlobals());

  it('says it is an unofficial fan game, on the home screen and elsewhere', async () => {
    const { default: userEvent } = await import('@testing-library/user-event');
    const user = userEvent.setup();
    render(<App now={() => new Date('2026-11-04T17:00:00Z')} search="" storage={null} />);
    const home = await screen.findByRole('button', { name: /^Play today/ });
    expect(home).toBeInTheDocument();
    expect(screen.getByText('Unofficial fan game. Not affiliated with the NBA.')).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'Archive' }));
    expect(within(document.querySelector('main')!).getByText('Unofficial fan game. Not affiliated with the NBA.')).toBeInTheDocument();
  });

  it('has exactly one h1: the wordmark on home, a hidden one on the other screens', async () => {
    const { default: userEvent } = await import('@testing-library/user-event');
    const user = userEvent.setup();
    render(<App now={() => new Date('2026-11-04T17:00:00Z')} search="" storage={null} />);
    await screen.findByRole('button', { name: /^Play today/ });
    expect(screen.getAllByRole('heading', { level: 1 })).toHaveLength(1);
    expect(screen.getByRole('heading', { level: 1 })).toHaveAccessibleName('NBA Deep Cut');
    await user.click(screen.getByRole('button', { name: 'Archive' }));
    expect(screen.getAllByRole('heading', { level: 1 })).toHaveLength(1);
  });
});
