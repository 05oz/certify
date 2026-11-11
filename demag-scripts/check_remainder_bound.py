#!/usr/bin/env python3
"""Check the Part L remainder bound against every certified entry of a demag certificate.

Part L addendum (Certify v0.17.0). Python 3 standard library only; no signals, subprocesses,
network or wall-clock.  Imports series_terms.py from its own directory.

Two identical axis-parallel cells, edges (dx, dy, dz), volume V, centre offset R, cell
diagonal D = sqrt(dx^2 + dy^2 + dz^2).  For R > D, every component, every odd n >= 3, and
the exact series truncated at error order n (terms through 1/R^(n-2) kept), the note proves

  (shape-free)   |N - S_n| <= V D^(n-3) / ( 2 pi R^(n-2) (R^2 - D^2) )
  (with shape)   |N - S_n| <= (V/4pi) [ (n-2)(n-1) E|u|^(n-3) / R^n + 2 D^(n-1) / ( R^n (R^2 - D^2) ) ]

This script tests both at n = 5, 7, 9, 11 on every entry with R > D, in exact rational
arithmetic: pi and R are replaced by rational brackets on the safe side, N may be anywhere in
the certified [N_lo, N_hi], and the largest possible error is compared with the smallest
possible bound.  It also checks the moment inequality (n-2)(n-1) E|u|^(n-3) <= 2 D^(n-3)
for every cell in the certificate.  The proof is in section 8 of the note.

Usage:  python3 check_remainder_bound.py <demag_certificate.json>
Exit code 0 and a final line "BOUND CHECK PASS" iff no comparison fails.
"""
import json
import math
import os
import sys
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import series_terms as st  # noqa: E402

DIG = 60
PI_LO = Fr(3141592653589793238462643383279502884197169399375105820974944, 10 ** DIG)
PI_HI = PI_LO + Fr(1, 10 ** DIG)          # pi lies in [PI_LO, PI_HI]


def sqrt_bracket(q):
    p, d = q.numerator, q.denominator
    m = math.isqrt(p * d * 10 ** (2 * DIG))
    return Fr(m, d * 10 ** DIG), Fr(m + 1, d * 10 ** DIG)


COMP = {"Nxx": (0, 0), "Nyy": (1, 1), "Nzz": (2, 2), "Nxy": (0, 1), "Nxz": (0, 2), "Nyz": (1, 2)}
ORDERS = (5, 7, 9, 11)


def main(path):
    cert = json.load(open(path))
    terms = {c: [st.term(k, comp) for k in range(4)] for c, comp in COMP.items()}
    worst = {(f, n): (Fr(0), None) for f in ("shape-free", "with shape") for n in ORDERS}
    fails = 0; tested = 0; skipped = 0
    cells = {}
    for e in cert["entries"]:
        if e["direction"] == "self":
            continue
        d = tuple(Fr(v) for v in e["cell_dims"]); off = tuple(Fr(v) for v in e["offset"])
        R2 = sum(v * v for v in off); D2 = sum(v * v for v in d)
        if not R2 > D2:
            skipped += 1
            continue
        tested += 1
        cells[e["cell"]] = d
        R_lo, R_hi = sqrt_bracket(R2)
        V = d[0] * d[1] * d[2]
        N_lo, N_hi = Fr(e["N_lo"]), Fr(e["N_hi"])
        Q = Fr(0)
        for idx, n in enumerate(ORDERS):
            Q += st.value(terms[e["component"]][idx], off, d) / R2 ** (idx + 1)
            a = -(V / 4) * Q / (PI_LO * R_lo); b = -(V / 4) * Q / (PI_HI * R_hi)
            S_lo, S_hi = min(a, b), max(a, b)
            err = max(abs(N_lo - S_hi), abs(N_hi - S_lo))          # largest possible |N - S_n|
            k = n - 3
            Rn = R2 ** ((n - 1) // 2) * R_hi                        # upper bracket of R^n
            Rn2 = R2 ** ((n - 3) // 2) * R_hi                       # upper bracket of R^(n-2)
            free = V * D2 ** (k // 2) / (2 * PI_HI * Rn2 * (R2 - D2))
            shape = V / (4 * PI_HI) * ((n - 2) * (n - 1) * st.moment(k, d) / Rn + 2 * D2 ** ((n - 1) // 2) / (Rn * (R2 - D2)))
            for form, bound in (("shape-free", free), ("with shape", shape)):
                ratio = err / bound
                if ratio > 1:
                    fails += 1
                    print("FAIL %s n=%d at %s %s %s" % (form, n, e["cell"], e["direction"], e["sep_cells"]))
                if ratio > worst[(form, n)][0]:
                    worst[(form, n)] = (ratio, "%s %s n_cells=%s %s" % (e["cell"], e["direction"], e["sep_cells"], e["component"]))
    mom_fail = 0
    for name, d in cells.items():
        D2 = sum(v * v for v in d)
        for n in ORDERS:
            k = n - 3
            if (n - 2) * (n - 1) * st.moment(k, d) > 2 * D2 ** (k // 2):
                mom_fail += 1
                print("FAIL moment inequality at %s, n=%d" % (name, n))
    print("certificate: %s (%d entries); tested %d with R > D; skipped %d with R <= D; self-terms excluded"
          % (os.path.basename(path), len(cert["entries"]), tested, skipped))
    for form in ("shape-free", "with shape"):
        for n in ORDERS:
            r, where = worst[(form, n)]
            print("  %-10s n=%2d  largest error/bound %.6f  (%s)" % (form, n, float(r), where))
    print("  moment inequality checked for %d cells x %d orders: %d failures" % (len(cells), len(ORDERS), mom_fail))
    if fails or mom_fail:
        print("BOUND CHECK FAIL")
        sys.exit(1)
    print("BOUND CHECK PASS")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1])
