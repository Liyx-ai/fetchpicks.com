#!/usr/bin/env python3
"""
Scan all markdown articles for image references,
check which are missing from public/, and generate
category-colored placeholder images for any that are missing.

Usage:
    python generate_missing_images.py          # Scan and generate
    python generate_missing_images.py --check  # Report only, no generation
"""

import os
import re
import sys
from pathlib import Path
from PIL import Image, ImageDraw

BASE = Path("D:/fetchpicks-site")
POSTS_DIR = BASE / "src" / "data" / "posts"
IMAGES_DIR = BASE / "public" / "images" / "posts"
SIZE = (400, 400)

CATEGORY_PALETTES = {
    'dog-food':     ('#FF6740', '#FFB088'),
    'dog-treats':   ('#F4A261', '#E9C46A'),
    'dog-health':   ('#2A9D8F', '#4ECDC4'),
    'dog-gear':     ('#4A90A4', '#6BBFCE'),
    'dog-training': ('#9C89B8', '#B8A9D4'),
    'dog-toys':     ('#E87A5D', '#F4A261'),
    'cat-supplies': ('#7B68EE', '#9B8EF0'),
    'guides':       ('#5A5A7A', '#8A8AAA'),
    'comparisons':  ('#4A90A4', '#F4A261'),
}


def hex_to_rgb(h):
    return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))


def make_gradient(w, h, c1h, c2h):
    c1, c2 = hex_to_rgb(c1h), hex_to_rgb(c2h)
    img = Image.new('RGB', (w, h))
    for y in range(h):
        r = int(c1[0] + (c2[0] - c1[0]) * y / h)
        g = int(c1[1] + (c2[1] - c1[1]) * y / h)
        b = int(c1[2] + (c2[2] - c1[2]) * y / h)
        for x in range(w):
            img.putpixel((x, y), (r, g, b))
    return img


def wrap_text(text, max_chars=18):
    words = text.split()
    lines, cur = [], ''
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur += (' ' if cur else '') + w
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def generate_placeholder(save_path, readable_name, palette):
    img = make_gradient(SIZE[0], SIZE[1], palette[0], palette[1])
    draw = ImageDraw.Draw(img)

    lines = wrap_text(readable_name)
    cx, cy = SIZE[0] // 2, SIZE[1] // 2 - 20
    bh = 30 + len(lines) * 24
    draw.rounded_rectangle([(30, cy-30), (370, cy+bh)],
                           radius=16, fill=(255, 255, 255, 25))
    yp = cy - 10
    for line in lines:
        bb = draw.textbbox((0, 0), line)
        tw = bb[2] - bb[0]
        draw.text((cx - tw//2, yp), line, fill=(255, 255, 255, 200))
        yp += 22

    save_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(save_path), 'JPEG', quality=80)


def extract_cat_from_path(ref):
    """Extract category name from image path like /images/posts/dog-food/product-xxx.jpg"""
    parts = ref.strip('/').split('/')
    if len(parts) >= 3:
        return parts[2]   # e.g. "dog-food"
    return None


def readable_name(filename):
    """Convert product-foo-bar.jpg to Foo Bar"""
    name = filename.replace('product-', '').replace('-', ' ').title()
    # Remove file extension
    name = re.sub(r'\.(jpg|png|webp|jpeg)$', '', name, flags=re.IGNORECASE)
    return name


def main():
    check_only = '--check' in sys.argv or '-c' in sys.argv

    # Step 1: Collect all image references from markdown files
    pattern = re.compile(r'!\[.*?\]\(/images/posts/[^)]+\.(jpg|png|webp|jpeg)\)', re.IGNORECASE)
    all_refs = set()

    for md_file in POSTS_DIR.glob('*.md'):
        text = md_file.read_text(encoding='utf-8')
        for m in pattern.finditer(text):
            # Extract path portion: /images/posts/xxx/yyy.jpg
            ref = m.group(0)
            path_match = re.search(r'/images/posts/[^)]+\.(jpg|png|webp|jpeg)', ref, re.IGNORECASE)
            if path_match:
                all_refs.add(path_match.group(0))

    if not all_refs:
        print("No image references found in articles.")
        return

    # Step 2: Check each reference against public/
    missing = []
    for ref in sorted(all_refs):
        file_path = IMAGES_DIR.parent.parent / ref.lstrip('/')  # public/images/posts/...
        if not file_path.exists():
            missing.append(ref)

    print(f"Image refs: {len(all_refs)} total, {len(missing)} missing, {len(all_refs)-len(missing)} present")

    if not missing:
        print("All images present. Nothing to do.")
        return

    if check_only:
        print("\nMissing images (--check mode, not generating):")
        for m in missing:
            print(f"  {m}")
        return

    # Step 3: Generate placeholders for missing images
    generated = 0
    for ref in missing:
        # e.g., /images/posts/dog-food/product-xxx.jpg
        cat = extract_cat_from_path(ref) or 'guides'
        palette = CATEGORY_PALETTES.get(cat, ('#5A5A7A', '#8A8AAA'))

        filename = Path(ref).name
        save_path = IMAGES_DIR / cat / filename
        name = readable_name(filename)

        generate_placeholder(save_path, name, palette)
        print(f"  Generated: {save_path.relative_to(BASE)}")
        generated += 1

    print(f"\nGenerated {generated} placeholder images for {len(missing)} missing references.")


if __name__ == '__main__':
    main()
