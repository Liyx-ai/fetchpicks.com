#!/usr/bin/env python3
"""Generate visible product placeholder images with high contrast."""
import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT = r'D:\fetchpicks-site\public\images\posts'

PRODUCTS = {
    'dog-food': ['product-purina-one', 'product-iams', 'product-diamond-naturals', 'product-pedigree', 'product-rachael-ray', 'product-blue-buffalo-puppy', 'product-purina-pro-puppy', 'product-hills-puppy', 'product-royal-canin-puppy'],
    'dog-health': ['product-cosequin', 'product-dasuquin', 'product-zesty-paws-joint', 'product-zesty-paws-multi', 'product-pethonesty', 'product-vets-best', 'product-greenies', 'product-oravet', 'product-virbac-cet'],
    'dog-gear': ['product-ruffwear', 'product-kong-harness', 'product-rabbitgoo', 'product-ruffwear-flagline', 'product-big-barker', 'product-petfusion', 'product-furhaven'],
    'dog-treats': ['product-nature-gnaws', 'product-jack-pup', 'product-redbarn', 'product-zukes-mini', 'product-blue-bits', 'product-cloud-star', 'product-wellness-wellbites'],
    'dog-toys': ['product-kong-classic', 'product-goughnuts', 'product-nylabone', 'product-chuckit', 'product-west-paw'],
    'dog-training': ['product-zukes-puppy', 'product-blue-baby', 'product-wellness-puppy'],
    'guides': ['product-midwest-icrate', 'product-nylabone-puppy'],
}

# Each category: (bg_color, card_color, accent_color, text_color)
STYLES = {
    'dog-food':    ((255,236,235), (192,57,43), (231,76,60), (255,255,255)),
    'dog-health':  ((235,245,235), (39,174,96), (46,204,113), (255,255,255)),
    'dog-gear':    ((235,242,250), (41,128,185), (52,152,219), (255,255,255)),
    'dog-treats':  ((245,235,250), (142,68,173), (155,89,182), (255,255,255)),
    'dog-toys':    ((255,240,235), (211,84,0), (230,126,34), (255,255,255)),
    'dog-training':((235,250,245), (22,160,133), (26,188,156), (255,255,255)),
    'guides':      ((240,242,245), (44,62,80), (52,73,94), (255,255,255)),
}

def generate():
    try:
        font_title = ImageFont.truetype('arial.ttf', 28)
        font_sub = ImageFont.truetype('arial.ttf', 20)
        font_badge = ImageFont.truetype('arial.ttf', 14)
    except:
        font_title = ImageFont.load_default()
        font_sub = font_title
        font_badge = font_title
    
    for cat, products in PRODUCTS.items():
        bg_rgb, card_rgb, accent_rgb, text_rgb = STYLES[cat]
        cat_dir = os.path.join(OUTPUT, cat)
        
        for i, pname in enumerate(products):
            fpath = os.path.join(cat_dir, f'{pname}.jpg')
            
            img = Image.new('RGB', (800, 800), bg_rgb)
            draw = ImageDraw.Draw(img)
            
            # Main product card - dark/colorful rectangle
            draw.rounded_rectangle([(120, 160), (680, 640)], radius=35, fill=card_rgb, outline=accent_rgb, width=4)
            
            # Inner lighter panel
            inner_color = (min(card_rgb[0]+80,255), min(card_rgb[1]+80,255), min(card_rgb[2]+80,255))
            draw.rounded_rectangle([(200, 240), (600, 560)], radius=20, fill=inner_color, outline=None)
            
            # Product icon placeholder (box with circle at center)
            draw.rounded_rectangle([(320, 270), (480, 410)], radius=60, fill=card_rgb, outline=accent_rgb, width=3)
            # Circle inside
            cx, cy = 400, 340
            draw.ellipse([(cx-25, cy-25), (cx+25, cy+25)], fill=accent_rgb, outline=text_rgb, width=2)
            
            # Category badge at top
            cat_label = cat.replace('dog-', '').replace('-', ' & ').title()
            bbox = draw.textbbox((0, 0), cat_label, font=font_badge)
            tw = bbox[2] - bbox[0]
            badge_x = 400 - tw//2 - 15
            draw.rounded_rectangle([(badge_x, 118), (badge_x+tw+30, 148)], radius=15, fill=accent_rgb)
            draw.text((400, 133), cat_label, fill=text_rgb, font=font_badge, anchor='mm')
            
            # Product name
            display_name = pname.replace('product-', '').replace('-', ' ').title()
            draw.text((400, 510), display_name, fill=card_rgb, font=font_title, anchor='mm')
            
            # Rating stars
            stars = '* * * * *'
            draw.text((400, 555), stars, fill=(243, 156, 18), font=font_sub, anchor='mm')
            
            # Price / CTA button
            btn_color = accent_rgb
            draw.rounded_rectangle([(310, 590), (490, 625)], radius=18, fill=btn_color)
            draw.text((400, 607), 'View on Amazon', fill=text_rgb, font=font_sub, anchor='mm')
            
            # Bottom tag line
            draw.text((400, 660), 'Best for: Check article for details', fill=(140,140,140), font=font_badge, anchor='mm')
            
            img.save(fpath, 'JPEG', quality=88, optimize=True)
            print(f'{pname}.jpg generated')
    
    # Verify images aren't blank
    print('\n=== Verifying ===')
    for cat, products in PRODUCTS.items():
        for pname in products[:1]:  # Check first of each category
            fpath = os.path.join(OUTPUT, cat, f'{pname}.jpg')
            img = Image.open(fpath)
            px = list(img.getdata())
            colors = len(set(px[:200]))
            sz = os.path.getsize(fpath) // 1024
            status = 'OK' if colors > 5 else 'BLANK!'
            print(f'  {cat}/{pname}: {sz}KB, {colors} colors in 200px => {status}')

if __name__ == '__main__':
    generate()
