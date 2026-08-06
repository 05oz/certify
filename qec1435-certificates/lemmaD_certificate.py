#!/usr/bin/env python3
"""LEMMA D exact certificate (stdlib only).

CLAIM: every additive (9, 2^15) code over GF(4) (equivalently every
15-dimensional F2-subspace of the 18-dim binary symplectic space of 9
qubits) has at least 1471 nonzero vectors of symplectic weight <= 4.

Same LP/Krawtchouk-positivity scheme as Lemma C (see lemmaC_certificate.py).
Used to close the (d0=3, e=2) branch of a hypothetical [[14,3,5]] with an
order-5 automorphism of cycle type (5-cycle + 9 fixed qubits): there the
fixed-space W has dim >= 18 - 3 = 15 and at most 2^3 - 1 = 7 low-weight
exceptions are allowed; 1471 > 7.
"""
from fractions import Fraction as F
from math import comb

def K(j, w, n=9):
    return sum((-1)**s * 3**(j - s) * comb(w, s) * comb(n - w, j - s)
               for s in range(min(j, w) + 1))

n = 9
size = 2**15
mu = F(811, 16384)
lam = [F(0), F(1455, 65536), F(255, 32768), F(105, 65536), F(0),
       F(19, 65536), F(25, 32768), F(45, 65536), F(5, 16384), F(55, 65536)]

assert all(l >= 0 for l in lam)
for w in range(1, n + 1):
    e = F(1 if w <= 4 else 0) - mu - sum(lam[j] * K(j, w) for j in range(n + 1))
    assert e >= 0, (w, e)
bound = (size - 1) * mu - sum(lam[j] * K(j, 0) for j in range(n + 1))
assert bound == 1471, bound
print("LEMMA D CERTIFIED: every additive (9, 2^15) code has >= 1471 nonzero")
print("vectors of symplectic weight <= 4.  (exact rational verification)")
