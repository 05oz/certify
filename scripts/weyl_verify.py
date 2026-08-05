#!/usr/bin/env python
"""
weyl_verify.py -- The canonical Weyl-algebra endomorphism attached to
Alpoge's Keller counterexample map (2026-07-19), the "quantum shadow".

Map (Keller, det JF = -2):
    F1 = (1+xy)^3 z + y^2 (1+xy)(4+3xy)
    F2 = y + 3x(1+xy)^2 z + 3x y^2 (4+3xy)
    F3 = 2x - 3x^2 y - x^3 z

Construction:
    JF   = Jacobian matrix of F,
    N    = adj(JF)/(-2) = (JF)^{-1}   (must have POLYNOMIAL entries),
    D_j  = sum_k N[k,j] * del_k       (first-order differential operators).

phi: W_3 -> W_3, x_i |-> F_i (multiplication), del_j |-> D_j is a
well-defined unital endomorphism of the third Weyl algebra iff

    (A) [D_j, F_i] = delta_ij   <=>   JF * N = Id        (9 identities), and
    (B) [D_i, D_j] = 0 for i<j  <=>   for all i<j, all l:
        sum_k ( N[k,i]*d(N[l,j])/dx_k - N[k,j]*d(N[l,i])/dx_k ) == 0
        (9 polynomial identities -- the real content).

The script checks polynomiality of N, (A), and all 9 identities of (B)
symbolically (sympy expand, identical vanishing), asserts everything,
prints PASS lines, and writes the fully expanded coefficients of
D_1, D_2, D_3 to weyl_endomorphism.txt.
"""

import os
import sympy as sp

OUTDIR = os.path.dirname(os.path.abspath(__file__))

x, y, z = sp.symbols('x y z')
V = [x, y, z]

u = 1 + x*y
F1 = u**3 * z + y**2 * u * (4 + 3*x*y)
F2 = y + 3*x*u**2 * z + 3*x*y**2 * (4 + 3*x*y)
F3 = 2*x - 3*x**2*y - x**3*z
F = [F1, F2, F3]

# ---------------------------------------------------------------- Jacobian
J = sp.Matrix(3, 3, lambda i, j: sp.diff(F[i], V[j]))

detJ = sp.expand(J.det())
assert detJ == -2, f"det JF != -2, got {detJ}"
print("PASS  det JF == -2 identically (Keller condition)")

# ------------------------------------------------- N = adj(JF)/(-2) = JF^{-1}
N = sp.Matrix(3, 3, lambda i, j: sp.expand(J.adjugate()[i, j] / sp.Integer(-2)))

# polynomiality: every entry must be a polynomial in x,y,z (rational coeffs)
for i in range(3):
    for j in range(3):
        e = N[i, j]
        assert e.is_polynomial(x, y, z), f"N[{i},{j}] not polynomial: {e}"
        p = sp.Poly(e, x, y, z)          # raises if not polynomial
        assert all(c.is_rational for c in p.coeffs()), \
            f"N[{i},{j}] has non-rational coefficient"
print("PASS  N = adj(JF)/(-2) has polynomial entries (all 9, rational coeffs)")

# ------------------------------------------------------------------ Check (A)
# [D_j, F_i] = sum_k N[k,j] * dF_i/dx_k = (JF * N)[i,j]  must equal delta_ij
A = sp.expand(J * N)
assert A == sp.eye(3), f"JF * N != Id:\n{A}"
print("PASS  (A) JF * N == Identity  =>  [D_j, F_i] = delta_ij for all i,j")

# ------------------------------------------------------------------ Check (B)
# [D_i, D_j] = sum_l ( sum_k N[k,i]*d(N[l,j])/dx_k - N[k,j]*d(N[l,i])/dx_k ) del_l
n_checked = 0
for i in range(3):
    for j in range(i + 1, 3):
        for l in range(3):
            expr = sp.Integer(0)
            for k in range(3):
                expr += N[k, i] * sp.diff(N[l, j], V[k]) \
                      - N[k, j] * sp.diff(N[l, i], V[k])
            expr = sp.expand(expr)
            assert expr == 0, \
                f"[D_{i+1}, D_{j+1}] coefficient of del_{l+1} nonzero:\n{expr}"
            n_checked += 1
            print(f"PASS  (B) [D_{i+1}, D_{j+1}]: coefficient of "
                  f"del_{l+1} vanishes identically")
assert n_checked == 9
print("PASS  (B) all 9 commutator identities vanish  =>  [D_i, D_j] = 0")

print()
print("ALL CHECKS PASS: phi: W_3 -> W_3, x_i |-> F_i, del_j |-> D_j is a")
print("well-defined unital endomorphism of the third Weyl algebra.")
print("(Injectivity is automatic: W_3 is simple and phi(1) = 1.)")

# ------------------------------------------------------------- operator stats
print()
print("Operator statistics (entries N[k,j] = coefficient of del_k in D_j):")
maxdeg = 0
maxterms = 0
for j in range(3):
    for k in range(3):
        p = sp.Poly(N[k, j], x, y, z)
        d = p.total_degree()
        t = len(p.terms())
        maxdeg = max(maxdeg, d)
        maxterms = max(maxterms, t)
        print(f"  N[{k+1},{j+1}] (D_{j+1}, coeff of del_{k+1}): "
              f"total degree {d}, {t} terms")
print(f"  max total degree = {maxdeg}, max term count = {maxterms}")

# ----------------------------------------------------- write operator file
outpath = os.path.join(OUTDIR, "weyl_endomorphism.txt")
with open(outpath, "w") as f:
    f.write(
"""The canonical Weyl-algebra endomorphism attached to Alpoge's Keller map
=======================================================================
(the "quantum shadow" of the Jacobian Conjecture counterexample in C^3,
 announced 2026-07-19; verified symbolically by weyl_verify.py)

Keller map (det JF = -2 identically):
  F1 = (1+xy)^3 z + y^2 (1+xy)(4+3xy)
  F2 = y + 3x(1+xy)^2 z + 3x y^2 (4+3xy)
  F3 = 2x - 3x^2 y - x^3 z

Let N = adj(JF)/(-2) = (JF)^{-1}, a 3x3 matrix with POLYNOMIAL entries
(verified). Define first-order differential operators

  D_j = N[1,j]*del_1 + N[2,j]*del_2 + N[3,j]*del_3     (j = 1,2,3),

where del_k = d/dx_k, (x_1,x_2,x_3) = (x,y,z). Then

  phi : W_3 -> W_3,   x_i |-> F_i (multiplication),  del_j |-> D_j

is a well-defined unital endomorphism of the third Weyl algebra:
  (A) [D_j, F_i] = delta_ij   (JF * N = Id, verified symbolically), and
  (B) [D_i, D_j] = 0 for all i,j (all 9 coefficient identities vanish
      identically, verified by sympy expand).

phi is automatically injective (W_3 is a simple ring and phi(1) = 1).
Non-surjectivity of phi is NOT conditional: it follows from the
order-filtration argument written out in the accompanying preprint
(Lemma 3.3): gr(phi) on order-zero symbols is the pullback F*, which is
not surjective because F is not injective (x separates the collision
fiber {(1,-3/2,13/2), (-1,3/2,13/2), (0,0,-1/4)}); phi preserves the
order filtration, so phi is a proper (injective, non-surjective)
endomorphism of W_3 in characteristic 0. See Bass-Connell-Wright 1982 /
Belov-Kanel--Kontsevich math/0512171 p.2 for the classical mechanism,
and Mayner's note (github.com/wmayner/dixmier-counterexample) for the
first public write-up, which this computation independently confirms.

Below: the nine fully expanded polynomial coefficients N[k,j].
""")
    for j in range(3):
        f.write("\n" + "=" * 71 + "\n")
        f.write(f"D_{j+1} = sum_k N[k,{j+1}] * del_k, with:\n")
        for k in range(3):
            e = sp.expand(N[k, j])
            f.write(f"\nN[{k+1},{j+1}]  (coefficient of del_{k+1} in D_{j+1}):\n")
            f.write(f"  {sp.sstr(e)}\n")
print(f"\nWrote fully expanded operators to: {outpath}")
