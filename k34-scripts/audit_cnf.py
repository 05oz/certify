#!/usr/bin/env python3
"""Independent syntactic audit of a structured cube CNF (or pure instance).

Rebuilds from scratch (fresh logic, no imports from the generators) the exact
clause SET that a correct (3,4,N) instance must contain:
  - one no-2-cycle clause per pair,
  - one I_3 clause per triple,
  - 24 TT_4 clauses per 4-subset,
  - unit clauses fixing vertex 0's neighbourhoods and the three block interiors
    per the given block JSON files (or no units for a pure instance),
and compares against the file's clause set. Any extra, missing, or malformed
clause fails the audit. Also re-checks that each block JSON is really
{I_3,L_3}-free (p,q blocks) / a TT_4-free tournament (s block).

Usage:
  audit_cnf.py pure N file.cnf
  audit_cnf.py cube N p q s pfile qfile sfile file.cnf
"""
import json, sys
from itertools import combinations, permutations


def vnum(u, v, N):
    # pair (min,max) lexicographic index; u->v is 2i+1 if u<v else 2i+2
    a, b = (u, v) if u < v else (v, u)
    i = 0
    # closed form for lexicographic pair index
    i = a * (2 * N - a - 1) // 2 + (b - a - 1)
    return 2 * i + 1 if u < v else 2 * i + 2


def expected_base(N, a=3, b=4):
    S = set()
    for u, v in combinations(range(N), 2):
        S.add(frozenset([-vnum(u, v, N), -vnum(v, u, N)]))
    for T in combinations(range(N), a):
        cl = []
        for u, v in combinations(T, 2):
            cl += [vnum(u, v, N), vnum(v, u, N)]
        S.add(frozenset(cl))
    for Q in combinations(range(N), b):
        for order in permutations(Q):
            S.add(frozenset(-vnum(order[i], order[j], N)
                            for i in range(b) for j in range(i + 1, b)))
    return S


def block_ok_i3l3(blk):
    n = blk["N"]
    arcs = {(u, v) for u, v in blk["arcs"]}
    for u, v in arcs:
        assert (v, u) not in arcs and u != v and 0 <= u < n and 0 <= v < n
    adj = arcs | {(v, u) for u, v in arcs}
    for T in combinations(range(n), 3):
        if all((x, y) not in adj for x, y in combinations(T, 2)):
            return False  # I_3
    for a in range(n):
        for b in range(n):
            for c in range(n):
                if len({a, b, c}) == 3 and (a, b) in arcs and (b, c) in arcs \
                        and (a, c) in arcs:
                    return False  # TT_3
    return True


def block_ok_tt4f(blk):
    n = blk["N"]
    arcs = {(u, v) for u, v in blk["arcs"]}
    for u, v in combinations(range(n), 2):
        if ((u, v) in arcs) == ((v, u) in arcs):
            return False  # not a tournament
    for Q in combinations(range(n), 4):
        sc = sorted(sum(1 for y in Q if (x, y) in arcs) for x in Q)
        if sc == [0, 1, 2, 3]:
            return False
    return True


def expected_units(N, p, q, s, pf, qf, sf):
    U = set()

    def arc(u, v):
        U.add(frozenset([vnum(u, v, N)]))
        U.add(frozenset([-vnum(v, u, N)]))

    def non(u, v):
        U.add(frozenset([-vnum(u, v, N)]))
        U.add(frozenset([-vnum(v, u, N)]))

    for x in range(1, p + 1):
        arc(0, x)
    for x in range(p + 1, p + q + 1):
        arc(x, 0)
    for x in range(p + q + 1, N):
        non(0, x)

    for path, base, k, tt in ((pf, 1, p, False), (qf, p + 1, q, False),
                              (sf, p + q + 1, s, True)):
        if path == "-":
            continue
        blk = json.load(open(path))
        assert blk["N"] == k
        assert (block_ok_tt4f(blk) if tt else block_ok_i3l3(blk)), \
            "block %s fails property check" % path
        arcs = {(u, v) for u, v in blk["arcs"]}
        for x, y in combinations(range(k), 2):
            if (x, y) in arcs:
                arc(base + x, base + y)
            elif (y, x) in arcs:
                arc(base + y, base + x)
            else:
                non(base + x, base + y)
    return U


def main():
    mode = sys.argv[1]
    if mode == "pure":
        # audit_cnf.py pure a b N file.cnf  [--sb01]
        a, b, N = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        cnf = sys.argv[5]
        exp = expected_base(N, a, b)
        if "--sb01" in sys.argv:
            exp.add(frozenset([vnum(0, 1, N)]))
        got = set()
        nv = None
        for line in open(cnf):
            t = line.split()
            if not t or t[0] == "c":
                continue
            if t[0] == "p":
                nv = int(t[2])
                continue
            lits = [int(x) for x in t]
            assert lits[-1] == 0
            got.add(frozenset(lits[:-1]))
        if nv != N * (N - 1):
            print("AUDIT FAIL: var count %s != %d" % (nv, N * (N - 1)))
            return 1
        missing = exp - got
        extra = got - exp
        if missing or extra:
            print("AUDIT FAIL: %d missing, %d extra (of %d expected)"
                  % (len(missing), len(extra), len(exp)))
            return 1
        print("AUDIT PASS: %s matches expected pure (%d,%d,N=%d) clause set (%d clauses)"
              % (cnf, a, b, N, len(exp)))
        return 0
    N = int(sys.argv[2])
    if False:
        pass
    else:
        p, q, s = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
        pf, qf, sf, cnf = sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9]
        assert 1 + p + q + s == N
        exp = expected_base(N) | expected_units(N, p, q, s, pf, qf, sf)

    got = set()
    nv = nc = None
    for line in open(cnf):
        t = line.split()
        if not t or t[0] == "c":
            continue
        if t[0] == "p":
            nv, nc = int(t[2]), int(t[3])
            continue
        lits = [int(x) for x in t]
        assert lits[-1] == 0
        got.add(frozenset(lits[:-1]))
    maxvar = N * (N - 1)
    if nv != maxvar:
        print("AUDIT FAIL: var count %s != %d" % (nv, maxvar)); return 1
    missing = exp - got
    extra = got - exp
    if missing or extra:
        print("AUDIT FAIL: %d missing, %d extra clauses (of %d expected)"
              % (len(missing), len(extra), len(exp)))
        return 1
    print("AUDIT PASS: %s matches expected clause set exactly (%d distinct clauses)"
          % (cnf, len(exp)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
