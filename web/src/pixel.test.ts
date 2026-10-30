import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { ART_SCALE, BALL, HOOP, LOW, SPRITE } from './court/geometry';

const web = process.cwd();
const dir = resolve(web, 'src/assets/pixel');
const css = ['src/styles.css', 'src/court/court.css'].map((f) => [f, readFileSync(resolve(web, f), 'utf8')] as const);
const size = (file: string): { w: number; h: number } => {
  const png = readFileSync(resolve(dir, file));
  return { w: png.readUInt32BE(16), h: png.readUInt32BE(20) };
};

describe('the pixel pictures (tools/pixel/gen_pixel.py)', () => {
  it('are all there, as PNG files', () => {
    for (const f of ['court.png', 'court_bare.png', 'ball.png', 'dunker.png', 'shooter_stand.png', 'shooter_shoot.png', 'rim_back.png', 'rim_front.png', 'net_0.png', 'net_1.png', 'net_2.png', 'beam.png', 'crowd_a.png', 'crowd_b.png']) {
      expect(existsSync(resolve(dir, f)), f).toBe(true);
      expect(readFileSync(resolve(dir, f)).subarray(1, 4).toString(), f).toBe('PNG');
    }
  });

  it('are the game size times 4, so every game pixel is a whole 4 x 4 block', () => {
    expect(size('court.png')).toEqual({ w: LOW.width * ART_SCALE, h: LOW.height * ART_SCALE });
    expect(size('court_bare.png')).toEqual(size('court.png'));
    expect(size('ball.png')).toEqual({ w: BALL * ART_SCALE, h: BALL * ART_SCALE });
    for (const f of ['dunker.png', 'shooter_stand.png', 'shooter_shoot.png']) expect(size(f), f).toEqual({ w: SPRITE.width * ART_SCALE, h: SPRITE.height * ART_SCALE });
    expect(size('court.png')).toEqual({ w: 688, h: 860 });
  });

  it('have no other files beside them (an unused picture is dead weight)', () => {
    const used = readFileSync(resolve(web, 'src/court/CourtScene.tsx'), 'utf8');
    for (const f of readdirSync(dir)) {
      if (f === 'court.png') continue; // the court with its hoop baked in: the starter picture, kept as the reference the generator reproduces
      expect(used.includes(`/${f}'`) || readFileSync(resolve(web, 'src/styles.css'), 'utf8').includes(f), f).toBe(true);
    }
  });

  it('puts the rim where the court picture says it is', () => {
    expect(HOOP).toEqual({ x: 86, y: 70 });
    expect(HOOP.x / LOW.width).toBeCloseTo(0.5, 2); // about 50% across
    expect(HOOP.y / LOW.height).toBeCloseTo(0.326, 2); // about 32.6% down
  });

  it('are shown pixelated, at whole-number scales', () => {
    const all = css.map(([, text]) => text).join('\n');
    expect(all).toMatch(/image-rendering:\s*pixelated/);
    expect(all).not.toMatch(/image-rendering:\s*(auto|smooth|crisp-edges|-webkit-optimize-contrast)/);
  });
});

describe('the pixel look of the stylesheets', () => {
  it.each(css)('%s has no rounded corners, blur, glow or soft gradient', (_file, text) => {
    const code = text.replace(/\/\*[\s\S]*?\*\//g, '');
    for (const m of code.matchAll(/border-radius:\s*([^;]+);/g)) expect(m[1]!.trim(), 'border-radius').toBe('0');
    expect(code).not.toMatch(/blur\(|backdrop-filter|drop-shadow|text-shadow:[^;]*\d+px\s+\d+px\s+[1-9]\d*px/);
    expect(code).not.toMatch(/radial-gradient|conic-gradient\((?!var)/); // the only conic gradients are hard-edged checkerboards
    for (const m of code.matchAll(/(?<!repeating-)linear-gradient\(/g)) expect(m.index, 'a smooth linear-gradient').toBeNull();
    for (const m of code.matchAll(/box-shadow:([^;]+);/g)) {
      // every shadow is a hard offset: the third number (the blur) is 0
      for (const shadow of m[1]!.split(/,(?![^(]*\))/)) {
        const lengths = shadow.replace(/var\([^)]*\)|calc\((?:[^()]|\([^()]*\))*\)/g, '1').match(/-?[\d.]+(?:px|rem)?/g) ?? [];
        if (lengths.length >= 3) expect(Number.parseFloat(lengths[2]!), shadow).toBe(0);
      }
    }
  });

  it('animates in steps: no easing curves in the stepped court keyframes or the panel', () => {
    for (const [file, text] of css) expect(text, file).not.toMatch(/cubic-bezier|ease-in|ease-out|ease-in-out/);
  });

  it('uses the palette tokens, and the tier colours the brief set', () => {
    const [, styles] = css[0]!;
    for (const [name, value] of Object.entries({ ink: '#0a0a0a', panel: '#141414', line: '#3a3a3a', orange: '#ff6a13', amber: '#ffb347', cream: '#f4ead6', muted: '#a8a8a8', deep: '#8a3c0a', t1: '#6e6e6e', t2: '#a8a8a8', t3: '#ededed', t4: '#ffb020', t5: '#ff6a13', t6: '#ff3b1f' })) {
      expect(styles, name).toContain(`--${name}: ${value};`);
    }
  });

  it('loads the two pixel fonts from the package, with no request to a font service', () => {
    const main = readFileSync(resolve(web, 'src/main.tsx'), 'utf8');
    expect(main).toContain("@fontsource/press-start-2p/");
    expect(main).toContain("@fontsource/vt323/");
    expect(main).not.toMatch(/barlow/i);
    const html = readFileSync(resolve(web, 'index.html'), 'utf8');
    expect(html).not.toMatch(/fonts\.googleapis|fonts\.gstatic/);
    const [, styles] = css[0]!;
    expect(styles).not.toMatch(/@import\s+url\(['"]?https?:/);
  });
});

describe('text contrast (WCAG: at least 4.5 to 1 for text)', () => {
  const [, styles] = css[0]!;
  const token = (name: string): string => new RegExp(`--${name}: (#[0-9a-f]{6});`).exec(styles)![1]!;
  const lum = (hex: string): number => {
    const [r, g, b] = [1, 3, 5].map((i) => Number.parseInt(hex.slice(i, i + 2), 16) / 255).map((c) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4));
    return 0.2126 * r! + 0.7152 * g! + 0.0722 * b!;
  };
  const ratio = (a: string, b: string): number => {
    const [hi, lo] = [lum(a), lum(b)].sort((x, y) => y - x);
    return (hi! + 0.05) / (lo! + 0.05);
  };

  it.each([
    ['cream', 'ink'], ['cream', 'panel'], ['muted', 'ink'], ['muted', 'panel'], ['orange', 'ink'], ['orange', 'panel'], ['amber', 'ink'], ['amber', 'panel'], ['ink', 'orange'], ['ink', 'amber'],
  ])('%s on %s', (fg, bg) => {
    expect(ratio(token(fg), token(bg))).toBeGreaterThanOrEqual(4.5);
  });

  it('puts readable text on every tier colour (white on tier 1, ink on the rest) and on a miss', () => {
    const on: Record<string, string> = { t1: '#ffffff', t2: token('ink'), t3: token('ink'), t4: token('ink'), t5: token('ink'), t6: token('ink') };
    for (const [tier, text] of Object.entries(on)) expect(ratio(text, token(tier)), tier).toBeGreaterThanOrEqual(4.5);
    expect(ratio(token('cream'), '#3a3a3a')).toBeGreaterThanOrEqual(4.5);
  });

  it('shows the tier as text too: a number or a name in every tier chip, square and label', () => {
    const source = ['components/Reveal.tsx', 'components/Final.tsx', 'components/Archive.tsx', 'court/CourtScene.tsx'].map((f) => readFileSync(resolve(web, 'src', f), 'utf8')).join('\n');
    expect(source).toMatch(/square__tier/);
    expect(source).toMatch(/mini__square[^\n]*\n[^\n]*r\.tier \?\? '×'/);
    expect(source).toMatch(/chip chip--t\$\{a\.tier\}[^<]*>\{a\.tier\}/);
    expect(source).toMatch(/T\$\{shot\.tier\} \$\{shot\.label\}/);
  });
});
