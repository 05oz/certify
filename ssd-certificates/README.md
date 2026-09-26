# A supersimple (31,6,3)-BIBD — staging

**Status: staged, not released.** The objects are verified. There is no note,
dated sweep record or DOI yet.

A (v,k,λ)-BIBD is *supersimple* if any two of its blocks share at most two
points. The CPro1 benchmark lists the parameter set (v,b,r,k,λ) = (31,93,18,6,3)
among its open instances. Its open-instance list is transcribed from the
*Handbook of Combinatorial Designs*, 2nd ed. (2006), §VI.57 (Gronau). This
directory holds two explicit supersimple (31,6,3)-BIBDs, so such designs exist.

| file | construction | automorphism group | SHA-256 |
|---|---|---|---|
| `SSBIBD_31_6_3_Z31_sat.json` | Base blocks {0,11,17,20,23,24}, {0,6,11,15,16,29}, {0,2,4,14,23,30} developed mod 31 (found by SAT, 2026-09-26) | exactly ℤ₃₁ (per the audit) | `417e65be…67b0d8` |
| `SSBIBD_31_6_3_cyclotomic.json` | {0} ∪ s·C₅ for s ∈ {1,5,25}, where C₅ = ⟨2⟩ = {1,2,4,8,16} ≤ GF(31)*, developed mod 31 | exactly ℤ₃₁ ⋊ ℤ₁₅, block-transitive (per the audit) | `49dc9f25…a72f1e` |
| `sbibd_31_93_18_6_3.txt` | The SAT design as a 31×93 incidence matrix, in CPro1's output format | — | — |

The two designs are not isomorphic, because their automorphism groups differ.
The cyclotomic one is the orbit of {0,1,2,4,8,16} under x ↦ ax + b with a a
nonzero square mod 31. That group has order 465 and is 2-homogeneous, so the
orbit is automatically a 2-design; only the intersection condition needs
checking. By contrast, the full AGL(1,31) orbit is a (31,6,6)-design whose
blocks can share 3 points, so it is **not** supersimple. The checker rejects
it, and it serves as a control.

## Replay

```sh
python3 ssd-scripts/verify_ssbibd.py ssd-certificates/*.json
```

The checker is standard-library only. It checks:
* every block has 6 distinct points in range;
* b = 93 and r = 18, re-derived from the parameters;
* all 465 point pairs are covered exactly 3 times;
* all 4278 block pairs meet in at most 2 points (intersection histogram {0: 930, 1: 1953, 2: 1395});
* the listed base blocks develop mod 31 to exactly the listed blocks.

CPro1's own benchmark verifier `v(soltext, [31,93,18,6,3])` returns `True` on
`sbibd_31_93_18_6_3.txt` and `False` on a one-entry-flipped copy.

The controls are all rejected:
* one point swapped in a block;
* one block dropped;
* a wrong base block;
* the non-supersimple (31,6,6) AGL(1,31) orbit.

## Priority: what is and is not claimed

The existence claim is at audit strength "probably new", not "new". Two
priority audits on 2026-09-26 found no published supersimple BIBD with block
size 6 for any index. They also found no later resolution of this Handbook
entry, and CPro1's repository (head of 2026-06-03) still lists it as open.

Caveats that a release must state:
* Every full text was blocked by the network proxy, so all literature evidence
  is from search snippets. In particular, Dinitz's online Handbook updates page
  and Bluskov–Heinrich, "Super-simple designs with v ≤ 32" (JSPI 95, 2001),
  were not read.
* The cyclotomic construction is classical in form (Wilson-type, 1972). A
  source noting that this particular orbit is supersimple would anticipate the
  result.
* CPro1's list is stale for other supersimple cells. Two further cells that
  CPro1 still lists as open are already settled in the literature:
  * (25,5,3): Chen–Chen–Li–Wei, Discrete Appl. Math. 161 (2013) 2396–2404.
  * (26,6,3): a PSL(2,25)-orbit of Baer sublines, explicit in arXiv:2512.21143 (Dec 2025).
  
  So appearing on the CPro1 list is not evidence of openness.
