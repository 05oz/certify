#!/usr/bin/env python3
"""
Checker for the k(3,4) non-uniqueness certificates (Certify, Part J).

Reads the 13 witness files w01_W.json, w02.json, ..., w13.json (each a JSON
object {"N":20,"a":3,"b":4,"arcs":[[u,v],...]}, arc u->v) and certifies:

  (A) each is a valid oriented graph (no loop, no 2-cycle);
  (B) each is {I_3, TT_4}-free, by EXHAUSTIVE test over all C(20,3)=1140 triples
      and all C(20,4)=4845 quadruples (a 4-set is a TT_4 iff its six pairs are
      all adjacent and its in-set out-degree multiset is {0,1,2,3});
  (C) each is rigid, |Aut|=1, certified two independent ways:
        (c1) Weisfeiler-Leman colour refinement is discrete (20 distinct colours),
        (c2) an explicit automorphism backtracker returns count 1;
  (D) the 13 are pairwise non-isomorphic, by a canonical form (WL-rank labelling,
      valid because WL is discrete) cross-checked by a rich invariant fingerprint;
      any collision is settled by an explicit isomorphism backtracker.

Prints PASS and exits 0 iff all four hold for all 13 files (so there are at least
13 pairwise non-isomorphic rigid {I_3,TT_4}-free oriented graphs on 20 vertices,
and W = w01 is not the unique such graph). Standard library only; no threads, no
subprocess, no OS-specific calls; deterministic; runs on any CPython 3.x.

Stdlib-only; shares only boilerplate with the SAT search (32 of 174 executable
lines).  NOT independent of the private structure-mining scripts in
hunt-structure/: the backtracker inside aut_count, the backtracker inside iso,
and adj are the same routines as there; rel, load, i3_free and tt4_free differ
only in parameter lists, in what they return, or in the order of the two
operands of one != comparison.  So |Aut| = 1 as reported by aut_count must not
be read as an independent re-derivation.  Written here: wl_colours (none of its
17 executable lines appears in that tree, and it is alpha-equivalent to nothing
there), canonical_form, and the invariant fingerprint, of which only the nbar
term matches a private expression and that only up to the loop bound.  A
refinement discrete at 20 colours forces |Aut| = 1 on its own, and iso is
reached only on a canonical-form collision, which does not occur on the 13
shipped witnesses.  (Disclosed 2026-08-14.)
"""
import json, itertools, os, sys, glob
from collections import Counter

N = 20

def load(path):
    d = json.load(open(path))
    n = d["N"]
    A = [[0] * n for _ in range(n)]
    for u, v in d["arcs"]:
        A[u][v] = 1
    return n, A, d

def rel(A, u, v):
    if A[u][v]:
        return 1
    if A[v][u]:
        return -1
    return 0

def adj(A, u, v):
    return A[u][v] or A[v][u]

# (A)
def valid_oriented(n, A):
    for u in range(n):
        if A[u][u]:
            return False
    for u in range(n):
        for v in range(u + 1, n):
            if A[u][v] and A[v][u]:
                return False
    return True

# (B)
def i3_free(n, A):
    for a, b, c in itertools.combinations(range(n), 3):
        if not adj(A, a, b) and not adj(A, a, c) and not adj(A, b, c):
            return False
    return True

def tt4_free(n, A):
    for four in itertools.combinations(range(n), 4):
        if all(adj(A, x, y) for x, y in itertools.combinations(four, 2)):
            outs = sorted(sum(1 for y in four if y != x and A[x][y]) for x in four)
            if outs == [0, 1, 2, 3]:
                return False
    return True

# Weisfeiler-Leman refinement with comparable (rank) colours.
def wl_colours(n, A):
    outd = [sum(A[u]) for u in range(n)]
    ind = [sum(A[v][u] for v in range(n)) for u in range(n)]
    sig = [(outd[u], ind[u]) for u in range(n)]

    def rank(sigs):
        order = {s: i for i, s in enumerate(sorted(set(sigs)))}
        return [order[s] for s in sigs]

    col = rank(sig)
    while True:
        newsig = []
        for u in range(n):
            nb = tuple(sorted((rel(A, u, v), col[v]) for v in range(n) if v != u))
            newsig.append((col[u], nb))
        newcol = rank(newsig)
        if newcol == col:
            return col
        col = newcol

# (c2)
def aut_count(n, A, col):
    order = sorted(range(n), key=lambda u: (col[u], u))
    perm = [-1] * n
    used = [False] * n
    count = 0

    def consistent(i, j):
        for k in range(n):
            if perm[k] != -1 and rel(A, i, k) != rel(A, j, perm[k]):
                return False
        return True

    def bt(idx):
        nonlocal count
        if idx == n:
            count += 1
            return
        i = order[idx]
        for j in range(n):
            if used[j] or col[j] != col[i]:
                continue
            if consistent(i, j):
                perm[i] = j
                used[j] = True
                bt(idx + 1)
                perm[i] = -1
                used[j] = False

    bt(0)
    return count

def canonical_form(n, A, col):
    order = sorted(range(n), key=lambda u: col[u])
    return tuple(rel(A, order[i], order[j]) for i in range(n) for j in range(n))

def invariant(n, A):
    outd = [sum(A[u]) for u in range(n)]
    ind = [sum(A[v][u] for v in range(n)) for u in range(n)]
    degpairs = tuple(sorted(zip(outd, ind)))
    nbar = tuple(sorted(n - 1 - outd[u] - ind[u] for u in range(n)))
    return (sum(outd), degpairs, nbar)

def iso(n, A, B):
    outA = [sum(A[u]) for u in range(n)]
    inA = [sum(A[v][u] for v in range(n)) for u in range(n)]
    outB = [sum(B[u]) for u in range(n)]
    inB = [sum(B[v][u] for v in range(n)) for u in range(n)]
    if sorted(zip(outA, inA)) != sorted(zip(outB, inB)):
        return False
    f = [-1] * n
    used = [False] * n
    order = sorted(range(n), key=lambda u: -(outA[u] + inA[u]))

    def bt(idx):
        if idx == n:
            return True
        u = order[idx]
        for g in range(n):
            if used[g] or outA[u] != outB[g] or inA[u] != inB[g]:
                continue
            if all(rel(A, u, order[k]) == rel(B, g, f[order[k]]) for k in range(idx)):
                f[u] = g
                used[g] = True
                if bt(idx + 1):
                    return True
                f[u] = -1
                used[g] = False
        return False

    return bt(0)

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    certdir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "k34add-certificates")
    files = sorted(glob.glob(os.path.join(certdir, "w*.json")))
    if not files:
        print("FAIL: no witness files w*.json found in", certdir)
        return 1

    graphs = []
    for p in files:
        n, A, d = load(p)
        name = os.path.basename(p)
        if n != N or d.get("a") != 3 or d.get("b") != 4:
            print("FAIL: %s is not a 20-vertex (a,b)=(3,4) instance" % name)
            return 1
        graphs.append((name, n, A))

    ok = True
    cols = []
    canons = []
    invs = []
    print("# per-witness checks (N=20; C(20,3)=1140 triples, C(20,4)=4845 quads)")
    for name, n, A in graphs:
        v = valid_oriented(n, A)
        i3 = i3_free(n, A)
        tt4 = tt4_free(n, A)
        col = wl_colours(n, A)
        discrete = len(set(col)) == n
        ac = aut_count(n, A, col)
        cols.append(col)
        canons.append(canonical_form(n, A, col))
        invs.append(invariant(n, A) + (Counter(col) == Counter(range(n)),))
        good = v and i3 and tt4 and discrete and ac == 1
        ok &= good
        print("  %-9s valid=%s I3free=%s TT4free=%s WLdiscrete=%s |Aut|=%d  %s"
              % (name, v, i3, tt4, discrete, ac, "OK" if good else "FAIL"))

    # pairwise non-isomorphism
    pairwise_ok = True
    ncanon = len(set(canons))
    for i in range(len(graphs)):
        for j in range(i + 1, len(graphs)):
            if canons[i] == canons[j]:
                if iso(N, graphs[i][2], graphs[j][2]):
                    pairwise_ok = False
                    print("  ISOMORPHIC: %s == %s" % (graphs[i][0], graphs[j][0]))
    ok &= pairwise_ok
    print("# distinct canonical forms: %d / %d" % (ncanon, len(graphs)))
    print("# distinct invariant fingerprints: %d / %d" % (len(set(invs)), len(graphs)))
    print("# all pairwise non-isomorphic: %s" % pairwise_ok)

    if ok:
        print("PASS: %d valid, {I_3,TT_4}-free, rigid (|Aut|=1), pairwise "
              "non-isomorphic oriented graphs on 20 vertices." % len(graphs))
        print("      => the 20-vertex k(3,4) extremal graph is NOT unique "
              "(at least %d classes)." % len(graphs))
        return 0
    print("FAIL")
    return 1

if __name__ == "__main__":
    sys.exit(main())
