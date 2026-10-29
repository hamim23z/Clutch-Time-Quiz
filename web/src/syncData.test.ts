import { mkdtempSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { parseNames, sync } from '../scripts/sync-data.mjs';

describe('parseNames', () => {
  it('reads the name column of the outside-range CSV', () => {
    expect(parseNames('name\nLarry Bird\nMagic Johnson\n')).toEqual(['Larry Bird', 'Magic Johnson']);
    expect(parseNames('name\r\n"Kareem Abdul-Jabbar"\r\n\r\n')).toEqual(['Kareem Abdul-Jabbar']);
    expect(parseNames('"name"\n"Say ""Hey"" Jones"\n')).toEqual(['Say "Hey" Jones']);
  });

  it('refuses a file without the header', () => {
    expect(() => parseNames('Larry Bird\n')).toThrow(/header/);
  });
});

describe('sync', () => {
  it('copies prompts.json and universe.json and writes outside_range.json from the CSV', () => {
    const repo = mkdtempSync(join(tmpdir(), 'deepcut-repo-'));
    mkdirSync(join(repo, 'data/export'), { recursive: true });
    mkdirSync(join(repo, 'pipeline/data'), { recursive: true });
    writeFileSync(join(repo, 'data/export/prompts.json'), '[1]');
    writeFileSync(join(repo, 'data/export/universe.json'), '{"a":1}');
    writeFileSync(join(repo, 'pipeline/data/outside_range.csv'), 'name\nLarry Bird\nMagic Johnson\n');
    const out = join(repo, 'web-public');
    expect(sync(repo, out)).toBe(2);
    expect(readFileSync(join(out, 'prompts.json'), 'utf8')).toBe('[1]');
    expect(readFileSync(join(out, 'universe.json'), 'utf8')).toBe('{"a":1}');
    expect(JSON.parse(readFileSync(join(out, 'outside_range.json'), 'utf8'))).toEqual(['Larry Bird', 'Magic Johnson']);
  });

  it('says what to run when the export is missing', () => {
    const repo = mkdtempSync(join(tmpdir(), 'deepcut-empty-'));
    expect(() => sync(repo, join(repo, 'out'))).toThrow(/pipeline\/export\.py/);
  });

  it('the real repository syncs: 63 or more prompts and the outside-range names', () => {
    const out = mkdtempSync(join(tmpdir(), 'deepcut-real-'));
    expect(sync(resolve(process.cwd(), '..'), out)).toBeGreaterThan(100);
    expect((JSON.parse(readFileSync(join(out, 'prompts.json'), 'utf8')) as unknown[]).length).toBeGreaterThanOrEqual(63);
  });
});
