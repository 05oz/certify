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

## Post-review addendum (2026-08-11)
The flagged verification asymmetry on k(6,3) >= 29 is resolved: a dedicated adversarial referee
(fresh code, raw definitions, no reuse of the shipped TT_3 criterion) CONFIRMED the claim —
alpha = 5 by exhaustive scan of all 376,740 six-subsets; 0 transitive triples; the object
verified arc-for-arc as Cay(Z_28,{3,8,10,12,17}); novelty supported (strongest prior lower
bound was the trivial 18). Full verdict: REFEREE-k63.md. The model-credit footnote was
corrected from "Claude Fable 5" to "Claude (Anthropic)" — the work spanned multiple Claude
models and a single-model claim was inaccurate.

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
