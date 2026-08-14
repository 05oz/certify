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
