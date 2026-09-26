#!/usr/bin/env python3
"""Standard-library checker for oriented-Ramsey lower-bound witnesses.

A witness file is JSON {"N": int, "a": int, "b": int, "arcs": [[u, v], ...]},
arc u -> v on vertices 0..N-1.  It certifies k(a, b) = r(I_a, L_b) >= N + 1
when the arcs form an oriented graph (no loops, no repeated arcs, no 2-cycles)
with no independent a-set and no transitive tournament on b vertices.

This checker does not test subsets one by one.  It computes two exact
invariants by exhaustive bitmask branch-and-bound and compares them with a, b:

  alpha = independence number of the underlying undirected graph;
  tau   = order of the largest transitive subtournament.  A transitive
          tournament is a chain v1, ..., vt with vi -> vj for all i < j, so
          tau is the longest chain in which every new vertex lies in the
          out-neighbourhood of every earlier one.

The witness passes iff alpha <= a - 1 and tau <= b - 1.

Usage: python3 verify_bounds.py FILE [FILE ...]
Exit status 0 iff every file passes.
"""
import hashlib
import json
import sys


def load(path):
    raw = open(path, "rb").read()
    w = json.loads(raw)
    return w, hashlib.sha256(raw).hexdigest()


def check_oriented(N, arcs):
    out = [0] * N
    seen = set()
    for pair in arcs:
        if len(pair) != 2:
            return None, "arc %r is not a pair" % (pair,)
        u, v = pair
        if not (isinstance(u, int) and isinstance(v, int)):
            return None, "arc %r has a non-integer endpoint" % (pair,)
        if not (0 <= u < N and 0 <= v < N):
            return None, "arc (%d,%d) out of range" % (u, v)
        if u == v:
            return None, "loop at %d" % u
        if (u, v) in seen:
            return None, "repeated arc (%d,%d)" % (u, v)
        if (v, u) in seen:
            return None, "2-cycle on {%d,%d}" % (u, v)
        seen.add((u, v))
        out[u] |= 1 << v
    return out, None


def popcount(x):
    return bin(x).count("1")


def independence_number(N, nonadj):
    """Exact maximum independent set size (maximum clique of the complement)."""
    best = [0]

    def expand(size, cand):
        if cand == 0:
            if size > best[0]:
                best[0] = size
            return
        if size + popcount(cand) <= best[0]:
            return
        while cand:
            if size + popcount(cand) <= best[0]:
                return
            v = cand.bit_length() - 1
            cand &= ~(1 << v)
            expand(size + 1, cand & nonadj[v])

    expand(0, (1 << N) - 1)
    return best[0]


def largest_transitive(N, out):
    """Exact order of the largest transitive subtournament (longest chain)."""
    # Unlike cliques, a vertex tried at one level may still extend a chain
    # through a later sibling, so each branch is bounded by its own
    # candidate set, never by the siblings not yet tried.
    best = [0]

    def expand(size, cand):
        if size > best[0]:
            best[0] = size
        c = cand
        while c:
            v = c.bit_length() - 1
            c &= ~(1 << v)
            nxt = cand & out[v]
            if size + 1 + popcount(nxt) > best[0]:
                expand(size + 1, nxt)

    expand(0, (1 << N) - 1)
    return best[0]


def main(paths):
    ok_all = True
    for path in paths:
        w, digest = load(path)
        N, a, b, arcs = w["N"], w["a"], w["b"], w["arcs"]
        out, err = check_oriented(N, arcs)
        if err:
            print("FAIL %s: %s" % (path, err))
            ok_all = False
            continue
        full = (1 << N) - 1
        inn = [0] * N
        for u in range(N):
            x = out[u]
            while x:
                v = x.bit_length() - 1
                x &= ~(1 << v)
                inn[v] |= 1 << u
        nonadj = [full & ~(out[u] | inn[u] | (1 << u)) for u in range(N)]
        alpha = independence_number(N, nonadj)
        tau = largest_transitive(N, out)
        ok = alpha <= a - 1 and tau <= b - 1
        ok_all = ok_all and ok
        print("%s %s: N=%d arcs=%d alpha=%d (need <= %d) largest TT=%d (need <= %d)"
              " sha256=%s" % ("PASS" if ok else "FAIL", path, N, len(arcs),
                              alpha, a - 1, tau, b - 1, digest))
        if ok:
            print("     => k(%d,%d) = r(I_%d, L_%d) >= %d" % (a, b, a, b, N + 1))
    return 0 if ok_all else 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
