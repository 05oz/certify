#!/usr/bin/env python3
"""Checker for the certified two-sided logical-error bracket of the
rotated surface code (one round, circuit-level depolarizing noise,
lookup-table / coset-leader decoder), distance-scalable version.

PUBLISHABLE ARTIFACT.  Python 3 standard library only; OS-independent;
no signals, no subprocesses, no network.  Re-derives every certified
quantity from the mechanism list inside the certificate and fails loudly
on any mismatch.

Usage:  python3 check_wedge_d5.py certificate.json

Why this differs from check_wedge.py (the d=3 checker): at d=5 the full
coset-leader table has 2^24 entries and the uncorrectable subsets number
in the millions, so neither is embedded in the certificate.  The checker
instead RE-COMPUTES them:

  1. SHA-256 of the canonically serialized mechanism list.
  2. The coset-leader decoder by a depth-truncated FIFO breadth-first
     search to depth WMAX over the syndrome space from syndrome 0,
     mechanisms in canonical index order, first assignment wins.  A fault
     set of weight w<=WMAX has a syndrome at BFS distance <=w<=WMAX, so its
     coset leader is assigned by this truncated search identically to the
     full-BFS table; the syndromes of all weight-<=WMAX fault sets are
     therefore decoded correctly.
  3. Exhaustive enumeration of ALL fault subsets of weight 1..WMAX: the
     uncorrectable counts A_w, a per-weight SHA-256 over the uncorrectable
     index tuples (in enumeration order), the exhaustion record
     (subsets_checked == binomial(m, w)), and the circuit-level distance
     (least weight <=WMAX of a zero-syndrome, observable-flip-1 subset).
  4. The exact lower bound L, accumulated in integer arithmetic over the
     common denominator D = prod_j p_den_j:
         term_F = num_F / D,
         num_F  = (prod_{i in F} p_num_i) * (Mall // prod_{i in F} m_i),
         m_j = p_den_j - p_num_j,   Mall = prod_j m_j.
     prod_{i in F} m_i divides Mall (F is a subset of all indices), so the
     // is exact.  L = Fraction(SUMINT, D).
  5. The exact Poisson-binomial tail T = P(W >= WMAX+1) and U = L + T.
Each is compared string-for-string / entry-for-entry to the certificate.
The certified claim is  L <= P_L <= U  for the independent-mechanism fault
model listed in the certificate, under the stated decoder.  Exit code 0 and
final line "CHECK PASS" iff every re-derivation agrees.
"""
import hashlib
import itertools
import json
import sys
from fractions import Fraction
from math import comb


def fail(msg):
    print("CHECK FAIL: %s" % msg)
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    cert = json.load(open(sys.argv[1]))
    mechs = cert["mechanisms"]
    m = cert["num_mechanisms"]
    n_det = cert["num_detectors"]
    wmax = cert["WMAX"]
    if len(mechs) != m:
        fail("mechanism count mismatch")

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
    p_num = [mm["p_num"] for mm in mechs]
    p_den = [mm["p_den"] for mm in mechs]
    if not all(0 < p_num[j] < p_den[j] for j in range(m)):
        fail("mechanism probability outside (0,1)")

    # 2. coset-leader decoder by depth-truncated FIFO BFS to depth WMAX
    size = 1 << n_det
    pred = bytearray(size)
    seen = bytearray(size)
    seen[0] = 1
    frontier = [0]
    depth = 0
    while frontier and depth < wmax:
        depth += 1
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

    # 4-constants: integer accumulation of the exact lower bound
    D = 1
    for d in p_den:
        D *= d
    mvals = [p_den[j] - p_num[j] for j in range(m)]
    Mall = 1
    for mv in mvals:
        Mall *= mv

    # 3+4. exhaustive enumeration, weights 1..WMAX
    SUMINT = 0
    dmin = None
    for w in range(1, wmax + 1):
        hw = hashlib.sha256()
        aw = 0
        cnt = 0
        for cmb in itertools.combinations(range(m), w):
            cnt += 1
            s = 0
            o = 0
            for j in cmb:
                s ^= dets[j]
                o ^= obss[j]
            if s == 0 and o == 1 and dmin is None:
                dmin = w
            if not seen[s]:
                fail("syndrome unreached by truncated BFS at w=%d "
                     "(WMAX too small for a weight-%d syndrome)" % (w, w))
            if pred[s] != o:
                aw += 1
                hw.update((",".join(map(str, cmb)) + "\n").encode())
                PN = 1
                PM = 1
                for j in cmb:
                    PN *= p_num[j]
                    PM *= mvals[j]
                SUMINT += PN * (Mall // PM)
        if cnt != comb(m, w):
            fail("exhaustion record broken at w=%d" % w)
        if cnt != cert["exhaustion_record"]["subsets_checked"][str(w)]:
            fail("subsets_checked mismatch at w=%d" % w)
        if aw != cert["A_w_uncorrectable_counts"][str(w)]:
            fail("A_%d mismatch: derived %d, certified %s"
                 % (w, aw, cert["A_w_uncorrectable_counts"][str(w)]))
        if hw.hexdigest() != cert["uncorrectable_set_sha256"][str(w)]:
            fail("uncorrectable-set hash mismatch at w=%d" % w)

    if dmin != cert["circuit_level_distance"]:
        fail("circuit-level distance mismatch: derived %s, certified %s"
             % (dmin, cert["circuit_level_distance"]))

    L = Fraction(SUMINT, D)

    # 5. exact Poisson-binomial tail and bracket
    probs = [Fraction(p_num[j], p_den[j]) for j in range(m)]
    K = wmax + 1
    dp = [Fraction(0)] * (K + 1)
    dp[0] = Fraction(1)
    for p in probs:
        ndp = [Fraction(0)] * (K + 1)
        for k in range(K + 1):
            if dp[k] == 0:
                continue
            if k == K:
                ndp[K] += dp[k]
            else:
                ndp[k] += dp[k] * (1 - p)
                tgt = K if k + 1 >= K else k + 1
                ndp[tgt] += dp[k] * p
        dp = ndp
    T = dp[K]
    U = L + T

    def frs(x):
        return "%d/%d" % (x.numerator, x.denominator)

    br = cert["bracket"]
    if frs(L) != br["L"]:
        fail("lower bound L mismatch")
    if frs(T) != br["tail_T"]:
        fail("tail T mismatch")
    if frs(U) != br["U"]:
        fail("upper bound U mismatch")
    if not (Fraction(0) <= L <= U <= Fraction(1)):
        fail("bracket not in [0,1] or inverted")

    print("distance %d   WMAX %d   mechanisms %d   detectors %d   "
          "circuit-level distance %d"
          % (cert["model"]["distance"], wmax, m, n_det, dmin))
    print("A_w (uncorrectable subsets): %s"
          % {w: cert["A_w_uncorrectable_counts"][str(w)]
             for w in range(1, wmax + 1)})
    print("L = %s  (~%.6e)" % (br["L"], float(L)))
    print("T = %s  (~%.6e)" % (br["tail_T"], float(T)))
    print("U = %s  (~%.6e)" % (br["U"], float(U)))
    print("Certified: %.10e <= P_L <= %.10e" % (float(L), float(U)))
    print("CHECK PASS")


if __name__ == "__main__":
    main()
