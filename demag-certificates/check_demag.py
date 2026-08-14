#!/usr/bin/env python3
"""Checker for the certified Newell demagnetization-tensor reference table.

PUBLISHABLE ARTIFACT.  Python 3 standard library only; OS-independent; no
signals, no subprocesses, no network, no wall-clock.  It recomputes every
certified enclosure from the certificate alone.  NOT independent of the private
generator: 212 of 558 executable lines are verbatim from it, the naive-double
Newell block almost entirely, so a passing check is not an independent
re-derivation of the formulas.  What is original: the consistency identities at
642-670, the comparisons, and the failure paths.  Fails loudly on any mismatch.

Usage:  python3 check_demag.py demag_certificate.json [--sample K]

What is re-verified, from scratch, for every entry:
  1. entries_sha256 over the canonical serialization of the entry list.
  2. The certified two-sided enclosure [N_lo, N_hi] of the Newell tensor
     entry, recomputed by this file's own certified interval arithmetic at
     the certificate's stated precision, and compared as exact rationals.
     Every interval operation rounds OUTWARD, so the recomputed [c_lo, c_hi]
     rigorously encloses the true analytic value; agreement pins the claim
     N_lo <= N_true <= N_hi.
  3. The naive IEEE-754 double evaluation of the same closed form, recomputed
     and compared bit-for-bit (via float.hex()).
  4. The rigorous correct-significant-digit brackets for the naive double
     value (and the OOMMF asymptotic value, where present), recomputed from
     the enclosure.
Exit code 0 and a final line "CHECK PASS" iff every re-derivation agrees.
"""
import sys
import json
import math
import hashlib
from fractions import Fraction as Fr


def fail(msg):
    print("CHECK FAIL: %s" % msg)
    sys.exit(1)


# ===========================================================================
# Certified interval arithmetic over dyadic-rational endpoints
# ===========================================================================
class CIV:
    def __init__(self, PREC):
        self.PREC = PREC
        self.D = 1 << PREC
        self.TAILEPS = Fr(1, self.D << 8)
        self.NT_MAX = 4 * PREC
        self.LOG2 = self._log2()
        self.PI = self._pi()
        self.SQRT2 = self.sqrt_rat(Fr(2))
        l1s2 = self.log_iv(self.iadd(self.iconst(1), self.SQRT2))
        self.K = (self._rd(2 * self.SQRT2[0] - 6 * l1s2[1], "d"),
                  self._rd(2 * self.SQRT2[1] - 6 * l1s2[0], "u"))

    # ---- outward rounding to grid 2**PREC ----
    def _rd(self, x, dirn):
        n = x.numerator * self.D
        d = x.denominator
        q = n // d if d > 0 else -((-n) // d)
        lo = Fr(q, self.D)
        if dirn == "d":
            return lo
        return lo if lo == x else lo + Fr(1, self.D)

    def iconst(self, c):
        c = c if isinstance(c, Fr) else Fr(c)
        return (self._rd(c, "d"), self._rd(c, "u"))

    def iadd(self, a, b):
        return (self._rd(a[0] + b[0], "d"), self._rd(a[1] + b[1], "u"))

    def isub(self, a, b):
        return (self._rd(a[0] - b[1], "d"), self._rd(a[1] - b[0], "u"))

    def imul(self, a, b):
        p = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
        return (self._rd(min(p), "d"), self._rd(max(p), "u"))

    def idiv(self, a, b):
        if b[0] <= 0 <= b[1]:
            raise ZeroDivisionError
        p = (a[0] / b[0], a[0] / b[1], a[1] / b[0], a[1] / b[1])
        return (self._rd(min(p), "d"), self._rd(max(p), "u"))

    def scale(self, a, c):
        c = c if isinstance(c, Fr) else Fr(c)
        if c >= 0:
            return (self._rd(a[0] * c, "d"), self._rd(a[1] * c, "u"))
        return (self._rd(a[1] * c, "d"), self._rd(a[0] * c, "u"))

    # ---- integer sqrt ----
    @staticmethod
    def _isqrt(n):
        if n < 0:
            raise ValueError
        if n == 0:
            return 0
        x = 1 << ((n.bit_length() + 1) // 2)
        while True:
            y = (x + n // x) >> 1
            if y >= x:
                return x
            x = y

    def sqrt_rat(self, q):
        q = q if isinstance(q, Fr) else Fr(q)
        if q < 0:
            raise ValueError
        if q == 0:
            return (Fr(0), Fr(0))
        N = q.numerator * (self.D * self.D)
        Dd = q.denominator
        m = self._isqrt(N // Dd)
        return (Fr(m, self.D), Fr(m + 1, self.D))

    def sqrt_iv(self, X):
        return (self.sqrt_rat(X[0])[0], self.sqrt_rat(X[1])[1])

    # ---- atan of nonnegative interval ----
    def _atan_small(self, p):
        p2 = p * p
        powI = self.iconst(p)
        p2I = self.iconst(p2)
        s = self.iconst(0)
        sign = 1
        j = 0
        while True:
            s = self.iadd(s, self.scale(powI, Fr(sign, 2 * j + 1)))
            powI = self.imul(powI, p2I)
            mag = max(abs(powI[0]), abs(powI[1]))
            B = mag / (2 * j + 3)
            if B < self.TAILEPS or j > self.NT_MAX:
                break
            sign = -sign
            j += 1
        return (self._rd(s[0] - B, "d"), self._rd(s[1] + B, "u"))

    def _atan_point(self, p, which):
        if p == 0:
            return Fr(0)
        k = 0
        T = (p, p)
        while T[1] > Fr(1, 2) and k < 8:
            s = self.sqrt_iv(self.iadd(self.iconst(1), self.imul(T, T)))
            T = self.idiv(T, self.iadd(self.iconst(1), s))
            k += 1
        if which == "lo":
            return self._rd(self._atan_small(T[0])[0] * (1 << k), "d")
        return self._rd(self._atan_small(T[1])[1] * (1 << k), "u")

    def atan_nonneg(self, T):
        if T[0] < 0:
            raise ValueError
        return (self._atan_point(T[0], "lo"), self._atan_point(T[1], "hi"))

    def atan2_nonneg(self, num, den):
        if den[0] <= 0:
            raise ValueError
        return self.atan_nonneg(self.idiv(num, den))

    # ---- log ----
    def _atanh_point(self, w):
        w2 = w * w
        inv = 1 / (1 - w2)
        powI = self.iconst(w)
        w2I = self.iconst(w2)
        s = self.iconst(0)
        j = 0
        while True:
            s = self.iadd(s, self.scale(powI, Fr(1, 2 * j + 1)))
            powI = self.imul(powI, w2I)
            mag = max(abs(powI[0]), abs(powI[1]))
            B = (mag / (2 * j + 3)) * inv
            if B < self.TAILEPS or j > self.NT_MAX:
                break
            j += 1
        return (self._rd(s[0] - B, "d"), self._rd(s[1] + B, "u"))

    def _log2(self):
        lo, hi = self._atanh_point(Fr(1, 3))
        return (self._rd(2 * lo, "d"), self._rd(2 * hi, "u"))

    def _log_point(self, p, which):
        if p <= 0:
            raise ValueError
        e = 0
        m = p
        two = Fr(2)
        while m > Fr(4, 3):
            m /= two
            e += 1
        while m < Fr(2, 3):
            m *= two
            e -= 1
        w = (m - 1) / (m + 1)
        a_lo, a_hi = self._atanh_point(w)
        lm_lo, lm_hi = 2 * a_lo, 2 * a_hi
        if e >= 0:
            e_lo, e_hi = e * self.LOG2[0], e * self.LOG2[1]
        else:
            e_lo, e_hi = e * self.LOG2[1], e * self.LOG2[0]
        if which == "lo":
            return self._rd(e_lo + lm_lo, "d")
        return self._rd(e_hi + lm_hi, "u")

    def log_iv(self, X):
        if X[0] <= 0:
            raise ValueError
        return (self._log_point(X[0], "lo"), self._log_point(X[1], "hi"))

    def _pi(self):
        a5 = self._atan_small(Fr(1, 5))
        a239 = self._atan_small(Fr(1, 239))
        lo = 4 * (4 * a5[0] - a239[1])
        hi = 4 * (4 * a5[1] - a239[0])
        return (self._rd(lo, "d"), self._rd(hi, "u"))


# ===========================================================================
# Newell f, g, self-demag in intervals + stencils   (43 of 143 lines shared with the private newell.py)
# ===========================================================================
_STENCIL = [
    (+1, +1, +1, -1), (+1, -1, +1, -1), (+1, -1, -1, -1), (+1, +1, -1, -1),
    (-1, +1, -1, -1), (-1, +1, +1, -1), (-1, -1, +1, -1), (-1, -1, -1, -1),
    (0, -1, -1, 2), (0, -1, +1, 2), (0, +1, +1, 2), (0, +1, -1, 2),
    (+1, +1, 0, 2), (+1, 0, +1, 2), (+1, 0, -1, 2), (+1, -1, 0, 2),
    (-1, -1, 0, 2), (-1, 0, +1, 2), (-1, 0, -1, 2), (-1, +1, 0, 2),
    (0, -1, 0, -4), (0, +1, 0, -4), (0, 0, -1, -4), (0, 0, +1, -4),
    (+1, 0, 0, -4), (-1, 0, 0, -4), (0, 0, 0, 8),
]


class Newell:
    def __init__(self, civ):
        self.c = civ

    def f(self, x, y, z):
        c = self.c
        x = abs(Fr(x)); y = abs(Fr(y)); z = abs(Fr(z))
        xsq, ysq, zsq = x * x, y * y, z * z
        Rsq = xsq + ysq + zsq
        if Rsq == 0:
            return c.iconst(0)
        R = c.sqrt_iv(c.iconst(Rsq))
        s = c.iconst(0)
        if z > 0:
            s = c.iadd(s, c.scale(R, 2 * (2 * xsq - ysq - zsq)))
            if x > 0 and y > 0 and z > 0:
                s = c.iadd(s, c.scale(c.atan2_nonneg(c.iconst(y * z), c.scale(R, x)),
                                      -12 * x * y * z))
            if y > 0 and (xsq + zsq) > 0:
                yR = c.iadd(R, c.iconst(y))
                arg = c.scale(c.imul(yR, yR), Fr(1, xsq + zsq))
                s = c.iadd(s, c.scale(c.log_iv(arg), 3 * y * (zsq - xsq)))
            if (xsq + ysq) > 0:
                zR = c.iadd(R, c.iconst(z))
                arg = c.scale(c.imul(zR, zR), Fr(1, xsq + ysq))
                s = c.iadd(s, c.scale(c.log_iv(arg), 3 * z * (ysq - xsq)))
        else:
            if x == y:
                s = c.iadd(s, c.scale(c.K, xsq * x))
            else:
                s = c.iadd(s, c.scale(R, 2 * (2 * xsq - ysq)))
                if y > 0 and x > 0:
                    arg = c.scale(c.iadd(R, c.iconst(y)), Fr(1, x))
                    s = c.iadd(s, c.scale(c.log_iv(arg), -6 * y * xsq))
        return c.scale(s, Fr(1, 12))

    def g(self, x, y, z):
        c = self.c
        x = Fr(x); y = Fr(y); z = Fr(z)
        sign = 1
        if x < 0:
            sign = -sign
        if y < 0:
            sign = -sign
        x = abs(x); y = abs(y); z = abs(z)
        xsq, ysq, zsq = x * x, y * y, z * z
        Rsq = xsq + ysq + zsq
        if Rsq == 0:
            return c.iconst(0)
        R = c.sqrt_iv(c.iconst(Rsq))
        s = c.scale(R, -2 * x * y)
        if z > 0:
            if x > 0 and y > 0:
                s = c.iadd(s, c.scale(c.atan2_nonneg(c.iconst(x * y), c.scale(R, z)), -z * zsq))
                s = c.iadd(s, c.scale(c.atan2_nonneg(c.iconst(x * z), c.scale(R, y)), -3 * z * ysq))
                s = c.iadd(s, c.scale(c.atan2_nonneg(c.iconst(y * z), c.scale(R, x)), -3 * z * xsq))
            if (xsq + ysq) > 0:
                zR = c.iadd(R, c.iconst(z))
                arg = c.scale(c.imul(zR, zR), Fr(1, xsq + ysq))
                s = c.iadd(s, c.scale(c.log_iv(arg), 3 * x * y * z))
            if (ysq + zsq) > 0:
                xR = c.iadd(R, c.iconst(x))
                arg = c.scale(c.imul(xR, xR), Fr(1, ysq + zsq))
                s = c.iadd(s, c.scale(c.log_iv(arg), Fr(3 * zsq - ysq, 2) * y))
            if (xsq + zsq) > 0:
                yR = c.iadd(R, c.iconst(y))
                arg = c.scale(c.imul(yR, yR), Fr(1, xsq + zsq))
                s = c.iadd(s, c.scale(c.log_iv(arg), Fr(3 * zsq - xsq, 2) * x))
        else:
            if y > 0:
                arg = c.scale(c.iadd(R, c.iconst(x)), Fr(1, y))
                s = c.iadd(s, c.scale(c.log_iv(arg), -y * ysq))
            if x > 0:
                arg = c.scale(c.iadd(R, c.iconst(y)), Fr(1, x))
                s = c.iadd(s, c.scale(c.log_iv(arg), -x * xsq))
        return c.scale(s, Fr(sign, 6))

    def self_nx(self, x, y, z):
        c = self.c
        x = Fr(x); y = Fr(y); z = Fr(z)
        if x <= 0 or y <= 0 or z <= 0:
            return c.iconst(0)
        if x == y and y == z:
            return c.iconst(Fr(1, 3))
        xsq, ysq, zsq = x * x, y * y, z * z
        R = c.sqrt_iv(c.iconst(xsq + ysq + zsq))
        Rxy = c.sqrt_iv(c.iconst(xsq + ysq))
        Rxz = c.sqrt_iv(c.iconst(xsq + zsq))
        Ryz = c.sqrt_iv(c.iconst(ysq + zsq))
        xyz = x * y * z

        def term(a, asq, bsq, csq, Rab, Rac):
            c2 = 2 * asq + bsq + csq
            t1 = c.idiv(c.iadd(c.idiv(c.iconst(a), c.iadd(Rab, c.iconst(a))),
                               c.idiv(c.iconst(c2), c.iadd(c.imul(R, Rab), c.scale(Rac, a)))),
                        c.iadd(Rac, c.iconst(a)))
            t2 = c.idiv(c.iadd(c.idiv(c.iconst(a), c.iadd(Rac, c.iconst(a))),
                               c.idiv(c.iconst(c2), c.iadd(c.imul(R, Rac), c.scale(Rab, a)))),
                        c.iadd(Rab, c.iconst(a)))
            return c.idiv(c.iadd(t1, t2), c.imul(c.iadd(R, c.iconst(a)), c.iadd(c.iadd(Rab, Rac), R)))

        s = c.scale(term(x, xsq, ysq, zsq, Rxy, Rxz), 2 * xyz)
        s = c.iadd(s, c.scale(term(y, ysq, xsq, zsq, Rxy, Ryz), -xyz))
        s = c.iadd(s, c.scale(term(z, zsq, xsq, ysq, Rxz, Ryz), -xyz))
        s = c.iadd(s, c.scale(c.atan2_nonneg(c.iconst(y * z), c.scale(R, x)), 6))
        s = c.iadd(s, c.idiv(c.scale(c.log_iv(c.idiv(c.scale(c.iadd(R, c.iconst(y)), x),
                     c.imul(Rxz, c.iadd(Rxy, c.iconst(y))))), 3 * x), c.iconst(z)))
        s = c.iadd(s, c.idiv(c.scale(c.log_iv(c.idiv(c.scale(c.iadd(R, c.iconst(z)), x),
                     c.imul(Rxy, c.iadd(Rxz, c.iconst(z))))), 3 * x), c.iconst(y)))
        s = c.iadd(s, c.idiv(c.scale(c.log_iv(c.idiv(c.scale(c.iadd(R, c.iconst(z)), y),
                     c.imul(Rxy, c.iadd(Ryz, c.iconst(z))))), -3 * y), c.iconst(x)))
        s = c.iadd(s, c.idiv(c.scale(c.log_iv(c.idiv(c.scale(c.iadd(R, c.iconst(y)), z),
                     c.imul(Rxz, c.iadd(Ryz, c.iconst(y))))), -3 * z), c.iconst(x)))
        return c.idiv(s, c.scale(c.PI, 3))

    def _stencil(self, func, x, y, z, dx, dy, dz):
        c = self.c
        acc = c.iconst(0)
        for i, j, k, w in _STENCIL:
            acc = c.iadd(acc, c.scale(func(x + i * dx, y + j * dy, z + k * dz), w))
        return acc

    def Nxx(self, x, y, z, dx, dy, dz):
        c = self.c
        x, y, z, dx, dy, dz = map(Fr, (x, y, z, dx, dy, dz))
        if x == 0 and y == 0 and z == 0:
            return self.self_nx(dx, dy, dz)
        return c.idiv(self._stencil(self.f, x, y, z, dx, dy, dz),
                      c.scale(c.PI, 4 * dx * dy * dz))

    def Nxy(self, x, y, z, dx, dy, dz):
        c = self.c
        x, y, z, dx, dy, dz = map(Fr, (x, y, z, dx, dy, dz))
        if x == 0 or y == 0:
            return c.iconst(0)
        return c.idiv(self._stencil(self.g, x, y, z, dx, dy, dz),
                      c.scale(c.PI, 4 * dx * dy * dz))

    def comp(self, name, x, y, z, dx, dy, dz):
        if name == "Nxx":
            return self.Nxx(x, y, z, dx, dy, dz)
        if name == "Nyy":
            return self.Nxx(y, x, z, dy, dx, dz)
        if name == "Nzz":
            return self.Nxx(z, y, x, dz, dy, dx)
        if name == "Nxy":
            return self.Nxy(x, y, z, dx, dy, dz)
        if name == "Nxz":
            return self.Nxy(x, z, y, dx, dz, dy)
        if name == "Nyz":
            return self.Nxy(y, z, x, dy, dz, dx)
        raise ValueError(name)


# ===========================================================================
# Naive IEEE-754 double Newell (76 of 103 lines verbatim from the private newell.py -- NOT an independent re-derivation)
# ===========================================================================
def f_float(x, y, z):
    x = abs(x); y = abs(y); z = abs(z)
    xsq, ysq, zsq = x * x, y * y, z * z
    Rsq = xsq + ysq + zsq
    if Rsq <= 0.0:
        return 0.0
    R = math.sqrt(Rsq)
    s = 0.0
    if z > 0.0:
        s += 2 * (2 * xsq - ysq - zsq) * R
        if x > 0 and y > 0 and z > 0:
            s += -12 * x * y * z * math.atan2(y * z, x * R)
        if y > 0 and (xsq + zsq) > 0:
            s += 3 * y * (zsq - xsq) * math.log(((y + R) * (y + R)) / (xsq + zsq))
        if (xsq + ysq) > 0:
            s += 3 * z * (ysq - xsq) * math.log(((z + R) * (z + R)) / (xsq + ysq))
    else:
        if x == y:
            K = 2 * math.sqrt(2.0) - 6 * math.log(1 + math.sqrt(2.0))
            s += K * xsq * x
        else:
            s += 2 * (2 * xsq - ysq) * R
            if y > 0 and x > 0:
                s += -6 * y * xsq * math.log((y + R) / x)
    return s / 12.0


def g_float(x, y, z):
    sign = 1.0
    if x < 0:
        sign = -sign
    if y < 0:
        sign = -sign
    x = abs(x); y = abs(y); z = abs(z)
    xsq, ysq, zsq = x * x, y * y, z * z
    Rsq = xsq + ysq + zsq
    if Rsq <= 0.0:
        return 0.0
    R = math.sqrt(Rsq)
    s = -2 * x * y * R
    if z > 0.0:
        if x > 0 and y > 0:
            s += -z * zsq * math.atan2(x * y, z * R)
            s += -3 * z * ysq * math.atan2(x * z, y * R)
            s += -3 * z * xsq * math.atan2(y * z, x * R)
        if (xsq + ysq) > 0:
            s += 3 * x * y * z * math.log(((z + R) * (z + R)) / (xsq + ysq))
        if (ysq + zsq) > 0:
            s += 0.5 * y * (3 * zsq - ysq) * math.log(((x + R) * (x + R)) / (ysq + zsq))
        if (xsq + zsq) > 0:
            s += 0.5 * x * (3 * zsq - xsq) * math.log(((y + R) * (y + R)) / (xsq + zsq))
    else:
        if y > 0:
            s += -y * ysq * math.log((x + R) / y)
        if x > 0:
            s += -x * xsq * math.log((y + R) / x)
    return sign * s / 6.0


def self_nx_float(x, y, z):
    if x == y == z:
        return 1.0 / 3.0
    xsq, ysq, zsq = x * x, y * y, z * z
    R = math.sqrt(xsq + ysq + zsq)
    Rxy = math.sqrt(xsq + ysq); Rxz = math.sqrt(xsq + zsq); Ryz = math.sqrt(ysq + zsq)
    xyz = x * y * z

    def term(a, asq, bsq, csq, Rab, Rac):
        c2 = 2 * asq + bsq + csq
        t1 = (a / (a + Rab) + c2 / (R * Rab + a * Rac)) / (a + Rac)
        t2 = (a / (a + Rac) + c2 / (R * Rac + a * Rab)) / (a + Rab)
        return (t1 + t2) / ((a + R) * (Rab + Rac + R))
    s = 2 * xyz * term(x, xsq, ysq, zsq, Rxy, Rxz)
    s += -xyz * term(y, ysq, xsq, zsq, Rxy, Ryz)
    s += -xyz * term(z, zsq, xsq, ysq, Rxz, Ryz)
    s += 6 * math.atan2(y * z, x * R)
    s += 3 * x * math.log(x * (y + R) / (Rxz * (y + Rxy))) / z
    s += 3 * x * math.log(x * (z + R) / (Rxy * (z + Rxz))) / y
    s += -3 * y * math.log(y * (z + R) / (Rxy * (z + Ryz))) / x
    s += -3 * z * math.log(z * (y + R) / (Rxz * (y + Ryz))) / x
    return s / (3 * math.pi)


def _stencil_float(func, x, y, z, dx, dy, dz):
    acc = 0.0
    for i, j, k, w in _STENCIL:
        acc += w * func(x + i * dx, y + j * dy, z + k * dz)
    return acc


def Nxx_float(x, y, z, dx, dy, dz):
    if x == 0 and y == 0 and z == 0:
        return self_nx_float(dx, dy, dz)
    return _stencil_float(f_float, x, y, z, dx, dy, dz) / (4 * math.pi * dx * dy * dz)


def Nxy_float(x, y, z, dx, dy, dz):
    if x == 0 or y == 0:
        return 0.0
    return _stencil_float(g_float, x, y, z, dx, dy, dz) / (4 * math.pi * dx * dy * dz)


def comp_float(name, x, y, z, dx, dy, dz):
    if name == "Nxx":
        return Nxx_float(x, y, z, dx, dy, dz)
    if name == "Nyy":
        return Nxx_float(y, x, z, dy, dx, dz)
    if name == "Nzz":
        return Nxx_float(z, y, x, dz, dy, dx)
    if name == "Nxy":
        return Nxy_float(x, y, z, dx, dy, dz)
    if name == "Nxz":
        return Nxy_float(x, z, y, dx, dz, dy)
    if name == "Nyz":
        return Nxy_float(y, z, x, dy, dz, dx)
    raise ValueError(name)


# ===========================================================================
def parse_fr(s):
    a, b = s.split("/")
    return Fr(int(a), int(b))


def digit_bracket(N_lo, N_hi, v):
    vv = Fr(v)
    absend = max(abs(N_lo), abs(N_hi))
    minabs = Fr(0) if (N_lo <= 0 <= N_hi) else min(abs(N_lo), abs(N_hi))
    if vv < N_lo:
        d_lo = N_lo - vv; d_hi = N_hi - vv
    elif vv > N_hi:
        d_lo = vv - N_hi; d_hi = vv - N_lo
    else:
        d_lo = Fr(0); d_hi = max(vv - N_lo, N_hi - vv)
    inside = (N_lo <= vv <= N_hi)

    def nlog10(fr):
        if fr <= 0:
            return None
        return -math.log10(float(fr))
    rel_lo = d_lo / absend if absend > 0 else None
    rel_hi = (d_hi / minabs) if minabs > 0 else None
    dig_hi = nlog10(rel_lo) if d_lo > 0 else float("inf")
    dig_lo = nlog10(rel_hi) if (rel_hi is not None and d_hi > 0) else (float("inf") if d_hi == 0 else None)
    return {
        "inside": inside,
        "rel_err_lo": (float(d_lo / absend) if absend > 0 else None),
        "correct_digits_lo": dig_lo,
        "correct_digits_hi": dig_hi,
    }


def canonical_line(e):
    return "|".join([
        e["cell"], e["direction"], str(e["sep_cells"]), e["component"],
        e["N_lo"], e["N_hi"], e["naive_double"], e.get("asymp_oommf", "-"),
    ])


def approx_eq(a, b):
    # brackets stored as floats/inf/None in JSON; compare with tolerance
    if a is None or b is None:
        return a is None and b is None
    if a == float("inf") or b == float("inf"):
        return a == b
    return abs(a - b) <= 1e-6 * (1 + abs(a))


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    sample = None
    if "--sample" in args:
        i = args.index("--sample")
        sample = int(args[i + 1])
        del args[i:i + 2]
    cert = json.load(open(args[0]))
    entries = cert["entries"]
    if len(entries) != cert["num_entries"]:
        fail("num_entries mismatch")

    # 1. hash
    lines = [canonical_line(e) for e in entries]
    h = hashlib.sha256(("\n".join(lines) + "\n").encode()).hexdigest()
    if h != cert["entries_sha256"]:
        fail("entries_sha256 mismatch")

    PREC = cert["method"]["PREC_bits"]
    civ = CIV(PREC)
    nw = Newell(civ)

    check_idx = range(len(entries))
    if sample is not None and sample < len(entries):
        # deterministic stride sample (no RNG; reproducible)
        step = max(1, len(entries) // sample)
        check_idx = range(0, len(entries), step)

    n_ok = 0
    breakdown = {}   # (cell,direction) -> smallest sep with naive correct_digits_hi <= 0
    for idx in check_idx:
        e = entries[idx]
        dx, dy, dz = [parse_fr(t) for t in e["cell_dims"]]
        x, y, z = [parse_fr(t) for t in e["offset"]]
        N_lo = parse_fr(e["N_lo"]); N_hi = parse_fr(e["N_hi"])
        if N_lo > N_hi:
            fail("inverted enclosure at entry %d" % idx)
        # 2. re-derive enclosure (independent), require containment c in [N_lo,N_hi]
        c_lo, c_hi = nw.comp(e["component"], x, y, z, dx, dy, dz)
        if not (N_lo <= c_lo and c_hi <= N_hi):
            fail("enclosure not verified at entry %d (%s %s sep=%d): "
                 "recomputed [%s] not inside certified [%s,%s]"
                 % (idx, e["cell"], e["component"], e["sep_cells"],
                    "%d/%d..%d/%d" % (c_lo.numerator, c_lo.denominator,
                                      c_hi.numerator, c_hi.denominator),
                    e["N_lo"], e["N_hi"]))
        # sanity: certified enclosure not grossly wider than the recomputed one
        if (N_hi - N_lo) > (c_hi - c_lo) * 8 + Fr(1, civ.D):
            fail("certified enclosure implausibly wide at entry %d" % idx)
        # 3. naive double re-derivation, exact bit match
        v = comp_float(e["component"], float(x), float(y), float(z),
                       float(dx), float(dy), float(dz))
        if float(v).hex() != e["naive_double"]:
            fail("naive double mismatch at entry %d: %s vs %s"
                 % (idx, float(v).hex(), e["naive_double"]))
        # 4. digit brackets
        db = digit_bracket(N_lo, N_hi, v)
        ce = e["naive_digits"]
        for key in ("correct_digits_lo", "correct_digits_hi"):
            if not approx_eq(db[key], ce[key]):
                fail("naive %s mismatch at entry %d: %r vs %r"
                     % (key, idx, db[key], ce[key]))
        if db["inside"] != ce["inside"]:
            fail("naive inside flag mismatch at entry %d" % idx)
        if "asymp_oommf" in e:
            av = float.fromhex(e["asymp_oommf"])
            adb = digit_bracket(N_lo, N_hi, av)
            ae = e["asymp_digits"]
            for key in ("correct_digits_lo", "correct_digits_hi"):
                if not approx_eq(adb[key], ae[key]):
                    fail("asymp %s mismatch at entry %d" % (key, idx))
        # breakdown tracking
        cdh = ce["correct_digits_hi"]
        if cdh != float("inf") and cdh is not None and cdh <= 0.0:
            key = (e["cell"], e["direction"], e["component"])
            if key not in breakdown or e["sep_cells"] < breakdown[key]:
                breakdown[key] = e["sep_cells"]
        n_ok += 1

    # consistency identities from the certified endpoints (no re-derivation):
    # trace-freeness at mutual points, sum-to-one at the self-term. Uses the
    # STORED enclosures, so it holds regardless of --sample.
    from collections import defaultdict
    byloc = defaultdict(dict)
    for e in entries:
        byloc[(e["cell"], e["direction"], e["sep_cells"])][e["component"]] = \
            (parse_fr(e["N_lo"]), parse_fr(e["N_hi"]))
    tr_ok = tr_n = sf_ok = sf_n = 0
    for (cell, direction, sep), comps in byloc.items():
        if all(c in comps for c in ("Nxx", "Nyy", "Nzz")):
            lo = comps["Nxx"][0] + comps["Nyy"][0] + comps["Nzz"][0]
            hi = comps["Nxx"][1] + comps["Nyy"][1] + comps["Nzz"][1]
            target = 1 if direction == "self" else 0
            if not (lo <= target <= hi):
                fail("consistency identity failed: %s %s sep=%d trace/sum does "
                     "not enclose %d" % (cell, direction, sep, target))
            if direction == "self":
                sf_ok += 1; sf_n += 1
            else:
                tr_ok += 1; tr_n += 1

    print("certificate: %s" % cert.get("title", "")[:70])
    print("PREC = %d bits (grid denominator 2**%d)" % (PREC, PREC))
    print("entries in certificate: %d   entries verified: %d%s"
          % (len(entries), n_ok, "" if sample is None else " (deterministic sample)"))
    print("entries_sha256: %s OK" % h[:24])
    print("consistency: trace encloses 0 at %d/%d mutual points; self-term "
          "encloses 1 at %d/%d" % (tr_ok, tr_n, sf_ok, sf_n))
    # report a few breakdown radii (naive double -> <=0 correct digits)
    shown = 0
    for (cell, direction, comp), sep in sorted(breakdown.items()):
        if shown < 8:
            print("  naive double reaches 0 correct digits by sep=%d cells  (%s %s %s)"
                  % (sep, cell, direction, comp))
        shown += 1
    print("CHECK PASS")


if __name__ == "__main__":
    main()
