# Certified brackets at the published ZEFOZ points of ¹⁶⁷Er³⁺:Y₂SiO₅: existence, curvature, and the measured cost of a completeness certificate

**Daniel Kirtchakov** — Independent researcher (`05oz`), Half Ounce Research; no institutional affiliation. ORCID [0009-0009-5213-4098](https://orcid.org/0009-0009-5213-4098). daniel@halfounce.io · https://halfounce.io

*Draft of August 12, 2026. This is a faithful Markdown mirror of `note.tex`.*

> **Computation and authorship.** All model rationalization, interval-arithmetic implementation, certification, verification, and drafting in this work were produced by Claude (Anthropic), directed by the author, on a single Apple laptop. The public artifact is a certificate together with a checker that imports only the Python standard library and shares no code with the generator; the checker re-derives every claim from the certificate alone.

> **Prior-art record.** The primary sources — Matsuura et al. (arXiv:2412.10126 v1/v2/v3 = Phys. Rev. B 113, 085421 (2026)), Wang–Chen–Longdell–Zhang (J. Lumin. 262, 119935 (2023)) — were read at the relevant sections on 2026-08-11/12; passages quoted are verbatim. Novelty was swept 2026-08-12 against arXiv and the web; the dated record ships with the artifacts (`SWEEP-RECORD-ZEFOZ-2026-08-12.md`).

## Abstract

The magnetic-field points at which a hyperfine transition frequency of ¹⁶⁷Er³⁺:Y₂SiO₅ is stationary — the ZEFOZ (zero-first-order-Zeeman) points — set the predicted coherence times of a leading solid-state quantum-memory platform. The published atlas of these points (Matsuura et al., Phys. Rev. B **113**, 085421 (2026); arXiv:2412.10126) is produced by Newton iteration from finite grids of starting fields, and its authors state plainly that the number of points found depends on the initial grid. Two questions follow. First: do the published points survive rigorous scrutiny — does a true stationary point of the exact spin Hamiltonian provably exist near each tabulated field, and can its location, frequency, and curvature (the quantity that sets the predicted T₂) be pinned by two-sided bounds a skeptic can re-derive with a standard-library program? Second: can the published list be proven *complete* over an explicit field box at laptop scale? To the first question we give a full positive answer: for each of the twenty tabulated nonzero-field points of both crystallographic sites we certify, in exact rational arithmetic, eigenvalue and transition brackets of width 4e-10 MHz, a gradient-norm bound |∇f| ≤ 3.2e-37 MHz/mT at an exactly specified rational field, two-sided brackets on all three eigenvalues of the 3×3 frequency Hessian, its signature, and — by a Krawczyk contraction with a rigorous third-derivative bound — the existence and local uniqueness of an exact stationary point within 2.9e-14 mT of the stated field. The certified signatures show that none of the twenty published points is a local minimum of its transition frequency: thirteen are saddles and seven are local maxima. At zero field we certify exactly, by an explicit time-reversal identity, that all 120 transitions of both sites are stationary, with certified curvature brackets for the ten published zero-field pairs. To the second question the answer is a documented negative: a pre-registered kill condition for the completeness search fired. Certified branch-and-bound exclusion over the box ‖B‖∞ ≤ 100 mT, measured on stratified sample chunks, gives a strict lower bound above 1e6 laptop-hours against a pre-registered budget of 200; the obstruction — quasi-degenerate hyperfine doublets that force per-level spectral-gap machinery below its validity radius — is quantified. Three errata in the reference paper are recorded, with version history: a load-bearing sign error in a printed quadrupole matrix that stood for eleven months (v1, v2; corrected upstream in v3), two tabulated frequencies inconsistent with their own stationary points by 2.7 and 4.3 MHz (certified restatements given), and an inconsistent sign pairing in a printed field vector. The certificate and a standard-library checker are the public unit.

## 1. The question

A hyperfine transition of ¹⁶⁷Er³⁺ in Y₂SiO₅ has a frequency `f_ij(B) = λ_j(B) − λ_i(B)`, the difference of two eigenvalues of a 16×16 effective spin Hamiltonian depending on the applied field `B ∈ R³`. At a field where `∇f_ij(B) = 0` — a ZEFOZ point (Fraval–Sellars–Longdell 2004) — the transition is first-order insensitive to magnetic noise, and the residual dephasing is set by the 3×3 Hessian of `f_ij`. For ¹⁶⁷Er³⁺:Y₂SiO₅ — a rare-earth system combining a telecom-band optical interface with a nuclear spin — the atlas of ZEFOZ points and curvatures of Matsuura et al. is the design input for spin-wave storage proposals.

That atlas is numerical in an essential way: Newton iteration from finite grids, and the authors state the consequence themselves — "because the total number of ZEFOZ points found depends on the initial grid conditions, the initial magnetic fields for the search were established by combining the three conditions below" (App. D). No error bounds accompany the tabulated locations, frequencies, or curvatures; nothing excludes further points; and the printed inputs of the calculation carried a load-bearing sign error through two arXiv versions (Section 5).

**Question 1.** Near each published ZEFOZ field, does a stationary point of the *exact* transition frequency provably exist? Can its location, frequency, and Hessian spectrum be enclosed in machine-checkable two-sided brackets, with no trust in the software that produced them?

**Question 2.** Can the published list be proven *complete* — every stationary point of every one of the 120 transitions — over an explicit field box, at laptop scale?

Question 1 is answered in full (Theorems 3.1, 3.2). Question 2 carried a pre-registered kill condition, and the kill condition fired (Section 4). Both outcomes are results, and both are recorded with the same precision.

## 2. The model and its exact rationalization

    H(B) = I·A·S + I·Q·I + μ_B B·g·S − μ_N g_n B·I        (1)

S = 1/2, I = 7/2 (dimension 16), field in the optical frame (D₁,D₂,b); A, Q, g the site-dependent matrices printed in App. B of v3, attributed to Wang et al. (2023). Every printed entry is adopted exactly as a rational; μ_B/h = 13.996244936 MHz/mT, μ_N/h = 7.622593285e-3 MHz/mT (CODATA truncations as exact rationals), g_n = −0.1618; both sites. The only irrationalities are the ladder amplitudes √7, √12, √15, enclosed by rational intervals validated by squaring; all further arithmetic is exact rational rectangle-interval arithmetic with outward rounding. Every stated interval contains the corresponding true value of the exact spectrum of the exact matrix (1). (Whether (1) describes the physical crystal is a separate, experimental question; the certificate is unconditional about the mathematics and silent about the spectroscopy.)

## 3. Certified statements

### 3.1 Zero field

**Theorem 3.1 (exact zero-field stationarity).** With the signed permutation `M = R^(1/2) ⊗ R^(7/2)`, `R^(j)|j,m> = (−1)^(j−m)|j,−m>`, the identities `M conj(H0) M^T = H0` and `M conj(Z_k) M^T = −Z_k` (k = 1,2,3) hold **exactly**, over Q[√7,√12,√15], for both sites. Hence the spectrum of H(B) is even in B; with the certified simple zero-field spectra (disjoint brackets of width 2e-10 MHz) every level is analytic near B = 0 and `∇f_ij(0) = 0` exactly, for all 120 pairs, both sites.

This upgrades the folklore "at zero field all transitions are ZEFOZ" to a machine-checked identity. For the ten published zero-field pairs the certificate carries two-sided brackets on all three Hessian eigenvalues of `∇²f_ij(0)` (widths ≤ 2.1e-9 MHz/mT²); e.g. site 1 (7,9): {−11.9910…, +1.6899…e-4, +1.1300…}. The signatures are mixed: none of the ten is definite, so at zero field each of these frequencies is a saddle in B.

### 3.2 The twenty published nonzero-field points

**Theorem 3.2 (certified brackets, curvature, and existence).** For each of the twenty entries of v3 Table 5 (ten per site) there is an exactly specified rational field B\* (dyadic, denominator 2^120), within the rounding radius of the published coordinates, such that the certificate proves:

1. brackets of width 2e-10 MHz for all sixteen `λ_n(B*)`, hence width 4e-10 MHz for `f_ij(B*)`;
2. `|∇f_ij(B*)| ≤ 3.2e-37` MHz/mT;
3. two-sided brackets, width ≤ 2.1e-15 MHz/mT², for the three eigenvalues of `∇²f_ij(B*)`, with certified signs;
4. existence and uniqueness of a point B̂ with `∇f_ij(B̂) = 0` in the box `B* + [−r,r]³`, `r = 2^-45 mT ≈ 2.9e-14 mT` (Krawczyk contraction; worst ratio 0.096).

**Corollary 3.3 (certified stationary-point types).** None of the twenty published ZEFOZ points is a local minimum of its transition frequency. All ten site-1 points and site-2 (5,6), (5,7), (6,7) have certified signature (−,−,+) (saddles); the remaining seven site-2 points, including the optimal (14,15) transition, are local maxima (−,−,−).

For the site-2 (14,15) point singled out in the reference, the certified Hessian spectrum is {−1.65241e-4, −8.94878e-5, −1.44676e-6} MHz/mT² (brackets < 3e-16 wide) and the certified field is B̂ = (−378.9856, +73.2675, +502.3521) mT ± 2.9e-14 mT — which also settles item (E3) of Section 5. Every curvature number a proposal takes from the reference's T₂ model can now be taken with a proof.

### 3.3 Method, in brief

Eigenvalue brackets: interval LDLᵀ of `H(B*) − μI` at certified shifts; sign-definite pivots ⇒ Sylvester inertia. Eigenvectors: 70-digit candidates frozen as dyadic rationals (2^-170), certified a posteriori by exact residuals against certified gaps (Davis–Kahan sinθ ~ 1e-42). Gradients: Hellmann–Feynman on the enclosed vectors. Hessians: signed second-order perturbation sums with certified matrix elements and gaps; eigenvalues via Gershgorin discs after an approximate rotation with the exact Ostrowski congruence correction. Existence: the Krawczyk operator `K(X) = B* − C∇f(B*) + (I − C∇²f(X))[−r,r]³ ⊂ int X`, with the Hessian-over-box enclosure inflated entrywise by `9√3·M·r`, `M = 192 D³(γ_i^-2 + γ_j^-2)` a rigorous third-derivative bound proved in the appendix from a resolvent estimate and Cauchy coefficients. The margins are enormous (|∇f| ≲ 1e-37 against a needed ≲ 1e-18) because clock-transition flatness makes the test brutally stringent: the smallest certified |Hessian eigenvalue| is 5.67e-8 MHz/mT², the preconditioner norm reaches 1.8e7, and existence is provable only from candidates polished far beyond double precision.

### 3.4 Relation to the pilot certificate and prior tools

The same-program pilot (eigenvalue/transition brackets only) re-verifies: checker exit 0; 352 brackets contain an independent 60-digit diagonalization. Generic verified eigensolvers exist (symveig, arXiv:2606.16217; verified numerics per Rump), but we find no prior certified treatment of *parametric* eigenvalue-difference stationary points for spin Hamiltonians, and no certified object attached to any ZEFOZ table (novelty sweep 2026-08-12). Claims are application-first; every mathematical tool is classical and credited.

## 4. The completeness question: a pre-registered kill

Target (pre-registered): certify the published list complete over ‖B‖∞ ≤ 100 mT — all twenty published points lie *outside* this box (191 mT–5.3 T), so the claim would state that B = 0 is the only in-box stationary set. Kill condition K2 (pre-registered): if measured statistics project > 200 laptop-hours to close the domain, kill and downgrade to certified existence + curvature at the known points.

Engine: adaptive subdivision; per box, Bauer–Fike eigenvalue brackets at the center, per-level gap bounds over the box, Davis–Kahan eigenvector enclosures, certified Hellmann–Feynman gradients, signed perturbation-sum Hessian sup-bounds, first-order exclusion test; a box closes when all 120 pairs are excluded.

Measured (unambiguous): certified per-box cost 1.4–2.4 s. At box radius 6.25 and 0.78 mT, **zero** of 120 pairs excludable at a generic center — the certified Hessian sup-bounds, inflated by eigenvector drift ∝ rD/γ, dominate the certified gradients. First majority exclusions at r ≈ 0.1 mT (87/120 generic; 68/120 near-origin), with 33–52 pairs surviving. Six adaptive sample chunks (half-width 0.39 mT, both sites, stratified in radius, 340-s budgets):

| site | chunk center (mT) | boxes | closed | surviving pairs | wall |
|---|---|---|---|---|---|
| 1 | generic (50,50,50) | 234 | 0 | 2 | 341 s |
| 1 | near-origin (1.2,1.2,1.2) | 176 | 0 | 32 | 340 s |
| 1 | far (87.5,62.5,37.5) | 177 | 153 | 0 | 340 s |
| 1 | near-axis (75,5,5) | 136 | 10 | 3 | 342 s |
| 2 | generic (50,50,50) | 251 | 218 | 0 | 340 s |
| 2 | near-origin (1.2,1.2,1.2) | 191 | 0 | 19 | 340 s |

Closed boxes are finest-level (r = 0.098 mT) boxes with all 120 pairs excluded; surviving pairs are those still active at the depth cap. No chunk finished its tree; the weakest measured rate is 713 s/mT^3.

Every chunk exhausted its budget without finishing its subdivision tree, so the certified cost per closed volume strictly exceeds the measured wall/volume rate; the weakest chunk gives the strict lower bound > 7.9e+05 per site (> 1.6e+06 both sites) laptop-hours for both sites — more than three orders of magnitude over the 200-hour budget. **K2 fired; the completeness claim is dead at laptop scale**, and this note's certificate is the pre-registered downgrade.

The obstruction is structural, in two regimes. Near the origin, near-degenerate level pairs (certified splittings from 0.004 MHz at site 1, 0.16 MHz at site 2) make every per-level bound degrade as `rD/γ_n` (D ≈ 104 MHz/mT certified): a level in a quasi-doublet of splitting γ is processable only for `r ≲ γ/(4√3 D)`, i.e. boxes of 1e-5–5e-2 mT near the doublet-crossing set (a 32-pair web survives every near-origin box). At generic fields the levels are well split (≥ 715 MHz measured at (50,50,50)), but the flattest pairs — including the clock pairs themselves, e.g. site-1 (0,1) with true |∇f| ≈ 0.10 MHz/mT against ~200 MHz/mT for generic pairs — exclude only at r ≈ 0.024 mT, because the certified Hessian sup-bound over a box cannot see the cancellations that make clock-pair curvatures small. Closing the domain requires certified cluster-projector (block) enclosures or a different certification principle; with single-level machinery the cost diverges near the crossing set. We record this as the concrete engineering frontier, not an impossibility result.

## 5. Errata in the reference

- **(E1) Site-1 quadrupole sign, v1 and v2.** Appendix B of v1 (2024-12-13) and v2 (2025-02-12) prints site-1 `Q23 = Q32 = +15.5` MHz. With +15.5 the paper's own zero-field Table 4 is irreproducible (off by up to 68 MHz); with −15.5 it reproduces to ≤ 0.05 MHz. The paper's computations used −15.5 throughout; the printed table was wrong for eleven months. v3 (2025-11-14), matching the version of record (PRB 113, 085421), prints −15.5: corrected upstream — credited — and any reader who rationalized v1/v2 as printed inherited a wrong Hamiltonian.
- **(E2) Two tabulated frequencies inconsistent with their own points, v3.** Table 5, site 1: (6,7) tabulated 745.8 MHz, (4,7) tabulated 2216.2 MHz. Certified brackets at the stationary points nearest the stated coordinates (existence certified): `f_67 = 748.5431883 ± 2e-10` MHz, `f_47 = 2220.5387344 ± 2e-10` MHz — discrepancies −2.74 and −4.34 MHz, ~50× the table's rounding. No alternative level pair at those fields is both stationary and at the tabulated frequency; the other eighteen entries agree to ≤ 0.06 MHz. The two values appear stale.
- **(E3) Sign pairing of the highlighted site-2 field, v3.** The bullet prints `B_(D1,D2,b) = (∓378.9, ±73.2, ∓502.3)` mT alongside `B_(B,θ,φ) = (633.52 mT, ∓37.5383°, −10.9417°)`. These are inconsistent: the angles (upper signs) give (−379.0, +73.3, +502.3) mT, and the certified stationary point is at (−378.99, +73.27, +502.35) mT. The printed Cartesian pairing should read (∓, ±, ±).

(E1) verified against the v1, v2, v3 source files directly; (E2), (E3) against certified brackets. The version of record was not re-checked entry-by-entry beyond its Appendix B.

## 6. What is certified, what is enclosed, what is trusted

*Certified* (machine-checked from first principles by the stdlib checker): every claim of Theorems 3.1, 3.2 and Corollary 3.3, as inequalities among exact rationals. *Enclosed but pointing at published data:* the identification of certified points with rows of Table 5 is by proximity of the published rounded coordinates. *Trusted:* the Python `fractions`/`json`/`math` standard library; the classical theorems cited; nothing else — no floating point, no eigensolver, no code shared with the generator. The kill statistics of Section 4 are measurements of a private search engine, shipped as run logs, and are *not* part of the certified surface.

**The computation, in one paragraph.** Candidate fields and eigenvectors by Newton iteration and 70-digit diagonalization (mpmath), frozen as dyadic rationals; certification a separate exact-rational pass (outward rounding, denominator cap 2^200), ~4.6 s per point; the 23-object certificate (1.9 MB JSON) verifies in 39 s under `zefoz_checker2.py` (CPython 3.14, stdlib only; also passes on CPython 3.9.6), exit 0; the six-item tamper battery is rejected item-by-item (exit 1) and an untampered control passes; the pilot certificate re-verifies (47 s, exit 0) and its 352 brackets contain an independent 60-digit recomputation. Branch-and-bound measurements ran as memory-capped queued jobs (34 min wall-clock total); artifacts, checker, run logs, and the dated novelty sweep ship in the release; the search engine stays private per the program's certificate-plus-checker model.

## 7. Open questions

1. **Cluster-certified completeness.** Can ‖B‖∞ ≤ 100 mT be closed with certified two-dimensional doublet-projector enclosures (block perturbation sums, inter-cluster gaps only), and at what measured cost?
2. **Existence certificates from double precision.** The Krawczyk test at clock points needed candidates polished to 1e-40. Is there a certification principle — exploiting evenness in B, or analyticity — whose stringency does not scale with the inverse Hessian?
3. **The physical atlas.** Do measured second-order shifts at the site-2 (14,15) point distinguish the certified Hessian spectrum {−1.652e-4, −8.949e-5, −1.447e-6} MHz/mT² from the scalar |S₂| summaries in use?
4. **Which certified object does the experiment want next:** brackets at the |B| ≤ 3 T points, certified *optimality* of the (10,11)/(14,15) choices within the tabulated list, or completeness over the small ball |B| ≤ 25 mT actually swept by the published grids?

## Appendix A. A third-derivative bound from a resolvent estimate

**Lemma.** H Hermitian, λ simple with gap γ, V Hermitian with ‖V‖ ≤ D. For complex |t| < ρ := γ/(4D), H + tV has exactly one eigenvalue λ(t) within γ/2 of λ; λ(t) is analytic; |λ'''(0)| ≤ 192 D³/γ².

*Proof sketch (standard resolvent argument with constants tracked, cf. Kato).* On the circle Γ of radius γ/2 about λ, ‖(H−z)⁻¹‖ ≤ 2/γ, so the Neumann series of (H+tV−z)⁻¹ converges for |t| < ρ (‖tV(H−z)⁻¹‖ ≤ 1/2); the Riesz projection is analytic of rank 1; λ(t) = tr[(H+tV)P(t)] stays inside Γ. Cauchy estimates on |t| ↑ ρ give |a₃| ≤ (γ/2)/ρ³, so |λ'''(0)| = 6|a₃| ≤ 3γ(4D/γ)³ = 192 D³/γ². ∎

Applied along unit directions with box-uniform certified gaps, this gives `sup |∂³_e f_ij| ≤ M = 192 D³(γ̃_i^-2 + γ̃_j^-2)`; polarization of the trilinear form gives |T[a,b,c]| ≤ (8·27/48)M = 4.5M (the certificate uses the laxer 9M); integrating bounds each Hessian entry's variation over the box by 9√3·M·r — the entrywise inflation in the Krawczyk operator, recomputed by the checker from the certified D and gaps.

## References

As in `note.tex`: Matsuura et al. (arXiv:2412.10126; PRB 113, 085421 (2026)); Wang–Chen–Longdell–Zhang (J. Lumin. 262, 119935 (2023)); Fraval–Sellars–Longdell (PRL 92, 077601 (2004)); Zhong et al. (Nature 517, 177 (2015)); arXiv:2601.16362; arXiv:2606.15009; Davis–Kahan (SINUM 7, 1 (1970)); Krawczyk (Computing 4, 187 (1969)); Neumaier (1990); Horn–Johnson (2013), Thm 4.5.9; Kato (1980); Rump (Acta Numerica 19, 287 (2010)); symveig (arXiv:2606.16217).
