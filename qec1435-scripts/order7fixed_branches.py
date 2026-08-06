#!/usr/bin/env python3
"""Branch analysis for a putative [[14,3,5]] with an order-7 automorphism
fixing 7 qubits (one 7-cycle block + 7 fixed qubits).

Setup (see RESULTS-1435.md): S = U0 + Up + Uq with U0 in the 16-dim trivial
component (d0 = dim U0), Up a K-subspace of Vp = K^2 (K = F8 = ideal of
p = x^3+x+1 in F2[x]/(x^7+1)), Uq in Vq = K'^2 (q-ideal), d0 + 3(dp+dq) = 11.
Lemmas A and B close d0 = 11 and d0 = 2. This script attacks d0 = 8
(dp+dq = 1) and d0 = 5 with (dp,dq) = (1,1) via the block-only dual space.

Block-only members of S^perp include M = (Uq^perp cap Vp) + (Up^perp cap Vq)
(all supported on the 7-qubit block). Block-only members of S form
B_S = Up + Uq + (U0 cap V_avg-lifts), with dim B_S <= 3dp + 3dq + 2.
Every element of M \ B_S lies in S^perp \ S so must have symplectic
weight >= 5. Thus the number of nonzero weight-<=4 vectors of M that are NOT
coverable by B_S gives a contradiction when it exceeds |B_S| - 1.

Case d0=8 (dp,dq)=(1,0): M = Vp + (Up^perp cap Vq), dim 9, |M|=512;
  B_S has dim <= 3 + 2 = 5, so at most 31 nonzero elements.
  For each of the 9 K-lines Up: count nonzero weight-<=4 vectors of M.
  If always > 31 the branch is impossible. ((0,1) symmetric by p<->q.)
Case d0=5 (dp,dq)=(1,1): M = (Uq^perp cap Vp) + (Up^perp cap Vq), dim 6;
  B_S = Up + Uq (+ <=2 avg dims), dim <= 8. Here we must check containment:
  for each pair (Up, Uq) (9 x 9), list nonzero weight-<=4 vectors of M and
  test whether each lies in Up + Uq + span(J_a, J_b) (J = all-ones on the
  block; the only possible avg-lift block parts). If some weight-<=4 vector
  of M falls outside for ALL choices, that pair dies; if every pair dies the
  branch is impossible.
"""
import sys
from itertools import combinations

M7 = (1 << 7) - 1

def pmul(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        b >>= 1
    return r

def pdeg(a):
    return a.bit_length() - 1

def pmod(a, b):
    db = pdeg(b)
    while a and pdeg(a) >= db:
        a ^= b << (pdeg(a) - db)
    return a

def pdiv(a, b):
    q = 0
    db = pdeg(b)
    while a and pdeg(a) >= db:
        s = pdeg(a) - db
        q ^= 1 << s
        a ^= b << s
    return q

def pxgcd(a, b):
    r0, r1, s0, s1, t0, t1 = a, b, 1, 0, 0, 1
    while r1:
        qq = pdiv(r0, r1)
        r0, r1 = r1, r0 ^ pmul(qq, r1)
        s0, s1 = s1, s0 ^ pmul(qq, s1)
        t0, t1 = t1, t0 ^ pmul(qq, t1)
    return r0, s0, t0

X71 = (1 << 7) | 1
P, Q = 0b1011, 0b1101

def idem(F):
    G = pdiv(X71, F)
    g, u, v = pxgcd(G, F)
    assert g == 1
    e = pmod(pmul(u, G), X71)
    assert pmod(pmul(e, e), X71) == e
    return e

EP, EQ = idem(P), idem(Q)

def mul7(a, b):
    return pmod(pmul(a, b), X71)

KP = sorted({mul7(EP, t) for t in range(128)})
KQ = sorted({mul7(EQ, t) for t in range(128)})
assert len(KP) == 8 and len(KQ) == 8

# block vectors: (a,b) packed a | b<<7 (14 bits); symplectic weight:
def wt(v):
    return bin((v | (v >> 7)) & M7).count('1')

def sp_block(u, v):
    ua, ub = u & M7, u >> 7
    va, vb = v & M7, v >> 7
    return (bin(ua & vb).count('1') + bin(ub & va).count('1')) & 1

def span(gens):
    out = [0]
    for g in gens:
        out += [x ^ g for x in out]
    return out

def kline_elems(u, w, K):
    """K-line through (u,w) in K^2 as set of packed vectors"""
    return {mul7(lam, u) | (mul7(lam, w) << 7) for lam in K}

def klines(K, e):
    """the q+1 = 9 K-lines of K^2, as (basis-3-vector-list, element-set)"""
    reps = [(0, e)] + [(e, c) for c in K]
    out = []
    for (u, w) in reps:
        els = kline_elems(u, w, K)
        gens = [mul7(lam, u) | (mul7(lam, w) << 7)
                for lam in (e, mul7(e, 0b10), mul7(e, 0b100))]
        out.append((gens, els))
    return out

LP_ = klines(KP, EP)
LQ_ = klines(KQ, EQ)
assert len(LP_) == 9 and len(LQ_) == 9

Vp = span([EP, mul7(EP, 0b10), mul7(EP, 0b100),
           EP << 7, mul7(EP, 0b10) << 7, mul7(EP, 0b100) << 7])
Vq = span([EQ, mul7(EQ, 0b10), mul7(EQ, 0b100),
           EQ << 7, mul7(EQ, 0b10) << 7, mul7(EQ, 0b100) << 7])
assert len(Vp) == 64 and len(Vq) == 64

def orth_line(line_gens, lines_other):
    """the unique K'-line in the other component orthogonal to given K-line"""
    matches = []
    for gens, els in lines_other:
        if all(sp_block(g, h) == 0 for g in line_gens for h in gens):
            matches.append((gens, els))
    assert len(matches) == 1, len(matches)
    return matches[0]

print("=== Case d0=8, (dp,dq)=(1,0): M = Vp + (Up^perp cap Vq), need <=31 "
      "low-weight to survive ===")
ok8 = True
for idx, (gens, els) in enumerate(LP_):
    og, oe = orth_line(gens, LQ_)
    Mspace = {vp ^ vq for vp in Vp for vq in span(og)}
    assert len(Mspace) == 512
    lw = sum(1 for v in Mspace if v and wt(v) <= 4)
    status = "SURVIVES (needs check)" if lw <= 31 else "IMPOSSIBLE"
    print(f"Up line {idx}: weight<=4 nonzero in M: {lw}  -> {status}")
    if lw <= 31:
        ok8 = False
print("branch (1,0) %s" % ("CLOSED" if ok8 else "NOT closed"))
print("(the (0,1) case is identical under the p<->q relabeling, which is an "
      "automorphism of the setup)")

print()
print("=== Case d0=5, (dp,dq)=(1,1): M = (Uq^perp cap Vp)+(Up^perp cap Vq) "
      "vs B = Up+Uq+<Ja,Jb> ===")
J = M7
alive = 0
for ip, (pg, pe) in enumerate(LP_):
    for iq, (qg, qe) in enumerate(LQ_):
        # M
        og_p, _ = orth_line(qg, LP_)   # Uq^perp cap Vp
        og_q, _ = orth_line(pg, LQ_)   # Up^perp cap Vq
        Mspace = {a ^ b for a in span(og_p) for b in span(og_q)}
        # B = Up + Uq + <J_a, J_b>  (largest possible block stabilizer)
        B = set(span(pg + qg + [J, J << 7]))
        bad = [v for v in Mspace if v and wt(v) <= 4 and v not in B]
        if not bad:
            alive += 1
            print(f"pair (Up={ip},Uq={iq}): all low-weight M-vectors inside "
                  f"max-B — SURVIVES")
print(f"(1,1) pairs surviving the block test: {alive} of 81; branch "
      f"{'CLOSED' if alive == 0 else 'NOT closed by this test'}")
