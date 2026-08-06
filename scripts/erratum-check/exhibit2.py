#!/usr/bin/env python3
"""Lean exact exhibit for the Delta_1=0 (fibre 1) and Gamma (empty) strata,
plus a recap of the disputed Delta_2=0 factorizations.  No slow radsimp."""
import sympy as sp
from sympy import Rational, symbols, groebner, Poly, QQ

x, y, z = symbols('x y z')
F1 = (1 + x*y)**3 * z + y**2 * (1 + x*y) * (4 + 3*x*y)
F2 = y + 3*x*(1 + x*y)**2 * z + 3*x*y**2 * (4 + 3*x*y)
F3 = 2*x - 3*x**2*y - x**3*z
F = [sp.expand(F1), sp.expand(F2), sp.expand(F3)]

def elim_x(target):
    X, Y, t = target
    h1 = sp.expand(x**3*(F[0]-X) + (1+x*y)**3*(F[2]-t))
    h2 = sp.expand(x**3*(F[1]-Y) + 3*x*(1+x*y)**2*(F[2]-t))
    G = groebner([Poly(h1, x, y, domain=QQ), Poly(h2, x, y, domain=QQ)],
                 y, x, order='lex')
    polys = list(G.polys)
    if len(polys) == 1 and polys[0].total_degree() == 0:
        return "UNIT (empty fibre)", polys
    px = next((Poly(g.as_expr(), x, domain=QQ) for g in polys
               if all(m[0] == 0 for m in g.monoms())), None)
    return px, polys

for tgt, lab in [((4,-12,1),"Delta2=0 (p,q)=(-11,4)"),
                 ((-8,-12,1),"Delta2=0 (p,q)=(-11,-8)"),
                 ((5,1,1),"generic (p,q)=(2,5)"),
                 ((2,-7,1),"Delta1=0 (p,q)=(-6,2)"),
                 ((-4,-4,1),"Delta1=0 (p,q)=(-3,-4)"),
                 ((Rational(4,27),Rational(4,3),1),"Gamma (p,q)=(7/3,4/27)")]:
    px, polys = elim_x(tgt)
    print(f"\n{lab}: target={tgt}")
    if isinstance(px, str):
        print("  reduced GB =", [sp.factor(g.as_expr()) for g in polys], "->", px)
        continue
    fac = sp.factor(px.as_expr())
    sqf = px.gcd(px.diff(x))
    nd = px.total_degree() - sqf.total_degree()
    print(f"  elim poly in x = {fac}")
    print(f"  degree={px.total_degree()}  distinct x-roots={nd}  "
          f"squarefree={'yes' if sqf.total_degree()==0 else 'NO'}")

# Exact confirmation of the Delta_1=0 single rational preimage (p,q)=(-6,2):
print("\nExact single preimage over Delta1=0 target (2,-7,1):")
sol = sp.solve([sp.Eq(F[0],2), sp.Eq(F[1],-7), sp.Eq(F[2],1)], [x,y,z], dict=True)
for d in sol:
    print("  ", d, " F=", tuple(sp.simplify(Fi.subs(d)) for Fi in F))

# Exact confirmation Gamma target has NO solution:
print("\nGamma target (4/27,4/3,1) [(p,q)=(7/3,4/27)]: solving F=target ->",
      sp.solve([sp.Eq(F[0],Rational(4,27)), sp.Eq(F[1],Rational(4,3)),
                sp.Eq(F[2],1)], [x,y,z], dict=True))
print("DONE")
