#!/usr/bin/env python3
"""Independent anchor check for Part K (certified demag tensor).

Standard library only.  Re-derives the certified interval Newell tensor at the
16 geometries for which OOMMF's demagcoef.cc records Maple-computed 50-digit
values, and verifies that each gold value agrees with the recomputed enclosure
midpoint to >= 48 digits (the gold's own precision).  This exercises the SHIPPED
checker's own Newell/interval code (check_demag.py) against an external gold
standard, with no dependence on the private generator.

(Containment is not the test: the recomputed enclosure is ~77 digits tight at
PREC=256, far tighter than the 50-digit gold, so a gold value cannot lie inside
it.  Agreement to the gold's precision is the correct consistency check.  The
enclosure is separately verified by the two-sided-bound machinery in
check_demag.py.)

Usage:  python3 anchor_check.py
(run from demag-scripts/ with demag-certificates/ alongside, or set the path)
"""
import os
import sys
from fractions import Fraction as Fr

# locate the shipped checker (demag-certificates/check_demag.py)
_here = os.path.dirname(os.path.abspath(__file__))
for cand in (os.path.join(_here, "..", "demag-certificates"), _here,
             os.path.join(_here, "..", "certificates")):
    if os.path.exists(os.path.join(cand, "check_demag.py")):
        sys.path.insert(0, cand)
        break
from check_demag import CIV, Newell  # noqa: E402

PREC = 256
civ = CIV(PREC)
nw = Newell(civ)

# OOMMF demagcoef.cc header: (x,y,z,dx,dy,dz, comp, Maple 50-digit value)
GOLD = [
    (0, 0, 0, 50, 10, 1, "Nxx", "0.021829576458713811627717362556500594396802771830582"),
    (0, 0, 0, 1, 1, 1, "Nxx", "0.33333333333333333333333333333333333333333333333333"),
    (0, 0, 0, 1, 1, 2, "Nxx", "0.40084192360558096752690050789034014000452668298259"),
    (0, 0, 0, 2, 1, 1, "Nxx", "0.19831615278883806494619898421931971999094663403481"),
    (0, 0, 0, 1, 2, 3, "Nxx", "0.53879030592371444784959040590642585972177691027128"),
    (1, 0, 0, 1, 1, 1, "Nxx", "-0.13501718054449526838713434911401361334238669929852"),
    (0, 1, 0, 1, 1, 1, "Nxx", "0.067508590272247634193567174557006806671193349649259"),
    (1, 1, 0, 1, 2, 3, "Nxx", "-0.083703755298020462084677435631518487669613050161980"),
    (1, 1, 1, 1, 1, 1, "Nxx", "0"),
    (1, 2, 3, 1, 2, 3, "Nxx", "0.0074263570277919738841364667668809954237071479183522"),
    (10, 4, 6, 1, 2, 3, "Nxx", "-0.00025381260722622800624859078080421562302790329870984"),
    (6, 6, 6, 1, 2, 3, "Nxx", "-0.000017252712652486259473939673630209925239022411008957"),
    (1, 1, 0, 1, 2, 3, "Nxy", "-0.077258075615212400146921495217230818857603260305042"),
    (1, 1, 1, 1, 1, 1, "Nxy", "-0.016062127810508233979724830686189874772059681376565"),
    (1, 2, 3, 1, 2, 3, "Nxy", "-0.0088226536707711039322880437795490754270432698781039"),
    (6, 6, 6, 1, 2, 3, "Nxy", "-0.00043908646098482886546108269881031774163900540796564"),
]


def dec_to_fr(s):
    s = s.strip()
    neg = s.startswith("-")
    s = s.lstrip("+-")
    if "." in s:
        i, f = s.split(".")
    else:
        i, f = s, ""
    val = Fr(int(i + f) if (i + f) else 0, 10 ** len(f))
    return -val if neg else val


def main():
    worst = 999.0
    fails = 0
    for x, y, z, dx, dy, dz, comp, gold in GOLD:
        lo, hi = nw.comp(comp, x, y, z, dx, dy, dz)
        g = dec_to_fr(gold)
        mid = (lo + hi) / 2
        # digits of agreement between gold and enclosure midpoint
        if g == 0:
            agree = 99 if abs(mid) < Fr(1, 10 ** 40) else 0
        else:
            rel = abs(mid - g) / abs(g)
            agree = 99 if rel == 0 else _neglog10(rel)
        worst = min(worst, agree)
        if agree < 48:
            fails += 1
            print("ANCHOR FAIL %s(%d,%d,%d;%d,%d,%d): agree=%.1f digits"
                  % (comp, x, y, z, dx, dy, dz, agree))
    if fails:
        print("ANCHOR CHECK FAILED: %d/%d" % (fails, len(GOLD)))
        sys.exit(1)
    print("all %d OOMMF/Maple gold values agree with recomputed enclosure "
          "midpoints to at least %.1f digits" % (len(GOLD), worst))
    print("ANCHOR CHECK PASS")


def _neglog10(fr):
    # -log10 of a positive Fraction, via integer bit lengths (stdlib only)
    import math
    return -math.log10(fr.numerator / fr.denominator) if fr.numerator else 99.0


if __name__ == "__main__":
    main()
