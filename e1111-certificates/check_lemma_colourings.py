#!/usr/bin/env python3
"""Stdlib check of the explicit colourings used in Lemma 3 (README):
for every k in 4..K, phi_k on Z_{2k+1} (parity on 0..2k-1, colour 2 on {1,2k-2,2k}) is proper for
Cay(Z_{2k+1},{+-1,+-3}); and Cay(Z_7,{+-1,+-3}) is not 3-colourable (exhaustive) but 4-colourable."""
import itertools, sys
K = int(sys.argv[1]) if len(sys.argv) > 1 else 500
ok = True
for k in range(4, K + 1):
    N = 2 * k + 1
    phi = [i % 2 for i in range(N)]
    for i in (1, 2 * k - 2, 2 * k):
        phi[i] = 2
    for x in range(N):
        for d in (1, 3):
            if phi[x] == phi[(x + d) % N]:
                ok = False; print('FAIL k=%d x=%d d=%d' % (k, x, d))
three = any(all(c[x] != c[(x + d) % 7] for x in range(7) for d in (1, 3)) for c in itertools.product(range(3), repeat=7))
four = [0, 1, 0, 1, 2, 3, 2, 3][:7]
four = next(c for c in itertools.product(range(4), repeat=7) if all(c[x] != c[(x + d) % 7] for x in range(7) for d in (1, 3)))
if three:
    ok = False; print('FAIL: Z7 circulant 3-colourable?')
print('k=4..%d 3-colourings proper: %s; Cay(Z7,{1,3}) 3-colourable: %s; 4-colouring %s' % (K, ok, three, four))
print('PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
