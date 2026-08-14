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
`newell.py`). F2 is infrastructure, so the shipped checker carries the
mathematics rather than deferring to a hidden engine. It is NOT code-independent
of the generator: 212 of its 558 executable lines are verbatim from
`gen_demag.py`/`civ.py`/`newell.py`/`validate.py`.

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

## Documentation-correction round, 2026-08-13

The v0.14.0 round made three corrections to this part. All three were applied in the note and,
for the first, in a dated erratum footnote inside the note; none was recorded in this log, whose
only change this round was the date added to its title line. The Engine 2 gate of 2026-08-13
found the omission. No certificate, checker or certified value changed —
`demag-certificates/demag_certificate.json` is byte-identical to its released form.

**L-1. The anchor was described as "the 16 diagonal and off-diagonal values Donahue computed to
50 digits in Maple and recorded in `demagcoef.cc`".** That misdescribes the source: the
`demagcoef.cc` header carries a table of Nxx and Nxy check values, 31 rows, 24 of them nonzero.
16 is the size of the subset the certificate anchors against, not the size of the table.
Corrected in both twins, and a dated erratum footnote records the superseded wording verbatim.
The anchor set, the ≥ 49.6-digit agreement figure and the enclosures are unchanged.
Propagation grep (`16 diagonal and off-diagonal`): 1 site, the erratum footnote in `note.md`
quoting the superseded sentence, which is that footnote's purpose; the `.tex` twin carries the
same quotation with LaTeX math delimiters. The PDF carries both the corrected sentence and the
footnote. `demag-scripts/anchor_check.py`'s docstring was corrected to the same description.

**L-2. The permutation-identity remark asserted more than is tested.** It said the identities
hold among "the six components" because Nyy, Nzz, Nxz and Nyz are relabelings of the same f and
g evaluations. Nyz is carried nowhere in the table, so no identity involving it is tested.
Corrected in both twins to state the identities over the components the table actually carries,
naming Nyy, Nzz and Nxz, and to say so of Nyz explicitly.

**L-3. The coverage figure was unqualified.** The note gave 862 certified entries over "fifty
geometry-and-component pairs", which does not account for the origin. Re-derived from the
certificate rather than transcribed: `demag_certificate.json` carries 862 entries, of which 12
have `sep_cells == 0` — the self-terms, Nxx, Nyy and Nzz at each of four cells — and 850 lie
away from the origin across exactly 50 distinct (cell, direction, component) combinations.
850 + 12 = 862. Corrected in both twins to state that split.
Propagation grep (`fifty geometry-and-component pairs`): 0 remaining in tracked text.
(`a gold value cannot lie inside`, the absolute retired earlier in the round): 0 remaining.


## 2026-08-14 — independence-claim round (Part L, v0.15.0)

§5 clause (ii) and the trust paragraph were replaced by measured statements: 212 of
`check_demag.py`'s 558 executable lines appear in `gen_demag.py`, `civ.py`,
`newell.py` or `validate.py`, with 31- and 26-line byte-identical runs against
`newell.py`. The 16-row OOMMF/Maple anchor and the 862-entry consistency identities
are stated as what the result rests on, with their coverage named. `anchor_check.py`
imports `CIV` and `Newell` from the shipped checker, so it is the shipped arithmetic
checked against external values at 16 rows, never an independent re-derivation.
The README, the sweep record, this log and three comments in `check_demag.py` carry
the same correction. No enclosure, digit-loss figure or hash changed.
