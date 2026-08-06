#!/usr/bin/env python3
"""Emit candidate minimizer tournaments in gentourng ascii format (stdout).

Construction from OPG page: vertex set split V1->V2->V3->V1 (cyclic blow-up).
For n=9: parts (3,3,3); for n=10: parts (4,3,3) in each rotation position.
Inside each 3-part: C3 (cyclic) or TT3 (transitive); inside a 4-part: each of the
4 tournaments on 4 vertices. Each candidate printed as C(n,2) chars, char at
pair (i,j), i<j (row-by-row upper triangle) = '1' iff arc i->j.
Label lines go to stderr, aligned 1:1 with stdout lines.
"""
import sys
from itertools import product

C3 = {(0, 1), (1, 2), (2, 0)}
TT3 = {(0, 1), (0, 2), (1, 2)}
T3 = [("C3", C3), ("TT3", TT3)]
# the 4 tournaments on 4 vertices
TT4 = {(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)}
VC3 = {(0, 1), (0, 2), (0, 3), (1, 2), (2, 3), (3, 1)}        # vertex -> C3
C3V = {(1, 2), (2, 3), (3, 1), (1, 0), (2, 0), (3, 0)}        # C3 -> vertex
STR4 = {(0, 1), (1, 2), (2, 3), (0, 2), (1, 3), (3, 0)}       # strong
T4 = [("TT4", TT4), ("VC3", VC3), ("C3V", C3V), ("STR4", STR4)]


def emit(parts, inners, label):
    """parts: list of vertex lists; inners: list of arc-sets on 0..len(part)-1.
    Between parts: part p -> part p+1 (mod 3)."""
    n = sum(len(p) for p in parts)
    arc = set()
    for p, (verts, inner) in enumerate(zip(parts, inners)):
        for (a, b) in inner:
            arc.add((verts[a], verts[b]))
        nxt = parts[(p + 1) % 3]
        for u in verts:
            for v in nxt:
                arc.add((u, v))
    bits = []
    for i in range(n):
        for j in range(i + 1, n):
            assert ((i, j) in arc) != ((j, i) in arc)
            bits.append('1' if (i, j) in arc else '0')
    print(''.join(bits))
    print(label, file=sys.stderr)


n = int(sys.argv[1])
if n == 9:
    parts = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    for (l1, a1), (l2, a2), (l3, a3) in product(T3, T3, T3):
        emit(parts, [a1, a2, a3], f"9:{l1},{l2},{l3}")
elif n == 10:
    for pos in range(3):
        sizes = [3, 3, 3]
        sizes[pos] = 4
        parts, s = [], 0
        for sz in sizes:
            parts.append(list(range(s, s + sz)))
            s += sz
        choices = [T4 if len(p) == 4 else T3 for p in parts]
        for combo in product(*choices):
            labels = ','.join(c[0] for c in combo)
            emit(parts, [c[1] for c in combo], f"10:pos{pos}:{labels}")
