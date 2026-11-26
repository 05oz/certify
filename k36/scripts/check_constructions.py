#!/usr/bin/env python3
"""Rebuild the three witness graphs from the constructions stated in note.md
(section 3) and compare them with the certificate files.

Standard library only. No network. Reads the three JSON files, writes nothing.

Usage:  python3 check_constructions.py [CERT_DIR]
CERT_DIR defaults to ../certificates next to this script.
Exit status 0 iff every check passes.

Checks for each file:
  1. N, a, b and the connection sets stored in the file equal the ones
     written below, which are the ones printed in note.md.
  2. The arc list has no repeated arc and, as a set, equals the arc set
     rebuilt from the construction.
  3. The construction gives an oriented graph (no loop, no 2-cycle); this is
     checked on the connection sets themselves.
  4. One condition a reader can check by hand from the connection sets:
     - the two bicirculants on Z_q x {0,1}: there is no transitive triangle
       iff (S_ab + S_bc) and S_ac are disjoint mod q for all a, b, c in {0,1};
     - the Cayley digraph on G = Z_24 x Z_3: there is no independent 3-set
       iff T = G minus (S, -S and 0) is sum-free (no t1, t2 in T with
       t1 + t2 in T, t1 = t2 allowed).
  5. Every vertex has the stated out-degree and in-degree.

Not recomputed here: the independence number of the two bicirculants and the
largest transitive subtournament of the Cayley digraph. verify_bounds.py and
Part G's verify_witness.py compute those.
"""
import hashlib
import json
import os
import sys
import time

# The constructions, as printed in note.md section 3. Vertex (i, a) of a
# bicirculant is numbered a*q + i; arc (i, a) -> (i + d mod q, b) iff d in S_ab.
BICIRCULANTS = [
    ("k73_N38.json", {"N": 38, "a": 7, "b": 3, "q": 19, "deg": 6,
                      "S": {"S00": [8, 12, 13, 17], "S01": [2, 6],
                            "S10": [1, 5], "S11": [8, 12, 14, 18]}}),
    ("k83_N46.json", {"N": 46, "a": 8, "b": 3, "q": 23, "deg": 7,
                      "S": {"S00": [1, 3, 11, 18], "S01": [6, 14, 16],
                            "S10": [6, 14, 16], "S11": [1, 3, 11, 16]}}),
]
# Element (x, y) of Z_24 x Z_3 is numbered 3*x + y; arc g -> g + s for s in S.
CAYLEY = [
    ("k36_N72.json", {"N": 72, "a": 3, "b": 6, "mod": (24, 3), "deg": 25,
                      "S": [(0, 2), (2, 0), (2, 1), (2, 2), (3, 0), (5, 1),
                            (6, 1), (6, 2), (8, 0), (8, 1), (9, 2), (10, 0),
                            (10, 1), (11, 0), (11, 1), (11, 2), (12, 2),
                            (14, 1), (15, 2), (16, 1), (18, 0), (19, 0),
                            (19, 1), (21, 1), (21, 2)]}),
]

failures = []


def check(ok, label):
    print("  %s  %s" % ("ok  " if ok else "FAIL", label))
    if not ok:
        failures.append(label)
    return ok


def load(path):
    raw = open(path, "rb").read()
    return json.loads(raw.decode("utf-8")), hashlib.sha256(raw).hexdigest()


def file_arcs(w, name):
    arcs = []
    for pair in w["arcs"]:
        good = (isinstance(pair, list) and len(pair) == 2
                and type(pair[0]) is int and type(pair[1]) is int)
        if not good:
            check(False, "%s: arc %r is not a pair of integers" % (name, pair))
            return None
        arcs.append((pair[0], pair[1]))
    check(len(arcs) == len(set(arcs)), "%s: no repeated arc in the file" % name)
    return set(arcs)


def degrees_ok(N, arcs, deg, name):
    out = [0] * N
    inn = [0] * N
    for u, v in arcs:
        out[u] += 1
        inn[v] += 1
    check(all(x == deg for x in out) and all(x == deg for x in inn),
          "%s: every vertex has out-degree %d and in-degree %d" % (name, deg, deg))


def check_bicirculant(name, spec, w):
    q, S = spec["q"], spec["S"]
    N = 2 * q
    print("%s: claim: the file is the Z_%d bicirculant with S00=%s S01=%s "
          "S10=%s S11=%s, and it has no transitive triangle"
          % (name, q, S["S00"], S["S01"], S["S10"], S["S11"]))
    check((w["N"], w["a"], w["b"]) == (spec["N"], spec["a"], spec["b"]),
          "%s: N, a, b in the file are %d, %d, %d"
          % (name, spec["N"], spec["a"], spec["b"]))
    stored = w.get("connection_sets", {})
    check(all(sorted(stored.get(k, [])) == sorted(v) for k, v in S.items())
          and sorted(stored) == sorted(S),
          "%s: connection sets stored in the file equal the note's" % name)
    sets = {}
    for a in (0, 1):
        for b in (0, 1):
            vals = S["S%d%d" % (a, b)]
            check(len(set(x % q for x in vals)) == len(vals),
                  "%s: S%d%d has distinct residues mod %d" % (name, a, b, q))
            sets[(a, b)] = set(x % q for x in vals)
    neg = lambda X: set((-x) % q for x in X)
    check(0 not in sets[(0, 0)] and 0 not in sets[(1, 1)],
          "%s: no loop (0 is in neither S00 nor S11)" % name)
    check(not (sets[(0, 0)] & neg(sets[(0, 0)]))
          and not (sets[(1, 1)] & neg(sets[(1, 1)]))
          and not (sets[(0, 1)] & neg(sets[(1, 0)])),
          "%s: no 2-cycle (S00, S11 meet their negatives nowhere; "
          "S01 and -S10 are disjoint)" % name)
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                sums = set((x + y) % q for x in sets[(a, b)] for y in sets[(b, c)])
                check(not (sums & sets[(a, c)]),
                      "%s: (S%d%d + S%d%d) and S%d%d are disjoint mod %d"
                      % (name, a, b, b, c, a, c, q))
    rebuilt = set()
    for a in (0, 1):
        for b in (0, 1):
            for i in range(q):
                for d in sets[(a, b)]:
                    rebuilt.add((a * q + i, b * q + (i + d) % q))
    arcs = file_arcs(w, name)
    if arcs is not None:
        check(arcs == rebuilt,
              "%s: arc set in the file equals the rebuilt arc set (%d arcs)"
              % (name, len(rebuilt)))
        degrees_ok(N, rebuilt, spec["deg"], name)


def check_cayley(name, spec, w):
    m0, m1 = spec["mod"]
    S = [(x % m0, y % m1) for (x, y) in spec["S"]]
    N = m0 * m1
    print("%s: claim: the file is Cay(Z_%d x Z_%d, S) with |S| = %d, and it has "
          "no independent 3-set" % (name, m0, m1, len(S)))
    check((w["N"], w["a"], w["b"]) == (spec["N"], spec["a"], spec["b"]),
          "%s: N, a, b in the file are %d, %d, %d"
          % (name, spec["N"], spec["a"], spec["b"]))
    stored = sorted(tuple(p) for p in w.get("S", []))
    check(stored == sorted(spec["S"]),
          "%s: connection set stored in the file equals the note's" % name)
    Sset = set(S)
    check(len(Sset) == len(S), "%s: the %d elements of S are distinct"
          % (name, len(S)))
    neg = lambda g: ((-g[0]) % m0, (-g[1]) % m1)
    add = lambda g, h: ((g[0] + h[0]) % m0, (g[1] + h[1]) % m1)
    check((0, 0) not in Sset, "%s: no loop (0 is not in S)" % name)
    check(not any(neg(s) in Sset for s in S),
          "%s: no 2-cycle (S and -S are disjoint)" % name)
    G = [(x, y) for x in range(m0) for y in range(m1)]
    T = [g for g in G if g != (0, 0) and g not in Sset and neg(g) not in Sset]
    Tset = set(T)
    check(len(T) == N - 1 - 2 * len(S),
          "%s: T = G minus (S, -S, 0) has %d elements" % (name, len(T)))
    bad = [(t1, t2) for t1 in T for t2 in T if add(t1, t2) in Tset]
    check(not bad, "%s: T is sum-free, so no independent 3-set" % name)
    rebuilt = set()
    for g in G:
        for s in S:
            h = add(g, s)
            rebuilt.add((m1 * g[0] + g[1], m1 * h[0] + h[1]))
    arcs = file_arcs(w, name)
    if arcs is not None:
        check(arcs == rebuilt,
              "%s: arc set in the file equals the rebuilt arc set (%d arcs)"
              % (name, len(rebuilt)))
        degrees_ok(N, rebuilt, spec["deg"], name)


def main(argv):
    t0 = time.time()
    here = os.path.dirname(os.path.abspath(__file__))
    cdir = argv[1] if len(argv) > 1 else os.path.join(here, os.pardir, "certificates")
    for name, spec in BICIRCULANTS:
        w, digest = load(os.path.join(cdir, name))
        print("%s sha256=%s" % (name, digest))
        check_bicirculant(name, spec, w)
    for name, spec in CAYLEY:
        w, digest = load(os.path.join(cdir, name))
        print("%s sha256=%s" % (name, digest))
        check_cayley(name, spec, w)
    dt = time.time() - t0
    if failures:
        print("FAIL: %d check(s) failed (%.2f s)" % (len(failures), dt))
        return 1
    print("PASS: all three files equal the constructions stated in note.md (%.2f s)" % dt)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
