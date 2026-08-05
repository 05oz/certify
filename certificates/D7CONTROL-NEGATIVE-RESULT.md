# Degree-7 positive control — negative computational record (2026-08-04)

`ms_D7control_c32003.ms` (23 unknowns, 36 equations, degree-7 caps, Branch II f0-normalized):
msolve -g 2 -t 8 did NOT terminate within a 600 s wall cap on Apple M4 / 16 GB (two attempts).
This is expected: the degree-7 system is satisfiable (nonempty variety), and reduced-GB computation
on nonempty positive-dimensional varieties is far harder than emptiness certification.

The ACTUAL positive control for the pipeline is exact substitution, verified symbolically:
the torus-scaled Alpöge map (nu^5 = 1/2, r = -1/nu) satisfies the identical normalized system —
bracket = 1 with C1-coefficient = 1 — i.e. every equation of the D7 system vanishes on it identically.
(The asserted form of this check is `min_verify.py d7control` — it builds the exactly-scaled
triple (nu r^-2 A, nu r^-1 B, nu r C) with nu = (1/2)^(1/5) kept symbolic, and asserts
bracket == 1 identically with the C1-coefficient normalized to 1. It ships in this
repository as `scripts/min_verify.py`; see also the preprint's positive-control paragraph.)
This file replaces a previously-empty out_D7control.txt so the record cannot be mistaken
for a silently-failed run.
