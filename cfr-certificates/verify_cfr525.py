#!/usr/bin/env python3
"""Self-contained, exhaustive verifier for the circular Florentine rectangle
CFR(5,25) shipped with this note.

Standard library only (json, hashlib, sys, os); no third-party package, no
external solver, no randomness, no floating point, and no POSIX-only call, so
it runs unchanged on any platform with CPython 3.

Usage:
    python3 verify_cfr525.py [path-to-CFR_5_25.json]

With no argument it reads CFR_5_25.json from the directory that holds this
script. It exits 0 and prints "VERIFIED" iff the object on disk is a genuine
5 x 25 circular Florentine rectangle whose SHA-256 matches the recorded value.

DEFINITION (circular Florentine rectangle CFR(r,n)).
An r x n array; each of the r rows is a permutation of the symbol set
S = {0,1,...,n-1}. Positions in a row are read circularly (indices mod n).
Circular-Florentine property: for every ordered pair of distinct symbols
(a,b) and every distance m in {1,...,n-1}, there is at most one row in which
symbol b sits exactly m steps circularly to the right of symbol a. See
Handbook of Combinatorial Designs, 2nd ed. (2006), Definitions 62.1 and 62.26.

The check is exhaustive and exact. It enumerates all r*n*(n-1) ordered
distance events (a,b,m) directly, by two independent methods, and confirms
they are pairwise distinct. There is no sampling and no unproven step: the
only things a reader must trust are that CPython executes this file as written
and that the definition above is transcribed correctly.
"""

import hashlib
import json
import os
import sys

RECORDED_SHA256 = (
    "9e2d9b339a79d13783d2e24efde49e5ed7904418f2179bf7d3f0143d779ffdcc"
)

# Independent transcription of the object, used only to cross-check the disk
# file against a second copy of the data (belt and suspenders); the verdict is
# computed from whatever the JSON on disk actually contains.
ROWS_REFERENCE = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
     15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
    [0, 7, 14, 21, 3, 10, 17, 24, 6, 13, 20, 2, 9, 16, 23,
     5, 12, 19, 1, 8, 15, 22, 4, 11, 18],
    [0, 24, 3, 12, 16, 20, 14, 18, 2, 6, 15, 4, 8, 17, 21,
     10, 19, 23, 7, 11, 5, 9, 13, 22, 1],
    [0, 5, 22, 11, 23, 19, 18, 10, 24, 16, 8, 21, 13, 12, 4,
     17, 9, 1, 15, 7, 6, 2, 14, 3, 20],
    [0, 15, 9, 24, 7, 22, 19, 5, 17, 14, 4, 12, 2, 23, 13,
     21, 11, 8, 20, 6, 3, 18, 1, 16, 10],
]


def is_permutation(row, n):
    return sorted(row) == list(range(n))


def events_by_window(rows, n):
    """Method A: literal circular sliding window.

    For each row, each start position i, and each distance m in 1..n-1, form
    the event (a,b,m) with a = row[i], b = row[(i+m) mod n]. Return the number
    of events generated and the number of distinct events; equal iff the
    circular-Florentine property holds."""
    seen = set()
    generated = 0
    for row in rows:
        for i in range(n):
            a = row[i]
            for m in range(1, n):
                b = row[(i + m) % n]
                seen.add((a, b, m))
                generated += 1
    return generated, len(seen)


def events_by_positions(rows, n):
    """Method B: per ordered pair via symbol positions.

    In each row the distance from a to b is uniquely (pos[b]-pos[a]) mod n.
    The property holds iff, for every ordered pair (a,b) of distinct symbols,
    these per-row distances are pairwise distinct across the rows. Return the
    number of (pair,row) distances checked and the number that were distinct
    within their pair; equal iff the property holds."""
    r = len(rows)
    pos = [[0] * n for _ in range(r)]
    for ri, row in enumerate(rows):
        for idx, sym in enumerate(row):
            pos[ri][sym] = idx
    checked = 0
    distinct = 0
    for a in range(n):
        for b in range(n):
            if a == b:
                continue
            per_pair = set()
            for ri in range(r):
                m = (pos[ri][b] - pos[ri][a]) % n
                checked += 1
                if m not in per_pair:
                    per_pair.add(m)
                    distinct += 1
    return checked, distinct


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "CFR_5_25.json")

    with open(path, "rb") as f:
        raw = f.read()
    sha = hashlib.sha256(raw).hexdigest()
    data = json.loads(raw)

    rows = data["rows"]
    n = data["n"]
    r = data["r"]

    checks = []

    sha_ok = (sha == RECORDED_SHA256)
    print("[sha256] computed =", sha)
    print("[sha256] recorded =", RECORDED_SHA256)
    print("[sha256] match    =", sha_ok)
    checks.append(sha_ok)

    shape_ok = (r == len(rows) == 5) and (n == 25) and all(
        len(row) == n for row in rows)
    print("[shape ] r=%d, n=%d, %d rows of length n: %s"
          % (r, n, len(rows), shape_ok))
    checks.append(shape_ok)

    ref_ok = (rows == ROWS_REFERENCE)
    print("[cross ] disk rows == independent transcription:", ref_ok)
    checks.append(ref_ok)

    perm_ok = all(is_permutation(row, n) for row in rows)
    print("[perm  ] every row is a permutation of {0..%d}: %s"
          % (n - 1, perm_ok))
    checks.append(perm_ok)

    expected = r * n * (n - 1)
    genA, distinctA = events_by_window(rows, n)
    A_ok = (genA == expected) and (distinctA == expected)
    print("[meth A] window events %d/%d distinct (expected %d): %s"
          % (distinctA, genA, expected, A_ok))
    checks.append(A_ok)

    checkedB, distinctB = events_by_positions(rows, n)
    B_ok = (checkedB == expected) and (distinctB == expected)
    print("[meth B] per-pair distances %d/%d distinct (expected %d): %s"
          % (distinctB, checkedB, expected, B_ok))
    checks.append(B_ok)

    agree = (A_ok == B_ok)
    print("[cross ] methods A and B agree:", agree)
    checks.append(agree)

    ok = all(checks)
    print()
    if ok:
        print("VERIFIED: the object is a valid CFR(5,25); all %d ordered "
              "distance events are distinct, so F_c(25) >= 5." % expected)
        return 0
    print("FAILED: the object is NOT a valid CFR(5,25).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
