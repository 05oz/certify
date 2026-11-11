#!/usr/bin/env python3
"""Correct digits of truncated asymptotic forms, measured against the certified enclosures.

Part L addendum (Certify v0.17.0). Python 3 standard library only.  Imports series_terms.py
from its own directory.

For each diagonal entry (Nxx, Nyy, Nzz) of a demag certificate, this evaluates in IEEE-754
double precision the asymptotic series truncated after three terms (1/r^3, 1/r^5, 1/r^7)
and after four terms (adding 1/r^9), and reports a rigorous lower bound on the correct
significant digits of each, -log10( max|v - N| / min|N| ) over N in the certified enclosure.
The three-term form is the one the certificate's asymp_oommf field holds (as transcribed in
the demagderiv notebook); the four-term form is the one OOMMF's demagcoef.cc carries, without
OOMMF's cell subdivision.  Near the double-precision floor (about 16 digits) the last digit
depends on the order of floating-point operations, so values there agree with the stored
asymp_digits only to within a digit or so.

Usage:  python3 four_term_digits.py <certificate.json> [cell direction component]
"""
import json
import math
import os
import sys
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import series_terms as st  # noqa: E402

COMP = {"Nxx": (0, 0), "Nyy": (1, 1), "Nzz": (2, 2)}


def _float_term(t, s2, d2):
    tot = 0.0
    for mono, coef in t.items():
        cv = 0.0
        for k, v in coef.items():
            cv += float(v) * d2[0] ** k[0] * d2[1] ** k[1] * d2[2] ** k[2]
        tot += cv * s2[0] ** (mono[0] // 2) * s2[1] ** (mono[1] // 2) * s2[2] ** (mono[2] // 2)
    return tot


def asymptotic_double(terms, off, d, nterms):
    x, y, z = (float(v) for v in off)
    dx, dy, dz = (float(v) for v in d)
    r2 = x * x + y * y + z * z
    r = math.sqrt(r2)
    s2 = (x * x / r2, y * y / r2, z * z / r2)
    d2 = (dx * dx, dy * dy, dz * dz)
    ts = [_float_term(terms[n], s2, d2) for n in range(nterms)]
    acc = ts[-1]
    for t in reversed(ts[:-1]):
        acc = acc / r2 + t
    return (-dx * dy * dz / (4.0 * math.pi)) * acc / (r2 * r)


def correct_digits(lo, hi, v):
    vv = Fr(v)
    dmax = max(abs(vv - lo), abs(vv - hi))
    nmin = Fr(0) if lo <= 0 <= hi else min(abs(lo), abs(hi))
    if dmax == 0:
        return float("inf")
    return -math.log10(float(dmax / nmin)) if nmin > 0 else float("-inf")


def main(argv):
    cert = json.load(open(argv[1]))
    sel = tuple(argv[2:5]) if len(argv) >= 5 else None
    terms = {c: [st.term(k, comp) for k in range(4)] for c, comp in COMP.items()}
    print("%-14s %-9s %-4s %7s  %7s %7s %7s" % ("cell", "direction", "comp", "n", "naive", "3-term", "4-term"))
    for e in cert["entries"]:
        if e["direction"] == "self" or e["component"] not in COMP:
            continue
        if sel and (e["cell"], e["direction"], e["component"]) != sel:
            continue
        d = tuple(Fr(v) for v in e["cell_dims"])
        off = tuple(Fr(v) for v in e["offset"])
        lo, hi = Fr(e["N_lo"]), Fr(e["N_hi"])
        t = terms[e["component"]]
        naive = float.fromhex(e["naive_double"])
        print("%-14s %-9s %-4s %7d  %7.1f %7.1f %7.1f" % (
            e["cell"], e["direction"], e["component"], e["sep_cells"], correct_digits(lo, hi, naive),
            correct_digits(lo, hi, asymptotic_double(t, off, d, 3)),
            correct_digits(lo, hi, asymptotic_double(t, off, d, 4))))


if __name__ == "__main__":
    if len(sys.argv) not in (2, 5):
        print(__doc__)
        sys.exit(2)
    main(sys.argv)
