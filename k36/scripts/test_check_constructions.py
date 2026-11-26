#!/usr/bin/env python3
"""Controls for check_constructions.py. Standard library only, no network,
writes nothing (all tampering is done in memory).

Usage:  python3 test_check_constructions.py [CERT_DIR]
Exit status 0 iff every control behaves as expected.

Part 1: the three genuine files pass, and nine corrupted copies fail.
Part 2: the two conditions that note.md states as equivalences are tested
against brute force on random small cases (fixed seed):
  (a) a Z_q bicirculant has no transitive triangle iff
      (S_ab + S_bc) and S_ac are disjoint mod q for all a, b, c;
  (b) a Cayley digraph Cay(Z_m0 x Z_m1, S) has no independent 3-set iff
      T = G minus (S, -S, 0) is sum-free.
"""
import contextlib
import copy
import importlib.util
import io
import itertools
import json
import os
import random
import sys

sys.dont_write_bytecode = True  # importing check_constructions.py must not write a cache
HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "check_constructions", os.path.join(HERE, "check_constructions.py"))
cc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cc)

problems = []


def run(fn, *args):
    """Run one check function quietly; return the number of failed checks."""
    del cc.failures[:]
    with contextlib.redirect_stdout(io.StringIO()):
        fn(*args)
    n = len(cc.failures)
    del cc.failures[:]
    return n


def expect(label, nfail, want_fail):
    ok = (nfail > 0) == want_fail
    print("  %s  %s (failed checks: %d, expected %s)"
          % ("ok  " if ok else "BAD ", label, nfail, "> 0" if want_fail else "0"))
    if not ok:
        problems.append(label)


def part1(cdir):
    print("Part 1: genuine files pass, corrupted copies fail")
    files = {}
    for name in ("k73_N38.json", "k83_N46.json", "k36_N72.json"):
        files[name] = json.load(open(os.path.join(cdir, name), "rb"))
    b73 = dict(cc.BICIRCULANTS)["k73_N38.json"]
    b83 = dict(cc.BICIRCULANTS)["k83_N46.json"]
    c36 = dict(cc.CAYLEY)["k36_N72.json"]
    expect("k73 genuine", run(cc.check_bicirculant, "k73", b73, files["k73_N38.json"]), False)
    expect("k83 genuine", run(cc.check_bicirculant, "k83", b83, files["k83_N46.json"]), False)
    expect("k36 genuine", run(cc.check_cayley, "k36", c36, files["k36_N72.json"]), False)

    w = copy.deepcopy(files["k73_N38.json"]); u, v = w["arcs"][0]; w["arcs"][0] = [v, u]
    expect("k73 with one arc reversed", run(cc.check_bicirculant, "k73", b73, w), True)
    w = copy.deepcopy(files["k73_N38.json"]); w["arcs"].append(list(w["arcs"][5]))
    expect("k73 with one arc repeated", run(cc.check_bicirculant, "k73", b73, w), True)
    w = copy.deepcopy(files["k73_N38.json"]); w["arcs"].pop(7)
    expect("k73 with one arc deleted", run(cc.check_bicirculant, "k73", b73, w), True)
    w = copy.deepcopy(files["k73_N38.json"]); w["connection_sets"]["S00"] = [8, 12, 13, 16]
    expect("k73 with a stored connection set changed", run(cc.check_bicirculant, "k73", b73, w), True)
    w = copy.deepcopy(files["k83_N46.json"]); w["a"] = 9
    expect("k83 with a changed to 9", run(cc.check_bicirculant, "k83", b83, w), True)
    w = copy.deepcopy(files["k83_N46.json"]); w["arcs"][3][1] = (w["arcs"][3][1] + 1) % 46
    expect("k83 with one arc head moved", run(cc.check_bicirculant, "k83", b83, w), True)
    w = copy.deepcopy(files["k36_N72.json"]); w["arcs"].pop(0)
    expect("k36 with one arc deleted", run(cc.check_cayley, "k36", c36, w), True)
    w = copy.deepcopy(files["k36_N72.json"]); w["S"][0] = [1, 2]
    expect("k36 with a stored element of S changed", run(cc.check_cayley, "k36", c36, w), True)
    w = copy.deepcopy(files["k36_N72.json"]); w["arcs"][10] = [w["arcs"][10][0], True]
    expect("k36 with a boolean arc endpoint", run(cc.check_cayley, "k36", c36, w), True)


def bicirculant_arcs(q, sets):
    arcs = set()
    for (a, b), D in sets.items():
        for i in range(q):
            for d in D:
                arcs.add((a * q + i, b * q + (i + d) % q))
    return arcs


def has_tt3(N, arcs):
    for u, v in arcs:
        for w in range(N):
            if (v, w) in arcs and (u, w) in arcs:
                return True
    return False


def random_bicirculant(rng, q):
    # S00, S11: oriented within an orbit (pick at most one of d, -d; d != 0);
    # S01, S10: S01 and -S10 disjoint. Sizes |S00| = |S11|, |S01| = |S10|
    # so that the graph is regular, as check_bicirculant expects.
    pairs = [(d, q - d) for d in range(1, (q + 1) // 2)]
    x = rng.randint(0, len(pairs))
    s00 = [rng.choice(p) for p in rng.sample(pairs, x)]
    s11 = [rng.choice(p) for p in rng.sample(pairs, x)]
    y = rng.randint(0, q // 2)
    s01 = rng.sample(range(q), y)
    rest = [e for e in range(q) if (-e) % q not in s01]
    if len(rest) < y:
        return None
    s10 = rng.sample(rest, y)
    return {"S00": s00, "S01": s01, "S10": s10, "S11": s11}, x + y


def part2a(rng, trials):
    agree = disagree = with_tt3 = 0
    for _ in range(trials):
        q = rng.randint(5, 11)
        made = random_bicirculant(rng, q)
        if made is None:
            continue
        S, deg = made
        sets = {(a, b): set(S["S%d%d" % (a, b)]) for a in (0, 1) for b in (0, 1)}
        arcs = bicirculant_arcs(q, sets)
        spec = {"N": 2 * q, "a": 2 * q, "b": 3, "q": q, "deg": deg, "S": S}
        w = {"N": 2 * q, "a": 2 * q, "b": 3, "connection_sets": S,
             "arcs": [list(e) for e in sorted(arcs)]}
        script_says_free = run(cc.check_bicirculant, "rand", spec, w) == 0
        brute_free = not has_tt3(2 * q, arcs)
        with_tt3 += not brute_free
        if script_says_free == brute_free:
            agree += 1
        else:
            disagree += 1
    print("  (a) bicirculants: %d agree, %d disagree (%d of them contain a transitive triangle)"
          % (agree, disagree, with_tt3))
    if disagree or agree == 0 or with_tt3 == 0 or with_tt3 == agree:
        problems.append("part 2a")


def part2b(rng, trials):
    agree = disagree = with_i3 = 0
    for _ in range(trials):
        m0, m1 = rng.randint(2, 8), rng.randint(1, 3)
        G = [(x, y) for x in range(m0) for y in range(m1)]
        neg = lambda g: ((-g[0]) % m0, (-g[1]) % m1)
        seen, S = set(), []
        for g in G:
            if g == (0, 0) or g in seen or neg(g) == g:
                seen.add(g)
                continue
            seen.add(g); seen.add(neg(g))
            r = rng.random()
            if r < 0.4:
                S.append(g)
            elif r < 0.8:
                S.append(neg(g))
        N = m0 * m1
        idx = lambda g: m1 * g[0] + g[1]
        arcs = set()
        for g in G:
            for s in S:
                h = ((g[0] + s[0]) % m0, (g[1] + s[1]) % m1)
                arcs.add((idx(g), idx(h)))
        adj = arcs | set((v, u) for u, v in arcs)
        brute_ok = not any((u, v) not in adj and (u, w) not in adj and (v, w) not in adj
                           for u, v, w in itertools.combinations(range(N), 3))
        spec = {"N": N, "a": 3, "b": 99, "mod": (m0, m1), "deg": len(S), "S": S}
        w = {"N": N, "a": 3, "b": 99, "S": [list(s) for s in S],
             "arcs": [list(e) for e in sorted(arcs)]}
        script_ok = run(cc.check_cayley, "rand", spec, w) == 0
        with_i3 += not brute_ok
        if script_ok == brute_ok:
            agree += 1
        else:
            disagree += 1
    print("  (b) Cayley digraphs: %d agree, %d disagree (%d of them contain an independent 3-set)"
          % (agree, disagree, with_i3))
    if disagree or agree == 0 or with_i3 == 0 or with_i3 == agree:
        problems.append("part 2b")


def main(argv):
    cdir = argv[1] if len(argv) > 1 else os.path.join(HERE, os.pardir, "certificates")
    part1(cdir)
    print("Part 2: stated equivalences against brute force (seed 20261111)")
    rng = random.Random(20261111)
    part2a(rng, 600)
    part2b(rng, 600)
    if problems:
        print("FAIL: %d control(s) did not behave as expected: %s" % (len(problems), problems))
        return 1
    print("PASS: every control behaved as expected")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
