export interface CategoryMeta {
  name: string;
  desc: string;
  image: string | null;
  gradient: string;
  icon: string;
}

export const categoryMeta: Record<string, CategoryMeta> = {
  'dog-food': { name: 'Dog Food Reviews', desc: 'Honest reviews of the best dog foods - dry, wet, raw, and freeze-dried.', image: 'dog-food-hero.jpg', gradient: 'linear-gradient(135deg, #FF6740, #FFB088)', icon: '🍖' },
  'dog-treats': { name: 'Dog Treats', desc: 'Healthy and tasty treats your pup will love.', image: 'dog-treats-hero.jpg', gradient: 'linear-gradient(135deg, #F4A261, #E9C46A)', icon: '🦴' },
  'dog-health': { name: 'Dog Health', desc: 'Supplements, grooming, and wellness guides for a happy, healthy dog.', image: 'dog-health-hero.jpg', gradient: 'linear-gradient(135deg, #2A9D8F, #4ECDC4)', icon: '💊' },
  'dog-gear': { name: 'Dog Gear', desc: 'Collars, beds, leashes, and every essential your dog needs.', image: 'dog-gear-hero.jpg', gradient: 'linear-gradient(135deg, #4A90A4, #6BBFCE)', icon: '🎒' },
  'dog-training': { name: 'Training', desc: 'Tools and tips to help you train your dog effectively.', image: 'dog-training/hero-dog-training.jpg', gradient: 'linear-gradient(135deg, #9C89B8, #B8A9D4)', icon: '🎓' },
  'dog-toys': { name: 'Dog Toys', desc: 'Toys that entertain, engage, and stand up to heavy chewers.', image: 'dog-toys/hero-dog-toys.jpg', gradient: 'linear-gradient(135deg, #E87A5D, #F4A261)', icon: '🧸' },
  'cat-supplies': { name: 'Cat Supplies', desc: 'Everything for your feline friend.', image: 'cat-supplies/hero-cat-supplies.jpg', gradient: 'linear-gradient(135deg, #7B68EE, #9B8EF0)', icon: '🐱' },
  'guides': { name: 'Guides', desc: 'In-depth guides to help you make the best choices for your pet.', image: 'guides/hero-guides.jpg', gradient: 'linear-gradient(135deg, #5A5A7A, #8A8AAA)', icon: '📖' },
  'comparisons': { name: 'Comparisons', desc: 'Side-by-side product comparisons to find the winner.', image: 'comparisons/hero-comparisons.jpg', gradient: 'linear-gradient(135deg, #4A90A4, #F4A261)', icon: '⚖️' },
};

export const categoryIcons = ['🍖','🦴','💊','🎒','🎓','🧸','🐱','📖','⚖️'];
