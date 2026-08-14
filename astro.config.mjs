import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  output: 'server',
  adapter: cloudflare({
    imageService: 'passthrough',
  }),
  site: 'https://fetchpicks.com',
  integrations: [sitemap()],
  markdown: {
    shikiConfig: {
      theme: 'github-light',
    },
  },
  build: {
    format: 'directory',
  },
});
