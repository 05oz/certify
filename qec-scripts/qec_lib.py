"""qec_lib.py -- GF(2) linear algebra, code constructors, canonical CNF encoding
for certified minimum-distance computation of stabilizer codes.

Pipeline side (numpy allowed). The checkers are separate stdlib-only scripts
and none of them imports this module. They are not all code-disjoint from it:
check_witness.py and check_duality.py share 1 and 3 executable lines, both
boilerplate, but check_lower.py shares 36 of 358 and check_prof.py 40 of 387,
and in both the CSS-CNF construction is a transliteration of build_css_cnf
below -- same accumulators, same order of emission, and the same custom
assertion `assert sup, "zero pairing row"`. A CSS-encoding fault here would be
common-mode with those two checkers. The GF(2) layer (rref, rank, in_rowspace)
is a genuinely separate implementation: bitmask ints here, numpy arrays there,
zero substantive shared lines.
"""
import numpy as np


# ----------------------------------------------------------------------------
# GF(2) linear algebra
# ----------------------------------------------------------------------------

def rref(M):
    """Reduced row echelon form over GF(2). Returns (R, pivots)."""
    M = (np.array(M, dtype=np.uint8) % 2).copy()
    rows, cols = M.shape
    pivots = []
    r = 0
    for c in range(cols):
        if r >= rows:
            break
        pr = None
        for i in range(r, rows):
            if M[i, c]:
                pr = i
                break
        if pr is None:
            continue
        M[[r, pr]] = M[[pr, r]]
        for i in range(rows):
            if i != r and M[i, c]:
                M[i] ^= M[r]
        pivots.append(c)
        r += 1
    return M, pivots


def rank(M):
    if M.size == 0:
        return 0
    return len(rref(M)[1])


def kernel_basis(M):
    """Basis of {x : M x = 0 (mod 2)} as rows of a matrix."""
    M = np.array(M, dtype=np.uint8) % 2
    rows, cols = M.shape
    R, pivots = rref(M)
    free = [c for c in range(cols) if c not in pivots]
    basis = []
    for f in free:
        v = np.zeros(cols, dtype=np.uint8)
        v[f] = 1
        for i, p in enumerate(pivots):
            if R[i, f]:
                v[p] = 1
        basis.append(v)
    return np.array(basis, dtype=np.uint8) if basis else np.zeros((0, cols), np.uint8)


def in_rowspace(M, v):
    """Is v in the GF(2) rowspace of M?"""
    return rank(np.vstack([M, v[None, :]])) == rank(M)


def quotient_basis(K, S):
    """Rows of K spanning K's rowspace modulo rowspace(S): greedy selection."""
    picked = []
    base = S.copy()
    r0 = rank(base)
    for row in K:
        cand = np.vstack([base, row[None, :]])
        r1 = rank(cand)
        if r1 > r0:
            picked.append(row)
            base = cand
            r0 = r1
    return np.array(picked, dtype=np.uint8) if picked else np.zeros((0, K.shape[1]), np.uint8)


def css_logical_reps(HX, HZ):
    """Return (LX, LZ): X-logical reps = basis of ker HZ / row HX,
    Z-logical reps = basis of ker HX / row HZ."""
    LX = quotient_basis(kernel_basis(HZ), HX)
    LZ = quotient_basis(kernel_basis(HX), HZ)
    return LX, LZ


# ----------------------------------------------------------------------------
# Code constructors
# ----------------------------------------------------------------------------

def steane():
    H = np.array([[0, 0, 0, 1, 1, 1, 1],
                  [0, 1, 1, 0, 0, 1, 1],
                  [1, 0, 1, 0, 1, 0, 1]], dtype=np.uint8)
    return H.copy(), H.copy()   # HX, HZ


def five_qubit():
    """[[5,1,3]] perfect code, non-CSS. Returns symplectic stabilizer matrix
    S = [A|B] (rows: XZZXI cyclic) and logical reps L = [X̄; Z̄] symplectic."""
    paulis = ["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"]
    n = 5

    def to_symp(s):
        a = [1 if ch in "XY" else 0 for ch in s]
        b = [1 if ch in "ZY" else 0 for ch in s]
        return a + b
    S = np.array([to_symp(p) for p in paulis], dtype=np.uint8)
    L = np.array([to_symp("XXXXX"), to_symp("ZZZZZ")], dtype=np.uint8)
    return S, L, n


def golay():
    """[[23,1,7]] quantum Golay code. C = [23,12,7] binary Golay (cyclic,
    g = x^11+x^10+x^6+x^5+x^4+x^2+1), C_perp subset C; H_X = H_Z = basis of
    C_perp = parity-check matrix of C."""
    n = 23
    g = [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1]         # coeffs c_0..c_11
    G = np.zeros((12, n), dtype=np.uint8)
    for i in range(12):
        for j, c in enumerate(g):
            G[i, i + j] = c
    H = kernel_basis(G)                               # 11 x 23, generates C_perp
    assert H.shape == (11, n)
    # C_perp subset C check: every row of H must be in rowspace(G)
    for row in H:
        assert in_rowspace(G, row)
    return H.copy(), H.copy()


def rotated_surface(d):
    """Rotated surface code [[d^2,1,d]]. Qubit (r,c) -> index r*d+c."""
    assert d % 2 == 1
    n = d * d
    x_rows, z_rows = [], []
    for r in range(-1, d):
        for c in range(-1, d):
            qs = [(r + dr, c + dc) for dr in (0, 1) for dc in (0, 1)
                  if 0 <= r + dr < d and 0 <= c + dc < d]
            if len(qs) == 0:
                continue
            typ = 'X' if (r + c) % 2 == 0 else 'Z'
            interior = (0 <= r <= d - 2) and (0 <= c <= d - 2)
            if not interior:
                if len(qs) != 2:
                    continue          # corners
                # X boundary checks on top/bottom rows, Z on left/right cols
                if r in (-1, d - 1) and typ != 'X':
                    continue
                if c in (-1, d - 1) and typ != 'Z':
                    continue
            row = np.zeros(n, dtype=np.uint8)
            for (qr, qc) in qs:
                row[qr * d + qc] = 1
            (x_rows if typ == 'X' else z_rows).append(row)
    return np.array(x_rows, dtype=np.uint8), np.array(z_rows, dtype=np.uint8)


def bb_code(l, m, a_terms, b_terms):
    """Bivariate bicycle code (Bravyi et al., Nature 627 (2024)).
    a_terms/b_terms: lists of (i,j) meaning monomial x^i y^j.
    x = S_l ⊗ I_m, y = I_l ⊗ S_m acting on Z_l × Z_m; index (r,s) -> r*m+s.
    HX = [A|B], HZ = [B^T|A^T]; n = 2lm."""
    lm = l * m

    def mono(i, j):
        M = np.zeros((lm, lm), dtype=np.uint8)
        for r in range(l):
            for s in range(m):
                M[r * m + s, ((r + i) % l) * m + ((s + j) % m)] = 1
        return M
    A = np.zeros((lm, lm), dtype=np.uint8)
    for (i, j) in a_terms:
        A ^= mono(i, j)
    B = np.zeros((lm, lm), dtype=np.uint8)
    for (i, j) in b_terms:
        B ^= mono(i, j)
    HX = np.hstack([A, B])
    HZ = np.hstack([B.T % 2, A.T % 2])
    return HX % 2, HZ % 2


BB_PARAMS = {
    "bb72":  dict(l=6,  m=6,  a=[(3, 0), (0, 1), (0, 2)], b=[(0, 3), (1, 0), (2, 0)], nkd=(72, 12, 6)),
    "bb90":  dict(l=15, m=3,  a=[(9, 0), (0, 1), (0, 2)], b=[(0, 0), (2, 0), (7, 0)], nkd=(90, 8, 10)),
    "bb108": dict(l=9,  m=6,  a=[(3, 0), (0, 1), (0, 2)], b=[(0, 3), (1, 0), (2, 0)], nkd=(108, 8, 10)),
    "bb144": dict(l=12, m=6,  a=[(3, 0), (0, 1), (0, 2)], b=[(0, 3), (1, 0), (2, 0)], nkd=(144, 12, 12)),
    "bb288": dict(l=12, m=12, a=[(3, 0), (0, 2), (0, 7)], b=[(0, 3), (1, 0), (2, 0)], nkd=(288, 12, 18)),
}


# ----------------------------------------------------------------------------
# Canonical CNF encoding  (SPEC — the independent checker re-implements this)
#
# Instance CSS-X(H, L, K, forced):  "exists x in F_2^n with H x = 0,
#   at least one pairing row l in L with l·x = 1, wt(x) <= K, forced lits true"
# Variables: x_i = i+1 for qubit i (0-indexed).  Aux vars allocated in order:
#   (1) per row of H in row order: XOR chain aux (support sorted ascending;
#       u_1 := x_{s_1}; for j>=2 fresh u_j = u_{j-1} XOR x_{s_j}; assert ¬u_t)
#   (2) per row of L in row order: same chain, final var b_j (no assert)
#   (3) big clause (b_1 ... b_k)
#   (4) Sinz sequential at-most-K counter on x_1..x_n: vars s_{i,j},
#       i = 1..n-1 outer, j = 1..K inner
#   (5) unit clauses for forced literals, in given order
# XOR gate u = a ⊕ b emits, in order:
#   (-u a b) (-u -a -b) (u -a b) (u a -b)
# ----------------------------------------------------------------------------

class CNF:
    def __init__(self, nvars):
        self.nv = nvars
        self.clauses = []

    def new_var(self):
        self.nv += 1
        return self.nv

    def add(self, *lits):
        self.clauses.append(list(lits))


def _xor_chain(cnf, lits):
    """Return literal equal to XOR of lits (len >= 1)."""
    cur = lits[0]
    for lit in lits[1:]:
        u = cnf.new_var()
        a, b = cur, lit
        cnf.add(-u, a, b)
        cnf.add(-u, -a, -b)
        cnf.add(u, -a, b)
        cnf.add(u, a, -b)
        cur = u
    return cur


def _at_most_k(cnf, xs, K):
    """Sinz sequential counter, at-most-K over literals xs."""
    n = len(xs)
    if K >= n:
        return
    s = [[None] * (K + 1) for _ in range(n)]   # s[i][j], 1-indexed j
    for i in range(1, n):                       # registers for x_1..x_{n-1}
        for j in range(1, K + 1):
            s[i][j] = cnf.new_var()
    # i = 1
    cnf.add(-xs[0], s[1][1])
    for j in range(2, K + 1):
        cnf.add(-s[1][j])
    for i in range(2, n):                       # x_i, i = 2..n-1
        cnf.add(-xs[i - 1], s[i][1])
        cnf.add(-s[i - 1][1], s[i][1])
        for j in range(2, K + 1):
            cnf.add(-xs[i - 1], -s[i - 1][j - 1], s[i][j])
            cnf.add(-s[i - 1][j], s[i][j])
        cnf.add(-xs[i - 1], -s[i - 1][K])
    cnf.add(-xs[n - 1], -s[n - 1][K])


def build_css_cnf(H, L, K, forced=()):
    """Canonical CNF for the CSS sector instance. H: parity checks that x must
    satisfy; L: pairing rows (conjugate-sector logical reps); K: max weight.
    forced: iterable of DIMACS literals to assert."""
    n = H.shape[1]
    cnf = CNF(n)
    for row in H:
        sup = [int(i) + 1 for i in np.flatnonzero(row)]
        if not sup:
            continue
        t = _xor_chain(cnf, sup)
        cnf.add(-t)
    bs = []
    for row in L:
        sup = [int(i) + 1 for i in np.flatnonzero(row)]
        assert sup, "zero pairing row"
        bs.append(_xor_chain(cnf, sup))
    cnf.add(*bs)
    _at_most_k(cnf, list(range(1, n + 1)), K)
    for lit in forced:
        cnf.add(lit)
    return cnf


def build_stab_cnf(S, L, K, forced=()):
    """General stabilizer instance. S: symplectic stabilizer rows (a|b),
    L: symplectic logical reps. Error e=(u|v): vars u_i = i+1, v_i = n+i+1,
    q_i = 2n+i+1 (support indicators). Commutation with row (a|b):
    XOR over {v_i : a_i=1} ∪ {u_i : b_i=1} = 0 (chain over sorted var index).
    Same aux ordering discipline as build_css_cnf; at-most-K on q."""
    n = S.shape[1] // 2
    cnf = CNF(3 * n)
    U = lambda i: i + 1
    V = lambda i: n + i + 1
    Q = lambda i: 2 * n + i + 1
    for i in range(n):                     # support indicator definitions
        cnf.add(-U(i), Q(i))
        cnf.add(-V(i), Q(i))
        cnf.add(U(i), V(i), -Q(i))
    def pairing_vars(row):
        a, b = row[:n], row[n:]
        vs = sorted([V(i) for i in np.flatnonzero(a)] +
                    [U(i) for i in np.flatnonzero(b)])
        return vs
    for row in S:
        vs = pairing_vars(row)
        if not vs:
            continue
        t = _xor_chain(cnf, vs)
        cnf.add(-t)
    bs = []
    for row in L:
        vs = pairing_vars(row)
        assert vs
        bs.append(_xor_chain(cnf, vs))
    cnf.add(*bs)
    _at_most_k(cnf, [Q(i) for i in range(n)], K)
    for lit in forced:
        cnf.add(lit)
    return cnf


def write_dimacs(cnf, path):
    with open(path, "w") as f:
        f.write(f"p cnf {cnf.nv} {len(cnf.clauses)}\n")
        for c in cnf.clauses:
            f.write(" ".join(map(str, c)) + " 0\n")


def save_matrix(M, path):
    with open(path, "w") as f:
        f.write(f"{M.shape[0]} {M.shape[1]}\n")
        for row in M:
            f.write("".join(map(str, row.tolist())) + "\n")
