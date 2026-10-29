import { act, render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import App from './App';
import { pickDive } from './dive';
import { matchAnswer } from './matching';
import { PROMPTS_PATH, UNIVERSE_PATH, mockIndex, mockPrompts, mockUniverse, readJson } from './testUtils';
import { TIER_POINTS } from './tiers';
import type { Answer, Prompt } from './types';

// A fixed random source: each call to rng() starts the same sequence, so the test knows which dive the app picks.
const rng = () => {
  const values = [0.37, 0.81, 0.12, 0.55, 0.93, 0.26, 0.68, 0.44];
  let i = 0;
  return () => values[i++ % values.length] ?? 0;
};
const expectedDive = (): Prompt[] => pickDive(mockPrompts(), rng());

function serveMockFiles() {
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const body = String(url).endsWith('universe.json') ? readJson(UNIVERSE_PATH) : readJson(PROMPTS_PATH);
    return new Response(JSON.stringify(body), { status: 200 });
  }));
}

beforeEach(() => {
  vi.useFakeTimers({ shouldAdvanceTime: true });
  serveMockFiles();
});
afterEach(() => {
  vi.useRealTimers();
  vi.unstubAllGlobals();
});

const setup = () => userEvent.setup({ advanceTimers: vi.advanceTimersByTime });
type User = ReturnType<typeof setup>;

async function start(user: User) {
  render(<App random={rng()} />);
  await user.click(await screen.findByRole('button', { name: 'Play' }));
  await screen.findByRole('combobox');
}

const promptText = (): string => screen.getByRole('heading', { level: 2 }).textContent ?? '';
const typeAnswer = async (user: User, text: string) => {
  await user.type(screen.getByRole('combobox'), text);
  await user.keyboard('{Enter}');
};
const next = async (user: User, last = false) => user.click(await screen.findByRole('button', { name: last ? 'See results' : 'Next prompt' }));
const resultHeading = async () => (await screen.findByRole('heading', { level: 3, name: /points|data range/ })).textContent ?? '';

const validAnswers = (p: Prompt): Answer[] => p.answers;
const notValid = (p: Prompt): string => {
  const valid = new Set(p.answers.map((a) => a.id));
  const u = mockUniverse();
  return (p.answerType === 'player' ? u.players : u.teams).find((e) => !valid.has(e.id) && !e.name.includes('('))!.name;
};
/** A one-letter-short spelling of a long answer name that the matcher still resolves to the same entry. */
const typo = (a: Answer): string => {
  const index = mockIndex();
  for (let i = 1; i < a.name.length - 2; i++) {
    const text = a.name.slice(0, i) + a.name.slice(i + 1);
    const r = matchAnswer(index, text);
    if (r.kind === 'match' && r.entry.id === a.id && r.via === 'typo') return text;
  }
  throw new Error(`no typo found for ${a.name}`);
};

describe('loading and the screens around the game', () => {
  it('shows the home screen with Play and How to play, and says the data is a demo', async () => {
    const user = setup();
    render(<App />);
    expect(await screen.findByRole('button', { name: 'Play' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'How to play' })).toBeInTheDocument();
    expect(screen.getByText(/made up to test the game/i)).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'How to play' }));
    expect(screen.getByRole('heading', { name: 'How to play' })).toBeInTheDocument();
  });

  it('explains the rules and the tier points on the how-to-play screen', async () => {
    const user = setup();
    render(<App />);
    await user.click(await screen.findByRole('button', { name: 'How to play' }));
    expect(screen.getByText(/7 prompts/)).toBeInTheDocument();
    expect(screen.getByText(/25 seconds/)).toBeInTheDocument();
    const table = screen.getByRole('table', { name: 'Points by tier' });
    const points = within(table).getAllByRole('row').slice(1).map((r) => within(r).getAllByRole('cell').pop()?.textContent);
    expect(points).toEqual(['10', '20', '35', '55', '75', '100']);
    expect(screen.getByText(/approximation/i)).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'Back' }));
    expect(screen.getByRole('button', { name: 'Play' })).toBeInTheDocument();
  });

  it('says so when the data cannot be loaded or does not follow the schema', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => new Response('nope', { status: 404 })));
    render(<App />);
    expect(await screen.findByRole('alert')).toHaveTextContent(/could not load/i);
  });

  it('refuses prompts whose answers are not in the universe', async () => {
    vi.stubGlobal('fetch', vi.fn(async (url: string) => {
      const prompts = readJson(PROMPTS_PATH) as Prompt[];
      prompts[0]!.answers[0]!.id = 'mock-pl-999';
      return new Response(JSON.stringify(String(url).endsWith('universe.json') ? readJson(UNIVERSE_PATH) : prompts), { status: 200 });
    }));
    render(<App />);
    expect(await screen.findByRole('alert')).toHaveTextContent(/not in the universe/);
  });
});

describe('a prompt', () => {
  it('shows the prompt, a 25 second countdown and a text input', async () => {
    const user = setup();
    await start(user);
    expect(promptText()).toBe(expectedDive()[0]!.text);
    expect(screen.getByText(/Prompt 1 of 7/)).toBeInTheDocument();
    expect(screen.getByRole('timer')).toHaveTextContent('25');
    expect(screen.getByRole('combobox')).toHaveFocus();
    await act(async () => void vi.advanceTimersByTime(5000));
    expect(screen.getByRole('timer')).toHaveTextContent('20');
  });

  it('announces 10 and 5 seconds left, but not every second', async () => {
    const user = setup();
    await start(user);
    await act(async () => void vi.advanceTimersByTime(15_100));
    expect(screen.getByTestId('announcer')).toHaveTextContent('10 seconds left');
    await act(async () => void vi.advanceTimersByTime(5000));
    expect(screen.getByTestId('announcer')).toHaveTextContent('5 seconds left');
  });

  it('runs out of time after 25 seconds: 0 points, and the answer is not scored', async () => {
    const user = setup();
    await start(user);
    await user.type(screen.getByRole('combobox'), 'Aldric Ash');
    await act(async () => void vi.advanceTimersByTime(25_200));
    expect(await resultHeading()).toBe("Time's up: 0 points");
    expect(screen.getByText(/ran out of time/i)).toBeInTheDocument();
  });

  it('suggests from the whole universe, never only the valid answers', async () => {
    const user = setup();
    await start(user);
    const prompt = expectedDive()[0]!;
    const valid = new Set(validAnswers(prompt).map((a) => a.name));
    await user.type(screen.getByRole('combobox'), 'a');
    const options = screen.getAllByRole('option').map((o) => o.querySelector('.suggestion__name')?.textContent ?? '');
    expect(options.length).toBe(6);
    expect(options.some((n) => !valid.has(n))).toBe(true);
    // players and teams are both offered, whatever the prompt asks for
    await user.clear(screen.getByRole('combobox'));
    await user.type(screen.getByRole('combobox'), 'har');
    const kinds = screen.getAllByRole('option').map((o) => o.querySelector('.suggestion__meta')?.textContent ?? '');
    expect(kinds.some((k) => k.includes('Team'))).toBe(true);
    expect(kinds.some((k) => k.includes('Player'))).toBe(true);
  });

  it('supports the keyboard: arrows move through suggestions, Enter picks, Escape closes', async () => {
    const user = setup();
    await start(user);
    const input = screen.getByRole('combobox');
    await user.type(input, 'ald');
    expect(input).toHaveAttribute('aria-expanded', 'true');
    await user.keyboard('{ArrowDown}');
    const active = screen.getAllByRole('option').find((o) => o.getAttribute('aria-selected') === 'true');
    expect(active).toBeDefined();
    expect(input).toHaveAttribute('aria-activedescendant', active!.id);
    await user.keyboard('{Escape}');
    expect(input).toHaveAttribute('aria-expanded', 'false');
    await user.keyboard('{ArrowDown}{Enter}');
    expect(await resultHeading()).toMatch(/points/); // picking a suggestion answers at once
  });

  it('asks which one when two people share the typed name, without using up the prompt', async () => {
    const user = setup();
    await start(user);
    await typeAnswer(user, 'Dex Marrow');
    expect(screen.getByText(/could be Dex Marrow \(2003-2009\) or Dex Marrow \(2015-2022\)/)).toBeInTheDocument();
    expect(screen.getAllByRole('option')).toHaveLength(2);
    expect(screen.queryByRole('heading', { level: 3, name: /points/ })).not.toBeInTheDocument(); // still answering
    await user.click(screen.getAllByRole('option')[0]!);
    expect(await resultHeading()).toMatch(/points/);
  });

  it('asks for something to be typed before it accepts an empty answer', async () => {
    const user = setup();
    await start(user);
    await user.click(screen.getByRole('button', { name: 'Answer' }));
    expect(screen.getByText(/Type a name/i, { selector: 'p' })).toBeInTheDocument();
    expect(screen.getByRole('timer')).toBeInTheDocument(); // the prompt is still running
  });
});

describe('the reveal', () => {
  it('shows the tier and points, and the most famous and the rarest valid answers', async () => {
    const user = setup();
    await start(user);
    const prompt = expectedDive()[0]!;
    const sorted = validAnswers(prompt).map((a, i) => ({ a, i }));
    const pick = validAnswers(prompt)[4]!;
    await typeAnswer(user, pick.name);
    expect(await resultHeading()).toBe(`Tier ${pick.tier}: ${pick.points} points`);
    const famous = [...sorted].sort((x, y) => x.a.tier - y.a.tier || x.i - y.i).slice(0, 3).map((x) => x.a.name);
    const rarest = [...sorted].sort((x, y) => y.a.tier - x.a.tier || y.i - x.i).slice(0, 3).map((x) => x.a.name);
    const lists = screen.getAllByRole('list').filter((l) => l.className === 'answers');
    expect(within(lists[0]!).getAllByRole('listitem').map((li) => li.querySelector('.answers__name')?.textContent)).toEqual(famous);
    expect(within(lists[1]!).getAllByRole('listitem').map((li) => li.querySelector('.answers__name')?.textContent)).toEqual(rarest);
    expect(screen.getByText(`All ${prompt.answers.length} valid answers`)).toBeInTheDocument();
    expect(screen.getByRole('heading', { level: 3, name: /points/ })).toHaveFocus();
  });

  it('says an invalid answer is invalid, and names the person it recognized', async () => {
    const user = setup();
    await start(user);
    const prompt = expectedDive()[0]!;
    const other = notValid(prompt);
    await typeAnswer(user, other);
    expect(await resultHeading()).toBe('Not a valid answer: 0 points');
    expect(screen.getByText(`${other} is not a valid answer for this prompt.`)).toBeInTheDocument();
  });

  it('says "outside the data range" gently, scoring 0', async () => {
    const user = setup();
    await start(user);
    await typeAnswer(user, 'Orson Quillfeather');
    expect(await resultHeading()).toBe('Outside the data range');
    expect(screen.getByText(/does not count against you/i)).toBeInTheDocument();
    expect(screen.queryByText(/not a valid answer/i)).not.toBeInTheDocument();
  });
});

describe('a full dive', () => {
  it('plays 7 prompts end to end and shows the total, seven colored squares and a share line', async () => {
    const user = setup();
    await start(user);
    const dive = expectedDive();
    expect(dive).toHaveLength(7);
    let expected = 0;
    const tiers: Array<number | null> = [];
    const record = (a: Answer | null) => {
      expected += a?.points ?? 0;
      tiers.push(a?.tier ?? null);
    };

    for (let i = 0; i < 7; i++) {
      const p = dive[i]!;
      expect(promptText()).toBe(p.text);
      expect(screen.getByText(new RegExp(`Prompt ${i + 1} of 7`))).toBeInTheDocument();
      const answers = validAnswers(p);
      if (i === 0) {
        await typeAnswer(user, answers[0]!.name); // an exact name
        record(answers[0]!);
      } else if (i === 1) {
        const long = answers.find((a) => a.name.length >= 11 && !a.name.includes('('))!;
        await typeAnswer(user, typo(long)); // a typo
        record(long);
      } else if (i === 2) {
        await typeAnswer(user, notValid(p)); // a real name that is not an answer
        record(null);
      } else if (i === 3) {
        await typeAnswer(user, 'qwerty zxcv'); // gibberish
        record(null);
      } else if (i === 4) {
        await typeAnswer(user, 'Orson Quillfeather'); // outside the data range
        record(null);
      } else if (i === 5) {
        await act(async () => void vi.advanceTimersByTime(25_200)); // out of time
        record(null);
      } else {
        const deepest = [...answers].sort((a, b) => b.tier - a.tier)[0]!;
        await typeAnswer(user, deepest.name);
        record(deepest);
      }
      await resultHeading();
      await next(user, i === 6);
    }

    const total = screen.getByLabelText(/^Total \d+ out of 700$/);
    expect(total).toHaveAttribute('aria-label', `Total ${expected} out of 700`);
    const squares = within(screen.getByRole('list', { name: 'Your seven answers' })).getAllByRole('listitem');
    expect(squares).toHaveLength(7);
    squares.forEach((s, i) => {
      const t = tiers[i];
      expect(s).toHaveClass(t === null ? 'square--miss' : `square--t${t}`);
      expect(s.getAttribute('aria-label')).toMatch(new RegExp(`^Prompt ${i + 1}: ${t === null ? '(not a valid|time ran out|outside)' : `tier ${t}, ${TIER_POINTS[t as 1]} points`}`));
    });
    expect(tiers.filter((t) => t === null)).toHaveLength(4);
    expect(screen.getByRole('heading', { name: 'Dive complete' })).toHaveFocus();

    // share: the line is shown and copies to the clipboard
    const preview = screen.getByLabelText('Your result');
    expect(preview.textContent).toMatch(new RegExp(`^Deep Cut #1: ${expected}\\n.{7,21}$`, 's'));
    await user.click(screen.getByRole('button', { name: 'Copy result' }));
    expect(await navigator.clipboard.readText()).toBe(preview.textContent);
    expect(screen.getByTestId('announcer')).toHaveTextContent('Copied to the clipboard.');
  });

  it('shows the share text to copy by hand when the clipboard is refused, and can play again as dive #2', async () => {
    const user = setup();
    await start(user);
    const dive = expectedDive();
    for (let i = 0; i < 7; i++) {
      await typeAnswer(user, validAnswers(dive[i]!)[0]!.name);
      await resultHeading();
      await next(user, i === 6);
    }
    vi.spyOn(navigator.clipboard, 'writeText').mockRejectedValue(new Error('denied'));
    await user.click(screen.getByRole('button', { name: 'Copy result' }));
    const box = await screen.findByLabelText('Your result, ready to copy');
    expect((box as HTMLTextAreaElement).value).toMatch(/^Deep Cut #1: \d+\n/);
    expect(screen.getByTestId('announcer')).toHaveTextContent(/Could not copy/);
    await user.click(screen.getByRole('button', { name: 'Play again' }));
    expect(await screen.findByRole('combobox')).toBeInTheDocument();
    expect(screen.getByText(/Prompt 1 of 7/)).toBeInTheDocument();
  });
});
