#!/usr/bin/env python3
"""CNF generator for the oriented Ramsey problem r(I_a, L_b) on N vertices.

Encodes: "there EXISTS an oriented graph on N vertices with no independent set of
size a and no transitive tournament on b vertices".
SAT  -> witness exists       -> r(I_a, L_b) > N
UNSAT-> no witness on N      -> (with SAT at N-1) pins the value.

Pure encoding, no symmetry breaking (soundness of UNSAT certificates depends only
on this encoding; symmetry-broken variants are written by separate flags and used
ONLY for witness search, where any model is independently re-verified anyway).

Variables: vertices 0..N-1. For each unordered pair u<v with pair index p
(lexicographic), arc u->v is variable 2p+1 and arc v->u is variable 2p+2.

Clauses:
  no-2-cycle:      for each pair: (-x_uv | -x_vu)
  no I_a:          for each a-subset S: OR_{u<v in S} (x_uv | x_vu)
  no L_b:          for each b-subset and each of the b! linear orders v1..vb:
                   OR of -x_{vi vj} over i<j  (at least one forward arc missing)

Usage: gen_cnf.py a b N out.cnf [--sb01]
  --sb01: adds the single unit clause x_{0->1}=true (valid symmetry breaking for
          witness search only if some arc exists; for a<=N any I_a-free graph on
          N>=a>=2 vertices has an arc, and vertex/direction relabeling maps it to 0->1
          ... direction symmetry: reversing ALL arcs preserves both properties, so
          fixing the direction of one existing arc is sound for existence questions
          when N >= 2 and the graph must contain at least one arc (true when N >= a).
          Still: used only for SAT-side search, never for UNSAT claims.
"""
import sys
from itertools import combinations, permutations


def var(u, v, N, pair_index):
    if u < v:
        return 2 * pair_index[(u, v)] + 1
    return 2 * pair_index[(v, u)] + 2


def main():
    a = int(sys.argv[1]); b = int(sys.argv[2]); N = int(sys.argv[3]); out = sys.argv[4]
    sb01 = "--sb01" in sys.argv[5:]
    pairs = list(combinations(range(N), 2))
    pair_index = {p: i for i, p in enumerate(pairs)}
    nvars = 2 * len(pairs)
    clauses = []
    # no 2-cycles
    for (u, v) in pairs:
        clauses.append([-var(u, v, N, pair_index), -var(v, u, N, pair_index)])
    # no independent set of size a
    for S in combinations(range(N), a):
        cl = []
        for (u, v) in combinations(S, 2):
            cl.append(var(u, v, N, pair_index))
            cl.append(var(v, u, N, pair_index))
        clauses.append(cl)
    # no transitive tournament of size b
    for S in combinations(range(N), b):
        for order in permutations(S):
            cl = [-var(order[i], order[j], N, pair_index)
                  for i in range(b) for j in range(i + 1, b)]
            clauses.append(cl)
    if sb01:
        clauses.append([var(0, 1, N, pair_index)])
    with open(out, "w") as f:
        f.write("p cnf %d %d\n" % (nvars, len(clauses)))
        for cl in clauses:
            f.write(" ".join(map(str, cl)) + " 0\n")
    print("wrote %s: a=%d b=%d N=%d vars=%d clauses=%d" % (out, a, b, N, nvars, len(clauses)))


if __name__ == "__main__":
    main()
