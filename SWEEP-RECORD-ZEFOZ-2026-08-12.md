# Dated novelty and verification sweep — certified ZEFOZ brackets, 167Er3+:Y2SiO5 (Part M)

Searches run 2026-08-12 (arXiv + web), same day as every "first" phrasing in the
note. This record is the priority-and-replay provenance for the ZEFOZ note
(`zefoz-paper/`) and the released Part M artifacts (`zefoz-certificates/`,
`zefoz-scripts/`), v0.13.0.

## Primary sources, read at the relevant sections and quoted verbatim

* **Matsuura, Yasui, Kaji, Sasakura, Tawara, Adachi**, "Exploration of optimal
  hyperfine transitions for spin-wave storage in 167Er3+:Y2SiO5,"
  arXiv:2412.10126. Local full copies of v1 (2024-12-13) and v3 (2025-11-14)
  read in full; v2 (2025-02-12) Appendix B fetched and inspected 2026-08-12.
  Version of record: **Phys. Rev. B 113, 085421 (published 2026-02-17)**,
  corresponding to v3. Decisive passages:
  - Hamiltonian (Eq. 2): H = I.A.S + I.Q.I + muB B.g_e.S − muN g_n B.I,
    g_n = −0.1618; A, Q, g_e "reported recently by S-J. Wang et al. [40]"
    = J. Lumin. 262, 119935 (2023), reproduced in Appendix B Table 2.
  - Non-exhaustiveness admitted in v3 Appendix D (local copy line 687):
    "because the total number of ZEFOZ points found depends on the initial
    grid conditions, the initial magnetic fields for the search were
    established by combining the three conditions below" (grid
    {±5,±15,±25}^3 mT plus two 1-D ray searches).
  - Errata basis: v1 site-1 Q prints Q23=Q32=+15.5 (local v1 text lines
    510–511); v2 also prints +15.5 (arXiv HTML v2 Appendix B, fetched
    2026-08-12); v3 prints −15.5 (local v3 text lines 566–567). v3 Table 5
    site-1 rows (6,7) 745.8 MHz and (4,7) 2216.2 MHz (local v3 lines
    991–1003). v3 site-2 bullet: B_(D1,D2,b) = (∓378.9, ±73.2, ∓502.3) mT
    against B_(B,θ,φ) = (633.52 mT, ∓37.5383°, −10.9417°) (lines 277–285) —
    mutually inconsistent sign pairing.
* **S.-J. Wang, Y.-H. Chen, J. J. Longdell, X. Zhang**, J. Lumin. 262, 119935
  (2023): source of the A, Q, g_e matrices. Cited as the parameter provenance;
  the certificate rationalizes the Appendix-B reprint of these matrices.

## Novelty sweep (2026-08-12), queries and outcomes

1. "certified ZEFOZ points interval arithmetic rare-earth spin Hamiltonian
   rigorous eigenvalue bounds" — nearest hits are generic verified eigensolver
   work: **symveig**, arXiv:2606.16217 (2026-06-15; abstract + scope read:
   "rigorous, machine-checkable enclosures of all eigenvalues of a Hermitian
   matrix, with an optional symmetry-sector decomposition" — fixed matrices
   only, no parametric derivatives, no stationary points, no ZEFOZ); a 2011
   interval eigendecomposition method (arXiv:1112.5052); verified
   Rayleigh–Ritz (arXiv:2110.01822). None touches ZEFOZ/clock-transition
   tables or eigenvalue-difference stationary points.
2. '"ZEFOZ" clock transition enumeration completeness erbium Y2SiO5 2026' —
   returns the Matsuura paper itself (PRB 113, 085421), the Er:CaWO4 ZEFOZ
   measurement stream (arXiv:2601.16362), Yb/Eu ZEFOZ experiments. All
   experimental or uncertified numerics; no completeness objects, no bounds.
3. "interval Newton Krawczyk stationary points parametric eigenvalue problem
   verified computation avoided crossing" — generic interval
   equilibrium/bifurcation certification (arXiv:2608.07071, 2608.07119) and
   Krawczyk surface certification (arXiv:2602.07718); parametric-eigenvalue
   Taylor/Chebyshev tracking (SIMAX 10.1137/23M1551961) is uncertified. No
   application to spin-Hamiltonian transition-frequency stationary points.
4. "rigorous certified bounds hyperfine transition frequency curvature T2
   second-order Zeeman verified" — spectroscopy and clock-shift assessment
   literature; nothing certified in the interval/machine-checkable sense.
5. arXiv listing of 2412.10126 re-checked 2026-08-12: three versions, no v4;
   no citing work with certified content found via the searches above.

## Novelty verdict

The intersection the note occupies — certified (two-sided, exact-rational,
stdlib-re-checkable) gradient bounds, Hessian-spectrum brackets with signs,
and Krawczyk existence/uniqueness boxes at the ZEFOZ points of a rare-earth
spin Hamiltonian, an exact symbolic time-reversal certificate for zero-field
stationarity, and a measured certified-cost assessment of ZEFOZ completeness —
is unoccupied. **Verdict: PRIORITY-CLEAN / NOVEL as a certified object.**
The ZEFOZ concept (Fraval–Sellars–Longdell 2004), the atlas and its physics
(Matsuura et al.), the parameter matrices (Wang et al. 2023), and every
mathematical tool (Sylvester inertia, Davis–Kahan, Hellmann–Feynman,
perturbation sums, Ostrowski, Krawczyk, Kato-type resolvent bounds, verified
numerics per Rump) are prior art, credited at point of use. Claim wording in
the note is application-first ("we find no prior certified treatment of ...").

## Verification summary (this build, 2026-08-12)

* Pilot re-verification (before building on it): `zefoz_checker.py
  certificate.json` (pilot, 22 points, 352 eigenvalue brackets) — exit 0,
  "CERTIFICATE VERIFIED", 46.5 s; three-item pilot tamper battery (corrupted
  inertia count, shifted bracket, invalid sqrt enclosure) all rejected exit 1;
  independent mpmath 60-digit diagonalization: 352/352 brackets contain the
  recomputed eigenvalues, worst containment margin 1.0e-6 MHz.
* Part M certificate: `zefoz_checker2.py certificate2.json` — exit 0,
  "CERTIFICATE VERIFIED", 38.5 s, CPython 3.14, stdlib only. 23 objects:
  time-reversal identity (exact symbolic check over Q[sqrt d]); 2 zero-field
  points (simple spectra certified; Hessian brackets for the 10 published
  Table-4 pairs); 20 Krawczyk points (gradient bound <= 3.2e-37 MHz/mT,
  Hessian eigenvalue bracket width <= 2.1e-15 MHz/mT^2 over the twenty
  (worst 2.009e-15; the highlighted site-2 (14,15) brackets are the narrowest
  at 2.51e-16), signatures certified, contraction ratio <= 0.096 at radius
  2^-45 mT).
* Tamper battery (6 items + control): `tamper_demo.py` — control passes exit
  0; T1 shifted Hessian bracket, T2 shifted gradient enclosure, T3 corrupted
  inertia count, T4 flipped time-reversal sign, T5 understated gradient-norm
  bound, T6 inflated Krawczyk radius — each rejected exit 1.
* Anchor: `anchor_check.py` (mpmath, independent code path) — every certified
  eigenvalue bracket of both certificates contains the 60-digit recomputed
  eigenvalue; zero containment failures.
* Kill condition K2 (pre-registered in the program's target dossier): FIRED.
  Measured certified-exclusion statistics (memory-capped queued jobs, logs in
  `zefoz-scripts/kill-logs/`) give a strict lower bound above 7.9e5
  laptop-hours per site (above 1.58e6 for both sites) against the
  pre-registered 200-hour budget; the completeness claim is dead at laptop
  scale and the note says so plainly (note Section 4). Deliverable downgraded
  exactly as pre-registered: certified existence + curvature at the known
  points (this Part).

## Scope statement

No claim of priority over the physics or the parameters. The certificate is
unconditional about the mathematics of the printed model and silent about the
spectroscopy. The completeness negative is a measured-cost statement about the
single-level certified branch-and-bound route at laptop scale, not an
impossibility theorem.
