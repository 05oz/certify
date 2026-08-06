# Certify: replayable certificates for machine-checked mathematics

**Archival records (Zenodo):** all versions [doi:10.5281/zenodo.21799111](https://doi.org/10.5281/zenodo.21799111) · Part A (v0.1.x) [doi:10.5281/zenodo.21799112](https://doi.org/10.5281/zenodo.21799112) · Part B (v0.2.0) [doi:10.5281/zenodo.21799780](https://doi.org/10.5281/zenodo.21799780) · Part C (v0.3.0) [doi:10.5281/zenodo.21816010](https://doi.org/10.5281/zenodo.21816010) · Part D (v0.4.0) [doi:10.5281/zenodo.21816018](https://doi.org/10.5281/zenodo.21816018)

Author: Daniel Kirtchakov (Independent researcher, Half Ounce Research) — daniel@halfounce.io. Repository: https://github.com/05oz/certify. Date of this snapshot: 2026-08-05.

Two independent bodies of work live here, sharing a method rather than a subject: **produce an artifact a skeptic can re-check without trusting the tool that made it, then say exactly what still has to be believed.**

| | Part A — Alpöge Keller map (v0.1.0) | Part B — quantum code distances (v0.2.0) |
|---|---|---|
| Subject | Degree minimality in the equivariant class of the Alpöge Keller map; moment-map structure of its cotangent lift | Certified minimum distances of eleven stabilizer codes, through IBM's [[288,12,18]] |
| Artifact | 8 msolve Gröbner unit-ideal certificates + SymPy verification scripts | witness pairs + LRAT unsatisfiability proofs + ZX-duality permutations |
| Checker | `scripts/` (SymPy) | `qec-scripts/` — 649 lines of Python, standard library only |
| Paper | `paper/preprint-dixmier-poisson.*` | `paper/preprint-qec-distances.*` |
| Certificates | `certificates/` | `qec-certificates/` |
| Provenance | [PROVENANCE.md](PROVENANCE.md) §§1–4 | [PROVENANCE.md](PROVENANCE.md) §5, [SWEEP-RECORD-QEC-2026-08-04.md](SWEEP-RECORD-QEC-2026-08-04.md) |

Every mathematical claim in either preprint maps to a script whose `assert` statements pass, or to a stored certificate a checker accepts. Nothing is conjectural unless labeled so.

**Since v0.3.0 two further parts live here under the same method:** **Part C** (v0.3.0) — the first certified determination of the tournament packing numbers ν₃(9) = 9 and ν₃(10) = 12, extending the verified range of Yuster's 2004 formula from n ≤ 8 to n ≤ 10 (`tt3-paper/`, `tt3-certificates/`, `tt3-scripts/`); **Part D** (v0.4.0) — a certificate-backed automorphism exclusion for the [[14,3,5]] quantum code existence question, open since June 2005: any such code has monomial automorphism group of order 2^a·3^b·5^c (`qec1435-paper/`, `qec1435-certificates/`, `qec1435-scripts/`). Both notes passed a three-lens adversarial review (claims-vs-artifacts, priority against primary sources, and a replay audit with negative controls) before release; the decision logs ship as `FIXLOG.md` in each paper directory.

---

# Part A — the Alpöge Keller map

**Degree minimality in the equivariant class of the Alpöge Keller map, and the moment-map structure of its cotangent lift — certificates, verification scripts, and preprint.** All computations carried out with Claude (Fable 5), SymPy 1.14, msolve 0.10.1. Everything here is in characteristic zero.

## Credit — read this first

- **The map.** The degree-7 Keller counterexample F to the Jacobian conjecture in dimension 3 is **Levent Alpöge's**, announced **2026-07-19**. The problem was posed by **Akhil Mathew**; per the announcement, the search that produced the map was run with Claude Fable 5. Everything in this repository is downstream of that example. See T. Tao's expository post (terrytao.wordpress.com, 2026-07-21) and the Secret Blogging Seminar thread (sbseminar.wordpress.com, 2026-07-20).
- **The Dixmier corollary AND the symplectic cotangent lift.** Both are **W. G. P. Mayner's**, from the same repository and the same day. The statement that DC_n is false for n ≥ 3, with the explicit Weyl-algebra endomorphism Ψ_F as witness, was first stated publicly in a Secret Blogging Seminar comment (2026-07-20, 22:08), backed by a GitHub note prepared with Claude Fable 5 (github.com/wmayner/dixmier-counterexample, two commits on 2026-07-21). The accompanying `REPORT.md` §8 in that same repository contains the cotangent lift Φ(q,p) = (F(q), G(q)p), machine-verified there to preserve the standard symplectic form *exactly*, to have det DΦ = 1, and to be non-injective; his priority section §12 lists "the symplectic lift to C⁶" explicitly. **We credit both fully and claim neither.** An earlier version of this README credited Mayner for the Weyl endomorphism only — that was an attribution error, now corrected.
- **Most of the structural material here was anticipated.** The master equation, the anchor lemma, the parked square, the S₃/discriminant computation, the trace identity, and the exact image theorem were all obtained independently here and then found to have earlier public sources: T. Shaska, *Graded Keller maps and the Jacobian Conjecture*, arXiv:2607.20210 (v1 2026-07-22, v2 2026-07-25); the anonymous note at ulam.ai/research/jacobian.pdf (2026-07-20); MathOverflow 513387 (2026-07-20); A. Lou (2026-07-20); and Mayner. [PROVENANCE.md](PROVENANCE.md) §2b gives the claim-by-claim table with dates and theorem numbers. We retain those results for self-containedness and credit priority to those sources.
- **What is actually new here** (as of 2026-08-04): (1) the **degree-minimality theorem** in the weight-(1,−1,−2) equivariant class — no Keller lift of degree ≤ 6 exists at all in the sector containing Alpöge's map, and every degree-≤6 lift elsewhere in the class is an automorphism, by eight msolve unit-ideal certificates over Q reproduced mod 32003; (2) the **moment-map identity** ν∘Φ = μ and the **no-go lemma** (s-free C with s-affine A, B ⟹ automorphism, all weights k, all degrees); and (3) a **reframing**, not a new object: Mayner's Φ identified as an explicit PC_n witness via Adjamagbo–van den Essen, with degrees, momenta, and the quantization identity gr Ψ_F = Φ*. The k = 1, 3 certificates are in progress and are **not** claimed.
- **Open, and not claimed settled here:** JC_2, DC_1 (Zheglov's claimed proof is under review), DC_2, and unconditional minimality of degree 7 among all counterexamples in C^3. Note also that PC_n false for n > 2 is *not* our result — it follows formally from Mayner's ¬DC_3, and is already asserted in secondary sources.

## The claims table

Each row: claim → certificate/artifact → how to re-run. All scripts are pure SymPy and terminate with all asserts passing; the msolve certificates are re-run from their stored input files. **The "Origin" column records who first stated the claim publicly** — "ours" means we have found no earlier public source; everything else is credited. Verification status and priority are independent: a row marked *Mayner* or *Shaska* is still machine-checked here.

| # | Claim | Origin | Certificate / artifact | Re-run |
|---|-------|--------|------------------------|--------|
| 1 | F is Keller: det JF = −2 identically; matches the published form; degrees (7,6,4) | Alpöge (2026-07-19) | `scripts/core_verify.py` (PASS lines) | `python scripts/core_verify.py` |
| 2 | Rational triple collision F(1,−3/2,13/2) = F(−1,3/2,13/2) = F(0,0,−1/4) = (−1/4,0,0) | Alpöge (2026-07-19) | `scripts/core_verify.py` | same |
| 3 | Master equation (all weights k): det JG = C^k · [C·J(B,A) + k·A·J(B,C) + B·J(C,A)]; example bracket = 2 | **Shaska**, arXiv:2607.20210v2 Thm. 8.3 (2026-07-25); divisorial form v1 Thm. 6.1 (07-22) | `scripts/core_verify.py` | same |
| 4 | Critical-line restriction, Wronskian = 2; no-go lemma layer identities | no-go lemma **ours**; critical-line contraction in Shaska Prop. 5.1(1) | `scripts/core_verify.py` | same |
| 5 | Minimal cubic of the cover, trace identity (no u² term: fiber u-values sum to 0) | phenomenon in **Mayner** §4.2 (coord. x) and **Shaska** Rem. 5.4 (coord. s); u-coordinate version ours | `scripts/cover_verify.py` | `python scripts/cover_verify.py` |
| 6 | disc = −4·Δ₁·Δ₂², Δ₁ irreducible ⇒ monodromy full S₃ (cover not Galois) | **MathOverflow 513387** and **Lou** (both 2026-07-20); also Mayner §4.4, Shaska Thm. 4.4(2) | `scripts/cover_verify.py` | same |
| 7 | s ∈ Q(u,p,q) ⇒ F is generically exactly 3:1 | **ulam.ai** Thm. 4.2 / **MO 513387** (2026-07-20) | `scripts/cover_verify.py` | same |
| 8 | Exact image: F misses precisely the punctured curve (4/(27t²), 4/(3t), t), t ≠ 0 | **ulam.ai** Thm. 4.2 (2026-07-20); also Mayner §4.3, Shaska Prop. 5.1 | `scripts/cover_verify.py` (+ preprint §5) | same |
| 9 | Ψ_F is a well-defined unital endomorphism of W₃: (A) [D_j,F_i] = δ_ij, (B) [D_i,D_j] = 0 (all 9 + 9 identities) | **Mayner** (2026-07-20/21) | `scripts/weyl_verify.py`; expanded operators in `scripts/weyl_endomorphism.txt` | `python scripts/weyl_verify.py` |
| 10 | Cotangent lift Φ(q,p) = (F(q), (JF)^{-T} p) is polynomial, MᵀΩM = Ω exactly, det M = 1 | **Mayner**, `REPORT.md` §8 (2026-07-21) | `scripts/dixmier_symplectic_verify.py` | `python scripts/dixmier_symplectic_verify.py` |
| 10b | Component degrees of Φ are (7,6,4,9,10,12) | ours | `scripts/dixmier_symplectic_verify.py` | same |
| 11 | Φ has a rational triple collision in C⁶ (generically 3:1); Φ* is therefore an injective non-surjective Poisson endomorphism — a PC_n witness | non-injectivity of Φ is **Mayner's**; PC_n false for n > 2 follows formally from Mayner's ¬DC_3 via Adjamagbo–van den Essen and is already asserted in secondary sources; the **explicit identification, the momenta, and gr Ψ_F = Φ*** are ours | `scripts/dixmier_symplectic_verify.py` | same |
| 12 | Moment-map preservation: ν∘Φ = μ with μ = xp₁ − yp₂ − 2zp₃ (Hamiltonian C*-equivariance) | **ours** — no occurrence of "moment map" found in the 2026-07/08 literature on this example | `scripts/dixmier_symplectic_verify.py` | same |
| 13 | Degree minimality in the equivariant class: no Keller lift of degree ≤ 6 in the s-in-C sector; eight unit-ideal certificates over Q | **ours** — cf. Shaska Thm. 10.10 (weaker: A, B degree one in the invariants; general case explicitly open) and Mayner §7 (different ansatz, covering degree) | `certificates/ms_*_c0.ms` → `certificates/out_*_q.txt` (each basis = `[1]`) | `msolve -g 2 -f certificates/ms_I-A2c-g1_c0.ms -o out.txt` etc. (8 files) |
| 14 | Same eight certificates reproduced mod 32003 | ours | `certificates/ms_*_c32003.ms` → `certificates/out_*_p.txt` (each basis = `[1]`) | same, on the `_c32003` inputs |
| 15 | Positive control: the degree-7 example satisfies the identical normalized degree-7 system (pipeline provably contains the counterexample) | ours | `scripts/min_verify.py` part `d7control` (exact scaled substitution, asserted); computational record in `certificates/D7CONTROL-NEGATIVE-RESULT.md` (the msolve reduced-basis run on `certificates/ms_D7control_c32003.ms` did not terminate in 600 s — expected for a nonempty variety) | `python scripts/min_verify.py d7control` |

The eight emptiness certificates are the six Branch-I systems `I-A2c-g1`, `I-A2c-g2`, `I-A2L-g1`, `I-A2L-g2`, `I-B2-g1`, `I-B2-g2` and the two full-generality Branch-II systems `II-f0`, `II-f1` (19 and 18 unknowns). Naming: `*_c0` = characteristic 0 input, `*_c32003` = mod 32003 input; `out_*_q.txt` = char-0 output, `out_*_p.txt` = mod-32003 output. A stored output whose reduced Gröbner basis is `[1]` is a Nullstellensatz certificate that the corresponding system is empty.

## Quickstart

```sh
python3 -m venv venv
venv/bin/pip install sympy

venv/bin/python scripts/core_verify.py                 # map, det, collisions, master equation, no-go identities
venv/bin/python scripts/cover_verify.py                # cubic, trace, discriminant, S3, 3:1, image locus
venv/bin/python scripts/weyl_verify.py                 # Weyl endomorphism: CCR (A) and (B), writes weyl_endomorphism.txt
venv/bin/python scripts/dixmier_symplectic_verify.py   # symplectomorphism, C^6 collision, moment map
venv/bin/python scripts/min_verify.py ident            # anchor lemma, layer identities, image certificate at (7/3, 4/27)
venv/bin/python scripts/min_verify.py d7control        # degree-7 positive control (exact scaled substitution)
venv/bin/python scripts/min_verify.py kdet             # det JF = -bracket_k upstairs, k = 1,2,3
venv/bin/python scripts/min_verify.py axis             # axis-target uniqueness certificate
venv/bin/python scripts/min_verify.py I                # SymPy GB reproduction, six Branch-I leaves, mod 32003
venv/bin/python scripts/min_verify.py II               # SymPy GB reproduction, two Branch-II leaves, mod 32003 (may TIMEOUT; see below)

# msolve (https://github.com/algebraic-solving/msolve), v0.10.1 used here:
brew install msolve          # macOS; or build from source
for f in certificates/ms_I-*_c0.ms certificates/ms_II-*_c0.ms;         do msolve -g 2 -f "$f" -o "${f%.ms}.out"; done   # 8 unit ideals over Q
for f in certificates/ms_I-*_c32003.ms certificates/ms_II-*_c32003.ms; do msolve -g 2 -f "$f" -o "${f%.ms}.out"; done   # mod-32003 reproductions
```

Every Python script must end with its `PASS` lines and no assertion failures — with one documented exception: `min_verify.py II` re-derives the two largest systems in SymPy under a 150 s per-leaf alarm, and on many machines prints `[II-f0] TIMEOUT after 150s` / `[II-f1] TIMEOUT after 150s` instead of a result. A timeout is **inconclusive, not a failure**: the proof of Branch-II emptiness is the stored msolve certificates (`ms_II-*` → reduced basis `[1]`), which the loop below replays; the SymPy run is a convenience cross-check. To give SymPy longer over ℚ, `venv/bin/python scripts/min_verify.py QQ II-f0 II-f1` uses a 240 s alarm. Every `ms_I-*`/`ms_II-*` msolve run must output the reduced basis `[1]`, matching the stored `out_*_q.txt` (char 0) and `out_*_p.txt` (mod 32003). Expected runtimes: the six Branch-I systems finish in well under a second each; the two `ms_II-*_c0.ms` char-0 runs take on the order of **5 minutes each** — do not interrupt them. Do not loop `ms_D7control_c32003.ms` in: that reduced-basis run does not terminate in reasonable time (see `certificates/D7CONTROL-NEGATIVE-RESULT.md`); the asserted positive control is `scripts/min_verify.py d7control`.

---

# Part B — certified quantum code distances

**Replayable minimum-distance certificates for stabilizer codes, with no solver and no proof assistant in the trusted base: the bivariate-bicycle family through n = 288.** Paper: [`paper/preprint-qec-distances.pdf`](paper/preprint-qec-distances.pdf).

This is a **verification contribution, not a discovery.** The distance values are largely known and are credited below. What did not exist is a standalone artifact anyone can replay without a SAT solver and without a proof assistant.

## Lead with the audit

The corpus was re-checked by a separate agent instance with no access to the generating pipeline and no shared code. Its report is [INDEPENDENT-VERIFICATION.md](INDEPENDENT-VERIFICATION.md).

| | |
|---|---|
| Certificate checks run | **47** |
| Passed / failed | **47 / 0** |
| LRAT bytes replayed | **5,459,315,046 (5.08 GiB)**, in **pure Python** — no compiled code in the trusted base |
| Peak resident set, worst case | **79 MB** (the 2.94 GB proof) |
| IBM BB parity-check matrices vs. arXiv:2308.07915 | **byte-identical, all five codes** |
| `manifest.json` SHA-256 entries re-hashed | **182 / 182 match** |
| Negative controls | **11 / 11 correctly rejected** |
| Brute-force cross-checks (codes small enough) | **6 / 6 agree** |

## Results

| code | n, k | certified | lower-bound proof | in this repo? |
|---|---|---|---|---|
| Steane [[7,1,3]] | 7, 1 | **d = 3** | 699 B each sector | yes |
| five-qubit [[5,1,3]] (non-CSS) | 5, 1 | **d = 3** | 1,514 B | yes |
| rotated surface d=3 / 5 / 7 | 9 / 25 / 49, 1 | **d = 3 / 5 / 7** | 518 B – 75 kB | yes |
| Golay [[23,1,7]] | 23, 1 | **d = 7** | 226 kB each | yes |
| IBM BB [[72,12,6]] | 72, 12 | **d = 6** | 1.5 / 1.9 MB | yes |
| IBM BB [[90,8,10]] | 90, 8 | **d = 10** | 128 / 151 MB | yes (gzipped) |
| IBM BB [[108,8,10]] | 108, 8 | **d = 10** | 72 / 82 MB | yes (gzipped) |
| **IBM gross [[144,12,12]]** | 144, 12 | **d = 12** | 124 MB symmetry-broken; **868 / 672 MB symmetry-FREE** | symmetry-broken yes; symmetry-free regenerable |
| IBM BB [[288,12,18]] | 288, 12 | **14 ≤ d ≤ 18** | 2.94 GB (K = 13) | K=9 rung yes; K=11, K=13 regenerable |

Four proofs (79 MB–646 MB compressed) are too large for git. [`qec-certificates/REGENERATE.md`](qec-certificates/REGENERATE.md) gives the exact CaDiCaL command, expected byte count, and expected SHA-256 for each. Everything else ships, so a reader with nothing but CPython can still replay a certified **d = 12 for the gross code**.

## Credit — read this first

- **The codes and the distances are IBM's.** The bivariate-bicycle family, including the gross code, is Bravyi, Cross, Gambetta, Maslov, Rall and Yoder, *Nature* **627** (2024) 778 / arXiv:2308.07915. Their distances were computed there by the MIP method of Landahl, Anderson and Rice (arXiv:1108.5738). The gross-code value `d = 12` was confirmed exactly, at MIP gap 0, by Cruz-Benito, Cross, Kremer and Faro (IBM, arXiv:2606.02418, 1 Jun 2026). **We claim no distance value.**
- **`d_X = d_Z` for BB codes is Bravyi et al.'s lemma**, from their supplemental material. Only the explicit permutation, packaged as a ~15 ms checkable certificate, is ours.
- **Machine-checked quantum distance proofs are LEAN-QEC's** (arXiv:2605.16523). Their *paper* dispatches the gross code to `cvc5` outside the Lean kernel and calls kernel replay "the next concrete engineering target" — but **their repository has moved past their paper**: commit `c73827d` (2026-07-10) records a full [[144,12,12]] verification via `bv_decide` in about 30 minutes, including kernel replay. **We claim no priority for a machine-checked gross-code distance.** What differs, at that commit: their `BB144.lean` carries two `sorry`s (`BB144_X_ker_rank` L69, `BB144_Z_ker_rank` L72) that `BB144_dist_12` routes through; three lemmas use `native_decide`, which their own paper notes extends the trusted base with Lean's compiler; no LRAT artifact is committed for BB144; and their encoding is symmetry-broken only. Ours has no admitted lemmas, ships the artifacts, includes symmetry-**free** proofs, and needs no proof assistant. Their kernel-checked ladder should **not** be described as reaching n = 108 either: `BB108.lean` carries `sorry` at L120 and L132 with `--bv_decide` commented out.
- **[[288,12,18]], stated correctly.** Bravyi et al. assert `d = 18` **exactly**, by ILP, without shipping a checkable artifact — their Table 3 lists it with no "≤", unlike [[360,12,≤24]]. Our interval [14,18] is **not** new information about the value. What is defensible, and all we claim: Chen, Jafari and Lai (arXiv:2606.12445) report `d ≥ 11` solver-asserted with no proof artifact in their repository; we certify `d_X ≥ 14` with a 2.94 GB LRAT that replays independently — improving the strongest quantity previously published *as a lower bound*, and the only machine-checkable one on record for this code.
- **Also prior art, cited at point of use:** QDistRnd (JOSS 2022, upper bounds only, "no performance guarantee"); Stim's `search_for_undetectable_logical_errors` (documented verbatim as "THIS IS A HEURISTIC METHOD"); the Webster–Jacob–Higgott survey (arXiv:2603.22532); PBLean (arXiv:2602.08692); Heule's `drat-trim`/LRAT; Biere's CaDiCaL; Sinz's cardinality encoding; Tseitin's gate encoding.

The dated adversarial sweep behind these statements is [SWEEP-RECORD-QEC-2026-08-04.md](SWEEP-RECORD-QEC-2026-08-04.md). It broke two claims of an earlier draft; both were withdrawn.

## Quickstart (Part B)

No virtual environment, no packages, no compiled binary — the checkers import only the Python standard library.

```sh
# small, instant
python3 qec-scripts/check_witness.py  qec-certificates/steane/witness_X.json
python3 qec-scripts/check_lower.py    qec-certificates/steane/lower_X_K2.json
python3 qec-scripts/check_lower.py    qec-certificates/golay/lower_X_K6.json

# the gross code, d = 12, from artifacts in this repository
gunzip qec-certificates/bb144/*.lrat.gz
python3 qec-scripts/check_witness.py  qec-certificates/bb144/witness_X.json     # d_X <= 12
python3 qec-scripts/check_lower.py    qec-certificates/bb144/lower_X_K11_sym.json  # d_X >= 12
python3 qec-scripts/check_duality.py  qec-certificates/bb144/duality.json       # d_X = d_Z

# n = 288
gunzip qec-certificates/bb288/*.lrat.gz
python3 qec-scripts/check_lower.py    qec-certificates/bb288/lower_X_K9_sym.json   # d_X >= 10
python3 qec-scripts/check_duality.py  qec-certificates/bb288/duality.json

# integrity: re-hash every artifact against the audited manifest
python3 qec-scripts/verify_manifest.py
```

Expected runtimes: everything above is seconds, except the bb144 `lower_X_K11_sym`
replay (~10–15 s in pure Python) and the bb288 `lower_X_K9_sym` replay (~5–10 s).

`verify_manifest.py` reports `172 match, 0 mismatch, 10 absent` on a fresh clone: the
ten "absent" are the six proofs that ship gzipped (decompress them and they match, since
the manifest hashes the *uncompressed* bytes) and the four that are too large for git.
After `gunzip qec-certificates/*/*.lrat.gz` the count is 178 match, 4 absent.

Note that `qec-scripts/manifest.py` is the *pipeline's* manifest generator, not a verifier:
it expects a `certificates/` directory beside itself and it **overwrites** `manifest.json`.
It is included because it is part of the pipeline, and the pipeline is explicitly not trusted.

`check_lower.py` never reads the shipped `.cnf`: it regenerates the CNF from the raw parity-check matrices and replays the LRAT against its own clause list. Corrupting a shipped `.cnf` changes nothing, and the audit confirmed that by doing it.

## Known gaps in Part B

1. `bb288/duality.json` was generated **after** the audit closed — it passes `check_duality.py` and its permutation was independently re-verified, but it is outside the 47 audited checks and absent from `manifest.json`.
2. `manifest.json` covers the full audited corpus including the four large proofs this repository does not carry.
3. The shipped `check_lower.py` is 481 lines; the auditor read 419. The difference is an optional totalizer cardinality encoding that no certificate in this release selects. The whole corpus was re-run against the shipped 481-line checker before release — 20 witnesses, 5 duality certificates, 23 lower-bound certificates, **48 in all, every one accepted**, including a second pure-Python replay of the 2.94 GB proof.
4. `run_all.sh` expects a `tools-drat-trim/lrat-check` binary that is not vendored. The pure-Python path needs nothing but CPython and is what every number in the paper reports.

Three further defects the audit found are reported verbatim in §8 of the paper, including a latent soundness hole in a checker branch that no shipped certificate exercises. A paper about trusted bases that suppresses its own audit findings is not one.

---

# Part C — tournament packing numbers ν₃(9), ν₃(10)

**The first certified determination of ν₃(9) = 9 and ν₃(10) = 12**, where ν₃(n) is the minimum over all n-vertex tournaments of the maximum number of arc-disjoint transitive triples, confirming Yuster's conjectured formula ⌈n(n−1)/6 − n/3⌉ at n = 9, 10. Paper: [`tt3-paper/note.pdf`](tt3-paper/note.pdf).

- **Credit.** The quantity and the formula are R. Yuster's (2004), who verified n ≤ 8 (n ≤ 7 by direct argument, n = 8 by computer, uncertified); the matching upper-bound constructions are also **Yuster's (2004)** — the note's new content is the certified integral **lower bounds** over all isomorphism classes (191,536 at n = 9; 9,733,056 at n = 10), plus SAT optimality certificates on the minimizing tournaments. Kabiya–Yuster 2008 supplies the fractional strengthening and is credited at point of use.
- **Declared trust assumption:** `gentourng` (nauty) enumerates completely — cross-validated exhaustively for n ≤ 7 and count-validated against OEIS A000568 and exact Burnside numbers at n = 9, 10.
- **Replay:** exact commands, file inventory, and all 32 MD5 pins are in [`tt3-paper/note.md`](tt3-paper/note.md) §6 ("Artifacts"); certificates in `tt3-certificates/` (LRAT optimality proofs `min9_ge10.lrat`, `min10_ge13.lrat` replay against `tt3-scripts/` with stock Python), full sweep logs included. Expected runtimes: the n = 9 sweep verification is seconds; the full n = 10 sweep verification over all sixteen gzipped slices takes ~2–3 minutes.
- The adversarial review that preceded release re-verified the sweeps with independently written code (fresh enumeration, an independent exact solver on both minimizers, negative controls); the dated novelty sweep is [SWEEP-RECORD-TT3-2026-08-05.md](SWEEP-RECORD-TT3-2026-08-05.md).

# Part D — [[14,3,5]]: a certificate-backed automorphism exclusion

**If a [[14,3,5]] qubit stabilizer code exists, its monomial automorphism group has order 2^a·3^b·5^c** — no automorphism of order divisible by 7, 11, or 13 is possible. The existence question itself, open since the [[14,3]] table entry's construction of June 2005 (codetables.de, retrieved 2026-08-05), **remains open and is not claimed**. Paper: [`qec1435-paper/note.pdf`](qec1435-paper/note.pdf).

- **Credit.** The open entry is recorded in M. Grassl's codetables.de; the automorphism question descends from Ball–Centelles–Huber 2020 (Research Problem 1). The **CSS case is settled by Koh et al., arXiv:2601.20927** (exhaustive CSS enumeration at n ≤ 14; their Table VI gives max CSS [[14,3]] distance 4) — that result is theirs, cited and not claimed; an earlier in-house CSS derivation is subsumed and appears only as a remark. Cross–Vandeth arXiv:2501.17447 covers general stabilizer enumeration at n ≤ 9.
- **What ships:** 43 certificate files (`qec1435-certificates/`, SHA-256-pinned in the paper), the generators and the independent checker (`qec1435-scripts/`, incl. `check1435.c` and `verify_1435.py`), and the classical code tables used (`qec1435-scripts/data/`). Every candidate of every nonzero symmetry class was distance-checked; an exact-rational Krawtchouk LP lemma closes the fixed-qubit branches (a second LP lemma belongs to the order-5 work in progress, outside the theorem). Scope, gaps, and unarchived intermediate runs are disclosed in the paper itself (§5, §7).
- **Replay:** commands in [`qec1435-paper/note.md`](qec1435-paper/note.md) §7; quick control: `python3 qec1435-scripts/verify_1435.py qec1435-scripts/data/ct_14_3_stab.txt` reproduces the d = 4 control verdict. Dated novelty sweep: [SWEEP-RECORD-1435-2026-08-05.md](SWEEP-RECORD-1435-2026-08-05.md).

---

## Layout

```
README.md            this file
PROVENANCE.md        timeline, what is new, how to verify, what is not claimed (§§1-4 Part A, §5 Part B)
CITATION.cff         citation metadata
.zenodo.json         Zenodo deposit metadata
LICENSE-CODE         Apache-2.0 (code and machine-readable certificates)
LICENSE-DOCS         CC-BY-4.0 (prose and paper)
paper/               both preprints (LaTeX + PDF + readable Markdown mirror)

  -- Part A: Alpoge Keller --
certificates/        17 msolve input files (ms_*.ms) + stored outputs (out_*.txt) + D7 control record
scripts/             the verification scripts (incl. min_verify.py) + expanded Weyl operators
schema/              certificate-schema (pending; see schema/PENDING.md)
checker/             independent certificate checker (pending; see checker/PENDING.md)

  -- Part B: quantum code distances --
qec-certificates/    the certificate corpus, by code; manifest.json; REGENERATE.md
qec-scripts/         the three checkers (check_witness / check_lower / check_duality),
                     verify_manifest.py, and the (untrusted) generating pipeline
INDEPENDENT-VERIFICATION.md   the audit: 47/47 checks, 5.08 GiB replayed in pure Python
SWEEP-RECORD-QEC-2026-08-04.md   the dated adversarial prior-art sweep

  -- Part C: tournament packing (v0.3.0) --
tt3-paper/           note (LaTeX + PDF + Markdown mirror) + FIXLOG.md review log
tt3-certificates/    minimizers, SAT optimality certificates (LRAT), full sweep logs, MD5SUMS.txt
tt3-scripts/         tt3pack.c searcher, CNF encoder, stdlib-only independent verifiers
SWEEP-RECORD-TT3-2026-08-05.md   dated novelty sweep

  -- Part D: [[14,3,5]] automorphism exclusion (v0.4.0) --
qec1435-paper/       note (LaTeX + PDF + Markdown mirror) + FIXLOG.md review log
qec1435-certificates/  43 SHA-256-pinned certificates by symmetry class
qec1435-scripts/     generators, check1435.c, verify_1435.py, data/ classical code tables
SWEEP-RECORD-1435-2026-08-05.md  dated novelty sweep
```

For Part A, the reduction library and the system generators are intentionally not part of this repository; the published claims are the certificates themselves plus the verification scripts, which are self-contained. For Part B, the generating pipeline **is** included (`qec-scripts/certify.py`, `qec_lib.py`, `run_all.sh`) precisely because it is *not* trusted: it can be deleted and every certificate still verifies.

## Licensing

Dual license by content type:

- **Code and machine-readable certificate files** — everything under `scripts/`, `certificates/`, `schema/`, `checker/`, `qec-scripts/`, `qec-certificates/` — are licensed under the **Apache License 2.0** ([LICENSE-CODE](LICENSE-CODE)).
- **Documentation and the paper** — `paper/`, `README.md`, `PROVENANCE.md`, and all other prose — are licensed under **CC BY 4.0** ([LICENSE-DOCS](LICENSE-DOCS)).

## Citing

See [CITATION.cff](CITATION.cff). Archival DOIs are minted per release on Zenodo — concept DOI for all versions [10.5281/zenodo.21799111](https://doi.org/10.5281/zenodo.21799111); Part A (v0.1.x) [10.5281/zenodo.21799112](https://doi.org/10.5281/zenodo.21799112); Part B (v0.2.0) [10.5281/zenodo.21799780](https://doi.org/10.5281/zenodo.21799780); Part C (v0.3.0) [10.5281/zenodo.21816010](https://doi.org/10.5281/zenodo.21816010); Part D (v0.4.0) [10.5281/zenodo.21816018](https://doi.org/10.5281/zenodo.21816018). To cite an individual result, cite its note and the matching version DOI. External timestamps for this repository's claims begin at the first public push and the Zenodo deposits — not at local file dates (see PROVENANCE.md §3).

## Contact

Daniel Kirtchakov — daniel@halfounce.io
