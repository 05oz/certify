#!/usr/bin/env python3
"""Independent verifier for a minimizer certificate. Stdlib only.

verify_minimizer.py --n N --value V --bits F --witness F --cnf F --lrat F

Establishes, from raw artifacts only, that the tournament T in the bits file has
maximum arc-disjoint-TT3-packing EXACTLY V:
  (1) lower bound: the witness file holds V pairwise arc-disjoint transitive
      triples of T (checked directly against the bits);
  (2) upper bound: the CNF file is EXACTLY (same clause multiset) this script's
      own regeneration of the spec encoding of "T contains V+1 pairwise
      arc-disjoint TT3s" (spec in encode_cnf.py docstring: conflict clauses on
      lexicographic TT3 variables + Sinz sequential at-most-(m-(V+1)) counter on
      the negations), and the LRAT file is a valid RUP refutation of that CNF
      (checked by this script's own LRAT checker, no external tools).
Soundness of the encoding (any packing of size >= V+1 extends to a satisfying
assignment of the Sinz counter) is a standard property of the sequential-counter
encoding; given that, UNSAT => max <= V.
"""
import argparse
import sys


def pair_index(n, i, j):
    return i * (2 * n - i - 1) // 2 + (j - i - 1)


def beats(bits, n, u, v):
    i, j = (u, v) if u < v else (v, u)
    one = bits[pair_index(n, i, j)] == '1'
    return one if u < v else not one


def tt3_list(bits, n):
    out = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                ij, jk, ki = beats(bits, n, i, j), beats(bits, n, j, k), beats(bits, n, k, i)
                if not ((ij and jk and ki) or (not ij and not jk and not ki)):
                    out.append((i, j, k))
    return out


def regen_encoding(bits, n, k):
    """Regenerate the spec CNF as a list of int-tuples (order irrelevant)."""
    tris = tt3_list(bits, n)
    m = len(tris)
    arcs = [frozenset((pair_index(n, a, b), pair_index(n, b, c), pair_index(n, a, c)))
            for (a, b, c) in tris]
    cls = []
    for s in range(m):
        for t in range(s + 1, m):
            if arcs[s] & arcs[t]:
                cls.append((-(s + 1), -(t + 1)))
    K = m - k
    assert K >= 1

    def S(i, j):
        return m + (i - 1) * K + j
    cls.append((1, S(1, 1)))
    for j in range(2, K + 1):
        cls.append((-S(1, j),))
    for i in range(2, m + 1):
        cls.append((i, S(i, 1)))
        cls.append((-S(i - 1, 1), S(i, 1)))
        for j in range(2, K + 1):
            cls.append((i, -S(i - 1, j - 1), S(i, j)))
            cls.append((-S(i - 1, j), S(i, j)))
        cls.append((i, -S(i - 1, K)))
    return m + m * K, cls, m, tris


def parse_dimacs(fn):
    nvars = ncls = None
    clauses = []
    with open(fn) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('c'):
                continue
            if line.startswith('p'):
                _, _, v, c = line.split()
                nvars, ncls = int(v), int(c)
                continue
            lits = list(map(int, line.split()))
            assert lits[-1] == 0
            clauses.append(tuple(lits[:-1]))
    assert ncls == len(clauses)
    return nvars, clauses


def check_lrat(nvars, clauses, lratfn):
    """RUP-with-hints LRAT check. Returns True iff empty clause derived validly."""
    db = {i + 1: clauses[i] for i in range(len(clauses))}
    empty_ok = False
    with open(lratfn) as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            tok = raw.split()
            cid = int(tok[0])
            if len(tok) >= 2 and tok[1] == 'd':
                for x in tok[2:]:
                    x = int(x)
                    if x == 0:
                        break
                    db.pop(x, None)
                continue
            nums = list(map(int, tok[1:]))
            z1 = nums.index(0)
            lits, hints = nums[:z1], nums[z1 + 1:]
            assert hints and hints[-1] == 0
            hints = hints[:-1]
            # RUP check: assume negation of lits, propagate hint clauses in order
            assign = {}
            for l in lits:
                assign[-l] = True
                assign[l] = False
            conflict = False
            for h in hints:
                if h < 0:
                    return False  # RAT step: not produced by cadical, reject
                cl = db.get(h)
                if cl is None:
                    return False
                unassigned = None
                sat = False
                for l in cl:
                    v = assign.get(l)
                    if v is True:
                        sat = True
                        break
                    if v is None:
                        if unassigned is not None:
                            unassigned = 'many'
                        else:
                            unassigned = l
                if sat:
                    return False  # hint clause satisfied: not a proper RUP hint
                if unassigned is None:
                    conflict = True
                    break
                if unassigned == 'many':
                    return False  # hint clause not unit: invalid hint sequence
                assign[unassigned] = True
                assign[-unassigned] = False
            if not conflict:
                return False
            db[cid] = tuple(lits)
            if not lits:
                empty_ok = True
    return empty_ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, required=True)
    ap.add_argument('--value', type=int, required=True)
    ap.add_argument('--bits', required=True)
    ap.add_argument('--witness', required=True)
    ap.add_argument('--cnf', required=True)
    ap.add_argument('--lrat', required=True)
    a = ap.parse_args()
    n, V = a.n, a.value
    bits = open(a.bits).read().split()[0]
    assert len(bits) == n * (n - 1) // 2 and set(bits) <= {'0', '1'}

    # (1) lower bound: witness of V arc-disjoint TT3s
    wtxt = open(a.witness).read().split()
    # witness file format: "MAX <k> <t;t;...>" or just "<t;t;...>"
    wit = wtxt[-1]
    triples = [tuple(map(int, t.split(','))) for t in wit.split(';')]
    assert len(triples) == V, f"witness has {len(triples)} triples, want {V}"
    used = set()
    for (x, y, z) in triples:
        assert 0 <= x < y < z < n
        xy, yz, zx = beats(bits, n, x, y), beats(bits, n, y, z), beats(bits, n, z, x)
        assert not ((xy and yz and zx) or (not xy and not yz and not zx)), \
            f"triple {(x,y,z)} is cyclic"
        for e in ((x, y), (y, z), (x, z)):
            assert e not in used, f"arc {e} reused"
            used.add(e)
    print(f"lower bound OK: {V} pairwise arc-disjoint transitive triples verified")

    # (2) upper bound: CNF matches spec encoding for V+1, LRAT refutes it
    nvars_r, cls_r, m, _ = regen_encoding(bits, n, V + 1)
    nvars_f, cls_f = parse_dimacs(a.cnf)
    assert nvars_f == nvars_r, f"nvars {nvars_f} != regenerated {nvars_r}"
    assert sorted(cls_f) == sorted(cls_r), "CNF clause multiset != regenerated spec encoding"
    print(f"CNF match OK: {len(cls_f)} clauses == independent regeneration "
          f"(m={m} TT3s, k={V+1})")
    ok = check_lrat(nvars_f, cls_f, a.lrat)
    assert ok, "LRAT check FAILED"
    print(f"LRAT OK: empty clause derived; UNSAT verified => max packing <= {V}")
    print(f"VERIFIED: tournament {bits} has maximum TT3-packing EXACTLY {V}")


if __name__ == '__main__':
    main()
