#!/usr/bin/env python3
"""Independent anchor check for Part M (certified ZEFOZ brackets).

Requires mpmath (the one dependency; everything shipped as a checker is
standard-library -- this anchor is an OPTIONAL independent cross-check, not
part of the certified surface).

For every point of the certificate (certificate2.json and, if present,
certificate_pilot.json), rebuilds H(B*) from the certificate's own rational
matrices in 60-digit arithmetic, diagonalizes it with mpmath's Hermitian
eigensolver -- a code path sharing nothing with the interval LDL^T machinery
of the shipped checker -- and verifies that every certified eigenvalue bracket
contains the recomputed eigenvalue.  Zero containment failures expected.

Usage:  python3 anchor_check.py
(run from zefoz-scripts/ with zefoz-certificates/ alongside)
"""
import json
import os
import sys
from fractions import Fraction as F

try:
    import mpmath as mp
except ImportError:
    print("anchor_check.py needs mpmath (pip install mpmath); the shipped "
          "checker zefoz_checker2.py does not.")
    sys.exit(2)

mp.mp.dps = 60

_here = os.path.dirname(os.path.abspath(__file__))
CERTDIR = None
for cand in (os.path.join(_here, "..", "zefoz-certificates"), _here):
    if os.path.exists(os.path.join(cand, "certificate2.json")):
        CERTDIR = cand
        break


def frmp(s):
    f = F(s)
    return mp.mpf(f.numerator) / mp.mpf(f.denominator)


def spinm(j):
    d = int(2 * j + 1)
    ms = [mp.mpf(j) - k for k in range(d)]
    jp = mp.zeros(d, d)
    for k in range(1, d):
        m = ms[k]
        jp[k - 1, k] = mp.sqrt(j * (j + 1) - m * (m + 1))
    jx = (jp + jp.T) / 2
    jy = (jp - jp.T) / (2 * mp.mpc(0, 1))
    jz = mp.diag(ms)
    return jx, jy, jz


def kron(A, B):
    ra, ca, rb, cb = A.rows, A.cols, B.rows, B.cols
    M = mp.zeros(ra * rb, ca * cb)
    for i in range(ra):
        for j in range(ca):
            if A[i, j] == 0:
                continue
            for k in range(rb):
                for l in range(cb):
                    M[i * rb + k, j * cb + l] = A[i, j] * B[k, l]
    return M


def check(path):
    cert = json.load(open(path))
    sx, sy, sz = spinm(mp.mpf(1) / 2)
    ix, iy, iz = spinm(mp.mpf(7) / 2)
    I2, I8 = mp.eye(2), mp.eye(8)
    S = [kron(s, I8) for s in (sx, sy, sz)]
    I = [kron(I2, i) for i in (ix, iy, iz)]
    muB = frmp(cert["constants"]["muB_MHz_per_mT"])
    muN = frmp(cert["constants"]["muN_MHz_per_mT"])
    gn = frmp(cert["constants"]["gn"])
    npts = nbr = fails = 0
    worst = None
    for p in cert["points"]:
        if "B_mT" not in p or "eigenvalue_brackets_MHz" not in p:
            continue
        sd = cert["sites"][str(p["site"])]
        A = [[frmp(x) for x in r] for r in sd["A"]]
        Q = [[frmp(x) for x in r] for r in sd["Q"]]
        g = [[frmp(x) for x in r] for r in sd["g"]]
        B = [frmp(x) for x in p["B_mT"]]
        H = mp.zeros(16, 16)
        for a in range(3):
            for b in range(3):
                H += A[a][b] * (I[a] * S[b]) + Q[a][b] * (I[a] * I[b])
        for k in range(3):
            for l in range(3):
                H += muB * g[k][l] * B[k] * S[l]
            H -= muN * gn * B[k] * I[k]
        E = mp.eighe(H, eigvals_only=True)
        w = sorted(mp.re(e) for e in E)
        for n, (lo, hi) in enumerate(p["eigenvalue_brackets_MHz"]):
            lo, hi = frmp(lo), frmp(hi)
            nbr += 1
            m = min(w[n] - lo, hi - w[n])
            if worst is None or m < worst:
                worst = m
            if not (lo <= w[n] <= hi):
                fails += 1
                print("CONTAINMENT FAIL", p.get("label", "?"), n)
        npts += 1
    print("%s: %d points, %d brackets, %d containment failures; "
          "worst margin %s MHz" % (os.path.basename(path), npts, nbr, fails,
                                   mp.nstr(worst, 5)))
    return fails


def main():
    total = 0
    for name in ("certificate2.json", "certificate_pilot.json"):
        path = os.path.join(CERTDIR, name)
        if os.path.exists(path):
            total += check(path)
    if total == 0:
        print("ANCHOR PASS: independent 60-digit eigenvalues inside every "
              "certified bracket")
        return 0
    print("ANCHOR FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
