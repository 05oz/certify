# PROVENANCE

This file states exactly who did what, when, what this repository claims as new, how each claim is verified, and what is not claimed. It is written to be checkable: every date below is either a public timestamp controlled by someone else, or a claim of ours whose external timestamp begins only when this repository is first pushed publicly or deposited with a DOI.

The repository now carries **four independent bodies of work**. Part A (v0.1.0) is the Alpöge–Keller / Dixmier–Poisson material: §§1–4 below. Part B (v0.2.0) is the quantum error-correction certificate corpus: §5 below. Part C (v0.3.0, tournament packing numbers) and Part D (v0.4.0, the [[14,3,5]] automorphism exclusion) were added on 2026-08-05: see §6 below for their release-boundary facts, and each paper directory's note and FIXLOG for their own provenance statements. They share nothing but an author, a method, and a discipline about credit.

## 1. Timeline

| Date (2026) | Event | Actor | Evidence |
|---|---|---|---|
| Jul 19 | Announcement of an explicit degree-7 Keller counterexample F to the Jacobian conjecture in dimension 3 (JC₃ false, hence JC_n false for all n ≥ 3). The problem was posed by Akhil Mathew; per the announcement, the search that produced the map was run with Claude Fable 5. | Levent Alpöge | Public announcement of 2026-07-19; see the two posts below, which record and discuss it. |
| Jul 20, 04:32 EDT | Independent derivation of the map, explaining why geometric degree 3 is forced. | A. Lou | https://aaronlou.com/jacobian_counterexample_derivation.pdf (PDF CreationDate 2026-07-20 04:32 EDT) |
| Jul 20, 05:54 EDT | **Earliest published exact image theorem and fiber counts** (3/1/0) with the image complement Γ given explicitly (Thm. 4.2), plus a (λ,a,c,H) family (Thm. 5.1) and nonproper Keller maps of every generic degree ≥ 3 (Cor. 5.3). | Anonymous | https://ulam.ai/research/jacobian.pdf (PDF CreationDate 2026-07-20 05:54 EDT) |
| Jul 20, 07:56 UTC | **Earliest public S₃-monodromy analysis**: explicit cubic model, discriminant, full S₃, trivial deck group, and the Campbell/Razar/Wright Galois-case theorem invoked. Zero answers as of 2026-08-04. | MathOverflow 513387 | https://mathoverflow.net/q/513387 |
| Jul 20 | Expository blog post and comment thread on the counterexample. | D. E. Speyer (Secret Blogging Seminar) | https://sbseminar.wordpress.com/2026/07/20/the-new-counterexample-to-the-jacobian-conjecture/ |
| Jul 20, 22:08 | **First public statement of the Dixmier corollary**: DC_n is false for n ≥ 3, witnessed by the explicit Weyl-algebra endomorphism Ψ_F attached to F. | W. G. P. Mayner | Comment on the Secret Blogging Seminar thread above, timestamped 2026-07-20 22:08. |
| Jul 21, 05:36 + 06:41 UTC | GitHub repository with two artifacts: a six-page note (`dixmier-note.tex`) constructing Ψ_F, its exact image, non-members, codimension table and non-f.g. cokernel; and `REPORT.md`, a wider structural study whose **§8 contains the cotangent lift Φ(q,p) = (F(q), G(q)p)** with machine-verified statements that it preserves the standard symplectic form *exactly*, that det DΦ = 1, and that it is non-injective (verified-facts table item 24), and whose priority section §12 lists "the symplectic lift to ℂ⁶" as item 3. Also §4.2 the trace-zero cubic, §4.3 the exact image, §4.4 S₃ monodromy, §6 the ℂ*-equivariance, §7 a quadratic no-go in the line-congruence ansatz. Not on arXiv; no DOI. | W. G. P. Mayner | https://github.com/wmayner/dixmier-counterexample (both commits 2026-07-21, verified via the GitHub API) |
| Jul 21 | Expository post digesting the counterexample. | T. Tao | https://terrytao.wordpress.com/2026/07/21/a-digestion-of-the-jacobian-conjecture-counterexample/ |
| Jul 22 (v1), Jul 25 (v2) | **Graded Keller maps and the Jacobian Conjecture.** v1: Thm. 4.4(2) S₃ monodromy; Prop. 5.1 fiber counts 3/1/0 and the missed curve {(4/27·t⁻², 4/3·t⁻¹, t)}; Thm. 6.1 the order-two vanishing of the quotient Jacobian on the contracted locus. v2 adds: **Thm. 8.3 the master equation** (the same trilinear bracket identity, with Keller ⟺ constant), **Lem. 8.5 the base-point/anchor identity**, §9.2 "The master equation" in dimension n, and §10 a classification whose Thm. 10.10 gives emptiness only for A, B of degree one in the invariants (the general case explicitly left open). | T. Shaska | arXiv:2607.20210v1 (2026-07-22 14:30 UTC), v2 (2026-07-25 13:48 UTC); LaTeX source of both versions read directly. |
| Jul 22 – Jul 31 | Further consequence papers: Jelonek arXiv:2607.20597; Migus arXiv:2607.21572; Huq-Kuruvilla arXiv:2607.20968; Meng–Yang arXiv:2607.22198; Long arXiv:2607.18186; Zhu arXiv:2607.18166; Gao arXiv:2608.00222. **None contains Dixmier, Poisson, Weyl, symplectic or moment-map content** (checked by full-text grep of the arXiv sources). | various | arXiv |
| Aug 4 | This repository assembled: verification scripts (all asserts passing), eight Gröbner-basis emptiness certificates over ℚ reproduced mod 32003, and the preprint draft stating the results of §2 below. **A first-hand prior-art check on this date established that most of the structural material previously claimed here as new was anticipated by the July 2026 sources above; the preprint and this file were re-scoped accordingly.** Computations with Claude (Fable 5), SymPy 1.14, msolve 0.10.1. | Daniel Kirtchakov | This repository. **The external timestamp for everything in §2 begins at the first public push / DOI mint, not at this date.** |

| Aug 4 | QEC certificate corpus assembled and independently audited (47/47 checks passed, 5.08 GiB of LRAT replayed in pure Python, all five bivariate-bicycle parity-check matrices rebuilt byte-identically from arXiv:2308.07915). A full-text adversarial prior-art sweep on the same date withdrew two claims of an earlier draft; see `SWEEP-RECORD-QEC-2026-08-04.md` and §5 below. | Daniel Kirtchakov | This repository; `INDEPENDENT-VERIFICATION.md`. |

## 2. What this repository claims as new (as of 2026-08-04, after the prior-art check)

*(Part A — the Alpöge–Keller material. For the QEC claims see §5.)*

Two results, plus one reframing. Everything else in the preprint is either downstream of Alpöge's map or anticipated by the sources in §1, and is retained for self-containedness only.

1. **Degree minimality in the equivariant class.** In the weight-(1,−1,−2) class — maps F = (A/x², B/x, xC) with A, B, C ∈ ℂ[u,s] subject to the lift conditions — no Keller lift of degree ≤ 6 exists at all in the sector where C involves s (the sector containing Alpöge's map), and every degree-≤6 Keller lift elsewhere in the class is a polynomial automorphism of ℂ³. Eight msolve unit-ideal certificates over ℚ, reproduced mod 32003, plus a degree-7 positive control. *Nearest prior statements, and why they are different:* Shaska Thm. 10.10 (arXiv:2607.20210v2, 2026-07-25) proves emptiness only when A and B both have degree one in the invariants, and explicitly leaves the general case open ("whether 𝒦(3,(1,−1,−1)) is empty we do not know"); Mayner §7 proves a quadratic no-go about the *covering* degree in a different (line-congruence) ansatz; Jelonek (arXiv:2607.20597) proves the opposite kind of statement (generic elements of X(n,d) for d ≥ 6 are counterexamples, conditional on irreducibility).
2. **The moment-map identity, and the no-go lemma.** (a) The ℂ*-action lifts Hamiltonianly to T*ℂ³ ≅ ℂ⁶ with moment map μ = xp₁ − yp₂ − 2zp₃, the target carries the weight-(−2,−1,1) action with ν = −2Q₁P₁ − Q₂P₂ + Q₃P₃, and the cotangent lift preserves it exactly: **ν∘Φ = μ**. No occurrence of "moment map" was found anywhere in the July–August 2026 literature on this example. (b) The no-go lemma: if C is s-free and A, B are at most affine in s, every Keller lift is a polynomial automorphism — at any degree, for every weight k ≥ 1.
3. **A reframing, not a new object: the Poisson-conjecture identification.** The cotangent lift Φ(q,p) = (F(q), (JF(q))⁻ᵀ p), the fact that it preserves the symplectic form exactly, that det JΦ = 1, and that it is non-injective, are **W. G. P. Mayner's** (`REPORT.md` §8, commits of 2026-07-21). The conclusion that PC_n is false for n > 2 is also not new: it follows formally from ¬DC₃ via Adjamagbo–van den Essen, and Wikipedia already asserts it. What this repository adds is (i) the explicit identification of Φ* as the PC_n witness in the Adjamagbo–van den Essen formulation, (ii) the component degrees (7,6,4,9,10,12) and the explicit momenta of a rational triple collision in ℂ⁶, (iii) the quantization identity gr Ψ_F = Φ*, and (iv) a non-invertibility proof that is two lines from the collision. **An earlier version of this file credited Mayner for the Weyl endomorphism only, and claimed the symplectic lift as new. That was an attribution error and is corrected here.**
4. **The k = 1, 3 minimality certificates** (other torus weights): in progress; **not** part of this snapshot's claims and not to be cited as a result.

### 2b. Claim-by-claim priority for the material we do *not* claim

| Item as stated in the preprint | Earliest verified public source | Date (2026) |
|---|---|---|
| Weyl endomorphism Ψ_F, ¬DC_n for n ≥ 3 | Mayner, SBS comment; then `dixmier-note.tex` | Jul 20 / 21 |
| Cotangent lift Φ; Φ*ω = ω exactly; det DΦ = 1; non-injective | Mayner, `REPORT.md` §8 (table item 24; priority §12 item 3) | Jul 21 |
| Master equation (trilinear bracket = const ⟺ Keller) | Shaska, arXiv:2607.20210**v2**, Thm. 8.3 (§9.2 is titled "The master equation") | Jul 25 |
| Parked square / order-two vanishing on the contracted locus | Shaska, Thm. 7.1 of v2 = Thm. 6.1 of v1 | Jul 22 |
| Anchor lemma (base-point evaluation of the bracket) | Shaska, v2 Lem. 8.5 | Jul 25 |
| S₃ monodromy, non-Galois, disc not a square, Campbell's theorem as the reason | MathOverflow 513387; Lou; then Mayner §4.4, Shaska Thm. 4.4(2) | Jul 20 |
| Trace-free fiber cubic | Mayner §4.2 (coordinate x); Shaska Rem. 5.4 (coordinate s) | Jul 21 |
| Exact image: complement is a single punctured rational curve; fiber counts 3/1/0 | ulam.ai Thm. 4.2; also Mayner §4.3, Shaska Prop. 5.1 | Jul 20 |
| Leading-form / degree pattern analysis behind "anatomy of the exit at degree 7" | Shaska v2 Thm. 10.6 + Example 10.9 | Jul 25 |

**Limits of this survey.** The table rests on a targeted search of the July–August 2026 record and cannot prove a negative. MathOverflow question 513390, referenced in Mayner `REPORT.md` §12, could not be retrieved (404; absent from the StackExchange API) and is therefore neither cited nor relied upon.

## 3. How to verify

Every claim of §2 (items 1–3) maps to a script or certificate in this repository whose checks pass. Note that "verified" here means the mathematics is machine-checked; it says nothing about priority, for which see §2b.

| Claim | Verifier | Pass condition |
|---|---|---|
| Φ polynomial, MᵀΩM = Ω, det M = 1, triple collision in ℂ⁶, ν∘Φ = μ (Φ and the first three are Mayner's; ν∘Φ = μ is ours) | `scripts/dixmier_symplectic_verify.py` | all asserts pass |
| Ψ_F well defined (CCR identities (A) and (B)) — Mayner's construction, independently re-verified | `scripts/weyl_verify.py` | all asserts pass; prints `ALL CHECKS PASS` |
| det JF = −2, collisions, master equation, anchor/no-go layer identities | `scripts/core_verify.py` | all asserts pass; prints `ALL CORE CHECKS PASS` |
| Cover cubic, trace identity, disc = −4Δ₁Δ₂², S₃ monodromy, generic 3:1, image locus | `scripts/cover_verify.py` | all asserts pass |
| Eight emptiness certificates (degree ≤ 6, both branches) over ℚ | `certificates/ms_*_c0.ms` vs stored `certificates/out_*_q.txt` | msolve reduced basis = `[1]` (unit ideal) for all eight |
| Same, mod 32003 | `certificates/ms_*_c32003.ms` vs stored `certificates/out_*_p.txt` | reduced basis = `[1]` for all eight |
| Degree-7 positive control | `scripts/min_verify.py` part `d7control` (exact scaled substitution: nu^5 = 1/2, r = −1/nu, bracket == 1 with C1-coefficient == 1, asserted); record in `certificates/D7CONTROL-NEGATIVE-RESULT.md` | all asserts pass. (The msolve reduced-basis run on `certificates/ms_D7control_c32003.ms` did not terminate within a 600 s cap — expected for a nonempty positive-dimensional variety; the input file is retained for the record.) |

Two things stated plainly:

- **Local file dates prove nothing.** The modification times in this repository are local and freely editable; we do not offer them as evidence of anything. External, third-party-checkable timestamps for our claims begin at the **first public push of this repository and/or the minting of its Zenodo DOI** — whichever comes first — and priority questions should be judged from those, from the arXiv submission, and from the public record in §1.
- **Verification is independent of us.** The scripts are short, self-contained SymPy programs; the msolve inputs are plain-text ideal presentations. Anyone can re-run everything (see README quickstart) without trusting this repository's outputs.

## 4. What we do not claim

- **The counterexample itself.** F is Alpöge's (announced 2026-07-19; problem posed by Akhil Mathew; search run with Claude Fable 5, per the announcement). Nothing here is a claim on the map or its discovery.
- **The first statement of the Dixmier corollary.** That is Mayner's (2026-07-20, 22:08, SBS comment; GitHub note of 2026-07-21 with the explicit endomorphism, exact image, and cokernel results). Our Weyl-algebra section is an independent confirmation and adds only the quantization framing.
- **The cotangent lift Φ and its symplectic properties.** Also Mayner's, from the same repository and the same day (`REPORT.md` §8). We do not claim the object, only its identification as a PC_n witness and the moment-map identity attached to it.
- **The master equation, the anchor lemma, the parked square, the S₃/discriminant computation, the trace identity, and the exact image theorem.** All anticipated; see §2b for the precise sources and dates. We obtained them independently and retain them for self-containedness, with priority credited.
- **Any of the open problems.** JC₂ (planar), DC₁ (Zheglov's claimed proof is under review at the time of writing), and DC₂ remain open. Unconditional minimality of degree 7 among all counterexamples in ℂ³ remains open — our minimality theorem is relative to the stated equivariant class.
- **Anything beyond characteristic-zero algebra.** In particular, nothing here concerns quantum hardware or physical quantization, and nothing here has any bearing on markets, securities, or any financial instrument. The words "quantum" and "moment" above are mathematical terms of art (Weyl algebras, moment maps), nothing more.

---

## 5. Part B — the QEC certificate corpus (v0.2.0, 2026-08-04)

Everything in this section concerns `qec-certificates/`, `qec-scripts/`, and
`paper/preprint-qec-distances.*`. It is a **verification contribution, not a
discovery**: the distance values are largely known and are credited below at
full strength. What did not exist is a standalone artifact anyone can replay
without a SAT solver and without a proof assistant.

The claim strengths below are the ones the adversarial sweep of 2026-08-04 left
standing. Two claims of an earlier draft did not survive it and were withdrawn;
`SWEEP-RECORD-QEC-2026-08-04.md` records both, with the sources that broke them.

### 5a. What is claimed, at its corrected strength

| # | Claim | Origin | Certificate / artifact | Re-run |
|---|-------|--------|------------------------|--------|
| 16 | A certificate format for quantum minimum distance in which **neither the solver nor the shipped CNF is in the trusted base**: the checker regenerates the CNF from the raw parity-check matrices and machine-checks the three algebraic side conditions that make the encoding exact | **ours** | `qec-scripts/check_lower.py` (481 lines), Theorem 3.1 of the paper | `python3 qec-scripts/check_lower.py qec-certificates/<code>/lower_*.json` |
| 17 | Certified `d = 3` (Steane, five-qubit, rotated surface d=3), `d = 5`, `d = 7` (rotated surface d=7, Golay) | values are textbook | witnesses + LRAT proofs, all shipped | as above |
| 18 | Certified `d = 6` for BB [[72,12,6]]; `d = 10` for [[90,8,10]] and [[108,8,10]] | **values are Bravyi et al.**, arXiv:2308.07915 Table 3, by the MIP method of arXiv:1108.5738; also computed exactly by SAT in arXiv:2606.12445. Replayable Lean artifacts exist for several of these in the LEAN-QEC repository | witnesses, LRAT proofs, duality certificates | as above |
| 19 | Certified `d = 12` for the IBM gross code [[144,12,12]], including a **symmetry-free** proof in each sector, so that no symmetry lemma enters the trusted base | **value is Bravyi et al.**; confirmed exactly at MIP gap 0 by Cruz-Benito, Cross, Kremer, Faro (IBM), arXiv:2606.02418; reproduced by SAT in arXiv:2606.12445. A **machine-checked** proof is **also not ours** — LEAN-QEC's repository reports a completed `bv_decide` verification incl. kernel replay at commit `c73827d`, 2026-07-10. **No priority claimed.** What is ours: the certificate format, the symmetry-free variant, and the trusted base | `bb144/witness_{X,Z}.json`, `lower_X_K11_sym.json` (shipped), `lower_{X,Z}_K11.json` (proofs regenerable, see `qec-certificates/REGENERATE.md`), `duality.json` | as above |
| 20 | Certified `d_X >= 14` for BB [[288,12,18]] by a 2.94 GB LRAT proof — **the only machine-checkable lower bound on record for this code at any strength**, improving on the strongest quantity previously published *as a lower bound* (`d >= 11`, Chen–Jafari–Lai, arXiv:2606.12445, solver-asserted, no proof files in their repository) | the **value `d = 18` is Bravyi et al.'s**, asserted exactly by ILP without a checkable artifact. Our `[14,18]` is **not** new information about the value | `bb288/lower_X_K13_sym.json` (proof regenerable), `witness_X.json`, `duality.json` | as above |
| 21 | An explicit ZX-duality permutation for each BB code, packaged as a ~15 ms checkable certificate | **the fact `d_X = d_Z` for BB codes is Bravyi et al.'s supplemental lemma.** Only the explicit permutation certificate is ours | `<code>/duality.json` + `duality_perm.txt` | `python3 qec-scripts/check_duality.py qec-certificates/<code>/duality.json` |
| 22 | Independent audit: 47/47 certificate checks passed, 0 failed; 5,459,315,046 bytes (5.08 GiB) of LRAT replayed **in pure Python**, 79 MB peak RSS; all five BB parity-check matrices rebuilt **byte-identically** from the published construction; 182/182 manifest SHA-256 entries matching; 11/11 negative controls rejected; six codes cross-checked by brute force | **ours** (a separate agent instance with no access to the pipeline and no shared code) | `INDEPENDENT-VERIFICATION.md` | re-run the checkers; the report lists every command |

### 5b. Explicitly **not** claimed

- **Any distance value.** Every value certified here was already published. The BB codes and their distances are Bravyi, Cross, Gambetta, Maslov, Rall and Yoder's (Nature **627** (2024) 778 / arXiv:2308.07915), computed there by the MIP method of Landahl, Anderson and Rice (arXiv:1108.5738).
- **Priority for machine-checked quantum distance proofs.** That is LEAN-QEC's (arXiv:2605.16523), and their repository reports the gross code completed at commit `c73827d`, 2026-07-10 — before this write-up was finished.
- **That `d < 18` for [[288,12,18]].** Our `d_X >= 14` is a lower bound four short of the standing literature value, and the shortfall is a limitation of our encoding, not evidence against `d = 18`.
- **The `d_X = d_Z` duality fact for BB codes.** Bravyi et al.'s lemma.
- **`k`.** The code dimensions are recomputed, not certified (though side condition (c) pins the logical dimension implicitly, and the audit recomputed every `k` independently).
- **A defect-free corpus.** Four defects are reported verbatim in §8 of the paper — one of them, D2, fixed in this release; the other three, including a latent soundness hole in an unexercised checker branch, are not.

### 5c. Known gaps in this snapshot

1. `bb288/duality.json` was generated **after** the audit closed. It passes `check_duality.py` and its permutation was independently re-verified, but it is not among the audit's 47 checks and not among `manifest.json`'s 182 hashes.
2. `manifest.json` covers the full 182-file audited corpus, including four proofs (79 MB–646 MB compressed) that are too large for git and are **not** in this repository. `qec-certificates/REGENERATE.md` gives the exact CaDiCaL invocation, expected byte count, and expected SHA-256 for each.
3. The shipped `check_lower.py` is 481 lines; the auditor read a 419-line version. The difference is an optional totalizer cardinality encoding that **no certificate in this release selects**. See Remark 4.1 of the paper.
4. `run_all.sh` still expects a `tools-drat-trim/lrat-check` binary that is not vendored (defect D3). The pure-Python path needs nothing but CPython and is the one every number in the paper reports.

---

## 6. Parts C and D — release-boundary facts (added 2026-08-06)

Stated plainly, because an auditor of timestamps will notice it and the record should say it first:

- **Both Part C and Part D were committed together** in commit `89e164c` (2026-08-05), the commit tagged **v0.3.0**, whose commit message names only Part C. The entire Part D corpus (`qec1435-paper/`, the 43 pinned certificates, `qec1435-scripts/`, `SWEEP-RECORD-1435-2026-08-05.md`) is therefore already present in the v0.3.0 tag tree.
- Commit `fc8b4fc`, tagged **v0.4.0**, changed exactly one file: `.zenodo.json` (the deposit metadata for the Part D Zenodo record). The v0.3.0 and v0.4.0 tag trees are snapshots of the same night's tree and differ only in that file; the v0.4.0 commit message ("Part D … paper, 43 certificates, scripts") describes content that entered the history one commit earlier.
- Consequently the Zenodo archive of v0.3.0 (doi:10.5281/zenodo.21816010, the Part C record) also contains the Part D files, and **the external timestamp for Part D's claims begins at the v0.3.0 push/deposit of 2026-08-05**, not at v0.4.0. Nothing about either result changes; this section exists so that the mislabeled commit messages (which cannot be rewritten without rewriting public history) cannot be read as an attempt to blur dating.
