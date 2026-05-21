#!/usr/bin/env python3
"""Auto-rename generated images to their correct filenames based on prompt keywords."""
import os, re

MAPPINGS = {
    'Taste_of_the_Wild': 'product-taste-wild',
    'Blue_Buffalo_Life_Protection_kibble': 'product-blue-buffalo',
    'Purina_Pro_Plan_dog_food_kibble_falling': 'product-purina-pro',
    'Wellness_CORE_Grain': 'product-wellness-core',
    'Science_Diet_wet': 'product-hills-science',
    'Royal_Canin_canned': 'product-royal-canin-wet',
    'Blue_Buffalo_Homestyle': 'product-blue-buffalo-wet',
    'Purina_Pro_Plan_shredded': 'product-purina-pro-wet',
    'Purina_ONE_SmartBlend': 'product-purina-one',
    'IAMS_Proactive': 'product-iams',
    'Diamond_Naturals': 'product-diamond-naturals',
    'Pedigree_Adult': 'product-pedigree',
    'Rachael_Ray_Nutrish': 'product-rachael-ray',
    'Blue_Buffalo_Life_Protection_Puppy': 'product-blue-buffalo-puppy',
    'Purina_Pro_Plan_Puppy': 'product-purina-pro-puppy',
    'Science_Diet_Puppy': 'product-hills-puppy',
    'Royal_Canin_Small_Puppy': 'product-royal-canin-puppy',
    'Colorado_Labrador_Retriever_Rocky_aged': 'hero-dog-health',
    'Cosequin_joint': 'product-cosequin',
    'Nutramax_Dasuquin': 'product-dasuquin',
    'Zesty_Paws_Mobility_Bites': 'product-zesty-paws-joint',
    'Zesty_Paws_8': 'product-zesty-paws-multi',
    'PetHonesty_10': 'product-pethonesty',
    'Vet_Best_Multivitamin': 'product-vets-best',
    'Greenies_dental': 'product-greenies',
    'OraVet_Dental': 'product-oravet',
    'Virbac_CET': 'product-virbac-cet',
    'medium_mixed': 'hero-dog-gear',
    'Ruffwear_Front_Range': 'product-ruffwear',
    'Kong_Comfort': 'product-kong-harness',
    'Rabbitgoo_No': 'product-rabbitgoo',
    'Ruffwear_Flagline': 'product-ruffwear-flagline',
    'Big_Barker_orthopedic': 'product-big-barker',
    'PetFusion_Ultimate': 'product-petfusion',
    'FurHaven_orthopedic': 'product-furhaven',
    'Labrador_Retriever_Rocky_looking_eagerly': 'hero-dog-treats',
    'Nature_Gnaws': 'product-nature-gnaws',
    'Jack_Pup': 'product-jack-pup',
    'Redbarn_6': 'product-redbarn',
    'Zuke_Mini_Naturals_training': 'product-zukes-mini',
    'Blue_Buffalo_Blue_Bits': 'product-blue-bits',
    'Cloud_Star_Tricky': 'product-cloud-star',
    'Wellness_Soft_WellBites': 'product-wellness-wellbites',
    'Labrador_Retriever_Rocky_surrounded': 'hero-dog-toys',
    'Kong_Classic_red': 'product-kong-classic',
    'Goughnuts_Maxx': 'product-goughnuts',
    'Nylabone_Dura_Chew_textured': 'product-nylabone',
    'Chuckit_Ultra': 'product-chuckit',
    'West_Paw_Zogoflex': 'product-west-paw',
    'week_old_Golden': 'hero-dog-training',
    'Zuke_Mini_Naturals_puppy': 'product-zukes-puppy',
    'Blue_Buffalo_Baby_Blue': 'product-blue-baby',
    'Wellness_Soft_Puppy_Bites': 'product-wellness-puppy',
    'Golden_Retriever_puppy_next': 'hero-guides',
    'MidWest_iCrate': 'product-midwest-icrate',
    'Nylabone_Puppy_Teething': 'product-nylabone-puppy',
}

def auto_rename():
    image_dirs = [
        r'D:\fetchpicks-site\public\images\posts\dog-food',
        r'D:\fetchpicks-site\public\images\posts\dog-health',
        r'D:\fetchpicks-site\public\images\posts\dog-gear',
        r'D:\fetchpicks-site\public\images\posts\dog-treats',
        r'D:\fetchpicks-site\public\images\posts\dog-toys',
        r'D:\fetchpicks-site\public\images\posts\dog-training',
        r'D:\fetchpicks-site\public\images\posts\guides',
    ]
    
    renamed = 0
    for d in image_dirs:
        if not os.path.exists(d):
            continue
        for f in os.listdir(d):
            if not f.endswith('.png') or f.startswith('.'):
                continue
            # Try to match
            for prompt_keyword, target in MAPPINGS.items():
                if prompt_keyword.replace('_', ' ') in f.replace('_', ' ') or prompt_keyword in f:
                    old_path = os.path.join(d, f)
                    new_path = os.path.join(d, f'{target}.jpg')
                    os.rename(old_path, new_path)
                    print(f'  {f} → {target}.jpg')
                    renamed += 1
                    break
    
    print(f'\nTotal renamed: {renamed}')
    
    # Show leftovers
    for d in image_dirs:
        if not os.path.exists(d):
            continue
        leftovers = [f for f in os.listdir(d) if f.endswith('.png') and not f.startswith('.')]
        if leftovers:
            print(f'\nUnmatched in {os.path.basename(d)}:')
            for f in leftovers:
                print(f'  {f}')

if __name__ == '__main__':
    auto_rename()
