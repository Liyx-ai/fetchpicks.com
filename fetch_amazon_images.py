#!/usr/bin/env python3
"""
Fetch real Amazon product images for FetchPicks.com affiliate site.

Replaces AI-generated placeholder images with actual product images from Amazon.
Uses playwright-cli for browser automation (handles JavaScript-rendered pages).
Implements rate limiting and error handling to avoid Amazon blocking.

Usage:
    python fetch_amazon_images.py                    # Fetch all products
    python fetch_amazon_images.py --category dog-food # Fetch only one category
    python fetch_amazon_images.py --dry-run           # Show what would be fetched
    python fetch_amazon_images.py --start 0 --count 5 # Batch: first 5 products
"""

import os
import sys
import time
import json
import subprocess
import re
import urllib.parse
import argparse
from pathlib import Path
from datetime import datetime

AFFILIATE_TAG = "fetchpicks20-20"
BASE_DIR = Path("D:/fetchpicks-site")
IMAGES_DIR = BASE_DIR / "public" / "images" / "posts"
OUTPUT_DIR = BASE_DIR

# =============================================================================
# COMPLETE PRODUCT IMAGE MAPPING
# Extracted from generate_content.py articles
# Format: (image_filename, amazon_search_query, category, article_slug)
# =============================================================================
PRODUCTS = [
    # === Dog Food ===
    ("product-orijen", "Orijen Original Dog Food 30lb", "dog-food", "best-dry-dog-food-2026"),
    ("product-taste-wild", "Taste of the Wild High Prairie dog food", "dog-food", "best-dry-dog-food-2026"),
    ("product-blue-buffalo", "Blue Buffalo Life Protection dog food", "dog-food", "best-dry-dog-food-2026"),
    ("product-purina-pro", "Purina Pro Plan dog food 30lb", "dog-food", "best-dry-dog-food-2026"),
    ("product-wellness-core", "Wellness CORE Grain-Free dog food", "dog-food", "best-dry-dog-food-2026"),
    ("product-hills-science", "Hill's Science Diet Wet Dog Food canned", "dog-food", "best-wet-dog-food"),
    ("product-royal-canin-wet", "Royal Canin Canned Dog Food wet", "dog-food", "best-wet-dog-food"),
    ("product-blue-buffalo-wet", "Blue Buffalo Homestyle Recipe wet dog food", "dog-food", "best-wet-dog-food"),
    ("product-purina-pro-wet", "Purina Pro Plan Canned dog food", "dog-food", "best-wet-dog-food"),
    ("product-purina-one", "Purina ONE SmartBlend dog food", "dog-food", "cheap-dog-food-thats-still-healthy"),
    ("product-iams", "IAMS Proactive Health dog food", "dog-food", "cheap-dog-food-thats-still-healthy"),
    ("product-diamond-naturals", "Diamond Naturals dog food", "dog-food", "cheap-dog-food-thats-still-healthy"),
    ("product-pedigree", "Pedigree Adult dog food", "dog-food", "best-dry-dog-food-2026"),
    ("product-rachael-ray", "Rachael Ray Nutrish dog food", "dog-food", "best-dry-dog-food-2026"),
    ("product-blue-buffalo-puppy", "Blue Buffalo Life Protection Puppy dog food", "dog-food", "best-puppy-food"),
    ("product-purina-pro-puppy", "Purina Pro Plan Puppy dog food large breed", "dog-food", "best-puppy-food"),
    ("product-hills-puppy", "Hill's Science Diet Puppy dog food", "dog-food", "best-puppy-food"),
    ("product-royal-canin-puppy", "Royal Canin Puppy dog food", "dog-food", "best-puppy-food"),
    ("product-canidae-pure", "Canidae PURE Grain-Free dog food", "dog-food", "best-grain-free-dog-food"),
    ("product-merrick-grainfree", "Merrick Grain-Free Texas Beef dog food", "dog-food", "best-grain-free-dog-food"),

    # === Dog Gear (Harnesses, Beds) ===
    ("product-ruffwear", "Ruffwear Front Range Harness dog", "dog-gear", "best-dog-harnesses"),
    ("product-kong-harness", "Kong Comfort Dog Harness", "dog-gear", "best-dog-harnesses"),
    ("product-rabbitgoo", "Rabbitgoo No-Pull Dog Harness", "dog-gear", "best-dog-harnesses"),
    ("product-ruffwear-flagline", "Ruffwear Flagline Harness dog", "dog-gear", "best-dog-harnesses"),
    ("product-big-barker", "Big Barker Orthopedic Dog Bed", "dog-gear", "best-orthopedic-dog-beds"),
    ("product-petfusion", "PetFusion Ultimate Dog Bed", "dog-gear", "best-orthopedic-dog-beds"),
    ("product-furhaven", "FurHaven Orthopedic Dog Bed", "dog-gear", "best-orthopedic-dog-beds"),

    # === Dog Health ===
    ("product-cosequin", "Cosequin Joint Health Supplement for dogs", "dog-health", "best-dog-joint-supplements"),
    ("product-dasuquin", "Nutramax Dasuquin dog supplement", "dog-health", "best-dog-joint-supplements"),
    ("product-zesty-paws-joint", "Zesty Paws Mobility Bites dog joint", "dog-health", "best-dog-joint-supplements"),
    ("product-zesty-paws-multi", "Zesty Paws 8-in-1 Bites dog multivitamin", "dog-health", "best-dog-multivitamins"),
    ("product-pethonesty", "PetHonesty 10-in-1 Daily Supplement dog", "dog-health", "best-dog-multivitamins"),
    ("product-vets-best", "Vet's Best Multivitamin for dogs", "dog-health", "best-dog-multivitamins"),
    ("product-greenies", "Greenies Dental Dog Treats", "dog-health", "best-dental-chews-for-dogs"),
    ("product-oravet", "OraVet Dental Hygiene Chews for dogs", "dog-health", "best-dental-chews-for-dogs"),
    ("product-virbac-cet", "Virbac CET Enzymatic Chews for dogs", "dog-health", "best-dental-chews-for-dogs"),

    # === Dog Toys ===
    ("product-kong-classic", "Kong Classic Dog Toy red rubber", "dog-toys", "best-dog-toys-for-aggressive-chewers"),
    ("product-goughnuts", "Goughnuts Maxx 50 Stick dog toy", "dog-toys", "best-dog-toys-for-aggressive-chewers"),
    ("product-nylabone", "Nylabone Dura Chew Textured dog", "dog-toys", "best-dog-toys-for-aggressive-chewers"),
    ("product-chuckit", "Chuckit Ultra Ball dog toy", "dog-toys", "best-dog-toys-for-aggressive-chewers"),
    ("product-west-paw", "West Paw Zogoflex dog toy tough", "dog-toys", "best-dog-toys-for-aggressive-chewers"),

    # === Dog Treats ===
    ("product-zukes-mini", "Zuke's Mini Naturals dog training treats", "dog-treats", "best-dog-treats-for-training"),
    ("product-cloud-star", "Cloud Star Tricky Trainers dog treats", "dog-treats", "best-dog-treats-for-training"),
    ("product-wellness-wellbites", "Wellness Soft WellBites dog treats", "dog-treats", "best-dog-treats-for-training"),
    ("product-nature-gnaws", "Nature Gnaws Bully Sticks for dogs", "dog-treats", "best-bully-sticks"),
    ("product-jack-pup", "Jack Pup Premium Bully Sticks for dogs", "dog-treats", "best-bully-sticks"),
    ("product-redbarn", "Redbarn 6 Inch Bully Sticks for dogs", "dog-treats", "best-bully-sticks"),
    ("product-blue-bits", "Blue Buffalo Blue Bits dog training treats", "dog-treats", "best-dog-treats-for-training"),

    # === Dog Training (Puppy treats) ===
    ("product-zukes-puppy", "Zuke's Mini Naturals Puppy Training Treats", "dog-training", "best-dog-training-treats-for-puppies"),
    ("product-blue-baby", "Blue Buffalo Baby Blue Healthy Growth dog treats", "dog-training", "best-dog-training-treats-for-puppies"),
    ("product-wellness-puppy", "Wellness Soft Puppy Bites training treats", "dog-training", "best-dog-training-treats-for-puppies"),

    # === Guides ===
    ("product-midwest-icrate", "MidWest iCrate Dog Crate", "guides", "new-puppy-essentials-checklist"),
    ("product-nylabone-puppy", "Nylabone Puppy Teething Set", "guides", "new-puppy-essentials-checklist"),

    # === New Weekly (May 24, 2026) — cat-supplies ===
    ("product-litter-robot", "Litter-Robot 4 self cleaning litter box", "cat-supplies", "best-cat-litter-boxes"),
    ("product-modkat-flip", "Modkat Flip Litter Box top entry", "cat-supplies", "best-cat-litter-boxes"),
    ("product-natures-miracle-box", "Nature's Miracle High Sided Litter Box", "cat-supplies", "best-cat-litter-boxes"),

    # === New Weekly (May 24, 2026) — dog-toys ===
    ("product-nina-ottosson-tornado", "Nina Ottosson Dog Tornado puzzle toy", "dog-toys", "best-interactive-dog-toys"),
    ("product-hide-a-squirrel", "Outward Hound Hide-A-Squirrel puzzle toy", "dog-toys", "best-interactive-dog-toys"),
    ("product-kong-goodie-bone", "KONG Goodie Bone dog treat toy", "dog-toys", "best-interactive-dog-toys"),

    # === New Weekly (May 24, 2026) — dog-training ===
    ("product-petmate-sky", "Petmate Sky Kennel dog crate travel", "dog-training", "how-to-crate-train-a-puppy"),
    ("product-kh-crate-pad", "K&H Pet Products Bolster Crate Pad", "dog-training", "how-to-crate-train-a-puppy"),
]

# Products that come from same Amazon listing (share images)
SHARED_IMAGES = {
    "product-kong-classic": "dog-toys",  # primary copy
}


def build_search_url(query):
    """Build Amazon search URL with affiliate tag."""
    encoded = urllib.parse.quote(query)
    return f"https://www.amazon.com/s?k={encoded}&tag={AFFILIATE_TAG}"


PCLI = r"D:\Program Files\NodeJS\playwright-cli.cmd"
NODE_DIR = r"D:\Program Files\NodeJS"
ENV = {**os.environ, "PATH": f"{NODE_DIR};{os.environ.get('PATH', '')}"}


def run_playwright_command(cmd, timeout=30):
    """Run a playwright-cli command and return output."""
    full_cmd = [PCLI] + cmd
    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(BASE_DIR),
            env=ENV,
            shell=False,
        )
        stdout = result.stdout or ""
        stderr = result.stderr or ""
        return stdout, stderr
    except subprocess.TimeoutExpired:
        print(f"  ⚠️  Command timed out: {' '.join(full_cmd[:3])}")
        return "", "TIMEOUT"
    except FileNotFoundError:
        print(f"  ❌ playwright-cli not found at {PCLI}")
        sys.exit(1)


def extract_image_url_from_page():
    """Extract the main product image URL from the current Amazon page."""
    # Try multiple selectors to find product images
    scripts = [
        "document.querySelector('img.s-image')?.src",
        "document.querySelector('[data-component-type=s-product-image] img')?.src",
        "document.querySelector('.s-image')?.src",
        "document.querySelector('img[alt*=\"Orijen\"], img[alt*=\"product\"]')?.src",
    ]
    for script in scripts:
        stdout, _ = run_playwright_command(
            ["eval", f"(() => {{ const el = {script}; return el ? el : null; }})()"],
            timeout=15
        )
        match = re.search(r'"([^"]+\.jpg[^"]*)"', stdout)
        if match:
            return match.group(1)
    return None


def extract_image_from_amazon_js():
    """Try to extract image URL from Amazon's JavaScript data."""
    # Amazon often stores image data in script tags
    stdout, _ = run_playwright_command(
        ["eval", """() => {
            const scripts = document.querySelectorAll('script');
            for (const s of scripts) {
                if (s.textContent.includes('imageUrl') || s.textContent.includes('s-image')) {
                    const match = s.textContent.match(/https?:\\/\\/[^"']*?\\.jpg[^"']*/);
                    if (match) return match[0];
                }
            }
            return null;
        }"""],
        timeout=15
    )
    match = re.search(r'"([^"]+\.jpg[^"]*)"', stdout)
    if match:
        return match.group(1)
    return None


def find_all_images():
    """Get all product images visible on the search results page."""
    stdout, _ = run_playwright_command(
        ["eval", """() => {
            const imgs = document.querySelectorAll('img.s-image');
            return Array.from(imgs).slice(0, 5).map(img => img.src);
        }"""],
        timeout=15
    )
    # Parse the JS array output
    urls = re.findall(r'"([^"]+\.jpg[^"]*)"', stdout)
    return urls


def upscale_amazon_url(url):
    """Convert Amazon image URL to higher resolution."""
    if not url:
        return url
    # Replace small size with large
    url = url.replace('_AC_UL320_', '_AC_SL1500_')
    url = url.replace('_AC_US160_', '_AC_SL1500_')
    url = url.replace('_AC_US200_', '_AC_SL1500_')
    url = url.replace('_AC_US230_', '_AC_SL1500_')
    url = url.replace('_AC_UL480_', '_AC_SL1500_')
    url = url.replace('_AC_SX480_', '_AC_SL1500_')
    url = url.replace('_AC_SX679_', '_AC_SL1500_')
    url = url.replace('_AC_SR180,180_', '_AC_SL1500_')
    url = url.replace('_AC_UX679_', '_AC_SL1500_')
    url = url.replace('_AC_UY679_', '_AC_SL1500_')
    return url


def download_image(url, save_path):
    """Download an image from URL to save_path using Python requests."""
    import requests as req

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.amazon.com/',
    }

    try:
        r = req.get(url, headers=headers, timeout=30)
        if r.status_code == 200 and len(r.content) > 1000:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(r.content)
            size_kb = len(r.content) / 1024
            print(f"    ✅ Downloaded ({size_kb:.0f} KB)")
            return True
        else:
            print(f"    ❌ HTTP {r.status_code}, size={len(r.content)}")
            return False
    except Exception as e:
        print(f"    ❌ Error downloading: {e}")
        return False


def fetch_single_product(img_name, search_query, category, dry_run=False):
    """Fetch the product image from Amazon for a single product."""
    save_path = IMAGES_DIR / category / f"{img_name}.jpg"

    if save_path.exists():
        size_kb = save_path.stat().st_size / 1024
        if size_kb > 5000:
            print(f"  ⏭️  {img_name}: already exists ({size_kb:.0f} KB), skipping")
            return True
        else:
            print(f"  🔄 {img_name}: exists but small ({size_kb:.0f} KB), replacing")

    if dry_run:
        print(f"  📋 {img_name}: would search '{search_query}' → {save_path}")
        return True

    # Navigate to search page
    url = build_search_url(search_query)
    stdout, stderr = run_playwright_command(
        ["goto", url],
        timeout=30
    )
    if "TIMEOUT" in stderr:
        print(f"  ⚠️  {img_name}: goto timed out, retrying once...")
        time.sleep(5)
        stdout, stderr = run_playwright_command(
            ["goto", url],
            timeout=30
        )
        if "TIMEOUT" in stderr:
            print(f"  ❌ {img_name}: goto failed twice, skipping")
            return False

    # Wait briefly for images to load
    time.sleep(3)

    # Try wait for network idle (optional, can timeout)
    run_playwright_command(["wait", "--load", "networkidle"], timeout=10)

    # Extract image URLs
    image_urls = find_all_images()

    if not image_urls:
        print(f"  ⚠️  {img_name}: no images found on page, trying backup method...")
        image_url = extract_image_url_from_page()
        if image_url:
            image_urls = [image_url]

    if not image_urls:
        print(f"  ❌ {img_name}: could not find any product image")
        return False

    # Try upscaled version first
    target_url = upscale_amazon_url(image_urls[0])
    print(f"  📥 {img_name}: {target_url[:80]}...")

    if download_image(target_url, save_path):
        return True

    # Fallback: try original size
    print(f"  🔄 {img_name}: trying original size...")
    if download_image(image_urls[0], save_path):
        return True

    print(f"  ❌ {img_name}: all download attempts failed")
    return False


def main():
    parser = argparse.ArgumentParser(description="Fetch Amazon product images for FetchPicks.com")
    parser.add_argument("--category", help="Only fetch products in this category")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without doing it")
    parser.add_argument("--start", type=int, default=0, help="Start index (for batching)")
    parser.add_argument("--count", type=int, default=100, help="Number of products to process")
    args = parser.parse_args()

    # Filter products
    products = PRODUCTS
    if args.category:
        products = [p for p in products if p[2] == args.category]
        print(f"Filtered to category '{args.category}': {len(products)} products")

    # Apply batch range
    end_idx = min(args.start + args.count, len(products))
    products = products[args.start:end_idx]
    print(f"Processing products {args.start}-{end_idx-1} ({len(products)} total)")

    if args.dry_run:
        print(f"\n{'='*60}")
        print(f"DRY RUN — No images will be downloaded")
        print(f"{'='*60}")
        idx = args.start
        for img_name, search_query, category, article in products:
            save_path = IMAGES_DIR / category / f"{img_name}.jpg"
            print(f"[{idx}] {img_name:35s} → category={category:15s} article={article}")
            print(f"     Search: '{search_query}'")
            print(f"     Save to: {save_path}")
            idx += 1
        print(f"\n{'='*60}")
        print(f"Total products: {len(products)}")
        print(f"{'='*60}")
        return

    # Summary
    print(f"\n{'='*60}")
    print(f"Starting Amazon image fetch for {len(products)} products")
    print(f"Browser: WebKit via playwright-cli")
    print(f"Rate limit: 5s between products, 15s cooldown per batch of 5")
    print(f"{'='*60}\n")

    # Start browser session
    print("🚀 Opening browser...")
    stdout, stderr = run_playwright_command(
        ["open", "--browser=webkit"],
        timeout=15
    )
    if "opened" not in stdout.lower():
        print(f"⚠️  Browser may not have opened properly: {stderr[:200]}")

    # Track stats
    stats = {"success": 0, "skipped": 0, "failed": 0, "errors": []}

    try:
        for idx, (img_name, search_query, category, article) in enumerate(products):
            print(f"\n[{idx}/{len(products)-1}] {img_name} ({search_query})")

            success = fetch_single_product(img_name, search_query, category)

            if success:
                stats["success"] += 1
            else:
                stats["failed"] += 1
                stats["errors"].append(img_name)

            # Rate limiting
            if idx < len(products) - 1:
                delay = 5
                if (idx + 1) % 5 == 0:
                    delay = 15
                    print(f"\n💤 Cooldown: {delay}s...")
                time.sleep(delay)

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    finally:
        # Always close the browser
        print("\n🔒 Closing browser...")
        run_playwright_command(["close"], timeout=10)

    # Final report
    print(f"\n{'='*60}")
    print(f"RESULTS")
    print(f"{'='*60}")
    print(f"✅ Success: {stats['success']}")
    print(f"❌ Failed:  {stats['failed']}")
    if stats["errors"]:
        print(f"Errors: {', '.join(stats['errors'])}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
