import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const posts = await getCollection('posts');
  return rss({
    title: 'FetchPicks — Pet Product Reviews',
    description: 'Honest reviews and guides for the best pet products. Research-backed recommendations for your furry friend.',
    site: context.site,
    items: posts.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()).map(post => ({
      title: post.data.title,
      pubDate: post.data.pubDate,
      description: post.data.description,
      link: `/posts/${post.id}/`,
    })),
    customData: '<language>en-us</language>',
  });
}
