# Erdős Problem #1111: d(3,3) ≥ 6 — staging

**Status: staged, not released.** Everything below is verified. There is no
note, dated sweep record or DOI yet.

**Result.** El Zahar and Erdős (Combinatorica 5 (1985) 295–300) proved
d(3,3) ≤ 8, and no lower bound for d(3,3) is recorded on the problem page. The
Mycielskian of the Grötzsch graph, M(M(C₅)), on 23 vertices has three
properties:
* it is triangle-free;
* it is not 4-colourable (LRAT-certified);
* it has no two anticomplete non-bipartite vertex sets.

Hence **d(3,3) ≥ 6**, and the recorded bracket becomes 6 ≤ d(3,3) ≤ 8. The
property is certified three independent ways:
* exhaustive induced-odd-cycle enumeration (Criterion A);
* an all-pairs test (Criterion B);
* an LRAT-certified SAT encoding (Criterion C), which shares no code with the
  enumeration.

Three further 5-chromatic witnesses pass the same checks:
* M(Chvátal) (25 vertices);
* M(Clebsch) (33 vertices);
* the circulant Cay(ℤ₂₉, {±2,±5,±6,±14}), the only one that is not a Mycielskian.

**Also proved (pen and paper, below).** Two structural lemmas:
* **Lemma 3.** No generalized Mycielskian M_r(H) of any base can witness
  d(3,3) ≥ 7.
* **Lemma 4.** An odd-girth argument reproves d(3,3) ≤ 8. It also shows that a
  7-chromatic witness (which would give d(3,3) = 8) needs odd girth exactly 5 and
  χ(G[N[C]]) = 5 for every 5-cycle C.

## Replay

```sh
sh e1111-certificates/run_all.sh     # about 3 s; ends "ALL EXPECTATIONS MET"
```

The script covers:
* 24 positive checks on the four witnesses: graph checker, construction
  check, CNF audits, and LRAT replays by Part G's `k34-scripts/lrat_check.py`;
* the Lemma 4 colouring check;
* 14 tamper controls, each rejected.

Every checker is standard-library Python. CaDiCaL 3.0.1 (`--lrat`) was used
only to produce the proofs.

## Independent verification (2026-09-26)

An adversarial referee agent rebuilt all four graphs from textbook
definitions and checked them with its own code: its own induced-cycle DFS, an
N[C] bipartiteness test, and exhaustive DSATUR colouring. It had not read
`check_P.py`, `audit_cnf.py`, `gen_cnf.py` or `check_construction.py`. It
re-derived and compared the CNFs and replayed all eight LRAT proofs. It passed
83 of 83 controls for M(M(C₅)), among them:
* all 71 single-edge deletions become 4-colourable;
* all 182 single-edge additions create a triangle;
* six classes of proof and CNF corruption are rejected.

The orchestrating session independently reproduced the count of 646 induced
odd cycles and the absence of any anticomplete pair with its own enumerator,
before this certificate was built.

## Priority record (2026-09-26)

A skeptical novelty audit found no published or online statement of any lower
bound d(3,3) ≥ 6.
* **The problem page.** The erdosproblems.com/1111 text (scrape of 2026-07-10;
  page last edited 2025-12-07) gives only d(3,3) ≤ 8, and small values only for
  c = 2. The teorth database lists it as open, unchanged through 2026-09-22.
* **Other repositories.** JSP, lean-genius, DeepMind formal-conjectures and
  several LLM-attack repositories have nothing beyond d(3,3) ≤ 8.

Caveats a release must state:
* **Precursor.** The public repository `przchojecki/agentic-erdos` (March 2026)
  sampled this same 23-vertex graph for this property at random, 2000 samples,
  and found no pair. It did not state a bound. The same repository's exhaustive
  scan of the Grötzsch graph implicitly gives d(3,3) ≥ 5, which is essentially
  folklore. What is new here is the exhaustive, certified determination and
  the bound as stated.
* **Unread full text.** The El Zahar–Erdős full text was not readable in this
  session (proxy-blocked). Bloom's summary lists no lower bound.
* **Significance.** It is modest: a finite check on a textbook graph moves the
  unrecorded bracket to [6, 8]. The structural lemmas explain why d(3,3) ≥ 7 is
  harder.

---

**Definition.** d(t,c) is the least d such that every graph G with chi(G) >= d and omega(G) < t has disjoint
anticomplete sets A, B (no edge between them) with chi(G[A]) >= chi(G[B]) >= c. El Zahar–Erdős (1985) proved d(3,3) <= 8.

**Property P.** G has property P if no two disjoint anticomplete sets both induce non-bipartite subgraphs.
For c = 3, "chi >= 3" is the same as "non-bipartite". So a triangle-free G with chi(G) >= k and property P shows
d(3,3) >= k+1: if d(3,3) <= k, then G would have to contain such a pair.

## Claims, stated at the strength the checkers support

| # | Claim | Status | Evidence |
|---|-------|--------|----------|
| 1 | **d(3,3) >= 6.** G = M(M(C5)) (Mycielskian of the Grötzsch graph, 23 vertices, 71 edges) is triangle-free, not 4-colourable, and has P. | **CERTIFIED** | `graphs/mmc5.edges`; `check_P.py` (Criteria A and B); LRAT `proofs/mmc5_col4.lrat` (not 4-colourable); LRAT `proofs/mmc5_pair.lrat` (Criterion C, P again, independently of cycle enumeration) |
| 1b | Three more triangle-free graphs have P and are not 4-colourable: M(Chvátal) (25 v), M(Clebsch) (33 v), circulant Cay(Z_29, {±2,±5,±6,±14}). | **CERTIFIED** (same checks) | `graphs/{mchvatal,mclebsch,circ29}.edges` plus their CNFs and LRAT proofs |
| 2 | A triangle-free graph with chi >= 6 and P (would give d(3,3) >= 7) | **not_found** | searches below; none are exhaustive |
| 3 | A triangle-free graph with chi >= 7 and P (would give d(3,3) = 8) | **not_found** | same searches; Lemma 4 limits where such a graph could be |
| L | Lemmas 1–4 below (proofs in this README). Lemma 3 rules out every generalized Mycielskian as a witness for chi >= 6. Lemma 4 says a chi >= 7 witness needs odd girth 5 and chi(G[N[C]]) = 5 for **every** 5-cycle C. | proved (pen and paper); the colourings used in Lemma 4 are also checked by `check_lemma_colourings.py` | |

Only chi >= 5 is claimed for G, which is all that d >= 6 needs (chi = 5 exactly also follows from Mycielski's theorem, but nothing here relies on it).

## How to verify (python3 stdlib only)

```
sh e1111-certificates/run_all.sh      # runs every check below plus 14 tamper controls; ends with "ALL EXPECTATIONS MET" (38 [ok] lines)
```
Individual commands:
```
python3 check_P.py graphs/mmc5.edges                         # triangle-free + Criteria A, B -> PASS
python3 check_P.py graphs/mmc5.edges --pruned                # Criterion A with the pruned DFS -> PASS
python3 check_construction.py mmc5 graphs/mmc5.edges         # file is exactly M(M(C5)) -> PASS
python3 audit_cnf.py col graphs/mmc5.edges 4 cnf/mmc5_col4.cnf   # CNF = from-definition 4-colouring CNF + edge symmetry break
python3 ../k34-scripts/lrat_check.py cnf/mmc5_col4.cnf proofs/mmc5_col4.lrat   # VERIFIED (217 steps)
python3 audit_cnf.py pair graphs/mmc5.edges cnf/mmc5_pair.cnf    # CNF = from-definition anticomplete-pair CNF
python3 ../k34-scripts/lrat_check.py cnf/mmc5_pair.cnf proofs/mmc5_pair.lrat   # VERIFIED (571 steps)
```
How the CNFs and proofs were made (not needed to verify them): `python3 gen_cnf.py col graphs/mmc5.edges 4 0 1`, `python3 gen_cnf.py pair graphs/mmc5.edges`,
and CaDiCaL 3.0.1 `cadical --lrat --no-binary -q F.cnf P.lrat`. Graphs come from `generators/build_graphs.py` (`mmc5`, `mchvatal`, `mclebsch`) and the circulant definition.
The tamper controls cover:
- graphs that fail P: M^3(C5), M(M(Chvátal)), and two disjoint C5s (also with `--pruned`);
- corrupted graph files: an added triangle edge, a repeated edge;
- corrupted CNFs: an extra unit clause, a foreign unit clause;
- proofs replayed against the wrong formula: Grötzsch 4-colouring, 5-colouring, and M^3(C5) pair CNFs;
- a proof with one hint removed;
- a wrong construction.

Every one is rejected.

sha256 prefixes: mmc5.edges a864b6c19b2b8270, mmc5_col4.cnf 56931fd660f6d649, mmc5_col4.lrat 68815e58feab3efd,
mmc5_pair.cnf a02d88f7ab4a685a, mmc5_pair.lrat 6d80af2259b6fd09.

## What each check proves

**Lemma 0 (equivalence).** The following are equivalent for any graph G:
- (a) G has disjoint anticomplete A, B with G[A] and G[B] both non-bipartite;
- (b) some induced odd cycle C has G − N[C] non-bipartite;
- (c) G has two vertex-disjoint induced odd cycles with no edge between them.

*Proof.*
- (a)⇒(c): a shortest odd cycle of G[A] is induced, because a chord would split it into two shorter cycles and one of them is odd. Being induced in G[A], it is induced in G. Take the same kind of cycle in G[B]. The two cycles are disjoint and have no edge between them.
- (c)⇒(b): C2 avoids N[C1], so G − N[C1] contains the odd cycle C2.
- (b)⇒(a): take A = V(C) and B = V(G) − N[C].

∎ Also, a pair of induced cycles C1, C2 is disjoint and anticomplete if and only if V(C2) ∩ N[C1] = ∅.

- **(1) Triangle-free.** For every edge uv, `check_P.py` checks N(u) ∩ N(v) = ∅.
- **Criterion A (`check_P.py`).** A DFS lists every induced cycle exactly once. It starts from the cycle's minimum vertex s, extends induced paths through vertices > s, and closes a cycle when the new vertex is adjacent to s and the last path vertex and to nothing else. It keeps the orientation with c1 < c_last.
  - *Completeness:* for an induced cycle (c0 = min, c1, …, c_{L−1}) with c1 < c_{L−1}, every prefix c0…c_j is an induced path. c_{j+1} is adjacent to no earlier path vertex except c_j, and to c0 only when j+1 = L−1. So the DFS reaches the cycle and records it once.
  - The checker also re-checks that each listed cycle is induced, odd and not a duplicate.
  - For each listed cycle it builds a 2-colouring of G − N[C] and re-checks it on every edge.
  - By Lemma 0(b), this proves P. For M(M(C5)) there are 646 induced odd cycles (616 of length 5, 30 of length 7).
- **Criterion B (`check_P.py`).** Among all listed cycles, no pair satisfies V(C2) ∩ N[C1] = ∅. By Lemma 0(c) this proves P again. It does not use the bipartiteness routine (208 335 pairs for M(M(C5))).
- **`--pruned` mode.** If an induced path P is part of a cycle C, then N[P] ⊆ N[C], so G − N[C] is an induced subgraph of G − N[P]. If G − N[P] is bipartite, every cycle that extends P is fine, and the DFS stops extending P. This rule is sound and keeps the search exhaustive. The C++ search tool `pcheck` (not shipped) uses the same rule.
- **Criterion C (`gen_cnf.py pair`, checked by `audit_cnf.py pair` and `lrat_check.py`).** The formula uses these variables:
  - x_e and y_e for edges; a_v and b_v for vertices; two XOR chains of auxiliary variables.
  - **Degree clauses:** every vertex has x-degree 0 or 2, and y-degree 0 or 2.
  - **Parity:** the XOR of all x_e is 1, and likewise for y.
  - **Links:** x_e → a_u and a_w; y_e → b_u and b_w.
  - **Disjoint and anticomplete:** ¬a_v ∨ ¬b_v for every vertex v; ¬a_u ∨ ¬b_w and ¬a_w ∨ ¬b_u for every edge uw.

  *Soundness of UNSAT:* suppose C1 and C2 form a pair as in Lemma 0(c). Set x = E(C1), y = E(C2), a = 1 exactly on V(C1), b = 1 exactly on V(C2), and let each chain variable be the prefix XOR. Every clause is then satisfied (the parity holds because |E(Ci)| is odd). So UNSAT means no such pair, which is P.

  This criterion shares no code with the cycle enumeration. `audit_cnf.py` re-derives the clause set independently and checks that every clause of the file belongs to it. Only this direction matters for UNSAT: a subset of a satisfiable clause set is satisfiable. It also reports that the full encoding is present.
- **Not 4-colourable (`gen_cnf.py col`, checked by `audit_cnf.py col` and LRAT).**
  - Clauses: every vertex gets at least one colour, and for every edge and colour the two ends do not share it. No at-most-one clauses are included; this only weakens the formula, and any satisfying assignment still yields a proper colouring by picking one true colour per vertex.
  - Symmetry break: units x[U,0] and x[V,1] for an **edge** UV. It is sound because a proper colouring f has f(U) ≠ f(V), and permuting colours sends f(U) to 0 and f(V) to 1.
  - The audit rejects any extra clause other than two such units on an edge.
  - The LRAT proof of UNSAT, replayed by `../k34-scripts/lrat_check.py`, gives chi(G) >= 5.

## Proved structural lemmas (these narrow the chi >= 6 search)

**Lemma 1.** P is hereditary: it passes to induced subgraphs, because anticomplete sets in G[S] are anticomplete in G. Adding a twin vertex (a copy with the same neighbourhood, not adjacent to the original) also preserves P. The twin argument is short: in an anticomplete pair, replace the twin by the original. The twin does not raise chi.

**Lemma 2 (property Q forces chi <= 4).** Call a triangle-free H "Q" if for every induced odd cycle C, H − N[C] has no edges.
- Q is equivalent to: for every edge uv, H − (N[u] ∪ N[v]) is bipartite. If that graph had an odd cycle, a shortest one C is induced and misses N[u] ∪ N[v], so u, v ∉ N[C], and uv is an edge of H − N[C].
- N[u] ∪ N[v] = N(u) ∪ N(v) is a union of two independent sets.
- Hence chi(H) <= 2 + 2 = 4.

**Lemma 3 (no Mycielski-type witness).** For r >= 1, if the generalized Mycielskian M_r(H) of a triangle-free H has P, then H is Q. Here M_r(H) has layers V_0 = H, …, V_r, edges (u,i)~(v,i+1) for uv ∈ E(H), and an apex joined to V_r; M = M_1.

*Proof.* Let C be an induced odd cycle of H in V_0, and let uv be an edge of H − N_H[C]. Consider the closed walk that goes (u,0) (v,0), then climbs (u,1), (v,2), … alternately up to V_r, goes to the apex, and climbs back down the other alternating path to (u,0). It is a cycle of length 2r+3 and it avoids N[C]:
- layers >= 2 and the apex are not adjacent to V_0;
- (w,1) ∈ N[C] only when w ∈ N_H(C);
- u and v lie outside N_H[C].

So G − N[C] is not bipartite. ∎

*Consequence:* if M_r(H) has P, then chi(H) <= 4 by Lemma 2, so chi(M_r(H)) <= chi(H)+1 <= 5. **No generalized Mycielskian, of any base and any r, can witness d(3,3) >= 7.**

This also explains the failures observed in the probe: M^3(C5), M(M(Chvátal)) and M(M(Clebsch)) have 5-chromatic bases, and M_2(M(M(C5))) was also checked and fails. The probe's passing graphs M(M(C5)), M(Chvátal) and M(Clebsch) have 4-chromatic Q bases.

**Lemma 4 (odd girth).** Let G be triangle-free with P, and let C = c_0 … c_{2k} be a shortest odd cycle.
1. chi(G) <= chi(G[N[C]]) + 2, because G − N[C] is bipartite. Note N[C] = ∪_i N(c_i), and each N(c_i) is independent.
2. For k >= 3, N(c_i) ∪ N(c_j) is independent unless the cyclic distance δ(i,j) is 1 or 3. If x ∈ N(c_i) is adjacent to y ∈ N(c_j), then x, c_i, (an arc of C), c_j, y is a closed walk of length d+3, where d is the arc length. One of the two arcs makes this length odd. If δ is even and at least 2, or odd and at least 5, that odd walk is shorter than 2k+1, which contradicts the choice of C.
3. So colouring each vertex by the index of one cycle vertex it is adjacent to maps N[C] properly into Cay(Z_{2k+1}, {±1,±3}). This circulant has chromatic number 4 for k = 3 and 3 for every k >= 4. The 3-colouring is parity on 0..2k−1, with colour 2 on {1, 2k−2, 2k}; it is verified for k <= 300 by `check_lemma_colourings.py`, and the pen proof covers all k.
4. For k = 2, N[C] is a union of 5 independent sets.

**Hence:**
- chi(G) <= 7 if the odd girth is 5 (this reproves d(3,3) <= 8);
- chi(G) <= 6 if the odd girth is 7;
- chi(G) <= 5 if the odd girth is >= 9.

**What a witness would need:**
- For d(3,3) >= 7 (chi >= 6): odd girth 5 or 7, and chi(G[N[C]]) >= 4 for every induced odd cycle C.
- For d(3,3) = 8 (chi >= 7): odd girth 5, and chi(G[N[C]]) = 5 for **every** 5-cycle C.

The witnesses found here do not meet this. In M(M(C5)), chi(G[N[C5]]) is 3 for 47 of 400 sampled 5-cycles (uncertified SAT; the script is not shipped).

## Search for chi >= 6 with P (claims 2 and 3). All negative results are uncertified and non-exhaustive.

The P tester was `pcheck` (C++, not shipped). It uses the exhaustive DFS with the pruning rule above. It prints PASS or FAIL, and on FAIL it prints a witness: an induced odd cycle C and an odd cycle in G − N[C]. The `vt` option (start only from vertex 0) is used only for Cayley graphs, which are vertex-transitive. Chromatic numbers in the searches come from CaDiCaL via pysat and are uncertified.

| Family | Result |
|---|---|
| Schrijver SG(2k+2,k), k = 3,4,5 (chi 4) | PASS |
| SG(11,4), SG(13,5), SG(15,6) (chi 5); SG(14,5), SG(16,6) (chi 6); SG(17,6) (chi 7); Kneser KG(11,4) | all FAIL, witnesses in `pcheck` output; SG(14,5) already fails with a 5-cycle |
| Higman–Sims graph (100 v; not 5-colourable, CaDiCaL, 40 s) | FAIL: all 22 176 induced 5-cycles through a vertex fail |
| M22 graph (77 v; not 4-colourable) | FAIL: 5760 of 5760 5-cycles through a vertex fail |
| Generalized Mycielskians | ruled out by Lemma 3; spot checks M^3(C5), M(M(Chvátal)), M(M(Clebsch)), M_2(M(M(C5))), M(M_3(C7)) all FAIL; M_2(Grötzsch) and M_3(C7) PASS (chi <= 5) |
| Random maximal sum-free circulants, n = 13..60, seed 1 (~740 distinct up to multipliers) | P-passing with chi 5: 10 (e.g. n = 29, 30, 42, 59); chi 6: 0 |
| Same, n = 60..130, seed 2 (14 392 distinct) | 728 pass P (chi 3: 242, chi 4: 477, chi 5: 9); none has chi >= 6 |
| Same, n = 40..100, seed 7 | one chi-6 circulant (Z_81, degree 18); it FAILS P badly (6860 of 8561 5-cycles through 0) |
| Same, n = 130..220, seed 9 (10 min, 96 453 distinct) | 892 pass P (chi 3: 287, chi 4: 604, chi 5: 1 at n = 142); none has chi >= 6; 1 hit the node limit (undecided) |
| Cayley graphs on 21 abelian groups of order 64–243 (random maximal sum-free S, seed 5, 9 min) | P-passing chi-5 graphs in Z2^2×Z3×Z7 and Z3^3×Z5 (search log not shipped); none has chi >= 6 |
| Greedy vertex extension (not shipped) from M(M(C5)), M(Chvátal), M(Clebsch), M_2(Grötzsch); seeds 1 and 11–30 | 81 runs; each adds a vertex whose independent neighbourhood is rainbow in sampled 5-colourings, keeping P (checked exhaustively) |
| Result of the vertex-extension runs | every run got stuck (no admissible neighbourhood found) at 36–61 vertices while still 5-colourable |

**Status of targets:**
- chi >= 6 with P: **not found**.
- chi >= 7 with P: **not found**.
- Nothing is claimed about their existence.

Lemmas 3 and 4 show that Mycielski-type constructions cannot work, and that any chi-7 example must be extremely tight around every 5-cycle.

## Files

* **Checkers** (standard library): `check_P.py`, `audit_cnf.py`, `check_construction.py`, `check_lemma_colourings.py`; `gen_cnf.py` generates the CNFs from the definitions; `run_all.sh` runs everything.
* **Certificates:**
  * `graphs/`: edge lists, first line `n m`. The four witnesses, plus the control graphs M³(C₅), M(M(Chvátal)) and Grötzsch, and the base graphs.
  * `cnf/`: the 4-colouring and anticomplete-pair formulas.
  * `proofs/`: text LRAT, 2.5 MB in total.
* **Generator** (untrusted, not needed to verify): `generators/build_graphs.py`.
