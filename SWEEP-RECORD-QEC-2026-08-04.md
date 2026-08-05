# Prior-art record for the QEC certificate release (sweep of 4 August 2026)

A full-text adversarial sweep was run against the draft of
`paper/preprint-qec-distances.tex` immediately before this release. Its purpose
was not to find support for the paper's claims but to break them. It broke two,
and both were withdrawn. This file is the dated record of what was read, what
was found, and what changed in consequence.

**Method.** Every source below was read in raw form — arXiv LaTeX source
(main and supplemental), GitHub repository trees at a named commit, and package
documentation — not from abstracts, not from summaries, and not from memory.
Statements about repositories are pinned to a commit and a date, because
repositories move.

**Coverage boundary.** arXiv through the listings of Tuesday 4 August 2026;
GitHub as of 4 August 2026. A negative result from a sweep is not a proof of
absence, and is not reported as one anywhere in the paper.

---

## Sources read in full

| source | what was read | date read |
|---|---|---|
| Bravyi, Cross, Gambetta, Maslov, Rall, Yoder, *High-threshold and low-overhead fault-tolerant quantum memory*, Nature **627** (2024) 778 / arXiv:2308.07915v2 | main text + supplemental LaTeX, Table 3 and its caption, the distance-method statement, the ZX-duality lemma | 2026-08-04 |
| Cruz-Benito, Cross, Kremer, Faro (IBM Quantum), arXiv:2606.02418 | full text; MILP formulation and the gross-code result | 2026-08-04 |
| Chen, Jafari, Lai, arXiv:2606.12445 | `main.tex` + result tables; repository `guluchen/QDistSAT` file tree | 2026-08-04 |
| LEAN-QEC, arXiv:2605.16523v1 (15 May 2026) | all 10 source files; repository `VerifiedQC/Lean-QEC` at commit `c73827d` (2026-07-10), including `BB144.lean`, `BB108.lean`, and the notes file | 2026-08-04 |
| Webster, Jacob, Higgott, arXiv:2603.22532 | full text, incl. exhaustive search for occurrences of "certificate"/"certification" | 2026-08-04 |
| Landahl, Anderson, Rice, arXiv:1108.5738 | the MIP distance method used by Bravyi et al. | 2026-08-04 |
| QDistRnd, *J. Open Source Softw.* **7** (2022) 4120 | full paper; the "no performance guarantee" statement | 2026-08-04 |
| Stim documentation, `search_for_undetectable_logical_errors` | the verbatim warning "THIS IS A HEURISTIC METHOD" | 2026-08-04 |
| PBLean, arXiv:2602.08692 | full text (adjacent certificate-import work) | 2026-08-04 |

---

## What the sweep broke

### 1. The [[288,12,18]] framing — the significant one

**Withdrawn claim.** An earlier internal draft of `RESULTS.md` stated that
Bravyi et al. concede their `d <= 18` for [[288,12,18]] "is unlikely to be
tight", and inferred that our interval `[14,18]` was the first distance
information ever produced for that code.

**What the source actually says.** The quoted caveat is about the
**circuit-level** distance `d_circ`, a different quantity from the code
distance. Table 3 of arXiv:2308.07915 lists [[288,12,18]] with **no** `<=`,
unlike `[[360,12,<=24]]` and `[[756,16,<=34]]`, and the caption states that the
`<= d` notation marks entries for which only an upper bound is known. The
supplemental material states that the actual distance "of each candidate code
was computed using the integer linear programming method".

**Conclusion.** Bravyi et al. **assert `d = 18` exactly** for this code, by ILP,
without shipping a checkable artifact. Our `[14,18]` is **not** new information
about the value. Every "first distance information" claim has been deleted from
the paper, from `RESULTS.md`, and from the release notes.

**What survives, and is what the paper claims.** Chen–Jafari–Lai
(arXiv:2606.12445, 29 May 2026) report `d >= 11` for this code, solver-asserted
after 7200 s timeouts, and ship no proof artifact — their repository
`guluchen/QDistSAT` contains none. We certify `d_X >= 14` with a 2.94 GB LRAT
proof that replays independently in pure Python. That improves on the strongest
quantity previously published *as a lower bound*, and is the only
machine-checkable lower bound on record for this code at any strength.

### 2. The LEAN-QEC contrast — stale, and would have been a false public statement

**Withdrawn claim.** An earlier draft contrasted our work against the LEAN-QEC
**paper**, which states that the gross code is dispatched to `cvc5` outside the
Lean kernel and names kernel replay at that size as "the next concrete
engineering target". That is what the paper says, and it is still true of the
paper.

**What the sweep found.** Their **repository has moved past their paper.**
Commit `c73827d` (2026-07-10) records a full [[144,12,12]] verification via
`bv_decide` in about 30 minutes, *including* kernel replay. Publishing the
paper-only contrast would have been a false public statement about a
competitor.

**Consequence.** The paper now states both, at their respective dates, and
makes **no priority claim** for a machine-checked gross-code distance.

**The differentiators that do survive**, each checked at their HEAD and stated
in the paper as observations of a moving repository:

* `BB144.lean` carries two `sorry`s — `BB144_X_ker_rank` (L69) and
  `BB144_Z_ker_rank` (L72) — through which `BB144_dist_12` routes, so that
  theorem is not `sorry`-free as committed;
* three lemmas use `native_decide`, which their own paper notes extends the
  trusted base with Lean's compiler;
* no LRAT artifact is committed for BB144;
* their 144-qubit encoding is symmetry-broken only.

Ours: no admitted lemmas, artifacts shipped, symmetry-**free** proofs included,
no proof assistant needed.

**Also explicitly not claimed about them.** Their kernel-checked ladder must
**not** be described as reaching n = 108: `BB108.lean` at the same commit
carries `sorry` at L120 and L132, with its `--bv_decide` invocation commented
out. The paper says so.

---

## Prior art credited at point of use

* **Bravyi, Cross, Gambetta, Maslov, Rall, Yoder** — the codes themselves, the
  ILP-computed distances, and the `d_X = d_Z` duality lemma for BB codes. The
  duality **fact** is theirs; only the explicit permutation, packaged as a
  ~15 ms checkable certificate, is ours.
* **Cruz-Benito, Cross, Kremer, Faro (IBM), arXiv:2606.02418, 1 June 2026** —
  gross-code distance `d = 12` confirmed exactly by MILP at MIP gap 0. No
  certificate is emitted. This is the current reference point for the value.
* **Chen, Jafari, Lai, arXiv:2606.12445** — SAT/MaxSAT distance computation at
  scale; explicitly no proof logging.
* **LEAN-QEC, arXiv:2605.16523 + repo commit `c73827d`** — kernel-checked SAT
  distance proofs for quantum codes. Prior art for the whole idea.
* **Landahl, Anderson, Rice, arXiv:1108.5738** — the MIP distance method.
* **QDistRnd (JOSS 2022)** — upper bounds only, "no performance guarantee".
* **Stim** — `search_for_undetectable_logical_errors`, documented verbatim as
  "THIS IS A HEURISTIC METHOD".
* **Webster, Jacob, Higgott, arXiv:2603.22532** — the survey that classifies
  exact against heuristic methods.
* **PBLean, arXiv:2602.08692** — adjacent certificate-import work; the closest
  prior art to the general project of making solver output externally checkable
  in a small trusted base.
* **Heule and coauthors** — LRAT and `drat-trim`.
* **Biere and coauthors** — CaDiCaL.
* **Sinz (2005)**, **Tseitin (1968)** — the cardinality and gate encodings.

---

## Net position after the sweep

This release is a **verification contribution, not a discovery**. The distance
values are largely known and are credited to their sources. What did not exist,
and what is offered here, is a standalone artifact anyone can replay without a
solver and without a proof assistant, together with an independent audit of it:
47 of 47 certificate checks passed, 5.08 GiB of LRAT replayed in pure Python at
79 MB peak RSS, all five bivariate-bicycle parity-check matrices rebuilt
byte-identically from the published construction, 11 of 11 negative controls
rejected. See `INDEPENDENT-VERIFICATION.md`.
