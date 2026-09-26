#!/usr/bin/env python3
"""Audit that a CNF is (a subset of) the from-definition encoding of a graph (stdlib only).
Independent re-implementation of the clause semantics documented in gen_cnf.py.

  audit_cnf.py col  GRAPH.edges K FORMULA.cnf
  audit_cnf.py pair GRAPH.edges FORMULA.cnf

For UNSAT certificates only the direction 'every clause of FORMULA is a valid
constraint' matters (a subset of a satisfiable set is satisfiable); the audit
also reports whether the clause set is exactly the full encoding.
Prints PASS/FAIL, exit 0 iff PASS.
"""
import sys
from itertools import combinations


def graph(path):
    t = open(path).read().split()
    n, m = int(t[0]), int(t[1])
    E = [(int(t[2 + 2 * i]), int(t[3 + 2 * i])) for i in range(m)]
    return n, E


def cnf(path):
    cls = []
    for line in open(path):
        s = line.split()
        if not s or s[0] in ('c', 'p'):
            continue
        lits = list(map(int, s))
        if lits[-1] != 0 or 0 in lits[:-1]:
            print('FAIL: malformed clause line')
            sys.exit(1)
        cls.append(frozenset(lits[:-1]))
    return cls


def allowed_col(n, E, K):
    x = lambda v, c: v * K + c + 1
    ok = set()
    for v in range(n):
        ok.add(frozenset(x(v, c) for c in range(K)))
    for (u, w) in E:
        for c in range(K):
            ok.add(frozenset((-x(u, c), -x(w, c))))
    return ok, x


def allowed_pair(n, E):
    m = len(E)
    ok = set()
    inc = {v: [] for v in range(n)}
    for e, (u, w) in enumerate(E):
        inc[u].append(e)
        inc[w].append(e)
    for off, aoff, poff in ((0, 2 * m, 2 * m + 2 * n), (m, 2 * m + n, 3 * m + 2 * n)):
        X = lambda e: off + e + 1
        Av = lambda v: aoff + v + 1
        P = lambda i: poff + i + 1
        for v in range(n):
            for t in combinations(inc[v], 3):
                ok.add(frozenset(-X(e) for e in t))
            for e in inc[v]:
                ok.add(frozenset([-X(e)] + [X(f) for f in inc[v] if f != e]))
        for e, (u, w) in enumerate(E):
            ok.add(frozenset((-X(e), Av(u))))
            ok.add(frozenset((-X(e), Av(w))))
        ok.add(frozenset((-P(0), X(0))))
        ok.add(frozenset((P(0), -X(0))))
        for i in range(1, m):
            p, q, z = P(i), P(i - 1), X(i)
            # p <-> (q xor z): exactly the 4 clauses excluding the 4 bad assignments
            ok |= {frozenset((-p, q, z)), frozenset((-p, -q, -z)), frozenset((p, -q, z)), frozenset((p, q, -z))}
        ok.add(frozenset((P(m - 1),)))
    a = lambda v: 2 * m + v + 1
    b = lambda v: 2 * m + n + v + 1
    for v in range(n):
        ok.add(frozenset((-a(v), -b(v))))
    for (u, w) in E:
        ok.add(frozenset((-a(u), -b(w))))
        ok.add(frozenset((-a(w), -b(u))))
    return ok


def main():
    mode = sys.argv[1]
    n, E = graph(sys.argv[2])
    Es = {(min(u, w), max(u, w)) for (u, w) in E}
    if mode == 'col':
        K = int(sys.argv[3])
        F = cnf(sys.argv[4])
        ok, x = allowed_col(n, E, K)
        units = [c for c in F if c not in ok]
        # the only extra clauses allowed: units x(U,0), x(V,1) with UV an edge
        pos = {}
        for c in units:
            if len(c) != 1:
                print('FAIL: clause not in encoding:', sorted(c)); sys.exit(1)
            (l,) = tuple(c)
            if l <= 0 or l > n * K:
                print('FAIL: bad unit', l); sys.exit(1)
            v, col = (l - 1) // K, (l - 1) % K
            if col in pos and pos[col] != v:
                print('FAIL: two units with same colour'); sys.exit(1)
            pos[col] = v
        if set(pos) - {0, 1}:
            print('FAIL: symmetry-break units must use colours 0 and 1'); sys.exit(1)
        if len(pos) == 2 and (min(pos[0], pos[1]), max(pos[0], pos[1])) not in Es:
            print('FAIL: symmetry-break vertices are not an edge'); sys.exit(1)
        exact = set(F) - set(units) == ok
        print('audit col: %d clauses, all valid; symmetry-break units %s on edge; full encoding present: %s'
              % (len(F), {c: v for c, v in pos.items()}, exact))
    elif mode == 'pair':
        F = cnf(sys.argv[3])
        ok = allowed_pair(n, E)
        for c in F:
            if c not in ok:
                print('FAIL: clause not in encoding:', sorted(c)); sys.exit(1)
        print('audit pair: %d clauses, all valid; full encoding present: %s' % (len(F), set(F) == ok))
    else:
        print('FAIL: mode'); sys.exit(1)
    print('PASS')


if __name__ == '__main__':
    main()
