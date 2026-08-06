#!/usr/bin/env python3
"""INDEPENDENT verifier for a claimed [[14,3,5]] qubit stabilizer code.

Stdlib-only. Shares no code with the search tools (written separately,
different algorithms: no Gray-code walk, no early abort; verifies by direct
exhaustive enumeration of the full normalizer).

Input: a file with 11 generators, one per line, either
  "[a0 a1 ... a13|b0 ... b13]" bit rows, or a single 28-bit hex word per line
  (bit i = X on qubit i, bit 14+i = Z on qubit i), or 11 hex words on 1 line.

Checks, from scratch:
  1. The 11 vectors are F2-independent.
  2. They pairwise commute under the symplectic form (isotropic).
  3. Builds the FULL group S (2^11 elements) and the FULL normalizer
     S_perp = {v : sp(v, g) = 0 for all g in S} by testing all 2^28 vectors
     -- too slow; instead solves the linear system by enumerating the
     nullspace basis via Gaussian elimination WITHOUT reusing search code,
     then enumerates all 2^17 normalizer elements explicitly.
  4. Confirms |S_perp| = 2^17, S subset of S_perp.
  5. Computes min symplectic weight over the set difference S_perp - S by
     exhaustive scan of all 131072 elements.
  6. Verdict PASS iff that minimum is exactly 5 (>=5 proves d>=5; the code
     is a [[14,3,5]] iff min == 5; min > 5 would exceed the table upper
     bound 5 and be reported as suspicious).
"""
import sys

def parse(path):
    gens = []
    text = open(path).read()
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if '|' in line or line.count(' ') > 6 and ('[' in line or set(line) <= set('01 []')):
            bits = [c for c in line if c in '01']
            if len(bits) != 28:
                continue
            v = 0
            for i, c in enumerate(bits):
                if c == '1':
                    v |= 1 << i
            gens.append(v)
        else:
            for tok in line.split():
                gens.append(int(tok, 16))
    return gens

def symp(u, v):
    ua, ub = u & 0x3FFF, u >> 14
    va, vb = v & 0x3FFF, v >> 14
    return (bin(ua & vb).count('1') + bin(ub & va).count('1')) % 2

def weight(v):
    return bin((v | (v >> 14)) & 0x3FFF).count('1')

def main():
    gens = parse(sys.argv[1])
    if len(gens) != 11:
        print(f"FAIL: expected 11 generators, got {len(gens)}")
        sys.exit(1)

    # 1. independence: build row echelon from scratch
    ech = []
    for g in gens:
        x = g
        for e in ech:
            if x ^ e < x:
                x ^= e
        if x == 0:
            print("FAIL: generators dependent")
            sys.exit(1)
        ech.append(x)
        ech.sort(reverse=True)

    # 2. isotropy
    for i in range(11):
        for j in range(i + 1, 11):
            if symp(gens[i], gens[j]):
                print(f"FAIL: generators {i},{j} anticommute")
                sys.exit(1)

    # 3. normalizer basis: nullspace of the 11 linear forms
    #    v -> parity(v & mask_i), mask_i = swapped halves of gens[i]
    masks = [((g & 0x3FFF) << 14) | (g >> 14) for g in gens]
    # Gaussian elimination on 11x28 system
    rows = masks[:]
    pivots = []
    r = 0
    rows = rows[:]
    for c in range(28):
        p = None
        for i in range(r, len(rows)):
            if rows[i] >> c & 1:
                p = i
                break
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        for i in range(len(rows)):
            if i != r and (rows[i] >> c & 1):
                rows[i] ^= rows[r]
        pivots.append(c)
        r += 1
    if r != 11:
        print("FAIL: rank of constraint system != 11")
        sys.exit(1)
    free = [c for c in range(28) if c not in pivots]
    nsbasis = []
    for c in free:
        v = 1 << c
        for i, pc in enumerate(pivots):
            if rows[i] >> c & 1:
                v |= 1 << pc
        nsbasis.append(v)
    if len(nsbasis) != 17:
        print(f"FAIL: normalizer dimension {len(nsbasis)} != 17")
        sys.exit(1)
    for v in nsbasis:
        for g in gens:
            if symp(v, g):
                print("FAIL: claimed normalizer vector anticommutes")
                sys.exit(1)

    # 4. build full S (as a set) and full normalizer
    S = {0}
    for g in gens:
        S |= {x ^ g for x in S}
    if len(S) != 2048:
        print(f"FAIL: |S| = {len(S)}")
        sys.exit(1)
    Np = {0}
    for g in nsbasis:
        Np |= {x ^ g for x in Np}
    if len(Np) != 131072:
        print(f"FAIL: |normalizer| = {len(Np)}")
        sys.exit(1)
    if not S <= Np:
        print("FAIL: S not inside its normalizer")
        sys.exit(1)

    # 5. min weight over Np - S
    dmin = 99
    for v in Np:
        if v in S:
            continue
        w = weight(v)
        if w < dmin:
            dmin = w
    print(f"generators independent: yes")
    print(f"pairwise commuting (isotropic): yes")
    print(f"|S| = 2048, |N(S)| = 131072, S in N(S): yes")
    print(f"min symplectic weight over N(S) - S = {dmin}")
    if dmin == 5:
        print("PASS: this is a [[14,3,5]] qubit stabilizer code")
        sys.exit(0)
    elif dmin > 5:
        print(f"SUSPICIOUS: d = {dmin} > 5 exceeds the known upper bound; recheck input")
        sys.exit(1)
    else:
        print(f"FAIL: distance {dmin} < 5")
        sys.exit(1)

if __name__ == '__main__':
    main()
