# Novelty sweep record — circuit-level distances of the Kishony–Fowler colour-code circuit (as of 2026-10-20; re-checked as of 2026-10-29, §7)

**As of: 2026-10-20, 19:45 UTC, for §1, §2 and §4–§6; 2026-10-29, 00:50 UTC, for §3 and §7, with
arXiv covered through its mailing of 2026-10-28 (§7.8).**
Every "not found" below holds only up to its time, and only for the sources listed. This record
consolidates three sweeps run under PROTOCOL §8 (primary sources read in full), dated 2026-09-01,
2026-10-07 and 2026-10-20, the round-7 re-check of 2026-10-27 and 2026-10-28 (§7) and its update of
2026-10-29 (§7.8), whose arXiv coverage ends earlier (§7.1, §7.8). Line numbers are `file:line` in
the stored source files.

*Revision of 2026-10-20 (later the same day).* After the first independent battery, §2(a), §2(c)
and §3 were corrected and the sources re-read for that are listed at the end of §4. No new
external search was run, so the as-of time above is unchanged. A later revision (round 3) added
the §2(a) line on qsim-lab's d = 13 figure, from the stored copies; again no new search was run.
Round 4 corrected the commits named for the Jaspersands lines (§2(c), §5); round 5 read the files
cited in full and moved the entry to §4. Both used stored copies; no external search or download was run.
Round 7 (2026-10-28) re-checked §3 against what was published after 2026-10-20 (§7). It marked
§2(c)'s verdict as superseded, updated the Pan entry there, rewrote §3, noted two §6 items as
re-checked, and added §7.
Round 8 (2026-10-29) added §7.8, moved the as-of date of §3 and §7 to 2026-10-29 (with §7.1's
coverage line, §7.2's heading, §7.6's gaps and §7.7's list), and corrected the range of equality
in §3's not-permitted list (d ≤ 8).

## 1. Statements under sweep

Each statement concerns C(d, r): the circuit returned by `build_parallel_circuit` of the
companion code of arXiv:2603.28852 (Classiq/classiq-library a43d3bd4), with schedule row 1,
DEPOLARIZE2 after every CNOT and Z-basis memory.

- **S1.** d_circ(C(13, r)) = 11 and d_circ(C(15, r)) = 12 for r = 1 and r = d.
- **S2.** The formula d − ⌊(d+3)/6⌋ holds at d = 15, the first d at which ⌊(d+3)/6⌋ = 3.
- **S3.** Each value at d = 3, …, 15 carries a checkable proof of its lower bound (an LRAT
  refutation, replayed by a standard-library checker and, at d = 15, by drat-trim's
  `lrat-check`), together with an explicit fault set for its upper bound.

## 2. Verdicts

**(a) Values for this circuit.**
- **d = 13.** The authors state that their formula holds numerically up to d = 13
  (arXiv:2603.28852v1 §II, main.tex:201: "we verify numerically that, up to d=13, …"). That
  sentence gives d_circ = 11 at d = 13. It gives no per-d values beyond the formula, and no method,
  round count or noise model. qsim-lab reads it the same way: "K–F's formula is their numerical
  observation for d ≤ 13" (research/theory/theory-colour.md:269). No independent computation and no
  checkable proof at d = 13 was found.
- **d = 15.** No source read reports a circuit-level distance for C(15, ·).
- **The authors' asymptotic argument.** Just before that sentence they derive that the
  circuit-level distance along the boundaries is "asymptotically reduced by a factor of 5/6"
  (main.tex:199–200). A value at d = 15 tests that argument beyond their numerical range.
- The largest independent values found are qsim-lab's: d = 9 at rounds = d (value 7) and d = 11
  at one round (value 9), posted 2026-10-04 (research/qec/qec-r4.md:223–230).
- At HEAD 682845a (2026-10-11), qsim-lab still lists its d = 13 run of this circuit as "still
  running" (research/theory/theory-colour.md:315). Separately, it records its d = 13 search of the
  authors' schedule space as unresolved (research/qec/colour-global.md:212). These blobs are
  identical to the 2026-10-07 reads.
- qsim-lab's colour-global.md gives the authors' schedule the value 10 at d = 13, as an evaluation
  of d − ⌊(d+3)/6⌋ (:11; also :212). The formula evaluates to 11 there, and qsim-lab's own d = 13
  run of this circuit is listed as still running (theory-colour.md:315), so no computed value is
  reported there.

**(b) The formula.**
- No source proves or refutes d − ⌊(d+3)/6⌋.
- qsim-lab reproduces it numerically at d = 3–9 (rounds = d) and d = 11 (one round)
  (qec-r4.md:24). It states that no general lower bound is known (theory-colour.md:268–269), and
  it proves the corner bound d_circ ≤ d − 1 for every single-auxiliary schedule
  (theory-colour.md:11).
- No source tests the formula at d = 15.

**(c) Checkable proofs of colour-code circuit-distance lower bounds.** No proof object (LRAT,
DRAT or formal) was found. The nearest items are listed below. *(As of 2026-10-20. Superseded in
round 7: Crocker's record of 2026-10-25 has a DRAT proof for the extended-code step of a lower
bound for another schedule of the same family, C9, at d = 9; §7.3.)*
- **Shutty's bundle** (doi:10.5281/zenodo.22820614, for arXiv:2609.21376): `distance/check.py
  --small` is a re-runnable, Stim-based exhaustive check that reproduces 12 exact small-instance
  lower bounds, triangular d = 3 and torus d = 4, for a native-CZ 4.8.8 circuit
  (distance/README.md:19–21, 51–61). It is a re-runnable search that trusts Stim, not a proof
  object, and the larger lower bounds are outside the bundle (:21–23).
- **qsim-lab:** DRAT-checked UNSAT certificates. These show that no schedule in a stated design
  space reaches a stated distance at one round. They are upper bounds over schedules, conditional
  on an empirically validated symbolic model (colour-global.md §3).
- **Lean-kernel-checked distances:** QECCertificates, arXiv:2610.04306, arXiv:2610.03214 and
  Lean-QEC. These cover static codes and phenomenological or timelike fault models, not
  gate-level colour-code circuits.
- **Exact colour-code circuit distances without a shipped proof of the lower bound:**
  - arXiv:2412.14256, superdense circuit, MaxSAT, d ≤ 7;
  - arXiv:2604.09797, morphing circuits, Gurobi, d ≤ 9;
  - arXiv:2609.21376, a 4.8.8 circuit with shared auxiliaries, d = 3, 7, 11, 15. Its lower-bound
    method is not named, and its bundle reproduces lower bounds only for small instances (above);
  - github.com/Jaspersands/quantum-simulator-qec, by integer program. At commit 8e2eb07
    (2026-10-07): Stim's XYZ colour-code memory at d = 3 and 5 (CHANGELOG.md:29–34). In the
    README read at commit 899df56 (2026-10-20; the README is byte-identical at 49e6253 of
    2026-10-19): also d = 7, and a generic 6.6.6 schedule at d = 3, 5 (README.md:1876–1885,
    1893–1897). When d = 7 was added between 8e2eb07 and 49e6253 was not determined. Its
    "certificates" are decoder-conformance checks (tools/verify_certificates.py:1–10 at
    899df56; the file is not in 8e2eb07).
- **Proof-carrying circuit distances for non-colour codes.** These rule out any unqualified
  "first proof-carrying circuit distance" claim:
  - **Kornstein**, doi:10.5281/zenodo.23394575 (2026-10-15): [[72,12,6]] depth-8 cycle,
    d_circ = 6, backed by "120 block CNFs … DRAT VERIFIED" (depth8_cycle/DERIVATION.md:222). For
    the gross code, d_ext and the candidate lists rest on enumerators
    (depth8_cycle/DERIVATION.md:229; depth8_cycle_independent_checks/REVIEW.md:97–98). His §3b
    key check and "Lemma 3 (projection)" (depth8_cycle/DERIVATION.md:161–165; on SBB's Prop. 3,
    :54–59) are the same projection argument as our Hypothesis B, for bivariate-bicycle cycles;
    the note and README credit it.
  - **Pan**, github.com/GavinNull/gross-code-distance-12 (created 2026-10-13). Release v1.0
    (2026-10-20, a period-18 circuit): DRAT-certified lift steps; in v1.0 its d_ext and list of
    weight-11 logicals rest on searches (release/arxiv/main.tex:613–615, 1089–1091). It cites
    Kishony–Fowler only as a precedent for check-dependent orders (main.tex:92–93).
  - **Pan, later (read in round 7, §7.4).** Release v2.0 (2026-10-24) supersedes v1.0: circuits
    of period 11 with circuit distance 12 for the gross code and 10 for [[90,8,10]], with VeriPB
    proofs for d_ext and for the completeness of the logical lists, and DRAT proofs, checked by
    drat-trim and `cake_lpr`, for the lifts (v2.0 release notes; paper/draft.tex:262–267).
    Experiment E-037 (2026-10-25) adds VeriPB-checked lower bounds of 10 for IBM's depth-8
    gross-code cycle for every number of rounds up to 12, in both bases; its certificates are
    regenerable from the public code and are not in the repository
    (research/journal/2026-10-25-E-037-ibm-cert.md:1–11; paper/draft.tex:62–65, :899–905). The
    v2.0 draft still cites Kishony–Fowler only for check-dependent orders (paper/draft.tex:120–121).

## 3. Permitted sentences

These are the 2026-10-29 forms (round 8, §7.8), worded as the 2026-10-28 forms of round 7 (§7).
Those replaced the 2026-10-07 forms and the 2026-10-20 forms (FIXLOG F-23, F-24, F-53, F-54):
Crocker's record of 2026-10-25 contradicts the third 2026-10-20 item (§7.3), and the program's
wording rule (PROTOCOL §9) does not allow its "first".

**Record form.** Not found in the sources read, as of 2026-10-29 (§4, §7.4, §7.8):
- a circuit-level distance for the Kishony–Fowler single-auxiliary colour-code circuit at d = 15,
  or any test there of d − ⌊(d+3)/6⌋, whose loss term first equals 3 at d = 15;
- an independent computation, or a checkable proof, of that circuit's distance at d = 13. The
  authors state that the formula holds numerically up to d = 13 (main.tex:201), which gives 11 at
  d = 13, with no per-d values, round count or method;
- a checkable proof (an LRAT, DRAT or formal proof object) of a lower bound on the circuit
  distance of any circuit with the authors' schedule S₀, at any d, or of any colour-code
  syndrome-extraction circuit at d ≥ 11. The nearest items are Crocker's DRAT proof for the
  extended-code step of a lower bound for another schedule of the family, C9, at d = 9 (§7.3), and
  Shutty's re-runnable, Stim-based exhaustive check of small-instance lower bounds (§2(c)).

**Note-ready form.** d_circ = 12 at d = 15 (rounds = d and rounds = 1). The lower bound is an
LRAT refutation of every fault set of weight ≤ 11, accepted by drat-trim's `lrat-check` and by a
standard-library checker that regenerates the CNF. The upper bound is an explicit weight-12 fault
set. Not found in the sources read, as of 2026-10-29:
- a circuit-level distance for this circuit at d = 15, or any test there of the authors' formula,
  whose loss term reaches 3 at d = 15;
- an independent computation, or a checkable proof, of this circuit's distance at d = 13, where
  the authors state that the formula holds (main.tex:201) but give no per-d value, round count or
  method;
- a checkable proof (an LRAT, DRAT or formal proof object) of a lower bound on the circuit
  distance of any circuit with the authors' schedule, at any d, or of any colour-code
  syndrome-extraction circuit at d ≥ 11.

**Conditions on these sentences.**
- Each "not found" sentence carries its as-of date and points to the sources read in full (§4,
  §7.4, §7.8). The date stays 2026-10-29 until a later re-check has read the arXiv mailings after
  that of 2026-10-28 (§7.6, §7.8).
- The third item must keep the words "lower bound", the parenthetical "(an LRAT, DRAT or formal
  proof object)" and both of its limits, "any circuit with the authors' schedule" and "at
  d ≥ 11". qsim-lab has DRAT-checked upper bounds over the Kishony–Fowler schedule space;
  Shutty's bundle has a re-runnable lower-bound check that is not a proof object; Crocker has a
  DRAT proof for the extended-code step of a lower bound for C9 at d = 9.
- Wherever the "not found" list appears, Crocker's C9 proof and Shutty's small-instance check are
  credited next to it.
- The values at d ≤ 11 must be credited as reproductions of qsim-lab: rounds = d at d = 3–9, and
  one round at d = 5–11. qsim-lab's are "the earliest independent values found in the sources
  read, as of 2026-10-29", never simply "the first". Crocker's values for the Kishony–Fowler rule
  (d = 3–9) and Issa–Martonosi's d − 1 upper bounds (d = 7, 9, 11) are credited as later
  independent results on the same CNOT schedule.
- The statement that the circuit avoids all malign hook errors in the bulk is reported as the
  authors', with Issa–Martonosi's counterexample next to it.

**Not permitted.** Each item is contradicted by a source read.
- "First proof-carrying, certified or machine-checked circuit-level distance of any
  syndrome-extraction circuit": Kornstein (2026-10-15), Pan, qsim-lab, Crocker (2026-10-25).
- "First circuit distance of a single-auxiliary colour-code circuit": Kishony–Fowler,
  qsim-lab, Jaspersands, Crocker.
- "First independent test or reproduction of the formula" for d ≤ 11: qsim-lab, 2026-10-04.
- "First colour-code circuit distance at d = 15": arXiv:2609.21376, a different 4.8.8 circuit.
- "Every prior circuit-distance value is a heuristic upper bound": exact values exist
  (2606.20263, 2609.39522, 2610.03429, 2609.18922, qsim-lab, 2412.14256, 2604.09797, Jaspersands).
- "Kishony–Fowler verified to d = 13 by ILP": their paper names no method.
- "No circuit-level distance at any d ≥ 13", "the first value at d = 13", or "the authors'
  sentence gives no values": main.tex:201 states the formula, and so the value 11, at d = 13.
- "None of the other colour-code circuits ships a checkable lower-bound check" without the
  proof-object qualifier: Shutty's bundle ships a re-runnable small-instance check. With the
  qualifier, "none of the other colour-code circuits has a checkable proof of its lower bound":
  Crocker's C9 (§7.3).
- "First checkable proof of a colour-code circuit distance", or of a colour-code
  circuit-distance lower bound: Crocker, doi:10.5281/zenodo.23633600 (2026-10-25), C9 at d = 9
  (§7.3).
- The 2026-10-20 third item, that "a checkable proof (an LRAT, DRAT or formal proof object) of a
  lower bound on, or the exact value of, the circuit distance of any colour-code
  syndrome-extraction circuit" was not found, in any form without the two limits above: the same
  record.
- That Crocker's DRAT proof covers the circuit step or every number of rounds, or that his record
  stores it: it covers the extended-code step d_ext(C9) ≥ 8; the record ships the CNF, and its
  script regenerates the proof, checks it and deletes it; the circuit step is a Stim-based check
  at R = 1–5, 9 and 25 plus a hand lemma in a note that is not in the record (§7.3).
- That Crocker's values for the Kishony–Fowler rule carry a proof object: they come from
  exhaustive search and Stim-based checks (§7.3).
- That Crocker computed this circuit, or "the same circuit": he uses the same CNOT schedule in his
  own construction, whose builder, order of halves, noise, observable and detectors differ (§7.3).
- That the circuit "avoids malign hook errors in the bulk", as a fact rather than as the authors'
  statement: Issa–Martonosi, arXiv:2610.33347v1 (main.tex:88–89, :237–247).
- That junction hook errors bring the distance below d − ⌊(d+3)/6⌋, or that their d − 1 sets are
  below the formula's value: d − 1 ≥ d − ⌊(d+3)/6⌋ for every d ≥ 3, with equality for d ≤ 8 (of
  the sizes Issa and Martonosi checked, at d = 7), and Issa–Martonosi say that the junction hook
  errors leave the reported distance unchanged (arXiv:2610.33347v1, main.tex:265–268).
- That Pan's d_ext and logical lists rest on searches, for his current release: true of v1.0;
  since v2.0 (2026-10-24) they carry VeriPB proofs for his period-11 circuits (§2(c)).
- "DRAT-checked circuit distances for bivariate-bicycle cycles" without naming [[72,12,6]] as the
  case checked end to end: Kornstein's larger codes rest in part on enumerators
  (depth8_cycle/DERIVATION.md:229).
- That the projection check (Hypothesis B) is new: Kornstein's §3b makes the same check for
  bivariate-bicycle cycles (depth8_cycle/DERIVATION.md:161–165).
- That the extended-code reduction, or its use as a lower-bound route, is new. It is
  Strikis–Browne–Beverland's. Pan uses it, and credits its use for screening schedules to
  arXiv:2608.19917 (Pan, v1.0, main.tex:90–91); Crocker uses it for C9 (§7.3).

**Not permitted by the wording rule (PROTOCOL §9).** "First", "new", "novel", "earliest" or "only"
as a priority claim about this package's results, in particular the 2026-10-20 note-ready forms
"the first test of the authors' formula at d = 15" and "the first independent computation of the
value and the first proof of it" at d = 13. The permitted form is "not found in the sources read,
as of <date>", with the sources listed.

## 4. Sources read in full

### Sweep of 2026-09-01

Every source below was fetched as its arXiv LaTeX source and read completely.
- **The target paper:** arXiv:2603.28852v1 (Kishony, Fowler).
- **The companion code**, read file by file: `benchmark_circuits.py`,
  `exhaustive_schedule_search.py`, `generate_zero_collision_schedules.py`,
  `ilp_circuit_distance.py`, README, results CSVs.
- **The target's citers:** 2607.05501v1 and 2605.03180v2.
- **Other papers:** 2412.14256, 2603.22532v2, 2605.16523v1, 2604.09797v2, 2603.05481v1,
  2602.09099v1, 2607.28504v1, 2607.01473v1, 2601.17580v1, 2601.12509v2, 2312.08813v1,
  2511.15177v1.

### Sweep of 2026-10-07

**Read by the sweep lead:**
- qsim-lab at b5f4b289: research/qec/qec-r4.md, research/qec/colour-global.md,
  research/qec/colour-flags.md and research/theory/theory-colour.md. Also tests/qec/color_code.rs
  (l.148–182), RESULTS.md §3 and research/process/audit.md §16;
- arXiv:2603.05481v2, all .tex files, with the v1 diff;
- QECCertificates: README.md and paper/main.tex;
- the arXiv:2609.21376 bundle: distance/README.md.

**Read by dedicated readers, every line of the e-print source:**
- 2609.03048, 2609.21376, 2610.05928, 2609.02428, 2609.37231, 2610.04306, 2610.03429;
- 2606.12445, 2606.20263, 2606.25330, 2610.06749, 2610.03682;
- 2609.17706v3, 2609.16929, 2609.18922v3;
- 2603.01628, 2609.26736, 2609.39758, 2609.39522v2, 2609.16159;
- 2610.03920, 2609.12020, 2608.11516v1, 2605.30455;
- 2606.06365v2, 2605.11318v2, 2609.26973, 2609.40319, 2606.03507;
- 2603.05496, 2603.05402v2;
- 2610.03214 v1 and v2, and 2610.03594.

### Sweep of 2026-10-20

**Read in full:**
- arXiv:2610.24077v1 (Lavasani et al.). Colour-code memory at d = 3, 5, 7 on Helios
  (arXiv_v1.tex:98) with a SWAP-superdense circuit (:159). It gives no circuit-distance value.
- The Kornstein deposit: README, depth8_cycle/DERIVATION.md and
  depth8_cycle_independent_checks/REVIEW.md.
- Pan, release/arxiv/main.tex.

**Read in full in round 5, from copies already stored (nothing was fetched):**
- github.com/Jaspersands/quantum-simulator-qec, cited in §2(c) and §3. At commit 899df56 (the
  clone of 2026-10-20): README.md, all 2,718 lines, byte-identical at commit 49e6253;
  tools/verify_certificates.py, all 71 lines, also identical at 49e6253; tools/distances.py and
  data/distances.json, from which the README's distance table comes (README.md:1866–1889); and
  src/generated.rs, Stim's generated memories as the repository writes them. At commit 8e2eb07:
  CHANGELOG.md, all 407 lines.
- On colour codes, the repository's exact circuit distances are integer-program optima (scipy's
  HiGHS), called proven when the program finishes (README.md:1855–1857): 2, 3, 4 at d = 3, 5, 7
  for Stim's XYZ memory, which in the repository's copy of Stim's generator has one auxiliary
  qubit per check (src/generated.rs:496–539), and 2, 3 at d = 3, 5 for the generic 6.6.6
  schedule (README.md:1876–1878, 1883–1884). Its CHANGELOG at commit 8e2eb07 says the graph-like
  search (faults of at most two detectors) matches Stim's lengths on Stim's generated colour codes
  up to d = 15 (CHANGELOG.md:20–25); it states no value.
- No proof object is in the repository's clone: a word-bounded search of all its files for LRAT,
  DRAT, FRAT and VeriPB (any case) and Lean found none, and it holds no .lrat, .drat, .frat, .pbp,
  .lean or .cnf file. The README's file list calls tools/verify_certificates.py "the distance
  certificates checked independently" (README.md:2614); the script checks decoder-conformance
  certificates (tools/verify_certificates.py:1–10), as §2(c) says.

**Re-read in the revision of 2026-10-20 (stored copies):**
- arXiv:2603.28852v1 main.tex, in full (e-print SHA-256 `ccc781db…`), for the asymptotic argument
  at :199–200 and the d = 13 sentence at :201.
- Kornstein, depth8_cycle/DERIVATION.md, in full; depth8_cycle_independent_checks/REVIEW.md:93–100.
- Shutty's bundle (doi:10.5281/zenodo.22820614), distance/README.md, in full.
- qsim-lab at b5f4b289, research/theory/theory-colour.md:1–15, 262–280 and 312–318.

**Re-checked against the 2026-10-07 reads:**
- qsim-lab HEAD 682845a. The colour-code files are blob-identical to b5f4b289, and the only qec
  changes are a `wilson_interval` fix and API documentation.
- QECCertificates, identical to its v0.3.0 tag.
- The versions of 18 earlier sources. 2603.28852 is still v1 only; 2603.05481 is still v2.

## 5. Screened, not read in full

**arXiv listings, 2026-10-07 to 10-19.**
- quant-ph and cs.IT: 1,079 records; 147 QEC-related by abstract.
- Full source text was screened for 190 e-prints, 51 of which mention colour codes. The screen was
  a keyword-in-context pass for circuit-distance, colour-code and certificate terms.
- Notable: 2610.14778, 2610.06730, 2610.03429v2, 2610.04306v2, and cultivation and factory papers
  (2610.06828, 2610.10731, 2610.20591, 2610.22315).
- None reports a value for this circuit or a colour-code circuit-distance lower-bound proof.

**Zenodo.**
- Crocker, doi:10.5281/zenodo.23452754 (2026-10-18): gross code only, search-based. A grep of all
  194 files found no colour-code term.
- Kulkarni, doi:10.5281/zenodo.22842236: a transfer circuit; distance by enumeration; not this
  circuit.

**Repositories.**
- QEC-pages/dist-m4ri: its benchmark has no colour code and it produces no proof object.

**Citation graphs.**
- Citers of 2603.28852: Semantic Scholar lists 2607.05501 and 2605.03180; Google Scholar lists
  2609.03048; OpenAlex lists none. All three were read in full earlier.

**Unchanged:** Error Correction Zoo colour pages, the Kishony–Fowler authors' repositories, and
the Classiq error_correction folder.

## 6. Gaps

- 49 colour-code-mentioning e-prints of the 10-20 window were screened, not read line by line.
- **Crocker, doi:10.5281/zenodo.23489148** ("Certified syndrome-extraction schedules for 4D
  geometric codes", 2026-10-20). Its files are embargoed until **2026-10-26**; only the metadata
  was read. The description says "search-based results" with "fault-set witnesses". *(Round 7:
  its concept now has a v2.0 on 4D geometric codes with no colour-code term; §7.3.)*
- The arXiv API cannot filter by update date, so replacements were covered only by the version
  checks above.
- Papers submitted on 2026-10-20 were not yet announced.

**Re-check before any public statement made after 2026-10-20:** the Crocker record, qsim-lab
HEAD, and arXiv listings from 2026-10-20 on. *(Done in round 7, §7; the list for statements made
after 2026-10-29 is §7.7.)*

## 7. Round 7 re-check (2026-10-27 and 2026-10-28)

### 7.1 What was checked, and when

Two read-only sessions re-checked §3 against what was published or changed after 2026-10-20.
Nothing was posted or uploaded, and no downloaded code was run.
- **Recency check, 2026-10-27, 22:32–23:07 UTC** (110 requests, all answered). DataCite and
  Zenodo: records created since 2026-10-20, searched by topic and by the names Crocker, Kornstein,
  Pan and Kishony, and the versions of the Crocker and Kornstein records cited here. GitHub: the
  repositories named in §2, §4 and §5, and seven repository searches. arXiv: the quant-ph
  submissions from 2026-10-20 on (386 entries, plus 2 from keyword queries in other categories),
  keyword, replacement and author queries, the versions of 31 cited papers, and the mailing page
  of 2026-10-27.
- **Sweep, 2026-10-28, 00:55–01:25 UTC** (43 requests). Crocker's record
  doi:10.5281/zenodo.23633600, read in full (§7.3); the changes since the recency check (DataCite
  by name; Pan's and qsim-lab's repositories). The arXiv mailing of 2026-10-28 was not obtained
  (§7.6).
- **arXiv coverage.** New submissions announced up to the quant-ph mailing of 2026-10-27, i.e.
  received before about 2026-10-26 18:00 UTC. §7.8 extends it through the mailing of 2026-10-28,
  i.e. to submissions received before about 2026-10-27 18:00 UTC.
- The round-7 builder re-read the cited lines below from the stored copies; the edits are FIXLOG
  F-53 to F-59.

### 7.2 Verdicts as of 2026-10-28, 01:25 UTC (re-dated to 2026-10-29 in §7.8)

| statement | status | deciding sources |
|---|---|---|
| S1: d_circ 11 at d = 13 and 12 at d = 15 | not found elsewhere | Crocker 23633600 states nothing for d ≥ 11; Issa–Martonosi stop at d = 11; qsim-lab is unchanged; nothing else in the window (§7.3, §7.5) |
| S2: the formula at d = 15 | not found elsewhere | the same |
| d = 13: an independent computation or a checkable proof | not found elsewhere | the same |
| §3's 2026-10-20 third item (any colour-code circuit) | contradicted | Crocker 23633600, 2026-10-25 (§7.3) |
| third item narrowed: any circuit with the authors' schedule, any d | not found | Crocker's values for the authors' rule carry no proof object; Issa–Martonosi give upper bounds and integer-program values; qsim-lab's DRAT statements are upper bounds over schedules |
| third item narrowed: any colour-code circuit at d ≥ 11 | not found | Crocker excludes d ≥ 11; Shutty's lower bounds at d = 11 and 15 name no method (§2(c)) |
| S3 | describes this package | — |

### 7.3 Findings, source by source

**Crocker, doi:10.5281/zenodo.23633600** (v1.0, created 2026-10-25T04:54:45Z, CC BY 4.0; "A d = 9
single-auxiliary colour-code schedule with circuit distance d - 1: reproducibility package"). Its
concept, doi:10.5281/zenodo.23633599, has this one version. The record holds README.md,
HAND_CHECK.md, SHA256SUMS.txt and colour_c9_pack_v1.0.zip; the 34 SHA-256 the zip lists all match.
The paths below are inside the zip, whose top directory is colour_c9_pack/.
- **Claim.** In Crocker's reconstruction of the Kishony–Fowler family (one bare auxiliary per
  plaquette, X half then Z half, uniform depolarising noise on every location), the schedule C9
  has circuit distance exactly 8 = d − 1 at d = 9, for every number of rounds, in Z and X memory
  (colour_c9_pack/README.md:8–11).
- **Lower bound, extended-code step.** C9's extended code has 127 distinct nonzero columns, and no
  7 of them sum to the logical: by exhaustive search, and by a DRAT proof. The checker compares
  the shipped CNF certificates/C9_ext_le7.cnf with one regenerated from the 127 columns; with
  `RUN_DRAT=1` it has kissat write a proof to a temporary file, drat-trim check it, and then
  deletes it (colour_c9_pack/check_full.py:179–196). The record's clean-run transcript shows kissat
  UNSATISFIABLE in 151 s and drat-trim VERIFIED in 65 s (colour_c9_pack/CLEAN_RUN.txt:50–57). No
  DRAT, LRAT or other proof file is in the record.
- **Lower bound, circuit step.** Stim's detector-error-model images of every single fault are
  checked against the 127 columns at R = 1, 2, 3, 4, 5, 9 and 25 in both bases; the step to every R
  is a hand lemma in the companion note (colour_c9_pack/README.md:10–11), which is not in the
  record. The record says its lower bound rests on Stim's detector error model and on numpy
  (colour_c9_pack/README.md:79–80). Earlier DRAT-checked lower bounds at R = 1 by other verifiers
  are described but not shipped (colour_c9_pack/README.md:74–79).
- **Upper bound.** An 8-fault witness, 3 hooks and 5 data faults, also checkable by hand
  (colour_c9_pack/HAND_CHECK.md).
- **The authors' colour rule.** Re-extracted from the authors' published d = 5 circuit; extended-code
  distances 2, 4, 6, 7 at d = 3, 5, 7, 9 by exhaustive search; at d = 9, for R = 1 and 3, both
  orders of the halves and both bases, the single-fault images are columns and a 7-fault witness
  flips the logical, so circuit distance 7 (colour_c9_pack/check_kf.py:8–15). No proof object
  covers the rule at any d.
- **Not claimed.** d ≥ 11; the authors' generator was not run (colour_c9_pack/README.md:20–22).
  Every computation loops over d in {3, 5, 7, 9} only (colour_c9_pack/check_kf.py:86).
- **Same schedule, another circuit.** The record's rule is our S₀. Compared by our own text-only
  script: the authors' published five-round d = 5 circuit, as the record ships it, equals our
  `certs/c_d5_r5.stim` in its qubit coordinates, all 60 CX layers and every DETECTOR,
  OBSERVABLE_INCLUDE and SHIFT_COORDS line, apart from noise placement and one extra final ancilla
  reset; at d = 9 the record's rule on its lattice gives the same CNOT order and layers as our
  `certs/c_d9_r1.stim` on all 30 plaquettes. Crocker's circuits differ from ours in builder, order
  of halves, noise, observable (Z^n or X^n on all 61 data qubits) and detectors
  (colour_c9_pack/MAPPING.md:35–42). His value 7 for the rule at d = 9 agrees with ours.
- **Effect.** It contradicts §3's 2026-10-20 third item. It does not touch d = 13 or 15.

**Crocker, concept doi:10.5281/zenodo.23489147.** Version 0.1, 23489148 (§6), is superseded by
v2.0, 23690807 (2026-10-27), whose paper Crocker_4D_schedules.pdf is on 4D geometric codes and has
no colour-code term. The v0.1 files and the v2.0 data zip were not read. No effect.

**Issa and Martonosi, arXiv:2610.33347v1**, "Junction Hook Errors in the Color Code" (submitted
2026-10-23, announced in the mailing of 2026-10-27; its e-print's main.tex, 25,852 bytes;
paraphrased, as its licence was not checked).
- Their schedule is the one provided with the authors' circuits, with the R, G, B orders of S₀
  (arXiv:2610.33347v1, main.tex:119–123).
- On every non-corner plaquette, bulk included, one weight-2 "junction" hook error and d − 2 data
  errors form an undetected logical error of d − 1 faults. They checked this at d = 7, 9 and 11,
  and by fault injection with Stim in the authors' circuits (arXiv:2610.33347v1, main.tex:31–32,
  :88–89, :203–209).
- This is a counterexample to the authors' statement that, away from the corners, no single hook
  error alone reduces the distance (arXiv:2603.28852v1, main.tex:196), and it qualifies their
  statement that all malign hook errors are avoided in the bulk (arXiv:2603.28852v1, main.tex:61).
- With noise only after the bulk CNOTs and once per round on the data qubits, the companion
  integer program gives 6 at d = 7 and 8 at d = 9 (arXiv:2610.33347v1, main.tex:242–247).
- The junction hook errors leave the distance the authors report unchanged; for d ≥ 9 the further
  loss comes from the boundary (arXiv:2610.33347v1, main.tex:265–268).
- No value at d = 13 or 15, and no proof object. In their repository's file tree, the data files
  that name a distance are for d = 7 and 9 (only the tree was read, §7.5).
- **Effect.** A background sentence of the note (FIXLOG F-55), and a later independent result on
  the same schedule.

**Pan.** Release v2.0 (2026-10-24) and experiment E-037 (2026-10-25), as in §2(c). On 2026-10-28
the main branch was unchanged since commit 1f9757458f (2026-10-27) and the releases were
unchanged. No colour-code work. **Effect.** A credit update (FIXLOG F-56).

**qsim-lab.** Unchanged since 682845a (2026-10-11): the comparison with main is identical, and
every branch is at its 2026-10-20 commit. Its d = 13 run of this circuit is still listed as running
and is unposted.

**Unchanged since this record's reads.** Kornstein 23394575 and Crocker 23452754, one version
each, the latter's description still calling it search-based; arXiv:2603.28852 still at v1 and
arXiv:2603.05481 still at v2; QECCertificates (tags to v0.3.0), Lean-QEC, dist-m4ri and the Classiq
error_correction folder, with no commits. Jaspersands/quantum-simulator-qec has 165 commits since
the 2026-10-20 clone; its circuit-distance section changed by one paragraph on memory use, and
data/distances.json is byte-identical, so §2(c) and §4 stand.

### 7.4 Sources read in full in round 7

- Crocker, doi:10.5281/zenodo.23633600 v1.0: README.md, HAND_CHECK.md and SHA256SUMS.txt; in the
  zip, MAPPING.md, CLEAN_RUN.txt, requirements.txt, the checkers check_kf.py, check_c9.py,
  check_full.py and analyse_hooks.py, the library c9core.py, build/make_files.py,
  build/run_clean.sh, the six schedule tables, the six witness files,
  certificates/extended_code_C9_d9.txt and the CNF's header. The eight circuits/*.stim bodies and
  the CNF's clause body (machine data) were parsed and compared, not read line by line.
- arXiv:2610.33347v1 (Issa, Martonosi): main.tex. The figures were not opened.
- arXiv:2603.28852v1 (Kishony, Fowler): main.tex, re-read for its hook-error statements
  (arXiv:2603.28852v1, main.tex:61, :112, :184, :193–197, :247, :250).
- Crocker, doi:10.5281/zenodo.23690807: Crocker_4D_schedules.pdf.
- Pan: the v2.0 and v1.0 release notes; at commit 1f9757458f, paper/draft.tex (1,558 lines) and
  the E-037 journal.
- DataCite records and descriptions: 23633599 and 23633600; 23489147, 23489148 and 23690807;
  23452753 and 23452754; 23394574 and 23394575; 23492468.

### 7.5 Screened, not read in full

- arXiv submissions of 2026-10-20 to about 2026-10-26 18:00 UTC: the 45 QEC-related abstracts of
  388 papers; keyword queries (circuit-level distance, circuit distance, syndrome extraction,
  colour or color code, bivariate bicycle, gross code, fault distance, hook, effective distance);
  replacements by update date; the mailing page of 2026-10-27; the versions of 31 cited papers. The
  colour-code papers among them are Issa–Martonosi (read in full) and a decoder study whose abstract
  concerns decoding superdense colour-code circuits and gives no circuit distance.
- DataCite searches for Zenodo records created since 2026-10-20, by topic words and by the names
  Crocker, Kornstein, Pan and Kishony, and for Crocker, Kornstein and Pan records created or
  updated after 2026-10-27 12:00 UTC.
- GitHub: commits and releases since the last reads of the repositories named in §2, §4 and §5,
  and seven repository searches (circuit distance, circuit-level distance, colour code, color code
  quantum, gross code, bivariate bicycle, syndrome extraction), with nothing relevant beyond the
  items above.
- Crocker, doi:10.5281/zenodo.23630980 (the two-gross code; its description says upper bounds
  only): metadata.
- Jaspersands/quantum-simulator-qec at 92f5a5bd: the README's circuit-distance section, compared
  with the 2026-10-20 clone, data/distances.json, and a term search of the README.
- Issa–Martonosi's repository, github.com/SalahedeenIssa/junction_hook_errors: its file tree.

### 7.6 Gaps

- **arXiv after about 2026-10-26 18:00 UTC.** Not read in round 7. On 2026-10-28 arxiv.org still
  served the listing of 2026-10-27, and the first API request was refused (HTTP 429), so arXiv work
  stopped. *Closed through the mailing of 2026-10-28 (§7.8), which announced the submissions
  received before about 2026-10-27 18:00 UTC; the limits of that read are in §7.8. No mailing was
  issued on the evening of 2026-10-28, because of arXiv's scheduled maintenance. The submissions
  received from 14:00 EDT on 2026-10-27 to 14:00 EDT on 2026-10-29 are announced on 2026-10-29 at
  20:00 EDT (arXiv's status page, §7.8) and are not covered; that announcement, and every later
  one, must be read before any "not found" sentence takes a date later than 2026-10-29.*
- **Crocker's companion note** is not in record 23633600, so its hand lemma for every number of
  rounds was not read. It does not bear on d ≥ 11.
- No DRAT proof of Crocker's was regenerated or checked here; that needs a SAT solver.
- Not re-checked in round 7: the Kishony–Fowler authors' own repositories (their handles are not
  recorded here) and the Error Correction Zoo colour pages. *(Both checked on 2026-10-29, §7.8.)*
- 44 of the 45 QEC papers of the arXiv window were read at abstract level only; none of them
  concerns colour-code circuit distances.
- The files of Crocker's v0.1 record 23489148 were not read.
- The Zenodo records of Shutty's bundle (doi:10.5281/zenodo.22820614) and of QECCertificates
  (doi:10.5281/zenodo.23056679) were not checked for later versions; arXiv:2609.21376 is still at
  v3, and QECCertificates' GitHub tags still end at v0.3.0. *(Both checked on 2026-10-29, §7.8:
  Shutty's record has one version, and QECCertificates' Zenodo record was last updated on
  2026-10-03, before the sweep of 2026-10-07 read QECCertificates, §4.)*

### 7.7 Re-check before any public statement made after 2026-10-29

The arXiv announcements after the mailing of 2026-10-28, starting with that of 2026-10-29 at
20:00 EDT, which covers the submissions received from 14:00 EDT on 2026-10-27 to 14:00 EDT on
2026-10-29 (§7.6), new versions of the cited papers among them; qsim-lab HEAD (its d = 13 run);
Crocker's records (a colour-code result at d ≥ 11, or the companion note); Issa–Martonosi's
repository and any later version of arXiv:2610.33347; Pan's repository; the Kishony–Fowler
authors' repositories (§7.8).

### 7.8 Round 8: the arXiv mailing of 2026-10-28 and the recency list of 2026-10-29

Two read-only sessions re-checked §3 against the arXiv mailing that §7.6 left unread and against
the re-check list of §7.7 as it stood on 2026-10-28. Nothing was posted or uploaded, no downloaded
code was run, and nothing found bears on S1, S2, the d = 13 item or the narrowed third item. This
section moves the as-of date of §3 and §7 to 2026-10-29, 00:50 UTC.

**What was checked, and when.** Each class of source has its own check time.
- **The arXiv mailing of 2026-10-28.** One request for the quant-ph "new" listing at
  2026-10-28T04:14:32Z. Its heading read "Showing new listings for Wednesday, 28 October 2026": the
  mailing that announced the submissions received from about 2026-10-26 18:00 to 2026-10-27
  18:00 UTC. 137 entries: 50 new submissions, 27 cross-lists and 60 replacements.
- **The evening of 2026-10-28.** No mailing was issued. Two requests for the same listing after
  2026-10-29 00:00 UTC, at 00:18:33Z and 00:45:06Z, each with its own cache-busting query string
  and each answered by arXiv's origin server, returned the listing of 2026-10-28, byte-identical to
  the copy read at 04:14:32Z (SHA-256 `2a939331…a387`). arXiv's operational status page (heading
  "arXiv.org Operational Status"; the copy saved at 2026-10-29T00:49:52Z has SHA-256
  `30838f9e…c810`) gives the reason: scheduled database maintenance on Wednesday, 2026-10-28, and
  "No announcement Wednesday evening". It also states that the articles received and accepted from
  14:00 EDT on 2026-10-27 to 14:00 EDT on 2026-10-29 are announced on 2026-10-29 at 20:00 EDT.
  So at this section's time the mailing of 2026-10-28 was the latest one issued, and those
  articles are not covered (§7.6). arXiv requests in all: three listing requests to arxiv.org, none
  to export.arxiv.org, no e-print and no HTTP 429.
- **DataCite searches of Zenodo records**, 38 requests, 2026-10-29 00:24:26–00:25:48 UTC: the
  round-7 topic and name searches (circuit-level or circuit distance, syndrome extraction,
  colour or color code, bivariate bicycle, gross code, fault distance, hook errors, syndrome
  schedules; Crocker, Kornstein, Pan with bicycle or gross, "Guancheng Pan", Kishony; quantum error
  correction with certificate, LRAT, DRAT or VeriPB), each for records created since
  2026-10-27 22:00 UTC and again for records updated since then; and Crocker, Kornstein and
  "Guancheng Pan", created or updated since 2026-10-28 00:58 UTC.
- **DataCite version checks**, 18 requests, 00:24:22–00:29:34 UTC: Crocker 23633600 and its
  concept 23633599, 23452754 and 23452753, 23690807 with 23489147 and 23489148, and 23630980;
  Kornstein 23394575 and 23394574; Li et al. 23407242 and 23407241; 23535389, 23492468 and
  23666382; Shutty's bundle 22820614; QECCertificates 23056679.
- **Repository checks**, 104 requests, 00:27:52–00:37:41 UTC (29 to the GitHub API, among them the
  Kishony–Fowler authors' profiles and repository lists, and 75 raw files, most of them
  qldpc-challenge files changed on 2026-10-28): Pan's repository (compare with `1f9757458f`,
  releases, branches), qsim-lab (compare with `682845a`, branches), Jaspersands, the Classiq
  error_correction folder and its history since `a43d3bd4`, dist-m4ri, QECCertificates (commits,
  tags), Lean-QEC, BivariateBicycleCodes, tesseract-decoder, qiskit-qec, Li et al.'s repository,
  unitaryfoundation/qldpc-challenge and Issa–Martonosi's repository, each as commits since
  2026-10-27 22:00 UTC or as a comparison with the state read last.
- **Repository searches**, 9 requests, 00:30:20–00:31:20 UTC, at least 7 s apart: the seven of
  §7.5 for repositories pushed since 2026-10-27, and user searches for Kishony and Austin Fowler.
- **Error Correction Zoo**, 5 requests, 00:32:24–00:32:30 UTC: the pages color, 2d_color,
  triangular_color and 488_color, and one guessed page name, which does not exist (HTTP 404).

Every other request was answered with HTTP 200; there was no 403, no 429 and no bot page.

**Findings, source by source.**
- **arXiv, the mailing of 2026-10-28.** On 2026-10-28 a term scan of every entry's title, authors
  and abstract (colour or color code, circuit distance, circuit-level, Kishony, Fowler, hook,
  syndrome extraction, bivariate, gross code, BB code, fault distance, effective distance,
  stabiliser or stabilizer code, surface code, qLDPC or LDPC, error correction, fault tolerance,
  decoder or decoding, the names Crocker, Pan, Kornstein, Issa, Martonosi and Shutty, DRAT, LRAT,
  VeriPB, proof certificate and certification words) hit 18 entries. Seven hit only through "drat"
  inside other words; the full abstracts of the other eleven were read. On 2026-10-29 a stricter
  scan, which anchors each term at the start of a word and adds fault-tolerant, satisfiability,
  MaxSAT, proof-carrying, machine-check and plaquette, was run on the saved entries: 20 hits, the
  eleven among them. The full abstracts of the other nine were read; they concern estimation of
  observables, gamma-ray source detection, entanglement of levitated particles, two
  key-distribution protocols, a seam of Wen's plaquette model on a lattice Klein bottle,
  free-electron optics, SAT-oracle synthesis and coherence of three-qubit states. Of the eleven,
  six are not about codes or mention error correction only: arXiv:2610.36965 (QCCD compilers), 2610.37268 (quantum-dot key distribution),
  2607.04586 (compiler pass tuning), 2607.13975 (multi-mode cat-state gates), 2609.09993
  (cultivation of a magic state that grows into a surface-code patch) and 2610.35227 (control-line
  multiplexing). Five concern error correction: 2610.37347 (measurement incompatibility and
  noiseless codes), 2610.36029 (condensable algebras in twisted quantum doubles), 2610.36700 (exact
  distances of quasi-cyclic additive codes: code distances, not circuit distances), and the
  replacements 2510.06257 (neural decoding of bivariate-bicycle codes) and 2608.31040 (fast
  decoders for hypergraph-product and lifted-product codes, with hook errors as trapping sets).
  None gives a circuit distance, a test of the formula or a lower-bound proof object for a
  colour-code circuit. No entry is a new version of a paper that the note, the README or the
  Zenodo text cites.
- **Crocker.** 23633600 and its concept, 23452754, 23690807 with its concept and 23630980 are
  unchanged (byte-identical answers). The records created or updated since 2026-10-27 22:00 UTC
  under the family name Crocker are five records by other authors, none on quantum error
  correction. Nothing at d ≥ 11 and no companion note.
- **Kornstein** 23394575 is unchanged, and no record of Kornstein or of "Guancheng Pan" was
  updated.
- **qsim-lab** is unchanged since `682845a` (the comparison with main is identical, and the
  branches are unchanged); its d = 13 run of this circuit is still not posted.
- **Issa–Martonosi's repository**: its tree is unchanged, and its latest commit is of 2026-10-23.
  No later version of arXiv:2610.33347 was announced.
- **Pan**: main still at `1f9757458f` (identical comparison), releases and branches unchanged. No
  colour-code work.
- **The Kishony–Fowler authors' repositories.** The GitHub account `kishonyWIS` gives no profile
  name, but its repositories `color_code_off_the_hook_overleaf` (last pushed 2026-03-29) and
  `syndrome_extraction_optimization` (last pushed 2026-03-26; the companion code's folder has the
  same name) make it very likely Kishony's. None of its 12 repositories was pushed after
  2026-08-24. The account `afowler` (Austin Fowler, Google) has no public repository. The Classiq
  error_correction folder has no commit after `a43d3bd4` (its newest commit is of 2026-07-02).
- **The other repositories of §2, §4 and §5.** Jaspersands/quantum-simulator-qec is still at
  `92f5a5bd`, so its README and data/distances.json are as §7.3 and §7.5 describe them. dist-m4ri,
  QECCertificates (tags still to v0.3.0), Lean-QEC, BivariateBicycleCodes, tesseract-decoder and
  Li et al.'s repository have no commit since 2026-10-27 22:00 UTC; qiskit-qec is unchanged
  (archived). unitaryfoundation/qldpc-challenge has 50 commits on 2026-10-28 (code-table additions
  for other codes, distance tightenings, a cost-grid update, site rebuilds): no changed path names
  the gross code, a circuit or a colour code; the 14 changed files whose patches the comparison
  shows, and the other 66 changed code and notes files, read at the new head, contain no
  colour-code or circuit-level claim.
- **New Zenodo records found by the topic searches.** "syndrome extraction": a version of Tomar's
  threshold record for the rotated surface code under circuit-level noise (23725694). "color code":
  Myo Oo's automated-theory-formation records (23740216, 23740217), which describe gauge
  colour-code switching between [[15,1,3]] and [[7,1,3]] and give no circuit distance or lower
  bound. "bivariate bicycle": Thalluri's code-distance records (23719464, 23719465, 23716457,
  23716458), code distances, not circuit distances. "fault distance": 23736286 and 23736287, on
  power-cable fault location. Quantum error correction with a certificate: Tomar's data and Lean
  proofs for certified lower bounds on the surface code's optimal-decoding threshold (23725564 to
  23725567). None of them bears on §3; the descriptions of the colour-code, bivariate-bicycle and
  syndrome-extraction records were read in full.
- **Repository searches.** "colour code": 31 colour-coding user-interface projects. "bivariate
  bicycle": one decoder repository, for [[72,12,6]]. "gross code": Pan's repository only. The other
  four: none.
- **Error Correction Zoo.** The four colour pages were read; their newest edits are of
  2026-10-12 (color and 4.8.8), 2026-07-22 (6.6.6) and 2026-06-08 (2D). None mentions a circuit
  distance, LRAT, DRAT, a proof object or Kishony; "circuit-level" appears only beside thresholds
  and in decoder titles.
- **Shutty's bundle** 22820614: its concept has this one version (2026-09-17). **QECCertificates**
  23056679: two versions, the record last updated on 2026-10-03.

**Verdicts as of 2026-10-29, 00:50 UTC.**

| statement | status | deciding sources |
|---|---|---|
| S1: d_circ 11 at d = 13 and 12 at d = 15 | not found elsewhere | as §7.2; nothing in this section bears on it |
| S2: the formula at d = 15 | not found elsewhere | the same |
| d = 13: an independent computation or a checkable proof | not found elsewhere | the same |
| third item narrowed: any circuit with the authors' schedule, any d | not found | the same |
| third item narrowed: any colour-code circuit at d ≥ 11 | not found | the same |
| S3 | describes this package | — |

**Limits.**
- arXiv: the quant-ph "new" listing only, with its cross-lists and replacements; a submission to
  another category that is not cross-listed to quant-ph would be missed. Abstracts only, because no
  entry was adjacent. The submissions received from 14:00 EDT on 2026-10-27 to 14:00 EDT on
  2026-10-29 are not covered (§7.6).
- The DataCite searches cover Zenodo's records and their metadata (titles, descriptions,
  creators), not full texts. The repository searches match names, descriptions and topics, not
  file contents.
- qldpc-challenge's 86 regenerated site files were not read.
- `kishonyWIS` is identified by its repository names only, and its two colour-code repositories,
  last pushed in March 2026, were not read.
- No earlier copy of the Error Correction Zoo pages was kept, so their comparison rests on each
  page's own edit log.
- No certificate, checker or program of any source was run.
