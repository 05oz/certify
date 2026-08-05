# Certify: machine-verified structure of the Alpöge Keller map

**Degree minimality in the equivariant class of the Alpöge Keller map, and the moment-map structure of its cotangent lift — certificates, verification scripts, and preprint.**

Author: Daniel Kirtchakov (Independent researcher). Repository: https://github.com/05oz/certify. Date of this snapshot: 2026-08-04. All computations carried out with Claude (Fable 5), SymPy 1.14, msolve 0.10.1. Everything here is in characteristic zero.

This is the open half of the Certify project: schema, checker, certificates, verification scripts, and the preprint. Every mathematical claim in the preprint maps to a script whose `assert` statements pass, or to an msolve Gröbner-basis certificate stored verbatim in `certificates/`. Nothing is conjectural unless labeled so.

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
venv/bin/python scripts/min_verify.py II               # SymPy GB reproduction, two Branch-II leaves, mod 32003

# msolve (https://github.com/algebraic-solving/msolve), v0.10.1 used here:
brew install msolve          # macOS; or build from source
for f in certificates/ms_I-*_c0.ms certificates/ms_II-*_c0.ms;         do msolve -g 2 -f "$f" -o "${f%.ms}.out"; done   # 8 unit ideals over Q
for f in certificates/ms_I-*_c32003.ms certificates/ms_II-*_c32003.ms; do msolve -g 2 -f "$f" -o "${f%.ms}.out"; done   # mod-32003 reproductions
```

Every Python script must end with its `PASS` lines and no assertion failures. Every `ms_I-*`/`ms_II-*` msolve run must output the reduced basis `[1]`, matching the stored `out_*_q.txt` (char 0) and `out_*_p.txt` (mod 32003). Do not loop `ms_D7control_c32003.ms` in: that reduced-basis run does not terminate in reasonable time (see `certificates/D7CONTROL-NEGATIVE-RESULT.md`); the asserted positive control is `scripts/min_verify.py d7control`.

## Layout

```
README.md            this file
PROVENANCE.md        timeline, what is new, how to verify, what is not claimed
PUBLISH-CHECKLIST.md publication steps (all performed by the author, not by any assistant)
CITATION.cff         citation metadata
.zenodo.json         Zenodo deposit metadata
LICENSE-CODE         Apache-2.0 (code and machine-readable certificates)
LICENSE-DOCS         CC-BY-4.0 (prose and paper)
paper/               preprint (LaTeX + PDF + readable Markdown mirror), draft of 2026-08-04
certificates/        17 msolve input files (ms_*.ms) + stored outputs (out_*.txt) + D7 control record
scripts/             the verification scripts (incl. min_verify.py) + expanded Weyl operators
schema/              certificate-schema (pending; see schema/PENDING.md)
checker/             independent certificate checker (pending; see checker/PENDING.md)
```

The reduction library and the system generators are intentionally not part of this repository; the published claims are the certificates themselves plus the verification scripts, which are self-contained.

## Licensing

Dual license by content type:

- **Code and machine-readable certificate files** — everything under `scripts/`, `certificates/`, `schema/`, `checker/` — are licensed under the **Apache License 2.0** ([LICENSE-CODE](LICENSE-CODE)).
- **Documentation and the paper** — `paper/`, `README.md`, `PROVENANCE.md`, and all other prose — are licensed under **CC BY 4.0** ([LICENSE-DOCS](LICENSE-DOCS)).

## Citing

See [CITATION.cff](CITATION.cff). A DOI will be minted on the first Zenodo deposit; until then, external timestamps for this repository's claims begin at the first public push — not at local file dates (see PROVENANCE.md §3).

## Contact

Daniel Kirtchakov — daniel@halfounce.io
