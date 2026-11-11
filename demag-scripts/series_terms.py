#!/usr/bin/env python3
"""Asymptotic series of the Newell demagnetization tensor, to any order, in exact arithmetic.

Part L addendum (Certify v0.17.0). Python 3 standard library only.

Two identical rectangular cells with edges (dx, dy, dz), volume V = dx dy dz, centre offset
r = (x, y, z), r = |r|, unit direction s = r/r.  For r larger than the cell diagonal,

    N_ij(r) = -(V/4 pi) * sum_{n >= 0} term_(2n+3)(s) / r^(2n+3),

    term_(2n+3)(s) = sum_{a+b+c=n} E[ux^2a] E[uy^2b] E[uz^2c] / ((2a)!(2b)!(2c)!) * P_alpha(s),

where u = (ux, uy, uz) is the difference of two independent uniform points of the cell (each
coordinate has the triangular law on [-d, d], so E[u^2m] = 2 d^2m / ((2m+1)(2m+2))),
alpha = e_i + e_j + (2a, 2b, 2c), and d^alpha (1/r) = P_alpha(x, y, z) / r^(2|alpha|+1).
term3, term5, term7 and term9 of N_xx and N_xy equal the coefficients OOMMF's demagcoef.cc
carries (a1..a6, b1..b10, c1..c15 for Nxx; c1..c10 over 64 for Nxy).  This file computes the
series; certification rests on the certificates and their checkers.

Usage:  python3 series_terms.py            (self-test, then prints term9 of Nxx)
"""
import math
import sys
from fractions import Fraction as Fr


def _padd(p, q, c=1):
    out = dict(p)
    for k, v in q.items():
        out[k] = out.get(k, 0) + c * v
        if out[k] == 0:
            del out[k]
    return out


def _pdiff(p, var):
    out = {}
    for k, v in p.items():
        if k[var] > 0:
            kk = list(k); kk[var] -= 1
            out[tuple(kk)] = out.get(tuple(kk), 0) + v * k[var]
    return out


def _pmul(p, q):
    out = {}
    for k1, v1 in p.items():
        for k2, v2 in q.items():
            k = (k1[0] + k2[0], k1[1] + k2[1], k1[2] + k2[2])
            out[k] = out.get(k, 0) + v1 * v2
    return {k: v for k, v in out.items() if v != 0}


_R2 = {(2, 0, 0): Fr(1), (0, 2, 0): Fr(1), (0, 0, 2): Fr(1)}
_cache = {(0, 0, 0): {(0, 0, 0): Fr(1)}}


def derivative_numerator(alpha):
    """P_alpha with d^alpha (1/r) = P_alpha / r^(2|alpha|+1), as {(i,j,k): coefficient}."""
    alpha = tuple(alpha)
    if alpha in _cache:
        return _cache[alpha]
    var = next(i for i in range(3) if alpha[i] > 0)
    prev = list(alpha); prev[var] -= 1
    q = derivative_numerator(prev)
    m = sum(prev)
    mono = [0, 0, 0]; mono[var] = 1
    shifted = {(k[0] + mono[0], k[1] + mono[1], k[2] + mono[2]): v for k, v in q.items()}
    res = _padd(_pmul(_R2, _pdiff(q, var)), shifted, -(2 * m + 1))
    _cache[alpha] = res
    return res


def triangular_moment(a):
    """E[u^(2a)] / d^(2a) for the triangular law on [-d, d]."""
    return Fr(2, (2 * a + 1) * (2 * a + 2))


def term(n, comp=(0, 0)):
    """term_(2n+3) of component comp = (i, j): {(direction exponents): {(a, b, c): coefficient}},
    where the inner key gives the powers dx^(2a) dy^(2b) dz^(2c)."""
    out = {}
    for a in range(n + 1):
        for b in range(n + 1 - a):
            c = n - a - b
            w = (triangular_moment(a) * triangular_moment(b) * triangular_moment(c)
                 / (math.factorial(2 * a) * math.factorial(2 * b) * math.factorial(2 * c)))
            alpha = [2 * a, 2 * b, 2 * c]
            alpha[comp[0]] += 1; alpha[comp[1]] += 1
            for mono, v in derivative_numerator(alpha).items():
                d = out.setdefault(mono, {})
                d[(a, b, c)] = d.get((a, b, c), 0) + w * v
    return {m: {k: v for k, v in d.items() if v != 0} for m, d in out.items()
            if any(v != 0 for v in d.values())}


def value(t, s, d):
    """term t at direction s (any nonzero rational vector; normalised here) and cell d, exactly."""
    s2 = sum(Fr(v) * Fr(v) for v in s)
    tot = Fr(0); deg = None
    for mono, coef in t.items():
        deg = sum(mono)
        cv = sum(v * Fr(d[0]) ** (2 * k[0]) * Fr(d[1]) ** (2 * k[1]) * Fr(d[2]) ** (2 * k[2])
                 for k, v in coef.items())
        tot += cv * Fr(s[0]) ** mono[0] * Fr(s[1]) ** mono[1] * Fr(s[2]) ** mono[2]
    if deg is None:
        return Fr(0)
    return tot / s2 ** (deg // 2)


def moment(k, d):
    """E|u|^k for even k, exactly."""
    h = k // 2
    tot = Fr(0)
    for a in range(h + 1):
        for b in range(h + 1 - a):
            c = h - a - b
            multin = Fr(math.factorial(h), math.factorial(a) * math.factorial(b) * math.factorial(c))
            tot += (multin * triangular_moment(a) * Fr(d[0]) ** (2 * a) * triangular_moment(b)
                    * Fr(d[1]) ** (2 * b) * triangular_moment(c) * Fr(d[2]) ** (2 * c))
    return tot


def _selftest():
    ok = True
    # trace-free for every order (r != 0)
    for n in range(5):
        for s, d in (((3, 5, 7), (1, Fr(13, 10), Fr(1, 10))), ((1, 1, 1), (2, 1, 1))):
            tr = sum(value(term(n, (i, i)), s, d) for i in range(3))
            ok &= (tr == 0)
    # the 1/r^5 term vanishes for a cube, in every direction tested
    for s in ((1, 0, 0), (3, 5, 7), (1, 1, 1)):
        ok &= value(term(1, (0, 0)), s, (1, 1, 1)) == 0
    # cube on axis: term3 = 2, term9 = 1/6 for Nxx and -1/12 for Nyy
    ok &= value(term(0, (0, 0)), (1, 0, 0), (1, 1, 1)) == 2
    ok &= value(term(3, (0, 0)), (1, 0, 0), (1, 1, 1)) == Fr(1, 6)
    ok &= value(term(3, (1, 1)), (1, 0, 0), (1, 1, 1)) == Fr(-1, 12)
    # term9 of Nxx: 15 direction monomials, 150 nonzero coefficients over 192
    t9 = term(3, (0, 0))
    ok &= len(t9) == 15 and sum(len(c) for c in t9.values()) == 150
    ok &= all((192 * v).denominator == 1 for c in t9.values() for v in c.values())
    # moments: E|u|^6 = (dx^6+dy^6+dz^6)/28 + (sum_{i!=j} di^4 dj^2)/30 + dx^2 dy^2 dz^2/36
    for d in ((1, 1, 1), (2, 3, 5), (1, Fr(13, 10), Fr(1, 10))):
        X, Y, Z = (Fr(v) ** 2 for v in d)
        m6 = (X**3 + Y**3 + Z**3) / 28 + (X*X*Y + X*X*Z + Y*Y*X + Y*Y*Z + Z*Z*X + Z*Z*Y) / 30 + X*Y*Z / 36
        ok &= moment(6, d) == m6
    return ok


if __name__ == "__main__":
    if not _selftest():
        print("SELFTEST FAIL")
        sys.exit(1)
    print("SELFTEST PASS")
    t9 = term(3, (0, 0))
    print("term9 of Nxx = (1/192) * sum over direction monomials sx^i sy^j sz^k of:")
    for mono in sorted(t9, reverse=True):
        parts = " ".join("%+d dx^%d dy^%d dz^%d" % (int(192 * v), 2 * k[0], 2 * k[1], 2 * k[2])
                         for k, v in sorted(t9[mono].items(), reverse=True))
        print("  sx^%d sy^%d sz^%d : %s" % (mono[0], mono[1], mono[2], parts))
