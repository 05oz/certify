# Lower bounds for nine small oriented Ramsey numbers r(Iₙ, Lₘ) (Erdős Problem #112), by explicit verified witnesses

**Daniel Kirtchakov**
Independent researcher (`05oz`); no institutional affiliation — daniel@halfounce.io — halfounce.io — ORCID [0009-0009-5213-4098](https://orcid.org/0009-0009-5213-4098)

*Addendum to Part G (Certify, version DOI [10.5281/zenodo.21890619](https://doi.org/10.5281/zenodo.21890619)). Draft of September 26, 2026 — not released.*

> **Computation and authorship.** The searches, the witnesses, and this note
> were produced by **Claude** (Anthropic), directed by the author, in a cloud
> Linux container with four cores. The witnesses were located by several means:
> * simulated annealing and parallel tempering;
> * SAT solving (CaDiCaL 1.9.5 through PySAT);
> * Cayley-digraph sweeps over the SmallGroups library of GAP.
>
> None of these tools enters the verification. Every claim in §2 is an
> explicit oriented graph that two standard-library checkers accept:
> * `kbounds-scripts/verify_bounds.py`, new. The orchestrating session wrote it
>   without opening any search program or any referee's checker. Its
>   independence from the searchers holds by construction. It has **not** been
>   measured by clone detection in the sense of this program's independence-claim
>   round (doi:10.5281/zenodo.21933031).
> * Part G's `k34-scripts/verify_witness.py`, which predates this campaign.
>
> Each witness was also re-checked by an adversarial referee agent. The
> referee wrote its own checker without reading the search code, and it ran
> tamper controls.

> **Prior-art record.** Two novelty audits ran on September 26, 2026; the
> second was instructed to try to refute. Neither found a published lower
> bound for any of the nine quantities at or above the values proved here
> (§4).
> * **Access.** In this session the network proxy blocked arxiv.org,
>   erdosproblems.com, ScienceDirect and Springer. [IRW21] was therefore not
>   re-read; this note relies on the program's full reading of it in August 2026
>   (Part G §1 and its referee record REFEREE-k63.md). By that reading, [IRW21]
>   constructs extremal graphs only on 8, 14 and 22 vertices and gives no lower
>   bound for m ≥ 6 in the k(m,3) column.
> * **#112 page.** The erdosproblems #112 entry was seen through a third-party
>   scrape (accessed 2026-07-10: no comments) and through `teorth/erdosproblems`
>   (commit of 2026-09-22: open).
> * **Recent preprints.** A scan of an arXiv math.CO RSS archive
>   (2024-03 to 2026-09-25, 20,641 items) found no paper on r(Iₘ,Lₙ).
> * **Residual risk.** Comments posted on #112 after 2026-08-11, and
>   [LaMi97] and [Ber74], were seen only through search snippets.

*2020 MSC: Primary 05C55; Secondary 05C20, 05D10, 68V15. Keywords: oriented
graph, Ramsey number, transitive tournament, independent set, Cayley digraph,
certified computation.*

---

## Abstract

Let k(n,m) = r(Iₙ,Lₘ) be the least N such that every oriented graph on N
vertices contains an independent set of size n or a transitive tournament on
m vertices (Erdős–Rado; Erdős Problem #112). Exact values are known only for
k(2,m) (m ≤ 6), k(3,3) = 9, k(4,3) = 15, k(5,3) = 23 and k(3,4) = 21. We give
explicit witnesses for nine further lower bounds:

  k(6,3) ≥ 30,  k(7,3) ≥ 39,  k(8,3) ≥ 47,  k(9,3) ≥ 61,
  k(4,4) ≥ 40,  k(3,5) ≥ 43,  k(5,4) ≥ 61,  k(4,5) ≥ 72,  k(3,6) ≥ 73.

The k(6,3) bound raises the program's own value of 29 (Part G). The other
eight exceed every bound we could find stated in, or assemble from, published
graphs. Those baselines, in the order listed, are 32, 37, 45, 28, 27, 41, 43 and 55,
and §4 gives the constructions. Each witness is an oriented graph file that a
standard-library checker accepts in well under a second. The checker computes
the exact independence number and the exact order of the largest transitive
subtournament, and both equal n − 1 and m − 1 for every witness. No value is
determined. The k(m,3) column now reads 9, 15, 23, ≥ 30, ≥ 39, ≥ 47, ≥ 61
against the upper bound m² − m + 3 = 9, 15, 23, 33, 45, 59, 75 of [IRW21],
which is attained for m ≤ 5.

## 1. The numbers

An *oriented graph* is a loopless digraph with at most one arc between any two
vertices. Iₙ is the independent set on n vertices. TTₘ (= Lₘ) is the
transitive tournament on m vertices. A graph is *(n,m)-free* if it contains
neither Iₙ nor TTₘ, and an (n,m)-free graph on N vertices proves
k(n,m) ≥ N + 1.

**Known values.**
* k(2,m) = v(m), the tournament Ramsey number: k(2,3) = 4, k(2,4) = 8,
  k(2,5) = 14, k(2,6) = 28.
* k(3,3) = 9 [Ber74].
* k(4,3) = 15 and k(5,3) = 23 [IRW21].
* k(3,4) = 21 (Part G).

**Upper bounds.** Two sources give them:
* **[IRW21]:** k(m,3) ≤ m² − m + 3 for all m.
* **The neighbourhood recursion** [IRW21, Lemma 2.1]. In an (n,m)-free graph
  the out- and in-neighbourhood of every vertex is (n, m−1)-free, and the
  non-neighbourhood is (n−1, m)-free. Hence

  k(n,m) ≤ 2·k(n,m−1) + k(n−1,m) − 1.

  This gives k(4,4) ≤ 50 and k(3,5) ≤ 55 (Part G §8.3), and, with those,
  k(5,4) ≤ 95, k(4,5) ≤ 154 and k(3,6) ≤ 137.

**Lower bounds before this note.** The only explicit ones for n ≥ 3 beyond the
exact values were:
* k(6,3) ≥ 29 (Part G, the circulant Cay(ℤ₂₈, {3,8,10,12,17}));
* k(4,4) ≥ 21 (Part G §8.3, by monotonicity);
* r(I₃,Lₘ) ≥ 2v(m) − 1 (Part J), which gives k(3,5) ≥ 27 and k(3,6) ≥ 55.

## 2. Results

**Theorem 2.1.** *Each file in `kbounds-certificates/` is an (n,m)-free
oriented graph on N vertices. Hence:*

| quantity | witness file | N | lower bound | upper bound |
|---|---|---|---|---|
| k(6,3) | `k63_N29.json` | 29 | **k(6,3) ≥ 30** | 33 |
| k(7,3) | `k73_N38.json` | 38 | **k(7,3) ≥ 39** | 45 |
| k(8,3) | `k83_N46.json` | 46 | **k(8,3) ≥ 47** | 59 |
| k(9,3) | `k93_N60.json` | 60 | **k(9,3) ≥ 61** | 75 |
| k(4,4) | `k44_N39.json` | 39 | **k(4,4) ≥ 40** | 50 |
| k(3,5) | `k35_N42.json` | 42 | **k(3,5) ≥ 43** | 55 |
| k(5,4) | `k54_N60.json` | 60 | **k(5,4) ≥ 61** | 95 |
| k(4,5) | `k45_N71.json` | 71 | **k(4,5) ≥ 72** | 154 |
| k(3,6) | `k36_N72.json` | 72 | **k(3,6) ≥ 73** | 137 |

*In every witness the independence number is exactly n − 1 and the largest
transitive subtournament has exactly m − 1 vertices.*

The witnesses fall into three kinds.

**The k(6,3) witness is not vertex-transitive.** It has 138 arcs, and its
out- and in-degrees are 4 or 5, so its total degrees range over 8–10. All 117
of its triangles are directed 3-cycles, as they must be. It was found by
unstructured simulated annealing, and parallel tempering later found others
on 29 vertices in seconds. By contrast, **no** Cayley digraph on any group of
order 29, 30, 31 or 32 is (6,3)-free. This is a complete C enumeration of
every inverse-free, product-free connection set of size at most 5 over all 57
groups of those orders (§5). So the record for k(6,3) is not algebraic.
Part G's sweep had covered only the cyclic groups of orders 29–31 and three of
the seven abelian groups of order 32.

**The k(7,3) and k(8,3) witnesses are bicirculants.** Each is invariant under a
semiregular ℤ₁₉ or ℤ₂₃ with two orbits. Write the vertex (i,a) as 19a + i
(resp. 23a + i), with arcs (i,a) → (i+d, b) for d ∈ S_ab:
* k(7,3): S₀₀ = {8,12,13,17}, S₀₁ = {2,6}, S₁₀ = {1,5}, S₁₁ = {8,12,14,18};
  6-regular.
* k(8,3): S₀₀ = {1,3,11,18}, S₀₁ = S₁₀ = {6,14,16}, S₁₁ = {1,3,11,16};
  7-regular.

No Cayley digraph of order 37–45 is (7,3)-free. The best Cayley (8,3)-witness
has 45 vertices.

**The other five are Cayley digraphs** Cay(G,S), with arcs g → g + s:

| quantity | G | S |
|---|---|---|
| k(9,3) | ℤ₆₀ | {2,3,21,22,35,36,54,55} |
| k(4,4) | ℤ₃₉ | {11,15,17,19,25,27,29,30,33,34,38} |
| k(3,5) | ℤ₄₂ | {2,3,4,9,10,22,23,25,26,28,29,30,35,36} |
| k(5,4) | ℤ₆₀ | {4,7,8,11,17,20,21,22,24,32,34,35,45,54} |
| k(4,5) | ℤ₇₁ | {10,11,12,19,21,22,27,28,30,32,33,34,46,47,54,55,57,63,65,66,68,69} |
| k(3,6) | ℤ₂₄ × ℤ₃ | 25 elements, listed in the file |

For a Cayley digraph, TT₃-freeness is exactly product-freeness of S (S ∩ S·S = ∅).

## 3. Verification

The file format is JSON `{"N", "a", "b", "arcs"}`, with arc u → v on vertices
0..N−1; it is Part G's format. Replay:

```sh
python3 kbounds-scripts/verify_bounds.py kbounds-certificates/*.json      # all nine, < 0.5 s
python3 k34-scripts/verify_witness.py kbounds-certificates/<file>.json    # Part G's checker, per file
```

**`verify_bounds.py`** (standard library only). It checks that the arcs form
an oriented graph: indices in range, no loops, no repeated arcs, no 2-cycles.
It then computes two exact invariants by bitmask branch-and-bound:
* α, the independence number of the underlying graph, as a maximum clique of
  the complement;
* τ, the order of the largest transitive subtournament. A transitive
  tournament is a chain v₁, …, v_t with vᵢ → vⱼ for all i < j, so τ is the
  longest chain in which each vertex lies in the out-neighbourhood of every
  earlier one.

A file passes iff α ≤ n − 1 and τ ≤ m − 1. The measured values are
α = n − 1 and τ = m − 1 in all nine files.

The checker was tested before use in two ways:
* **Brute-force cross-check.** On 600 random oriented graphs on 3–11 vertices
  its α and τ agree with exhaustive subset enumeration, with zero
  disagreements. A first draft of the τ search pruned against the siblings not
  yet tried, which is valid for cliques but not for chains, and so reported too
  small a τ. This cross-check caught it before any use.
* **Tamper controls.** For each witness three corruptions are rejected:
  deleting the arcs among n chosen vertices (creating an Iₙ); orienting m
  chosen vertices transitively (creating a TTₘ); and adding the reverse of an
  arc (a 2-cycle).

**Part G's `verify_witness.py`** tests every n-subset for independence and
every m-subset for a transitive score sequence. It passes the five witnesses
k63, k73, k83, k44 and k35 in about two minutes in total. On k93 it must scan
all C(60,9) ≈ 1.5×10¹⁰ nine-subsets, and on k36 all C(72,6) ≈ 1.6×10⁸
six-subsets. It passes k54 (3 s), k45 (8 s) and k36 (89 s). [k93 RUN IN PROGRESS — record verdict and time here.]

SHA-256 digests of the nine files are listed in
`kbounds-certificates/README.md`.

## 4. How much is new: buildable baselines

Stating an improvement only against *stated* bounds would overstate it:
several better bounds can be assembled in a line from published graphs. The
second audit therefore built, and checked, the best disjoint unions,
lexicographic blow-ups and substitutions of published extremal graphs. Its
inventory of published graphs:
* from [Ber74] and [IRW21]: Bermond's 8-vertex circulant, W₁₄ and W₂₂;
* from Part G and Part J: the ℤ₂₈ circulant and the 20-vertex W;
* classical tournaments: QR₇, a 13-vertex TT₅-free tournament, QR₂₇.

Under disjoint union, independence numbers add and τ is the maximum. Under a
lexicographic product, α and τ multiply.

| quantity | best from the literature before Part G | best with Part G/J | this note |
|---|---|---|---|
| k(6,3) | 26 (W₂₂ ⊔ directed C₃) | 29 | **30** |
| k(7,3) | 31 (W₂₂ ⊔ Bermond's graph) | 32 (ℤ₂₈ ⊔ C₃) | **39** |
| k(8,3) | 37 (W₂₂ ⊔ W₁₄) | 37 | **47** |
| k(9,3) | 45 (W₂₂ ⊔ W₂₂) | 45 | **61** |
| k(4,4) | 22 (QR₇[I₃]) | 28 (W ⊔ QR₇) | **40** |
| k(3,5) | 27 (T₁₃ ⊔ T₁₃) | 27 | **43** |
| k(5,4) | 31 (W₂₂ with C₃ substituted on an independent 4-set) | 41 (W ⊔ W) | **61** |
| k(4,5) | 43 (W₁₄[C₃]) | 43 | **72** |
| k(3,6) | 55 (QR₂₇ ⊔ QR₂₇) | 55 (Part J) | **73** |

Two further remarks:
* **Part G §5.2 is off by one.** It states that no lower bound for k(6,3)
  beyond 24 appears in the literature. That is true of *stated* bounds, but
  W₂₂ ⊔ C₃ has 25 vertices and α = 5, so k(6,3) ≥ 26 was buildable. This is a
  correction to Part G's prose, not to any of its results.
* **k(9,3).** The best union using this campaign's own graphs is k83 ⊔ C₃, with
  49 vertices, giving k(9,3) ≥ 50. The Cayley witness beats it by 11.

## 5. Search record

Nothing in this section is claimed. Every "UNSAT" is a plain CaDiCaL answer
with no DRAT/LRAT proof, and every annealing failure is heuristic. It is
recorded so that others need not repeat it.

**k(6,3), N = 30–32.**
* **Complete Cayley sweeps.** No Cayley digraph on any group of order 29–32 is
  (6,3)-free. This covers all 1 + 4 + 1 + 51 groups and every admissible S. By
  order, the smallest independence number over admissible S is:
  * order 30: 6 for C₃₀, C₅ × S₃ and C₃ × D₁₀;
  * order 31: 6;
  * order 32: 6 for C₃₂, SmallGroup(32,15) and C₁₆ × C₂.
* **Solver-UNSAT, N = 32.** Every bi-Cayley graph over the 14 groups of order
  16, and every 4-orbit graph over the 5 groups of order 8, with the valid
  degree constraints d⁺, d⁻ ≤ 5 and d ≥ 9.
* **Solver-UNSAT, N = 30.** ℤ₁₅ with 2 orbits; ℤ₁₀ and D₁₀ with 3 orbits;
  S₃ with 5 orbits.
* **Annealing at N = 30.** Unstructured parallel tempering, in seven runs and
  about 65 CPU-minutes, always reached exactly four violations (all TT₃) and
  never fewer. On 29 vertices the same method finds witnesses in 1–5 s, and it
  finds the extremal k(5,3), k(4,3) and k(3,3) graphs in about 1 s.
* **Extensions.** Every one-vertex extension of six distinct 29-vertex
  witnesses is solver-UNSAT.

**k(7,3), N = 39.**
* **Near-miss.** Annealing restricted to ℤ₁₃ × 3 polycirculants reached cost 1
  (a single violated orbit of 13 TT₃) in five runs out of five.
* **That class is empty.** The ℤ₁₃ × 3 class is solver-UNSAT, in 17–61 s, in
  four runs. Those runs used two independently written eager encoders, with
  every I₇ condition enumerated as a clause over edge orbits (884,211 minimal
  clauses). Their lex-leader symmetry breaking was unit-tested against all 4056
  group elements. The same pipeline returns verified SAT on the I₈ variant, and
  it recovers the 38-vertex witness.
* **Order-5 classes are empty.** Every class with an automorphism of order 5
  (4, 9, …, 34 fixed points) is solver-UNSAT.
* **Consequence.** A counting argument uses k(j,3) for j ≤ 5 and k(6,3) ≤ 33.
  It excludes automorphisms of prime order p ≥ 7 other than 13, and order 13
  forces the ℤ₁₃ × 3 class. So any 39-vertex (7,3)-free graph has an
  automorphism group of order 2ᵃ3ᵇ. This rests on the solver answers above.
* **Other classes.** No Cayley digraph of order 37–45 is (7,3)-free. 2-orbit
  graphs at N = 40, 42 and 44 are solver-UNSAT, and the ℤ₃ × 13 class timed out
  at 900 s.

**k(4,4), k(3,5).**
* **Cayley.** Complete Cayley SAT sweeps found no witness at orders 34–36, 38
  or 40–49 for (4,4), and none at 43–48 or 50 for (3,5). The only
  Cayley (4,4)-witnesses at orders 37 and 39 are on C₃₇ and C₃₉.
* **Polycirculant annealing floors.** 13 or more for (4,4) at N = 40–44; 6 for
  (3,5) in ℤ₂₂ × 2 and ℤ₂₃ × 2.

**k(9,3), k(5,4), k(4,5), k(3,6)** (Cayley and circulant searches above the records).
* **k(9,3).** No circulant on 61–71 vertices has an admissible connection set;
  this is an exhaustive DFS. No group of order 61, 62 or 63 has one either.
* **k(5,4).** Every circulant on 61–72 vertices is solver-UNSAT, with
  multiplier symmetry breaking. Of the 256 non-abelian groups of order 64:
  * 204 are excluded by hand, because an elementary abelian subgroup of order 8
    has only involutions, which can never lie in S, so it is an independent
    8-set;
  * 40 are solver-UNSAT;
  * 12 timed out.
* **k(4,5).** The circulant on ℤ₇₂ timed out after 603 s. All 142 circulants on
  72–90 vertices invariant under a multiplier subgroup H ≠ 1 are solver-UNSAT.
* **k(3,6).** The circulant on ℤ₇₃ timed out after 627 s. All 198 circulants
  on 73–96 vertices invariant under a multiplier subgroup H ≠ 1 are
  solver-UNSAT.

## 6. Questions

1. **Is m² − m + 3 attained at m = 6?** Is k(6,3) = 33? The bound is attained
   for m = 3, 4, 5. A 32-vertex witness would have to be regular of out- and
   in-degree 5 on most vertices, and no Cayley or bi-Cayley graph qualifies.
   The four-violation plateau at N = 30 is heuristic evidence that 30 may
   already be the truth or close to it. An exhaustion in the style of Part G
   would need inventories of (5,3)-free graphs on up to 22 vertices.
2. **Algebraic versus rigid extremal graphs.** The records in the k(m,3) column
   are non-Cayley for m = 6, 7, 8 and Cayley for m = 9. For m = 4, 5 the
   extremal graphs of [IRW21] are non-Cayley and circulant respectively. For
   k(3,4) = 21 the thirteen known extremal graphs are rigid (Part J). Is there
   a pattern?
3. **k(4,4).** The best witness is the circulant on ℤ₃₉, and nothing on 40
   vertices was found in any structured class. Where between 40 and 50 is
   k(4,4)?

## References

- **[Ber74]** J.-C. Bermond, *Some Ramsey numbers for directed graphs*,
  Discrete Math. **9** (1974), 313–321.
- **[Blo]** T. F. Bloom, *Erdős Problem #112*,
  https://www.erdosproblems.com/112 (not reachable from this session; see the
  prior-art record).
- **[ErRa67]** P. Erdős and R. Rado, *Partition relations and
  transitivity domains of binary relations*, J. London Math. Soc.
  **42** (1967), 624–633.
- **[IRW21]** F. Ihringer, D. Rajendraprasad and T. Weinert, *New bounds
  on the Ramsey number r(I_m,L_n)*, Discrete Math. **344** (2021),
  no. 3, 112268; arXiv:1707.09556.
- **[LaMi97]** J. A. Larson and W. J. Mitchell, *On a problem of Erdős
  and Rado*, Ann. Comb. **1** (1997), 245–252.
- **[PartG]** D. Kirtchakov, *An Erdős–Rado oriented Ramsey number
  determined: k(3,4) = r(I₃,L₄) = 21*, Certify v0.7.0 (2026),
  doi:10.5281/zenodo.21890619.
- **[PartJ]** D. Kirtchakov, *The extremal graph for k(3,4) = 21 is not
  unique*, Certify v0.10.0 (2026), doi:10.5281/zenodo.21898266.
- **[SF98]** A. Sánchez-Flores, *On tournaments free of large transitive
  subtournaments*, Graphs Combin. **14** (1998), 181–200.
