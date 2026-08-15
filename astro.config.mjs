import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Static export: Cloudflare Pages serves all files (HTML/CSS/JS/images)
// natively as static assets. No _worker.js / Functions -> no HTTP 500 / 1101
// on static assets. All pages are pre-renderable (posts & category use
// `prerender = true`; index/about/privacy/rss render at build time).
export default defineConfig({
  site: 'https://fetchpicks.com',
  integrations: [sitemap()],
  markdown: {
    shikiConfig: {
      theme: 'github-light',
    },
  },
});
