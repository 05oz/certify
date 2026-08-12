#!/usr/bin/env python3
"""mkcontrols.py -- build the certificate-checker negative controls.

Standard library only; no imports from the searchers or the checkers.  Reads a
file of genuine CERT lines and writes a control file in which line 1 is the
intact certificate and every later line is one deliberately doctored copy of
it.  Each doctored line is designed to trip a DIFFERENT gate of the checkers:

  1  non-path triple        -- a triple whose middle vertex is not adjacent
  2  cover gap              -- a covered vertex removed from the partition
  3  overlapping triple     -- one triple duplicated over another
  4  sub-maximum packing    -- valid partition, one triple demoted to avoided,
                               so |avoided| != n mod 3 (the avoided-count gate)
  5  non-canonical g6       -- the same graph relabelled: valid certificate,
                               but a graph6 string geng never emits
                               (only the membership gate can catch this)
  6  trailing g6 garbage    -- a valid graph6 string with one extra character
  7  corrupted g6           -- one character changed (breaks cubicity)

Usage:  mkcontrols.py GENUINE_CERT_FILE OUT_FILE
Prints one line per emitted case describing the intended rejection reason.
"""
import sys


def g6_decode(s):
    data = [ord(c) - 63 for c in s]
    n = data[0]
    need = n * (n - 1) // 2
    bits = []
    for d in data[1:]:
        for k in range(5, -1, -1):
            bits.append((d >> k) & 1)
    adj = [set() for _ in range(n)]
    idx = 0
    for j in range(1, n):
        for i in range(j):
            if bits[idx]:
                adj[i].add(j); adj[j].add(i)
            idx += 1
    return n, adj


def g6_encode(n, adj):
    bits = []
    for j in range(1, n):
        for i in range(j):
            bits.append(1 if j in adj[i] else 0)
    while len(bits) % 6:
        bits.append(0)
    out = [chr(n + 63)]
    for k in range(0, len(bits), 6):
        v = 0
        for b in bits[k:k + 6]:
            v = (v << 1) | b
        out.append(chr(v + 63))
    return ''.join(out)


def parse(line):
    head, trip, avoid = line.split('|')
    g6 = head.split()[1]
    triples = [tuple(int(x) for x in t.split('-')) for t in trip.split()]
    avoided = [int(x) for x in avoid.split()]
    return g6, triples, avoided


def fmt(g6, triples, avoided):
    return ("CERT %s | %s | %s"
            % (g6, ' '.join('%d-%d-%d' % t for t in triples),
               ' '.join(str(v) for v in avoided)))


def main():
    src, dst = sys.argv[1], sys.argv[2]
    line = None
    for raw in open(src):
        if raw.startswith('CERT '):
            line = raw.strip(); break
    if line is None:
        sys.exit("no CERT line in " + src)
    g6, triples, avoided = parse(line)
    n, adj = g6_decode(g6)

    out, desc = [line], ["line 1: INTACT -- must be accepted"]

    # 1. non-path triple: replace the middle vertex by a non-neighbour
    a, b, c = triples[0]
    bad = next(v for v in range(n) if v not in (a, b, c) and v not in adj[a])
    t = list(triples)
    t[0] = (a, bad, c)
    keep = [v for v in avoided]
    keep.append(b)
    keep.remove(bad) if bad in keep else None
    # keep the partition intact so the PATH gate is what fires
    t2 = list(triples)
    t2[0] = (a, bad, c)
    rest = [x for tt in t2 for x in tt] + avoided
    out.append(fmt(g6, t2, avoided))
    desc.append("line %d: non-path triple (%d-%d-%d) -- path gate" % (len(out), a, bad, c))

    # 2. cover gap: drop one triple entirely, do not compensate
    out.append(fmt(g6, triples[1:], avoided))
    desc.append("line %d: cover gap (one triple deleted) -- partition gate" % len(out))

    # 3. overlapping triple: duplicate triple 0 over triple 1
    t3 = list(triples)
    t3[1] = triples[0]
    out.append(fmt(g6, t3, avoided))
    desc.append("line %d: overlapping triples -- disjointness gate" % len(out))

    # 4. sub-maximum packing: demote the last triple to the avoided list
    t4 = list(triples[:-1])
    a4 = sorted(avoided + list(triples[-1]))
    out.append(fmt(g6, t4, a4))
    desc.append("line %d: sub-maximum packing, |avoided|=%d != n mod 3=%d "
                "-- avoided-count gate" % (len(out), len(a4), n % 3))

    # 5. non-canonical relabelling: swap two vertices, re-encode, remap triples
    p = list(range(n))
    p[0], p[1] = p[1], p[0]
    adj2 = [set() for _ in range(n)]
    for u in range(n):
        for v in adj[u]:
            adj2[p[u]].add(p[v])
    g6b = g6_encode(n, adj2)
    t5 = [tuple(p[x] for x in tt) for tt in triples]
    a5 = [p[x] for x in avoided]
    out.append(fmt(g6b, t5, a5))
    desc.append("line %d: valid certificate for a NON-CANONICAL relabelling "
                "(%s) -- membership gate only" % (len(out), g6b))

    # 6. trailing garbage on the graph6 string
    out.append(fmt(g6 + '?', triples, avoided))
    desc.append("line %d: graph6 string with one extra character -- length gate" % len(out))

    # 7. corrupted graph6 string
    ch = chr(((ord(g6[3]) - 63) ^ 1) + 63)
    out.append(fmt(g6[:3] + ch + g6[4:], triples, avoided))
    desc.append("line %d: one graph6 character flipped -- cubicity gate" % len(out))

    with open(dst, 'w') as f:
        f.write('\n'.join(out) + '\n')
    for d in desc:
        print(d)


if __name__ == '__main__':
    main()
