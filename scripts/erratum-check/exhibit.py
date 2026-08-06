#!/usr/bin/env python3
"""
Ironclad exhibit: over a target on the pullback of {Delta_2=0} (Delta_1 != 0),
display the EXACT preimages of raw F and verify each maps to the target.
Also {Delta_1=0} and Gamma.  x separates the fibre, so the lex GB (y>x) is in
shape position [P(x), y - r(x)]; z is recovered from F3=t (x != 0).
"""
import sympy as sp
from sympy import Rational, symbols, groebner, Poly, QQ

x, y, z = symbols('x y z')
F1 = (1 + x*y)**3 * z + y**2 * (1 + x*y) * (4 + 3*x*y)
F2 = y + 3*x*(1 + x*y)**2 * z + 3*x*y**2 * (4 + 3*x*y)
F3 = 2*x - 3*x**2*y - x**3*z
F = [sp.expand(F1), sp.expand(F2), sp.expand(F3)]

def h1h2(target):
    X, Y, t = target
    h1 = sp.expand(x**3*(F[0]-X) + (1+x*y)**3*(F[2]-t))
    h2 = sp.expand(x**3*(F[1]-Y) + 3*x*(1+x*y)**2*(F[2]-t))
    return h1, h2

def solve_fibre(target, label):
    print(f"\n=== {label}: target = {target} ===")
    h1, h2 = h1h2(target)
    G = groebner([Poly(h1, x, y, domain=QQ), Poly(h2, x, y, domain=QQ)],
                 y, x, order='lex')
    polys = list(G.polys)
    if len(polys) == 1 and polys[0].total_degree() == 0:
        print("  GB = [1]  ->  EMPTY fibre (0 preimages)")
        return []
    px = next((Poly(g.as_expr(), x, domain=QQ) for g in polys
               if all(m[0] == 0 for m in g.monoms())), None)
    print("  elim poly in x:", sp.factor(px.as_expr()))
    sqf = px.gcd(px.diff(x))
    ndist = px.total_degree() - sqf.total_degree()
    print(f"  degree={px.total_degree()}  #distinct x-roots={ndist}"
          f"  (radical? {'yes' if sqf.total_degree()==0 else 'NO'})")
    # shape-position generator giving y as a function of x
    ygen = next((g.as_expr() for g in polys
                 if any(m[0] == 1 for m in g.monoms())
                 and all(m[0] <= 1 for m in g.monoms())), None)
    yfun = None
    if ygen is not None:
        c1 = sp.Poly(ygen, y).coeff_monomial(y)
        c0 = sp.Poly(ygen, y).coeff_monomial(1)
        yfun = sp.cancel(-c0 / c1)   # y = -c0/c1  (mod P(x))
    pts = []
    for r, mult in px.all_roots(multiple=False):
        if yfun is not None:
            yr = sp.simplify(yfun.subs(x, r))
        else:
            yr = sp.solve(sp.gcd(sp.Poly(h1.subs(x, r), y),
                                 sp.Poly(h2.subs(x, r), y)).as_expr(), y)[0]
        zr = sp.simplify((2*r - 3*r**2*yr - target[2]) / r**3)
        chk = tuple(sp.simplify(sp.expand(Fi.subs({x: r, y: yr, z: zr})) - tv)
                    for Fi, tv in zip(F, target))
        uu = sp.radsimp(sp.simplify(1 + r*yr))
        ss = sp.radsimp(sp.simplify(r**2*zr))
        pts.append((r, yr, zr, uu, ss, chk, mult))
    print(f"  --> {len(pts)} distinct preimage point(s):")
    for (r, yr, zr, uu, ss, chk, mult) in pts:
        ok = all(c == 0 for c in chk)
        print(f"     x={sp.N(r,10)}  y={sp.N(yr,10)}  z={sp.N(zr,10)}")
        print(f"        u=1+xy={sp.nsimplify(sp.N(uu,20))}  s=x^2 z={sp.nsimplify(sp.N(ss,20))}"
              f"   F(pt)-target={chk}  EXACT-OK={ok}")
    uvals = [sp.nsimplify(sp.N(pt[3], 20)) for pt in pts]
    svals = [sp.nsimplify(sp.N(pt[4], 20)) for pt in pts]
    print("  u-values:", uvals)
    print("  s-values:", svals)
    return pts

solve_fibre((4, -12, 1),  "Delta2=0  (p,q)=(-11,4)")
solve_fibre((-8, -12, 1), "Delta2=0  (p,q)=(-11,-8)")
solve_fibre((5, 1, 1),    "generic   (p,q)=(2,5)")
solve_fibre((2, -7, 1),   "Delta1=0  (p,q)=(-6,2)")
solve_fibre((Rational(4,27), Rational(1,3), 1), "Gamma  (p,q)=(7/3,4/27)")
print("\nDONE")
