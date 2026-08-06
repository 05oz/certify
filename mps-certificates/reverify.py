#!/usr/bin/env python3
"""
Independent re-verification of the claimed object:

  A^0 = [[1,0],[0,-1]],  A^1 = [[-2,-1],[1,0]]
  |psi_L> = sum_s Tr(A^{s_1}...A^{s_L}) |s...>   (periodic)
  claimed: H |psi_L> = 0 exactly for EVERY L, where
  H = - sum_{i=1}^{L} (1 + X_i)(X_{i+1} + Z_{i+1})   (periodic, site L+1 = site 1)

Written from scratch. No imports from the crashed agent's code. Pure Python
integers and Fractions only — every check is exact.

Proof structure verified here:
  (P1) The telescoping certificate: with the CLOSED-FORM bond operator
       h = -(1+X) (x) (X+Z), exhibit 2x2 integer matrices C^0, C^1 with
         sum_{s,t} <uv|h|st> A^s A^t  =  C^u A^v - A^u C^v      (all u,v)
       This is a finite identity (16 scalar equations). Given it, for any L:
         (H psi)_u = sum_i Tr(A^{u_1}..[C^{u_i}A^{u_{i+1}} - A^{u_i}C^{u_{i+1}}]..A^{u_L})
       which telescopes to zero around the periodic trace. Hence H|psi_L> = 0
       for every L. We derive C ourselves by solving the linear system exactly.
  (P2) Dense substitution: independently build psi_L and apply H directly to it
       (never forming H from the certificate) and assert H psi = 0 exactly,
       for L = 3..10.
  (P3) Sanity: psi_L != 0 for those L; h is real-symmetric (H Hermitian).
  (P4) Non-triviality: exact Schmidt ranks over Q.
       - contiguous half-cut rank at L=4,6,8 (claim: 4 = D^2)
       - odd/even-site bipartition rank at L=4,6,8 (claim: 2,4,8 growing)
       A sum of k product states has rank <= k across every bipartition, so
       growing rank => not a finite cat of product states.
  (P5) Irreducibility: {I, A0, A1, A0A1} spans M_2 (det of coefficient matrix != 0).
  (P6) Not frustration-free: a single bond term applied to psi_4 is nonzero.
"""
from fractions import Fraction
from itertools import product
import sys

FAIL = []

def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAIL.append(name)

# ---------- exact 2x2 integer matrix helpers ----------
def mmul(X, Y):
    return [[sum(X[i][k]*Y[k][j] for k in range(len(Y))) for j in range(len(Y[0]))]
            for i in range(len(X))]

def madd(X, Y):
    return [[X[i][j] + Y[i][j] for j in range(len(X[0]))] for i in range(len(X))]

def msub(X, Y):
    return [[X[i][j] - Y[i][j] for j in range(len(X[0]))] for i in range(len(X))]

def mscale(c, X):
    return [[c*X[i][j] for j in range(len(X[0]))] for i in range(len(X))]

def mzero(X):
    return all(v == 0 for row in X for v in row)

A = {0: [[1, 0], [0, -1]], 1: [[-2, -1], [1, 0]]}

# ---------- the Hamiltonian: closed form bond operator ----------
# single-site operators in basis |0>,|1>
X1 = [[0, 1], [1, 0]]
Z1 = [[1, 0], [0, -1]]
I1 = [[1, 0], [0, 1]]

def kron(P, Q):
    n, m = len(P), len(Q)
    return [[P[i][j]*Q[k][l] for j in range(n) for l in range(m)]
            for i in range(n) for k in range(m)]

h_closed = mscale(-1, kron(madd(I1, X1), madd(X1, Z1)))   # -(1+X) (x) (X+Z)

# (P3a) Hermiticity: real symmetric
check("h_closed is real-symmetric (H Hermitian)",
      all(h_closed[a][b] == h_closed[b][a] for a in range(4) for b in range(4)))

# ---------- (P1) derive C^0, C^1 exactly and verify the certificate ----------
# LHS(u,v) = sum_{s,t} h[(u,v),(s,t)] A^s A^t   with row index u*2+v, col s*2+t
def LHS(h, u, v):
    out = [[0, 0], [0, 0]]
    for s in range(2):
        for t in range(2):
            out = madd(out, mscale(h[u*2+v][s*2+t], mmul(A[s], A[t])))
    return out

# Solve linear system for 8 unknowns c = (C0_00,C0_01,C0_10,C0_11,C1_00,...,C1_11):
#   C^u A^v - A^u C^v = LHS(u,v)  for all u,v  -> 16 scalar equations.
# Build matrix rows exactly with Fractions and Gaussian eliminate.
def unknown_matrix(u, i, j):
    """C^u as a matrix with 1 in (i,j), else 0 — used to build columns."""
    M = [[0, 0], [0, 0]]
    M[i][j] = 1
    return M

cols = []   # each column: the 16-vector of (C^u A^v - A^u C^v) entries for basis unknown
basis_idx = [(u, i, j) for u in range(2) for i in range(2) for j in range(2)]
for (u0, i0, j0) in basis_idx:
    Cb = {0: [[0, 0], [0, 0]], 1: [[0, 0], [0, 0]]}
    Cb[u0] = unknown_matrix(u0, i0, j0)
    colvec = []
    for u in range(2):
        for v in range(2):
            M = msub(mmul(Cb[u], A[v]), mmul(A[u], Cb[v]))
            colvec.extend([M[0][0], M[0][1], M[1][0], M[1][1]])
    cols.append(colvec)

rhs = []
for u in range(2):
    for v in range(2):
        M = LHS(h_closed, u, v)
        rhs.extend([M[0][0], M[0][1], M[1][0], M[1][1]])

# solve 16x8 least-structure system exactly (find ANY exact solution)
Mrows = [[Fraction(cols[c][r]) for c in range(8)] + [Fraction(rhs[r])] for r in range(16)]
# Gaussian elimination
nrow, ncol = 16, 8
piv_of_col = {}
r = 0
for c in range(ncol):
    p = next((i for i in range(r, nrow) if Mrows[i][c] != 0), None)
    if p is None:
        continue
    Mrows[r], Mrows[p] = Mrows[p], Mrows[r]
    pivval = Mrows[r][c]
    Mrows[r] = [x / pivval for x in Mrows[r]]
    for i in range(nrow):
        if i != r and Mrows[i][c] != 0:
            f = Mrows[i][c]
            Mrows[i] = [a - f*b for a, b in zip(Mrows[i], Mrows[r])]
    piv_of_col[c] = r
    r += 1
consistent = all(Mrows[i][ncol] == 0 for i in range(r, nrow))
check("certificate linear system is consistent (a C exists)", consistent)

sol = [Fraction(0)] * 8
for c, rr in piv_of_col.items():
    sol[c] = Mrows[rr][ncol]
C = {0: [[sol[0], sol[1]], [sol[2], sol[3]]], 1: [[sol[4], sol[5]], [sol[6], sol[7]]]}
print("       derived C^0 =", [[str(x) for x in row] for row in C[0]])
print("       derived C^1 =", [[str(x) for x in row] for row in C[1]])

allzero = True
for u in range(2):
    for v in range(2):
        D = msub(LHS(h_closed, u, v), msub(mmul(C[u], A[v]), mmul(A[u], C[v])))
        if not mzero(D):
            allzero = False
check("(P1) telescoping certificate holds: sum h A A = C A - A C, all 16 entries, e = 0",
      allzero, "=> H|psi_L> = 0 exactly for EVERY L by the periodic telescope")

# cross-check against the journal's B (with its solver-h) is NOT needed for the
# proof; the closed-form certificate above independently covers all L.

# ---------- build psi_L and apply H densely, exact integers ----------
def psi(L):
    v = []
    for bits in product((0, 1), repeat=L):
        M = [[1, 0], [0, 1]]
        for s in bits:
            M = mmul(M, A[s])
        v.append(M[0][0] + M[1][1])   # trace
    return v   # index = binary number, s_1 = most significant

def apply_H(v, L):
    """(H v) with H = sum_i h_closed acting on sites (i, i+1 mod L)."""
    N = 1 << L
    out = [0] * N
    for idx in range(N):
        amp = v[idx]
        if amp == 0:
            continue
        bits = [(idx >> (L - 1 - k)) & 1 for k in range(L)]
        for i in range(L):
            j = (i + 1) % L
            s, t = bits[i], bits[j]
            for u in range(2):
                for w in range(2):
                    coef = h_closed[u*2+w][s*2+t]
                    if coef == 0:
                        continue
                    nb = list(bits)
                    nb[i], nb[j] = u, w
                    nidx = 0
                    for b in nb:
                        nidx = (nidx << 1) | b
                    out[nidx] += coef * amp
    return out

for L in range(3, 11):
    v = psi(L)
    nz = any(x != 0 for x in v)
    Hv = apply_H(v, L)
    check(f"(P2) L={L}: psi != 0 and H psi = 0 exactly (dense, integer)",
          nz and all(x == 0 for x in Hv))

# ---------- (P4) exact Schmidt ranks over Q ----------
def rank_exact(rows):
    M = [[Fraction(x) for x in row] for row in rows]
    if not M:
        return 0
    nr, nc = len(M), len(M[0])
    rk = 0
    for c in range(nc):
        p = next((i for i in range(rk, nr) if M[i][c] != 0), None)
        if p is None:
            continue
        M[rk], M[p] = M[p], M[rk]
        pv = M[rk][c]
        M[rk] = [x / pv for x in M[rk]]
        for i in range(nr):
            if i != rk and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f*b for a, b in zip(M[i], M[rk])]
        rk += 1
        if rk == nr:
            break
    return rk

def schmidt_rank(v, L, left_sites):
    """rank of the matrix v reshaped by (left_sites | rest)."""
    left = sorted(left_sites)
    right = [k for k in range(L) if k not in left_sites]
    rows = {}
    for idx, amp in enumerate(v):
        bits = [(idx >> (L - 1 - k)) & 1 for k in range(L)]
        li = 0
        for k in left:
            li = (li << 1) | bits[k]
        ri = 0
        for k in right:
            ri = (ri << 1) | bits[k]
        rows.setdefault(li, {})[ri] = amp
    nL, nR = 1 << len(left), 1 << len(right)
    mat = [[rows.get(i, {}).get(j, 0) for j in range(nR)] for i in range(nL)]
    return rank_exact(mat)

for L in (4, 6, 8):
    v = psi(L)
    rc = schmidt_rank(v, L, set(range(L // 2)))
    ro = schmidt_rank(v, L, set(range(0, L, 2)))
    check(f"(P4) L={L}: contiguous half-cut Schmidt rank = 4 (found {rc})", rc == 4)
    expected = {4: 2, 6: 4, 8: 8}[L]
    check(f"(P4) L={L}: odd/even bipartition Schmidt rank = {expected} (found {ro})",
          ro == expected)

# ---------- (P5) irreducibility ----------
mats = [I1, A[0], A[1], mmul(A[0], A[1])]
G = [[m[0][0], m[0][1], m[1][0], m[1][1]] for m in mats]
check("(P5) {I,A0,A1,A0A1} spans M_2 (bond dimension genuinely 2)",
      rank_exact(G) == 4)

# ---------- (P6) not frustration-free ----------
v4 = psi(4)
out = [0] * 16
for idx in range(16):
    amp = v4[idx]
    if amp == 0:
        continue
    bits = [(idx >> (3 - k)) & 1 for k in range(4)]
    s, t = bits[0], bits[1]
    for u in range(2):
        for w in range(2):
            coef = h_closed[u*2+w][s*2+t]
            if coef == 0:
                continue
            nb = list(bits)
            nb[0], nb[1] = u, w
            nidx = 0
            for b in nb:
                nidx = (nidx << 1) | b
            out[nidx] += coef * amp
check("(P6) single bond term h_{1,2} psi_4 != 0 (not frustration-free; genuinely telescoping)",
      any(x != 0 for x in out))

# ---------- (P7) East-type characterization: rotated form ----------
# Claim: a global spin rotation U with U X U^-1 = Z, U Z U^-1 = -X maps H to
#   H_east = -2 sum_i P0_i (Z_{i+1} - X_{i+1}),  P0 = |0><0| = diag(1,0)
#          =  2 sum_i n_i X_{i+1} - 2 sum_i n_i + 4 sum_i n_i n_{i+1}  (n = P0)
# i.e. a one-sided (East-type / facilitated) chain. Verify by exact conjugation:
# use V = sqrt(2) U = [[1,1],[-1,1]] so that V M V^T / 2 = U M U^-1 (V real orthogonal*sqrt2).
V = [[1, 1], [-1, 1]]
VT = [[1, -1], [1, 1]]
def conj2(M):   # U M U^-1 with exact integers: V M V^T / 2, entries must be even
    N = mmul(mmul(V, M), VT)
    assert all(x % 2 == 0 for row in N for x in row)
    return [[x // 2 for x in row] for row in N]
ok_rot = conj2(X1) == Z1 and conj2(Z1) == mscale(-1, X1)
P0 = [[1, 0], [0, 0]]
h_east = mscale(-2, kron(P0, msub(Z1, X1)))
VV = kron(V, V); VVT = kron(VT, VT)
N4 = mmul(mmul(VV, h_closed), VVT)
h_rot = [[x // 4 for x in row] for row in N4]  # (V(x)V) h (V(x)V)^T / 4
ok_conj = all(N4[i][j] % 4 == 0 for i in range(4) for j in range(4)) and h_rot == h_east
check("(P7) rotation X->Z, Z->-X maps H to the East-type form -2 sum_i P0_i (Z-X)_{i+1}",
      ok_rot and ok_conj)

print()
if FAIL:
    print("RESULT: FAILURES:", FAIL)
    sys.exit(1)
print("RESULT: ALL CHECKS PASS — the object is a real, exact, all-L eigenstate "
      "(E=0) of H = -sum_i (1+X_i)(X_{i+1}+Z_{i+1}), periodic, genuinely "
      "bond-dimension-2 and not a finite sum of product states.")
