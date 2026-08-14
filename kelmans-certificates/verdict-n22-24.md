# REFEREE VERDICT — Problem 4 extension to n = 22, 24 (Kelmans 1984, OPG-46613)

Verdict opened 2026-08-11 (incremental; sections are dated as they are closed).
Extends REFEREE-VERDICT.md (n <= 20, signed 2026-08-06). Same referee pipeline:
`refcheck.c` + `refcert.py`. `refcheck.c` shares no code with the attack side `p3span.c` —
their function inventories are disjoint apart from `main` — and the independent recount at
n = 22 rests on that C binary's own union-find re-derivation of 3-connectivity over all
7,319,447 generated graphs. The two Python certificate checkers `refcert.py` and
`verify_cert.py` do NOT satisfy that condition: they share a 3-connectivity routine
(`connected_after_removing` and its caller, the same code under local renaming), so the
certificate-side 3-connectivity gate is **not** independent of the attack side and must not
be read as such. See section 6.
Negative-controlled again TODAY (section 4). Machine rules: all heavy runs via
jobrunner on NEW queues `q_ref22.jsonl` / `q_ref24.jsonl`, --workers 1, mem_mb 2500.

## 1. Attack-side completeness at n = 22 and n = 24 — VERIFIED 2026-08-11

The attack sweeps ran across three queues: `q.jsonl` (original, 70 jobs), `q24b.jsonl`
(25 retries of q.jsonl timeouts, timeout 5400), `q24c.jsonl` (3 retries of q24b
timeouts, timeout 18000). I reconstructed the final status of every job id by replaying
all three state files in order (last record per id wins, later queue supersedes earlier):

- All 8 n=22 jobs (n22r0..r7) and all 60 n=24 jobs (n24r0..r59) are present and
  their FINAL attempt is `status=done, rc=0`. Checked mechanically (python over the
  three `*.state.jsonl` files): "ALL n22+n24 jobs finally done rc=0".
- Slices that timed out earlier (25 in q.jsonl, of which 3 timed out again in q24b:
  n24r40, n24r42, n24r48) had their `out/n24_r*.txt` overwritten by the completing
  rerun via `>` redirection, so every surviving output file is from a complete run.
- Zero failure lines anywhere: `grep -l FAIL out/n22_r*.txt out/n24_r*.txt` -> 0 files;
  `grep -rl FAIL q.jsonl.logs q24b.jsonl.logs q24c.jsonl.logs` -> 0 files.
  (This covers FAIL / SFAIL / BASEFAIL — p3span failure lines all contain "FAIL".)

Final per-slice SUMMARY lines (from the .err log of each job's completing queue).
n=22 (p3span `-strong` = base + f1, cert every 1000th), verbatim:

    SUMMARY read=518580 cubic=518580 conn3=424804 basefail=0 sfail=0 certs=424
    SUMMARY read=670736 cubic=670736 conn3=458412 basefail=0 sfail=0 certs=458
    SUMMARY read=982556 cubic=982556 conn3=765759 basefail=0 sfail=0 certs=765
    SUMMARY read=1068280 cubic=1068280 conn3=886684 basefail=0 sfail=0 certs=886
    SUMMARY read=1569040 cubic=1569040 conn3=1408573 basefail=0 sfail=0 certs=1408
    SUMMARY read=879959 cubic=879959 conn3=693971 basefail=0 sfail=0 certs=693
    SUMMARY read=978267 cubic=978267 conn3=699819 basefail=0 sfail=0 certs=699
    SUMMARY read=652029 cubic=652029 conn3=571270 basefail=0 sfail=0 certs=571

n=22 totals: read = 7319447, conn3 = 5909292, basefail = 0, sfail = 0, certs = 5904
(5904 CERT lines counted directly in out/n22_r*.txt — matches).

n=24 (p3span base claim = Λ-factor, cert every 10000th): 60 SUMMARY lines, all with
basefail=0 sfail=0 (three representative lines, verbatim — full set in the
aggregation transcript and the .err logs):

    SUMMARY read=1807860 cubic=1807860 conn3=1663561 basefail=0 sfail=0 certs=166   (n24r0, q.jsonl)
    SUMMARY read=2469195 cubic=2469195 conn3=1865041 basefail=0 sfail=0 certs=186   (n24r40, q24c.jsonl)
    SUMMARY read=2297761 cubic=2297761 conn3=2069953 basefail=0 sfail=0 certs=206   (n24r58, q24b.jsonl)

n=24 totals: read = 117940535, conn3 = 98101019, basefail = 0, sfail = 0,
certs = 9776 (9776 CERT lines counted directly in out/n24_r*.txt — matches).

### Cross-check against published enumeration (fetched and read 2026-08-11)

Connected cubic totals — Brinkmann, Goedgebeur, McKay, "Generation of Cubic graphs",
DMTCS vol. 13:2 (2011), 69-80, Table 1 ("Number of prime graphs vs. number of cubic
graphs"), read from the publisher's PDF: |V(G)| = 22 -> "7 319 447";
|V(G)| = 24 -> "117 940 535". Same values as OEIS A002851(11), A002851(12).
Our read sums: 7319447 and 117940535 — EXACT match.

3-connected cubic counts — OEIS A204198 "Number of (strictly) 3-connected cubic
graphs on 2n nodes", terms quoted verbatim from oeis.org (fetched 2026-08-11):

    0, 1, 2, 4, 14, 57, 341, 2828, 30468, 396150, 5909292, 98101019, 1782392646, 35085504243

i.e. a(11) = 5909292 (22 vertices), a(12) = 98101019 (24 vertices); extension credit
line on the entry: "a(11)-a(14) from Ed Wynn, Jul 22 2023". Our conn3 sums:
5909292 and 98101019 — EXACT match. (A204198 cites McKay-Royle and snarkhunter.
Of the n<=20 prefix 1,2,4,14,57,341,2828,30468,396150, the six orders n = 10 through
20 — 14, 57, 341, 2828, 30468, 396150 — are the ones the n<=20 verdict checked against
McKay's published counts; n = 4, 6 and 8 have no McKay value in that ledger and rest on
A204198 and the two pipelines only.)

Attack-side completeness: CONFIRMED. Every connected cubic graph on 22 and 24
vertices was generated (counts match the published enumeration exactly), the
3-connected filter kept exactly the published number of 3-connected ones, and the
attack solver reported zero base failures and zero strong-form (f1) failures.

## 2. Referee recount, n = 22 (refcheck -strong = base + f1, 8 geng slices) — CLOSED 2026-08-11

Provenance of this section, stated plainly: the recount itself is the referee's — its queue
(`q_ref22.jsonl`), its binary (`refcheck.c`, no code shared with `p3span.c`), its outputs
(`out_ref/ref_n22_r*.txt`). The section was written and closed on 2026-08-11 by the
pre-release fix pass, which recomputed every figure below mechanically from those artifacts
rather than copying any reported total. Nothing here was re-run on the attack side.

Job accounting, replayed from `q_ref22.jsonl.state.jsonl` (last record per id wins):
all 9 jobs — `refn22r0` … `refn22r7` and `refn22certs` — have final `status=done`.
`jobrunner.py` rewrites `done` to `failed`/`oom` whenever `rc != 0`, so `done` is exactly
`rc = 0`; `refn22certs` was started twice (the first attempt was interrupted, see
`q_ref22.restart.log`) and completed on the second. No job id is missing.

Per-slice RSUMMARY lines, verbatim from `out_ref/ref_n22_r{0..7}.txt`:

    RSUMMARY n=22 read=518580 noncubic=0 conn3=424804 basefail=0 sfail=0 rcerts=42
    RSUMMARY n=22 read=670736 noncubic=0 conn3=458412 basefail=0 sfail=0 rcerts=45
    RSUMMARY n=22 read=982556 noncubic=0 conn3=765759 basefail=0 sfail=0 rcerts=76
    RSUMMARY n=22 read=1068280 noncubic=0 conn3=886684 basefail=0 sfail=0 rcerts=88
    RSUMMARY n=22 read=1569040 noncubic=0 conn3=1408573 basefail=0 sfail=0 rcerts=140
    RSUMMARY n=22 read=879959 noncubic=0 conn3=693971 basefail=0 sfail=0 rcerts=69
    RSUMMARY n=22 read=978267 noncubic=0 conn3=699819 basefail=0 sfail=0 rcerts=69
    RSUMMARY n=22 read=652029 noncubic=0 conn3=571270 basefail=0 sfail=0 rcerts=57

Totals recomputed: read = 7,319,447 = A002851(11) and BGM11 Table 1; conn3 = 5,909,292 =
A204198(11); basefail = 0; sfail = 0 (the strong form at n ≡ 4 mod 6 with `-strong` and
without `-f2` is (f1), i.e. "G − x has a Λ-factor for every vertex x", decided for all
5,909,292 graphs); rcerts = 586 referee-side certificates emitted. The eight slice read,
conn3, basefail and sfail figures equal those of the eight attack-side SUMMARY lines of
section 1, slice for slice. The certificate counts differ by design: the referee slices ran
`./refcheck -strong -rcert 10000` against the attack side's `./p3span -strong -cert 1000`,
a tenfold coarser sampling cadence, so rcerts = 586 against certs = 5,904. (The referee line
also reports `noncubic=0` where the attack line reports `cubic=<read>`; these are the same
fact stated as a defect count and as a pass count.)

Certificate cross-check (`refn22certs`), verbatim from `out_ref/ref_n22_certcheck.txt`:

     7319447 out_ref/geng22.g6
    REFCERT-SUMMARY file=out_ref/n22_certs_all.txt ok=5904 rejected=0 [membership checked] [3-connectivity checked]

i.e. all 5,904 attack-side n = 22 certificates were re-derived from the graph6 string alone
by the referee's checker, with 3-connectivity re-proved by exhaustive vertex-pair deletion
and with membership in a freshly regenerated `geng` stream of 7,319,447 lines.

Cost, from the runner log: eight slices 3,118.7 s, certificate cross-check 2,791.6 s,
total 5,910.3 s = 1.64 h single-core.

**n = 22: CONFIRMED** — base claim (P) and strong form (f1) for all 5,909,292 3-connected
cubic graphs on 22 vertices, counts matching both published enumerations, zero failures,
certificates cross-checked. (f2) was NOT tested at this order.

## 3. Referee recount, n = 24 (refcheck base claim, 60 geng slices) — NOT RUN

`q_ref24.jsonl` was written (61 jobs: 60 recount slices plus `refn24certs`) but never
executed: there is no `q_ref24.jsonl.logs`
directory and no `q_ref24.jsonl.state.jsonl`. n = 24 therefore has NO independent recount.
What section 1 establishes for it is attack-side completeness only.

## 4. Negative controls re-run TODAY (2026-08-11) — both failure paths still fire

Control A — the known non-3-connected example (the unique sub-3-connected base
failure at n<=16, g6 `O???E?oBEAWOKGK_@o?W_`, 1-connected, identified independently
by both pipelines in the original audit) pushed through today's referee binary with
the 3-connectivity filter disabled (out_ref/ref_negctl_2026-08-11_base.txt), verbatim:

    BASEFAIL O???E?oBEAWOKGK_@o?W_
    RSUMMARY n=16 read=1 noncubic=0 conn3=1 basefail=1 sfail=0 rcerts=0

Control B — one doctored certificate: line 1 of out/n22_r0.txt with its last triple
`20-8-21` replaced by a duplicate of its first triple `10-0-11` (creates overlap +
cover gap), fed to refcert.py together with the intact original
(out_ref/ref_negctl_2026-08-11_certs_input.txt). Output
(out_ref/ref_negctl_2026-08-11_certs.txt), verbatim:

    REJECT line 2: overlap between triples/avoided
    REFCERT-SUMMARY file=out_ref/ref_negctl_2026-08-11_certs_input.txt ok=1 rejected=1 [3-connectivity checked]
    refcert exit: 1

Both referee tools still reject what they must reject and accept what they must accept.

## 5. Verdict — CLOSED 2026-08-11

Written by the pre-release fix pass from the artifacts named in sections 1–4; every count
was recomputed from the raw per-slice output rather than from any reported total. It extends
REFEREE-VERDICT.md (n ≤ 20, signed 2026-08-06 by the adversarial referee) and supersedes
that verdict's line "Confirmed boundary: n ≤ 20 and nothing more" only for n = 22, and only
to the extent section 2 states.

**n = 22 — CONFIRMED.** Independent recount complete: 9/9 jobs `done` (rc = 0); read
7,319,447 = A002851(11) = BGM11 Table 1; conn3 5,909,292 = A204198(11); basefail = sfail = 0
on all eight slices, i.e. the base claim (P) and strong form (f1) hold for every one of the
5,909,292 3-connected cubic graphs on 22 vertices; all 5,904 attack-side certificates
accepted by the referee's checker with membership and 3-connectivity re-proved, 0 rejected.
Strong form (f2) was NOT tested at order 22 and is not claimed there.

**n = 24 — ATTACK-SIDE COMPLETE ONLY. NOT CONFIRMED.** Section 1 establishes that the search
pipeline finished all 60 slices (final attempt `rc = 0` on every job id), that its counts
equal 117,940,535 = A002851(12) and 98,101,019 = A204198(12), and that no output file
anywhere contains a failure line. The independent recount (`q_ref24.jsonl`) was never run
(section 3). This order must not be reported at theorem strength. The outstanding work is
exactly that queue.

**Confirmed boundary after this verdict: n ≤ 22, and nothing more.**

**Negative controls.** Both referee failure paths were re-exercised on 2026-08-11
(section 4), and again, more thoroughly, during the pre-release pass: the strong-form
control over the raw connected-cubic stream fires at orders 10, 12, 14 and 16 with the
per-type breakdown recorded in `out_ref/ctl_base_strong_2026-08-11.txt`, and eight distinct
corruption classes are each rejected by the gate that targets it — `refcert.py` with
`--g6set` and `--check3c` rejects all eight, `verify_cert.py` has no membership gate and so
rejects seven and accepts the non-canonical relabelling — with two controls-on-the-controls,
recorded in `out_ref/ctl_certs_2026-08-11_refcert.txt` and
`out_ref/ctl_certs_2026-08-11_verifycert.txt`.

— closed by the pre-release fix pass, 2026-08-11; recount and artifacts the referee's,
arithmetic re-done independently here.

## 6. Provenance disclosures added 2026-08-13 (documentation only; no count changed)

**6.1 The two Python certificate checkers are not independent of each other.** The header of
this document previously claimed that the referee pipeline shared no code with the attack
side `p3span.c`/`verify_cert.py`. That is true of the C pair and false of the Python pair.
`refcert.py:is_3connected` and `verify_cert.py:is_3_connected` are the same 85-token routine
under identifier renaming; their callee carries the identical name `connected_after_removing`
in both files and the same body up to local variable names. Both files also mis-describe the
routine — `refcert.py` said "BFS", `verify_cert.py` said "fresh BFS each time" — while both
implementations are a stack DFS (`stack.pop()`); that shared misdescription is itself evidence
of copying rather than convergence. About 24 of `refcert.py`'s 122 executable lines are
involved. The docstrings have been corrected; the code has not been touched.

This matters because the gate is load-bearing: `q_ref22.jsonl` job `refn22certs` runs
`python3 refcert.py … --g6set out_ref/geng22.g6 --check3c`, so the `[3-connectivity checked]`
token in section 2 comes through the shared code. **The n = 22 boundary stands anyway**, on a
separate footing: `refcheck.c` and `p3span.c` have disjoint function inventories apart from
`main` (`refcheck.c`: `uf_find`, `conn_minus`, `three_connected`, …; `p3span.c`: `dfs`,
`connected_without`, `is_3connected`, …), and the referee's C binary re-derives 3-connectivity
by union-find over all 7,319,447 generated graphs, arriving at conn3 = 5,909,292 =
A204198(11). The classification is independently corroborated by that binary. What is not
independent is the certificate-side 3-connectivity re-check, and it must not be read as such.

**6.2 `verify_cert.py` was replaced on release day and the change is UNVERIFIABLE.**
Filesystem birthtimes (not merely mtimes):

    p3span.c                  birth 2026-08-05T13:43:08
    refcheck.c                birth 2026-08-05T15:11:40
    refcert.py                birth 2026-08-05T15:13:07
    mkcontrols.py             birth 2026-08-11T21:13:11
    verify_cert.py            birth 2026-08-11T21:13:36
    REFEREE-VERDICT-n2224.md  birth 2026-08-11T21:22:52

`verify_cert.py`'s inode was created on release day, 25 s after `mkcontrols.py` and 9 minutes
before this verdict. An earlier `verify_cert.py` demonstrably existed on 2026-08-05:
`count3conn.py` (birth 2026-08-05T13:49:54) imports `g6_decode`, `neighbors` and
`is_3_connected` from it. No earlier revision survives to diff against — the two copies on
disk (`solve/problem-4/` and `certify-repo/kelmans-scripts/`) are byte-identical, and
`certify-repo` has a single commit touching the file (`bb58dc0`). **The content of that
replacement is therefore unverifiable, and it cannot be excluded that it is what introduced
the shared 3-connectivity routine recorded in 6.1.** No claim is made about what changed;
only what the filesystem supports is stated here.

The referee side by contrast did not move between 2026-08-05 and this pass:
`__pycache__/refcert.cpython-314.pyc` embeds source mtime 2026-08-05T15:13:07 and source
size 5435, which as of 2026-08-13 immediately before this documentation pass were exactly the
mtime and size of the live `refcert.py`; CPython invalidates that cache on any mismatch, so
`refcert.py` was byte-frozen across the release. (This pass edits `refcert.py`'s module
docstring per 6.1, so the `.pyc` no longer matches the live file. Its executable code is
unchanged — the diff is comment text only.)

**6.3 What did not change.** No count, no job status, no certificate, and no artifact was
touched by this pass. The confirmed boundary remains **n ≤ 22, and nothing more**.
