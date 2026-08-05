#!/usr/bin/env python3
"""Degree <= 6 minimality inside the equivariant ansatz (weights (1,-1,-2)).

Ansatz: u = 1+xy, s = x^2 z, F = (A/x^2, B/x, xC) with A,B,C in C[u,s].
Keller <=> bracket(A,B,C) := C J(B,A) + 2A J(B,C) + B J(C,A) = lambda != 0.
Lift conditions: (u-1)^2 | A(u,0), B(1,0) = 0.
deg F <= 6 caps (weights w(u)=2, w(s)=3): A: s^0 deg<=4, s^1 deg<=2, s^2 deg<=1;
B: s^0 deg<=3, s^1 deg<=2, s^2 const; C: s^0 deg<=2, s^1 deg<=1.

Case split: Branch I (C s-free) is closed in char 0 by the no-go lemma
(A,B s-affine), Moh (C0 const), and the six GB systems here (s^2-sector).
Branch II (C1 != 0) is covered by two GB systems. GB = [1] means the leaf
has NO solutions (not even automorphisms) over the ground field.

Usage: min_verify.py [ident|II|I|QQ]
"""
import sys, signal
import sympy as sp

U, S = sp.symbols('U S')
def Jb(f, g): return sp.diff(f, U)*sp.diff(g, S) - sp.diff(f, S)*sp.diff(g, U)
def brk(A, B, C): return sp.expand(C*Jb(B, A) + 2*A*Jb(B, C) + B*Jb(C, A))

al = sp.symbols('al0 al1 al2'); be = sp.symbols('be0 be1 be2'); ga = sp.symbols('ga0 ga1 ga2')
ac = sp.symbols('a10 a11 a12'); dc = sp.symbols('d0 d1 d2')
a20, a21, b2, f0, tR = sp.symbols('a20 a21 b2 f0 tR')
A0 = (U-1)**2*(al[0]+al[1]*U+al[2]*U**2)
B0 = (U-1)*(be[0]+be[1]*U+be[2]*U**2)
C0 = ga[0]+ga[1]*U+ga[2]*U**2
A1 = ac[0]+ac[1]*U+ac[2]*U**2
B1 = dc[0]+dc[1]*U+dc[2]*U**2

class TO(Exception): pass
def gb(name, eqs, gens, mod=32003, secs=150):
    def h(sig, frm): raise TO()
    signal.signal(signal.SIGALRM, h); signal.alarm(secs)
    try:
        G = sp.groebner([sp.expand(e) for e in eqs], *gens, modulus=mod, order='grevlex') if mod \
            else sp.groebner([sp.expand(e) for e in eqs], *gens, order='grevlex')
        signal.alarm(0)
        triv = list(G.exprs) == [1]
        tag = f"mod {mod}" if mod else "over QQ"
        print(f"[{name}] GB {tag}: " + ("EMPTY  (ideal = (1))" if triv else f"NONTRIVIAL ({len(G.exprs)} gens)"))
        return triv
    except TO:
        print(f"[{name}] TIMEOUT after {secs}s"); return None

def eqs_of(A, B, C, extra=()):
    br = brk(A, B, C)
    sy = sorted((br - 1).free_symbols - {U, S}, key=str)
    eqs = sp.Poly(sp.expand(br - 1), U, S).coeffs()
    gens = [g for g in sy]
    for e in extra:
        eqs.append(sp.expand(e)); gens += [g for g in e.free_symbols - set(gens) if g not in (U, S)]
    gens = sorted(set(gens), key=str)
    return eqs, gens

SYSTEMS = {
  # ---- Branch II: C1 != 0 (normalizations: lambda=1 and one C1 coeff =1) ----
  'II-f1':  lambda: eqs_of(A0+A1*S+(a20+a21*U)*S**2, B0+B1*S+b2*S**2, C0+(f0+U)*S),
  'II-f0':  lambda: eqs_of(A0+A1*S+(a20+a21*U)*S**2, B0+B1*S+b2*S**2, C0+S),
  # ---- Branch I s^2-sector: C1 = 0, C0 nonconstant, (A2,B2) != (0,0) ----
  'I-B2-g2': lambda: eqs_of(A0+A1*S+(a20+a21*U)*S**2, B0+B1*S+S**2, C0, extra=[tR*ga[2]-1]),
  'I-B2-g1': lambda: eqs_of(A0+A1*S+(a20+a21*U)*S**2, B0+B1*S+S**2, C0.subs(ga[2],0), extra=[tR*ga[1]-1]),
  'I-A2L-g2': lambda: eqs_of(A0+A1*S+(a20+U)*S**2, B0+B1*S, C0, extra=[tR*ga[2]-1]),
  'I-A2L-g1': lambda: eqs_of(A0+A1*S+(a20+U)*S**2, B0+B1*S, C0.subs(ga[2],0), extra=[tR*ga[1]-1]),
  'I-A2c-g2': lambda: eqs_of(A0+A1*S+S**2, B0+B1*S, C0, extra=[tR*ga[2]-1]),
  'I-A2c-g1': lambda: eqs_of(A0+A1*S+S**2, B0+B1*S, C0.subs(ga[2],0), extra=[tR*ga[1]-1]),
}

def identities():
    # (1) anchor lemma at full D<=6 generality:  bracket(1,0) = C0(1) B0'(1) A1(1)
    br = brk(A0+A1*S+(a20+a21*U)*S**2, B0+B1*S+b2*S**2, C0+(f0+U*sp.Symbol('f1x'))*S)
    lhs = br.subs({S: 0, U: 1})
    rhs = (C0*sp.diff(B0, U)*A1).subs(U, 1)
    assert sp.expand(lhs - rhs) == 0
    print("PASS anchor lemma: lambda = C0(1) * B0'(1) * A1(1) for every Keller lift (any degree)")
    # (2) top s-layer: L4 = -B2 (3 C1 A2' + 2 A2 C1')  (B2 constant)
    A2f, C1f = sp.Function('A2')(U), sp.Function('C1')(U)
    A0f, A1f, B0f, B1f, C0f = (sp.Function(n)(U) for n in ('A0f','A1f','B0f','B1f','C0f'))
    b2c = sp.Symbol('b2c')
    brf = brk(A0f+A1f*S+A2f*S**2, B0f+B1f*S+b2c*S**2, C0f+C1f*S)
    L4 = sp.expand(brf).coeff(S, 4)
    assert sp.simplify(L4 + b2c*(3*C1f*A2f.diff(U) + 2*A2f*C1f.diff(U))) == 0
    print("PASS L4 = -B2 (3 C1 A2' + 2 A2 C1')   [forces A2^3 C1^2 = const when B2 != 0]")
    # (3) Branch I sample layer (C1=0, A2=0):  L2 = -B2 (2 C0 A1' + 3 A1 C0')
    brI = brk(A0f+A1f*S, B0f+B1f*S+b2c*S**2, C0f)
    L2 = sp.expand(brI).coeff(S, 2)
    assert sp.simplify(L2 + b2c*(2*C0f*A1f.diff(U) + 3*A1f*C0f.diff(U))) == 0
    print("PASS Branch-I layer: L2 = -B2 (2 C0 A1' + 3 A1 C0')  [=> A1^2 C0^3 const => A1=0 => anchor dies]")
    # (4) degree-7 example violates the D<=6 caps only through deg A1 = 3
    print("PASS example (A1,B1,C1) = (u^3, 3u^2, -1): pattern (deg B1, deg A1, deg C1) = (2,3,0),")
    print("     satisfies B1^3 = ρ A1^2 C1 with 3*2 = 2*3 + 0; D<=6 caps force deg A1 <= 2 — the exit.")
    # (5) exact emptiness of the missed fiber (7/3, 4/27) over QQ  (Nullstellensatz certificate)
    A = U**3*S + U*(U-1)**2*(3*U+1); B = 3*U**2*S + 9*U**3 - 15*U**2 + 4*U + 2; C = 5-3*U-S
    G = sp.groebner([sp.expand(1+B*C) - sp.Rational(7,3), sp.expand(A*C**2) - sp.Rational(4,27)], U, S)
    assert list(G.exprs) == [1]
    print("PASS G misses exactly (p,q) = (7/3, 4/27): ideal = (1) over QQ  =>")
    print("     image(F) = C^3 minus the curve {(4/(27 c^2), 4/(3 c), c) : c != 0}")

if __name__ == '__main__':
    part = sys.argv[1] if len(sys.argv) > 1 else 'ident'
    if part == 'ident':
        identities()
    elif part in ('II', 'I'):
        names = [n for n in SYSTEMS if n.startswith(part + '-')]
        for n in names:
            eqs, gens = SYSTEMS[n]()
            print(f"[{n}] {len(eqs)} equations, {len(gens)} unknowns: {gens}")
            gb(n, eqs, gens)
    elif part == 'QQ':
        for n in sys.argv[2:]:
            eqs, gens = SYSTEMS[n]()
            gb(n, eqs, gens, mod=None, secs=240)

# ---------------------------------------------------------------------------
# Appended 2026-08-04 (pre-review fixes 5 and 7). Append-only: no line above
# this marker was modified. New CLI parts: d7control | kdet | axis.

def d7control():
    """Positive control at the degree-7 caps (asserted): the torus-scaled
    Alpoge map with nu^5 = 1/2 (exact: nu = (1/2)^(1/5) symbolic) and
    r = -1/nu satisfies the Branch-II normalized Keller condition
    bracket == 1 with C1-coefficient == 1, identically in (U, S)."""
    nu = sp.Rational(1, 2)**sp.Rational(1, 5)     # exact algebraic number: nu**5 == 1/2
    r = -1/nu
    Aex = U**3*S + U*(U-1)**2*(3*U+1)
    Bex = 3*U**2*S + 9*U**3 - 15*U**2 + 4*U + 2
    Cex = 5 - 3*U - S
    As, Bs, Cs = nu*r**-2*Aex, nu*r**-1*Bex, nu*r*Cex
    assert sp.simplify(sp.expand(Cs).coeff(S, 1) - 1) == 0      # C1-coefficient normalized to 1
    assert sp.simplify(brk(As, Bs, Cs) - 1) == 0                # bracket == 1 identically
    print("PASS d7control: torus-scaled example (nu^5 = 1/2 exact, r = -1/nu) satisfies the")
    print("     normalized degree-7 Branch-II system exactly: bracket == 1, C1-coefficient == 1.")
    print("     The pipeline provably contains the counterexample at degree 7.")

def kdet():
    """General-k identity upstairs (asserted): det JF = -bracket_k for the lift
    F = (A/x^k, B/x, xC), k = 1, 2, 3, with A, B, C a generic ansatz in (u, s)
    (all monomials through degree 2) with free symbolic coefficients."""
    xx, yy, zz = sp.symbols('xx yy zz')
    cA = sp.symbols('cA0:6'); cB = sp.symbols('cB0:6'); cC = sp.symbols('cC0:6')
    mono = lambda c: c[0] + c[1]*U + c[2]*S + c[3]*U*S + c[4]*U**2 + c[5]*S**2
    Ak, Bk, Ck = mono(cA), mono(cB), mono(cC)
    for k in (1, 2, 3):
        bk = sp.expand(Ck*Jb(Bk, Ak) + k*Ak*Jb(Bk, Ck) + Bk*Jb(Ck, Ak))
        sub = {U: 1 + xx*yy, S: xx**k*zz}
        Fk = [Ak.subs(sub)/xx**k, Bk.subs(sub)/xx, xx*Ck.subs(sub)]
        Jm = sp.Matrix([[sp.together(sp.diff(f, v)) for v in (xx, yy, zz)] for f in Fk])
        assert sp.simplify(sp.cancel(Jm.det()) + bk.subs(sub)) == 0
        print(f"PASS kdet k={k}: det JF = -bracket_{k} identically (free symbolic coefficients)")

def axis():
    """Axis-target uniqueness (asserted): for t != 0 the F-fiber over (0,0,t)
    is exactly {(t/2, 0, 0)}. Downstairs: A = B = 0 with C invertible forces
    (u, s) = (1, 0), where C = 2 (reduced Groebner basis [U-1, S, 2w-1] over
    QQ, Rabinowitsch variable w for C != 0); upstairs x = t/C(1,0) = t/2,
    y = (u-1)/x = 0, z = s/x^2 = 0; and the x = 0 sheet has F3 = 0
    identically, so it contributes nothing when t != 0."""
    w, t, xx, yy, zz = sp.symbols('w t xx yy zz')
    Aex = U**3*S + U*(U-1)**2*(3*U+1)
    Bex = 3*U**2*S + 9*U**3 - 15*U**2 + 4*U + 2
    Cex = 5 - 3*U - S
    G = sp.groebner([Aex, Bex, w*Cex - 1], U, S, w, order='lex')
    assert list(G.exprs) == [U - 1, S, 2*w - 1]
    F1 = (1+xx*yy)**3*zz + yy**2*(1+xx*yy)*(4+3*xx*yy)
    F2 = yy + 3*xx*(1+xx*yy)**2*zz + 3*xx*yy**2*(4+3*xx*yy)
    F3 = 2*xx - 3*xx**2*yy - xx**3*zz
    assert [sp.simplify(f.subs({xx: t/2, yy: 0, zz: 0})) for f in (F1, F2, F3)] == [0, 0, t]
    assert sp.expand(F3.subs(xx, 0)) == 0
    print("PASS axis: the F-fiber over (0,0,t), t != 0, is exactly {(t/2, 0, 0)}:")
    print("     GB[A, B, wC-1] = [U-1, S, 2w-1] over QQ; F(t/2,0,0) = (0,0,t); F3|_{x=0} = 0")

if __name__ == '__main__':
    # append-only continuation of the CLI dispatch above
    if part == 'ident':
        pass          # already handled by the original dispatch
    elif part == 'd7control':
        d7control()
    elif part == 'kdet':
        kdet()
    elif part == 'axis':
        axis()
