import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';

interface VercelJson {
  framework: string;
  outputDirectory: string;
  buildCommand: string;
  rewrites: Array<{ source: string; destination: string }>;
  headers: Array<{ source: string; headers: Array<{ key: string; value: string }> }>;
}
const config = JSON.parse(readFileSync(resolve(process.cwd(), 'vercel.json'), 'utf8')) as VercelJson;
const cacheFor = (path: string): string | undefined => {
  const rule = config.headers.find((h) => new RegExp(`^${h.source}$`).test(path));
  return rule?.headers.find((h) => h.key === 'Cache-Control')?.value;
};

describe('vercel.json', () => {
  it('builds a Vite site into dist with the normal build command', () => {
    expect(config.framework).toBe('vite');
    expect(config.outputDirectory).toBe('dist');
    expect(config.buildCommand).toBe('npm run build');
  });

  it('falls back to index.html for page addresses but never for files, so the JSON requests are not rewritten', () => {
    const rewrite = config.rewrites[0]!;
    expect(rewrite.destination).toBe('/index.html');
    const re = new RegExp(`^${rewrite.source}$`);
    for (const page of ['/', '/archive', '/some/page']) expect(re.test(page), page).toBe(true);
    for (const file of ['/prompts.json', '/universe.json', '/outside_range.json', '/social.png', '/favicon.png', '/assets/index-abc.js', '/assets/font.woff2', '/apple-touch-icon.png']) {
      expect(re.test(file), file).toBe(false);
    }
  });

  it('caches the three data files briefly and revalidates them', () => {
    for (const file of ['/prompts.json', '/universe.json', '/outside_range.json']) {
      expect(cacheFor(file)).toMatch(/max-age=60/);
      expect(cacheFor(file)).toMatch(/must-revalidate/);
      expect(cacheFor(file)).not.toMatch(/immutable/);
    }
  });

  it('caches hashed assets for a year, immutable', () => {
    expect(cacheFor('/assets/index-Dqc4jwmH.js')).toBe('public, max-age=31536000, immutable');
    expect(cacheFor('/assets/press-start-2p-latin-400-normal-qiz4-Cze.woff2')).toMatch(/immutable/);
  });

  it('always revalidates the page itself, so a new deploy is picked up', () => {
    expect(cacheFor('/')).toMatch(/max-age=0/);
  });
});
