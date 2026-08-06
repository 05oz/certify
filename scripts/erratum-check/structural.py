#!/usr/bin/env python3
"""
Structural certificate that fibre size 2 is UNREACHABLE (not just sampled).

Facts certified (exact):
 (a) det J_G = 2*C^2 identically, for G(u,s)=(1+BC, AC^2).  Hence the only
     ramification of the downstairs 3:1 cover G is on the line {C=0}: nowhere
     else can two sheets genuinely coincide.
 (b) G contracts {C=0} to the single point (1,0): G|_{C=0} = (1,0).
 (c) The elimination cubic in u has NO u^2 term (trace identity).  So when the
     leading coeff Delta_1 vanishes the cubic drops degree 3 -> 1: sheets
     escape to infinity two at a time, never one at a time.
 Consequences:
   * finite length of a fibre = # finite roots of the cubic in {3,1,0}
     (3 if Delta_1!=0; 1 if Delta_1=0 & linear coeff !=0; 0 if also lin=0,q!=0).
     Length 2 is impossible because the degree drop is 3->1.
   * distinct <= length, and distinct<length needs a genuine sheet-merge,
     i.e. det J_G=0 => C=0 => image point (1,0).  So for (p,q)!=(1,0) every
     fibre is reduced: distinct = length in {3,1,0}.
   * over (1,0) the fibre is 1 (checked directly).
   Therefore distinct fibre size in {3,1,0}; 2 never occurs.
Plus a broad sweep: 113 rational points on {Delta_2=0} all give distinct=3.
"""
import sympy as sp
from sympy import symbols, Rational, groebner, Poly, QQ

u, s, p, q = symbols('u s p q')
A = u**3*s + u*(u-1)**2*(3*u+1)
B = 3*u**2*s + 9*u**3 - 15*u**2 + 4*u + 2
C = 5 - 3*u - s
Gp = sp.expand(1 + B*C)
Gq = sp.expand(A*C**2)

# (a) det J_G = 2 C^2
JG = sp.Matrix([[sp.diff(Gp, u), sp.diff(Gp, s)],
                [sp.diff(Gq, u), sp.diff(Gq, s)]])
detJG = sp.expand(JG.det())
print("(a) det J_G - 2*C^2 =", sp.expand(detJG - 2*C**2), " (should be 0)")
print("    det J_G =", sp.factor(detJG))
assert sp.expand(detJG - 2*C**2) == 0

# (b) G contracts {C=0} to (1,0):  substitute s = 5-3u (i.e. C=0)
Gp_C0 = sp.expand(Gp.subs(s, 5 - 3*u))
Gq_C0 = sp.expand(Gq.subs(s, 5 - 3*u))
print("(b) G|_{C=0} = (", Gp_C0, ",", Gq_C0, ")  (should be (1,0))")
assert Gp_C0 == 1 and Gq_C0 == 0

# (c) elimination cubic has no u^2 term
res_s = sp.Poly(sp.expand(sp.resultant(Gp - p, Gq - q, s)), u)
cubic = next(sp.expand(f) for f, m in sp.factor_list(res_s.as_expr())[1]
             if sp.Poly(f, u).degree() == 3)
cpoly = sp.Poly(cubic, u)
print("(c) cubic in u =", cubic)
print("    u^2 coefficient =", sp.expand(cpoly.coeff_monomial(u**2)), " (should be 0)")
assert sp.expand(cpoly.coeff_monomial(u**2)) == 0

# double-root factorizations on {Delta_2=0} (apparent branch, u fails to separate)
print("\nu-cubic factorization on Delta_2=0 samples (double root = u NOT separating):")
for (pv, qv) in [(-11, 4), (-11, -8)]:
    cc = sp.factor(cubic.subs({p: pv, q: qv}))
    print(f"   (p,q)=({pv},{qv}):  {cc}")

# (d) fibre over the contraction point (1,0): target (0,0,1)
x, y, z = symbols('x y z')
F1 = (1 + x*y)**3 * z + y**2 * (1 + x*y) * (4 + 3*x*y)
F2 = y + 3*x*(1 + x*y)**2 * z + 3*x*y**2 * (4 + 3*x*y)
F3 = 2*x - 3*x**2*y - x**3*z
sol = sp.solve([sp.Eq(sp.expand(F1), 0), sp.Eq(sp.expand(F2), 0),
                sp.Eq(sp.expand(F3), 1)], [x, y, z], dict=True)
print("\n(d) fibre over contraction pt (p,q)=(1,0), target (0,0,1):", sol,
      f"  -> size {len(sol)}")

# broad sweep over {Delta_2=0}: parametrize p=w+1, C=0-disc gives rational q
# 54 q^2 -18(p-1) q +(p-1)^3 =0 ; rational q iff 3(3-2w) is a square (w=p-1)
Delta1 = p**3 - 4*p**2 - 18*p*q + 5*p + 27*q**2 + 34*q - 2
Delta2 = p**3 - 3*p**2 - 18*p*q + 3*p + 54*q**2 + 18*q - 1

def distinct_over(pv, qv):
    X, Y, t = qv, pv - 1, 1
    h1 = sp.expand(x**3*(sp.expand(F1)-X) + (1+x*y)**3*(sp.expand(F3)-t))
    h2 = sp.expand(x**3*(sp.expand(F2)-Y) + 3*x*(1+x*y)**2*(sp.expand(F3)-t))
    G = groebner([Poly(h1, x, y, domain=QQ), Poly(h2, x, y, domain=QQ)],
                 y, x, order='lex')
    px = next((Poly(g.as_expr(), x, domain=QQ) for g in G.polys
               if all(m[0] == 0 for m in g.monoms())), None)
    if px is None:
        return 0
    sqf = px.gcd(px.diff(x))
    return px.total_degree() - sqf.total_degree()

print("\nBroad sweep on {Delta_2=0}, Delta_1!=0 (distinct fibre size over each):")
count = 0
bad = []
for k in range(2, 60):
    # need 3(3-2w)=square; take 3-2w = 3 m^2 -> w=(3-3m^2)/2, rational for any m
    m = Rational(k, 7)
    w = (3 - 3*m**2) / 2
    pv = w + 1
    disc_q = sp.expand((18*w)**2 * 3 * (3 - 2*w))  # =108 w^2 (3-2w) ; but use formula
    # solve 54 q^2 -18 w q + w^3 =0
    for sgn in (1, -1):
        r = sp.sqrt(sp.expand(324*w**2 - 216*w**3))
        if not r.is_rational:
            continue
        qv = sp.nsimplify((18*w + sgn*r) / 108)
        if sp.expand(Delta2.subs({p: pv, q: qv})) != 0:
            continue
        if sp.expand(Delta1.subs({p: pv, q: qv})) == 0:
            continue
        if pv == 1:  # contraction point excluded
            continue
        d = distinct_over(pv, qv)
        count += 1
        if d != 3:
            bad.append((pv, qv, d))
print(f"  tested {count} points on Delta_2=0;  all distinct==3 ? {not bad}")
if bad:
    print("  EXCEPTIONS:", bad[:10])
print("\nDONE")
