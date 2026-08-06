#!/usr/bin/env python3
"""encode_cnf.py <n> <bitsfile-line-or-string> <k> <out.cnf>

CNF asserting: the tournament (gentourng ascii upper-triangle format, char at pair
(i,j), i<j, row-by-row, '1' iff i->j) contains k pairwise arc-disjoint transitive
triples. UNSAT => max packing <= k-1.

ENCODING SPEC (fixed; the independent verifier regenerates it byte-identically):
- Enumerate triples (i,j,k), i<j<k, in lexicographic order; keep the transitive ones
  (triple cyclic iff orientation pattern (i->j, j->k, k->i) or (j->i, i->k, k->j)).
  TT3 t gets variable x_t = t+1 (1-based, in this order). m = number of TT3s.
- Conflict clauses: for each pair s<t of TT3s sharing >=1 arc (unordered vertex
  pair), clause (-x_s -x_t), in lexicographic order of (s,t).
- Cardinality sum x >= k via Sinz sequential at-most-K counter on the negations
  y_t = NOT x_t, K = m-k: aux vars s_{i,j} = m + (i-1)*K + j for i=1..m, j=1..K.
  Clauses in this order:
    ( x_1  s_{1,1})
    (-s_{1,j})                       for j=2..K
    for i=2..m:
      ( x_i  s_{i,1})
      (-s_{i-1,1}  s_{i,1})
      for j=2..K: ( x_i  -s_{i-1,j-1}  s_{i,j}) ; (-s_{i-1,j}  s_{i,j})
      ( x_i  -s_{i-1,K})
  (y_i = -x_i, so -y_i = x_i.)  Requires K >= 1 and m >= k.
"""
import sys


def transitive_triples(n, bits):
    pidx = {}
    p = 0
    for i in range(n):
        for j in range(i + 1, n):
            pidx[(i, j)] = p
            p += 1
    adj = {}
    for (i, j), q in pidx.items():
        b = bits[q] == '1'
        adj[(i, j)] = b
        adj[(j, i)] = not b
    tris = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                a, b, c = adj[(i, j)], adj[(j, k)], adj[(i, k)]
                cyc = (a and b and not c) or (not a and not b and c)
                if not cyc:
                    tris.append((i, j, k))
    return tris, pidx


def build_cnf(n, bits, k):
    tris, pidx = transitive_triples(n, bits)
    m = len(tris)
    assert m >= k and m - k >= 1
    arcsets = [frozenset((pidx[(t[0], t[1])], pidx[(t[1], t[2])], pidx[(t[0], t[2])]))
               for t in tris]
    clauses = []
    for s in range(m):
        for t in range(s + 1, m):
            if arcsets[s] & arcsets[t]:
                clauses.append((-(s + 1), -(t + 1)))
    K = m - k
    S = lambda i, j: m + (i - 1) * K + j
    clauses.append((1, S(1, 1)))
    for j in range(2, K + 1):
        clauses.append((-S(1, j),))
    for i in range(2, m + 1):
        clauses.append((i, S(i, 1)))
        clauses.append((-S(i - 1, 1), S(i, 1)))
        for j in range(2, K + 1):
            clauses.append((i, -S(i - 1, j - 1), S(i, j)))
            clauses.append((-S(i - 1, j), S(i, j)))
        clauses.append((i, -S(i - 1, K)))
    nvars = m + m * K
    return nvars, clauses, m


def main():
    n = int(sys.argv[1])
    bits = sys.argv[2].strip()
    k = int(sys.argv[3])
    out = sys.argv[4]
    assert len(bits) == n * (n - 1) // 2 and set(bits) <= {'0', '1'}
    nvars, clauses, m = build_cnf(n, bits, k)
    with open(out, 'w') as f:
        f.write(f"c tt3 packing >= {k} in tournament n={n} bits={bits} m_TT3={m}\n")
        f.write(f"p cnf {nvars} {len(clauses)}\n")
        for cl in clauses:
            f.write(' '.join(map(str, cl)) + ' 0\n')
    print(f"wrote {out}: n={n} k={k} m={m} vars={nvars} clauses={len(clauses)}")


if __name__ == '__main__':
    main()
