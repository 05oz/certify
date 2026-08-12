# Part I — replay, regenerate, and the exact commands

Kelmans' 1984 problem on 3-vertex path packings in cubic 3-connected graphs
(paper: [`kelmans-paper/note.pdf`](../kelmans-paper/note.pdf)).

Everything below runs on a laptop. Checking the certificate corpus needs **only CPython**
(no third-party packages, no compiler, no network). Regenerating the graph streams needs
`geng` from [`nauty`](https://users.cecs.anu.edu.au/~bdm/nauty/) 2.9.3.

---

## 1. Check the certificates (no compiler, no generator, ~1 minute)

Two checkers ship, written independently of each other and of the searchers; they share no
code and use different graph6 decoders, different adjacency representations and different
rejection orders.

```bash
# checker A: verifies packing shape AND lambda(G) = floor(n/3), 3-connectivity on by default
python3 kelmans-scripts/verify_cert.py \
    kelmans-certificates/certs_n04-16.txt \
    kelmans-certificates/certs_n18.txt \
    kelmans-certificates/certs_n20.txt \
    kelmans-certificates/certs_n22.txt
# -> VERIFIED 43580 certificates (43580 distinct graphs) by order:
#    [(4,1),(6,2),(8,4),(10,14),(12,57),(14,341),(16,2828),(18,30468),(20,3961),(22,5904)]

python3 kelmans-scripts/verify_cert.py kelmans-certificates/certs_n24.txt
# -> VERIFIED 9776 certificates (9776 distinct graphs) by order: [(24, 9776)]

# checker B, independent: same corpus, different code
for n in 18 20 22 24; do
  python3 kelmans-scripts/refcert.py kelmans-certificates/certs_n$n.txt --n $n --check3c
done
python3 kelmans-scripts/refcert.py kelmans-certificates/certs_n04-16.txt --check3c
# -> REFCERT-SUMMARY ... ok={30468,3961,5904,9776,3247} rejected=0 [3-connectivity checked]
```

Both exit 0 on success and nonzero on the first violation. Every one of the 53,356
certificates in this directory passes both.

`refcert.py` additionally checks membership of each graph6 string in a reference generator
stream, which no other gate can catch (see §4):

```bash
/opt/homebrew/bin/geng -q -c -d3 -D3 18 > /tmp/geng18.g6         # 41301 lines
python3 kelmans-scripts/refcert.py kelmans-certificates/certs_n18.txt \
        --n 18 --g6set /tmp/geng18.g6 --check3c
# -> REFCERT-SUMMARY ... ok=30468 rejected=0 [membership checked] [3-connectivity checked]
```

## 2. What a certificate line says

```
CERT <graph6> | <a-b-c> <a-b-c> ... | <avoided vertices>
```

Everything is re-derived from the graph6 string alone: the checker decodes it with its own
decoder, verifies the graph is simple and cubic, re-proves 3-connectivity by deleting every
vertex and every vertex pair and testing connectivity, checks that each listed triple is a
path of the graph, and checks that the triples and the avoided vertices partition the
vertex set with `|avoided| = n mod 3`. A reader who trusts nothing but the graph6 format
can check any line by hand.

Example (order 22, the line printed in §2.3 of the paper; it is line 1 of `certs_n22.txt`):

```
CERT U???????C?W?[?Y?C`Cc?Aa?X??BG?I_?Ao?@K?? | 10-0-11 12-1-13 2-14-5 15-3-17 4-16-6 18-7-19 20-8-21 | 9
```

## 3. Regenerate the graph streams

Each order was swept over the output of

```bash
geng -q -c -d3 -D3 <n>            # all connected cubic graphs on n vertices
geng -q -c -d3 -D3 <n> <res>/<mod>   # one generator slice (large orders)
```

The 3-connectivity filter is each pipeline's own; no symmetry reduction beyond `geng`'s
isomorph rejection was used at any stage. The generated counts are in
[`summaries/search-pipeline.txt`](summaries/search-pipeline.txt) (search side) and
[`summaries/referee-pipeline.txt`](summaries/referee-pipeline.txt) (independent recount);
they match OEIS A002851 and A204198 at every order.

Slicing used per order: n = 18 in 4 slices (referee) or one run (search); n = 20 and n = 22
in 8 slices; n = 24 in 60 slices.

The filter itself is reproducible from the shipped checker's own 3-connectivity routine:

```bash
for n in 8 10 12 14 16; do
  /opt/homebrew/bin/geng -q -c -d3 -D3 $n | python3 kelmans-scripts/count3conn.py
done
# total=5    cubic=5    threeconn=4
# total=19   cubic=19   threeconn=14
# total=85   cubic=85   threeconn=57
# total=509  cubic=509  threeconn=341
# total=4060 cubic=4060 threeconn=2828
```

## 4. The negative controls

A sweep that only ever reports success proves nothing about its own failure path.

**Certificate checkers.** `controls/ctl_certs_2026-08-11_input.txt` is one genuine order-18
certificate (line 1) followed by eight lines, each doctored to trip a different gate;
`controls/ctl_certs_2026-08-11_manifest.txt` names them. Rebuild it from any genuine
certificate file with

```bash
python3 kelmans-scripts/mkcontrols.py kelmans-certificates/certs_n18.txt /tmp/ctl.txt
```

(the ninth line — a genuine Λ-factor certificate for a connected cubic graph that is *not*
3-connected, and which *is* in the `geng` stream, so only the 3-connectivity gate can reject
it — is appended by hand; it is line 9 of the shipped file and can be copied from there).
Then

```bash
/opt/homebrew/bin/geng -q -c -d3 -D3 18 > /tmp/geng18.g6
python3 kelmans-scripts/refcert.py kelmans-certificates/controls/ctl_certs_2026-08-11_input.txt \
        --n 18 --g6set /tmp/geng18.g6 --check3c
# -> 8 REJECT lines, one per gate; ok=1 rejected=8; exit 1
```

Recorded outputs, including the two controls-on-the-controls (dropping `--g6set` admits the
non-canonical relabelling and nothing else; dropping `--check3c` admits the sub-3-connected
certificate and nothing else):
[`controls/ctl_certs_2026-08-11_refcert.txt`](controls/ctl_certs_2026-08-11_refcert.txt) and
[`controls/ctl_certs_2026-08-11_verifycert.txt`](controls/ctl_certs_2026-08-11_verifycert.txt).
`verify_cert.py` exits on the first violation, so it is run one line at a time there.

**Searchers.** With the 3-connectivity filter disabled, the sweep over all *connected* cubic
graphs finds exactly one base-claim failure at orders 10–16 — the 16-vertex graph
`O???E?oBEAWOKGK_@o?W_`, which has cut vertices {6, 11, 13, 14} and λ = 4 < 5 — and the
strong-form paths fire with the per-type breakdown recorded in
[`controls/ctl_base_strong_2026-08-11.txt`](controls/ctl_base_strong_2026-08-11.txt)
(order 8: none; 10: 2 (f1) + 52 (f2); 12: 4 (z2) + 8 (z3) + 106 (z7) + 135 (z8);
14: 145 (t2); 16: 317 (f1) + 15,374 (f2)). Reproducing those numbers needs the searcher
binaries, which are not part of this deposit; the outputs are shipped verbatim so the
figures quoted in the paper can be read off the record.

## 5. What is NOT in this deposit

The two searchers (`p3span.c`, `refcheck.c`) are specified in §2.2 of the paper but are not
deposited. Consequence, stated plainly: from this deposit a reader can re-check **every
positive answer the searchers gave** — that is what the 53,356 certificates are — and can
reproduce the enumeration counts, but cannot re-run a sweep to re-derive the absence of
failures. That absence rests on the per-slice summaries and the independent recount, both
shipped here, and on the referee's verdict records
([`verdict-n04-20.md`](verdict-n04-20.md), [`verdict-n22-24.md`](verdict-n22-24.md)).

Order 24 has **no independent recount** (`q_ref24.jsonl` was written and never run) and is
reported at search-side-complete strength only, in the paper and in the verdict record.

## 6. Inventory and hashes (SHA-256)

```
d46b5d21a50fb616630c2beebd5c9442173a187f83651085faa5493206f07e7a  certs_n04-16.txt          3,247 certificates, orders 4-16
8d8dd8a9c16d261e6e524c7f7ef1846b906f0a20c7b09807321db9b80c1caa8a  certs_n18.txt            30,468 certificates, every 3-connected cubic graph on 18 vertices
ac72101acae251f8d470a92fad9e3926f8da8d51abdeb60edb4a26267c66e3ea  certs_n20.txt             3,961 certificates, every 100th graph
d3ab4d6724a5b7cc1e4e99364b123adbebbe9543a4c8582678f9fb642057a651  certs_n22.txt             5,904 certificates, every 1000th graph per slice
f2e9f006dd9904074144165d85b88b1a1e237a4507f39c2b18e06197277d25d9  certs_n24.txt             9,776 certificates, every 10000th graph per slice
67cba957116bb4446a3b6c53e519531eb568e84f325c0ca27d88eb8d65beb5f4  controls/ctl_base_strong_2026-08-11.txt
24effde5d971c4d1b98139d5f61f8cae952a28aaecf44d070471a70b1e91202c  controls/ctl_certs_2026-08-11_input.txt
e143308a80e0433298700a4639b3b712a84d6e4b0c5aadb3bd2500481ba94613  controls/ctl_certs_2026-08-11_manifest.txt
3c0ea99bcd25e7f174d811c0b1afdb5dea187fdc09d4bc4574a4ef266a5d758c  controls/ctl_certs_2026-08-11_refcert.txt
58b46f50c792449bf8864a996af2e76a51768236718103f929246ab8d74f93f9  controls/ctl_certs_2026-08-11_verifycert.txt
54eaed58f7fa11e59272ea62cdb67959526434ea3ccc70580250e455595e257a  summaries/referee-pipeline.txt
5e4b99caaddd6ebba67d24b21dc05292cd49ebd9a8a3d56436d52b86ddbf876c  summaries/search-pipeline.txt
a1f1b22434d88b2192b11da05510484f5bf6054ae02940701c2637f6b524bfbb  ../kelmans-scripts/count3conn.py
7f56caf08449a3f7c4a797a557a22deaf58b00b12699f6dd12145b794559ded8  ../kelmans-scripts/mkcontrols.py
d4c159172d0302b48cecaf58198e9efcbac122be6945ead314b264813d9d1320  ../kelmans-scripts/refcert.py
81d37968db7eb47f4cfc44a01932dc29992842a712b713aa8063911e57df05c6  ../kelmans-scripts/verify_cert.py
```

Re-hash with `shasum -a 256 certs_n*.txt controls/*.txt summaries/*.txt`.

## 7. Portability

Both checkers import only the Python standard library (`sys`, and `gzip` in `verify_cert.py`
for optional `.gz` input). No signals, subprocesses, threads, network, wall-clock,
filesystem assumptions, locale dependence or recursion. Verified on macOS system CPython
3.9.6 and on 3.14.2.
