#!/usr/bin/env python3
"""Standalone stdlib checker for Erdos #1111 (t = c = 3) counterexample graphs.

Usage:  python3 check_P.py GRAPH.edges [--pruned]

GRAPH.edges: first line 'n m', then m lines 'u v' (0 <= u,v < n).
Checks, from the definitions:
  (0) the file is a simple graph (no loops, no repeated edges, ids in range);
  (1) G is triangle-free (omega(G) < 3);
  (2) Criterion A: enumerates EVERY induced odd cycle C of G (each exactly once)
      and verifies that G - N[C] is bipartite by constructing an explicit proper
      2-colouring of G - N[C] and re-checking every edge of G - N[C] against it;
  (3) Criterion B (independent of the bipartiteness routine): among all induced
      odd cycles enumerated in (2), no two are vertex-disjoint with no edge between them.
With --pruned (for large graphs), Criterion A is run as a DFS over induced paths
that stops extending a path P as soon as G - N[P] is bipartite (sound: every
cycle C through P has N[C] >= N[P]); Criterion B is then skipped.
Why (2) and (3) each prove "no two anticomplete non-bipartite sets": see README.md.
Prints PASS/FAIL, exits 0 iff PASS.
"""
import sys


def fail(msg):
    print('FAIL:', msg)
    sys.exit(1)


def read_graph(path):
    with open(path) as f:
        toks = f.read().split()
    if len(toks) < 2:
        fail('empty file')
    n, m = int(toks[0]), int(toks[1])
    if len(toks) != 2 + 2 * m:
        fail('edge count mismatch')
    adj = [set() for _ in range(n)]
    for i in range(m):
        u, v = int(toks[2 + 2 * i]), int(toks[3 + 2 * i])
        if not (0 <= u < n and 0 <= v < n):
            fail('vertex out of range')
        if u == v:
            fail('loop')
        if v in adj[u]:
            fail('repeated edge')
        adj[u].add(v)
        adj[v].add(u)
    return n, m, adj


def two_colouring(adj, allowed):
    """Return a dict colouring of G[allowed] with 2 colours, or None if an odd cycle exists.
    The returned colouring is re-verified edge by edge by the caller."""
    col = {}
    for s in allowed:
        if s in col:
            continue
        col[s] = 0
        stack = [s]
        while stack:
            u = stack.pop()
            for w in adj[u]:
                if w not in allowed:
                    continue
                if w not in col:
                    col[w] = 1 - col[u]
                    stack.append(w)
                elif col[w] == col[u]:
                    return None
    return col


def verify_colouring(adj, allowed, col):
    for u in allowed:
        if col.get(u) not in (0, 1):
            return False
        for w in adj[u]:
            if w in allowed and col[w] == col[u]:
                return False
    return True


def closed_nbhd(adj, S):
    out = set(S)
    for x in S:
        out |= adj[x]
    return out


def induced_odd_cycles(n, adj):
    """Yield every induced cycle of odd length >= 5 exactly once as a vertex list
    (c0 = min vertex, c1 < c_last).  Triangles are excluded by the caller's check (1)."""
    res = []

    def ext(path, pset):
        s = path[0]
        u = path[-1]
        for w in sorted(adj[u]):
            if w <= s or w in pset:
                continue
            nbp = adj[w] & pset  # path vertices adjacent to w (always contains u)
            other = nbp - {u}
            if len(path) >= 2 and other == {s}:
                # w closes the induced cycle path + [w]
                if len(path) + 1 >= 4 and (len(path) + 1) % 2 == 1 and path[1] < w:
                    res.append(path + [w])
                continue
            if other:
                continue  # w adjacent to an interior path vertex (or to s when len(path)==1: impossible)
            pset.add(w)
            path.append(w)
            ext(path, pset)
            path.pop()
            pset.discard(w)

    for s in range(n):
        ext([s], {s})
    return res


def is_induced_cycle(adj, cyc):
    k = len(cyc)
    if len(set(cyc)) != k or k < 3:
        return False
    S = set(cyc)
    for i, x in enumerate(cyc):
        want = {cyc[(i - 1) % k], cyc[(i + 1) % k]}
        if adj[x] & S != want:
            return False
    return True


def pruned_search(n, adj):
    """Criterion A with sound pruning. Returns (ok, stats)."""
    stats = {'nodes': 0, 'cycles': 0}
    V = set(range(n))

    def rest_bip(closed):
        allowed = V - closed
        col = two_colouring(adj, allowed)
        if col is None:
            return False
        if not verify_colouring(adj, allowed, col):
            fail('internal: colouring check')
        return True

    def ext(path, pset, closed):
        stats['nodes'] += 1
        s = path[0]
        u = path[-1]
        for w in sorted(adj[u]):
            if w <= s or w in pset:
                continue
            other = (adj[w] & pset) - {u}
            if len(path) >= 2 and other == {s}:
                if (len(path) + 1) % 2 == 1 and path[1] < w:
                    cyc = path + [w]
                    if not is_induced_cycle(adj, cyc):
                        fail('internal: non-induced cycle produced')
                    stats['cycles'] += 1
                    if not rest_bip(closed | adj[w] | {w}):
                        return cyc
                continue
            if other:
                continue
            c2 = closed | adj[w] | {w}
            if rest_bip(c2):
                continue  # prune: every cycle through path+[w] leaves a bipartite rest
            pset.add(w)
            path.append(w)
            r = ext(path, pset, c2)
            path.pop()
            pset.discard(w)
            if r:
                return r
        return None

    for s in range(n):
        cl = adj[s] | {s}
        if rest_bip(cl):
            continue
        r = ext([s], {s}, cl)
        if r:
            return r, stats
    return None, stats


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    pruned = '--pruned' in sys.argv
    n, m, adj = read_graph(args[0])
    print('graph: n=%d m=%d' % (n, m))
    # (1) triangle-free
    for u in range(n):
        for v in adj[u]:
            if u < v and adj[u] & adj[v]:
                fail('triangle on edge %d-%d' % (u, v))
    print('(1) triangle-free: ok')
    if pruned:
        bad, st = pruned_search(n, adj)
        if bad:
            fail('induced odd cycle %s leaves G-N[C] non-bipartite' % bad)
        print('(2) pruned exhaustive search: every induced odd cycle C leaves G-N[C] bipartite '
              '(%d DFS nodes, %d cycles closed)' % (st['nodes'], st['cycles']))
        print('PASS')
        return
    cycles = induced_odd_cycles(n, adj)
    seen = set()
    for c in cycles:
        if not is_induced_cycle(adj, c) or len(c) % 2 == 0:
            fail('enumerator produced a non-induced/even cycle %s' % c)
        key = frozenset(c)
        if key in seen:
            fail('cycle enumerated twice')
        seen.add(key)
    V = set(range(n))
    hist = {}
    for c in cycles:
        hist[len(c)] = hist.get(len(c), 0) + 1
        allowed = V - closed_nbhd(adj, c)
        col = two_colouring(adj, allowed)
        if col is None or not verify_colouring(adj, allowed, col):
            fail('Criterion A: G - N[C] not bipartite for induced odd cycle C=%s' % c)
    print('(2) Criterion A: %d induced odd cycles (by length %s); for each, G-N[C] has a verified 2-colouring'
          % (len(cycles), dict(sorted(hist.items()))))
    # (3) Criterion B
    sets = [frozenset(c) for c in cycles]
    closed = [frozenset(closed_nbhd(adj, c)) for c in cycles]
    for i in range(len(cycles)):
        for j in range(i + 1, len(cycles)):
            # anticomplete & disjoint  <=>  C_j avoids N[C_i]
            if sets[j].isdisjoint(closed[i]):
                fail('Criterion B: anticomplete disjoint odd cycles %s , %s' % (cycles[i], cycles[j]))
    print('(3) Criterion B: no two of the %d induced odd cycles are disjoint and anticomplete '
          '(%d pairs)' % (len(cycles), len(cycles) * (len(cycles) - 1) // 2))
    print('PASS')


if __name__ == '__main__':
    main()
