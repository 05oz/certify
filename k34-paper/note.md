# An Erdős–Rado oriented Ramsey number determined: k(3,4) = r(I₃,L₄) = 21, by explicit witness and certified exhaustion

**Daniel Kirtchakov**
Independent researcher (`05oz`); no institutional affiliation — daniel@halfounce.io — halfounce.io — ORCID [0009-0009-5213-4098](https://orcid.org/0009-0009-5213-4098)

*Draft of August 11, 2026.*

> **Computation and authorship.** All encodings, decompositions, searches,
> verifiers, and audits in this work were produced by **Claude**
> (Anthropic), directed by the author, on a single Apple M4 laptop. The
> independent proof checker imports only the Python standard library and
> shares no code with the solving pipeline; the adversarial referee of
> §4.2 was a separate agent instance given no access to the pipeline's
> code and wrote its own code throughout, including its own LRAT checker.
> This is a factual methods statement, and it is part of the point of the
> note: the artifacts are designed so that the provenance of the *search*
> is irrelevant to the validity of the *result*. External tools used by
> the pipeline: CaDiCaL 3.0.1 (`--lrat`) and Python 3.

> **Prior-art record.** The primary source [IRW21] was read in full on
> August 5, 2026 (arXiv v3; a copy is archived in the author's working tree, not
> redistributed here, and
> section references follow its numbering). The Erdős problems entry
> [Blo] was fetched live on August 5 and again on August 11, 2026
> (including once more immediately before this draft was written): status
> OPEN, zero comments, zero claimed proofs, no exact value of any k(n,m)
> recorded. An arXiv sweep of the same dates found no paper on r(I_m,L_n)
> other than [IRW21], whose single recorded citation is off-target. The
> line has been dormant since 2020/2021.

*2020 MSC: Primary 05C55; Secondary 05C20, 05D10, 68V15. Keywords:
oriented graph, Ramsey number, transitive tournament, independent set,
Erdős problem, SAT, cube-and-conquer, LRAT, certified computation.*

---

## Abstract

Let k(n,m) be the least N such that every directed graph on N vertices
contains an independent set of size n or a transitive tournament on m
vertices. Determining k(n,m) is a problem of Erdős and Rado (1967), #112
in the Erdős problems collection; it coincides with the oriented-graph
Ramsey number r(Iₙ,Lₘ) studied by Bermond and by Ihringer,
Rajendraprasad, and Weinert (IRW). Beyond the classical tournament
column k(2,m), the known exact values were k(3,3) = 9 (Bermond 1974) and
k(4,3) = 15, k(5,3) = 23 (IRW 2021); for k(3,4), the case IRW single out
as the next feasible one, the published bounds were 9 ≤ k(3,4) ≤ 25. We
determine **k(3,4) = r(I₃,L₄) = 21**.

The lower bound is an explicit oriented graph on 20 vertices, printed in
full in §2 and checkable in milliseconds. The upper bound is an
exhaustion of the 21-vertex case: a neighbourhood decomposition splits
it into 346 propositional instances; CaDiCaL refuted every instance with
an LRAT certificate, and every certificate was replayed by an
independently written standard-library checker. Completeness of the
decomposition was audited at content level: complete block inventories
(three independent enumerations), a base encoding with no symmetry
breaking whose models are exactly the {I₃,TT₄}-free oriented graphs
(brute-forced at small orders), and a one-to-one clause-multiset match
of the 346 instance files against the decomposition re-derived from the
definitions. With logically redundant confirming exhaustions at
N = 22, 23, 24, the corpus is 445 certificates and just over 10⁹ checked
proof steps; certificates regenerate bit-for-bit from the recorded
solver commands (11 of 11 attempts). Every component was then confirmed by
an adversarial referee writing fresh code throughout. From the same
campaign: 29 ≤ k(6,3) ≤ 33, the lower bound new, by an explicit Cayley
witness on 28 vertices; the upper bound is IRW's. We close with the
questions the computation opens: the structure and possible uniqueness
of the 20-vertex extremal graph, the k(6,3) gap, the feasibility of
k(4,4) (the new value gives k(4,4) ≤ 50), and what a human-readable
proof would require.

## 1. Introduction

### 1.1. The question

An *oriented graph* is a loopless directed graph with at most one arc
between any two vertices; a *tournament* is an oriented graph in which
every pair is adjacent; a tournament is *transitive* when its arc
relation is a linear order. Write Iₙ for the independent set on n
vertices and Lₘ (equivalently TTₘ) for the transitive tournament on m
vertices. Following [IRW21], r(Iₙ,Lₘ) is the least N such that every
oriented graph on N vertices contains an independent set of size n or a
transitive tournament on m vertices (for tournaments, subdigraph and
induced-subdigraph containment coincide).

Erdős and Rado [ErRa67] asked for the same quantity over directed
graphs: let k(n,m) be minimal such that any directed graph on k(n,m)
vertices contains an independent set of size n or a transitive
tournament of size m. The two functions are equal (Remark 1.3), and
determining k(n,m) is #112 in the Erdős problems collection [Blo],
recorded there as open. That entry records the following. Erdős and Rado
proved k(n,m) ≪ₘ n^(m−1), with
the explicit bound k(n,m) ≤ (2^(m−1)(n−1)^m + n − 2)/(2n − 3); Larson
and Mitchell [LaMi97] sharpened the dependence on m, in particular to
k(n,3) ≤ n² — a bound also stated as [IRW21, Lemma 2.4], where it is
attributed to [LaMi97]; and Z. Hunter observed
R(n,m) ≤ k(n,m) ≤ R(n,m,m), hence k(n,m) ≤ 3^(n+2m).

The exact values previously known form two families. The tournament
column is classical: k(2,3) = 4, k(2,4) = 8, k(2,5) = 14, k(2,6) = 28
(see [IRW21] and the references there). In the third-column direction,
Bermond [Ber74] proved k(3,3) = 9; the extremal graph on 8 vertices is
unique up to isomorphism by [IRW21, Lemma 3.1], which also gives its
description as the circulant on ℤ₈ with connection set {1,6}. Ihringer,
Rajendraprasad, and Weinert [IRW21] proved k(4,3) = 15 and k(5,3) = 23,
gave the general bound k(m,3) ≤ m² − m + 3, and — combining their upper
bound with Kim's lower bound for r(Iₘ,K₃) — determined the order of
growth k(m,3) = Θ(m²/log m). For k(3,4) — the case [IRW21] single out
in closing as the next one within reach — the record stood at

  9 ≤ k(3,4) ≤ 25,

the lower bound by monotonicity from k(3,3) = 9, the upper bound from
the recursion of [IRW21, Lemma 2.3],
r(I₃,L₄) ≤ 2 r(I₃,L₃) + r(I₂,L₄) − 1 = 25; the same value 25 is what
[IRW21, Proposition 6.1], the small-parameter formula the authors
describe as the state of the art for small m and n, returns at
(m,n) = (3,4).

### 1.2. Result

**Theorem 1.1.** *k(3,4) = r(I₃,L₄) = 21. That is: every directed graph
— equivalently, every oriented graph — on 21 vertices contains an
independent set of size 3 or a transitive tournament on 4 vertices, and
there is an explicit oriented graph on 20 vertices, exhibited in §2,
containing neither.*

This determines the first previously unknown value in the k(3,m) column
of Erdős Problem #112. The proof is machine-checkable end to end. The
lower bound is the explicit witness of §2. The upper bound is an
exhaustive case decomposition of the 21-vertex problem into 346
propositional instances (§3), each refuted by CaDiCaL 3.0.1 [BFF+24]
with an LRAT certificate [CFHKS17], in the spirit of cube-and-conquer
[HKWB11] and of the certified exhaustions of [HKM16]; the completeness
of the decomposition — that the 346 cases cover everything, with no
symmetry breaking hidden in the encoding — was itself audited at
content level (§4). Every certificate was verified by an independently
written checker, and twelve of them by a second, unrelated one; the
whole was confirmed by a final adversarial referee (§4.2).

Two secondary results from the same campaign are recorded at exact
strength. The certified exhaustions at N = 22, 23 (and a structured
instance at N = 24) are
logically redundant given Theorem 1.1 but stand as independent
confirmations (§5.1). And:

**Proposition 1.2.** *29 ≤ k(6,3) ≤ 33. The lower bound is new, by the
explicit 28-vertex witness Cay(ℤ₂₈, {3,8,10,12,17}); the upper bound is
m² − m + 3 at m = 6, due to [IRW21].*

k(6,3) remains open, and nothing stronger about it is claimed here.

**Remark 1.3** (Directed versus oriented graphs). Erdős Problem #112 is
phrased for directed graphs, which may carry 2-cycles; the computation
here is over oriented graphs. The two Ramsey functions coincide. Every
oriented graph is a directed graph, so k(n,m) ≥ r(Iₙ,Lₘ). Conversely, a
directed graph avoiding both patterns yields an oriented one on the same
vertex set: delete one arc of each 2-cycle. Deletion preserves adjacency
and non-adjacency of every pair — hence preserves every independent set
— and only removes transitive subtournaments; so k(n,m) ≤ r(Iₙ,Lₘ). The
extremal orders are equal, and the value 21 answers the problem as
posed.

### 1.3. What is not claimed

We do not claim to resolve Erdős Problem #112. The problem asks for
k(n,m) as a function of two parameters and is not settled by any finite
computation; a single new entry in its table leaves it open. We do not
claim a human-readable proof of the upper bound: what a
skeptic must believe and can replay is stated in §7; what a human proof
would require, in §8. We do not claim uniqueness of the 20-vertex
extremal graph (Question 8.1). The asymptotics of k(n,m) are untouched:
the best general results remain those of [ErRa67, LaMi97, IRW21]. We do
not claim k(6,3): Proposition 1.2 narrows its range and no more. The
prior bounds improved on here are credited at their sources: the
interval [9,25] is [Ber74] plus [IRW21].

## 2. The lower bound: an explicit graph on 20 vertices

Table 1 defines an oriented graph W on vertex set {0,…,19} by its
out-neighbourhoods; W has 126 arcs.

| v | out-neighbours | v | out-neighbours |
|---|---|---|---|
| 0 | 1, 3, 4, 7, 9, 18 | 10 | 2, 3, 5, 6, 17, 19 |
| 1 | 2, 4, 6, 7, 10, 14, 16 | 11 | 2, 4, 6, 8, 9, 10 |
| 2 | 0, 8, 12, 16, 17, 18, 19 | 12 | 9, 10, 11, 15, 17, 19 |
| 3 | 1, 6, 11, 12, 13, 16 | 13 | 0, 1, 9, 10, 11, 14, 17 |
| 4 | 3, 5, 10, 12, 13, 14 | 14 | 0, 3, 6, 16, 18, 19 |
| 5 | 2, 6, 11, 12, 13, 15, 18 | 15 | 0, 1, 2, 8, 9, 14 |
| 6 | 4, 8, 12, 13, 17, 19 | 16 | 0, 4, 7, 13, 15, 17 |
| 7 | 2, 3, 13, 14, 15, 18 | 17 | 1, 3, 4, 5, 8, 11 |
| 8 | 3, 5, 7, 9, 10, 12, 18 | 18 | 1, 9, 13, 15, 16, 19 |
| 9 | 2, 5, 7, 14, 16, 19 | 19 | 0, 4, 5, 7, 8, 11, 15 |

*Table 1. The 20-vertex witness W: out-neighbourhoods.*

**Theorem 2.1.** *W contains no independent set of size 3 and no
transitive tournament on 4 vertices. Hence k(3,4) ≥ 21.*

The check is a finite verification over the C(20,3) = 1140 triples and
C(20,4) = 4845 quadruples, and runs in milliseconds; it was performed by
independently written verifiers using three distinct transitivity
criteria (among them the score-sequence criterion: transitive if and
only if the scores are {0,1,2,3}), and again from scratch by the
adversarial referee of §4.2, who additionally pushed a randomly
relabelled copy of W through the full canonicalization of §3.3 at every
one of its 20 vertices.

Three facts about W, directly checkable from Table 1, are worth
recording for §8. Every out- and in-degree is 6 or 7, and the vertex
types (d⁺(v), d⁻(v), |I(v)|) — out-degree, in-degree, number of
non-neighbours — take exactly four values: (6,6,7) at eleven vertices,
and (6,7,6), (7,6,6), (7,7,5) at three vertices each. In particular W is
not vertex-transitive. Finally, at each vertex of type (6,6,7) the
non-neighbourhood is a 7-vertex TT₄-free tournament, hence
(Proposition 3.3) a copy of the Paley tournament QR₇.

## 3. The upper bound: exhaustion at N = 21

Call an oriented graph *free* if it contains neither I₃ nor TT₄. The
upper bound is the assertion that no free graph on 21 vertices exists.
The exhaustion has three mathematical ingredients — a neighbourhood
lemma, two vanishing endpoints, and complete inventories of the
neighbourhood blocks — and one computational engine: 346 certified
refutations.

### 3.1. The case decomposition

For a vertex w of an oriented graph D, write N⁺(w), N⁻(w), I(w) for the
sets of out-neighbours, in-neighbours, and non-neighbours of w.

**Lemma 3.1.** *Let D be free and w a vertex of D. Then (i) N⁺(w) and
N⁻(w) each induce an oriented graph with no I₃ and no TT₃; (ii) I(w)
induces a tournament with no TT₄.*

*Proof.* (i) An independent triple inside N⁺(w) is one in D. A
transitive triangle inside N⁺(w) extends by w, a common in-neighbour of
its three vertices, to a TT₄ in D. The argument for N⁻(w) is the same
with w as common out-neighbour (sink side). (ii) Two non-adjacent
vertices of I(w) together with w form an I₃, so I(w) induces a
tournament; a TT₄ inside it is one in D. ∎

**Lemma 3.2.** *There is no {I₃,TT₃}-free oriented graph on 9 vertices,
and no TT₄-free tournament on 8 vertices.*

Lemma 3.2 is equivalent to k(3,3) = 9 [Ber74] and to the classical
k(2,4) = 8, but the exhaustion does not rest on the literature for it:
both statements were established internally four ways — by direct
enumeration of all labelled graphs of the two families (the labelled
counts of {I₃,TT₃}-free graphs on 1,…,9 vertices are 1, 3, 20, 224,
2554, 18370, 30960, 5040, 0; of TT₄-free tournaments on 1,…,8 vertices,
1, 2, 8, 40, 184, 240, 240, 0), re-derived twice more by independent
enumerations during the audits, and by LRAT-certified refutations of the
corresponding instances, replayed by both checkers.

By Lemma 3.1 and Lemma 3.2, in a free graph every vertex w has
d⁺(w) ≤ 8, d⁻(w) ≤ 8, |I(w)| ≤ 7; counting N = 1 + d⁺ + d⁻ + |I| ≤ 24
caps free graphs at 24 vertices, hence k(3,4) ≤ 25 by pure arithmetic.
This is the specialization to (3,4) of the argument of [IRW21,
Lemma 2.3], and it is exactly where the previous record stood. The exhaustion works
at N = 21: there (p,q,s) := (d⁺(w), d⁻(w), |I(w)|) satisfies
p + q + s = 20 with p,q ≤ 8, s ≤ 7, which also forces p,q ≥ 5 and
s ≥ 4.

**Proposition 3.3** (Block inventories). *Up to isomorphism, the
{I₃,TT₃}-free oriented graphs on 5, 6, 7, 8 vertices number 25, 31, 7,
1 respectively — the unique one on 8 vertices being Bermond's circulant,
in agreement with [IRW21, Lemma 3.1] — and the TT₄-free tournaments on 4, 5, 6, 7 vertices number 3,
3, 1, 1, the unique one on 7 vertices being the Paley tournament QR₇.*

These inventories were computed by orbit-peeling of the labelled
enumerations under S_k, with a built-in closure assertion (every
relabelled image of every representative must reappear in the labelled
set), and re-derived by three independent enumerations in total; the
labelled orbit sizes cross-check exactly against the automorphism groups
(order 8 for Bermond's graph, 21 for QR₇).

Reversing all arcs preserves non-adjacency (hence I₃-freeness), maps TT₄
to TT₄, and swaps (p,q,s) ↦ (q,p,s); both block families of
Proposition 3.3 are closed under reversal. So one may assume p ≤ q, and
the possible types at N = 21 are exactly six. Assigning to each type
every ordered choice of isomorphism classes for the three blocks (both
ordered pairs are kept when p = q) yields the case list of Table 2: 346
cases in all.

| type (p,q,s) | block classes | cases |
|---|---|---|
| (5,8,7) | 25 × 1 × 1 | 25 |
| (6,7,7) | 31 × 7 × 1 | 217 |
| (6,8,6) | 31 × 1 × 1 | 31 |
| (7,7,6) | 7 × 7 × 1 | 49 |
| (7,8,5) | 7 × 1 × 3 | 21 |
| (8,8,4) | 1 × 1 × 3 | 3 |
| **total** | | **346** |

*Table 2. The six vertex types at N = 21 (with p ≤ q) and the case
count.*

### 3.2. The encoding

The base formula base(N) has one Boolean variable per ordered pair
(x_{u→v}: the arc u→v is present; 2·C(N,2) = 420 variables at N = 21)
and three clause families, transcribing the definition and nothing
else: for each pair, no 2-cycle (¬x_{u→v} ∨ ¬x_{v→u}); for each triple,
not independent (the disjunction of its six arc variables); for each
4-set, for each of the 24 transitive orientations, a clause forbidding
that orientation. At N = 21 this is
C(21,2) + C(21,3) + 24·C(21,4) = 145,180 clauses. There is no symmetry
breaking of any kind in base(N): its models correspond to free oriented
graphs and to nothing else, and this semantic claim was verified by
brute force at small orders — over all 3^C(N,2) orientations, the
models of base(4) are exactly the 612 free graphs among 729, and the
models of base(5) exactly the 35,488 among 59,049.

Each of the 346 cases becomes a *cube*: base(21) together with unit
clauses fixing vertex 0's complete arc pattern (arcs to 1,…,p, arcs from
p+1,…,p+q, non-adjacency to the rest) and fixing each of the three
blocks to its chosen class representative —
2(20 + C(p,2) + C(q,2) + C(s,2)) units in all, two per constrained
pair. All arcs between different blocks are left entirely free,
constrained only by base(21).

### 3.3. Soundness of the case split

**Proposition 3.4.** *Suppose some free oriented graph D on 21 vertices
existed. Then, for one of the 346 cubes, some relabelling of D (of D
with all arcs reversed, if necessary) would satisfy every clause of that
cube.*

*Proof.* Fix any vertex w of D and let (p,q,s) be its type; by
Lemma 3.1, Lemma 3.2, and p + q + s = 20, the type appears in Table 2
after reversing all arcs if p > q (reversal preserves freeness and swaps
the type; when p = q both ordered block pairs are among the cubes, so no
choice is lost). By Lemma 3.1 the three blocks induced by N⁺(w), N⁻(w),
I(w) belong to the enumerated families, and by the completeness of the
inventories (Proposition 3.3) each is isomorphic to exactly one class
representative. Relabel w ↦ 0, N⁺(w) onto {1,…,p}, N⁻(w) onto
{p+1,…,p+q}, and I(w) onto the rest, choosing within each block an
isomorphism onto its representative. The relabelled graph is free, so it
satisfies base(21) (whose models are exactly the free graphs), and by
construction it satisfies every unit clause of the cube indexed by its
type and block classes. ∎

Since all 346 cubes are unsatisfiable — §3.4 — no free graph on 21
vertices exists, and with Theorem 2.1, Theorem 1.1 follows. The proof
above is a short argument whose computational inputs are Lemma 3.2, the
completeness of Proposition 3.3, the semantics of base(N), the identity
of the 346 cube files with base(21)-plus-units, and the 346 refutations;
every input was machine-checked independently, most several times over
(§4).

### 3.4. The certificates

CaDiCaL 3.0.1 [BFF+24] refuted each of the 346 cubes, emitting an LRAT
proof [CFHKS17] for each; every proof was verified by an independently
written checker that imports only the Python standard library, accepts
only on derivation of the empty clause, and rejects deliberately
corrupted controls. The verification ledger records, per certificate,
the verdict, the checked-step count, the SHA-256 digests of formula and
of proof, and the proof's byte count. Across the N = 21 layer the certificates
range from 236,431 to 7,816,216 checked steps, about 245 GB of
uncompressed proof in total; the complete corpus of the campaign
(including the redundant layers of §5.1) is 445 certificates and just
over 10⁹ checked steps. All 346 solver logs report unsatisfiability;
every base has exactly one ledger line, verdict VERIFIED, formula digest
matching the audited file; no failures, no rejections.

## 4. Verification and audit

### 4.1. Completeness at content level

The decomposition was audited by a referee-style completeness audit,
with independent code, and later re-derived once more from scratch: the
required cube inventory was recomputed from the type arithmetic and
fresh block enumerations, and each of the 346 cube files was required to
equal base(21) plus its expected units *as a clause multiset* — no
missing clause, no duplicate, no stray unit, exact DIMACS header — with
the match established one-to-one across the whole layer, filename-blind.
Negative controls (a dropped clause, a duplicated clause, a hidden extra
unit, a flipped literal) were all rejected. The same audit passed for
the N = 22, N = 23, and N = 24 layers.

As a positive control, the identical pipeline — same generator, same
unit-fixing — was run at N = 20, where a free graph is known to exist:
the witness W, canonicalized per Proposition 3.4 onto its class
representatives, satisfies all 117,750 clauses of the generated N = 20
cube; the solver reports satisfiability on both the cube and the pure
instance; and the extracted models were independently re-verified free.
A false-unsatisfiability pipeline would have failed this control.

Two operational events are recorded for honesty. Mid-campaign the
checker's hint semantics were relaxed from strict format checking to
sound fixpoint semantics (skip hints unusable under the current
assignment, hard-fail on missing identifiers, accept only on the empty
clause) to accommodate a solver emission quirk; the change was ruled
sound, and all negative controls still fail. And three ledger lines were
poisoned by infrastructure failures and repaired: one when the checker
process was killed without output under memory and disk pressure, and
later two more (a second such kill, and a cloud-storage file eviction).
In every case only the verdict field changed — never a formula and never
a proof. The two later originals survive in a ledger backup whose
formula and proof digests and byte counts are identical to the current
lines; the first survives verbatim in the failure log, the backup having
been taken afterwards. All three certificates verify with matching
digests, two of them under the referee's independent checker and one
regenerated byte-identically from its recorded solver command.

### 4.2. The adversarial referee

The confirmed result rests on a final adversarial referee pass, by a
separate agent instance under an explicit independence rule: every
load-bearing check used code written fresh in that session, sharing
nothing with the pipeline or the earlier audits beyond the DIMACS
variable-numbering convention. The referee re-derived the entire
skeleton from the definitions — the neighbourhood lemma, both endpoints
of Lemma 3.2, the inventories of Proposition 3.3, the six types, the
count 346 — and re-established the content bijection between the 346
required formulas and the files on disk over regenerated content. It
wrote and control-validated its own LRAT checker, then attacked ten
adversarially chosen certificates: the largest proof in the corpus, all
three entries with a repair history (these four are the 2.0–2.3 GB
proofs, four of the five largest), the smallest, the largest of every
remaining type, and one further cube. All ten verified,
with step counts and digests equal to the ledger's in every field; in
all twelve cases where both checkers ran the same certificate, their
step counts agreed exactly. Eight of the ten proofs were regenerated
from nothing but the formula by re-running the recorded solver command;
all eight came out byte-identical to the recorded certificates. The
canonicalization of Proposition 3.4 was attacked with 57 pivot
canonicalizations across three graphs, including a family member at 18
vertices found by simulated annealing from a uniformly random start,
sharing no ancestry with the witness; no escape from the inventory was
found. Novelty was swept live the same day. On this protocol the result
was confirmed on August 11, 2026. The referee's verdict record and fresh
code are retained by the author and are not part of the public deposit;
what the deposit carries is the review log and the separate verdict
record for the k(6,3) bound of §5.2.

## 5. Redundant layers, and k(6,3)

### 5.1. Certified exhaustions at N = 22, 23, 24

Freeness is hereditary, so the N = 21 exhaustion already implies that no
free graph exists on any larger order. The campaign nevertheless
produced certified exhaustions at
N = 23 (8 cubes: types (7,8,7) across the seven 7-vertex block classes,
and (8,8,6)) and N = 22 (90 cubes: types (6,8,7)×31, (7,7,7)×49,
(7,8,6)×7, (8,8,5)×3), as well as a single structured instance at
N = 24; all 99 certificates are verified and ledgered, and the multiset
completeness audit of §4.1 passed for each layer. These layers are
logically redundant given Theorem 1.1; they stand as independent
confirmations along the descent 25 → 24 → 23 → 22 → 21, and their
certificates are part of the corpus.

### 5.2. The bracket for k(6,3)

*Proof of Proposition 1.2.* Upper bound: k(m,3) ≤ m² − m + 3 is [IRW21,
Proposition 3.4]; at m = 6 this is 33. Lower bound: let
S = {3, 8, 10, 12, 17} ⊂ ℤ₂₈ and let D = Cay(ℤ₂₈, S), with arcs x → x+s
for s ∈ S. Since −S = {11, 16, 18, 20, 25} is disjoint from S, D is an
oriented graph; it is 5-regular in and out, with 140 arcs. A transitive
triangle x → y → z, x → z in Cay(G,S) is exactly a pair a = y − x,
b = z − y in S with a + b = z − x also in S; here
S + S = {1, 6, 11, 13, 15, 16, 18, 20, 22, 24, 25, 27} is disjoint from
S, so D has no TT₃. The underlying graph of D is Cay(ℤ₂₈, S ∪ −S), whose
independence number is 5; so D has no I₆. Hence k(6,3) ≥ 29. ∎

Only the independence number is a machine check, over the
C(28,6) = 376,740 six-subsets. It was performed by the independently
written witness verifiers of §2, and again by exact computation of the
independence number by branch and bound. Two further 28-vertex
witnesses, one of them a Cayley digraph over ℤ₁₄ × ℤ₂, verify equally
and are archived.

Disjoint unions cannot reach 28: splitting the independence budget 5
across components with the extremal component orders available (3 at
budget 1, since a TT₃-free tournament has at most 3 vertices;
k(a+1,3) − 1 in general) gives 3 + 22 = 25 as the best partition, so
every witness on 26 or more vertices — including D, whose connection set
contains a generator — is connected in the underlying adjacency. No
lower bound beyond 24 (W₂₂, the {I₅,TT₃}-free circulant of [IRW21,
Observation 4.2], plus an isolated vertex) appears in the literature.

## 6. Certification

The permanent record of the computation is deliberately small: the
verification ledger (one line per certificate: verdict, checked-step
count, SHA-256 of formula and of proof, and the proof's byte count), the
queue files recording the exact solver command line for every cube of
the N = 21, 22 and 23 layers, the generator and checker scripts, the
block-inventory representatives the generator consumes, the witness
files, and the audit and referee records. That record is split between a
public deposit and a private regeneration kit.

Deposited with this note in the program's public certificate repository
*Certify* ([github.com/05oz/certify](https://github.com/05oz/certify);
concept DOI
[10.5281/zenodo.21799111](https://doi.org/10.5281/zenodo.21799111)),
version DOI [10.5281/zenodo.21890619](https://doi.org/10.5281/zenodo.21890619),
are the ledger, the regeneration instructions, the two witness files,
six scripts — the encoder `gen_cnf.py`, the structured-cube generator
`make_structured.py`, the proof checker `lrat_check.py`, the witness
checker `verify_witness.py`, and the audits `audit_cnf.py` and
`audit_multiset.py` — and the review log together with the referee
verdict for k(6,3). Retained by the author and not redistributed are the
queue files, the 70 block-class representatives the generators consume,
the rest of the checking and audit pipeline, and the audit and k(3,4)
referee records. So the lower-bound half replays from the deposit
outright, as does any certificate whose formula and proof the reader
has; regenerating a case formula to its recorded `cnf_sha256` needs the
representatives, and `audit_multiset.py` imports a module of the kit and
does not run from the deposit alone.

The multi-gigabyte proofs themselves are a cache, not the record: each
regenerates from its recorded command — deterministically, in our
environment: the referee's eight regenerations were all byte-identical to
the originals, matching the ledger's digests — and the deposit documents
the regeneration procedure and what it requires. As to tooling, the
checkers are standard-library only, so replaying a certificate or a
witness requires only CPython; regenerating proofs requires
CaDiCaL 3.0.1.

## 7. The trusted base

What a skeptic must believe, separated from what they can replay.

*Machine-checked, replayable with standard-library Python:* the witness
W and the 28-vertex witness of Proposition 1.2 (milliseconds); the
labelled enumerations behind Lemma 3.2 and Proposition 3.3, performed
three independent times, with closure assertions (minutes); the
brute-force semantics of base(4) and base(5) over all orientations; the
clause-multiset identity of all 445 cube files with their re-derived
specifications (this audit runs in the regeneration kit, not from the
deposit alone); and the LRAT replay of all 445 certificates by an
independently written checker, with twelve of them re-run by a second,
unrelated checker agreeing on the exact step count in every case. Both
checkers reject all negative controls.

*Trusted:*

1. *The checkers' proof semantics.* Both checkers implement
   RUP-with-hints with sound fixpoint treatment of hints and accept only
   on derivation of the empty clause. That this discipline is sound is a
   short argument on paper, not a machine-checked one; the mitigation is
   two independent implementations in agreement, plus negative controls
   (corrupted proof, mutated formula, dropped hint) rejected by both.
2. *The assembly of §3.3.* The proof of Proposition 3.4 is half a page
   of mathematics to be read by a human. Every computational input to it
   is machine-checked; the gluing is not, and is short by design.
3. *The generalization of the base semantics from N = 4, 5 to N = 21.*
   The brute-force model check is exhaustive only at N = 4, 5; at N = 21
   the claim rests on the clause families being uniform in N (with
   closed-form clause count C(N,2) + C(N,3) + 24·C(N,4) matching at
   every audited order) and on the independent re-derivation of the
   exact clause multiset from the definitions.
4. *SHA-256 collision resistance*, for the bookkeeping that ties ledger
   lines to files. The LRAT corpus is a regenerable cache and is not shipped,
   so no shipped certificate depends on a hash for its replay; regenerating a case formula to its recorded
   `cnf_sha256`, however, needs the block representatives, which are part
   of the private regeneration kit and not of this deposit.
5. *CPython, the operating system, and the hardware.*

CaDiCaL, the cube generators, and the solving pipeline are *not* in the
trusted base: nothing depends on the solver being correct, only on its
proofs checking, and every proof was checked by code unrelated to the
solver — a sample of them by two such checkers independently.

## 8. Questions

What is this computation *for*? Four directions it opens.

### 8.1. The extremal structure at (3,4)

The extremal graph for k(3,3) is unique up to isomorphism
[IRW21, Lemma 3.1] — a circulant. The witness W of §2 shows no such symmetry: it has four
vertex types, so it is not vertex-transitive, although the Paley
tournament QR₇ appears as the non-neighbourhood of eleven of its twenty
vertices. This mirrors the situation at k(4,3), where [IRW21] remark
that no Cayley witness on 14 vertices exists, while the k(5,3) witness
is again circulant.

**Question 8.1.** Is W the unique {I₃,TT₄}-free oriented graph on 20
vertices up to isomorphism? If not, what is the number of extremal
graphs, and does any admit an algebraic description?

A related quantitative puzzle: the counting bound of §3.1 caps free
graphs at 24 vertices, yet the largest free graph has 20 — at
N = 21, 22, 23 every one of the 346 + 90 + 8 cases dies, with no
tightness anywhere. A structural explanation of this slack of 4 (at
k(3,3) the analogous cap 1 + 2 + 2 + 3 = 8 is attained, by Bermond's
graph) is exactly what a human proof would have to supply.

### 8.2. The gap at k(6,3)

Proposition 1.2 leaves k(6,3) ∈ [29,33], now the smallest open case of
the k(m,3) column. Every witness on 26 or more vertices is connected in
the underlying adjacency, which points toward vertex-transitive
candidates: for Cayley digraphs, TT₃-freeness of Cay(G,S) is exactly
sum-freeness of S, which makes the search cheap. This is how the
28-vertex witness was found. An exhaustive sweep of connection sets over
the cyclic groups of orders 29, 30 and 31 — the only abelian groups of
those orders — and over three of the seven abelian groups of order 32
produced nothing, so any witness beating 28 lies outside that range of
constructions. The upper bound looks harder: an exhaustion in this
note's style would need complete inventories of {I₅,TT₃}-free graphs on up
to 22 vertices, far beyond present enumeration, so progress below 33
seems likelier to come from sharpening the m² − m + 3 argument of
[IRW21].

### 8.3. k(4,4) and beyond

The new value propagates through the standard recursion. By Lemma 3.1 in
its general form [IRW21, Lemma 2.1], every {I₄,TT₄}-free graph has
d±(v) ≤ k(4,3) − 1 = 14 and |I(v)| ≤ k(3,4) − 1 = 20, so such a graph
has at most 1 + 14 + 14 + 20 = 49 vertices, and likewise every
{I₃,TT₅}-free graph has at most 1 + 20 + 20 + 13 = 54; hence

  k(4,4) ≤ 50,   k(3,5) ≤ 55,

which is the recursion of [IRW21, Lemma 2.3] evaluated at the new value.
Meanwhile k(4,4) ≥ k(3,4) = 21, since a graph with no I₃ has no I₄, so W is
also {I₄,TT₄}-free. An honest feasibility assessment: determining k(4,4)
or k(3,5) by the present method is out of reach. The decomposition would
require complete isomorph inventories of {I₄,TT₃}-free graphs up to 14
vertices, or of {I₃,TT₄}-free graphs up to 20 vertices — and the
labelled counts of the latter family are already 35,488 at 5 vertices
and 4,490,572 at 6 — and the resulting instances at N in the forties
would dwarf the 10⁹ checked steps spent here at N = 21. What does look
feasible: raising lower bounds by witness search (any verified witness
is a one-line check), and isomorph-free generation of the free families
at small orders to map the terrain.

### 8.4. Toward a human-readable proof

The upper-bound half of Theorem 1.1 is 346 machine proofs averaging
about two and a half million checked steps. Two concrete paths would shrink it. First,
structure theory: the proof of Proposition 3.4 shows that any free graph
on 21 vertices is assembled from three blocks drawn from very short
lists around every vertex simultaneously; a human argument that such an
assembly forces an I₃ or a TT₄ — perhaps via the QR₇ and Bermond
blocks, which dominate the type table — would replace the certificates
outright, and would likely explain the slack of §8.1 as a by-product.
Second, proof compression: the LRAT corpus is an upper bound on the
difficulty of the theorem, not a measure of it, and nothing is known
about the minimum certificate size; a decomposition chosen for proof
economy rather than for engineering convenience might cut the corpus by
orders of magnitude and expose which cases are genuinely hard. Either
advance would turn a determined value into an understood one.

## Acknowledgments

The problem is Erdős and Rado's; its continued visibility owes much to
Thomas Bloom's Erdős problems collection [Blo]. The line of exact values
this note extends was opened by Jean-Claude Bermond and carried to
k(4,3) and k(5,3) by Ferdinand Ihringer, Deepak Rajendraprasad, and
Thilo Weinert, whose paper also named this note's target. The
certificate infrastructure rests on CaDiCaL by Armin Biere and
coauthors, on the LRAT format of Cruz-Filipe, Heule, Hunt, Kaufmann, and
Schneider-Kamp, and on the cube-and-conquer paradigm of Heule, Kullmann,
Wieringa, and Biere. The computation and drafting were AI-assisted as
stated in the first footnote; the adversarial referee protocol of §4.2
and the referee's rule that a computation-only paper close with the
questions it opens shaped this note's final form.

## References

- **[Ber74]** J.-C. Bermond, *Some Ramsey numbers for directed graphs*,
  Discrete Math. **9** (1974), 313–321.
- **[BFF+24]** A. Biere, T. Faller, K. Fazekas, M. Fleury, N. Froleyks
  and F. Pollitt, *CaDiCaL 2.0*, in: Computer Aided Verification — CAV
  2024, Lecture Notes in Comput. Sci. **14681**, Springer, 2024,
  133–152. Version used to produce the proofs: CaDiCaL 3.0.1 (`--lrat`).
- **[Blo]** T. F. Bloom, *Erdős Problem #112*,
  https://www.erdosproblems.com/112, accessed 2026-08-11.
- **[CFHKS17]** L. Cruz-Filipe, M. J. H. Heule, W. A. Hunt Jr.,
  M. Kaufmann and P. Schneider-Kamp, *Efficient certified RAT
  verification*, in: Automated Deduction — CADE-26, Lecture Notes in
  Comput. Sci. **10395**, Springer, 2017, 220–236.
- **[ErRa67]** P. Erdős and R. Rado, *Partition relations and
  transitivity domains of binary relations*, J. London Math. Soc.
  **42** (1967), 624–633.
- **[HKM16]** M. J. H. Heule, O. Kullmann and V. W. Marek, *Solving and
  verifying the Boolean Pythagorean triples problem via
  cube-and-conquer*, in: Theory and Applications of Satisfiability
  Testing — SAT 2016, Lecture Notes in Comput. Sci. **9710**, Springer,
  2016, 228–245.
- **[HKWB11]** M. J. H. Heule, O. Kullmann, S. Wieringa and A. Biere,
  *Cube and conquer: guiding CDCL SAT solvers by lookaheads*, in:
  Hardware and Software: Verification and Testing — HVC 2011, Lecture
  Notes in Comput. Sci. **7261**, Springer, 2012, 50–65.
- **[IRW21]** F. Ihringer, D. Rajendraprasad and T. Weinert, *New bounds
  on the Ramsey number r(I_m,L_n)*, Discrete Math. **344** (2021),
  no. 3, 112268. Also arXiv:1707.09556 (v3, April 2020), the text read
  here (see the second footnote).
- **[LaMi97]** J. A. Larson and W. J. Mitchell, *On a problem of Erdős
  and Rado*, Ann. Comb. **1** (1997), 245–252.
