# Dated novelty and verification sweep — k(3,4) uniqueness addendum (Part J)

Scope of the new content: the **multiplicity** of the 20-vertex extremal graph
for k(3,4) = r(I_3,L_4) = 21 (Question 8.1 of Part G), the QR_7 forcing lemma,
and the tournament-blow-up bound.

## Novelty (2026-08-11)

* The value k(3,4) = 21 itself has no prior appearance beyond Part G (Certify
  v0.7.0, DOI 10.5281/zenodo.21890619, published 2026-08-11): erdosproblems.com/112
  records OPEN with no exact k(n,m); Ihringer–Rajendraprasad–Weinert (IRW,
  Discrete Math. 344 (2021) 112268; arXiv:1707.09556) remains the only paper on
  r(I_m,L_n). Since the value is brand new, the *number of extremal graphs* for
  it is a fortiori new. Web sweep on the drafting date returned nothing on the
  count or uniqueness of 20-vertex {I_3,TT_4}-free oriented graphs.
* The QR_7 forcing lemma is elementary and NOT claimed as new: it combines the
  local {I_3,TT_4}-freeness argument with two classical tournament facts —
  v(4) = 8 (tournament Ramsey; Erdős–Moser 1964) and the uniqueness of the
  7-vertex TT_4-free tournament as the Paley tournament QR_7 (A. Sánchez-Flores,
  "On tournaments free of large transitive subtournaments", Graphs Combin. 14
  (1998), 181–200). Both were re-established here by exhaustive enumeration and match Part G,
  Prop. 3.3. The lemma is presented as an explanation of the observed structure,
  not a standalone result.
* The blow-up bound r(I_3,L_m) ≥ 2·v(m) − 1 (giving 15 at m = 4) is a standard
  product observation, likely implicit in IRW's product bounds; novelty not
  claimed. The load-bearing new content is the negative answer to Question 8.1
  and the rigidity of the exhibited family.

## Independent verification (2026-08-11)

All checks re-derived by code that shares only boilerplate with the SAT search
(25, 32 and 11 lines of 115, 174 and 51, all of them returns, loop headers or
main-guards). It is NOT code-independent of the structure-mining dig
(`hunt-structure/`, private): 24, 30 and 9 executable lines are verbatim from it,
and `tour_iso`, `qr7`, `adj` and the backtrackers inside `aut_count` and `iso`
are the same routines, PEP8-expanded from a compressed original with their local
names preserved. What the dig did not supply — the tournament enumerator, the
automorphism counter, the TT_4 detector, the Weisfeiler-Leman refinement, the
canonical form — is what the two load-bearing conclusions actually rest on; see
the methods note for the orbit-stabilizer argument that makes the shared
isomorphism test redundant.

* 13 witnesses (w01_W = the Part G graph W; w02–w13): each a valid oriented
  graph, exhaustively {I_3,TT_4}-free over all C(20,3)=1140 triples and
  C(20,4)=4845 quadruples; each rigid, |Aut| = 1, certified twice (WL refinement
  discrete at 20 colours; explicit automorphism count = 1); all 78 pairs
  non-isomorphic (distinct canonical forms AND distinct invariant fingerprints).
  Number I can certify: **13**.
* QR_7 lemma inputs: exactly 240 labelled TT_4-free tournaments on 7 vertices,
  every one isomorphic to QR_7; 0 on 8 vertices; |Aut(QR_7)| = 21; 240 = 7!/21.
* Blow-up: QR_7[I_2] free on 14 vertices, QR_7[I_3] not I_3-free; largest
  tournament-blow-up witness = 14 vertices, bound k(3,4) ≥ 15, truth 21, gap 6.
* Checkers stdlib-only, run on CPython 3.14.2 and 3.9.6 with identical PASS
  verdicts; no threads, subprocess, or OS-specific calls.

## Public claim (exact strength)

Question 8.1 of Part G is answered in the negative: the 20-vertex extremal graph
for k(3,4) = r(I_3,L_4) = 21 is not unique. There are **at least thirteen**
pairwise non-isomorphic {I_3,TT_4}-free oriented graphs on 20 vertices, and all
thirteen are rigid (trivial automorphism group), so the extremal configuration is
far from a single symmetric object. Whether some other extremal graph might still
be vertex-transitive or otherwise algebraic is not decided here. In any {I_3,TT_4}-free
oriented graph every vertex has at most seven non-neighbours, and a vertex with
exactly seven has its non-neighbourhood equal to the Paley tournament QR_7
(the QR_7 forcing lemma). The largest {I_3,TT_4}-free tournament blow-up has 14
vertices, six short of the extremal order 20, so the extremal family is
substantially non-algebraic. Whether every extremal witness must contain a QR_7
block (equivalently, whether the all-vertices-≤6-non-neighbours instance is
unsatisfiable) is left open.
