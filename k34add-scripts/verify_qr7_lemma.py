#!/usr/bin/env python3
"""
Verification of the inputs to the QR_7 forcing lemma (Certify, Part J).

The lemma: in any {I_3, TT_4}-free oriented graph, a vertex's non-neighbourhood
induces a TT_4-free tournament; such a tournament has at most 7 vertices, and the
unique 7-vertex TT_4-free tournament is the Paley (quadratic-residue) tournament
QR_7 = Cay(Z_7, {1,2,4}).  Hence every vertex has at most 7 non-neighbours, and a
vertex with exactly 7 carries a QR_7 block.

This script checks the two tournament facts by exhaustive enumeration:
  (1) exactly 240 labelled TT_4-free tournaments on 7 vertices, EVERY one
      isomorphic to QR_7  (=> unique up to isomorphism, and 240 = 7!/|Aut(QR_7)|);
  (2) zero TT_4-free tournaments on 8 vertices (=> every 8-vertex tournament has a
      TT_4, so the non-neighbourhood bound is 7).
It also reports |Aut(QR_7)| = 21 and that QR_7 is TT_4-free and doubly regular.

Classical primary source for both facts: A. Sanchez-Flores, "On tournaments free
of large transitive subtournaments", Graphs Combin. 14 (1998), 181-200.
Standard library only; deterministic; no OS-specific calls.

Stdlib-only; shares only boilerplate with the SAT search (25 of 115 executable
lines: returns, loop headers, the main guard).  NOT independent of the private
structure-mining scripts in hunt-structure/.  tour_iso, its inner backtracker,
and qr7 are the same routines as there, PEP8-expanded from a compressed
original with every local name preserved (oa, ob, perm, used, i, j, k, bt).
The TT_4-detection kernel inside has_tt4 and inside new_vertex_ok is the
private kernel with the two operands of one != transposed, and the backtracking
loop of aut_count_tour follows the private aut_count's statement for statement,
differing only in the pruning key.  Original here: the vertex-by-vertex mask
recursion of enumerate_tt4free (one of its nineteen lines is shared) and the
3-regularity test.  So neither the "all isomorphic to QR_7" sweep nor the counts
240, 21 and 0 may be read as independent re-derivations.  The uniqueness
conclusion does not need the isomorphism test: by orbit-stabilizer the labelled
tournaments isomorphic to QR_7 number 7!/21 = 240, all TT_4-free since QR_7 is,
so they exhaust the enumerated 240.  (Disclosed 2026-08-14.)
"""
import itertools, math, sys

def qr7():
    QR = {1, 2, 4}
    M = [[0] * 7 for _ in range(7)]
    for i in range(7):
        for j in range(7):
            if i != j and (j - i) % 7 in QR:
                M[i][j] = 1
    return M

def has_tt4(M, verts):
    for four in itertools.combinations(verts, 4):
        outs = sorted(sum(1 for y in four if y != x and M[x][y]) for x in four)
        if outs == [0, 1, 2, 3]:
            return True
    return False

def new_vertex_ok(adj, k):
    # only 4-subsets containing the freshly completed vertex k need checking
    for trip in itertools.combinations(range(k), 3):
        four = trip + (k,)
        outs = sorted(sum(1 for y in four if y != x and adj[x][y]) for x in four)
        if outs == [0, 1, 2, 3]:
            return False
    return True

def enumerate_tt4free(n, collect):
    adj = [[0] * n for _ in range(n)]
    out = {"count": 0, "reps": []}

    def rec(k):
        if k == n:
            out["count"] += 1
            if collect:
                out["reps"].append([row[:] for row in adj])
            return
        for mask in range(1 << k):
            for i in range(k):
                if (mask >> i) & 1:
                    adj[i][k], adj[k][i] = 1, 0
                else:
                    adj[i][k], adj[k][i] = 0, 1
            if new_vertex_ok(adj, k):
                rec(k + 1)

    rec(0)
    return out["count"], out["reps"]

def tour_iso(A, B):
    n = len(A)
    oa = [sum(r) for r in A]
    ob = [sum(r) for r in B]
    if sorted(oa) != sorted(ob):
        return False
    perm = [-1] * n
    used = [False] * n

    def bt(i):
        if i == n:
            return True
        for j in range(n):
            if used[j] or oa[i] != ob[j]:
                continue
            if all(A[i][k] == B[j][perm[k]] and A[k][i] == B[perm[k]][j] for k in range(i)):
                perm[i] = j
                used[j] = True
                if bt(i + 1):
                    return True
                used[j] = False
                perm[i] = -1
        return False

    return bt(0)

def aut_count_tour(A):
    n = len(A)
    outd = [sum(r) for r in A]
    perm = [-1] * n
    used = [False] * n
    cnt = 0

    def ok(i, j):
        for k in range(n):
            if perm[k] != -1 and (A[i][k] != A[j][perm[k]] or A[k][i] != A[perm[k]][j]):
                return False
        return True

    def bt(i):
        nonlocal cnt
        if i == n:
            cnt += 1
            return
        for j in range(n):
            if used[j] or outd[i] != outd[j]:
                continue
            if ok(i, j):
                perm[i] = j
                used[j] = True
                bt(i + 1)
                perm[i] = -1
                used[j] = False

    bt(0)
    return cnt

def main():
    Q = qr7()
    aut = aut_count_tour(Q)
    tt4free_Q = not has_tt4(Q, range(7))
    reg = sorted(set(sum(r) for r in Q)) == [3]
    print("# QR_7 = Cay(Z_7,{1,2,4}): TT4-free=%s, doubly-regular(out=3)=%s, |Aut|=%d"
          % (tt4free_Q, reg, aut))

    c7, reps = enumerate_tt4free(7, collect=True)
    all_iso = all(tour_iso(R, Q) for R in reps)
    print("# 7-vertex TT4-free tournaments: labelled count=%d, all isomorphic to QR_7=%s"
          % (c7, all_iso))
    print("#   cross-check 7!/|Aut(QR_7)| = %d" % (math.factorial(7) // aut))

    c8, _ = enumerate_tt4free(8, collect=False)
    print("# 8-vertex TT4-free tournaments: labelled count=%d" % c8)

    ok = (tt4free_Q and reg and aut == 21 and c7 == 240 and all_iso
          and math.factorial(7) // aut == 240 and c8 == 0)
    if ok:
        print("PASS: the unique 7-vertex TT_4-free tournament is QR_7, and every "
              "8-vertex tournament contains a TT_4 (non-neighbourhood bound = 7).")
        return 0
    print("FAIL")
    return 1

if __name__ == "__main__":
    sys.exit(main())
