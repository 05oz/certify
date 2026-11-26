#!/usr/bin/env python3
"""check_same_graphs.py: G38 and G46 are the two bicirculants of [Orden2], relabelled.

[Orden2] is T. S. Orden's Zenodo record doi:10.5281/zenodo.24390891 (2026-11-20). Its two
bicirculants are rebuilt here from the connection sets printed in its README (vertex (x, i)
numbered q*i + x; arc (x, i) -> (x + s mod q, j) for s in S_ij). The check: the map
(i, a) -> (u*i + t*a mod q, 1 - a) carries the arc list of our certificate file onto his graph.

Standard library only. Reads the two certificate files; writes nothing; no network.
Usage: python3 scripts/check_same_graphs.py   (from the package folder; prints PASS, exit status 0)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CERT = os.path.join(HERE, "..", "certificates")

# file, q, connection sets of [Orden2] (S_00, S_01, S_10, S_11), multiplier u, shift t
CASES = [
    ("k73_N38.json", 19, {(0, 0): [5, 6, 16, 17], (0, 1): [16, 17], (1, 0): [5, 6], (1, 1): [10, 11, 16, 17]}, 14, 16),
    ("k83_N46.json", 23, {(0, 0): [2, 5, 11, 19], (0, 1): [4, 10, 18], (1, 0): [0, 8, 17], (1, 1): [2, 11, 19, 20]}, 19, 18),
]


def bicirculant(q, sets):
    arcs = set()
    for (i, j), s_ij in sets.items():
        for x in range(q):
            for s in s_ij:
                arcs.add((q * i + x, q * j + (x + s) % q))
    return arcs


def read_graph(name):
    """Return (N, arc list) of one certificate file. Raises ValueError with the reason if the
    file cannot be read or is not a JSON object with an integer N and a list of integer pairs."""
    try:
        with open(os.path.join(CERT, name), "rb") as f:
            data = json.loads(f.read().decode("utf-8"))
    except OSError as err:
        raise ValueError("cannot be read (%s)" % err.__class__.__name__)
    except (ValueError, RecursionError):
        raise ValueError("is not a JSON text")
    if not isinstance(data, dict) or type(data.get("N")) is not int or not isinstance(data.get("arcs"), list):
        raise ValueError("has no integer N or no list of arcs")
    for pair in data["arcs"]:
        if not (isinstance(pair, list) and len(pair) == 2 and type(pair[0]) is int and type(pair[1]) is int):
            raise ValueError("has an arc that is not a pair of integers")
    return data["N"], [(x, y) for x, y in data["arcs"]]


def main():
    ok = True
    for name, q, sets, u, t in CASES:
        try:
            n, arcs = read_graph(name)
        except ValueError as err:
            ok = False
            print("FAIL: certificates/%s %s" % (name, err))
            continue
        ours = set(arcs)
        his = bicirculant(q, sets)

        def phi(v):
            a, i = divmod(v, q)
            return q * (1 - a) + (u * i + t * a) % q

        bijection = n == 2 * q and sorted(phi(v) for v in range(n)) == list(range(n))
        image = set((phi(x), phi(y)) for x, y in ours)
        same = bijection and len(ours) == len(arcs) and image == his
        ok = ok and same
        print("%s: %d vertices, %d arcs here, %d arcs in the graph of [Orden2]; "
              "(i, a) -> (%d*i + %d*a mod %d, 1 - a) maps ours onto his: %s"
              % (name, n, len(ours), len(his), u, t, q, "yes" if same else "NO"))
    print("PASS: both graphs are the graphs of [Orden2] up to the stated relabelling" if ok
          else "FAIL: a relabelling is not shown to hold")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
