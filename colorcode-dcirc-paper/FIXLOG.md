# FIXLOG — colorcode-dcirc-2026-09-01 (build decisions and corrections, in order)

## 2026-09-01

- **F-1 (prose defect caught at re-derivation).** The first note draft stated that the d = 9, rounds = 9 CaDiCaL
  witness and Stim's heuristic fault set were "the identical fault set". Re-derived: the two weight-7 sets are
  different (indices [16779, 16780, 16806, 16820, 16834, 16848, 16853] vs [192, 206, 500, 727, 1183, 1497, 1565]).
  Sentence corrected to "a different weight-7 fault set"; both witnesses ship. Propagation grep for "identical
  fault set": 0 remaining hits. Written from working memory instead of from the files — the failure class the
  program's §15 addendum names.
- **F-2 (checker scope).** `check_dcirc.py object` and `tamper_demo.py` assumed a detector-error-model object
  with a same-named circuit file; extended-code objects (`m_Xext_d*.json`, built from `c_d*_r1.stim`) were not
  covered. Extended-code branch added to both (re-derivation via `extcode_from_circuit.build`); `all` mode
  now verifies extended-code objects too.
- **F-3 (anchor result recorded exactly).** ILP anchor on (7,7): SCIP hit the 1,500 s limit, status FEASIBLE,
  incumbent 7, best bound 3 (logs/ilp_anchor.log). The SAT witness of weight 6 (certs/witness_d7_r7_w6.json)
  shows the incumbent is not optimal. Recorded in the note's Anchors paragraph and Table 2 as an incumbent,
  not as agreement; the companion code's `compute_circuit_distance` would have returned 7 here.
- **F-4 (Table 1 qubit column).** The "qubits" column was Stim's `num_qubits` (max index + 1), which counts the
  layout class's unused X-auxiliary indices (13 at d = 3). Physical count is data (3d²+1)/4 + auxiliaries
  3(d²−1)/8 = 10, 28, 55, 91, 136, 190 for d = 3..13 (referee economics verdict caught it). Both notes corrected.
- **F-5 (scoping, from REFEREE.md).** Added: Fig. 1(b) = CSV row 1 (referee matched the figure); the released
  exhaustive search builds a different circuit (separate ancillas, fixed edge schedules) and its CSV distance
  column is copied from one d = 7, one-round run; DEM built with decompose_errors=False and no filtering; noise-
  model support equality; X-basis covered by the (identical) Z-sector extended code; the paper's sentence has no
  stated method; the 863 other schedules are not certified.
- **F-6 (compute scope decision, disk-bound).** The proof-carrying d = 9, rounds = 9, K = 6 run was stopped after
  44 min with a 2.5 GB gzip partial proof because free disk fell below 10 GB with three proofs growing; the
  verdict-only twin continues (a verdict without a proof will be recorded as a solver verdict, not as a
  certificate). d = 9 remains certified two-sided by the one-round direct refutation and the extended-code
  refutation, both with LRAT; the direct d-round refutation at d = 9 is recorded as NOT OBTAINED (disk), with the
  measured cost so far. Watchdog replaced by disk_watchdog2.sh protecting the d = 7 and extended-code d = 13 runs.
- **F-7 (d = 7, rounds = 7, K = 5 direct refutation NOT OBTAINED).** Killed by the disk watchdog at 1 GB free
  after 4,105 s wall (3,155 s process, 5.7 M conflicts) with a 5.2 GB gzip partial proof, which was deleted. The
  d-round direct lower bound at d = 7 is therefore not certified on the full mechanism list on this machine; the
  d = 7 value 6 stays certified by the one-round direct refutation and the extended-code refutation. Both notes
  record "NOT OBTAINED (disk)" with the measured cost, per the referee's scoping sentence 8.
- **F-8 (extended code d = 13 certified).** Xext_d13 K = 10 UNSAT in 1,396 s; with the weight-11 witness,
  d_ext(13) = 11 = d − ⌊(13+3)/6⌋: the formula now holds with certificates over the paper's whole stated range.
- **F-9 (checker: satisfied hints).** The d = 9 X-part refutation (686 s, 4.06 GB gzip) was rejected at LRAT line
  8,759,413 because a hint clause was already satisfied under the running assignment; the checker aborted on
  that case. A satisfied hint propagates nothing, so skipping it is sound (this is what the program's released
  `check_lower.py` does); the checker now skips and counts such hints, still aborts on non-unit hints, RAT hints,
  dangling hints, non-increasing ids and a missing empty clause. Self-test extended with a satisfied-hint chain;
  tamper battery re-run. The proof is being replayed again.
- **F-10 (d = 9, rounds = 9 certified on the X-part sub-list).** K = 6 UNSAT in 686 s (4.06 GB gzip), replayed by the
  checker in 1,364 s (8,262,355 lemmas, one satisfied hint skipped); with the weight-7 witness, d_circ(9, 9) = 7 on
  M_Z, hence on the full list by the X-part lemma. All ⟨PENDING⟩ markers in both notes resolved.
- **F-11 (Table 3 cell written from memory).** The extended-code d = 13 CNF size was typed as 5,159 / 12,845; the
  metadata file says 4,009 / 9,669. Corrected from the file; every Table 3 size cell was then re-checked against
  its .meta.json (script in the build log).

## 2026-10-20 (staging for release; build session for this package, not a gate verdict — PROTOCOL §17)

Propagation greps below were run over every `.md`, `.py`, `.json` (except mechanism lists) and `.sha256` file of the
staged overlay, excluding `logs/` (unedited historical records); the hits listed are the only ones.

- **F-12 (CLAIM correction: scope of "first").** Removed every form of "no published circuit-level distance of any
  syndrome-extraction circuit carries a machine-checkable proof; these are the first" (09-01 note abstract and §1) and the
  third clause of the 2026-10-07 note-ready sentence ("first circuit-level distance of a gate-level syndrome-extraction
  circuit whose lower bound is carried by an independently checked LRAT refutation"). Kornstein (Zenodo 23394575,
  2026-10-15: DRAT-verified d_circ = 6 for the [[72,12,6]] depth-8 cycle) contradicts the general form; Pan (DRAT lift steps)
  and qsim-lab (DRAT upper bounds over schedule spaces) bound it further. Replaced by the 10-20 permitted sentence, narrowed
  to colour codes and keeping "lower bound". Also removed "its use here as a certified route is new" (extended-code route):
  Pan uses d_ext and credits its screening use to arXiv:2608.19917. Propagation: "these are the first" 0; "no published
  circuit-level distance" 0; "carries/carry a proof object" 0; "first circuit-level distance of a gate-level" 0; "certified
  route is new" 0; "first proof-carrying" 2, both in SWEEP-RECORD §2(c)/§3 as the forbidden form.
- **F-13 (CLAIM correction: credit at d ≤ 11).** qsim-lab posted solver-trusted independent values on 2026-10-04 (rounds = d
  at d = 3, 5, 7, 9; one round at d = 5, 7, 9, 11). Our 09-01 values there were unreleased, so they are credited in the note
  §6, README and PROVENANCE as reproductions of qsim-lab. Propagation: "first independent test" 1 (SWEEP-RECORD §3, forbidden
  list).
- **F-14 (prose defect: anchor count).** The 09-01 paper-style note said the authors' ILP agreed "on seven instances";
  `logs/2026-09-01/ilp_anchor.log` shows OPTIMAL on six — (3,1), (3,3), (5,1), (7,1), (9,1), (5,5) — and FEASIBLE
  (incumbent 7, bound 3) on (7,7). Now "six instances" everywhere. Propagation: "seven instances" 0.
- **F-15 (checker docstring vs code).** `check_dcirc.py`'s docstring still said "a satisfied or non-unit hint aborts"; the code
  has skipped and counted satisfied hints since F-9. Docstring corrected; no logic change. Propagation: "satisfied or non-unit
  hint aborts" 0.
- **F-16 (§10 portability).** `purex_from_object.py` and `extcode_from_circuit.py` used `path.split("/")[-1]` for an
  informational file-name field (never compared) — now `os.path.basename`. `tamper_demo.py` hard-coded `/usr/bin/python3` —
  now `sys.executable`. `extcode_from_circuit.py`'s docstring contained the invalid escape `\ ` (a SyntaxWarning since Python
  3.12, slated to become an error) — reworded ("minus"). All files parse with `-W error`. No verification logic changed.
- **F-17 (trust base narrowed).** (a) Upper bounds at d = 11, 13, 15 (r = d) and d = 15 (r = 1) are now explicit fault sets of
  the circuit's own mechanism list, lifted from the extended-code witnesses by `tools/lift_ext_witness.py` (untrusted) and
  checked by `check_dcirc.py witness` (logs/check_direct_witness_2026-10-20.log). (b) The lower-bound bridge from the
  extended code to the circuit is now stated as two finite hypotheses (A: X-part closure; B: projection onto columns) plus
  two short arguments; `certs/lemma_b_check.py` (standard-library port of the build session's Stim-based script, now also
  checking A) checks both on all 14 (d, r) objects. The proof of [SBB]'s theorem is no longer in the trust base. Its
  B-lines are identical to the Stim-based script's logged output on all 14 objects (09-01 log for d ≤ 13; 10-07 log for
  d = 15).
- **F-18 (scope).** Build-session files outside this release's scope are not part of this package. What ships is the
  distances d = 3, …, 15, each with its one-round and d-round objects, hypothesis checks, witnesses and lower bounds. *(Reworded in the revision; see F-26. The first wording
  named the excluded files and said the build logs mentioning them ship unedited; PROTOCOL §9b rules out both.)*
- **F-19 (record field).** `lower_Xext_d15_K11.json` "solver" said the converted text proof was "byte-identical to
  --no-binary output". Converter identity was checked on test instances (blrat2lrat.c header), never on this instance, and
  no --no-binary run of it exists. Field reworded to describe the converter as untrusted. Propagation: "byte-identical to
  --no-binary" 0.
- **F-20 (CLAIM correction: X-basis).** The 09-01 note claimed the extended-code certificates "cover X-basis memory too" and
  certify the full min(d_circ^X, d_circ^Z). That rests on [SBB]'s theorem applied to an X-memory circuit that was never
  built or checked. Now listed under "not claimed", with the hash identity of the two sectors as a remark. Propagation:
  "cover x-basis memory" 0.
- **F-21 (forbidden phrasings re-checked).** "first colour-code circuit distance at d = 15" 1, "by ILP" 1, "heuristic upper
  bound" 1 — all three in SWEEP-RECORD §3's forbidden list only. "without exception" 0 (the 09-01 note's "without exception in
  the sources read" sentence about how d_circ is reported is gone).
- **F-22 (re-run scope recorded).** Re-run on staged copies on 2026-10-20: all objects, witnesses, shipped proofs, hypotheses,
  tamper battery; plus three out-of-git proofs (d5_r5 44.0 s, pxd7 139.0 s, Xext_d13 706.7 s). Not re-run (20 CPU-minute
  per-run cap): pxd9_r9_K6 (09-01 logs) and Xext_d15_K11 (10-07 logs, two checkers); their CNF bindings and file hashes were
  re-checked. Stated in README and VERIFY.log.

## 2026-10-20, revision (builder session acting on the first independent battery's report R1–R11; not a gate verdict, §17)

Propagation counts below are from the whitespace-normalised grep in `VERIFY.log` §10 (lower case, any run of whitespace
matched as one space) over every `.md`, `.py`, `.c`, `.json` (mechanism lists excluded) and `.sha256` file and
`.gitattributes`, excluding `logs/`, `VERIFY.log` and `_staging-not-for-repo/STAGING-NOTES.md`. "Outside FIXLOG" counts
exclude this file, whose entries quote the superseded wording.

- **F-23 (CLAIM correction, R1: d = 13).** The authors' sentence (arXiv:2603.28852v1 main.tex:201) states that the formula
  holds numerically up to d = 13, so it gives the value 11 there; qsim-lab reads it the same way (theory-colour.md:269).
  The "not found" claim "a circuit-level distance for this circuit at any d ≥ 13 (the authors' … sentence gives no values
  or method)" was therefore false at d = 13. Replaced everywhere by: not found at d = 15; at d = 13 the authors state the
  formula with no per-d values, round count or method, and what is ours there is the first independent computation and the
  first proof (as of 2026-10-20, sources read). Supersedes F-12's replacement sentence. Places: README "What is new",
  note §6 "What is ours", PROVENANCE row Mar 30 and "d = 13", SWEEP-RECORD §2(a) and §3 (record and note-ready forms),
  PROPOSED.zenodo.json. Propagation outside FIXLOG: "at any d ≥ 13" 1, "gives no values" 1, "first value at d = 13" 1, all
  three in SWEEP-RECORD §3's not-permitted list; "gives no values or method" 0; "at d ≥ 13" 0. *(Its "first" wording superseded in round 7; F-54.)*
- **F-24 (CLAIM correction, R2: proof-object qualifier and Shutty credit).** F-12's permitted sentence had lost its
  qualifier in the note and README. Every "not found … checkable proof" sentence now reads "a checkable proof (an LRAT, DRAT
  or formal proof object)", and each is followed by the credit for Shutty's bundle (doi:10.5281/zenodo.22820614,
  distance/README.md:19–21, 51–61), which ships a re-runnable, Stim-based exhaustive check of small-instance lower bounds
  (triangular d = 3, torus d = 4). note §6 "None of these ships a checkable proof of its lower bound" now carries the
  qualifier and the credit; reference [ShuttyData] added. Places: note §6 (two places), README "What is new",
  SWEEP-RECORD §2(c) and §3, PROPOSED.zenodo.json. Propagation outside FIXLOG: "None of these ships a checkable proof of its
  lower bound." 0; "a checkable proof of" 2 (SWEEP-RECORD S1–S3 statement, which carries its own parenthetical, and the
  Zenodo text's d = 13 clause, which is about this circuit only). *(Its third item superseded in round 7; F-53.)*
- **F-25 (CLAIM correction, R3: "first" about qsim-lab).** "First public independent values" became "the earliest
  independent values found in the sources read, as of 2026-10-20" (note §6, README, PROVENANCE row Oct 4 and "Values at
  d ≤ 11", Zenodo text). The Zenodo text's "d ≤ 11 at one round" became "d = 5–11 at one round" (and "d = 3–9 at d
  rounds"). Propagation outside FIXLOG: "first public independent" 0; "first public" 0; "first independent values" 0;
  "d ≤ 11 at one round" 0.
- **F-26 (§9b, R4: scope of the shipped README and logs).** README lines 263–264 (a sentence about runs outside this
  release's scope) deleted. Ten lines about those computations were removed from four shipped 09-01 logs: `check_all_final_2026-09-01.log`
  (original lines 5, 6, 27), `object_rederivation_ext_2026-09-01.log` (8, 9), `ladder.log` (85, 86, 103),
  `ladder_ext.log` (36, 37). No other line was changed; the unredacted originals stay in the build folder, and their hashes
  and the removed text are recorded in `_staging-not-for-repo/STAGING-NOTES.md`. One removed line (`ladder.log`:103) also
  recorded that a direct one-round d = 13, K = 10 run was stopped without a verdict; README "Logs" says so. README "Logs" no
  longer calls the 09-01 logs unedited. F-18 was reworded so that it no longer names them. The round-1 `VERIFY.log`, whose
  propagation table named them, was replaced by this session's transcript. The d = 15 lemma-B log of 2026-10-07 ships only
  as an extract of its d = 13 and d = 15 lines. Propagation outside STAGING-NOTES: the eight patterns that name those
  computations (listed in STAGING-NOTES, not here) have 0 hits, apart from matches inside SHA-256 hex strings.
  *(Superseded in round 3: the lines are now redacted in place instead of deleted; see F-42.)*
- **F-27 (credit, R5: projection check).** Kornstein's deposit (doi:10.5281/zenodo.23394575, depth8_cycle/DERIVATION.md
  §3b, :161–165, with :54–59 on SBB Prop. 3) checks every fault's key against "0 or an extended-code column" and proves the
  projection lemma that Hypothesis B uses. Credited in note §3, README "How the lower bounds reach the circuit", PROVENANCE
  row Oct 15, SWEEP-RECORD §2(c), and the Zenodo text; question 7.2 reworded to cite it; SWEEP-RECORD's not-permitted list
  now forbids calling the projection check new.
- **F-28 (CLAIM framing, R6: the authors' asymptotic argument).** note §1 now gives KF's boundary argument (main.tex:199–200,
  "asymptotically reduced by a factor of 5/6") before the d ≤ 13 sentence, and frames d = 15 as a test of that argument
  beyond their numerical range as well as of the formula. Also in PROVENANCE row Mar 30, SWEEP-RECORD §2(a) and the Zenodo
  text.
- **F-29 (prose defect, R7: two README times).** Solver-cost table: direct (9,1) "26.7 s (10-20)" → "35.7 s", ext d = 11
  "20.8 s (10-20)" → "24.9 s", the values in `logs/run_all_full_2026-10-20.log`; the table now names that log. Propagation:
  "26.7 s" 0, "20.8 s" 0.
- **F-30 (tamper control, R8).** The shipped control "one CX reversed, hash left (would change DEM)" reversed a pair in the
  first CX instruction and only tested the hash binding; with the hash recomputed, that edit is accepted, because no fault
  precedes the gate (`logs/tamper_cx_layer_control_2026-10-20.log`: instruction #1 accepted, #2–#12 rejected).
  `tamper_demo.py` now reverses a pair in the third CX instruction, twice: hash left (rejected by the circuit hash) and
  circuit hash recomputed (rejected by the re-derivation). Twelve corruptions; README, `run_all.py` docstring and
  `tamper_demo.py` docstring updated. The 09-01 tamper logs keep the old label as historical records. Propagation outside
  FIXLOG: "would change DEM" 0; "eleven corruptions" 1 (README, describing the staging run); "11 corruptions" 0.
- **F-31 (metadata, R9).** `PROPOSED.zenodo.json`: title now "Certify vSTAGING-TAG: Part STAGING-LETTER — …",
  `publication_date` "STAGING-SET-ON-RELEASE-DAY", description rewritten for F-23–F-28. Version and Part letter are Kirt's
  batch decision; the pre-push hook refuses the placeholder title. Draft CITATION.cff delta and root-README index entry are
  in `_staging-not-for-repo/STAGING-NOTES.md` (certify-repo is outside this session's write scope). The §13 tag diff
  remains a release-time step.
- **F-32 (citations, R10).** note references: [Stim], [CaDiCaL], [LRAT] and [drat-trim] moved under "Tool references",
  labelled as software cited only for what was run, not read in full, with no statement resting on them. Kornstein file
  references now name their folders (`depth8_cycle/DERIVATION.md`, `depth8_cycle_independent_checks/REVIEW.md`) in
  SWEEP-RECORD §2(c) and §4, README, PROVENANCE and the note.
- **F-33 (advisories acted on).**
  (a) *drat-trim's input.* It read the converter's stream of the binary proof, not the stored `.lrat.gz`. Now said in README
  "d = 15 in detail", REGENERATE.md and note §4. The two texts were then compared: both 30,547,997,901 bytes, SHA-256
  `d1220b7e…77fb84` (`logs/d15_proof_text_identity_2026-10-20.log`), so the two checkers read the same proof text.
  (b) *Converter identity.* F-19 recorded that identity with CaDiCaL's text output was only claimed for test instances. On
  2026-10-20 the converter's output was byte-identical to CaDiCaL 3.0.1's own text LRAT on five shipped instances, and the
  re-solved proofs were byte-identical to the shipped ones (`logs/converter_identity_2026-10-20.log`). The
  `blrat2lrat.c` header now says this; its code is unchanged.
  (c) *Over-broad wording.* "reproduced the earlier circuits byte for byte" → the three circuit texts compared, (5,5),
  (13,13), (15,1) (note §2, README trust base; `cmp` in VERIFY.log). "longest identical run … in the Sinz counter and the
  XOR-chain emitter" → Sinz counter only; the emitter shares at most 3 consecutive lines (README; overlap statistics moved
  out of the note). "by every route" at d = 9 → the routes actually certified at r = d and r = 1 (note §4). "Every claim
  below" → "Every value and every machine check stated below" (note box). PROVENANCE's "contained no colour-code material"
  → the text search actually run, with its terms. Kornstein's BB result narrowed to [[72,12,6]] end to end, the larger codes
  resting in part on enumerators (README, note §6, PROVENANCE). "later relaunches also unfinished" now cites the two 09-25
  logs, shipped in `logs/2026-09-25/`. Propagation outside FIXLOG: "reproduced the earlier circuits" 0; "Sinz counter and
  the XOR-chain emitter" 0; "cardinality counter and the parity-chain emitter" 0; "by every route" 0; "Every claim below"
  0; "contained no colour-code material" 0; "DRAT-checked circuit distances for bivariate-bicycle syndrome cycles" 0;
  "later relaunches also unfinished" 0.
  (d) *Labels.* README now says that for extended-code objects the checker's "d_circ(d=…, rounds=0)" and the
  `lower_Xext_*.json` "statement" field denote d_ext. Record files unchanged.
  (e) *Unshipped evidence now shipped:* `logs/2026-10-07/lemma_b_check_d13_d15_extract_2026-10-07.log` (the d = 15 lines
  behind the "14 of 14 identical" claim), `logs/2026-10-07/lazy-annotations.patch` (the eight-module generator patch),
  `logs/2026-09-25/` (the two relaunch logs).
- **F-34 (documentation, from the battery's command advisories).** Printed commands now use `python3`, with "on Windows,
  type `py` (or `python`)" in README and REGENERATE.md; usage lines in `run_all.py`, `tools/emit_cnf.py`,
  `tools/lift_ext_witness.py` and `tamper_demo.py` likewise. `run_all.py` said "about 2-4 minutes" and the README "about
  100 s". The README now gives about 2-3 minutes (full) and about 10-15 s (`--fast`), with the measured 112.2 s and 115.7 s
  (full) and 11.3 s twice (`--fast`, Python 3.9.6) and their logs; `run_all.py`'s docstring points to that README section
  instead of carrying numbers. (A first revision run under heavier load took 197.9 s; it was superseded by the final run
  after the last edit to `run_all.py` and is not shipped.) `blrat2lrat.c` header: the pointer to an unshipped `.py` file and the `zstd` usage line removed;
  build and usage lines now match REGENERATE.md. `.gitattributes` (`* -text`) added, because every hash is over raw bytes.
  Propagation outside FIXLOG: "python run_all" 0, "python certs/" 0, "python tools/" 0, "python -m gzip" 0, "about 2-4
  minutes" 0, "about 100 s" 0, "about 10 s" 0, "well under a minute" 0, "zstd" 0, "blrat2lrat.py" 0.
- **F-35 (§11 style, battery AMBER).** The note body no longer names scripts (`lemma_b_check.py`, `purex_from_object.py`,
  `check_dcirc.py`) or gives overlap statistics; those stay in the README. Dates removed from the body: "The referee pass of
  2026-09-01" → "An internal referee pass"; Kornstein's "posted on 2026-10-15" removed. The as-of dates that §8.4 requires
  stay. Propagation in note.md: "The referee pass of 2026-09-01" 0; "posted on 2026-10-15" 0.
- **F-36 (owner decision marked, not resolved).** An owner decision, recorded in `_staging-not-for-repo/STAGING-NOTES.md`
  §1, is open and is Kirt's. README and note carry a "STAGING BLOCKER — owner decision (Kirt)" paragraph pointing at that
  section; this session did not act on the question. *(Reworded in round 3; see F-38.)*
- **F-37 (V8 and re-run record).** All checkers re-run on the staged copies after these edits (VERIFY.log): full
  `run_all.py` under Python 3.14.7, `--fast` under 3.9.6, `lemma_b_check.py` on all 14 objects, the tamper battery on d3_r3
  and Xext_d9, CNF bindings with byte comparison, lifted-witness regeneration, rebuild comparison, AST portability scan,
  `-W error` compile under both Pythons. `check_dcirc.py`, `dem_from_circuit.py`, `extcode_from_circuit.py`,
  `purex_from_object.py` and `lemma_b_check.py` are byte-identical to the staging session's copies, so the staging
  session's replays of the out-of-git proofs stand for the shipped checker. The note PDF was built from `note.md` with
  cached TeX resources only and checked by text extraction (VERIFY.log §12). Both manifests rebuilt last. *(Round 4
  added a one-line guard to these five files; see F-46.)*

## 2026-10-20, round 3 (second revision session, acting on the second independent battery's report; build record, not a gate verdict, §17)

Propagation counts below are from round 3's whitespace-normalised, lower-case grep (VERIFY.log, round-3 section R3.9),
over every UTF-8 file of the package, with `logs/`, VERIFY.log, the text extracted from `note.pdf` and
`_staging-not-for-repo/` counted separately. "Shipped prose" means every other file; "outside FIXLOG" excludes this file,
whose entries quote superseded wording. Hits in `logs/` and VERIFY.log are earlier transcripts, kept as written.

- **F-38 (§9b, battery item 1: what the owner-decision text names).** F-36 named an internal document by path and by
  status, and the STAGING paragraphs of README (lines 7–9) and note (line 8) named the subject of the open owner
  decision. F-36 and both paragraphs now say only that an owner decision recorded in
  `_staging-not-for-repo/STAGING-NOTES.md` §1 is open; the paragraphs still block release. `note.pdf` was rebuilt
  (F-45). Propagation: the twelve subject patterns (listed in STAGING-NOTES, not here) have 0 hits in shipped prose, in
  `logs/`, in VERIFY.log and in the PDF text.
- **F-39 (tamper control, battery item 2).** The case "lower: object mechanism removed, rehashed (CNF changes)" was
  rejected by the certificate's binding to its object ("certificate bound to a different object") and never reached the
  CNF; it duplicated "lower: bound to wrong object hash". Same class as F-30. It is relabelled "lower: mechanism removed,
  object rehashed, certificate not rebound (certificate-to-object binding)", and two cases follow it: the certificate
  rebound to the new object (rejected by the regenerated CNF's hash), and, in addition, its `cnf_sha256` set to the
  regenerated CNF's hash (rejected by the LRAT replay; on d3_r3 "line 1: hint 4112 is not unit"). So that a label cannot
  drift from its check again, every case now lists the checker message(s) of the check it names, and the battery fails
  a case that is rejected by any other check. A control with the old mislabel restored as an expectation, and with one
  corruption made a no-op, fails as it should: the first as "rejected by a different check", the second as "ACCEPTED",
  exit 1 (`logs/tamper_label_control_round3_2026-10-20.log`). Smaller changes in `tamper_demo.py`:
  `purex_from_object.py` is now copied into each temp directory, so X-part stems run; a bare exception is printed with the
  file and line that raised it (the extended-code CX-reversal case is rejected at `extcode_from_circuit.py:54`, the
  parser's control/target check, which is part of the re-derivation); the two "(re-derivation mismatch)" labels became
  "(rejected by the re-derivation)", and three labels gained the name of their check ("(XOR check)", "(regenerated CNF
  hash mismatch)", "(replay: no empty clause)"). Fourteen corruptions; passed on nine certificates
  (`logs/tamper_stems_round3_2026-10-20.log`). Docs: README "What each check does" and "What was re-run", `run_all.py`
  docstring, `tamper_demo.py` docstring. Propagation outside FIXLOG: "(CNF changes)" 0 in shipped prose (6 in `logs/`, 2 in
  VERIFY.log); "twelve corruptions" 0; "12 corruptions" 0 in shipped prose; "re-derivation mismatch" 0 in shipped prose.
- **F-40 (prose defect, battery item 3: an unsourced figure).** README "Notes on the costs" gave a figure about the
  build machine's use during the staging session's replays. No shipped log records it; its only record was the staging
  session's own transcript, which round 2 replaced and which does not ship. It is removed rather than re-sourced, under
  §9b. README now says what the shipped logs show: the 10-20 replays are longer than the 09-01 replays of the same
  proofs, their logs record no load figure, and the revision session's runs logged a load average of 33-55 (VERIFY.log).
  README "Run it" likewise no longer makes a statement about the machine's use during every quoted run: it lists each
  measured time with its session and log, and the load figures that the logs record. Its estimate for the full run is
  now "about 1.5-2.5 minutes", the range of the shipped full-run times (83.1-151.2 s); this supersedes F-34's "about
  2-3 minutes". Propagation outside FIXLOG: the superseded wording (listed in STAGING-NOTES, not here) 0 in shipped prose
  (1 in VERIFY.log, the round-2 header); "heavy machine load" 0; "about 2-3 minutes" 0. *(Reworded in round 4; F-47.)*
- **F-41 (citation, battery item 4).** note §7.3 cited "[qsim-lab, README.md:28]" for qsim-lab's schedule with circuit
  distance 8 at d = 9 in the authors' design space. That line does not say it; research/qec/colour-global.md:18 does, with
  the checks in its §4 (stored copy at b5f4b289, blob-identical at HEAD 682845a per SWEEP-RECORD §4). The note now cites
  "[qsim-lab, research/qec/colour-global.md:18 and §4]". qsim-lab's README.md is no longer cited and was never recorded as
  read in full (§8.1), so it is removed from the [qsim-lab] reference. Propagation: "README.md:28" 0 outside FIXLOG;
  "theory-colour.md, README.md" 0.
- **F-42 (§9b, the 09-01 log lines: redacted in place).** F-26 deleted ten lines from four 09-01 logs. They are now
  redacted in place: nine whole lines are replaced by `[REDACTED: outside this release's scope]`
  (`check_all_final_2026-09-01.log` lines 5, 6, 27; `object_rederivation_ext_2026-09-01.log` 8, 9; `ladder.log` 85, 86;
  `ladder_ext.log` 36, 37), and in `ladder.log` line 103 two items are replaced by `[REDACTED]`, so that line again
  records the stop of the direct one-round d = 13, K = 10 run. A script built each file from the unredacted original,
  re-read it, and confirmed the original's hash, the unchanged line count (156, 9, 159, 37), that exactly the listed lines
  differ from the original, and that none of the out-of-scope patterns is left. README "Logs" now describes the
  redactions line by line. Propagation: the 17 out-of-scope patterns (the eight of F-26 and nine more, listed in
  STAGING-NOTES) have 0 hits in shipped prose, `logs/`, VERIFY.log and the PDF text, apart from matches inside SHA-256 hex
  strings; "removed from four" and "One removed line" 0 outside FIXLOG (F-26 only).
- **F-43 (prose defect, battery advisory: "every rung").** note §4 said the README gives solver costs "for every rung";
  its table omits several certified rungs (the one-round direct refutations at d = 3, 5, 7 and the extended-code ones at
  d = 3, 5, 7) and the stopped one-round direct runs at d = 11 (K = 8) and d = 13 (K = 10). Now "The
  repository README gives solver costs and proof sizes for the larger refutations, and for the direct d-round
  refutations at d = 7 and 9, which were not obtained." Propagation: "every rung" 0 outside FIXLOG.
- **F-44 (record, battery advisory: qsim-lab's d = 13 figure).** Since the note now cites colour-global.md (F-41),
  SWEEP-RECORD §2(a) gains one line: that file gives the authors' schedule the value 10 at d = 13 as an evaluation of
  d − ⌊(d+3)/6⌋ (:11; also :212), which evaluates to 11, and qsim-lab's own d = 13 run of this circuit is listed as
  still running (theory-colour.md:315), so no computed value is reported there. Read from the stored copies; no new
  search, so SWEEP-RECORD's as-of time is unchanged (its revision paragraph says so).
- **F-45 (re-run record, V8, pointers).** Round 3 re-ran on the staged copies: full `run_all.py` under Python 3.14.7
  (83.1 s) and, for the first time in a shipped log, under 3.9.6 (151.2 s); `--fast` under 3.9.6 (11.9 s); the tamper
  battery on nine certificates; the label control; the AST portability scan and a `-W error` compile under both Pythons;
  the propagation grep; a check that every quoted hash fragment matches a full hash. The five verification-path files are
  byte-identical to the staging session's copies, and no object, witness, lower-bound record, circuit text or shipped
  proof changed, so round 2's comparisons and the out-of-git replays stand (not re-run: CNF bindings, lifted witnesses,
  converter identity, d = 15 proof-text identity, circuit `cmp`, overlap location). README "What was re-run" names the
  three sessions. `note.pdf` rebuilt from the final `note.md` and checked by text extraction (VERIFY.log R3.12); PDF title
  and author metadata added (battery advisory). VERIFY.log keeps round 2's transcript unchanged and appends round 3's;
  line numbers inside the round-2 part refer to the files as they were at the end of round 2. Round 2's report gave
  README and SWEEP-RECORD line pointers that were 1–3 lines off (the files themselves were not affected); this round's
  pointers were read back from the final files. Both manifests rebuilt last. *(Round 4 added a one-line guard to the
  five verification-path files, F-46, and redacted VERIFY.log line 7 and three lines of round 3's table in place, F-47.)*

## 2026-10-21, round 4 (third revision session, acting on the third independent battery's report; build record, not a gate verdict, §17)

Propagation counts below are from round 4's whitespace-normalised, lower-case grep (VERIFY.log, round-4 section R4.10),
over the same file groups as round 3's. Line numbers inside VERIFY.log's round-2 and round-3 sections refer to the files
as they were at the end of those rounds.

- **F-46 (soundness, battery item R1: the checks are asserts, and `python -O` strips them).** Every binding and
  validity check of `check_dcirc.py` outside the LRAT replay is an `assert` statement (23 asserts; its 8 raises are the
  replay's 7 and the usage exit), and Python removes assert statements under `-O`, `-OO` or `PYTHONOPTIMIZE`. The
  battery showed that under `-O` both `check_dcirc.py witness` and `run_all.py --fast` accepted
  `witness_d15_r15_w12.json` with one mechanism dropped, a false d_circ(15, 15) ≤ 11. No assert was rewritten. Every
  shipped script that relies on assert statements for a check now refuses to run when `__debug__` is false, with one
  line, `if not __debug__: sys.exit("<file>: refusing to run with Python optimisation on (-O, -OO or PYTHONOPTIMIZE):
  …")`, which prints the reason on standard error and exits with status 1. In the six files marked "one line" the
  guard replaces the empty line that followed the import line, so no other line moved and every existing file:line
  pointer into them still holds.
  - `certs/check_dcirc.py` (one line, :44): SHA-256 before → after:
    `402a5051ea79ffc5e6aff5e253358bc33b06523028f8669d9efa6ff0605ad926` → `306c293a74353c8a0500325f0efbc08a0f8bb368c01dd9882fca6f1c2ea760f1`.
  - `certs/dem_from_circuit.py` (one line, :27): SHA-256 before → after:
    `fcb49fdf6ae3c6b79140fe3b1cf813221823ff3ad469208603dba6d5dd0c717b` → `4160fb0f4585508903bb65447af9d5363898732fccd95c5a08650c75031181ff`.
  - `certs/extcode_from_circuit.py` (one line, :23): SHA-256 before → after:
    `fac37eb7b4cf5795acac6190fc078ddeefec95765d13c89c707fb0c5f1f291b7` → `2c7b48a832bba1cf304015453afc8aa1850382993d0fb60509c97b4a5789457b`.
  - `certs/purex_from_object.py` (one line, :17): SHA-256 before → after:
    `56211ce309c7804faf7067440a9209f90ccd607ec6affcf4d9b461352a1c502c` → `b673a57cf09abd3a209e85c0c8063a108f11c7de06f9e3e2777966fdb74691cd`.
  - `certs/lemma_b_check.py` (one line, :37): SHA-256 before → after:
    `d68473b2015442be878dfc4c1ef8670e86c37c29bb2490e5fd06ac4c50042db5` → `9001e5beec54ab7d4bccb39cafc69972824081cd38620b59618fa4ce1f235883`.
  - `tools/emit_cnf.py` (one line, :11): SHA-256 before → after:
    `1877c6ac9978fa589cdf2cea12a1a2807829b979beb6d92610c598fdb12e0912` → `1908df2c368e8b7f1a662ac0a05650be127e373ea792696748bf290c39db37cc`.
  - `run_all.py` (guard at :33, on what was the empty line after the imports; docstring: "fifteen" corruptions and
    one new line on `-O`): SHA-256 before → after:
    `5331d660f5c6f1260dec4443911d549927bcbe7e1bcaaee33565456947d32eda` → `bb78403be07eb073737a1e0e284f106b4ed0a5c3090a97fb088932711cbc0a11`.
  - `certs/tamper_demo.py` (guard as a new line 19; docstring; `run()` and `corrupt()` take interpreter options; the
    fifteenth case): SHA-256 before → after:
    `fde9f3949faa666e2464db66a4a133f4c7863bf0fda753896b8b3c721126692a` → `39de1d9dfd5fb1102774f68817643bfd3934d895d1c1c975d026197ac27139e4`.
  `tools/lift_ext_witness.py` is unchanged: it is the untrusted generator, its asserts are self-checks, and its output
  is checked by `check_dcirc.py witness`.
  *Control* (`logs/optimisation_guard_control_round4_2026-10-21.log`, on two scratch copies of `certs/` in which the d = 15
  witness is forged that way): with the round-3 files, `python3 -O` accepts the forged witness (rc 0) and `run_all.py
  --fast` passes (rc 0), as the battery found. With the round-4 files the witness is refused under `-O`, `-OO`,
  `PYTHONOPTIMIZE=1` without `-I` (the README's command form) and Python 3.9.6 `-O`, and so is `run_all.py --fast` under
  `-O` and under `PYTHONOPTIMIZE=1` (rc 1 each). Without `-O` it is rejected by the XOR check, alone and inside
  `run_all.py --fast` ("witness flips detectors [166, 167]"). All ten guarded commands tried on valid inputs refuse
  under `-O`. The new battery case discriminates: run against the round-3 checker it fails as "ACCEPTED" (battery exit
  1); against the guarded checker it passes (15 of 15, exit 0).
  *Replays* (the battery's "guard-only diff"): F-37 and F-45 rested the staging session's out-of-git replays on the five
  verification-path files being byte-identical to the staging copies. They now differ from those copies by the guard line
  only (VERIFY.log R4.2 prints each diff). Round 4 also replayed the same three proofs with the guarded checker
  (`logs/replay_out_of_git_proofs_round4_2026-10-21.log`): `d5_r5_K3` 190.8 s (46.9 s of CPU), `pxd7_r7_K5` 308.4 s
  (145.4 s of CPU) and `Xext_d13_K10` 1,465.3 s (708.4 s of CPU; 8,991,405 lemmas, as on 2026-10-20), each OK, from
  proof files whose SHA-256 equal `PROOFS-NOT-IN-GIT.sha256`. `pxd9_r9_K6` and `Xext_d15_K11` were not replayed (20
  CPU-minute per-run budget).
  *Docs:* README "Run it" (new paragraph "Do not use `python -O`"), "What each check does" (fifteen corruptions and the
  new case), "What was re-run" (round 4, the guard-only diff, the round-4 replays), the line count of `check_dcirc.py`
  in the trust base, "Solver cost", "Logs" and "Platforms"; `run_all.py` and `tamper_demo.py` docstrings; the draft
  index in STAGING-NOTES. Propagation, in shipped prose outside FIXLOG: "fourteen corruptions" 0; "14 corruptions" 0;
  "applies fourteen" 0; "neither revision changed" 0; "their SHA-256 are unchanged" 0; "with the same checker" 0;
  "'s 220 executable lines" 0; "14 controls" 0 (also 0 in STAGING-NOTES). The remaining hits are in round 3's logs and
  in VERIFY.log's transcripts (its diffs and its grep tables, which print the patterns).
- **F-47 (§9b, the battery's owner item 4: VERIFY.log:7 folded into the redaction).** Line 7 of VERIFY.log, round 2's
  header, carried a clause about the build machine's use during that session's runs. The clause is replaced in place by
  `[REDACTED]`; the load average after it stays, as the source of README's "load average of 33-55". Round 3's propagation
  table in the same file quoted that wording in three pattern labels (lines 814, 815, 824); they are `[REDACTED]` too,
  and F-40 above was reworded. A script changed exactly those four lines, re-read the file, and confirmed that its line
  count is unchanged and no other line differs (VERIFY.log R4.9). Round 2's part (lines 1-528), whose SHA-256 round 3
  recorded as `fd3f519d…` (VERIFY.log:534), is now `a08e5dd9…`. README "Logs" lists the four redactions. Propagation:
  the nine load patterns (listed in STAGING-NOTES, not here) 0 in shipped prose, `logs/`, VERIFY.log and the PDF text.
- **F-48 (citation, battery item R2: the Jaspersands commit).** SWEEP-RECORD §2(c) and §5 named commit 8e2eb07 for
  README.md:1876–1885, 1893–1897 and tools/verify_certificates.py:1–10 of github.com/Jaspersands/quantum-simulator-qec.
  At 8e2eb07 those README lines are a source-file inventory and the script does not exist (the battery's fetches). The
  lines cited are those of the README at 899df56, the clone of 2026-10-20 (re-read from that stored clone), and that
  README is byte-identical to the battery's copy at 49e6253 (2026-10-19). At 8e2eb07 the CHANGELOG (:29–34) gives the
  XYZ colour-code memory's circuit distance at d = 3 and 5 only. §2(c) now dates the two separately: d = 3 and 5 at
  8e2eb07 (2026-10-07); d = 7 and the 6.6.6 values in the README at 899df56, with the date d = 7 was added left open;
  the script at 899df56. §5 names both commits, and the revision paragraph says so. Nothing was downloaded; the as-of
  time is unchanged. Propagation in shipped prose outside FIXLOG: "quantum-simulator-qec (2026-10-07)" 0; "commit
  8e2eb07: the lines cited" 0. *(Round 5 moved the entry from §5 to §4; see F-51.)*
- **F-49 (prose defect, battery item R3: an unsourced load claim).** REGENERATE.md "Expected cost" said that the d = 13
  replay of 2026-10-20 ran under heavy load. Its log (`logs/replay_out_of_git_proofs_2026-10-20.log`) records no load
  figure, as README says; F-40's grep had searched for "heavy machine load" and missed this wording. The line now says
  that log records no load figure, and adds round 4's replay with the load averages its log records. Propagation in
  shipped prose outside FIXLOG: "heavy load" 0.
- **F-50 (re-run record, V8, manifests, pointers).** After the last edit to a script, round 4 ran on the package: full
  `run_all.py` under Python 3.14.7 and 3.9.6 (24 objects, 25 witnesses, 11 proofs, 14 hypothesis checks, the battery
  15 of 15) and `--fast` under 3.9.6 (20, 25, 9 and 10), all passing; the battery on nine certificates; the guard
  control; the three replays; the §10 scan and a `-W error` compile under both Pythons; the propagation grep; and a
  mechanical check of every quoted hash fragment and file:line pointer in the package (VERIFY.log R4.12). The load
  averages recorded in these logs reach 168.1, so README lists their times separately and does not use them for its
  estimates. `note.md` and `note.pdf` are unchanged since round 3 (VERIFY.log R4.13), so round 3's V8 check stands. Not
  re-run (inputs and logic unchanged): CNF bindings, lifted witnesses, converter identity, the d = 15 proof-text identity,
  the circuit `cmp`, the overlap location. Both manifests rebuilt last.

## 2026-10-21, round 5 (fourth revision session, acting on the fourth independent battery's report; build record, not a gate verdict, §17)

Propagation counts below are from round 5's whitespace-normalised, lower-case grep (VERIFY.log, round-5 section R5.5),
over the same file groups as rounds 3 and 4. Line numbers inside VERIFY.log's round-2, round-3 and round-4 sections refer
to the files as they were at the end of those rounds.

- **F-51 (§8.1, battery item G1: a cited source recorded as screened).** SWEEP-RECORD §2(c) cites
  github.com/Jaspersands/quantum-simulator-qec with line pointers into its files and §3 uses it twice as evidence,
  while §5 listed it under "Screened, not read in full". §8.1 requires a source cited for any purpose to be read in full.
  Round 5 read in full, from the copies already stored: at commit 899df56 (the clone of 2026-10-20) its README.md
  (2,718 lines; byte-identical at 49e6253), tools/verify_certificates.py (71 lines; identical at 49e6253),
  tools/distances.py, data/distances.json and src/generated.rs; at commit 8e2eb07 its CHANGELOG.md (407 lines). It
  also searched the whole clone for proof-object words and proof files and found none. What these files say agrees
  with §2(c) and §3 as written: the colour-code circuit distances there are integer-program optima (2, 3, 4 at
  d = 3, 5, 7 for Stim's XYZ memory, one auxiliary qubit per check there; 2, 3 at d = 3, 5 for the generic 6.6.6
  schedule), and the script named for "certificates" checks decoder conformance. So no sentence of §2 or §3, and
  none of the note, README, PROVENANCE or Zenodo text, changed. The entry moved from §5 to §4, as a new group
  "Read in full in round 5" under "Sweep of 2026-10-20", listing the files, their commits, what they hold on colour
  codes and the search; §5's "Repositories." keeps dist-m4ri only. The entry also records the README's own label for
  the script, "the distance certificates checked independently" (the battery's advisory A4), and that the 8e2eb07
  CHANGELOG says the graph-like search matches Stim's lengths on Stim's colour codes up to d = 15, giving no value.
  The revision paragraph's round-4 sentence now covers round 5 in the same two lines, so SWEEP-RECORD's lines 1-197
  did not move and every pointer into §1-§3 still holds (§2(c) is still at 77-83, §3's items at 136 and 140); the
  later lines moved down 20 (18 after §5's "Repositories." heading). Nothing was fetched, so the as-of time is
  unchanged. Propagation in shipped prose outside FIXLOG: "the README and tools/verify_certificates.py lines cited
  in" 0; "(cloned on 2026-10-20)" 0; "Jaspersands/quantum-simulator-qec: the README" 0; "from copies already
  stored; no new search" 0.
- **F-52 (record, pointers, manifests).** Round 5 changed SWEEP-RECORD, this file and STAGING-NOTES (internal), and
  appended VERIFY.log's round-5 section. No script, object, witness, lower-bound record, circuit text, proof, file
  under `logs/`, `note.md` or `note.pdf` changed (VERIFY.log R5.1), so no checker was re-run: round 4's runs and the
  fourth battery's re-runs stand, and round 3's V8 check of the unchanged PDF stands. The mechanical pointer and hash
  check over the package reports 0 FAIL (VERIFY.log R5.6). The new §4 entry's pointers into the clone, which that
  check cannot resolve, were read back against the stored copies (VERIFY.log R5.3). Both manifests rebuilt last.

## 2026-10-28, round 7 (fifth revision session, acting on the release-day recency check of 2026-10-27, an independent review of that check, and the sweep of 2026-10-28; build record, not a gate verdict, §17)

The recency check and the sweep are internal records; what they read is listed in SWEEP-RECORD §7. Propagation counts below
are from round 7's whitespace-normalised, lower-case grep (VERIFY.log, round-7 section R7.6), over the same file groups as
rounds 3 to 5; "outside FIXLOG" excludes this file, whose entries quote the superseded wording. Line numbers are those of the
files at the end of round 7. No script, object, witness, lower-bound record, circuit text, proof or file under `logs/`
changed.

- **F-53 (CLAIM correction, recency check: the third "not found" item).** The 2026-10-20 item, that "a checkable proof (an
  LRAT, DRAT or formal proof object) of a lower bound on, or the exact value of, the circuit distance of any colour-code
  syndrome-extraction circuit" was not found, is contradicted by Crocker's record doi:10.5281/zenodo.23633600 (v1.0,
  2026-10-25), read in full by the sweep of 2026-10-28. For another single-auxiliary schedule of the authors' family, C9,
  circuit distance 8 = d − 1 at d = 9, the extended-code step of the lower bound has a DRAT proof (kissat, checked by
  drat-trim), which the record's script regenerates from the shipped CNF, checks and deletes; the circuit step is a
  Stim-based single-fault check at 1–5, 9 and 25 rounds, with a hand lemma for every number of rounds in a companion note
  that is not in the record (SWEEP-RECORD §7.3). The item is replaced by the narrower form that the sweep found available,
  in the "not found in the sources read, as of 2026-10-28" form only: "a checkable proof (an LRAT, DRAT or formal proof
  object) of a lower bound on the circuit distance of any circuit with the authors' schedule, at any d, or of any
  colour-code syndrome-extraction circuit at d ≥ 11". Crocker's record is added to the other colour-code circuits as the
  one with a DRAT proof for its lower bound, saying exactly what that proof covers. Places: note.md:242–256 (the list and
  the paragraph after it), :278–280 (the item), :328 ([Crocker]); README.md:36–44 (the item), :46–56 (new paragraph);
  PROVENANCE.md:22 (row Oct 25), :47–52; PROPOSED.zenodo.json:3 (the "Not found" list); SWEEP-RECORD:119–129 (record
  form), :140–142 (note-ready form), :148–154 (conditions), :175–193 (not permitted), :356–366 (§7.2), :370–409 (§7.3).
  Propagation outside FIXLOG: "found for any other colour-code syndrome-extraction circuit" 0; "lower bound on, or the
  exact value of, the circuit distance of any colour-code" 1 (SWEEP-RECORD:183, the not-permitted list); "the nearest item
  found is the bundle of Shutty" 0; "the nearest item is Shutty" 0.
- **F-54 (CLAIM wording, from the review: "first").** The note's "What is ours" used "first" three times as a priority
  claim (2026-10-20 lines 245–249). The three items now read "not found in the sources read, as of 2026-10-28; this note
  gives each of them" (note.md:271–280). The same rewrite: SWEEP-RECORD:131–142 (note-ready form), PROVENANCE.md:40–43
  ("d = 13"), PROPOSED.zenodo.json:3 (the d = 13 sentence), and README.md:26–28, whose heading "What is new, and what is not"
  became "What was not found elsewhere, and what was", with "Not new:" headings now "Found earlier:" (README.md:46, :58,
  :72). A scan of every UTF-8 file of the package for first, new, novel(ty), earliest, only and unique (VERIFY.log R7.5)
  finds no other priority use: the remaining hits are ordinal or mathematical ("the first distance beyond the authors'
  numerical range", "the loss term first equals 3"), negated ("not a new idea"), the "earliest … found in the sources read,
  as of" form for qsim-lab, the quoted forms of SWEEP-RECORD §3's not-permitted lists, earlier FIXLOG entries, and
  transcripts. Propagation outside FIXLOG: "is the first test of the authors' formula" 0; "this is the first test of" 0;
  "ours is the first independent" 0; "the first proof of it" 1 (SWEEP-RECORD:214, the wording-rule list); "the first
  independent computation and the first proof" 0; "in which nothing earlier was found" 0; "to our knowledge" 0; "what is
  new, and what is not" 0; "not new: the values" 0; "not new: proof-carrying" 0.
- **F-55 (credit: the authors' bulk statement, and later results on the same schedule).** note.md:25–27 (2026-10-20) said
  the circuit "avoids malignant hook errors in the bulk [KF]" as a fact. It is now the authors' statement (arXiv:2603.28852v1
  main.tex:61, :196), followed by Issa and Martonosi's counterexample (arXiv:2610.33347v1, submitted 2026-10-23): on every
  non-corner plaquette, bulk included, a weight-2 junction hook error and d − 2 data errors form an undetected logical error
  of d − 1 faults, checked at d = 7, 9 and 11 (main.tex:31–32, :88–89, :203–209). The sentence does not say that these sets
  fall below the formula's value, which they do not (d − 1 ≥ d − ⌊(d+3)/6⌋, with equality at d = 7); it reports, as they do,
  that they leave the authors' distance unchanged (main.tex:265–268). Places: note.md:26–32, :322 ([IM]). The sweep
  confirmed that Crocker's Kishony–Fowler rule is the same CNOT schedule as S₀ (a different circuit construction), and
  Issa–Martonosi use the schedule of the authors' circuits (main.tex:119–123), so both are credited as later independent
  results on the same schedule: Crocker's extended-code distances 2, 4, 6, 7 at d = 3–9 by exhaustive search, with circuit
  distance 7 at d = 9 for one and three rounds, and Issa–Martonosi's d − 1 upper bounds at d = 7, 9, 11. qsim-lab stays
  the earliest found at d ≤ 11, now "as of 2026-10-28". Places: note.md:216, :228–236; README.md:58–70; PROVENANCE.md:15,
  :20 (row Oct 23), :30, :33–35; PROPOSED.zenodo.json:3; SWEEP-RECORD:155–161, :415–434. Propagation outside FIXLOG:
  "which avoids malignant hook" 0; "avoids malignant hook errors" 0. *(Its "with equality at d = 7" corrected in round 8; F-60.)*
- **F-56 (credit: Pan's release v2.0 and experiment E-037).** Pan's credit described release v1.0 only, and said that his
  d_ext and logical lists rest on searches. Since release v2.0 (2026-10-24) his period-11 circuits (circuit
  distance 12 for the gross code, 10 for [[90,8,10]]) carry VeriPB proofs for d_ext and for list completeness, and
  DRAT proofs checked by drat-trim and `cake_lpr` for the lifts; experiment E-037 (2026-10-25) gives VeriPB-checked
  lower bounds of 10 for IBM's depth-8 gross-code cycle for every number of rounds up to 12, with certificates
  regenerable from his public code and not in his repository (line pointers: SWEEP-RECORD §2(c)). The note body carries no
  day-level dates (§11; F-35); the dates are in the reference and in PROVENANCE. Places: note.md:265–269, :333 ([Pan]);
  README.md:76–81; PROVENANCE.md:18 (v1.0 row, now labelled as v1.0), :21 (v2.0), :23 (E-037); SWEEP-RECORD:99–111 (§2(c)),
  :200–201 (not permitted), :436–438. Propagation outside FIXLOG: "drat-checked steps in a circuit-distance argument for the
  gross code" 0; "gross-code circuit-distance argument with drat-checked lift steps. its d_ext" 0; "release v1.0
  (2026-10-20)." 0.
- **F-57 (record: as-of times, the sweep record's round-7 section, not-permitted additions).** Every "not found" sentence
  and the qsim-lab "earliest" sentence now say "as of 2026-10-28" (note.md:216, :271; README.md:26–27, :59; PROVENANCE.md:15,
  :30, :43, :45, :50; PROPOSED.zenodo.json:3; SWEEP-RECORD:119, :134, :157). SWEEP-RECORD: title (:1); as-of statement
  (:3–7), which keeps 2026-10-20 for §1, §2 and §4–§6; the revision paragraph (:15–17); §2(c)'s 2026-10-20 verdict marked
  superseded (:64–66); §3 rewritten (:113–215), with the not-permitted additions "first checkable proof of a colour-code
  circuit distance" (:179–181), the 2026-10-20 third item without its limits (:182–185), four sentences about what
  Crocker's record proves and computes (:186–193), the bulk-hook sentence as fact (:194–195), "junction hook errors bring
  the distance below the formula" (:196–199), Pan's v1.0 limits as current (:200–201), Crocker added to two earlier items
  (:165, :167, :209), and a list barred by the wording rule (:211–215); two §6 items marked re-checked (:324–325, :331–332);
  §7 added (:334–510: what was checked and when, verdicts, findings, sources read in full, screened sources, gaps, and the
  next re-check list). PROVENANCE.md gains rows Oct 23, Oct 24, Oct 25 (two) and Oct 27–28 (:20–24). The note's draft date
  is October 28, 2026 (note.md:6). Propagation outside FIXLOG: "draft of october 20, 2026" 0; "no value appears in any source
  read as of 2026-10-20" 0; "found in the sources read (as of oct 20)" 0.
- **F-58 (prose defects found in passing).** (a) README.md:449 still said that VERIFY.log holds "the three revision
  sessions, rounds 2, 3 and 4", although round 5 had appended its transcript; it now lists rounds 2, 3, 4, 5 and 7.
  (b) README.md:208–210, new: rounds 5 and 7 changed records and prose only, so neither re-ran a checker. (c)
  PROVENANCE.md:13 said arXiv:2603.28852 was "still v1 only on Oct 20"; the recency check's version query found it still
  at v1 on Oct 27. Propagation outside FIXLOG: "three revision sessions, rounds 2, 3 and 4" 0; "(still v1 only on oct 20)"
  0.
- **F-59 (re-run record, V8, manifests, pointers).** Nothing on the verification path changed, so no checker was re-run:
  round 4's runs and the later batteries' re-runs on these byte-identical files stand (VERIFY.log R7.1). `note.pdf` was
  rebuilt last from the final `note.md` with the recipe in the internal build record (pandoc 3.10.2; Tectonic 0.17.0 with
  cached resources only) and checked by text extraction: 17,241 normalised characters, 0 differing blocks, all thirteen
  symbol counts equal, title and author metadata present, 7 pages (VERIFY.log R7.7). The mechanical pointer and hash check
  reports 0 FAIL (VERIFY.log R7.8); the new pointers into Crocker's record, the two arXiv sources and Pan's files, most of
  which that check cannot resolve, were read back against the stored copies (VERIFY.log R7.3). Both manifests rebuilt last.

## 2026-10-29, round 8 (sixth revision session, acting on the advisories of the fifth independent battery, which re-gated round 7, the arXiv mailing of 2026-10-28, the recency list of 2026-10-29, the second-machine runs of 2026-10-28 and the owner's decisions of 2026-10-28; build record, not a gate verdict, §17)

Propagation counts below are from round 8's whitespace-normalised, case-insensitive grep (VERIFY.log, round-8 section
R8.7), over the same file groups as rounds 3 to 7, with the drafts of the repository's root files, the release notes and
the library entry counted as shipped; "outside FIXLOG" excludes this file, whose entries quote the superseded wording,
and VERIFY.log. Line numbers are those of the files at the end of round 8. No script, object, witness, lower-bound
record, circuit text, proof or earlier file under `logs/` changed; `logs/2026-10-28/` is new (F-65).

- **F-60 (CLAIM wording, battery advisory A-r7-1: the range of equality).** SWEEP-RECORD §3's not-permitted list said
  that d − 1 ≥ d − ⌊(d+3)/6⌋ for every d ≥ 3 "with equality at d = 7", as F-55 did. Equality holds exactly when
  ⌊(d+3)/6⌋ = 1, that is, for 3 ≤ d ≤ 8: at d = 3, 5 and 7 among odd d, and, of the sizes Issa and Martonosi checked
  (7, 9 and 11), at d = 7 only (VERIFY.log R8.5 tabulates d = 3 to 15). The item now reads "with equality for d ≤ 8 (of
  the sizes Issa and Martonosi checked, at d = 7)" (SWEEP-RECORD:203–205), and F-55 has a same-line note pointing here
  (:486), as at :124 and :133. No other sentence stated the range. Propagation outside FIXLOG: "with equality at d = 7"
  0 (also 0 in VERIFY.log, `logs/` and the PDF text).
- **F-61 (record, battery advisory A-r7-2: the ranges of VERIFY.log R7.2).** R7.2 gives the ranges that round 7
  appended as SWEEP-RECORD "new 334-511", the internal build notes "new 358-429", FIXLOG "new 434-524" and PROVENANCE
  "new 47-53": each ends one line past its file, which had 510, 428, 523 and 52 lines at the end of round 7, each line
  ending in a newline. Round 7's change map split each file at its newlines, so the empty string after the final
  newline counted as a line. VERIFY.log is append-only, so R7.2 stays as written; R8.2 gives the ranges as 334-510,
  358-428, 434-523 and 47-52. Round 8's change map (R8.3) compares lines with their line endings, and no range it gives
  runs past the end of a file.
- **F-62 (CLAIM wording, battery advisory A-r7-3: "ours").** The note's heading "What is ours" (note.md:269), README's
  "what is ours there is the independent computation and the proof" (README.md:29–30) and PROVENANCE's "ours gives
  both" (PROVENANCE.md:44) each stood on a "not found in the sources read, as of" sentence, so none was a bare priority
  claim, but PROTOCOL §9 lists "ours" beside "first". They now read "What was not found elsewhere.", "what this
  package adds there is the independent computation and the proof" and "this package gives both", as README's own
  heading already did. The other uses of "our" in these files are attributive ("Our value at d = 13 agrees with that
  statement") or negated ("not ours in general"). Propagation outside FIXLOG: "What is ours" 0; "what is ours there" 0;
  "ours gives both" 0 (the PDF text in R8.7).
- **F-63 (credit, battery advisory A-r7-6: Shutty beside PROVENANCE's third item).** SWEEP-RECORD §3 asks that
  Crocker's C9 proof and Shutty's small-instance check be credited wherever the "not found" list appears
  (SWEEP-RECORD:159–160). PROVENANCE's paragraph "Checkable proofs." gave the third item with Crocker's credit only. It
  now continues with the gated sentence of README.md:33–39: the nearest items found are Crocker's record and the bundle
  of Shutty's arXiv:2609.21376 (doi:10.5281/zenodo.22820614, `distance/README.md`), which ships a re-runnable,
  Stim-based exhaustive check of that paper's small-instance lower bounds for a different circuit, a search that trusts
  Stim and not a proof object (PROVENANCE.md:53–56). Propagation: a credit addition, so no superseded phrase.
- **F-64 (CLAIM date and record: the as-of date moves to 2026-10-29; SWEEP-RECORD §7.8).** The arXiv mailing that
  round 7 could not obtain, that of 2026-10-28 (137 entries), was read on 2026-10-28: no entry gives a circuit distance,
  a test of the formula or a lower-bound proof object for a colour-code circuit, and none is a new version of a paper
  the note, README or Zenodo text cites. The re-check list of SWEEP-RECORD §7.7 was issued again after 2026-10-29
  00:00 UTC: the Zenodo records by topic and by name, the version checks, the repositories and repository searches,
  the Kishony–Fowler authors' repositories, the Error Correction Zoo colour pages and the later versions of Shutty's and
  QECCertificates' records. Nothing found bears on S1, S2, the d = 13 item or the narrowed third item. arXiv issued no
  mailing on the evening of 2026-10-28, because of scheduled database maintenance, so the mailing of 2026-10-28 was the
  latest one; the submissions received from 14:00 EDT on 2026-10-27 to 14:00 EDT on 2026-10-29, announced on 2026-10-29
  at 20:00 EDT, are not covered, and SWEEP-RECORD says so (§7.6, §7.7, §7.8). The date of every "not found" sentence and
  of the qsim-lab "earliest" sentence moves to 2026-10-29: note.md:214, :269–270; README.md:21–22, :54;
  PROVENANCE.md:15 ("as of Oct 29"), :31, :44, :46, :51; PROPOSED.zenodo.json:3 (twice); SWEEP-RECORD:1 (title), :3–4
  and :7–9 (the as-of statement: 2026-10-29, 00:50 UTC, for §3 and §7, arXiv through its mailing of 2026-10-28),
  :120–123 (the 2026-10-29 forms, worded as round 7's), :125, :140, :152–153 (the date stays 2026-10-29 until the later
  announcements are read), :163, :338 (the list for statements after 2026-10-29 is §7.7), :358–359 (§7.1's coverage),
  :363 (§7.2's heading points to §7.8), :498–505 (§7.6's arXiv gap, closed through the mailing of 2026-10-28, with what
  is not covered), :510 and :516–518 (two more §7.6 gaps, closed), :520–527 (§7.7, now the list for statements after
  2026-10-29) and :529–674 (§7.8: what was checked and when, each class of source with its own check time; the
  findings, source by source; the verdicts as of 2026-10-29; the limits). The revision paragraph gains a round-8
  sentence (SWEEP-RECORD:20–22), and PROVENANCE a row Oct 28–29 (PROVENANCE.md:25). Propagation outside FIXLOG: "as of
  2026-10-28" 1 (SWEEP-RECORD:363, §7.2's heading, which dates round 7's verdicts and points to §7.8); "as of Oct 28"
  0; "These are the 2026-10-28 forms" 0; "after 2026-10-28 is §7.7" 0; "The date stays 2026-10-28" 0; "Re-check before
  any public statement made after 2026-10-28" 0.
- **F-65 (record: the second-machine runs of 2026-10-28; README "Platforms" and "Logs").** On 2026-10-28 a byte copy of
  this directory as it was after round 7 ran on GitHub-hosted runners, ubuntu-latest and windows-latest, under Python
  3.9 and 3.14; under Python 3.14 the proofs that are not in git were also fetched, checked against
  `PROOFS-NOT-IN-GIT.sha256` and replayed by `certs/check_dcirc.py lower` (`d5_r5_K3`, `pxd7_r7_K5` and `Xext_d13_K10`
  on Linux and on Windows, `Xext_d15_K11` on Linux). The 18 logs ship under `logs/2026-10-28/`, byte-identical to the
  runs' outputs; the Windows ones keep their CRLF line endings, which `.gitattributes` keeps byte-exact. README
  "Platforms" replaces "Not yet run on Windows or Linux." with the runs and their results, each read back from the logs
  (README.md:466–475; VERIFY.log R8.4): `SHA256SUMS` 156 of 156 with none unlisted on all four; `run_all.py` in full (24
  objects, 25 witnesses, 11 proofs, 14 hypothesis checks, all 15 tamper corruptions rejected) and with `--fast` (20, 25,
  9 and 10); the four out-of-git replays, the d = 15 one with 53,140,862 lemmas in 3,968.4 s; `pxd9_r9_K6` not replayed
  off the build laptop. Apart from times and line endings, each `run_all` log equals, line for line, the round-4 log of
  record of the same mode and Python version, without that log's own header and footer lines (R8.4). README "Logs" gains
  an item for `logs/2026-10-28/` and lists round 8 among the VERIFY.log transcripts (README.md:451–458); "What was re-run"
  gains a paragraph on round 8 (README.md:208–211) and leaves the sentence on rounds 5 and 7 (README.md:204–206) as it
  was, since round 8 added logs; and the `Xext_d15_K11` item points to the 2026-10-28 replay (README.md:254–255).
  Propagation outside FIXLOG: "Not yet run on Windows or Linux" 0; "rounds 2, 3, 4, 5 and 7" 0.
- **F-66 (record: the two blocker paragraphs removed).** The owner decided, on 2026-10-28 at about 03:30 EDT, the open
  question recorded in the internal build notes, §1, that the two blocker paragraphs held open. The paragraphs are
  removed (README.md, the former lines 7–9; note.md, the former line 8, with one adjacent blank line each), README's
  title drops its "(staging)", and README's status paragraph (the former lines 3–5, which said the directory carried no
  version number, Part letter or DOI) is replaced by "Part N of Certify (v0.16.0)", the note and its PDF, and
  `VERIFY.log` (README.md:1, :3–4). The marker sweep (VERIFY.log R8.8) finds no marker outside the historical
  quotations that FIXLOG F-31 and VERIFY.log's round-7 section hold. Propagation outside FIXLOG: "staged, not released"
  0; "carries no version number, Part letter or DOI" 0; "certificates (staging)" 0.
- **F-67 (release labels and the root-file drafts).** Part N and v0.16.0, as the owner stated on 2026-10-28: the note's
  line 6 is now "Part N of Certify (v0.16.0). Version of October 29, 2026." (note.md:6), `PROPOSED.zenodo.json`'s title
  begins "Certify v0.16.0: Part N — " and its `publication_date` is 2026-10-29 (PROPOSED.zenodo.json:2, :5). Drafts of
  the repository's root files for this release were written with the internal build notes: `CITATION.cff` (the Part N
  clause of `message`, "Parts B–N", the title "Parts A through N", `date-released` 2026-10-29, `version` 0.16.0 and three
  keywords), `README.md` (a Part N section built from the package's gated sentences, its layout block, `colorcode-dcirc-`
  among the licensed directories, "B through N", Part N's six checkers in the import list, and one sentence on the runs
  of 2026-10-28), the release notes, the library entry, and the list of the lines that receive the DOI once the record is
  minted. Propagation outside FIXLOG: "Draft of October 28" 0 (2 in VERIFY.log, round 7's quotation of the former
  line 6).
- **F-68 (proof hosting).** As the owner stated on 2026-10-28, the five proofs that are not in git are to be attached
  to the GitHub release v0.16.0 of this repository, the two larger than 2 GiB in parts of 1,900,000,000 bytes, and the
  binary original of the d = 15 proof is not. REGENERATE.md gains "Downloading the original proofs" (REGENERATE.md:23–58:
  where the files are, the parts, the joining commands for POSIX and for Windows cmd, the hash commands, and the check);
  README.md:144–146 says that a proof marked "In git: no" is attached to that release (in parts if over 2 GiB); and the
  Zenodo text says that the five are attached to the release, not to the archive, and that REGENERATE.md gives the
  joining commands and the hashes and recreates them (PROPOSED.zenodo.json:3). note.md:194–198 ("…or by obtaining the
  originals, whose SHA-256 are listed there") was true already and is unchanged. The part sizes, 1,900,000,000 ×2 +
  257,166,967 = 4,057,166,967 and 1,900,000,000 ×4 + 1,345,210,112 = 8,945,210,112, equal the byte counts of
  `PROOFS-NOT-IN-GIT.sha256`. Propagation outside FIXLOG: "recreates them from the shipped objects and lists" 0;
  "listed in `PROOFS-NOT-IN-GIT.sha256` and recreated" 0.
- **F-69 (re-run record, V8, manifests).** Nothing on the verification path changed, so this session ran no checker:
  the 18 logs of F-65 record runs made on GitHub-hosted runners on 2026-10-28, and round 4's runs and the later
  batteries' re-runs on these byte-identical files stand (VERIFY.log R8.1, R8.11). `note.pdf` was rebuilt last from the
  final `note.md` by the recipe in the internal build notes (pandoc 3.10.2; Tectonic 0.17.0 with cached resources only),
  after the same tools had reproduced round 7's `note.tex` byte for byte, and checked by text extraction: 17,024
  normalised characters, 0 differing blocks, all thirteen symbol counts equal, title and author metadata present, 7
  pages (VERIFY.log R8.10). The priority-word scan (R8.6), the propagation grep (R8.7), the marker sweep (R8.8) and the
  §9b scan of every added line (R8.9) ran on the final files. `SHA256SUMS` now lists 174 files, the 18 logs among
  them; both manifests were rebuilt last.

## 2026-10-29, round 9 (seventh revision session, acting on the two findings of the sixth independent battery's report on round 8; build record, not a gate verdict, §17)

Propagation counts below are from round 9's whitespace-normalised, case-insensitive grep (VERIFY.log, round-9 section
R9.4), over the same file groups as rounds 3 to 8; "outside FIXLOG" excludes this file, whose entries quote the superseded
wording, and VERIFY.log. Line numbers are those of the files at the end of round 9. Round 9 changed records and prose only:
no script, object, witness, lower-bound record, circuit text, proof, earlier file under `logs/`, `note.md` or `note.pdf`
changed.

- **F-70 (§9b redaction, the sixth battery's finding on VERIFY.log).** Round 8's §9b scan summary (R8.9, the former line
  2584) listed its scan groups by name, and one name stated the subject of a lane of work that is not part of this release,
  which PROTOCOL §9b keeps off a public surface. The name was replaced in place by a neutral group label, `sibling-internal`,
  of the same generic form as the group labels `internal-labels` and `other-lanes`; the superseded name is recorded in the
  internal build notes, not in any shipped file. `VERIFY.log` is append-only, so this is an in-place redaction like round 4's
  (R4.9): the change is inside round 8's own appended region, and every byte written before round 8 (221,009 bytes) is
  unchanged. The round-9 `VERIFY.log` section R9.2 gives the before and after SHA-256 and the single changed line, and
  README's `VERIFY.log` note is extended to name the relabel (README.md:466–471). Propagation outside FIXLOG: the superseded
  group name 0 in shipped files, `logs/`, VERIFY.log and the PDF text (it is a §9b subject label, recorded in the internal
  build notes); `sibling-internal` is not a priority word and matches no marker pattern.
- **F-71 (CLAIM record, the sixth battery's finding on PROVENANCE.md).** The timeline row for Oct 28–29 (PROVENANCE.md:25)
  stated two of the three arXiv-coverage facts the lead's ruling requires. It now carries the third as well: the submissions
  received from 14:00 EDT on Oct 27 to 14:00 EDT on Oct 29, announced on Oct 29 at 20:00 EDT, are not covered, with arXiv's
  status page and SWEEP-RECORD §7.8 cited. The row now gives the same three facts as SWEEP-RECORD §7.6 and §7.8 (F-64), and
  the internal build notes' statement that every place stating arXiv coverage gives the same three facts holds again.
  Propagation outside FIXLOG: a clause addition, so no superseded phrase.
- **F-72 (record: the round-label note, V8, manifests).** README's "What was re-run" section gains a round-9 paragraph
  (README.md:213–218), and its `VERIFY.log` transcript list now reads "rounds 2, 3, 4, 5, 7, 8 and 9 in that order"
  (README.md:465), because round 9 appends a transcript section to `VERIFY.log`. No file on the verification path, `note.md`
  or `note.pdf` changed, so this session ran no checker, and V8 stands as round 8 recorded it (R8.10; `note.pdf` is
  byte-identical). `SHA256SUMS` was rebuilt because `README.md` and `VERIFY.log` changed, and it is the last shipped file
  written (VERIFY.log R9.1, R9.6). Propagation outside FIXLOG: "rounds 2, 3, 4, 5, 7 and 8" 0.
