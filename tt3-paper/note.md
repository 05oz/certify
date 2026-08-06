# The minimum number of arc-disjoint transitive triples in a tournament: a first certified determination of ν₃(9) = 9 and ν₃(10) = 12

**Daniel Kirtchakov**
Independent researcher (`05oz`); no institutional affiliation — daniel@halfounce.io — halfounce.io

*Draft of August 5, 2026.*

> **Computation and authorship.** All searches, encodings, and certificate
> designs in this work were produced by **Claude Fable 5** (Anthropic),
> directed by the author, on a single Apple M4 laptop. The independent
> verifiers import only the Python standard library and share no code with
> the search pipeline; the adversarial referee of §3.2 was a separate agent
> instance given no access to the pipeline and wrote its own code
> throughout. This is a factual methods statement, and it is part of the
> point of the note: the artifacts are designed so that the provenance of
> the *search* is irrelevant to the validity of the *result*. External
> tools used by the pipeline only: `gentourng` (nauty 2.9.3),
> CaDiCaL 3.0.1 (`--lrat --no-binary`), Apple clang 17.0.0, Python 3.

> **Prior-art record.** The Kabiya–Yuster text [KY08] was read in full
> on August 5, 2026, from the copy saved with the artifacts (an author
> preprint; section references follow its numbering). The
> concluding-remarks account in [Yus04] of the verified range and of the
> upper-bound construction was checked verbatim against the arXiv text
> (`math/0304180`) the same day; the results of [Yus04] are otherwise
> used as reported in [KY08]. The novelty sweep of the same date — the
> Open Problem Garden entry fetched live, the arXiv API, and general web
> sweeps — found no determination of the integral values ν₃(9) or ν₃(10)
> anywhere in the record since 2008. The upper-bound half of both values
> was never open; see §1.3.

---

## Abstract

For a tournament *T* let ν₃(*T*) be the maximum number of pairwise
arc-disjoint transitive triples in *T*, and let ν₃(*n*) = min over all
*n*-vertex tournaments *T* of ν₃(*T*). Yuster (2004) conjectured
ν₃(*n*) = ⌈*n*(*n*−1)/6 − *n*/3⌉ and verified this for all *n* ≤ 8
(*n* = 8 by computer, the smaller cases by direct argument), without
published certificates; no determination of ν₃(9) or
ν₃(10), certified or otherwise, appears in the record since. We supply
the first certified determination: **ν₃(9) = 9 and ν₃(10) = 12**, the
conjectured values.

The new content is the two lower bounds. An exact branch-and-bound packer
was run over every tournament isomorphism class — all 191,536 at *n* = 9
and all 9,733,056 at *n* = 10, enumerated by `gentourng` with counts
validated against OEIS A000568 and independently recomputed Burnside
numbers — and emitted, for every class, an explicit packing of 9
(resp. 12) arc-disjoint transitive triples, each re-verified from the raw
arc data by a standard-library checker sharing no code with the search.
The matching upper bounds are not new: they are Yuster's (2004), via
oriented Turán blow-ups, restated with a fractional strengthening by
Kabiya and Yuster (2008), §2.4. What we add on that side
is an artifact: for an explicit minimizer in each order —
C₃[C₃,C₃,C₃] at *n* = 9 and C₃[TT₄,C₃,C₃] at *n* = 10 — an
LRAT-certified proof that no packing of 10 (resp. 13) triples exists,
replayed by an independent checker that regenerates the CNF from its
specification.

One trust assumption is declared rather than checked: that `gentourng`
(nauty) enumerates the isomorphism classes completely. It was
cross-validated exhaustively for *n* ≤ 7 and count-validated at
*n* = 9, 10. Everything else was verified twice: by stdlib-only
verifiers, and by an adversarial referee who re-ran the enumeration to
byte-level set equality, re-solved both minimizers with an independent
exact solver, and exercised both verifiers with negative controls. The
next open case, ν₃(11) (conjectured value 15), is a factor of roughly 93
larger and is within reach of the same pipeline (CPU-days, not
CPU-years); it has not been started.

## 1 Introduction

### 1.1 The problem

A tournament is an orientation of the complete graph. A transitive triple
(TT₃) is a 3-vertex subtournament with no directed cycle; a TT₃-packing
of a tournament *T* is a set of pairwise arc-disjoint transitive triples
of *T*, and ν₃(*T*) is the maximum size of one. Following Kabiya and
Yuster [KY08] we write

ν₃(*n*) = min { ν₃(*T*) : *T* a tournament on *n* vertices },

the value of the packing problem on the *worst* *n*-vertex tournament.
Yuster [Yus04] proved that ν₃(*n*) ≥ (51/392) *n*² (1 − o(1)),
conjectured the exact value, and verified the conjecture for all
*n* ≤ 8 — *n* = 8 by computer, the smaller cases by direct argument
[Yus04, §4]:

> **Conjecture** (Yuster [Yus04]; Conjecture 1.1 of [KY08]).
> ν₃(*n*) = ⌈*n*(*n*−1)/6 − *n*/3⌉.

The conjectured sequence begins, from *n* = 3: 0, 1, 2, 3, 5, 7, 9, 12,
15, … Kabiya and Yuster [KY08] improved the asymptotic lower bound to
(41/300) *n*² (1 − o(1)), still the best known, by solving the
*fractional* relaxation at *r* = 10 by linear programming (ν₃\*(10) = 12)
and transferring the bound to the integral problem with a loss. Their
paper is the last progress recorded on the problem's Open Problem Garden
entry [OPG], which records no progress beyond 2008.

The state of the integral problem at the start of this work was
therefore: conjectured value known for all *n*; verified for *n* ≤ 8 by
Yuster (*n* = 8 by computer), with no certificates for that range in
[Yus04] or anywhere else in the record; at *n* = 9
and *n* = 10, an upper-bound half that was closed in print (see §1.3) and
a lower-bound half with nothing in the record. *No certified
determination of ν₃(9) or ν₃(10) existed.*

### 1.2 Result

**Theorem 1.1.** *ν₃(9) = 9 and ν₃(10) = 12. Consequently, together with
the verified range n ≤ 8 ([Yus04], reproduced in §2.2), Yuster's
conjectured formula ⌈n(n−1)/6 − n/3⌉ holds for all n ≤ 10, and a
counterexample, if one exists, has n ≥ 11.*

Every claim in Theorem 1.1 is backed by a machine-checkable artifact: an
explicitly verified witness packing for every one of the
191,536 + 9,733,056 tournament isomorphism classes (the lower bounds),
and LRAT unsatisfiability certificates on explicit minimizer tournaments
(the upper bounds), all replayable with standard-library Python and
shipped with hashes (§6). This extends the verified range of the
conjecture from *n* ≤ 8 (uncertified) to *n* ≤ 10 (certified).

### 1.3 Provenance and credit

The division of labor between this note and the literature is exact, and
stating it precisely is a referee-imposed condition on the writing.

*The upper bounds are Yuster's.* Section 4 of [Yus04] orients
the complete 3-partite Turán graph V₁→V₂→V₃→V₁, completes the classes
arbitrarily, and observes that every transitive triple of the resulting
tournament uses at least one within-class arc; hence no TT₃-packing
exceeds the number of within-class arcs, which
is exactly ⌈*n*(*n*−1)/6 − *n*/3⌉. Kabiya and Yuster [KY08, §2.4]
restate the construction — crediting the tournaments to [Yus04] — and
strengthen the bound to the *fractional* packing number. At *n* = 9 with
parts (3,3,3) this gives ν₃(9) ≤ 9; at *n* = 10 with parts (4,3,3) it
gives ν₃(10) ≤ 12. So the upper-bound half of Theorem 1.1 was never open, and
nothing about the *values* 9 and 12 being upper bounds is claimed here.
What this note adds on the upper side is a certificate: an LRAT proof,
for an explicit minimizer in each order, that one more triple does not
fit (§2.4).

*The lower bounds are the new content.* ν₃(9) ≥ 9 and ν₃(10) ≥ 12 assert
something about *every* tournament of the given order, and for these no
argument, computation, or certificate existed in the record. They are
established here by exhaustive per-isomorphism-class computation with
per-class witnesses (§2.3).

*The enumeration is nauty's; the counts are classical.* Tournament
isomorphism classes were generated by `gentourng` from the nauty suite of
McKay and Piperno [MP14], and the class counts 191,536 and 9,733,056 are
OEIS sequence A000568 [OEIS], recomputed independently during
verification via Burnside's lemma (Davis's formula [Dav54]).

### 1.4 What is not claimed

We do not claim the upper bounds, which are [Yus04]'s (with the
fractional strengthening of [KY08]). We do not claim any asymptotic improvement; the
best general lower bound remains (41/300) *n*² (1 − o(1)) of [KY08]. We
do not claim the values were unexpected: they are exactly the conjectured
ones. We do not claim the conjecture; it remains open for *n* ≥ 11. And
one link in the chain is trusted rather than machine-checked — the
completeness of the `gentourng` enumeration — and §4 states exactly what
supports that trust.

## 2 The two halves of the computation

### 2.1 Enumeration

All tournaments were handled up to isomorphism, which suffices because ν₃
is an isomorphism invariant. `gentourng -q 9` produced 191,536
tournaments and `gentourng -q 10 r/16`, r = 0,…,15, produced 9,733,056 in
sixteen slices (per-slice counts are shipped in `n10_chunk_counts.txt`
and sum exactly). Both totals equal A000568 [OEIS]. Each tournament is a
line of C(*n*,2) characters, the upper triangle row by row, `1` at pair
(i,j), i<j, iff the arc is i→j; the output strings were checked to be
pairwise distinct (`sort -u`: 191,536 and 9,733,056).

### 2.2 The exact packer, validated on the known range

`tt3pack.c` (136 lines of C) computes ν₃(*T*) exactly by branch and
bound: it branches on a live uncovered arc with the fewest free triples
through it — either some free triple through it joins the packing, or the
arc is marked permanently uncovered — and prunes with the bound
|packing| + ⌊live free arcs / 3⌋. With a target t > 0 it stops early as
soon as a packing of size ≥ t is found and prints it; with target 0 it
returns the exact maximum with an optimal packing. Before any new claim
was attempted, the packer was run in exact mode over the complete
enumeration for *n* = 4,…,8 and returned minima 1, 2, 3, 5, 7 —
reproducing Yuster's verified range [Yus04] exactly (achieving
tournaments and optimal packings in `smalln_table.txt`).

### 2.3 Lower bounds: a witness for every isomorphism class

The sweep `gentourng -q 9 | tt3pack 9 9` terminated with every one of the
191,536 classes reporting a packing of ≥ 9 arc-disjoint transitive
triples, each line carrying the packing itself (about a second of wall
clock; log `n9_sweep.txt.gz`). The sixteen *n* = 10 slices, run as
`gentourng -q 10 r/16 | tt3pack 10 12`, terminated with all 9,733,056
classes reporting a packing of ≥ 12, about 3 s per slice (logs
`n10_sweep_0..15.txt.gz`). Since every tournament is isomorphic to a
listed one and ν₃ is invariant,

ν₃(9) ≥ 9,  ν₃(10) ≥ 12.

These 9,924,592 witness lines are the note's entire novel mathematical
content, and they are what the verification of §3 re-checks line by line.

### 2.4 Upper bounds: certified optimality on explicit minimizers

Following [Yus04, §4] and [KY08, §2.4], the candidate minimizers are the
cyclic blow-ups C₃[T₁,T₂,T₃]: three vertex classes with all arcs V₁→V₂→V₃→V₁ and
arbitrary tournaments inside the classes. The packer, in exact mode, was
run on every within-class variant: all 8 variants with parts (3,3,3) at
*n* = 9 have ν₃(*T*) = 9 exactly, and all 48 variants with parts (4,3,3)
at *n* = 10 have ν₃(*T*) = 12 exactly (`cand9.out`, `cand10.out`) —
consistent with [Yus04, §4] and [KY08, §2.4], where the upper bound is
proved for an arbitrary within-class completion. The representatives
fixed for certification are

T₉ = C₃[C₃,C₃,C₃],  T₁₀ = C₃[TT₄,C₃,C₃]

(arc strings in `minimizer9.bits`, `minimizer10.bits`; T₁₀ has the
transitive 4-tournament in its 4-class). For each, two artifacts are
shipped:

- an optimal packing — 9 triples in T₉, 12 in T₁₀ (`minimizer9.witness`,
  `minimizer10.witness`) — so the values are attained;
- a proof that no larger packing exists: a CNF asserting "*T* contains 10
  (resp. 13) pairwise arc-disjoint transitive triples", refuted by
  CaDiCaL 3.0.1 [BFF+24] with an LRAT proof [CFHKS17]: `min9_ge10.cnf`
  (2,430 variables, 5,058 clauses; proof `min9_ge10.lrat`,
  419,396 bytes) and `min10_ge13.cnf` (5,740 variables, 11,916 clauses;
  proof `min10_ge13.lrat`, 1,938,465 bytes).

The encoding (full byte-exact specification in the `encode_cnf.py`
docstring) has one variable per transitive triple of *T*, a binary
conflict clause for each pair of triples sharing an arc, and a Sinz
sequential at-most-K counter [Sin05] on the negated triple variables,
K = m − k with m the number of transitive triples, so that at least k
triples must be selected. Its correctness splits asymmetrically. That any
satisfying assignment yields k arc-disjoint triples is forced clause by
clause (conflict clauses; counter soundness). The direction that makes
UNSAT meaningful — any packing of size k extends to a satisfying
assignment of the counter variables — is the standard completeness
property of the sequential-counter encoding [Sin05], and it sits in the
trusted base (§4). As positive controls, the same encoding at the
attained value is satisfiable, and was solved as such: `min9_ge9.cnf` and
`min10_ge12.cnf` are SAT (CaDiCaL exit 10), so unsatisfiability appears
exactly at value+1. Hence ν₃(T₉) = 9 and ν₃(T₁₀) = 12, giving ν₃(9) ≤ 9
and ν₃(10) ≤ 12 — the bounds already available on paper from
[Yus04, §4], now in checkable form. With §2.3, Theorem 1.1 follows.

**Remark 2.1 (The fractional parameter).** The blow-up bound holds for
the fractional packing number ν₃\* as well — this strengthening is
Kabiya–Yuster's [KY08, §2.4] — so
ν₃\*(9) ≤ 9 and ν₃\*(10) ≤ 12; combining with ν₃\*(*n*) ≥ ν₃(*n*) and
Theorem 1.1 gives ν₃\*(9) = 9 and ν₃\*(10) = 12. The r = 10 value agrees
with the LP computation reported in [KY08, §3] and provides an
independent derivation of it that does not rest on an uncertified LP
solve. This is consistent with the observation of [KY08, §2.4] that their
Conjecture 1.1 implies ν₃\*(*n*) = ν₃(*n*) for all *n*.

## 3 Verification

### 3.1 Independent stdlib-only verifiers

Two verifiers, sharing no code with the searcher and importing only the
Python standard library, re-check everything the pipeline produced.

`verify_sweep.py` re-checks every one of the 9,924,592 sweep lines from
the raw arc string alone: each witness triple is transitive in the stated
tournament, no arc is used twice, the count meets the target, the line
totals match the expected class counts exactly. All 17 witness files pass
with zero failures. A below-target line would be flagged loudly as a
candidate counterexample; there were none.

`verify_minimizer.py` re-establishes ν₃(T₉) = 9 and ν₃(T₁₀) = 12 from raw
artifacts: it re-checks the optimal packing against the bits;
*regenerates* the CNF from the encoding specification with independent
code and demands equality with the shipped CNF as a clause multiset; and
replays the LRAT proof with its own RUP-with-hints checker — no external
tool, and RAT steps are refused outright, which incidentally establishes
that both proofs are pure RUP. Both certificates verify.

### 3.2 The adversarial-referee protocol

The result was then subjected to an adversarial referee — a separate
agent instance with no access to the pipeline, writing entirely fresh
code — whose protocol is part of the contribution and is recorded in the
program's results ledger of 2026-08-05. The referee re-ran the
enumeration from scratch and confirmed byte-level set equality with the
shipped sweeps; recomputed the class counts 191,536, 9,733,056 exactly
via Burnside's lemma (Davis's formula [Dav54]), independently of both
nauty and OEIS; re-verified
all 9,924,592 witness lines with its own sweep verifier (zero failures);
re-solved both minimizers with its own exact solver, of a different
design and not SAT-based, obtaining 9 and 12; re-ran CaDiCaL afresh on
the shipped CNFs; and exercised both stdlib verifiers with negative
controls — deliberately corrupted artifacts — all of which were correctly
rejected. The referee also imposed the credit framing of §1.3 and caught
one error in an internal draft (Remark 5.1). On this protocol the result
was confirmed on 2026-08-05.

## 4 The trusted base

What a skeptic must believe, split into what is re-checked by short
readable code and what is assumed.

*Machine-checked:* every witness packing, per isomorphism class, from raw
arc data (§3.1); the totals and per-slice counts; pairwise distinctness
of the enumerated strings; the optimal packings in both minimizers; the
clause-multiset equality of each shipped CNF with an independent
regeneration from the specification; and the LRAT replay of both
unsatisfiability proofs, in a checker that refuses RAT steps.

*Assumed:*

1. *`gentourng` enumerates completely* — one representative of every
   isomorphism class. This is the one substantive trust assumption, and
   it is supported rather than proved: exhaustive cross-validation for
   *n* ≤ 7; class counts at *n* = 9, 10 equal to OEIS A000568 [OEIS] and
   to the referee's independent exact Burnside computation [Dav54];
   output strings pairwise distinct; and a fresh re-run by the referee,
   equal to the shipped enumeration as a set of strings byte for byte.
   Distinct strings with the right count do not by themselves
   imply completeness (two listed strings could in principle be
   isomorphic, hiding a missed class), which is why this item is listed
   here and not above.
2. *The sequential-counter encoding is complete* [Sin05]: every packing
   of size k extends to a satisfying assignment of the counter variables.
   If the counter accidentally over-constrained, UNSAT would mean less
   than claimed. ([Sin05] states the property; the short conference
   paper omits the proofs for space.)
3. *The arc-string convention is read as written.* Searcher and verifiers
   necessarily share the *convention* (not code) for interpreting
   `gentourng`'s output format. A consistent misreading on both sides
   would not be caught by line re-checking; it is caught instead by the
   *n* ≤ 8 reproduction of Yuster's values and by the minimizers, whose
   blow-up structure is known independently of the format.
4. CPython and the operating system.

The searcher `tt3pack`, the encoder, CaDiCaL, and the shipped CNF files
are *not* in the trusted base: every claim they produced was re-derived
from raw data or regenerated and re-checked independently.

## 5 The frontier: n = 11

The next open case is ν₃(11), conjectured value ⌈110/6 − 11/3⌉ = 15.
There are A000568(11) = 903,753,248 isomorphism classes, a factor of
about 93 over the *n* = 10 sweep — CPU-days, not CPU-years, for the
pipeline exactly as shipped (`tt3pack` as written handles *n* ≤ 11; the
55 arc pairs fit one 64-bit mask). The corresponding minimizer candidates
are the blow-ups with parts (4,4,3), whose 6+6+3 = 15 within-class arcs
match the conjectured value, so both halves are within reach of the same
two-sided method. This computation is the program's next target; it has
not been started, and no result at *n* = 11 is claimed here. The fractional side (ν₃\*(r) for
r = 11, which would sharpen the 41/300 of [KY08]) is LP-based, separate,
and was not touched.

**Remark 5.1 (A corrected estimate).** An earlier internal draft of the
working notes misstated A000568(11) as ≈ 9.04 × 10¹¹ and priced the
*n* = 11 sweep accordingly ("~100 TB of logs"). The referee's exact
Burnside computation gives 903,753,248 ≈ 9.04 × 10⁸ — the same mantissa,
three orders of magnitude smaller — and the feasibility claim above rests
on the corrected value. We record the error because estimates that die in
private make the surviving ones less trustworthy.

## 6 Artifacts

The artifacts ship in two directories of the public repository
(github.com/05oz/certify): `tt3-certificates/` (sweeps, certificates,
minimizers — 148 MB of gzipped *n* = 10 sweep logs in sixteen files,
2.3 MB for *n* = 9) and `tt3-scripts/` (code and verifiers), everything
besides the sweep logs under 2 MB. The certified release is exactly the
32 files pinned by MD5 digest in `MD5SUMS.txt` and reproduced in the
table below: the sweeps, certificates, minimizers, verifiers, and code.
Of the auxiliary files cited in the text, `n10_chunk_counts.txt` and
`smalln_table.txt` ship alongside them, unpinned; `cand9.out`,
`cand10.out`, and the archived primary-source PDFs are retained in the
author's private working tree and are not redistributed (the PDFs for
copyright reasons). The certified chain of Theorem 1.1 runs entirely
through the pinned files.

To replay from scratch on any machine with nauty, CaDiCaL, a C compiler
and Python 3 (the commands are written for a flat working directory —
in the repository the pinned files sit in `tt3-scripts/` and
`tt3-certificates/`; copy them into one directory first):

```
cc -O2 -o tt3pack tt3pack.c
gentourng -q 9  | ./tt3pack 9 9      # lower-bound sweep, n=9
gentourng -q 10 | ./tt3pack 10 12    # lower-bound sweep, n=10
python3 encode_cnf.py 9  "$(cat minimizer9.bits)"  10 min9_ge10.cnf
cadical --lrat --no-binary min9_ge10.cnf min9_ge10.lrat  # s UNSATISFIABLE
python3 verify_sweep.py --n 9 --target 9 --expect 191536 n9_sweep.txt.gz
python3 verify_minimizer.py --n 9 --value 9 --bits minimizer9.bits \
    --witness minimizer9.witness --cnf min9_ge10.cnf --lrat min9_ge10.lrat
```

and the same pattern at *n* = 10 with target 12, value 12, and K = 13
files. (The sweep commands stream to standard output; redirect to a
file. The first field of each sweep line is a per-run line number, which
restarts in every slice: when comparing an unsliced *n* = 10 replay
against the sixteen shipped slices, compare the remaining fields.
Production ran the sixteen-slice form.) The two verifiers need only the
Python standard library;
re-checking the shipped artifacts requires neither nauty, nor CaDiCaL,
nor a compiler, except for the enumeration itself, which is the declared
trust assumption of §4. Tool versions used: nauty 2.9.3, CaDiCaL 3.0.1,
Apple clang 17.0.0, CPython 3.

| file | MD5 |
|---|---|
| `tt3pack.c` | `46592e2c895dcd88f485f35f408940dc` |
| `encode_cnf.py` | `c277f53e7343a44c93375159c248f08a` |
| `verify_sweep.py` | `a3726bfbb524e1d5d29bdfa892776fe0` |
| `verify_minimizer.py` | `373639d979b8f44f559ca9ea78ef880b` |
| `make_candidates.py` | `546aabe9b6d4a28499da6be2c27e3b45` |
| `minimizer9.bits` | `34ed2059bf5e33ff439e040d0306b7a4` |
| `minimizer10.bits` | `66d67402bb479a6bc831d10d632c980c` |
| `minimizer9.witness` | `35a3d4136122454cb41624bd013c083c` |
| `minimizer10.witness` | `e1b9923118dbe2358007edf31da8da1f` |
| `min9_ge10.cnf` | `f0080051d89ec538e86501efeeaecadf` |
| `min9_ge10.lrat` | `d13133b094e5bc0ab5fd7f7b7cf1af3b` |
| `min10_ge13.cnf` | `ce16d4fc654198dcb1e3ff0782dd5b1a` |
| `min10_ge13.lrat` | `ad546eece47db3d3f7abf9baacc859bf` |
| `min9_ge9.cnf` | `a9acac4e212214975eb28f3690d21f86` |
| `min10_ge12.cnf` | `eb5ae68eb5262236e2c0c8e4947b9c25` |
| `n9_sweep.txt.gz` | `b43c323b55c2f199d94cacc025d3d15b` |
| `n10_sweep_0.txt.gz` | `5069371e1500dda7eabdf5fe7a0d4e35` |
| `n10_sweep_1.txt.gz` | `73e36c3db19e0815e57de78761d92dd2` |
| `n10_sweep_2.txt.gz` | `f9c71121e500d9594fab895a8fb9d6ba` |
| `n10_sweep_3.txt.gz` | `4e243e0e91582866523d512669c9eba4` |
| `n10_sweep_4.txt.gz` | `d3d96b7b0a78432cb8e80dec1366a36a` |
| `n10_sweep_5.txt.gz` | `bbe411ec67ba2e144ddd1fdb13cb1ce4` |
| `n10_sweep_6.txt.gz` | `9fb5d3da724fcf453451e1ce4e639573` |
| `n10_sweep_7.txt.gz` | `ece12815439e764a813c99a70b20ddb8` |
| `n10_sweep_8.txt.gz` | `b9fcb0b5939650e5b5a1f1fa51173438` |
| `n10_sweep_9.txt.gz` | `1cd91ac37afb04e120415e5790a34bb6` |
| `n10_sweep_10.txt.gz` | `a1e999d85ba88c3dd131fb123702b46b` |
| `n10_sweep_11.txt.gz` | `64afda1fb8d36eebf04d70a53d2664b1` |
| `n10_sweep_12.txt.gz` | `90485a8cf9e63e716980c0ef74a6726c` |
| `n10_sweep_13.txt.gz` | `0109f71fbb2a111405b175b6c40f2120` |
| `n10_sweep_14.txt.gz` | `a1bb606d782c973e784672c6b90a3f11` |
| `n10_sweep_15.txt.gz` | `a91a473a46034db7d448cd2eb6165019` |

## Acknowledgments

The problem, the conjectured formula, the verified range *n* ≤ 8, and
the blow-up upper-bound argument used here at both orders are Raphael
Yuster's; the fractional method that still holds the best general lower
bound is Mohamad Kabiya and Raphael Yuster's. The enumeration rests
entirely on Brendan McKay and Adolfo Piperno's nauty. To Carsten Sinz for
the cardinality encoding, to Cruz-Filipe, Heule, Hunt, Kaufmann and
Schneider-Kamp for LRAT, and to Armin Biere and coauthors for CaDiCaL.
The computation and drafting were AI-assisted as stated in the first
footnote; the adversarial referee's insistence on the credit framing of
§1.3 made this a better and a more honest note.

## References

- **[KY08]** M. Kabiya and R. Yuster, *Packing transitive triples in a
  tournament*, Ann. Comb. **12** (2008), no. 3, 291–306.
  DOI 10.1007/s00026-008-0352-3. Read in full on August 5, 2026,
  from an archived copy (`primary-source-kabiya-yuster-tt3.pdf`,
  retained in the author's private working tree; not redistributed for
  copyright reasons); that copy is the author preprint, and section
  references follow its numbering: the blow-up upper-bound argument is
  §2.4, and the r = 10 fractional LP computation is §3.
- **[MP14]** B. D. McKay and A. Piperno, *Practical graph isomorphism,
  II*, J. Symbolic Comput. **60** (2014), 94–112. Version used here:
  nauty 2.9.3 (`gentourng`).
- **[Dav54]** R. L. Davis, *Structures of dominance relations*, Bull.
  Math. Biophys. **16** (1954), 131–140.
- **[OEIS]** OEIS Foundation Inc., *The On-Line Encyclopedia of Integer
  Sequences*, sequence A000568 (the number of tournaments on n unlabeled
  nodes), https://oeis.org/A000568.
- **[OPG]** Open Problem Garden, *Minimum number of arc-disjoint
  transitive subtournaments of order 3 in a tournament*,
  http://www.openproblemgarden.org/op/minimum_number_of_transitive_subtournaments_of_order_3_in_a_tournament.
  Fetched live August 5, 2026; the entry records no progress beyond
  [KY08].
- **[BFF+24]** A. Biere, T. Faller, K. Fazekas, M. Fleury, N. Froleyks
  and F. Pollitt, *CaDiCaL 2.0*, in: Computer Aided Verification —
  CAV 2024, Lecture Notes in Comput. Sci. **14681**, Springer, 2024,
  133–152. DOI 10.1007/978-3-031-65627-9_7. Version used to produce the
  proofs: CaDiCaL 3.0.1 (`--lrat --no-binary`).
- **[CFHKS17]** L. Cruz-Filipe, M. J. H. Heule, W. A. Hunt Jr.,
  M. Kaufmann and P. Schneider-Kamp, *Efficient certified RAT
  verification*, in: Automated Deduction — CADE-26, Lecture Notes in
  Comput. Sci. **10395**, Springer, 2017, 220–236.
- **[Sin05]** C. Sinz, *Towards an optimal CNF encoding of Boolean
  cardinality constraints*, in: Principles and Practice of Constraint
  Programming — CP 2005, Lecture Notes in Comput. Sci. **3709**,
  Springer, 2005, 827–831.
- **[Yus04]** R. Yuster, *The number of edge-disjoint transitive triples
  in a tournament*, Discrete Math. **287** (2004), 187–191. Also
  arXiv:math/0304180. The concluding remarks (§4: the oriented Turán
  upper-bound construction; the verified range n ≤ 8, with n = 8 by
  computer) were checked verbatim against the arXiv text on August 5,
  2026 (archived copy retained in the author's private working tree;
  not redistributed).
