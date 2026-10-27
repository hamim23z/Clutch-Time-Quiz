import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import App from './App';
import { readMockJson, readMockScenarios } from './testUtils';

// random() === 0 keeps the mock file's order, so a round is its first five scenarios:
// mock-foul3-01, -02, -03, -04 and mock-down3-01.
const FIRST_FIVE = () => 0;

function serveMockFile() {
  vi.stubGlobal(
    'fetch',
    vi.fn(async () => new Response(JSON.stringify(readMockJson()), { status: 200 })),
  );
}

async function startGame() {
  render(<App random={FIRST_FIVE} />);
  await screen.findByRole('group', { name: 'Your options' });
}

beforeEach(serveMockFile);
afterEach(() => vi.unstubAllGlobals());

describe('loading', () => {
  it('shows a loading message, then the first hole', async () => {
    render(<App random={FIRST_FIVE} />);
    expect(screen.getByRole('status')).toHaveTextContent('Loading scenarios');
    expect(await screen.findByRole('heading', { name: /you lead by 3 and they have the ball/i })).toBeInTheDocument();
    expect(screen.getByText('Hole 1 of 5')).toBeInTheDocument();
  });

  it('says so when the file cannot be loaded', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => new Response('nope', { status: 404 })));
    render(<App />);
    expect(await screen.findByRole('alert')).toHaveTextContent(/could not load/i);
  });

  it('says so when the file does not follow the schema', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => new Response(JSON.stringify([{ id: 'x' }]), { status: 200 })));
    render(<App />);
    expect(await screen.findByRole('alert')).toHaveTextContent(/scenario x/i);
  });

  it('tells the player the data is mock data', async () => {
    await startGame();
    expect(screen.getByText(/demo data/i)).toBeInTheDocument();
  });
});

describe('a hole', () => {
  it('shows the situation and both options, and hides teams and date', async () => {
    await startGame();
    const quarter = screen.getByText('Quarter').closest('div') as HTMLElement;
    expect(within(quarter).getByText('4th quarter')).toBeInTheDocument();
    expect(screen.getByText('You lead by 3')).toBeInTheDocument();
    expect(screen.getByText('0:08')).toBeInTheDocument();
    expect(screen.getByText('They have the ball')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Foul before the shot' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Play straight defense' })).toBeInTheDocument();

    const scenario = readMockScenarios()[0]!;
    const page = document.body.textContent ?? '';
    expect(page).not.toContain(scenario.actual.game);
    expect(page).not.toContain(scenario.actual.summary);
    expect(page).not.toMatch(/Harbor City|Lakeshore|2019/);
    expect(page).not.toMatch(/\d+% of \d/); // no win rates before the pick
  });

  it('reveals win rates, what happened, the teams and the caveat after a pick', async () => {
    const user = userEvent.setup();
    await startGame();
    await user.click(screen.getByRole('button', { name: 'Play straight defense' })); // 81% vs best 93%: 12 points

    const result = screen.getByRole('heading', { name: /double bogey/i });
    expect(result).toHaveTextContent('Double bogey (+2)');
    expect(result).toHaveFocus(); // keyboard and screen reader users land on the result
    expect(screen.getByText(/won 12 points less often/i)).toBeInTheDocument();

    expect(screen.getByText(/Won 93% of 212 similar situations/)).toBeInTheDocument();
    expect(screen.getByText(/Won 81% of 1,480 similar situations/)).toBeInTheDocument();
    expect(screen.getByText(/Your pick/)).toBeInTheDocument();
    expect(screen.getByText(/Best/)).toBeInTheDocument();
    expect(screen.getByText(/Mock game: Lakeshore Rapids vs Harbor City Gulls/)).toBeInTheDocument();
    expect(screen.getByText(/switched everything/)).toBeInTheDocument();
    expect(screen.getByText(/Harbor City 104, Lakeshore 101/)).toBeInTheDocument();
    expect(screen.getByText(/not what would have happened in this exact game/i)).toBeInTheDocument();

    expect(screen.queryByRole('group', { name: 'Your options' })).not.toBeInTheDocument(); // cannot pick twice
    expect(screen.getByRole('button', { name: 'Next hole' })).toBeInTheDocument();
    expect(screen.getByText('Score').parentElement).toHaveTextContent('+2');
  });

  it('scores the best option a birdie', async () => {
    const user = userEvent.setup();
    await startGame();
    await user.click(screen.getByRole('button', { name: 'Foul before the shot' }));
    expect(screen.getByRole('heading', { name: /birdie/i })).toHaveTextContent('Birdie (−1)');
    expect(screen.getByText('You picked the best option.')).toBeInTheDocument();
  });

  it('moves focus to the next question when the player continues', async () => {
    const user = userEvent.setup();
    await startGame();
    await user.click(screen.getByRole('button', { name: 'Foul before the shot' }));
    await user.click(screen.getByRole('button', { name: 'Next hole' }));
    expect(screen.getByText('Hole 2 of 5')).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /five seconds left/i })).toHaveFocus();
    expect(screen.queryByText(/Mock game: Lakeshore/)).not.toBeInTheDocument(); // the last reveal is gone
  });
});

describe('a full round', () => {
  it('plays 5 holes from the mock file and shows the total against par', async () => {
    const user = userEvent.setup();
    await startGame();

    // Always pick the first option. By the mock numbers:
    //  1 foul3-01 foul 93% (best)            birdie  -1
    //  2 foul3-02 foul 90% (best)            birdie  -1
    //  3 foul3-03 foul 89% (best)            birdie  -1
    //  4 foul3-04 foul 86% vs best 90%       bogey   +1  (4 points)
    //  5 down3-01 three 27% (best)           birdie  -1
    const expected = ['Birdie (−1)', 'Birdie (−1)', 'Birdie (−1)', 'Bogey (+1)', 'Birdie (−1)'];
    for (let hole = 1; hole <= 5; hole++) {
      expect(screen.getByText(`Hole ${hole} of 5`)).toBeInTheDocument();
      const first = within(screen.getByRole('group', { name: 'Your options' })).getAllByRole('button')[0]!;
      await user.click(first);
      expect(screen.getByRole('heading', { name: new RegExp(expected[hole - 1]!.split(' ')[0]!, 'i') })).toHaveTextContent(
        expected[hole - 1]!,
      );
      await user.click(screen.getByRole('button', { name: hole === 5 ? 'See results' : 'Next hole' }));
    }

    const final = screen.getByRole('heading', { name: 'Round complete' });
    expect(final).toHaveFocus();
    expect(screen.getByLabelText('Final score −3')).toHaveTextContent('−3');
    const holes = screen.getAllByText(/^Hole \d: /);
    expect(holes.map((h) => h.textContent)).toEqual([
      'Hole 1: Birdie (−1)',
      'Hole 2: Birdie (−1)',
      'Hole 3: Birdie (−1)',
      'Hole 4: Bogey (+1)',
      'Hole 5: Birdie (−1)',
    ]);
    expect(screen.getByRole('button', { name: 'Play another round' })).toBeInTheDocument();
  });

  it('can start another round after the final score', async () => {
    const user = userEvent.setup();
    await startGame();
    for (let hole = 1; hole <= 5; hole++) {
      await user.click(within(screen.getByRole('group', { name: 'Your options' })).getAllByRole('button')[0]!);
      await user.click(screen.getByRole('button', { name: hole === 5 ? 'See results' : 'Next hole' }));
    }
    await user.click(screen.getByRole('button', { name: 'Play another round' }));
    expect(screen.getByText('Hole 1 of 5')).toBeInTheDocument();
    expect(screen.getByText('Score').parentElement).toHaveTextContent('E');
    expect(screen.getByRole('group', { name: 'Your options' })).toBeInTheDocument();
  });

  it('adds up bad picks too: five double bogeys or bogeys never go below the floor', async () => {
    const user = userEvent.setup();
    await startGame();
    // always the second option: -> double, par(2 pts), bogey(3.. wait 4 pts), then compare with the scorer
    for (let hole = 1; hole <= 5; hole++) {
      await user.click(within(screen.getByRole('group', { name: 'Your options' })).getAllByRole('button')[1]!);
      await user.click(screen.getByRole('button', { name: hole === 5 ? 'See results' : 'Next hole' }));
    }
    // 1 foul3-01 defend 81 vs 93: 12 -> +2 | 2 foul3-02 defend 88 vs 90: 2 -> 0 | 3 foul3-03 defend 82 vs 89: 7 -> +1
    // 4 foul3-04 defend 90 (best) -> -1    | 5 down3-01 two 14 vs 27: 13 -> +2     total +4
    expect(screen.getByLabelText('Final score +4')).toBeInTheDocument();
  });
});
