# Lower-bound witnesses for small oriented Ramsey numbers (Erdős Problem #112) — staging

**Status: staged, not released.** The witnesses are verified. They carry no note,
no dated sweep record and no DOI yet, and the search campaign that produced them
is still running; the bounds below may be raised before release.

k(n,m) = r(I_n, L_m) is the least N such that every oriented graph on N vertices
contains an independent set of size n or a transitive tournament on m vertices.
Each file here is an oriented graph on N vertices containing neither, so it
proves k(n,m) >= N + 1.

| file | N | proves | previously recorded lower bound | best bound buildable from published graphs | upper bound |
|---|---|---|---|---|---|
| `k63_N29.json` | 29 | k(6,3) >= 30 | 29 (Certify Part G, 2026-08-11) | 29 (Part G); 26 from the literature alone (IRW's W₂₂ + a disjoint directed 3-cycle) | 33 (IRW 2021, m²−m+3) |
| `k73_N38.json` | 38 | k(7,3) >= 39 | none explicit | 32 (Part G's ℤ₂₈ circulant + a directed 3-cycle); 31 from the literature alone | 45 (IRW 2021) |
| `k83_N46.json` | 46 | k(8,3) >= 47 | none explicit | 37 (IRW's W₂₂ + W₁₄, disjoint) | 59 (IRW 2021) |
| `k44_N39.json` | 39 | k(4,4) >= 40 | 21 (Certify Part G §8.3) | 28 (Part G's W + a disjoint QR₇); 22 from the literature alone (QR₇ blown up by I₃) | 50 (Part G §8.3) |
| `k35_N42.json` | 42 | k(3,5) >= 43 | none explicit | 27 (a 13-vertex TT₅-free tournament blown up by I₂; Part J's 2v(m)−1) | 55 (Part G §8.3) |
| `k93_N60.json` | 60 | k(9,3) >= 61 | none explicit | 45 (IRW's W₂₂ ⊔ W₂₂); 50 with this campaign's k(8,3) witness ⊔ a directed 3-cycle | 75 (IRW 2021, m²−m+3) |
| `k54_N60.json` | 60 | k(5,4) >= 61 | none explicit | 41 (Part G's W ⊔ W); 31 from the literature alone | 95 (recursion, with k(4,4) ≤ 50) |
| `k45_N71.json` | 71 | k(4,5) >= 72 | none explicit | 43 (IRW's W₁₄ blown up by a directed 3-cycle) | 154 (recursion) |
| `k36_N72.json` | 72 | k(3,6) >= 73 | 55 (Certify Part J, r(I₃,L_m) ≥ 2v(m)−1 with v(6) = 28) | 55 | 137 (recursion) |

The recursion is the neighbourhood count of [IRW21, Lemma 2.1/2.3]: in a
{I_n,TT_m}-free graph the out- and in-neighbourhoods are {I_n,TT_{m−1}}-free and
the non-neighbourhood is {I_{n−1},TT_m}-free, so k(n,m) ≤ 2k(n,m−1) + k(n−1,m) − 1
(k(2,6) = v(6) = 28).

The four witnesses k93, k54, k45, k36 are Cayley digraphs:
* k93: Cay(ℤ₆₀, {2,3,21,22,35,36,54,55});
* k54: Cay(ℤ₆₀, {4,7,8,11,17,20,21,22,24,32,34,35,45,54});
* k45: Cay(ℤ₇₁, {10,11,12,19,21,22,27,28,30,32,33,34,46,47,54,55,57,63,65,66,68,69});
* k36: Cay(ℤ₂₄ × ℤ₃, S) with |S| = 25, S listed in the file.

Each file records its connection set.

"Buildable" baselines are disjoint unions, blow-ups and substitutions of published
extremal graphs; they come from the 2026-09-26 adversarial priority audit, which
rebuilt and checked each one. (That audit also notes that Part G §5.2's "no lower
bound beyond 24" for k(6,3) is off by one: W₂₂ plus a directed 3-cycle has 25
vertices and independence number 5.)

Format: JSON `{"N": int, "a": n, "b": m, "arcs": [[u, v], ...]}`, arc u → v on
vertices 0..N−1. This is the format of Part G's `k34-scripts/verify_witness.py`.

## Replay

```sh
python3 kbounds-scripts/verify_bounds.py kbounds-certificates/*.json   # < 0.5 s for all nine
for f in kbounds-certificates/*.json; do python3 k34-scripts/verify_witness.py "$f"; done
```

Both checkers are standard-library Python.
* `verify_bounds.py` passes all nine files.
* Part G's brute-force `verify_witness.py` passes the first five in about 2 minutes (k83 dominates).
* It also passes the other four: k54 in 3 s, k45 in 8 s, k36 in 89 s and k93 in 8,198 s (all C(60,9) nine-subsets).

* **`verify_bounds.py`** computes two exact invariants by bitmask branch-and-bound:
  the independence number α and the order τ of the largest transitive subtournament.
  It passes a file iff α ≤ n − 1 and τ ≤ m − 1. Measured values: α = n − 1 and
  τ = m − 1 for every witness, so each bound is tight for its object.
  * It was cross-checked against brute-force subset enumeration on 600 random
    oriented graphs on 3–11 vertices, with 0 disagreements.
  * A first draft pruned the chain search against the wrong candidate set and
    under-reported τ. The cross-check caught this before any use.
  * Three tamper controls per witness are rejected: an injected independent
    n-set, an injected transitive m-tournament, and a 2-cycle.
* **Part G's `verify_witness.py`** tests every n-subset and every m-subset
  directly. Its criterion is the score sequence.

`verify_bounds.py` was written without reading the searchers' code or the
referees' checkers. Part G's `verify_witness.py` predates this campaign.

## SHA-256

```
c57037ac2a45fa70502beee6a472c16495ee855f7beec90c2d5ca51abe97bbbc  k63_N29.json
773aaa18ab4630f9d959617a6b471d3f170f91d74933ef932fe129a67701fbb7  k93_N60.json
2a6d13eb3d9f80d52207e57bbdec34c181792dab797091cb54b5a828563bc05e  k54_N60.json
97810955d303b6e176a28b3d760035ccdccf9634262640b53524a54ed8fe1377  k45_N71.json
3c8dc5150b6efd58093aa4724f14d78f9608a7afac49b0099b377e273a9911c3  k36_N72.json
42f6b3f624907602821e42c57601e311d9f3941bd6af1046e7903b11455801f4  k73_N38.json
73b58fcce089c13a090c21727106175d1424cfdbe5ff386b725481664920d840  k83_N46.json
e8980dd058834bc087b5f008a490e9de84ab921da2d70fb5301ed9b591d11c6c  k44_N39.json
ee7a4b9e0bbf387768df7aa4e81b0b205ace96c8a7f38ec28485c868dcbb623b  k35_N42.json
```

## How they were found (untrusted; irrelevant to validity)

* **k63_N29:** unstructured simulated annealing on all oriented graphs on 29
  labelled vertices. Cost = #TT₃ + #I₆, maintained incrementally; seed 201;
  zero cost reached after 2.4×10⁹ moves. The graph is irregular, with total
  degrees 8–10, so it is not vertex-transitive.
* **k73_N38, k83_N46:** CaDiCaL with lazily added independent-set clauses,
  over graphs invariant under a semiregular Z₁₉ or Z₂₃ with two orbits.
* **k44_N39, k35_N42:** Cayley-digraph SAT sweeps over every SmallGroups group
  of the relevant orders.
  * k44_N39 is the circulant Cay(ℤ₃₉, {11,15,17,19,25,27,29,30,33,34,38}).
  * k35_N42 is the circulant Cay(ℤ₄₂, {2,3,4,9,10,22,23,25,26,28,29,30,35,36}).

Negative search evidence (for example, no {I₆,TT₃}-free Cayley digraph on any
of the 51 groups of order 32) is solver output without proof logs. It is
recorded for the note, not claimed.
