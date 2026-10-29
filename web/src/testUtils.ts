import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { parsePrompts, parseUniverse } from './loadData';
import { buildIndex, type Index } from './matching';
import type { Prompt, Universe } from './types';

// Tests run from web/ (npm test), so paths are relative to that folder.
export const PROMPTS_PATH = resolve(process.cwd(), 'src/__fixtures__/prompts.json');
export const UNIVERSE_PATH = resolve(process.cwd(), 'src/__fixtures__/universe.json');
export const PROMPTS_SCHEMA_PATH = resolve(process.cwd(), '../schema/prompts.schema.json');
export const UNIVERSE_SCHEMA_PATH = resolve(process.cwd(), '../schema/universe.schema.json');

export const readJson = (path: string): unknown => JSON.parse(readFileSync(path, 'utf8')) as unknown;
export const mockUniverse = (): Universe => parseUniverse(readJson(UNIVERSE_PATH));
export const mockPrompts = (): Prompt[] => parsePrompts(readJson(PROMPTS_PATH), mockUniverse());
export const mockIndex = (): Index => buildIndex(mockUniverse());

/** The id of the mock entry with this exact name. */
export function idOf(name: string): string {
  const u = mockUniverse();
  const found = [...u.players, ...u.teams].find((e) => e.name === name);
  if (!found) throw new Error(`no mock entry named ${name}`);
  return found.id;
}
