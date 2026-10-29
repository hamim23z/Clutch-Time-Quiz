import type { Prompt, Universe } from './types';

type Obj = Record<string, unknown>;
const isObject = (v: unknown): v is Obj => typeof v === 'object' && v !== null && !Array.isArray(v);

function str(o: Obj, k: string, where: string): string {
  const v = o[k];
  if (typeof v !== 'string' || v === '') throw new Error(`${where}: "${k}" must be a non-empty string`);
  return v;
}

function entries(raw: unknown, where: string): Universe['players'] {
  if (!Array.isArray(raw) || raw.length === 0) throw new Error(`${where} must be a non-empty array`);
  return raw.map((e: unknown, i: number) => {
    if (!isObject(e)) throw new Error(`${where}[${i}] must be an object`);
    const aliases = e['aliases'];
    if (!Array.isArray(aliases) || aliases.some((a) => typeof a !== 'string' || a === '')) throw new Error(`${where}[${i}]: "aliases" must be an array of strings`);
    return { id: str(e, 'id', `${where}[${i}]`), name: str(e, 'name', `${where}[${i}]`), aliases: aliases as string[] };
  });
}

export function parseUniverse(data: unknown): Universe {
  if (!isObject(data)) throw new Error('universe.json must be an object');
  return { players: entries(data['players'], 'players'), teams: entries(data['teams'], 'teams') };
}

/** Check the shape of prompts.json at runtime, and that every answer points at an entry of the universe. */
export function parsePrompts(data: unknown, universe: Universe): Prompt[] {
  if (!Array.isArray(data) || data.length === 0) throw new Error('prompts.json must be a non-empty array');
  const names = new Map([...universe.players, ...universe.teams].map((e) => [e.id, e.name]));
  return data.map((raw: unknown, i: number) => {
    if (!isObject(raw)) throw new Error(`prompt ${i} must be an object`);
    const id = str(raw, 'id', `prompt ${i}`);
    const where = `prompt ${id}`;
    const answerType = raw['answerType'];
    const difficulty = raw['difficulty'];
    if (answerType !== 'player' && answerType !== 'team') throw new Error(`${where}: answerType must be player or team`);
    if (difficulty !== 'easy' && difficulty !== 'medium' && difficulty !== 'hard') throw new Error(`${where}: difficulty must be easy, medium or hard`);
    const rawAnswers = raw['answers'];
    if (!Array.isArray(rawAnswers) || rawAnswers.length === 0) throw new Error(`${where}: answers must be a non-empty array`);
    const answers = rawAnswers.map((a: unknown, j: number) => {
      if (!isObject(a)) throw new Error(`${where}: answer ${j} must be an object`);
      const tier = a['tier'];
      const points = a['points'];
      if (typeof tier !== 'number' || !Number.isInteger(tier) || tier < 1 || tier > 6) throw new Error(`${where}: answer ${j} has a bad tier`);
      if (typeof points !== 'number') throw new Error(`${where}: answer ${j} has no points`);
      const aid = str(a, 'id', `${where} answer ${j}`);
      if (!names.has(aid)) throw new Error(`${where}: answer ${aid} is not in the universe`);
      return { id: aid, name: str(a, 'name', `${where} answer ${j}`), tier: tier as 1 | 2 | 3 | 4 | 5 | 6, points };
    });
    return { id, answerType, text: str(raw, 'text', where), answers, difficulty };
  });
}

/** The names in outside_range.json. This file only drives a gentle message, so a missing or broken one means "no names". */
export function parseOutsideNames(data: unknown): string[] {
  return Array.isArray(data) ? data.filter((n): n is string => typeof n === 'string' && n.trim() !== '') : [];
}

export interface GameData {
  prompts: Prompt[];
  universe: Universe;
  outsideNames: string[];
}

export async function loadData(baseUrl: string): Promise<GameData> {
  const get = async (file: string): Promise<unknown> => {
    const response = await fetch(`${baseUrl}${file}`);
    if (!response.ok) throw new Error(`Could not load ${file} (${response.status})`);
    return (await response.json()) as unknown;
  };
  const universe = parseUniverse(await get('universe.json'));
  const prompts = parsePrompts(await get('prompts.json'), universe);
  const outsideNames = await get('outside_range.json').then(parseOutsideNames, () => []);
  return { universe, prompts, outsideNames };
}
