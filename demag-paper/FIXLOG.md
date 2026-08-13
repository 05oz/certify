# Build-and-verification log — note-demag (Part L), 2026-08-12

Target: the certified Newell demagnetization-tensor reference table
(`demag-certificates/demag_certificate.json`), its standard-library checker
(`demag-certificates/check_demag.py`), the scripts
(`demag-scripts/anchor_check.py`, `tamper_demo.py`), and the note (`note.tex`,
`note.md`). This is the build/verification decision log; the dated novelty and
verification sweep is `SWEEP-RECORD-DEMAG-2026-08-12.md`.

The note claims exactly one thing: rigorous two-sided enclosures of the analytic
Newell tensor entries, plus a rigorous measurement of the double-precision and
asymptotic floating-point failures against those enclosures. No new tensor value
and no physical result is claimed; the Newell formulas and the pathology are
cited to their primary sources at point of use.

## Primary-source fidelity

- Newell f, g, self-demag and the 27-point stencils are transcribed from OOMMF
  `app/oxs/ext/demagcoef.cc` (`Oxs_Newell_f`, `Oxs_Newell_g`,
  `Oxs_SelfDemagNx`, `Oxs_CalculateNxx/Nxy`), pulled from the `fangohr/oommf`
  mirror. Every guard the code takes when an argument coordinate vanishes is
  mirrored. The `asinh` form quoted in the note equals the `log` form the code
  uses via `asinh(y/sqrt(x^2+z^2)) = (1/2) ln((y+R)^2/(x^2+z^2))`.
- The pathology statement (r^6 law, ~300-cell breakdown) is quoted verbatim
  from Chernyshenko-Fangohr S II.B (arXiv:1403.1978).
- The OOMMF asymptotic expansion is the `DemagNxxAsymptotic` powers-of-1/r form
  (through 1/r^6) from Fangohr's `demagderiv` reverse-engineering, with mu0
  dropped (the tensor is dimensionless). Sign/scale validated against the
  enclosure: leading term at cube on-axis n=100 is -1/(2 pi 10^6) = -1.5915e-7,
  matching the certified midpoint.

## Verification (independent, this build)

- ANCHOR: the demagcoef.cc header table of Maple 50-digit check values has 31
  rows (24 of them nonzero); the 16 of those rows we anchor against all
  agree with the recomputed enclosure midpoints to >= 49.6 digits
  (`anchor_check.py`, exercising the shipped checker's own Newell/interval code).
- INDEPENDENT CROSSCHECK (build only, not shipped): an independent mpmath 220-dps
  evaluation of the same Newell formulas lies inside every enclosure of the
  table (0 containment failures); the trace identity Nxx+Nyy+Nzz encloses 0 at
  all 136 mutual points where the three diagonals are present, and the self-term
  sum encloses 1 at all 4 cells. The checker re-tests both identities from the
  certified endpoints on every run.
- CHECKER: `check_demag.py` re-derives every enclosure independently, verifies
  containment of its own rigorous interval inside the certified one (pinning
  N_lo <= N_true <= N_hi), recomputes the naive double bit-for-bit, and
  recomputes every digit-loss bracket. Full run over all 862 entries: CHECK PASS.
- TAMPER: `tamper_demo.py`, six controls, all rejected nonzero -- enclosure
  narrowed to exclude truth and enclosure shifted (caught by the enclosure
  re-derivation), enclosure grossly widened (width sanity), corrupted naive
  double (float re-derivation), altered digit-loss claim (digit re-derivation),
  falsified hash (hash) -- with the hash recomputed to match in the enclosure
  cases so the mathematical layer is the one that fires.

## Decisions

- **S1 (precision).** Working precision PREC = 256 bits (~77 decimal digits).
  Rationale: at the worst point of the regime (cube on-axis Nxx, n=10^4) the
  cancellation costs ~r^6 = 10^24 ~ 2^80 bits of working precision, leaving a
  relative enclosure width ~2^{80-256} ~ 2e-54 there -- tens of digits tighter
  than double precision, which has zero (indeed negative) correct digits at that
  separation. 256 is comfortably above the pre-registered kill threshold and
  keeps the checker tractable.
- **S2 (verification predicate).** The checker verifies that its own
  independently re-derived rigorous interval [c_lo, c_hi] lies inside the
  certified [N_lo, N_hi] (which pins N_true in [N_lo, N_hi]), plus a
  width-sanity bound, rather than demanding bit-identical endpoints. This is the
  mathematically correct statement (a valid, tight enclosure) and is robust to
  incidental implementation differences, while still rejecting narrowing,
  shifting, and gross widening.
- **S3 (digit-loss metric).** "Correct significant digits" of a floating-point
  value are reported as a RIGOROUS bracket derived from the enclosure:
  -log10(rel_err) with rel_err two-sidedly bounded using the enclosure's
  endpoints. When the float lies outside the enclosure (the pathological
  regime), the bound is finite and is the reported number; a value with
  <= 0 correct digits is one whose relative error is >= 1.
- **S4 (anchor test precision, corrected).** `anchor_check.py` initially tested
  CONTAINMENT of the 50-digit gold values in the recomputed enclosures; this is
  wrong -- the enclosures are ~77 digits tight, far tighter than the 50-digit
  gold, so a nonzero gold value lies outside. Corrected to test AGREEMENT to the
  gold's own precision (>= 48 digits). The enclosures' rigor is established
  separately by the two-sided-bound construction, not by the anchor.
- **S5 (symmetry zeros excluded).** Entries whose certified midpoint is below
  1e-25 in magnitude (e.g. Nxx on the body diagonal of a cube, which is
  identically zero) are dropped: they carry no pathology signal and would make
  the relative-error metric ill-defined.
- **S6 (self-demag included).** The r=0 diagonal self-terms are carried as
  certified reference constants (cube = 1/3 exactly; film/rod factors to working
  precision; each cell's three diagonals sum to 1). They have no cancellation
  pathology but are the single most-used demag numbers.

## IP boundary

Public (staged): `demag_certificate.json`, `check_demag.py`, `anchor_check.py`,
`tamper_demo.py`, the note. PRIVATE (method repo, not staged): the generator
`gen_demag.py`, and the interval/Newell engine it imports (`civ.py`,
`newell.py`). F2 is infrastructure, so the shipped checker is by design close to
a full independent reimplementation of the math -- there is little hidden engine,
and maximal reproducibility is the point. The checker shares no code with the
generator.

## KILL/LIVE

Pre-registered kill condition: DEAD if enclosures cannot be made tighter than
double precision anywhere in the regime of interest. NOT triggered. Enclosures
are tighter than double precision everywhere in the regime and tens of digits
tighter where double precision fails outright. **LIVE.**

## E1 — erratum release v0.12.1 (2026-08-12, post-release)

Decision S4 corrected the containment claim to an agreement claim in the anchor CODE
(anchor_check.py) but the correction was never propagated to the prose: note.tex:233,
note.md:61 and SWEEP-RECORD-DEMAG line 17 all shipped in v0.12.0 still asserting the 16
Maple gold values "lie inside" the enclosures. False: the enclosures are ~77 digits
tight; direct test shows 15 of 16 gold values lie outside (the exact zero is the
exception). Caught 2026-08-12 by an outbound-email fact-check that re-executed
anchor_check.py and read S4 — i.e., at the last gate before external harm, but after
release. The 49.6-digit agreement figure and every certified enclosure are unaffected.
Fixed in v0.12.1 with a dated erratum footnote in both note twins; sweep record
corrected in-place with annotation. Root cause and the resulting PROTOCOL §14
(claim-correction propagation gate) are recorded in the program PROTOCOL.
