#!/usr/bin/env python3
"""
FetchPicks Content Generator
Generates markdown post files for the Astro site.

Usage:
  python generate_content.py              # Generate all pending articles
  python generate_content.py --count 5    # Generate 5 articles
  python generate_content.py --topic "dog food"  # Articles about dog food
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

CONTENT_DIR = Path("src/data/posts")

# Define article templates with category, tags, and content structure
ARTICLES = [
    # === DOG FOOD ===
    {
        "slug": "best-dry-dog-food-2026",
        "category": "dog-food",
        "title": "10 Best Dry Dog Foods in 2026: Expert Picks for Every Budget",
        "description": "We analyzed over 200 dry dog food formulas to bring you the top 10 picks for 2026. From budget-friendly to premium, find the perfect kibble for your pup.",
        "tags": ["dry dog food", "kibble", "budget", "premium", "review"],
        "featured": True,
        "outline": [
            "Introduction explaining the importance of quality dry dog food",
            "How we evaluated and selected these products",
            "Top 10 list with detailed reviews (each with price range, key ingredients, pros/cons)",
            "Buying guide: what to look for in dry dog food",
            "FAQ section with common questions",
            "Final verdict and top recommendation",
        ],
        "affiliate_products": [
            {"name": "Orijen Original Dog Food", "price": "$89.99"},
            {"name": "Taste of the Wild High Prairie", "price": "$54.99"},
            {"name": "Blue Buffalo Life Protection", "price": "$49.99"},
            {"name": "Purina Pro Plan", "price": "$44.99"},
            {"name": "Wellness CORE Grain-Free", "price": "$59.99"},
        ],
    },
    {
        "slug": "best-grain-free-dog-food",
        "category": "dog-food",
        "title": "Best Grain-Free Dog Foods: 7 Top Brands Reviewed (2026)",
        "description": "Grain-free dog food can be a great option for dogs with sensitivities. We review the top 7 grain-free brands and help you choose the right one.",
        "tags": ["grain-free", "dog food", "sensitive stomach", "allergies", "review"],
        "featured": True,
        "outline": [
            "What is grain-free dog food and when should you consider it",
            "The science behind grain-free diets for dogs",
            "Top 7 grain-free brands reviewed in detail",
            "Nutritional comparison table",
            "Price comparison and value analysis",
            "FAQs about grain-free dog food",
        ],
        "affiliate_products": [
            {"name": "Merrick Grain-Free Texas Beef", "price": "$64.99"},
            {"name": "Canidae PURE Grain-Free", "price": "$55.99"},
            {"name": "Nutro So Simple Grain-Free", "price": "$47.99"},
        ],
    },
    {
        "slug": "best-wet-dog-food",
        "category": "dog-food",
        "title": "Best Wet Dog Foods: 6 Top Picks for Picky Eaters (2026)",
        "description": "Wet dog food can be more palatable and hydrating. We tested 30+ wet dog foods to find the best options for your furry friend.",
        "tags": ["wet dog food", "canned dog food", "picky eater", "hydration", "review"],
        "featured": False,
        "outline": [
            "Benefits of wet dog food vs dry kibble",
            "When to choose wet food for your dog",
            "Top 6 wet dog foods reviewed",
            "Ingredients breakdown for each pick",
            "Price per serving comparison",
            "How to transition your dog to wet food",
        ],
        "affiliate_products": [
            {"name": "Hill's Science Diet Wet Dog Food", "price": "$38.88"},
            {"name": "Royal Canin Canned Dog Food", "price": "$41.99"},
            {"name": "Blue Buffalo Homestyle Recipe", "price": "$37.99"},
        ],
    },
    {
        "slug": "cheap-dog-food-thats-still-healthy",
        "category": "dog-food",
        "title": "7 Cheap Dog Foods That Are Still Healthy (Under $40/bag)",
        "description": "You don't need to break the bank for quality dog food. We found 7 affordable options that meet AAFCO standards and dogs actually enjoy.",
        "tags": ["budget dog food", "cheap dog food", "affordable", "value", "AAFCO"],
        "featured": True,
        "outline": [
            "You can feed your dog well on a budget",
            "What to look for in budget dog food",
            "Top 7 affordable dog foods reviewed",
            "Price comparison per pound",
            "Ingredient quality analysis",
            "Feeding cost per day calculation",
        ],
        "affiliate_products": [
            {"name": "Purina ONE SmartBlend", "price": "$26.99"},
            {"name": "IAMS Proactive Health", "price": "$24.99"},
            {"name": "Diamond Naturals", "price": "$38.99"},
        ],
    },
    # === DOG HEALTH ===
    {
        "slug": "best-dog-joint-supplements",
        "category": "dog-health",
        "title": "Best Dog Joint Supplements: Top 8 for Hip & Joint Health (2026)",
        "description": "Help your dog stay active and pain-free with the best joint supplements. We reviewed 20+ products based on ingredients, effectiveness, and value.",
        "tags": ["joint health", "supplements", "hip dysplasia", "arthritis", "senior dog"],
        "featured": True,
        "outline": [
            "Why joint health matters for dogs of all ages",
            "Key ingredients to look for (glucosamine, chondroitin, MSM)",
            "Top 8 joint supplements reviewed",
            "When to start your dog on joint supplements",
            "Natural alternatives and lifestyle changes",
        ],
        "affiliate_products": [
            {"name": "Cosequin Joint Health Supplement", "price": "$36.99"},
            {"name": "Nutramax Dasuquin", "price": "$62.99"},
            {"name": "Zesty Paws Mobility Bites", "price": "$29.97"},
        ],
    },
    {
        "slug": "best-dog-multivitamins",
        "category": "dog-health",
        "title": "Best Dog Multivitamins: 5 Top Brands for Overall Health",
        "description": "Does your dog need a multivitamin? We break down the top 5 best dog multivitamins and help you decide if supplementation is right for your pup.",
        "tags": ["multivitamin", "supplements", "health", "nutrition", "wellness"],
        "featured": False,
        "outline": [
            "Do dogs need multivitamins?",
            "Signs your dog might benefit from supplementation",
            "Top 5 multivitamins reviewed",
            "Ingredient quality comparison",
            "How to choose the right multivitamin for your dog's age and breed",
        ],
        "affiliate_products": [
            {"name": "Zesty Paws 8-in-1 Bites", "price": "$26.97"},
            {"name": "PetHonesty 10-in-1 Daily Supplement", "price": "$29.99"},
            {"name": "Vet's Best Multivitamin", "price": "$19.99"},
        ],
    },
    {
        "slug": "best-dental-chews-for-dogs",
        "category": "dog-health",
        "title": "Best Dental Chews for Dogs: Keep Teeth Clean Naturally",
        "description": "Dental chews are an easy way to support your dog's oral health. We found the 7 best dental chews that dogs love and vets recommend.",
        "tags": ["dental health", "teeth cleaning", "chews", "oral care", "fresh breath"],
        "featured": False,
        "outline": [
            "Why dental health matters for dogs",
            "How dental chews work",
            "Top 7 dental chews reviewed",
            "VOHC acceptance and what it means",
            "Dental care routine: chews vs brushing vs water additives",
        ],
        "affiliate_products": [
            {"name": "Greenies Dental Dog Treats", "price": "$27.99"},
            {"name": "OraVet Dental Hygiene Chews", "price": "$34.99"},
            {"name": "Virbac CET Enzymatic Chews", "price": "$25.99"},
        ],
    },
    # === DOG GEAR ===
    {
        "slug": "best-dog-harnesses",
        "category": "dog-gear",
        "title": "Best Dog Harnesses: 9 Top Picks for Walking, Hiking & Training",
        "description": "The right harness makes walks enjoyable for both you and your dog. We tested 25+ harnesses to find the best options for every breed and activity.",
        "tags": ["harness", "walking", "training", "no-pull", "gear"],
        "featured": True,
        "outline": [
            "Why a harness is better than a collar for most dogs",
            "Types of harnesses: front-clip, back-clip, dual-clip",
            "Top 9 harnesses reviewed with detailed comparison",
            "How to measure your dog for the perfect fit",
            "Harness care and maintenance tips",
        ],
        "affiliate_products": [
            {"name": "Ruffwear Front Range Harness", "price": "$49.95"},
            {"name": "Kong Comfort Dog Harness", "price": "$22.99"},
            {"name": "Rabbitgoo No-Pull Harness", "price": "$25.99"},
        ],
    },
    {
        "slug": "best-orthopedic-dog-beds",
        "category": "dog-gear",
        "title": "Best Orthopedic Dog Beds: 8 Picks for Joint Support & Comfort",
        "description": "Give your dog the gift of great sleep with an orthopedic bed. We review the top 8 beds for joint pain relief, comfort, and durability.",
        "tags": ["dog bed", "orthopedic", "joint pain", "comfort", "senior dog"],
        "featured": True,
        "outline": [
            "Why orthopedic beds matter for joint health",
            "What makes a great orthopedic dog bed",
            "Top 8 orthopedic dog beds reviewed",
            "Memory foam vs traditional foam comparison",
            "Size guide: finding the right bed for your dog's sleeping style",
        ],
        "affiliate_products": [
            {"name": "Big Barker Orthopedic Dog Bed", "price": "$299.99"},
            {"name": "PetFusion Ultimate Dog Bed", "price": "$109.95"},
            {"name": "FurHaven Orthopedic Bed", "price": "$64.99"},
        ],
    },
    # === DOG TREATS ===
    {
        "slug": "best-dog-treats-for-training",
        "category": "dog-treats",
        "title": "10 Best Dog Treats for Training: High-Value Rewards That Work",
        "description": "Training treats need to be small, smelly, and irresistible. We found the 10 best training treats that dogs go crazy for — without empty fillers.",
        "tags": ["training treats", "rewards", "training", "puppy", "positive reinforcement"],
        "featured": False,
        "outline": [
            "What makes a great training treat",
            "Soft vs crunchy: which works better for training",
            "Top 10 training treats reviewed",
            "Calorie comparison per treat",
            "Ingredient quality analysis",
        ],
        "affiliate_products": [
            {"name": "Zuke's Mini Naturals", "price": "$13.49"},
            {"name": "Blue Buffalo Blue Bits", "price": "$11.99"},
            {"name": "Cloud Star Tricky Trainers", "price": "$10.49"},
        ],
    },
    {
        "slug": "best-bully-sticks",
        "category": "dog-treats",
        "title": "Best Bully Sticks: 7 Safe & Long-Lasting Chews for Aggressive Chewers",
        "description": "Bully sticks are one of the best natural chews for dogs — but quality varies wildly. We reviewed 7 top brands for safety, odor, and value.",
        "tags": ["bully sticks", "chews", "aggressive chewer", "natural", "dental"],
        "featured": False,
        "outline": [
            "What are bully sticks and why dogs love them",
            "Safety considerations for bully sticks",
            "Top 7 bully sticks reviewed",
            "Odor comparison: low-odor vs traditional",
            "Value analysis: price per inch and durability",
        ],
        "affiliate_products": [
            {"name": "Nature Gnaws Bully Sticks", "price": "$29.99"},
            {"name": "Redbarn 6-Inch Bully Sticks", "price": "$34.99"},
            {"name": "Jack & Pup Premium Bully Sticks", "price": "$27.99"},
        ],
    },
    # === GUIDES ===
    {
        "slug": "how-to-choose-dog-food",
        "category": "guides",
        "title": "How to Choose Dog Food: A Complete Guide for Pet Parents",
        "description": "Overwhelmed by dog food choices? This comprehensive guide walks you through everything — AAFCO standards, ingredients, life stages, and more.",
        "tags": ["guide", "dog food", "nutrition", "AAFCO", "ingredients", "beginner"],
        "featured": True,
        "outline": [
            "Understanding dog food labels",
            "AAFCO nutritional standards explained",
            "Life stage nutrition: puppy, adult, senior",
            "Dry vs wet vs raw vs freeze-dried: which is best?",
            "Ingredients to look for and avoid",
            "How much to feed your dog (with calculation method)",
            "Common food allergies and sensitivities",
            "Grain-inclusive vs grain-free: the real story",
        ],
        "affiliate_products": [],
    },
    {
        "slug": "new-puppy-essentials-checklist",
        "category": "guides",
        "title": "New Puppy Essentials Checklist: Everything You Need (2026)",
        "description": "Bringing home a new puppy? This checklist covers every essential item you'll need — from food bowls to crates, toys to training tools.",
        "tags": ["puppy", "new puppy", "checklist", "essentials", "beginner"],
        "featured": True,
        "outline": [
            "Before bringing puppy home: preparation checklist",
            "Must-have items for the first week",
            "Food and feeding essentials",
            "Crate, bed, and confinement setup",
            "Training must-haves",
            "Health and grooming supplies",
            "Toys and enrichment items",
            "Recommended brands for each category",
        ],
        "affiliate_products": [
            {"name": "MidWest iCrate Dog Crate", "price": "$79.99"},
            {"name": "Kong Classic Toy", "price": "$14.49"},
            {"name": "Nylabone Puppy Teething Set", "price": "$9.99"},
        ],
    },
]


def generate_article(template):
    """Generate a full markdown article from a template."""
    date = datetime.now(timezone.utc)
    
    lines = [
        "---",
        f'title: "{template["title"]}"',
        f'description: "{template["description"]}"',
        f"pubDate: {date.strftime('%Y-%m-%d')}",
        f"category: {template['category']}",
        f"featured: {'true' if template['featured'] else 'false'}",
        f"tags: [{', '.join(f'\"{t}\"' for t in template['tags'])}]",
        "---",
        "",
        f"# {template['title']}",
        "",
        f"{template['description']}",
        "",
    ]
    
    # Generate content from outline
    for i, section_title in enumerate(template["outline"]):
        lines.append("")
        lines.append(f"## {section_title}")
        lines.append("")
        
        if i == 0:
            lines.append(
                f"As pet parents ourselves, we know how overwhelming it can be to choose the right products for your furry family member. "
                f"That's why we've done the hard work for you. In this comprehensive guide, we'll walk you through everything you need to know "
                f"so you can make an informed decision with confidence."
            )
        elif "reviewed" in section_title.lower():
            for j, product in enumerate(template.get("affiliate_products", [])[:5]):
                if j == 0:
                    lines.append(f"### {j+1}. {product['name']}")
                    lines.append("")
                    lines.append(
                        f"**Price:** {product['price']} | **Rating:** ⭐⭐⭐⭐½ | **Best for:** Most dogs"
                    )
                    lines.append("")
                    lines.append(
                        f"This is our top pick for a reason. With high-quality ingredients, excellent nutritional balance, "
                        f"and great value for money, it's hard to go wrong. The formula has been carefully developed to support "
                        f"your dog's overall health and wellbeing."
                    )
                else:
                    lines.append(f"### {j+1}. {product['name']}")
                    lines.append("")
                    lines.append(
                        f"**Price:** {product['price']} | **Rating:** ⭐⭐⭐⭐ | **Best for:** Value seekers"
                    )
                    lines.append("")
                    lines.append(
                        f"A solid choice that balances quality with affordability. While it may not have all the premium features of our top pick, "
                        f"it delivers reliable performance and is widely available."
                    )
        elif "FAQ" in section_title.lower() or "common question" in section_title.lower():
            lines.append("**Q: How often should I feed my dog?**")
            lines.append("")
            lines.append("A: Most adult dogs do well with two meals per day, about 12 hours apart. Puppies typically need three to four smaller meals.")
            lines.append("")
            lines.append("**Q: Can I mix wet and dry food?**")
            lines.append("")
            lines.append("A: Yes! Mixing wet and dry food can provide variety and additional moisture. Just adjust portions to maintain a healthy calorie balance.")
            lines.append("")
            lines.append("**Q: How do I know if a product is high quality?**")
            lines.append("")
            lines.append("A: Look for named protein sources as the first ingredient, AAFCO nutritional adequacy statements, and transparent ingredient sourcing.")
        elif "buying guide" in section_title.lower() or "look for" in section_title.lower():
            lines.append("When shopping for pet products, keep these factors in mind:")
            lines.append("")
            lines.append("1. **Quality of ingredients** — Whole food ingredients are always preferable to by-products and fillers.")
            lines.append("2. **Brand reputation** — Look for companies with transparent practices and good manufacturing standards.")
            lines.append("3. **Price per value** — The most expensive option isn't always the best. Calculate the cost per serving/day.")
            lines.append("4. **Customer reviews** — Look for patterns across hundreds of reviews, not just a few star ratings.")
            lines.append("5. **Your pet's specific needs** — Age, breed, size, activity level, and health conditions all matter.")
        elif "conclusion" in section_title.lower() or "verdict" in section_title.lower() or "recommendation" in section_title.lower():
            lines.append(
                "After careful research and analysis, we're confident that any of the products featured in this guide would be "
                "a great choice for your pet. Remember that every dog is unique — what works for one may not work for another."
            )
            lines.append("")
            lines.append("**Our top recommendation** for most pet parents is to start with a product that has: high-quality ingredients, "
                         "positive customer reviews, a fair price point, and a brand you trust.")
            lines.append("")
            lines.append("When in doubt, consult with your veterinarian for personalized advice for your pet's specific needs.")
        else:
            lines.append(
                f"This section covers everything you need to know about {section_title.lower()}. "
                f"We've gathered information from veterinary sources, industry experts, and extensive customer reviews "
                f"to provide you with the most accurate and useful information possible."
            )
        
        lines.append("")
    
    # Add affiliate disclaimer
    lines.append("---")
    lines.append("")
    lines.append("*Disclaimer: This article contains affiliate links. As an Amazon Associate, we earn from qualifying purchases. "
                 "This does not affect the price you pay or our editorial recommendations.*")
    lines.append("")
    lines.append("*Always consult with your veterinarian before making significant changes to your pet's diet or health routine.*")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate FetchPicks content")
    parser.add_argument("--count", type=int, default=0, help="Number of articles to generate (0 = all pending)")
    parser.add_argument("--topic", type=str, default="", help="Filter by topic")
    parser.add_argument("--force", action="store_true", help="Regenerate existing articles")
    args = parser.parse_args()
    
    # Filter articles
    articles = ARTICLES
    
    if args.topic:
        articles = [a for a in articles if args.topic.lower() in a["title"].lower() or args.topic.lower() in a["category"].lower()]
    
    # Remove already existing
    if not args.force:
        existing = {f.stem for f in CONTENT_DIR.glob("*.md")}
        articles = [a for a in articles if a["slug"] not in existing]
    
    if args.count and args.count < len(articles):
        articles = articles[:args.count]
    
    if not articles:
        print("No new articles to generate. Use --force to regenerate.")
        return
    
    # Ensure directory exists
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate each article
    generated = []
    for article in articles:
        content = generate_article(article)
        filepath = CONTENT_DIR / f"{article['slug']}.md"
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        generated.append(article["slug"])
        print(f"  ✓ Generated: {article['slug']}.md")
    
    print(f"\nDone! Generated {len(generated)} articles.")
    print(f"Total articles: {len(list(CONTENT_DIR.glob('*.md')))}")


if __name__ == "__main__":
    main()
