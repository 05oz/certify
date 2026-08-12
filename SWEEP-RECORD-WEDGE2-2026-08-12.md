# Novelty sweep — Part K (wedge2): exact certified logical error probability via syndrome-space transforms

Date: 2026-08-12. Scope: the specific claim of the v2 note — an EXACT (not
bracketed, not estimated) logical error probability of a stated decoder on a
circuit-level detector error model, computed by syndrome-space character sums
(Walsh–Hadamard transforms) in exact rational arithmetic, shipped as a
machine-checkable certificate re-verifiable by a Python-standard-library
checker; plus the full decoder-specific uncorrectable weight spectrum `A_w`
(all weights at once) by the same transform.

Queries run (web, 2026-08-12): exact logical error rate surface code
Walsh-Hadamard transform syndrome space; exact computation logical error
probability QEC Fourier transform detector error model; Darmawan Poulin tensor
network exact logical error rate; "logical error rate" exact rational
certificate verified checker; coset leader weight enumerator exact probability
decoding error MacWilliams; "detector error model" Walsh / character sum /
coset decoder-specific weight enumerator certified 2026.

## Nearest neighbors found, and why none is this object

1. **Classical coset-leader weight enumerators** (textbook material; e.g.
   Jurrius–Pellikaan, *Codes, arrangements and weight enumerators*, and
   standard coding-theory references). The probability of correct syndrome
   decoding of a linear code on a q-ary symmetric channel is classically
   computed from the coset-leader weight enumerator; MacWilliams-type
   transforms are the standard tool. This is the correct classical lineage for
   the method and the note cites it as such. It is not this object: single
   symmetric channel parameter (i.i.d. p), code coordinates = error positions
   (m = n), no observable bit, no heterogeneous dyadic mechanism
   probabilities, no circuit-level DEM, and no machine-checkable certificate
   whose exact rational value an independent stdlib checker re-derives.
2. **Tensor-network exact maximum-likelihood decoding** (Bravyi–Suchara–Vargo
   arXiv:1405.4883; Darmawan–Poulin arXiv:1607.06460). "Numerically exact"
   contraction of coset probabilities for surface codes, used for ML decoding
   and threshold studies; floating-point, code-capacity/phenomenological
   focus, no exact rational output, no certificate, no independent checker.
3. **Estimator lineage** (Mullan–Weippert–Brown arXiv:2607.27153;
   Bravyi–Vargo arXiv:1308.6270): sub-threshold sampling estimators; a value
   with an error bar, not an exact value, not certified.
4. **Analytic approximations** (Regev et al. arXiv:2605.03054;
   Forlivesi–Valentini–Chiani arXiv:2305.01301 / Quantum 9, 1950 (2025)):
   closed-form or MacWilliams-enumerator approximations/bounds; the
   enumerators are code-level (undetectable errors), not decoder-specific
   uncorrectable counts; approximations valid in asymptotic windows; no
   certificate.
5. **DEM estimation via Walsh–Hadamard relations** (arXiv:2512.10814,
   *Estimating Detector Error Models on Google's Willow* — WHT relates
   detector parities to DEM parameters for estimation; arXiv:2606.16288,
   *Reconstruction of detector error model* — hypergraph reconstruction from
   syndrome statistics). Both ESTIMATE the DEM from data; neither computes an
   exact decoder logical error probability, and neither certifies anything.
   Abstract-level checks 2026-08-12 confirm no exact-P_L or certification
   content.
6. **Formal verifiers** (Lean-QEC arXiv:2605.16523; Veri-QEC
   arXiv:2504.07732): machine-checked distance / error-correction conditions,
   Boolean properties — not probabilities.
7. **Part H itself** (this program, doi:10.5281/zenodo.21895825): the
   two-sided rational bracket this note supersedes; its §6/Q7.1 asked for
   exactly this object ("a locality-exploiting exact convolution ... that a
   standard-library checker can re-verify").

## Verdict

No prior work found that computes and CERTIFIES the exact rational logical
error probability of a stated decoder on a circuit-level detector error model
(nor the full decoder-specific uncorrectable spectrum by transform), with
independent standard-library re-verification. The transform technique itself
is a MacWilliams-type character sum and is classical in lineage — the note
says so and claims only the intersection: exact decoder-specific object +
circuit-level DEM + exact rational arithmetic + replayable certificate.
"First" phrasing is restricted to that intersection, qualified by "no prior
work found" and the classical-lineage acknowledgement.
