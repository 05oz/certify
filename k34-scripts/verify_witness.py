#!/usr/bin/env python3
"""INDEPENDENT witness verifier for r(I_a, L_b) lower-bound witnesses.

Deliberately shares no code with gen_cnf.py and uses a DIFFERENT criterion for
transitive tournaments: a b-subset is a TT_b iff (all pairs adjacent) and (the
out-degree multiset inside the subset is exactly {0,1,...,b-1}). [A tournament is
transitive iff its score sequence is 0,1,...,b-1.] The generator instead
enumerates linear orders. Stdlib only.

Witness file format (JSON): {"N": int, "a": int, "b": int,
  "arcs": [[u,v], ...]}   meaning arc u->v.
Exit 0 and print PASS iff the witness is a valid {I_a, L_b}-free oriented graph.
"""
import json, sys
from itertools import combinations


def main(path):
    w = json.load(open(path))
    N, a, b = w["N"], w["a"], w["b"]
    arcs = set()
    for u, v in w["arcs"]:
        if not (0 <= u < N and 0 <= v < N):
            print("FAIL: arc (%d,%d) out of range" % (u, v)); return 1
        if u == v:
            print("FAIL: loop at %d" % u); return 1
        if (v, u) in arcs:
            print("FAIL: 2-cycle on (%d,%d)" % (u, v)); return 1
        arcs.add((u, v))
    adj = {(u, v) for (u, v) in arcs} | {(v, u) for (u, v) in arcs}

    # independent sets of size a
    for S in combinations(range(N), a):
        if all((u, v) not in adj for u, v in combinations(S, 2)):
            print("FAIL: independent set %s" % (S,)); return 1

    # transitive tournaments of size b
    for S in combinations(range(N), b):
        if all((u, v) in adj for u, v in combinations(S, 2)):
            scores = sorted(sum(1 for v in S if (u, v) in arcs) for u in S)
            if scores == list(range(b)):
                print("FAIL: transitive tournament %s" % (S,)); return 1
    print("PASS: N=%d graph with %d arcs is {I_%d, L_%d}-free -> r(I_%d,L_%d) >= %d"
          % (N, len(arcs), a, b, a, b, N + 1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
