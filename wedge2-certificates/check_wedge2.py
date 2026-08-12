#!/usr/bin/env python3
"""Checker for the EXACT logical error probability certificate of the
rotated surface code (one round, circuit-level depolarizing noise,
lookup-table / coset-leader decoder).  Supersedes the two-sided bracket
of Part H (doi:10.5281/zenodo.21895825): the certificate carries the exact
rational P_L and the full uncorrectable weight spectrum A_w, and this
checker re-derives both from the mechanism list alone.

PUBLISHABLE ARTIFACT.  Python 3 standard library only; OS-independent;
no signals, no subprocesses, no network, no wall-clock dependence.

Usage:  python3 check_wedge2.py certificate.json

Method (re-derived, not copied, from the certificate's mechanism list).
Write v_j = (d_j, o_j) in F_2^{n+1} for mechanism j with probability p_j,
sigma(F) = xor_{j in F} d_j, obs(F) = xor_{j in F} o_j.  The decoder D is
the coset-leader lookup table from a FULL (untruncated) FIFO breadth-first
search over all 2^n syndromes from 0, mechanisms in canonical index order,
first assignment wins; F is uncorrectable iff D(sigma(F)) != obs(F).
For characters chi_y(u) = (-1)^{<y,u>} of F_2^{n+1} the products

    prod_j (1 + t e_{v_j})           (counting)
    prod_j ((1-p_j) + p_j e_{v_j})   (probability)

evaluate at y to (1+t)^{a(y)} (1-t)^{m-a(y)} and prod_{j:<y,v_j>=1}(1-2p_j)
respectively, where a(y) = #{j : <y,v_j> = 0}.  Fourier inversion of the
failure indicator I(s,b) = [b != D(s)] (every syndrome is reachable; the
checker verifies this) gives, with E^ = FWHT of e(s) = (-1)^{D(s)},
a1(y) = #{j : <y,d_j> = o_j} and g_w(k) = [t^w](1+t)^k (1-t)^{m-k}:

  A_w  = 2^{-(n+1)} ( 2^n g_w(m) - sum_y g_w(a1(y)) E^(y) )            (*)
  N_w  = 2^{-(n+1)} sum_y ( g_w(a0(y)) - g_w(a1(y)) )                  (**)
         [ N_w = #{F : |F|=w, sigma(F)=0, obs(F)=1 }, the undetectable
           logical operators; circuit distance = min{w : N_w > 0} ]
  P_L  = 2^{-(n+1)} ( 2^n - sum_y E^(y) prod_{j:<y,d_j> xor o_j =1}(1-2p_j) )
                                                                       (dia)
All arithmetic is exact: FWHTs on int64 'q' arrays, the (dia) products as
big integers over the dyadic common denominator (all p_j are dyadic).
The checker verifies, against the certificate, each of:
  mechanism-list SHA-256 and canonical order; syndrome-space spanning;
  the full A_w spectrum; sum_w A_w = 2^{m-1}; the N_w spectrum;
  sum_w N_w = 2^{m-n-1}; the circuit-level distance; the v1 counts;
  the exact P_L numerator/denominator; and containment of P_L in the
  cited Part H bracket L <= P_L <= U.
Any mismatch prints CHECK FAIL and exits nonzero; success prints CHECK PASS.
"""
import hashlib
import json
import sys
from array import array
from fractions import Fraction


def fail(msg):
    print("CHECK FAIL: %s" % msg)
    sys.exit(1)


def fwht(a, size):
    """In-place unnormalised Walsh-Hadamard transform on array('q')."""
    h = 1
    while h < size:
        step = h * 2
        for i in range(0, size, step):
            for j in range(i, i + h):
                x = a[j]
                y = a[j + h]
                a[j] = x + y
                a[j + h] = x - y
        h = step
    return a


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    cert = json.load(open(sys.argv[1]))
    mechs = cert["mechanisms"]
    m = cert["num_mechanisms"]
    n = cert["num_detectors"]
    size = 1 << n
    if len(mechs) != m:
        fail("mechanism count mismatch")
    if cert["num_observables"] != 1:
        fail("checker requires exactly one observable")

    # 1. canonical order and hash
    sigs = [(mm["det"], mm["obs"]) for mm in mechs]
    if sigs != sorted(sigs):
        fail("mechanism list not in canonical order")
    if len(set(sigs)) != m:
        fail("duplicate (det, obs) signature")
    lines = ["%d:%d:%d/%d" % (mm["det"], mm["obs"], mm["p_num"], mm["p_den"])
             for mm in mechs]
    h = hashlib.sha256(("\n".join(lines) + "\n").encode("utf-8")).hexdigest()
    if h != cert["mechanism_list_sha256"]:
        fail("mechanism list hash mismatch")
    dets = [mm["det"] for mm in mechs]
    obss = [mm["obs"] for mm in mechs]
    pnum = [mm["p_num"] for mm in mechs]
    pden = [mm["p_den"] for mm in mechs]
    for j in range(m):
        if not (0 < pnum[j] < pden[j]):
            fail("mechanism probability outside (0,1)")
        if pden[j] & (pden[j] - 1):
            fail("denominator not a power of two (certificate requires dyadic p)")
        if not (0 <= dets[j] < size):
            fail("detector mask out of range")

    # 2. FULL coset-leader decoder (untruncated BFS over all 2^n syndromes)
    pred = bytearray(size)
    seen = bytearray(size)
    seen[0] = 1
    frontier = [0]
    while frontier:
        nxt = []
        for s in frontier:
            ps = pred[s]
            for j in range(m):
                s2 = s ^ dets[j]
                if not seen[s2]:
                    seen[s2] = 1
                    pred[s2] = ps ^ obss[j]
                    nxt.append(s2)
        frontier = nxt
    if sum(seen) != size:
        fail("detector masks do not span the syndrome space "
             "(identity (*) as certified assumes spanning)")
    del seen

    # 3. transforms
    e = array('q', bytes(8 * size))
    for s in range(size):
        e[s] = -1 if pred[s] else 1
    del pred
    fwht(e, size)                       # e is now E^
    hd = array('q', bytes(8 * size))
    hd1 = array('q', bytes(8 * size))
    for j in range(m):
        hd[dets[j]] += 1
        hd1[dets[j]] += 1 - 2 * obss[j]
    fwht(hd, size)                      # = 2 a0 - m
    fwht(hd1, size)                     # = 2 a1 - m
    if (m + hd[0]) & 1 or (m + hd1[0]) & 1:
        fail("parity violation in mask transforms")

    # probability classes, split into two groups for the product tables
    classes = {}
    for j in range(m):
        classes.setdefault((pnum[j], pden[j]), []).append(j)
    ckeys = sorted(classes)
    csz = [len(classes[k]) for k in ckeys]
    C = len(ckeys)
    split = 0
    r1 = 1
    while split < C and r1 * (csz[split] + 1) <= (1 << 18):
        r1 *= (csz[split] + 1)
        split += 1
    g2 = list(range(split, C))
    r2 = 1
    for ci in g2:
        r2 *= (csz[ci] + 1)
    if r2 > (1 << 26):
        fail("class radix split failed (unexpected class structure)")

    def group_hist(idxs, radix_bases):
        hh = array('q', bytes(8 * size))
        const = 0
        for bi, ci in enumerate(idxs):
            for j in classes[ckeys[ci]]:
                hh[dets[j]] += radix_bases[bi] * (1 - 2 * obss[j])
            const += radix_bases[bi] * csz[ci]
        return hh, const

    bases1 = []
    b = 1
    for ci in range(split):
        bases1.append(b)
        b *= (csz[ci] + 1)
    bases2 = []
    b = 1
    for ci in g2:
        bases2.append(b)
        b *= (csz[ci] + 1)
    Hlo, CL = group_hist(list(range(split)), bases1)
    Hhi, CH = group_hist(g2, bases2)
    fwht(Hlo, size)
    fwht(Hhi, size)
    if (CL - Hlo[0]) & 1 or (CH - Hhi[0]) & 1:
        fail("parity violation in class transforms")

    # scaled power tables: u_c[k] = rnum_c^k << e_c (m_c - k), so that a
    # product over all classes equals prod rnum^k << (E_tot - sum e_c k_c)
    e_exp = [pd.bit_length() - 1 for (pn, pd) in ckeys]
    rnum = [pd - 2 * pn for (pn, pd) in ckeys]
    E_tot = sum(e_exp[ci] * csz[ci] for ci in range(C))
    powt = []
    for ci in range(C):
        t = []
        for k in range(csz[ci] + 1):
            t.append((rnum[ci] ** k) << (e_exp[ci] * (csz[ci] - k)))
        powt.append(t)
    # T1: exact scaled product for every group-1 digit tuple (odometer)
    T1 = [0] * r1
    digits = [0] * max(split, 1)
    for key in range(r1):
        prod = 1
        for ci in range(split):
            prod *= powt[ci][digits[ci]]
        T1[key] = prod
        for ci in range(split):
            digits[ci] += 1
            if digits[ci] <= csz[ci]:
                break
            digits[ci] = 0

    # 4. fused pass over syndrome space
    Q = [0] * (m + 1)
    R0 = [0] * (m + 1)
    R1 = [0] * (m + 1)
    acc = [0] * r2
    for eh, v0, v1, kl, kh in zip(e, hd, hd1, Hlo, Hhi):
        i0 = (m + v0) >> 1
        i1 = (m + v1) >> 1
        R0[i0] += 1
        R1[i1] += 1
        Q[i1] -= eh
        acc[(CH - kh) >> 1] -= T1[(CL - kl) >> 1] * eh
    del e, hd, hd1, Hlo, Hhi, T1
    Q[m] += size                        # C^ contributes 2^n at y = 0

    # 5. count assembly:  g_w(k) = [t^w](1+t)^k (1-t)^{m-k}
    g = []
    for k in range(m + 1):
        poly = [1]
        for _ in range(k):
            poly = [a2 + b2 for a2, b2 in zip(poly + [0], [0] + poly)]
        for _ in range(m - k):
            poly = [a2 - b2 for a2, b2 in zip(poly + [0], [0] + poly)]
        g.append(poly)
    A = []
    Nlog = []
    Rd = [R0[k] - R1[k] for k in range(m + 1)]
    for w in range(m + 1):
        numA = sum(g[k][w] * Q[k] for k in range(m + 1))
        numN = sum(g[k][w] * Rd[k] for k in range(m + 1))
        if numA % (1 << (n + 1)) or numN % (1 << (n + 1)):
            fail("transform inversion not integral at w=%d" % w)
        A.append(numA >> (n + 1))
        Nlog.append(numN >> (n + 1))
    if any(x < 0 for x in A) or any(x < 0 for x in Nlog):
        fail("negative count from inversion")
    for w in range(m + 1):
        if str(A[w]) != cert["A_w_full_spectrum"][str(w)]:
            fail("A_%d mismatch: derived %d, certified %s"
                 % (w, A[w], cert["A_w_full_spectrum"][str(w)]))
        if str(Nlog[w]) != cert["N_w_logical_spectrum"][str(w)]:
            fail("N_%d mismatch: derived %d, certified %s"
                 % (w, Nlog[w], cert["N_w_logical_spectrum"][str(w)]))
    if sum(A) != 1 << (m - 1):
        fail("involution invariant sum_w A_w = 2^{m-1} violated")
    if sum(Nlog) != 1 << (m - n - 1):
        fail("logical-coset invariant sum_w N_w = 2^{m-n-1} violated")
    dist = min(w for w in range(1, m + 1) if Nlog[w] > 0)
    if dist != cert["circuit_level_distance"]:
        fail("circuit-level distance mismatch: derived %d, certified %s"
             % (dist, cert["circuit_level_distance"]))
    v1c = cert["v1_reference"]["A_w_certified"]
    for w, aw in v1c.items():
        if A[int(w)] != aw:
            fail("v1 count A_%s mismatch: derived %d, v1 certified %d"
                 % (w, A[int(w)], aw))

    # 6. exact P_L assembly:  P_L = (2^n 2^{E_tot} + W) / 2^{n+1+E_tot}
    W = 0
    digits = [0] * max(len(g2), 1)
    for key in range(r2):
        if acc[key]:
            prod = acc[key]
            for bi in range(len(g2)):
                prod *= powt[g2[bi]][digits[bi]]
            W += prod
        for bi in range(len(g2)):
            digits[bi] += 1
            if digits[bi] <= csz[g2[bi]]:
                break
            digits[bi] = 0
    PL = Fraction((1 << (n + E_tot)) + W, 1 << (n + 1 + E_tot))
    pc = cert["P_L_exact"]
    if str(PL.numerator) != pc["num"] or str(PL.denominator) != pc["den"]:
        fail("exact P_L mismatch")
    if not (Fraction(0) < PL < Fraction(1)):
        fail("P_L outside (0,1)")

    # 7. containment in the cited Part H bracket
    br = cert["v1_reference"]
    Lb = Fraction(*map(int, br["bracket_L"].split("/")))
    Ub = Fraction(*map(int, br["bracket_U"].split("/")))
    if not (Lb <= PL <= Ub):
        fail("exact P_L falls outside the v1 bracket")

    print("distance %d   mechanisms %d   detectors %d   classes %d"
          % (dist, m, n, C))
    print("A_w head: %s" % {w: A[w] for w in range(min(9, m + 1)) if A[w]})
    print("sum_w A_w = 2^%d   sum_w N_w = 2^%d" % (m - 1, m - n - 1))
    print("P_L = %s... / %s...  (%d / %d digits)"
          % (pc["num"][:24], pc["den"][:24], len(pc["num"]), len(pc["den"])))
    print("P_L ~ %.12e" % float(PL))
    print("v1 bracket [%.12e, %.12e] contains P_L: yes"
          % (float(Lb), float(Ub)))
    print("CHECK PASS")


if __name__ == "__main__":
    main()
