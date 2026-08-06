#!/usr/bin/env python3
"""Complete enumeration of CYCLIC [[14,3]] stabilizer codes.

Cyclic = additive GF(4) code invariant under the qubit shift i -> i+1 mod 14,
i.e. T-invariant 11-dim isotropic subspaces of F2^28 where T rotates both the
X-half (bits 0..13) and Z-half (bits 14..27) left by one.

Method: x^14+1 = ((x+1) p q)^2 over F2 with p = x^3+x+1, q = x^3+x^2+1.
Primary (CRT) decomposition of the F2[x]-module V = (F2[x]/(x^14+1))^2 into
components V1 (dim 4), Vp (dim 12), Vq (dim 12).  Every invariant subspace is
the direct sum of invariant subspaces of the components (CRT idempotents act as
projections and belong to F2[T]).  Component submodules are enumerated by
closure: all cyclic submodules <g>, then closure under sums to a fixpoint
(over a chain ring the ambient is 2-generated, so sums of two cyclics already
suffice; the fixpoint iteration makes completeness independent of that fact).

Isotropy: reciprocal pairing sends the p-component to the q-component, so
sp vanishes on V1 x Vp, V1 x Vq, Vp x Vp, Vq x Vq (asserted, not assumed) and
the constraints are: M1 isotropic, sp(Mp, Mq) = 0.

Dimension count: dim M1 + dim Mp + dim Mq = 11 with dim Mp, dim Mq multiples
of 3 forces dim M1 = 2, dim Mp + dim Mq = 9.

Output: one candidate per line, 11 hex words (basis), for check1435 batch 11.
Summary counts go to stderr.
"""
import sys
from itertools import combinations

N = 14
MASK = (1 << N) - 1

# ---------- F2[x] on ints ----------
def pmul(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        b >>= 1
    return r

def pdeg(a):
    return a.bit_length() - 1

def pdivmod(a, b):
    q = 0
    db = pdeg(b)
    while a and pdeg(a) >= db:
        s = pdeg(a) - db
        q ^= 1 << s
        a ^= b << s
    return q, a

def pmod(a, b):
    return pdivmod(a, b)[1]

def pxgcd(a, b):
    # returns (g, u, v) with u a + v b = g
    r0, r1 = a, b
    s0, s1 = 1, 0
    t0, t1 = 0, 1
    while r1:
        qq, rr = pdivmod(r0, r1)
        r0, r1 = r1, rr
        s0, s1 = s1, s0 ^ pmul(qq, s1)
        t0, t1 = t1, t0 ^ pmul(qq, t1)
    return r0, s0, t0

XN1 = (1 << N) | 1          # x^14 + 1
P = 0b1011                  # x^3+x+1
Q = 0b1101                  # x^3+x^2+1
F1 = pmul(0b11, 0b11)       # (x+1)^2
FP = pmul(P, P)
FQ = pmul(Q, Q)
assert pmul(F1, pmul(FP, FQ)) == XN1

def idempotent(F):
    G = pdivmod(XN1, F)[0]
    g, u, v = pxgcd(G, F)
    assert g == 1
    e = pmod(pmul(u, G), XN1)
    assert pmod(pmul(e, e), XN1) == e
    return e

E1, EP, EQ = idempotent(F1), idempotent(FP), idempotent(FQ)
assert (E1 ^ EP ^ EQ) == 1  # partition of unity

# ---------- vectors: 28-bit, (a | b<<14) ----------
def rot(h):                 # multiply 14-bit poly by x mod x^14+1
    return ((h << 1) | (h >> (N - 1))) & MASK

def Tmap(v):
    return rot(v & MASK) | (rot(v >> N) << N)

def sp(u, v):
    ua, ub = u & MASK, u >> N
    va, vb = v & MASK, v >> N
    return (bin(ua & vb).count('1') + bin(ub & va).count('1')) & 1

def rref(vecs):
    """canonical basis tuple (sorted, reduced) of span"""
    basis = []
    for x in vecs:
        for h in basis:
            hb = 1 << (h.bit_length() - 1)
            if x & hb:
                x ^= h
        if x:
            basis.append(x)
            basis.sort(key=lambda z: -z)
            # re-reduce fully
            changed = True
            while changed:
                changed = False
                for i in range(len(basis)):
                    for j in range(len(basis)):
                        if i != j:
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
        out += [x ^ b for x in out]
    return out

# ---------- component bases ----------
def comp_basis(e):
    vecs = []
    h = e
    for i in range(N):
        vecs.append(h)              # (x^i e, 0)
        vecs.append(h << N)         # (0, x^i e)
        h = rot(h)
    return rref(vecs)

B1 = comp_basis(E1)
BP = comp_basis(EP)
BQ = comp_basis(EQ)
assert len(B1) == 4 and len(BP) == 12 and len(BQ) == 12, (len(B1), len(BP), len(BQ))

# assert vanishing of sp on V1xVp, V1xVq, VpxVp, VqxVq
for u in B1:
    for v in BP + BQ:
        assert sp(u, v) == 0
for A, Bb in ((BP, BP), (BQ, BQ)):
    for u in A:
        for v in Bb:
            assert sp(u, v) == 0

# ---------- submodule enumeration in a component ----------
def cyclic_mod(g):
    vecs = []
    h = g
    for _ in range(N):
        vecs.append(h)
        h = Tmap(h)
    return rref(vecs)

def all_submodules(basis):
    elems = span_elems(basis)
    cyc = set()
    for g in elems:
        cyc.add(cyclic_mod(g))
    subs = set(cyc)
    frontier = set(cyc)
    while frontier:
        new = set()
        for M in frontier:
            for C in cyc:
                Ssum = rref(list(M) + list(C))
                if Ssum not in subs:
                    new.add(Ssum)
        subs |= new
        frontier = new
    return subs

sub1 = all_submodules(B1)
subp = all_submodules(BP)
subq = all_submodules(BQ)
print(f"submodule counts: V1 {len(sub1)}  Vp {len(subp)}  Vq {len(subq)}",
      file=sys.stderr)

by_dim = lambda subs, d: [M for M in subs if len(M) == d]
for M in subp:
    assert len(M) % 3 == 0
for M in subq:
    assert len(M) % 3 == 0

# M1: dim 2, isotropic (invariant already by construction)
M1s = []
for M in by_dim(sub1, 2):
    b = list(M)
    if all(sp(u, v) == 0 for u, v in combinations(b, 2)):
        M1s.append(M)
print(f"V1: {len(by_dim(sub1,2))} invariant dim-2, {len(M1s)} isotropic",
      file=sys.stderr)

count = 0
for dp in (0, 3, 6, 9):
    dq = 9 - dp
    Mps = by_dim(subp, dp)
    Mqs = by_dim(subq, dq)
    pairs = 0
    for Mp in Mps:
        bp = list(Mp)
        # precompute swapped masks for orthogonality test
        for Mq in Mqs:
            if all(sp(u, v) == 0 for u in bp for v in Mq):
                pairs += 1
                for M1 in M1s:
                    basis = list(M1) + bp + list(Mq)
                    assert len(basis) == 11
                    print(' '.join(f'{g:07x}' for g in basis))
                    count += 1
    print(f"dp={dp} dq={dq}: {len(Mps)} x {len(Mqs)} -> {pairs} orthogonal pairs",
          file=sys.stderr)

print(f"total candidates emitted: {count}", file=sys.stderr)
