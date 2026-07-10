#!/usr/bin/env python3
"""Post-build fix: replace individual /images/ entries in _routes.json with /images/* wildcard.

Cloudflare _routes.json has a 100-entry limit. The Astro Cloudflare adapter lists
individual static assets, which overflows when there are many images. This script
replaces all /images/* entries with a single wildcard.
"""
import json
from pathlib import Path

routes_file = Path("dist/_routes.json")
if not routes_file.exists():
    print("fix-routes: dist/_routes.json not found, skipping")
    exit(0)

with open(routes_file) as f:
    data = json.load(f)

old_count = len(data["exclude"])
new_exclude = [e for e in data["exclude"] if not e.startswith("/images/")]
if len(new_exclude) < old_count:
    new_exclude.append("/images/*")
    data["exclude"] = new_exclude
    with open(routes_file, "w") as f:
        json.dump(data, f, indent=2)
    print(f"fix-routes: {old_count} -> {len(new_exclude)} entries (added /images/* wildcard)")
else:
    print(f"fix-routes: no image entries to replace ({old_count} entries)")
