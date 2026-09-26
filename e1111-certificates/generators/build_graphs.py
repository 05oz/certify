#!/usr/bin/env python3
"""Graph constructions (stdlib only).  Writes edge-list files:
   first line 'n m', then m lines 'u v' (0-based, u<v).

Usage: build_graphs.py NAME OUTFILE
NAME in: c5, grotzsch, mmc5, mmmc5, chvatal, mchvatal, clebsch, mclebsch,
         sg:n:k (Schrijver), kg:n:k (Kneser), mr:r:NAME (generalized Mycielskian)
"""
import itertools
import sys


def cycle(n):
    return n, {(i, (i + 1) % n) if i < (i + 1) % n else ((i + 1) % n, i) for i in range(n)}


def norm(E):
    return {(min(u, v), max(u, v)) for (u, v) in E}


def mycielski(n, E):
    """Vertices: v (0..n-1), copy v' = n+v, apex 2n.  v' ~ N(v); apex ~ all copies."""
    F = set(E)
    for (u, v) in E:
        F.add((u, n + v))
        F.add((v, n + u))
    for v in range(n):
        F.add((n + v, 2 * n))
    return 2 * n + 1, norm(F)


def gen_mycielski(r, n, E):
    """Generalized Mycielskian M_r(G): layers V_0..V_r (vertex (v,i) = i*n+v),
    V_0 carries E; (u,i)~(v,i+1) for uv in E (both orientations); apex (r+1)*n ~ all of V_r."""
    F = set(E)
    for i in range(r):
        for (u, v) in E:
            F.add((i * n + u, (i + 1) * n + v))
            F.add((i * n + v, (i + 1) * n + u))
    apex = (r + 1) * n
    for v in range(n):
        F.add((r * n + v, apex))
    return apex + 1, norm(F)


def chvatal():
    adj = {0: [1, 4, 6, 9], 1: [2, 5, 7], 2: [3, 6, 8], 3: [4, 7, 9], 4: [5, 8],
           5: [10, 11], 6: [10, 11], 7: [8, 11], 8: [10], 9: [10, 11]}
    return 12, norm({(u, v) for u in adj for v in adj[u]})


def clebsch():
    S = [1, 2, 4, 8, 15]
    return 16, norm({(x, x ^ s) for x in range(16) for s in S})


def schrijver(n, k):
    """Stable k-subsets of the n-cycle (no two cyclically consecutive), adjacent iff disjoint."""
    V = [S for S in itertools.combinations(range(n), k)
         if all((S[i] + 1) % n not in S for i in range(k))]
    idx = {S: i for i, S in enumerate(V)}
    E = set()
    for a in range(len(V)):
        sa = set(V[a])
        for b in range(a + 1, len(V)):
            if sa.isdisjoint(V[b]):
                E.add((a, b))
    return len(V), E, V


def kneser(n, k):
    V = list(itertools.combinations(range(n), k))
    E = set()
    for a in range(len(V)):
        sa = set(V[a])
        for b in range(a + 1, len(V)):
            if sa.isdisjoint(V[b]):
                E.add((a, b))
    return len(V), E, V


def build(name):
    if name == 'c5':
        return cycle(5)
    if name == 'grotzsch':
        return mycielski(*cycle(5))
    if name == 'mmc5':
        return mycielski(*mycielski(*cycle(5)))
    if name == 'mmmc5':
        return mycielski(*mycielski(*mycielski(*cycle(5))))
    if name == 'chvatal':
        return chvatal()
    if name == 'mchvatal':
        return mycielski(*chvatal())
    if name == 'clebsch':
        return clebsch()
    if name == 'mclebsch':
        return mycielski(*clebsch())
    if name.startswith('sg:'):
        _, n, k = name.split(':')
        n, E, _ = schrijver(int(n), int(k))
        return n, E
    if name.startswith('kg:'):
        _, n, k = name.split(':')
        n, E, _ = kneser(int(n), int(k))
        return n, E
    if name.startswith('mr:'):
        _, r, rest = name.split(':', 2)
        return gen_mycielski(int(r), *build(rest))
    if name.startswith('m:'):
        return mycielski(*build(name[2:]))
    if name.startswith('cyc:'):
        return cycle(int(name[4:]))
    raise SystemExit('unknown graph ' + name)


def write(path, n, E):
    with open(path, 'w') as f:
        f.write('%d %d\n' % (n, len(E)))
        for (u, v) in sorted(E):
            f.write('%d %d\n' % (u, v))


if __name__ == '__main__':
    n, E = build(sys.argv[1])
    write(sys.argv[2], n, E)
    print(sys.argv[1], 'n=%d m=%d' % (n, len(E)))
