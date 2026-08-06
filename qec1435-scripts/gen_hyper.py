#!/usr/bin/env python3
"""Emit all 4095 hyperplanes (index-2 subgroups) of a 12-generator [[14,2]]
stabilizer as 11-generator candidates, hex words, for check1435 batch 11."""
import sys

def parse(path):
    gens = []
    for line in open(path):
        if '|' not in line:
            continue
        bits = [c for c in line if c in '01']
        assert len(bits) == 28, line
        v = 0
        for i, c in enumerate(bits):
            if c == '1':
                v |= 1 << i
        gens.append(v)
    return gens

T = parse(sys.argv[1])
assert len(T) == 12
for phi in range(1, 4096):
    j0 = (phi & -phi).bit_length() - 1
    rows = []
    for i in range(12):
        if i == j0:
            continue
        g = T[i]
        if phi >> i & 1:
            g ^= T[j0]
        rows.append(g)
    print(' '.join(f'{g:07x}' for g in rows))
