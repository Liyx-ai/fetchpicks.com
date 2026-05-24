#!/usr/bin/env python3
"""
Generate ALL missing images for fetchpicks.com.
交叉比对文章引用 vs 磁盘文件，生成所有缺失图片（英雄图 + 产品图）。
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = r'D:\fetchpicks-site\public\images\posts'

# ── 所有文章引用的图片（来自 grep 结果） ──
REFERENCED = set()
for line in sys.stdin:
    path = line.strip()
    if path:
        REFERENCED.add(path)

# ── 已有图片 ──
EXISTING = set()
for root, dirs, files in os.walk(ROOT):
    for f in files:
        if f.lower().endswith(('.jpg', '.png', '.webp')):
            rel = os.path.relpath(os.path.join(root, f), ROOT).replace('\\', '/')
            EXISTING.add(f'/images/posts/{rel}')

MISSING = REFERENCED - EXISTING

if not MISSING:
    print('No missing images!')
    sys.exit(0)

print(f'Missing {len(MISSING)} images. Generating...')

# ── Color palette ──
COLORS = [
    ('#4A90D9', '#357ABD'), ('#50B86C', '#3E9657'), ('#D9754A', '#C05E3A'),
    ('#9B59B6', '#8E44AD'), ('#E74C3C', '#C0392B'), ('#2ECC71', '#27AE60'),
    ('#F39C12', '#E67E22'), ('#1ABC9C', '#16A085'), ('#3498DB', '#2980B9'),
    ('#E84393', '#D6336C'), ('#6C5CE7', '#5B3CC4'), ('#00B894', '#009877'),
]
color_idx = 0

def make_gradient(bg_start, bg_end, img):
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for i in range(h):
        ratio = i / h
        r = int(int(bg_start[1:3], 16) * (1-ratio) + int(bg_end[1:3], 16) * ratio)
        g = int(int(bg_start[3:5], 16) * (1-ratio) + int(bg_end[3:5], 16) * ratio)
        b = int(int(bg_start[5:7], 16) * (1-ratio) + int(bg_end[5:7], 16) * ratio)
        draw.line([(0, i), (w-1, i)], fill=(r, g, b))
    return draw

def generate_hero(cat, name, path):
    """Generate hero image — 1024x1024 gradient with category name"""
    bg_start, bg_end = COLORS[color_idx % len(COLORS)]
    img = Image.new('RGB', (1024, 1024), bg_start)
    draw = make_gradient(bg_start, bg_end, img)
    
    try:
        font_title = ImageFont.truetype('arial.ttf', 56)
        font_sub = ImageFont.truetype('arial.ttf', 28)
    except:
        font_title = ImageFont.load_default()
        font_sub = font_title
    
    display_name = cat.replace('-', ' ').title()
    bbox = draw.textbbox((0, 0), display_name, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text(((1024 - tw) // 2, 430), display_name, fill=(255,255,255), font=font_title)
    
    draw.text((340, 520), 'FetchPicks.com', fill=(220,220,220), font=font_sub)
    draw.text((390, 560), '★', fill=(255,215,0), font=font_sub)
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, 'JPEG', quality=85)
    print(f'  [HERO] {name}')

def generate_product(cat, name, path):
    """Generate product placeholder — 500x500 gradient with product name"""
    global color_idx
    bg_start, bg_end = COLORS[color_idx % len(COLORS)]
    color_idx += 1
    
    img = Image.new('RGB', (500, 500), bg_start)
    draw = make_gradient(bg_start, bg_end, img)
    
    # White box silhouette
    draw.rounded_rectangle([(150, 120), (350, 370)], radius=20, fill=(255,255,255,20))
    
    try:
        font_large = ImageFont.truetype('arial.ttf', 22)
        font_small = ImageFont.truetype('arial.ttf', 16)
    except:
        font_large = ImageFont.load_default()
        font_small = font_large
    
    display_name = name.replace('product-', '').replace('-', ' ').title()
    bbox = draw.textbbox((0, 0), display_name, font=font_large)
    tw = bbox[2] - bbox[0]
    draw.text(((500 - tw) // 2, 200), display_name, fill=(255,255,255), font=font_large)
    draw.text((195, 270), 'Product Image', fill=(200,200,200), font=font_small)
    draw.text((205, 295), 'Coming Soon', fill=(180,180,180), font=font_small)
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, 'JPEG', quality=80)
    print(f'  [PROD] {cat}/{name}')

count = 0
for img_path in sorted(MISSING):
    rel = img_path.replace('/images/posts/', '')
    parts = rel.split('/')
    
    full_path = os.path.join(ROOT, *parts)
    
    if os.path.exists(full_path):
        continue
    
    if parts[-1].startswith('hero-'):
        cat_name = parts[0]
        filename = parts[-1]
        generate_hero(cat_name, filename, full_path)
    else:
        cat_name = parts[0]
        prod_name = parts[-1].replace('.jpg', '')
        generate_product(cat_name, prod_name, full_path)
    
    count += 1

print(f'\nDone! Generated {count} missing images.')
