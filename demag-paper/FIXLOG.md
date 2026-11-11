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
- [Superseded 2026-11-10 by decision L-4 below: the form described next is the three-term
  truncation of the demagderiv notebook, which is K. M. Lebecki's (the line credits Fangohr);
  OOMMF's demagcoef.cc carries four terms.] The OOMMF asymptotic expansion is the `DemagNxxAsymptotic` powers-of-1/r form
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


## 2026-11-10: asymptotic-form correction and remainder-bound addendum (Part L, v0.17.0)

Prompted by a re-read of OOMMF's own source in November, while preparing a reply to its author.
No certified enclosure, digit-loss bracket or hash of `demag_certificate.json` changed; that file
is byte-identical to its released form. Every number below was re-derived for this entry.

**L-4. The three-term asymptotic form was called "OOMMF's asymptotic expansion".** It is the form
of the demagderiv notebook (K. M. Lebecki, 2012, in the ovf2mfm repository of Boardman, Lebecki and
Fangohr, `bitbucket.org/fangohr/ovf2mfm`, commit 494b363f7edb), whose functions `nXXfunNoncubic` and `nXYfunNoncubic` carry `term3`, `term5` and
`term7` only and whose introduction says it follows `oommf12a4pre-20100909`. Every
`app/oxs/ext/demagcoef.cc` on the public mirror `github.com/fangohr/oommf`, read at 1.2a5bis (commit
17ef69411f6c), 1.2a6 (commit 2a310acc9bd7) and the tags for 1.2b0, 2.0a0, 2.0a1, 2.0a2, 2.0a3,
2.0b0 and 2.1a0, also carries `term9`
(coefficients c1..c15 over 192 for Nxx, c1..c10 over 64 for Nxy), with the comment that the error
is of order 1/R^11; the order is fixed through 2.0a1 and is the default of `asymptotic_order` from
2.0a2, where `FindKnotSchedule` also begins to set the switching radii from assumed error and speed
models.
The asymptotic section of `demagcoef.cc` was not read in August (decision record above, "Primary-
source fidelity"). Corrected in both twins: the abstract, §3 ("line for line" now limited to the
analytic routines), the Table 1 caption and a new four-term column, the crossover paragraph of §4,
§6, and Questions 7.1 and 7.2, and the prior-art note (above the abstract in the Markdown twin; carried into the LaTeX twin
and the PDF at the release gate, L-9),
each with a dated correction note (the Table 1 caption gained its own note at the release gate,
L-9; §6 needed only the clause on the field name, since its old text did not name OOMMF). Also corrected: the README entry, the August sweep record (dated note), the docstring of
`check_demag.py` (no executable line changed; the file has no published hash anywhere in the
repository, checked by searching for its digest), and the metadata text of the new six-cell
certificate (not part of its hashed entry list). Not changed: the `formulas` text and the field
name `asymp_oommf` of the released `demag_certificate.json`, which would break its record; both
are explained in the note (§6) and in CORRECTIONS.md.
Propagation grep (`OOMMF's asymptotic`, `OOMMF asymptotic`, `DemagNxxAsymptotic`, `through
1/r^6`, `order-1/r^6`): remaining sites are the dated correction notes that quote the old
wording, the August line of this log (marked superseded), the August sweep record's line (followed
by its correction note), the unchanged metadata of `demag_certificate.json` (disclosed, L-9), and
the new §8 sentence that OOMMF's asymptotic order is n (accurate).

**L-5. Equation (1) carried a leading minus sign.** Copied from Chernyshenko and Fangohr, eq. (2).
With one gradient in each integration variable, the double integral in (1) with that minus sign
gives Nxx > 0 for two cells in line along x, the opposite of the certified values and of OOMMF
(Nxx = -1.59155e-7 at n = 100 for the cube, matching -1/(2 pi 10^6)). The certified values were
always computed from Newell's closed form with OOMMF's sign. Corrected in both twins with a dated
note. The `formulas.tensor_def` text of the released `demag_certificate.json` carries the same
superseded sign; it is left unchanged so that the record stays byte-identical, and the note and
CORRECTIONS.md say so (added at the release gate, L-9). The six-cell certificate's text is
corrected.

**L-6. New result: Theorem 8.1, a bound on the asymptotic truncation error.** Statement, proof and
tests are in §8. The series (6) and its first four terms are attributed to Donahue (HMM-2007 talk;
`demagcoef.cc`); our exact derivation (`demag-scripts/series_terms.py`) reproduces OOMMF's integers
for Nxx (18, 60, 150) and Nxy (9, 36, 100). Independent checks before release, each by an agent
that did not write the proof: a blind re-derivation of the series by a different route (binomial
expansion and direct integration over both boxes), equal to ours coefficient by coefficient through
`term13` for all six components; an adversarial proof referee (verdict: correct after repairs, which were
applied: the 1/k! of the Taylor term, the parity and moment steps written out, the hypotheses
listed, the citation of the norm theorem made more precise; the release gate asked for three
further repairs to the proof's wording, recorded in L-9, and later rounds for more, recorded in
L-10 and L-11); a second referee on the stated form. Test
of exactly the stated forms, replayable: `check_remainder_bound.py` on `demag_certificate.json`
(776 entries with r > D) and on `demag_certificate_six_cells.json` (1,162), n = 5, 7, 9, 11, no
failure, largest ratio 0.833 (shape-free, n = 5, elongated cell along z at 10,000 cells); the
moment inequality holds for all six cells. Not replayable from this repository: 2,759 random
cases certified with the private interval engine, no violation, largest ratio 0.99997 (needle
1 : 1/300 : 1/300 along its axis). Prior art: `SWEEP-RECORD-DEMAG-BOUND-2026-11-10.md`.

**L-7. Second certificate.** `demag-certificates/demag_certificate_six_cells.json`: 1,310 entries,
entries_sha256 42caa5e6883d625e24d5ebe236e4aba01a3231502cacfe9beacf4667c1207bf4, computed on
2026-08-14 with the same generator and grid. Its 862 entries for the four original cells are
identical, field by field, to those of `demag_certificate.json` (checked 2026-11-10); 448 entries
are new, for the cells (1, 1, 1/10) and (1, 1.3, 1/10). `check_demag.py` (full run, 1,310
entries): CHECK PASS, trace encloses 0 at 204/204 mutual points, self-terms enclose 1 at 6/6.
Its metadata text, outside the hashed entry list, was edited in this round: `formulas.source`
(the asymptotic value is the three-term truncation of the demagderiv notebook), and at the
release gate `formulas.tensor_def` (no leading minus), `formulas.stencil` (written as the
corrected (4)) and `method.transcendentals` (Machin's formula, written for pi). entries_sha256
recomputed from the entries after the edit: unchanged. No digest of the whole file is published.

**L-8. Table 1, four-term column.** `demag-scripts/four_term_digits.py` evaluates the series
truncated after three and four terms in IEEE-754 double and brackets their correct digits against
the certified enclosure. The three-term column of Table 1 is the certificate's stored value,
unchanged; where the script's own three-term evaluation sits at the double-precision floor it can
differ from the stored value by about a digit (n = 300: 15.9 against the stored 17.2), because the
last digit there depends on the order of the floating-point operations. The caption says so.

**L-9. Release gate, round 1 (2026-11-10), and the repairs.** Four agents that did not write this
round read the candidate against its sources: a mechanical check (FAIL, three small fixes), a
correction check (NOT READY, text only), an addendum check (PASS with minor corrections) and a
referee (PUBLISH AFTER CHANGES). No finding touched a certified value, a hash or Theorem 8.1.
Each repair below was checked against the source named before it was made.
- Equation (4) had no leading minus sign. With the standard second difference its operator gives
  weights +1, -2, +4, -8 (corners, edges, faces, centre), the opposite of the weights printed with
  it, which are OOMMF's (`Oxs_CalculateNxx`: -1, +2, -4, +8, divided by 4 pi dx dy dz) and which
  the certified values use (a gate agent reproduced 16 certified midpoints from the printed
  weights). Fixed in both twins, with the second difference defined and a dated note.
- Certificate metadata (see L-5 and L-7): released certificate unchanged and disclosed in the
  note (§2, §6) and CORRECTIONS.md; six-cell certificate corrected outside its hashed entries.
- §2: "Machin's 4 atan(1/5) - atan(1/239)" is pi/4; now pi = 4(4 atan(1/5) - atan(1/239)).
- §1 and §4: since 2.0a2 `demagcoef.h` makes `OXS_DEMAG_REAL_ANALYTIC` the double-double type
  `Xp_DoubleDouble` (a long-double stand-in exists only for STANDALONE builds). Before 2.0a2 the
  precision depends on release and platform (gate round 2, L-10, checked in the sources): 1.2a6
  to 2.0a1 take the 27-point differences in `OC_REALWIDE` arrays (`ComputeD6f` in `demag.cc`),
  a type the platform file sets (long double for g++ in `config/platforms/linux-x86_64.tcl`,
  double in `darwin.tcl` and for Visual C++ in `windows-x86_64.tcl`); 1.2a5bis stores each f and
  g value in a double scratch array (`OXS_FFT_REAL_TYPE`, `fft3v.h`) and differences it there.
  Both sentences now date the double-double evaluation and give the earlier precision as double
  or long double.
- §3: "independent re-verification" replaced; the checker is not code-independent (§5).
- §5: clause (iii) said bit for bit; since v0.16.0 (commit fb02971) the default is a relative
  1e-4, with `--strict-naive` for the bit-exact gate. The tamper control on the naive value sets
  it to 0.999 and is still rejected. Line numbers are now those of the shipped file, read off it:
  393 to 509 (naive-double block), 663 to 691 (consistency identities and their report), 545 to
  549 and 580 to 581 (serialisation and hash). The counts (212 of 558) stay those of v0.15.0 and
  are labelled so; the shipped file has 568 executable lines. The checker's docstring says the
  same, with its line count kept fixed so these numbers hold.
- §6: the checker uses `asymp_oommf` only in the entry hash (`canonical_line`, check_demag.py
  line 548) and to recompute its digit bracket (lines 648 to 654); a gate agent multiplied one
  entry's value by 1.5, recomputed digits and hash, and the checker passed. §6
  now says that the checker does not recompute the stored value, and names `four_term_digits.py`
  as the script that recomputes the truncation.
- Table 1 caption (draft wording: "Beyond about 100 cells both truncations sit at the
  double-precision floor") and §4 (released wording: "beyond a few tens of cells"): for the cube
  of Table 1 the floor is reached near 100 cells for four terms (16.7 digits at 100) and near
  300 for three (13.1 at 100, 14.9 at 200, 17.2 at 300); for the film (1, 1, 1/4) along its
  normal, near 500 and 2,000 (`four_term_digits.py`; added at gate round 2, L-10).
- Abstract and README: MuMax3 computes the kernel "by brute-force integration of magnetic
  charges" (`mag/demagkernel.go`), so it does not evaluate Newell's closed form. The first
  sentence now says which codes do what, without the list of other codes.
- §8: the convergence step is argued by analyticity in t (the zeros of |r + t u|^2 have modulus
  r/|u|); the norm identity is cited to Banach 1938, Satz I (read on the Studia Mathematica scan,
  p. 38), with Kellogg 1928, Theorem IV, named as a gradient bound from which it follows by
  induction; the needle statement is a limit, with continuity after division by V; notation
  clashes removed (phi for the kernel, l for the derivative order, s for the half order, Q for the
  grid denominator of §2, delta^2 for the second difference, n declared a truncation order, V
  tied to |sigma|); S_n declared the exact truncated series, rounding error excluded; the test
  counts stated as nested (1,162 including 776); the classical multipole estimate credited
  (Greengard and Rokhlin 1987, a two-dimensional paper, so the note calls the argument the
  three-dimensional form of their estimate; checked on Crossref and zbMATH 0629.65005); Donahue and Porter's MMM 2019 poster cited
  for the error model (title, poster number and date from Donahue's talks page); OOMMF's model
  coefficient for the cube, 4 pi/5, printed beside the true 99/64 (largest over directions and
  components, checked by a scan of T_11 over directions with `series_terms.py`: Nxx 99/64 with
  offset along x and -99/128 along y or z, off-diagonal maximum 0.916) and the bounds 162 and 1122/35; "proved rather than assumed"
  and two other contrast sentences removed.
- README and .zenodo.json: "every odd truncation order n >= 3" (for even n the stated bound
  fails), and "attained in the limit of a thin needle".
- References: [Bjork2023] is article 171245, doi:10.1016/j.jmmm.2023.171245 (Crossref; the title
  was also garbled in the LaTeX twin); [demagderiv] is by K. M. Lebecki (the notebook's own line:
  "Written by Kristof M. Lebecki, 2012, Universitat Konstanz"), in the ovf2mfm repository of
  Boardman, Lebecki and Fangohr, commit 494b363f7edb.
- Bookkeeping: Questions 7.1 and 7.2 notes dated; the Table 1 caption carries its own note; the
  PDF now carries the Markdown twin's authorship statement and prior-art record; the Markdown
  header no longer lists sections; the README layout index says the bound is tested on entries
  with r > D; the README's import-scan sentence covers the two new scripts (scanned 2026-11-10);
  CITATION.cff identifier descriptions use colons, and Part A's identifier is labelled v0.1.1
  (Zenodo record 21799112 is v0.1.1; v0.1.2 is 21831894, listed separately); the August sweep
  record's notes name the notebook's author and the v0.15.0 line count.

Not changed, by decision: the dated August records keep their text and gain dated notes only; the
release dates in .zenodo.json and CITATION.cff stay 2026-11-10 until the release day is known.

**L-10. Release gate, round 2 (2026-11-10).** Three reviewers that did not write the repairs
(fix verification, mathematics, sources) found no blocking defect and nothing touching a
certified value, a hash or Theorem 8.1. The fix-verification reviewer found all 39 round-1
items repaired; the mathematics and sources reviewers found five of them only partly repaired
(items 28, 29, 31, 34 and 36), and the repairs below complete them. Repairs, each
checked against the file or source named:
- CORRECTIONS.md item 4 had listed two errors that existed only in the round-1 draft (a floor
  sentence in the Table 1 caption; a three-author [demagderiv] reference, which v0.16.0 did not
  have) and missed the released one: this log (August line), the August sweep record and the
  released certificate's `formulas.source` credit the demagderiv notebook to Fangohr. Rewritten,
  and the August notes in this log and in the sweep record now name Lebecki.
- OOMMF before 2.0a2 (L-9 had "long double by default"): double or long double by release and
  platform, as now recorded in L-9 and stated in note §1 and §4.
- §4: the floor sentence is tied to Table 1, and the film's later floor is given.
- `.zenodo.json`: equation (4) is described as the note describes it, a form whose second
  difference was undefined and which needs a leading minus sign under the standard one.
- §8: the moment constants are called mu (c was also an exponent index), each coordinate of u is
  named (u_a reused a as a label), and the derivative order l is tied to k; Greengard and
  Rokhlin 1987 is two-dimensional, so the argument is called the three-dimensional form of their
  estimate; "Nxx along an axis" is now "Nxx with offset along x, or any diagonal component along
  its own axis" (along y or z the cube's Nxx coefficient is -99/128).
- §2: the sentence after (4) now attaches the stencil weights to (4) with its leading minus sign
  (the weights of the triple second difference alone are +1, -2, +4, -8).
- Writing rule: contrast sentences removed from the note (§4, §8 twice), the docstrings of
  `check_remainder_bound.py` and `check_demag.py` (line count kept, so the line numbers of note
  §5 still hold), CORRECTIONS.md, the bound sweep record (the point-source sentence) and this
  log.
- Records: the August sweep record gained dated notes on [Bjork2023] and on its "independent"
  wording; the bound sweep record no longer says the 2.1a3 User's Guide describes the same scheme
  (the record cited no source for it; the round-2 sources reviewer found it true); L-4 now says
  where the prior-art note sits in each twin; `check_remainder_bound.py`'s docstring states odd n >= 3; CITATION.cff's
  message labels Part A v0.1.1 and names the v0.1.2 erratum.

**L-11. Release gate, round 3 (2026-11-10).** Two reviewers that did not write the repairs (fix
verification; a fresh expert reading as OOMMF's author or a journal referee would) found no
blocking or moderate defect and no sentence unfair to OOMMF or its authors. The
fix-verification reviewer found all 24 round-2 defects repaired. The second reviewer re-derived
the proof step by step and found it correct, found one round-2 defect (sources-0) only partly
repaired, since the [OOMMF] reference did not yet name `demagcoef.h` and the platform files,
and found statements about OOMMF and the demagderiv notebook in §1, §4, §8, Question 7.1 and
[demagderiv] incomplete or not supported by the source cited. The repairs below cover these. Repairs, each checked against the
source named:
- OOMMF's `FindKnotSchedule` chooses its radii from assumed error and speed models (its comment:
  "built-in assumptions about analytic, asymptotic, and refined asymptotic method errors and
  speed"; `analytic_speed_factor` = 60). Note §4, §8 and Question 7.1, CORRECTIONS item 1, the
  README, .zenodo.json, the bound sweep record and L-4 of this log now say "error and speed
  models"; Question 7.1
  now asks whether radii with certified error bounds can be supplied to such a schedule.
- §1: Chernyshenko and Fangohr describe one switching radius, 32 cells by default; the schedule of radii is 2.0a2's and is cited to
  [OOMMF], whose file list now names `demagcoef.h`, `fft3v.h` and `config/platforms/*.tcl`, on
  which the precision statements rest (paths checked on the mirror at the 1.2a5bis commit).
- [demagderiv]: the notebook transcribes the asymptotic tensor from OOMMF's 2010 code ("taken
  from the OOMMF code") and differentiates it for the MFM signal; "deriving" replaced.
- §6 and README: `four_term_digits.py` recomputes the three-term truncation and does not read
  the stored value. §6 now says both; the README says that it recomputes the truncation behind
  the stored value.
- "Every cell shape" (abstract, Question 7.2, Theorem 8.1, the bound sweep record) now reads "every rectangular cell" or
  "all edges"; the moment step uses the box's triangular law.
- Notation: the direction r-hat in (6) (the Markdown twin printed r/r); the six-cell
  certificate's `formulas.source` sentence on the field name reworded (entries_sha256
  recomputed after the edit: unchanged); `series_terms.py` docstring reworded.
- Typesetting: the LaTeX preamble lets the gap above footnotes shrink by up to 3 pt, which
  removes a 1.8 pt overfull page that the longer §1 produced; the PDF builds with no overfull box.
- Bookkeeping: L-6, L-9 (the checker also hashes `asymp_oommf`) and L-10 corrected;
  CORRECTIONS.md's opening paragraph says which records keep their text, and its table lists the
  prior-art record and decisions L-4 to L-11.
