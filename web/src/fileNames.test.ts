import { execFileSync } from 'node:child_process';
import { existsSync, readdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';

// The owner develops on Windows, where two files whose names differ only by case cannot exist side by side.
const root = resolve(process.cwd(), '..');

function trackedFiles(): string[] {
  try {
    return execFileSync('git', ['ls-files'], { cwd: root, encoding: 'utf8' }).split('\n').filter(Boolean);
  } catch {
    // no git (web/ alone): walk the folders instead
    const walk = (dir: string, prefix: string): string[] =>
      readdirSync(dir, { withFileTypes: true }).flatMap((d) => (d.name === 'node_modules' || d.name === 'dist' ? [] : d.isDirectory() ? walk(resolve(dir, d.name), `${prefix}${d.name}/`) : [`${prefix}${d.name}`]));
    return walk(process.cwd(), 'web/');
  }
}

describe('file names', () => {
  it('has no two files whose names differ only by case', () => {
    const seen = new Map<string, string>();
    const clashes: string[] = [];
    for (const f of trackedFiles()) {
      const key = f.toLowerCase();
      const other = seen.get(key);
      if (other && other !== f) clashes.push(`${other} and ${f}`);
      seen.set(key, f);
    }
    expect(clashes).toEqual([]);
  });

  it('has no two folders or file-and-folder names that differ only by case', () => {
    const dirs = new Map<string, string>();
    const clashes: string[] = [];
    for (const f of trackedFiles()) {
      const parts = f.split('/');
      for (let i = 1; i <= parts.length; i++) {
        const path = parts.slice(0, i).join('/');
        const key = path.toLowerCase();
        const other = dirs.get(key);
        if (other && other !== path) clashes.push(`${other} and ${path}`);
        dirs.set(key, path);
      }
    }
    expect(clashes).toEqual([]);
  });

  it('keeps the game logic in dive2.ts next to Dive.tsx', () => {
    expect(existsSync(resolve(process.cwd(), 'src/dive2.ts'))).toBe(true);
    expect(existsSync(resolve(process.cwd(), 'src/Dive.tsx'))).toBe(true);
  });
});
