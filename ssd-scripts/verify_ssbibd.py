#!/usr/bin/env python3
"""Standard-library checker for supersimple BIBD certificates.

A certificate is JSON {"v": int, "k": int, "lambda": int, "blocks": [[...], ...]}.
It is a supersimple (v, k, lambda)-BIBD iff
  * every block is a set of k distinct points of {0, ..., v-1};
  * every 2-subset of points lies in exactly lambda blocks (the BIBD condition),
    which forces b = lambda v(v-1) / (k(k-1)) blocks and r = lambda (v-1)/(k-1)
    blocks through each point, both re-derived and checked here;
  * any two blocks share at most two points (supersimplicity).

Every pair of points and every pair of blocks is examined; nothing is sampled.
If the certificate lists "base_blocks", the checker also confirms that
developing them modulo v reproduces "blocks" exactly.

Usage: python3 verify_ssbibd.py FILE [FILE ...]      Exit status 0 iff all pass.
"""
import hashlib
import json
import sys
from itertools import combinations


def check(path):
    raw = open(path, "rb").read()
    c = json.loads(raw)
    v, k, lam, blocks = c["v"], c["k"], c["lambda"], c["blocks"]
    digest = hashlib.sha256(raw).hexdigest()

    def fail(msg):
        print("FAIL %s: %s" % (path, msg))
        return False

    sets = []
    for B in blocks:
        if len(B) != k or len(set(B)) != k:
            return fail("block %r does not have %d distinct points" % (B, k))
        if any(not isinstance(x, int) or not 0 <= x < v for x in B):
            return fail("block %r has a point outside 0..%d" % (B, v - 1))
        sets.append(frozenset(B))

    b_expected, rem_b = divmod(lam * v * (v - 1), k * (k - 1))
    r_expected, rem_r = divmod(lam * (v - 1), k - 1)
    if rem_b or rem_r:
        return fail("parameters (%d,%d,%d) fail the divisibility conditions" % (v, k, lam))
    if len(sets) != b_expected:
        return fail("%d blocks, expected b = %d" % (len(sets), b_expected))

    pair_count = {}
    for S in sets:
        for p in combinations(sorted(S), 2):
            pair_count[p] = pair_count.get(p, 0) + 1
    for p in combinations(range(v), 2):
        if pair_count.get(p, 0) != lam:
            return fail("pair %r lies in %d blocks, not %d" % (p, pair_count.get(p, 0), lam))

    for x in range(v):
        rx = sum(1 for S in sets if x in S)
        if rx != r_expected:
            return fail("point %d lies in %d blocks, not r = %d" % (x, rx, r_expected))

    hist = {}
    for S, T in combinations(sets, 2):
        m = len(S & T)
        hist[m] = hist.get(m, 0) + 1
        if m > 2:
            return fail("blocks %s and %s share %d points (not supersimple)"
                        % (sorted(S), sorted(T), m))

    if "base_blocks" in c:
        dev = sorted(tuple(sorted((x + t) % v for x in B))
                     for B in c["base_blocks"] for t in range(v))
        if dev != sorted(tuple(sorted(B)) for B in blocks):
            return fail("developing base_blocks mod %d does not reproduce blocks" % v)

    print("PASS %s: supersimple (%d,%d,%d)-BIBD, b=%d, r=%d, all %d pairs covered "
          "exactly %d times, block intersections %s, sha256=%s"
          % (path, v, k, lam, len(sets), r_expected, v * (v - 1) // 2, lam,
             dict(sorted(hist.items())), digest))
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    results = [check(p) for p in sys.argv[1:]]
    sys.exit(0 if all(results) else 1)
