#!/usr/bin/env python3
"""Complete enumeration of [[14,3]] stabilizer codes invariant under a
coordinate permutation of order 11 (necessarily one 11-cycle + 3 fixed qubits;
conjugate to the standard one, distance is permutation-invariant).

Qubits 0..10 = the 11-cycle, qubits 11,12,13 fixed.
x^11+1 = (x+1) Phi, Phi = x^10+...+1 irreducible (ord(2) mod 11 = 10).
Components of F2^28 under sigma:
  trivial: dim 8  (block averages J11 in a and b halves + 6 fixed-qubit dims)
  Phi:     L^2 with L = F2[x]/Phi = F_1024, slots (a-block, b-block), dim 20.
Invariant subspace dims: d0 + 10 m = 11, d0 <= 8  ->  d0 = 1, m = 1.
Phi is self-reciprocal -> the Phi-part pairs with itself: the L-line must be
isotropic. Trivial-part 1-dim is automatically isotropic. Cross-pairing between
trivial and Phi parts vanishes (asserted).

Output: 11 hex words per line for check1435 batch 11.
"""
import sys

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

def pmod(a, b):
    db = pdeg(b)
    while a and pdeg(a) >= db:
        a ^= b << (pdeg(a) - db)
    return a

X111 = (1 << 11) | 1
J11 = (1 << 11) - 1          # all ones, idempotent for factor x+1
EPH = 1 ^ J11                # idempotent for Phi  (x + x^2 + ... + x^10)

def mul11(a, b):
    return pmod(pmul(a, b), X111)

assert mul11(J11, J11) == J11
assert mul11(EPH, EPH) == EPH
assert (J11 ^ EPH) == 1

# embedding: a-half bits 0..13 (block bits 0..10, fixed 11..13), b-half bits 14..27
def emb_a(c):
    return c            # 11-bit poly into bits 0..10

def emb_b(c):
    return c << 14

def sp(u, v):
    MA = (1 << 14) - 1
    ua, ub = u & MA, u >> 14
    va, vb = v & MA, v >> 14
    return (bin(ua & vb).count('1') + bin(ub & va).count('1')) & 1

# trivial component basis (8 vectors)
triv = [emb_a(J11), emb_b(J11),
        1 << 11, 1 << 12, 1 << 13,
        1 << (14 + 11), 1 << (14 + 12), 1 << (14 + 13)]

# L = ideal EPH*R11; elements
L = sorted({mul11(EPH, t) for t in range(2048)})
assert len(L) == 1024

# line reps in L^2: (0, e) and (e, c) for c in L, e = EPH (identity of L)
reps = [(0, EPH)] + [(EPH, c) for c in L]
assert len(reps) == 1025

def line_basis(u, w):
    """F2-basis of L-line through (u,w): x^i * (u,w) for i = 0..9"""
    vecs = []
    cu, cw = u, w
    for i in range(10):
        vecs.append(emb_a(cu) ^ emb_b(cw))
        cu = mul11(cu, 0b10)
        cw = mul11(cw, 0b10)
    return vecs

# assert cross-pairing trivial x Phi vanishes
_lb = line_basis(EPH, EPH)
for t in triv:
    for v in _lb + line_basis(0, EPH):
        assert sp(t, v) == 0

iso_lines = []
for (u, w) in reps:
    vecs = line_basis(u, w)
    ok = True
    for i in range(10):
        for j in range(i + 1, 10):
            if sp(vecs[i], vecs[j]):
                ok = False
                break
        if not ok:
            break
    if ok:
        iso_lines.append(vecs)
print(f"lines: 1025 total, {len(iso_lines)} isotropic", file=sys.stderr)

count = 0
for c0 in range(1, 256):
    v0 = 0
    for s in range(8):
        if c0 >> s & 1:
            v0 ^= triv[s]
    for vecs in iso_lines:
        basis = [v0] + vecs
        print(' '.join(f'{g:07x}' for g in basis))
        count += 1
print(f"total emitted: {count}", file=sys.stderr)
