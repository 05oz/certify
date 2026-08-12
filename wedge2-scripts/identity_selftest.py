#!/usr/bin/env python3
"""Standard-library self-test of the two transform identities of the wedge2
note (Part L):

  (Thm 2.1)  A_w  = 2^{-(n+1)} sum_k g_w(k) Q(k)        (all counts at once)
  (Thm 2.2)  P_L  = 2^{-(n+1)} sum_y I^(y) prod_{j:<y,v_j>=1} (1 - 2 p_j)

Verifies both against exact brute force over ALL 2^m fault configurations,
in exact Fraction arithmetic, on random small DEMs -- including DEMs whose
detector masks do NOT span the syndrome space (exercising the general
reachable-set term; the shipped certificates' masks span, and the shipped
checker verifies that they do).  Decoder convention is identical to the
shipped checkers: full FIFO BFS coset leader, mechanisms in canonical index
order, first assignment wins.

This file is a trust-building artifact, not part of any certificate's
verification chain: it demonstrates the identities the checker implements.
Python 3 standard library only.  Usage:  python3 identity_selftest.py
"""
import random
from fractions import Fraction
from math import comb


def bfs_decoder(dets, obss, n):
    size = 1 << n
    pred = bytearray(size)
    seen = bytearray(size)
    seen[0] = 1
    frontier = [0]
    while frontier:
        nxt = []
        for s in frontier:
            ps = pred[s]
            for j in range(len(dets)):
                s2 = s ^ dets[j]
                if not seen[s2]:
                    seen[s2] = 1
                    pred[s2] = ps ^ obss[j]
                    nxt.append(s2)
        frontier = nxt
    return pred, seen


def fwht(a):
    n = len(a)
    h = 1
    while h < n:
        for i in range(0, n, h * 2):
            for j in range(i, i + h):
                x, y = a[j], a[j + h]
                a[j], a[j + h] = x + y, x - y
        h *= 2
    return a


def brute(dets, obss, probs, n, m, pred, seen):
    """Exact brute force over all 2^m subsets: A_w and P_L."""
    A = [0] * (m + 1)
    PL = Fraction(0)
    for mask in range(1 << m):
        s = 0
        o = 0
        w = 0
        pF = Fraction(1)
        for j in range(m):
            if (mask >> j) & 1:
                s ^= dets[j]
                o ^= obss[j]
                w += 1
                pF *= probs[j]
            else:
                pF *= (1 - probs[j])
        assert seen[s], "sigma(F) is always reachable"
        if pred[s] != o:
            A[w] += 1
            PL += pF
    return A, PL


def transform_counts(dets, obss, n, m, pred, seen):
    """Theorem 2.1: every A_w from four length-2^n transforms."""
    size = 1 << n
    C = fwht([1 if seen[s] else 0 for s in range(size)])
    E = fwht([((-1) ** pred[s]) if seen[s] else 0 for s in range(size)])
    hd = [0] * size
    hd1 = [0] * size
    for j in range(m):
        hd[dets[j]] += 1
        hd1[dets[j]] += (-1) ** obss[j]
    A0 = fwht(hd)    # = 2 a0 - m
    A1 = fwht(hd1)   # = 2 a1 - m
    Q = [0] * (m + 1)
    for y in range(size):
        Q[(m + A0[y]) // 2] += C[y]
        Q[(m + A1[y]) // 2] -= E[y]
    g = []
    for k in range(m + 1):
        poly = [1]
        for _ in range(k):
            poly = [a + b for a, b in zip(poly + [0], [0] + poly)]
        for _ in range(m - k):
            poly = [a - b for a, b in zip(poly + [0], [0] + poly)]
        g.append(poly)
    A = []
    for w in range(m + 1):
        num = sum(g[k][w] * Q[k] for k in range(m + 1))
        assert num % (1 << (n + 1)) == 0, "inversion must be integral"
        A.append(num >> (n + 1))
    return A


def transform_pl(dets, obss, probs, n, m, pred, seen):
    """Theorem 2.2: exact P_L, general reachable-set form."""
    size = 1 << n
    C = fwht([1 if seen[s] else 0 for s in range(size)])
    E = fwht([((-1) ** pred[s]) if seen[s] else 0 for s in range(size)])
    total = Fraction(0)
    for y in range(size):
        w0 = Fraction(1)
        w1 = Fraction(1)
        for j in range(m):
            bit = bin(y & dets[j]).count("1") & 1
            if bit:
                w0 *= (1 - 2 * probs[j])
            if bit ^ obss[j]:
                w1 *= (1 - 2 * probs[j])
        total += C[y] * w0 - E[y] * w1
    return total / (1 << (n + 1))


def run_case(seed, n, m, span):
    rng = random.Random(seed)
    while True:
        if span:
            dets = [1 << i for i in range(n)] + \
                   [rng.randrange(1, 1 << n) for _ in range(m - n)]
        else:
            dets = [rng.randrange(1, 1 << (n - 1)) for _ in range(m)]
        obss = [rng.randrange(2) for _ in range(m)]
        if len(set(zip(dets, obss))) == m:
            break
    probs = [Fraction(rng.randrange(1, 200), rng.randrange(600, 4000))
             for _ in range(m)]
    pred, seen = bfs_decoder(dets, obss, n)
    A_bf, PL_bf = brute(dets, obss, probs, n, m, pred, seen)
    A_tr = transform_counts(dets, obss, n, m, pred, seen)
    PL_tr = transform_pl(dets, obss, probs, n, m, pred, seen)
    ok_A = (A_bf == A_tr)
    ok_P = (PL_bf == PL_tr)
    print("seed=%d n=%d m=%d span=%-5s  A_w match: %s   P_L match: %s"
          % (seed, n, m, span, ok_A, ok_P))
    if not (ok_A and ok_P):
        print("  brute A:", A_bf)
        print("  trans A:", A_tr)
        print("  brute P_L:", PL_bf)
        print("  trans P_L:", PL_tr)
        raise SystemExit(1)


if __name__ == "__main__":
    for seed in (1, 2, 3):
        run_case(seed, n=6, m=10, span=True)
    for seed in (4, 5):
        run_case(seed, n=6, m=9, span=False)
    run_case(6, n=5, m=12, span=True)
    print("ALL SMALL-CASE IDENTITY CHECKS PASS (exact Fraction arithmetic)")
