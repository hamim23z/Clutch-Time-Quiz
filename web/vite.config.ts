import react from '@vitejs/plugin-react';
import { defineConfig, type Plugin } from 'vitest/config';
import { SITE_URL } from './src/config.ts';

/** Puts the one SITE_URL constant (src/config.ts) into the social tags of index.html. */
const siteUrl = (): Plugin => ({
  name: 'site-url',
  transformIndexHtml: (html) => html.replaceAll('%SITE_URL%', SITE_URL),
});

export default defineConfig({
  // Relative asset paths so the build works from any URL path (GitHub Pages project sites).
  base: './',
  plugins: [react(), siteUrl()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/setupTests.ts'],
    css: false,
  },
});
