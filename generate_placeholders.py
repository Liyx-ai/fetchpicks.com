#!/usr/bin/env python3
"""
Quick image filler: download hero images from Unsplash + generate placeholder product images.
"""
import os, json, requests, io
from PIL import Image, ImageDraw, ImageFont

OUTPUT = r'D:\fetchpicks-site\public\images\posts'

# === 1. Download Hero Images from Unsplash ===
# Using direct unsplash photo URLs for dog breeds matching our characters
HERO_PHOTOS = {
    'dog-training': {
        'url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=1024',  # golden puppy
        'filename': 'hero-dog-training.jpg'
    },
    'guides': {
        'url': 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=1024',  # same golden puppy for puppy guide
        'filename': 'hero-guides.jpg'
    },
}

def download_hero_images():
    for cat, info in HERO_PHOTOS.items():
        filepath = os.path.join(OUTPUT, cat, info['filename'])
        if os.path.exists(filepath):
            print(f'  {info["filename"]} already exists, skipping')
            continue
        try:
            r = requests.get(info['url'], timeout=15)
            if r.status_code == 200:
                img = Image.open(io.BytesIO(r.content))
                # Resize to 1024x1024 center crop
                w, h = img.size
                sz = min(w, h)
                left = (w - sz) // 2
                top = (h - sz) // 2
                img = img.crop((left, top, left+sz, top+sz))
                img = img.resize((1024, 1024))
                img.save(filepath, 'JPEG', quality=85)
                print(f'  Downloaded: {info["filename"]}')
            else:
                print(f'  Failed to download {info["filename"]}: HTTP {r.status_code}')
        except Exception as e:
            print(f'  Error downloading {info["filename"]}: {e}')

# === 2. Generate Placeholder Product Images ===
PRODUCT_IMAGES = {
    'dog-food': [
        'product-purina-one', 'product-iams', 'product-diamond-naturals',
        'product-pedigree', 'product-rachael-ray', 'product-blue-buffalo-puppy',
        'product-purina-pro-puppy', 'product-hills-puppy', 'product-royal-canin-puppy',
    ],
    'dog-health': [
        'product-cosequin', 'product-dasuquin', 'product-zesty-paws-joint',
        'product-zesty-paws-multi', 'product-pethonesty', 'product-vets-best',
        'product-greenies', 'product-oravet', 'product-virbac-cet',
    ],
    'dog-gear': [
        'product-ruffwear', 'product-kong-harness', 'product-rabbitgoo',
        'product-ruffwear-flagline', 'product-big-barker', 'product-petfusion',
        'product-furhaven',
    ],
    'dog-treats': [
        'product-nature-gnaws', 'product-jack-pup', 'product-redbarn',
        'product-zukes-mini', 'product-blue-bits', 'product-cloud-star',
        'product-wellness-wellbites',
    ],
    'dog-toys': [
        'product-kong-classic', 'product-goughnuts', 'product-nylabone',
        'product-chuckit', 'product-west-paw',
    ],
    'dog-training': [
        'product-zukes-puppy', 'product-blue-baby', 'product-wellness-puppy',
    ],
    'guides': [
        'product-midwest-icrate', 'product-nylabone-puppy',
    ],
}

# Color palette for product placeholders
COLORS = [
    ('#4A90D9', '#357ABD'),  # Blue
    ('#50B86C', '#3E9657'),  # Green
    ('#D9754A', '#C05E3A'),  # Orange
    ('#9B59B6', '#8E44AD'),  # Purple
    ('#E74C3C', '#C0392B'),  # Red
    ('#2ECC71', '#27AE60'),  # Emerald
    ('#F39C12', '#E67E22'),  # Amber
    ('#1ABC9C', '#16A085'),  # Teal
    ('#3498DB', '#2980B9'),  # Light Blue
]

def generate_product_placeholders():
    color_idx = 0
    total = 0
    for cat, products in PRODUCT_IMAGES.items():
        cat_dir = os.path.join(OUTPUT, cat)
        os.makedirs(cat_dir, exist_ok=True)
        
        for pname in products:
            filepath = os.path.join(cat_dir, f'{pname}.jpg')
            if os.path.exists(filepath):
                continue
            
            # Create gradient placeholder
            bg_start, bg_end = COLORS[color_idx % len(COLORS)]
            color_idx += 1
            
            img = Image.new('RGB', (1024, 1024), bg_start)
            draw = ImageDraw.Draw(img)
            
            # Draw a simple diagonal gradient effect
            for i in range(1024):
                ratio = i / 1024
                r = int(int(bg_start[1:3], 16) * (1-ratio) + int(bg_end[1:3], 16) * ratio)
                g = int(int(bg_start[3:5], 16) * (1-ratio) + int(bg_end[3:5], 16) * ratio)
                b = int(int(bg_start[5:7], 16) * (1-ratio) + int(bg_end[5:7], 16) * ratio)
                draw.line([(0, i), (1023, i)], fill=(r, g, b))
            
            # Draw a product silhouette icon (simple box)
            box_color = (255, 255, 255, 40)
            draw.rounded_rectangle([(312, 262), (712, 762)], radius=30, fill=(255,255,255,30))
            
            # Add text label
            try:
                font_large = ImageFont.truetype('arial.ttf', 36)
                font_small = ImageFont.truetype('arial.ttf', 24)
            except:
                font_large = ImageFont.load_default()
                font_small = font_large
            
            display_name = pname.replace('product-', '').replace('-', ' ').title()
            
            # Center text
            bbox = draw.textbbox((0, 0), display_name, font=font_large)
            tw = bbox[2] - bbox[0]
            draw.text(((1024 - tw) // 2, 420), display_name, fill=(255,255,255), font=font_large)
            
            draw.text((350, 560), 'Product Image', fill=(220,220,220), font=font_small)
            draw.text((370, 600), 'Coming Soon', fill=(200,200,200), font=font_small)
            
            img.save(filepath, 'JPEG', quality=80)
            total += 1
    
    print(f'Generated {total} placeholder product images')

# === 3. Run ===
print('=== Downloading hero images ===')
download_hero_images()

print('\n=== Generating product placeholders ===')
generate_product_placeholders()

print('\nDone!')
