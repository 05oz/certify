#!/usr/bin/env python3
"""Independent verifier for p3span CERT lines (Kelmans OPG-46613 sweep).

Stdlib only. Shares NO code with the searcher: its own graph6 decoder, its own
adjacency representation (set of frozenset edges), its own connectivity check.

For each line "CERT <g6> | a-b-c a-b-c ... | v v ..." it checks:
  1. g6 decodes to a simple graph on n vertices, every vertex degree exactly 3;
  2. the graph is 3-connected: it is connected, stays connected after deleting
     any single vertex and any pair of vertices (checked by fresh BFS each time);
  3. the listed triples are vertex-disjoint, each triple (a,b,c) satisfies
     {a,b} and {b,c} being edges of the graph (a path on 3 vertices);
  4. the avoided list is exactly V minus the union of the triples;
  5. len(avoided) == n mod 3 and #triples == n // 3  (i.e. lambda(G) = floor(n/3),
     which is Kelmans' claim (P) for this graph).

Usage: verify_cert.py file1 [file2 ...]   (also accepts .gz)
Exit 0 and prints "VERIFIED <k> certificates, <files>" if every line passes;
exits 1 on the first failure with a diagnostic.
"""
import sys, gzip

def g6_decode(s):
    data = [ord(c) - 63 for c in s]
    if any(d < 0 or d > 63 for d in data):
        raise ValueError("bad g6 char")
    n = data[0]
    if n > 62:
        raise ValueError("only short-form g6 supported")
    need = n * (n - 1) // 2
    nbytes = -(-need // 6)
    if len(data) - 1 != nbytes:
        raise ValueError("bad g6 length")
    bits = []
    for d in data[1:]:
        for k in range(5, -1, -1):
            bits.append((d >> k) & 1)
    edges = set()
    idx = 0
    for j in range(1, n):
        for i in range(j):
            if bits[idx]:
                edges.add(frozenset((i, j)))
            idx += 1
    return n, edges

def neighbors(n, edges):
    nb = {v: set() for v in range(n)}
    for e in edges:
        a, b = tuple(e)
        nb[a].add(b); nb[b].add(a)
    return nb

def connected_after_removing(n, nb, removed):
    verts = [v for v in range(n) if v not in removed]
    if not verts:
        return True
    seen = {verts[0]}
    stack = [verts[0]]
    while stack:
        v = stack.pop()
        for w in nb[v]:
            if w not in removed and w not in seen:
                seen.add(w); stack.append(w)
    return len(seen) == len(verts)

def is_3_connected(n, nb):
    if not connected_after_removing(n, nb, set()):
        return False
    for u in range(n):
        if not connected_after_removing(n, nb, {u}):
            return False
    for u in range(n):
        for v in range(u + 1, n):
            if not connected_after_removing(n, nb, {u, v}):
                return False
    return True

def check_line(line, lineno, fname, seen_g6, opts):
    parts = line.split('|')
    if len(parts) != 3:
        raise SystemExit(f"{fname}:{lineno}: malformed CERT line")
    head = parts[0].split()
    if head[0] != 'CERT':
        raise SystemExit(f"{fname}:{lineno}: not a CERT line")
    g6 = head[1]
    try:
        n, edges = g6_decode(g6)
    except ValueError as e:
        raise SystemExit(f"{fname}:{lineno}: graph6 decode: {e}")
    nb = neighbors(n, edges)
    for v in range(n):
        if len(nb[v]) != 3:
            raise SystemExit(f"{fname}:{lineno}: vertex {v} degree {len(nb[v])} != 3")
    if opts.get('check_conn', True) and not is_3_connected(n, nb):
        raise SystemExit(f"{fname}:{lineno}: graph not 3-connected")
    triples = []
    for tok in parts[1].split():
        abc = tok.split('-')
        if len(abc) != 3:
            raise SystemExit(f"{fname}:{lineno}: bad triple {tok}")
        triples.append(tuple(int(x) for x in abc))
    avoided = [int(x) for x in parts[2].split()]
    used = []
    for (a, b, c) in triples:
        if frozenset((a, b)) not in edges or frozenset((b, c)) not in edges:
            raise SystemExit(f"{fname}:{lineno}: {a}-{b}-{c} is not a path in the graph")
        if a == c:
            raise SystemExit(f"{fname}:{lineno}: degenerate triple {a}-{b}-{c}")
        used.extend((a, b, c))
    if len(set(used)) != len(used):
        raise SystemExit(f"{fname}:{lineno}: triples not vertex-disjoint")
    if set(used) | set(avoided) != set(range(n)) or set(used) & set(avoided):
        raise SystemExit(f"{fname}:{lineno}: triples+avoided is not a partition of V")
    if len(avoided) != n % 3 or len(triples) != n // 3:
        raise SystemExit(f"{fname}:{lineno}: not a maximum packing shape: "
                         f"{len(triples)} triples, {len(avoided)} avoided, n={n}")
    seen_g6.add(g6)
    return n

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    opts = {'check_conn': '--no-conn' not in sys.argv}
    total = 0
    seen = set()
    ns = {}
    for fname in args:
        op = gzip.open if fname.endswith('.gz') else open
        with op(fname, 'rt') as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line or not line.startswith('CERT'):
                    continue
                n = check_line(line, i, fname, seen, opts)
                ns[n] = ns.get(n, 0) + 1
                total += 1
    print(f"VERIFIED {total} certificates ({len(seen)} distinct graphs) "
          f"by order: {sorted(ns.items())}")

if __name__ == '__main__':
    main()
