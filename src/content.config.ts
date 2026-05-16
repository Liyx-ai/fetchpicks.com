import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/data/posts' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
    updatedDate: z.date().optional(),
    heroImage: z.string().optional(),
    category: z.enum([
      'dog-food',
      'dog-treats',
      'dog-health',
      'dog-gear',
      'dog-training',
      'dog-toys',
      'cat-supplies',
      'guides',
      'comparisons',
    ]),
    tags: z.array(z.string()).default([]),
    featured: z.boolean().default(false),
    affiliate: z.boolean().default(true),
  }),
});

export const collections = { posts };
