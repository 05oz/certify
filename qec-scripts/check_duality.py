#!/usr/bin/env python3
"""check_duality.py -- INDEPENDENT ZX-duality certificate checker.

Pure Python stdlib. Certificate: a permutation Pi of the n qubits such that
    rowspace(H_X . Pi) = rowspace(H_Z)   and   rowspace(H_Z . Pi) = rowspace(H_X)
(column-permuted matrices, (M.Pi)[r][i] = M[r][Pi[i]]).

LEMMA (5 lines): if both hold, then y with y_i = x_{Pi[i]} maps every
nontrivial X-logical x to a nontrivial Z-logical y of the SAME weight, and
vice versa. Hence d_X = d_Z, and a certificate for one sector transfers to
the other. Proof: for h a row of H_X: y.h = x.(h o Pi^{-1}) and
rowspace(H_X Pi^{-1}) = rowspace(H_Z) (apply Pi^{-1} to hypothesis 2), so
y.h = 0 since H_Z x = 0. If y were c.H_Z then x = y o Pi^{-1} would lie in
rowspace(H_Z Pi^{-1}) = rowspace(H_X) (hypothesis 1... apply Pi^{-1} to
hypothesis 1: rowspace(H_X) = rowspace(H_Z Pi^{-1})), contradiction.
Weight is preserved because Pi is a bijection on coordinates.

Usage: check_duality.py duality.json
"""
import json, os, sys, time


def load_matrix(path):
    with open(path) as fh:
        rows, cols = map(int, fh.readline().split())
        return [[int(c) for c in fh.readline().strip()] for _ in range(rows)]


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


def rowspace_equal(M1, M2):
    a, b = to_masks(M1), to_masks(M2)
    ra, rb, rab = rank_masks(a), rank_masks(b), rank_masks(a + b)
    return ra == rb == rab


def main(path):
    t0 = time.perf_counter()
    cert = json.load(open(path))
    base = os.path.dirname(os.path.abspath(path))
    HX = load_matrix(os.path.join(base, cert["HX_file"]))
    HZ = load_matrix(os.path.join(base, cert["HZ_file"]))
    pi = [int(t) for t in open(os.path.join(base, cert["perm_file"])).read().split()]
    n = len(HX[0])
    assert sorted(pi) == list(range(n)), "not a permutation"
    HXp = [[row[pi[i]] for i in range(n)] for row in HX]
    HZp = [[row[pi[i]] for i in range(n)] for row in HZ]
    assert rowspace_equal(HXp, HZ), "rowspace(HX.Pi) != rowspace(HZ)"
    assert rowspace_equal(HZp, HX), "rowspace(HZ.Pi) != rowspace(HX)"
    ms = (time.perf_counter() - t0) * 1000
    print(f"OK duality: d_X = d_Z (weight-preserving ZX bijection) "
          f"[checked in {ms:.2f} ms]")


if __name__ == "__main__":
    main(sys.argv[1])
