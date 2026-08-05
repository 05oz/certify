#!/usr/bin/env python3
"""gen_duality.py -- emit ZX-duality certificates for the BB codes.
Pi: left qubit (r,s) -> right position (-r mod l, -s mod m); right -> left.
Verified independently by check_duality.py (two rowspace-equality rank checks)."""
import json, os
import qec_lib as Q

HERE = os.path.dirname(os.path.abspath(__file__))

for name in ("bb72", "bb90", "bb108", "bb144", "bb288"):
    p = Q.BB_PARAMS[name]
    l, m = p["l"], p["m"]
    lm = l * m
    pi = [0] * (2 * lm)
    for r in range(l):
        for s in range(m):
            src = r * m + s
            tgt = ((-r) % l) * m + ((-s) % m)
            pi[src] = lm + tgt
            pi[lm + src] = tgt
    d = os.path.join(HERE, "certificates", name)
    if not os.path.isdir(d):
        continue
    with open(os.path.join(d, "duality_perm.txt"), "w") as f:
        f.write(" ".join(map(str, pi)) + "\n")
    with open(os.path.join(d, "duality.json"), "w") as f:
        json.dump(dict(kind="zx_duality", HX_file="HX.txt", HZ_file="HZ.txt",
                       perm_file="duality_perm.txt"), f, indent=1)
    print("wrote duality certificate:", name)
