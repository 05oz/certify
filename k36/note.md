# An explicit oriented graph gives k(3,6) ≥ 73 (Erdős Problem #112)

**Daniel Kirtchakov.** Independent researcher (`05oz`), no institutional affiliation. daniel@halfounce.io, halfounce.io, ORCID [0009-0009-5213-4098](https://orcid.org/0009-0009-5213-4098).

*Certify Part O, v0.19.0. Each graph is checked by two independent checkers on one machine; a replay on a second machine has not been made. The certificates and scripts are in the folder `k36/` of https://github.com/05oz/certify, archived on Zenodo (all versions: doi:10.5281/zenodo.21799111).*

> **Computation and authorship.** The graphs, the scripts in `scripts/` and this note were produced with Claude (Anthropic), directed by the author. How the graphs were found plays no part in their validity and is not described here: each statement is an explicit graph in a file that the checkers of section 4 accept.

**Abstract.** Let k(n,m) be the least k such that every oriented graph on k vertices contains n pairwise non-adjacent vertices or a transitive tournament on m vertices (Erdős Problem #112). We give a Cayley digraph G72 on Z_24 × Z_3 with 25 generators that has no three pairwise non-adjacent vertices and no transitive tournament on six vertices, so k(3,6) ≥ 73; the largest published lower bound found is 71. The first property has a short proof by hand. The second is checked on the whole graph by two independently written programs; by vertex-transitivity it amounts to a check of a 25-vertex subdigraph. We also record two graphs that show k(7,3) ≥ 39 and k(8,3) ≥ 47, bounds first published by T. S. Orden, with explicit isomorphisms to his graphs.

**Question.** Erdős Problem #112 asks for the least number k(n,m) of vertices that forces every directed graph to contain n independent vertices or a transitive tournament on m vertices. Exact values are known only for a few small pairs. This note gives an explicit graph for one lower bound, k(3,6) ≥ 73. It also contains two graphs for k(7,3) ≥ 39 and k(8,3) ≥ 47. Those two bounds are T. S. Orden's, published on 2026-11-20 [Orden2]; section 5 says how his graphs and these are related.

## 1. The number k(n,m)

The problem page [Blo] (page and forum thread read in full on 2026-11-11) defines k = k(n,m) as minimal such that any directed graph on k vertices contains an independent set of size n or a transitive tournament of size m, asks for its value, and attributes the problem to Erdős and Rado [ErRa67]. Ihringer, Rajendraprasad and Weinert [IRW21] write the same number as r(I_m, L_n), with the size of the independent set written before the size of the tournament: the least order at which every oriented graph contains an independent set of cardinality m or a transitive tournament on n vertices. Oriented means no loops and at most one arc between two vertices; a footnote in [IRW21] gives this as the reason for writing "oriented" rather than "directed". So k(n,m) = r(I_n, L_m), and [Orden], [Orden2] and [rsv] (section 5) use the same definition.

A set of vertices is independent when no arc joins two of its members; a transitive tournament TT_m is a set of m vertices ordered v_1, ..., v_m with v_i → v_j whenever i < j. An oriented graph on N vertices with neither an independent n-set nor a TT_m shows k(n,m) ≥ N + 1. The graphs below are oriented, so each is a witness under either wording.

## 2. Result

**Theorem.** k(3,6) ≥ 73.

The proof is an explicit oriented graph, G72 (section 3). Two more graphs, G38 and G46, show k(7,3) ≥ 39 and k(8,3) ≥ 47. Orden published those two bounds before this release [Orden2], and the two graphs are his graphs up to relabelling (section 5); they are in this release as a record, not as a claim. Below, α is the independence number and τ the number of vertices of the largest transitive subtournament; both are exact values computed by `verify_bounds.py`. The last two columns are the published values of section 5.

| graph | file | vertices | arcs | α | τ | bound | largest published lower bound found | published upper bound |
|---|---|---|---|---|---|---|---|---|
| G72 | `certificates/k36_N72.json` | 72 | 1800 | 2 | 5 | k(3,6) ≥ 73 | 71 [Orden2] | 161 [IRW21]; 137 with k(3,4) = 21 [PartG] |
| G38 | `certificates/k73_N38.json` | 38 | 228 | 6 | 2 | k(7,3) ≥ 39 | 39 [Orden2] | 45 [IRW21] |
| G46 | `certificates/k83_N46.json` | 46 | 322 | 7 | 2 | k(8,3) ≥ 47 | 47 [Orden2] | 59 [IRW21] |

τ = 2 means that G38 and G46 have no transitive triangle: every triangle in them is a directed 3-cycle.

## 3. The three graphs

**G38, over Z_19.** Vertices are the pairs (i, a) with i in Z_19 and a in {0, 1}, numbered 19a + i in the file. There is an arc (i, a) → (i + d mod 19, b) exactly when d ∈ S_ab, where S_00 = {8, 12, 13, 17}, S_01 = {2, 6}, S_10 = {1, 5} and S_11 = {8, 12, 14, 18}. Every vertex has out-degree 6 and in-degree 6, and (i, a) ↦ (i + 1, a) is an automorphism with two orbits.

**G46, over Z_23.** The same rule with Z_23 and numbering 23a + i, where S_00 = {1, 3, 11, 18}, S_01 = S_10 = {6, 14, 16} and S_11 = {1, 3, 11, 16}. Every vertex has out-degree 7 and in-degree 7.

**G72, a Cayley digraph on G = Z_24 × Z_3.** The element (x, y) is vertex 3x + y in the file, and there is an arc g → g + s for every s in S = {(0,2), (2,0), (2,1), (2,2), (3,0), (5,1), (6,1), (6,2), (8,0), (8,1), (9,2), (10,0), (10,1), (11,0), (11,1), (11,2), (12,2), (14,1), (15,2), (16,1), (18,0), (19,0), (19,1), (21,1), (21,2)}. So |S| = 25, and every vertex has out-degree 25 and in-degree 25.

**Checks by hand.**
(a) *Orientation.* 0 is in neither S_00 nor S_11, and S_00 ∩ -S_00, S_11 ∩ -S_11 and S_01 ∩ -S_10 are empty; (0,0) ∉ S and S ∩ -S is empty. So there are no loops and no 2-cycles.
(b) *No transitive triangle in G38 and G46.* A transitive triangle u → v → w, u → w with u, v, w in orbits a, b, c translates to u = (0, a), v = (d, b), w = (d + e, c) with d ∈ S_ab, e ∈ S_bc and d + e ∈ S_ac, and any such d and e give one. So there is none exactly when the eight sets (S_ab + S_bc) ∩ S_ac, taken mod q, are empty: a short hand computation.
(c) *No three independent vertices in G72.* Vertices g ≠ h are non-adjacent exactly when h - g lies in T = G minus (S ∪ -S ∪ {(0,0)}), so three independent vertices exist exactly when T contains t_1, t_2 and t_1 + t_2. Here T = ({1, 4, 7, 17, 20, 23} × Z_3) ∪ {(9,0), (12,0), (15,0)}, with 21 elements. The Z_24 coordinates of T lie in F = {1, 4, 7, 9, 12, 15, 17, 20, 23}, and F + F = {0, 2, 3, 5, 6, 8, 10, 11, 13, 14, 16, 18, 19, 21, 22} does not meet F. So α(G72) ≤ 2; and T is not empty, so α(G72) = 2.
(d) *Reduction for transitive tournaments.* Let D[S] be the subdigraph of G72 induced on S, the out-neighbourhood of (0,0). Then τ(G72) = τ(D[S]) + 1; in particular G72 contains a TT_6 exactly when D[S], which has 25 vertices, contains a TT_5. Proof: G72 is a Cayley digraph, so each translation g ↦ g + h is an automorphism. A transitive tournament has exactly one vertex with no in-neighbour in it, its source. Translating the source to (0,0) puts the other vertices in S, where they form a transitive tournament with one vertex fewer. Conversely, (0,0) has an arc to every vertex of S, so a transitive tournament in D[S] together with (0,0) is a transitive tournament with one vertex more.
(e) *The computer part* is what remains: α(G38) ≤ 6, α(G46) ≤ 7, and no TT_5 in D[S] (equivalently, no TT_6 in G72). Both checkers of section 4 test the whole graph G72; `verify_bounds.py` finds τ(G72) = 5, so τ(D[S]) = 4 by (d).

*Proof of the theorem.* By (a) and (c), G72 is an oriented graph on 72 vertices with no three pairwise non-adjacent vertices, and by the computation of section 4 it has no transitive tournament on six vertices. So k(3,6) ≥ 72 + 1 = 73.

`scripts/check_constructions.py` rebuilds the three arc sets from the data above (written into the script, not read from the files), checks that they equal the arc lists in the files, and checks (a), (b), (c) and the degrees.

## 4. How to verify

```
42f6b3f624907602821e42c57601e311d9f3941bd6af1046e7903b11455801f4  certificates/k73_N38.json
73b58fcce089c13a090c21727106175d1424cfdbe5ff386b725481664920d840  certificates/k83_N46.json
3c8dc5150b6efd58093aa4724f14d78f9608a7afac49b0099b377e273a9911c3  certificates/k36_N72.json
```

Each file is JSON `{"N": N, "a": n, "b": m, "arcs": [[u, v], ...]}` with arc u → v on vertices 0, ..., N-1 (the format of [PartG]), plus the construction data of section 3. Run from the folder `k36/` of the repository (on Windows, `py` in place of `python3`); `..` is the repository root, which holds Part G's checker `k34-scripts/verify_witness.py`, unchanged since its release in v0.7.0:

```
python3 scripts/verify_bounds.py certificates/k73_N38.json certificates/k83_N46.json certificates/k36_N72.json
python3 scripts/check_constructions.py
python3 scripts/test_check_constructions.py
python3 scripts/check_same_graphs.py
python3 ../k34-scripts/verify_witness.py certificates/k73_N38.json
python3 ../k34-scripts/verify_witness.py certificates/k83_N46.json
python3 ../k34-scripts/verify_witness.py certificates/k36_N72.json
```

Every command prints PASS and exits with status 0; `verify_bounds.py` prints `alpha=6 ... largest TT=2`, `alpha=7 ... largest TT=2` and `alpha=2 ... largest TT=5`, then `k(7,3) = r(I_7, L_3) >= 39`, `k(8,3) = r(I_8, L_3) >= 47` and `k(3,6) = r(I_3, L_6) >= 73`. Times on 2026-11-11 (arm64 macOS laptop running other jobs, Python 3.15.2, low priority): `verify_bounds.py` under 0.1 s per file, the two construction scripts 0.02 s and 0.24 s, Part G's checker 7.4 s, 135.3 s and 115.5 s; `check_same_graphs.py` (2026-11-25, the same laptop) under 0.1 s.

All five scripts are standard-library Python, make no network calls and write nothing. `verify_bounds.py` rejects loops, repeated arcs and 2-cycles and computes α and τ exactly by bitmask branch-and-bound; a file passes iff α ≤ n - 1 and τ ≤ m - 1. Part G's `verify_witness.py` tests every n-subset for independence and every m-subset for a transitive tournament (score sequence 0, 1, ..., m - 1). `test_check_constructions.py` shows that `check_constructions.py` rejects nine corrupted copies of the files and that (b) and (c) agree with brute force on 600 random small cases each. `check_same_graphs.py` rebuilds the two bicirculants of [Orden2] from the connection sets printed in its README and checks that the relabellings of section 5 carry G38 and G46 onto them.

## 5. Published values and credit

- **[Orden2]** T. S. Orden's second Zenodo dataset on this problem (published 2026-11-20, version 1.0; data and text CC BY 4.0, code MIT) states k(7,3) ≥ 39, k(8,3) ≥ 47, k(6,4) ≥ 78 and k(3,6) ≥ 71. Its graphs are bicirculants on Z_19 × {0,1} and Z_23 × {0,1}, a circulant on Z_77, and a circulant on Z_70 with a 23-element connection set; a second circulant, on Z_69, gives k(3,6) ≥ 70. Its README says that the graphs were found by computer searches run by AI agents under the author's direction, and that the record has not been peer reviewed. Erdős Problem a Day rebuilt the four graphs from their connection sets and checked them with its own program on 2026-11-22 [EPAD]. On 2026-11-25 `verify_bounds.py` accepted all five witness graphs of the record. The bounds k(7,3) ≥ 39 and k(8,3) ≥ 47 are Orden's: his record is the earlier publication.
- **The same two graphs.** G38 is the 38-vertex graph of [Orden2] relabelled, and G46 is its 46-vertex graph relabelled. Both records number the vertex with residue i in orbit a as qa + i, with q = 19 or 23. The map (i, a) ↦ (14i + 16a mod 19, 1 - a) carries the arc list of `k73_N38.json` onto his 38-vertex graph, and (i, a) ↦ (19i + 18a mod 23, 1 - a) carries the arc list of `k83_N46.json` onto his 46-vertex graph (`scripts/check_same_graphs.py`).
- **[rsv]** The GitHub repository rsvaultpudgy-create/erdos-112-lower-bounds (CC0, created 2026-11-11 13:54 UTC, one commit, d305711817) states k(7,3) ≥ 37 (a circulant on Z_36 with connection set {6, 8, 10, 11, 13, 15}), k(8,3) ≥ 46 (Z_45, {7, 13, 15, 19, 23, 25, 31}) and k(3,6) ≥ 68 (Z_67, a 22-element set), and bounds for seven other pairs. Its README says the work was produced by an AI system and is unrefereed. On 2026-11-11 `verify_bounds.py` accepted its graphs for our three quantities.
- **[Orden]** T. S. Orden's first Zenodo dataset on this problem (published 2026-11-09, version 2 on 2026-11-16; data and text CC BY 4.0, code MIT) gives a 29-vertex witness for k(6,3) ≥ 30 and a written proof of k(6,3) ≤ 32 that, it says, has not been peer reviewed. A separate record, [OrdenLean], gives a Lean 4 proof of both bounds; it has not been built here. [Orden] states no value for the three quantities of this note, and neither does the README of [OrdenLean].
- **[IRW21]** gives k(4,3) = 15, k(5,3) = 23 and k(m,3) ≤ m^2 - m + 3, so k(7,3) ≤ 45 and k(8,3) ≤ 59. Its closing section bounds r(I_m, L_n) by an explicit v(m,n), and v(3,6) = 161. Its recursion r(I_(m+1), L_(n+1)) ≤ 2 r(I_(m+1), L_n) + r(I_m, L_(n+1)) - 1, with k(3,4) = 21 [PartG] and the values r(I_2, L_5) = 14 and r(I_2, L_6) = 28 listed in [IRW21], gives k(3,5) ≤ 55 and k(3,6) ≤ 137, as [rsv] also states. The certificates of [PartG] were rebuilt and replayed with a formally verified checker by Erdős Problem a Day on 2026-11-18 [EPAD2]. **[Ber74]** gives k(3,3) = 9; its added-in-proof note says this result (its Proposition 2.5) also appears in Harary and Hell, Bull. London Math. Soc. 6 (1974) 175-182.

The row k(n,3) as of 2026-11-25 reads 9, 15, 23 for n = 3, 4, 5; then 30 ≤ k(6,3) ≤ 32 ([Orden]; [rsv] also gives 30); 39 ≤ k(7,3) ≤ 45; 47 ≤ k(8,3) ≤ 59 (lower bounds from [Orden2]).

## 6. Prior-art status and what is open

**Not found in the sources read, as of 2026-11-25.** None of the sources read in full or scanned (the first two lists below) states k(3,6) ≥ 73 or a larger lower bound for k(3,6); the largest stated is 71 [Orden2]. The date 2026-11-25, here and for the row k(n,3) in section 5, does not cover the problem page [Blo] and its forum thread, which were last read on 2026-11-11, or the records that the list *Not read* below gives as not read again on 2026-11-25. For k(7,3) and k(8,3) the largest stated are 39 and 47 [Orden2], the values of G38 and G46. The assemblies of published graphs that were built and checked on 2026-11-11 (disjoint unions and blow-ups of the graphs published by then) reach at most 37, 46 and 68. Whether one of the three graphs is an induced subgraph of a larger published graph (for example those of McCarthy and Springfield, arXiv:2311.02135, or of McCarthy and Monico, arXiv:2408.04067) was checked only in part, by computer runs without proof objects, so that question stays open.

*Read in full* (prior-art reads of 2026-10-14 to 2026-10-20, of 2026-11-11, of 2026-11-17 and of 2026-11-25). Problem records: erdosproblems.com/112 with its LaTeX, history and forum pages (page and forum again on 2026-11-11); the erdosproblems.ai entry for #112; teorth/erdosproblems; plasma-ai/erdos E0112; Erdős Problem a Day (#112 report, its k(3,4) = 21 page, progress page) with the two #112 folders in pw/erdosproblemaday-verification on 2026-11-11 (n21-attack and order21-casesplit), and on 2026-11-25 its problem page, [EPAD] with the review of [Orden2], [EPAD2], and the README of each of the three #112 folders added to that repository since 2026-11-11 (orden-k63, orden-small-lower-bounds and kirtchakov-certificates-cake-lpr; their other files were not read); the forum post of 2026-09-22 by Muhamadiev Faridun and gitlab.com/faridunislom/math.erdos112. Papers: [IRW21] (arXiv v1 and v3), [Ber74], Larson and Mitchell 1997, Erdős and Rado 1956 and [ErRa67], Benhocine 1978, Weinert arXiv:2611.08079, Klausner and Weinert arXiv:1810.13316, McCarthy and Springfield arXiv:2311.02135, McCarthy and Monico arXiv:2408.04067 (and the journal version), Neiman, Mackey and Heule arXiv:2011.00683, Lohn, Lambert and Heule (FMCAD 2022), Momihara and Suda arXiv:1605.02469, Nagy arXiv:1401.6823, Fox, He and Wigderson arXiv:2105.02383, Grzesik et al. arXiv:2305.19959, Caicedo and Hilton arXiv:1510.00078, Chung 1997, Erdős and Moser 1964 (two papers), Stearns 1959, Moon 1971, Haddad and Sabbagh 1969 (three notes), the 1975 corrections of Harary and Hell, and the theses of Weinert, Sánchez-Flores and Araujo-Pardo; Reid and Parker 1970 and Choudum and Ponnusamy 1999 (both read in full on 2026-11-11 from the publishers' open-archive PDFs); Manoussakis and Tuza 2001 (read in full on 2026-11-17 from the publisher's open-archive PDF); X. Zeng, A Computer-Assisted Proof of the Oriented Ramsey Value k(3,4) = 21 (nine pages; the PDF in the GitHub repository ArtificialZeng/AI-Has-Taste, commit 2537a78914 of 2026-09-13, read in full on 2026-11-25; it states nothing on the three quantities of this note). Data: [Orden] (all seven files of version 1; of version 2, the README and the proof, its other five files being identical to version 1's); [Orden2] (the README, the definitions, the three scripts and their output; the five arc lists checked by program); the README of [OrdenLean]; the README of Tyorden/erdos-112-small-bounds-lean; the file math/directed-ramsey/results/k112-2026-11-19.md of the GitHub repository adineo-cmd/open-research-lab, which states k(4,4) ≥ 40 and k(3,5) ≥ 39 from circulants and nothing on the three quantities of this note; [rsv] (README, log, witness lists and logs); OEIS A122026, A122027, A224886, A003141, A001225, A362137 and A027688, with W. D. Smith's pages linked from A122026; Certify Parts G and J.

*Scanned, not read in full:* arXiv math.CO from 2026-10-19 to 2026-11-10 (1,122 titles and abstracts) and 16 targeted arXiv queries; 29 DataCite queries; 10 GitHub searches; the works citing [IRW21] in OpenAlex, Semantic Scholar, OpenCitations, Crossref and zbMATH (two: Klausner and Weinert, and [Orden]); arXiv:2604.23433, 2608.12207 and 2403.02298 in part. On 2026-11-25, for the window since 2026-11-11: six arXiv queries, eight Zenodo and DataCite queries, 44 GitHub searches (repositories, commits, issues and code) with the READMEs of 74 of the repositories found (five of them cut at 512,000 bytes), two web searches, and the works citing [IRW21] in OpenAlex (four: the two above, [Orden2] and an SSRN record with the title of X. Zeng's paper listed above, doi:10.2139/ssrn.7416699, which was not opened); also the description of the Zenodo record of J. Mackey and A. T. Mat, The directed Ramsey number R(7) is at most 45 (doi:10.5281/zenodo.24446589, 2026-11-22), which concerns tournaments; and four searches of the public data of the Palomar registry of Lean 4 formalizations (palomar-registry.org) and a search of its feed of 200 recent entries, which returned two entries on #112, both Orden's: PALOMAR-2026-11-15-000004 (his bounds on k(6,3)) and PALOMAR-2026-11-22-000008 (the four bounds of [Orden2]).

*Not read:*
- The Lean files of [OrdenLean] and of Tyorden/erdos-112-small-bounds-lean, whose README says they prove the four bounds of [Orden2]. Nothing of either was built here.
- Not read again since 2026-11-11: erdosproblems.com/112 and its forum thread. [Orden2] reports a read of the thread on 2026-11-20 that found no bound above its own for its four cases.
- Not read again on 2026-11-25: the OEIS entries and the k(3,4) = 21 page of Erdős Problem a Day. Its #112 report and its progress page were fetched on 2026-11-25 and searched by program for values of the three quantities, and were not read in full again.
- The files of the three #112 folders added to pw/erdosproblemaday-verification since 2026-11-11, apart from their READMEs. [EPAD] and [EPAD2] name these folders as the bundles of their checks.
- M. Chen, Y. Kou, X. Ma and S. Zhang, TT3-factors in oriented graphs with low independence number, Discrete Math. 349 (2026) 115229, doi:10.1016/j.disc.2026.115229.
- Library only: F. Harary and P. Hell, Generalized Ramsey theory for graphs V. The Ramsey number of a digraph, Bull. London Math. Soc. 6 (1974) 175-182 (main text); J. Bang-Jensen and F. Havet, Tournaments and semicomplete digraphs, chapter 2 of *Classes of Directed Graphs* (Springer, 2018), section 2.7.1; A. Benhocine's 1977 thesis (Paris VI).
- Not reachable from our machine: the Google Scholar and MathSciNet lists of works citing [IRW21].
- Also not read in full: the ordinal-partition sources of Rosenstein (1982, chapter 11), Williams (1977, chapter 7), Nosal, Milner, and Hajnal and Larson (2010); Wang, Wang and Yan, arXiv:2606.14161; Chen, Miao and Zhou, J. Comb. Optim. 51 (2026) 15 (publisher preview only).

The exact values of all three numbers are open.

## 7. What would falsify this

- Seven pairwise non-adjacent vertices or a transitive triangle in `k73_N38.json`; eight pairwise non-adjacent vertices or a transitive triangle in `k83_N46.json`; three pairwise non-adjacent vertices or a transitive tournament on six vertices in `k36_N72.json`. Part G's checker prints such a set when it meets one.
- A file whose SHA-256 differs from section 4.
- For priority, not for truth: a source dated before the release that states k(3,6) ≥ 73 or a larger lower bound for k(3,6).
- For the entry of section 5 on G38 and G46, which is not a claim to a bound: a failure of `scripts/check_same_graphs.py`.

## 8. Questions

1. The three numbers lie in [39, 45], [47, 59] and [73, 137] (the last using k(3,4) = 21). Where are the true values? The bound m^2 - m + 3 of [IRW21] is attained for m = 3, 4 and 5, and [Orden] puts k(6,3) below it (a written proof that, by its own account, is not peer reviewed, and a Lean 4 proof in [OrdenLean] that was not built here); how far below it are k(7,3) and k(8,3)?
2. G38 and G46 have a semiregular automorphism of prime order with two orbits, and G72 is a Cayley digraph of a non-cyclic abelian group. Is there an algebraic family behind them that reaches other pairs (n, m)?
3. Two records, [Orden2] and the files of this release, hold the same graph on 38 vertices and the same graph on 46 vertices, up to relabelling. Is G38 the only oriented graph on 38 vertices with no transitive triangle and no seven independent vertices that has an automorphism of order 19 with two orbits, and G46 the only one of its kind on 46 vertices? What happens with no symmetry assumed?

## References

- [Ber74] J.-C. Bermond, Some Ramsey numbers for directed graphs, Discrete Math. 9 (1974) 313-321, doi:10.1016/0012-365X(74)90077-6.
- [Blo] T. F. Bloom, Erdős Problem #112, https://www.erdosproblems.com/112, accessed 2026-11-11.
- [EPAD] Erdős Problem a Day (P. White with Claude), "#112, oriented Ramsey numbers: k(6,3) is 30, 31 or 32. Tyler Orden's bounds check out, and four more small cases move up", 2026-11-22, https://erdosproblemaday.com/day/112-orden-k63-between-30-and-32-and-four-new-lower-bounds, with the review of [Orden2] at https://erdosproblemaday.com/submission/eqf2h6; accessed 2026-11-25.
- [EPAD2] Erdős Problem a Day, page of 2026-11-18 on the certificates of [PartG], https://erdosproblemaday.com/day/112-kirtchakov-k34-certificates-checked-by-a-verified-checker; accessed 2026-11-25.
- [ErRa67] P. Erdős and R. Rado, Partition relations and transitivity domains of binary relations, J. London Math. Soc. 42 (1967) 624-633, doi:10.1112/jlms/s1-42.1.624.
- [IRW21] F. Ihringer, D. Rajendraprasad and T. Weinert, New bounds on the Ramsey number r(I_m, L_n), Discrete Math. 344 (2021), no. 3, 112268; arXiv:1707.09556.
- [Orden] T. S. Orden, New bounds on the Erdős-Rado number k(6,3): 30 <= k(6,3) <= 32, Zenodo (2026-11-09), doi:[10.5281/zenodo.24064871](https://doi.org/10.5281/zenodo.24064871); version 2 (2026-11-16), doi:10.5281/zenodo.24272287.
- [Orden2] T. S. Orden, New lower bounds for small Erdős-Rado numbers k(7,3), k(8,3), k(6,4) and k(3,6) (Erdős problem #112), Zenodo (2026-11-20), version 1.0, doi:[10.5281/zenodo.24390891](https://doi.org/10.5281/zenodo.24390891).
- [OrdenLean] T. S. Orden, Erdős Problem #112: a machine-checked proof that 30 ≤ k(6,3) ≤ 32 (Lean 4), Zenodo, version 1.3 (2026-11-16), doi:10.5281/zenodo.24272901; all versions, doi:10.5281/zenodo.24237180.
- [PartG] D. Kirtchakov, An Erdős-Rado oriented Ramsey number determined: k(3,4) = r(I_3, L_4) = 21, Certify v0.7.0 (2026), doi:10.5281/zenodo.21890619.
- [rsv] rsvaultpudgy-create, erdos-112-lower-bounds, GitHub, CC0, commit d305711817 (2026-11-11), https://github.com/rsvaultpudgy-create/erdos-112-lower-bounds.
