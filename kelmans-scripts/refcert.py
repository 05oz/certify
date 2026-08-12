#!/usr/bin/env python3
"""refcert.py — REFEREE-side certificate checker (problem-4 audit, 2026-08-05).

Fresh stdlib-only code; shares nothing with p3span.c / verify_cert.py.
Reads CERT/RCERT lines:  CERT <g6> | a-b-c a-b-c ... | avoided...
For each certificate it re-derives everything from the g6 string alone:
  - graph6 decode (own decoder), simple graph, every degree = 3;
  - optional: g6 string must be a member of a reference generator stream (--g6set);
  - optional: 3-connectivity (connected after every deletion of <= 2 vertices, BFS);
  - each listed triple a-b-c is a path: 3 distinct vertices, edges ab and bc present;
  - triples + avoided vertices partition {0..n-1} exactly (no overlap, no gap);
  - |avoided| == n mod 3.
Any violation -> "REJECT <line#> <reason>" and exit code 1 at the end.

Usage: refcert.py CERTFILE [--n N] [--g6set FILE] [--check3c]
"""
import sys


def decode_g6(s):
    n = ord(s[0]) - 63
    if not (1 <= n <= 62):
        raise ValueError("bad order byte")
    nbits = n * (n - 1) // 2
    nbytes = -(-nbits // 6)
    if len(s) != 1 + nbytes:
        raise ValueError("bad length")
    acc = 0
    for ch in s[1:]:
        v = ord(ch) - 63
        if not (0 <= v <= 63):
            raise ValueError("bad byte")
        acc = (acc << 6) | v
    acc >>= (6 * nbytes - nbits)          # drop padding bits at the end
    adj = [set() for _ in range(n)]
    # acc now holds the nbits upper-triangle bits, first bit = MSB
    pos = nbits - 1
    for col in range(1, n):
        for row in range(col):
            if (acc >> pos) & 1:
                adj[row].add(col)
                adj[col].add(row)
            pos -= 1
    return n, adj


def connected_after_removing(n, adj, gone):
    left = [v for v in range(n) if v not in gone]
    if not left:
        return True
    seen = {left[0]}
    stack = [left[0]]
    while stack:
        u = stack.pop()
        for w in adj[u]:
            if w not in gone and w not in seen:
                seen.add(w)
                stack.append(w)
    return len(seen) == len(left)


def is_3connected(n, adj):
    if not connected_after_removing(n, adj, set()):
        return False
    for u in range(n):
        if not connected_after_removing(n, adj, {u}):
            return False
    for u in range(n):
        for v in range(u + 1, n):
            if not connected_after_removing(n, adj, {u, v}):
                return False
    return True


def main():
    args = sys.argv[1:]
    certfile = args[0]
    expect_n = None
    g6set = None
    check3c = False
    i = 1
    while i < len(args):
        if args[i] == "--n":
            expect_n = int(args[i + 1]); i += 2
        elif args[i] == "--g6set":
            g6set = set(l.strip() for l in open(args[i + 1]) if l.strip()); i += 2
        elif args[i] == "--check3c":
            check3c = True; i += 1
        else:
            sys.exit("unknown arg " + args[i])

    ok = bad = 0
    for lineno, raw in enumerate(open(certfile), 1):
        raw = raw.strip()
        if not raw or not (raw.startswith("CERT ") or raw.startswith("RCERT ")):
            continue
        def rej(msg):
            print(f"REJECT line {lineno}: {msg}")
        parts = raw.split("|")
        head = parts[0].split()
        if len(parts) != 3 or len(head) != 2:
            rej("malformed line"); bad += 1; continue
        g6 = head[1]
        try:
            n, adj = decode_g6(g6)
        except ValueError as e:
            rej(f"g6 decode: {e}"); bad += 1; continue
        if expect_n is not None and n != expect_n:
            rej(f"order {n} != expected {expect_n}"); bad += 1; continue
        if any(len(adj[v]) != 3 for v in range(n)):
            rej("not cubic"); bad += 1; continue
        if any(v in adj[v] for v in range(n)):
            rej("self-loop"); bad += 1; continue
        if g6set is not None and g6 not in g6set:
            rej("g6 not in reference generator stream"); bad += 1; continue
        if check3c and not is_3connected(n, adj):
            rej("not 3-connected"); bad += 1; continue
        trips = []
        fail = None
        for tok in parts[1].split():
            try:
                a, b, c = (int(x) for x in tok.split("-"))
            except ValueError:
                fail = f"bad triple token {tok}"; break
            if len({a, b, c}) != 3 or not all(0 <= x < n for x in (a, b, c)):
                fail = f"triple {tok} vertices invalid"; break
            if b not in adj[a] or c not in adj[b]:
                fail = f"triple {tok} is not a path (missing edge)"; break
            trips.append((a, b, c))
        if fail:
            rej(fail); bad += 1; continue
        avoided = []
        for tok in parts[2].split():
            avoided.append(int(tok))
        used = [v for t in trips for v in t] + avoided
        if len(used) != len(set(used)):
            rej("overlap between triples/avoided"); bad += 1; continue
        if set(used) != set(range(n)):
            rej("cover gap: triples+avoided != V"); bad += 1; continue
        if len(avoided) != n % 3:
            rej(f"avoided count {len(avoided)} != n mod 3 = {n % 3}"); bad += 1; continue
        ok += 1
    print(f"REFCERT-SUMMARY file={certfile} ok={ok} rejected={bad}"
          + (" [membership checked]" if g6set is not None else "")
          + (" [3-connectivity checked]" if check3c else ""))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
