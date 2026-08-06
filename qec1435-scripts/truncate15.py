#!/usr/bin/env python3
"""Truncations of the codetables [[15,3,5]] to length 14.

For each position i and each single-qubit condition C in
{ g_i = I }, { g_i in {I,X} }, { g_i in {I,Z} }, { g_i in {I,Y} }:
take the subgroup of the [[15,3,5]] stabilizer whose elements satisfy C at i,
delete coordinate i, and record the resulting isotropic subspace of F2^28.
dim 11 -> [[14,3]] candidate, dim 12 -> [[14,2]] candidate (walk2 seed).

Output: for each case, prints dim and the exact distance via check1435 check.
"""
import subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))

def parse(path, n):
    gens = []
    for line in open(path):
        if '|' not in line:
            continue
        bits = [c for c in line if c in '01']
        assert len(bits) == 2 * n, (len(bits), line)
        a = 0
        b = 0
        for i in range(n):
            if bits[i] == '1':
                a |= 1 << i
            if bits[n + i] == '1':
                b |= 1 << i
        gens.append((a, b))
    return gens

G15 = parse(os.path.join(HERE, 'data/ct_15_3_stab.txt'), 15)
assert len(G15) == 12

def span(gens):
    out = [0]
    for g in gens:
        out += [x ^ g for x in out]
    return out

def basis_of(vecs):
    basis = []
    for x in vecs:
        for h in basis:
            hb = 1 << (h.bit_length() - 1)
            if x & hb:
                x ^= h
        if x:
            basis.append(x)
            basis.sort(reverse=True)
    return basis

# pack (a,b) length-15 pairs into 30-bit ints: a bits 0..14, b bits 15..29
full = span([a | (b << 15) for a, b in G15])
assert len(full) == 4096

conds = {'I': lambda a, b: a == 0 and b == 0,
         'IX': lambda a, b: b == 0,
         'IZ': lambda a, b: a == 0,
         'IY': lambda a, b: a == b}

results = []
for i in range(15):
    for cname, cf in conds.items():
        sub = []
        for v in full:
            a, b = v & 0x7FFF, v >> 15
            ai, bi = (a >> i) & 1, (b >> i) & 1
            if cf(ai, bi):
                # delete coordinate i, repack to 28-bit (14 qubits)
                amask_lo = (1 << i) - 1
                a14 = (a & amask_lo) | ((a >> (i + 1)) << i)
                b14 = (b & amask_lo) | ((b >> (i + 1)) << i)
                sub.append(a14 | (b14 << 14))
        bas = basis_of(sub)
        results.append((i, cname, len(bas), bas))

# check distances via check1435
for i, cname, dim, bas in results:
    if dim not in (11, 12):
        print(f"pos {i:2d} cond {cname:2s}: dim {dim} (skip)")
        continue
    hexline = ' '.join(f'{g:07x}' for g in bas)
    p = subprocess.run([os.path.join(HERE, 'check1435'), 'batch', str(dim)],
                       input=hexline + '\n', capture_output=True, text=True)
    out = p.stdout.strip().splitlines()
    hit = [l for l in out if l.startswith('HIT')]
    k = 14 - dim
    print(f"pos {i:2d} cond {cname:2s}: dim {dim} -> [[14,{k}]] "
          f"{'*** ' + hit[0] if hit else 'd<5'}")
    if hit and dim == 12:
        # save as extra walk2 seed
        fn = os.path.join(HERE, f'data/seed_1425_p{i}_{cname}.txt')
        with open(fn, 'w') as f:
            for g in bas:
                rowa = ' '.join(str((g >> j) & 1) for j in range(14))
                rowb = ' '.join(str((g >> (14 + j)) & 1) for j in range(14))
                f.write(f"[{rowa}|{rowb}]\n")
        print(f"      saved seed {fn}")
