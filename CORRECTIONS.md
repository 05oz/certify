# CORRECTIONS: v0.18.0 correction round

Written 2026-11-17, with additions of 2026-11-25 (items 1, 5 and 7). This round corrects statements in
Parts A, B, D, E, G, H, I, J and K, changes one checker in Part B, and removes local paths from the
logs of Parts B, E, G and N.

**No certified value changed.** One checker's logic changed: `qec-scripts/check_lower.py` gained the
guard that its audit proposed (finding D4), and every Part B lower-bound certificate whose proof ships
with the repository passes the changed checker. Every other script edited in this round changed in its docstring only:
`k34-scripts/verify_chain.py`, `k34-scripts/make_structured.py`, `k34-scripts/audit_multiset.py` and
`k34add-scripts/blowup_bound.py` (none of the five has a published digest anywhere in the repository; checked). In the notes, each
corrected statement carries a dated note, most of the form "(Correction, 2026-11-17: ...)", with
"Updated", "Addition", "Later work" or "Noted" for updates and additions; the removal of Part
A's draft-only header, which made no claim, is recorded in its LaTeX header comment and in
paper/FIXLOG.md (A-2); dated records
(FIXLOGs, sweep records, referee and verdict records) keep their text and gain a bracketed dated note.
Each part's FIXLOG has a section "Correction round, 2026-11-17" with one decision per corrected claim
and its propagation grep. The PDFs of the nine changed notes were rebuilt and checked by text
extraction.

1. **Part G (k(3,4) = 21).** §5.2 said that no lower bound for k(6,3) beyond 24 appears in the
   literature. The literature stated 18, and one-line assemblies of known graphs give 26 (IRW's W₂₂
   with a disjoint directed 3-cycle); the bound 29 of the note exceeds that by 3. Found in our own
   records (a record of 2026-10-20, a review of 2026-11-11). §8.3 gave k(4,4) ≥ 21 where W ⊔ QR₇
   gives 28 (same records). The note did not credit the first arXiv version of Ihringer,
   Rajendraprasad and Weinert (2017), which states r(I₃,L₄) ≤ 24 and remarks that the largest
   {I₃,L₄}-free Cayley graph has 20 vertices, so k(3,4) ≥ 21; pointed out by the reviewers at
   erdosproblemaday.com on 2026-11-16 (our own sweep of 2026-10-14 had recorded it, and the note
   was not corrected then). Nor did it mention the working report of Erdős Problem a Day on
   problem 112 (dated 2026-08-12, initial run 2026-07-26), which exhibits a 20-vertex circulant
   witness and states 21 ≤ k(3,4) ≤ 25 (found by the referee of this round). Four overstatements
   about the checking of the certificates, found by our own record check of 2026-11-17, made to
   answer a question from the
   reviewers at erdosproblemaday.com: the header said the referee had no access to the
   pipeline's code; "twelve" certificates re-checked by a second checker were ten ledger certificates
   and two small ones; that checker, called "unrelated", is ours, written in the same campaign; "11 of
   11" regeneration attempts were nine on record. The note now states that no established LRAT checker
   ran in August, a deviation from the program's own rule for certificates, and that drat-trim's
   `lrat-check` accepted 30 ledger certificates on 2026-11-17; the weakness of `lrat-check` on an
   unsupported empty clause is credited to X. Zeng. Addition of 2026-11-25: on 2026-11-18 the
   reviewers at erdosproblemaday.com completed a rebuild and check of the whole certificate chain
   from commit 4794560. By their record, all 445 formulas regenerate to the ledger's `cnf_sha256`,
   and cake_lpr, which the record describes as an LRAT checker with a soundness proof in the HOL4
   theorem prover, accepted a proof of each, made with their own build of CaDiCaL 3.0.1; 307 of
   those proofs equal the ledger's in SHA-256 and size. The check is theirs and was not repeated by
   us; the note states it in §7 (item 1) and cites their record.
   The regeneration inputs, whose absence from the
   public tree the reviewers at erdosproblemaday.com pointed out on 2026-11-16, were added by commit
   4794560 and are described, and "70 representatives" is corrected to 72 (found by our own
   regeneration work of 2026-11-17). Question 8.1 is answered
   in part by the circulant Cay(ℤ₂₀,{2,4,5,7,11,14}), which appears in the working report of Erdős
   Problem a Day on problem 112 and in Muhamadiev Faridun's repository of 22 September 2026, and
   which the reviewers at erdosproblemaday.com pointed out to us. Later work is credited: T. S.
   Orden's 30 ≤ k(6,3) ≤ 32, Muhamadiev Faridun's k(4,4) ≥ 34 and k(3,5) ≥ 31, and the
   k(4,4) ≥ 40 and k(3,5) ≥ 43 of the repository rsvaultpudgy-create/erdos-112-lower-bounds. The
   header of `verify_chain.py` no longer calls it independent (found by our own regeneration work
   of 2026-11-17). Build log: `k34-paper/FIXLOG.md`, G-5 to G-18.
2. **Part J (the extremal graph for k(3,4) is not unique).** §6 posed as open a question the circulant
   answers; "the algebraic route falls short" and "the picture at (3,4) is the opposite" are corrected;
   the conclusion that the extremal family is substantially non-algebraic is withdrawn; the prior-art
   record called IRW the only paper on r(I_m,L_n) (Bermond 1974 and Larson and Mitchell 1997 are
   others) and the count "a fortiori new". The description of the Zenodo record of v0.10.0 said that no
   20-vertex extremal graph is vertex-transitive; it was corrected on 2026-11-17, and the note now
   states the same facts. Found by the reviewers at erdosproblemaday.com (2026-11-16) and our own
   records. Build log: `k34add-paper/FIXLOG.md`, J-3 to J-7.
3. **Part E (CFR(5,25)).** H.-Y. Song's 2000 paper, described as unread, has been read in full; it
   gives the same lower bound 4 for n = 25. The Handbook table the note compares with is out of date at
   n = 33, 35 and 39, so exceeding it is not by itself evidence of novelty; the difference-matrix check
   and its unread sources are stated. The sweep record's "F_c(25) = 4" and "independent
   standard-library checkers" are corrected. Found by the release gate of 2026-08-14 and a review of
   2026-11-11 (Song, the table), and by this round's propagation grep. Build log: `cfr-paper/FIXLOG.md`,
   E-1 to E-5.
4. **Part D ([[14,3,5]]).** An addition: the SDP bounds of G. Anglès Munné and F. Huber
   (arXiv:2603.19901, March 2026) on the same family are cited; they do not exclude [[14,3,5]]. Found
   by a review of 2026-11-11. Build log: `qec1435-paper/FIXLOG.md`, D-3.
5. **Part B (code distances).** The Lean-QEC repository (Ehatamm, Lee, Wu and Tao) has held a formal
   statement of 18 ≤ d for [[288,12,18]] since June 2026, with four unproved lemmas; the word "first"
   is withdrawn wherever Part B used it, and the difference is stated. Addition of 2026-11-25:
   PROVENANCE.md (row 20) and the August sweep record called Part B's bound of 2026-08-04 "the only
   machine-checkable lower bound on record" for this code; each now carries a dated note that names
   the Lean file (found by a release gate of this program). d = 24 for [[360,12]] has since
   been reported by G. Lee's bicycle-race database, by Crocker, by Daugherty, Ryan and Ward, by
   tropidist (B. Cheng, N. Guo and F. Pan) and by QEDist (J. Y. Lee); credited, and Part B's certified
   d ≥ 16 stands. Addition of 2026-11-25, from our reading of the first four of these sources (what
   was read is in `paper/FIXLOG-qec.md`, B-2): by their manuscript, the certificates that Daugherty,
   Ryan and Ward ship prove 19 ≤ d ≤ 24 for this code, a lower bound above Part B's 16, and their
   exact value 24 comes from an exhaustive enumeration and not from a shipped certificate (their
   certificates were not replayed for this correction); Crocker's record defines the same
   parity-check matrices as Part B's checker builds; and the reference [CCKF26] of the note gave
   D. Kremer's initial as F. Correction of 2026-11-25: since its update of 2026-08-06 Part B said
   that no lower bound of any kind had been reported for [[360,12]]. At least two were on record.
   Chen, Jafari and Lai (arXiv:2606.12445, May 2026) ran their solvers on this code too: all 46
   configurations time out, with d ≥ 11 the best lower bound reached, solver-asserted as for
   [[288,12,18]]. And a theorem of Symons, Rajput and Browne (arXiv:2511.13560, November 2025)
   gives d ≥ 6 for it as a 5-fold cover of [[72,12,6]]. The sentence is withdrawn wherever Part B
   had it, and §6.4 of the note states both bounds; the certified d ≥ 16 is above both. The audit's finding D4
   is fixed in `check_lower.py`, and its line counts are updated. "A separate agent instance that was
   given no access to the pipeline" is narrowed to what the audit's report shows (found by this
   round's propagation grep). Found by our own
   reviews of 2026-11-17 and 2026-11-11, our own reading of 2026-11-25 and the
   Part B audit (D4). Build log: `paper/FIXLOG-qec.md`, B-1 to B-8.
6. **Parts H and K.** At the notes' own operating points a 10⁷-shot Monte Carlo run resolves the
   logical error probability, to about 12 percent either side at d = 5, p = 10⁻³; what the
   certificate adds there is exactness. The statement that the regime is inaccessible to direct Monte
   Carlo is Mullan, Weippert and Brown's, concerns the low error rates needed for utility-scale
   computation, and stays attributed to them. Found by our own reading of 2026-11-17. Both
   notes also cited the Lean-QEC paper (arXiv:2605.16523) with wrong initials and a wrong title;
   corrected (found by the referee of this round). Build logs: `wedge-paper/FIXLOG.md`, W-3 and W-4;
   `wedge2-paper/FIXLOG.md`, K-5 and K-6.
7. **Part I (Kelmans).** The two Python certificate checkers share their 3-connectivity routine, which
   the n = 22 verdict had disclosed but the note and README had not carried; the claim that the two C
   pipelines share no code was never measured and is now stated as untested. Found by the site
   independence audit of 2026-11-10. Addition of 2026-11-25: §3.4 of the note still said that every
   load-bearing check of the referee used code sharing nothing with the search pipeline; it now
   carries a dated note (found by a release gate of this program). Build log:
   `kelmans-paper/FIXLOG.md`, I-2 and I-3.
8. **Part A.** The public preprint no longer says "DRAFT ONLY, not for circulation". Found by the
   organization audit of 2026-11-11. Build log: `paper/FIXLOG.md`, A-2.
9. **Front matter.** README: a parts index A to N with versions, DOIs and dates of record; the
   v0.14.0 and v0.15.0 DOIs; one line on the byte-identical second Zenodo record of v0.2.1
   (10.5281/zenodo.21832017; cite 10.5281/zenodo.21831995); the lead no longer counts two bodies of
   work; Parts E and F have headings; the layout lists this file and `SWEEP-RECORD-2026-08-05.md`.
   PROVENANCE.md counts fourteen parts. CITATION.cff names v0.2.1 for Part B and v0.17.0 for Part L.
   Found by the organization audit of 2026-11-11.

## Local paths and the login name

Through v0.17.0, 82 lines in 11 files named folders of the author's computer or the author's login
name: 66 lines with absolute paths in seven files (five logs of Part N, `cfr-paper/FIXLOG.md` and
`paper/FIXLOG-qec.md`), 7 lines in `colorcode-dcirc-certificates/logs/2026-09-01/ilp_anchor.log` and 1
line in `k34-paper/REFEREE-k63.md` with the path of a temporary session folder, and 8 lines (six of
`colorcode-dcirc-certificates/VERIFY.log`, two of `colorcode-dcirc-paper/FIXLOG.md`) that used the
login name as a word. Each was replaced in place by this rule, applied in order, to those 11 files
only; no line was added or removed, and every other byte is as written:

- R1. The path of the research folder in the author's home folder, up to and including its trailing
  slash, becomes `[archive]/`.
- R2. The same path where the log writer cut it at the space in the folder's name, at the end of a
  line, becomes `[archive]`.
- R3. The path of the research archive on the author's external drive, up to and including its
  trailing slash, becomes `[archive]/`. (The folder of R1 holds links into this archive.)
- R4. The path of a temporary session folder, up to and including `scratchpad/`, becomes `[scratch]/`.
- R5. An elided form of such a path (`.../scratchpad/`) becomes `[scratch]/`.
- R6. The login name used as a word becomes `[author]`.

`colorcode-dcirc-certificates/SHA256SUMS` carries the new digests of the seven changed files of that
directory and of its README, which records the same rule; lines 798 and 799 of `VERIFY.log` quote two
digests from before the redaction and are kept as a dated record. Releases up to v0.17.0 keep the old
text under their DOIs. The organization audit of 2026-11-11 recorded the home-folder path and the
session path in these files and proposed no action; a release gate of this program found them as a
defect on 2026-11-17 (the paths), and this round's propagation grep found the elided session path
and the login name.

## Statements this round did not check

- Parts C and I say that their adversarial referee was "a separate agent instance" given "no
  access" to the pipeline's code (`tt3-paper/note`, `kelmans-paper/note`), and Part D that its
  re-verification was made by "a separate agent instance" (`qec1435-paper/note`). Parts G and B made
  the same statement; the records read for them (for Part B, the audit's report only) did not
  support it, so both were narrowed in this round; the records of Parts C, D and I were not checked.
  Untested, not refuted.
- Part J attributes the uniqueness of the 7-vertex TT₄-free tournament to Sánchez-Flores (1998); that
  paper is not in our corpus. Unverified.
- Part L's README calls `anchor_check.py` an independent anchor, Part M's README does the same for its
  `anchor_check.py`, and Part N's README says one program "shares no code with either"; none was
  re-measured in this round.

## Text of earlier releases that this round cannot change

The metadata deposited with earlier releases keeps wording that this round or an earlier one
corrected in the repository. The descriptions or titles deposited with v0.2.1 (both records,
10.5281/zenodo.21831995 and 10.5281/zenodo.21832017) call d([[288,12,18]]) = 18 "the first
machine-checkable determination" and 16 ≤ d "a first lower bound" for [[360,12,≤24]]; v0.5.0 says
that Song's 2000 paper could not be accessed and names its journal as Discrete Applied Mathematics
(it is Comput. Math. Appl. 39 (2000)); v0.7.0 gives "11/11 attempts" and the prior bounds
9 ≤ k(3,4) ≤ 25; v0.9.0's title says "two independent pipelines"; v0.10.0's title says
"independently verified"; v0.15.0's title says that every "shares no code" sentence in the corpus
was measured, and its description that the Part H bracket was re-derived by an independent route
at all five certificates (the whole bracket was re-derived at d = 3 only). The body of the GitHub
release v0.10.0 says that QR₇ appears in every extremal graph (the note proves it only for graphs
with a vertex of seven non-neighbours; its Question 6.1 is open) and that blow-up constructions
reach only 15 vertices (they reach 14, giving k(3,4) ≥ 15). Where these differ from the repository,
the repository and this file are the record. The Zenodo description of v0.10.0 was corrected on
2026-11-17 (Part J above).

## Files changed

Regenerate with `git diff --name-status v0.17.0`; that list also holds the 77 files of commit 4794560
(the Part G regeneration inputs of 2026-11-17), which no earlier release carries.

---

# CORRECTIONS: v0.17.0 Part L round

Dated 2026-11-10. This round corrects Part L and adds a result to it.

**No certified enclosure, digit-loss bracket or checker logic changed.**
`demag-certificates/demag_certificate.json` is byte-identical to its released form, and
`check_demag.py` changed only in its docstring. The statements below were wrong. In the
note and the README each is corrected in place, and each correction in the note's text
carries a dated note; the dated August records (the August line of `demag-paper/FIXLOG.md` and
`SWEEP-RECORD-DEMAG-2026-08-12.md`) keep their text and gain dated notes, and the released
certificate keeps its text (see below). The [Bjork2023] fix and the editorial changes
(notation, wording) are recorded in the build log.

1. The note, its README entry and its certificate called a three-term asymptotic form
   (terms in 1/r^3, 1/r^5, 1/r^7) "OOMMF's asymptotic expansion". That form comes from
   the demagderiv notebook (K. M. Lebecki, 2012, in the ovf2mfm repository of Boardman,
   Lebecki and Fangohr), which follows a 2010 pre-release of OOMMF. OOMMF's `demagcoef.cc`
   carries a fourth term in every version on the public mirror of its releases, from
   1.2a5bis to 2.1a0, and since 2.0a2 chooses its switching radii from assumed error and
   speed models. The three-term digit counts are correct for that truncation and are unchanged.
2. Equation (1) of the note carried a leading minus sign copied from a cited source. With
   one gradient in each integration variable that sign gives the opposite of the certified
   values, which were always computed with the correct sign.
3. Equation (4), the stencil, had no leading minus sign and did not define its second
   difference. Read with the standard second difference, it gave the opposite of the
   stencil weights printed with it. The weights, which are OOMMF's and which the certified
   values use, are unchanged.
4. Smaller statements. §1 did not date OOMMF's double-double evaluation (since 2.0a2;
   earlier releases take the differences in double or long double, depending on the
   release and the platform). §2 printed Machin's formula for pi/4 as pi. §3 called the
   checker's re-verification independent. §4 placed the asymptotic double-precision floor
   "beyond a few tens of cells"; for the cube of Table 1 it is about 100 cells for four
   terms and 300 for three, and later for some other cells. §5 said the naive double is
   recomputed bit for bit (since v0.16.0 that is the `--strict-naive` mode; the default is
   a relative 1e-4) and gave line numbers of the v0.15.0 checker. §6 said the checker
   re-derives all of the record; it does not recompute the stored asymptotic value. The
   abstract counted MuMax3, which integrates numerically, among codes using Newell's
   closed form. The reference [Bjork2023] gave article number 171235 (it is 171245). The
   build log, the August sweep record and the certificate's `formulas.source` credited the
   demagderiv notebook to Fangohr; it is K. M. Lebecki's (2012), in the ovf2mfm repository
   of Boardman, Lebecki and Fangohr.

What is left as released. The released certificate keeps its metadata text so that the
record stays byte-identical: the field name `asymp_oommf` and the `formulas.source` text
(items 1 and 4), the minus sign in `formulas.tensor_def` (item 2), the form in `formulas.stencil`
(item 3) and the Machin expression in `method.transcendentals` (item 4). The note
supersedes each of these texts; no value they describe changed. The new six-cell
certificate carries the corrected texts, outside its hashed entry list.

The added result is §8 of the note: a proven bound on the truncation error of the
asymptotic series, with its checker `demag-scripts/check_remainder_bound.py`, the series
generator `demag-scripts/series_terms.py`, and a second certificate,
`demag_certificate_six_cells.json`, which adds two thin-film cells.

| Part | Version | Note | Places corrected | Build log |
|---|---|---|---|---|
| L | v0.12.x | [`demag-paper/note.pdf`](demag-paper/note.pdf) | abstract, prior-art record (dated note), §1, equations (1) and (4), §2 (Machin), §3, Table 1 caption, §4 crossover paragraph, §5, §6, Questions 7.1 and 7.2, reference [Bjork2023]; the PDF now also carries the authorship statement and prior-art record of the Markdown twin | [`demag-paper/FIXLOG.md`](demag-paper/FIXLOG.md), decisions L-4 to L-11 |

The rebuilt PDF was checked by text extraction. The deposit is
versioned: the v0.12.x to v0.16.0 records keep resolving to the text with the old
wording, and the concept DOI resolves forward to this version.

---

# CORRECTIONS — v0.15.0 independence-claim round

Dated 2026-08-14. This round changed documentation only.

**No certified value changed, and no checker's verification logic changed.** An
independence audit found that a set of public sentences asserting a checker shares no
code with the pipeline that produced its certificate are false as written. Each has
been replaced by a measured statement of what is shared, what independence survives,
and what a passing check may and may not be read as. Every checker passes as before,
every tamper battery passes as before, and every mathematical result of Parts A
through M stands. Two independence backstops that did not previously exist were
established before this round was written and are stated in the notes.

This file is an index, not a record. The measured counts and the reasoning behind each
replacement live in each part's note and build log, which are the places they are checked.

## Deposited documents whose text changed

| Part | Version | Note | Sentences replaced | Build log |
|---|---|---|---|---|
| A | v0.1.x | [`paper/ERRATUM-v0.1.2.md`](paper/ERRATUM-v0.1.2.md) (not the deposited PDF) | 2 (§3, and the closing note under the run block) | [`paper/FIXLOG.md`](paper/FIXLOG.md) |
| B | v0.2.x | [`paper/preprint-qec-distances.pdf`](paper/preprint-qec-distances.pdf) | 2 (§4.1 the fourth checker; front matter) | [`paper/FIXLOG-qec.md`](paper/FIXLOG-qec.md) |
| D | v0.4.0 | [`qec1435-paper/note.pdf`](qec1435-paper/note.pdf) | 1 (§5, the independent verifier) + one SHA-256 manifest line | [`qec1435-paper/FIXLOG.md`](qec1435-paper/FIXLOG.md) |
| E | v0.5.0 | [`cfr-paper/note.pdf`](cfr-paper/note.pdf) | 2 (§3, and the abstract/trusted-base "independently written" clause; the §1 search claim is true and untouched) | [`cfr-paper/FIXLOG.md`](cfr-paper/FIXLOG.md) |
| H | v0.8.0 | [`wedge-paper/note.pdf`](wedge-paper/note.pdf) | 1 (front-matter methods note) | [`wedge-paper/FIXLOG.md`](wedge-paper/FIXLOG.md) |
| J | v0.10.0 | [`k34add-paper/note.pdf`](k34add-paper/note.pdf) | 4 (front matter and the artifacts section; located by content, not line) | [`k34add-paper/FIXLOG.md`](k34add-paper/FIXLOG.md) |
| K | v0.11.0 | [`wedge2-paper/note.pdf`](wedge2-paper/note.pdf) | 1 (front-matter methods note) | [`wedge2-paper/FIXLOG.md`](wedge2-paper/FIXLOG.md) |
| L | v0.12.x | [`demag-paper/note.pdf`](demag-paper/note.pdf) | 2 (§5, clause (ii) and the trust paragraph) | [`demag-paper/FIXLOG.md`](demag-paper/FIXLOG.md) |
| M | v0.13.0 | [`zefoz-paper/note.pdf`](zefoz-paper/note.pdf) | 1 (§6, the trusted list) | [`zefoz-paper/FIXLOG.md`](zefoz-paper/FIXLOG.md) |

**PDF rebuild complete, 2026-08-14.** All eight deposited PDFs — B, D, E, H, J, K, L and
M above — were rebuilt from their corrected `.tex` with `tectonic` 0.17.0 (`pdflatex`,
`xelatex` and `latexmk` are absent from this machine) and each was verified by
`pdftotext -layout` extraction, never by timestamp: for every one of the eight, none of
the sentences this round set out to replace survives into the rebuilt text, and every
replacement sentence is present. The extraction check was run de-hyphenated and on token
boundaries, because a crude match reports both false survivors and false absences on
these documents. That check tests the sentences the round had already identified; it
cannot find a false claim the round never flagged, and the adversarial referee pass found
two of those in Parts B and E after the first rebuild. Both are fixed and both papers
were rebuilt again; see the section below. Part A's
`paper/preprint-dixmier-poisson.pdf` is not in that list: its text was left unchanged
(see the flagged item below), and it was deliberately not rebuilt.

Three of the eight would not compile at all on first attempt: `wedge-paper`,
`wedge2-paper` and `k34add-paper` had acquired a `\par` inside the non-`\long` `\thanks`
argument when this round's replacement paragraphs were written, which halts XeTeX with a
runaway-argument error. The nine occurrences were changed to `\endgraf`, which produces
the identical paragraph break without the token that trips the runaway check. No word of
prose changed.

The Markdown mirrors, the drafts tree, `README.md`, the demag sweep record, the k34add
sweep record and certificate README, and the affected checker docstrings carry the same
corrections; they are not deposited separately.

**The deposit is versioned.** The v0.14.0 DOI keeps resolving to the text containing the
false sentences. This correction lands as a new version with the concept DOI resolving
forward. No existing record was edited in place.

## One checker file changed, and its published hash with it

`qec1435-scripts/verify_1435.py` had its docstring corrected (the disclosure required by
Part D). Its SHA-256 is published in that paper's own manifest, so the manifest line was
updated in the same pass: `2527266d13b604029120ed11174730ef1ed3fe6d5405d8fe3f82c21668ae0d3c`
becomes `6e23299bf878165ecef94044efa3e2cf180c5ece4ca60665c7af6d04f237a1b2`. Only the
docstring changed; no executable line of that file was touched. Every other checker edited
in this round (`check_demag.py`, `zefoz_checker_pilot.py`, `check_prof.py`, `check_lower.py`,
`qec_lib.py`, the three k34add checkers, `fibre_check.py`) has no published hash anywhere in
the repository, verified by searching for each file's digest before editing.

That last sentence was true of the eight checkers it names and false of the round as a
whole. Two files edited earlier in the batch, `kelmans-scripts/refcert.py` and
`kelmans-scripts/verify_cert.py`, **do** have published digests, in the integrity block of
`kelmans-certificates/REGENERATE.md`, and both were stale. A reader re-hashing the shipped
scripts against that block would have found a mismatch and been entitled to read it as
tampering. Both lines were updated and all sixteen digests in that block re-verified
against the files they name. `REGENERATE.md` is inside a `*-certificates/` directory and
so is otherwise read-only for this round; the two-line change is recorded here because it
is an exception, and because the alternative was shipping a manifest that contradicts its
own artifacts.

## Caught by the pre-release battery, after the corrections were drafted

The Engine 2 re-derivation pass re-executed every measured figure in this round rather
than re-reading it, and three of the round's own replacement sentences did not survive it.
All three are fixed above and in the FIXLOGs; none changes a certified value.

- **Part E.** The replacement said the longest identical run between the two CFR verifiers
  "is seven lines and is pure input/output". Measured, the longest identical run is five
  lines and is the header of the distinctness double loop; the longest purely
  input/output run is three. A round correcting false independence claims had written a
  false measurement into the correction itself.
- **Part D.** The §5 disclosure landed, but the front-matter `\thanks` of the same paper
  still read "independently written checker code that shares nothing with the generating
  pipeline" — so the paper's own §5 refuted its own front matter, which is the §14 failure
  mode this protocol exists to prevent. The front matter now records the dependence and
  points at §5. Separately, that paper's FIXLOG recorded the new `verify_1435.py` digest
  as `3471eacf...`, which is not the file's SHA-256; `note.tex`, `note.md` and this file
  had the correct `6e23299b...` and the FIXLOG was the lone wrong copy.
- **Part B.** The sentence introducing the new third LRAT acceptance was itself written as
  an independence claim — "a third acceptance that shares nothing with either" — and is
  false on the same measurement: 34 of that replay's 239 executable lines appear in
  `check_lower.py` or `check_prof.py`. It now states the measurement. The shared lines are
  bare `continue`/`break`/`else:`, flag initialisations, the main guard and a three-line
  gzip-open idiom, so the substance stands; the wording did not.

## Caught by the adversarial referee, after the first rebuild

A referee session that did no editing was then given a kill-the-paper brief (PROTOCOL
§17). It re-derived the round's measurements independently and reproduced all of them,
and it found four further defects that every earlier pass had missed. Parts B and E were
rebuilt a second time.

- **Part B, four stale line counts.** The trusted-base section says "Four files, 1,128
  lines of Python in total: `check_witness.py` (95), `check_duality.py` (73),
  `check_lower.py` (481), and `check_prof.py` (479)… the first three, 649 lines". Adding
  the disclosure docstrings *in this round* took `check_lower.py` to 488 lines and
  `check_prof.py` to 488. The round rewrote prose forty lines away and never re-derived
  the counts in the same section. Now 1,144 / 95 / 73 / 488 / 488 / 656, propagated to
  the Markdown twin, `README.md` and `PROVENANCE.md`.
- **Part B, a surviving independence claim.** §7 read "re-checked by a separate agent
  instance with no access to the pipeline **and no shared code**" — refuted by the same
  paper's own front matter, which now measures `check_lower.py` at 36 of 358 lines shared
  with `qec_lib.py`. The clause is gone from the note, its twin, `README.md` and
  `PROVENANCE.md`. The propagation grep that caught the identical fault in Part D had
  never been run for this phrasing.
- **Part E, a surviving independence claim.** The abstract and the trusted-base section
  both described the second CFR verifier as "independently written", which §3 of the same
  paper now refutes at 26 of 104 shared lines. Both sentences, the section heading and
  the source-header comment now state the dependence. The separate §1 claim about the
  *search* remains, deliberately: it is untested, not refuted.
- **Part B, an overstated characterisation.** The replacement sentence for the third LRAT
  acceptance said every shared line was one of an enumerated list and that a "three-line
  gzip-open idiom" was the longest identical run. Seven of the eighteen distinct shared
  lines fell outside the list, and the three gzip lines are not consecutive in that file:
  the longest run of consecutive identical lines is two. The sentence now says so.

The round's own numbers were re-derived by the referee from the files rather than read
from the prose, and every one reproduced. What did not survive was prose *about* those
numbers.

## Part J's disclosure moved out of the paper (2026-08-14)

The Part J correction had been written as a 1,010-word methods footnote in a five-page
paper, carrying per-file executable-line counts, script names and routine-by-routine
overlap figures, and it broke across a page and a half. That violates PROTOCOL §11 rule 1,
adopted on a referee's advice: computation files live in the repository, not the paper.

The footnote is now one paragraph of 187 words. It keeps every load-bearing statement — the
checkers are standard-library only; they are **not** code-independent of the private
structure-mining scripts in `hunt-structure/`, naming `tour_iso` and its backtracker,
`qr7`, `adj` and the backtrackers inside `aut_count` and `iso`; a passing check is
therefore not, on its own, an independent re-derivation of the isomorphism tests, the QR_7
construction or the pattern-freeness predicates; and the orbit-stabilizer argument that
makes the uniqueness conclusion independent of the shared routine anyway. Nothing was
softened and no measurement was restated in shortened form.

The full measurement text moved verbatim to `k34add-certificates/README.md`, the manifest
§11 rule 1 names. `k34add-paper/note.md` and the two working copies in
`drafts/note-k34-addendum/` were reconciled to match, and the working copies' PDF was
rebuilt.

## How to re-derive the counts in this round

Every "N of M executable lines" figure in these notes uses one convention: **executable
lines are non-blank, non-comment lines with docstring line spans excluded**, compared
after stripping leading and trailing whitespace. The docstring exclusion matters — this
round edited docstrings, so a count that includes them does not reproduce. **Run lengths
are different, and not uniform across the corpus.** In Parts B, D, E, H, K, L and M — "an
eleven-line byte-identical run", "a 31-line run", "the longest identical run is five
lines" — a run is a span of consecutive *physical* lines identical in **both** files,
which is why a run length can exceed the executable-line count of the same region. In Part
J the two run figures (three against the SAT search, two against the private dig) are
spans of consecutive *executable* lines, again matched contiguously in both files;
measured on physical lines instead, both come out at two. One sub-clause of that Part J
passage — `blowup_bound.py`'s "one further run", `return False` / `return True` / `def
main():` — is contiguous in the checker but not in the search corpus, so it is a one-sided
run rather than a shared one; those three lines are boilerplate and the passage's
conclusion is unaffected. A reader applying one convention where another is meant will
get numbers that differ by a line or two and read it as a discrepancy. The measuring script
is `audit-2026-08-14/clonecheck.py` in the program's working tree, which implements
verbatim overlap, longest run, AST alpha-equivalence and shared literals; note that its
own `execlines` retains docstrings, so it reproduces the *relative* findings but not the
published counts.

## Independence claims that remain untested

Distinct from the false claims this round replaced, these are claims the round could not
test either way. They are not asserted here as verified, and they are not corrections.

- `qec1435-paper/note` states in three places that the adversarial re-verification of the
  Part D corpus was carried out "with independently written code". That code is the
  auditing agent's and is not on this filesystem, so the claim cannot be measured. It is
  not refuted by this round's measurements, which concern the shipped `verify_1435.py` —
  a different program, and one whose front matter now discloses its dependence.
- `INDEPENDENT-VERIFICATION.md` states that the Part B brute-force cross-check used code
  "that shares nothing with either the pipeline or the checkers (`brute.py`)". No file
  named `brute.py` exists anywhere in the tree, so this one cannot be tested at all.
- `cfr-paper/note` §1: the shipped CFR verifier shares no code with the search. No private
  CFR generator is on this filesystem. Untested, not refuted; deliberately retained.
- Roughly 54 further independence claims across the corpus, including every C-language
  pair, were not reached. See the section below.

## Flagged and deliberately not taken

The three-script enumeration in `paper/preprint-dixmier-poisson.tex:328-331`,
`.md:6` and `README.md:42` describes the erratum re-verification as done
"independently". The audit judged the wording not false as written, so it was left
alone rather than triggering a ninth deposited-PDF rebuild. The narrowing text, if it
is ever taken, is in `audit-2026-08-14/COMPLETION-PASS-raw.json`, `drafted[1].replacement` §D.

## Files changed

Regenerate with `git diff --name-status v0.14.0`.

---

# CORRECTIONS — v0.14.0 documentation-correction round

Dated 2026-08-13. This round changed documentation only.

**No certified value changed, and no checker's verification logic changed.** Of the
8 scripts touched, 7 change only comments, docstrings or printed messages; one
non-gating demonstration script had the rational point it queries corrected; and a
machine-specific symlink to an absolute path outside the repository was removed. Every
checker passes as before, and every mathematical result of Parts A through M stands.

This file is an index, not a record. It carries no restated counts, claims or
replacement text: those live in each part's note, and the reasoning behind them in that
part's build log, which are the places they are checked. It lists what changed and
where to find the reasoning.

## Where the corrections are recorded

| Part | Version | Note | Build log | Dated round entry added |
|---|---|---|---|---|
| A | v0.1.x | [`paper/preprint-dixmier-poisson.pdf`](paper/preprint-dixmier-poisson.pdf) | [`paper/FIXLOG.md`](paper/FIXLOG.md) | yes |
| B | v0.2.x | [`paper/preprint-qec-distances.pdf`](paper/preprint-qec-distances.pdf) | [`paper/FIXLOG-qec.md`](paper/FIXLOG-qec.md) | yes |
| C | v0.3.0 | [`tt3-paper/note.pdf`](tt3-paper/note.pdf) | [`tt3-paper/FIXLOG.md`](tt3-paper/FIXLOG.md) | yes |
| D | v0.4.0 | [`qec1435-paper/note.pdf`](qec1435-paper/note.pdf) | [`qec1435-paper/FIXLOG.md`](qec1435-paper/FIXLOG.md) | yes |
| E | v0.5.0 | [`cfr-paper/note.pdf`](cfr-paper/note.pdf) | [`cfr-paper/FIXLOG.md`](cfr-paper/FIXLOG.md) | yes |
| F | v0.6.0 | [`mps-paper/note.pdf`](mps-paper/note.pdf) | [`mps-paper/FIXLOG.md`](mps-paper/FIXLOG.md) | yes |
| G | v0.7.0 | [`k34-paper/note.pdf`](k34-paper/note.pdf) | [`k34-paper/FIXLOG.md`](k34-paper/FIXLOG.md) | yes |
| H | v0.8.0 | [`wedge-paper/note.pdf`](wedge-paper/note.pdf) | [`wedge-paper/FIXLOG.md`](wedge-paper/FIXLOG.md) | yes |
| I | v0.9.0 | [`kelmans-paper/note.pdf`](kelmans-paper/note.pdf) | [`kelmans-paper/FIXLOG.md`](kelmans-paper/FIXLOG.md) | yes |
| J | v0.10.0 | [`k34add-paper/note.pdf`](k34add-paper/note.pdf) | [`k34add-paper/FIXLOG.md`](k34add-paper/FIXLOG.md) | yes |
| K | v0.11.0 | [`wedge2-paper/note.pdf`](wedge2-paper/note.pdf) | [`wedge2-paper/FIXLOG.md`](wedge2-paper/FIXLOG.md) | yes |
| L | v0.12.x | [`demag-paper/note.pdf`](demag-paper/note.pdf) | [`demag-paper/FIXLOG.md`](demag-paper/FIXLOG.md) | yes |
| M | v0.13.0 | [`zefoz-paper/note.pdf`](zefoz-paper/note.pdf) | [`zefoz-paper/FIXLOG.md`](zefoz-paper/FIXLOG.md) | yes |

The last column is mechanical and says exactly one thing: this round's diff against `main`
added a dated line to that log which is not its title. It does not certify that the entry is
complete or correct — only that the log gained one.

Every part carries a build-log entry for this round. Part J's log was created on
2026-08-13 and records only this round's corrections: no build-time log was kept for
v0.10.0, and none has been reconstructed.

## Files changed

81 files. Regenerate this list with `git diff --name-status main`.

**Part A** (6)

- `paper/FIXLOG.md`
- `paper/preprint-dixmier-poisson.md`
- `paper/preprint-dixmier-poisson.pdf`
- `paper/preprint-dixmier-poisson.tex`
- `scripts/erratum-check/exhibit.py`
- `scripts/erratum-check/fibre_check.py`

**Part B** (7)

- `paper/FIXLOG-qec.md`
- `paper/preprint-qec-distances.md`
- `paper/preprint-qec-distances.pdf`
- `paper/preprint-qec-distances.tex`
- `qec-certificates/REGENERATE.md`
- `qec-certificates/bb288/bb288_prof_K16_exact.lrat.gz` — deleted
- `qec-scripts/verify_manifest.py`

**Part C** (4)

- `tt3-paper/FIXLOG.md`
- `tt3-paper/note.md`
- `tt3-paper/note.pdf`
- `tt3-paper/note.tex`

**Part D** (4)

- `qec1435-paper/FIXLOG.md`
- `qec1435-paper/note.md`
- `qec1435-paper/note.pdf`
- `qec1435-paper/note.tex`

**Part E** (4)

- `cfr-paper/FIXLOG.md`
- `cfr-paper/note.md`
- `cfr-paper/note.pdf`
- `cfr-paper/note.tex`

**Part F** (5)

- `mps-certificates/reverify.py`
- `mps-paper/FIXLOG.md`
- `mps-paper/note.md`
- `mps-paper/note.pdf`
- `mps-paper/note.tex`

**Part G** (5)

- `k34-certificates/REGENERATE.md`
- `k34-paper/FIXLOG.md`
- `k34-paper/note.md`
- `k34-paper/note.pdf`
- `k34-paper/note.tex`

**Part H** (4)

- `wedge-paper/FIXLOG.md`
- `wedge-paper/note.md`
- `wedge-paper/note.pdf`
- `wedge-paper/note.tex`

**Part I** (6)

- `kelmans-certificates/verdict-n04-20.md`
- `kelmans-certificates/verdict-n22-24.md`
- `kelmans-paper/FIXLOG.md`
- `kelmans-paper/note.md`
- `kelmans-paper/note.pdf`
- `kelmans-paper/note.tex`

**Part J** (5)

- `k34add-certificates/README.md`
- `k34add-paper/FIXLOG.md` — added
- `k34add-paper/note.md`
- `k34add-paper/note.pdf`
- `k34add-paper/note.tex`

**Part K** (5)

- `wedge2-paper/FIXLOG.md`
- `wedge2-paper/note.md`
- `wedge2-paper/note.pdf`
- `wedge2-paper/note.tex`
- `wedge2-scripts/identity_selftest.py`

**Part L** (6)

- `demag-paper/FIXLOG.md`
- `demag-paper/note.md`
- `demag-paper/note.pdf`
- `demag-paper/note.tex`
- `demag-scripts/anchor_check.py`
- `demag-scripts/tamper_demo.py`

**Part M** (6)

- `zefoz-paper/FIXLOG.md`
- `zefoz-paper/note.md`
- `zefoz-paper/note.pdf`
- `zefoz-paper/note.tex`
- `zefoz-scripts/kill-logs/KILL-STATS.md`
- `zefoz-scripts/tamper_demo.py`

**Repository-wide** (14)

- `.gitignore`
- `.zenodo.json`
- `CITATION.cff`
- `CORRECTIONS.md` — added
- `INDEPENDENT-VERIFICATION.md`
- `PROVENANCE.md`
- `README.md`
- `SWEEP-RECORD-CFR-2026-08-06.md`
- `SWEEP-RECORD-DEMAG-2026-08-12.md`
- `SWEEP-RECORD-K34ADD-2026-08-11.md`
- `SWEEP-RECORD-KELMANS-2026-08-11.md`
- `SWEEP-RECORD-MPS-2026-08-06.md`
- `SWEEP-RECORD-TT3-2026-08-05.md`
- `SWEEP-RECORD-ZEFOZ-2026-08-12.md`
