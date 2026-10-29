// Mirrors schema/prompts.schema.json and schema/universe.schema.json. data.test.ts checks the data against the schemas.

export type AnswerType = 'player' | 'team';
export type Difficulty = 'easy' | 'medium' | 'hard';
export type Tier = 1 | 2 | 3 | 4 | 5 | 6;

export interface Answer {
  id: string;
  name: string;
  tier: Tier;
  points: number;
}

export interface Prompt {
  id: string;
  answerType: AnswerType;
  text: string;
  answers: Answer[];
  difficulty: Difficulty;
}

export interface UniverseEntry {
  id: string;
  name: string;
  aliases: string[];
}

export interface Universe {
  players: UniverseEntry[];
  teams: UniverseEntry[];
}

/** An entry with the kind of thing it is, as the matcher and the autocomplete see it. */
export interface Entry extends UniverseEntry {
  kind: AnswerType;
}

export type ResultStatus = 'valid' | 'invalid' | 'outside_range' | 'timeout';

/** What happened on one prompt. */
export interface PromptResult {
  promptId: string;
  status: ResultStatus;
  /** What the player typed or picked ('' when time ran out with nothing typed). */
  input: string;
  /** The universe entry the answer was recognized as, if any (it may still not be a valid answer). */
  matched: { id: string; name: string } | null;
  tier: Tier | null;
  points: number;
  /** False for an answer outside the data range: it must not count against a streak. */
  countsAsWrong: boolean;
}
