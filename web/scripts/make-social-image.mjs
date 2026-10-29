// Draws web/public/social.png (1200x630) and web/public/apple-touch-icon.png (180x180) from plain SVG, with no logos,
// team marks or real people. It is a development tool: it needs Playwright (`npx playwright install chromium`), which is
// not a dependency of the site. The two PNGs are committed, so you only run this to change them.
//   node scripts/make-social-image.mjs
import { readFileSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const out = resolve(here, '../public');

// The site's own fonts (the @fontsource files in node_modules), embedded so the drawing uses them.
const font = (pkg, file, family, weight) =>
  `@font-face{font-family:'${family}';font-weight:${weight};src:url(data:font/woff2;base64,${readFileSync(resolve(here, `../node_modules/@fontsource/${pkg}/files/${file}.woff2`)).toString('base64')}) format('woff2');}`;
const fonts = `<style>${font('barlow-condensed', 'barlow-condensed-latin-800-normal', 'Barlow Condensed', 800)}${font('barlow-condensed', 'barlow-condensed-latin-700-normal', 'Barlow Condensed', 700)}${font('barlow', 'barlow-latin-400-normal', 'Barlow', 400)}</style>`;

const ball = (x, y, r) => `
  <circle cx="${x}" cy="${y}" r="${r}" fill="#ff7a1a" stroke="#7a3a00" stroke-width="${r / 14}"/>
  <path d="M${x - r} ${y}H${x + r}M${x} ${y - r}V${y + r}M${x - r * 0.72} ${y - r * 0.72}Q${x} ${y} ${x - r * 0.72} ${y + r * 0.72}M${x + r * 0.72} ${y - r * 0.72}Q${x} ${y} ${x + r * 0.72} ${y + r * 0.72}" fill="none" stroke="#5b2a00" stroke-width="${r / 11}"/>`;

const social = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <radialGradient id="glow" cx="50%" cy="-10%" r="90%"><stop offset="0" stop-color="#26335a"/><stop offset="1" stop-color="#0b0e14"/></radialGradient>
    <linearGradient id="wood" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#c58b4b"/><stop offset="1" stop-color="#6f431c"/></linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#glow)"/>
  <rect y="540" width="1200" height="90" fill="url(#wood)"/>
  <g stroke="#00000033" stroke-width="3">${Array.from({ length: 24 }, (_, i) => `<line x1="${i * 50}" y1="540" x2="${i * 50}" y2="630"/>`).join('')}</g>
  <circle cx="300" cy="620" r="230" fill="none" stroke="#c58b4b33" stroke-width="5"/>
  <g transform="translate(820 90)">
    <rect x="200" y="0" width="22" height="230" rx="5" fill="#e9edf4"/>
    <rect x="190" y="90" width="10" height="80" fill="none" stroke="#ff7a1a" stroke-width="4"/>
    <line x1="60" y1="170" x2="200" y2="170" stroke="#ff7a1a" stroke-width="12" stroke-linecap="round"/>
    <circle cx="60" cy="170" r="9" fill="#ff7a1a"/>
    <path d="M68 176L86 300M94 176L102 300M122 176V300M150 176L142 300M176 176L158 300M76 212H170M84 248H162M92 284H154" fill="none" stroke="#f1f3f7" stroke-width="3.5" opacity="0.85"/>
    ${ball(122, 120, 34)}
    <g stroke="#ffb23f" stroke-width="5" stroke-linecap="round" opacity="0.55" stroke-dasharray="2 22"><path d="M-160 420Q-20 -60 118 110" fill="none"/></g>
  </g>
  <text x="70" y="280" font-family="'Barlow Condensed', 'Arial Narrow', Impact, sans-serif" font-size="190" font-weight="800" fill="#f1f3f7" letter-spacing="6">DEEP CUT</text>
  <text x="76" y="360" font-family="'Barlow Condensed', 'Arial Narrow', Impact, sans-serif" font-size="58" font-weight="700" fill="#ffb23f" letter-spacing="4">THE OBVIOUS ANSWER LOSES</text>
  <text x="76" y="440" font-family="Barlow, Arial, sans-serif" font-size="36" fill="#a3afc1">A daily basketball trivia game. Seven prompts, 25 seconds each.</text>
  <g transform="translate(76 480)">
    ${['#cfd6e2', '#5aa2ff', '#3ed28a', '#ffd23f', '#ff8a2b', '#b66bff'].map((c, i) => `<rect x="${i * 62}" y="0" width="50" height="50" rx="9" fill="${c}"/><text x="${i * 62 + 25}" y="36" text-anchor="middle" font-family="'Barlow Condensed', Arial, sans-serif" font-size="32" font-weight="800" fill="#10151d">${i + 1}</text>`).join('')}
  </g>
</svg>`;

const icon = `<svg xmlns="http://www.w3.org/2000/svg" width="180" height="180" viewBox="0 0 64 64">
  <rect width="64" height="64" fill="#0b0e14"/>
  <rect x="3" y="3" width="58" height="58" rx="11" fill="none" stroke="#c58b4b" stroke-width="3"/>
  ${ball(32, 32, 17)}
</svg>`;

const { chromium } = createRequire(import.meta.url)('playwright');
const browser = await chromium.launch();
for (const [name, svg, width, height] of [['social.png', social, 1200, 630], ['apple-touch-icon.png', icon, 180, 180]]) {
  const page = await browser.newPage({ viewport: { width, height } });
  await page.setContent(`${fonts}<body style="margin:0">${svg}</body>`);
  await page.evaluate(() => document.fonts.ready);
  writeFileSync(resolve(out, name), await page.screenshot({ type: 'png' }));
  await page.close();
}
await browser.close();
console.log('wrote social.png and apple-touch-icon.png');
