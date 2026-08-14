#!/usr/bin/env python3
"""
Re-verification for the Part A erratum GATE, from the RAW map
F : C^3 -> C^3 (preprint sec. 1.2, displayed map eq. (2)).  SymPy over QQ,
exact arithmetic throughout.

NOT written from scratch, and NOT code-independent of the other scripts in
this repository.  Of the 115 executable lines of this file, 21 appear
verbatim in exhibit.py, exhibit2.py or structural.py and 4 in
scripts/dixmier_symplectic_verify.py:
  - the transcription of eq. (2), lines 81-83, is a 3-line byte-identical
    run with dixmier_symplectic_verify.py:15-17 -- a file the repository has
    carried since the v0.1.0 commit of 2026-08-04, two days before the
    erratum commit that added this one -- and with structural.py:65-67;
    lines 81-84 are a 4-line byte-identical run with exhibit.py:12-15 and
    with exhibit2.py:8-11;
  - the z-elimination make_h (99-103) is the same routine as
    exhibit.py:h1h2 (17-21): identical abstract syntax after consistent
    renaming, and 100-102 == exhibit.py:18-20 == exhibit2.py:14-16 byte for
    byte.  structural.py:80-81 carries the same two formulas spelled
    differently;
  - the downstairs data of eq. (ABC) at 155-158 is a 4-line byte-identical
    run with structural.py:27-30, and the Delta_1, Delta_2 literals at
    164-165 a 2-line run with structural.py:75-76 -- both sitting directly
    under the comment at line 154 that reads "independent derivation".
A pass here may therefore not be read, on its own, as an independent
re-derivation of eq. (2), of the z-elimination, or of the downstairs map.

Consequence for the gate.  The four erratum scripts hold ONE transcription
of eq. (2), not four.  A mistranscribed eq. (2) would be common-mode across
this gate and all three exhibits; they would agree on a wrong fibre count,
and exhibit.py and exhibit2.py contain no assertions at all.  What
constrains the transcription is local to this file: det JF == -2 (line 90)
and the three coeff_z(F_i) identities (95-97), the latter also fixing the
two multipliers make_h uses.

What is NOT shared, and what still is.  The upper bracket is this file's
alone: length_with_mult (105-118) reads the scheme length off a Groebner
staircase, and no other script under scripts/ computes a length at all.  So
are the seven separating linear forms and the empty-fibre vote (123-144), the
Delta_1 = 0 rational-point scan (188-204), and the four assertions.  The
LOWER bracket is shared.  Line 140, `sqf = pw.gcd(pw.diff(w))`, is
exhibit.py:35, exhibit2.py:38 and structural.py:88 with x for w -- byte
identical among those three -- and the degree difference at 141 is their 36,
39 and 89 with a different assignment target.  All four therefore count
distinct fibre points as deg P - deg gcd(P, P'); the three exhibits count in
x, assuming x separates, while this file counts in a generic w = a x + b y
and takes the max over seven forms, which is a strengthening but not a
different method.  Byte-identity alone hides this: inside 105-144 the only
lines occurring verbatim anywhere else under scripts/ are two `return None`,
two `continue` and one `return 0`, and the sharing is one character wide.  It
is recorded because it is what structural.py's 113-point sweep and this
file's fibre counts have in common.  The bracket is thus genuine on the
length side and common-mode on the distinct side.  (Disclosed 2026-08-14.)

Test: the Theorem-D statement of v0.1.0 and v0.1.1 said the fibre "drops
(generically) to two over the pullback of {Delta_2 = 0}".  The erratum claims
fibre size 2 is UNREACHABLE and the true set-theoretic fibre sizes are
{3, 1, 0}.  This script is the gate on that claim; since v0.1.2 (2026-08-06)
the preprint carries the corrected statement, and the quoted phrase survives
only inside the erratum notice.

Key structural fact used (exact): F1, F2, F3 are all LINEAR in z, with
  coeff_z(F1) = (1+xy)^3,  coeff_z(F2) = 3x(1+xy)^2,  coeff_z(F3) = -x^3.
So z is eliminated by exact polynomial combinations giving h1,h2 in QQ[x,y]:
  h1 = x^3 (F1-X) + (1+xy)^3 (F3-t)
  h2 = x^3 (F2-Y) + 3x(1+xy)^2 (F3-t)
For a target with t != 0 one checks h1(0,y) = -t != 0, so NO fibre point has
x = 0; hence {(x,y): h1=h2=0} maps bijectively (z recovered uniquely from F3=t)
onto the fibre.  Distinct fibre size = # distinct (x,y) roots -- counted
exactly via a random separating linear form w = a x + b y (a generic form
separates all points; take the max over several).
"""
import sys, itertools
import sympy as sp
from sympy import QQ, Rational, groebner, Poly, symbols

x, y, z, w = symbols('x y z w')

# ---- RAW map F (preprint sec. 1.2, displayed map eq. (2)), verbatim --------
F1 = (1 + x*y)**3 * z + y**2 * (1 + x*y) * (4 + 3*x*y)
F2 = y + 3*x*(1 + x*y)**2 * z + 3*x*y**2 * (4 + 3*x*y)
F3 = 2*x - 3*x**2*y - x**3*z
F = [sp.expand(F1), sp.expand(F2), sp.expand(F3)]

# ---- (0) det JF must be identically -2 ------------------------------------
JF = sp.Matrix([[sp.diff(Fi, v) for v in (x, y, z)] for Fi in F])
detJF = sp.expand(JF.det())
print("det JF =", detJF, "(expected -2)")
assert detJF == -2

# coefficients of z (confirm the linear-in-z structure) --------------------
cz = [sp.expand(sp.diff(Fi, z)) for Fi in F]
print("coeff_z(F1,F2,F3) =", cz, "(expected (1+xy)^3, 3x(1+xy)^2, -x^3)")
assert sp.expand(cz[0] - (1+x*y)**3) == 0
assert sp.expand(cz[1] - 3*x*(1+x*y)**2) == 0
assert sp.expand(cz[2] + x**3) == 0

def make_h(target):
    X, Y, t = target
    h1 = sp.expand(x**3*(F[0]-X) + (1+x*y)**3*(F[2]-t))
    h2 = sp.expand(x**3*(F[1]-Y) + 3*x*(1+x*y)**2*(F[2]-t))
    return h1, h2  # in QQ[x,y]; z already cancelled

def length_with_mult(target):
    h1, h2 = make_h(target)
    I = [Poly(h1, x, y, domain=QQ), Poly(h2, x, y, domain=QQ)]
    if I[0].is_zero or I[1].is_zero:
        return None
    G = groebner(I, x, y, order='grevlex')
    lead = [g.LM(order='grevlex') for g in G.polys]
    for i in range(2):  # 0-dim iff each variable has a pure-power leader
        if not any(lm[1-i] == 0 and lm[i] > 0 for lm in lead):
            return None
    md = [max(lm[i] for lm in lead) for i in range(2)]
    def divides(a, b): return all(ai <= bi for ai, bi in zip(a, b))
    return sum(1 for e in itertools.product(range(md[0]+1), range(md[1]+1))
               if not any(divides(lm, e) for lm in lead))

def distinct_points(target):
    """t != 0 assumed: no x=0 solutions, so distinct (x,y) roots = fibre size."""
    h1, h2 = make_h(target)
    forms = [(1, 2), (1, -3), (2, 1), (3, -5), (4, 7), (5, -2), (1, 11)]
    best, empty_votes = 0, 0
    for (a, b) in forms:
        polys = [Poly(h1, x, y, w, domain=QQ), Poly(h2, x, y, w, domain=QQ),
                 Poly(w - (a*x + b*y), x, y, w, domain=QQ)]
        G = groebner(polys, x, y, w, order='lex')
        univ = None
        for g in G.polys:
            if all(m[0] == 0 and m[1] == 0 for m in g.monoms()):
                univ = g
                break
        if univ is None:
            continue
        pw = Poly(univ.as_expr(), w, domain=QQ)
        if pw.total_degree() == 0:      # unit ideal on w -> empty fibre
            empty_votes += 1
            continue
        sqf = pw.gcd(pw.diff(w))
        best = max(best, pw.total_degree() - sqf.total_degree())
    if best == 0 and empty_votes > 0:
        return 0
    return best

def report(name, target):
    D = distinct_points(target)
    L = length_with_mult(target)
    print(f"  {name}: target=({target[0]},{target[1]},{target[2]})  "
          f"distinct_points={D}  length_w_mult={L}")
    sys.stdout.flush()
    return D, L

# ---- (1) independent derivation of Delta_1, Delta_2 -----------------------
u, s, p, q = symbols('u s p q')
A = u**3*s + u*(u-1)**2*(3*u+1)
B = 3*u**2*s + 9*u**3 - 15*u**2 + 4*u + 2
C = 5 - 3*u - s
g1 = sp.expand(1 + B*C - p)
g2 = sp.expand(A*C**2 - q)
res_s = sp.Poly(sp.expand(sp.resultant(g1, g2, s)), u)
fl = sp.factor_list(res_s.as_expr())
cubic_u = next(sp.expand(f) for f, m in fl[1] if sp.Poly(f, u).degree() == 3)
Delta1 = p**3 - 4*p**2 - 18*p*q + 5*p + 27*q**2 + 34*q - 2
Delta2 = p**3 - 3*p**2 - 18*p*q + 3*p + 54*q**2 + 18*q - 1
paper_cubic = Delta1*u**3 + ((p-1)**2 - 12*q)*u - 4*q
ratio = sp.cancel(sp.expand(cubic_u) / sp.expand(paper_cubic))
print("\nresultant cubic / paper cubic =", ratio, "(should be u-free constant in QQ(p,q))")
disc = sp.expand(sp.discriminant(sp.Poly(paper_cubic, u), u))
print("disc + 4*Delta1*Delta2^2 =", sp.expand(disc + 4*Delta1*Delta2**2), "(should be 0)")

def onD(D, pv, qv): return sp.expand(D.subs({p: pv, q: qv})) == 0

# ---- (2) DIRECT fibre counts over raw F (t = 1: target = (q, p-1, 1)) ------
print("\n=== DIRECT set-theoretic fibre counts over raw F (t=1) ===")
print("[generic]")
for (pv, qv) in [(0, 1), (2, 5), (-3, 2), (4, -1)]:
    if not onD(Delta1, pv, qv) and not onD(Delta2, pv, qv):
        report(f"generic (p,q)=({pv},{qv})", (qv, pv-1, 1))

print("[Delta_2 = 0, Delta_1 != 0  -- DISPUTED stratum]")
for (pv, qv) in [(-11, 4), (-11, -8)]:
    d1 = sp.expand(Delta1.subs({p: pv, q: qv}))
    print(f"    check: Delta2({pv},{qv})={sp.expand(Delta2.subs({p:pv,q:qv}))}, "
          f"Delta1={d1}")
    report(f"Delta2=0 (p,q)=({pv},{qv})", (qv, pv-1, 1))

print("[Delta_1 = 0 rational points (scan), excluding Gamma (7/3,4/27)]")
found = []
for pv in [Rational(k) for k in range(-15, 16)]:
    aa, bb, cc = 27, (-18*pv+34), (pv**3-4*pv**2+5*pv-2)
    dq = sp.expand(bb**2 - 4*aa*cc)
    if dq >= 0:
        r = sp.sqrt(dq)
        if r.is_rational:
            for sgn in (1, -1):
                qv = sp.nsimplify((-bb+sgn*r)/(2*aa))
                if onD(Delta1, pv, qv) and (pv, qv) not in found:
                    found.append((pv, qv))
for (pv, qv) in found:
    if (pv, qv) == (Rational(7,3), Rational(4,27)):
        continue
    d2 = sp.expand(Delta2.subs({p: pv, q: qv}))
    report(f"Delta1=0 (p,q)=({pv},{qv}) [Delta2={d2}]", (qv, pv-1, 1))

print("[Gamma point (7/3, 4/27) -- expect EMPTY]")
report("Gamma (p,q)=(7/3,4/27)", (Rational(4,27), Rational(7,3)-1, 1))
print("\nDONE")
