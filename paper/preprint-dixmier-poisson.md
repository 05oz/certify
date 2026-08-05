# Degree minimality in the equivariant class of the Alpöge Keller map, and the moment-map structure of its cotangent lift

**Daniel Kirtchakov** (Independent researcher, daniel@halfounce.io) — *draft of August 4, 2026 — DRAFT ONLY, not for circulation.*
Readable mirror of `preprint-dixmier-poisson.tex`. All computations carried out with Claude (Fable 5), SymPy 1.14, msolve 0.10.1. Every displayed identity is asserted by a script listed in §7; nothing is conjectural unless labeled so. Coordinate with W. G. P. Mayner before any public posting (see §1.4).

> **Re-scoped 2026-08-04** after a first-hand prior-art check. Sources read in full and verified that day: `github.com/wmayner/dixmier-counterexample` (REPORT.md, dixmier-note.tex; both commits 2026-07-21); arXiv:2607.20210 (Shaska), LaTeX source of v1 (2026-07-22) and v2 (2026-07-25); `ulam.ai/research/jacobian.pdf` (PDF CreationDate 2026-07-20 05:54 EDT); `aaronlou.com/jacobian_counterexample_derivation.pdf` (2026-07-20 04:32); MathOverflow 513387 and 513392 (both 2026-07-20, both with zero answers). MathOverflow 513390 could not be retrieved (404, absent from the API) and is **not** cited. Several results previously claimed here as new are anticipated by those sources; §1.4 gives the claim-by-claim table.

**Abstract.** Let F : ℂ³ → ℂ³ be the degree-7 Keller map announced by L. Alpöge on July 19, 2026, which refutes the Jacobian conjecture in dimension three. Our two new results concern its ℂ*-equivariant class, in which F = (A/x², B/x, xC) with A, B, C polynomials in the invariants u = 1+xy, s = x²z.

First, a **degree-minimality theorem**: in that class no Keller map of degree ≤ 6 exists at all in the sector where C genuinely involves s — the sector containing Alpöge's map — and every Keller map of degree ≤ 6 elsewhere in the class is a polynomial automorphism of ℂ³. Degree 7 is therefore minimal in the class. The emptiness statements rest on eight Gröbner-basis unit-ideal certificates computed over ℚ (msolve, multi-modular F4) and reproduced mod 32003, together with a **no-go lemma** valid for every weight k ≥ 1 and every degree: if C is s-free and A, B are at most affine in s, the map is an automorphism.

Second, a **moment-map identity**. The ℂ*-action lifts Hamiltonianly to T*ℂ³, and the cotangent lift Φ(q,p) = (F(q), (JF(q))⁻ᵀp) preserves the moment map exactly: ν∘Φ = μ with μ = xp₁ − yp₂ − 2zp₃.

The map Φ itself is **not ours**: it was written down, and its exact preservation of the symplectic form, det JΦ = 1, and non-injectivity verified, by W. G. P. Mayner on July 21, 2026. We identify it as an explicit witness for the Poisson conjecture PC₃ via the Adjamagbo–van den Essen chain, record its component degrees (7,6,4,9,10,12) and an explicit rational triple collision in ℂ⁶, and prove the quantization identity gr Ψ_F = Φ* for Mayner's Weyl-algebra endomorphism Ψ_F. The remaining structural material — the master equation, the base-point (anchor) identity, the S₃ cover, and the exact image theorem — was obtained independently here but is anticipated by Shaska, by the anonymous ulam.ai note, and by Mayner, all in July 2026; it is retained for self-containedness and priority is credited to those sources in §1.4. Everything is in characteristic zero; JC₂, DC₁, DC₂ remain open.

---

## 1. Introduction

### 1.1 The three conjectures

We work over ℂ throughout; every statement in this note is in characteristic zero. A polynomial map F : ℂⁿ → ℂⁿ is a **Keller map** if det JF is a nonzero constant [Kel39].

- **JC_n** (Jacobian conjecture): every Keller map ℂⁿ → ℂⁿ is a polynomial automorphism.
- **DC_n** (Dixmier conjecture [Dix68]): every unital ℂ-algebra endomorphism of the n-th Weyl algebra W_n is an automorphism.
- **PC_n** (Poisson conjecture): every unital endomorphism of the polynomial Poisson algebra P_n = (ℂ[q₁..q_n, p₁..p_n], { , }) preserving the bracket is an automorphism.

These are linked by the chain

    JC_{2n} ⟹ PC_n ⟹ DC_n ⟹ JC_n

established by Tsuchimoto [Tsu05], Belov-Kanel–Kontsevich [BKK07], Bavula [Bav05], and Adjamagbo–van den Essen [AvdE07] (who inserted the Poisson link); for DC_n ⟹ JC_n see [vdE00] and [BKK07, p. 2].

On **July 19, 2026**, Levent Alpöge announced an explicit counterexample to JC₃ [Alp26] — the map F of (1.2) below — refuting JC_n for all n ≥ 3. (The problem was suggested by Akhil Mathew; per the announcement, the search that produced the map was run with Claude Fable 5. We do not describe the discovery process beyond the announcement; see Tao's expository post [Tao26] and the Secret Blogging Seminar discussion [Spe26].) Read contrapositively, the chain shows that the failure of JC₃ formally entails the failure of DC₃ and hence of PC₃. Both consequences are already on the public record: Mayner [May26] gave the explicit Weyl-algebra witness for ¬DC₃ on July 20–21, 2026, and the Wikipedia article on the Jacobian conjecture states flatly that "the Dixmier and Poisson conjectures are false in every dimension n > 2", citing [AvdE07]. Nothing in §§3–4 should be read as a priority claim on either statement; what those sections contribute is an explicit PC₃-witness, its degrees and momenta, and the quantization identity relating it to Ψ_F. **The new results of this note are the degree-minimality theorem (Theorem E) and the moment-map identity (Theorem C(i))**; see §1.4 for a claim-by-claim priority table.

### 1.2 The map

    F₁ = (1+xy)³ z + y²(1+xy)(4+3xy)      (degree 7)
    F₂ = y + 3x(1+xy)² z + 3xy²(4+3xy)    (degree 6)
    F₃ = 2x − 3x²y − x³z                  (degree 4)

with det JF ≡ −2. It is non-injective in a way anyone can check by hand in a minute:

    F(1, −3/2, 13/2) = F(−1, 3/2, 13/2) = F(0, 0, −1/4) = (−1/4, 0, 0),

a triple collision at rational points.

### 1.3 Statement of results

*What is new here is Theorem E and Theorem C(i)*, together with the no-go Lemma 6.2 on which Theorem E rests. Theorem E says that in the ℂ*-equivariant class of Alpöge's map, degree 7 is minimal: below it the relevant sector is *empty*, and what survives elsewhere in the class is automorphisms only. Theorem C(i) says that the ℂ*-action lifts Hamiltonianly to the cotangent bundle and that the cotangent lift preserves the moment map on the nose. The remaining theorems are stated because the note is meant to be self-contained; each carries its priority attribution in its own statement, and §1.4 gives the full table. The reader interested only in the new material may go directly to §5.2 and §6.

Let N = (JF)⁻¹ = adj(JF)/(−2), a 3×3 matrix with **polynomial** entries (total degree ≤ 11, at most 14 monomials each — 77 in total across the nine entries), and D_j = Σ_k N_kj ∂_k.

**Theorem A (Dixmier conjecture fails for n ≥ 3; *Mayner's theorem*, independently verified here).** The assignments x_i ↦ F_i, ∂_j ↦ D_j extend to a well-defined unital ℂ-algebra endomorphism Ψ_F : W₃ → W₃. It is injective, and it is not surjective: the generator x is not in its image. Consequently DC_n is false for every n ≥ 3, with explicit witness Ψ_F ⊗ id. **This is due to W. G. P. Mayner** (comment of July 20, 2026 on [Spe26]; note and report of July 21, 2026 [May26], where the non-member exhibited is y rather than x). We claim no priority whatsoever for it; §3 is an independent re-verification, retained because Theorem B and Theorem C(ii) are stated relative to Ψ_F.

**Theorem B (Mayner's cotangent lift, identified as a counterexample to the Poisson conjecture).** *The map Φ below and its three displayed properties are Mayner's* [May26, §8], who verified there that the cotangent lift Φ(q,p) = (F(q), G(q)p), G = (JF)⁻ᵀ, is a polynomial self-map of ℂ⁶ which "preserves the standard symplectic form exactly", has det JΦ = 1 identically, and is not injective; his priority section lists "the symplectic lift to ℂ⁶" among the items apparently not previously public. *What is added here* is: the identification of Φ* as an explicit witness for PC_n through the Adjamagbo–van den Essen formulation [AvdE07]; the component degrees; the explicit momenta of a rational triple collision; and, in Theorem C, the moment map and the quantization identity. Precisely: Φ : ℂ⁶ → ℂ⁶, Φ(q,p) = (F(q), (JF(q))⁻ᵀ p), is a polynomial map with component degrees (7,6,4,9,10,12) whose Jacobian M = JΦ satisfies MᵀΩM = Ω identically and det M = 1. Φ is generically 3:1; in particular the three rational points

    a₁ = ( 1, −3/2, 13/2 ; −405/16, 25/8, −13/8 )
    a₂ = (−1,  3/2, 13/2 ; −387/16, 31/8,  11/8 )
    a₃ = ( 0,  0,  −1/4  ;  9/2,    2,     1    )

satisfy Φ(a₁) = Φ(a₂) = Φ(a₃) = (−1/4, 0, 0 ; 1, 2, 3). Consequently Φ* is an injective, non-surjective Poisson endomorphism of P₃, and PC_n is false for every n ≥ 3.

**Theorem C (equivariant structure; *part (i) is new*).**
(i) The ℂ*-action t·(x,y,z) = (tx, t⁻¹y, t⁻²z) lifts to a Hamiltonian action on T*ℂ³ ≅ ℂ⁶ with moment map μ = xp₁ − yp₂ − 2zp₃; the target carries the action of weights (−2,−1,1) with moment map ν = −2Q₁P₁ − Q₂P₂ + Q₃P₃. Φ is equivariant and preserves the moment map exactly: ν∘Φ = μ.
(ii) Ψ_F preserves the order filtration of W₃, and under gr W₃ ≅ 𝒪(T*ℂ³) one has **gr Ψ_F = Φ***. In this precise sense Ψ_F is the canonical quantization of Φ, and quantization does not restore invertibility. (The symbol computation behind this — that the σ₁(D_j) = Σ_k N_kj ξ_k form a ℂ[x,y,z]-basis of the degree-one part of gr W₃ — is step 2 of Mayner's self-contained proof [May26, §8]; the identification of the resulting graded endomorphism with Φ* is our packaging.)

The ℂ*-equivariance of F itself is not new: it is recorded by Speyer [Spe26], in [MO513387], by Mayner [May26, §6], and is the organizing hypothesis of Shaska [Sha26]. Part (i) — the Hamiltonian lift and the exact identity ν∘Φ = μ — is, to our knowledge, not in any of them; we found no occurrence of "moment map" anywhere in the July–August 2026 literature on this example.

**Theorem D (exact image; *anticipated*, see the attribution below).** The image of F is ℂ³ minus the punctured rational curve

    Γ = { (4/(27t²), 4/(3t), t) : t ∈ ℂ* },

and consequently im Φ = ℂ⁶ ∖ (Γ × ℂ³). Generic fibers of F have three points; the count drops (generically) to two over the pullback of {Δ₂ = 0} and to one over the pullback of {Δ₁ = 0} — two sheets escaping to infinity — and to zero exactly on Γ, where all three sheets have escaped. (Δ₁, Δ₂ are the explicit discriminant polynomials of §5.3.)

*Priority.* The fiber counts 3/1/0 and the identification of the missed locus with the curve Γ were obtained first in the anonymous note [Ula26, Thm. 4.2] (PDF timestamp July 20, 2026), and independently in [May26, §4.3] and in [Sha26, Prop. 5.1], where the same curve appears in the same normalization, {(4/27·t⁻², 4/3·t⁻¹, t)}. Our proof is independent and is retained only for self-containedness and because the transfer to im Φ is used later.

**Theorem E (degree minimality in the equivariant class; *new*).** In the equivariant class of weights (1,−1,−2) — maps F = (A/x², B/x, xC) with A,B,C ∈ ℂ[u,s], u = 1+xy, s = x²z, subject to the polynomial-lift conditions — every Keller map of degree ≤ 6 is a polynomial automorphism of ℂ³. Stronger: in the entire sector where C genuinely involves s (the sector containing Alpöge's map), no Keller map of degree ≤ 6 exists at all, automorphisms included. Hence degree 7 is minimal in this class. Unconditional minimality of degree 7 among all counterexamples in ℂ³ remains open.

Theorem E is proved in §6; it rests on the no-go Lemma 6.2 (valid for all weights k ≥ 1 and all degrees, and also new) together with eight Gröbner-basis unit-ideal certificates computed over ℚ (msolve, multi-modular F4) and reproduced mod 32003. We record how it sits against the nearest published statements.

- Shaska [Sha26, Thm. 10.10] proves that no graded Keller counterexample in dimension three has *both* A and B of degree one in the invariants, for any signature (r,s) — a strictly weaker emptiness statement, and one he explicitly leaves incomplete: "the smallest cases left open in dimension three are (r,s) = (1,1) with **d** = (2,1,d₃) and **d** = (1,2,d₃); whether 𝒦(3,(1,−1,−1)) is empty we do not know." Theorem E clears an entire degree band, in his hyperbolic signature (r,s) = (1,2), with no degree-one hypothesis on A or B.
- Mayner [May26, §7] proves a *quadratic no-go* inside a different ansatz — the z-linear line congruences with a quadratic direction field — concluding that "within the parallel-congruence construction, degree 3 is the minimum degree of the covering". That is a statement about the covering degree in his structural class; Theorem E is a statement about the total degree in the ℂ*-equivariant class. Neither contains the other.
- Jelonek [Jel26] shows that if X(n,d) is irreducible then for n ≥ 3, d ≥ 6 a *generic* element is a counterexample. That is the opposite direction: an abundance statement above degree 6, not an emptiness statement below it, and it is conditional on irreducibility.
- Unconditionally, invertibility of Keller maps is known only through degree 2, in every dimension, by Wang's theorem [Wan80]; and ulam.ai [Ula26, Cor. 5.3] exhibits nonproper Keller maps of every generic degree d ≥ 3 (their total degrees grow, and none of their degree-≤6 members is equivariant of our type). Theorem E is therefore the first emptiness result we know of that rules out an explicit degree band inside a class known to contain a counterexample.

Every displayed identity is asserted by a script listed in §7.

### 1.4 Provenance and credit

*This subsection was rewritten on August 4, 2026 after a first-hand check of the prior art, in which several results stated here turned out to have earlier public sources. What follows is the corrected record.*

**The map.** The counterexample F is Alpöge's, announced July 19, 2026; the problem was posed by Akhil Mathew, and the search was run with Claude Fable 5, per the announcement. Everything in this note is downstream of that example.

**The Weyl endomorphism _and_ the symplectic lift.** Both are W. G. P. Mayner's, from the same day and the same source. The explicit operators D_j and the statement that Ψ_F refutes DC₃ were made public in a comment of July 20, 2026 on the SBS thread [Spe26] and in a six-page informal note of July 21, 2026 (prepared with Claude Fable 5); the accompanying report, in the same repository and the same two commits of July 21, 2026, contains in §8 the cotangent lift Φ(q,p) = (F(q), G(q)p) together with the statement — machine-verified there — that it preserves the standard symplectic form exactly, that det JΦ = 1, and that it is not injective; his verified-facts table lists it as item 24, and his priority section §12 lists "the symplectic lift to ℂ⁶" as item 3 among the results apparently not previously public [May26]. Mayner also records the correct caution that this does *not* bear on the Belov-Kanel–Kontsevich automorphism conjecture, a caution we repeat in §1.5. **An earlier draft of the present note credited Mayner for the Weyl endomorphism only; that was an error of attribution, and it is corrected here.** Mayner's note additionally goes further than our §3: it computes the exact image ⊕_α ℂ[F]D^α, exhibits non-members, tabulates the codimension of the image in filtration degrees d ≤ 7, and observes that the cokernel is not finitely generated. We claim no priority for either Ψ_F or Φ.

**Independently obtained, subsequently found to be anticipated.** The material of §§5.1, 5.3, 5.4 and Lemma 6.1 was obtained here independently, before we became aware of the sources below; it is **not** new, and we retain it only for self-containedness. Priority belongs to those sources, as follows. All dates are 2026 and were checked against the sources themselves (arXiv submission records, PDF timestamps, Git commit timestamps, StackExchange creation timestamps) on August 4, 2026.

| Item (as stated here) | Earliest public source we could verify | Date |
|---|---|---|
| Master equation (Prop. 5.1) | Shaska [Sha26, Thm. 8.3] — identical trilinear bracket identity Λ{B,A} + sA{B,Λ} + rB{Λ,A} = κ, with Keller ⟺ constant; his §9.2 is titled "The master equation". Only in v2 — v1 has the divisorial form Jac_{u,v}(P,Q) = κΛ² as Thm. 6.1. | Jul 25 |
| Parked square: det JG = λC^k, order-two vanishing on the contracted line | Shaska [Sha26, Thm. 7.1] (= Thm. 6.1 of v1, Jul 22) | Jul 22 |
| Anchor lemma (Lemma 6.1) | Shaska [Sha26, Lem. 8.5]: evaluating the master equation at the base point gives Λ(O)·{B,A}(O) = κ, which is our λ = C₀(1)B₀′(1)A₁(1) after translating u ↦ u−1. | Jul 25 |
| S₃ monodromy, non-Galois, discriminant not a square | [MO513387] (explicit cubic model, discriminant, S₃, trivial deck group, and the Campbell/Razar/Wright "Galois case" theorem quoted for exactly the reason we quote it); Lou [Lou26]; Mayner [May26, §4.4]; Shaska [Sha26, Thm. 4.4(2)] | Jul 20 |
| Trace identity (fiber cubic has no subleading term) | Mayner [May26, §4.2], in the coordinate x ("the x-coordinates of the preimages sum to zero"); Shaska [Sha26, Rem. 5.4], in the coordinate s (the roots sum to 2 = κ). Our version is the same phenomenon in the invariant coordinate u. | Jul 21 |
| Exact image (Theorem D) | ulam.ai [Ula26, Thm. 4.2]; Mayner [May26, §4.3]; Shaska [Sha26, Prop. 5.1] | Jul 20 |

**What is new here.** Two things, plus one reframing.

(a) **Theorem E**, degree minimality in the equivariant class, with its eight unit-ideal certificates and the degree-7 positive control. We have found nothing comparable; the nearest statements are compared in §1.3.

(b) **Theorem C(i)**, the Hamiltonian lift and the exact moment-map identity ν∘Φ = μ; and **Lemma 6.2**, the no-go lemma for all weights k ≥ 1 and all degrees.

(c) A **reframing**: Mayner's Φ is identified as an explicit PC_n-witness through the Adjamagbo–van den Essen formulation [AvdE07], and tied to Ψ_F by gr Ψ_F = Φ* (Theorem C(ii)). The object is not new and the conclusion ¬PC_n is not new — it follows formally from ¬DC₃ and is already asserted in secondary sources. What is added is that the witness is written down, its degrees and momenta computed, and its non-invertibility checked in two lines from the triple collision with no filtration or reduction argument.

Minimality certificates for the other weights k = 1 and k = 3 are in preparation and are **not** claimed here.

**Limits of this survey.** The table above rests on a targeted search of the July–August 2026 record: the arXiv listings for math.AG and math.RA in that window, the Speyer and Tao threads, the two MathOverflow questions cited, the ulam.ai note, Lou's derivation, and Mayner's repository. A negative cannot be proved this way. In particular we were unable to retrieve MathOverflow question 513390, referenced in [May26, §12]; it returns a 404 and does not appear in the StackExchange API, so we do not cite it and record its content as unverified.

### 1.5 What is not claimed

JC₂ (planar), DC₁, and DC₂ remain open; for DC₁ there is a claimed proof by Zheglov [Zhe24] currently under review, and see Bavula–Levandovskyy [BL20] for prior partial results. The Belov-Kanel–Kontsevich conjecture Aut(W_n) ≅ Aut(P_n) [BKK05] is **not** refuted by anything here: our maps are proper endomorphisms, not automorphisms, so they do not belong to the groups in question. This caution is Mayner's, stated in the same place as the lift itself ([May26, §8]: "an earlier draft called this construction 'Kontsevich-relevant', which overstates the connection"), and we repeat it because it is easy to get wrong. The pair (Φ, Ψ_F) is, however, a sharp stress test for the proposed lifting machinery relating polynomial symplectomorphisms to Weyl-algebra automorphisms [KBEY18], whose status we do not assess here: any such machinery must be compatible with a non-invertible symplectic endomorphism whose canonical quantization is a non-invertible Weyl endomorphism. All statements are in characteristic zero.

## 2. Certified facts about F and its cotangent lift

**Proposition 2.1** (verified in `core_verify.py`, `weyl_verify.py`).
(i) det JF = −2 identically: F is a Keller map and an everywhere-local biholomorphism.
(ii) The triple collision above holds; the three source points are distinct points of ℚ³. A further rational fiber point on the generic side: F(−1/4, −4, 48) = (608, −232, 1).
(iii) N := (JF)⁻¹ = adj(JF)/(−2) has polynomial entries with rational coefficients, of total degree ≤ 11. (All nine expanded entries: `weyl_endomorphism.txt`.)

Two representative entries:

    N₁₁ = 3x⁶yz + 9x⁵y² + 3x⁵z + 3x⁴y − 4x³
    N₂₁ = 3x⁴yz + 9x³y² + 3x³z + 3x²y − 3x

**Definition 2.2** (Mayner [May26, §8])**.** The cotangent lift of F is Φ(q,p) = (F(q), (JF(q))⁻ᵀ p), a polynomial map ℂ⁶ → ℂ⁶ by (iii). This map, and the facts recorded in Prop. 2.3 that it preserves the symplectic form exactly, has det JΦ = 1, and is non-injective, are due to Mayner; our verification is independent. Ω denotes the standard symplectic matrix in coordinates (x,y,z,p₁,p₂,p₃).

**Proposition 2.3** (Mayner [May26, §8]; component degrees added here; verified in `dixmier_symplectic_verify.py`). M := JΦ satisfies MᵀΩM = Ω identically, and det M = 1 (automatic for symplectic matrices; verified independently). Component degrees: (7,6,4,9,10,12). In particular Φ has everywhere-invertible differential, hence open image, hence is dominant.

A fiber of Φ over (Q,P) is {(q, JF(q)ᵀP) : F(q) = Q}, so fibers of Φ biject canonically with fibers of F: all fiber statements transfer verbatim. The points a₁, a₂, a₃ of Theorem B are the collision fiber decorated with momenta p = JF(q_i)ᵀ(1,2,3).

## 3. The Weyl endomorphism and the Dixmier conjecture

W₃ = ℂ⟨x₁,x₂,x₃,∂₁,∂₂,∂₃⟩ with [∂_i, x_j] = δ_ij. Order filtration W₃^(m) = span{x^β∂^α : |α| ≤ m}; gr W₃ ≅ ℂ[x,y,z,ξ₁,ξ₂,ξ₃] = 𝒪(T*ℂ³) via principal symbols, with the standard Poisson bracket. Identify (ξ₁,ξ₂,ξ₃) with (p₁,p₂,p₃).

**Proposition 3.1 (CCR; machine-verified).** With D_j = Σ_k N_kj ∂_k:
(A) [D_j, F_i] = δ_ij for all i,j — equivalently JF·N = I (nine identities);
(B) [D_i, D_j] = 0 for all i,j — nine coefficient polynomials vanish identically.
Hence x_i ↦ F_i, ∂_j ↦ D_j extends to a well-defined unital endomorphism Ψ_F : W₃ → W₃. (Verified by `weyl_verify.py`; re-checked in `dixmier_symplectic_verify.py`.)

(A) repackages N = (JF)⁻¹; the substantive content is (B), the pairwise commutativity of the vector fields D_j — the flatness of the "inverse coordinate frame" of the non-invertible map F.

**Lemma 3.2.** Ψ_F preserves the order filtration, and gr Ψ_F = Φ*.
*Proof.* Ψ_F(x^β ∂^α) = F^β D^α has order ≤ |α|, so the filtration is preserved and the graded endomorphism is defined. On generators: gr Ψ_F(x_i) = F_i and gr Ψ_F(ξ_j) = σ₁(D_j) = Σ_k N_kj ξ_k. On the other side, with B = (JF)⁻ᵀ = Nᵀ: Φ*(ξ_j) = (Bp)_j = Σ_k N_kj ξ_k and Φ*(x_i) = F_i. The maps agree on generators. ∎

**Lemma 3.3 (strictness).** ord Ψ_F(S) = ord S for every nonzero S. In particular every preimage of an order-zero operator has order zero.
*Proof.* Φ is dominant (Prop. 2.3), so Φ* is injective; if σ_m(S) ≠ 0 then the class of Ψ_F(S) in gr_m is Φ*σ_m(S) ≠ 0. ∎

**Proof of Theorem A.** Well-definedness is Prop. 3.1. Injectivity: W₃ is simple and Ψ_F(1) = 1. Non-surjectivity: if x = Ψ_F(S), then ord S = 0 by Lemma 3.3, so S = g(x,y,z) and x = g(F₁,F₂,F₃); evaluating at the first two collision points (same F-image, x-coordinates 1 and −1) gives 1 = −1. For n > 3 take Ψ_F ⊗ id on W_n = W₃ ⊗ W_{n−3}; the same argument goes through verbatim. ∎

**Remark 3.4 (Mayner's finer results).** Much more is true, and was established first in [May26]: im Ψ_F = ⊕_α ℂ[F]D^α exactly; none of x, y, z, ∂_i lies in the image; codimension table for d ≤ 7; the cokernel is not finitely generated. The restriction of Ψ_F to the order-zero subalgebra ℂ[x,y,z] is precisely the pullback F* — the classical non-surjective shadow. The mechanism "Ψ_F automorphism ⟹ F invertible" is classical; see [vdE00] and [BKK07, p. 2]. Lemmas 3.2–3.3 are our packaging of that argument for this specific F.

## 4. The symplectic counterexample and the Poisson conjecture

A polynomial map Φ of ℂ⁶ satisfies {g∘Φ, h∘Φ} = {g,h}∘Φ for all g,h iff its Jacobian satisfies MᵀΩM = Ω pointwise; then Φ* is a unital Poisson endomorphism of P₃. PC_n [AvdE07] asserts every such endomorphism of P_n is an automorphism — equivalently, every polynomial map of ℂ²ⁿ preserving the standard symplectic form is a polynomial automorphism.

**Proof of Theorem B.** MᵀΩM = Ω, det M = 1, the degrees, and the collision Φ(a₁) = Φ(a₂) = Φ(a₃) are exact symbolic facts (Prop. 2.3; momenta of the a_i are JF(q_i)ᵀ(1,2,3)). Hence Φ* is a Poisson endomorphism; injective since Φ is dominant. Not surjective: if x = g∘Φ, evaluation at a₁, a₂ (equal images, x-coordinates 1 and −1) gives 1 = −1. So PC₃ fails. Φ is generically 3:1 because its fibers biject with those of F (§2) and F is generically 3:1 (Prop. 5.2). For n > 3 take Φ × id with the extra coordinates in symplectic pairs. ∎

**Remark 4.1 (relation to the formal implication, stated exactly).** Given ¬DC₃ (Theorem A, Mayner's), ¬PC₃ follows abstractly from PC₃ ⟹ DC₃ [AvdE07], and is already asserted in secondary sources. The map Φ is Mayner's [May26, §8], as are the three properties verified in Prop. 2.3; his priority section lists the symplectic lift explicitly. What is added by Theorem B is the identification of Φ* with the Poisson-endomorphism side of [AvdE07] — i.e. the label PC_n — together with the component degrees, the explicit momenta of the collision, and a non-invertibility proof that is two lines from the triple collision, with no filtration and no reduction argument. Mayner does not use the words "Poisson conjecture" anywhere, and we have found no source that does in this connection; but the reader should treat Theorem B as a labelling and packaging contribution, not as the discovery of a new object.

**Remark 4.2 (quantization does not restore invertibility).** Theorem C(ii) (= Lemma 3.2) realizes the hoped-for diagram exactly: Ψ_F is a filtered quantization of Φ with gr Ψ_F = Φ*, and both are proper endomorphisms. Whatever mechanism destroys injectivity of F survives passage to the Weyl algebra. This bears on the lifting program of [KBEY18]: a correct lifting theory must map the non-invertible symplectic endomorphism Φ to a non-invertible object, as the canonical quantization does. The BKK automorphism conjecture [BKK05] concerns groups of automorphisms and is untouched (§1.5).

## 5. Equivariant structure: reduction, moment map, cover, image

### 5.1 The ℂ*-reduction and the master equation

Weights (1,−1,−2) on (x,y,z); invariants u = 1+xy, s = x²z. The components of F are semi-invariant of weights (−2,−1,1):

    x²F₁ = A(u,s),   xF₂ = B(u,s),   F₃ = x·C(u,s)

with

    A = u³s + u(u−1)²(3u+1),   B = 3u²s + 9u³ − 15u² + 4u + 2,   C = 5 − 3u − s.

The invariant target combinations p = 1 + F₂F₃, q = F₁F₃² define the downstairs plane map **G(u,s) = (1+BC, AC²)**.

**Proposition 5.1 (master equation; *Shaska [Sha26, Thm. 8.3]*, obtained independently and machine-verified here).** For k ≥ 1, s = x^k z, arbitrary A,B,C ∈ ℂ[u,s], J(f,g) = f_u g_s − f_s g_u, and G = (1+BC, AC^k):

    det JG = C^k · 𝓑_k,   𝓑_k := C·J(B,A) + k·A·J(B,C) + B·J(C,A),

identically. If F = (A/x^k, B/x, xC) is a polynomial map, then det JF = −𝓑_k identically. Hence **F is Keller ⟺ 𝓑_k is a nonzero constant.** For Alpöge's map (k = 2): det JG = 2C², 𝓑₂ = 2, det JF = −2.

The identity isolates the design pattern: JG "parks" a full square C^k (for k = 2, on the line ℓ : 3u+s = 5), and the fiber scaling x ↦ xC cancels it exactly. This divisorial form of the Keller condition — det JG = κC^k, i.e. order-k vanishing on the contracted locus with constant leading coefficient — is [Sha26, Thm. 7.1] (Thm. 6.1 of the July 22 version), and the expanded trilinear identity itself is [Sha26, Thm. 8.3]; his Remark 8.4 identifies the exponent k = Σ_{i≥2} r_i − 1 in general. We obtained the identity independently and give the machine verification, but the result is his. Two further verified facts:

- G **contracts the critical line** ℓ = {C = 0} to the point (1,0); restricted to ℓ, (A,B)|_ℓ = (u²+u, 4u+2) and the one-variable Wronskian b·a′ − 2a·b′ = 2 — the same constant as the Jacobian. The construction is tight along its critical line.
- The triple collision sits exactly over the contraction point (1,0): the three fiber points have u = 1 (the x = 0 sheet) and u = −1/2, s = 13/2 (twice, on {C = 0}).

Heuristic for "why not ℂ²": the mechanism needs a fiber direction to absorb the parked square; in the plane there is none (and Moh [Moh83] proved the planar conjecture through degree 100).

### 5.2 The Hamiltonian lift and the moment map (new)

**Proof of Theorem C(i).** Equivariance of F is the collapse identity: F(t·q) = S_t F(q) with S_t = diag(t⁻²,t⁻¹,t). Differentiating, JF(t·q)T_t = S_t JF(q) with T_t = diag(t,t⁻¹,t⁻²), whence (JF(t·q))⁻ᵀ = S_t⁻¹(JF(q))⁻ᵀT_t. Since the cotangent lift acts on momenta by T_t⁻¹ upstairs and S_t⁻¹ on target momenta, Φ intertwines the lifted actions. These are Hamiltonian with quadratic moment maps μ = xp₁ − yp₂ − 2zp₃ and ν = −2Q₁P₁ − Q₂P₂ + Q₃P₃, and the exact identity **ν∘Φ = μ** is verified in `dixmier_symplectic_verify.py`. ∎

**Remark (the parked square on the symplectic quotient).** Informally: Φ descends to the symplectic quotients of the μ- and ν-level sets, where its reduced Jacobian degenerates along (the image of) the critical line {C = 0} — the parked square lives on the quotient — while the group direction, the fiber coordinate x, carries the compensating factor keeping det M ≡ 1 upstairs. We use this only as an organizing picture; the verified content is the intertwining identity and the master equation.

### 5.3 Arithmetic of the 3:1 cover

**Proposition 5.2** (verified in `cover_verify.py`; *the conclusions of (i) and (ii) are anticipated* — see the attribution note after the proposition). Eliminating s from G = (p,q), the minimal polynomial of u over ℂ(p,q) is the cubic

    Δ₁·u³ + ((p−1)² − 12q)·u − 4q = 0,
    Δ₁ = p³ − 4p² − 18pq + 5p + 27q² + 34q − 2.

Moreover:
(i) **Trace identity.** No u² term: the three preimages of a generic point satisfy (1+x₁y₁) + (1+x₂y₂) + (1+x₃y₃) = 0. On the collision fiber: 1 − 1/2 − 1/2 = 0.
(ii) **Discriminant.** disc = −4·Δ₁·Δ₂² with Δ₂ = p³ − 3p² − 18pq + 3p + 54q² + 18q − 1, and Δ₁ irreducible over ℚ — in particular squarefree of odd degree 3 in p. Hence disc is not a square in ℂ(p,q): the Galois group over ℂ(p,q) is the full **S₃**, and the cover is not Galois (see the ground-field remark below).
(iii) **3:1.** s ∈ ℚ(u,p,q) (degree-one subresultant, verified identically), so [ℂ(u,s) : ℂ(p,q)] = 3 and F is generically 3-to-1.

**Remark (attribution for Prop. 5.2).** Only the coordinate is ours. That the function-field extension has degree exactly 3 with full S₃ monodromy, that the discriminant is not a square, and that the deck group is therefore trivial, were all established on July 20, 2026 in [MO513387] (with an explicit cubic model in the weight-(−1) coordinate t = y + 1/x, discriminant −4Q with Q = 27a²c² − 18abc + 16a + b³c − b², and the Campbell/Razar/Wright Galois-case theorem invoked for precisely the reason we invoke Campbell's below), and independently by Lou [Lou26] the same day; Mayner [May26, §4.4] has the same S₃ statement with his discriminant factorization −4S²Δ, and Shaska [Sha26, Thm. 4.4(2)] states it in the s-coordinate with Δ(P,Q) = −4P³ + 4P² + 72PQ − 64Q − 108Q². The trace identity (i) is the same phenomenon as Mayner's "the x-coordinates of the preimages sum to zero" [May26, §4.2] and Shaska's "the three roots always sum to 2 = |det JF|" [Sha26, Rem. 5.4], transported to the invariant coordinate u; the three cubics are genuinely different cubics (different primitive elements of the same cubic extension), and we do not know whether the trace-free shape in u specifically is forced.

**Remark (from the ℚ-certificates to ℂ(p,q)).** The certificates behind Prop. 5.2 operate over ℚ, and irreducibility over ℚ(p,q) does not by itself preclude a factorization over ℂ(p,q); the gap closes as follows. F is an everywhere-local biholomorphism (Prop. 2.1(i)), so each of the three distinct points of the collision fiber has a neighborhood mapped biholomorphically onto a neighborhood of (−1/4, 0, 0); every nonempty Zariski-open subset of ℂ³ meets the intersection of these image neighborhoods, so some target with t ≠ 0 and (p,q) ≠ (1,0) has at least three F-preimages. Its F-fiber bijects with the G-fiber over (p,q) (§5.4), whose points all satisfy C ≠ 0, where det JG = 2C² ≠ 0; so G is a local biholomorphism at each of the ≥ 3 fiber points, and the same openness argument, now downstairs, produces a Zariski-generic point of ℂ² with at least three G-preimages. Since the generic fiber count of a dominant map between irreducible varieties of equal dimension equals the function-field degree in characteristic zero, [ℂ(u,s) : ℂ(p,q)] ≥ 3. On the other hand s ∈ ℂ(u,p,q) by (iii), so ℂ(u,s) = ℂ(p,q)(u), and u satisfies the cubic: the degree is ≤ 3. Hence the degree is exactly 3, the cubic is the minimal polynomial of u over ℂ(p,q) — in particular irreducible over ℂ(p,q), with no descent argument needed — and the monodromy group is transitive. Finally, disc = −4Δ₁Δ₂² is a square in ℂ(p,q) iff −Δ₁ is; because ℂ[p,q] is a UFD, that would force −Δ₁ to be the square of a polynomial, which is impossible: Δ₁ is squarefree (squarefreeness — gcd(Δ₁, ∂ₚΔ₁) = 1 — is insensitive to extending the ground field in characteristic zero) of odd degree 3 in p, while nonconstant polynomial squares have even degrees. So disc is not a square in ℂ(p,q), the monodromy is not contained in A₃, and, being transitive, it is all of S₃.

**Remark (Campbell's theorem makes S₃ a necessity).** By Campbell [Cam73] — proved independently, in general characteristic zero, by Razar and by Wright — a Keller map whose function-field extension is Galois is invertible. A counterexample of covering degree 3 therefore *had* to be non-Galois — monodromy S₃ rather than ℤ/3 — and (ii) confirms Alpöge's map threads exactly that needle. This observation is also not ours: it is made in [MO513387] on July 20, 2026, with the same citation. Whether the trace identity is forced by the mechanism or is extra tuning is open — worth testing on any future examples with other weights.

### 5.4 The image theorem

The statement of Theorem D is not new; see the priority note in its statement and §1.4. The proof below is our own and is included because the G-fiber correspondence it sets up is reused in Theorem E, and because the transfer im Φ = ℂ⁶ ∖ (Γ × ℂ³) needs it. Readers who prefer the published treatments should consult [Ula26, Thm. 4.2], which routes the fiber count through a binary cubic 2pS³ − qS²T + 2ST² − rT³ and an incidence variety in ℂ³ × ℙ¹, or [Sha26, Prop. 5.1], which routes it through the contracted line.

**Proof of Theorem D.** Target coordinates (X,Y,t).

*The plane t = 0 is covered.* On the sheet x = 0 the map is F(0,y,z) = (z+4y², y, 0), visibly bijective onto the plane {t = 0}.

*Targets with t ≠ 0.* A preimage with F₃ = t ≠ 0 has x ≠ 0 and C(u,s) ≠ 0, and corresponds to a point of the G-fiber over (p,q) = (1 + tY, t²X), with x = t/C recovered uniquely; conversely every G-fiber point with C ≠ 0 arises this way. If (p,q) ≠ (1,0), every G-fiber point automatically has C ≠ 0 (C = 0 forces (p,q) = (1,0)), so the F-fiber bijects with the G-fiber. The axis targets (0,0,t), t ≠ 0 — exactly the case (p,q) = (1,0) — are hit exactly once, by (t/2, 0, 0): the system A = B = 0, C ≠ 0 has the single solution (u,s) = (1,0), where C = 2 (reduced Gröbner basis over ℚ, asserted in `min_verify.py` part `axis`), whence x = t/2, y = 0, z = 0.

*The line q = 0 is covered.* On the u = 0 sheet q ≡ 0 and p = 11 − 2s takes every value; so every (p,q) with q = 0 has a G-fiber point, and roots u₀ = 0 of the cubic — which occur only when the constant term −4q vanishes — never need to be lifted.

*From cubic roots to fiber points.* Fix a target (p,q) with q ≠ 0 and let u₀ be any root of the cubic of §5.3. Viewed as polynomials in s, p − P and q − Q have degrees 2 and 3 with s-leading coefficients −3u² and u³ respectively (from BC and AC²), and the cubic is an irreducible factor of their s-resultant — indeed the resultant equals −u³ times the cubic, the extraneous factor being supported on {u = 0} (`cover_verify.py` extracts the cubic from precisely this resultant). Since q ≠ 0, the constant term −4q of the cubic is nonzero, so u₀ ≠ 0 and both s-leading coefficients −3u₀², u₀³ are nonzero; hence specializing u = u₀ commutes with taking the resultant, and the specialized resultant vanishes because the cubic does. Two univariate polynomials with nonvanishing leading coefficients and vanishing resultant have a common root: there is s₀ ∈ ℂ with (u₀, s₀) ∈ G⁻¹(p,q). So the G-fiber over any (p,q) with q ≠ 0 is nonempty whenever the cubic has a root.

*Emptiness locus of G.* By the previous two steps, the fiber can be empty only where the cubic has no root at all: only where its leading coefficient Δ₁ and its linear coefficient (p−1)² − 12q both vanish while the constant term −4q does not. Solving, the unique such point is (p,q) = (7/3, 4/27), and a Gröbner certificate over ℚ shows the ideal of the G-equations at that point is the **unit ideal**: that fiber is indeed empty (Nullstellensatz; `min_verify.py`, `cover_verify.py`).

*The missed curve.* Pulling (7/3, 4/27) back through (p,q) = (1+tY, t²X) gives, for each t ≠ 0, the unique missed target (4/(27t²), 4/(3t), t) — the curve Γ. Every other target is attained, so im F = ℂ³ ∖ Γ, and im Φ = ℂ⁶ ∖ (Γ × ℂ³).

*Fiber counts.* Generic fibers have three points. Over {Δ₂ = 0} (Δ₁ ≠ 0) two sheets merge; over {Δ₁ = 0} ∖ {(7/3, 4/27)} the cubic drops degree and exactly one preimage remains — two sheets escape to infinity; at (7/3, 4/27), i.e. over Γ, all three sheets have escaped and the fiber is empty. ∎

So F is an everywhere-local biholomorphism, generically 3:1, surjective except for one explicit punctured rational curve — over Γ the missing preimages have escaped to infinity along {Δ₁ = 0}.

**Remark 5.3 (transport to Ψ_F).** At order zero, the deficiency of Ψ_F *is* the deficiency of F*: ℂ[F] ⊊ ℂ[x,y,z], dual to F itself, whose failure of surjectivity is exactly Γ. In higher filtration degrees, Mayner's computations [May26] (exact image, codim table d ≤ 7, non-f.g. cokernel) quantify the deficiency; at the symbol level, Lemma 3.2 bounds the image by im Φ*, whose geometric deficiency is Γ × ℂ³ (Theorem D). We expect the growth of coker Ψ_F to be governed by functions along Γ and the S₃ monodromy of §5.3; a precise statement is left to future work.

## 6. Degree minimality in the equivariant class

Fix weights (1,−1,−2): F = (A/x², B/x, xC), A,B,C ∈ ℂ[u,s]. Writing A = A₀(u) + A₁(u)s + A₂(u)s² + ⋯ etc., the **lift conditions** are (u−1)² | A₀ and B₀(1) = 0, and Keller ⟺ 𝓑₂ = λ ∈ ℂ*. Alpöge's map is the member with λ = 2.

**Degree dictionary.** u^i s^j ↦ x^{i+2j} y^i z^j is injective on exponent pairs — no cancellation — so deg F ≤ 6 caps the s-expansion coefficients exactly:

| | s⁰-part | s¹-part | s²-part |
|---|---|---|---|
| A | deg ≤ 4 | deg ≤ 2 | deg ≤ 1 |
| B | deg ≤ 3 | deg ≤ 2 | constant |
| C | deg ≤ 2 | deg ≤ 1 | — |

**Normalization.** The two diagonal ℂ*-automorphisms upstairs scale (A,B,C) ↦ (νr⁻²A, νr⁻¹B, νrC), λ ↦ ν³r⁻²λ; this legitimately sets λ = 1 plus one further leading coefficient to 1 in each case.

**Lemma 6.1 (anchor; *Shaska [Sha26, Lem. 8.5]*, obtained independently here).** For every Keller map in the class, of any degree,

    λ = C₀(1) · B₀′(1) · A₁(1).

In particular every Keller lift — counterexample or automorphism — has C₀(1) ≠ 0, B₀′(1) ≠ 0, A₁(1) ≠ 0.
*Proof.* Evaluate 𝓑₂ at (u,s) = (1,0). Lift conditions give A(1,0) = A_u(1,0) = 0 (double root) and B(1,0) = 0; two of the three terms vanish and the third contributes C₀(1)·B₀′(1)·A₁(1). (Machine-verified at full deg ≤ 6 generality; the derivation is degree-free.) Example: 2 = 2·1·1. ∎

**Remark (attribution for Lemma 6.1).** Shaska states this as: evaluating the master equation at the base point O of the quotient plane gives Λ(O)·{B,A}(O) = κ, whence Λ(O) ≠ 0 and dA∧dB|_O ≠ 0 [Sha26, Lem. 8.5]. Translating his base point to (u,s) = (1,0) and using the lift conditions to kill A_u(1,0) turns {B,A}(O) = B_u A_s − B_s A_u into B₀′(1)A₁(1), which is the displayed factorization: the two statements are the same lemma, and his is earlier (July 25, 2026, in v2 of [Sha26]). We keep our formulation because the factored form is what the case analysis of Theorem E consumes.

The following appears to be new; we have found no analogue in [May26], [Sha26], [Ula26], [Lou26], [MO513387]. The nearest published statements are [Sha26, Rem. 8.8], which handles the case Λ constant (where the graded problem in dimension n collapses to the ordinary Jacobian conjecture in dimension n−1), and [Sha26, Thm. 10.10], which handles A and B both of degree one in the invariants. Lemma 6.2 constrains the s-degree rather than the total degree, and is what makes Branch I of Theorem E finite.

**Lemma 6.2 (no-go; all weights k ≥ 1; *new*).** If C is s-free and A, B are at most affine in s, every Keller lift in the class is a polynomial automorphism — at any degree.
*Proof.* Write A = A₀(u) + A₁(u)s, B = B₀(u) + B₁(u)s, C = C₀(u), and recall the invariant outputs p − 1 = BC and q = AC^k. Note first that C₀ ≠ 0 as a polynomial (else 𝓑_k = 0), and that if A₁ = B₁ = 0 then 𝓑_k = 0 and the map is not Keller; so at least one of A₁, B₁ is nonzero. Throughout, (X,Y,T) denote the target coordinates of F, so that p = 1 + YT and q = XT^k are rational in the target.

*Main case A₁B₁ ≠ 0.* The bracket 𝓑_k is affine in s; setting its s-coefficient to zero and dividing by A₁B₁C₀ gives B₁′/B₁ − A₁′/A₁ − (k−1)C₀′/C₀ = 0, i.e. B₁ = κA₁C₀^{k−1} for a constant κ ∈ ℂ* (a logarithmic-derivative computation). With this substitution the bracket collapses to the verified identity

    𝓑_k = A₁·(C₀B₀ − κC₀^k A₀)′.

A polynomial times a derivative being the nonzero constant λ forces A₁ ∈ ℂ* and C₀B₀ − κC₀^k A₀ = λ̃u + μ with λ̃ = λ/A₁ ≠ 0. A second verified identity says that, with these forced shapes, the s-terms of (p−1) − κq cancel *identically*:

    (p−1) − κq = C₀B₀ − κC₀^k A₀ = λ̃u + μ.

Now invert F rationally, in three steps. First, u = ((p−1) − κq − μ)/λ̃ is a polynomial in (p,q), hence rational in the target. Second, at fixed u the relation p − 1 = (B₀ + B₁s)C₀ is affine in s with s-coefficient B₁C₀ = κA₁C₀^k ≠ 0 in ℂ(u), so s = ((p−1) − B₀C₀)/(κA₁C₀^k) is rational in the target. Third, x = F₃/C(u,s) = T/C₀(u), then y = (u−1)/x and z = s/x^k, are rational in the target. So F is birational, and a birational Keller map is a polynomial automorphism [vdE00, Cor. 1.1.35] (equivalently [BCW82, Thm. 2.1]; the birational case goes back to Keller [Kel39]).

*Edge case B₁ = 0, A₁ ≠ 0.* Here the bracket collapses to 𝓑_k = A₁·(C₀B₀)′ — the κ = 0 instance of the displayed identity — so again A₁ ∈ ℂ* and C₀B₀ = λ̃u + μ with λ̃ ≠ 0. Since B is s-free, p − 1 = B₀C₀ = λ̃u + μ, so u is affine in p; then q = (A₀ + A₁s)C₀^k gives s = (qC₀^{−k} − A₀)/A₁, rational in the target, and x, y, z are recovered as above: F is birational, hence an automorphism.

*Edge case A₁ = 0, B₁ ≠ 0.* Here the bracket reduces to the relation B₁·(C₀^k A₀)′ = −λC₀^{k−1}. Compare orders of vanishing at u = 1, writing a = ord₁A₀ and c = ord₁C₀: the lift condition (u−1)^k | A₀ gives a ≥ k, so the left side has ord₁ = ord₁B₁ + kc + a − 1 (the derivative drops the order by exactly one in characteristic zero), while the right side has ord₁ = (k−1)c; equality forces ord₁B₁ + c + a = 1, impossible for k ≥ 2 since a ≥ k ≥ 2 — this subcase is empty, consistent with Theorem E. For k = 1 the relation reads B₁·(C₀A₀)′ = −λ: a product of polynomials equal to a nonzero constant, so B₁ ∈ ℂ* and C₀A₀ is affine in u with nonzero slope. Then q = AC = A₀C₀ is affine in u with nonzero slope: u is affine in q; then p − 1 = (B₀ + B₁s)C₀ recovers s rationally (B₁C₀ ≠ 0), and x, y, z follow as above: F is birational, hence an automorphism. (The two identities displayed in the main case are verified in `core_verify.py`.) ∎

**Corollary 6.3.** A counterexample must put s inside C, or s²-terms inside A or B. Alpöge's map takes the first exit: C = 5 − 3u − s.

**Proof of Theorem E.** Split on the shape of C under the deg ≤ 6 caps.

*Branch I: C s-free.* (a) C₀ constant: G is affine ∘ (planar Keller pair of degree ≤ 4), invertible by Moh [Moh83]. (b) A, B s-affine: Lemma 6.2. (c) s²-sector (C₀ nonconstant, (A₂,B₂) ≠ (0,0)): six normalized polynomial systems (leading-coefficient nonvanishing via a Rabinowitsch variable); **msolve returns the unit ideal over ℚ for all six** — empty by the Nullstellensatz.

*Branch II: C₁ ≠ 0.* Two systems at *full* generality — no hand-derived reduction is load-bearing — with only λ = 1 and C₁ monic (resp. = 1) normalized. **Unit ideal over ℚ, both.** Nothing exists in this sector below degree 7, automorphisms included.

| Leaf | Sector | Eqs | Unknowns | Result (ℚ and 𝔽₃₂₀₀₃) |
|---|---|---|---|---|
| II-f1 | C₁ monic linear | 26 | 19 | (1) |
| II-f0 | C₁ = 1 | 23 | 18 | (1) |
| I-B2-g2 | B₂ = 1, deg C₀ = 2 | 23 | 18 | (1) |
| I-B2-g1 | B₂ = 1, deg C₀ = 1 | 19 | 17 | (1) |
| I-A2L-g2 | A₂ monic linear, deg C₀ = 2 | 20 | 17 | (1) |
| I-A2L-g1 | A₂ monic linear, deg C₀ = 1 | 17 | 16 | (1) |
| I-A2c-g2 | A₂ = 1, deg C₀ = 2 | 19 | 16 | (1) |
| I-A2c-g1 | A₂ = 1, deg C₀ = 1 | 16 | 15 | (1) |

*Positive control.* At the degree-7 caps the torus-scaled example satisfies the identical normalized system (𝓑₂ = 1, C₁-coefficient = 1) — verified exactly by substitution: with ν = 2^{−1/5} (exact, ν⁵ = 1/2) and r = −1/ν, the scaled triple (νr⁻²A, νr⁻¹B, νrC) has C₁-coefficient 1 and bracket identically 1; the asserted form of this check is `min_verify.py` part `d7control`. (An msolve reduced-basis run on the degree-7 control system did not terminate within a 600-second cap — expected for a nonempty positive-dimensional variety; the exact substitution above is the control, and the computational record is `certificates/D7CONTROL-NEGATIVE-RESULT.md` in the repository.) The pipeline provably contains the counterexample at degree 7 and provably contains nothing at degree ≤ 6. All eight emptiness certificates were computed over ℚ (msolve multi-modular F4); the mod-32003 reproductions were run independently in both msolve and SymPy's Gröbner engine (`min_verify.py` parts `I` and `II`). SymPy additionally verifies the structural layer identities used to organize — but not to prove — the case split. ∎

**Remark (anatomy of the exit at degree 7).** In the sector A₂ = B₂ = 0, C₁ ≠ 0, a layer computation shows the top s-layer forces B₁³ = ρ·A₁²C₁, i.e. 3·deg B₁ = 2·deg A₁ + deg C₁. Under the deg ≤ 6 caps only the patterns (0,0,0) and (1,1,1) survive, and both die against the anchor lemma; the example lives on the pattern (deg B₁, deg A₁, deg C₁) = (2,3,0) — 6 = 6 + 0 — which forces deg F₁ = 7. Degree 7 is not an accident; it is the first rung the mechanism can reach.

This layer relation is a special case of a published one. Shaska [Sha26, Thm. 10.6] shows that the leading forms Â, B̂, Λ̂ of any graded Keller map are, up to constants, products of powers of a common set of linear forms, subject to the Diophantine system β_i + rγ_i = (ν_B/e)m_i, α_i + sγ_i = (ν_A/e)m_i; and his Example 10.9 works out that system at the degrees **d** = (4,3,1) of Alpöge's map, finding h = u(3u+v), m = (1,1), β = (2,1), γ = (0,1), α = (3,1) and concluding that "the leading data of the announced counterexample is thus the solution of a small system of linear equations in nonnegative integers, and not an accident". Our relation B₁³ = ρA₁²C₁ is the same constraint read one s-layer at a time, and the conclusion above is the same conclusion; his is earlier (July 25, 2026) and more general. What the remark adds is the pairing of that constraint with the anchor identity to *exclude* the surviving low-degree patterns — exactly the content that Theorem E certifies and that [Sha26, Rem. 10.8] explicitly says the stratification alone does not give ("emptiness must therefore be proved stratum by stratum").

**Scope caveats, stated plainly.** (i) Theorem E is relative to this symmetry class: weights (1,−1,−2) and this lift shape. Other weights (1,−1,−k) and non-equivariant maps are untouched; "no degree ≤ 6 counterexample in ℂ³" remains open — unconditionally, invertibility of Keller maps is known only through degree 2, in every dimension, by Wang's theorem [Wan80]. (ii) The char-0 emptiness certificates rest on msolve's multi-modular F4 over ℚ; the mod-p runs concur. An independent certificate checker that replays the unit-ideal cofactor identities has not yet been built, so a reader who does not trust msolve over ℚ has at present only the mod-32003 cross-reproduction. (iii) Moh's and Campbell's theorems are quoted from the literature. (iv) Certificates for the weights k = 1 and k = 3 are in preparation and are not claimed here. (v) Emptiness *inside* a class is not emptiness outside it: ulam.ai [Ula26, Thm. 5.1, Cor. 5.3] produces a (λ,a,c,H)-family with the same cubic geometry, and nonproper Keller maps of every generic degree d ≥ 3; Gao [Gao26] produces further explicit counterexamples in every dimension > 2 by a tangent-sweep construction; Migus [Mig26] determines the possible generic degrees over ℝ. None of these is a degree-≤6 member of our equivariant class, but they are a reminder that the map is not isolated in any broad sense — a point Mayner records as a correction to his own rigidity claim [May26, §12].

**Stable reductions.** By Bass–Connell–Wright [BCW82], Yagzhev [Yag80], and Drużkowski [Dru83], the example yields cubic-homogeneous (even cubic-linear-form) counterexamples in some higher ℂᴺ; in the SBS thread an explicit cubic-homogeneous reduction in 24 variables was described (Thompson), and Long [Lon26] tracks a conservative Bass–Connell–Wright reduction of the announced map to 79 variables en route to the Gaussian Moments conjecture. Explicit degree/dimension bookkeeping, the smallest such N, and minimality for the other weights (1,−1,−k) are worthwhile follow-ups — the master equation is already general and the same certificate pipeline applies.

**Other consequences drawn elsewhere.** For orientation, the July 2026 consequence-drawing around this map includes: the Dixmier conjecture, Mayner [May26]; the Gaussian Moments conjecture, Long [Lon26]; the Hessian conjecture in five variables, Meng–Yang [MY26]; the separable Jacobian conjecture in characteristic 2, Huq-Kuruvilla [HK26]; quantum inequivalence of scalar field redefinitions, Zhu [Zhu26]; the structure of the space of Keller maps, Jelonek [Jel26]; real generic degrees, Migus [Mig26]; further families, ulam.ai [Ula26] and Gao [Gao26]; and the graded classification, Shaska [Sha26]. The present note contributes to none of those lines except the last.

## 7. Reproducibility

Trust model, stated exactly (it matches scope caveat (ii) of §6): every polynomial identity in this note is an exact symbolic check asserted in SymPy 1.14 (arbitrary-precision rational arithmetic). The characteristic-zero emptiness certificates of Theorem E rest on msolve 0.10.1's certified multi-modular F4 over ℚ; SymPy independently reproduces the mod-32003 runs, so the cross-system reproduction concerns the mod-p computations, while the characteristic-zero certificates rest on msolve alone. No numerical approximation occurs anywhere. A self-contained independent certificate checker (replaying unit-ideal cofactor identities) is desirable and not yet built.

| Artifact | Contents |
|---|---|
| `core_verify.py` | map, det JF = −2, collisions, collapse, master equation (all k), critical-line facts, no-go identities |
| `cover_verify.py` | cubic, trace, discriminant, S₃, 3:1, image/escape analysis |
| `weyl_verify.py` | polynomiality of N, CCR identities (A) and (B); writes `weyl_endomorphism.txt` |
| `dixmier_symplectic_verify.py` | MᵀΩM = Ω, det M = 1, degrees, ℂ⁶ triple collision, ν∘Φ = μ, CCR re-check |
| `min_verify.py` | anchor lemma at full generality, layer identities, image certificate at (7/3, 4/27) over ℚ (`ident`); SymPy Gröbner harness for the eight leaf systems mod 32003 (`I`, `II`); degree-7 positive control by exact scaled substitution (`d7control`); upstairs identity det JF = −𝓑_k for k = 1,2,3 (`kdet`); axis-target uniqueness certificate (`axis`) |
| `ms_*_c{0,32003}.ms`, `out_*.txt` | the eight leaf systems, char 0 and mod 32003 (`out_*_q.txt` = char 0, `out_*_p.txt` = mod 32003); all sixteen outputs are the reduced Gröbner basis [1] |

    python3 -m venv venv && venv/bin/pip install sympy
    venv/bin/python core_verify.py
    venv/bin/python cover_verify.py
    venv/bin/python weyl_verify.py
    venv/bin/python dixmier_symplectic_verify.py
    venv/bin/python min_verify.py ident
    venv/bin/python min_verify.py d7control
    venv/bin/python min_verify.py kdet
    venv/bin/python min_verify.py axis
    venv/bin/python min_verify.py I    # SymPy GB, six Branch-I leaves, mod 32003
    venv/bin/python min_verify.py II   # SymPy GB, two Branch-II leaves, mod 32003
    brew install msolve
    for f in ms_I-*_c0.ms ms_II-*_c0.ms; do b=${f#ms_}; \
      msolve -g 2 -f "$f" -o "out_${b%_c0.ms}_q.txt"; done          # char 0
    for f in ms_I-*_c32003.ms ms_II-*_c32003.ms; do b=${f#ms_}; \
      msolve -g 2 -f "$f" -o "out_${b%_c32003.ms}_p.txt"; done      # mod 32003

Expected: every `out_*_q.txt` and `out_*_p.txt` contains the reduced Gröbner basis [1], matching the stored outputs.

## Acknowledgments

We are grateful to W. G. P. Mayner, whose note and report [May26] first put both the Weyl-algebra endomorphism *and* the symplectic cotangent lift on public record, and whose computations go beyond ours at several points; to T. Shaska [Sha26], whose graded framework contains, in greater generality and earlier, the master equation, the base-point identity, the divisorial form of the Keller condition, and the leading-form analysis that we had arrived at independently; to the anonymous author of [Ula26] for the earliest published fiber-count and image theorem; and to the participants of the Secret Blogging Seminar discussion [Spe26] — in particular the explicit 24-variable cubic-homogeneous reduction described there (Thompson). Discovering that a result one has proved was proved first by someone else is the ordinary condition of working on a problem that is three weeks old and crowded; we have tried to record it accurately rather than minimally. The debt to Levent Alpöge's example, and to Akhil Mathew for posing the problem, is total. Computations were carried out with Claude (Fable 5), SymPy 1.14, and msolve 0.10.1.


## Note added (August 4, 2026)

A final pre-release survey found two independent observations adjacent to Theorem C: a note of
A. Husain (github.com/Cobord/Jacobian, Aug 1, 2026) constructs the cotangent-lift Poisson
endomorphism and observes the weighted-torus intertwining, posing the isotropy computation as
open, without moment-map structure; and a blog comment of D. Fillmore (Jul 31, 2026, on Tao's
digestion post) interprets the 3-to-1 fiber via Majorana spin addition, without symplectic
content. Neither states the moment-map identity nu∘Phi = mu proved here.

## References

- [AvdE07] P. K. Adjamagbo, A. van den Essen, *A proof of the equivalence of the Dixmier, Jacobian and Poisson conjectures*, Acta Math. Vietnam. 32 (2007), 205–214; arXiv:math/0608009.
- [Alp26] L. Alpöge, *A counterexample to the Jacobian conjecture in dimension three*, public announcement, July 19, 2026; see [Tao26], [Spe26].
- [BCW82] H. Bass, E. H. Connell, D. Wright, *The Jacobian conjecture: reduction of degree and formal expansion of the inverse*, Bull. Amer. Math. Soc. (N.S.) 7 (1982), 287–330.
- [Bav05] V. V. Bavula, *The Jacobian conjecture₂ₙ implies the Dixmier problemₙ*, arXiv:math/0512250 (2005).
- [BL20] V. V. Bavula, V. Levandovskyy, *A remark on the Dixmier conjecture*, Canad. Math. Bull. 63 (2020), 6–12.
- [BKK05] A. Belov-Kanel, M. Kontsevich, *Automorphisms of the Weyl algebra*, Lett. Math. Phys. 74 (2005), 181–199; arXiv:math/0512169.
- [BKK07] A. Belov-Kanel, M. Kontsevich, *The Jacobian conjecture is stably equivalent to the Dixmier conjecture*, Mosc. Math. J. 7 (2007), 209–218; arXiv:math/0512171.
- [Cam73] L. A. Campbell, *A condition for a polynomial map to be invertible*, Math. Ann. 205 (1973), 243–248.
- [Dix68] J. Dixmier, *Sur les algèbres de Weyl*, Bull. Soc. Math. France 96 (1968), 209–242.
- [Dru83] L. M. Drużkowski, *An effective approach to Keller's Jacobian conjecture*, Math. Ann. 264 (1983), 303–313.
- [Gao26] S. Gao, *Counterexamples to the Jacobian conjecture in dimensions greater than two*, arXiv:2608.00222v1, July 31, 2026.
- [HK26] I. Huq-Kuruvilla, *An explicit characteristic-2 counterexample to the separable Jacobian conjecture*, arXiv:2607.20968v1, July 23, 2026.
- [Jel26] Z. Jelonek, *On mappings with Jacobian one*, arXiv:2607.20597v1, July 22, 2026.
- [KBEY18] A. Kanel-Belov, A. Elishev, J.-T. Yu, *Automorphisms of Weyl Algebra and a Conjecture of Kontsevich*, arXiv:1802.01225 (2018).
- [Kel39] O.-H. Keller, *Ganze Cremona-Transformationen*, Monatsh. Math. Phys. 47 (1939), 299–306.
- [Lon26] C. D. Long, *Small counterexamples to the Gaussian Moments conjecture*, arXiv:2607.18186v1, July 20, 2026.
- [Lou26] A. Lou, *A derivation of the Jacobian conjecture counterexample*, note, https://aaronlou.com/jacobian_counterexample_derivation.pdf; PDF timestamp July 20, 2026.
- [May26] W. G. P. Mayner, *The Dixmier conjecture fails for Aₙ, n ≥ 3* (informal note, 6 pp., `dixmier-note.tex`) together with *Structural analysis of the Jacobian conjecture counterexample in ℂ³* (`REPORT.md`), both prepared with Claude Fable 5, github.com/wmayner/dixmier-counterexample, commits of July 21, 2026, 05:36 and 06:41 UTC; the Dixmier statement was first made in a comment on [Spe26], July 20, 2026. Section references of the form §n are to `REPORT.md`. The symplectic cotangent lift is §8 of `REPORT.md` (verified-facts table item 24; priority list §12, item 3) and item 2 of "What this does not give" in `dixmier-note.tex`.
- [MO513387] *Galois structure of the new counterexample to the Jacobian conjecture: an explicit cubic model with S₃ monodromy — is this known?*, MathOverflow question 513387, posted July 20, 2026, 07:56 UTC (no answers as of August 4, 2026), https://mathoverflow.net/q/513387.
- [MY26] G. Meng, L. Yang, *A five-variable counterexample to the Hessian conjecture, and the low-dimensional status of the Jacobian and Hessian conjectures*, arXiv:2607.22198v2, July 24/27, 2026.
- [Mig26] P. Migus, *Generic degrees of real polynomial Keller maps with non-dense image*, arXiv:2607.21572v2, July 23/30, 2026.
- [Moh83] T. T. Moh, *On the Jacobian conjecture and the configurations of roots*, J. Reine Angew. Math. 340 (1983), 140–212.
- [Sha26] T. Shaska, *Graded Keller maps and the Jacobian Conjecture*, arXiv:2607.20210; v1 July 22, 2026, v2 July 25, 2026. References here are to v2 unless stated otherwise; Thm. 7.1 of v2 is Thm. 6.1 of v1, and Thm. 8.3, Lem. 8.5, §9.2 and §10 appear only in v2.
- [Spe26] D. E. Speyer, *The new counterexample to the Jacobian conjecture*, blog post with comment thread, Secret Blogging Seminar, July 20, 2026, https://sbseminar.wordpress.com/2026/07/20/the-new-counterexample-to-the-jacobian-conjecture/.
- [Tao26] T. Tao, *A digestion of the Jacobian conjecture counterexample*, blog post, What's new, July 21, 2026, https://terrytao.wordpress.com/2026/07/21/a-digestion-of-the-jacobian-conjecture-counterexample/.
- [Tsu05] Y. Tsuchimoto, *Endomorphisms of Weyl algebra and p-curvatures*, Osaka J. Math. 42 (2005), 435–452.
- [Ula26] Anonymous, *A counterexample to the Jacobian conjecture*, note (7 pp.), https://ulam.ai/research/jacobian.pdf; PDF timestamp July 20, 2026, 05:54 EDT.
- [vdE00] A. van den Essen, *Polynomial Automorphisms and the Jacobian Conjecture*, Progress in Mathematics 190, Birkhäuser, 2000.
- [Wan80] S. S.-S. Wang, *A Jacobian criterion for separability*, J. Algebra 65 (1980), 453–494.
- [Yag80] A. V. Yagzhev, *On Keller's problem*, Sibirsk. Mat. Zh. 21 (1980), no. 5, 141–150; English transl., Siberian Math. J. 21 (1980), 747–754.
- [Zhu26] B. Zhu, *Non-injective field redefinitions and quantum inequivalence in scalar theories*, arXiv:2607.18166v1, July 20, 2026.
- [Zhe24] A. B. Zheglov, *The Conjecture of Dixmier for the first Weyl algebra is true*, arXiv:2410.06959 (2024; v5, January 19, 2026); claimed proof of DC₁, under review at the time of writing.
