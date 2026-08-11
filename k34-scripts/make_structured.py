#!/usr/bin/env python3
"""Generic structured-cube CNF generator for {I_3,L_4}-free existence on N vertices.

Fixes vertex 0 with prescribed out/in/nonadjacent blocks:
  vertex 0; N+(0) = 1..p; N-(0) = p+1..p+q; I(0) = p+q+1..N-1.
Block induced structures are read from JSON files ({"N":k, "arcs":[[u,v],..]},
vertices 0..k-1, translated onto the block). Emits the PURE (3,4,N) encoding
plus unit clauses for vertex 0's arcs and all intra-block pairs (pairs with no
arc in the block file are fixed nonadjacent).

Soundness of the cube system (documented in NOTES.md): in any {I_3,L_4}-free D,
every vertex v has N+(v),N-(v) {I_3,L_3}-free and I(v) an {I_2,L_4}-free
tournament; with r(I_3,L_3)=9, r(I_2,L_4)=8 (certified) this bounds p,q<=8,s<=7.
An existence question at N is decided by trying all (p,q,s) with 1+p+q+s=N
(reversal symmetry maps (p,q,s)-cubes to (q,p,s)-cubes, so only p<=q needed ...
we enumerate all class combinations for the chosen (p,q,s)).
SAT model of any cube = witness (independently verified); all cubes UNSAT =>
no witness on N vertices.

Usage: make_structured.py N p q s plusfile minusfile ifile out.cnf
       (ifile = "-" means s=0, no I block; plus/minus files must have p,q vertices)
"""
import json, sys
from itertools import combinations, permutations

A, B = 3, 4


def main():
    N = int(sys.argv[1]); p = int(sys.argv[2]); q = int(sys.argv[3]); s = int(sys.argv[4])
    pf, qf, sf, out = sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8]
    assert 1 + p + q + s == N
    pairs = list(combinations(range(N), 2))
    pidx = {pr: i for i, pr in enumerate(pairs)}

    def var(u, v):
        if u < v:
            return 2 * pidx[(u, v)] + 1
        return 2 * pidx[(v, u)] + 2

    clauses = []
    for (u, v) in pairs:
        clauses.append([-var(u, v), -var(v, u)])
    for S in combinations(range(N), A):
        cl = []
        for (u, v) in combinations(S, 2):
            cl += [var(u, v), var(v, u)]
        clauses.append(cl)
    for S in combinations(range(N), B):
        for order in permutations(S):
            clauses.append([-var(order[i], order[j])
                           for i in range(B) for j in range(i + 1, B)])
    units = []

    def fix_arc(u, v):
        units.append([var(u, v)]); units.append([-var(v, u)])

    def fix_nonadj(u, v):
        units.append([-var(u, v)]); units.append([-var(v, u)])

    for x in range(1, p + 1):
        fix_arc(0, x)
    for x in range(p + 1, p + q + 1):
        fix_arc(x, 0)
    for x in range(p + q + 1, N):
        fix_nonadj(0, x)

    def fix_block(path, base, k):
        blk = json.load(open(path))
        assert blk["N"] == k, (path, blk["N"], k)
        arcs = {(u, v) for u, v in blk["arcs"]}
        for x, y in combinations(range(k), 2):
            if (x, y) in arcs:
                fix_arc(base + x, base + y)
            elif (y, x) in arcs:
                fix_arc(base + y, base + x)
            else:
                fix_nonadj(base + x, base + y)

    fix_block(pf, 1, p)
    fix_block(qf, p + 1, q)
    if sf != "-":
        fix_block(sf, p + q + 1, s)

    allc = clauses + units
    with open(out, "w") as f:
        f.write("p cnf %d %d\n" % (2 * len(pairs), len(allc)))
        for cl in allc:
            f.write(" ".join(map(str, cl)) + " 0\n")
    print("wrote %s: N=%d (p,q,s)=(%d,%d,%d) units=%d free_pairs=%d"
          % (out, N, p, q, s, len(units), len(pairs) - len(units) // 2))


if __name__ == "__main__":
    main()
