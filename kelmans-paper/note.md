# Kelmans' 1984 problem on 3-vertex path packings in cubic 3-connected graphs: exhaustive verification through 22 vertices

**Daniel Kirtchakov**
Independent researcher (`05oz`); no institutional affiliation — daniel@halfounce.io — halfounce.io — ORCID [0009-0009-5213-4098](https://orcid.org/0009-0009-5213-4098)

*Draft of August 11, 2026.*

> **Computation and authorship.** The searchers, the independent verifiers,
> and the audits in this work were produced by **Claude** (Anthropic),
> directed by the author, on a single Apple M4 laptop. The certificate
> checkers import only the Python standard library and share no code with
> the searchers; the adversarial referee of §3.4 was a separate agent
> instance given no access to the search pipeline's code and wrote its own
> code throughout. This is a factual methods statement, and it is part of
> the point of the note: the artifacts are designed so that the provenance
> of the *search* is irrelevant to the validity of the *result*. External
> tools used by the pipelines: `geng` from `nauty` 2.9.3 [McKP14], Apple
> clang 17, and Python 3.

> **Prior-art record.** The primary source [Kel11] was read in full (arXiv
> v2; a copy is archived in the author's working tree, not redistributed here, and all statement numbers
> below follow its numbering). A novelty sweep was run on August 5 and
> again on August 11, 2026, the latter immediately before this draft was
> written: the arXiv API (abstracts mentioning P₃-factors or 3-vertex
> paths; *Kelmans* in math.CO; *Akiyama–Kano*), the citing literature of
> [Kel11] through OpenAlex and Semantic Scholar, the Open Problem Garden
> entry [OPG] fetched live, West's REGS page [West] fetched live, and
> general web sweeps. The problem is recorded as open in both problem
> collections, and no computational verification of it at any order was
> found anywhere in the record.

*2020 MSC: Primary 05C70; Secondary 05C40, 05C69, 68V15. Keywords: cubic
graph, 3-connected graph, 3-vertex path packing, P₃-factor, Λ-factor,
Kelmans' problem, Akiyama–Kano conjecture, Reed's domination conjecture,
exhaustive verification, certified computation.*

---

## Abstract

A Λ-packing of a graph is a subgraph all of whose components are 3-vertex
paths, and a Λ-factor is a spanning one; λ(G) denotes the maximum number
of vertex-disjoint 3-vertex paths in G, so that λ(G) ≤ ⌊v(G)/3⌋ always.
Kelmans asked in 1984 whether equality holds for every cubic 3-connected
graph; specialized to v(G) ≡ 0 mod 6 this is the Akiyama–Kano conjecture
that such a graph has a P₃-factor, and a positive answer would give
Reed's domination conjecture for cubic 3-connected graphs. The problem is
open, and no computational verification of it at any order appears in the
record.

We supply one. For every 3-connected cubic graph on at most 22 vertices —
all 6,339,157 of them — λ(G) = ⌊v(G)/3⌋, and the applicable strong forms
of Kelmans' equivalence theorem hold as well: (z2), (z3), (z7), (z8) at
orders 6, 12, 18; (t2) at 8, 14, 20; (f1), (f2) at 4, 10, 16 and (f1) at
22. Those equivalences are constructive, so a single failure at any of
these orders would have yielded an explicit cubic 3-connected graph of
order divisible by 6 with no Λ-factor. None was found. The graphs were
generated with `geng`, and the generated counts agree exactly, at every
order, with the published enumerations of connected cubic graphs and of
3-connected cubic graphs. Two pipelines sharing no code — different
connectivity tests, different search orders, both negative-controlled —
agree on every count and report zero failures, and all 43,580 Λ-factor
certificates in the corpus were re-verified from the `graph6` strings
alone by standard-library checkers sharing no code with the searcher that
produced them (34,429 of them by two such checkers independently). At 24
vertices the search pipeline has completed all 98,101,019 3-connected
cubic graphs with no failure and with counts again matching the published
enumeration, but the independent recount is outstanding; that order is
reported at that strength and no higher. We close with the questions the
computation opens.

---

## 1. Introduction

### 1.1. The question

All graphs here are finite, undirected, and simple. Write v(G) for the
number of vertices of G and Λ for the 3-vertex path P₃. Following
[Kel11], a *Λ-packing* of G is a subgraph all of whose components are
isomorphic to Λ, and a *Λ-factor* is a spanning Λ-packing — what is
elsewhere called a *P₃-factor*. Let λ(G) be the maximum number of
pairwise disjoint 3-vertex paths in G. Counting vertices gives

> (1)  λ(G) ≤ ⌊v(G)/3⌋

for every graph, and the question is when (1) is tight.

> **Problem** (A. Kelmans, 1984; Problem 1.10 of [Kel11]). *Is the
> following claim true?*
>
> (P) *If G is a 3-connected cubic graph, then λ(G) = ⌊v(G)/3⌋.*

A cubic graph has even order, so (P) splits into three cases by the
residue of v(G) modulo 6: for v(G) ≡ 0 the claim is that G has a
Λ-factor; for v(G) ≡ 4 that some G − x has one; for v(G) ≡ 2 that some
G − {x,y} has one. The first of these is the conjecture of Akiyama and
Kano, which we take in the form recorded by West [West] — "when 3
divides n, every 3-connected 3-regular n-vertex graph has a P₃-factor",
there attributed to the survey [AK85] — and it is the form in which the
problem is posed at the Open Problem Garden [OPG]: does every
3-connected cubic graph on 3k vertices admit a partition into k paths on
3 vertices?

Three facts fix the difficulty. First, the Λ-packing problem is NP-hard
in general [HK86] and remains NP-hard already for cubic bipartite planar
graphs [KMZ05], so (P) is not a statement about an easy
optimization problem but about a class on which the optimum is
conjecturally forced. Second, 3-connectivity is not a convenience:
Kelmans [Kel07] constructs infinitely many 2-connected cubic bipartite
planar graphs G with λ(G) < ⌊v(G)/3⌋, so the hypothesis cannot be
weakened by one unit of connectivity. Third, the problem has a
consequence outside path packing. Reed [Reed96] conjectured that a
connected cubic graph G has domination number γ(G) ≤ ⌈v(G)/3⌉; that
conjecture is false for connected and even for 2-connected cubic graphs
[Kel06, KS05], but as Kelmans observes [Kel11, §1], if (P) holds then —
by way of the strong forms of Theorem 1.4, not directly — Reed's
conjecture holds for cubic 3-connected graphs. A *positive* resolution of
(P) therefore settles a domination question as a corollary; a
counterexample would leave Reed's conjecture on this class untouched.

The problem has been open since 1984. Partial results are known. For
every cubic graph λ(G) ≥ ⌈v(G)/4⌉ [KM04], and for connected cubic graphs
this has been improved to λ(G) ≥ (39/152)·v(G) when v(G) ≥ 17 [KMZ08]
and to λ(G) ≥ (3/11)·v(G) when v(G) ≥ 9 [KZ08], as recorded in
[Kel11, 1.3, 1.6, 1.8]. In restricted classes the exact statement is
known: λ(G) = ⌊v(G)/3⌋ for 2-connected claw-free graphs [KKN01], and
claims (z1)–(z5) of Theorem 1.4 below hold for cubic 3-connected
claw-free graphs [Kel07b] (see also [Kel11b]). But the general case is
untouched, and, as far as our sweeps can determine, no exhaustive
verification of (P) at any order has ever been published.

### 1.2. Result

> **Theorem 1.1.** Let G be a 3-connected cubic graph with v(G) ≤ 22.
> Then λ(G) = ⌊v(G)/3⌋. In particular, every 3-connected cubic graph on
> 6, 12, or 18 vertices has a Λ-factor, i.e. admits a partition of its
> vertex set into v(G)/3 paths on 3 vertices.

The statement ranges over all 6,339,157 3-connected cubic graphs of order
at most 22; the counts by order are in the table of §2.1. Theorem 1.1 is
the base claim (P). The verification also establishes the applicable
strong forms of Kelmans' equivalence theorem, which is where its
counterexample-hunting power lies (§1.3).

> **Theorem 1.2.** Let G be a 3-connected cubic graph. Then, in the ranges
> indicated,
>
> - (z2) for v(G) ∈ {6,12,18}: G − e has a Λ-factor for every e ∈ E(G);
> - (z3) for v(G) ∈ {6,12,18}: for every e ∈ E(G) some Λ-factor of G
>   contains e;
> - (z7) for v(G) ∈ {6,12,18}: G − X has a Λ-factor for every X ⊆ E(G)
>   with |X| = 2;
> - (z8) for v(G) ∈ {6,12,18}: G − L has a Λ-factor for every 3-vertex
>   path L in G;
> - (t2) for v(G) ∈ {8,14,20}: G − {x,y} has a Λ-factor for every
>   xy ∈ E(G);
> - (f1) for v(G) ∈ {4,10,16,22}: G − x has a Λ-factor for every
>   x ∈ V(G);
> - (f2) for v(G) ∈ {4,10,16}: G − {x,e} has a Λ-factor for every
>   x ∈ V(G) and every e ∈ E(G) not incident with x.

Kelmans states (f2) without an incidence restriction; restricting it here
to edges not incident with x loses nothing, and for the reason his own
proof gives: if e is incident with x then G − {x,e} = G − x, so the
incident case is (f1) [Kel11, 3.21].

The evidence for both theorems is a complete search: every 3-connected
cubic graph of each order was generated, and for each the relevant
existence questions were decided exactly — not estimated, not sampled —
by an exhaustive procedure (§2.2). The result was then recounted end to
end by a second pipeline written independently of the first, and the
whole was confirmed by an adversarial referee (§3).

One further order was searched but is *not* part of Theorems 1.1 and 1.2,
and is recorded separately at the strength it has reached.

> **Proposition 1.3.** The search pipeline reports λ(G) = v(G)/3 — that
> is, a Λ-factor — for every one of the 98,101,019 3-connected cubic
> graphs on 24 vertices, with no failure on any graph. The enumeration
> underlying that sweep was audited independently (job accounting
> reconstructed from the run records, generated counts matched against the
> published enumerations, zero failure lines in any output), but the
> graphs themselves have not been re-solved by the independent pipeline.
> This order is asserted at exactly that strength.

### 1.3. Why the strong forms are the counterexample hunt

Theorem 1.2 is not a collection of sanity checks. Its statements are the
ones Kelmans proves equivalent to (P) as universal claims over the class
of cubic 3-connected graphs.

> **Theorem 1.4** (Kelmans [Kel11, 3.1]). Read as universal statements
> over the class of cubic 3-connected graphs, the nineteen claims
> (z1)–(z9), (t1)–(t4), (f1)–(f6) — conditioned on v(G) ≡ 0, 2, 4 mod 6
> respectively, and including the seven forms listed in Theorem 1.2 —
> are pairwise equivalent.

Two remarks on the statement. Claim (P) is not one of the nineteen, but
is equivalent to them, as Kelmans records [Kel11, §1]: (z1) is exactly
the v(G) ≡ 0 case of (P), so (P) implies (z1), while conversely (z1)
yields (t1) and (f1) by the theorem, and those are stronger than the
v(G) ≡ 2 and v(G) ≡ 4 cases of (P). And the quantification is over the
class: the equivalences hold between claims each universally quantified
over all cubic 3-connected graphs, not graph by graph. A single graph
failing one strong form is therefore not by itself a graph failing
another; what it yields is a construction, and that is the next point.

The equivalences are proved by explicit graph compositions — the
operations AaσbB and Y(·) and the graph-compositions B{·} of [Kel11, §2],
all of which preserve cubicity and 3-connectivity [Kel11, 2.1–2.3] — and
Kelmans draws the consequence himself: he gives several different proofs
of 3.1, so that "if there is a counterexample C to one of the above
claims, then these different proofs provide different constructions of
counterexamples to the other claims in 3.1" [Kel11, §1]. The implications
therefore run constructively in the direction that matters here: a single
cubic 3-connected graph violating any one of (z2), (z3), (z7), (z8),
(t2), (f1), or (f2) can be converted, by those compositions, into an
explicit cubic 3-connected graph of order ≡ 0 mod 6 with no Λ-factor,
i.e. into a counterexample to (P) and to the Akiyama–Kano conjecture.

This changes what the orders v(G) ≡ 2, 4 mod 6 are worth. They are not
orders at which the factor question is vacuous; they are orders at which
a cheap local test — delete an edge's two endpoints, or one vertex, and
ask for a factor of the remainder — is a valid search for a
counterexample to the factor case. Of the 6,339,157 graphs covered by
Theorem 1.1, only 30,527 have order divisible by 3; the strong forms are
what makes the other 99.5% of the corpus evidence rather than context.

Kelmans also records where the strong forms stop [Kel11, (r1)–(r8)], and
the boundary is close. Claim (z7) is false for |X| = 3: a 3-edge cut
whose sides have orders not divisible by 3 obstructs any Λ-factor of
G − X. Claim (z8) is tight for two disjoint paths — [Kel11, 6.1]
constructs cubic graphs R_s with v(R_s) = 12s, cyclically 6-connected for
s ≥ 2 (the smallest member has c(R₁) = 5, [Kel11, 6.1(a2)]), having
disjoint 3-vertex paths L, L′ for which R_s − (L ∪ L′) has no
Λ-factor, while R_s − L − e has one for every edge e and every 3-vertex
path L of R_s − e. Since v(R₁) = 12, the exact boundary of the phenomenon
lies inside the verified range: the sweep confirms (z8) for every single
3-vertex path at order 12, and Kelmans' construction exhibits the
two-path failure at the same order. A verification that reported success
on a strong form known to be false would be diagnostic of a broken
pipeline; none of the forms tested here is known to be false in the
tested range, and none failed.

### 1.4. What is not claimed

We do not claim to resolve Kelmans' problem, the Akiyama–Kano conjecture,
or Reed's conjecture for cubic 3-connected graphs. Each is a statement
about an infinite class and is untouched by any finite computation; what
a proof would have to supply is discussed in §6. We do not claim a bound
on the order of a putative counterexample beyond the one Theorem 1.1
gives, namely that none has at most 22 vertices. We do not claim the
strong forms outside the orders listed in Theorem 1.2: in particular (f2)
was not tested at order 22, and (z7) and (z8) were not tested at order
24. We do not claim order 24 at the strength of Theorem 1.1: Proposition
1.3 is a report of a completed search whose independent recount has not
been performed, and it is stated in those terms deliberately. Finally, we
claim no priority over the mathematics: the problem, the equivalence
theorem, the tightness constructions, and the link to Reed's conjecture
are all Kelmans' [Kel11], and the conjecture in its P₃-factor form is
Akiyama and Kano's [AK85].

---

## 2. The verification

### 2.1. Enumeration

Each order was swept over the output of `geng` from `nauty` 2.9.3
[McKP14], invoked as `geng -q -c -d3 -D3 n`, which emits one `graph6`
string per isomorphism class of connected cubic graph on n vertices; the
large orders were split into residue classes by `geng`'s `res/mod`
slicing. Each pipeline then applied its own 3-connectivity filter. No
graph was excluded on any other ground, and no symmetry reduction beyond
`geng`'s isomorph rejection was used at any stage.

The completeness of the enumeration is the load-bearing external
assumption of this note (§5), and it is supported by count agreement at
every order against two independent published sources. The number of
connected cubic graphs read matches the published enumeration of
Brinkmann, Goedgebeur, and McKay [BGM11] — whose Table 1 gives 7,319,447
at 22 vertices and 117,940,535 at 24 — and equivalently OEIS A002851. The
number surviving the 3-connectivity filter matches the published counts
of 3-connected cubic graphs: through 20 vertices those of McKay and Royle
[McKR86], and through 24 vertices OEIS A204198, whose terms

> 0, 1, 2, 4, 14, 57, 341, 2828, 30468, 396150, 5909292, 98101019, …

(indexed by half the order, with a(11) and a(12) credited to Ed Wynn,
2023) reproduce our filtered counts exactly at every order. The two
checks are independent of each other in the useful direction: the first
tests the generator, the second tests the filter.

| n | connected cubic | 3-connected | strong forms verified | recount |
|---:|---:|---:|---|---|
| 4 | 1 | 1 | (f1), (f2) | yes |
| 6 | 2 | 2 | (z2), (z3), (z7), (z8) | yes |
| 8 | 5 | 4 | (t2) | yes |
| 10 | 19 | 14 | (f1), (f2) | yes |
| 12 | 85 | 57 | (z2), (z3), (z7), (z8) | yes |
| 14 | 509 | 341 | (t2) | yes |
| 16 | 4,060 | 2,828 | (f1), (f2) | yes |
| 18 | 41,301 | 30,468 | (z2), (z3), (z7), (z8) | yes |
| 20 | 510,489 | 396,150 | (t2) | yes |
| 22 | 7,319,447 | 5,909,292 | (f1) | yes |
| **≤ 22** | **7,875,918** | **6,339,157** | | |
| 24 | 117,940,535 | 98,101,019 | — (base claim only) | *pending* |

*Coverage by order. The "connected cubic" column is the generator's
output and matches [BGM11] and OEIS A002851; the "3-connected" column is
what survives each pipeline's own filter and matches OEIS A204198 at
every order and [McKR86] at orders 10 through 20. Every graph counted in
the third column was decided for the base
claim (P) and for the strong forms listed. The last row is Proposition
1.3: complete on the search side, not yet recounted independently.*

### 2.2. Deciding each graph

For a cubic graph on n ≤ 31 vertices the whole question fits in machine
words, and both pipelines decide it exactly rather than approximately.
The base claim asks for a set S of n mod 3 vertices such that G − S has a
Λ-factor; a Λ-factor is found, or proved absent, by depth-first search
over vertex triples (a,b,c) with ab, bc ∈ E(G), extending a partial
packing until the covered set is everything, with a hash cache of
covered-set masks already shown to admit no completion. The strong forms
are decided by running the same factor decision on each of the linearly
or quadratically many derived graphs: G − e and G-with-e-forced for (z2),
(z3); G − {e,f} over all C(|E|,2) pairs for (z7); G − V(L) over all
3-vertex paths for (z8); G − {x,y} over all edges for (t2); G − x over
all vertices for (f1); G − {x,e} for (f2). Because the procedure is
exhaustive, a negative answer is a proof of non-existence, which is why a
single failure anywhere would have been the object of interest rather
than a nuisance.

The second pipeline decides the same questions by deliberately different
means: connectivity by union–find rather than bitmask breadth-first
search; 3-vertex-path triples precomputed into per-vertex tables rather
than generated on the fly; depth-first branching on the highest uncovered
vertex rather than the lowest; the base claim by explicit iteration over
avoided sets rather than by a skip counter; and a four-way probed failure
cache rather than a single-slot one. It shares no code with the first.
Agreement between the two is therefore agreement between two search
orders and two data structures, not between two runs of one program.

### 2.3. Certificates

A completed packing is a short, checkable object, and the sweeps emit it:
one line per certified graph carrying the `graph6` string, the list of
vertex triples forming the paths, and the avoided vertices, for example

```
CERT U???????C?W?[?Y?C`Cc?Aa?X??BG?I_?Ao?@K?? | 10-0-11 12-1-13 2-14-5 15-3-17 4-16-6 18-7-19 20-8-21 | 9
```

at order 22, where the seven triples and the single avoided vertex 9
partition the 22 vertices. Certificates were stored for every 3-connected
cubic graph through order 18 and for a fixed sample at higher orders
(43,580 lines through order 22; 9,776 more at order 24). A checker
re-derives everything from the `graph6` string alone: it decodes the
string with its own decoder, verifies that the graph is simple and cubic,
optionally verifies membership of the string in a freshly generated
`geng` stream for that order and re-proves 3-connectivity by exhaustive
deletion of vertex pairs, checks that each listed triple is a path of the
graph, and checks that the triples and the avoided vertices partition the
vertex set with |avoided| = n mod 3. Certificates are not the primary
evidence — full coverage rests on the searches themselves — but they make
spot-checking cheap for a reader, and they are regenerable: the searchers
are deterministic, so any certificate reproduces from the recorded
command.

---

## 3. Independent recount, controls, and referee

### 3.1. The recount

The second pipeline re-ran the sweep from the generator forward. Through
order 16 it re-solved the full stream with all strong forms enabled; at
order 18 with (z2), (z3), (z7), (z8); at order 20 with (t2); at order 22
with (f1), in eight generator slices. At every order the count of graphs
read and the count surviving the 3-connectivity filter agree with the
first pipeline and with the published enumerations, and the number of
base-claim failures and strong-form failures is zero on every slice. At
order 22 the eight slices read

> 518,580 + 670,736 + 982,556 + 1,068,280 + 1,569,040 + 879,959 + 978,267
> + 652,029 = 7,319,447

graphs and kept 5,909,292, both exactly the published values; the
order-22 recount and its certificate cross-check together consumed under
two hours of single-core time on the laptop.

### 3.2. Certificate cross-checks

The certificate corpus was re-verified across the pipeline boundary. All
30,468 certificates at order 18, all 3,961 at order 20, and all 5,904 at
order 22 — 40,333 in total — were accepted by the second pipeline's own
checker, with zero rejections; at orders 20 and 22 the check included
re-proving 3-connectivity from the `graph6` string, and at all three
orders it included membership in a freshly regenerated generator stream
(41,301, 510,489, and 7,319,447 lines respectively, each line count
re-derived at check time). The 3,247 certificates at orders ≤ 16 were
accepted by the first pipeline's independent standard-library checker,
and those graphs were in addition re-solved from scratch by the second
pipeline.

### 3.3. Negative controls

A sweep that only ever reports success proves nothing about its own
failure path, so both tools were forced to fail. With the 3-connectivity
filter disabled, the base sweep over all *connected* cubic graphs of
orders 10 through 16 reports exactly one failure: the 16-vertex graph
with `graph6` string `O???E?oBEAWOKGK_@o?W_`, which has a cut vertex. The
same graph had been identified independently by the first pipeline's own
control, and a third, unrelated brute-force implementation confirms
λ = 4 < 5 for it; the two pipelines agree on the unique sub-3-connected
failure in that range. With the filter disabled the strong-form paths
fire as well: no failure at order 8, where none exists; 54 at order 10
(2 of type (f1), 52 of (f2)); 253 at order 12, spread over all four (z·)
paths (4 of (z2), 8 of (z3), 106 of (z7), 135 of (z8)); 145 of (t2) type
at order 14; and 15,691 at order 16 (317 of (f1), 15,374 of (f2); the captured
control log's own header line prints 15692 for this total, an arithmetic slip in
the log, not in the count — its `RSUMMARY` two lines below reads `sfail=15691`). Each
checker was likewise run on deliberately doctored certificates, one
corruption per line: a non-path triple, a cover gap, an overlapping
triple, a valid partition of sub-maximum shape, a `graph6` string with a
trailing character, a `graph6` string with a flipped character, a valid
certificate for a non-canonical relabelling of the graph (a string the
generator never emits), and a genuine Λ-factor certificate for a
connected cubic graph that is not 3-connected. Each corruption is
rejected by the gate that targets it, with a nonzero exit code, while
the intact certificate in the same file is accepted. The membership gate
is `refcert.py`'s alone: run with `--g6set` and `--check3c` it rejects
all eight, whereas `verify_cert.py`, which tests no membership in a
generator stream, rejects seven and accepts the relabelling with exit
code 0 (it exits on the first violation, so the control is run one line
at a time). Two controls on the controls confirm the diagnosis, since
disabling the membership test admits the relabelling and nothing else,
and disabling the 3-connectivity test admits the sub-3-connected
certificate and nothing else. All controls in this subsection were
re-run on the drafting date against the current binaries and checkers.

### 3.4. The adversarial referee

The result rests on an adversarial referee pass by a separate agent
instance under an explicit independence rule: every load-bearing check
used code written in that session, sharing nothing with the search
pipeline beyond the `graph6` format specification. The referee wrote the
second pipeline, ran the recount and the cross-checks and the controls
described above, recomputed every count sum mechanically from the raw
per-slice summary lines rather than accepting reported totals, and
fetched the published enumeration values itself. On this protocol the
range v(G) ≤ 20 was confirmed on August 6, 2026, and order 22 was
recounted to completion on August 11, 2026; Theorems 1.1 and 1.2 are
stated at exactly the strength those passes support. Order 24 was not
recounted. What the referee did establish there is the completeness of
the search side — that every job finished successfully, that the
generated and filtered counts equal the published enumeration values, and
that no output file anywhere contains a failure line — which is why
Proposition 1.3 is phrased as a report of a completed search rather than
as a verification.

---

## 4. Certification

The permanent record of the computation is the part a reader can check
without us: the two certificate checkers in source form, the recorded
command line for every sweep and every generator slice at every order,
the per-slice summary outputs, the full certificate corpus, the
negative-control inputs and outputs, and the referee's verdict records.
It ships with this note in the program's public certificate repository
*Certify* (<https://github.com/05oz/certify>; concept DOI
[10.5281/zenodo.21799111](https://doi.org/10.5281/zenodo.21799111)), as
Part I, version DOI
[10.5281/zenodo.21897011](https://doi.org/10.5281/zenodo.21897011). The
two searchers are specified in §2.2 but are not part of that deposit, and
we say so rather than imply otherwise: what is deposited is what
re-checks their output without them, which is every positive answer they
gave. Nothing large needs to be archived either — the graph streams are
outputs of `geng` and regenerate from the recorded commands. To replay:
checking any certificate, or the whole corpus, requires only CPython;
regenerating any graph stream requires `nauty` 2.9.3. The full sweep
through order 22 is about an hour and a half of single-core time per
pipeline; order 24 was about 29 hours of completing-run time on the
search side, and about 48 hours of machine time once the slices that
exceeded their first time limit and were rerun are counted.

---

## 5. The trusted base

What a skeptic must believe, separated from what they can replay.

*Machine-checked, replayable:* the decision, for each of the 6,339,157
graphs, of the base claim and of the strong forms listed in Theorem 1.2,
by each of two pipelines sharing no code; the count of graphs read and of
graphs kept at every order, by both pipelines and against two published
enumerations; all 43,580 certificates through order 22, re-verified from
the `graph6` strings alone, 34,429 of them by two unrelated checkers; and
the negative controls, which both pipelines' failure paths pass.

*Trusted:*

1. **Completeness of the enumeration.** That `geng -c -d3 -D3 n` emits at
   least one representative of every isomorphism class of connected cubic
   graph on n vertices is assumed, not proved here. It is the only
   assumption a counterexample could hide behind, and the mitigation is
   count agreement with the independent published
   enumerations — [BGM11] at every order and [McKR86] at orders 10 through 20,
   its tables stopping there — values obtained by different
   generators (`minibaum`, `snarkhunter`, and McKay and Royle's
   constructions) — and, for the filtered counts, with OEIS A204198. A
   generator that missed a class would have to miss it while still
   producing the published totals.
2. **The 3-connectivity filters.** Both pipelines test 3-connectivity
   directly, by verifying that G, every G − u, and every G − {u,v} is
   connected, rather than by any equivalence between vertex and edge
   connectivity for cubic graphs. The two implementations differ
   (breadth-first search on bitmasks; union–find) and agree on every
   count; and the standard-library checker's own 3-connectivity routine,
   driven over the raw generator stream by a separate driver, reproduced
   the filtered counts at orders 8 through 16, closing the question in
   both directions at those orders.
3. **The correctness of the exhaustive search.** A "no" from either
   searcher is a claim of non-existence and is not certifiable by a short
   witness. Nothing in Theorems 1.1 and 1.2 depends on such a "no" being
   right — every reported outcome is a "yes", witnessed by a packing —
   but the *absence of failures* does depend on the searchers not
   silently skipping graphs, which is why the counts, and not only the
   verdicts, are cross-checked at every order.
4. **The equivalences of Theorem 1.4**, on which the
   counterexample-hunting reading of the strong forms rests. These are
   Kelmans' theorems, proved on paper in [Kel11]; they are not
   machine-checked here.
5. **CPython, the C compiler, the operating system, and the hardware.**

Neither searcher is in the trusted base in the usual sense: every
positive answer carries a packing that a reader can re-check without
trusting the program that found it.

---

## 6. Questions

### 6.1. What a structural proof would need

The computation supplies no tightness anywhere. Every one of the
6,339,157 graphs meets the bound (1), and meets it after the deletions
demanded by the strong forms as well; nothing in the range distinguishes
hard instances from easy ones. That is evidence for (P) and
simultaneously evidence that a proof will not come from extremal
considerations at small orders.

Theorem 1.4 says a proof needs only one of the equivalent claims, and the
local ones look most tractable: (t2) asserts that G − {x,y} has a
Λ-factor for *every* edge xy, and (f1) that G − x has one for *every*
vertex — universally quantified statements about a single deletion, the
natural shape for a discharging or a minimal-counterexample argument. The
known obstructions say where such an argument must be careful: by [Kel11,
(r1)] a 3-edge cut with both sides of order not divisible by 3 kills
Λ-factors of G − X, and by [Kel11, (r4)] claim (t2) is false for
non-adjacent x, y. Adjacency and the divisibility of the two sides of a
cut are exactly the hypotheses that cannot be dropped.

> **Question 6.1.** Does (P) reduce to cyclically 4- or 5-connected cubic
> graphs? That is, do the compositions of [Kel11, §2] let a minimum
> counterexample be assumed to have large cyclic connectivity, and if so,
> does the Λ-factor problem become tractable on that class — where, by
> [Kel11, 6.1], cyclically 6-connected examples with delicate behaviour
> already exist, from 24 vertices upward?

> **Question 6.2.** Kelmans proves (z1)–(z5) for cubic 3-connected
> *claw-free* graphs [Kel07b, Kel11b]. The class is narrow: in a cubic claw-free
> graph the three neighbours of any vertex cannot be pairwise
> non-adjacent, so every vertex lies in a triangle. What is the weakest
> local-structure hypothesis — a bound on the number of independent
> claws, say — under which the claw-free argument still runs?

### 6.2. The strong forms' status

Theorem 1.2 is complete for the forms it lists and silent elsewhere.
Three gaps are immediate. Claim (f2) was tested only through order 16; at
order 22 its cost is the number of vertex–edge pairs times a factor
decision, an order of magnitude above (f1), and it was not run. Claims
(z7) and (z8) have never been tested at order 24, which is the first
order divisible by 6 beyond the verified range and therefore the first
place where a (z·) failure would be a direct counterexample rather than a
converted one. And the remaining forms of Theorem 1.4 — (z4), (z5), (z6),
(z9), (t1), (t3), (t4), (f3)–(f6) — have not been tested at any order.
They are equivalent to (P), so testing them adds no logical strength, but
they are different searches with different failure modes, and one of them
may be cheap enough to push several orders past 22 on its own.
Identifying which is a concrete question.

> **Question 6.3.** Among the claims of Theorem 1.4, which admits the
> cheapest exhaustive test per graph at order n? A form testable in time
> comparable to a single factor decision would move the frontier further
> than any improvement to the base search.

### 6.3. Where the frontier sits

The binding constraint is enumeration, not search. Order 24 took about 29
hours of completing-run single-core time on the search side for
117,940,535 generated graphs, a throughput near a thousand graphs per
second; the outstanding
work at that order is the independent recount, which is a comparable cost
and would raise Proposition 1.3 to the strength of Theorem 1.1. Order 26
requires generating 2,094,480,864 connected cubic graphs and deciding
1,782,392,646 of them — roughly three weeks of single-core time per
pipeline at the order-24 throughput, and more than that in truth, since
per-graph cost grows with order; it is embarrassingly parallel across
generator slices and so is a matter of core-days, not of algorithms.
Order 26 is ≡ 2 mod 6, so it tests (t2); order 28 (≡ 4) tests (f1) and
has 35,085,504,243 graphs to decide.

The real wall is at order 30, the next order divisible by 6 after 24.
OEIS A204198 currently stops at 28 vertices, so beyond that order there
is no published count of 3-connected cubic graphs to check a generator
against — and count agreement with an independent enumeration is the
mitigation that makes the trusted base of §5 tolerable. Past 28 vertices
a sweep would be asserting its own completeness.

> **Question 6.4.** Can the frontier be advanced much further on a
> restricted class? The obstructions of [Kel11, (r1)–(r4)] are cuts and
> short cycles, which suggests looking where neither is available; but
> the suggestion is not safe, since [Kel11, (r5), (r6)] exhibit
> obstructions to the (f·) forms in cubic 3-connected graphs with no
> 3-cycles and no 4-cycles. Generators for sparse families — `genreg`
> [Mer99], `snarkhunter` [BGM11] — reach far higher orders than the full
> cubic enumeration does, because the families are far sparser. A sweep
> of, say, all cyclically 5-connected cubic graphs of order ≡ 0 mod 6 up
> to 34 or 36 vertices looks feasible today, and would test the
> conjecture on the class where the compositions of [Kel11, §2] have the
> least room to work.

---

## Acknowledgments

The problem is Alexander Kelmans'; the equivalence theorem, the tightness
constructions, and the connection to Reed's domination conjecture that
give this verification its meaning are all his, and this note is a
computation performed inside his framework. The P₃-factor form of the
conjecture is due to Jun-ichi Akiyama and Mikio Kano, and its continued
visibility owes much to Douglas West's problem pages and to the Open
Problem Garden. The enumeration rests on Brendan McKay's `nauty`, and the
count cross-checks on the published cubic-graph enumerations of
Brinkmann, Goedgebeur, and McKay and of McKay and Royle, and on the OEIS.
The computation and drafting were AI-assisted as stated in the first
footnote; the adversarial referee protocol of §3.4, its rule that a claim
be stated at exactly the strength its recount supports, and its rule that
a computation-only note close with the questions it opens shaped this
note's final form.

---

## References

**[AK85]** J. Akiyama and M. Kano, *Factors and factorizations of graphs
— a survey*, J. Graph Theory **9** (1985), no. 1, 1–42. Updated and
augmented in: *Factors and Factorizations of Graphs*, Lecture Notes in
Math. **2031**, Springer, 2011.

**[BGM11]** G. Brinkmann, J. Goedgebeur and B. D. McKay, *Generation of
cubic graphs*, Discrete Math. Theor. Comput. Sci. **13** (2011), no. 2,
69–80. Table 1 supplies the connected cubic counts used here; the
generator is `snarkhunter`.

**[HK86]** P. Hell and D. G. Kirkpatrick, *Packings by complete bipartite
graphs*, SIAM J. Algebraic Discrete Methods **7** (1986), no. 2,
199–209.

**[KKN01]** A. Kaneko, A. Kelmans and T. Nishimura, *On packing 3-vertex
paths in a graph*, J. Graph Theory **36** (2001), 175–197.

**[Kel06]** A. Kelmans, *Counterexamples to the cubic graph domination
conjecture*, arXiv:math/0607512 (2006).

**[Kel07]** A. Kelmans, *Packing 3-vertex paths in 2-connected graphs*,
arXiv:0712.4151 (2007); also RUTCOR Research Report RRR 21–2005, Rutgers
University (2005).

**[Kel07b]** A. Kelmans, *Packing 3-vertex paths in claw-free graphs*,
arXiv:0711.3871 (2007).

**[Kel11]** A. Kelmans, *Packing 3-vertex paths in cubic 3-connected
graphs*, arXiv:0910.2766v2 (July 25, 2011); the text records acceptance
by Discrete Math. on August 14, 2009, but no journal version has
appeared, and the arXiv text is the version of record used here. Problem
1.10 is the 1984 problem; Theorem 3.1 is the equivalence theorem; §6 is
the R_s construction.

**[Kel11b]** A. Kelmans, *Packing 3-vertex paths in claw-free graphs and
related topics*, Discrete Appl. Math. **159** (2011), no. 2–3, 112–127.

**[KM04]** A. Kelmans and D. Mubayi, *How many disjoint 2-edge paths must
a cubic graph have?*, J. Graph Theory **45** (2004), 57–79.

**[KMZ05]** A. Kosowski, M. Małafiejski and P. Żyliński, *Parallel
processing subsystems with redundancy in a distributed environment*, in:
Parallel Processing and Applied Mathematics (PPAM 2005), Lecture Notes in
Comput. Sci. **3911**, Springer, 2006, 1002–1009; cited in [Kel11] for
the NP-hardness of 3-vertex path packing on cubic bipartite planar
graphs.

**[KMZ08]** A. Kosowski, M. Małafiejski and P. Żyliński, *Tighter bounds
on the size of a maximum P₃-matching in a cubic graph*, Graphs Combin.
**24** (2008), no. 5, 461–468.

**[KS05]** A. V. Kostochka and B. Y. Stodolsky, *On domination in
connected cubic graphs*, Discrete Math. **304** (2005), no. 1–3, 45–50.

**[KZ08]** A. Kosowski and P. Żyliński, *Packing three-vertex paths in
2-connected cubic graphs*, Ars Combin. **89** (2008). (The bound quoted
here is the one recorded as [Kel11, 1.8].)

**[McKR86]** B. D. McKay and G. F. Royle, *Constructing the cubic graphs
on up to 20 vertices*, Ars Combin. **21A** (1986), 129–140. Author's
copy: <https://users.cecs.anu.edu.au/~bdm/papers/Gobstoppers.pdf>; the
connectivity tables there give the 3-connected counts used above.

**[McKP14]** B. D. McKay and A. Piperno, *Practical graph isomorphism,
II*, J. Symbolic Comput. **60** (2014), 94–112. Version used: `nauty`
2.9.3 (`geng`).

**[Mer99]** M. Meringer, *Fast generation of regular graphs and
construction of cages*, J. Graph Theory **30** (1999), 137–146.
(`genreg`.)

**[OPG]** *Partition of a cubic 3-connected graph into paths of length
2*, Open Problem Garden, posed by A. Kelmans, posted March 4, 2013,
<http://www.openproblemgarden.org/op/partition_of_a_cubic_3_connected_graphs_into_paths_of_length_2>,
accessed 2026-08-11.

**[Reed96]** B. Reed, *Paths, stars and the number three*, Combin.
Probab. Comput. **5** (1996), 277–295.

**[West]** D. B. West, *Factors in regular graphs*, REGS problem page,
<https://dwest.web.illinois.edu/regs/facreg.html>, accessed 2026-08-11.
