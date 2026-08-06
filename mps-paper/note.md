# A bond-dimension-two matrix-product state that is an exact zero-energy eigenstate at every length of a nearest-neighbour spin-½ chain

**Daniel Kirtchakov**
Independent researcher (`05oz`); no institutional affiliation — daniel@halfounce.io — halfounce.io

*Draft of August 6, 2026.*

> **Computation and authorship.** The construction, the certificate, and
> the verifiers in this note were produced by **Claude Fable 5**
> (Anthropic), directed by the author, on a single Apple M4 laptop. The
> exact-arithmetic verifier `reverify.py` imports only the Python standard
> library; the independent cross-check `xcheck.py` assembles the
> Hamiltonian densely from Pauli matrices in `numpy` with `object`-dtype
> (exact integer) arithmetic and shares no code with `reverify.py`. This is
> a factual methods statement: the artifacts are designed so that the
> provenance of the *search* is irrelevant to the validity of the *result*,
> which is a finite exact identity together with an elementary algebraic
> argument.

> **Prior-art record.** The four primary sources cited for the certificate
> technique and the model class — arXiv:2503.16327, arXiv:2605.03020,
> arXiv:2603.28349, and arXiv:1910.06616 (PRX **10**, 021051, 2020) — were
> read directly on August 6, 2026. The telescoping matrix-product-ansatz
> certificate is a published, standard technique and is credited to it at
> every point of use; only the specific Hamiltonian–eigenstate pair is
> offered as new, and only to the extent that a finite literature sweep of
> that date can support (§1.4).

---

## Abstract

We exhibit a translation-invariant matrix-product state (MPS) of bond
dimension two, with integer transfer matrices A⁰ = [[1,0],[0,−1]] and
A¹ = [[−2,−1],[1,0]], that is an exact zero-energy eigenstate, at *every*
finite length *L*, of the periodic nearest-neighbour spin-½ Hamiltonian
*H* = −Σᵢ (I+Xᵢ)(Xᵢ₊₁+Zᵢ₊₁). The proof is a single finite identity: a
telescoping certificate Σₛₜ ⟨uv|h|st⟩ AˢAᵗ = CᵘAᵛ − AᵘCᵛ holds with the
integer matrices C⁰ = [[−2,1],[1,−2]], C¹ = [[3,2],[0,−1]] (sixteen scalar
equations, all exact), whose right-hand side telescopes around the periodic
trace, giving *H*|ψ_L⟩ = 0 for all *L* at once. This is the
matrix-product-ansatz mechanism of Derrida, Evans, Hakim and Pasquier
(1993) in its eigenstate form (Gehrmann and Essler, arXiv:2605.03020,
Eq. (10)); the existence of a certificate of this form for any injective
MPS eigenstate is the local characterization of Garre Rubio, Molnár, Schuch
and Verstraete (arXiv:2603.28349), so the *technique* is not new and is
credited as such. The state is genuinely bond dimension two
({I, A⁰, A¹, A⁰A¹} spans M₂(ℂ)): its exact odd/even sublattice Schmidt rank
over ℚ is 2, 4, 8 at *L* = 4, 6, 8, so the minimal number of product states
in a decomposition across that cut grows over the computed range. Every
quantitative claim is re-established from raw data by a standard-library
exact-arithmetic verifier, and the eigenvalue property is independently
re-established by a dense `numpy` build; both are shipped with SHA-256
digests. We make no claim about
the thermal or non-thermal character of the remainder of the spectrum of
*H*, and object-level novelty rests on a finite sweep and cannot be absolute
(§1.4).

---

## 1. Introduction

### 1.1. The construction

Fix the single-site basis |0⟩, |1⟩ and the Pauli matrices
X = [[0,1],[1,0]], Z = [[1,0],[0,−1]], I = [[1,0],[0,1]]. For a chain of *L*
sites with periodic boundary conditions (site *L*+1 identified with site 1),
let

> **(1)**   *H* = −Σᵢ₌₁ᴸ (I + Xᵢ)(Xᵢ₊₁ + Zᵢ₊₁),

where (I + Xᵢ)(Xᵢ₊₁ + Zᵢ₊₁) denotes the two-site operator (I + X) ⊗ (X + Z)
acting on the neighbouring pair (*i*, *i*+1) and the identity elsewhere.
Both factors are real symmetric, so *H* is Hermitian.

Define the two integer 2×2 transfer matrices

> **(2)**   A⁰ = [[1, 0], [0, −1]],   A¹ = [[−2, −1], [1, 0]],

and the translation-invariant, periodic matrix-product state

> **(3)**   |ψ_L⟩ = Σ_{s ∈ {0,1}ᴸ} Tr(A^{s₁} A^{s₂} ⋯ A^{s_L}) |s₁ s₂ ⋯ s_L⟩.

The bond dimension is 2: the auxiliary index summed in the trace ranges over
two values. Note A⁰ = Z; the second matrix A¹ is not normal and {A⁰, A¹} do
not commute.

### 1.2. Result

**Theorem 1.1.** *For every L ≥ 3 the state |ψ_L⟩ of (3) is nonzero and
satisfies H|ψ_L⟩ = 0 exactly, with H the periodic Hamiltonian (1). The state
is genuinely of bond dimension two (the four matrices I, A⁰, A¹, A⁰A¹ are
linearly independent and span M₂(ℂ)), and its exact Schmidt rank across the
odd/even sublattice bipartition is 2, 4, 8 at L = 4, 6, 8 respectively, so
the minimal number of product states in a decomposition across that cut is at
least eight at L = 8 and grows over the computed range.*

The eigenvalue statement *H*|ψ_L⟩ = 0 for all *L* is not a numerical
observation extrapolated from small sizes: it follows from a single finite
identity in the 2×2 matrices, proved in §2 (Lemma 2.1 and Proposition 2.2).
Sizes *L* = 3,…,10 are additionally checked by direct dense substitution as
corroboration (§4). The norm is ‖ψ_L‖² = 4ᴸ for *L* = 3,…,9 (§4), so
|ψ_L⟩ ≠ 0 there; nonvanishing for all *L* also follows from
bond-dimension-two irreducibility (Proposition 2.3).

### 1.3. Provenance of the method, and what is new

The mechanism behind Theorem 1.1 is the *matrix-product ansatz*. In the
exact solution of the asymmetric simple exclusion process, Derrida, Evans,
Hakim and Pasquier [DEHP93] represent the stationary weight as a matrix
product and reduce stationarity to a local algebraic relation between the
representing matrices; the same device produces *eigenstates*, not only
steady states, when the local relation is read as a commutator identity.
Gehrmann and Essler [GE26] write this eigenstate form explicitly — their
Eq. (10), *h A A = E A − A E*, a generalization of the DEHP ansatz — and use
it to construct exact MPS eigenstates of several spin-*S* chains and
square-lattice models. Garre Rubio, Molnár, Schuch and Verstraete [GRMSV26]
prove that a local, fixed-size equation of exactly this shape — how one
Hamiltonian term acts on a block of tensors — is *necessary and sufficient*
for an injective MPS to be an exact eigenstate of an extensive local
operator.

Two consequences frame this note precisely. First, the *certificate
technique is not new*: it is standard, and the existence of a certificate of
the form used here is guaranteed *a priori* for any injective MPS eigenstate
by [GRMSV26]. We credit it as such at the point of use in §2, and claim no
novelty in the method. Second, what a certificate does not do is exhibit the
pair; the content offered here is the specific Hamiltonian–eigenstate pair
(1)–(3) together with its explicit integer certificate (5) and the
entanglement facts of §3. The scope and the limits of that object-level
claim are stated in §1.4.

### 1.4. What is not claimed

The claim is object-level and is bounded in three explicit ways.

*The technique is credited, not claimed.* As above, the telescoping
matrix-product-ansatz certificate is due to [DEHP93] in origin, is written
in eigenstate form in [GE26], and is guaranteed to exist by [GRMSV26].
Nothing about the *method* is asserted to be new.

*No spectral or thermalization claim is made.* We establish that |ψ_L⟩ is
one exact eigenstate, with eigenvalue 0, of *H*. We do not analyse the rest
of the spectrum of *H*, its level-spacing statistics, or whether the model
thermalizes; no statement about non-thermal behaviour, weak ergodicity
breaking, or the surrounding spectrum is made or implied. The proven content
is exactly the four properties of Theorem 1.1.

*Object-level novelty rests on a finite sweep.* On August 6, 2026 the four
sources above were read directly. In [IM25] the exact area-law eigenstates
are constructed inside a kinetically constrained subspace (PXP-type models,
via a projector onto a Fibonacci-constrained space); our |ψ_L⟩ lives in the
full 2ᴸ-dimensional Hilbert space with no projector-defined subspace, and
its transfer matrices (2) are not among theirs. The spin-½ instance of
Model I of [GE26] is a Rydberg-plus-Dzyaloshinskii–Moriya chain with a
complex free-parameter family of tensors, a different Hamiltonian with
non-integer tensors; the worked example of [GRMSV26] is the quantum-group
symmetry of the XXZ chain; and the states of [PGCGB20] become exact only in
the large-size limit, whereas |ψ_L⟩ is exact at every finite *L*. In none of
the four was the pair (1)–(3) found. A finite sweep cannot exclude a
unitarily or gauge-equivalent reformulation in a venue not examined; the
novelty claim is made at exactly that strength and no more.

## 2. The telescoping certificate and the all-length proof

### 2.1. The bond operator

Write the two-site bond operator of (1) as

> **(4)**   h = −(I + X) ⊗ (X + Z),

so that *H* = Σᵢ₌₁ᴸ h_{i,i+1} (periodic). In the ordered two-site basis
|00⟩, |01⟩, |10⟩, |11⟩,

> h = −[[1,1,1,1],[1,−1,1,−1],[1,1,1,1],[1,−1,1,−1]],

which is real symmetric, confirming *H*† = *H*. We index its entries by
⟨uv|h|st⟩ with *u, v, s, t* ∈ {0,1}.

### 2.2. The certificate identity

The following is the matrix-product-ansatz certificate in the eigenstate
form of [GE26] (Eq. (10)), whose existence for an injective MPS eigenstate
is guaranteed by [GRMSV26] and whose mechanism is that of [DEHP93].

**Lemma 2.1 (Certificate).** *With h as in (4), A⁰, A¹ as in (2), and the
integer matrices*

> **(5)**   C⁰ = [[−2, 1], [1, −2]],   C¹ = [[3, 2], [0, −1]],

*the sixteen scalar equations*

> **(6)**   Σ_{s,t ∈ {0,1}} ⟨uv|h|st⟩ AˢAᵗ = CᵘAᵛ − AᵘCᵛ   (u, v ∈ {0,1})

*hold exactly.*

*Proof.* Both sides of (6) are 2×2 integer matrices, so this is a finite
verification. For (u,v) = (0,0) the row ⟨00|h|·⟩ is −(1,1,1,1), so the
left-hand side is −(A⁰A⁰ + A⁰A¹ + A¹A⁰ + A¹A¹) = −[[0,2],[−2,0]] =
[[0,−2],[2,0]], while C⁰A⁰ − A⁰C⁰ = [[−2,−1],[1,2]] − [[−2,1],[−1,2]] =
[[0,−2],[2,0]], which agree. The remaining fifteen equations are identical
finite checks. The verifier `reverify.py` (§4) does not assume (5): it solves
the linear system (6) for the eight entries of C⁰, C¹ exactly over ℚ, finds
it consistent, recovers (5), and confirms all sixteen residuals vanish. ∎

### 2.3. The periodic telescope

**Proposition 2.2.** *For every L ≥ 1, H|ψ_L⟩ = 0.*

*Proof.* Fix a basis configuration *u* = (u₁,…,u_L) ∈ {0,1}ᴸ. The amplitude
of |ψ_L⟩ at *u* is Tr(A^{u₁} ⋯ A^{u_L}). Applying the single bond term
h_{i,i+1} and reading off the amplitude at *u* replaces the adjacent pair
A^{uᵢ}A^{uᵢ₊₁} inside the trace by Σ_{s,t} ⟨uᵢuᵢ₊₁|h|st⟩ AˢAᵗ; by the
certificate (6) this equals C^{uᵢ}A^{uᵢ₊₁} − A^{uᵢ}C^{uᵢ₊₁}. Hence

> (h_{i,i+1}|ψ_L⟩)_u = Tr(A^{u₁} ⋯ A^{uᵢ₋₁} [C^{uᵢ}A^{uᵢ₊₁} − A^{uᵢ}C^{uᵢ₊₁}] A^{uᵢ₊₂} ⋯ A^{u_L}) = f(i) − f(i+1),

where f(*i*) denotes the trace Tr(A^{u₁} ⋯ A^{uᵢ₋₁} C^{uᵢ} A^{uᵢ₊₁} ⋯ A^{u_L})
with the single insertion A^{uᵢ} ↦ C^{uᵢ} at position *i*, and where the
second term is f(*i*+1) because a *C* at the right factor of the bond
(*i*, *i*+1) is a *C* at position *i*+1. Summing over the periodic chain,

> (H|ψ_L⟩)_u = Σᵢ₌₁ᴸ (f(i) − f(i+1)) = f(1) − f(L+1) = 0,

the sum telescoping and f(*L*+1) = f(1) by periodicity of the trace. As *u*
was arbitrary, *H*|ψ_L⟩ = 0. ∎

The argument uses only the finite identity (6) and the cyclic invariance of
the trace; it is uniform in *L*. This is precisely the telescoping
guaranteed by [GRMSV26] for an MPS eigenstate and realized concretely as in
[GE26, DEHP93].

### 2.4. Genuine bond dimension two, and non-frustration-freeness

**Proposition 2.3.** *The matrices I, A⁰, A¹, A⁰A¹ are linearly independent
and span M₂(ℂ); equivalently, the MPS (3) is injective of bond dimension
exactly two. Consequently |ψ_L⟩ ≠ 0 for all L ≥ 3.*

*Proof.* Writing each 2×2 matrix as a row vector in the basis
(E₁₁, E₁₂, E₂₁, E₂₂) gives I = (1,0,0,1), A⁰ = (1,0,0,−1), A¹ = (−2,−1,1,0)
and A⁰A¹ = (−2,−1,−1,0); the determinant of the resulting 4×4 integer matrix
is −4 ≠ 0, so the four matrices are a basis of M₂(ℂ). Spanning M₂(ℂ) is
injectivity of the MPS transfer map, which forces |ψ_L⟩ ≠ 0 for *L* ≥ 3; the
explicit norms ‖ψ_L‖² = 4ᴸ of §4 confirm this for *L* = 3,…,9. ∎

**Remark 2.4 (Not frustration-free).** The cancellation in Proposition 2.2
is global, not termwise: a single bond term does not annihilate the state.
Explicitly h_{1,2}|ψ₄⟩ ≠ 0 (checked exactly; §4), so |ψ_L⟩ is not a common
zero of the individual bond terms and *H* is not frustration-free on it. The
eigenvalue 0 is produced by the telescoping sum of nonzero local
contributions, which is the whole point of the certificate.

## 3. Entanglement: a growing sublattice Schmidt rank

For a bipartition of the sites into two blocks, the Schmidt rank of a state
is the rank of its coefficient matrix under the induced reshaping; a state
that is a sum of *k* product states has Schmidt rank at most *k* across
*every* bipartition. Two bipartitions are computed exactly over ℚ (§4).

**Proposition 3.1.** *For the contiguous half-cut
{1,…,L/2} | {L/2+1,…,L}, the exact Schmidt rank of |ψ_L⟩ is 4 at
L = 4, 6, 8, saturating the bond-dimension bound D² = 4. For the odd/even
sublattice bipartition {1,3,5,…} | {2,4,6,…}, the exact Schmidt rank of
|ψ_L⟩ is 2, 4, 8 at L = 4, 6, 8 respectively.*

The contiguous half-cut rank equalling D² = 4 is the generic MPS value and
is consistent with an area law along a contiguous cut. The odd/even rank is
the substantive fact: it *increases* with *L* over the computed range,
2 → 4 → 8. Since a sum of *k* product states has Schmidt rank at most *k*
across every bipartition, the odd/even Schmidt rank equals the minimal number
of product states in any decomposition across that cut; thus |ψ₈⟩ requires at
least eight such product states, and this minimal number grows over
*L* = 4, 6, 8. The computed values follow the pattern 2^{L/2−1}; we state the
three exact values as proven and record the growth as observed at
*L* = 4, 6, 8, not established for all *L*, and we make no *L*-uniform
product-state-complexity claim for the family {|ψ_L⟩}.

**Remark 3.2 (A one-sided rotated form).** The global single-site rotation
*U* with *U*X*U*⁻¹ = Z, *U*Z*U*⁻¹ = −X sends I + X ↦ I + Z = 2P₀, with
P₀ = |0⟩⟨0| = (I + Z)/2, and X + Z ↦ Z − X, so

> *U H U*⁻¹ = −2 Σᵢ₌₁ᴸ P₀^{(i)} (Z − X)ᵢ₊₁,

a one-sided facilitated ("East-type") form in which site *i*+1 is acted on
conditioned on site *i* (verified by exact conjugation; §4). This is
East-type only in the structural sense of a one-sided facilitation; it is
not the quantum East model of Pancotti, Giudice, Cirac, Garrahan and Bañuls
[PGCGB20] (whose non-thermal states become exact eigenstates only in the
large-size limit, in contrast to the exact-at-every-*L* state here), and it
carries an additional density-density term relative to the standard East
interaction. We record the reformulation as a structural observation and
draw no dynamical conclusion from it.

## 4. Verification and reproduction

Every quantitative claim is re-established from the raw data (2)–(5) by two
independent codes, shipped with the note and pinned by SHA-256 in Table 1.

*Exact-arithmetic verifier* (`reverify.py`, Python standard library only; no
third-party imports; no POSIX-only calls). It (i) forms *h* from I, X, Z and
checks it real symmetric; (ii) *solves* the linear system (6) for C⁰, C¹
exactly over ℚ, finds it consistent, recovers (5), and confirms all sixteen
residuals vanish (Lemma 2.1); (iii) builds |ψ_L⟩ from (3) and applies *H*
densely in exact integers, obtaining *H*|ψ_L⟩ = 0 and |ψ_L⟩ ≠ 0 for
*L* = 3,…,10; (iv) computes the exact Schmidt ranks of Proposition 3.1 over
ℚ; (v) confirms I, A⁰, A¹, A⁰A¹ span M₂(ℂ) (Proposition 2.3); (vi) confirms
h_{1,2}|ψ₄⟩ ≠ 0 (Remark 2.4); and (vii) confirms the rotation identity of
Remark 3.2 by exact integer conjugation. It reports `ALL CHECKS PASS`
(20/20).

*Independent cross-check* (`xcheck.py`). A from-scratch `numpy` build sharing
no code with `reverify.py`: the dense Hamiltonian is assembled directly from
Pauli matrices by Kronecker products, the amplitudes from explicit
Tr(A^{s₁} ⋯ A^{s_L}), all in `object`-dtype (arbitrary-precision integer)
arithmetic. It confirms *H*|ψ_L⟩ = 0 exactly, ‖ψ_L‖² = 4ᴸ (hence
|ψ_L⟩ ≠ 0), and *H* real symmetric, for *L* = 3,…,9. Two disjoint code paths
agree.

*The trusted base.* The all-length statement (Theorem 1.1, eigenvalue part)
rests on the finite identity (6) — sixteen integer equations — and the
elementary telescoping of Proposition 2.2; there is no numerical
extrapolation in it and no solver in its trusted base. The dense checks at
*L* = 3,…,10 are corroboration, not the proof. What must be trusted is
minimal: (i) exact-integer/rational arithmetic (CPython for `reverify.py`;
`numpy` `object`-dtype for `xcheck.py`); (ii) the shared convention, stated
in `object.json`, for reading the amplitude (3) and the operator ordering of
(4) — a consistent misconvention on both sides would not be caught by
re-checking, but the two codes fix the operator independently from Pauli
matrices; (iii) the object-level novelty of §1.4, which is a finite
literature sweep and cannot be absolute. The searcher's provenance is *not*
in the trusted base: the certificate is re-derived by an independent exact
linear solve and the eigenvalue is re-checked by two disjoint dense builds.

To reproduce on any machine with Python 3 (and, for the cross-check,
`numpy`):

```
python3 reverify.py     # stdlib only; prints ALL CHECKS PASS (20/20)
python3 xcheck.py       # independent numpy build; H@psi==0, ||psi||^2=4^L
shasum -a 256 reverify.py xcheck.py object.json   # match Table 1
```

On a platform whose hashing tool is `sha256sum` rather than `shasum`,
substitute `sha256sum reverify.py xcheck.py object.json`.

**Table 1.** SHA-256 digests of the shipped verifier, cross-check, and
machine-readable object specification. `object.json` records (2), (4), (5),
the amplitude and operator conventions, and the verified properties.

| file | SHA-256 |
|------|---------|
| `reverify.py` | `eac86c337770fc6512937f17e83fb066b01a9ee529ed12ed68f1d2faf7177ec4` |
| `xcheck.py` | `f43eb90b738f74fef71650fd1b7c78f9a7ff706f31e367fefa3843a6bbef4fc2` |
| `object.json` | `1353baa37f960332ad3b6a8013d57c92168befd18be3323b4f16309ae13076a3` |

## Acknowledgments

The matrix-product ansatz is Derrida, Evans, Hakim and Pasquier's; its
eigenstate form used here is written explicitly by Gehrmann and Essler, and
the local necessary-and-sufficient characterization that guarantees a
certificate of this shape for any injective MPS eigenstate is Garre Rubio,
Molnár, Schuch and Verstraete's. The quantum East model referenced in
Remark 3.2 is Pancotti, Giudice, Cirac, Garrahan and Bañuls's. The
computation and drafting were AI-assisted as stated in the first footnote.

## References

**[DEHP93]** B. Derrida, M. R. Evans, V. Hakim and V. Pasquier, *Exact
solution of a 1D asymmetric exclusion model using a matrix formulation*, J.
Phys. A: Math. Gen. **26** (1993), no. 7, 1493–1517.
DOI 10.1088/0305-4470/26/7/011.

**[GE26]** A. Gehrmann and F. H. L. Essler, *Exact quantum many-body scars by
a generalized matrix-product ansatz*, arXiv:2605.03020 (2026); read directly
on August 6, 2026. The eigenstate matrix-product-ansatz certificate
*h A A = E A − A E* is their Eq. (10) (general form Eq. (6)), attributed
there to [DEHP93]. Their worked models are spin-*S* chains and square-lattice
models, distinct from (1).

**[GRMSV26]** J. Garre Rubio, A. Molnár, N. Schuch and F. Verstraete, *The
local characterization of global tensor network eigenstates*,
arXiv:2603.28349 (2026); read directly on August 6, 2026. A local,
fixed-size equation — how one operator term acts on a block of tensors — is
proved necessary and sufficient for an injective MPS to be an exact
eigenstate of an extensive local operator; the worked example is the
quantum-group symmetry of the XXZ chain.

**[IM25]** A. A. Ivanov and O. I. Motrunich, *Many exact area-law scar
eigenstates in the nonintegrable PXP and related models*, arXiv:2503.16327
(2025); read directly on August 6, 2026. Exact area-law eigenstates are
constructed
inside a kinetically constrained subspace (PXP-type models), via a projector
onto a Fibonacci-constrained space; the present |ψ_L⟩ lives in the full 2ᴸ
Hilbert space with no such projector.

**[PGCGB20]** N. Pancotti, G. Giudice, J. I. Cirac, J. P. Garrahan and
M. C. Bañuls, *Quantum East model: localization, non-thermal eigenstates and
slow dynamics*, Phys. Rev. X **10** (2020), 021051; also
arXiv:1910.06616. Read directly on August 6, 2026. Its non-thermal states
become exact eigenstates in the large-size limit, in contrast to the
exact-at-every-finite-*L* state of Theorem 1.1.
