#!/usr/bin/env python3
"""Create the image generation plan for FetchPicks site."""

import json

plan = {}
plan['hero-dog-food'] = ('dog-food', 'A happy yellow Labrador Retriever (Rocky) wagging tail in front of colorful dog food bags, kibble spilling from a bowl, bright kitchen setting, photorealistic, professional pet photography, high detail')
plan['product-orijen'] = ('dog-food', 'Close-up of Orijen Original premium dog food kibble in a stainless steel bowl, next to a yellow Labrador Retriever waiting patiently, bright natural lighting, product photography style')
plan['product-taste-wild'] = ('dog-food', 'Taste of the Wild High Prairie dog food kibble piled on rustic wooden surface, bison and venison ingredients visible, bag in background, warm earthy tones, product photography')
plan['product-blue-buffalo'] = ('dog-food', 'Blue Buffalo Life Protection dog food kibble with LifeSource Bits visible, measuring scoop next to bowl, bright white background, clean product shot')
plan['product-purina-pro'] = ('dog-food', 'Purina Pro Plan dog food kibble falling from a scoop into a bowl, motion capture style, bright natural lighting, yellow Lab in background, product photography')
plan['product-wellness-core'] = ('dog-food', 'Wellness CORE Grain-Free dog food kibble spread on dark slate surface, high protein ingredients highlighted, modern pet food photography, studio quality')
plan['product-hills-science'] = ('dog-food', "Hill's Science Diet wet dog food opened can next to a bowl of smooth pate, fresh ingredients visible, bright clean background, clinical product photography")
plan['product-royal-canin-wet'] = ('dog-food', 'Royal Canin canned dog food on clean surface, breed-specific labeling visible, bowl of food nearby, clinical white background, product photography')
plan['product-blue-buffalo-wet'] = ('dog-food', 'Blue Buffalo Homestyle Recipe wet dog food with visible meat chunks in gravy, open can next to bowl, hearty meal presentation, product photography')
plan['product-purina-pro-wet'] = ('dog-food', 'Purina Pro Plan shredded wet dog food in bowl, kibble mixed in as topper, close-up of texture, bright lighting, practical feeding scene')
plan['product-purina-one'] = ('dog-food', 'Purina ONE SmartBlend dog food kibble in a measuring cup, simple clean composition, bright natural lighting, affordable dog food presentation')
plan['product-iams'] = ('dog-food', 'IAMS Proactive Health dog food kibble next to a large breed dog bowl, large kibble visible, practical feeding setup, bright lighting')
plan['product-diamond-naturals'] = ('dog-food', 'Diamond Naturals dog food kibble with real meat visible as first ingredients, modern bag in background, green and black color scheme, natural lighting')
plan['product-pedigree'] = ('dog-food', 'Pedigree Adult dog food kibble in a simple bowl, budget-friendly presentation, basic clean setup, bright lighting, honest product photography')
plan['product-rachael-ray'] = ('dog-food', 'Rachael Ray Nutrish natural dog food kibble, clean ingredient list visible on bag nearby, soft natural lighting, rustic kitchen style')
plan['product-blue-buffalo-puppy'] = ('dog-food', 'Blue Buffalo Life Protection Puppy dog food kibble, small kibble size visible, puppy-themed bowl, bright playful lighting, cute puppy food presentation')
plan['product-purina-pro-puppy'] = ('dog-food', 'Purina Pro Plan Puppy dog food kibble for large breeds, larger kibble pieces, measuring scoop, bright clinical lighting, product photography')
plan['product-hills-puppy'] = ('dog-food', "Hill's Science Diet Puppy dog food kibble in a puppy-sized bowl, DHA enrichment callout, clean veterinary style, bright white background")
plan['product-royal-canin-puppy'] = ('dog-food', 'Royal Canin Small Puppy dog food kibble, tiny kibble pieces visible next to a coin for scale, clean white background, product photography')
plan['hero-dog-health'] = ('dog-health', 'A glowing healthy yellow Labrador Retriever (Rocky, aged 8, gray muzzle) sitting on vet exam table, joint supplement bottle visible, warm clinical lighting')
plan['product-cosequin'] = ('dog-health', 'Cosequin joint supplement tablets next to a peanut butter treat, bottle on clean surface, bright white background, veterinary product photography')
plan['product-dasuquin'] = ('dog-health', 'Nutramax Dasuquin supplement capsules, premium presentation, bottle with avocado soybean label visible, clean clinical setting')
plan['product-zesty-paws-joint'] = ('dog-health', 'Zesty Paws Mobility Bites soft chews in owner hand, treat-like appearance, bright natural lighting, warm friendly composition')
plan['product-zesty-paws-multi'] = ('dog-health', 'Zesty Paws 8-in-1 Bites multivitamin soft chews in bright packaging, colorful health benefit icons, pet store shelf style')
plan['product-pethonesty'] = ('dog-health', 'PetHonesty 10-in-1 Daily Supplement bag and soft chews, natural ingredient icons, bright natural lighting, grass background')
plan['product-vets-best'] = ('dog-health', "Vet's Best Multivitamin chewable tablets and bottle, simple no-frills packaging, clean white background, product photography")
plan['product-greenies'] = ('dog-health', 'Greenies dental dog treat in brushing teeth shape, fresh mint green color, smiling yellow Lab Rocky in background, dental care photography')
plan['product-oravet'] = ('dog-health', 'OraVet Dental Hygiene Chew and tube packaging, clinical dental sealant visual, clean sterile background, product photography')
plan['product-virbac-cet'] = ('dog-health', 'Virbac CET Enzymatic Dental Chew with enzyme coating, rawhide-like texture close up, clean bright background, dental health product photography')
plan['hero-dog-gear'] = ('dog-gear', 'A medium mixed-breed dog (Luna, tan coat, floppy ears, deep chest) wearing a blue dog harness on a mountain hiking trail, sunlight filtering through trees, action shot, professional pet photography')
plan['product-ruffwear'] = ('dog-gear', 'Ruffwear Front Range dog harness in blue, detailed view of clips and adjusters, neutral background, showing two leash attachment points, product photography')
plan['product-kong-harness'] = ('dog-gear', 'Kong Comfort dog harness in red, step-in design visible, padded chest plate detail, neutral background, affordable gear product photography')
plan['product-rabbitgoo'] = ('dog-gear', 'Rabbitgoo No-Pull dog harness in black, front clip martingale loop mechanism visible, detailed product shot against light gray background')
plan['product-ruffwear-flagline'] = ('dog-gear', 'Ruffwear Flagline adventure harness streamlined design, reflective trim visible, outdoor gear aesthetic against mountain backdrop, product photography')
plan['product-big-barker'] = ('dog-gear', 'Big Barker orthopedic dog bed with thick 7-inch foam visible, tan cover, large size, pet furniture photography, luxury comfort style')
plan['product-petfusion'] = ('dog-gear', 'PetFusion Ultimate memory foam dog bed, bolster edges, gray quilted cover, 4-inch foam base highlighted, comfortable pet furniture photography')
plan['product-furhaven'] = ('dog-gear', 'FurHaven orthopedic dog bed with egg-crate foam, nesting design with raised edges, cozy home setting, pet bed photography')
plan['hero-dog-treats'] = ('dog-treats', 'A yellow Labrador Retriever (Rocky) looking eagerly at an assortment of dog treats on floor, tail wagging, joyful expression, bright kitchen lighting')
plan['product-nature-gnaws'] = ('dog-treats', 'Nature Gnaws bully sticks arranged neatly on kraft paper, natural grass-fed beef pizzle, rustic pet treat photography, warm earthy tones')
plan['product-jack-pup'] = ('dog-treats', 'Jack and Pup Premium bully sticks thick cut, neutral background with small bag, premium treat photography')
plan['product-redbarn'] = ('dog-treats', 'Redbarn 6-inch bully sticks thick and uniform, USA-sourced label visible, rustic wooden background, premium product photography')
plan['product-zukes-mini'] = ('dog-treats', "Zuke's Mini Naturals training treats pea-sized in owner palm, small size visible, bright white background, training product photography")
plan['product-blue-bits'] = ('dog-treats', 'Blue Buffalo Blue Bits salmon training treats, soft texture, blue packaging, close-up showing treat texture, pet treat product photography')
plan['product-cloud-star'] = ('dog-treats', 'Cloud Star Tricky Trainers soft training treats, peanut butter texture visible, oatmeal-based ingredients, clean bright product photography')
plan['product-wellness-wellbites'] = ('dog-treats', 'Wellness Soft WellBites lamb and salmon recipe, quarter-sized soft chew, meaty texture close-up, premium training treat product photography')
plan['hero-dog-toys'] = ('dog-toys', 'A yellow Labrador Retriever (Rocky) surrounded by durable dog toys including Kong, Nylabone, Chuckit ball, all intact, playful bright setting')
plan['product-kong-classic'] = ('dog-toys', 'Kong Classic red rubber dog toy, natural rubber texture, hollow center, iconic hourglass shape, simple clean white background, product photography')
plan['product-goughnuts'] = ('dog-toys', 'Goughnuts Maxx 50 stick dog toy, black rubber wear indicator layer, heavy-duty chew toy, outdoor backdrop, extreme durability product shot')
plan['product-nylabone'] = ('dog-toys', 'Nylabone Dura Chew textured ring dog toy in bacon flavor, nylon material, ring shape, bright red color, clean white background')
plan['product-chuckit'] = ('dog-toys', 'Chuckit Ultra Ball orange rubber fetch ball, textured surface, floating in water with splashes, action sports toy photography')
plan['product-west-paw'] = ('dog-toys', 'West Paw Zogoflex Tux dog toy in bright green, recycled material texture, eco-friendly branding, minimal product photography against natural background')
plan['hero-dog-training'] = ('dog-training', 'A cute 10-week-old Golden Retriever puppy (Milo) sitting attentively, tiny training treat between paws, soft warm studio lighting, professional puppy photography')
plan['product-zukes-puppy'] = ('dog-training', "Zuke's Mini Naturals puppy training treats with DHA label, tiny pea-sized treats in puppy bowl, bright playful setting, puppy product photography")
plan['product-blue-baby'] = ('dog-training', 'Blue Buffalo Baby Blue Healthy Growth puppy treats, limited ingredient formula, soft texture close-up, soft pastel background, puppy product shot')
plan['product-wellness-puppy'] = ('dog-training', 'Wellness Soft Puppy Bites in lamb and salmon recipe, soft texture for teething puppies, warm puppy-themed photography')
plan['hero-guides'] = ('guides', 'A Golden Retriever puppy next to neatly arranged puppy essentials: wire crate, dog bed, food bowls, toys, leash, collar, organized clean photography')
plan['product-midwest-icrate'] = ('guides', 'MidWest iCrate dog crate with divider panel visible, fold-flat design, metal wire construction, clean home setting, pet product photography')
plan['product-nylabone-puppy'] = ('guides', 'Nylabone Puppy Teething Set with multiple textures, bacon flavor colored bones, arranged on soft puppy bed, soothing teething relief product photography')

with open('D:/fetchpicks-site/image_gen_plan.json', 'w') as f:
    json.dump(plan, f, indent=2)

# Group by directory
by_cat = {}
for name, (cat, prompt) in plan.items():
    by_cat.setdefault(cat, []).append(name)

total = len(plan)
print(f"Total images to generate: {total}")
print()
for cat in sorted(by_cat.keys()):
    imgs = by_cat[cat]
    print(f"{cat}/: {len(imgs)} images")
    for img in sorted(imgs, key=lambda x: ('hero' not in x, x)):
        print(f"  {img}.jpg")
    print()
