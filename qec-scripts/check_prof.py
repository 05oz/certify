#!/usr/bin/env python3
"""check_prof.py -- checker for a profile-normalised distance
certificate.  Python standard library only; imports nothing from the pipeline
(`qec_lib`, `enc.py`, numpy are all absent from the trusted base).

NOT independent of `check_lower.py`: 88 of 387 executable lines are verbatim
there, `386-393 == check_lower.py:295-302` is the LRAT propagation loop, and the
Tseitin encoders are alpha-equivalent.  Independent of `check_witness.py` and
`check_duality.py` (10 and 18 shared lines, all boilerplate).  The CSS-CNF
construction at the head of `regen` (236-248) is a transliteration of
`qec_lib.build_css_cnf` (270-291), the custom assertion `assert sup, "zero
pairing row"` included, so a CSS-encoding fault would be common-mode with the
pipeline even though `qec_lib` is not imported.

What it verifies, in order:

 1. Rebuilds H_X, H_Z for the named bivariate-bicycle code from its polynomial
    spec (l, m, A-monomials, B-monomials) -- the shipped matrices are not
    trusted.
 2. CSS side conditions: H_X H_Z^T = 0; every shipped pairing row lies in
    ker H_X; the pairing rows are independent modulo rowspace(H_Z) and there
    are exactly k = n - rank H_X - rank H_Z of them.  (These are what make
    "some pairing row pairs oddly with x" equivalent to "x is a nontrivial
    X-logical".)
 3. AUTOMORPHISM: the two generating translations (1,0) and (0,1) preserve
    rowspace(H_X) and rowspace(H_Z), so the group T = Z_l x Z_m they generate
    acts on nontrivial X-logicals preserving weight.  This is the hypothesis
    of Lemma S; Lemma S itself is the on-paper part of the trusted base and is
    stated in BUILD-algorithm.md.
 4. PARITY (only if the certificate claims it): exhibits c with c^T H_Z = 1_n,
    so every element of ker H_Z has even weight (Lemma P).
 5. REGENERATES the CNF from (H_Z, pairing rows, K, mode) with its own
    encoder and requires the shipped .cnf to be identical clause-for-clause.
 6. Replays the LRAT proof against the regenerated clause list.

Usage: check_prof.py cert.json
"""
import gzip, json, sys, os


# --------------------------------------------------------------------- GF(2)
def rref(rows, ncols):
    """rows: list of int bitmasks.  Returns (reduced rows, pivot columns)."""
    rows = list(rows)
    piv, r = [], 0
    for c in range(ncols):
        p = None
        for i in range(r, len(rows)):
            if rows[i] >> c & 1:
                p = i
                break
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        for i in range(len(rows)):
            if i != r and (rows[i] >> c & 1):
                rows[i] ^= rows[r]
        piv.append(c)
        r += 1
        if r == len(rows):
            break
    return [x for x in rows if x], piv


def rank(rows, ncols):
    return len(rref(rows, ncols)[1])


def rowspace_key(rows, ncols):
    R, piv = rref(rows, ncols)
    return (tuple(sorted(R)), tuple(piv))


def in_rowspace(rows, v, ncols):
    return rank(list(rows) + [v], ncols) == rank(rows, ncols)


def solve_left(rows, target, ncols):
    """Bitmask c with XOR_{i: c_i=1} rows[i] == target, or None.  Tracks the
    combination alongside the value during elimination."""
    pivots = {}                       # lowest set column -> (value, combination)
    for i, r in enumerate(rows):
        v, t = r, 1 << i
        while v:
            c = (v & -v).bit_length() - 1
            if c in pivots:
                pv, pt = pivots[c]
                v ^= pv
                t ^= pt
            else:
                pivots[c] = (v, t)
                break
    v, t = target, 0
    while v:
        c = (v & -v).bit_length() - 1
        if c not in pivots:
            return None
        pv, pt = pivots[c]
        v ^= pv
        t ^= pt
    return t


# ------------------------------------------------------------------ BB codes
def bb_matrices(l, m, aterms, bterms):
    """H_X = [A|B], H_Z = [B^T|A^T] as lists of int bitmasks over n = 2lm bits.
    Qubit index (block, r, s) -> block*l*m + r*m + s."""
    N, n = l * m, 2 * l * m
    def circ(terms):
        M = [0] * N
        for (i, j) in terms:
            for r in range(l):
                for s in range(m):
                    M[r * m + s] ^= 1 << (((r + i) % l) * m + (s + j) % m)
        return M
    A, B = circ(aterms), circ(bterms)
    def transpose(M):
        T = [0] * N
        for i in range(N):
            x = M[i]
            while x:
                b = (x & -x).bit_length() - 1
                T[b] |= 1 << i
                x ^= 1 << b
        return T
    At, Bt = transpose(A), transpose(B)
    HX = [A[i] | (B[i] << N) for i in range(N)]
    HZ = [Bt[i] | (At[i] << N) for i in range(N)]
    return HX, HZ, N, n


def shift_perm(l, m, a, c):
    """p[i] = index of the image of qubit i under translation by (a,c)."""
    N = l * m
    p = [0] * (2 * N)
    for b in range(2):
        for r in range(l):
            for s in range(m):
                p[b * N + r * m + s] = b * N + ((r + a) % l) * m + (s + c) % m
    return p


def permute_row(row, p, n):
    out = 0
    for i in range(n):
        if row >> i & 1:
            out |= 1 << p[i]
    return out


# ------------------------------------------------------- independent encoder
class CNF:
    def __init__(self, nv):
        self.nv = nv
        self.cl = []
    def new_var(self):
        self.nv += 1
        return self.nv
    def add(self, *l):
        self.cl.append(list(l))


def xor_chain(cnf, lits):
    cur = lits[0]
    for lit in lits[1:]:
        u = cnf.new_var()
        cnf.add(-u, cur, lit)
        cnf.add(-u, -cur, -lit)
        cnf.add(u, -cur, lit)
        cnf.add(u, cur, -lit)
        cur = u
    return cur


def tot(cnf, xs, K, exact):
    if len(xs) == 1:
        return [xs[0]]
    mid = len(xs) // 2
    A = tot(cnf, xs[:mid], K, exact)
    B = tot(cnf, xs[mid:], K, exact)
    return merge(cnf, A, B, K, exact, cap=len(xs))


def merge(cnf, A, B, K, exact, cap=None):
    total = cap if cap is not None else len(A) + len(B)
    m = min(total, K + 1)
    O = [cnf.new_var() for _ in range(m)]
    na, nb = len(A), len(B)
    for a in range(na + 1):
        for b in range(nb + 1):
            s = a + b
            if 1 <= s <= m:
                lits = [O[s - 1]]
                if a > 0:
                    lits.append(-A[a - 1])
                if b > 0:
                    lits.append(-B[b - 1])
                cnf.add(*lits)
            if exact and s + 1 <= m:
                lits = [-O[s]]
                if a < na:
                    lits.append(A[a])
                if b < nb:
                    lits.append(B[b])
                cnf.add(*lits)
    return O


def lex_ge(cnf, X, Y):
    e = None                                    # None == constant true
    for i in range(len(X)):
        xi, yi = X[i], Y[i]
        if xi == yi:
            continue
        if e is None:
            cnf.add(xi, -yi)
        else:
            cnf.add(-e, xi, -yi)
        if i == len(X) - 1:
            break
        ne = cnf.new_var()
        if e is None:
            cnf.add(-ne, -xi, yi)
            cnf.add(-ne, xi, -yi)
            cnf.add(ne, xi, yi)
            cnf.add(ne, -xi, -yi)
        else:
            cnf.add(-ne, e)
            cnf.add(-ne, -xi, yi)
            cnf.add(-ne, xi, -yi)
            cnf.add(ne, -e, xi, yi)
            cnf.add(ne, -e, -xi, -yi)
        e = ne


def regen(HZ, L, l, m, K, sym, exact, parity, n, N, axis=None):
    cnf = CNF(n)
    for row in HZ:
        sup = [i + 1 for i in range(n) if row >> i & 1]
        if not sup:
            continue
        cnf.add(-xor_chain(cnf, sup))
    bs = []
    for row in L:
        sup = [i + 1 for i in range(n) if row >> i & 1]
        assert sup, "zero pairing row"
        bs.append(xor_chain(cnf, sup))
    cnf.add(*bs)

    def var(b, r, s):
        return b * N + (r % l) * m + (s % m) + 1

    if axis is None:
        axis = "row" if l >= m else "col"
    nfield = l if axis == "row" else m
    nslice = m if axis == "row" else l
    if sym == "prof":
        rowc = []
        for r in range(nfield):
            if axis == "row":
                xs = [var(b, r, s) for b in range(2) for s in range(m)]
            else:
                xs = [var(b, t, r) for b in range(2) for t in range(l)]
            rowc.append(tot(cnf, xs, K, True))
        level = list(rowc)
        while len(level) > 1:
            nxt = []
            for i in range(0, len(level) - 1, 2):
                nxt.append(merge(cnf, level[i], level[i + 1], K, exact))
            if len(level) % 2:
                nxt.append(level[-1])
            level = nxt
        O = level[0]
    else:
        O = tot(cnf, list(range(1, n + 1)), K, exact)

    if exact:
        cnf.add(O[K - 1])
        if len(O) > K:
            cnf.add(-O[K])
    else:
        if len(O) > K:
            cnf.add(-O[K])
    if parity and not exact:
        for j in range(1, K + 1, 2):
            if j < len(O):
                cnf.add(-O[j - 1], O[j])

    if sym == "prof":
        def prof_string(off):
            out = []
            for r in range(nfield):
                c = rowc[(r + off) % nfield]
                out.extend(c[:min(len(c), K)])
                out.extend([None] * (K - min(len(c), K)))
            return out
        base = prof_string(0)
        for a in range(1, nfield):
            rot = prof_string(a)
            Xs = [p for p, q in zip(base, rot) if p is not None and q is not None]
            Ys = [q for p, q in zip(base, rot) if p is not None and q is not None]
            lex_ge(cnf, Xs, Ys)
        def pat(off):
            if axis == "row":
                return [var(b, 0, s + off) for b in range(2) for s in range(m)]
            return [var(b, t + off, 0) for b in range(2) for t in range(l)]
        p0 = pat(0)
        for c in range(1, nslice):
            lex_ge(cnf, p0, pat(c))
        t0 = rowc[0]
        for r in range(1, nfield):
            tr = rowc[r]
            for j in range(min(len(t0), len(tr))):
                cnf.add(-tr[j], t0[j])
        for j in range(len(t0)):
            idx = nfield * (j + 1)
            if idx <= len(O):
                cnf.add(t0[j], -O[idx - 1])
    elif sym == "anchor2":
        cnf.add(1)
    return cnf


# ----------------------------------------------------------------- LRAT
def open_lrat(path):
    return gzip.open(path, "rt") if path.endswith(".gz") else open(path)


def replay(clauses, path):
    store = {i + 1: tuple(c) for i, c in enumerate(clauses)}
    maxvar = max((abs(x) for c in clauses for x in c), default=0)
    val = [0] * (maxvar + 2)
    stamp = 0
    got_empty = False
    nlem = 0
    with open_lrat(path) as fh:
        for line in fh:
            t = line.split()
            if not t:
                continue
            if len(t) > 1 and t[1] == 'd':
                for x in t[2:]:
                    i = int(x)
                    if i == 0:
                        break
                    store.pop(i, None)
                continue
            cid = int(t[0])
            nums = [int(x) for x in t[1:]]
            z = nums.index(0)
            lits, hints = nums[:z], nums[z + 1:]
            assert hints and hints[-1] == 0, "malformed LRAT line"
            hints = hints[:-1]
            stamp += 1
            nlem += 1
            for lit in lits:
                v = abs(lit)
                if v > maxvar:
                    val.extend([0] * (v - maxvar + 1))
                    maxvar = v
                val[v] = -stamp if lit > 0 else stamp
            conflict = False
            for h in hints:
                if h < 0:
                    raise SystemExit("RAT hint: this checker handles RUP only")
                cl = store.get(h)
                assert cl is not None, f"hint {h} missing"
                unit, sat = None, False
                for lit in cl:
                    v = abs(lit)
                    if v > maxvar:
                        val.extend([0] * (v - maxvar + 1))
                        maxvar = v
                    s = val[v]
                    if s == stamp or s == -stamp:
                        if (s > 0) == (lit > 0):
                            sat = True
                            break
                        continue
                    if unit is None:
                        unit = lit
                    else:
                        unit = 'many'
                if sat or unit == 'many':
                    continue
                if unit is None:
                    conflict = True
                    break
                val[abs(unit)] = stamp if unit > 0 else -stamp
            if not conflict:
                raise SystemExit(f"LRAT lemma {cid} NOT verified (no conflict)")
            store[cid] = tuple(lits)
            if not lits:
                got_empty = True
    return got_empty, nlem


def read_dimacs(path):
    cl, nv = [], 0
    with open(path) as fh:
        for line in fh:
            if line.startswith('c'):
                continue
            if line.startswith('p'):
                nv = int(line.split()[2])
                continue
            t = [int(x) for x in line.split()]
            if t and t[-1] == 0:
                cl.append(t[:-1])
    return cl, nv


# ------------------------------------------------------------------- main
def main():
    cert = json.load(open(sys.argv[1]))
    base = os.path.dirname(os.path.abspath(sys.argv[1]))
    P = lambda f: f if os.path.isabs(f) else os.path.join(base, f)
    c = cert["code"]
    l, m = c["l"], c["m"]
    aterms = [tuple(x) for x in c["a"]]
    bterms = [tuple(x) for x in c["b"]]
    HX, HZ, N, n = bb_matrices(l, m, aterms, bterms)
    print(f"[1] rebuilt {c['name']}: n={n} l={l} m={m}")

    # CSS orthogonality
    for rx in HX:
        for rz in HZ:
            assert bin(rx & rz).count('1') % 2 == 0, "H_X H_Z^T != 0"
    rX, rZ = rank(HX, n), rank(HZ, n)
    k = n - rX - rZ
    print(f"[2] CSS orthogonality OK; rank H_X={rX} rank H_Z={rZ} k={k}")

    # pairing rows
    L = []
    with open(P(cert["pairing"])) as fh:
        nr, nc = map(int, fh.readline().split())
        assert nc == n
        for _ in range(nr):
            s = fh.readline().strip()
            L.append(sum(1 << i for i, ch in enumerate(s) if ch == '1'))
    assert len(L) == k, f"expected {k} pairing rows, got {len(L)}"
    for row in L:
        for rx in HX:
            assert bin(rx & row).count('1') % 2 == 0, "pairing row not in ker H_X"
    assert rank(HZ + L, n) == rZ + len(L), "pairing rows not independent mod H_Z"
    print(f"[3] pairing rows OK ({len(L)} rows, in ker H_X, independent mod rowspace H_Z)")

    # automorphism
    kx, kz = rowspace_key(HX, n), rowspace_key(HZ, n)
    for (a, cc) in ((1, 0), (0, 1)):
        p = shift_perm(l, m, a, cc)
        assert rowspace_key([permute_row(r, p, n) for r in HX], n) == kx
        assert rowspace_key([permute_row(r, p, n) for r in HZ], n) == kz
    print("[4] translations (1,0),(0,1) preserve both rowspaces -> T <= Aut")

    # parity
    if cert.get("parity_claim"):
        comb = solve_left(HZ, (1 << n) - 1, n)
        assert comb is not None, "1_n NOT in rowspace(H_Z): parity claim unsound"
        chk = 0
        for i in range(len(HZ)):
            if comb >> i & 1:
                chk ^= HZ[i]
        assert chk == (1 << n) - 1
        print(f"[5] parity: c^T H_Z = 1_n with |c| = {bin(comb).count('1')} rows "
              f"-> every x in ker H_Z has even weight")
    else:
        print("[5] parity not claimed")

    # regenerate + compare
    K = cert["K"]
    cnf = regen(HZ, L, l, m, K, cert["sym"], cert.get("exact", False),
                cert.get("parity_in_cnf", False), n, N, cert.get("axis"))
    ship, shipnv = read_dimacs(P(cert["cnf"]))
    assert shipnv == cnf.nv, f"var count differs: shipped {shipnv} regen {cnf.nv}"
    assert len(ship) == len(cnf.cl), f"clause count differs: {len(ship)} vs {len(cnf.cl)}"
    for i, (a, b) in enumerate(zip(ship, cnf.cl)):
        assert a == b, f"clause {i+1} differs: shipped {a} regen {b}"
    print(f"[6] shipped CNF regenerated exactly: {cnf.nv} vars, {len(cnf.cl)} clauses")

    ok, nlem = replay(cnf.cl, P(cert["proof"]))
    assert ok, "LRAT proof does not derive the empty clause"
    print(f"[7] LRAT replayed: {nlem} lemmas, empty clause derived -> UNSAT")
    print(f"\nACCEPTED: {cert['claim']}")


if __name__ == "__main__":
    main()
