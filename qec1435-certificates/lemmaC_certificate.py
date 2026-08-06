#!/usr/bin/env python3
"""LEMMA C exact certificate (stdlib only).

CLAIM: every F2-linear subspace W of dimension 9 of the 14-dimensional
binary symplectic space of 7 qubits (equivalently: every additive code
C < GF(4)^7 with |C| = 2^9 = 512, weight = number of nonzero GF(4)
coordinates = symplectic weight) has at least 52 nonzero vectors of
weight <= 4.  (Subspaces of dimension > 9 inherit the bound from any
9-dimensional subspace.)

PROOF (linear programming / Krawtchouk positivity, exact rationals):
For an additive code C over GF(4), length n=7, the trace-dual weight
distribution B_j = (1/|C|) sum_w A_w K_j(w) is a vector of nonnegative
counts (MacWilliams for additive GF(4) codes, Calderbank-Rains-Shor-
Sloane), where K_j(w) = sum_s (-1)^s 3^(j-s) C(w,s) C(n-w,j-s).

Take mu = 5/32 and lambda = (0, 27/256, 0, 0, 0, 1/256, 0, 1/384) >= 0.
This script verifies EXACTLY that
    e(w) := [w<=4] - mu - sum_j lambda_j K_j(w) >= 0   for w = 1..7.
Then for any (7, 2^9) additive code (sum_{w>=1} A_w = 511):
  A_{1..4} = sum_{w=1..4} A_w
           >= sum_{w>=1} A_w (mu + sum_j lambda_j K_j(w))
           =  511 mu + sum_j lambda_j (512 B_j - K_j(0))
           >= 511 mu - sum_j lambda_j K_j(0)          (B_j >= 0)
and the script verifies exactly that the last quantity equals 52. QED
"""
from fractions import Fraction as F
from math import comb

def K(j, w, n=7):
    return sum((-1)**s * 3**(j - s) * comb(w, s) * comb(n - w, j - s)
               for s in range(min(j, w) + 1))

mu = F(5, 32)
lam = [F(0), F(27, 256), F(0), F(0), F(0), F(1, 256), F(0), F(1, 384)]

assert all(l >= 0 for l in lam), "lambda must be nonnegative"
for w in range(1, 8):
    e = F(1 if w <= 4 else 0) - mu - sum(lam[j] * K(j, w) for j in range(8))
    assert e >= 0, (w, e)
bound = 511 * mu - sum(lam[j] * K(j, 0) for j in range(8))
assert bound == 52, bound
print("LEMMA C CERTIFIED: every additive (7, 2^9) code has >= 52 nonzero")
print("vectors of symplectic weight <= 4.  (exact rational verification)")
