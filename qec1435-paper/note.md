# If a [[14,3,5]] stabilizer code exists, its monomial automorphism group has order 2^a 3^b 5^c: a certificate-backed exclusion of the primes 7, 11 and 13

**Daniel Kirtchakov** (independent researcher, daniel@halfounce.io)

Draft of August 5, 2026.

*This file is a faithful Markdown mirror of `note.tex` (the LaTeX source is
the authoritative version).*

MSC 2020: primary 81P73; secondary 94B05, 94B65.
Keywords: quantum error correction, stabilizer codes, additive codes over
GF(4), automorphism groups, linear programming bound, certificates.

> **Computation and authorship.** All reductions, enumerations, certificate
> designs and searches in this work were produced by **Claude Fable 5**
> (Anthropic), directed by the author, on a single Apple M4 laptop (10
> cores, 16 GB). The enumeration corpus was then re-verified adversarially
> by a separate agent instance using independently written checker code
> that shares nothing with the generating pipeline: every enumerated
> candidate of every nonzero symmetry class was re-checked, and the
> linear-programming certificate of Lemma C was replayed in exact rational
> arithmetic. This is a factual methods statement, and it is part of the
> point: the artifacts are designed so that the provenance of the *search*
> is irrelevant to the validity of the *result*. External tools used by the
> pipeline only: a C compiler for the distance checker, SymPy for one
> polynomial factorization; the closure certificates themselves replay with
> the stock Python interpreter (Section 7).

> **Status and provenance record.** The problem statement was verified
> against the primary source (codetables.de, retrieved August 5, 2026, raw
> HTML archived with the artifacts), and a novelty sweep was completed the
> same day: no published existence or nonexistence result for [[14,3,5]]
> was found beyond the CSS case of [Koh26], and no published automorphism
> restriction for it was found. A negative cannot be proved this way; we
> record the scope of the search rather than a claim.

## Abstract

Whether a [[14,3,5]] qubit stabilizer code exists is open, and this note
does not resolve it. The [[14,3]] entry of Grassl's online tables
records lower bound 4 (construction dated June 30, 2005) and upper bound
5 (page retrieved
August 5, 2026) [Gra], and Ball, Centelles and Huber pose the existence
question explicitly [BCH20]. What is proved here is a structure theorem:
if a [[14,3,5]] exists, its group of monomial automorphisms — local
Clifford x qubit permutation, equivalently monomial symplectic maps on
F_2^28 — contains no element of order divisible by 7, 11 or 13, and
therefore has order 2^a 3^b 5^c. The proof is an exhaustive,
certificate-backed elimination of every conjugacy class of monomial maps
of order 7, 11 and 13: three of the four prime classes are closed by
complete enumeration of the invariant isotropic 11-dimensional subspaces,
every candidate certified to have d ≤ 4 by an exhibited low-weight vector
(1,298,700 candidates
for the fixed-point-free order-7 class, 8,415 for order 11, none for
order 13); the fourth, order 7 with seven fixed qubits, is closed by an
exact-rational linear-programming certificate (Krawtchouk positivity:
every additive (7,2^9) code has at least 52 nonzero vectors of symplectic
weight at most 4) together with two short counting arguments. The
composite-order and locally twisted classes are enumerated as well, as
redundant confirmation. The corpus was re-verified adversarially with
independently written code, and the LP and branch certificates replay
with the stock Python interpreter.

The CSS case is settled by Koh et al. [Koh26], whose exhaustive
enumeration of CSS codes through n = 14 shows that the maximal distance
of a CSS [[14,3]] code is 4; we cite this and claim nothing there. The
open territory for [[14,3,5]] is thus genuinely non-CSS, with monomial
symmetries confined to {2,3,5}-groups. Negative search data is recorded
as boundary information, not as evidence.

## 1. Introduction

### 1.1 The problem

Let [[n,k,d]] denote a binary (GF(4)-additive) quantum stabilizer code on
n qubits with k logical qubits and minimum distance d [Got97, CRSS98].
The entry [[14,3]] of Grassl's online tables [Gra] records lower bound 4
and upper bound 5; the [[14,3,4]] construction there is dated June 30,
2005 (page last changed June 10, 2024, retrieved August 5, 2026).
Both neighbors exist: [[15,3,5]] and [[14,2,5]]
are settled constructions in the same tables, so [[14,3,5]] is exactly
the missing corner. Ball, Centelles and Huber raise its existence as
Research Problem 1 of [BCH20]. For context on nearby exhaustive work:
Bierbrauer, Fears, Marcugini and Pambianco proved [[13,5,4]] does not
exist [BFMP11]; Cross and Vandeth enumerate all general stabilizer codes
through n = 9 [CV25]; and Koh et al. enumerate all CSS codes through
n = 14 [Koh26]. On the quantum side, automorphism groups of stabilizer
codes have been studied in their own right — Hao [Hao21] proves
nonexistence results for stabilizer codes with highly transitive
automorphism groups — but that work contains nothing at length 14.

**The existence of [[14,3,5]] remains open.** This note proves a
restriction on what such a code could look like, and ships the
machine-checkable certificates behind it. It does not resolve the
question.

### 1.2 The result

Call a linear map on F_2^28 *monomial* if it is a qubit permutation
composed with an invertible local symplectic map on each qubit's
(X,Z)-plane — in operator language, a local Clifford circuit times a
qubit permutation, modulo Paulis; in GF(4) language, a monomial
semilinear map. These maps form the group M ≅ S_3 wr S_14 of order
6^14 · 14!, whose prime divisors are exactly 2, 3, 5, 7, 11, 13. A
*monomial automorphism* of a stabilizer code with stabilizer subspace
S ⊂ F_2^28 is a monomial map with g(S) = S.

**Theorem (main; Theorem 3.1 below).** No [[14,3]] stabilizer code of
minimum distance ≥ 5 admits a monomial automorphism of order 7, 11 or 13.

**Corollary.** If a [[14,3,5]] code exists, no element of its monomial
automorphism group has order divisible by 7, 11 or 13 (Cauchy's theorem
applied to a cyclic subgroup), so the group order is of the form
2^a 3^b 5^c.

Two by-products are worth stating at their own strength. First, no
[[14,3]] stabilizer code of *any* distance has a monomial automorphism of
order
13: the invariant-subspace dimension arithmetic is already empty
(Proposition 3.2). Second, every [[14,3,5]] would be a hyperplane
(index-2 subgroup) of a [[14,2,5]] code (Proposition 6.1), which turns
hyperplane sweeps of known [[14,2,5]] codes into complete searches of
their neighborhoods; the two such sweeps performed here were negative
(Section 6).

### 1.3 What is not claimed

We do not claim that [[14,3,5]] does not exist, and nothing here is
evidence either way about codes with trivial monomial symmetry, which one
expects to be the bulk of the search space. We do not claim the CSS case:
that is Koh et al.'s [Koh26], whose Table VI shows the maximal distance
of a CSS [[14,3]] code (pure or impure) is 4; our own weaker pure-CSS
observation appears only as Remark 6.2, crediting them. We do not claim
novelty for the prescribed-automorphism technique, which is classical in
coding theory (Huffman [Huf98]; see also [CRSS98]); what appears to be
new, per the dated sweep in the front matter, is its certified
application to this open entry. The very shape of the theorem — pinning
the automorphism group of a putative extremal code down to a small set
of orders by excluding primes class by class — is also classical: it is
the shape of the long program on the putative binary doubly-even
self-dual [72,36,16] code, opened by Conway and Pless in 1982 and
continued by many authors (the surviving group orders there are now 1, 3
and 5, by work of Borello and others); see Huffman [Huf98] for the early
history. The constructive searches of Section 6
are boundary data, not evidence: a rugged objective landscape says
nothing about existence. Finally, the theorem concerns *monomial*
automorphisms only; equivalences that entangle qubits are not addressed.

## 2. Setting

We use the binary symplectic picture [CRSS98, Got97]. A vector
v ∈ F_2^28 is a pair (a,b) of 14-bit words (X- and Z-parts); the
symplectic form is w(u,v) = |u_a ∧ v_b| + |u_b ∧ v_a| mod 2, and the
symplectic weight wt(v) = |a ∨ b| is the number of qubits touched. A
[[14,3]] stabilizer code is an isotropic subspace S ⊂ F_2^28 of
dimension 11; then dim S^perp = 17 and the minimum distance is

    d = min{ wt(v) : v ∈ S^perp \ S },

a minimum over 2^17 − 2^11 = 129,024 vectors. Monomial maps preserve the
form and the weight, so if g is monomial and g(S) = S' then S' is a code
with the same parameters; in particular, closing a conjugacy class of
monomial maps for one representative closes it for all.

**Lemma 2.1 (prime-order normal form).** Let g ∈ M have prime order
p ∈ {7, 11, 13}. Then g is conjugate in M to a pure qubit permutation of
cycle type (7,7) or (7,1^7) if p = 7, type (11,1^3) if p = 11, and type
(13,1) if p = 13.

*Proof.* Write g = (t_1, ..., t_14; pi) with local parts
t_i ∈ Sp(2,F_2) ≅ S_3 and pi ∈ S_14. Since S_3^14 has no element of
order p, pi ≠ 1; pi^p = 1 forces the stated cycle types. At a fixed point
i of pi, g^p = 1 gives t_i^p = 1, and gcd(p,6) = 1 forces t_i = 1. Along
a p-cycle, the p-th power acts by conjugates of the cycle product
T = t_{i_p} ... t_{i_1}, so T = 1; and a cycle with trivial product is
conjugate, by a coordinatewise gauge u_j chosen recursively along the
cycle, to the untwisted cycle. QED

So the theorem reduces to four classes of pure permutations. The
certified record (Sections 3–4) in fact closes more: all monomial classes
with a 14-cycle permutation part (orders 14, 28, 42) and all locally
twisted classes over the (7,7) cycle type (orders 14, 21, 42; no
order-28 class exists there, S_3 having no element of order 4). By
Lemma 2.1 these composite-order closures are logically redundant — a
power of any such element lands in a prime class — and we report them as
confirmation.

## 3. The enumerated classes

**Theorem 3.1.** No [[14,3]] stabilizer code with d ≥ 5 admits a monomial
automorphism of order 7, 11 or 13.

The proof occupies this section and the next. For a fixed representative
sigma, the sigma-invariant isotropic 11-dimensional subspaces are
enumerated exhaustively, and each candidate is screened by a distance
scan with early abort at weight ≤ 4: the scan certifies d ≤ 4 by
exhibiting a weight-≤ 4 vector of S^perp \ S, and any survivor would
have received its exact distance by full enumeration of S^perp \ S
(129,024 vectors). No candidate survived. Table 1 is the complete
certified record; every nonempty row traces to a file hashed in
Section 7 (the empty `c13` class leaves no output file; its emptiness
replays via `gen_generic.py c13`).

**Table 1.** The certified class closures: 1,314,223 distinct enumerated
candidates (1,315,483 distance checks in all, the `swapshift` re-run of
the cyclic class contributing a further 1,260), each certified d ≤ 4 by
the early-abort scan described above,
none reaching d = 5. Twists over (7,7) are classified by the pair of
cycle products in S_3 up to simultaneous conjugacy and block swap (s, s'
involutions in different positions); over a 14-cycle, by the single cycle
product.

| class (representative sigma)                        | order | candidates | outcome       |
|-----------------------------------------------------|-------|-----------:|---------------|
| 14-cycle, untwisted (`cyclic`; `swapshift` re-run)  | 14    | 1,260      | all d ≤ 4     |
| 14-cycle, involution twist (`shift28`)              | 28    | 4          | all d ≤ 4     |
| 14-cycle, order-3 twist (`s3shift`, `s3shift2`)     | 42    | 0          | class empty   |
| (7,7), twist (1,1) (`qc7`, jobs `dp0`–`dp3`)        | 7     | 1,298,700  | all d ≤ 4     |
| (7,7), twist (1,s) (`qc7_1swap`)                    | 14    | 4,764      | all d ≤ 4     |
| (7,7), twist (s,s) (`qc7swap`)                      | 14    | 540        | all d ≤ 4     |
| (7,7), twist (s,s') (`qc7_swap_s2`)                 | 14    | 540        | all d ≤ 4     |
| (7,7), twists with an order-3 part (4 classes)      | 21,42 | 0          | classes empty |
| 11-cycle + 3 fixed (`c11`)                          | 11    | 8,415      | all d ≤ 4     |
| 13-cycle + 1 fixed (`c13`)                          | 13    | 0          | class empty   |
| 7-cycle + 7 fixed                                   | 7     | —          | Section 4     |

### 3.1 Enumeration method

Each representative sigma is an explicit linear map on F_2^28 preserving
the symplectic form. The invariant subspaces are enumerated through the
primary (Fitting) decomposition of F_2^28 as an F_2[sigma]-module — the
classical prescribed-automorphism method [Huf98] — with complete
submodule enumeration per primary component and isotropy imposed through
the pairing of components (the reciprocal pairing swaps the two degree-3
factors of x^7 + 1, so only cross-orthogonality constraints survive
there). Two structural examples:

*Cyclic.* For the qubit 14-cycle,
x^14 + 1 = ((x+1)(x^3+x+1)(x^3+x^2+1))^2 over F_2; the invariant
isotropic 11-dimensional subspaces number exactly 1,260 (7 isotropic
choices in the (x+1)-component times 180 orthogonal pairs in the two
cubic components).

*QC-7.* For two disjoint 7-cycles, x^7 + 1 = (x+1)pq is squarefree with
p, q cubic; an invariant subspace is U_0 ⊕ U_p ⊕ U_q with U_0 a
Lagrangian plane in the 4-dimensional fixed component (15 choices) and
(U_p, U_q) an orthogonal pair of K-subspaces, K = F_8
(585 + 42,705 + 42,705 + 585 = 86,580 pairs), for
15 x 86,580 = 1,298,700 candidates.

Every emitted candidate is re-checked for rank 11 and isotropy before its
distance is computed ("0 bad" in every batch log). The batch screener
also has a positive control: run with generator count 12 on the reference
[[14,2,5]] matrix, it flags the code as a d ≥ 5 hit. (The control is a
separate `batch 12` run — a 12-generator matrix cannot ride the
11-generator stream, where it would be counted "bad" — and its console
output was not archived; it replays in seconds.)

### 3.2 Order 13

**Proposition 3.2.** No [[14,3]] stabilizer code, of any distance, has a
monomial automorphism of order 13.

*Proof.* By Lemma 2.1 the automorphism may be taken to be a pure
permutation sigma: a 13-cycle plus a fixed qubit. Then the trivial
F_2[sigma]-component of F_2^28 has dimension 4 and Phi_13 is irreducible
of degree 12 over F_2 (the order of 2 mod 13 is 12), so any invariant
subspace has dimension d_0 + 12m with d_0 ≤ 4. No such value equals 11.
The generic enumerator confirms: zero invariant 11-dimensional subspaces
(Table 1). QED

The order-11 class is not empty — the Phi_11-part is a line over
F_{2^10}, giving 33 isotropic lines x 255 choices of fixed-component part
= 8,415 candidates — and all 8,415 fail. By Lemma 2.1, orders 11 and 13
are thereby fully monomially closed.

## 4. Order 7 with fixed qubits

Let sigma be the permutation acting as a 7-cycle on qubits 0..6 and
fixing qubits 7..13, and suppose S is a sigma-invariant [[14,3,5]]
stabilizer subspace. Decompose S = U_0 ⊕ U_p ⊕ U_q as above, now with
the trivial component of F_2^28 of dimension 16 (the 14 fixed-qubit
coordinates plus the two block averages), a symplectic space. Write
d_0 = dim U_0; then d_0 + 3(d_p + d_q) = 11, so d_0 ∈ {2, 5, 8, 11}.
Each branch is impossible:

**Lemma 4.1 (d_0 = 11).** U_0 would be an isotropic subspace of dimension
11 in a 16-dimensional symplectic space, whose maximal isotropic
dimension is 8.

**Lemma 4.2 (LP certificate; `lemmaC_certificate.py`).** Every additive
(7, 2^9) code over GF(4) — equivalently, every 9-dimensional
F_2-subspace of the 14-dimensional symplectic space of 7 qubits — has at
least 52 nonzero vectors of symplectic weight at most 4.

*Proof.* Delsarte-style linear programming [Del73] with the quaternary
Krawtchouk polynomials K_j and the MacWilliams nonnegativity of the
trace-dual weight distribution of an additive GF(4) code [CRSS98]. With
mu = 5/32 and lambda = (0, 27/256, 0, 0, 0, 1/256, 0, 1/384) ≥ 0, one
checks exactly that e(w) := [w ≤ 4] − mu − sum_j lambda_j K_j(w) ≥ 0 for
w = 1, ..., 7, whence for any (7, 2^9) additive code,
A_1 + ... + A_4 ≥ 511 mu − sum_j lambda_j K_j(0) = 52. The shipped
certificate performs every step in exact rational arithmetic (Python
`fractions`); it was re-verified independently. (An empirical floor of
104 over 2,000 random subspaces suggests the constant is not tight;
harmless.) QED

*Closure of d_0 ∈ {2, 5}.* Let V_fix ≅ F_2^14 be the span of the
fixed-qubit coordinates and let W = {f ∈ V_fix : f ⊥_w U_0}. Since V_fix
is symplectically orthogonal to the block components and to the
block-average plane, W ⊆ S^perp, and dim W ≥ 14 − d_0 ≥ 9. Moreover
W ∩ S = U_0 ∩ V_fix has at most 2^{d_0} − 1 ≤ 31 nonzero vectors, and
every vector of W \ S lies in S^perp \ S, hence has weight ≥ 5. But W
contains a 9-dimensional subspace supported on 7 qubits, which by
Lemma 4.2 has at least 52 nonzero vectors of weight ≤ 4: contradiction.

*Closure of d_0 = 8.* Here d_p + d_q = 1; by the p <-> q relabeling
symmetry take (d_p, d_q) = (1, 0). The block-supported subspace
M = V_p ⊕ (U_p^perp ∩ V_q) has dimension 9 and lies in S^perp; its
weight-≤ 4 vectors must lie in the block-only part of S, contained in a
subspace B_S of dimension ≤ 5 (at most 31 nonzero vectors). Direct
enumeration over all 9 possible K-lines U_p counts 112–140 nonzero
weight-≤ 4 vectors in M (`order7fixed_full.txt`): contradiction. (M is
itself 9-dimensional on 7 qubits, so Lemma 4.2 independently forces
≥ 52: the branch dies twice.)

*Proof of Theorem 3.1.* By Lemma 2.1 it suffices to treat pure
permutations of the four cycle types. Types (7,7), (11,1^3) and (13,1)
are closed by the exhaustive enumerations of Table 1; type (7,1^7) by
Lemmas 4.1 and 4.2 with the branch arguments above. The composite-order
rows of Table 1 are consistent redundant confirmation. QED

## 5. Verification

The corpus is guarded at four levels.

*Controls.* The C distance checker reproduces d = 4 on the codetables
[[14,3,4]] matrix and d = 5 on the codetables [[14,2,5]] matrix before
any enumeration is trusted; batch mode carries the positive control
described in Section 3.

*Independent verifier.* A standard-library-only Python verifier, written
separately, sharing no code with the search tools and using a different
algorithm (explicit construction of the full 2^11-element group and
2^17-element normalizer), agrees with the C checker on the codetables
[[14,3,4]] reference code (both find d = 4; the verifier reports FAIL by
design, since 4 < 5) and on a random sample of 8 enumerated cyclic
candidates, with exact distance agreement in all cases. (The verifier
accepts only 11-generator [[14,3]] inputs, so the 12-generator
[[14,2,5]] reference is outside its scope; the sample's console output
was not archived.)

*Structural cross-checks.* The cyclic class was enumerated by two
structurally different programs (CRT-idempotent construction; generic
kernel-of-matrix method): identical count (1,260) and identical component
submodule statistics. The QC-7 class likewise: the specialized
Grassmannian generator emits exactly 1,298,700 candidates, the generic
tool independently reproduces that count (a count-only cross-check:
candidates constructed and isotropy-checked, not re-distance-checked),
and the orthogonal-pair counts match the Gaussian-binomial
predictions over F_8 exactly (585 x 73 = 42,705; 4,745 x 9 = 42,705).

*Adversarial re-verification.* After the corpus was frozen, a separate
agent instance with independently written checker code re-ran the
verification: every enumerated candidate of every nonzero symmetry class
in Table 1 was re-checked, and Lemma 4.2 was replayed in exact rational
arithmetic. The re-verification confirmed every closure and also
confirmed that the hyperplane and truncation sweeps of Section 6 are
complete as stated.

## 6. Boundary data, and the CSS case

Nothing in this section is evidence about existence; it is recorded so
that the next attempt does not repeat it.

**Proposition 6.1.** If S is a [[14,3,5]] stabilizer subspace, then for
every logical l ∈ S^perp \ S, the subspace T = S + <l> is a
[[14,2,≥5]] stabilizer subspace. Hence every [[14,3,5]] is a hyperplane
(index-2 subgroup) of some [[14,2,5]].

*Proof.* T is isotropic of dimension 12 since l ∈ S^perp, and
T^perp \ T ⊆ S^perp \ S, so the minimum weight can only go up; the
tables' upper bound d ≤ 5 at [[14,2]] [Gra] then pins d(T) = 5. QED

*Hyperplane sweeps.* All 4,095 hyperplanes of the codetables [[14,2,5]]
have d ≤ 4; the same holds for all 4,095 hyperplanes of a second
[[14,2,5]] found here by transvection annealing (seed 44; stabilizer in
`data/seed_1425_anneal44.txt`, verified d = 5). So neither known
[[14,2,5]] sits over a [[14,3,5]].

*Truncations.* All 45 rank-preserving single-qubit truncations of the
codetables [[15,3,5]] give d < 5.

*Walks and annealing.* A d ≥ 5-preserving random walk on the [[14,2,5]]
manifold scores each visited code by its minimum, over nonzero syndromes,
of the number of weight-≤ 4 Pauli errors mapping to that syndrome; the
value 0 anywhere would yield a candidate [[14,3,5]], which an exact
re-check would then settle. From the codetables seed, a 15,000,000-step
run (seed 101;
4,039,818 accepted states) drove this coverage from 13 to 5 within the
first 251,000 steps and never below 5 thereafter; a second seed's runner
died early (step ≈ 48,000 of the planned 15,000,000) and its partial log
is retained.
Random-start transvection annealing on the [[14,3]] objective floors at
a single residual weight-4 dual-coset vector at best (restarts typically
stall at 1–4). Evidence of a rugged landscape
and of a coverage floor on the explored component, not of nonexistence.

**Remark 6.2 (the CSS case is Koh et al.'s).** Koh, Gong, Diaconu, Tan,
Geim, Gullans, Yao, Lukin and Majidy [Koh26] exhaustively enumerate all
CSS codes up to n = 14 (2.71 x 10^10 inequivalent codes) with exact
distances valid for impure codes; their Table VI at (n,k) = (14,3) lists
no d ≥ 5 row and exactly two codes of distance 4. Hence no CSS
[[14,3,5]] exists, pure or impure, and (distances being invariant under
local Cliffords) neither does any local-Clifford image of a CSS code with
these parameters. This settles the entire CSS branch of the question by
citation, and it subsumes the only CSS statement we had derived
independently — that a *pure* CSS [[14,3,5]] is impossible because the
best [14,7]_2 distance is exactly 4 while d(C_1) ≥ 5 and
d(C_2^perp) ≥ 5 would force dim C_1 ≤ 6 and dim C_1 ≥ 11 [Gra]. That
two-line argument survives only as an independent hand proof of two rows
of their computed table; the result is theirs. Their catalogue is
CSS-only; the open territory for [[14,3,5]] is therefore
genuinely non-CSS.

**Remark 6.3 (partial results toward orders 2, 3, 5).** Outside the
adversarially re-verified perimeter of Theorem 3.1, the working record
contains a partial closure of the order-5 classes by the same machinery:
all order-5 monomial elements reduce to pure permutations of cycle type
(5,1^9) or (5,5,1^4); the invariant dimensions satisfy d_0 + 4e = 11;
the branches (d_0,e) = (11,0) and (3,2) are impossible — (11,0) by a
weight-2 vector surviving in the field component, (3,2) for the
one-5-cycle type via a second exact-rational LP certificate
(`lemmaD_certificate.py`: every additive (9, 2^15) code has at least
1,471 nonzero vectors of weight ≤ 4) and for the two-5-cycle type by a
fixed-space dimension count — leaving only (d_0,e) = (7,1) open. We
record this as work in progress with its certificate, not as part of the
theorem.

## 7. Artifacts and replay

The artifacts sit in `solve/problem-3/` beside the working notes:
generators `gen_cyclic.py`, `gen_qc7.py`, `gen_c11.py`, `gen_generic.py`;
the distance checker `check1435.c` (single C file: exact check, batch
screening, annealing, walks); the independent verifier `verify_1435.py`;
`gen_hyper.py`, `truncate15.py`, `order7fixed_branches.py`; reference
matrices in `data/` (retrieved from [Gra] on August 5, 2026); and the
run outputs behind Table 1 and Section 4 in `certificates/`. (The
hyperplane and truncation sweeps of Section 6 were confirmed in the
adversarial re-verification, but their console outputs were not
archived; the empty `c13` class leaves no output file. The directory
also retains `sample_c7fixed.py`, the defective sampler disclosed in the
Acknowledgments, unhashed; nothing depends on it.) The differentiator is deliberate and worth
one plain sentence: the closure certificates — both LP lemmas, the branch
enumeration, and the independent distance verifier — replay with the
stock Python interpreter and nothing else; no package, no solver, no
proof assistant. To replay:

```
cd solve/problem-3
python3 certificates/lemmaC_certificate.py   # Lemma C, exact rationals
python3 certificates/lemmaD_certificate.py   # Lemma D, exact rationals
python3 order7fixed_branches.py              # d0 = 8 branch counts
python3 verify_1435.py data/ct_14_3_stab.txt # control: d=4, "FAIL" by design
cc -O2 -o check1435 check1435.c              # distance checker
python3 gen_cyclic.py | ./check1435 batch 11         # 1,260 cand., 0 hits
python3 gen_qc7.py 1  | ./check1435 batch 11         # QC-7 slice dp=1
python3 gen_c11.py    | ./check1435 batch 11         # 8,415 cand., 0 hits
python3 gen_generic.py shift28 | ./check1435 batch 11  # needs sympy
```

The four `gen_qc7.py` slices (0..3) total 1,298,700 candidates;
`gen_generic.py` (the only script with a dependency: SymPy, for one
factorization) accepts every twisted class name of Table 1. Expected
terminal lines are the `SUMMARY candidates=... hits=0 bad=0` records
reproduced in the certificate files; acceptance is by the `SUMMARY` line
itself — `candidates` equal to the class count, `hits=0`, `bad=0` — not
by exit status (`batch` exits 0 even when `bad>0`). Two expected
oddities of a verbatim replay: the independent verifier exits 1 on its
control by design (it reports the exact distance 4, then `FAIL: distance
4 < 5`); and the second section of `order7fixed_branches.py` is a
superseded block-test attack on the d_0 = 5 branch, retained for the
record — its closing line "branch NOT closed by this test" is expected,
that branch being closed by Lemma 4.2. SHA-256 hashes of every file in
`certificates/` (repeated hashes are genuinely identical outputs of
independent runs):

```
10bdfe41bb4bc1b2d46e3649d6952fdc8da17c2631cad08e889164ef736488cc  anneal2_s11.out
029aae2eb7cb54809488669f4198b56bfc7796743089b8f49bdb2efffa7db6d4  anneal2_s22.out
7b235c01f0c8a68a17f2478b7745c11913300ea999a913b21d10d14dd4ae4098  anneal2_s33.out
71780fe55a5f3e50927cf3efe4bff13f76c88c55f62620ce5d5a1d50b51ce9bc  anneal2_s44.out
3a49de35dc9175e0b0efe66e593da006d1a83d3764255bc13a96d4ae2d7744ac  anneal_s55.out
d99197bb63d8acfc926c687e05688fdfa012842a91692cc1018b8d8d9fbdd407  c11_result.txt
c4c4abab60c19de617c980c132013cd289ca2933b34e5b1d197dec757c3112bc  cyclic_candidates_1260.txt
517cce87f8c4a3642afe82e8be4196fa4628734a6a8ed0c2e08ee3ff1c715f62  cyclic_result.txt
c0305d1a9307bb8b6ae7d9328c6ea5b62498125e0098a9dfa1217c3c55705e46  lemmaC_certificate.py
7ef4f10dbf47e132957814bc16fd10f71775e64f5e383fad6e98f682036c1492  lemmaD_certificate.py
f3fe027b7fe84f59d70b9fa0e21b11ca667b75d2913011bc1aed9d3c8b4e0d17  order7fixed_full.txt
b81a7565ac6b6be87616917c1ded8f80221efde2b517d03d5e02532cab14c982  order7fixed_summary.txt
abc5f982aff4ce5e7f6aef7548daf2eb6610eda19142b821ec3ffbc96c353b12  qc7_1rho.log
dda0a0d23bf6df85f929a070415f1aedeafc7bbc4af73238554ef69310a7427b  qc7_1rho_result.txt
b7b7ab2b92e8870be0cd184b21aa9b89727cc5f62c7304b3cfc382a29aaf4ca5  qc7_1swap.log
8257c009248694646c5a81daa77fb3bb474316f9b466339b49e240e389626932  qc7_1swap_result.txt
58b70180f2e45b8d55c42218f4f11dd57e38211064c3019d7f2f3534e1447445  qc7_dp0.log
b3220909a34b785cb058e62610a7a9538dd7cb7b8b30b5e4cb9ca3c27d0fbd05  qc7_dp0.out
a11bea4de8c1ff90a25f2844f92158bd135ac935a7dba32acad7d83dd2011d1f  qc7_dp1.log
7e5fc32bb0d4f480fc2d111eb8910d8b204963c7cb7409177100e11a151355ab  qc7_dp1.out
b95ee11c013c340554e6a9791f3b842ffde2bb77b0f9d99a1c373e6e5e43f814  qc7_dp2.log
7e5fc32bb0d4f480fc2d111eb8910d8b204963c7cb7409177100e11a151355ab  qc7_dp2.out
043be1db5d5de02a7d4f2ac12306010a5b8b8ba23229b8223030d9404419bae1  qc7_dp3.log
b3220909a34b785cb058e62610a7a9538dd7cb7b8b30b5e4cb9ca3c27d0fbd05  qc7_dp3.out
393a15714494f641badc0778b4abffa00f1739b6b97f4d077ea52f0601640ca0  qc7_rho_rho2.log
dda0a0d23bf6df85f929a070415f1aedeafc7bbc4af73238554ef69310a7427b  qc7_rho_rho2_result.txt
eded10efb983e8f44a324d731f08b310df7c4f3310a4fc962e7f6f285d9dddac  qc7_swap_rho.log
dda0a0d23bf6df85f929a070415f1aedeafc7bbc4af73238554ef69310a7427b  qc7_swap_rho_result.txt
051d452751f6acb4dc50b496fb919eb3e2f843e1a52fd20f955ab503cef657ed  qc7_swap_s2.log
3feeaba0ed1dc6615dc8a234aaff3ad090582e644a9f6ae2a5de832a2b89bd8b  qc7_swap_s2_result.txt
1fe84310ee3ca4fbd289f1714c72bdb9d3041d0963e553d36fdec4615759d96e  qc7_xcheck.out
c133da9f6f78dcb64204ff6d5f001059521df14a1079d9655f130f7077180c3a  qc7s3.log
dda0a0d23bf6df85f929a070415f1aedeafc7bbc4af73238554ef69310a7427b  qc7s3_result.txt
aae109906f4f8efa3535a441ee67e08823a6bd7cd12c1b1270cac54dad853e97  qc7swap.log
3feeaba0ed1dc6615dc8a234aaff3ad090582e644a9f6ae2a5de832a2b89bd8b  qc7swap_result.txt
263c7234e893f016bd33ead2a8354b575575c15bb2f75872baf74114bdefc4ed  s3shift2.log
dda0a0d23bf6df85f929a070415f1aedeafc7bbc4af73238554ef69310a7427b  s3shift2_result.txt
316b8bd39998c6851ee4819c5a5ad45d5f8fb722d697290c1552daebbc24ee9e  s3shift_result.txt
93a7314da75f297284e912578c594bb14dbfc6182479aaa683ae087714ad0675  shift28.log
86a4b81844ebc832577ee7221ff8cc2b9ba2a40f8383c1096871974a985995ac  shift28_result.txt
2ac2e1ed208e3d7f29f39059f070681d4d637d911fbc589e7ed0a0a05e7dcf61  swapshift_result.txt
3fe92f126b0808dbf02a6fb5f45381d224f9f998d8251dbd1fd84d77a8358dcf  walk2_s101.out
71a58ebd0c85a2416713da85b7747581ed56cb515b371887682a3bd111cffe15  walk2_s202.out
```

and of the tools and reference data they replay against:

```
95599be7a1ea8f22b13328fef3c9c9e8fb489ef78e1c7d535007db6b736119d5  check1435.c
2527266d13b604029120ed11174730ef1ed3fe6d5405d8fe3f82c21668ae0d3c  verify_1435.py
77ee81af746879b8b56c3e1e259b26fd07c0ccb9be187871a61b08ee3e0762d8  gen_cyclic.py
9e9b4ecd954c848acf841fc1a227f911a2497ee81c7988853545105f9c5c87b7  gen_qc7.py
6713b83cdc18d5fc47e000530953180044658a402728d235cf566d26def50dd7  gen_c11.py
266ed6d4358bf1571de621e0819f4d46fba56d14015524a1e79239a7c9e4903e  gen_generic.py
23f4b2ccc019ec1ca5895f980a4687ee7a93cd35e9b4799c48cd0b97cf214674  gen_hyper.py
3782bda28af7426292f7409ba1971288ed788bbe02882debd7e5ff60fde88f6a  truncate15.py
e6f94ea565cda966bb02a70f919e54e67b4c83081e11feefd11d8aa7b765977d  order7fixed_branches.py
7668dcc98ef70aafb215c908728e19e177107879f683b4ff0b19a0ab104d0ee3  data/ct_14_3_stab.txt
80fc7aef58469c67d52faa3f73562041b051905284118f9404a0059102330505  data/ct_14_2_stab.txt
53c055242bdb7a77bf3c31884927464d89a49a132913a80ce209d887e0e8f7b1  data/ct_15_3_stab.txt
e6fce037fc1f0f3b8535ae30076678ee7c2359d22b5aff16ca402834dc013489  data/seed_1425_anneal44.txt
```

## Acknowledgments

The problem is Grassl's tables' and Ball, Centelles and Huber's: the
[[14,3]] entry [Gra] poses the question silently (its [[14,3,4]]
construction is dated June 30, 2005),
and [BCH20] posed it in print. The debt to Koh, Gong, Diaconu, Tan, Geim,
Gullans, Yao, Lukin and Majidy [Koh26] is recorded in Remark 6.2: their
enumeration closes the entire CSS branch and subsumes the one CSS
statement we had derived ourselves. The prescribed-automorphism method is
classical and Huffman's account [Huf98] is the one we followed; the
GF(4)/symplectic framework and the additive MacWilliams identities
underlying Lemma 4.2 are Calderbank, Rains, Shor and Sloane's [CRSS98],
and the linear programming method is Delsarte's [Del73]. All computations
were carried out with Claude Fable 5 (Anthropic), directed by the author.
One sampling-based falsification run present in an earlier working draft
was removed after the adversarial re-verification found its sampler
defective; the certified enumerations above do not depend on it.

## References

- [BCH20] S. Ball, A. Centelles and F. Huber, *Quantum error-correcting
  codes and their geometries*, Ann. Inst. Henri Poincaré D, Comb. Phys.
  Interact. 10 (2023), 337; arXiv:2007.05992, 2020. The existence of
  [[14,3,5]] is Research Problem 1 in both versions.
- [BFMP11] J. Bierbrauer, R. Fears, S. Marcugini and F. Pambianco, *The
  nonexistence of a [[13,5,4]]-quantum stabilizer code*, IEEE Trans.
  Inform. Theory 57 (2011), no. 7, 4788–4793. Earlier version:
  arXiv:0908.1348 (J. Bierbrauer, S. Marcugini and F. Pambianco, 2009).
- [CRSS98] A. R. Calderbank, E. M. Rains, P. W. Shor and N. J. A. Sloane,
  *Quantum error correction via codes over GF(4)*, IEEE Trans. Inform.
  Theory 44 (1998), 1369–1387.
- [CV25] A. W. Cross and D. Vandeth, *Small binary stabilizer subsystem
  codes*, arXiv:2501.17447, 2025. Exhaustive enumeration of general
  stabilizer codes (and subsystem codes) through n = 9.
- [Del73] P. Delsarte, *An algebraic approach to the association schemes
  of coding theory*, Philips Res. Rep. Suppl. 10 (1973).
- [Got97] D. Gottesman, *Stabilizer codes and quantum error correction*,
  Ph.D. thesis, California Institute of Technology, 1997;
  arXiv:quant-ph/9705052.
- [Gra] M. Grassl, *Bounds on the minimum distance of linear codes and
  quantum codes*, online tables at http://www.codetables.de. Entries
  retrieved August 5, 2026: [[14,3]] (lower bound 4, construction dated
  June 30, 2005; upper bound 5; page last changed June 10, 2024);
  [[15,3,5]]; [[14,2,5]]; and the classical entry [14,7]_2 (best
  distance 4) cited in Remark 6.2.
- [Hao21] H. Hao, *Investigations on automorphism groups of quantum
  stabilizer codes*, arXiv:2109.12735, 2021.
- [Huf98] W. C. Huffman, *Codes and groups*, in: Handbook of Coding
  Theory (V. S. Pless and W. C. Huffman, eds.), vol. II, North-Holland,
  1998, 1345–1440.
- [Koh26] J. M. Koh, A. Gong, A. C. Diaconu, D. B. Tan, A. A. Geim,
  M. J. Gullans, N. Y. Yao, M. D. Lukin and S. Majidy, *Entangling
  logical qubits without physical operations*, arXiv:2601.20927,
  January 28, 2026. Exhaustive enumeration of all CSS codes up to
  n = 14; Table VI at (n,k) = (14,3): two codes of distance 4, none
  higher.
