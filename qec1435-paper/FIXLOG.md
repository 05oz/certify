# FIXLOG — note-1435-automorphisms, fix pass of 2026-08-05

All fixes applied to BOTH `note.tex` and `note.md`; `note.pdf` rebuilt with tectonic.
Disputed facts were settled against the primary record (`solve/problem-3/NOTES.md`,
`RESULTS-1435.md`, `certificates/`) and by read-only replay (verify_1435.py on both
reference matrices, walk2_s202.out tail, qc7_xcheck.out, order7fixed_full.txt,
anneal2_s44.out, table-column sum). No new solver campaigns; artifacts untouched.

## CLAIM-LEVEL DOWNGRADES (read these first)

1. **Independent-verifier scope SHRUNK.** The note claimed agreement "on both
   reference codes"; the verifier structurally cannot read the 12-generator
   [[14,2,5]] file (replayed: `FAIL: expected 11 generators, got 12`). Now claims
   agreement only on the [[14,3,4]] control plus 8 enumerated CYCLIC candidates,
   and discloses the sample's console output was not archived. (L1-M1/M2/S5, L3-1/6)
2. **"Exact distance of every candidate" DOWNGRADED to early-abort certification.**
   The pipeline certifies d ≤ 4 by an exhibited weight-≤4 vector and would compute
   exact distance only for survivors (there were none). Abstract, §3 intro, and the
   Table 1 caption all restated. (L3-2)
3. **Artifact-completeness claim SHRUNK.** "Every run output in certificates/" is
   false: the hyperplane sweeps, truncation sweep, positive control, and verifier
   sample have no archived console outputs, and the empty c13 class has no file.
   §7 now discloses each gap instead of claiming completeness. (L1-S3, L3-3/5/6/10)
4. **Adversarial re-verification scope NARROWED** from "negative constructive sweeps
   of §6" to "hyperplane and truncation sweeps of §6" — the walk/anneal campaigns
   were not re-verified. (L1-S2)
5. **Table history claim SOFTENED.** "Bounds 4/5 since June 2005" is not supported:
   only the lower-bound construction is dated 2005; nothing dates the upper bound.
   Abstract, §1.1, and Acknowledgments ("twenty years") all restated as dated
   retrieval facts. (L1-S1, L2-F2)
6. **Proposition 3.2 and its §1.2 echo NARROWED to MONOMIAL automorphisms** of
   order 13 — the proof covers only the monomial normal form. (L1-M4)
7. **PRIORITY REPAIR: [BFMP11] was a chimera** — cited title belongs to a different
   paper (JCTA 2010), the IEEE 57(7) coordinates belong to the [[13,5,4]] paper
   whose second author is R. Fears (not G. Faina), and arXiv:0908.1348 has three
   authors. Reference and §1.1 prose corrected to Bierbrauer–Fears–Marcugini–
   Pambianco, "The nonexistence of a [[13,5,4]]-quantum stabilizer code". Note:
   the raw record NOTES.md carries the same Faina error — the error originated
   there; the reviewer is right and the record file is left as-is (it is a record).
   (L2-F1)

## MUST-FIX items — verdicts and actions

| Finding | Verdict | Action |
|---|---|---|
| L1-M1 / L3-1 (verifier never read [[14,2,5]]) | Reviewer right (replayed; NOTES.md agrees; RESULTS-1435.md "two reference codes" was itself wrong) | §5 restated; downgrade 1 |
| L1-M2 (shipped replay command errors) | Reviewer right (replayed, exit 1) | §7 command now `verify_1435.py data/ct_14_3_stab.txt # control: d=4, "FAIL" by design` |
| L1-M3 / L3-4 (caption 1,315,483 vs column sum 1,314,223) | Reviewer right (summed: 1,314,223 distinct; +1,260 swapshift re-run = 1,315,483 checks) | Caption now gives both numbers with the re-run explained |
| L1-M4 ("monomial" dropped in Prop 3.2 + intro) | Reviewer right (proof assumes monomial normal form) | "monomial" inserted both places; proof now invokes Lemma 2.1/normal form explicitly |
| L2-F1 ([BFMP11] chimera, wrong author) | Reviewer right (dblp/arXiv) | Downgrade 7; header comment also corrected |

## SHOULD-FIX items — verdicts and actions

| Finding | Verdict | Action |
|---|---|---|
| L1-S1 / L2-F2 ("since June 2005") | Reviewer right (record dates only the lb construction) | Downgrade 5 |
| L1-S2 (§6 re-verification scope) | Reviewer right (RESULTS.md lists hyperplanes/truncations, not walks) | Downgrade 4 |
| L1-S3 / L3-5 ("every run output") | Reviewer right (certificates/ listing checked) | Downgrade 3; softened + disclosed, did NOT regenerate artifacts (corpus frozen) |
| L1-S4 / L3-8 ("branch NOT closed" surprise) | Reviewer right (replayed tail of order7fixed_full.txt) | §7 sentence: second script section is a superseded d0=5 attack; branch closed by Lemma C |
| L1-S5 (sample was cyclic-only) | Reviewer right (NOTES.md) | "8 enumerated cyclic candidates" |
| L2-F3 ([CV25] missing title) | Reviewer right | Title "Small binary stabilizer subsystem codes" added, subsystem scope noted |
| L2-F4 ([BCH20] published version) | Reviewer right | AIHPD 10 (2023), 337 added; "Problem 1 in both versions" |
| L2-F5 ([72,36,16] precedent unnamed) | Reviewer right | One sentence added in §1.3 naming Conway–Pless 1982 and the 1/3/5 endpoint (Borello); pointed to [Huf98] rather than adding new unverified bibliography coordinates |
| L2-F6 (Hao 2021 unacknowledged) | Reviewer right (sweep statement stays literally true) | One sentence in §1.1 + [Hao21] reference added |
| L3-2 (early-abort vs exact scan) | Reviewer right (check1435.c header confirms) | Downgrade 2 |
| L3-3 (positive control mechanism) | Reviewer right (NOTES.md: "hit at s=12"; injection into batch-11 stream impossible) | §3.1 states the real mechanism (separate `batch 12` run), discloses unarchived log; did not fabricate an archived log |
| L3-6 (no artifact for 8-sample) | Reviewer right | Disclosed in §5 |

## NITs — applied or skipped

- L1-N1 / walk2_s202: APPLIED — "runner died early (step ≈48,000)" replaces "machine fault" (replayed: last line step 48007).
- L1-N2 anneal floor: APPLIED — "a single residual weight-4 vector at best (restarts typically stall at 1–4)" per NOTES.md.
- L1-N3 coverage-0 wording: APPLIED — "would yield a candidate, which an exact re-check would then settle".
- L1-N4 qc7 cross-check: APPLIED — generic tool "independently reproduces that count", count-only run disclosed (qc7_xcheck.out checked: submodule statistics only).
- L1-N5 abstract "closure certificates replay with stock Python": APPLIED — abstract now says "the LP and branch certificates"; §7's careful definition unchanged.
- L2-F7 Koh26 "(Section 1)" pointer: APPLIED — pointer dropped; "CSS-only" fact stands (verified in the record).
- L2-F8 [14,6]_2 phantom pointer in [Gra]: APPLIED — [14,6]_2 dropped from the bibliography (Remark 6.2 uses only [14,7]_2).
- L3-7 (SyntaxWarning + home path inside order7fixed_full.txt): SKIPPED in the note — fixing requires regenerating a frozen, hashed artifact; left as a repo-side follow-up before arXiv (regenerate file AND update both hash lists together).
- L3-9 (batch exits 0 on bad>0): APPLIED — §7 states acceptance is by the SUMMARY line, not exit status.
- L3-10 (sample_c7fixed.py ships unlisted): APPLIED — §7 labels it as the disclosed defective sampler, unhashed, nothing depends on it.

## Where the draft was right / reviewer-vs-reviewer

- RESULTS-1435.md itself contains the "two reference codes" and "Faina" errors the
  note inherited; the deeper record (NOTES.md raw results + replay) was the arbiter
  both times. The note is now aligned with NOTES.md, not RESULTS-1435.md, on those
  two points.
- No reviewer finding was rejected; every disputed fact settled on the reviewers'
  side after replay/record checks. No claim was strengthened anywhere in this pass.
