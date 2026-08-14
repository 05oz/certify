# Part J certificates — non-uniqueness of the k(3,4)=21 extremal graph

Thirteen 20-vertex oriented graphs, each free of `I_3` and `TT_4`, pairwise
non-isomorphic, and rigid (`|Aut| = 1`). Together they answer Question 8.1 of
Part G (`k34-paper/`, version DOI 10.5281/zenodo.21890619) in the negative: the
20-vertex extremal graph for `k(3,4) = r(I_3,L_4) = 21` is **not** unique.

## Files

Each `w*.json` is `{"N":20,"a":3,"b":4,"arcs":[[u,v],...]}`, meaning arc `u->v`.
`w01_W.json` is exactly the witness `W` of Part G, Table 1 (verified equal to
its out-neighbourhoods). `w02`–`w13` are twelve further free graphs.

| file | arcs | Nbar-degree sequence | #{s=7} = #QR_7 blocks |
|------|-----:|----------------------|----------------------:|
| w01_W | 126 | 7^11 6^6 5^3 | 11 |
| w02   | 125 | 7^12 6^6 5^2 | 12 |
| w03   | 128 | 7^6 6^12 5^2 | 6 |
| w04   | 125 | 7^12 6^6 5^2 | 12 |
| w05   | 126 | 7^11 6^6 5^3 | 11 |
| w06   | 123 | 7^14 6^6     | 14 |
| w07   | 126 | 7^9 6^10 5^1 | 9 |
| w08   | 126 | 7^12 6^4 5^4 | 12 |
| w09   | 124 | 7^14 6^4 5^2 | 14 |
| w10   | 127 | 7^8 6^10 5^2 | 8 |
| w11   | 124 | 7^13 6^6 5^1 | 13 |
| w12   | 125 | 7^13 6^4 5^3 | 13 |
| w13   | 125 | 7^11 6^8 5^1 | 11 |

The invariant triple (arcs, Nbar-degree sequence, #QR_7 blocks) does not by
itself separate all thirteen -- w1 and w5 agree in all three entries, as do w2
and w4, and the third entry is determined by the second. The canonical forms
and the richer fingerprint the checker computes do separate them.

## SHA-256

```
51890f9913fa60acbff07be1a526a747a2163782586b3371262d46edd51bf3af  w01_W.json
a1d142784faa669d3e51474a83f102c8a2f3dfd529b99233b25a665d8f41fef5  w02.json
db8c76b102fa95ab6a7a9f1cb6730536e39b98517bd91eafda95f673790fec8f  w03.json
da8009bcd4c75fd9268146621122a4080eecd5f3ea91422693bb0e74fa1897b3  w04.json
8c22b85571f0b0f63eca0415adc8cd69bce923a98372af671ae2ae5366ebd576  w05.json
a42a71428e67e5b3c7c7f8214d4dd838a61520587f8f5f44e1376dddc801d430  w06.json
59649ded6f1e65e195f7564c9a98af15b04e55b77dbf583ec722f963f474457a  w07.json
39cd1bcdf9e75609f69ebf1d690c50ad145319064c949417a8aa694b2afd5727  w08.json
a1375884049da075be8845b282845dbbbbc7c5a46580a61b6d8cdcbffa9207ec  w09.json
9188d0331a133b7c490f96ccd8618fc0ef47757ebb202f171cbe127ee329dc7a  w10.json
06e4dbe2c6b9d3b1f56fad2d40ee9cf24fd60463fa13221b4543bc9ee3fb14de  w11.json
63e44730737fe3fe4861836a9eca996ce59a66b01aac5d048f74a4bb09746d89  w12.json
928307a06e98664590d270e0bc61e0e106e8a721bb3e055446b3ab1474801239  w13.json
```

## Replay

```
python3 ../k34add-scripts/verify_witnesses.py     # 13 free, rigid, pairwise non-iso
python3 ../k34add-scripts/verify_qr7_lemma.py      # unique 7-vtx TT4-free tournament = QR_7
python3 ../k34add-scripts/blowup_bound.py          # QR_7[I_2] on 14 vertices, gap 6
```

Each prints `PASS` and exits 0. The checkers import only the Python standard
library and share only boilerplate with the SAT search, but are NOT
code-independent of the private structure-mining dig (`hunt-structure/`): 24, 30
and 9 of their 115, 174 and 51 executable lines are verbatim from it, `tour_iso`
and `qr7` among them. They were run on CPython 3.14.2 and 3.9.6 (identical
verdicts).

## Verdict (2026-08-11)

- `verify_witnesses.py`: PASS. All 13 valid oriented graphs; each exhaustively
  `{I_3,TT_4}`-free over all C(20,3)=1140 triples and C(20,4)=4845 quadruples;
  each rigid (Weisfeiler–Leman refinement discrete at 20 colours, and explicit
  automorphism count = 1); all 78 pairs non-isomorphic (distinct canonical
  forms; distinct invariant fingerprints).
- `verify_qr7_lemma.py`: PASS. 240 labelled TT_4-free tournaments on 7 vertices,
  all isomorphic to QR_7 = Cay(Z_7,{1,2,4}); 0 on 8 vertices; |Aut(QR_7)| = 21;
  240 = 7!/21.
- `blowup_bound.py`: PASS. QR_7[I_2] free on 14 vertices; QR_7[I_3] contains an
  I_3.

## Code independence, measured routine by routine (2026-08-14)

This section carries the full measurement text of the v0.15.0 independence round. It was
moved here verbatim from the front matter of `k34add-paper/note.tex`, where a 1,010-word
methods footnote in a five-page paper broke PROTOCOL §11 rule 1 (computation files live in
the repository, not the paper). Nothing was re-derived in the move and no figure changed;
the paper keeps the disclosure and the conclusion, and points here for the numbers.

### Against the SAT search that produced the original witness: boilerplate only

Of the 115, 174 and 51 executable lines of `verify_qr7_lemma.py`, `verify_witnesses.py`
and `blowup_bound.py`, the lines also present anywhere in the 24 Python files of that
search number 25, 32 and 11, and every one is a one-line `return`, a `continue`, an
`else:`, a loop header, `def main():`, `if ok:`, `ok = True`, a counter initialisation or
increment, `from collections import Counter`, `if __name__ == "__main__":` or
`sys.exit(main())`. No routine there is structurally identical to one in a checker, and
the longest run of consecutive shared lines is three: in `verify_qr7_lemma.py` and
`verify_witnesses.py` that run is `return 1` followed by the closing main guard, and
`blowup_bound.py` has one further run, `return False`, `return True`, `def main():`.

### Against the private structure-mining dig (`hunt-structure/`): not code-independent

They are not code-independent of the private structure-mining scripts in
`hunt-structure/`, which produced the twelve alternative witnesses. Measured against the
six Python files there, 24 of the 115 executable lines of `verify_qr7_lemma.py` appear
verbatim up to indentation, 30 of the 174 of `verify_witnesses.py`, and 9 of the 51 of
`blowup_bound.py`. Those counts understate the sharing, and the longest identical run of
consecutive lines between the two sets — two lines — understates it further: the private
originals are written in a compressed style with several statements to the line and the
public files are PEP8-expanded, so run length here measures reformatting rather than
independence.

At the level of whole routines the correspondence is exact. The tournament-isomorphism
test `tour_iso` carries the same name in both and has, after systematic renaming, an
abstract syntax tree identical to the private one, with all eighteen of its identifiers
preserved — including the unusual pair `oa`, `ob` — and its load-bearing predicate
`all(A[i][k] == B[j][perm[k]] and A[k][i] == B[perm[k]][j] for k in range(i))` identical
token for token. Its inner backtracker, the QR_7 construction `qr7`, the adjacency
predicate `adj`, the backtracker inside `aut_count`, and the backtracker inside `iso` are
identical in the same sense. The predicates `i3_free` and `tt4_free`, the relation
accessor `rel` and the loader `load` differ from their nearest private counterparts only
in parameter lists, in what they return, or in the order of the two operands of a single
`!=` comparison. A passing check may therefore not be read, on its own, as an independent
re-derivation of the isomorphism tests, of the QR_7 construction, or of the
pattern-freeness predicates.

### Routine by routine, `verify_qr7_lemma.py`

The sharing is not confined to the isomorphism tests, and the disclosure has to say so
routine by routine. `verify_qr7_lemma.py` prints PASS only if all of the following hold
together: QR_7 is TT_4-free and 3-regular; the labelled TT_4-free tournaments on 7
vertices number 240; |Aut(QR_7)| = 21; 7!/|Aut(QR_7)| = 240; there are none on 8 vertices;
and the enumerated 240 are all isomorphic to QR_7. `qr7`, which builds the matrix all six
are computed about, is the private `qr7_canon` under two renamings, the function name and
the matrix variable. The last conjunct is computed by the shared `tour_iso`.

Of the remaining four routines, two more are partly private in origin: the TT_4-detection
kernel — the statement `outs = sorted(sum(1 for y in four if y != x and M[x][y]) for x in
four)` together with the test `if outs == [0, 1, 2, 3]:` — is the private kernel with the
two operands of the `!=` transposed, and it appears both in the detector `has_tt4` and in
the enumerator's extension test `new_vertex_ok`, matching three separate private sites;
and the backtracking loop of the automorphism counter `aut_count_tour` follows the private
`aut_count`'s statement for statement — the same `used[j]`-or-prune guard, the same
`ok(i, j)` gate, the same order of assigning and undoing `perm[i]` and `used[j]` —
differing only in the pruning key, out-degree here and refined colour there; it is not
alpha-equivalent to it. What is original to this file is the enumeration scaffold itself —
the vertex-by-vertex mask recursion that prunes on the freshly completed vertex only,
which shares one of its nineteen lines with the private tree — and the 3-regularity test.
No part of this checker may be read as an independent re-derivation of the tournament
facts.

### Why the uniqueness conclusion survives it

The uniqueness conclusion nevertheless does not need the isomorphism test at all, and that
much a reader can check on paper. By orbit-stabilizer the labelled tournaments isomorphic
to QR_7 number 7!/|Aut(QR_7)| = 240; every one of them is TT_4-free because QR_7 is; so
they exhaust the 240 that were enumerated, and every 7-vertex TT_4-free tournament is
isomorphic to QR_7. The `tour_iso` sweep is a sixth check of what the counts have already
established, so a `tour_iso` returning a spurious `True` — the unsafe direction, and the
one a routine shared with the dig could carry silently — cannot change the verdict. The
counts themselves, however, come from code that is not independent of the dig, and no
separate re-implementation of them is deposited.

### The thirteen witnesses

For the thirteen witnesses the same distinction applies. Rigidity is certified twice and
the two certificates are not equally affected: the automorphism backtracker is the private
routine, while the Weisfeiler–Leman refinement that supplies its colours is not —
`wl_colours` shares none of its 17 executable lines with the private tree and is
alpha-equivalent to nothing in it — and a refinement discrete at twenty singleton colours
already forces |Aut| = 1 on its own. The canonical form is original too, and of the
invariant fingerprint only the `nbar` term matches a private expression, and that only up
to the loop bound. The shared isomorphism backtracker is never reached on the shipped
certificates: it is invoked only when two canonical forms collide, and the thirteen
canonical forms are distinct. That covers the computational content of this part. It does
not make the thirteen a complete list: the extremal count remains a lower bound, as Part J
§6 states.

### How to re-derive these counts

Executable lines are non-blank, non-comment lines with docstring line spans excluded,
compared after stripping whitespace. Run lengths are spans of consecutive physical lines.
See `CORRECTIONS.md`, "How to re-derive the counts in this round".

## Scope

The result is a **lower bound**: at least 13 pairwise non-isomorphic rigid
extremal graphs. The exact number is not determined here. Whether every free
graph on 20 vertices must carry a QR_7 block (equivalently, must have a vertex
with exactly 7 non-neighbours) is left open; see Part J, §6.
