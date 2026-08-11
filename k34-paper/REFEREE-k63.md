# Adversarial referee report — SECONDARY claim: 29 ≤ k(6,3) ≤ 33

**Referee:** independent verifier (own checker, wrote from raw definitions; shared nothing with
the finder or prior checkers).
**Date:** 2026-08-11
**Object under test:** the note's claim `29 ≤ k(6,3) ≤ 33`, where `k(6,3) = r(I_6, L_3)` is the
least N such that every oriented graph on N vertices contains an independent set of size 6 (I_6)
or a transitive tournament on 3 vertices (TT_3 = L_3). The lower bound rests on an explicit
28-vertex witness stated as `Cay(Z_28, {3,8,10,12,17})`.

---

## VERDICT: **CONFIRMED.** 29 ≤ k(6,3) holds. Combined with IRW's upper bound, **29 ≤ k(6,3) ≤ 33 stands at full strength.**

- **alpha (independence number of the primary witness) = 5 exactly** (not 6). So no I_6.
- The witness is TT_3-free: **0** transitive triples out of 112 tournament-triples (all 112 are directed 3-cycles).
- The witness is a genuine oriented graph (S ∩ −S = ∅; no 2-cycles, no loops), and its shipped
  arcs match the Cayley definition `u→v ⟺ (v−u mod 28) ∈ {3,8,10,12,17}` **exactly** (140/140 arcs).

---

## 1. The witnesses located and read (7 total)

| file | N | type | S / structure |
|---|---|---|---|
| `witness_cayley_6_3_n28_3_8_10_12_17.json` | 28 | Cay(Z_28, S) — **PRIMARY** | {3,8,10,12,17} |
| `witness_cayley_6_3_n28_4_5_6_19_26.json` | 28 | Cay(Z_14×Z_2, S) (group="14,2") | {4,5,6,19,26} |
| `witness_cayley_6_3_n27_5_9_11_13_17.json` | 27 | Cay(Z_27, S) | {5,9,11,13,17} |
| `witness_cayley_6_3_n26_4_11_18_20_21.json` | 26 | Cay(Z_26, S) | {4,11,18,20,21} |
| `witness_tw_6_3_28.json` | 28 | twisted construction | — |
| `witness_tw_6_3_26.json` | 26 | twisted construction | — |
| `witness_ls_6_3_26.json` | 26 | local-search graph | — |

**No witness reaches N ≥ 29.** The largest is N=28, so these witnesses support k(6,3) ≥ 29 and
cannot push the lower bound any higher. (Copies also exist in `method/erdos-112/`.)

## 2. Independent checker (written from raw definitions — did NOT reuse the shipped score-sequence TT_3 criterion)

Checker: `/private/tmp/.../scratchpad/referee_k63.py`. For each witness it (a) re-derives Cayley
arcs from scratch and compares to the shipped list; (b) tests TT_3-freeness by **two** independent
methods that must agree — a direct pattern search for `x→y, y→z, x→z`, and a full scan of every
C(N,3) triple classifying each 3-vertex tournament as transitive vs. 3-cycle; (c) computes the
independence number **exactly** by branch-and-bound, cross-checked by an **exhaustive** scan of all
C(28,6)=376,740 six-subsets for any independent one, plus exhibiting a genuine independent 5-set.

### Primary witness `Cay(Z_28,{3,8,10,12,17})` — full result

```
N=28, #arcs(distinct)=140, #arcs(listed)=140
Cayley S=[3,8,10,12,17], group=Z_28
S ∩ −S = []                         (EMPTY  -> oriented, no 2-cycles)
derived arcs from Cay(Z_28,S): 140; match shipped: True   <-- object IS the stated circulant
(a) 2-cycles/loops: NONE (oriented OK)
(b) triples: full-tournaments=112, transitive(TT_3)=0, 3-cycles=112
    TT_3 pattern-search  : NONE
    TT_3 combination-scan: NONE      -> TT_3-free: True
(c) independence number alpha = 5   (witness independent set {0,1,2,6,15}, verified independent)
    exhaustive: independent 6-sets = 0   -> alpha < 6
    an independent 5-set exists (e.g. {0,1,2,6,7}) -> alpha >= 5   => alpha = 5 EXACTLY
==> {I_6,TT_3}-FREE = PASS  (supports k(6,3) >= 29)
```

### All seven witnesses PASS

| file | N | alpha | TT_3-free | I_6-free | PASS | supports |
|---|---|---|---|---|---|---|
| cayley n28 {3,8,10,12,17} | 28 | **5** | yes (0/112) | yes | ✔ | k(6,3) ≥ 29 |
| cayley n28 {4,5,6,19,26} | 28 | 5 | yes (0/112) | yes | ✔ | k(6,3) ≥ 29 |
| cayley n27 {5,9,11,13,17} | 27 | 5 | yes (0/117) | yes | ✔ | k(6,3) ≥ 28 |
| cayley n26 {4,11,18,20,21} | 26 | 5 | yes (0/104) | yes | ✔ | k(6,3) ≥ 27 |
| tw n28 | 28 | 5 | yes (0/112) | yes | ✔ | k(6,3) ≥ 29 |
| tw n26 | 26 | 5 | yes (0/78) | yes | ✔ | k(6,3) ≥ 27 |
| ls n26 | 26 | 5 | yes (0/87) | yes | ✔ | k(6,3) ≥ 27 |

Two independent N=28 witnesses (the primary circulant and the twisted construction) both give the
lower bound 29. The alpha computation was confirmed a second, fully independent way (exhaustive
6-subset scan = 0, plus an exhibited 5-set), so **alpha = 5 is definitional, not algorithm-dependent.**

## 3. Novelty — is any lower bound for k(6,3) published?

The quantity is **Erdős Problem #112**: k(n,m) = least k such that every oriented (directed) graph
on k vertices has an independent set of size n or a transitive tournament of size m; equivalently
IRW's r(I_m, L_n). erdosproblems.com/112 lists only *general* bounds and marks the problem **open**:
Erdős–Rado k(n,m) ≪ n^(m−1); Larson–Mitchell k(n,3) ≤ n²; Zach Hunter's R(n,m) ≤ k(n,m) ≤ R(n,m,m).
(erdosproblems.com returned HTTP 403 to a direct fetch; content read via its search index.)

The canonical reference **Ihringer–Rajendraprasad–Weinert, "New bounds on the Ramsey number
r(I_m, L_n)", arXiv:1707.09556 (Discrete Math. 2021)** — read via the ar5iv HTML full text — gives:
> upper bound "r(I_m, L_3) ≤ m² − m + 3" (Prop. 3.4);  r(I_m,L_3) = Θ(m²/log m) (Thm 1.2)

and exact values **only up to m=5**:
> r(I_3,L_3)=9 (Bermond), r(I_4,L_3)=15, r(I_5,L_3)=23 (Thm 1.1),

with explicit extremal constructions on 8, 14, and 22 vertices respectively. **IRW give NO value
and NO lower bound for r(I_6,L_3);** their only m=6 statement is the upper bound m²−m+3 = **33**.

- The note's **upper bound 33 is IRW's** (m²−m+3 at m=6) — correctly attributed, not claimed as ours.
- The only lower bound implied by the prior literature is the trivial `k(6,3) ≥ R(6,3) = R(3,6) = 18`
  (from Hunter's R(n,m) ≤ k(n,m)). **The note's 29 improves this by 11.**
- Targeted searches (recent arXiv 2024–2026; oriented-Ramsey / circulant constructions; the
  Mathon-type digraph-Ramsey paper arXiv:2408.04067, which concerns *multicolor directed* Ramsey
  numbers, a different quantity) surfaced **no published lower bound of 29, nor any lower bound for
  k(6,3) beyond the trivial 18.** Caution against a false hit: "r⃗(6)=28" appearing in searches is
  the *classical* R(6)=28 (least n forcing TT_6 in a complete tournament) — an unrelated quantity;
  the 28 coincidence is spurious.

**Novelty conclusion: SUPPORTED.** No prior lower bound for k(6,3) beyond the trivial R(3,6)=18 is
published anywhere located; 29 ≤ k(6,3) is new. (Standard referee caveat: web search cannot prove a
negative with certainty, but the canonical source and the Erdős-problem page both stop short of any
m=6 lower bound.)

## 4. The exact defensible sentence

> **k(6,3) = r(I_6, L_3) satisfies 29 ≤ k(6,3) ≤ 33.** The lower bound is witnessed by the oriented
> circulant Cay(Z_28, {3,8,10,12,17}) — a 28-vertex oriented graph with independence number exactly
> 5 (hence no I_6) and containing no transitive triangle TT_3 (all 112 of its 3-vertex tournaments
> are directed 3-cycles) — and is new; the upper bound 33 = 6²−6+3 is due to Ihringer, Rajendra-
> prasad and Weinert (arXiv:1707.09556).

Do **not** claim more than ≥ 29 from these witnesses (none exceeds N=28). Do **not** attribute the
upper bound to this work.
