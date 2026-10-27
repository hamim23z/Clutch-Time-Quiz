// Mirrors schema/scenarios.schema.json. Keep the two in step; schema.test.ts checks the data against the schema.

export type ScenarioType = 'foul_up_three' | 'down_three' | 'last_shot';
export type Difficulty = 'easy' | 'medium' | 'hard';
export type Possession = 'team' | 'opponent';

export interface ScenarioState {
  quarter: number;
  margin: number;
  secondsLeft: number;
  possession: Possession;
}

export interface ScenarioOption {
  key: string;
  label: string;
  winRate: number;
  n: number;
}

export interface Actual {
  choice: string;
  summary: string;
  final: string;
  game: string;
}

export interface Scenario {
  id: string;
  type: ScenarioType;
  state: ScenarioState;
  question: string;
  options: ScenarioOption[];
  actual: Actual;
  difficulty: Difficulty;
}

export type HoleResult = 'birdie' | 'par' | 'bogey' | 'double_bogey';

export interface HoleRecord {
  scenarioId: string;
  pickedKey: string;
  bestKey: string;
  result: HoleResult;
  strokes: number;
  /** Win rate gap between the best option and the pick, in percentage points. */
  gap: number;
}
