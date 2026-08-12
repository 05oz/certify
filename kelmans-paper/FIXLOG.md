# FIXLOG — note-kelmans pre-release fix pass (2026-08-11)

Target: `note.tex` and `note.md` (faithful twins), plus the artifacts that ship with
them. Three review reports (CLAIMS, PRIORITY, REPLAY). Every finding was re-settled
against the primary artifact or the archived primary source before any edit; where a
reviewer and the draft disagreed, the winner is recorded. Primary source throughout:
Kelmans, *Packing 3-vertex paths in cubic 3-connected graphs*, arXiv:0910.2766v2,
archived with the note.

---

## CLAIM-LEVEL CHANGES (read first)

**C-1. The Reed corollary is downgraded to a one-directional one.** The draft: "A
resolution of $(P)$ therefore settles a domination question as a corollary." Only a
*positive* resolution does; a counterexample to $(P)$ says nothing about Reed's conjecture
on 3-connected cubic graphs. Settled against the source, which is also explicit that the
implication is not the naive one — "If claim (P) in 1.10 is true, then **from 3.1** it
follows, in particular, that Reed's conjecture is true for 3-connected cubic graphs"
(Kel11 §1, emphasis added). Both changes made. The abstract was already correctly
conditioned ("a positive answer would give …") and is unchanged.

**C-2. Theorem 1.4 (the Kelmans equivalence) is restated: $(P)$ is not one of the claims,
and the equivalence is between class-universal statements.** Kelmans 3.1 reads "The
following claims are equivalent for cubic 3-connected graphs G:" and then lists
$(z1)$–$(z9)$, $(t1)$–$(t4)$, $(f1)$–$(f6)$ — nineteen claims, $(P)$ not among them; the
equivalence with $(P)$ is his separate §1 remark. Every claim has the form
"$v(G) = k \bmod 6 \Rightarrow \ldots$", so the equivalences hold between claims each
universally quantified over the class, never graph by graph. The draft invited the
per-graph reading, which is false and which would have broken the very
counterexample-conversion argument the note rests on. Restated, with the derivation of
$(P) \Leftrightarrow (z1)$ spelled out and the quantification made explicit. **No claim of
the note weakens as a result** — the conversion argument is about a counterexample
existing, not about a single graph satisfying two claims at once — but the statement a
referee reads is now the one Kelmans proved.

**C-3. $R_1$ is cyclically 5-connected, not 6-connected; the claim that cyclically
6-connected examples sit inside the verified range is withdrawn.** All three reviewers
flagged it; settled against Kelmans 6.1(a2), verbatim: "$c(R_s) = 6$ for $s \ge 2$ and
$c(R_1) = 5$". Independently: cyclic connectivity is at most girth, and a cyclically
6-connected cubic graph has girth $\ge 6$, hence $\ge 14$ vertices, so no 12-vertex example
can exist. The mathematics the note uses survives intact — 6.1(a1) and (a3) hold for
$s \ge 1$, so the two-path failure really does sit at order 12 — but the adjective is gone
and Question 6.1 now says the cyclically 6-connected members start at 24 vertices, i.e.
*outside* the verified range.

**C-4. "It … is deposited in *Certify*" → "will be deposited on publication".** Checked:
`certify-repo` contained no problem-4 content at review time (no match for
`kelmans|p3span|refcert|A204198`, no SWEEP-RECORD for this note). The Part I staging done
in this same pass is staged, not committed, not released — so the present tense would still
be false at the moment the byline goes on. Future tense it is.

**C-5. "A third, standard-library implementation reproduced the filtered counts" → the
standard-library checker's own routine, run by a separate driver.** An honest downgrade of
an independence claim in the trusted-base section. `count3conn.py` line 5 reads
`from verify_cert import g6_decode, neighbors, is_3_connected`: it is a driver, not a third
implementation. There are two independent 3-connectivity implementations in this work
(bitmask BFS in `p3span.c`, union–find in `refcheck.c`) plus the checker's exhaustive
vertex-pair deletion — three routines, but the third is the checker's own, not a fourth
artifact. Sentence rewritten and the scope ("at those orders") made explicit.

**C-6. Question 6.4's motivation is withdrawn.** The draft: "The obstructions in
$(r1)$–$(r8)$ are all cut phenomena, which suggests a counterexample would have high cyclic
connectivity or high girth." False, and it cuts the wrong way: Kelmans' $(r5)$ and $(r6)$
both begin "There exist infinitely many … $G$ is a cubic 3-connected graph **with no
3-cycles and no 4-cycles**". Restricted to $(r1)$–$(r4)$ (cuts and short cycles), with the
$(r5)$/$(r6)$ counter-consideration stated, and the closing "where it is most likely to
fail" replaced by a claim that can be defended. The same overreach in §6.1 ("Both are cut
phenomena", of $(r1)$ and $(r4)$) was replaced: $(r4)$ is about non-adjacency, and Kelmans
gives no construction for it that would license calling it a cut phenomenon.

**C-7. §4 no longer claims the two searchers ship.** The Part I deposit staged in this pass
contains the two certificate checkers, the recorded commands, the summaries, the full
certificate corpus, the controls and the verdict records — not `p3span.c` and `refcheck.c`.
§4 said "the two searchers and the two certificate checkers in source form"; it now names
what is deposited, says outright that the searchers are not in it, and states the
consequence: a reader can re-check every positive answer the searchers gave, and cannot
re-run a sweep from this deposit alone. The replay sentence changed with it ("re-running any
slice requires `nauty` and a C compiler" → "regenerating any graph stream requires `nauty`").

Nothing else in this pass changes what the note asserts. **Theorems 1.1 and 1.2,
Proposition 1.3, and every count in them are unchanged and were re-verified in this pass.**

---

## MUST-FIX

**M-1. Order-12 negative control: "253 of $(z8)$ type" was wrong.** Re-ran the control
today (`geng -q -c -d3 -D3 12 | refcheck -skip3c -strong -z7 -f2`): 253 =
**4 Z2FAIL + 8 Z3FAIL + 106 Z7FAIL + 135 Z8FAIL**. The reviewer was right about the cause —
the saved artifact recorded only the total plus a `head -4` that happened to be all Z8FAIL,
and the draft read the head as the type of all 253. Also re-ran orders 8, 10, 14 (which
confirm the draft: 0; 2 (f1) + 52 (f2) = 54; 145 (t2)) **and order 16, which the draft
omitted entirely**: 317 (f1) + 15,374 (f2) = 15,691. §3.3 now gives the full per-type
breakdown at every order; artifact `out_ref/ctl_base_strong_2026-08-11.txt`.

**M-2. The n = 22 referee verdict was an unsigned stub while §4 promised verdict records.**
Confirmed: §§2, 3, 5 of `REFEREE-VERDICT-n2224.md` read "(filled in as … completes)". The
computation is sound — I recomputed all eight slice sums from `out_ref/ref_n22_r{0..7}.txt`
(read 7,319,447; conn3 5,909,292; basefail = sfail = 0; rcerts 586) and replayed the job
states (9/9 `done`, which `jobrunner.py` guarantees means `rc = 0`). §§2, 3 and 5 are now
written and closed, with the provenance stated plainly: the recount, the code and the
outputs are the referee's; the arithmetic and the write-up are this pass's, and the section
says so rather than impersonating the referee's signature. §3 records that
`q_ref24.jsonl` was **never run** (no logs directory, no state file), so n = 24 stays at
attack-side-complete strength.

**M-3. [KS05] page range 749–762 is wrong.** Crossref, DOI `10.1016/j.disc.2005.07.005`:
Kostochka & Stodolsky, *On domination in connected cubic graphs*, Discrete Mathematics
**304**, issue 1–3 (2005), **45–50**. The wrong range was inherited verbatim from Kelmans'
reference [17]. Fixed in both twins.

**M-4. The $R_1$ descriptor** — see C-3.

**M-5. The deposit tense** — see C-4.

---

## SHOULD-FIX

**S-1. $(f2)$'s incidence restriction is now attributed.** Kelmans' $(f2)$ carries no
restriction; the note adds "not incident with $x$" and justified it in its own voice. The
justification is Kelmans' own, in the proof of 3.21: "If $x \in \{y_1, y_2\}$, then
$G - \{x, e\} = G - x$, and therefore, by 3.20, our claim is true." Now cited as
`[Kel11, 3.21]`, and the note says outright that Kelmans states the claim unrestricted.

**S-2. The constructivity sentence is now quoted, not reconstructed.** The single
load-bearing sentence for the whole counterexample-hunt framing is in the source:
"We actually give different proofs of 3.1. Thus, if there is a counterexample C to one of
the above claims, then these different proofs provide different constructions of
counterexamples to the other claims in 3.1." (Kel11 §1). The draft inferred it from the
fact that the proofs use explicit compositions — strictly weaker than the source it could
cite. Quoted.

**S-3. The partial-results sentence cited the weakest known cubic bound.**
$\lambda \ge \lceil v/4 \rceil$ [KM04] is Kelmans 1.3 and correctly attributed, but 1.6 and
1.8 of the same introduction improve it for connected cubic graphs: $\frac{39}{152}v$ for
$v \ge 17$ and $\frac{3}{11}v$ for $v \ge 9$. Both added, with references verified
independently: Kosowski–Małafiejski–Żyliński, *Tighter Bounds on the Size of a Maximum
$P_3$-Matching in a Cubic Graph*, Graphs Combin. **24** (2008), no. 5, 461–468 (Crossref
`10.1007/s00373-008-0807-7`); Kosowski–Żyliński, *Packing Three-Vertex Paths in 2-Connected
Cubic Graphs*, Ars Combin. **89** (2008) (DBLP `journals/arscom/KosowskiZ08`; **page range
deliberately omitted** — Ars Combinatoria is not in Crossref and I could not verify
Kelmans' "95–113" independently, and his page range for [KS05] turned out to be wrong).
The bound itself is attributed as recorded in `[Kel11, 1.8]`. Also: $\lceil v/4 \rceil$
holds for *all* cubic graphs, so it no longer sits under "restricted classes".

**S-4. The claw-free result now cites the published version too.** [Kel07b] (arXiv
0711.3871) is what Kel11 cites, and the note's statement of it is faithful. Added
`[Kel11b]` = Kelmans, *Packing 3-vertex paths in claw-free graphs and related topics*,
Discrete Appl. Math. **159** (2011), no. 2–3, 112–127 (Crossref
`10.1016/j.dam.2010.05.001`) as a "see also". One reviewer reported that the published
paper proves substantially more (3-connected claw-free, not necessarily cubic); **I could
not read it** — Elsevier paywall, and the arXiv API was unresponsive during this pass — so
the note does not state its contents. Citation only.

**S-5. Akiyama–Kano sourcing made visible.** JGT 9 (1985) 1–42 and LNM 2031 are both
paywalled and neither was read; the conjecture as the note uses it comes from West's REGS
page, re-fetched live today (HTTP 200) and quoted verbatim: "Conjecture 1: (Akiyama-Kano
[AK1]) When $3$ divides $n$, every $3$-connected $3$-regular $n$-vertex graph has a
$P_3$-factor." The note now says it takes the conjecture *in the form recorded by West*,
attributed there to the survey — instead of asserting the survey's contents at first hand.

**S-6. NP-hardness citation narrowed.** Kelmans credits cubic-graph hardness to his own
unpublished [6] and only the cubic *bipartite planar* case to [16] = KMZ05. Logically the
subclass result suffices, but the note now says "remains NP-hard already for cubic
bipartite planar graphs [KMZ05]" so the citation cannot be read as KMZ05's cubic result.

**S-7. Runtimes corrected.** "A few hours per pipeline through order 22" → about an hour
and a half: replayed from the job state files, the attack side is 3,966 s = 1.10 h
(n = 22 slices 3,833.5 s, n = 20 125.3 s, n = 18 7.2 s) and the referee side 5,910.3 s =
1.64 h including the certificate cross-check. "Order 24 was about 29 hours" is the sum of
*completing* attempts (103,442.9 s = 28.73 h); 28 attempts across 60 slices hit their time
limit and were rerun, for 172,049.9 s = 47.79 h of machine time. Both figures now stated,
with the basis named. §6.3's throughput and order-26 projection are computed off the 29 h
figure and remain self-consistent with it.

**S-8. "Queue files recording the exact command line for every generator slice at every
order" overstated the queues.** True: no queue file covers n ≤ 16; those commands lived
only in `NOTES.md`, which was not in the shipped inventory. Fixed on both sides — the
sentence now says "the recorded command line for every sweep and every generator slice at
every order", and the staged repository ships `kelmans-certificates/REGENERATE.md`, which
carries every command including the n ≤ 16 sweeps and the checker invocations.

**S-9. The drafting-date control re-run had been reduced.** The 2026-08-11 certificate
control on file was 2 lines / 1 corruption, run without the membership check. Rather than
weaken the sentence, the controls were rebuilt and re-run in full today: eight distinct
corruption classes (non-path triple, cover gap, overlap, sub-maximum packing shape,
trailing graph6 character, flipped graph6 character, valid certificate for a non-canonical
relabelling, genuine certificate for a connected cubic graph that is not 3-connected), each
rejected by the gate it targets, by **both** checkers, plus two controls-on-the-controls
(disabling membership admits the relabelling and nothing else; disabling 3-connectivity
admits the sub-3-connected certificate and nothing else). §3.3 now describes exactly this.
Builder `mkcontrols.py`, artifacts `out_ref/ctl_certs_2026-08-11_*`.

**S-10. Table 1 caption.** The 3-connected column matches A204198 at every order but
[McKR86] only at orders 10–20 (the n ≤ 20 ledger has "—" for n = 4, 6, 8). Caption now
says so.

**S-11. Order-28 figure mislabelled.** 35,085,504,243 is A204198(14), the number of
3-connected cubic graphs on 28 vertices, not the number of decisions an $(f1)$ test costs
(that is 28 per graph). "needs 35,085,504,243 decisions" → "has 35,085,504,243 graphs to
decide", matching the parallel order-26 clause.

---

## NITS APPLIED

**N-1. Two n = 22 slices were listed out of order** (…879,959 + 652,029 + 978,267). Actual
r5, r6, r7 = 879,959, 978,267, 652,029. Sum unaffected; order corrected in both twins.

**N-2. `verify_cert.py` accepted trailing graph6 garbage.** Its decoder required
`len(bits) >= need`; `refcert.py` requires exact length. Fixed to the exact-length test, and
a decode failure now prints a clean diagnostic instead of a traceback. Affects no claim
(machine-generated corpus, membership checked at 18/20/22), but a shipped checker should not
have the hole. **Regression check: all 43,580 certificates through order 22 and all 9,776 at
order 24 still verify after the change.**

**N-3. Bibliographic corrections.** [HK86] title is "Packings by Complete Bipartite Graphs"
(plural; Crossref `10.1137/0607024`), author D. G. Kirkpatrick — the singular was inherited
from Kelmans' [3]. [KMZ05] LNCS 3911 is dated 2006 by Crossref (PPAM 2005 conference).
[Kel11] reads as a Discrete Math. citation, but no journal version exists (Crossref has no
Kelmans article of this title); the entry now says the arXiv text is the version of record.
[McKR86] now carries the author's public copy URL (fetched today, HTTP 200), since Ars
Combinatoria 21A is hard to obtain.

---

## CHECKED, DRAFT WAS RIGHT — NO EDIT

* Every count in the note recomputed from raw outputs in this pass: 429,865 (n ≤ 20);
  5,909,292 and 7,319,447 (n = 22, both pipelines, slice by slice); 6,339,157; 7,875,918;
  30,527 and the 99.5% complement; 43,580 / 34,429 / 40,333 / 3,247 / 9,776; 98,101,019 and
  117,940,535. All correct.
* The strong-form ledger of Theorem 1.2 against the actual flags: `refcheck.c` dispatches
  $r6 = 0$ + `-strong` → (z2),(z3),(z8), with (z7) only under `-z7`; $r6 = 2$ → (t2);
  $r6 = 4$ + `-strong` → (f1), with (f2) only under `-f2`. The queues passed `-strong -z7
  -f2` at n ≤ 16, `-strong -z7` at 18, `-strong` at 20 and 22, and no `-strong` at 24. The
  per-order list and §1.4's "(f2) was not tested at order 22, and (z7) and (z8) were not
  tested at order 24" are exactly right.
* The §2.3 exemplar certificate is line 1 of `out/n22_r0.txt` and verifies as printed.
* Problem 1.10, the labels (z2),(z3),(z7),(z8),(t2),(f1), and (r1)/(r4) are verbatim
  faithful to arXiv:0910.2766v2.
* The negative-control graph `O???E?oBEAWOKGK_@o?W_`: re-derived independently in this pass
  — connected, cubic, cut vertices {6, 11, 13, 14}, and $\lambda = 4 < 5$ by exhaustive
  maximum packing. Exactly as §3.3 says.
* Both checkers import only `sys` (and `gzip`) — PROTOCOL §10 satisfied; re-confirmed after
  the N-2 edit.
* §1.4 and Proposition 1.3 hold n = 24 at attack-side-complete strength with the recount
  named as outstanding. Nothing in the note inflates n = 24, and nothing in this pass
  changed that.

---

## NOT DONE, AND WHY

* **The n = 24 independent recount was not run.** It is roughly a day of machine time and
  two deep-research workflows were running; it is named as the outstanding work in
  Proposition 1.3, §3.4, §6.3 and the verdict record.
* **The abstract's "34,429 of them by two such checkers" was not raised**, although in this
  pass all 53,356 certificates (43,580 through order 22 plus 9,776 at order 24) were run
  through **both** shipped checkers from the staged repository, 0 rejected. The rule for
  this pass is never to strengthen a claim on the way to release, so the note keeps the
  number its own §3.2 documents; the repository README records the stronger run, which is
  a statement about the deposit rather than about the theorem. The two do not conflict —
  the note's figure is a lower bound and is stated as one.
* **The suggestion to note that Problem 1.10 is numbered 1.9 and undated in the earlier
  preprint arXiv:0801.1239 was not adopted** — the arXiv API did not respond during this
  pass, so the numbering could not be checked at first hand, and the note already names the
  version whose numbering it follows.

---

## RELEASE STAGING (Part I, v0.9.0) — staged, NOT committed, NOT released

Staged into `certify-repo/` and left for review:

* `kelmans-paper/` — `note.tex`, `note.md`, `note.pdf` (10 pp., tectonic 0.17.0, clean
  compile, no warnings), `FIXLOG.md`.
* `kelmans-certificates/` — the **full** corpus, 53,356 certificates in five files by
  order (4–16, 18, 20, 22, 24; 4.6 MB plain text, no compression, so both checkers read it
  directly); `summaries/` with the per-slice summary line of the completing attempt of
  every job on both pipelines; `controls/` with today's negative-control inputs and
  outputs; both referee verdict records; `REGENERATE.md` with the exact commands, the
  expected outputs and SHA-256 for every file.
* `kelmans-scripts/` — `verify_cert.py`, `refcert.py` (the two independent stdlib
  checkers), `count3conn.py` (the 3-connectivity recount driver), `mkcontrols.py` (the
  control builder). **The searchers are not staged**, per the release instruction; §4 of
  the note was changed to match (C-7).
* `SWEEP-RECORD-KELMANS-2026-08-11.md`, a README "Part I" section and layout entry, and
  `.zenodo.json` rewritten for v0.9.0 (title begins `"Certify v0.9.0`, so the PROTOCOL §12
  pre-push hook will pass for tag `v0.9.0`; verified by running the hook's own test).

**Staged-location test, run after staging:** `python3 kelmans-scripts/verify_cert.py
kelmans-certificates/certs_n*.txt` → `VERIFIED 53356 certificates (53356 distinct graphs)`,
exit 0, ~36 s; `refcert.py` over the same five files → `ok = 3247 / 30468 / 3961 / 5904 /
9776`, `rejected=0`, exit 0; the staged control file through the staged `refcert.py` →
7 rejections plus the membership case when a regenerated `geng` stream is supplied, exit 1;
`count3conn.py` from the staged path reproduces 4 / 14 / 57 / 341 / 2828 at orders 8–16.
Both checkers were also run under `/usr/bin/python3` (CPython 3.9.6) and under
`env -i python3 -I -S -E`; only `sys` and `gzip` are imported anywhere, so PROTOCOL §10
holds for the staged copies.

**Not touched:** `CITATION.cff` still reads `version: 0.4.0` and lists Part D as the last
DOI. It has been stale since v0.5.0 and updating it is a release-process decision, not a
fix-pass one; flagged here rather than changed.
