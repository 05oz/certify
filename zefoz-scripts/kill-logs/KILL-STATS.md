# Kill condition K2 — measured statistics (2026-08-12)

Pre-registration (program target dossier, F1, 2026-08-11): "K2 (cost, evaluated
at 20 laptop-hours of Phase 1): if box-exclusion statistics project > 200
laptop-hours to close the +-100 mT domain for all 120 pairs (e.g., pathological
near-degeneracy clustering) -> KILL the completeness claim; downgrade
deliverable to certified existence + curvature brackets at the known published
points only (still releasable, no longer the headline)."

Instrument: the private certified branch-and-bound exclusion engine
(single-level Davis-Kahan machinery; per box: Bauer-Fike eigenvalue brackets
with component counting, box-uniform gap bounds via the certified Lipschitz
constant D, eigenvector-drift sin-theta bounds, Hellmann-Feynman gradient
enclosures at the center, signed perturbation-sum Hessian sup-bounds over the
box, first-order exclusion test). All runs as memory-capped queued jobs
(jobrunner, --mem-mb 2500 --workers 1, 340-s budget per chunk, depth cap
r_min = 0.09 mT). Raw per-chunk logs: bnb_*.json in this directory.

## Single-box calibration (site 1, exact certified tests)

| center (mT) | box radius r (mT) | pairs excluded / 120 |
|---|---|---|
| (50,50,50) | 6.25       | 0   |
| (50,50,50) | 0.78125    | 0   |
| (50,50,50) | 0.09765625 | 87  |
| (6.25,6.25,6.25) | 0.09765625 | 68 |
| (50,50,50), pairs (0,1),(1,2) only | 0.048828125 | 0/2 |
| (50,50,50), pairs (0,1),(1,2) only | 0.0244140625 | 2/2 |

Per-box certified cost: 1.4-2.4 s (one diagonalization amortized over all
120 pairs). True (uncertified, float) scales at (50,50,50) site 1: generic
pair |grad f| ~ 200 MHz/mT; flattest pairs (0,1),(1,2): 0.10-0.16 MHz/mT with
true Hessian norms 6.7e-3-9.5e-3 MHz/mT^2. Site 2 flattest pairs at the same
center: (0,1),(14,15),(1,2),(13,14) at 0.14-0.19 MHz/mT -- the published clock
pairs are the flattest, i.e. the ones that force the deepest subdivision.

## Adaptive chunk campaign (six chunks, half-width 0.390625 mT each,
## volume 0.4768 mT^3 each, 340-s budget, r_min = 0.09 mT)

| site | chunk center (mT) | boxes | closed | surviving pairs | wall |
|---|---|---|---|---|---|
| 1 | generic (50,50,50) | 234 | 0 | 2 | 341 s |
| 1 | near-origin (1.2,1.2,1.2) | 176 | 0 | 32 | 340 s |
| 1 | far (87.5,62.5,37.5) | 177 | 153 | 0 | 340 s |
| 1 | near-axis (75,5,5) | 136 | 10 | 3 | 342 s |
| 2 | generic (50,50,50) | 251 | 218 | 0 | 340 s |
| 2 | near-origin (1.2,1.2,1.2) | 191 | 0 | 19 | 340 s |

Reading: every chunk exhausted its budget without completing its subdivision
tree. Where closure happens at all (far region), it happens only at the
r = 0.098 mT level; at the generic mid-domain center the flat pairs
(0,1),(1,2) survive r = 0.049 mT and exclude only at r = 0.024 mT; near the
origin a 32-pair web among quasi-doublet levels (zero-field splittings from
0.004 MHz site 1 / 0.16 MHz site 2) is unprocessable by per-level gap
machinery for r > gamma/(4 sqrt(3) D), D = 104 MHz/mT.

## Projection and verdict

Strict lower bound, most favorable reading: every chunk's certified cost per
volume exceeds its wall/volume rate because no chunk finished. The weakest
measured rate is 713 s per mT^3 (one site). Half domain after the
B -> -B symmetry: (200 mT)^3 / 2 = 4.0e6 mT^3. Hence

  projected cost  >  713 s/mT^3 * 4.0e6 mT^3 / 3600 s/h
                  =  7.92e+05 laptop-hours per site,
                  >  1.58e+06 laptop-hours for both sites,

before any refinement of the surviving pairs (which the mid-domain calibration
shows requires 2 further depth levels for the flattest pairs, and which the
near-origin web makes divergent for single-level machinery). The
pre-registered budget is 200 laptop-hours. The projection exceeds it by more
than three orders of magnitude.

VERDICT: K2 FIRED. The completeness claim over ||B||_inf <= 100 mT is dead at
laptop scale with single-level certified machinery. The released deliverable
is the pre-registered downgrade: certified existence + curvature at the known
published points (Part M certificate). The concrete open route is certified
two-dimensional cluster-projector enclosures (note, Question 7.1).

Total campaign wall clock: 34 min (six 340-s capped jobs + queue overhead);
peak memory per job < 40 MB against the 2500 MB cap.
