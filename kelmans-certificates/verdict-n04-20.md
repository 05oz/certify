# REFEREE VERDICT — Problem 4 (Kelmans 1984, OPG-46613)

Verdict written 2026-08-06 after the q_ref20.jsonl referee queue completed (15/15 jobs,
rc=0 each per q_ref20.jsonl.state.jsonl). All outputs below were read in full by the
signing referee; decisive lines are quoted verbatim. Referee pipeline: `refcheck.c`
(independent C verifier — own graph6 decoder, union-find connectivity, precomputed
per-vertex triple tables, highest-vertex DFS branching, 4-way probed failure cache;
shares no code with attack-side `p3span.c`/`verify_cert.py`) and `refcert.py`
(fresh stdlib-only certificate checker with its own graph6 decoder, membership and
3-connectivity checks). Both were negative-controlled (see section 5).

## 1. Claim audited

Kelmans 1984 (Problem 1.10 of arXiv:0910.2766): every 3-connected cubic graph G has
lambda(G) = floor(v(G)/3) (a P3-packing avoiding at most 2 vertices), together with the
Theorem-3.1 strong forms — (z2),(z3),(z7),(z8) for n ≡ 0 mod 6; (t2) for n ≡ 2 mod 6;
(f1),(f2) for n ≡ 4 mod 6 — for ALL 3-connected cubic graphs on ≤ 20 vertices.
A failure of any strong form on any single graph would convert, via Kelmans' constructive
equivalences, into a counterexample to the base claim; none was found.

## 2. Per-level verdicts

### n ≤ 16 — CONFIRMED (all strong forms incl. z7 and f2)

Job `refsmall` re-ran the full generator stream for n = 4..16 through
`refcheck -strong -z7 -f2`. Summary lines, verbatim (out_ref/ref_small_n*.txt):

    RSUMMARY n=4 read=1 noncubic=0 conn3=1 basefail=0 sfail=0 rcerts=0
    RSUMMARY n=6 read=2 noncubic=0 conn3=2 basefail=0 sfail=0 rcerts=0
    RSUMMARY n=8 read=5 noncubic=0 conn3=4 basefail=0 sfail=0 rcerts=0
    RSUMMARY n=10 read=19 noncubic=0 conn3=14 basefail=0 sfail=0 rcerts=0
    RSUMMARY n=12 read=85 noncubic=0 conn3=57 basefail=0 sfail=0 rcerts=0
    RSUMMARY n=14 read=509 noncubic=0 conn3=341 basefail=0 sfail=0 rcerts=0
    RSUMMARY n=16 read=4060 noncubic=0 conn3=2828 basefail=0 sfail=0 rcerts=5

Connected-cubic counts 1,2,5,19,85,509,4060 = OEIS A002851; 3-connected counts
1,2,4,14,57,341,2828 match the attack side and McKay's published tables exactly.

### n = 18 — CONFIRMED (strong forms z2, z3, z7, z8)

Four geng slices (18 k/4, k=0..3) through `refcheck -strong -z7`. Verbatim
(out_ref/ref_n18_r0..r3.txt):

    RSUMMARY n=18 read=8460 noncubic=0 conn3=5827 basefail=0 sfail=0 rcerts=2
    RSUMMARY n=18 read=10926 noncubic=0 conn3=8469 basefail=0 sfail=0 rcerts=4
    RSUMMARY n=18 read=8677 noncubic=0 conn3=6146 basefail=0 sfail=0 rcerts=3
    RSUMMARY n=18 read=13238 noncubic=0 conn3=10026 basefail=0 sfail=0 rcerts=5

Sums: read = 41301 (= A002851(18)); conn3 = 5827+8469+6146+10026 = **30468** (= attack
count = McKay). basefail = sfail = 0 across all slices.

Certificate cross-check (job `refn18certs`, out_ref/ref_n18_certcheck.txt, verbatim):

       41301 out_ref/geng18.g6
    REFCERT-SUMMARY file=out/n18_strong.txt ok=30468 rejected=0 [membership checked]

i.e. ALL 30468 attack-side certificates (one per 3-connected graph) re-verified by the
referee's own checker, each g6 string confirmed a member of a fresh geng stream of
41301 graphs (line count independently re-confirmed by this referee: wc -l = 41301).

### n = 20 — CONFIRMED (base claim + strong form t2, the applicable one for n ≡ 2 mod 6)

Eight geng slices (20 k/8, k=0..7) through `refcheck -strong` (r6=2 branch: for every
edge xy of every graph, G−{x,y} must have a P3-factor). Verbatim summary lines
(out_ref/ref_n20_r0..r7.txt):

    RSUMMARY n=20 read=60454 noncubic=0 conn3=44476 basefail=0 sfail=0 rcerts=8
    RSUMMARY n=20 read=61314 noncubic=0 conn3=50617 basefail=0 sfail=0 rcerts=10
    RSUMMARY n=20 read=77286 noncubic=0 conn3=67345 basefail=0 sfail=0 rcerts=13
    RSUMMARY n=20 read=62960 noncubic=0 conn3=45188 basefail=0 sfail=0 rcerts=9
    RSUMMARY n=20 read=58933 noncubic=0 conn3=46550 basefail=0 sfail=0 rcerts=9
    RSUMMARY n=20 read=59995 noncubic=0 conn3=49951 basefail=0 sfail=0 rcerts=9
    RSUMMARY n=20 read=61992 noncubic=0 conn3=50288 basefail=0 sfail=0 rcerts=10
    RSUMMARY n=20 read=67555 noncubic=0 conn3=41735 basefail=0 sfail=0 rcerts=8

Sums (recomputed mechanically by this referee, awk over the RSUMMARY lines):
read = 60454+61314+77286+62960+58933+59995+61992+67555 = **510489** = A002851(20);
conn3 = 44476+50617+67345+45188+46550+49951+50288+41735 = **396150** — exactly the
target count, equal to the attack side's and to McKay's published table.
basefail = 0 and sfail = 0 on every slice; a grep for "FAIL" over every main referee
output returns 0 matches in every file.

Certificate cross-check (job `refn20certs`, out_ref/ref_n20_certcheck.txt, verbatim):

      510489 out_ref/geng20.g6
    REFCERT-SUMMARY file=out/n20_strong.txt ok=3961 rejected=0 [membership checked] [3-connectivity checked]

All 3961 attack-side sampled certificates (every 100th 3-connected graph, per the
declared n=20 certificate policy) re-verified, with g6-membership in a fresh 510489-line
geng stream AND per-graph 3-connectivity re-proved by the referee's own code. The
geng20.g6 line count was independently re-run by this referee: wc -l = 510489.
(Full n=20 coverage rests on the referee's independent re-solve of all 396150 graphs
above, not on the sampled certificates; certificates are complete through n = 18.)

## 3. Count ledger (referee vs. attack vs. literature)

| n  | connected cubic (read) | A002851 | 3-connected (referee) | attack | McKay |
|----|--------|--------|--------|--------|--------|
| 4  | 1      | 1      | 1      | 1      | —      |
| 6  | 2      | 2      | 2      | 2      | —      |
| 8  | 5      | 5      | 4      | 4      | —      |
| 10 | 19     | 19     | 14     | 14     | 14     |
| 12 | 85     | 85     | 57     | 57     | 57     |
| 14 | 509    | 509    | 341    | 341    | 341    |
| 16 | 4060   | 4060   | 2828   | 2828   | 2828   |
| 18 | 41301  | 41301  | 30468  | 30468  | 30468  |
| 20 | 510489 | 510489 | 396150 | 396150 | 396150 |

Every cell agrees. Zero property failures (basefail = sfail = 0) at every order.

## 4. What each of the 15 jobs checked (q_ref20.jsonl)

1. `refsmall` — n=4..16 full streams, `-strong -z7 -f2` (ALL strong forms). PASS.
2-5. `refn18r0..r3` — n=18 in 4 geng slices, `-strong -z7` (z2,z3,z7,z8). PASS.
6-13. `refn20r0..r7` — n=20 in 8 geng slices, `-strong` (base + t2). PASS.
14. `refn18certs` — fresh geng 18 stream + refcert.py over ALL attack n=18 certs
    with membership check. PASS (ok=30468 rejected=0).
15. `refn20certs` — fresh geng 20 stream + refcert.py over all sampled attack n=20
    certs with membership + 3-connectivity checks. PASS (ok=3961 rejected=0).

## 5. Negative controls (the failure paths demonstrably work)

The sweep only ever reports success, so both referee tools were forced to fail:

- `refcheck -skip3c` base sweep over CONNECTED cubic n=10..16
  (out_ref/ref_negctl_base.txt) finds exactly one base failure, verbatim:

      BASEFAIL O???E?oBEAWOKGK_@o?W_
      RSUMMARY n=16 read=4060 noncubic=0 conn3=4060 basefail=1 sfail=0 rcerts=0

  This is the SAME 1-connected n=16 graph the attack side independently identified in
  its own negative control (NOTES.md) — the two independent pipelines agree on the
  unique sub-3-connected failure in this range, and the referee's failure path fires.
- `refcheck -skip3c -strong -z7 -f2` (out_ref/ref_negctl_strong.txt): strong-form
  failure paths fire on non-3-connected graphs — 54 F1/F2 failures at n=10, 253
  Z8-type failures at n=12, 145 T2 failures at n=14 (samples quoted in file, e.g.
  "T2FAIL xy=6-9 M??CEB@W_sE_J?F??"), and 0 at n=8 where none exist.
- `refcert.py` on 6 doctored lines (out_ref/ref_negctl_certs_input.txt): the 5
  corruptions (non-path triple, cover gap, overlapping triple, overlong avoided list,
  non-member g6) are ALL rejected with the correct reasons and exit code 1; the one
  intact line is accepted. Verbatim (out_ref/ref_negctl_certs.txt):

      REFCERT-SUMMARY file=out_ref/ref_negctl_certs_input.txt ok=1 rejected=5 [membership checked] [3-connectivity checked]
      refcert exit: 1

## 6. VERDICT

**CONFIRMED at exactly this strength:** Kelmans' 1984 claim (P) — every 3-connected
cubic graph on n vertices has a P3-packing covering all but (n mod 3) vertices — holds
for ALL 3-connected cubic graphs on n ≤ 20 vertices, together with the applicable
Theorem-3.1 strong forms at every order: (z2),(z3),(z7),(z8) at n = 6,12,18;
(t2) at n = 8,14,20; (f1),(f2) at n = 4,10,16. Two independently written pipelines
(attack: p3span.c + verify_cert.py; referee: refcheck.c + refcert.py, no shared code,
different algorithms, both negative-controlled) agree on every count and report zero
failures over all 429,865 3-connected cubic graphs with 4 ≤ n ≤ 20. Counts match
OEIS A002851 and McKay's published 3-connected cubic enumeration exactly.
Machine-checkable P3-factor certificates exist for every graph through n = 18
(all independently re-verified) and for every 100th graph at n = 20 (all 3961
independently re-verified with membership + 3-connectivity).

To our knowledge (novelty sweeps 2026-08-05, NOTES.md) this is the FIRST recorded
computational verification of Kelmans' 1984 problem at any order.

**Confirmed boundary: n ≤ 20 and nothing more.** n = 22 (f1 strong form) and n = 24
(Λ-factor case) are still computing in q.jsonl and are NOT covered by this verdict.

— adversarial referee, 2026-08-06
