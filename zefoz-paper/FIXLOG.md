# Build-and-verification log — note-zefoz (Part M), 2026-08-12

Target: the certified ZEFOZ certificate
(`zefoz-certificates/certificate2.json`), its standard-library checker
(`zefoz-certificates/zefoz_checker2.py`), the re-verified pilot certificate
(`certificate_pilot.json` + `zefoz_checker_pilot.py`), the scripts
(`zefoz-scripts/anchor_check.py`, `tamper_demo.py`, `kill-logs/`), and the
note (`note.tex`, `note.md`). This is the build/verification decision log; the
dated novelty and verification sweep is `SWEEP-RECORD-ZEFOZ-2026-08-12.md`.

The note claims exactly two things, one positive and one negative: (1)
certified gradient bounds, Hessian-spectrum brackets with signatures, and
Krawczyk existence/uniqueness boxes at the twenty published ZEFOZ points of
arXiv:2412.10126v3 (both sites), plus an exact symbolic time-reversal
certificate for zero-field stationarity of all 120 transitions with zero-field
curvature brackets for the ten published pairs; (2) the pre-registered
completeness kill condition K2 fired, with measured statistics. No physical
result is claimed; the model, the parameters, and all mathematical tools are
cited to their sources at point of use.

## Soundness defects found and fixed during the build (adversarial pass)

1. **Time-reversal identity could not be checked on interval matrices.** The
   first implementation compared endpoint rationals of the sqrt-interval
   entries of H0 under the signed-permutation transform; outward rounding is
   not equivariant under the transform and the check failed spuriously.
   Fixed by verifying the identity in exact symbolic arithmetic over
   Q[sqrt(d)] (squarefree-radical dictionaries); engine and checker both do
   the symbolic check; a flipped-sign tamper (T4) is rejected.
2. **Congruence is not similarity.** The 3x3 Hessian eigenvalue brackets were
   first taken from Gershgorin discs of R^T Hess R with a dyadic-rounded
   rotation R, which is not exactly orthogonal, so the discs do not directly
   bound the eigenvalues of Hess. Fixed by adding the exact Ostrowski
   congruence correction (lambda_k(H) = lambda_k(R^T H R)/theta_k with
   theta_k in [1-e, 1+e], e >= ||R^T R - I||, Horn-Johnson Thm 4.5.9) and
   merging overlapping discs into components before per-index claims. Both
   engine and checker carry the correction.
3. **Krawczyk radius was initially unsound-by-failure.** At the first-chosen
   box radius 2^-33 mT the certified contraction inequality cannot hold
   (||C|| * L * r ~ 86 with the smallest certified Hessian eigenvalue
   5.67e-8 MHz/mT^2); the radius was set to 2^-45 mT from the contraction
   arithmetic before any run. All twenty contractions then certify with worst
   ratio 0.096. This is why the candidates are polished to ~70 digits: an
   existence certificate at clock points is impossible from double-precision
   candidates with this operator (note Section 3.3).
4. **Polarization constant.** The trilinear polarization bound derived in the
   note's appendix is 4.5*M; engine and checker deliberately use the laxer
   9*M. Documented in the appendix; margins are orders of magnitude either
   way.
5. **mpmath precision floor.** Dyadic freezing at 2^-120 / 2^-170 requires
   mantissas beyond dps=60; working precision was set to dps=70 so that
   truncation error stays below the frozen resolution.

## Claims-vs-artifacts audit (note against certificate2.json, this build)

- 20/20 Krawczyk contractions present and re-verified; worst K/r ratio
  0.09561; radius 2^-45 mT = 2.842e-14 mT. Note quotes 0.096 and 2.9e-14. OK.
- Worst certified gradient-norm bound 3.10e-37 MHz/mT; note claims <=
  3.2e-37. OK.
- Eigenvalue bracket widths 2.0e-10 MHz; transition widths 4.0e-10 MHz. OK.
- Table-5 Hessian eigenvalue bracket widths <= 2.01e-15; zero-field <=
  2.06e-9 MHz/mT^2 (note: 2.1e-15, 2.1e-9). OK (first draft said 2.5e-16 and
  1e-10; corrected in audit).
- Signatures: ten site-1 plus site-2 (5,6),(5,7),(6,7) are (-,-,+); the
  remaining seven site-2 are (-,-,-); 13 saddles + 7 maxima; none minima. OK.
- Smallest certified |Hessian eigenvalue| among the twenty: 5.6706e-8
  MHz/mT^2 (site 1 (10,11)). OK.
- Certified restatements: f_67 = 748.5431883, f_47 = 2220.5387344 (+-2e-10);
  published 745.8, 2216.2; deltas -2.74, -4.34 MHz. OK.
- Site-2 (14,15) certified field (-378.985642, +73.267474, +502.352109) mT;
  certified Hessian spectrum {-1.65241e-4, -8.94878e-5, -1.44676e-6}. OK.
- Zero-field: TR identity checked symbolically for both sites; both B=0
  spectra certified simple (disjoint 2e-10 brackets; site-1 minimum gap
  0.004 MHz clears the width by 7 orders). OK.
- Checker wall time 38.5 s (CPython 3.14.2, macOS); pilot checker 46.5 s.
  Note quotes 39 s / 47 s. OK.
- Kill statistics in the note match `zefoz-scripts/kill-logs/*.json` and
  `KILL-STATS.md` (six chunks, both sites; zero closed boxes at 340-s budget;
  per-box 1.4-2.4 s; projection arithmetic recorded in KILL-STATS.md). OK.

## Replay audit (independent of the generator)

- `zefoz_checker2.py certificate2.json`: exit 0, "CERTIFICATE VERIFIED".
- `zefoz_checker_pilot.py certificate_pilot.json`: exit 0 (pilot re-verified
  before building on it, per program law).
- `tamper_demo.py`: control passes; six tampers (shifted Hessian bracket,
  shifted gradient enclosure, corrupted inertia count, flipped time-reversal
  sign, understated gradient-norm bound, inflated Krawczyk radius) each
  rejected exit 1, all at the mathematical re-derivation layer (no hash
  layer exists in this certificate).
- `anchor_check.py` (mpmath, independent eigensolver code path): all 352+352
  certified eigenvalue brackets of both certificates contain the 60-digit
  recomputed eigenvalues; worst margins 1.0e-10 MHz (Part M) and 1.0e-6 MHz
  (pilot).

## What is trusted

Python standard library (fractions/json/math/sys); the classical theorems
cited in the note (Sylvester inertia, Davis-Kahan, Ostrowski, Krawczyk, the
appendix resolvent/Cauchy lemma, analytic perturbation formulas for simple
eigenvalues); nothing else. The branch-and-bound kill statistics are engine
measurements (run logs shipped), not certified objects, and the note labels
them as such.

## Documentation-correction round, 2026-08-13

Recorded after the fact. The v0.14.0 round corrected six claims in this part and left no entry
here; the Engine 2 re-gate of 2026-08-13 found the omission. One is a mathematical misstatement
about the certified data; the rest are values restated from the artifacts. No certificate,
checker or certified value changed — every correction below is prose brought into agreement with
`zefoz-certificates/certificate2.json`, which is byte-identical to its released form.

**M-1. "None of the ten published zero-field transitions has a definite Hessian" was false.**
Re-derived from the certificate with exact `Fraction` arithmetic over all thirty eigenvalue
brackets of the ten zero-field transitions: four carry the certified signature (+,+,+) and are
therefore positive-definite — site 1 (6,8) and (6,9), site 2 (6,8) and (7,11) — six are
indefinite, and none is indeterminate. At zero field those four frequencies are local minima in
B, not saddles. Corrected in both twins and in the closing physical-atlas paragraph, which now
distinguishes the twenty published nonzero-field points (saddles or maxima, none minima) from
the ten zero-field pairs (six saddles, four local minima).
Propagation grep (`none of the ten`): 0 remaining in tracked text, 0 in extracted PDF text.

**M-2. The reported zero-field Hessian spectrum was stale.** The note printed a least eigenvalue
of −11.9910…; the certificate's bracket for site 1 (7,9) is
[−11.990569855135, −11.990569854807]. Corrected to −11.9905… in both twins.

**M-3. The search box was described as 191 mT–5.3 T.** The twenty published points span
191 mT–2.48 T; 5.3 T is not attained. Corrected in both twins.
Propagation grep (`5.3 T`, `5.3~T`, `$5.3$`): 0 remaining in tracked text, 0 in extracted PDF
text.

**M-4. The projected both-sites cost was rounded to 1.6e6 and the per-site figure was wrong in
the kill log.** Re-derived: 713 s/mT^3 × 4.0e6 mT^3 / 3600 s/h = 7.92e5 laptop-hours per site,
1.58e6 for both. `zefoz-scripts/kill-logs/KILL-STATS.md` printed 7.93e5; corrected to 7.92e5.
The note's both-sites figure corrected from 1.6e6 to 1.58e6 in both twins.
Propagation grep (`7.93e5`): 0 remaining in tracked text, 0 in extracted PDF text.

**M-5. The literature-agreement bound was stated as ≤ 0.06 MHz.** The worst of the eighteen
agreeing entries is 0.0634 MHz at site 1 (8,13). Corrected to ≤ 0.07 MHz with the worst case
named, in both twins.

**M-6. The tamper battery's T2 case was described as a narrowed gradient enclosure.** T2 shifts
the enclosure — both endpoints, width preserved — so the recomputed one escapes. Corrected in
the note's battery description and in `zefoz-scripts/tamper_demo.py`'s docstring. The script's
executable logic is unchanged; only the docstring was wrong.
