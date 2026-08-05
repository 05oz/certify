#!/usr/bin/env python3
"""check_witness.py -- INDEPENDENT upper-bound certificate checker.

Pure Python stdlib. No numpy, no solver, no imports from the pipeline.
Verifies a distance UPPER bound witness by a handful of matrix-vector
products over GF(2), reading only the raw parity-check matrix files and
the witness JSON.

CSS X-sector witness (x, z) for "d_X <= wt(x)":
    (1) H_Z x = 0          (x commutes with all Z stabilizers)
    (2) H_X z = 0          (z is orthogonal to every row of H_X ... i.e.
                            every row of H_X is orthogonal to z)
    (3) x . z = 1          (so x is NOT in rowspace(H_X): everything in
                            rowspace(H_X) is orthogonal to z)
    => x is a nontrivial X-logical of weight wt(x).
Z-sector: swap roles of H_X and H_Z.

General stabilizer witness (e, f) for "d <= qubit-weight(e)", symplectic:
    (1) omega(s, e) = 0 for every stabilizer row s
    (2) omega(s, f) = 0 for every stabilizer row s   (f in centralizer... not
        required) -- actually only (1), (3) needed:
    (3) omega(e, f) = 1 and omega(s, f) = 0 for all s => e not in rowspace(S).
Usage: check_witness.py witness.json
"""
import json, os, sys, time


def load_matrix(path):
    with open(path) as fh:
        first = fh.readline().split()
        rows, cols = int(first[0]), int(first[1])
        M = []
        for _ in range(rows):
            line = fh.readline().strip()
            assert len(line) == cols, "bad matrix row length"
            M.append([int(ch) for ch in line])
    return M, rows, cols


def matvec_is_zero(M, x):
    """All rows of M orthogonal to x over GF(2)?"""
    for row in M:
        if sum(r & v for r, v in zip(row, x)) % 2 != 0:
            return False
    return True


def dot(a, b):
    return sum(u & v for u, v in zip(a, b)) % 2


def main(path):
    t0 = time.perf_counter()
    cert = json.load(open(path))
    base = os.path.dirname(os.path.abspath(path))
    P = lambda f: os.path.join(base, f)
    kind = cert["kind"]
    if kind == "css_upper":
        HX, _, n = load_matrix(P(cert["HX_file"]))
        HZ, _, n2 = load_matrix(P(cert["HZ_file"]))
        assert n == n2
        x, z = cert["x"], cert["z"]
        assert len(x) == n and len(z) == n
        sector = cert["sector"]           # 'X': x is an X-logical
        Hcomm, Hquot = (HZ, HX) if sector == "X" else (HX, HZ)
        assert matvec_is_zero(Hcomm, x), "FAIL: witness does not commute"
        assert matvec_is_zero(Hquot, z), "FAIL: co-witness not in dual kernel"
        assert dot(x, z) == 1, "FAIL: witness is a stabilizer (trivial)"
        w = sum(x)
        assert w == cert["weight"], "FAIL: declared weight wrong"
        ms = (time.perf_counter() - t0) * 1000
        print(f"OK upper bound: d_{sector} <= {w}  [checked in {ms:.2f} ms]")
    elif kind == "stab_upper":
        S, _, twon = load_matrix(P(cert["S_file"]))
        n = twon // 2
        e, f = cert["e"], cert["f"]
        assert len(e) == twon and len(f) == twon

        def omega(p, q):
            return (sum(p[i] & q[n + i] for i in range(n)) +
                    sum(p[n + i] & q[i] for i in range(n))) % 2
        for s in S:
            assert omega(s, e) == 0, "FAIL: witness anticommutes with stabilizer"
            assert omega(s, f) == 0, "FAIL: co-witness anticommutes with stabilizer"
        assert omega(e, f) == 1, "FAIL: witness is trivial (in stabilizer group)"
        w = sum(e[i] | e[n + i] for i in range(n))
        assert w == cert["weight"], "FAIL: declared weight wrong"
        ms = (time.perf_counter() - t0) * 1000
        print(f"OK upper bound: d <= {w}  [checked in {ms:.2f} ms]")
    else:
        raise SystemExit(f"unknown certificate kind {kind}")


if __name__ == "__main__":
    main(sys.argv[1])
