#!/usr/bin/env python3
"""Regenerate product placeholder images with better visuals."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT = r'D:\fetchpicks-site\public\images\posts'

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

# Category-specific background colors (warm, pet-friendly palette)
CAT_COLORS = {
    'dog-food':    (('#c0392b', '#e74c3c'), '#fff5f0'),
    'dog-health':  (('#27ae60', '#2ecc71'), '#f0fff5'),
    'dog-gear':    (('#2980b9', '#3498db'), '#f0f7ff'),
    'dog-treats':  (('#8e44ad', '#9b59b6'), '#faf0ff'),
    'dog-toys':    (('#d35400', '#e67e22'), '#fff5f0'),
    'dog-training':(('#16a085', '#1abc9c'), '#f0fffa'),
    'guides':      (('#2c3e50', '#34495e'), '#f0f2f5'),
}

def generate():
    total = 0
    for cat, products in PRODUCT_IMAGES.items():
        cat_dir = os.path.join(OUTPUT, cat)
        bg_colors, bg_light = CAT_COLORS.get(cat, (('#7f8c8d', '#95a5a6'), '#f5f5f5'))
        
        for i, pname in enumerate(products):
            fpath = os.path.join(cat_dir, f'{pname}.jpg')
            # Always regenerate with better design
            
            img = Image.new('RGB', (800, 800), bg_light)
            draw = ImageDraw.Draw(img)
            
            # Draw product "card" shape
            c1, c2 = bg_colors
            draw.rounded_rectangle([(100, 150), (700, 650)], radius=40, 
                                   fill=c1, outline=c2, width=2)
            
            # Inner lighter area (where "product" would be)
            draw.rounded_rectangle([(180, 230), (620, 570)], radius=25,
                                   fill=bg_light, outline=None)
            
            # Draw some visual elements to make it look like packaging
            # Horizontal "band" on the product
            bx1, bx2 = 230, 570
            draw.rectangle([(bx1, 340), (bx2, 370)], fill=c1)
            draw.rectangle([(bx1, 380), (bx2, 395)], fill=c2)
            
            # Text label
            try:
                font = ImageFont.truetype('arial.ttf', 22)
                font_sub = ImageFont.truetype('arial.ttf', 18)
            except:
                font = ImageFont.load_default()
                font_sub = font
            
            display_name = pname.replace('product-', '').replace('-', ' ').title()
            
            # Category badge at top
            draw.rounded_rectangle([(300, 120), (500, 146)], radius=13, fill=c1)
            cat_label = cat.upper().replace('-', ' · ')
            bbox = draw.textbbox((0, 0), cat_label, font=font_sub)
            tw = bbox[2] - bbox[0]
            draw.text(((800 - tw) // 2, 123), cat_label, fill='white', font=font_sub)
            
            # Product name centered
            bbox = draw.textbbox((0, 0), display_name, font=font)
            tw = bbox[2] - bbox[0]
            draw.text(((800 - tw) // 2, 420), display_name, fill=c1, font=font)
            
            # Stars rating
            stars = '★★★★★'
            bbox = draw.textbbox((0, 0), stars, font=font_sub)
            tw = bbox[2] - bbox[0]
            draw.text(((800 - tw) // 2, 460), stars, fill=(241,196,15), font=font_sub)
            
            # Price tag
            price = f'Check Price →'
            draw.rounded_rectangle([(320, 560), (480, 600)], radius=25, fill=c2)
            bbox = draw.textbbox((0, 0), price, font=font_sub)
            tw = bbox[2] - bbox[0]
            draw.text(((800 - tw) // 2, 567), price, fill='white', font=font_sub)
            
            img.save(fpath, 'JPEG', quality=82, optimize=True)
            total += 1
    
    print(f'Generated/updated {total} product placeholder images')

if __name__ == '__main__':
    generate()
