#!/usr/bin/env python3
"""Check that an edge-list file IS a named construction (stdlib only).
  check_construction.py mmc5 GRAPH.edges      M(M(C5)) with the labelling of build_graphs.py
  check_construction.py circ N s1,s2,.. GRAPH.edges   circulant Cay(Z_N, {+-s_i})
Prints PASS/FAIL; exit 0 iff PASS.
Mycielskian M(H) (H on 0..n-1): copies n+v adjacent to N_H(v), apex 2n adjacent to all copies.
"""
import sys


def read(path):
    t = open(path).read().split()
    n, m = int(t[0]), int(t[1])
    E = {frozenset((int(t[2 + 2 * i]), int(t[3 + 2 * i]))) for i in range(m)}
    if len(E) != m:
        print('FAIL: repeated edges'); sys.exit(1)
    return n, E


def myc(n, E):
    F = set(E)
    for e in E:
        u, v = tuple(e)
        F.add(frozenset((u, n + v)))
        F.add(frozenset((v, n + u)))
    for v in range(n):
        F.add(frozenset((n + v, 2 * n)))
    return 2 * n + 1, F


def main():
    if sys.argv[1] == 'mmc5':
        n, E = read(sys.argv[2])
        c5 = {frozenset((i, (i + 1) % 5)) for i in range(5)}
        want = myc(*myc(5, c5))
    elif sys.argv[1] == 'circ':
        N = int(sys.argv[2])
        S = {int(x) % N for x in sys.argv[3].split(',')}
        S |= {(-s) % N for s in S}
        n, E = read(sys.argv[4])
        want = (N, {frozenset((a, (a + s) % N)) for a in range(N) for s in S})
    else:
        print('FAIL: unknown construction'); sys.exit(1)
    if (n, E) != want:
        print('FAIL: graph differs from construction (n=%d vs %d, |E|=%d vs %d)' % (n, want[0], len(E), len(want[1])))
        sys.exit(1)
    print('construction %s: identical edge set (n=%d, m=%d)' % (sys.argv[1], n, len(E)))
    print('PASS')


if __name__ == '__main__':
    main()
