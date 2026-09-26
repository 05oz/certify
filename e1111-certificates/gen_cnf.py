#!/usr/bin/env python3
"""From-definition CNF generators (stdlib only).

  gen_cnf.py col  GRAPH.edges K U V  > out.cnf
      proper K-colouring of G; var(v,c) = v*K + c + 1 (c = 0..K-1);
      clauses: (OR_c x[v,c]) for every v;  (-x[u,c] | -x[w,c]) for every edge uw, colour c;
      symmetry break (sound, see README): units x[U,0], x[V,1] for the EDGE UV.
  gen_cnf.py pair GRAPH.edges > out.cnf
      "G contains two vertex-disjoint, anticomplete odd cycles".  Edges e = 0..m-1 in file order.
      x[e] = e+1, y[e] = m+e+1, a[v] = 2m+v+1, b[v] = 2m+n+v+1,
      px[i] = 2m+2n+i+1, py[i] = 3m+2n+i+1  (i = 0..m-1).
      For X in {x,y} and every vertex v with incident edges I(v):
         (-X[e] | -X[f] | -X[g])   for all 3-subsets {e,f,g} of I(v)   (degree <= 2)
         (-X[e] | OR_{f in I(v)-e} X[f])  for e in I(v)                 (degree != 1)
      (-x[e] | a[u]), (-x[e] | a[w]), (-y[e] | b[u]), (-y[e] | b[w])  for e = uw
      (-a[v] | -b[v]) for all v;  (-a[u] | -b[w]), (-a[w] | -b[u]) for every edge uw
      parity chain: p[0] <-> X[0];  p[i] <-> p[i-1] XOR X[i];  unit p[m-1]  (odd #edges).
"""
import itertools
import sys


def read_graph(path):
    toks = open(path).read().split()
    n, m = int(toks[0]), int(toks[1])
    E = [(int(toks[2 + 2 * i]), int(toks[3 + 2 * i])) for i in range(m)]
    return n, E


def col_cnf(n, E, K, U, V):
    assert (U, V) in E or (V, U) in E, 'symmetry-break pair must be an edge'
    var = lambda v, c: v * K + c + 1
    cl = [[var(v, c) for c in range(K)] for v in range(n)]
    for (u, w) in E:
        for c in range(K):
            cl.append([-var(u, c), -var(w, c)])
    cl.append([var(U, 0)])
    cl.append([var(V, 1)])
    return n * K, cl


def pair_cnf(n, E):
    m = len(E)
    X = {'x': lambda e: e + 1, 'y': lambda e: m + e + 1}
    A = {'x': lambda v: 2 * m + v + 1, 'y': lambda v: 2 * m + n + v + 1}
    P = {'x': lambda i: 2 * m + 2 * n + i + 1, 'y': lambda i: 3 * m + 2 * n + i + 1}
    inc = [[] for _ in range(n)]
    for e, (u, w) in enumerate(E):
        inc[u].append(e)
        inc[w].append(e)
    cl = []
    for t in ('x', 'y'):
        xv, av, pv = X[t], A[t], P[t]
        for v in range(n):
            for (e, f, g) in itertools.combinations(inc[v], 3):
                cl.append([-xv(e), -xv(f), -xv(g)])
            for e in inc[v]:
                cl.append([-xv(e)] + [xv(f) for f in inc[v] if f != e])
        for e, (u, w) in enumerate(E):
            cl.append([-xv(e), av(u)])
            cl.append([-xv(e), av(w)])
        # parity chain
        cl.append([-pv(0), xv(0)])
        cl.append([pv(0), -xv(0)])
        for i in range(1, m):
            p, q, z = pv(i), pv(i - 1), xv(i)
            cl += [[-p, q, z], [-p, -q, -z], [p, -q, z], [p, q, -z]]
        cl.append([pv(m - 1)])
    for v in range(n):
        cl.append([-A['x'](v), -A['y'](v)])
    for (u, w) in E:
        cl.append([-A['x'](u), -A['y'](w)])
        cl.append([-A['x'](w), -A['y'](u)])
    return 4 * m + 2 * n, cl


def dump(nv, cl, out):
    out.write('p cnf %d %d\n' % (nv, len(cl)))
    for c in cl:
        out.write(' '.join(map(str, c)) + ' 0\n')


if __name__ == '__main__':
    mode = sys.argv[1]
    n, E = read_graph(sys.argv[2])
    if mode == 'col':
        K, U, V = map(int, sys.argv[3:6])
        dump(*col_cnf(n, E, K, U, V), sys.stdout)
    elif mode == 'pair':
        dump(*pair_cnf(n, E), sys.stdout)
    else:
        raise SystemExit('mode col|pair')
