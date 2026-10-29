# d_circ = d − ⌊(d+3)/6⌋ for the Kishony–Fowler colour-code circuit, d = 3 … 15 — certificates

**Part N of Certify (v0.16.0).** The note is `../colorcode-dcirc-paper/note.md`; its PDF is
`../colorcode-dcirc-paper/note.pdf`. The build sessions' checks are recorded in `VERIFY.log`.

## Result

The circuit is the single-auxiliary colour-code syndrome-extraction circuit of Kishony and Fowler
(arXiv:2603.28852). It is built by their own code, uses their default schedule, has two-qubit
depolarising noise after every CNOT and runs as a Z-basis memory experiment. For it,

> **d_circ = 2, 4, 6, 7, 9, 11, 12 at d = 3, 5, 7, 9, 11, 13, 15**, for d rounds and for one round,

which equals d − ⌊(d+3)/6⌋ at every point. Every value is two-sided:
- an explicit set of d_circ fault mechanisms that flips the observable and no detector;
- an LRAT proof that no smaller set does.

At d = 15 the loss term ⌊(d+3)/6⌋ is 3 for the first time. The LRAT refutation for d = 15 was
accepted by two checkers: this directory's standard-library checker and drat-trim's `lrat-check`.

**What was not found elsewhere, and what was.** These were not found in the sources read, as of
2026-10-29 (`../SWEEP-RECORD-COLORCODE-DCIRC-2026-10-20.md`, which lists the sources and the
as-of times):
- a circuit-level distance for this circuit at d = 15, or any test there of the authors' formula,
  whose loss term first equals 3 at d = 15;
- an independent computation, or a checkable proof, of this circuit's distance at d = 13. The
  authors state that their formula holds numerically up to d = 13 (arXiv:2603.28852v1,
  `main.tex`:201), which gives 11 at d = 13, but they give no per-d values, round count or method.
  Our value at d = 13 agrees with that statement; what this package adds there is the independent
  computation and the proof;
- a checkable proof (an LRAT, DRAT or formal proof object) of a lower bound on the circuit
  distance of any circuit with the authors' schedule, at any d, or of any colour-code
  syndrome-extraction circuit at d ≥ 11. The nearest items found are Crocker's record (next
  paragraph), with a DRAT proof for the extended-code step of a lower bound for another schedule
  of the same family at d = 9, and the bundle of Shutty's arXiv:2609.21376
  (doi:10.5281/zenodo.22820614, `distance/README.md`),
  which ships a re-runnable, Stim-based exhaustive check reproducing that paper's small-instance
  lower bounds (triangular d = 3, torus d = 4) for a different circuit. That bundle's check is a
  search that trusts Stim, not a proof object.

**Found earlier: a DRAT proof inside a colour-code circuit-distance lower bound.** Crocker's
record doi:10.5281/zenodo.23633600 (v1.0, 2026-10-25) gives circuit distance 8 = d − 1 at d = 9
for C9, another single-auxiliary schedule of the Kishony–Fowler family, in his own construction
(uniform depolarising noise; Z and X memory). The extended-code step of its lower bound has a
DRAT proof: kissat refutes the shipped CNF, which says that at most 7 of C9's 127 extended-code
columns sum to the logical, and drat-trim checks the proof. The record's script regenerates it and
deletes it after the check, so the proof file is not in the record. The step to the circuit is a
Stim-based check that every single fault acts as one of those columns, at 1–5, 9 and 25 rounds,
with a hand lemma for every number of rounds in a companion note that is not in the record. The
record states nothing for d ≥ 11. (Read in full; `../SWEEP-RECORD-COLORCODE-DCIRC-2026-10-20.md`
§7 gives the file pointers.)

**Found earlier: the values at d ≤ 11.** The earliest independent values there found in the
sources read, as of 2026-10-29, are qsim-lab's (github.com/dylanneve1/qsim-lab,
research/qec/qec-r4.md §2.3, 2026-10-04): rounds = d at d = 3–9, and one round at d = 5–11. Our
values agree, and we credit those points to qsim-lab. Two later results concern the same CNOT
schedule:
- Crocker's record (above) gives extended-code distances 2, 4, 6, 7 at d = 3, 5, 7, 9 for the
  authors' colour rule on his lattice, by exhaustive search, and circuit distance 7 at d = 9 for
  one and three rounds, through Stim-based checks;
- Issa and Martonosi (arXiv:2610.33347v1, submitted 2026-10-23) give undetected logical errors of
  d − 1 faults at d = 7, 9 and 11 in the authors' circuits, each made of one "junction" hook error
  and d − 2 data errors. These are upper bounds.

Neither ships a proof object for a lower bound on this schedule.

**Found earlier: proof-carrying circuit distances in general.** A DRAT-checked circuit distance for a
bivariate-bicycle syndrome cycle (IBM's depth-8 cycle of the [[72,12,6]] code, d_circ = 6) was
posted on 2026-10-15 by Kornstein (doi:10.5281/zenodo.23394575, `depth8_cycle/DERIVATION.md`:222).
His values for the larger codes rest in part on enumerators without DRAT (`:229`;
`depth8_cycle_independent_checks/REVIEW.md`:97–98). Pan's release v2.0
(github.com/GavinNull/gross-code-distance-12, 2026-10-24) gives circuits of period 11 with circuit
distance 12 for the gross code and 10 for the [[90,8,10]] code, with VeriPB proofs for the
extended-code distances and list completeness and DRAT proofs for the lift steps; his experiment
E-037 (2026-10-25) gives VeriPB-checked lower bounds of 10 for IBM's depth-8 gross-code cycle for
every number of rounds up to 12.

## Scope

Every claim concerns the hash-pinned circuit texts `certs/c_d{d}_r{r}.stim`.
- **Generator.** The texts were produced by `build_parallel_circuit(d, r, 0.001, S₀)` of
  github.com/Classiq/classiq-library at commit a43d3bd4 (path
  `algorithms/error_correction/syndrome_extraction_optimization/`), executed verbatim.
- **Schedule.** S₀ is row 1 of `results/zero_collision_schedules.csv`:
  R = [1,3,2,5,4,6], G = [5,1,4,3,6,2], B = [1,5,3,6,2,4].
- **Noise.** `add_depolarize2_after_cnot` (DEPOLARIZE2 after every CX, nothing else).
- **Memory experiment.** Z basis; the observable is the top row of data qubits.

**Not claimed:**
- the other 863 schedules of the CSV;
- the circuit built by the companion `exhaustive_schedule_search.py` (separate X and Z auxiliaries
  and different edge schedules);
- X-basis memory;
- round counts other than 1 and d;
- other noise models.

## Definitions

- **Mechanism list.** `m_d{d}_r{r}.json` holds M(d, r), the distinct (detector set,
  observable bit) signatures of the circuit's detector error model, sorted and hashed. One fault
  is one two-qubit Pauli after one CNOT.
- **Circuit-level distance.** d_circ = min |F| over F ⊆ M with ⊕ dets(F) = ∅ and ⊕ obs(F) = 1.
- **Extended code.** `m_Xext_d{d}.json` is the extended code of Strikis–Browne–Beverland
  (arXiv:2603.05481), in the same format. Its rows are the Z checks; its columns are the data
  qubits plus the residual suffixes of each X check's CNOT order. It is built from the circuit
  text by `certs/extcode_from_circuit.py`.
- **X-part sub-list.** `m_pxd{d}_r{d}.json` holds M_Z, the mechanisms of M(d, d) that touch only
  Z-type detectors.

## How the lower bounds reach the circuit

A refutation on M(d, r) itself (**direct**) needs no lemma. The other two routes need one or two
finite hypotheses about the explicit lists, which `certs/lemma_b_check.py` checks for every
(d, r) shipped.

**Hypothesis A.** Every mechanism, restricted to the Z-type detectors and the observable, is
empty or lies in M_Z.
- Restrict each member of an undetected logical fault set this way and cancel repeats. The result
  is an undetected logical subset of M_Z that is no larger.
- So d_circ(M) = d_circ(M_Z). This carries the **X-part** route.

**Hypothesis B.** Every mechanism of M_Z, projected to (per-check parity over all rounds,
observable bit), is zero or an extended-code column.
- Parity is additive. So the projections of an undetected logical subset of M_Z cancel, after
  removing repeats, to an undetected logical set of columns that is no larger.
- So d_circ(M_Z) ≥ d_ext. Together with A this carries the **extended-code** route: a refutation
  of the extended code at K gives d_circ(C(d, r)) ≥ K + 1.

These two paragraphs are the whole argument. The proof of the SBB theorem is not used. That
theorem predicts that the extended-code bound is tight; the shipped witnesses show that it is,
instance by instance.

**Credit for the projection check.** Hypothesis B is not a new idea. For IBM's depth-8
bivariate-bicycle cycles, Kornstein's deposit (doi:10.5281/zenodo.23394575, posted 2026-10-15)
checks that every fault's key, its data footprint modulo stabilisers, is 0 or an extended-code
column, and proves that the keys of an undetected logical fault set sum to an extended-code
logical (`depth8_cycle/DERIVATION.md`:161–165, "Lemma 3 (projection)"; on the proof of
Strikis–Browne–Beverland's Prop. 3, which the check makes finite, see `:54–59`). Hypothesis B is
the same check, made on the explicit fault list of this circuit; Hypothesis A is the X-part
reduction that comes before it.

## Claims, at exactly the strength the checker supports

Proof sizes are gzip bytes. "In git: no" means the proof is listed in
`PROOFS-NOT-IN-GIT.sha256`, attached to the GitHub release v0.16.0 (in parts if it is over 2 GiB),
and recreated by `REGENERATE.md`.

| d | value | upper bound, r = d | lower bounds, r = d (route: certificate, proof size, in git) | r = 1 (upper; lower) |
|---|---|---|---|---|
| 3 | 2 | `witness_d3_r3_w2` | direct: `lower_d3_r3_K1`, 20 KB, yes. ext: `lower_Xext_d3_K1`, yes | `witness_d3_r1_w2`; direct `lower_d3_r1_K1` |
| 5 | 4 | `witness_d5_r5_w4` | direct: `lower_d5_r5_K3`, 70.6 MB, **no**. X-part: `lower_pxd5_r5_K3`, 0.9 MB, yes. ext: `lower_Xext_d5_K3`, yes | `witness_d5_r1_w4`; direct `lower_d5_r1_K3` |
| 7 | 6 | `witness_d7_r7_w6` | X-part: `lower_pxd7_r7_K5`, 181 MB, **no**. ext: `lower_Xext_d7_K5`, 0.5 MB, yes | `witness_d7_r1_w6`; direct `lower_d7_r1_K5` |
| 9 | 7 | `witness_d9_r9_w7` (and `…_stimheur`, a different set) | X-part: `lower_pxd9_r9_K6`, 4.06 GB, **no**. ext: `lower_Xext_d9_K6`, 2.2 MB, yes | `witness_d9_r1_w7`; direct `lower_d9_r1_K6`, 42.6 MB |
| 11 | 9 | `witness_d11_r11_w9` (lifted) | ext: `lower_Xext_d11_K8`, 40.8 MB, yes | `witness_d11_r1_w9`; ext |
| 13 | 11 | `witness_d13_r13_w11` (lifted) | ext: `lower_Xext_d13_K10`, 1.17 GB, **no** | `witness_d13_r1_w11`; ext |
| **15** | **12** | `witness_d15_r15_w12` (lifted) | ext: `lower_Xext_d15_K11`, 8.95 GB, **no**; two checkers (below) | `witness_d15_r1_w12` (lifted); ext |

Notes on the table:
- **ext** means the extended-code refutation together with Hypotheses A and B at that (d, r).
- **Witnesses** are checked against the d-round list, which is itself re-derived from the circuit
  text. "Lifted" witnesses were made by `tools/lift_ext_witness.py` from the extended-code
  witness `witness_Xext_d{d}_w*.json`. The lifting tool is untrusted; only its output is checked.

**d = 15 in detail.**
- CaDiCaL 3.0.1 `--lrat` refuted the canonical CNF of `m_Xext_d15.json` at K = 11 (5,828
  variables, 13,932 clauses, SHA-256 `2b471a0f…83fde`). It took 15,724 s wall-clock, and the
  binary proof is 14,062,531,915 bytes.
- `tools/blrat2lrat.c` converted the proof to text LRAT (53,140,862 additions), gzipped to
  8,945,210,112 bytes. The converter is a format converter and is not trusted.
- **Checker 1: drat-trim `lrat-check`** (build of commit 2e3b2dc). It did not read the stored
  gzip file: it read the converter's output for the binary proof on standard input, against the
  CNF whose SHA-256 its log records (`2b471a0f…83fde`). It reported `c VERIFIED` in 1,168.4 s
  (`logs/2026-10-07/drat-trim_lrat-check_Xext_d15_K11.log`).
- **Checker 2: `certs/check_dcirc.py lower`.** It read the stored gzip file, regenerated the CNF
  from the object, matched its hash and replayed the proof: `OK lower bound … >= 12`, 6,167.4 s,
  with two hint clauses that were already satisfied skipped
  (`logs/2026-10-07/check_dcirc_lower_Xext_d15_K11.out`).
- **The stored proof equals the converted stream.** On 2026-10-20 the decompressed stored file and
  a fresh conversion of the binary proof, by the converter compiled from `tools/blrat2lrat.c`, were
  both 30,547,997,901 bytes with SHA-256 `d1220b7e…77fb84`
  (`logs/d15_proof_text_identity_2026-10-20.log`). drat-trim had been given the output of the
  same converter source on the same binary file, so both checkers read this text.
- On 2026-10-20, `tools/emit_cnf.py` re-emitted the CNF from the staged object; it is
  byte-identical to the solver's input file (`logs/cnf_binding_revision_2026-10-20.log`). The
  proof was not replayed again.

## What was re-run on 2026-10-20 and 2026-10-21, and what rests on earlier logs

Three sessions worked on this directory on 2026-10-20: the staging session, a revision session
that acted on the first independent battery's report, and a second revision session (round 3)
that acted on the second battery's report. A third revision session (round 4) worked on it on
2026-10-21 and acted on the third battery's report. Each ran every check below on the staged
copies (`VERIFY.log`; `logs/*2026-10-20*`, `logs/*2026-10-21*`):
- all 24 objects re-derived from their circuit text;
- all 25 witnesses;
- the 11 shipped proofs;
- Hypotheses A and B on all 14 (d, r) objects;
- the tamper battery: eleven corruptions in the staging run; twelve after the first revision
  corrected the CX-reversal control; fourteen after round 3 relabelled one lower-bound case,
  added the two that reach the CNF hash and the LRAT replay, and made the battery check that
  each rejection comes from the check its label names; fifteen after round 4 added a run of the
  checker under `python -O`, which must be refused (see "Run it").

Two later revision sessions, on 2026-10-21 (round 5) and 2026-10-28 (round 7), changed records
and prose only: no script, object, witness, lower-bound record, circuit text, proof or log under
`logs/` changed, so neither re-ran a checker (`VERIFY.log`).

A further revision session on 2026-10-29 (round 8) changed records and prose and added, under
`logs/2026-10-28/`, the 18 logs of the 2026-10-28 runs on GitHub-hosted runners (see Platforms).
It changed no script, object, witness, lower-bound record, circuit text, proof or existing log,
and ran no checker itself.

A seventh revision session on 2026-10-29 (round 9) acted on the sixth independent battery's
report and changed records and prose only: it relabelled one scan-group name in `VERIFY.log` in
place (the `VERIFY.log` note under "Logs" below), completed one arXiv-coverage row of
`colorcode-dcirc-paper/PROVENANCE.md`, and recorded both in `VERIFY.log` and
`colorcode-dcirc-paper/FIXLOG.md`. It changed no script, object, witness, lower-bound record,
circuit text, proof, existing log, `note.md` or `note.pdf`, and ran no checker itself.

Round 3 ran the full check under Python 3.14.7 and, for the first time in a shipped log, under
Python 3.9.6 (`logs/run_all_full_round3_2026-10-20.log`,
`logs/run_all_full_py39_round3_2026-10-20.log`), and the tamper battery on nine certificates,
the d = 9 extended-code one among them (`logs/tamper_stems_round3_2026-10-20.log`). Round 4 ran
the full check under both Pythons again (`logs/run_all_full_round4_2026-10-21.log`,
`logs/run_all_full_py39_round4_2026-10-21.log`), `--fast` under Python 3.9.6
(`logs/run_all_fast_py39_round4_2026-10-21.log`), the tamper battery on the same nine
certificates (`logs/tamper_stems_round4_2026-10-21.log`), and a control of the optimisation
guard (`logs/optimisation_guard_control_round4_2026-10-21.log`).

The first revision session also:
- regenerated the four lifted witnesses with `tools/lift_ext_witness.py`; each regenerated file
  is byte-identical to the shipped one (`logs/lift_ext_witness_revision_2026-10-20.log`);
- re-emitted the CNFs of the five out-of-git certificates and compared each, byte by byte, with
  the solver's input file; all five are identical (`logs/cnf_binding_revision_2026-10-20.log`);
- ran the tamper battery on the d = 9 extended-code certificate too
  (`logs/tamper_Xext_d9_revision_2026-10-20.log`);
- compared the d = 15 proof text that the two checkers read, and the converter's output with
  CaDiCaL's own text output (see "d = 15 in detail").

Neither revision of 2026-10-20 changed `check_dcirc.py`, `dem_from_circuit.py`,
`extcode_from_circuit.py`, `purex_from_object.py` or `lemma_b_check.py` (`VERIFY.log`). Round 4
changed each of them by one line, the optimisation guard (see "Run it"), and in no other way: in
each file the blank line after the imports became the guard, so no other line moved (`VERIFY.log`,
round 4, prints the five diffs).

Three proofs that are not shipped were also replayed from the author's copies: by the staging
session, with the checker as it was before round 4 (`logs/replay_out_of_git_proofs_2026-10-20.log`),
and again by round 4, with the guarded checker
(`logs/replay_out_of_git_proofs_round4_2026-10-21.log`). The two checkers differ by the guard
line only.
- `d5_r5_K3`: 44.0 s (staging), 190.8 s (round 4, 46.9 s of CPU);
- `pxd7_r7_K5`: 139.0 s (staging), 308.4 s (round 4, 145.4 s of CPU);
- `Xext_d13_K10`: 706.7 s (staging), 1,465.3 s (round 4, 708.4 s of CPU).

Round 4's replay log records one-minute load averages of 69.5 to 168.1 at the start and end of
each replay; the staging session's log records none.

Two proofs were **not** replayed on 2026-10-20 or 2026-10-21, because each session had a
per-run budget of 20 CPU-minutes:
- `pxd9_r9_K6`, replayed on 2026-09-01 in 1,124 s and 1,364 s;
- `Xext_d15_K11`, replayed on 2026-10-07 by both checkers, in 6,167 s and 1,168 s, and again on
  2026-10-28 by `check_dcirc.py`, on a Linux runner (see Platforms).

For both, the CNF binding was re-checked on 2026-10-20 (`logs/cnf_binding_2026-10-20.log` and
`logs/cnf_binding_revision_2026-10-20.log`), and the staging session re-hashed the proof files.
- `pxd9_r9_K6`: the hash matches the 2026-09-01 manifest.
- The d = 15 files had no recorded hash before. Their hashes are now in
  `PROOFS-NOT-IN-GIT.sha256`.

## Run it

Standard-library Python 3.9 or later; Linux, macOS or Windows. The commands are written with
`python3`; on Windows, type `py` (or `python`) in its place.

```
python3 run_all.py --fast     # every witness, the small objects and proofs: about 10-15 s
python3 run_all.py            # everything shipped, plus the tamper battery: about 1.5-2.5 minutes
```

These times were measured on the build laptop on 2026-10-20. It was not idle: the revision
session logged a load average of 33-55 (`VERIFY.log`), and the round-3 `run_all` logs record
one-minute load averages of 10.9-25.6 before and after each run. The staging session's logs
record no load figure. Round 4's runs of 2026-10-21 are listed separately below; they are not
used for the estimates above.
- Full run, Python 3.14.7: 112.2 s (staging), 115.7 s (revision) and 83.1 s (round 3)
  (`logs/run_all_full_2026-10-20.log`, `logs/run_all_full_revision_2026-10-20.log`,
  `logs/run_all_full_round3_2026-10-20.log`).
- Full run, Python 3.9.6: 151.2 s (round 3, `logs/run_all_full_py39_round3_2026-10-20.log`).
- `--fast`, Python 3.9.6: 11.3 s (staging), 11.3 s (revision) and 11.9 s (round 3)
  (`logs/run_all_fast_py39_2026-10-20.log`, `logs/run_all_fast_py39_revision_2026-10-20.log`,
  `logs/run_all_fast_py39_round3_2026-10-20.log`).

Round 4's runs, 2026-10-21. Their logs record one-minute load averages of 41.1 to 154.9 at their
starts and ends, so their wall-clock times say little about the checker; the CPU times
("user" in each log) are given too.
- Full run, Python 3.14.7: 144.7 s, 95.7 s CPU (`logs/run_all_full_round4_2026-10-21.log`).
- Full run, Python 3.9.6: 1,147.0 s, 143.0 s CPU (`logs/run_all_full_py39_round4_2026-10-21.log`).
- `--fast`, Python 3.9.6: 36.1 s, 10.9 s CPU (`logs/run_all_fast_py39_round4_2026-10-21.log`).

**Do not use `python -O`.** Most checks here are `assert` statements, and Python removes assert
statements when it runs with `-O` or `-OO`, or with the environment variable `PYTHONOPTIMIZE`
set. So every script that relies on them refuses to run in that mode: it says why on standard
error and exits with status 1. These are `run_all.py`, `certs/check_dcirc.py`,
`certs/dem_from_circuit.py`, `certs/extcode_from_circuit.py`, `certs/purex_from_object.py`,
`certs/lemma_b_check.py`, `certs/tamper_demo.py` and `tools/emit_cnf.py`. Before this guard
was added, `python3 -O` accepted a d = 15 witness with one mechanism removed, a false
d_circ(15, 15) ≤ 11; with the guard, it refuses
(`logs/optimisation_guard_control_round4_2026-10-21.log`).

Single checks, run from this directory:

```
python3 certs/check_dcirc.py object  certs/m_d15_r15.json certs/c_d15_r15.stim
python3 certs/check_dcirc.py witness certs/witness_d15_r15_w12.json
python3 certs/lemma_b_check.py certs 15 15
python3 certs/check_dcirc.py lower   certs/lower_Xext_d11_K8.json
```

`run_all.py` reports the proofs that are not present and does not count them. After
`REGENERATE.md` has put a proof back into `certs/`, `run_all.py` replays it like any other.

What each check does:
- **`object`** re-derives the mechanism list from the circuit text by an exact reverse
  Pauli-frame pass (`certs/dem_from_circuit.py`, no Stim) and compares it with the object. For
  extended-code objects it rebuilds the extended code from the circuit text instead. For X-part
  objects it rebuilds the parent list and the sub-list, and checks Hypothesis A.
- **`witness`** XORs the listed mechanisms against the object.
- **`lower`** regenerates the CNF from the object. The CNF is a parity chain per detector, one for
  the observable, and a Sinz at-most-K counter; the specification is in the docstring. The check
  compares the CNF's SHA-256 with the certificate, then replays the LRAT: RUP hints only; a
  non-unit, dangling or RAT hint aborts, as does a missing empty clause; already-satisfied hints
  are skipped and counted.
- **`lemma_b_check.py`** checks Hypotheses A and B.
- **`tamper_demo.py`** applies fifteen corruptions. Each must be rejected, and rejected by the
  check that its label names: the battery matches the checker's output against that check, so a
  corruption caught by any other check fails the battery
  (`logs/tamper_label_control_round3_2026-10-20.log`). Among the corruptions:
  - a CX pair in the third CX layer is reversed twice: once with the circuit hash left stale
    (caught by the hash), and once with the object rebound to the edited circuit (caught by the
    re-derivation). Reversing a pair in the first CX layer would not be a valid control: no fault
    precedes that gate, and the re-derived list is unchanged
    (`logs/tamper_cx_layer_control_2026-10-20.log`);
  - one mechanism is removed from the object and the object is rehashed, three times: with the
    lower-bound certificate left as it is (caught by its binding to the object), with the
    certificate rebound to the new object (caught by the regenerated CNF's hash), and with its
    recorded CNF hash rebound too (caught by the LRAT replay);
  - the witness with one mechanism dropped is checked a second time with the checker started
    under `python -O`. It must be refused by the optimisation guard; without the guard, `-O`
    accepts it (`logs/optimisation_guard_control_round4_2026-10-21.log`, section D).

For extended-code objects, the checker's output line reads `d_circ(d=…, rounds=0)`, and the
`statement` field of `lower_Xext_*.json` says `d_circ >= …`. In both places the quantity is the
extended code's distance d_ext. It reaches the circuit only through Hypotheses A and B.

## Trust base and independence

**Trusted:**
1. The circuit texts are the authors' construction. They were produced by executing their code
   with one `from __future__ import annotations` line added per module for Python 3.9: seven
   modules in the 2026-09-01 build, eight in the 2026-10-07 rebuild
   (`logs/2026-10-07/lazy-annotations.patch`). The rebuild was compared with the earlier build on
   three circuit texts, (d, r) = (5, 5), (13, 13) and (15, 1), and reproduced all three byte for
   byte (`VERIFY.log`); `c_d15_r15.stim` exists only from the rebuild. The texts are hash-pinned.
2. The fault model.
3. The two arguments above.
4. CPython, the operating system and the hardware.

**Not trusted:** Stim, CaDiCaL, the converter, the lifting tool.

**Measured overlap of checker and encoder** (2026-09-01, `logs/2026-09-01/code_overlap_2026-09-01.log`):
- Of the 220 executable lines of `check_dcirc.py` as it was then (round 4 added the one-line
  optimisation guard), 29 also appear in the private CNF encoder, and 16 of them are
  substantive. The longest identical run is 7 lines, in the Sinz counter; the XOR-chain emitter
  shares at most 3 consecutive lines (located on 2026-10-20, `VERIFY.log`). Both implement the
  shared specification.
- 41 lines (20 substantive) appear in the program's earlier `check_lower.py`.
- 25 lines (11 substantive) appear in its `indep_lrat.py`.
- So a pass is an independent re-derivation of the mechanisms and an independent replay of the
  proofs, but not an independent re-implementation of the encoding. The guards on that layer:
  - the tamper battery;
  - the authors' OR-Tools integer program, run verbatim (`logs/2026-09-01/ilp_anchor.log`):
    status OPTIMAL with the same value on (3,1), (3,3), (5,1), (7,1), (9,1) and (5,5); on (7,7),
    FEASIBLE with incumbent 7 and bound 3, beaten by the shipped weight-6 set;
  - at d = 15, drat-trim.

**Files added on 2026-10-20:**
- `certs/lemma_b_check.py` is a standard-library port of the build session's Stim-based script.
  On all 14 objects its Hypothesis-B lines are identical to that script's logged output
  (`logs/2026-09-01/lemma_b_check_2026-09-01.log` for d ≤ 13;
  `logs/2026-10-07/lemma_b_check_d13_d15_extract_2026-10-07.log`, an extract of the 2026-10-07 log,
  for d = 15).
- `tools/lift_ext_witness.py` and `certs/lemma_b_check.py` were written in the same session and
  share a near-identical circuit-geometry parser. The lifted witnesses are checked by
  `check_dcirc.py witness`, which shares no code with either.

**Second LRAT acceptance path.** The program's independently written `indep_lrat.py`, which
aborts on already-satisfied hints, accepted these proofs on 2026-09-01 against the emitted CNF
files (`logs/2026-09-01/indep_lrat_2026-09-01.log`):
- d3_r1, d3_r3, d5_r1, d7_r1, d9_r1 and d5_r5;
- Xext_d9 and Xext_d11;
- Xext_d13, under the label "(checker)".

It rejected `pxd9_r9_K6` at one already-satisfied hint. That proof therefore has a single
acceptance (`check_dcirc.py`, 1,124–1,364 s). Its value is also carried by the extended-code
route.

## Solver cost (build laptop: Apple, 10 cores, 16 GB)

| instance | K | vars | clauses | solver wall | proof (gzip) | replay by `check_dcirc.py` |
|---|---|---|---|---|---|---|
| direct (3,3) | 1 | 1,598 | 4,971 | < 1 s | 20 KB | < 0.1 s |
| direct (5,5) | 3 | 18,692 | 54,872 | 56 s | 70.6 MB | 16.8 s (09-01), 44.0 s (10-20), 190.8 s (10-21) |
| direct (9,1) | 6 | 3,054 | 7,587 | 31 s | 42.6 MB | 11.5 s (09-01), 35.7 s (10-20) |
| X-part (5,5) | 3 | 2,295 | 6,096 | 1 s | 0.9 MB | 0.2 s |
| X-part (7,7) | 5 | 9,178 | 23,276 | 87 s | 181 MB | 53.8 s (09-01), 139.0 s (10-20), 308.4 s (10-21) |
| X-part (9,9) | 6 | 23,046 | 57,555 | 686 s | 4.06 GB | 1,124 s and 1,364 s (09-01) |
| ext d = 9 | 6 | 1,286 | 3,275 | 2 s | 2.2 MB | 0.5 s |
| ext d = 11 | 8 | 2,399 | 5,925 | 34 s | 40.8 MB | 12.0 s (09-01), 24.9 s (10-20) |
| ext d = 13 | 10 | 4,009 | 9,669 | 1,396 s | 1.17 GB | 316 s and 503 s (09-01), 706.7 s (10-20), 1,465.3 s (10-21) |
| ext d = 15 | 11 | 5,828 | 13,932 | 15,724 s | 8.95 GB (14.06 GB binary) | 6,167 s; drat-trim 1,168 s |
| direct (7,7) | 5 | 78,182 | 218,748 | **not obtained**: killed at 4,105 s (disk); two relaunches on 2026-09-25 also ended without a verdict (`logs/2026-09-25/`) | — | — |
| direct (9,9) | 6 | 202,058 | 555,953 | **not obtained**: stopped at 2,707 s (disk) | — | — |

Notes on the costs:
- The "(10-20)" replay times are the staging session's (`logs/run_all_full_2026-10-20.log` and
  `logs/replay_out_of_git_proofs_2026-10-20.log`). They are longer than the 09-01 replays of the
  same proofs. Those logs record no load figure; the laptop was not idle that day (the revision
  session's runs logged a load average of 33-55, `VERIFY.log`), so the 10-20 times are not
  benchmarks.
- The "(10-21)" replay times are round 4's, with the guarded checker
  (`logs/replay_out_of_git_proofs_round4_2026-10-21.log`), at one-minute load averages of 69.5
  to 168.1. Their CPU times were 46.9 s, 145.4 s and 708.4 s. They are not benchmarks either.
- Solver times on 09-01 are from `logs/2026-09-01/ladder*.log`.
- The d = 15 times are from the 10-07 logs.

## Logs

- `logs/2026-09-01/`: the build session's logs. Paths in them point to the build machine. They
  are unedited except for redactions, in place, of text about computations outside this
  release's scope, in four of them:
  - nine whole lines are replaced by `[REDACTED: outside this release's scope]`:
    `check_all_final_2026-09-01.log` lines 5, 6 and 27, `object_rederivation_ext_2026-09-01.log`
    lines 8 and 9, `ladder.log` lines 85 and 86, and `ladder_ext.log` lines 36 and 37;
  - in `ladder.log` line 103, two items are replaced by `[REDACTED]`. The rest of that line
    records that the direct one-round run at d = 13, K = 10 was stopped without a verdict (its
    start is in `ladder_r1ext.log`).

  Every other line is as the build session wrote it, each file keeps its line count, and no
  certificate of this release rests on redacted text.
- `logs/2026-09-25/`: two later relaunches of the direct (7,7) refutation, neither of which
  reached a verdict.
- `logs/2026-10-07/`: the d = 15 solver output, both checker transcripts, the d = 13 and d = 15
  lines of that day's hypothesis check, and the generator patch of the rebuild.
- `logs/*2026-10-20*`: the staging session's runs, the two revision sessions' runs (round 3's
  are `logs/*round3*`), the d = 15 proof-text comparison and the converter comparison.
- `logs/*round4_2026-10-21*`: round 4's runs: the full and fast checks, the tamper battery, the
  three out-of-git replays and the control of the optimisation guard.
- `logs/2026-10-28/`: the 18 logs of the 2026-10-28 runs on GitHub-hosted runners (see Platforms).
  For each of ubuntu-latest and windows-latest under Python 3.9 and 3.14: the `SHA256SUMS` check
  (`sums_*.log`) and `run_all.py` in full and with `--fast` (`run_all_full_*.log`,
  `run_all_fast_*.log`). Under Python 3.14: the hash check of the proofs that are not in git
  (`fetch_*.log`) and their replays by `certs/check_dcirc.py lower` (`replay_*.log`). The Windows
  logs keep their CRLF line endings; in `replay_windows-d5-d7-d13.log` only the lines that the
  checker printed end in CRLF, and its `==` lines end in LF.
- `VERIFY.log`: the transcripts of the revision sessions, rounds 2, 3, 4, 5, 7, 8 and 9 in that order.
  Round 4 redacted four of its lines in place, replacing text outside this release's scope by
  `[REDACTED]`: one item of line 7 (round 2's header), and the pattern labels of lines 814, 815
  and 824 (round 3's propagation table). Round 9 made one further in-place replacement, at line
  2584 (round 8's §9b scan-group summary), putting the neutral label `sibling-internal` in place
  of a scan-group name outside this release's scope (`VERIFY.log` R9.2). These in-place
  replacements added or removed no line, and every other line is as written.

## Platforms

Run on macOS 26.2 (arm64) with Python 3.14.7, and with the system Python 3.9.6 (`--fast`; in
rounds 3 and 4 also the full check). On 2026-10-28 a byte copy of this directory, as it was after
round 7, was also run on GitHub-hosted runners, ubuntu-latest and windows-latest, under Python 3.9
and 3.14 (`logs/2026-10-28/`). On all four, `SHA256SUMS` matched 156 of 156 files with none
unlisted. `run_all.py` passed in full (24 objects, 25 witnesses, 11 proofs and 14 hypothesis
checks, with all 15 tamper corruptions rejected) and with `--fast` (20 objects, 25 witnesses, 9
proofs and 10 hypothesis checks). Under Python 3.14, `certs/check_dcirc.py lower` also replayed
proofs that are not in git, each first checked against `PROOFS-NOT-IN-GIT.sha256`: `d5_r5_K3`,
`pxd7_r7_K5` and `Xext_d13_K10` on Linux and on Windows, and `Xext_d15_K11` on Linux (53,140,862
lemmas, 3,968.4 s). `pxd9_r9_K6` has not been replayed off the build laptop.
- **Imports.** The verification path (`run_all.py`, `check_dcirc.py`, `dem_from_circuit.py`,
  `extcode_from_circuit.py`, `purex_from_object.py`, `lemma_b_check.py`) imports only `json`,
  `gzip`, `hashlib`, `os`, `re`, `sys`, `time`, `collections`, `tempfile` and `runpy`, plus the
  scripts' own modules.
- **No POSIX-only constructs** (AST scan in `VERIFY.log`).
- **Tamper battery.** `tamper_demo.py` additionally uses `shutil` and `subprocess`, to run the
  checker with `sys.executable` on corrupted copies.
- **Line endings.** Every hash here is over raw bytes. `.gitattributes` (`* -text`) stops git from
  converting line endings on any platform; a copy whose line endings were converted fails the
  hash checks.
