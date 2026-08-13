#!/usr/bin/env python3
"""Re-hash every artifact against qec-certificates/manifest.json.

Run from anywhere:  python3 qec-scripts/verify_manifest.py
Standard library only.

The manifest hashes the UNCOMPRESSED bytes, so the six check_lower proofs that
ship gzipped read as absent until they are decompressed:

    gunzip qec-certificates/*/lower_*.lrat.gz

That glob is restricted to lower_* on purpose. The *_prof_*.lrat.gz files are
not manifest entries -- the manifest predates them -- and their own descriptors
name the compressed file, so decompressing one breaks the certificate it
belongs to. Never gunzip a *_prof_*.lrat.gz.

Expected: 172 match, 0 mismatch, 10 absent on a fresh clone; 178 match, 0
mismatch, 4 absent after the gunzip above, the four being the proofs too large
for git (qec-certificates/REGENERATE.md).
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
