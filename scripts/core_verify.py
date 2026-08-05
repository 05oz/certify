#!/usr/bin/env python3
"""Core machine verification for the Alpoge degree-7 Keller map in C^3.
Everything asserts; script prints PASS lines. Run with sympy >= 1.12."""
import sympy as sp
from sympy import Rational as R

x, y, z = sp.symbols('x y z')
u = 1 + x*y; s = x**2*z
Aex = u**3*s + u*(u-1)**2*(3*u+1)
Bex = 3*u**2*s + 9*u**3 - 15*u**2 + 4*u + 2
Cex = 5 - 3*u - s
F1 = sp.expand(Aex/x**2); F2 = sp.expand(Bex/x); F3 = sp.expand(x*Cex)
assert all(f.is_polynomial(x, y, z) for f in (F1, F2, F3))
# match against Alpoge's published form
assert sp.expand(F1 - ((1+x*y)**3*z + y**2*(1+x*y)*(4+3*x*y))) == 0
assert sp.expand(F2 - (y + 3*x*(1+x*y)**2*z + 3*x*y**2*(4+3*x*y))) == 0
assert sp.expand(F3 - (2*x - 3*x**2*y - x**3*z)) == 0
print("PASS published form matches (F1,F2,F3), degrees:",
      [sp.Poly(f, x, y, z).total_degree() for f in (F1, F2, F3)])

J = sp.Matrix([[sp.diff(f, v) for v in (x, y, z)] for f in (F1, F2, F3)])
detJ = sp.expand(J.det())
assert detJ.is_number and detJ != 0
print("PASS det JF =", detJ, "(constant everywhere)")

P1 = (1, R(-3,2), R(13,2)); P2 = (-1, R(3,2), R(13,2)); P3 = (0, 0, R(-1,4))
vals = [tuple(f.subs(dict(zip((x,y,z), P))) for f in (F1,F2,F3)) for P in (P1,P2,P3)]
assert vals[0] == vals[1] == vals[2] == (R(-1,4), 0, 0)
print("PASS rational triple collision: F(1,-3/2,13/2)=F(-1,3/2,13/2)=F(0,0,-1/4)=(-1/4,0,0)")

# another rational fiber point demo (generic-side): (u,s)=(2,3)
Pd = (R(-1,4), -4, 48)
assert tuple(f.subs(dict(zip((x,y,z), Pd))) for f in (F1,F2,F3)) == (608, -232, 1)
print("PASS demo fiber point F(-1/4,-4,48) = (608,-232,1)")

# ------- downstairs plane map G and master equation -------
U, S, k = sp.symbols('U S k')
A = U**3*S + U*(U-1)**2*(3*U+1)
B = 3*U**2*S + 9*U**3 - 15*U**2 + 4*U + 2
C = 5 - 3*U - S
Jb = lambda f, g: sp.expand(sp.diff(f,U)*sp.diff(g,S) - sp.diff(f,S)*sp.diff(g,U))
p = sp.expand(1 + B*C); q = sp.expand(A*C**2)
assert sp.expand(Jb(p, q) - 2*C**2) == 0
print("PASS det JG = 2*(5-3u-s)^2  (Jacobian parks a full square on the line 3u+s=5)")
assert sp.expand(C*Jb(B,A) + 2*A*Jb(B,C) + B*Jb(C,A)) == 2
print("PASS bracket[C J(B,A) + 2A J(B,C) + B J(C,A)] = 2")

Af, Bf, Cf = (sp.Function(n)(U, S) for n in ('A','B','C'))
Jb2 = lambda f, g: sp.diff(f,U)*sp.diff(g,S) - sp.diff(f,S)*sp.diff(g,U)
lhs = Jb2(1 + Bf*Cf, Af*Cf**k)
rhs = Cf**k*(Cf*Jb2(Bf,Af) + k*Af*Jb2(Bf,Cf) + Bf*Jb2(Cf,Af))
assert sp.simplify(sp.expand(lhs - rhs)) == 0
print("PASS master equation, all weights k: det JG = C^k * bracket_k")

# restriction to the critical line C=0 (s = 5-3u): contracted to (1,0); Wronskian
a_l = sp.expand(A.subs(S, 5-3*U)); b_l = sp.expand(B.subs(S, 5-3*U))
assert a_l == sp.expand(U**2+U) and b_l == 4*U+2
assert sp.expand(b_l*a_l.diff(U) - 2*a_l*b_l.diff(U)) == 2
assert sp.expand(p.subs(S,5-3*U) - 1) == 0 and sp.expand(q.subs(S,5-3*U)) == 0
print("PASS on C=0: (A,B)|_line = (u^2+u, 4u+2), Wronskian b a' - 2 a b' = 2, line contracts to (1,0)")

# no-go lemma key identities (C=C0(u), A,B linear in s, general k)
kk = sp.symbols('kappa')
A0f, A1f, B0f, C0f = (sp.Function(n)(U) for n in ('A0','A1','B0','C0'))
Ag = A0f + A1f*S; Bg = B0f + kk*A1f*C0f**(k-1)*S; Cg = C0f
brg = sp.expand(Cg*Jb2(Bg,Ag) + k*Ag*Jb2(Bg,Cg) + Bg*Jb2(Cg,Ag))
target = sp.expand(A1f*sp.diff(C0f*B0f - kk*C0f**k*A0f, U))
assert sp.simplify(brg - target) == 0
lin = sp.expand((Bg*Cg) - kk*(Ag*Cg**k))   # = (p-1) - kappa*q
assert sp.simplify(lin.coeff(S, 1)) == 0
print("PASS no-go lemma: bracket = A1*(C0*B0 - kappa*C0^k*A0)' and (p-1)-kappa*q is s-free")
print("ALL CORE CHECKS PASS")
