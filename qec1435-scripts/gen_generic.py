#!/usr/bin/env python3
"""Generic enumerator of sigma-invariant isotropic 11-dim subspaces of F2^28
for an arbitrary F2-linear symplectic map sigma of finite order
(given by images of the 28 basis vectors).

Method: order n of sigma -> min poly divides x^n - 1; factor x^n-1 over F2
(sympy, modulus=2); primary component for irreducible factor f with
multiplicity m in x^n-1 is ker f(sigma)^m; V = direct sum of components;
every invariant subspace = direct sum of invariant subspaces of components.
Per component (dim <= LIMIT): enumerate ALL submodules by cyclic closure of
every element + closure under sums to a fixpoint. Combine across components
(dims summing to 11) with incremental isotropy pruning; emit basis as hex.

Usage: gen_generic.py <sigma_name> [--count-only]
sigma_name in: shift (14-cycle), qc7 (two 7-cycles), c11 (11-cycle+3 fixed),
c13 (13-cycle+1 fixed), swapshift (14-cycle followed by X<->Z swap on every
qubit = involution-twisted cyclic), s3shift (14-cycle followed by the order-3
local symplectic map (a,b)->(b,a+b) on every qubit).

Every class is closed under the choices made (conjugacy in the relevant
group), so one representative per class suffices for existence questions.
"""
import sys
from itertools import combinations, product as iproduct

MASKA = (1 << 14) - 1

def rot14(h):
    return ((h << 1) | (h >> 13)) & MASKA

def rot7(h):
    return ((h << 1) | (h >> 6)) & 0x7F

def sp(u, v):
    ua, ub = u & MASKA, u >> 14
    va, vb = v & MASKA, v >> 14
    return (bin(ua & vb).count('1') + bin(ub & va).count('1')) & 1

# ---- sigma definitions (on 28-bit vectors) ----
def sigma_shift(v):
    return rot14(v & MASKA) | (rot14(v >> 14) << 14)

def sigma_qc7(v):
    a, b = v & MASKA, v >> 14
    a = rot7(a & 0x7F) | (rot7(a >> 7) << 7)
    b = rot7(b & 0x7F) | (rot7(b >> 7) << 7)
    return a | (b << 14)

def rot11(h):
    return ((h << 1) | (h >> 10)) & ((1 << 11) - 1)

def sigma_c11(v):
    a, b = v & MASKA, v >> 14
    a = rot11(a & 0x7FF) | (a & (0x7 << 11))
    b = rot11(b & 0x7FF) | (b & (0x7 << 11))
    return a | (b << 14)

def rot13(h):
    return ((h << 1) | (h >> 12)) & ((1 << 13) - 1)

def sigma_c13(v):
    a, b = v & MASKA, v >> 14
    a = rot13(a & 0x1FFF) | (a & (1 << 13))
    b = rot13(b & 0x1FFF) | (b & (1 << 13))
    return a | (b << 14)

def sigma_swapshift(v):
    a, b = v & MASKA, v >> 14
    a, b = b, a                      # local swap X<->Z on every qubit
    a, b = rot14(a), rot14(b)        # then shift
    return a | (b << 14)

def sigma_s3shift(v):
    a, b = v & MASKA, v >> 14
    a, b = b, a ^ b                  # local order-3 map (a,b)->(b,a+b)
    a, b = rot14(a), rot14(b)
    return a | (b << 14)

def sigma_qc7swap(v):
    a, b = v & MASKA, v >> 14
    a, b = b, a                      # local swap X<->Z on every qubit
    v2 = a | (b << 14)
    return sigma_qc7(v2)             # then double-7-cycle shift

def sigma_qc7s3(v):
    a, b = v & MASKA, v >> 14
    a, b = b, a ^ b                  # local order-3 map on every qubit
    v2 = a | (b << 14)
    return sigma_qc7(v2)

def _local(v, qmask, kind):
    """apply a local symplectic map to the qubits in qmask.
    kind: 'swap' (a,b)->(b,a); 's2' (a,b)->(a,a+b); 's3' (a,b)->(a+b,b);
          'rho' (a,b)->(b,a+b); 'rho2' (a,b)->(a+b,a)"""
    a, b = v & MASKA, v >> 14
    am, bm = a & qmask, b & qmask
    ao, bo = a & ~qmask & MASKA, b & ~qmask & MASKA
    if kind == 'swap':
        am, bm = bm, am
    elif kind == 's2':
        am, bm = am, am ^ bm
    elif kind == 's3':
        am, bm = am ^ bm, bm
    elif kind == 'rho':
        am, bm = bm, am ^ bm
    elif kind == 'rho2':
        am, bm = am ^ bm, am
    return (ao | am) | ((bo | bm) << 14)

B2 = 0x3F80          # qubits 7..13
ALLQ = MASKA         # all 14 qubits

def sigma_qc7_1swap(v):   # twist class (1, swap), order 14
    return sigma_qc7(_local(v, B2, 'swap'))

def sigma_qc7_1rho(v):    # twist class (1, rho), order 21
    return sigma_qc7(_local(v, B2, 'rho'))

def sigma_qc7_swap_s2(v): # twist class (swap, s2), order 14
    return sigma_qc7(_local(_local(v, ~B2 & MASKA, 'swap'), B2, 's2'))

def sigma_qc7_swap_rho(v):  # twist class (swap, rho), order 42
    return sigma_qc7(_local(_local(v, ~B2 & MASKA, 'swap'), B2, 'rho'))

def sigma_qc7_rho_rho2(v):  # twist class (rho, rho2), order 21
    return sigma_qc7(_local(_local(v, ~B2 & MASKA, 'rho'), B2, 'rho2'))

def sigma_s3shift2(v):    # 14-cycle with global rho2 twist, order 42
    a, b = v & MASKA, v >> 14
    a, b = a ^ b, a
    a, b = rot14(a), rot14(b)
    return a | (b << 14)

def sigma_shift28(v):     # 14-cycle with swap twist on qubit 0 only, order 28
    return sigma_shift(_local(v, 1, 'swap'))

SIGMAS = dict(shift28=sigma_shift28, shift=sigma_shift, qc7=sigma_qc7, c11=sigma_c11, c13=sigma_c13,
              swapshift=sigma_swapshift, s3shift=sigma_s3shift,
              qc7swap=sigma_qc7swap, qc7s3=sigma_qc7s3,
              qc7_1swap=sigma_qc7_1swap, qc7_1rho=sigma_qc7_1rho,
              qc7_swap_s2=sigma_qc7_swap_s2, qc7_swap_rho=sigma_qc7_swap_rho,
              qc7_rho_rho2=sigma_qc7_rho_rho2, s3shift2=sigma_s3shift2)

name = sys.argv[1]
count_only = '--count-only' in sys.argv
sig = SIGMAS[name]

# sanity: sigma preserves the symplectic form
import random
random.seed(1)
for _ in range(200):
    u = random.getrandbits(28)
    v = random.getrandbits(28)
    assert sp(sig(u), sig(v)) == sp(u, v)

# matrix / order
IM = [sig(1 << i) for i in range(28)]

def apply(v):
    r = 0
    i = 0
    while v:
        if v & 1:
            r ^= IM[i]
        v >>= 1
        i += 1
    return r

order = 1
w = list(IM)
cur = IM
def compose_once(cur):
    return [apply_vec(cur, 1 << i) for i in range(28)]

def apply_mat(M, v):
    r = 0
    i = 0
    while v:
        if v & 1:
            r ^= M[i]
        v >>= 1
        i += 1
    return r

M = IM
order = 1
while M != [1 << i for i in range(28)]:
    M = [apply_mat(IM, M[i]) for i in range(28)]
    order += 1
    assert order <= 200
print(f"sigma = {name}, order {order}", file=sys.stderr)

# factor x^order - 1 over F2 with sympy
from sympy import symbols, Poly
x = symbols('x')
fl = Poly(x**order + 1, x, modulus=2).factor_list()[1]
factors = []
for poly, mult in fl:
    coeffs = poly.all_coeffs()  # highest first, entries mod 2
    fint = 0
    for c in coeffs:
        fint = (fint << 1) | (int(c) & 1)
    factors.append((fint, mult, poly.degree()))
print("factors of x^%d-1: %s" % (order, [(bin(f), m) for f, m, _ in factors]),
      file=sys.stderr)

# poly of matrix: f(sigma) as matrix (list of column images)
def matmul(A, B):          # A after B: (A.B)(v) = A(B(v))
    return [apply_mat(A, B[i]) for i in range(28)]

def poly_of_sigma(fint):
    R = [0] * 28                       # zero matrix
    P = [1 << i for i in range(28)]    # sigma^0
    f = fint
    while f:
        if f & 1:
            R = [R[i] ^ P[i] for i in range(28)]
        f >>= 1
        P = [apply_mat(IM, P[i]) for i in range(28)]  # NOTE: applies IM once
    return R

def mat_power(A, k):
    R = [1 << i for i in range(28)]
    for _ in range(k):
        R = matmul(A, R)
    return R

def kernel(A):
    """nullspace basis of matrix A given by column images: A(v) = xor of A[i]"""
    # build rows: we need v with A(v)=0. Solve via Gaussian elimination on the
    # 28x28 system: unknown v bits; equation bit j of A(v) = 0.
    # Represent equations: for output bit j: row_j = mask of input bits i with A[i] bit j set.
    rows = []
    for j in range(28):
        m = 0
        for i in range(28):
            if A[i] >> j & 1:
                m |= 1 << i
        rows.append(m)
    # eliminate
    pivots = []
    r = 0
    for c in range(28):
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
        pivots.append(c)
        r += 1
    rows = rows[:r]
    free = [c for c in range(28) if c not in pivots]
    basis = []
    for c in free:
        v = 1 << c
        for i, pc in enumerate(pivots):
            if rows[i] >> c & 1:
                v |= 1 << pc
        basis.append(v)
    for v in basis:
        assert apply_mat(A, v) == 0
    return basis

components = []
for fint, mult, deg in factors:
    F1 = poly_of_sigma(fint)
    Fm = mat_power(F1, mult) if mult > 1 else F1
    kb = kernel(Fm)
    components.append((fint, mult, deg, kb))
    print(f"factor {bin(fint)} mult {mult}: component dim {len(kb)}",
          file=sys.stderr)

assert sum(len(kb) for *_, kb in components) == 28

LIMIT = 13
skip_enum = {}
for idx, (fint, mult, deg, kb) in enumerate(components):
    if len(kb) > LIMIT:
        # semisimple component: submodule F2-dims are multiples of deg.
        # If deg > 11 the only usable submodule is 0 -> no enumeration needed.
        if mult == 1 and deg > 11:
            skip_enum[idx] = True
            print(f"component dim {len(kb)} (deg {deg} > 11, semisimple): "
                  f"only the zero submodule can occur; skipping enumeration",
                  file=sys.stderr)
        else:
            print(f"component dim {len(kb)} > {LIMIT}: class not enumerable "
                  f"by this method; ABORT", file=sys.stderr)
            sys.exit(2)

# ---- submodule enumeration per component ----
def rref(vecs):
    basis = []
    for x in vecs:
        for h in basis:
            hb = 1 << (h.bit_length() - 1)
            if x & hb:
                x ^= h
        if x:
            basis.append(x)
            basis.sort(key=lambda z: -z)
            changed = True
            while changed:
                changed = False
                for i in range(len(basis)):
                    for j in range(len(basis)):
                        if i != j and basis[j]:
                            hb = 1 << (basis[j].bit_length() - 1)
                            if basis[i] & hb:
                                basis[i] ^= basis[j]
                                changed = True
                basis = [b for b in basis if b]
                basis.sort(key=lambda z: -z)
    return tuple(sorted(basis))

def span_elems(basis):
    out = [0]
    for b in basis:
        out += [y ^ b for y in out]
    return out

def all_submodules(kb):
    elems = span_elems(kb)
    cyc = set()
    for g in elems:
        vecs = []
        h = g
        for _ in range(order):
            vecs.append(h)
            h = apply(h)
        cyc.add(rref(vecs))
    subs = set(cyc)
    frontier = set(cyc)
    while frontier:
        new = set()
        for Mb in frontier:
            for C in cyc:
                Sm = rref(list(Mb) + list(C))
                if Sm not in subs:
                    new.add(Sm)
        subs |= new
        frontier = new
    return subs

subs_by_comp = []
for idx, (fint, mult, deg, kb) in enumerate(components):
    if skip_enum.get(idx):
        subs_by_comp.append({0: [()]})
        continue
    subs = all_submodules(kb)
    byd = {}
    for Mb in subs:
        byd.setdefault(len(Mb), []).append(Mb)
    subs_by_comp.append(byd)
    print(f"factor {bin(fint)}: {len(subs)} submodules, dims "
          f"{sorted((d, len(v)) for d, v in byd.items())}", file=sys.stderr)

# recursion order: biggest component first so the expensive cross-filter
# between large components runs once, not once per small-component choice
comp_order = sorted(range(ncomp if False else len(components)),
                    key=lambda i: -sum(len(v) for v in subs_by_comp[i].values()))
subs_by_comp = [subs_by_comp[i] for i in comp_order]

# ---- combine across components, dims sum to 11, isotropy pruning ----
ncomp = len(components)
total = 0
emitted = 0

_iso_cache = {}
def is_self_iso(basis):
    r = _iso_cache.get(basis)
    if r is None:
        r = all(sp(u, v) == 0 for u, v in combinations(basis, 2))
        _iso_cache[basis] = r
    return r

def cross_ok(b1, b2):
    return all(sp(u, v) == 0 for u in b1 for v in b2)

def recurse(ci, dims_left, chosen):
    global total, emitted
    if ci == ncomp:
        if dims_left == 0:
            basis = [v for Mb in chosen for v in Mb]
            total += 1
            if not count_only:
                print(' '.join(f'{g:07x}' for g in basis))
            emitted += 1
        return
    byd = subs_by_comp[ci]
    for d, mods in sorted(byd.items()):
        if d > dims_left:
            continue
        # remaining components can absorb the rest? (loose check: skip)
        for Mb in mods:
            if not is_self_iso(Mb):
                continue
            ok = True
            for Cb in chosen:
                if not cross_ok(Cb, Mb):
                    ok = False
                    break
            if ok:
                recurse(ci + 1, dims_left - d, chosen + [Mb])

recurse(0, 11, [])
print(f"total isotropic invariant 11-dim subspaces: {total}", file=sys.stderr)
