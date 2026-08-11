#!/usr/bin/env python3
"""Referee-style MULTISET completeness audit for a whole cube layer.

For layer N it re-derives the required cube inventory (types p<=q with
p+q+s=N-1, p,q<=8, s<=7, all block-class combinations, same enumeration as
verify_chain.py), and for every cube CNF checks CLAUSE-MULTISET equality:

  file multiset == expected base(N) multiset + expected unit multiset

which is strictly stronger than set equality: it additionally requires that
(a) the DIMACS header clause count equals the number of clause lines,
(b) no clause appears twice in the file,
(c) the cube-splitting clauses (the units) exactly complement the base
    formula -- file minus base == units, as multisets, no leftovers.

Expected clauses are rebuilt via audit_cnf.py's independent logic (fresh
encoding rewrite, includes re-checking each block JSON's defining property).

Usage: audit_multiset.py N   (N in {21, 22, 23, 24})
Exit 0 iff every required cube file exists and passes.
"""
import os, sys
from collections import Counter

import audit_cnf
from verify_chain import I3L3, TT4F, cube_name

H = os.path.dirname(os.path.abspath(__file__))


def file_multiset(path):
    ms = Counter()
    header = None
    nlines = 0
    for line in open(path):
        t = line.split()
        if not t or t[0] == "c":
            continue
        if t[0] == "p":
            header = int(t[3])
            continue
        lits = [int(x) for x in t]
        assert lits[-1] == 0, path
        ms[frozenset(lits[:-1])] += 1
        nlines += 1
    return ms, header, nlines


def main():
    N = int(sys.argv[1])
    base = audit_cnf.expected_base(N)
    base_ms = Counter({c: 1 for c in base})
    fails = []
    total = 0
    for p in range(max(0, N - 16), 9):
        for q in range(p, 9):
            s = N - 1 - p - q
            if not (0 <= s <= 7):
                continue
            if p not in I3L3 or q not in I3L3 or s not in TT4F:
                fails.append("missing inventory for type %s" % ((p, q, s),))
                continue
            for i, pf in enumerate(I3L3[p]):
                for j, qf in enumerate(I3L3[q]):
                    for k, sf in enumerate(TT4F[s]):
                        name = cube_name(N, p, q, s, i, j, k)
                        total += 1
                        path = os.path.join(H, name + ".cnf")
                        if not os.path.exists(path):
                            fails.append(name + ": cnf missing")
                            continue
                        units = audit_cnf.expected_units(
                            N, p, q, s, os.path.join(H, pf),
                            os.path.join(H, qf),
                            os.path.join(H, sf) if sf != "-" else "-")
                        if base & units:
                            fails.append(name + ": unit collides with base")
                            continue
                        exp_ms = base_ms + Counter({c: 1 for c in units})
                        got_ms, header, nlines = file_multiset(path)
                        if header != nlines:
                            fails.append("%s: header %s != %d clause lines"
                                         % (name, header, nlines))
                        dup = [c for c, n in got_ms.items() if n > 1]
                        if dup:
                            fails.append("%s: %d duplicated clauses"
                                         % (name, len(dup)))
                        if got_ms != exp_ms:
                            miss = exp_ms - got_ms
                            extra = got_ms - exp_ms
                            fails.append("%s: multiset mismatch (%d missing, "
                                         "%d extra)" % (name, sum(miss.values()),
                                                        sum(extra.values())))
    if fails:
        print("MULTISET AUDIT FAIL (layer N=%d, %d cubes required):" % (N, total))
        for f in fails:
            print("  -", f)
        return 1
    print("MULTISET AUDIT PASS: layer N=%d, all %d required cube CNFs are "
          "exactly base+units as multisets (no dups, headers exact)" % (N, total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
