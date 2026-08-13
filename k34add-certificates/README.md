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
library, share no code with the search that produced the witnesses, and were
run on CPython 3.14.2 and 3.9.6 (identical verdicts).

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

## Scope

The result is a **lower bound**: at least 13 pairwise non-isomorphic rigid
extremal graphs. The exact number is not determined here. Whether every free
graph on 20 vertices must carry a QR_7 block (equivalently, must have a vertex
with exactly 7 non-neighbours) is left open; see Part J, §6.
