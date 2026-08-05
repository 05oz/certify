"""Machine checks for the two structural claims:
(1) D_i := rows of (JF)^{-T} applied to grad, i.e. D_i = sum_j B[i,j] d/dx_j with
    B = (JF^{-1})^T, are pairwise-commuting polynomial vector fields with D_i(F_j)=delta_ij.
    => Psi: x_i -> F_i, d_i -> D_i is a well-defined endomorphism of the Weyl algebra A_3
       preserving the canonical commutation relations. Non-surjective since F is 3:1.
(2) The cotangent lift Phi(q,p) = (F(q), B(q) p) is a POLYNOMIAL map C^6 -> C^6 whose
    Jacobian M satisfies M^T J M = J exactly (a polynomial symplectomorphism, det = +1),
    and Phi is generically 3:1 (inherits F's fibers), i.e. non-invertible.
"""
import sympy as sp

x, y, z = sp.symbols('x y z')
q = sp.Matrix([x, y, z])

F1 = (1 + x*y)**3 * z + y**2 * (1 + x*y) * (4 + 3*x*y)
F2 = y + 3*x*(1 + x*y)**2 * z + 3*x*y**2 * (4 + 3*x*y)
F3 = 2*x - 3*x**2*y - x**3*z
F = sp.Matrix([F1, F2, F3])

JF = F.jacobian(q)
d = sp.expand(JF.det())
print("det JF =", d)
assert d == -2

# B = (JF^{-1})^T ; polynomial because det is the constant -2
B = (JF.adjugate().T) / d
B = B.applyfunc(sp.expand)
# polynomiality check
for e in B:
    assert e.as_numer_denom()[1].is_number, "non-polynomial entry!"
print("B = (JF^-T) is polynomial; max total degree of entries:",
      max(sp.Poly(e, x, y, z).total_degree() for e in B if e != 0))

# (1a) D_i(F_j) = delta_ij
DF = sp.expand(B * JF.T)   # entry (i,j) = sum_k B[i,k] dF_j/dx_k = D_i(F_j)
assert DF == sp.eye(3)
print("D_i(F_j) = delta_ij : OK")

# (1b) [D_i, D_j] = 0 as vector fields  (=> [D_i,D_j]=0 in A_3, and with (1a) full CCR for Psi)
def vf_apply(row, f):
    return sum(row[k] * sp.diff(f, q[k]) for k in range(3))

ok = True
for i in range(3):
    for j in range(i + 1, 3):
        for k in range(3):
            comm = sp.expand(vf_apply(B.row(i), B[j, k]) - vf_apply(B.row(j), B[i, k]))
            ok &= (comm == 0)
assert ok
print("[D_i, D_j] = 0 : OK  => Psi is a CCR-preserving endomorphism of A_3")

# (2) cotangent lift on C^6
p1, p2, p3 = sp.symbols('p1 p2 p3')
p = sp.Matrix([p1, p2, p3])
Phi = sp.Matrix.vstack(F, B * p)          # (Q, P) = (F(q), B(q) p)
vars6 = [x, y, z, p1, p2, p3]
M = Phi.jacobian(vars6)
Jsym = sp.Matrix.zeros(6, 6)
for i in range(3):
    Jsym[i, 3 + i] = 1
    Jsym[3 + i, i] = -1
S = sp.expand(M.T * Jsym * M)
assert S == Jsym
print("M^T J M = J : OK  => Phi is an exact polynomial symplectomorphism of C^6")
print("det M =", sp.expand(M.det()))

# non-invertibility: the three collision points, each with the p-fiber matched so images agree.
# Phi(q,p)=(F(q), B(q)p): pick target momentum P0; preimages p = B(q)^{-1} P0 = -2^{-1}... use JF^T P0?
# B^{-1} = JF^T. So p = JF(q)^T P0 at each collision point gives SAME image (F(q_c), P0).
P0 = sp.Matrix([1, 2, 3])
pts = [sp.Matrix([1, sp.Rational(-3, 2), sp.Rational(13, 2)]),
       sp.Matrix([-1, sp.Rational(3, 2), sp.Rational(13, 2)]),
       sp.Matrix([0, 0, sp.Rational(-1, 4)])]
imgs = []
for qc in pts:
    sub = dict(zip([x, y, z], qc))
    pc = (JF.T.subs(sub)) * P0
    full = dict(sub); full.update(dict(zip([p1, p2, p3], pc)))
    imgs.append(sp.simplify(Phi.subs(full).T))
print("three distinct C^6 points map to:", imgs[0])
assert imgs[0] == imgs[1] == imgs[2]
# distinctness is clear from the q-parts
print("triple collision for Phi in C^6 : OK  => symplectic JC false in dim 6, explicitly")

degs = [sp.Poly(e, *vars6).total_degree() for e in Phi]
print("component degrees of Phi:", degs)

# (3) The C* symmetry of F lifts to Hamiltonian C* actions on both copies of C^6,
#     with moment maps mu_src = x p1 - y p2 - 2 z p3 (weights (1,-1,-2) on q) and
#     mu_tgt = -2 Q1 P1 - Q2 P2 + Q3 P3 (weights (-2,-1,1) on the targets F1,F2,F3).
#     Phi intertwines them exactly: mu_tgt o Phi = mu_src.
P = sp.expand(B * p)
mu_src = x*p1 - y*p2 - 2*z*p3
mu_tgt_pulled = sp.expand(-2*F1*P[0] - F2*P[1] + F3*P[2])
assert sp.expand(mu_tgt_pulled - mu_src) == 0
print("mu_tgt o Phi = mu_src : OK  => Phi is a moment-map-preserving Hamiltonian-equivariant")
print("non-invertible symplectomorphism; the 'parked square' lives on the symplectic quotient.")
