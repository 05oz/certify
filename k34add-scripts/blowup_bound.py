#!/usr/bin/env python3
"""
The tournament-blow-up bound for k(3,4) (Certify, Part J).

For a tournament T, the lexicographic blow-up T[I_m] replaces each vertex by an
independent m-set (arcs go between groups exactly as in T; no arcs inside a group).
A set of pairwise-adjacent vertices of T[I_m] uses at most one vertex per group, so
subtournaments of T[I_m] correspond to subtournaments of T; hence T[I_m] is
TT_4-free iff T is.  And alpha(T[I_2]) = 2, so T[I_2] is I_3-free; but any group of
3 vertices in T[I_3] is an I_3.  Therefore the largest {I_3,TT_4}-free
tournament-blow-up is T[I_2] with T the largest TT_4-free tournament, namely QR_7,
giving 2*7 = 14 vertices and the bound k(3,4) >= 15.

The true value is k(3,4) = 21 (the extremal order is 20).  The blow-up construction
falls 6 vertices short, so the extremal family is substantially non-algebraic.

This script verifies:
  QR_7[I_2] is {I_3,TT_4}-free on 14 vertices;
  QR_7[I_3] is NOT I_3-free (contains an independent triple).
Standard library only; deterministic; no OS-specific calls.
"""
import itertools, sys

def qr7():
    QR = {1, 2, 4}
    M = [[0] * 7 for _ in range(7)]
    for i in range(7):
        for j in range(7):
            if i != j and (j - i) % 7 in QR:
                M[i][j] = 1
    return M

def blowup(T, m):
    t = len(T)
    n = t * m
    A = [[0] * n for _ in range(n)]
    for a in range(t):
        for b in range(t):
            if a != b and T[a][b]:
                for x in range(m):
                    for y in range(m):
                        A[a * m + x][b * m + y] = 1
    return n, A

def adj(A, u, v):
    return A[u][v] or A[v][u]

def i3_free(n, A):
    for a, b, c in itertools.combinations(range(n), 3):
        if not adj(A, a, b) and not adj(A, a, c) and not adj(A, b, c):
            return False
    return True

def tt4_free(n, A):
    for four in itertools.combinations(range(n), 4):
        if all(adj(A, x, y) for x, y in itertools.combinations(four, 2)):
            outs = sorted(sum(1 for y in four if y != x and A[x][y]) for x in four)
            if outs == [0, 1, 2, 3]:
                return False
    return True

def main():
    Q = qr7()
    n2, A2 = blowup(Q, 2)
    n3, A3 = blowup(Q, 3)
    f2 = i3_free(n2, A2) and tt4_free(n2, A2)
    f3 = i3_free(n3, A3)
    print("# QR_7[I_2]: n=%d, {I_3,TT_4}-free=%s" % (n2, f2))
    print("# QR_7[I_3]: n=%d, I_3-free=%s (expected False: a group of 3 is an I_3)" % (n3, f3))
    ok = (n2 == 14 and f2 and (not f3))
    if ok:
        print("PASS: largest {I_3,TT_4}-free tournament-blow-up = QR_7[I_2] on 14 "
              "vertices (bound k(3,4) >= 15); truth is 21, so the gap is 6.")
        return 0
    print("FAIL")
    return 1

if __name__ == "__main__":
    sys.exit(main())
