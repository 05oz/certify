#!/usr/bin/env python3
"""Independent recount: how many of the geng-generated connected cubic graphs
are 3-connected (and cubic), using verify_cert.py's independent routines."""
import sys
from verify_cert import g6_decode, neighbors, is_3_connected
tot = c3 = cub = 0
for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith('>'):
        continue
    n, edges = g6_decode(line)
    nb = neighbors(n, edges)
    tot += 1
    if all(len(nb[v]) == 3 for v in range(n)):
        cub += 1
        if is_3_connected(n, nb):
            c3 += 1
print(f"total={tot} cubic={cub} threeconn={c3}")
