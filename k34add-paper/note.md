# The extremal graph for k(3,4) = r(I₃,L₄) = 21 is not unique: thirteen rigid witnesses, and a forced Paley tournament

**Daniel Kirtchakov**
Independent researcher (`05oz`); no institutional affiliation — daniel@halfounce.io — halfounce.io — ORCID [0009-0009-5213-4098](https://orcid.org/0009-0009-5213-4098)

*Addendum to Part G (Certify, version DOI [10.5281/zenodo.21890619](https://doi.org/10.5281/zenodo.21890619)). Draft of August 11, 2026.*

> **Computation and authorship.** All witnesses, checkers, and enumerations
> in this note were produced by **Claude** (Anthropic), directed by the
> author, on a single Apple M4 laptop. The three shipped checkers import only
> the Python standard library and share no code with the search that produced
> the witnesses; the tournament and rigidity facts were re-established here by
> code written from scratch. This addendum uses no propositional solver:
> every claim is a finite check a reader can rerun.

> **Prior-art record.** This note answers Question 8.1 of the companion
> determination [PartG] of k(3,4) = 21. The value was absent from the
> literature before [PartG]: the Erdős problems entry [Blo] (#112) records no
> exact k(n,m), and [IRW21] remains the only paper on r(Iₘ,Lₙ). A novelty
> sweep on the drafting date, August 11, 2026, found nothing on the number of
> extremal {I₃,TT₄}-free graphs on 20 vertices, which is a fortiori new.

*2020 MSC: Primary 05C55; Secondary 05C20, 05D10, 68V15. Keywords: oriented
graph, Ramsey number, transitive tournament, independent set, extremal graph,
Paley tournament, rigidity, certified computation.*

---

## Abstract

The companion note [PartG] determines the Erdős–Rado oriented Ramsey number
k(3,4) = r(I₃,L₄) = 21 by an explicit {I₃,TT₄}-free oriented graph W on 20
vertices together with a certified exhaustion at 21 vertices, and asks
(Question 8.1) whether W is the unique such graph. We answer in the negative.
There are at least **thirteen** pairwise non-isomorphic {I₃,TT₄}-free oriented
graphs on 20 vertices, and every one of the thirteen is **rigid** (trivial
automorphism group), so the extremal configuration is far from a single
symmetric object. We record the local structure they share as a short
forcing lemma: in any {I₃,TT₄}-free oriented graph a vertex has at most 7
non-neighbours, and a vertex with exactly 7 carries a copy of the Paley
tournament QR₇ = Cay(ℤ₇,{1,2,4}) as its non-neighbourhood. Finally the
algebraic route falls short: the largest {I₃,TT₄}-free tournament blow-up has
only 14 vertices, six short of the extremal order, and the thirteen exhibited
witnesses are rigid rather than Cayley. We close with the sharpened question
of whether a QR₇ block is unavoidable in every witness.

## 1. The question

An *oriented graph* is a loopless digraph with at most one arc between any two
vertices. Write Iₙ for the independent set on n vertices and TTₘ (equivalently
Lₘ) for the transitive tournament on m vertices; call an oriented graph *free*
if it contains neither I₃ nor TT₄. For a vertex w let N⁺(w), N⁻(w), I(w) be its
out-neighbours, in-neighbours, and non-neighbours, and call
(p,q,s) = (|N⁺(w)|,|N⁻(w)|,|I(w)|) the *type* of w, so p+q+s = |V|−1. The
companion note [PartG] proves k(3,4) = r(I₃,L₄) = 21: every oriented graph on
21 vertices contains an I₃ or a TT₄, and the explicit 20-vertex graph W of its
Table 1 is free. Its Question 8.1 asks:

> *Is W the unique free oriented graph on 20 vertices up to isomorphism? If
> not, what is the number of extremal graphs, and does any admit an algebraic
> description?*

The first part has a clean negative answer.

**Theorem 1.1.** *There are at least thirteen pairwise non-isomorphic free
oriented graphs on 20 vertices. Every one of the thirteen is rigid: its
automorphism group is trivial. In particular W is not the unique 20-vertex
extremal graph.*

The thirteen graphs are W itself together with twelve further free graphs; all
thirteen are printed as arc lists with the artifacts. Each of the thirteen is
in particular not vertex-transitive, since a vertex-transitive graph on
n ≥ 2 vertices has |Aut| ≥ n. We prove Theorem 1.1 by direct verification
(§2); the local structure that the thirteen share is explained by the forcing
lemma of §3; and the sense in which the algebraic construction falls short is
made precise in §4.

## 2. The witnesses

Table 1 lists the thirteen graphs by three isomorphism invariants: the number
of arcs, the degree sequence of the non-adjacency graph N̄ (whose edges are the
non-adjacent pairs, so the N̄-degree of w is s = |I(w)|), and the number of
vertices of type s = 7. By Lemma 3.1 below the last column equals the number of
induced QR₇ blocks.

| witness | arcs | N̄-degree sequence | #{s=7} = #QR₇ blocks |
|---|---|---|---|
| w₁ = W | 126 | 7¹¹ 6⁶ 5³ | 11 |
| w₂ | 125 | 7¹² 6⁶ 5² | 12 |
| w₃ | 128 | 7⁶ 6¹² 5² | 6 |
| w₄ | 125 | 7¹² 6⁶ 5² | 12 |
| w₅ | 126 | 7¹¹ 6⁶ 5³ | 11 |
| w₆ | 123 | 7¹⁴ 6⁶ | 14 |
| w₇ | 126 | 7⁹ 6¹⁰ 5¹ | 9 |
| w₈ | 126 | 7¹² 6⁴ 5⁴ | 12 |
| w₉ | 124 | 7¹⁴ 6⁴ 5² | 14 |
| w₁₀ | 127 | 7⁸ 6¹⁰ 5² | 8 |
| w₁₁ | 124 | 7¹³ 6⁶ 5¹ | 13 |
| w₁₂ | 125 | 7¹³ 6⁴ 5³ | 13 |
| w₁₃ | 125 | 7¹¹ 6⁸ 5¹ | 11 |

*Table 1. The thirteen free graphs on 20 vertices. Even this coarse
fingerprint separates all thirteen: no two rows agree in all three columns
(e.g. w₁ and w₅ share the first and second, but their full relation matrices
differ; see the certification). Arc counts range over 123–128 and the number
of QR₇ blocks over 6–14.*

Each wᵢ was verified free by an exhaustive test over all C(20,3) = 1140 triples
(none independent) and all C(20,4) = 4845 quadruples (none a TT₄: a quadruple
is a TT₄ exactly when its six pairs are all adjacent and its four in-set
out-degrees are 0,1,2,3). Rigidity, |Aut(wᵢ)| = 1, was certified two
independent ways: Weisfeiler–Leman colour refinement reaches twenty distinct
colours, so any automorphism fixes every vertex; and an explicit automorphism
backtracker returns count 1. Pairwise non-isomorphism was decided by a
canonical form read off the discrete refinement, and cross-checked by the
invariant fingerprint of Table 1, which already separates all thirteen; no two
are isomorphic.

**Remark 2.1.** The thirteen are only a lower bound on the extremal
population. They were obtained by completing random partial orientations to
free graphs and discarding isomorphic duplicates; in that sampling every
completion that survived deduplication was a new isomorphism class, which
suggests — but does not prove — that the family is large. Theorem 1.1 claims
only what the thirteen exhibited certificates establish.

## 3. A forced Paley block

The thirteen witnesses have no global symmetry, yet they share a rigid local
feature, visible in the last column of Table 1: each carries several induced
copies of the Paley tournament. This is forced by freeness alone.

**Lemma 3.1 (QR₇ forcing).** *Let D be a free oriented graph and w a vertex.
Then I(w) induces a tournament with no transitive subtournament on 4 vertices;
consequently |I(w)| ≤ 7, and if |I(w)| = 7 then I(w) induces a tournament
isomorphic to the Paley tournament QR₇ = Cay(ℤ₇,{1,2,4}).*

*Proof.* If two vertices x,y ∈ I(w) were non-adjacent, then {w,x,y} would be an
I₃; so every pair inside I(w) is adjacent and I(w) induces a tournament. A
transitive subtournament on 4 vertices inside I(w) is a TT₄ of D (for a
tournament target, induced and subdigraph containment coincide), so I(w) is
TT₄-free.

It remains to bound and identify a TT₄-free tournament T. Every tournament on 8
vertices contains a transitive subtournament on 4 vertices — the tournament
Ramsey value is v(4) = 8 — so |V(T)| ≤ 7; and the unique tournament on 7
vertices with no transitive subtournament on 4 vertices is the quadratic-residue
tournament QR₇ [SanchezFlores98, ErdosMoser64]. Applying this to T = I(w) gives
|I(w)| ≤ 7, with equality forcing I(w) ≅ QR₇. ∎

Both tournament inputs were re-established here from scratch, by exhaustive
enumeration: there are exactly 240 labelled TT₄-free tournaments on 7 vertices,
and every one is isomorphic to QR₇ (so the class is unique; and
240 = 7!/|Aut(QR₇)| with |Aut(QR₇)| = 21), while there are none on 8 vertices.
This matches the certified block inventory of [PartG, Prop. 3.3] and the
classical characterisation [SanchezFlores98].

**Corollary 3.2.** *In any free oriented graph every vertex has at most 7
non-neighbours; and a vertex has exactly 7 non-neighbours if and only if its
non-neighbourhood is a copy of QR₇.*

Corollary 3.2 is the endpoint |I(w)| ≤ 7 that drives the counting bound of
[PartG, §3]. It also explains the last column of Table 1: in each witness the
number of induced QR₇ blocks equals the number of type-s=7 vertices, which was
confirmed independently. Every one of the thirteen has between 6 and 14 such
vertices, so QR₇ appears in each; whether it must appear in *every* free graph
on 20 vertices is left open in §6.

## 4. The algebraic route falls short

The natural algebraic construction from QR₇ is a blow-up, and it falls well
short of the extremal order.

**Proposition 4.1.** *Let T be a tournament and m ≥ 1, and let T[Iₘ] be the
lexicographic blow-up in which each vertex of T is replaced by an independent
m-set. Then T[Iₘ] is free if and only if m ≤ 2 and T is TT₄-free.
Consequently the largest free graph of the form T[Iₘ] is QR₇[I₂] on 14
vertices, which gives only k(3,4) ≥ 15.*

*Proof.* In T[Iₘ] two vertices are adjacent exactly when they lie in different
groups (within a group there are no arcs; between groups the arc follows T,
which is a tournament). Hence the underlying graph is complete multipartite
with parts of size m, its independence number is m, and T[Iₘ] is I₃-free iff
m ≤ 2. A set of pairwise adjacent vertices meets each group at most once, so it
projects injectively onto a subtournament of T and the projection is an
isomorphism of induced sub-oriented-graphs; thus T[Iₘ] contains a TT₄ iff T
does. Combining the two, T[Iₘ] is free iff m ≤ 2 and T is TT₄-free. The largest
TT₄-free tournament is QR₇ on 7 vertices (Lemma 3.1), so the largest such
blow-up is QR₇[I₂] on 2·7 = 14 vertices. ∎

The bound k(3,4) ≥ 15 of Proposition 4.1 is six short of the truth 21: the
extremal order is 20, but the best tournament blow-up reaches 14. The thirteen
witnesses that reach the extremal order are rigid (Theorem 1.1), hence not
vertex-transitive, hence not Cayley digraphs; and they are not blow-ups, since
a proper blow-up has two vertices with identical neighbourhoods and every wᵢ
has twenty distinct colour classes under refinement. In the language of
[PartG, §8.1], where the extremal graph for k(3,3) = 9 is a single circulant,
the picture at (3,4) is the opposite: the extremal graph is not unique, and the
thirteen exhibited here are aperiodic and non-algebraic, with QR₇ surviving
only as a forced local block.

## 5. Certification

The thirteen witnesses (as arc lists) and three standard-library checkers are
deposited with this note in the program's public certificate repository
*Certify* ([github.com/05oz/certify](https://github.com/05oz/certify); concept
DOI [10.5281/zenodo.21799111](https://doi.org/10.5281/zenodo.21799111)), as
Part J. From each witness's arc list alone, `verify_witnesses.py` re-derives
validity as an oriented graph, freeness over all C(20,3) triples and C(20,4)
quadruples, rigidity (Weisfeiler–Leman refinement to twenty singleton colours,
cross-checked by an explicit automorphism count), and pairwise non-isomorphism
(a canonical form from the discrete refinement, cross-checked by the invariant
fingerprint of Table 1); `verify_qr7_lemma.py` enumerates the labelled TT₄-free
tournaments on 7 and 8 vertices (240, all isomorphic to QR₇; and 0) and reports
|Aut(QR₇)| = 21; and `blowup_bound.py` checks QR₇[I₂] and QR₇[I₃]. All three
checkers import only the Python standard library, share no code with the search
that produced the witnesses, and return PASS.

## 6. The sharpened question

Question 8.1 of [PartG] is answered: W is not unique, and the extremal count is
at least 13. The thirteen exhibited here are rigid, hence none is
vertex-transitive or Cayley; whether *some other* extremal graph might still be
algebraic is not decided here. Three questions remain.

**Question 6.1.** Is a QR₇ block unavoidable? Equivalently, does every free
oriented graph on 20 vertices have a vertex of type s = 7?

By Corollary 3.2 a vertex of type s = 7 is exactly a vertex whose
non-neighbourhood is a QR₇; so Question 6.1 asks whether the propositional
instance "free on 20 vertices with every vertex having at most 6 non-neighbours"
is unsatisfiable. All thirteen exhibited witnesses carry between 6 and 14 such
vertices, so QR₇ is present in each, but this is evidence, not a proof; the
all-vertices-s≤6 instance was not decided in a short trial and a certified
answer belongs to a dedicated computation.

**Question 6.2.** What is the exact number of free graphs on 20 vertices? The
thirteen here are a lower bound; the sampling behaviour suggests a large family,
but no count is certified.

**Question 6.3.** Can the counting slack of [PartG, §8.1] — the cap of 24
vertices against the true maximum of 20 — be explained structurally, for
instance through the forced QR₇ and Bermond blocks? Such an explanation would
bear on both the exact count and a human-readable upper bound.

## References

- **[Ber74]** J.-C. Bermond, *Some Ramsey numbers for directed graphs*,
  Discrete Math. **9** (1974), 313–321.
- **[Blo]** T. F. Bloom, *Erdős Problem #112*,
  https://www.erdosproblems.com/112, accessed 2026-08-11.
- **[ErdosMoser64]** P. Erdős and L. Moser, *On the representation of directed
  graphs as unions of orderings*, Magyar Tud. Akad. Mat. Kutató Int. Közl.
  **9** (1964), 125–132.
- **[IRW21]** F. Ihringer, D. Rajendraprasad and T. Weinert, *New bounds on the
  Ramsey number r(I_m,L_n)*, Discrete Math. **344** (2021), no. 3, 112268.
  Also arXiv:1707.09556.
- **[PartG]** D. Kirtchakov, *An Erdős–Rado oriented Ramsey number determined:
  k(3,4) = r(I₃,L₄) = 21, by explicit witness and certified exhaustion*,
  Certify (2026), version DOI
  [10.5281/zenodo.21890619](https://doi.org/10.5281/zenodo.21890619).
- **[SanchezFlores98]** A. Sánchez-Flores, *On tournaments free of large
  transitive subtournaments*, Graphs Combin. **14** (1998), 181–200.
