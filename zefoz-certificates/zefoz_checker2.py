#!/usr/bin/env python3
"""Standalone checker for certificate2.json (PUBLISHABLE).

Verifies, using ONLY the Python 3 standard library (fractions, json, math, sys),
every certified claim of the Phase-1 ZEFOZ certificate for the 167Er3+:Y2SiO5
ground-manifold (Z1) spin Hamiltonian

    H(B) = I.A.S + I.Q.I + muB * B.g.S - muN*gn * B.I     (MHz; B in mT),

S=1/2, I=7/2 (dim 16), A, Q, g exactly the rational matrices in the certificate
(arXiv:2412.10126v3 Appendix B).

Checked claims, per certificate point (nothing from the generator is trusted;
everything is recomputed here from B*, the dyadic eigenvector matrix V, the
Rayleigh values wt, and the certified LDL^T shift counts):

  1. sqrt enclosures validated by squaring; H(B*) rebuilt in exact rational
     rectangle-interval arithmetic with outward rounding.
  2. Eigenvalue brackets: interval LDL^T of H - mu*I at every certified shift;
     sign-definite pivots => Sylvester inertia => certified counts; counts pin
     each bracket.  Brackets must be pairwise disjoint (simple spectrum).
  3. Davis-Kahan: residual norms of the stored eigenvector columns against wt,
     certified gaps from the brackets => sin(theta) bounds => enclosures of the
     exact (phase-aligned) eigenvectors.
  4. Hellmann-Feynman gradient enclosure of f_ij = lambda_j - lambda_i at B*;
     the recomputed enclosure must lie inside the stated one, and the stated
     |grad| bound eps must dominate the recomputed enclosure norm.
  5. Signed second-order-perturbation Hessian enclosure (3x3); recomputed
     enclosure must lie inside the stated one; Hessian eigenvalue brackets via
     Gershgorin discs of R^T Hess R with component merging and the exact
     Ostrowski congruence correction (R^T R - I bounded); the stated brackets
     must contain the recomputed ones; the stated signature must follow.
  6. Krawczyk existence-and-uniqueness box (Table-5 points): with the stated
     rational C and box radius r, the operator
        K - B* = -C G  +  (I - C F'(X)) [-r, r]^3
     is recomputed, where F'(X) is the Hessian enclosure inflated entrywise by
     9*sqrt(3)*M*r, M = 192 D^3 (1/gam_i^2 + 1/gam_j^2), gam = certified gap
     lower bounds over X, D = certified bound on sup_{|e|=1} ||dH_e||_2.
     K must lie strictly inside the box and det C != 0 exactly.  This proves an
     exact stationary point of f_ij exists, and is unique, within the box.
  7. Time-reversal identity: the stated signed permutation M16 satisfies
     M16 M16^T = I and, in EXACT symbolic arithmetic over Q[sqrt(d)],
     M16 conj(H0) M16^T = H0 and M16 conj(Zk) M16^T = -Zk (k=1,2,3, both
     sites) => the spectrum of H(B) is even in B => with the certified simple
     zero-field spectrum, grad f_ij(0) = 0 exactly for all 120 pairs.

Exit code 0 and final line "CERTIFICATE VERIFIED" iff every claim checks.

Usage: python3 zefoz_checker2.py certificate2.json
"""
import sys, json, math
from fractions import Fraction as F

PREC = 2**200
N = 16

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

def pf(s): return F(s)
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

def sqrt_hi(x):
    """rational upper bound for sqrt(x >= 0)."""
    if x == 0: return F(0)
    b = 130
    s = math.isqrt((x.numerator << (2*b)) // x.denominator) + 1
    return F(s, 1 << b)

def iv_abs_hi(c):
    return max(abs(c.re.lo), abs(c.re.hi)) + max(abs(c.im.lo), abs(c.im.hi))

def op2_hi(M):
    n = len(M)
    ab = [[iv_abs_hi(M[i][j]) for j in range(n)] for i in range(n)]
    c1 = max(sum(ab[i][j] for i in range(n)) for j in range(n))
    ci = max(sum(ab[i][j] for j in range(n)) for i in range(n))
    return sqrt_hi(c1*ci)

def col_norm_hi(col):
    s = F(0)
    for c in col:
        a = max(abs(c.re.lo), abs(c.re.hi))
        b = max(abs(c.im.lo), abs(c.im.hi))
        s += a*a + b*b
    return sqrt_hi(s)

def inner(u, w):
    s = u[0].conj()*w[0]
    for k in range(1, len(u)):
        s = s + u[k].conj()*w[k]
    return s

# ------------------------------------------------------------- operator build
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

def site_mats(cert, site):
    sd = cert["sites"][str(site)]
    A = [[pf(x) for x in r] for r in sd["A"]]
    Q = [[pf(x) for x in r] for r in sd["Q"]]
    g = [[pf(x) for x in r] for r in sd["g"]]
    return A, Q, g

def build_H0_Zk(cert, site, Sops, Iops):
    A, Q, g = site_mats(cert, site)
    muB = pf(cert["constants"]["muB_MHz_per_mT"])
    muN = pf(cert["constants"]["muN_MHz_per_mT"])
    gn  = pf(cert["constants"]["gn"])
    H0 = [[cF(0) for _ in range(N)] for _ in range(N)]
    for a in range(3):
        for b in range(3):
            IS = matmul(Iops[a], Sops[b])
            II = matmul(Iops[a], Iops[b])
            ca, cb = Cv(Iv(A[a][b])), Cv(Iv(Q[a][b]))
            for i in range(N):
                for j in range(N):
                    H0[i][j] = H0[i][j] + ca*IS[i][j] + cb*II[i][j]
    Zk = []
    for k in range(3):
        M = [[cF(0) for _ in range(N)] for _ in range(N)]
        for l in range(3):
            c = Cv(Iv(muB*g[k][l]))
            for i in range(N):
                for j in range(N):
                    M[i][j] = M[i][j] + c*Sops[l][i][j]
        c = Cv(Iv(-muN*gn))
        for i in range(N):
            for j in range(N):
                M[i][j] = M[i][j] + c*Iops[k][i][j]
        Zk.append(M)
    return H0, Zk

def H_at(H0, Zk, B):
    M = [[H0[i][j] for j in range(N)] for i in range(N)]
    for k in range(3):
        if B[k] == 0: continue
        c = Cv(Iv(B[k]))
        for i in range(N):
            for j in range(N):
                M[i][j] = M[i][j] + c*Zk[k][i][j]
    return M

def neg_count(H, mu):
    A = [[Cv(H[i][j].re, H[i][j].im) for j in range(N)] for i in range(N)]
    for i in range(N):
        A[i][i] = Cv(A[i][i].re - Iv(mu), A[i][i].im)
    neg = 0
    for k in range(N):
        d = A[k][k].re
        if d.hi < 0: neg += 1
        elif d.lo > 0: pass
        else: return None
        for i in range(k+1, N):
            for j in range(k+1, i+1):
                A[i][j] = A[i][j] - (A[i][k]*A[j][k].conj()).divr(d)
    return neg

# ------------------------------------------- exact symbolic ring Q[sqrt(d)]
def _sqfree(n):
    s, d, r = 1, 2, n
    while d*d <= r:
        while r % (d*d) == 0:
            r //= d*d; s *= d
        d += 1
    return r, s

def sym(q=0, rad=1, coeff=None):
    d = {}
    if coeff is None:
        if q: d[1] = F(q)
    else:
        r, s = _sqfree(rad)
        if coeff: d[r] = F(coeff)*s
    return d

def sym_add(a, b):
    out = dict(a)
    for r, c in b.items():
        out[r] = out.get(r, F(0)) + c
        if out[r] == 0: del out[r]
    return out

def sym_mul(a, b):
    out = {}
    for r1, c1 in a.items():
        for r2, c2 in b.items():
            r, s = _sqfree(r1*r2)
            c = c1*c2*s
            if c:
                out[r] = out.get(r, F(0)) + c
                if out[r] == 0: del out[r]
    return out

def sym_scal(q, a):
    return {r: F(q)*c for r, c in a.items() if F(q)*c != 0}

def build_sym(cert, site):
    A, Q, g = site_mats(cert, site)
    muB = pf(cert["constants"]["muB_MHz_per_mT"])
    muN = pf(cert["constants"]["muN_MHz_per_mT"])
    gn  = pf(cert["constants"]["gn"])
    half = F(1, 2)
    Sx = [[(sym(), sym()), (sym(half), sym())], [(sym(half), sym()), (sym(), sym())]]
    Sy = [[(sym(), sym()), (sym(), sym(-half))], [(sym(), sym(half)), (sym(), sym())]]
    Sz = [[(sym(half), sym()), (sym(), sym())], [(sym(), sym()), (sym(-half), sym())]]
    lad = [7, 12, 15, 16, 15, 12, 7]
    Ix = [[(sym(), sym()) for _ in range(8)] for _ in range(8)]
    Iy = [[(sym(), sym()) for _ in range(8)] for _ in range(8)]
    Iz = [[(sym(), sym()) for _ in range(8)] for _ in range(8)]
    for k in range(7):
        c = sym(rad=lad[k], coeff=half)
        Ix[k][k+1] = (c, sym()); Ix[k+1][k] = (c, sym())
        Iy[k][k+1] = (sym(), sym_scal(-1, c)); Iy[k+1][k] = (sym(), c)
    for k in range(8):
        Iz[k][k] = (sym(F(7, 2) - k), sym())
    def ckron(Am, Bm):
        na, nb = len(Am), len(Bm)
        out = [[None]*(na*nb) for _ in range(na*nb)]
        for i in range(na*nb):
            for j in range(na*nb):
                a, b = Am[i//nb][j//nb], Bm[i%nb][j%nb]
                re = sym_add(sym_mul(a[0], b[0]), sym_scal(-1, sym_mul(a[1], b[1])))
                im = sym_add(sym_mul(a[0], b[1]), sym_mul(a[1], b[0]))
                out[i][j] = (re, im)
        return out
    def cmatmul(Am, Bm):
        n = len(Am)
        out = [[(sym(), sym()) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for k in range(n):
                a = Am[i][k]
                if not a[0] and not a[1]: continue
                for j in range(n):
                    b = Bm[k][j]
                    if not b[0] and not b[1]: continue
                    re = sym_add(sym_mul(a[0], b[0]), sym_scal(-1, sym_mul(a[1], b[1])))
                    im = sym_add(sym_mul(a[0], b[1]), sym_mul(a[1], b[0]))
                    out[i][j] = (sym_add(out[i][j][0], re), sym_add(out[i][j][1], im))
        return out
    I2m = [[(sym(1 if i == j else 0), sym()) for j in range(2)] for i in range(2)]
    I8m = [[(sym(1 if i == j else 0), sym()) for j in range(8)] for i in range(8)]
    Sops = [ckron(s, I8m) for s in (Sx, Sy, Sz)]
    Iops = [ckron(I2m, i) for i in (Ix, Iy, Iz)]
    H0 = [[(sym(), sym()) for _ in range(N)] for _ in range(N)]
    for a in range(3):
        for b in range(3):
            IS = cmatmul(Iops[a], Sops[b])
            II = cmatmul(Iops[a], Iops[b])
            for i in range(N):
                for j in range(N):
                    re = sym_add(sym_scal(A[a][b], IS[i][j][0]), sym_scal(Q[a][b], II[i][j][0]))
                    im = sym_add(sym_scal(A[a][b], IS[i][j][1]), sym_scal(Q[a][b], II[i][j][1]))
                    H0[i][j] = (sym_add(H0[i][j][0], re), sym_add(H0[i][j][1], im))
    Zk = []
    for k in range(3):
        Mz = [[(sym(), sym()) for _ in range(N)] for _ in range(N)]
        for l in range(3):
            c = muB*g[k][l]
            for i in range(N):
                for j in range(N):
                    Mz[i][j] = (sym_add(Mz[i][j][0], sym_scal(c, Sops[l][i][j][0])),
                                sym_add(Mz[i][j][1], sym_scal(c, Sops[l][i][j][1])))
        c = -muN*gn
        for i in range(N):
            for j in range(N):
                Mz[i][j] = (sym_add(Mz[i][j][0], sym_scal(c, Iops[k][i][j][0])),
                            sym_add(Mz[i][j][1], sym_scal(c, Iops[k][i][j][1])))
        Zk.append(Mz)
    return H0, Zk

def check_tr(cert, M16):
    # signed permutation with orthogonality
    for i in range(N):
        nz = [a for a in range(N) if M16[i][a] != 0]
        assert len(nz) == 1 and M16[i][nz[0]] in (1, -1), "M16 row not signed unit"
    for a in range(N):
        nz = [i for i in range(N) if M16[i][a] != 0]
        assert len(nz) == 1, "M16 column not signed unit"
    col_of = [next(a for a in range(N) if M16[i][a] != 0) for i in range(N)]
    for site in (1, 2):
        H0s, Zks = build_sym(cert, site)
        def conj_transform(A, sign):
            for i in range(N):
                a = col_of[i]
                for j in range(N):
                    b = col_of[j]
                    re, im = A[a][b]
                    s = M16[i][a]*M16[j][b]
                    assert sym_scal(s, re) == sym_scal(sign, A[i][j][0]), ("re", i, j)
                    assert sym_scal(-s, im) == sym_scal(sign, A[i][j][1]), ("im", i, j)
        conj_transform(H0s, 1)
        for k in range(3):
            conj_transform(Zks[k], -1)
    return True

# ----------------------------------------------------------- per-point checks
def iv_contains(outer_lo, outer_hi, inner_lo, inner_hi):
    return outer_lo <= inner_lo and inner_hi <= outer_hi

def hess_eig_brackets(Hess, Rd):
    T1 = [[None]*3 for _ in range(3)]
    for a in range(3):
        for l in range(3):
            s = Rd[0][a]*Hess[0][l]
            for k in range(1, 3):
                s = s + Rd[k][a]*Hess[k][l]
            T1[a][l] = s
    T = [[None]*3 for _ in range(3)]
    for a in range(3):
        for b in range(3):
            s = T1[a][0]*Rd[0][b]
            for l in range(1, 3):
                s = s + T1[a][l]*Rd[l][b]
            T[a][b] = s
    discs = []
    for a in range(3):
        off = sum(max(abs(T[a][b].lo), abs(T[a][b].hi)) for b in range(3) if b != a)
        discs.append([T[a][a].lo - off, T[a][a].hi + off])
    discs.sort(key=lambda t: t[0])
    comps = [discs[0][:]]; counts = [1]
    for d in discs[1:]:
        if d[0] <= comps[-1][1]:
            comps[-1][1] = max(comps[-1][1], d[1]); counts[-1] += 1
        else:
            comps.append(d[:]); counts.append(1)
    raw = []
    for c, k in zip(comps, counts):
        raw += [tuple(c)]*k
    E = [[None]*3 for _ in range(3)]
    for a in range(3):
        for b in range(3):
            s = Rd[0][a]*Rd[0][b]
            for k in range(1, 3):
                s = s + Rd[k][a]*Rd[k][b]
            E[a][b] = s - Iv(F(1)) if a == b else s
    e = max(sum(max(abs(E[a][b].lo), abs(E[a][b].hi)) for b in range(3)) for a in range(3))
    assert e < 1, "rotation too far from orthogonal"
    theta_inv = Iv(1/(F(1)+e), 1/(F(1)-e))
    return [tuple(x for x in ((Iv(lo, hi)*theta_inv).lo, (Iv(lo, hi)*theta_inv).hi))
            for lo, hi in raw]

def verify_point(cert, p, H0, Zk, znb, D_hi):
    ok = True
    B = [pf(x) for x in p["B_mT"]]
    H = H_at(H0, Zk, B)
    wt = [pf(x) for x in p["wt_MHz"]]
    Vd = [[Cv(Iv(pf(p["eigenvectors_dyadic"][r][c][0])),
             Iv(pf(p["eigenvectors_dyadic"][r][c][1]))) for c in range(N)]
          for r in range(N)]
    ebr = [(pf(a), pf(b)) for a, b in p["eigenvalue_brackets_MHz"]]

    # 1. LDL counts and bracket pinning
    counts = {}
    for srec in p["shifts"]:
        mu = pf(srec["mu"]); claimed = srec["neg_count"]
        c = neg_count(H, mu)
        if c is None or c != claimed:
            print(f"  FAIL [{p['label']}]: LDL count at mu={float(mu):.9g}: "
                  f"got {c}, claimed {claimed}")
            return False
        counts[mu] = c
    for n, (lo, hi) in enumerate(ebr):
        has_lo = any(m >= lo and c <= n for m, c in counts.items())
        has_hi = any(m <= hi and c >= n+1 for m, c in counts.items())
        if not (has_lo and has_hi and lo <= hi):
            print(f"  FAIL [{p['label']}]: eigenvalue {n} bracket not certified")
            return False
    for n in range(N-1):
        if not ebr[n][1] < ebr[n+1][0]:
            print(f"  FAIL [{p['label']}]: brackets {n},{n+1} overlap (not simple)")
            return False

    # 2. residuals, norms, Davis-Kahan
    HV = matmul(H, Vd)
    res, nlo, nhi = [], [], []
    for n in range(N):
        col = [HV[r][n] - Cv(Iv(wt[n]))*Vd[r][n] for r in range(N)]
        res.append(col_norm_hi(col))
        s = F(0)
        for r in range(N):
            c = Vd[r][n]
            s += c.re.lo*c.re.lo + c.im.lo*c.im.lo
        hi = sqrt_hi(s)
        nlo.append(s/hi); nhi.append(hi)
        if not (wt[n] >= ebr[n][0] - F(1, 10**6) and wt[n] <= ebr[n][1] + F(1, 10**6)):
            pass  # wt need not lie in the bracket; DK uses distances to other levels only
    st = []
    for n in range(N):
        gap = None
        for m in range(N):
            if m == n: continue
            d = max(wt[n] - ebr[m][1], ebr[m][0] - wt[n])
            if d <= 0:
                print(f"  FAIL [{p['label']}]: wt[{n}] not separated from bracket {m}")
                return False
            gap = d if gap is None else min(gap, d)
        st.append(res[n] / (nlo[n] * gap))
    SQ2 = sqrt_hi(F(2))
    delta = [SQ2*s for s in st]

    pairs = p["pairs"]
    lv = sorted(set([q["i"] for q in pairs] + [q["j"] for q in pairs]))
    Wrows = {}
    for k in range(3):
        ZV = matmul(Zk[k], Vd)
        for n in lv:
            vn = [Vd[r][n] for r in range(N)]
            row = []
            for m in range(N):
                num = inner(vn, [ZV[r][m] for r in range(N)])
                pr = Iv(nlo[n]*nlo[m], nhi[n]*nhi[m])
                base = num.divr(pr)
                err = znb[k]*(delta[n] + delta[m] + delta[n]*delta[m])
                E = Iv(-err, err)
                row.append(Cv(base.re + E, base.im + E))
            Wrows[(k, n)] = row

    for q in pairs:
        i, j = q["i"], q["j"]
        # 3. gradient
        g_enc = [Wrows[(k, j)][j].re - Wrows[(k, i)][i].re for k in range(3)]
        g_stated = [(pf(a), pf(b)) for a, b in q["gradient_enclosure_MHz_per_mT"]]
        for k in range(3):
            if not iv_contains(g_stated[k][0], g_stated[k][1], g_enc[k].lo, g_enc[k].hi):
                print(f"  FAIL [{p['label']}] ({i},{j}): gradient component {k} "
                      f"recomputed enclosure escapes stated one")
                ok = False
        eps_stated = pf(q["grad_norm_upper_MHz_per_mT"])
        eps_re = sqrt_hi(sum(max(abs(a), abs(b))**2 for a, b in g_stated))
        if eps_stated < eps_re:
            print(f"  FAIL [{p['label']}] ({i},{j}): stated eps below recomputed bound")
            ok = False

        # 4. Hessian
        Hess = [[Iv(F(0)) for _ in range(3)] for _ in range(3)]
        for n, sgn in ((j, 1), (i, -1)):
            for m in range(N):
                if m == n: continue
                den = Iv(ebr[n][0] - ebr[m][1], ebr[n][1] - ebr[m][0])
                for k in range(3):
                    for l in range(k, 3):
                        a = Wrows[(k, n)][m]; b = Wrows[(l, n)][m]
                        rec_ = a.re*b.re + a.im*b.im
                        Hess[k][l] = Hess[k][l] + rec_.divr(den)*Iv(F(2*sgn))
        for k in range(3):
            for l in range(k):
                Hess[k][l] = Hess[l][k]
        Hs = [[(pf(q["hessian_enclosure_MHz_per_mT2"][k][l][0]),
                pf(q["hessian_enclosure_MHz_per_mT2"][k][l][1])) for l in range(3)]
              for k in range(3)]
        for k in range(3):
            for l in range(3):
                if not iv_contains(Hs[k][l][0], Hs[k][l][1], Hess[k][l].lo, Hess[k][l].hi):
                    print(f"  FAIL [{p['label']}] ({i},{j}): Hessian entry ({k},{l}) "
                          f"recomputed enclosure escapes stated one")
                    ok = False
        HsIv = [[Iv(Hs[k][l][0], Hs[k][l][1]) for l in range(3)] for k in range(3)]
        Rd = [[Iv(pf(q["hessian_rotation_dyadic"][r][c])) for c in range(3)]
              for r in range(3)]
        heig_re = hess_eig_brackets(HsIv, Rd)
        heig_st = [(pf(a), pf(b)) for a, b in q["hessian_eig_brackets_MHz_per_mT2"]]
        for (slo, shi), (rlo, rhi) in zip(heig_st, heig_re):
            if not iv_contains(slo, shi, rlo, rhi):
                print(f"  FAIL [{p['label']}] ({i},{j}): Hessian eigenvalue bracket "
                      f"does not contain recomputed one")
                ok = False
        sig_re = ["+" if lo > 0 else ("-" if hi < 0 else "0") for lo, hi in heig_st]
        if sig_re != q["hessian_signature"]:
            print(f"  FAIL [{p['label']}] ({i},{j}): signature mismatch")
            ok = False

        # 5. Krawczyk
        if "krawczyk" in q:
            kw = q["krawczyk"]
            r = pf(kw["box_radius_mT"])
            Cd = [[pf(kw["C_dyadic"][k][l]) for l in range(3)] for k in range(3)]
            detC = (Cd[0][0]*(Cd[1][1]*Cd[2][2]-Cd[1][2]*Cd[2][1])
                    - Cd[0][1]*(Cd[1][0]*Cd[2][2]-Cd[1][2]*Cd[2][0])
                    + Cd[0][2]*(Cd[1][0]*Cd[2][1]-Cd[1][1]*Cd[2][0]))
            if detC == 0:
                print(f"  FAIL [{p['label']}] ({i},{j}): C singular")
                ok = False
            infl = D_hi * sqrt_hi(F(3)) * r
            gams = {}
            bad = False
            for n in (i, j):
                gap = None
                for m in range(N):
                    if m == n: continue
                    d = max(ebr[n][0] - ebr[m][1], ebr[m][0] - ebr[n][1])
                    if d <= 0: bad = True; break
                    gap = d if gap is None else min(gap, d)
                if bad: break
                gams[n] = gap - 2*infl
                if gams[n] <= 0: bad = True
            if bad:
                print(f"  FAIL [{p['label']}] ({i},{j}): gap bound over box not positive")
                ok = False
            else:
                Mbd = 192*D_hi**3*(1/(gams[i]*gams[i]) + 1/(gams[j]*gams[j]))
                Lent = 9*Mbd*sqrt_hi(F(3))*r
                FpX = [[HsIv[k][l] + Iv(-Lent, Lent) for l in range(3)] for k in range(3)]
                contained = True
                for k in range(3):
                    acc = Iv(F(0))
                    for l in range(3):
                        acc = acc + Iv(Cd[k][l])*Iv(g_stated[l][0], g_stated[l][1])
                    acc = Iv(-acc.hi, -acc.lo)
                    for l in range(3):
                        m = Iv(F(1 if k == l else 0))
                        s = Iv(Cd[k][0])*FpX[0][l]
                        for a in range(1, 3):
                            s = s + Iv(Cd[k][a])*FpX[a][l]
                        acc = acc + (m - s)*Iv(-r, r)
                    if not (-r < acc.lo and acc.hi < r):
                        contained = False
                if not contained:
                    print(f"  FAIL [{p['label']}] ({i},{j}): Krawczyk K(X) not inside X")
                    ok = False
                elif not kw.get("contraction", False):
                    print(f"  FAIL [{p['label']}] ({i},{j}): contraction flag false but "
                          f"K(X) verified -- inconsistent certificate")
                    ok = False
        if ok:
            heb = q["hessian_eig_brackets_MHz_per_mT2"]
            lo0 = float(pf(heb[0][0])); hi2 = float(pf(heb[2][1]))
            msg = f"  ok  [{p['label']}] ({i},{j}): |grad| <= {float(eps_stated):.2e}, " \
                  f"Hess eigs in [{lo0:+.3e},{hi2:+.3e}], sig {''.join(q['hessian_signature'])}"
            if "krawczyk" in q:
                msg += f", Krawczyk r={float(pf(q['krawczyk']['box_radius_mT'])):.1e} mT OK"
            print(msg)
    # transition bracket
    if "transition_bracket_MHz" in p:
        i, j = pairs[0]["i"], pairs[0]["j"]
        lo, hi = pf(p["transition_bracket_MHz"][0]), pf(p["transition_bracket_MHz"][1])
        if not (lo <= ebr[j][0] - ebr[i][1] and ebr[j][1] - ebr[i][0] <= hi):
            print(f"  FAIL [{p['label']}]: transition bracket inconsistent")
            ok = False
    return ok

def main(path):
    cert = json.load(open(path))
    Sops, Iops = build_ops(cert)
    print("sqrt enclosures validated; operators built")
    nfail = 0
    tr_points = [p for p in cert["points"] if p.get("kind") == "time_reversal_identity"]
    assert len(tr_points) == 1, "missing time-reversal identity"
    check_tr(cert, tr_points[0]["M16"])
    print("time-reversal identity verified EXACTLY (both sites): spectrum even in B;")
    print("  => with certified simple zero-field spectra, grad f_ij(0) = 0 for all pairs")
    cacheHZ = {}
    for site in (1, 2):
        H0, Zk = build_H0_Zk(cert, site, Sops, Iops)
        znb = [op2_hi(Zk[k]) for k in range(3)]
        D_hi = sqrt_hi(sum(z*z for z in znb))
        cacheHZ[site] = (H0, Zk, znb, D_hi)
    for p in cert["points"]:
        if p.get("kind") == "time_reversal_identity": continue
        H0, Zk, znb, D_hi = cacheHZ[p["site"]]
        if not verify_point(cert, p, H0, Zk, znb, D_hi):
            nfail += 1
    if nfail == 0:
        print("CERTIFICATE VERIFIED")
        return 0
    print(f"CERTIFICATE FAILED: {nfail} point(s) with failures")
    return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "certificate2.json"))
