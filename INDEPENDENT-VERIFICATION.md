# Independent verification of the QEC certificate corpus

**Auditor:** Claude Opus 5, acting as an independent re-checker. Nothing in the pipeline's own
prose (`RESULTS.md`, `manifest.json`, `meta.json`) was taken on trust; every number below was
re-measured on this machine.

**Date of audit:** 2026-08-04
**Machine:** Apple M4 laptop, macOS (Darwin 25.2.0)
**Interpreter:** `/usr/bin/python3` — Apple stock CPython **3.9.6**, no numpy, no site-packages,
no compiled helper of any kind. Confirmed by inspection: the only imports across all three
checkers are `json, os, subprocess, sys, tempfile, time` (`check_lower.py`) and `json, os, sys,
time` (`check_witness.py`, `check_duality.py`) — all Python standard library.

**External binaries used: NONE.** `lrat-check` is *not* present in this repository and the
`tools-drat-trim/` directory that `run_all.sh` refers to does not exist; fetching Heule's
drat-trim source would have required downloading a file, which is outside what I may do without
the user's explicit say-so. **Every LRAT proof in the corpus, including the 2.94 GB one, was
therefore replayed with the pure-Python RUP checker inside `check_lower.py`.** This is the
stronger result: zero compiled code sits in the trusted base of this audit.

---

## Headline

| | |
|---|---|
| Certificate checks run | **47** |
| Passed | **47** |
| Failed | **0** |
| Total LRAT bytes replayed | **5,459,315,046 B (5.08 GiB)** |
| Total LRAT replay wall-clock | **≈ 746 s (12.4 min)**, pure Python |
| Peak RSS, worst case | **79 MB** (bb288 K=13, 2.94 GB proof) |
| `manifest.json` SHA-256 entries re-hashed | **182 / 182 match**, 0 missing |
| Negative controls (mine, 11 of them) | **11 / 11 correctly rejected** |
| **IBM BB parity-check matrices vs. arXiv:2308.07915** | **byte-identical, all five codes** |
| Discrepancies found | **4** (documentation / missing artifacts, listed at the end) |

---

## 1. The most important check: are these actually IBM's codes?

A certificate for the wrong matrix is worthless, so this was done first and from scratch.

I wrote `bb_recon.py` (in my session working directory; described in Appendix A, not shipped) directly from the construction
in Bravyi, Cross, Gambetta, Maslov, Rall & Yoder, *"High-threshold and low-overhead fault-tolerant
quantum memory"*, Nature **627**, 778 (2024) / arXiv:2308.07915:

> n = 2ℓm qubits. x = S_ℓ ⊗ I_m, y = I_ℓ ⊗ S_m over GF(2), S_r the r×r cyclic shift.
> A = A₁+A₂+A₃, B = B₁+B₂+B₃ monomials in x, y. **H_X = [A | B]**, **H_Z = [Bᵀ | Aᵀ]**.

with the paper's Table-3 parameters:

| dir | (ℓ, m) | A | B | published |
|---|---|---|---|---|
| `bb72`  | (6, 6)   | x³ + y + y²   | y³ + x + x²   | [[72,12,6]] |
| `bb90`  | (15, 3)  | x⁹ + y + y²   | 1 + x² + x⁷   | [[90,8,10]] |
| `bb108` | (9, 6)   | x³ + y + y²   | y³ + x + x²   | [[108,8,10]] |
| `bb144` | (12, 6)  | **x³ + y + y²** | **y³ + x + x²** | **[[144,12,12]] (gross)** |
| `bb288` | (12, 12) | x³ + y² + y⁷  | y³ + x + x²   | [[288,12,18]] |

Result, for **all five** codes, with the natural x-outer index map i = a·m + b:

* `HX.txt` is **byte-identical** to my reconstructed [A | B];
* `HZ.txt` is **byte-identical** to my reconstructed [Bᵀ | Aᵀ];
* no row operations, no column permutation, no block swap were needed — literally the same file.

Independently recomputed code parameters (k = n − rank H_X − rank H_Z):

| dir | n | rank H_X | rank H_Z | k | published k |
|---|---|---|---|---|---|
| bb72 | 72 | 30 | 30 | **12** | 12 ✓ |
| bb90 | 90 | 41 | 41 | **8** | 8 ✓ |
| bb108 | 108 | 50 | 50 | **8** | 8 ✓ |
| bb144 | 144 | 66 | 66 | **12** | 12 ✓ |
| bb288 | 288 | 138 | 138 | **12** | 12 ✓ |

Row weight 6 and column weight 3 throughout (the paper's weight-6 codes), and H_X H_Zᵀ = 0.

**Verdict: the gross-code certificates are certificates for the gross code.** The one previously
un-audited link between "IBM's [[144,12,12]]" and "the thing this repo proves things about" is now
closed, and closed at the strongest possible level (byte equality, not equivalence).

I additionally re-ran every *algebraic* check (witnesses, pairing side conditions, duality
permutation, symmetry permutations, orbits) a **second time against my reconstructed matrices**
rather than against the shipped `.txt` files, using my own independent implementation
(`indep_alg.py`). All agreed.

Non-BB inputs were checked by inspection and by brute force (§3): `steane/HX.txt` = `HZ.txt` = the
standard [7,4,3] Hamming parity check; `golay/HX.txt` = `HZ.txt` = an 11×23 generator of the
[23,11,8] even Golay subcode (so k = 23−11−11 = 1, the quantum Golay code); the rotated surface
codes have the expected weight-2/weight-4 plaquette structure.

---

## 2. Full check table

Every row was executed as `/usr/bin/python3 <checker> <cert.json>` from the repo root. "Wall" is
the whole process, interpreter start-up included; the bracketed figure is the checker's own
internal timer. `.lrat.gz` archives were decompressed with `gunzip` first (6.2 GB on disk).

### 2.1 Upper bounds — `check_witness.py`

What is checked: H_c·x = 0, H_q·z = 0, x·z = 1 (mod 2), wt(x) = declared weight. Three
matrix–vector products over GF(2); no solver, no proof.

| dir | cert | claim | result | wall | needs beyond stdlib |
|---|---|---|---|---|---|
| steane | witness_X / witness_Z | d_X ≤ 3 / d_Z ≤ 3 | **PASS** | 0.04 s / 0.02 s | none |
| surface3 | witness_X / witness_Z | d ≤ 3 both | **PASS** | 0.02 s / 0.02 s | none |
| surface5 | witness_X / witness_Z | d ≤ 5 both | **PASS** | 0.02 s / 0.03 s | none |
| surface7 | witness_X / witness_Z | d ≤ 7 both | **PASS** | 0.03 s / 0.02 s | none |
| golay | witness_X / witness_Z | d ≤ 7 both | **PASS** | 0.02 s / 0.02 s | none |
| five_qubit | witness.json (symplectic) | d ≤ 3 | **PASS** | 0.02 s | none |
| bb72 | witness_X / witness_Z | d ≤ 6 both | **PASS** | 0.04 s / 0.02 s | none |
| bb90 | witness_X / witness_Z | d ≤ 10 both | **PASS** | 0.03 s / 0.03 s | none |
| bb108 | witness_X / witness_Z | d ≤ 10 both | **PASS** | 0.03 s / 0.03 s | none |
| **bb144** | witness_X / witness_Z | **d_X ≤ 12 / d_Z ≤ 12** | **PASS** | 0.04 s / 0.03 s | none |
| bb288 | witness_X | d_X ≤ 18 | **PASS** | 0.05 s | none |

20/20 pass.

### 2.2 Lower bounds — `check_lower.py` (pure-Python LRAT replay)

What is checked, per certificate: (i) CSS orthogonality H_X H_Zᵀ = 0; (ii) every pairing row in
ker of the quotient matrix; (iii) the rank/spanning condition; (iv) for `_sym` certificates, that
each shipped permutation is a genuine automorphism of both rowspaces, preserves the two qubit
blocks, and that the group it generates is transitive on each block, plus that the forced-literal
patterns are exactly the two the orbit lemma licenses; (v) **regeneration of the entire CNF from
the raw matrices**, and (vi) RUP-with-hints replay of the LRAT against that regenerated clause
list. The shipped `.cnf` is never read.

| dir | cert | K | claim | instances | LRAT bytes | result | wall | peak RSS |
|---|---|---|---|---|---|---|---|---|
| steane | lower_X_K2 / lower_Z_K2 | 2 | d ≥ 3 both | 1 | 699 / 699 | **PASS** | 0.04 / 0.03 s [0.3 / 0.9 ms] | — |
| surface3 | lower_X_K2 / lower_Z_K2 | 2 | d ≥ 3 both | 1 | 518 / 746 | **PASS** | 0.03 / 0.03 s [0.4 / 0.4 ms] | — |
| surface5 | lower_X_K4 / lower_Z_K4 | 4 | d ≥ 5 both | 1 | 4,685 / 7,085 | **PASS** | 0.03 / 0.03 s [1.1 / 1.4 ms] | — |
| surface7 | lower_X_K6 / lower_Z_K6 | 6 | d ≥ 7 both | 1 | 24,939 / 75,107 | **PASS** | 0.04 / 0.04 s [4.9 / 9.4 ms] | — |
| golay | lower_X_K6 / lower_Z_K6 | 6 | d ≥ 7 both | 1 | 226,377 / 226,377 | **PASS** | 0.06 / 0.06 s [24.1 / 24.3 ms] | — |
| five_qubit | lower_K2 (symplectic) | 2 | d ≥ 3 | 1 | 1,514 | **PASS** | 0.03 s [0.4 ms] | — |
| bb72 | lower_X_K5 / lower_Z_K5 | 5 | d ≥ 6 both | 1 | 1,542,208 / 1,928,204 | **PASS** | 0.16 / 0.20 s [136 / 168 ms] | — |
| bb90 | lower_X_K9 | 9 | d_X ≥ 10 | 1 | 128,445,595 | **PASS** | **10.91 s** | 28 MB |
| bb90 | lower_Z_K9 | 9 | d_Z ≥ 10 | 1 | 150,841,943 | **PASS** | **12.95 s** | 32 MB |
| bb108 | lower_X_K9 | 9 | d_X ≥ 10 | 1 | 71,551,704 | **PASS** | **6.23 s** | 25 MB |
| bb108 | lower_Z_K9 | 9 | d_Z ≥ 10 | 1 | 82,276,680 | **PASS** | **7.08 s** | 24 MB |
| **bb144** | lower_X_K11_sym | 11 | **d_X ≥ 12** | 2 (symmetry-broken) | 123,823,246 + 33,824 | **PASS** | **10.09 s** | 30 MB |
| **bb144** | lower_Z_K11 | 11 | **d_Z ≥ 12**, no symmetry lemma | 1 | 671,988,205 | **PASS** | **72.94 s** | 49 MB |
| **bb144** | lower_X_K11 | 11 | **d_X ≥ 12**, no symmetry lemma | 1 | 867,803,294 | **PASS** | **176.37 s** | 51 MB |
| bb288 | lower_X_K9_sym | 9 | d_X ≥ 10 | 2 | 65,337,067 + 103,869 | **PASS** | **5.27 s** | 26 MB |
| bb288 | lower_X_K11_sym | 11 | d_X ≥ 12 | 2 | 350,776,168 + 144,738 | **PASS** | **30.57 s** | 49 MB |
| bb288 | lower_X_K13_sym | 13 | **d_X ≥ 14** | 2 | 2,941,958,076 + 191,479 | **PASS** | **413.61 s** | 79 MB |

23/23 pass. Nothing beyond the Python standard library was required for **any** of them, including
the 2.94 GB bb288 K=13 proof. Note that the internal Python checker *refuses* RAT hints
(`h < 0` → hard exit), so the fact that all 23 replays succeeded also establishes that every proof
in the corpus is pure RUP — a stronger and more easily audited class than general DRAT.

### 2.3 ZX-duality — `check_duality.py`

Two rank computations per certificate: rowspace(H_X·Π) = rowspace(H_Z) and rowspace(H_Z·Π) =
rowspace(H_X).

| dir | result | wall | note |
|---|---|---|---|
| bb72 | **PASS** | 0.02 s [1.4 ms] | Π = block-swap ∘ (a,b) ↦ (−a,−b) |
| bb90 | **PASS** | 0.03 s [1.8 ms] | ditto |
| bb108 | **PASS** | 0.03 s [2.3 ms] | ditto |
| bb144 | **PASS** | 0.03 s [4.1 ms] | ditto |
| bb288 | **NO CERTIFICATE SHIPPED** | — | see Discrepancy D2 |

4/4 shipped duality certificates pass.

### 2.4 Corpus integrity

All 182 files listed in `manifest.json` are present and their SHA-256 and byte counts match
exactly — **0 mismatches, 0 missing**. Because the large proofs ship as `.lrat.gz` and the manifest
hashes the *uncompressed* `.lrat`, this also confirms the gzip archives decompress to precisely the
hashed bytes.

---

## 3. Cross-check that does not use the certificates at all

For every code small enough, I computed the minimum distance by **brute-force enumeration** of the
logical coset space, with code that shares nothing with either the pipeline or the checkers
(`brute.py`): d_X = min wt(x) over x ∈ ker H_Z \ rowspace H_X, enumerated by Gray code over a
kernel basis.

| code | n | k | search space | d_X | d_Z | d = min | certified value | agrees? |
|---|---|---|---|---|---|---|---|---|
| steane | 7 | 1 | 2⁴ | 3 | 3 | **3** | 3 | ✓ |
| surface3 | 9 | 1 | 2⁵ | 3 | 3 | **3** | 3 | ✓ |
| surface5 | 25 | 1 | 2¹³ | 5 | 5 | **5** | 5 | ✓ |
| golay | 23 | 1 | 2¹² | 7 | 7 | **7** | 7 | ✓ |
| surface7 | 49 | 1 | 2²⁵ (242 s) | 7 | 7 | **7** | 7 | ✓ |
| five_qubit | 5 | 1 | 2⁶ symplectic | — | — | **3** | 3 | ✓ |

Six exact distances, six agreements. bb72 and up are out of brute-force reach (2⁴² and beyond),
which is the entire point of the certificates.

---

## 4. Negative controls

`RESULTS.md` cites a `tamper_test/` directory. **It does not exist in this repository** (see D1).
So I built my own, on a scratch copy of `bb72` and `five_qubit`:

| # | tamper | expected | observed |
|---|---|---|---|
| 1 | flip one bit of witness x | reject | **rejected** — "witness does not commute" |
| 2 | understate the witness weight (6 → 4) | reject | **rejected** — "declared weight wrong" |
| 3 | relabel the K=5 certificate as K=6 | reject | **rejected** — "LRAT lemma 2015 NOT verified" |
| 4 | delete the final empty-clause line from the LRAT | reject | **rejected** — "LRAT proof failed" |
| 5 | truncate LRAT to 5,000 of 9,489 lines | reject | **rejected** — "LRAT proof failed" |
| 6 | keep the empty clause, replace its hints with a live-but-wrong id | reject | **rejected** — "hint 1 references deleted/absent clause" |
| 7 | gut the pairing matrix (1 of 12 rows) | reject | **rejected** — "pairing rows do not span ker/row quotient (31 != 42)" |
| 8 | flip one bit of H_X | reject | **rejected** — "CSS condition H_X H_Zᵀ = 0 fails" |
| 9 | swap the sector label X → Z | reject | **rejected** — "pairing row not in kernel of quotient matrix" |
| 10 | corrupt one hint id inside the LRAT | reject | **rejected** — "LRAT lemma 2014 NOT verified" |
| 11 | replace the duality permutation with the identity | reject | **rejected** — "rowspace(HX.Pi) != rowspace(HZ)" |

11/11 correctly rejected.

**Positive control on the "the .cnf is not trusted" claim:** I appended the contradictory pair
`1 0` / `-1 0` to `bb72/lower_X_K5.cnf` and re-ran the checker. It still passed, unchanged and in
the same time — confirming the shipped CNF is genuinely never read and genuinely not in the trusted
base. (See also finding D4 for the one place where a `forced` list *is* accepted without
justification.)

---

## 5. TRUSTED BASE — what a skeptic must actually believe

I read `check_lower.py` line by line and reconstructed the proofs of its side conditions. Below is
the honest inventory. Items marked **CHECKED** are re-verified per certificate at check time by
code you can read; items marked **ASSUMED** are mathematical or engineering facts asserted in
comments and *not* machine-verified anywhere in this repo.

### 5.1 Software you must trust

1. **The three checker scripts**, ~800 lines of Python total (`check_witness.py` 96 lines,
   `check_duality.py` 74, `check_lower.py` 419). That is the whole of it. They import only the
   standard library. I read all three in full.
2. **CPython 3.9.6 and the OS.** No numpy, no solver, no C helper — for *this* audit, `lrat-check`
   was never invoked, so the `--external` code path and the drat-trim binary are outside the
   trusted base entirely. (If you do use `--external`, you re-admit a compiled checker and the
   temp-file marshalling in `check_lrat_external`.)
3. **NOT trusted, and demonstrably so:** CaDiCaL, `certify.py`, `qec_lib.py`, `manifest.py`,
   `gen_duality.py`, the shipped `.cnf` files, `meta.json`, `manifest.json`, and every claim in
   `RESULTS.md`. All of these can be deleted and the certificates still verify.

### 5.2 The reduction from "d ≥ K+1" to "this CNF is UNSAT"

For the CSS X sector the encoding asserts: H_Z x = 0, some pairing row z has z·x = 1, and
wt(x) ≤ K. For this to be *exactly* "there is a nontrivial X-logical of weight ≤ K", one needs

  {x : H_Z x = 0} ∩ (rowspace pairing)^⊥ = rowspace(H_X).

The checker verifies three conditions — **CHECKED**, per certificate, over the raw matrices:

* (a) H_X H_Zᵀ = 0 ⟹ rowspace(H_X) ⊆ ker(H_Z);
* (b) every pairing row ⊥ every row of H_X ⟹ rowspace(H_X) ⊆ (rowspace pairing)^⊥, which gives
  **soundness**: z·x = 1 forces x ∉ rowspace(H_X), so any satisfying x really is a nontrivial
  logical;
* (c) rank(H_Z rows ∪ pairing rows) = n − rank(H_X), which gives **completeness**: the left-hand
  side above is (rowspace H_Z + rowspace pairing)^⊥, of dimension n − rank(H_Z ∪ pairing) =
  rank(H_X) = dim rowspace(H_X); combined with the two inclusions the sets are equal, so *no*
  logical of weight ≤ K escapes the encoding.

I verified this dimension argument by hand and re-verified conditions (a)–(c) numerically against
my own reconstructed matrices. The symplectic (`stab_lower`) analogue — abelian S, L in the
centralizer, rank(S ∪ L) = rank(S) + |L| = n + k — is likewise exact: the radical of ω restricted
to the centralizer C is span(S), so e ∈ C with ω(e,ℓ) = 0 for all ℓ ∈ L forces e ∈ span(S).

### 5.3 What is ASSUMED (stated, not machine-checked)

1. **The Sinz sequential at-most-K counter is complete.** `at_most_k` emits the standard Sinz
   encoding; the argument that every weight-≤K assignment extends to a satisfying assignment of the
   counter variables is a textbook fact, not verified here. If this encoding were accidentally
   *over*-constraining, UNSAT would not mean what is claimed. I read the code against Sinz (2005)
   and it is the standard clause set, with s-variables allocated i-outer/j-inner as documented.
2. **The Tseitin XOR-chain gate is definitional.** The four clauses per gate encode u = a ⊕ b; that
   they are always extendable given a, b is asserted, not checked.
3. **The orbit / symmetry-breaking lemma** (used by every `_sym` certificate: bb144 X sector,
   bb288 all three rungs). Stated in `check_lower.py`'s `verify_symmetry`. I reconstructed the
   proof and it is correct: if every generator π is a rowspace automorphism of both H_X and H_Z
   and preserves the two blocks (**CHECKED** by rank identity and by index comparison), and the
   generated group is transitive on each block (**CHECKED** by BFS), then for any nontrivial
   logical x of weight ≤ K, the relabelling y_j = x_{g(j)} is again a nontrivial logical of the
   same weight; choosing g to move a support element to qubit 0 (if the support meets the left
   block) or to qubit `block` (if not) shows x can be assumed to satisfy one of the two forced
   patterns. Both forced patterns are **CHECKED** to be literally `[1]` and
   `[−1,…,−block, block+1]`. So the *inputs* to the lemma are machine-checked; only the five-line
   implication itself is human-verified. For bb144 and bb288 I additionally identified the two
   permutations independently: they are exactly the torus translations x¹y⁰ and x⁰y¹.
   **The gross code's Z sector, and its X sector a second time, are certified with NO symmetry
   lemma at all** (672 MB and 868 MB single-instance proofs, both re-verified above), so the gross
   code's d = 12 does not depend on this item.
4. **The ZX-duality lemma** in `check_duality.py`: rowspace(H_X Π) = rowspace(H_Z) and vice versa
   ⟹ a weight-preserving bijection between nontrivial X- and Z-logicals ⟹ d_X = d_Z. The two rank
   conditions are **CHECKED**; the four-line implication is human-verified. I re-derived it and it
   holds.
5. **The CSS fact d = min(d_X, d_Z).** Used to convert the certified pair (d_X, d_Z) into a
   statement about the code distance. Not touched by any script.
6. **k is not certified.** `meta.json`'s k is a pipeline output. (I recomputed k = n − rank H_X −
   rank H_Z independently for every code; all match — see §1. Note also that side condition (c)
   pins down the logical space dimension implicitly, so k is not free-floating.)
7. **LRAT semantics.** `check_lrat_python` implements RUP-with-hints: negate the lemma, propagate
   through the hinted clauses in order, demand a conflict. It skips hints that are already
   satisfied or not unit — sound (it can only fail to find a conflict, never invent one). It
   refuses negative (RAT) hints outright. Clause-id reuse and out-of-order ids are not policed, but
   every stored clause is RUP-verified at insertion time against clauses that are themselves
   implied by the regenerated formula, so soundness is preserved by induction. It demands that an
   empty clause be derived *and verified*. I am satisfied this checker is sound.
8. **That `HX.txt` / `HZ.txt` are the intended code.** *Nothing in the corpus establishes this* —
   the checkers take the matrix files at face value. This was the single largest hole in the
   trusted base, and §1 of this document closes it for the five BB codes at byte level.

### 5.4 The honest one-sentence version

> A skeptic must believe: three short standard-library Python files do what they appear to do;
> CPython and macOS are not lying; the Sinz at-most-K and Tseitin XOR encodings are standard and
> complete; the four-line duality lemma and the five-line orbit lemma (the latter only for the
> `_sym` certificates, which the gross code does not depend on) are correct; and d = min(d_X, d_Z)
> for CSS codes. Everything else — the solver, the CNF files, the generator, the manifest, the
> prose — can be thrown away, and the identity of the input matrices is now independently pinned
> to arXiv:2308.07915.

---

## 6. Discrepancies

**D1 — `tamper_test/` does not exist.** `RESULTS.md` ("Negative controls: … see tamper_test/")
cites a directory that is absent from the repository. The claim itself is *true* — I rebuilt the
controls from scratch (§4) and all 11 were rejected — but as shipped, the citation is dangling.
Severity: documentation.

**D2 — bb288 has no duality certificate, so "14 ≤ d ≤ 18" is over-claimed as shipped.**
`RESULTS.md` states "IBM BB [[288,12,18]] — 14 ≤ d ≤ 18 certified (d_X, and d_Z via duality)". But
`certificates/bb288/` contains **no `duality.json`, no `duality_perm.txt`, and no `witness_Z.json`**
(unlike bb72/90/108/144). What the corpus actually certifies for bb288 is **d_X ≥ 14 and d_X ≤ 18**.
Since d = min(d_X, d_Z), the lower bound d ≥ 14 does **not** follow from the shipped artifacts alone.

  This is a missing-file problem, not a mathematical one. `gen_duality.py` *does* list bb288 and
  would emit the certificate; it appears simply not to have been re-run after bb288 was generated
  (`manifest.json` likewise has no bb288 duality entry). I independently confirmed the underlying
  fact: the permutation Π = block-swap ∘ ((a,b) ↦ (−a mod 12, −b mod 12)) satisfies
  rowspace(H_X·Π) = rowspace(H_Z) and rowspace(H_Z·Π) = rowspace(H_X) for bb288, so d_X = d_Z and
  the claim d ∈ [14,18] is **true**. It is just not certified by anything currently in
  `certificates/bb288/`. **Fix: run `python3 gen_duality.py`, then `python3 manifest.py`.**
  Severity: real — a reader re-checking the corpus cannot reproduce the headline bb288 claim.

**D3 — reproduction instructions are incomplete.** `run_all.sh` requires
`tools-drat-trim/lrat-check`, which is not in the repository and for which no source, URL, or
vendored copy is provided; it also requires numpy for the pipeline. `RESULTS.md`'s "independent
check time" column quotes lrat-check numbers (e.g. 72.3 s for bb288 K=13, 6.3 s for bb144 sym) that
cannot be reproduced from the repository as shipped. The pure-Python path *can* be reproduced and
is what I used; my timings are 413.6 s and 10.1 s respectively. Two of the prose's pure-Python
figures are also stale in the *conservative* direction: bb108 is quoted at "21 s pure Python"
(measured: 6.2 s) and bb144 sym at "17.3 s using nothing but Python stdlib" (measured: 10.1 s), and
the quoted throughput "~3.4 MB/s" is actually ~12 MB/s on this machine. Severity: documentation.

**D4 — a genuine (currently unexercised) soundness hole in `check_lower.py`.** In the `css_lower`
branch, a certificate with no `symmetry` block is required to have exactly one instance with an
empty `forced` list:

```python
else:
    assert len(instances) == 1 and instances[0]["forced"] == []
```

The `stab_lower` branch has **no such guard** — it takes `cert["instances"][0]` and passes
`inst["forced"]` straight into `regen_stab`, which emits them as unit clauses. I confirmed this
empirically: adding `"forced": [-1,-2,-3]` to `five_qubit/lower_K2.json` and re-running the checker
yields `OK lower bound: d >= 3` even though the UNSAT result now only covers assignments with
qubits 1–3 excluded from the X-support. The shipped `five_qubit/lower_K2.json` has `forced: []`
(I verified), so **no shipped certificate is affected** — but the checker would accept a forged one.
**Fix: mirror the CSS guard in the `stab_lower` branch** (`assert len(cert["instances"]) == 1 and
cert["instances"][0]["forced"] == []`). Severity: latent checker bug; no impact on any current
result. Two lesser observations in the same vein: `verify_symmetry` does not assert
`len(instances) == 2` (extra instances are harmless, since each is independently replayed), and the
`css_lower` branch does not re-check that `cert["sector"]` is one of `"X"`/`"Z"` (a typo would
silently select the Z branch — though the side conditions then fail, as negative control #9 shows).

Nothing else. No certificate failed, no hash mismatched, no matrix was wrong.

---

## 7. Bottom line

| claim in `RESULTS.md` | independently verified here? |
|---|---|
| Steane, five-qubit, surface d=3,5,7, Golay: d exact | **YES** — certificates pass *and* brute force agrees |
| IBM [[72,12,6]] d = 6 exact | **YES** |
| IBM [[90,8,10]] d = 10 exact | **YES** |
| IBM [[108,8,10]] d = 10 exact | **YES** |
| **IBM gross [[144,12,12]] d = 12 exact** | **YES** — witnesses at weight 12, and d_X ≥ 12 *and* d_Z ≥ 12 each by a single symmetry-free LRAT proof (868 MB / 672 MB), replayed here in pure Python in 176 s / 73 s. The symmetry-broken X proof (124 MB, 10 s) agrees. Input matrices byte-identical to arXiv:2308.07915. |
| IBM [[288,12,18]]: d_X ≥ 14 certified | **YES** — 2.94 GB LRAT replayed in pure Python in 414 s, 79 MB RSS |
| IBM [[288,12,18]]: 14 ≤ d ≤ 18 | **claim is true, artifact is missing** — see D2 |
| checkers need nothing beyond the Python stdlib, even for the gross code | **YES**, and stronger: nothing beyond the stdlib was needed for *any* code in the corpus, up to and including the 2.94 GB proof |
| shipped `.cnf` and the solver are not in the trusted base | **YES** — verified by corrupting the `.cnf` and watching the check still pass |
| negative controls are rejected | **YES**, though `tamper_test/` is missing (D1); I rebuilt 11 controls and all were rejected |

**47 checks run, 47 passed, 0 failed.** The central scientific claim — a certified, independently
re-checkable d = 12 for IBM's gross code, on the *correct* matrices — holds up.

---

## Appendix A — scripts I wrote for this audit

All written and run in the auditing agent's temporary session working directory. **They are
not distributed with this repository** — they were the audit's own throwaway tooling, and an
auditor's scripts carry no more authority than anyone else's. What each did is described
below, precisely so that a skeptical reader can rewrite them independently — which is the
point of an independent audit — rather than replay ours.

* `bb_recon.py` — builds H_X, H_Z for all five BB codes from the arXiv:2308.07915 polynomials
  (Kronecker products of cyclic-shift matrices, GF(2)), compares to the shipped files.
* `bb_exact.py` — byte-level equality test.
* `indep_alg.py` — second independent implementation of the witness check, the three CSS side
  conditions, the duality rank test, and the automorphism/orbit test, run against the reconstructed
  matrices rather than the shipped ones; also identifies the permutations.
* `brute.py` — from-scratch brute-force minimum distance (Gray-code enumeration over a kernel
  basis) for the six small codes, including the 2²⁵ surface-7 search.
* `dual288.py` — identifies the shipped duality permutation family and constructs/verifies the
  missing bb288 one.
* `neg/` — the eleven tamper tests.
