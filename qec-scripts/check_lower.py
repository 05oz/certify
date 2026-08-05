#!/usr/bin/env python3
"""check_lower.py -- INDEPENDENT lower-bound certificate checker.

Pure Python stdlib. Shares NO code with the pipeline. Trusted base:
this file (plus, optionally, the external lrat-check binary for speed).

What it does, given a lower-bound certificate JSON:
  1. Loads the RAW parity-check matrices (text files of 0/1 rows).
  2. Verifies the algebraic side conditions that make the SAT encoding
     equivalent to "a nontrivial logical of weight <= K exists":
       CSS X-sector (Hc = H_Z, Hq = H_X, pairing rows Z):
         (a) H_X H_Z^T = 0                    (CSS condition)
         (b) H_X z^T = 0 for every pairing row z
         (c) rank(rows of H_Z + pairing rows) = n - rank(H_X)
       => {x : H_Z x=0, some z.x=1} is EXACTLY the set of nontrivial
          X-logicals.  (Z-sector: swap X<->Z.)
     General stabilizer (S symplectic, pairing rows L):
         (a) omega(s,s')=0 for stabilizer rows   (abelian)
         (b) omega(s,l)=0  for l in L            (L in centralizer)
         (c) rank_symp of stacked (S,L) rows = rank(S) + |L| and
             rank(S)+|L| = n + k where k = n - rank(S)
  3. REGENERATES the CNF from the matrices per the canonical encoding
     spec (documented below) -- the shipped .cnf file is never trusted.
  4. Checks the LRAT unsatisfiability proof against the regenerated
     clause list (internal Python LRAT checker, or --external BINARY).
  5. If the certificate uses symmetry-broken instances, verifies that
     the given permutations are code automorphisms (rank checks), that
     they preserve the qubit blocks, and that the orbits cover the
     blocks (BFS), so the forced-literal instances are exhaustive.
On success prints:  OK lower bound: d_SECTOR >= K+1.

Canonical CNF encoding spec (must match byte-for-byte what the pipeline
solved; any mismatch makes the LRAT check fail, so no trust is needed):
  vars x_i = i+1, i = 0..n-1. Aux vars allocated sequentially:
  (1) per row of Hc in row order: XOR chain over support ascending
      (u_1 = x_{s1}; u_j fresh with u_j = u_{j-1} xor x_{sj}; clause -u_t)
      gate u=a xor b emits (-u a b)(-u -a -b)(u -a b)(u a -b)
  (2) per pairing row: same chain, output b_j, no final unit
  (3) clause (b_1 ... b_k)
  (4) at-most-K on x_1..x_n, in one of two encodings selected by the
      certificate's "cardinality" field (absent => "sinz"):
        "sinz"      Sinz sequential counter (i outer, j inner)
        "totalizer" truncated Bailleux-Boufkhad totalizer, see Gen.totalizer
  (5) forced literals as unit clauses
LRAT proofs may be stored gzip-compressed (.lrat.gz); both the internal
Python replay and the external lrat-check path decompress on the fly.
General stabilizer: vars u_i=i+1, v_i=n+i+1, q_i=2n+i+1; per qubit
  (-u q)(-v q)(u v -q); XOR rows over {v_i: a_i=1} u {u_i: b_i=1} sorted
  by variable index; at-most-K over q.
"""
import json, os, subprocess, sys, tempfile, time


# --------------------------- GF(2) via bitmask ints -------------------------

def load_matrix(path):
    with open(path) as fh:
        rows, cols = map(int, fh.readline().split())
        M = []
        for _ in range(rows):
            line = fh.readline().strip()
            assert len(line) == cols, f"bad row length in {path}"
            M.append([int(c) for c in line])
        return M


def to_masks(M):
    return [sum(bit << i for i, bit in enumerate(row)) for row in M]


def rank_masks(masks):
    pivots = {}
    r = 0
    for m in masks:
        while m:
            top = m.bit_length() - 1
            if top in pivots:
                m ^= pivots[top]
            else:
                pivots[top] = m
                r += 1
                break
    return r


def gf2_dot(a_row, b_row):
    return (sum(x & y for x, y in zip(a_row, b_row))) % 2


# --------------------------- canonical CNF regeneration ---------------------

class Gen:
    def __init__(self, nv):
        self.nv = nv
        self.clauses = []

    def var(self):
        self.nv += 1
        return self.nv

    def emit(self, *lits):
        self.clauses.append(tuple(lits))

    def xor_chain(self, lits):
        cur = lits[0]
        for lit in lits[1:]:
            u = self.var()
            self.emit(-u, cur, lit)
            self.emit(-u, -cur, -lit)
            self.emit(u, -cur, lit)
            self.emit(u, cur, -lit)
            cur = u
        return cur

    def totalizer(self, xs, K):
        """Truncated Bailleux-Boufkhad totalizer. Returns the unary counter
        [o_1..o_m], m = min(len(xs), K+1), o_j meaning "at least j of xs true"
        (only the forcing direction is encoded, which is what at-most-K needs).
        Recursion: split xs at mid = len(xs)//2, recurse LEFT first then RIGHT,
        then allocate the m output vars in ascending order, then emit, for
        a = 0..|A|, b = 0..|B| in that nested order with s = a+b in [1,m],
        the clause (o_s, -a_a, -b_b) omitting absent literals."""
        if len(xs) == 1:
            return [xs[0]]
        mid = len(xs) // 2
        A = self.totalizer(xs[:mid], K)
        B = self.totalizer(xs[mid:], K)
        m = min(len(xs), K + 1)
        O = [self.var() for _ in range(m)]
        for a in range(len(A) + 1):
            for b in range(len(B) + 1):
                s = a + b
                if s < 1 or s > m:
                    continue
                lits = [O[s - 1]]
                if a > 0:
                    lits.append(-A[a - 1])
                if b > 0:
                    lits.append(-B[b - 1])
                self.emit(*lits)
        return O

    def at_most_k_totalizer(self, xs, K):
        O = self.totalizer(xs, K)
        if len(O) > K:
            self.emit(-O[K])

    def at_most_k(self, xs, K):
        n = len(xs)
        if K >= n:
            return
        s = {}
        for i in range(1, n):
            for j in range(1, K + 1):
                s[(i, j)] = self.var()
        self.emit(-xs[0], s[(1, 1)])
        for j in range(2, K + 1):
            self.emit(-s[(1, j)])
        for i in range(2, n):
            self.emit(-xs[i - 1], s[(i, 1)])
            self.emit(-s[(i - 1, 1)], s[(i, 1)])
            for j in range(2, K + 1):
                self.emit(-xs[i - 1], -s[(i - 1, j - 1)], s[(i, j)])
                self.emit(-s[(i - 1, j)], s[(i, j)])
            self.emit(-xs[i - 1], -s[(i - 1, K)])
        self.emit(-xs[n - 1], -s[(n - 1, K)])


def regen_css(Hc, pairing, n, K, forced, cardinality="sinz"):
    g = Gen(n)
    for row in Hc:
        sup = [i + 1 for i, b in enumerate(row) if b]
        if not sup:
            continue
        t = g.xor_chain(sup)
        g.emit(-t)
    bs = []
    for row in pairing:
        sup = [i + 1 for i, b in enumerate(row) if b]
        assert sup, "zero pairing row"
        bs.append(g.xor_chain(sup))
    g.emit(*bs)
    if cardinality == "totalizer":
        g.at_most_k_totalizer(list(range(1, n + 1)), K)
    elif cardinality == "sinz":
        g.at_most_k(list(range(1, n + 1)), K)
    else:
        raise SystemExit(f"unknown cardinality encoding {cardinality}")
    for lit in forced:
        g.emit(lit)
    return g


def regen_stab(S, pairing, n, K, forced):
    g = Gen(3 * n)
    for i in range(n):
        u, v, q = i + 1, n + i + 1, 2 * n + i + 1
        g.emit(-u, q)
        g.emit(-v, q)
        g.emit(u, v, -q)

    def pvars(row):
        a, b = row[:n], row[n:]
        return sorted([n + i + 1 for i, bit in enumerate(a) if bit] +
                      [i + 1 for i, bit in enumerate(b) if bit])
    for row in S:
        vs = pvars(row)
        if not vs:
            continue
        t = g.xor_chain(vs)
        g.emit(-t)
    bs = []
    for row in pairing:
        vs = pvars(row)
        assert vs
        bs.append(g.xor_chain(vs))
    g.emit(*bs)
    g.at_most_k([2 * n + i + 1 for i in range(n)], K)
    for lit in forced:
        g.emit(lit)
    return g


# --------------------------- LRAT checking ----------------------------------

def check_lrat_python(clauses, lrat_path):
    """RUP-with-hints LRAT check. clauses: list of tuples (ids 1..m).
    Returns True iff an empty clause is derived and verified."""
    store = {i + 1: c for i, c in enumerate(clauses)}
    maxvar = 0
    for c in clauses:
        for lit in c:
            maxvar = max(maxvar, abs(lit))
    val = [0] * (maxvar + 1)      # 0 unassigned else +stamp true / -stamp false
    stamp = 0
    empty_ok = False
    with open_lrat(lrat_path) as fh:
        for line in fh:
            toks = line.split()
            if not toks:
                continue
            cid = int(toks[0])
            if len(toks) > 1 and toks[1] == 'd':
                for t in toks[2:]:
                    i = int(t)
                    if i == 0:
                        break
                    store.pop(i, None)
                continue
            nums = [int(t) for t in toks[1:]]
            z1 = nums.index(0)
            lits, hints = nums[:z1], nums[z1 + 1:]
            assert hints and hints[-1] == 0, "malformed LRAT line"
            hints = hints[:-1]
            stamp += 1
            # grow val if proof uses fresh vars (should not happen)
            for lit in lits:
                v = abs(lit)
                if v > maxvar:
                    val.extend([0] * (v - maxvar))
                    maxvar = v
            for lit in lits:            # negate the lemma
                val[abs(lit)] = -stamp if lit > 0 else stamp
            conflict = False
            for h in hints:
                if h < 0:
                    raise SystemExit("RAT hint encountered; use --external lrat-check")
                cl = store.get(h)
                assert cl is not None, f"hint {h} references deleted/absent clause"
                unit = None
                satisfied = False
                for lit in cl:
                    v = abs(lit)
                    if v > maxvar:
                        val.extend([0] * (v - maxvar)); maxvar = v
                    s = val[v]
                    if s == stamp or s == -stamp:      # assigned this round
                        if (s > 0) == (lit > 0):
                            satisfied = True
                            break
                        continue                        # falsified literal
                    if unit is None:
                        unit = lit
                    else:
                        unit = 'many'
                if satisfied or unit == 'many':
                    continue                            # useless hint: skip (sound)
                if unit is None:
                    conflict = True
                    break
                val[abs(unit)] = stamp if unit > 0 else -stamp
            if not conflict:
                raise SystemExit(f"LRAT lemma {cid} NOT verified (no conflict)")
            store[cid] = tuple(lits)
            if not lits:
                empty_ok = True
    return empty_ok


def open_lrat(path):
    """Text handle on a .lrat or gzip-compressed .lrat.gz proof."""
    if path.endswith(".gz"):
        import gzip
        return gzip.open(path, "rt")
    return open(path)


def check_lrat_external(clauses, nv, lrat_path, binary):
    with tempfile.NamedTemporaryFile("w", suffix=".cnf", delete=False) as f:
        f.write(f"p cnf {nv} {len(clauses)}\n")
        for c in clauses:
            f.write(" ".join(map(str, c)) + " 0\n")
        tmp = f.name
    fifo = None
    if lrat_path.endswith(".gz"):
        # feed the external checker through a FIFO so the plain-text proof is
        # never materialised on disk
        fifo = tmp + ".lrat"
        os.mkfifo(fifo)
        feeder = subprocess.Popen(f"gunzip -c {lrat_path!r} > {fifo!r}", shell=True)
        lrat_path = fifo
    try:
        out = subprocess.run([binary, tmp, lrat_path], capture_output=True,
                             text=True, timeout=36000)
        ok = "VERIFIED" in out.stdout and "NOT VERIFIED" not in out.stdout
        if not ok:
            sys.stderr.write(out.stdout[-2000:] + out.stderr[-2000:])
        return ok
    finally:
        os.unlink(tmp)
        if fifo:
            feeder.wait()
            os.unlink(fifo)


# --------------------------- side conditions --------------------------------

def verify_css_side_conditions(HX, HZ, pairing, sector, n):
    Hq, Hc = (HX, HZ) if sector == "X" else (HZ, HX)
    for r1 in HX:                    # (a) CSS orthogonality
        for r2 in HZ:
            assert gf2_dot(r1, r2) == 0, "CSS condition H_X H_Z^T = 0 fails"
    for z in pairing:                # (b) pairing rows in ker(Hq)
        for r in Hq:
            assert gf2_dot(z, r) == 0, "pairing row not in kernel of quotient matrix"
    rq = rank_masks(to_masks(Hq))    # (c) spanning condition
    rc = rank_masks(to_masks(Hc) + to_masks(pairing))
    assert rc == n - rq, f"pairing rows do not span ker/row quotient ({rc} != {n - rq})"


def verify_stab_side_conditions(S, pairing, n):
    def omega_row(p, q):
        return (sum(p[i] & q[n + i] for i in range(n)) +
                sum(p[n + i] & q[i] for i in range(n))) % 2
    for i, s in enumerate(S):
        for s2 in S[i:]:
            assert omega_row(s, s2) == 0, "stabilizer rows do not commute"
        for l in pairing:
            assert omega_row(s, l) == 0, "pairing row not in centralizer"
    rS = rank_masks(to_masks(S))
    k = n - rS
    rAll = rank_masks(to_masks(S) + to_masks(pairing))
    assert rAll == rS + len(pairing), "pairing rows dependent on stabilizers"
    # centralizer dim = n + k; S+L spans an rAll-dim subspace of it (all rows
    # shown to commute with S above); exhaustiveness requires rAll = n + k:
    assert rAll == n + k, "pairing rows do not span centralizer mod stabilizer"


# --------------------------- symmetry verification --------------------------

def verify_symmetry(perms, HX, HZ, n, block, instances, K):
    """perms: list of permutation arrays p (qubit i -> p[i]).
    Verifies each p is an automorphism of both rowspaces and preserves
    blocks [0,block) and [block,n). Verifies orbit of every position in
    block-0 reaches 0 and orbit of every position in block-1 reaches block.
    Verifies the forced-literal patterns are exactly:
      instance 0: [1]  (x_1 true)
      instance 1: [-1..-block, block+1]  (left block zero, first right true)"""
    for p in perms:
        assert sorted(p) == list(range(n)), "not a permutation"
        assert all((i < block) == (p[i] < block) for i in range(n)), \
            "permutation does not preserve blocks"
        for H in (HX, HZ):
            HP = [[row[p[i]] for i in range(n)] for row in H]
            mh = to_masks(H)
            assert rank_masks(mh) == rank_masks(mh + to_masks(HP)), \
                "permutation is not a code automorphism"
    # orbit BFS under the group generated by perms (and inverses)
    inv = []
    for p in perms:
        q = [0] * n
        for i in range(n):
            q[p[i]] = i
        inv.append(q)
    allp = perms + inv

    def orbit(start):
        seen = {start}
        todo = [start]
        while todo:
            v = todo.pop()
            for p in allp:
                w = p[v]
                if w not in seen:
                    seen.add(w)
                    todo.append(w)
        return seen
    orb0 = orbit(0)
    assert all(i in orb0 for i in range(block)), "orbit of qubit 0 misses left block"
    orbR = orbit(block)
    assert all(i in orbR for i in range(block, n)), "orbit misses right block"
    f0 = instances[0]["forced"]
    f1 = instances[1]["forced"]
    assert f0 == [1], "instance 0 forced pattern wrong"
    assert f1 == [-(i + 1) for i in range(block)] + [block + 1], \
        "instance 1 forced pattern wrong"


# --------------------------- main -------------------------------------------

def main():
    args = sys.argv[1:]
    external = None
    if "--external" in args:
        i = args.index("--external")
        external = args[i + 1]
        del args[i:i + 2]
    cert = json.load(open(args[0]))
    base = os.path.dirname(os.path.abspath(args[0]))
    P = lambda f: os.path.join(base, f)
    t0 = time.perf_counter()
    kind = cert["kind"]
    K = cert["K"]
    if kind == "css_lower":
        HX = load_matrix(P(cert["HX_file"]))
        HZ = load_matrix(P(cert["HZ_file"]))
        pairing = load_matrix(P(cert["pairing_file"]))
        n = len(HX[0])
        sector = cert["sector"]
        verify_css_side_conditions(HX, HZ, pairing, sector, n)
        Hc = HZ if sector == "X" else HX
        instances = cert["instances"]
        if cert.get("symmetry"):
            perms = [[int(t) for t in open(P(f)).read().split()]
                     for f in cert["symmetry"]["perm_files"]]
            verify_symmetry(perms, HX, HZ, n, cert["symmetry"]["block"],
                            instances, K)
        else:
            assert len(instances) == 1 and instances[0]["forced"] == []
        card = cert.get("cardinality", "sinz")
        for inst in instances:
            g = regen_css(Hc, pairing, n, K, inst["forced"], card)
            lp = P(inst["lrat_file"])
            if external:
                ok = check_lrat_external(g.clauses, g.nv, lp, external)
            else:
                ok = check_lrat_python(g.clauses, lp)
            assert ok, f"LRAT proof failed for {inst['lrat_file']}"
        ms = (time.perf_counter() - t0) * 1000
        print(f"OK lower bound: d_{sector} >= {K + 1}  [checked in {ms:.1f} ms]"
              f"  ({len(instances)} instance(s), "
              f"{'external ' + os.path.basename(external) if external else 'internal Python'} LRAT check)")
    elif kind == "stab_lower":
        S = load_matrix(P(cert["S_file"]))
        pairing = load_matrix(P(cert["pairing_file"]))
        n = len(S[0]) // 2
        verify_stab_side_conditions(S, pairing, n)
        inst = cert["instances"][0]
        g = regen_stab(S, pairing, n, K, inst["forced"])
        lp = P(inst["lrat_file"])
        ok = (check_lrat_external(g.clauses, g.nv, lp, external) if external
              else check_lrat_python(g.clauses, lp))
        assert ok, "LRAT proof failed"
        ms = (time.perf_counter() - t0) * 1000
        print(f"OK lower bound: d >= {K + 1}  [checked in {ms:.1f} ms]")
    else:
        raise SystemExit(f"unknown kind {kind}")


if __name__ == "__main__":
    main()
