#!/usr/bin/env python3
"""Arithmetic of the degree-3 cover G(u,s) = (1+BC, AC^2): minimal cubic,
trace identity, discriminant factorization, S3 monodromy, s-rationality,
image/escape locus. All asserts."""
import sympy as sp

U, S, P, Q = sp.symbols('U S P Q')
A = U**3*S + U*(U-1)**2*(3*U+1)
B = 3*U**2*S + 9*U**3 - 15*U**2 + 4*U + 2
C = 5 - 3*U - S
p = sp.expand(1 + B*C); q = sp.expand(A*C**2)

# eliminate S
Res = sp.resultant(p - P, q - Q, S)
fl = sp.factor_list(sp.expand(Res))
print("resultant factors (deg_U, mult):", [(sp.degree(f, U), m) for f, m in fl[1]])
cub = [f for f, m in fl[1] if sp.degree(f, U) == 3]
assert len(cub) == 1
cubic = sp.Poly(cub[0], U)
c3, c2, c1, c0 = cubic.all_coeffs()
# sign-normalize so leading coeff matches Delta1
D1 = P**3 - 4*P**2 - 18*P*Q + 5*P + 27*Q**2 + 34*Q - 2
if sp.expand(c3 + D1) == 0:
    c3, c2, c1, c0 = [-t for t in (c3, c2, c1, c0)]
assert sp.expand(c3 - D1) == 0
print("PASS leading coefficient = Delta1 = P^3-4P^2-18PQ+5P+27Q^2+34Q-2")
assert sp.expand(c2) == 0
print("PASS trace identity: no U^2 term  =>  u1+u2+u3 = 0 on every fiber")
print("cubic: Delta1*U^3 + (", sp.factor(c1), ")*U + (", sp.factor(c0), ")")
assert cubic.as_expr().subs({U: 2, P: -231, Q: 608}) == 0   # sanity vs demo fiber
assert D1.subs({P: 1, Q: 0}) == 0                            # image of critical line

# discriminant = -4 * Delta1 * Delta2^2
disc = sp.discriminant(c3*U**3 + c1*U + c0, U)
quo = sp.cancel(disc / (-4*D1))
qf = sp.factor_list(sp.expand(quo))
assert all(m % 2 == 0 for _, m in qf[1]) and qf[0] > 0
Delta2 = sp.sqrt(sp.factor(quo))
assert sp.expand(disc + 4*D1*sp.expand(Delta2**2)) == 0
print("PASS disc = -4 * Delta1 * Delta2^2 with Delta2 =", sp.factor(Delta2))
# S3: cubic irreducible (it is an irreducible factor of Res, positive U-degree,
# hence irreducible over Q(P,Q) by Gauss); disc is a square iff -Delta1 is;
# Delta1 is irreducible of odd P-degree, so not (a square)*(unit):
assert len(sp.factor_list(D1)[1]) == 1 and sp.factor_list(D1)[1][0][1] == 1
print("PASS Delta1 irreducible => disc not a square => monodromy = full S3 (not Galois)")

# s is rational in (u,p,q): first-degree subresultant
prs = sp.subresultants(sp.Poly(p - P, S), sp.Poly(q - Q, S))
lin = [f for f in prs if sp.degree(sp.Poly(f, S), S) == 1]
assert lin
e = sp.Poly(lin[-1], S)
s_of = sp.cancel(-e.nth(0)/e.nth(1))          # s = rational function of (U,P,Q)
chk = sp.cancel(s_of.subs({P: p, Q: q}) - S)  # must vanish identically
assert chk == 0
print("PASS s in Q(u,p,q)  =>  [C(u,s):C(p,q)] = 3 exactly; F is generically 3:1")

# escape/image analysis: fibers with c != 0 exist unless cubic degenerates
g = sp.groebner([sp.expand(c3), sp.expand(c1)], P, Q, order='lex')
print("V(Delta1, c1) Groebner (deg drop to <=1 locus):", [sp.factor(t) for t in g.exprs])
sols = sp.solve([c3, c1], [P, Q], dict=True)
print("common zeros of (Delta1, c1):", len(sols))
bad = []
for so in sols:
    c0v = sp.simplify(c0.subs(so))
    if sp.simplify(c0v) != 0:
        # cubic has no root here; check original system directly
        raw = sp.solve([sp.expand(p - so[P]), sp.expand(q - so[Q])], [U, S], dict=True)
        bad.append((so, c0v, len(raw)))
for so, c0v, n in bad:
    print("candidate empty fiber over (P,Q)=", so, " c0=", sp.nsimplify(c0v), " direct solutions:", n)
# ASSERTED (not just printed): the unique degenerate-and-nonzero candidate is (7/3, 4/27),
# and its emptiness carries a Nullstellensatz certificate over QQ (unit ideal).
assert len(bad) == 1 and bad[0][0] == {P: sp.Rational(7, 3), Q: sp.Rational(4, 27)} and bad[0][2] == 0
G713 = sp.groebner([sp.expand(p) - sp.Rational(7, 3), sp.expand(q) - sp.Rational(4, 27)], U, S)
assert list(G713.exprs) == [1]
print("PASS empty fiber exactly over (7/3, 4/27), certified: ideal = (1) over QQ")
# u=0 sheet: q(0,s)=0 identically, p(0,s)=11-2s covers all P at Q=0
assert sp.expand(q.subs(U, 0)) == 0 and sp.expand(p.subs(U, 0) - (11 - 2*S)) == 0
print("PASS u=0 sheet covers the whole line Q=0")
print("ALL COVER CHECKS PASS")
