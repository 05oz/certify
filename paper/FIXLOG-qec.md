# FIXLOG — adversarial pre-release review of the qec-d18 paper/update

Reviewer pass: 2026-08-06. Scope: `preprint-qec-distances.tex` (+ `.md` mirror,
`.pdf`) and the shipped certificate corpus behind the August-6 extension that
determines `d([[288,12,18]]) = 18` and adds the `[[360,12,<=24]]` lower bound.
Ground truth = the artifacts on disk (`qec-certificates/`, `qec-scripts/`) and
the on-machine replay results, never the prose. Rule observed: never strengthen
a claim; the artifacts are ground truth. A separate `FIXLOG.md` in this
directory belongs to the concurrent Part A (Dixmier–Poisson) erratum review and
was left untouched.

## Independent re-verification performed (all passed)

All replays used `/usr/bin/python3` (CPython 3.9.6) and the shipped
`qec-scripts/check_prof.py` (479 lines), reading the shipped certificate paths.

| certificate | result | regen CNF | lemmas | check |
|---|---|---|---|---|
| `bb288/bb288_prof_K14.json` | no wt<=14 → d_X>=15, +Lemma P → **d_X>=16** | 4939 vars, 27101 cl | 447,281 | matches paper §6.3 exactly |
| `bb288/bb288_prof_K16_exact.json` | no wt-exactly-16 → **d_X>=18** | 5249 vars, 31208 cl | 2,335,793 | matches paper §6.3 exactly |
| `bb360/bb360_prof_K12.json` | no wt<=12, +Lemma P → d_X>=14 | 13957 vars, 78648 cl | 184,403 | (corroboration) |
| `bb360/bb360_prof_K14.json` | no wt<=14, +Lemma P → **d_X>=16** | 14015 vars, 79397 cl | 428,498 | matches paper §6.4 exactly |

Also re-verified on this machine:
- `check_witness bb288/witness_X.json` → d_X<=18 (declared weight 18). ✓
- `check_duality bb288/duality.json` → d_X=d_Z (passes). ✓ (n=288 ships a duality cert)
- `check_duality bb144/duality.json`, `check_witness bb144/witness_X.json` → pass. ✓
- Lemma P hypothesis: `check_prof` exhibits `c` with `c^T H_Z = 1_n`, `|c|=72` at
  n=288 and `|c|=90` at n=360 — both match the paper. ✓
- Manifest: `verify_manifest.py` → `172 match, 0 mismatch, 10 absent (of 182)`,
  matching REGENERATE.md/§7. ✓
- Byte counts of the shipped prof proofs: 48,415,931 (K14), 43,367,744 (bb360 K14),
  14,725,981 (bb360 K12) — i.e. 48/43/14.7 MB, matching Table 1. ✓
- **bb360 ZX-duality independently confirmed in F₂**: for Π:(b,r,s)↦(1−b,−r,−s),
  rowsp(H_X·Π)=rowsp(H_Z) and rowsp(H_Z·Π)=rowsp(H_X) both hold (my own script,
  using the checker's rref). So the bb360 `d = d_X` step is mathematically true.

**Ladder verdict:** the full `d([[288,12,18]]) = 18` chain (K14 rung + Lemma P;
exact-K16 rung + Lemma P; weight-18 witness; shipped duality) reproduces
end-to-end on this machine with every published var/clause/lemma/|c| count exact.
The result is stated at defensible strength, and the single-encoding dependency
of the weight-16 rung is disclosed in the abstract, §1(B), §5, §6.3 and the
trusted base. No claim in the paper was found to exceed what the artifacts
support.

## Citations checked against primary source (title/authors/date/result)

- **Bravyi et al. [BCGMRY], arXiv:2308.07915, Table 3** (fetched): n=288 listed as
  distance "18" (no "≤"); n=360 as "≤24"; n=756 as "≤34"; caption "≤d indicates
  that only an upper bound … is known"; and "the upper bound d_circ ≤ 18 … is
  unlikely to be tight" refers to the **circuit-level** distance. This confirms
  Remark 5.1's correction verbatim. ✓
- **Okada–Kasai [OK26], arXiv:2607.14091** (fetched): title *Pair-Partition
  Constructions for CPM-Based Quantum LDPC Codes*, authors Okada & Kasai, Jul 2026
  — matches the bibliography. The Sec. V-A even-weight lemma could not be quoted
  from the abstract-only fetch, but the lemma itself is elementary and its
  hypothesis is machine-verified here (|c| exhibited). ✓ (attribution only)
- **Chen–Jafari–Lai [CJL26], arXiv:2606.12445** (fetched): title *SAT, MaxSAT, and
  SMT for QLDPC Distance Computation…*, authors Chen, Jafari, Lai, 29 May 2026 —
  matches. The specific "d≥11 at 7200 s for [[288,12,18]]" figure was not
  re-confirmable from the abstract; it is not load-bearing for any result here. ✓
- **Novelty sweep (today, 2026-08-06):** web search for a machine-checkable / LRAT
  distance certificate for [[288,12,18]] returned only the known sources (Bravyi,
  Tour de gross, BB-existence) — nothing that would pre-empt "first independently
  replayable determination." Consistent with the paper's hedge. ✓
  [Note, 2026-11-17: this sweep missed `BB288.lean` of the Lean-QEC repository, public since
  2026-06-04; see B-1 below.]

## MUST-FIX (applied)

**M1 — the printed replay block (§8/§10 "Reproducibility") is not replayable as
printed.** Empirically confirmed from a clean shell:
- the `gunzip … bb288/*.lrat.gz … bb360/*.lrat.gz` line **removes the very
  `*_prof_*.lrat.gz` files the three `check_prof.py` certs name**, so every
  check_prof command then fails `FileNotFoundError` (check_prof reads its LRAT
  gzipped). Demonstrated in a scratch copy.
- `check_lower … bb144/lower_X_K11.json` and `…/lower_Z_K11.json` reference the
  868/672 MB symmetry-free proofs that do not ship (REGENERATE items 1, 2) —
  `FileNotFoundError` confirmed.
- `check_lower … bb288/lower_X_K13_sym.json` references `lower_X_K13_i0.lrat`
  (2.94 GB, REGENERATE item 4), which does not ship — `FileNotFoundError`
  confirmed. Only `_i1.lrat` is present.
- the section flagged **only** the K16-exact command as needing regeneration,
  understating what a fresh clone cannot run.

Fix (both .tex and .md): the block is split into **(i)** commands that run on a
fresh clone from shipped artifacts (validated on this machine: witness_X,
duality bb144, prof K14, prof bb360 K12/K14, duality bb288) and **(ii)** commands
that each require regenerating one large proof first (REGENERATE.md items 1, 2,
4, 5). The harmful blanket `gunzip` is replaced by an explicit caution not to
gunzip the prof `.lrat.gz`. Verbatim lines were shortened to remove the overfull
hboxes this introduced.

## SHOULD-FIX (applied)

**S1 — bb360 `d` (vs `d_X`) rests on an unshipped duality.** Unlike n=288, the
bb360 directory ships **no** `check_duality` certificate (and no `HX.txt/HZ.txt`),
and `check_prof.py` does not verify ZX-duality (it checks only the (1,0),(0,1)
translations and the parity combiner). The passage `d_X>=16 ⇒ d>=16` for bb360
therefore relies on a duality lemma that is *verified in exact arithmetic* (I
re-confirmed it, above) but **not shipped as a one-command replayable artifact**.
Several passages implied it was ("… each converted to a statement about d by the
shipped duality certificate"; Table 1 footnote §; trusted-base item 4; §6.4).
Fix: those passages now state the replayable bb360 strength as `d_X>=16`, with
`16<=d<=24` following from the duality lemma verified in F₂ but not shipped for
this code. No claim strengthened; this is a weakening/clarification. (Abstract
left as "we certify 16≤d≤24, the lower end by this method" — defensible because
the bound is true and its main rung is replayable, and the body now carries the
shipping nuance precisely.)

**S2 — trusted-base inventory omitted the totalizer.** §5 "Assumed" item 1 named
only the Sinz counter's completeness, but the prof certificates (behind d=18 at
n=288 and the n=360 bound) use a Bailleux–Boufkhad totalizer with per-row exact
counters and a lex-leader predicate (`tot`/`merge`/`lex_ge` in `check_prof.py`),
not Sinz. Fix: item 1 and the one-sentence summary now record the totalizer's
completeness (and the lex-leader's) as assumed on the same footing as Sinz.

## FLAGGED, not modified (artifact/release hygiene — outside "fix the draft")

**S3 — absolute-path symlink in the certificate tree.**
`qec-certificates/bb288/bb288_prof_K16_exact.lrat.gz` is a symlink to
`[archive]/algo/proofs/bb288_prof_K16_exact.lrat.gz`
(an absolute path outside the repo). It is currently **untracked** in git, so it
is not yet in the release; but if `git add`-ed the release would carry a
machine-specific symlink to an absolute path outside the repository —
contradicting REGENERATE.md, which says this 310 MB proof is not carried in git
and must be regenerated. **Action for the author before commit:** do not commit
this symlink (leave the proof absent, as REGENERATE.md item 5 already
documents). Not deleted here: it is untracked (not
in the release), it is what enabled the local K16 replay above, and deleting
artifacts is outside a paper-text review.

*Outcome, recorded 2026-08-12.* The action was not carried out. The symlink was
staged and committed in `b3d00ba`, the v0.2.1 release commit reviewed above, and
it is present as mode `120000` in the tag trees v0.2.1 and v0.5.0 through
v0.13.0. Those trees carry, at the path REGENERATE.md item 5 tells the reader to
write the regenerated proof to, a machine-specific symlink to an absolute path
outside the repository, so the documented `gzip bb288_prof_K16_exact.lrat` step,
and any `gunzip bb288/*.lrat.gz` loop, act on that symlink rather than on a
regular file. The paragraph above therefore
describes the state at review time only; its "currently untracked" was overtaken
by the release commit. The symlink has now been removed from the index, and
REGENERATE.md item 5 states plainly that the path is empty and that the
procedure is what fills it.

**Directory-name mismatch (observation).** The printed commands use
`certificates/…` and bare `check_witness.py`, describing a bundled `qec/`
layout; the dev repo uses `qec-certificates/` and `qec-scripts/`. Ensure the
shipped bundle matches the printed paths (or vice-versa). Not edited, because the
intended release layout is the author's to fix and the paper is internally
consistent in the `qec/` convention.

*Outcome, recorded 2026-08-12.* Resolved the other way round: no `qec/`-layout
bundle exists in the repository, so §10 of both twins now names the release
layout — checkers in `qec-scripts/`, certificates in `qec-certificates/`, every
command run from the repository root. The six group-(i) commands were
re-executed verbatim from that root on 2026-08-12 and all six pass. The two
remaining bare `certificates/` references (§1.3 in each twin) were corrected to
`qec-certificates/` in the same pass.

## Erratum check (task item 5)

The paper's own internal correction (Remark 5.1: the earlier draft misread
Bravyi's circuit-level `d_circ ≤ 18` "unlikely to be tight" as a hedge on the
code distance). Confirmed **correct** against the primary source (Table 3 lists
288 as exact 18; the "unlikely to be tight" line is about `d_circ`). Confirmed
**no propagation**: `grep` over `.tex`/`.md` finds "unlikely to be tight" only
inside the corrective passage and the header comment; no live statement retains a
heuristic/upper-bound-only reading of the 288 distance.

## Compile

`tectonic preprint-qec-distances.tex` → PDF written, **22 pages**, 235,598 bytes.
Final-pass log: **0 undefined references, 0 undefined citations, 0
multiply-defined labels, 0 overfull hboxes**; rendered PDF has 0 `??`
placeholders. New cross-reference `\ref{ssec:bb360}` resolves.

## Bottom line

The d=18 result and the n=360 lower bound are sound and reproduce end-to-end on
this machine with every published count exact; the three verifiable citations
match their primary sources; the internal erratum is correct with no propagation.
One MUST-FIX (a replay block that did not replay) and two SHOULD-FIX
(bb360-duality-not-shipped; totalizer absent from the trusted base) were applied
without strengthening any claim; one release-hygiene item (an absolute-path
symlink) is flagged for the author to remove before commit.


## 2026-08-14 — independence-claim round (Part B, v0.15.0)

§4.1's "shares no code with the other three" and the front-matter "The three
independent checkers share no code with the generating pipeline" were replaced by
measured statements. `check_prof.py` shares 88 of 387 executable lines with
`check_lower.py`, including the 8-line LRAT propagation run `386-393 == 295-302`,
and their Tseitin encoders are alpha-equivalent. `check_lower.py` shares 36 of 358
with `qec_lib.py`, the CSS-CNF construction among them, down to the custom assertion
`assert sup, "zero pairing row"`. The third LRAT acceptance established in the
independence-backstop round is stated. `qec_lib.py`'s own "share NO code" docstring
was corrected. No certificate, proof or count changed.

**Engine 2 / V5 correction, same day.** The sentence introducing that third
acceptance was itself written as an independence claim — "a third acceptance that
shares nothing with either" — and is false on the same measurement that condemned
the others: 34 of `indep_lrat.py`'s 239 executable lines appear in `check_lower.py`
or `check_prof.py`. It now states the measurement. The 18 distinct shared lines are
bare `continue`/`break`/`else:`, flag initialisations, the main guard and the
three-line gzip-open idiom, which is the longest identical run; the claim's
substance survives, its wording did not. Propagation grep for "shares nothing with
either": 2 hits, `.tex` and `.md`, both replaced, 0 remaining. The four replayed
certificates were re-checked against the recorded backstop output: 447,281 /
2,335,793 / 184,403 / 428,498 additions, all four UNSAT, all four reproduced.

**Engine 2 / V6 corrections, same day.** The adversarial referee found three more,
all in this paper, none of which any earlier pass had caught:

1. **Stale line counts, caused by this round.** §"Software" says "Four files, 1,128
   lines of Python in total: `check_witness.py` (95), `check_duality.py` (73),
   `check_lower.py` (481), and `check_prof.py` (479)… the first three, 649 lines".
   The disclosure docstrings added in this round took `check_lower.py` from 481 to
   488 lines and `check_prof.py` from 479 to 488 (`wc -l`, and `git show HEAD:` for
   the before-state). Corrected to 1,144 / 488 / 488 / 656 here, in the `.md` twin,
   and at the six other sites that quote 481: `:633`, `:899`, `:909`, `:1042`,
   `:1322`, plus `README.md:15`, `README.md:207`, `PROVENANCE.md:105`,
   `PROVENANCE.md:126`. Propagation grep for `1,128`/`(481)`/`(479)`/`649 lines`
   across all `.tex`/`.md`/`.json`: 0 remaining.
2. **A surviving independence claim.** §7 read "with no access to the pipeline and
   no shared code". The same paper's front matter now measures `check_lower.py`
   sharing 36 of 358 executable lines with `qec_lib.py`, and the audit exercised
   `check_lower.py`. The clause is removed here, in the `.md` twin, `README.md:106`
   and `PROVENANCE.md:111`. Propagation grep for "no shared code": 3 hits remain,
   all in Parts F and I, which this round does not cover.
3. **The V5 replacement was itself overstated.** It claimed every shared line fell
   in an enumerated list and that a "three-line gzip-open idiom" was the longest
   identical run. Seven of the eighteen distinct shared lines fall outside the list
   (`args = sys.argv[1:]`, `for h in hints:`, `if not conflict:`, `if not lits:`,
   `return ok`, `return p`, `try:`), and the gzip lines are not consecutive in
   `indep_lrat.py` (`import gzip` at :50, the two-line body at :60-61). The longest
   run of consecutive identical lines is two, `indep_lrat.py:218-219`. Restated.

## Correction round, 2026-11-17

One change of checker logic (B-4); the rest is text. No certificate, witness, proof or manifest
entry changed. Each propagation grep was run over the whole tree of this release after the edits;
the hits it lists as remaining are dated notes that quote the old wording, dated records, or the
historical statements that say what the checker was before (the 488-line checker of the v0.2.1
re-run, and "a hole in 488 lines"). Counts were re-measured after the
fixes of the verification and the referee of 2026-11-17, across line breaks and markup; unless a
line says otherwise they leave out this log, CORRECTIONS.md and .zenodo.json, which quote old
wording as records.

**B-1. "The first machine-checkable determination on record" of d([[288,12,18]]) = 18.** The
Lean-QEC repository (`VerifiedQC/Lean-QEC`) has held `LeanQEC/Stabilizer/Examples/BB/BB288.lean`
since 2026-06-04 (last changed 2026-06-10; read at main `8d115519` on 2026-11-17, apart from its
long hexadecimal constants). Its theorem `BB288_dist_18` states 18 ≤ d; it rests on four rank
lemmas left as `sorry` (stated without proof), three lemmas by `native_decide` and two by
`bv_decide`. The
repository's README lists reaching [[288,12,18]] as a later goal. The sweep of 2026-08-04
inspected the tree at `c73827d` (2026-07-10), which held the file, and did not name it. Found by
our own review of 2026-11-17; the open check had been named by a review of 2026-11-11.
Credit: the Lean-QEC authors (Ehatamm, Lee, Wu and Tao). The word "first" goes in every place;
the difference is stated exactly (ours: replayable artifacts and two lemmas proved on paper,
Lemmas P and S, with no admitted step and no proof assistant; theirs: a formal Lean statement
whose proof leaves four rank lemmas as `sorry`; amended after the referee of 2026-11-17, which
asked that the comparison name our two on-paper lemmas). Corrected in the abstract,
§1.3, §1.4 (a dated paragraph of later facts, and the paragraph on Chen, Jafari and Lai), the
table of claims and its "offered as new" list, in both twins; the README, PROVENANCE.md (row 20a)
and the sweep record (dated note).
Propagation grep (`first machine-checkable`): 8 hits, each a dated note quoting the old words, or
the sentence of §1.4 in each twin that says those sentences are corrected. (`first replayable`): 1,
the README note. (`for the first time`): 6 Part B hits, three dated notes in each twin; the other
hits are an ordinal in Part N and statements of when something happened (Parts G and N).
[Addition, 2026-11-17, after the verification of this round: §6's remark still read "the first
determination ..., as far as our sweep could tell, that a third party can replay" (the words
break across lines, so the grep above missed them), and the LaTeX header comment still said "A
first lower bound of any kind". Both now carry dated notes. Propagation grep (`the first
determination`, `first lower bound`, across line breaks): the remaining hits are dated notes
and this log.]
[Addition after the referee of 2026-11-17, for the amended comparison: (`proved by sorry`): 0.
(`no admitted lemma`): 4 Part B hits, in each twin the sentence of §1 on what is offered and the
"offered as new" list; neither compares with the Lean file, and both twins state Lemmas P and S as
lemmas proved on paper (abstract, §6); 2 more, the README's and the sweep record's August
comparison with `BB144.lean`, about [[144,12,12]] and outside this entry. (`unproved lemma`): 2, the
dated note of the abstract in each twin, which describes the Lean file without a comparison.]
[Addition after a gate of 2026-11-25: row 20 of PROVENANCE.md and the "What survives" paragraph of
the August sweep record still called the bound of 2026-08-04 "the only machine-checkable lower bound
on record for this code at any strength", with no note beside the words; the greps above did not
search them. Each now carries a dated note that names the Lean file. Propagation grep (`only
machine-checkable`): 2 outside this log and CORRECTIONS.md, PROVENANCE.md (row 20) and the sweep
record, each followed by its note.]

**B-2. "[[360,12,≤24]], whose exact distance remains open".** Since Part B, d = 24 has been
reported for this code by G. Lee's bicycle-race database (github.com/gideonlsx/bicycle-race; first
release 2026-10-11, by the repository's own README, first commit and tag message and by Crocker's
record), by Crocker (Zenodo 10.5281/zenodo.23405904, version 1.3 of 2026-10-15; its first version,
10.5281/zenodo.23342752, is of 2026-10-13), by Daugherty, Ryan and Ward (Zenodo
10.5281/zenodo.23382175, version 1.0.0, dated 2026-10-14 and created on Zenodo on 2026-10-15), by
tropidist (B. Cheng, N. Guo and F. Pan; paper arXiv:2611.08247 of 2026-11-05; the result file for
this code is in the first commit of github.com/Fanerst/tropidist, dated 2026-10-07, and GitHub's
event record shows that repository made public on 2026-11-05; its two weight-24 witnesses are
logical operators of Part B's matrices, checked by the verification of 2026-11-17) and by QEDist 0.1
(J. Y. Lee, github.com/yeon-lee/QEDist, repository created 2026-11-16; its catalogue row BB360
records a completed exclusion through weight 23 in 36.6 s; its documents call such results
execution records and note that they rely on the correctness of the recorded search
implementation). The list is in the order of first public records. The Error Correction Zoo's pull
request 460 (2026-11-16) reports a local run with QEDist and dist-m4ri. Nobody has compared their
matrices with Part B's, with one exception found on 2026-11-25: the matrices that Crocker's README
defines equal the matrices `check_prof.py` builds for this code, entry for entry, and his weight-24
logical operators are logical operators of Part B's matrices. Part B's certified result for this
code stays d ≥ 16; by their manuscript, the certificates that Daugherty, Ryan and Ward ship prove
19 ≤ d ≤ 24, and those certificates were not replayed here. Found by the
review of 2026-11-11 (the first four) and our review of 2026-11-17 (QEDist, pull
request 460). Dated later-work notes in §1.4, §1.3, §1.5 and §6.4 of both twins, the README and
PROVENANCE.md (row 20b).
Reads. The QEDist README and catalogue were read on 2026-11-17. The read
of the other four sources that the program's rules ask for before release was made on 2026-11-25, each
at its own address. What was read in full and what was not, source by source:

- G. Lee's database, at commit `cee978f`, the head of its main branch. Read in full: its README,
  licence files, scripts and notebooks, its history (two commits and the tag `v1`), and the two
  records of its literature set, version 8, with n = 360 and k = 12. Line 6 of
  `data/literature/literature_v8.jsonl` and of `data/literature/status_v8.jsonl`, whose source is
  Table 3 of Bravyi et al., gives d = 24 with `d_status` `exact-recomputed-here` and `status`
  `confirmed`; its method field says that the value was rebuilt and recomputed there by one
  search program. The record holds no polynomials, no matrices and no witness, and neither file has
  changed since the first commit of 2026-10-11. Line 453, a record taken from Cruz-Benito et al.
  (arXiv:2606.02418) that prints the polynomials of §6.4, is kept there with `d_status`
  `upper-bound`. Parsed or searched by program and not read line by line: the other rows of the
  two literature files, the lists of codes and groups, the two coverage files and the four
  circuits. The companion paper (arXiv:2610.13880), which Part B does not cite, was read in part
  only. The database does not mention Part B. The day on which the repository became visible to
  the public cannot be read from GitHub's event feed now; 2026-10-11 is the repository's own date
  and Crocker's.
- Crocker's record, version 1.3, the latest of three versions. Read in full: its description and
  all 44 files of its archive, and the descriptions of the two earlier versions. Not read: the
  archives of the two earlier versions. None of the record's code was run. Its README says that
  G. Lee's database was first released on 11 Oct 2026 and already listed d = 24 for this code
  (commit aed705a, `data/literature/status_v8.jsonl`, line 6), and calls its own result an
  independent recomputation of that value, by two exhaustive searches with no proof certificate.
  It lists Part B (commit b3d00ba, 16 ≤ d ≤ 24) among the prior bounds for this code.
- Daugherty, Ryan and Ward, version 1.0.0, the only version. Read in full: the record's README,
  licence file and checksum file and all 16 pages of its manuscript. Not read: its data archive
  (970,898,044 bytes; by the README it holds the manuscript's source, the certificates with their
  proofs and verifiers, a Lean file and the simulation records), which was not downloaded. So this
  source was not read in full: none of their certificates was replayed, and the polynomials they
  use for this code were not seen (the manuscript does not print them; it names the code as the
  [[360,12]] code of Bravyi et al.). No statement of this release about this source rests on the
  archive. The manuscript states that the shipped certificates prove 19 ≤ d ≤ 24 (a proof tree at
  weight 18 in each sector) and that the exact value 24 comes from an exhaustive enumeration with
  no shipped certificate (its pages 4, 5 and 16). It does not mention Part B.
- tropidist. Read in full: the paper arXiv:2611.08247v1 (73 pages), and in the repository at
  commit `b03ec2d` its README, licence, citation file, instance list, benchmark report, audit and
  audit table, the result file for this code, the metadata of its three 360-qubit instances, and
  the dates and subjects of all 76 commits. Read in part: the other benchmark records of those
  instances, and the files that name this code in its survey of published codes. Not read: the
  rest of the repository's 15,675 files. The paper lists the code in its Supplementary Table 8,
  among the bivariate bicycle codes of Bravyi et al., with published value ≤ 24 and certified
  value 24; the repository defines it by the polynomials of §6.4 (ℓ = 30, m = 6, A = x⁹ + y + y²,
  B = y³ + x²⁵ + x²⁶) and records, for each sector, a completed search through weight 23 and a
  weight-24 witness. The paper and the files read do not name Part B.

Propagation grep (`remains open`): 4 Part B hits, each a dated note quoting the old words; the
other hits are about other parts. (`exact distance is unknown`): 2, the dated note of §1.4 in each
twin, which quotes it. (`not a formal proof`, `not formal proofs`): 0, after the referee of
2026-11-17 replaced them with QEDist's own terms. (`tropidist (2026-11-05)`): 0, after the
verification of 2026-11-17 dated tropidist by its first public record.
[Addition, 2026-11-25, after the reads listed above. (1) The verification of 2026-11-17 had taken
the date field of a GitHub event of the type PublicEvent, 2026-10-07, as the day the tropidist
repository became public. That field carries the repository's creation time: two such events of
other repositories, fetched as controls on 2026-11-25 minutes after they occurred, carry their
repositories' creation times of July and October 2026. For tropidist, the owner's public timeline
lists no push to the repository before the one of 2026-11-06 04:27 UTC, although the repository's
own list holds pushes of 2026-10-28, 2026-11-03 and 2026-11-05 (the last at 12:05 UTC), and the
event's identifier lies just above identifiers of other events dated 2026-11-05, 14:01 and 15:05
UTC, and well below the next one, dated 2026-11-06 01:23 UTC. So the repository was made public
between 2026-11-05 12:05 UTC and 2026-11-06 04:27 UTC, and by the identifier on 2026-11-05, the
day of the paper. The clauses "the day the repository became public" (said of 2026-10-07) and "on
its public main by 2026-10-20 at the latest" were wrong; neither was released. They are gone from
this entry, from §1.4 of both twins and from the README, and tropidist's authors are named. (2) The
list of the five reports is in the order of first public records in both twins, the README, this
entry and CORRECTIONS.md (item 5): tropidist moves from the head of the list to fourth place, and
Crocker, whose first version is of 2026-10-13, comes before Daugherty, Ryan and Ward. (3) Crocker's
record is dated by both versions. (4) G. Lee's database has its address, and its date now rests on
the repository itself as well as on Crocker's record. (5) For QEDist, "public 2026-11-16" rested
on the repository's creation date; the twins and this entry now say "repository created
2026-11-16" (created at 22:56 UTC that day; another account starred it on 2026-11-17 at 07:13
UTC). (6) The matrices that Crocker's record defines were compared with Part B's on 2026-11-25
and are equal, so "have not been compared" now names that exception in both twins, the README and
this entry. (7) A dated addition after "stays d ≥ 16" in §1.4 of both twins and in the README, and
an addition to item 5 of CORRECTIONS.md, state what the manuscript of Daugherty, Ryan and Ward
says its certificates prove. (8) In §1.4 of both twins the part on this code is marked as updated
on 2026-11-25, and so is the README note. Found by our own reading of 2026-11-25.
Propagation grep (`the day the repository became public`, `on its public main`,
`public 2026-11-16`): 0 outside this log. (`23405904, 2026-10-15`,
`a result file of its first commit`): 0. (`have not been compared`): 3 outside this log, §1.4 of
each twin and the README note, each followed by the exception. (`stays d ≥ 16`): 2 outside this
log, §1.4 of the Markdown twin and the README note, each followed by its dated addition; the LaTeX
twin has the sentence once in LaTeX form, followed by the same addition. (`d ≥ 16 stands`): 1,
item 5 of CORRECTIONS.md, followed by its addition. (`release checklist`): 0.]

**B-3. "A first lower bound of any kind for [[360,12,≤24]]".** True of August 2026 and kept as
a fact ("none had been reported by August 2026"), without the word "first". Changed in the
abstract (twice), §1.3, the "offered as new" list, the title and text of §6.4, in both twins; in
the README (header table, the update block, the replay comment) with dated notes.
Propagation grep (`first lower bound`): 11 hits, each a dated note quoting the old words, or the
sentence of the LaTeX header comment followed by its note (added after the verification of
2026-11-17; see B-1).
[Addition, 2026-11-25: this decision was wrong. "None had been reported by August 2026" is false
and is withdrawn everywhere; see B-8. Crocker's record, read that day (B-2), names one more paper
for this code, Symons, Rajput and Browne, arXiv:2511.13560. That paper was then read, and so was
the result table of Chen, Jafari and Lai for this code.]

**B-4. The D4 fix: `check_lower.py` now guards the symplectic branch.** The audit (D4, §8)
found that the `stab_lower` branch passes a certificate's forced literals into the encoder with no
guard, so a forged certificate with `"forced": [-1,-2,-3]` would pass. The fix is the one the
audit named: before encoding, `assert len(cert["instances"]) == 1 and
cert["instances"][0]["forced"] == []`, the guard of the CSS branch, with a one-line comment. This
changes checker logic. `check_lower.py` goes from 488 to 490 lines and from 358 to 359 executable
lines, of which 36 still occur in `qec_lib.py` (measured with the convention of CORRECTIONS.md,
which reproduces 36 of 358 on the released file); the four checkers total 1,146 lines and the
first three 658. Every `check_lower` certificate whose proof ships with the repository (19 of
23; the other four proofs are too large for git) was re-run against the changed checker and
accepted, and the auditor's forged five-qubit certificate is now rejected while the released
checker accepts it (the run is recorded with this release's build records); no certificate result
changed. Every count was updated with a dated
note: the front matter (36 of 359), the abstract and the "offered as new" list (1,146), §3 (490),
§4.1 (1,146, 490, 658), Remark 4.1, §5 (the 490-line reader) and the D4 paragraph of §8, in both
twins; the README (checker line, known gap 4), PROVENANCE.md (row 16, gap 3), the checker's own
docstring (36 of 359), and the audit record (a dated note under D4). `check_lower.py` has no
published digest in the repository (checked); `manifest.json` hashes certificates, not scripts.
Propagation grep (`36 of its 358`): 0. (`1,144`, `1{,}144`): the remaining hits are the dated
notes and the v0.15.0 records in CORRECTIONS.md and this log. (`488 lines`, `488-line`, `$488$`):
the remaining hits say what the checker was before, or are the v0.15.0 records.
[Addition, 2026-11-17, after the verification of this round: four places still called D4 open,
the paper's §1.5 ("one fixed in this release, three not") and §3 ("which is a missing guard"),
PROVENANCE.md §5b ("are not") and the README's gap paragraph; each now carries a dated note.
Propagation grep (`three not`, `is a missing guard`, `latent soundness hole`, across line
breaks): the remaining hits are the dated notes, §8's D4 paragraph (followed by its note "Fixed
2026-11-17"), the sentence of §1 in each twin that says the audit found such a hole (true as
written), and this log. (Enumeration re-measured by the fix session of 2026-11-17.)]

**B-5. "A separate agent instance that was given no access to the pipeline".** The audit's report,
`INDEPENDENT-VERIFICATION.md`, describes its author as "acting as an independent re-checker",
states no access rule, and records reading the pipeline's own outputs (`RESULTS.md`,
`manifest.json`, `meta.json`), which it did not take on trust. No other record of the audit was
read for this entry. So the sentence is narrowed to what the report shows, as for Part G (its
FIXLOG, G-8). Corrected in the front matter and §7 of both twins, the README and PROVENANCE.md
(row 22).
Propagation grep (`no access to the`): Part B hits are the dated notes; CORRECTIONS.md (v0.15.0)
and this log quote the older text as records. (`separate agent instance`): Part B hits are the
dated notes; Parts C, D and I carry the same phrase about their own audits, which this round did
not check (listed as open in CORRECTIONS.md).

**B-6. A local path in this log.** The S3 entry of this log named a proof file by an absolute path
of the author's computer; its prefix now reads `[archive]/` by the rule printed in CORRECTIONS.md
(R1). No other byte of that line changed.

**B-7. The reference [CCKF26] gave a wrong initial (added 2026-11-25).** The entry read "J.
Cruz-Benito, A. W. Cross, F. Kremer and I. Faro". The arXiv listing of 2606.02418, read on
2026-11-25, gives the authors as Juan Cruz-Benito, Andrew W. Cross, David Kremer and Ismael Faro.
Corrected to D. Kremer in both twins, with a dated note. The entry's description of the paper is
unchanged, and the paper was not read again for this entry. Found by our own reading of
2026-11-25.
Propagation grep (`F. Kremer`, `F.~Kremer`): 0 outside this entry.

**B-8. "No lower bound of any kind had been reported" for [[360,12,≤24]] was false (added
2026-11-25).** Part B has said so since its update of 2026-08-06: in these words in the README
bullet, PROVENANCE.md row 20b and §6.4, and with the word "first" in the places B-3 lists.
Decision B-3 of this round kept it as a fact. At least two lower bounds were on record before
Part B's.
(1) Chen, Jafari and Lai, arXiv:2606.12445v1 (29 May 2026), the paper Part B cites for d ≥ 11 on
[[288,12,18]]. The appendix table for their instance `BB_360_12` has 46 solver configurations
under a timeout of 7200 s each, none of them completed; the values at the timeout are ≥ 11 in one
configuration (the solver glucose4 with the encoding the table names kmtotalizer), ≥ 10 in 18,
≥ 9 in 5, ≥ 8 in 7, none in 14, and ≤ 24 from Magma. The paper describes the values of its
timeout runs as certified bounds reached before termination. Their instance is this code: the files
`data/tier5/BB_360_12_24_Hx.txt` and `_Hz.txt` of github.com/guluchen/QDistSAT (fetched on
2026-11-25, each checked against its git blob id; the repository's tree of 2026-05-25 holds the
same two blobs under `data/BB/`) have 180 rows of weight 6 each and rank 174 and 174, and their
rows are the rows of the matrices that `check_prof.py` builds for `bb360`, as sets, once each
site (i, j) is renumbered from their order j·ℓ + i to this note's i·m + j. §6.4 said of this
paper only that its solvers "time out on it".
(2) Symons, Rajput and Browne, arXiv:2511.13560 (first version 17 November 2025). They prove
that an h-fold cover of a bivariate bicycle code, with h odd and the same k, satisfies
d ≤ d_h ≤ hd, and their table of covers of [[72,12,6]] lists this code (ℓ = 30, m = 6, h = 5, the
polynomials of §6.4, k = 12). So d ≥ 6 follows from their theorem and their table; the paper
does not state it for this code. The table prints [[360,12,24]] without the sign ≤, and the text
says that above d = 14 only upper bounds were computed. The paper was not among the sources read
in August 2026.
Read on 2026-11-25, each from its arXiv LaTeX source: of arXiv:2606.12445v1 the main file (639
lines) in full and the two tables for the 288 and 360 instances (the other 25 tables of its
appendix were not read); of arXiv:2511.13560v3 the main file (1,849 lines) in full (its
bibliography file and five figures were not read), with versions 1 and 2 compared at the
theorem, the table and the sentence on how distances were computed, all three of which are in
version 1; and of arXiv:2606.02418v1 the lines that name the [[360,12]] code, the head of its
n = 360 catalogue table and the rules for its MILP statuses (it lists this code with an upper
bound only and prints no solver lower bound for it; the rest of that paper was not read again).
Corrected: the sentence is withdrawn in the abstract, §1.3 and §6.4 of both twins, in the README
(the update block, the bullet and the replay comment) and in PROVENANCE.md (row 20b), each with a
dated note; §6.4 now states both earlier bounds; item 5 of CORRECTIONS.md and the description in
`.zenodo.json` state the correction. Part B's certified d ≥ 16 is unchanged and is above both.
The released words "the only new distance information in this update" and "one genuinely new
bound" are left as they are: no lower bound as high as 16 was on record in the sources read.
Found by our own reading of 2026-11-25, which followed the paper that Crocker's record names
(B-3).
Propagation grep (`no lower bound of any kind`): 4 outside this log and CORRECTIONS.md, the dated
notes of 2026-11-25 in the README bullet, in PROVENANCE.md (row 20b) and in §6.4 of each twin,
each quoting the old words; CORRECTIONS.md states the correction once. (`none had been
reported`): 0 outside this log. (`time out on it`): 2, the dated note of §6.4 in each twin.
(`first lower bound`): 11, as in B-3; no hit was added.
