#!/usr/bin/env python3
"""Checker for the certified two-sided logical-error bracket of the d=3
rotated surface code (one round, circuit-level depolarizing noise,
lookup-table decoder).

PUBLISHABLE ARTIFACT.  Python 3 standard library only; OS-independent;
no signals, no subprocesses, no network.  Re-derives every certified
quantity from the mechanism list inside the certificate and fails
loudly on any mismatch.

Usage:  python3 check_wedge.py certificate_d3_r1_pX.json

What is re-verified, from scratch:
  1. The SHA-256 hash of the canonically serialized mechanism list.
  2. The decoder table: breadth-first search (FIFO) over the syndrome
     space from syndrome 0, mechanisms applied in canonical index order
     (ascending (det, obs)); first assignment wins.  This reconstructs
     the lookup-table (coset-leader) decoder and must equal the table
     embedded in the certificate, entry by entry.
  3. The circuit-level distance: minimum number of mechanisms with zero
     detector syndrome and net observable flip 1 (joint BFS).
  4. Exhaustive enumeration of ALL fault subsets of weight 1..4:
     the uncorrectable counts A_w, the exact list of uncorrectable
     subsets, and the exhaustion record (numbers of subsets checked
     equal binomial(m, w)).
  5. The exact rational lower bound L, Poisson-binomial tail
     T = P(W >= 5), and upper bound U = L + T, recomputed in exact
     arithmetic (fractions module) and compared string-for-string.
The certified claim is:  L <= P_L <= U  for the independent-mechanism
fault model listed in the certificate, under the stated decoder.
Exit code 0 and final line "CHECK PASS" iff every re-derivation agrees.
"""
import hashlib
import itertools
import json
import sys
from collections import deque
from fractions import Fraction
from math import comb

WMAX = 4


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
    if len(mechs) != m:
        fail("mechanism count mismatch")

    # canonical order and hash
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
    probs = [Fraction(mm["p_num"], mm["p_den"]) for mm in mechs]
    if not all(0 < p < 1 for p in probs):
        fail("mechanism probability outside (0,1)")

    # 2. decoder table by BFS
    size = 1 << n_det
    weight = [-1] * size
    pred = [0] * size
    weight[0] = 0
    q = deque([0])
    while q:
        s = q.popleft()
        for j in range(m):
            s2 = s ^ dets[j]
            if weight[s2] == -1:
                weight[s2] = weight[s] + 1
                pred[s2] = pred[s] ^ obss[j]
                q.append(s2)
    table = {int(k): v for k, v in cert["decoder_table"].items()}
    derived = {s: [weight[s], pred[s]] for s in range(size) if weight[s] != -1}
    if derived != table:
        fail("decoder table mismatch")

    # 3. circuit-level distance by joint BFS over (syndrome, observable)
    jsize = 1 << (n_det + 1)
    dist = [-1] * jsize
    dist[0] = 0
    q = deque([0])
    while q:
        st = q.popleft()
        for j in range(m):
            st2 = st ^ (dets[j] | (obss[j] << n_det))
            if dist[st2] == -1:
                dist[st2] = dist[st] + 1
                q.append(st2)
    if dist[1 << n_det] != cert["circuit_level_distance"]:
        fail("circuit-level distance mismatch")

    # 4. exhaustive enumeration w = 1..WMAX
    Qprod = Fraction(1)
    for p in probs:
        Qprod *= (1 - p)
    r = [p / (1 - p) for p in probs]
    A = {}
    L = Fraction(0)
    for w in range(1, WMAX + 1):
        aw = 0
        checked = 0
        bad = []
        for cmb in itertools.combinations(range(m), w):
            checked += 1
            s = 0
            o = 0
            for j in cmb:
                s ^= dets[j]
                o ^= obss[j]
            if pred[s] != o:
                aw += 1
                bad.append(list(cmb))
                term = Qprod
                for j in cmb:
                    term *= r[j]
                L += term
        if checked != comb(m, w):
            fail("exhaustion record broken at w=%d" % w)
        if checked != cert["exhaustion_record"]["subsets_checked"][str(w)]:
            fail("subsets_checked mismatch at w=%d" % w)
        if aw != cert["A_w_uncorrectable_counts"][str(w)]:
            fail("A_%d mismatch: derived %d, certified %s"
                 % (w, aw, cert["A_w_uncorrectable_counts"][str(w)]))
        if bad != cert["uncorrectable_sets"][str(w)]:
            fail("uncorrectable set list mismatch at w=%d" % w)
        A[w] = aw

    # 5. exact tail and bracket
    K = WMAX + 1
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
                if k + 1 >= K:
                    ndp[K] += dp[k] * p
                else:
                    ndp[k + 1] += dp[k] * p
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

    print("mechanisms: %d   detectors: %d   circuit-level distance: %d"
          % (m, n_det, cert["circuit_level_distance"]))
    print("A_w (uncorrectable subsets): %s"
          % {w: A[w] for w in sorted(A)})
    print("L = %s  (~%.6e)" % (br["L"], float(L)))
    print("T = %s  (~%.6e)" % (br["tail_T"], float(T)))
    print("U = %s  (~%.6e)" % (br["U"], float(U)))
    print("Certified: %.10e <= P_L <= %.10e" % (float(L), float(U)))
    print("CHECK PASS")


if __name__ == "__main__":
    main()
