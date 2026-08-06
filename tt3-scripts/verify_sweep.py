#!/usr/bin/env python3
"""Independent verifier for TT3-packing sweep witness files. Stdlib only.

verify_sweep.py --n N --target K --expect COUNT file1.gz [file2.gz ...]

Each line: <lineno> <bits> <GE|MAX> <k> <a,b,c;...>
Checks per line, from raw data only (no code shared with the searcher):
  * bits has length N(N-1)/2, chars in {0,1}. Tournament: for the P-th pair in the
    ordering (0,1),(0,2),..,(0,N-1),(1,2),..: bits[P]=='1' means i beats j (i<j).
  * status is GE and k >= K (a MAX line would be a below-target tournament: FAIL,
    report loudly - that is a counterexample candidate, not a verification error).
  * the witness lists exactly k triples; every triple a<b<c is TRANSITIVE in this
    tournament (some vertex beats both others and one of those beats the other:
    equivalently NOT a directed 3-cycle); no unordered pair (arc) appears in two
    witness triples.
Global: total number of lines == COUNT.
Exit 0 and print OK iff everything passes.
"""
import argparse
import gzip
import sys


def beats(bits, n, u, v):
    """True iff u beats v in the tournament (u != v)."""
    i, j = (u, v) if u < v else (v, u)
    p = i * (2 * n - i - 1) // 2 + (j - i - 1)
    one = bits[p] == '1'
    return one if u < v else not one


def is_transitive(bits, n, a, b, c):
    ab, bc, ca = beats(bits, n, a, b), beats(bits, n, b, c), beats(bits, n, c, a)
    cycle = (ab and bc and ca) or ((not ab) and (not bc) and (not ca))
    return not cycle


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, required=True)
    ap.add_argument('--target', type=int, required=True)
    ap.add_argument('--expect', type=int, required=True)
    ap.add_argument('files', nargs='+')
    args = ap.parse_args()
    n, K = args.n, args.target
    npairs = n * (n - 1) // 2
    total = 0
    minsize = None
    fails = 0
    for fn in args.files:
        op = gzip.open if fn.endswith('.gz') else open
        with op(fn, 'rt') as f:
            for line in f:
                parts = line.split()
                if len(parts) != 5:
                    print(f"FAIL {fn}: malformed line: {line[:80]}"); fails += 1; continue
                _, bits, status, kstr, wit = parts
                total += 1
                k = int(kstr)
                if len(bits) != npairs or set(bits) - {'0', '1'}:
                    print(f"FAIL {fn}: bad bits {bits}"); fails += 1; continue
                if status != 'GE' or k < K:
                    print(f"BELOW-TARGET tournament (candidate counterexample!) "
                          f"{fn}: {bits} status={status} k={k}")
                    fails += 1
                    continue
                triples = [tuple(map(int, t.split(','))) for t in wit.split(';')]
                if len(triples) != k:
                    print(f"FAIL {fn}: witness count {len(triples)} != {k} for {bits}")
                    fails += 1; continue
                used = set()
                ok = True
                for (a, b, c) in triples:
                    if not (0 <= a < b < c < n):
                        ok = False; break
                    if not is_transitive(bits, n, a, b, c):
                        ok = False; break
                    for e in ((a, b), (b, c), (a, c)):
                        if e in used:
                            ok = False; break
                        used.add(e)
                    if not ok:
                        break
                if not ok:
                    print(f"FAIL {fn}: bad witness for {bits}: {wit}"); fails += 1; continue
                if minsize is None or k < minsize:
                    minsize = k
    if total != args.expect:
        print(f"FAIL: total lines {total} != expected {args.expect}"); fails += 1
    if fails:
        print(f"RESULT: FAILED ({fails} failures)"); sys.exit(1)
    print(f"OK: {total} tournaments, every witness valid, arc-disjoint, transitive; "
          f"min witness size = {minsize} >= target {K}")


if __name__ == '__main__':
    main()
