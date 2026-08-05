#!/usr/bin/env python3
"""Re-hash every artifact against qec-certificates/manifest.json.

Run from anywhere:  python3 qec-scripts/verify_manifest.py
Standard library only. Decompress first:  gunzip qec-certificates/*/*.lrat.gz
"""
import hashlib, json, os, sys

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "qec-certificates")
man = json.load(open(os.path.join(ROOT, "manifest.json")))
ok = bad = absent = 0
for code, entry in sorted(man.items()):
    for name, meta in sorted(entry["files"].items()):
        p = os.path.join(ROOT, code, name)
        if not os.path.exists(p):
            absent += 1
            print(f"ABSENT   {code}/{name}  ({meta['bytes']} B) -- see REGENERATE.md")
            continue
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        if h.hexdigest() == meta["sha256"] and os.path.getsize(p) == meta["bytes"]:
            ok += 1
        else:
            bad += 1
            print(f"MISMATCH {code}/{name}")
print(f"\n{ok} match, {bad} mismatch, {absent} absent (of {ok+bad+absent} manifest entries)")
sys.exit(1 if bad else 0)
