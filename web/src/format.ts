import type { Possession, ScenarioState } from './types';

export function describeMargin(margin: number): string {
  if (margin === 0) return 'Tied';
  const points = Math.abs(margin);
  return `${margin > 0 ? 'You lead' : 'You trail'} by ${points}`;
}

export function formatClock(secondsLeft: number): string {
  const minutes = Math.floor(secondsLeft / 60);
  const seconds = secondsLeft % 60;
  return `${minutes}:${String(seconds).padStart(2, '0')}`;
}

export function describeQuarter(quarter: number): string {
  if (quarter <= 4) return '4th quarter';
  return quarter === 5 ? 'Overtime' : `${quarter - 4}OT`;
}

export function describePossession(possession: Possession): string {
  return possession === 'team' ? 'You have the ball' : 'They have the ball';
}

export function describeState(state: ScenarioState): string {
  const lower = (text: string) => text.charAt(0).toLowerCase() + text.slice(1);
  return [
    describeQuarter(state.quarter),
    lower(describeMargin(state.margin)),
    `${formatClock(state.secondsLeft)} left`,
    lower(describePossession(state.possession)),
  ].join(', ');
}

export function formatPercent(winRate: number): string {
  return `${Math.round(winRate * 100)}%`;
}
