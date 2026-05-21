#!/usr/bin/env python3
"""
Batch image generation script for FetchPicks.
Hits ImageGen API one at a time with pacing to avoid job queue limits.
"""
import os, json, time, urllib.request, urllib.parse, urllib.error

# Load plan
with open('D:/fetchpicks-site/image_gen_plan.json') as f:
    plan = json.load(f)

# Track what's already generated
def count_existing():
    existing = 0
    for img_name, (cat, _) in plan.items():
        path = f'D:/fetchpicks-site/public/images/posts/{cat}/{img_name}.jpg'
        if os.path.exists(path):
            existing += 1
    return existing

existing_count = count_existing()
total = len(plan)
print(f'Images: {existing_count}/{total} already generated')

# Show what's missing
for img_name, (cat, _) in plan.items():
    path = f'D:/fetchpicks-site/public/images/posts/{cat}/{img_name}.jpg'
    if not os.path.exists(path):
        print(f'  MISSING: {cat}/{img_name}.jpg')

print(f'\nRemaining to generate: {total - existing_count}')
