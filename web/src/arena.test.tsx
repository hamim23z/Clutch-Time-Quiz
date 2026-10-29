import { act, render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import AnimationsPage from './AnimationsPage';
import App from './App';
import { STRONG_SHARE } from './components/Final';
import { MAX_DIVE_POINTS } from './tiers';
import { divePrompts } from './schedule';
import { SHOT_NAMES } from './shots';
import type { StorageLike } from './storage';
import { MOCK_OUTSIDE_RANGE_NAMES } from './outsideRange';
import { PROMPTS_PATH, UNIVERSE_PATH, mockPrompts, readJson } from './testUtils';
import type { Prompt } from './types';

const LAUNCH = new Date('2026-11-03T17:00:00Z');
const dive = (): Prompt[] => divePrompts(mockPrompts(), 1);

const memory = (): StorageLike => {
  const data = new Map<string, string>();
  return { getItem: (k) => data.get(k) ?? null, setItem: (k, v) => void data.set(k, v) };
};

beforeEach(() => {
  vi.useFakeTimers({ shouldAdvanceTime: true });
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const u = String(url);
    const body = u.endsWith('universe.json') ? readJson(UNIVERSE_PATH) : u.endsWith('outside_range.json') ? MOCK_OUTSIDE_RANGE_NAMES : readJson(PROMPTS_PATH);
    return new Response(JSON.stringify(body), { status: 200 });
  }));
});
afterEach(() => {
  vi.useRealTimers();
  vi.unstubAllGlobals();
});

const setup = () => userEvent.setup({ advanceTimers: vi.advanceTimersByTime });
type User = ReturnType<typeof setup>;

async function begin(user: User, storage: StorageLike | null = memory()) {
  const r = render(<App now={() => LAUNCH} search="" storage={storage} />);
  await user.click(await screen.findByRole('button', { name: 'Play' }));
  await screen.findByRole('combobox');
  return r;
}
const answer = async (user: User, text: string) => {
  await user.type(screen.getByRole('combobox'), text);
  await user.keyboard('{Enter}');
};
const announcer = () => screen.getByTestId('announcer').textContent ?? '';

describe('the scoreboard', () => {
  it('shows the prompt number, the points and the dive number', async () => {
    const user = setup();
    await begin(user);
    const board = screen.getByRole('group', { name: 'Scoreboard' });
    expect(within(board).getByText('Prompt')).toBeInTheDocument();
    expect(within(board).getByText('Dive')).toBeInTheDocument();
    expect(within(board).getByText('#1')).toBeInTheDocument();
    expect(screen.getByText(/Prompt 1 of 7/)).toBeInTheDocument();
    expect(screen.getByTestId('scoreboard-points')).toHaveTextContent('0');
  });

  it('rolls the new points in after the shot', async () => {
    const user = setup();
    await begin(user);
    const first = dive()[0]!.answers[0]!;
    await answer(user, first.name);
    await screen.findByRole('heading', { level: 3, name: /points/ });
    expect(screen.getByTestId('scoreboard-points')).toHaveTextContent('0'); // before the roll
    await act(async () => void vi.advanceTimersByTime(2500));
    expect(screen.getByTestId('scoreboard-points')).toHaveTextContent(String(first.points));
  });
});

describe('the shot after an answer', () => {
  it('plays the shot for the tier and shows the points and the tier name', async () => {
    const user = setup();
    await begin(user);
    const first = dive()[0]!.answers[0]!;
    await answer(user, first.name);
    await screen.findByRole('heading', { level: 3, name: /points/ });
    const reveal = document.querySelector('.reveal')!;
    expect(reveal.querySelector('.shot')).not.toBeNull();
    expect(reveal.querySelector('.shot-label')).toHaveTextContent(String(first.points));
  });

  it('announces the points and the tier name when an answer is submitted', async () => {
    const user = setup();
    await begin(user);
    const first = dive()[0]!.answers[0]!;
    await answer(user, first.name);
    await screen.findByRole('heading', { level: 3, name: /points/ });
    const said = announcer();
    expect(said).toContain(`Tier ${first.tier}: ${first.points} points`);
    expect(said).toMatch(/Garbage time|Bench mob|Starting five|All-Star|Buzzer beater|Poster dunk/);
  });

  it('announces a miss as an airball', async () => {
    const user = setup();
    await begin(user);
    await answer(user, 'qwerty zxcv');
    await screen.findByRole('heading', { level: 3, name: /0 points/ });
    expect(announcer()).toContain('Not a valid answer: 0 points. Airball.');
    expect(document.querySelector('.shot--airball')).not.toBeNull();
  });

  it('an outside-the-range name is a gentle airball, with a shake of the message', async () => {
    const user = setup();
    await begin(user);
    await answer(user, 'Orson Quillfeather');
    const heading = await screen.findByRole('heading', { level: 3, name: 'Outside the data range' });
    expect(heading).toHaveClass('shake');
    expect(document.querySelector('.shot--airball')).not.toBeNull();
    expect(screen.getByText(/does not count against you/i)).toBeInTheDocument();
  });

  it('a tap or Enter skips the shot; the Next button, typing and focus keep working', async () => {
    const user = setup();
    await begin(user);
    await answer(user, dive()[0]!.answers[0]!.name);
    await screen.findByRole('heading', { level: 3, name: /points/ });
    const reveal = document.querySelector('.reveal')!;
    expect(reveal).not.toHaveClass('is-skipped');
    await user.keyboard('{Enter}');
    expect(reveal).toHaveClass('is-skipped');
    // the next prompt is not skipped, and its input takes focus and typing at once
    await user.click(screen.getByRole('button', { name: 'Next prompt' }));
    const input = await screen.findByRole('combobox');
    expect(input).toHaveFocus();
    await user.type(input, 'abc');
    expect(input).toHaveValue('abc');
  });

  it('skips on a tap too', async () => {
    const user = setup();
    await begin(user);
    await answer(user, 'qwerty zxcv');
    await screen.findByRole('heading', { level: 3, name: /points/ });
    const reveal = document.querySelector('.reveal')!;
    await user.pointer({ target: reveal.querySelector('.reveal__stage')!, keys: '[MouseLeft]' });
    expect(reveal).toHaveClass('is-skipped');
  });

  it('a skipped shot puts the points on the scoreboard at once', async () => {
    const user = setup();
    await begin(user);
    const first = dive()[0]!.answers[0]!;
    await answer(user, first.name);
    await screen.findByRole('heading', { level: 3, name: /points/ });
    await user.keyboard('{Enter}');
    expect(screen.getByTestId('scoreboard-points')).toHaveTextContent(String(first.points));
  });
});

describe('the input', () => {
  it('shakes when a name needs disambiguation, and the message stays gentle', async () => {
    const user = setup();
    await begin(user);
    await answer(user, 'Dex Marrow');
    expect(screen.getByText(/could be Dex Marrow/)).toBeInTheDocument();
    expect(document.querySelector('.answer__row')).toHaveClass('shake');
    expect(screen.getByRole('combobox')).toHaveFocus(); // the shake never takes focus away
  });
});

describe('reduced motion', () => {
  it('replaces the shot with the still hoop: no ball, no player, no particles, and the label is still there', async () => {
    vi.stubGlobal('matchMedia', vi.fn(() => ({ matches: true, addEventListener: () => undefined, removeEventListener: () => undefined })));
    const user = setup();
    await begin(user);
    await answer(user, dive()[0]!.answers[0]!.name);
    await screen.findByRole('heading', { level: 3, name: /points/ });
    const reveal = document.querySelector('.reveal')!;
    expect(reveal).toHaveClass('is-reduced');
    for (const sel of ['.shot__ball', '.shot__player', '.particle', '.shot__crowd']) expect(reveal.querySelector(sel)).toBeNull();
    expect(reveal.querySelector('.shot-label')).not.toBeNull();
    expect(announcer()).toMatch(/points\./); // still announced
    expect(screen.getByTestId('scoreboard-points')).not.toHaveTextContent(/^$/);
  });

  it('shows the results at once, with no confetti', async () => {
    vi.stubGlobal('matchMedia', vi.fn(() => ({ matches: true, addEventListener: () => undefined, removeEventListener: () => undefined })));
    const user = setup();
    await begin(user);
    for (let i = 0; i < 7; i++) {
      const rarest = [...dive()[i]!.answers].sort((a, b) => b.tier - a.tier)[0]!;
      await answer(user, rarest.name);
      await screen.findByRole('heading', { level: 3, name: /points/ });
      await user.click(screen.getByRole('button', { name: i === 6 ? 'See results' : 'Next prompt' }));
    }
    expect(document.querySelector('.final__show')).toHaveClass('is-reduced');
    expect(document.querySelector('.confetti')).toBeNull();
  });
});

async function playWith(user: User, pick: (p: Prompt) => string): Promise<number> {
  let total = 0;
  for (let i = 0; i < 7; i++) {
    const p = dive()[i]!;
    const name = pick(p);
    total += p.answers.find((a) => a.name === name)?.points ?? 0;
    await answer(user, name);
    await screen.findByRole('heading', { level: 3, name: /points/ });
    await user.click(screen.getByRole('button', { name: i === 6 ? 'See results' : 'Next prompt' }));
  }
  return total;
}

describe('the results screen', () => {
  it('plays back seven mini courts colored by tier, then the total', async () => {
    const user = setup();
    await begin(user);
    await playWith(user, (p) => p.answers[0]!.name);
    const squares = within(screen.getByRole('list', { name: 'Your seven answers' })).getAllByRole('listitem');
    expect(squares).toHaveLength(7);
    for (const s of squares) {
      expect(s.querySelector('svg.court-icon')).not.toBeNull();
      expect(s.className).toMatch(/square--(t[1-6]|miss)/);
    }
    // staggered: each square starts a little later than the one before
    expect(squares.map((s) => s.getAttribute('style'))).toEqual(squares.map((_, i) => expect.stringContaining(`--i: ${i}`)));
  });

  it('throws confetti only for a strong total (at least 60% of the maximum)', async () => {
    expect(STRONG_SHARE).toBe(0.6);
    const user = setup();
    await begin(user);
    const strong = await playWith(user, (p) => [...p.answers].sort((a, b) => b.points - a.points)[0]!.name);
    const confetti = document.querySelector('.confetti') !== null;
    expect(confetti).toBe(strong >= STRONG_SHARE * MAX_DIVE_POINTS);
  });

  it('has no confetti for a weak total', async () => {
    const user = setup();
    await begin(user);
    for (let i = 0; i < 7; i++) {
      await answer(user, 'qwerty zxcv');
      await screen.findByRole('heading', { level: 3, name: /points/ });
      await user.click(screen.getByRole('button', { name: i === 6 ? 'See results' : 'Next prompt' }));
    }
    expect(document.querySelector('.confetti')).toBeNull();
    expect(screen.queryByText(/strong dive/i)).not.toBeInTheDocument();
  });

  it('has a replay button that plays the seven shots again', async () => {
    const user = setup();
    await begin(user);
    await playWith(user, (p) => p.answers[0]!.name);
    const before = document.querySelector('.final__show');
    await user.click(screen.getByRole('button', { name: 'Replay the shots' }));
    const after = document.querySelector('.final__show');
    expect(after).not.toBeNull();
    expect(after).not.toBe(before); // a fresh element restarts every animation
    expect(within(screen.getByRole('list', { name: 'Your seven answers' })).getAllByRole('listitem')).toHaveLength(7);
    expect(screen.getByLabelText(/^Total \d+ out of 700$/)).toBeInTheDocument();
  });

  it('shows the streak, popping because it just went up, and again on the home screen', async () => {
    const user = setup();
    await begin(user);
    await playWith(user, (p) => p.answers[0]!.name);
    const streak = screen.getByTestId('final-streak');
    expect(streak).toHaveTextContent('1 day');
    expect(streak).toHaveClass('streak-badge--pop');
    await user.click(screen.getByRole('button', { name: /^Home$/ }));
    expect(screen.getByTestId('streak-current')).toHaveClass('streak-badge--pop');
  });

  it('does not pop the streak when the home screen just opens', async () => {
    render(<App now={() => LAUNCH} search="" storage={memory()} />);
    expect(await screen.findByTestId('streak-current')).not.toHaveClass('streak-badge--pop');
  });
});

describe('the sound toggle', () => {
  it('is in the header, off by default, and turning it on is remembered', async () => {
    const user = setup();
    const store = memory();
    const first = render(<App now={() => LAUNCH} search="" storage={store} />);
    const toggle = await screen.findByRole('button', { name: /Sound off/ });
    expect(toggle).toHaveAttribute('aria-pressed', 'false');
    await user.click(toggle);
    expect(screen.getByRole('button', { name: /Sound on/ })).toHaveAttribute('aria-pressed', 'true');
    expect(store.getItem('deepcut.sound')).toBe('on');
    first.unmount();
    render(<App now={() => LAUNCH} search="" storage={store} />);
    expect(await screen.findByRole('button', { name: /Sound on/ })).toBeInTheDocument();
  });

  it('works with no storage', async () => {
    const user = setup();
    render(<App now={() => LAUNCH} search="" storage={null} />);
    await user.click(await screen.findByRole('button', { name: /Sound off/ }));
    expect(screen.getByRole('button', { name: /Sound on/ })).toBeInTheDocument();
  });
});

describe('the animation review page', () => {
  it('shows every shot, and a reduced-motion version on request', async () => {
    const user = setup();
    render(<AnimationsPage />);
    for (const name of SHOT_NAMES) expect(screen.getByTestId(`demo-${name}`)).toBeInTheDocument();
    expect(document.querySelectorAll('.shot__ball')).toHaveLength(7);
    await user.click(screen.getByRole('checkbox', { name: /reduced-motion/i }));
    expect(document.querySelectorAll('.shot__ball')).toHaveLength(0);
    expect(document.querySelectorAll('.is-reduced').length).toBeGreaterThanOrEqual(7);
  });

  it('loops: the demos are replayed after a while', async () => {
    render(<AnimationsPage />);
    const first = screen.getByTestId('demo-dunk');
    await act(async () => void vi.advanceTimersByTime(3500));
    expect(screen.getByTestId('demo-dunk')).not.toBe(first);
  });
});
