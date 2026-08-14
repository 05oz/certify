#!/usr/bin/env python3
"""Standalone checker for certificate.json (PUBLISHABLE).

Verifies, using ONLY the Python 3 standard library (fractions, json, math),
the certificate's claims:

  For each listed point (site, exact rational field B, in mT, optical frame):
    every stated eigenvalue bracket [lo_n, hi_n] contains the n-th eigenvalue
    (ascending) of H(B), and every stated transition bracket [f_lo, f_hi]
    contains E_j - E_i, where

      H(B) = I.A.S + I.Q.I + muB * B.g.S - muN*gn * B.I     (MHz; B in mT)

    with S=1/2, I=7/2 (dim 16), and A, Q, g exactly the rational matrices in
    the certificate (arXiv:2412.10126v3 Appendix B).

Method (recomputation from the certificate alone, no trust in the generator's
values; NOT code-independent of it -- 53 of 166 executable lines are verbatim
from the private pilot engine):
  - sqrt(7), sqrt(12), sqrt(15) enclosures are validated by squaring;
  - H(B) is built in rectangle complex-interval arithmetic over exact
    rationals with outward rounding (every interval op encloses the exact op);
  - for each certified shift mu, an interval LDL^T factorization of H - mu*I
    is run; if every pivot interval is sign-definite, Sylvester's law of
    inertia gives a PROOF that exactly (#negative pivots) eigenvalues of the
    exact H(B) lie below mu;
  - counts at the bracket endpoints then pin each eigenvalue:
      #{lambda < lo} <= n  and  #{lambda < hi} >= n+1  ==>  lambda_n in [lo, hi);
  - transition brackets are checked by exact rational arithmetic.

Exit code 0 and final line "CERTIFICATE VERIFIED" iff every claim checks.
Any pivot interval containing zero, any count mismatch, or any bracket
violation is a FAILURE (the certificate proves nothing about that point).

Usage: python3 zefoz_checker.py certificate.json
"""
import sys, json, math
from fractions import Fraction as F

PREC = 2**200

def rnd_lo(x): return F(math.floor(x*PREC), PREC) if x.denominator > PREC else x
def rnd_hi(x): return F(-math.floor(-x*PREC), PREC) if x.denominator > PREC else x

class Iv:
    __slots__ = ("lo","hi")
    def __init__(self, lo, hi=None):
        if hi is None: hi = lo
        self.lo, self.hi = lo, hi
    def __add__(s,o): return Iv(rnd_lo(s.lo+o.lo), rnd_hi(s.hi+o.hi))
    def __sub__(s,o): return Iv(rnd_lo(s.lo-o.hi), rnd_hi(s.hi-o.lo))
    def __mul__(s,o):
        c = (s.lo*o.lo, s.lo*o.hi, s.hi*o.lo, s.hi*o.hi)
        return Iv(rnd_lo(min(c)), rnd_hi(max(c)))
    def divr(s,o):
        if not (o.lo > 0 or o.hi < 0): raise ZeroDivisionError
        c = (s.lo/o.lo, s.lo/o.hi, s.hi/o.lo, s.hi/o.hi)
        return Iv(rnd_lo(min(c)), rnd_hi(max(c)))
    def neg(s): return Iv(-s.hi, -s.lo)

class Cv:
    __slots__ = ("re","im")
    def __init__(s, re, im=None): s.re, s.im = re, (im if im is not None else Iv(F(0)))
    def __add__(a,b): return Cv(a.re+b.re, a.im+b.im)
    def __sub__(a,b): return Cv(a.re-b.re, a.im-b.im)
    def __mul__(a,b): return Cv(a.re*b.re - a.im*b.im, a.re*b.im + a.im*b.re)
    def conj(a): return Cv(a.re, a.im.neg())
    def divr(a,d): return Cv(a.re.divr(d), a.im.divr(d))

def pf(s): return F(s)          # "p/q" or decimal string -> Fraction (exact)

def cF(x): return Cv(Iv(F(x)))

def kron(A,B):
    n1, n2 = len(A), len(B)
    return [[A[i//n2][j//n2]*B[i%n2][j%n2] for j in range(n1*n2)] for i in range(n1*n2)]

def matmul(A,B):
    n = len(A)
    Bt = [[B[k][j] for k in range(n)] for j in range(n)]
    out = []
    for i in range(n):
        row = []
        for j in range(n):
            s = A[i][0]*Bt[j][0]
            for k in range(1, n):
                s = s + A[i][k]*Bt[j][k]
            row.append(s)
        out.append(row)
    return out

def build_ops(cert):
    sq = {}
    for key, target in (("7",7), ("12",12), ("15",15)):
        lo, hi = pf(cert["sqrt_enclosures"][key][0]), pf(cert["sqrt_enclosures"][key][1])
        if not (0 <= lo <= hi and lo*lo <= target and target <= hi*hi):
            raise AssertionError(f"invalid sqrt enclosure for {key}")
        sq[key] = Iv(lo, hi)
    half = F(1,2)
    Sx = [[cF(0), cF(half)],[cF(half), cF(0)]]
    Sy = [[cF(0), Cv(Iv(F(0)), Iv(-half))],[Cv(Iv(F(0)), Iv(half)), cF(0)]]
    Sz = [[cF(half), cF(0)],[cF(0), cF(-half)]]
    lad = [sq["7"], sq["12"], sq["15"], Iv(F(4)), sq["15"], sq["12"], sq["7"]]
    Ix = [[cF(0) for _ in range(8)] for _ in range(8)]
    Iy = [[cF(0) for _ in range(8)] for _ in range(8)]
    Iz = [[cF(0) for _ in range(8)] for _ in range(8)]
    for k in range(7):
        c = lad[k]*Iv(half)
        Ix[k][k+1] = Cv(c); Ix[k+1][k] = Cv(c)
        Iy[k][k+1] = Cv(Iv(F(0)), c.neg()); Iy[k+1][k] = Cv(Iv(F(0)), c)
    for k in range(8):
        Iz[k][k] = cF(F(7,2) - k)
    I2m = [[cF(1), cF(0)],[cF(0), cF(1)]]
    I8m = [[cF(1 if i==j else 0) for j in range(8)] for i in range(8)]
    Sops = [kron(s, I8m) for s in (Sx, Sy, Sz)]
    Iops = [kron(I2m, i) for i in (Ix, Iy, Iz)]
    return Sops, Iops

def build_H(cert, site, B, Sops, Iops):
    sd = cert["sites"][str(site)]
    A = [[pf(x) for x in r] for r in sd["A"]]
    Q = [[pf(x) for x in r] for r in sd["Q"]]
    g = [[pf(x) for x in r] for r in sd["g"]]
    muB = pf(cert["constants"]["muB_MHz_per_mT"])
    muN = pf(cert["constants"]["muN_MHz_per_mT"])
    gn  = pf(cert["constants"]["gn"])
    H = [[cF(0) for _ in range(16)] for _ in range(16)]
    for a in range(3):
        for b in range(3):
            IS = matmul(Iops[a], Sops[b])
            II = matmul(Iops[a], Iops[b])
            ca, cb = Cv(Iv(A[a][b])), Cv(Iv(Q[a][b]))
            for i in range(16):
                for j in range(16):
                    H[i][j] = H[i][j] + ca*IS[i][j] + cb*II[i][j]
    for k in range(3):
        if B[k] == 0: continue
        for l in range(3):
            c = Cv(Iv(muB*g[k][l]*B[k]))
            for i in range(16):
                for j in range(16):
                    H[i][j] = H[i][j] + c*Sops[l][i][j]
        c = Cv(Iv(-muN*gn*B[k]))
        for i in range(16):
            for j in range(16):
                H[i][j] = H[i][j] + c*Iops[k][i][j]
    return H

def neg_count(H, mu):
    n = 16
    A = [[Cv(H[i][j].re, H[i][j].im) for j in range(n)] for i in range(n)]
    for i in range(n):
        A[i][i] = Cv(A[i][i].re - Iv(mu), A[i][i].im)
    neg = 0
    for k in range(n):
        d = A[k][k].re
        if d.hi < 0: neg += 1
        elif d.lo > 0: pass
        else: return None
        for i in range(k+1, n):
            for j in range(k+1, i+1):
                A[i][j] = A[i][j] - (A[i][k]*A[j][k].conj()).divr(d)
    return neg

def main(path):
    cert = json.load(open(path))
    Sops, Iops = build_ops(cert)
    print("sqrt enclosures validated; operators built")
    nfail = 0
    for p in cert["points"]:
        site = p["site"]
        B = [pf(x) for x in p["B_mT"]]
        H = build_H(cert, site, B, Sops, Iops)
        counts = {}
        ok = True
        for srec in p["shifts"]:
            mu = pf(srec["mu"]); claimed = srec["neg_count"]
            c = neg_count(H, mu)
            if c is None:
                print(f"  FAIL [{p['label']}]: indefinite pivot at mu={float(mu):.9g}")
                ok = False; continue
            if c != claimed:
                print(f"  FAIL [{p['label']}]: count {c} != claimed {claimed} at mu={float(mu):.9g}")
                ok = False; continue
            counts[mu] = c
        ebr = [(pf(a), pf(b)) for a, b in p["eigenvalue_brackets_MHz"]]
        for n, (lo, hi) in enumerate(ebr):
            # pinning: count(mu1) <= n at some mu1 >= lo  ==> lambda_n >= mu1 >= lo;
            #          count(mu2) >= n+1 at some mu2 <= hi ==> lambda_n < mu2 <= hi.
            has_lo = any(m >= lo and c <= n for m, c in counts.items())
            has_hi = any(m <= hi and c >= n+1 for m, c in counts.items())
            if not (has_lo and has_hi and lo <= hi):
                print(f"  FAIL [{p['label']}]: eigenvalue {n} bracket not certified")
                ok = False
        for t in p["transitions"]:
            i, j = t["i"], t["j"]
            flo, fhi = pf(t["f_lo"]), pf(t["f_hi"])
            lo_ok = ebr[j][0] - ebr[i][1] >= flo
            hi_ok = ebr[j][1] - ebr[i][0] <= fhi
            if not (lo_ok and hi_ok):
                print(f"  FAIL [{p['label']}]: transition ({i},{j}) bracket inconsistent")
                ok = False
            else:
                pub = t.get("published_MHz")
                if pub is not None:
                    d = float(F(pub) - (flo+fhi)/2)
                    print(f"  ok  [{p['label']}] f({i},{j}) in [{float(flo):.6f},{float(fhi):.6f}] "
                          f"MHz; published {pub} (delta {d:+.3f})")
        if not ok: nfail += 1
    if nfail == 0:
        print("CERTIFICATE VERIFIED")
        return 0
    print(f"CERTIFICATE FAILED: {nfail} point(s) with failures")
    return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "certificate_pilot.json"))
