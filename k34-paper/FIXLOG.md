# FIXLOG — note-k34 fix pass

Target: `note.tex` and `note.md` (faithful twins), plus the artifacts that ship with
them. Three review reports (CLAIMS, PRIORITY, REPLAY). Every finding was re-settled
against the primary artifact or the archived primary source before any edit; where a
reviewer and the draft disagreed, the winner is recorded.

---

## CLAIM-LEVEL CHANGES (read first)

**C-1. k(6,3) lower bound raised 26 → 29. This is a CHANGE, not a fix, and it is the one
item in this pass that alters what the note asserts.** The draft published
26 ≤ k(6,3) ≤ 33 while the artifact set it ships contains three verified 28-vertex
{I₆,TT₃}-free oriented graphs. Publishing the weaker bracket alongside those files would
have been self-refuting on release. Settled against the artifacts, not the reports: I
re-verified all seven k(6,3) witnesses (orders 25–28) with my own code, using the raw
definition of TT₃ (explicit linear-order realisation) rather than the score-sequence
criterion the shipped verifier uses, plus exact independence numbers by branch and bound —
α = 5 in every case, no I₆, no TT₃. Cross-checked against the shipped `verify_witness.py`
(second criterion). The witness now printed in the note,
Cay(ℤ₂₈,{3,8,10,12,17}), is hand-checkable except for the independence number:
−S = {11,16,18,20,25} is disjoint from S (so it is an oriented graph) and
S+S = {1,6,11,13,15,16,18,20,22,24,25,27} is disjoint from S (so no TT₃).
*Verification standard, stated plainly: this bound has had one independent
re-derivation, not the multi-lens adversarial protocol that k(3,4) = 21 received.* It is a
finite check over 376,740 six-subsets and 3,276 triples, the cheapest class of claim in the
paper, and it is the same standard the note already applies to its 20-vertex witness.

**C-2. k(4,4) ≤ 49 → 50 and k(3,5) ≤ 54 → 55 (both were WRONG; the first was in the
abstract).** These are honest weakenings. 1+14+14+20 = 49 caps the *order of a free graph*;
the Ramsey number is one more — which is exactly how the note itself does the (3,4) case in
§3.1. Confirmed independently against the archived IRW v3, Lemma 2.3, whose proof reads
"|V| ⩽ |{v}|+|N⁻(v)|+|N⁺(v)|+|I(v)| ⩽ 2r(Iₘ₊₁,Lₙ)+r(Iₘ,Lₙ₊₁)−2. This implies the
assertion." Evaluating the recursion: r(I₄,L₄) ≤ 2·15+21−1 = 50, r(I₃,L₅) ≤ 2·21+14−1 = 55.

**C-3. "Every certificate was verified by two independently written checkers" → one
checker for all 445, a second for twelve.** An honest downgrade of the note's central
independence claim, in the trusted-base section. The abstract and §4.2 already had it
right; §1.2 and §7 overstated it.

**C-4. k(6,3) ≥ 26 remains true and is retained implicitly; no claim anywhere in the note
was strengthened beyond what an artifact I verified myself supports.**

---

## AUTHOR ACTION REQUIRED BEFORE SUBMISSION (not fixable here)

**A-1. The first footnote credits "Claude Fable 5 (Anthropic)".** I cannot verify from any
artifact which model produced the encodings, searches and audits. This is a factual methods
statement going out under a real byline, so I neither changed nor endorsed it. **The author
must confirm the model name.** Guessing would be worse than flagging.

**A-2. The Certify deposit must actually happen before submission.** §6 now says "deposited
… at release" rather than "is archived", so the note is no longer false in the present
tense — but at the time of this pass `certify-repo` contains no Erdős-112 / k(3,4)
directory (`git ls-files | grep -ic "erdos|k34|112"` → 0, working tree clean, nothing
unpushed).

---

## MUST-FIX

| # | Finding | Verdict | Action |
|---|---|---|---|
| M1 | k(4,4) ≤ 49 and k(3,5) ≤ 54 off by one (abstract + §8.3) | **Reviewer right**; confirmed against IRW Lemma 2.3 | Abstract → k(4,4) ≤ 50; §8.3 restated as order-cap 49/54 ⇒ k ≤ 50/55, credited to the IRW recursion |
| M2 | k(6,3) ≥ 26 refuted by the paper's own artifacts | **Reviewer right**; 7 witnesses re-verified by me, three at N=28 | Prop 1.4/1.2 → 29 ≤ k(6,3) ≤ 33 with the Cayley witness proved in-line; see C-1 |
| M3 | "two independently written checkers" for all 445 | **Reviewer right**; CERTLOG is written solely by `lrat_check.py`, `ref_lrat.py` ran on 12 | §1.2 and §7 corrected; §7 closing "checked twice by unrelated code" → "every proof checked by code unrelated to the solver, a sample by two such checkers" |
| M4 | Uniqueness of Bermond's 8-vertex graph credited to Bermond | **Reviewer right**; read in the archived IRW v3: intro credits Bermond with the value "mainly by providing an example establishing the lower bound", Lemma 3.1 proves uniqueness and gives the ℤ₈ description | §1.1, §3.1 (Prop) and §8.1 now cite [IRW21, Lemma 3.1] for uniqueness; Bermond keeps the value |
| M5 | Two characterizations lifted from erdosproblems but cited to unread primary sources | **Reviewer right**; NOTES.md lists only two sources read in full | §1.1 opens "As recorded at [Blo]:", the borrowed clause reworded, and the Larson–Mitchell bound additionally anchored to [IRW21, Lemma 2.4], which I read |
| M6 | REGENERATE.md's "what must never be lost" list cannot regenerate anything | **Reviewer right**; I rebuilt the kit and reproduced all three failures | Table now includes the 70 `blocks_*.json` + bermond8 + qr7, `verify_chain.py`, `verify_witness.py`, `make_structured24.py`. **Retested: kit alone regenerates `s21_587_1.cnf` to CERTLOG's `cnf_sha256`, and both witnesses verify** |
| M7 | §10 portability violation on the verification path (`gzip` shell-out) | **Reviewer right**; `verify_one.py:48`, `verify_and_pack.py:56`; `lrat_check.py` could not read `.lrat.gz` at all | Replaced with a stdlib `pack()`; `lrat_check.py` now reads `.lrat` and `.lrat.gz` interchangeably. **Retested: t339 → 2,097 steps, t248 → 855, s22_A0 → 310,450, all matching CERTLOG; truncated / final-line-removed / mutated-hint controls all still rejected, including through the gzip path** |
| M8 | Archival claim in the present tense but not yet true | **Reviewer right** | §6 recast to deposit-at-release; see A-2 |

## SHOULD-FIX

| # | Finding | Verdict | Action |
|---|---|---|---|
| S1 | "the four largest proofs in the corpus" | **Reviewer right**; `s21_677_22_2` (4th largest, 2.049 GB) was never checked. Error originates in FINAL-REFEREE-k34.md and propagated | §4.2 → "the largest proof in the corpus, all three entries with a repair history (these four are the 2.0–2.3 GB proofs, four of the five largest), the smallest, the largest of every remaining type, and one further cube" — 10, and it is what was actually done |
| S2 | "two ledger lines poisoned … were repaired" | **Reviewer right**; there were three. FAILLOG.txt line 1 records the 2026-08-06 `s21_677_0_1` repair; the backup diff shows only `s21_677_22_0` and `s21_677_6_1` | §4.1 rewritten: three repairs, causes named, and the backup's coverage stated honestly (two originals in the backup, the first only in the failure log, the backup having been taken afterwards) |
| S3 | "the best bound previously derivable from the literature was 24" | **Reviewer right**; C₃ ⊔ W₂₂ is one-line derivable | → "No lower bound beyond 24 … appears in the literature" |
| S4 | Ledger described as recording "byte counts of formula and proof" | **Reviewer right**; CERTLOG has no formula byte count | §3.4 → "the SHA-256 digests of formula and of proof, and the proof's byte count" |
| S5 | "the queue files … for every cube" false for `s2434` | **Reviewer right**; I confirmed: 444/445 covered, `s2434` alone missing | §6 scoped to the N=21, 22, 23 layers; REGENERATE.md documents `make_structured24.py` as the route for `s2434` |
| S6 | IRW pinpoints follow arXiv v3 but the bibitem leads with the journal version | **Reviewer right** | Left as is — the bibitem already states "Also arXiv:1707.09556 (v3, April 2020), the text read here". Judgment: the disclosure is already in the bibitem, not only the footnote |
| S7 | The published ≤ 25 has a second citable source | **Reviewer right**; I reconstructed IRW's v(m,n) and validated it on four known values (v(2,3)=4, v(3,3)=9, v(4,3)=15, v(5,3)=23), then v(3,4)=25 | §1.1 now cites [IRW21, Prop. 6.1] alongside Lemma 2.3 |
| S8 | §3.1 reproduces IRW Lemma 2.3's proof without citing it there | **Reviewer right** | Pinpoint added at the counting argument |
| S9 | The note never states #112 itself remains open | **Reviewer right** | §1.3 opens with the non-claim. Worded from the problem statement, not from the site (I did not fetch it) |
| S10 | REGENERATE.md size figures wrong by ~2× | **Reviewer right**; measured: CNFs 2.07 GB (s21 alone 1.53 GB), proofs 281.3 GB (s21 alone 244.8 GB) | Corrected, with the CERTLOG sum named as the check |
| S11 | RESULTS.md carries a stale problem-1 body contradicting its own UPDATE blocks | **Reviewer right** | SUPERSEDED banner added at the head of the section; the headline entry corrected to k(3,4)=21 and 29 ≤ k(6,3) ≤ 33 |

[Correction, 2026-11-17, to S3: the replacement sentence was itself wrong. The literature stated
only 18, and C₃ ⊔ W₂₂, which the row calls one-line derivable, gives k(6,3) ≥ 26, beyond 24. See
G-5 below.]

## NITs

| # | Finding | Verdict | Action |
|---|---|---|---|
| N1 | "averaging three million checked steps" | **Reviewer right**; s21 mean = 2,562,658 | → "about two and a half million" |
| N2 | "ten adversarially chosen" then nine enumerated | **Reviewer right** | Folded into S1; the tenth (`s21_884_0`) is now "one further cube" |
| N3 | "established internally three ways" followed by four | **Reviewer right** | → "four ways" |
| N4 | Chronology in the body ("computed before the N=21 layer settled") | **Reviewer right**; earns nothing | Removed from §1.2 and §5.1. The honesty disclosures and the referee date are kept — they earn their place |
| N5 | k(m,3) = Θ(m²/log m) is IRW's theorem but the lower half is Kim's | **Reviewer right**; confirmed in IRW ("since Kim in [11] established a lower bound of appropriate order") | §1.1 now says "combining their upper bound with Kim's lower bound for r(Iₘ,K₃)" |
| N6 | k(2,4) = 8 left as "classical" while k(3,3) gets Bermond by name | **Reviewer overreached** | No change. I verified only that IRW cite Erdős–Moser for a *lower* bound on r(I₂,Lₙ); I did not verify that they prove k(2,4)=8. "See [IRW21] and the references there" is already correct and safe |
| N7 | Cite the CaDiCaL upstream tag for reproducibility | Optional | No change; the bibitem already names 3.0.1 as the version used |
| N8 | §8.2 "an exhaustion … at N = 33" | Loose | Dropped the order; the sentence is about the inventory requirement, which is what matters |

## Corrections to the reviewers

- CLAIMS describes `witness_cayley_6_3_n28_4_5_6_19_26.json` as sitting in the same list as
  the ℤ₂₈ witness; it is in fact a Cayley digraph over ℤ₁₄ × ℤ₂, not ℤ₂₈. Its freeness is
  unaffected. The note says so.
- CLAIMS/REPLAY report the Cayley sweep at orders 29–32 as returning nothing. True, but the
  searches at 26–28 **stop at the first witness**, so nothing about exhaustiveness at those
  orders may be claimed, and the order-32 sweep covered three of the seven abelian groups.
  §8.2 is worded to exactly that scope.

## Build

`/opt/homebrew/bin/tectonic note.tex` — clean; one cosmetic underfull-vbox warning, no
errors. **10 pages** (unchanged).

## Spot-regeneration (within the 2-cube allowance)

`s21_587_1` regenerated end to end through the *edited* chain, inside an isolated kit so the
live ledger was untouched: CNF `sha256=fc75efa5…` = CERTLOG; proof `sha256=29be5fc9…`,
53,128,231 bytes = CERTLOG, byte-identical; `verify_one.py` → "VERIFIED: empty clause
derived after 236431 checked steps" = CERTLOG. Regeneration determinism now 11 of 11.
[Correction, 2026-11-17: nine regenerations are on record, the referee's eight and this one,
all byte-identical; the other two attempts in the count have no record. See G-11 below.]

## Post-review addendum (2026-08-11)
The flagged verification asymmetry on k(6,3) >= 29 is resolved: a dedicated adversarial referee
(fresh code, raw definitions, no reuse of the shipped TT_3 criterion) CONFIRMED the claim —
alpha = 5 by exhaustive scan of all 376,740 six-subsets; 0 transitive triples; the object
verified arc-for-arc as Cay(Z_28,{3,8,10,12,17}); novelty supported (strongest prior lower
bound was the trivial 18). Full verdict: REFEREE-k63.md. The model-credit footnote was
corrected from "Claude Fable 5" to "Claude (Anthropic)" — the work spanned multiple Claude
models and a single-model claim was inaccurate.
[Correction, 2026-11-17: 18 is the strongest bound the literature stated, but one-line
assemblies of IRW's graphs give 26. See G-5 below.]

## Documentation-correction round, 2026-08-13

Recorded after the fact. The v0.14.0 round corrected four claims in this part and left no entry
here; the Engine 2 re-gate of 2026-08-13 found the omission. All four concern what the public
deposit contains. No certified value, checker or mathematical result changed.

**G-1. The k(3,4) referee's verdict record and fresh code were claimed to ship.** The header
comment and the confirmation paragraph said they "ship with the artifacts". They are retained by
the author and are not deposited. What the deposit does carry is the review log and the separate
verdict record for the k(6,3) bound of the same note. Corrected in both twins.
Propagation grep (`ship with the artifacts`): 0 remaining in tracked text, 0 in extracted PDF
text across all thirteen shipped PDFs.

**G-2. The archived arXiv v3 copy was claimed to ship.** It is archived in the author's working
tree and not redistributed; section references still follow its numbering. Corrected in both
twins. Propagation grep (`archived with the artifacts`): 0 remaining in tracked text, 0 in
extracted PDF text.

**G-3. Regeneration determinism read "8 of 8 attempts" in the note.** This log already recorded
11 of 11 at line 124, written 2026-08-11 — the note was stale, not the log, and the two
disagreed for two days. Corrected to "11 of 11 attempts" in both twins.
Propagation grep (`8 of 8`): 0 remaining. (`11 of 11`): 4 tracked sites — this log, note.md, and
two Part B sites (`SWEEP-RECORD-QEC-2026-08-04.md`, `paper/preprint-qec-distances.md`) that
count Part B negative controls and are unrelated to this claim.
[Correction, 2026-11-17: "11 of 11" was itself not supported; nine attempts are on record. See
G-11 below.]

**G-4. "All of it is deposited in the program's public certificate repository" was false.** The
record is split between the public deposit and a private regeneration kit. The note now itemizes
both sides. Deposited: the ledger, the regeneration instructions, the two witness files, six
scripts (`gen_cnf.py`, `make_structured.py`, `lrat_check.py`, `verify_witness.py`,
`audit_cnf.py`, `audit_multiset.py`), the review log and the k(6,3) referee verdict. Retained and
not redistributed: the queue files, the 70 block-class representatives the generators consume,
the rest of the checking and audit pipeline, and the audit and k(3,4) referee records. Two
consequences are now stated rather than left implicit — `audit_multiset.py` imports a module of
the kit and does not run from the deposit alone, and regenerating a case formula to its recorded
`cnf_sha256` needs the representatives. The LRAT corpus is a regenerable cache and is not
shipped, so no shipped certificate depends on a hash for its replay. Corrected in both twins and
in `k34-certificates/REGENERATE.md`.
Propagation grep (`All of it is deposited`): 0 remaining in tracked text.
[Correction and update, 2026-11-17: the representatives number 72, the 70 block files and the two
witness files `witness_bermond8.json` and `witness_qr7.json` (the M6 row above already lists
them so). Since commit 4794560 of 2026-11-17 they are in the repository, with the queue files and
`verify_chain.py`. See G-13 below.]

## Correction round, 2026-11-17

Every decision below corrects or updates the text of the note, its records or its scripts. No
certificate, ledger line, witness or checker logic changed; `verify_chain.py`,
`make_structured.py` and `audit_multiset.py` changed in their docstrings only (no file's digest is
published anywhere in the repository; checked). Dated notes in the note use the form "(Correction,
2026-11-17: ...)"; dated records keep their text and gain a bracketed note. Each propagation grep
was run over the whole tree of this release after the edits; the hits it lists as remaining are
the places where a dated note quotes the old wording, or a dated record followed by its note. Counts were re-measured after the
fixes of the verification and the referee of 2026-11-17, across line breaks and markup; unless a
line says otherwise they leave out this log, CORRECTIONS.md and .zenodo.json, which quote old
wording as records.

**G-5. §5.2 misstated the prior lower bound for k(6,3).** It said that no lower bound beyond 24
appears in the literature. The literature stated only 18 (k(6,3) ≥ R(6,3), IRW v3, §1), and
one-line assemblies of known graphs give 23 (from k(5,3) = 23), 24 (IRW's W₂₂ plus an isolated
vertex) and 26 (W₂₂ with a disjoint directed 3-cycle, 25 vertices, the union of the paragraph's own
partition 3 + 22). This log knew the 26 in August (C-4 and S3) and wrote the wrong sentence anyway.
The 29 of Proposition 1.2 exceeds the best one-line assembly by 3. Found in our own records: a
record of 2026-10-20 and a review of 2026-11-11 that checked W₂₂, W₂₂ + K₁ and
W₂₂ ⊔ C₃ with code. Re-checked for this entry (W₂₂ has no I₅ and no TT₃; W₂₂ ⊔ C₃ has no I₆ and
no TT₃; adding one more isolated vertex gives an I₆). Corrected in both twins with a dated note;
dated notes added to REFEREE-k63.md ("improves this by 11"), to the August sweep record and to S3
and the post-review addendum of this log. Proposition 1.2 is unaffected.
Propagation grep (`No lower bound beyond`): 3 hits, the two dated notes and S3 of this log
(followed by its note). (`beyond 24`): 3, the same two dated notes and S3. (`improves this by
11`): 1, REFEREE-k63.md, followed by its note.
[Amended after the referee of 2026-11-17: the dated note said "Read literally that was false
both ways"; literally the sentence was false once, since the literature stated only 18, and it
missed the 26, which follows in one line. Both twins now say so. Propagation grep (`both ways`): 0.]

**G-6. §8.3 gave k(4,4) ≥ 21 where the note's own W gives 28.** W ⊔ QR₇ has 27 vertices,
independence number 2 + 1 = 3 and no TT₄ (a TT₄ is a tournament and lies inside one part), so
k(4,4) ≥ 28. Re-checked for this entry, with the control that one more isolated vertex gives an
I₄. Found in the same two records as G-5. Corrected in both twins with a dated note, which also
records later work: Muhamadiev Faridun's lower bounds k(4,4) ≥ 34 and k(3,5) ≥ 31 (22 September
2026), whose two circulants on ℤ₃₃ and ℤ₃₀ were re-checked for this entry, and, added after the
referee of 2026-11-17, the stronger k(4,4) ≥ 40 and k(3,5) ≥ 43 of the GitHub repository
rsvaultpudgy-create/erdos-112-lower-bounds (created 11 November 2026), whose circulants on ℤ₃₉ and
ℤ₄₂ the referee checked.
Propagation grep (`k(4,4) ≥ k(3,4) = 21`, `k(4,4)\ge k(3,4)`): 1 hit each, the dated notes.

**G-7. The 2017 remark that gives k(3,4) ≥ 21 was not credited.** The first arXiv version of
[IRW21], arXiv:1707.09556v1 (29 July 2017), states r(I₃,L₄) ≤ 24, with a proof by an integer
program, and remarks in its Section 2 (TeX source lines 757 and 758) that the largest
{I₃,L₄}-free Cayley graph has only 20 vertices, which implies k(3,4) ≥ 21; it gives no graph and
no group. Neither statement is in v2 or v3; August read v3 only. v1 was read in full for this
entry. Recorded in our own sweep of 2026-10-14 and pointed out publicly by the reviewers at
erdosproblemaday.com on 2026-11-16. Added after the referee of 2026-11-17: the working report of
Erdős Problem a Day on problem 112 (erdosproblemaday.com/report/112, dated 2026-08-12, initial
run 2026-07-26; read by our sweep of 2026-10-14) exhibits the circulant and states
21 ≤ k(3,4) ≤ 25; its first public date is not established in our records, and §1.1 now says so. Dated notes in both twins at the prior-art record, the
abstract and §1.1, the bibliography entry extended, a comment in the LaTeX header, a dated note in
the README section and in the August sweep record.
Propagation grep (`9 ≤ k(3,4) ≤ 25`, `9 <= k(3,4) <= 25`, `9\le k(3,4)\le 25`, and
`9 \;\le\; k(3,4)` in the LaTeX §1.1, which the first three miss): 6 places, each the
August statement followed by its dated note (README, abstract and §1.1 of both twins, the LaTeX
header comment).

**G-8. The header said the referee had no access to the pipeline's code.** The header said the
referee of §4.2 "was a separate agent instance given no access to the pipeline's code"; §4.2 said
"a separate agent instance". The records of the referee pass document neither. They show that
every load-bearing check used code written fresh for the pass, and that the pass worked inside the
run directory, used the ledger, the queue file, the block files and the failure log, and re-ran
one audit script of the pipeline. Found by our own record check of 2026-11-17 and confirmed by a
separate check the same day. Both sentences now say only what the records show, with dated notes,
in both twins.
Propagation grep (`given no access`), as re-run after the whole round: 2 Part G hits, the dated
notes; the Part B hits are the dated notes of its decision B-5; 4 more lines in Parts C and I
(`tt3-paper/note.*`, `kelmans-paper/note.*`), the same phrasing about their own audits, which are
not checked here (see CORRECTIONS.md). (`separate agent instance`): 4 Part G hits, all in the dated
notes; the Part B hits are dated notes (B-5); the rest are in Parts C, D and I (same remark). [The
counts first written here predated B-5; corrected after the referee of 2026-11-17.]
[Addition after the referee of 2026-11-17: the abstract, the README section and the LaTeX header
comment also said that the referee wrote "fresh code throughout". Each now says what the records
show, that its load-bearing checks used code written fresh for the pass and that it re-ran one
audit script of the pipeline, with a dated note. Propagation grep (`fresh code throughout`): 4,
the dated notes of the abstract (both twins) and of the README, and the LaTeX header comment
followed by its note. (`writing fresh code`): 3, the same three dated notes.]

**G-9. "Twelve of them by a second, unrelated one."** The second checker, `ref_lrat.py`, ran on
ten of the 445 ledger certificates, all in the N = 21 layer, and on the two certificates of
Lemma 3.2 (t339 and t248), which are not ledger entries (the referee's record: "10 cubes + t339 +
t248"). §4.2's "in all twelve cases where both checkers ran the same certificate" is correct and
stays. Found by the record check of 2026-11-17 (see G-8). Corrected in §1.2 and §7 of both twins
and in the August sweep record (dated note).
Propagation grep (`twelve of them`): 4 hits, the dated notes. (`twelve re-checked`): 1, the sweep
record, followed by its note.

**G-10. "Unrelated" and "two independent implementations".** Both checkers are ours, written in
the same campaign, in the same language, with the same relaxed hint rule; they share no long
passage (measured for this entry on the private copy of `ref_lrat.py`: the longest run of
identical lines is five physical lines). Their agreement guards against a coding slip and only
weakly against a shared misunderstanding. No count is printed in the note. Corrected in §1.2, §7
and its closing sentence, in both twins.
Propagation grep (`unrelated checker`): 3 Part G hits, the dated note in each twin and the sweep
record (followed by its note); in Part I the dated note in each twin and two lines of its log, a
different claim handled there. (`unrelated one`): 2, dated notes. (`two independent
implementations`): 2 Part G hits, the dated note in each twin; 2 in Part L (`demag-paper`), about
a different pair, not checked here. (`checkers independently`): 2 Part G hits, dated notes; 1 in
Part I, a line of its log.

**G-11. "11 of 11 attempts".** On record are eight regenerations in the referee pass of
2026-08-11 and one more of `s21_587_1` in the fix pass of the same day (this log, spot
regeneration), each byte-identical to the ledger's size and SHA-256: nine attempts on eight
distinct certificates. The two further attempts that "11 of 11" counted have no record. All were
made on one machine with one CaDiCaL build. On 2026-11-17, 17 more proofs were regenerated
byte-identical (`k34-certificates/REGENERATE.md`, "What was tested on 2026-11-17"). Corrected in
the abstract of both twins with a dated note; §6 gains the 2026-11-17 regenerations; dated notes in
this log (spot regeneration and G-3) and in the August sweep record.
Propagation grep (`11 of 11`, `$11$ of $11$`): Part G hits are the dated note in each twin and the
four lines of this log (spot regeneration, G-3), each followed by a note; the three Part B hits
(both twins and the sweep record) count Part B negative controls, as G-3 says. (`eleven of eleven`): 1, the sweep record, followed by
its note.

**G-12. A written deviation from the program's rule for certificates.** The program's own rule for certificates asks that an
UNSAT certificate be checked by an established LRAT checker such as cake_lpr or drat-trim. Part G did not
meet it. In August no established checker ran on any k(3,4) proof: every proof was checked by our
`lrat_check.py` (`s21_587_1` twice), ten of them and the two small certificates also by our second
checker `ref_lrat.py`, and 336 of the 346 N = 21 proofs were then deleted. On 2026-11-17
drat-trim's `lrat-check` (commit 2e3b2dc) accepted 30 distinct ledger certificates: 17
regenerated that day (the set in REGENERATE.md) and 14 of the stored proofs (ten of N = 21 and four of
N = 22; `s21_587_1` is in both), so 17 of N = 21, 4 of N = 22, 8 of N = 23 and 1 of N = 24 (counted
for this entry from the run's per-proof tables). `lrat-check` accepts a proof whose last line
asserts the empty clause with no hints; `lrat_check.py` and `ref_lrat.py` reject it, so
`lrat-check` alone is weak exactly there. X. Zeng reports this behaviour of `lrat-check.c`, found
by the audit of his own proof of k(3,4) = 21, in his paper ([Zen26] in the note; PDF dated
5 September 2026); the record check of 2026-11-17 confirmed it on variants of t339 and t248
whose last line asserts the empty clause with no hints. Credit for the observation: X. Zeng, whose
paper was read in full on 2026-11-17; §7 of both twins cites it (added after the verification and
the referee of 2026-11-17). cake_lpr was not run. Stated in plain words in §3.4
(dated note) and in item 1 of §7, in both twins, and in the README section.
Propagation grep (`two independent implementations`): see G-10. (`independently written checker`):
6 Part G hits outside this log, §1.2, §3.4 and §7 of each twin; 3 in Part D, about its own
checker; in this log C-3, M3 and this entry. In the note the phrase means written separately from
the solving pipeline; §1.2, §3.4 and §7 now also say that the checkers are ours. The abstract keeps "independently written standard-library checker" in the same sense.
(`14 stored proofs`): 0, after the referee of 2026-11-17 (now "14 of the stored proofs", in §7 of
both twins and in this entry).
[Addition, 2026-11-25: "cake_lpr was not run" is a statement of 2026-11-17 about our own runs and
stands as that. An outside check has since run cake_lpr on a proof of each of the 445 formulas. See
G-18 below.]

**G-13. The note said the regeneration inputs are private, and counted 70 representatives.**
Commit 4794560 of 2026-11-17 added to the repository the 70 block files, `witness_bermond8.json`,
`witness_qr7.json`, the queue files `q2.jsonl`, `q3.jsonl`, `q5.jsonl` and `q5b.jsonl` (each
command with the run-directory path and the solver's directory removed) and
`k34-scripts/verify_chain.py`, 77 files, and updated `REGENERATE.md` and the README; that commit
is recorded here for the first time. No release up to v0.17.0 holds these files. The representatives
the generator consumes are 72, not 70. §6 of the note describes the v0.7.0 deposit and keeps its
text, with "70" corrected to 72 and a dated note on the files added since; §7 (the audit's
location and trusted item 4) is updated with dated notes. Found by the regeneration work of
2026-11-17.
Propagation grep (`70 block-class`): 1 hit, G-4 of this log, followed by its note. (`private
regeneration kit`): 5, in each twin §6's description of the v0.7.0 deposit (followed by its dated
note) and the dated note of §7 item 4, and G-4. (`not from the deposit alone`): 0. (`six
scripts`): 2, §6 of each twin, which describes v0.7.0 and is followed by the note on the seventh.
[Added after the referee of 2026-11-17: the reviewers at erdosproblemaday.com pointed out on
2026-11-16 that these inputs were not in the public tree; CORRECTIONS.md credits them.]

**G-14. `verify_chain.py` and `make_structured.py`, docstrings only.** `verify_chain.py` called
itself a "FINAL INDEPENDENT VERIFICATION ORCHESTRATOR"; it is a driver of the same pipeline that
runs `verify_witness.py`, `audit_cnf.py` and `lrat_check.py` by subprocess, and its header now says
so. Its pointer "[4-line argument, see NOTES]" and the pointer of `make_structured.py` to
`NOTES.md`, which is not public, now point to Lemma 3.1 (and 3.2) of the note. The claim that
`audit_cnf.py` has "independently rewritten encoding logic" has no record behind it and now reads
that it rebuilds the expected clause set itself, importing nothing from the generators (true of
its imports). No executable line changed (the code of both files, docstrings set aside, parses to
the same syntax tree as before); the generator's output does not change. Found by the
regeneration work and its check of 2026-11-17.
Propagation grep (`FINAL INDEPENDENT`): 1 hit, the docstring's own note on the old line. (`see
NOTES`, `documented in NOTES.md`): 0. ("points to `NOTES`"): 1 hit,
`k34-certificates/REGENERATE.md`, which described the old header; updated in place with a dated
note.
[Addition after the release gate of 2026-11-17: the docstring of audit_multiset.py made the same claim about audit_cnf.py ("independent logic (fresh encoding rewrite ...)"); it now says what audit_cnf.py does, with a dated note; docstring only. Propagation grep (`independent logic`, `fresh encoding rewrite`, `independently rewritten`): 0 outside dated notes and this log.]

**G-15. §8.1 and Question 8.1: an extremal Cayley digraph exists.** Cay(ℤ₂₀,{2,4,5,7,11,14}) is
{I₃,TT₄}-free on 20 vertices and vertex-transitive (no independent triple among 1,140, no
transitive 4-set among 4,845, every translation an automorphism, automorphism group of order 20;
re-checked for this entry). So the comparison with k(4,3) does not extend to the extremal family,
and the last part of Question 8.1 has the answer yes. Credit: the working report of Erdős Problem
a Day on problem 112 (dated 2026-08-12, initial run 2026-07-26), which exhibits the circulant with a
census of eight cyclic witnesses; Muhamadiev Faridun's repository (22 September 2026), which gives it
as the witness for k(3,4) ≥ 21; the reviewers at erdosproblemaday.com, who pointed it out to us on
2026-11-16; and the 2017 remark (G-7). (The first version of this entry credited the reviewers
only; widened after the referee of 2026-11-17, from our own records of 2026-10-14 and 2026-10-20.) Dated note after the question, in
both twins, with a pointer to Part J, whose §6 carries the matching correction.
Propagation grep (`mirrors the situation at`): 2 hits, §8.1 of each twin, followed by the note.
[Amended after the verification of 2026-11-17: the dated note said that Part J "answers the first
two parts"; Part J answers the first (W is not unique) and bounds the second (at least thirteen
extremal graphs, and with this circulant at least fourteen). Propagation grep (`first two
parts`): 0.]

**G-16. Later work on k(6,3).** T. S. Orden has since reported 30 ≤ k(6,3) ≤ 32 (Zenodo, version 1 of
2026-11-09, version 2 of 2026-11-16); version 2 credits the 29 of Proposition 1.2 to this note. His
record says the proof has not been peer reviewed, and neither his witness nor his proof was checked
for this entry, so the note says "reported", not "shown" (changed after the verification and the
referee of 2026-11-17).
His 29-vertex witness has a trivial automorphism group by his record, so it is not a Cayley
digraph and does not bear on the sweep of §8.2. Dated later-work note in §8.2 of both twins, and
two references added ([Ord26], [MF26]).
Propagation grep (`since shown`): 0.

**G-17. A local path in the k(6,3) referee record.** Line 39 of `REFEREE-k63.md` named the
referee's checker by an elided absolute path of a temporary session folder; that prefix now reads
`[scratch]/` by the rule printed in CORRECTIONS.md. No other byte of that line changed.

**G-18. An outside check of the proofs with cake_lpr (added 2026-11-25).** On 2026-11-18 the
reviewers at erdosproblemaday.com completed a rebuild and check of the whole certificate chain
from commit 4794560 of this repository. Their entry is dated 18 November 2026 and was updated on
19 November with the final counts; the README of their bundle gives its status at 2026-11-19
09:02 UTC. By that record: all 445 formulas regenerate with `make_structured.py` to the ledger's
`cnf_sha256`; an encoder of their own writes the same clause set for each of the 445; each of the
72 block representatives has its defining property, those of one size are pairwise
non-isomorphic, and the counts 25, 31, 7, 1 and 3, 3, 1, 1 equal those of their own enumerations;
for the two formulas of Lemma 3.2, written by `gen_cnf.py`, the clause sets equal their encoder's
and cake_lpr accepted the proofs; each of the 445 formulas was solved again by CaDiCaL 3.0.1 (tag
rel-3.0.1, built from source with gcc 13.3.0 on x86-64 Linux, our recorded options without `-t`),
the proof passing straight to cake_lpr (github.com/tanyongkiam/cake_lpr, commit a36874a), which
accepted all 445, the 346 of N = 21 among them. The record describes cake_lpr as an LRAT checker
with a proof in the HOL4 theorem prover that a formula it reports verified is unsatisfiable, a
proof that does not cover its input and output wrapper, the assembler and linker, or the
operating system. 307 of their proofs equal our ledger lines in SHA-256 and byte count; the other
138 are different proofs of the same formulas, and their record says the difference lies between
the builds or the platforms (three runs of one cube on their machine gave one proof). The split
by layer is not printed there; counted for this entry from its list of the 138 names: 114 of
N = 21 and 24 of N = 22, so 232 of 346, 66 of 90, 8 of 8 and 1 of 1 are equal. Their controls
include a proof ending in an empty clause with no hints, which cake_lpr rejects (compare G-12).
Listed there as not checked: our `lrat_check.py`, the thirteen extremal graphs of Part J, and the
short argument that the 346 cases cover every graph, which is machine-checked neither there nor
here.
The check is theirs. Nothing of it was re-run for this entry; the entry and the README were read
in full on 2026-11-25 (the README as fetched that day has SHA-256
4980fb1014f546dbae9ed5ac10f1c010568b627922a2882aa63141362f2b6b78). G-12 stands as a statement
about our own runs: no established checker ran in August, `lrat-check` accepted 30 ledger
certificates on 2026-11-17, and no run of cake_lpr was made by us. The sentence "cake_lpr has not
been run", which this round wrote into §7 item 1 on 2026-11-17, was out of date from 2026-11-18.
It is replaced, in both twins, by the statement of the outside check, with a dated addition; §3.4
gains a dated addition after its note of 2026-11-17; a reference [EPD26] is added in both twins;
the README section, item 1 of this round's entry in CORRECTIONS.md and the description in
`.zenodo.json` state the same fact shortly; G-12 gains a bracketed note. Credit: the reviewers at
erdosproblemaday.com.
Propagation grep (`cake_lpr has not been run`): 0. (`cake_lpr was not run`): 0; in this log G-12,
followed by its note. (`no established`): 7, the August statement in the README section, in §3.4
and in §7 item 1 of each twin, each now followed by the outside check or by its dated addition,
and the dated note of §7 item 1 in each twin, which describes the text of v0.17.0. (`has not been
run`): 1, a comment in `kelmans-paper/note.tex` about a recount queue of Part I, a different
claim.
[Addition of the same day, second pass: the abstract of both twins said without a qualifier that certificates regenerate bit-for-bit from the recorded solver commands. Each twin gains a dated addition: the statement is about our environment, and in the outside check 307 of the 445 proofs equal the ledger's in SHA-256 and size while 138 are different proofs of the same formulas. Propagation grep (`regenerate bit-for-bit`): 2, the abstract of each twin, each now followed by its dated addition.]
[Addition of the same day, third pass: the reviewers' per-case files were then read and compared
with the ledger. All 30 files of the folder `112/kirtchakov-certificates-cake-lpr` of
github.com/pw/erdosproblemaday-verification were fetched through the GitHub API at commit b6c61c8
(the folder last changed on 2026-11-19 at 09:04 UTC). Its `results/results.jsonl` (SHA-256
61c81f8645b5f83fba86ddf33602c3c88d882d67ad28e331738edd31e2ad08f7) has one line for each of the 445
names of `CERTLOG.txt`, none missing and none extra. Compared line by line: the formula digest
equals `cnf_sha256` on all 445 (346, 90, 8 and 1 at N = 21, 22, 23 and 24); the proof's digest and
byte count equal `lrat_sha256` and `lrat_bytes` on 307 (232, 66, 8 and 1) and differ on 138 (114
and 24 at N = 21 and 22; eight of the 138 have the ledger's byte count and a different digest);
the recorded output of cake_lpr is `s VERIFIED UNSAT` on all 445, with CaDiCaL's exit code 20. The
138 names in their README are exactly the 138 that differ. So the counts 445, 307 and 138 of this
entry, and its split by layer, also follow from their per-case data. This was a comparison of
records: no solver and no checker was run for it, and no run of cake_lpr was made by us.]

Not taken in this round: depositing the two small certificates `validation/t339.*` and
`validation/t248.*` of Lemma 3.2 (they regenerate byte-identical from `gen_cnf.py` and CaDiCaL,
REGENERATE.md prints the commands); this is a release decision. §1.2 and the README keep "Every
component was confirmed by an adversarial referee": true at the level of components; for the
proofs, §4.2 states the sample of ten.
