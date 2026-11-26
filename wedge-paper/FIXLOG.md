# FIXLOG — note-wedge fix pass (2026-08-11)

Target: `note.tex` and `note.md` (faithful twins) and the lab record
(`wedge/NOTES.md`, `wedge/STATE.md`) that feeds them. Three review reports
(LENS 1 CLAIMS-vs-artifacts, LENS 2 REPLAY audit, LENS 3 NOVELTY/priority).
Every finding was re-settled against the shipped artifacts before any edit;
where a reviewer and NOTES disagreed, the artifact decides and the winner is
recorded. **No claim was strengthened by this pass; every change weakens,
scopes, or corrects.**

Independent re-verification done in this pass (system `python3` 3.9.6, checkers
under `env -i`): both d=3 certificates `CHECK PASS`; both d=5 WMAX=5
certificates `CHECK PASS` from the artifact location; `C(77,7)`, `C(77,8)`,
every MC ratio, and `E[W]=Sum p_i` for all four points recomputed from scratch.

---

## MUST-FIX

None. All three lenses returned **no MUST-level defect**: both stdlib checkers
replay `CHECK PASS` under system Python, every certified number matches the
artifacts, tamper controls are rejected nonzero, the two-sided bracket is
rigorous, and the IP boundary holds (grep of `artifact/` for engine/generator
tokens returned zero).

## SHOULD-FIX

| # | Finding (lens) | Verdict vs artifacts | Action |
|---|---|---|---|
| S1 | "Above threshold" at p=1e-2 is contradicted by the certificates' own numbers (L1) | **Reviewer right.** `P_L(d5,1e-2) in [1.61e-2,1.94e-2]` (kill_condition_eval_d5.json) `< P_L(d3,1e-2)~2.716e-2` (kill_condition_eval.json): the logical rate still FALLS with distance — the below-threshold signature. The loose bracket is driven by the truncation tail (E[W]=1.456 over 77 mechanisms), not a threshold crossing. | NOTES kill-condition block and STATE reworded from "above threshold" to "tail-dominated regime"; the note (§4) frames the DEAD verdict by E[W]/tail weight and never asserts "above threshold". |
| S2 | The "MC wins above threshold" story does not hold at d=3 (L1) | **Reviewer right.** `kill_condition_eval.json` records p=1/100 at d=3 as **LIVE**, bracket 2.33x narrower (I recompute 8.658576e-5 / 2.0148292055e-4 = 0.4297 → 2.33x). MC-overtakes is a d=5-only crossover. | NOTES adds the explicit d=3-LIVE-at-p=1e-2 contrast; the note (§4) reports both verdicts and scopes the MC-wins crossover to d=5 (large mechanism count). The one-sentence public claim is scoped accordingly. |
| S3 | "Certified" bounds the DEM, not the physical circuit; at d=5 sub-threshold the circuit MC drifts just outside the bracket (L1) | **Reviewer right.** `mc_d5_p1over1000.json` circuit p_hat=2.81e-5 sits ~1.17 sigma above U=2.6145e-5 (statistically consistent). The certificate's own `model.semantics` already discloses the DEM approximation. | NOTES adds a "Scope caveat (DEM vs physical circuit)"; the note (§5) states plainly the bracket bounds Stim's independent-mechanism DEM, not the true depolarizing circuit, and that "circuit-level" names the DEM's origin, not a bound on the physical circuit. |
| S4 | Trust root is the mechanism list, and only the mechanism list (L2) | **Reviewer right.** The checker re-derives L,T,U from the embedded `(det,obs,p_num/p_den)` list but cannot re-verify that list equals Stim's DEM — that binding is in the private generator. | NOTES adds a one-line "Trust root"; the note (§5, the single certification paragraph) states the bracket is conditional on the embedded mechanism list, the one link a stranger cannot re-check from the public artifact. README Part H repeats it. |
| S5 | WMAX=6 re-verification wall time understated (L2) | **Reviewer right.** On a stock laptop the WMAX=6 checker exceeded the 600 s foreground budget (completed CHECK PASS in the background). "A few minutes" is too optimistic. | NOTES and STATE reworded to "order ten-plus minutes (exceeded the 600 s foreground budget)". The note (§6) states the same. (WMAX=5 at ~34 s is accurate and unchanged.) |
| S6 | Novelty: 2605.03054 and 2305.01301 are NOT "code-capacity only" (L3) | **Reviewer right.** 2605.03054's abstract analyses measurement errors / a locally-correlated model; 2305.01301 extends to noisy syndrome-extraction circuits. The true differentiator is analytic (weight-enumerator / closed-form) vs. a machine-checkable certificate. | NOTES novelty block re-stated: both are analytic with no machine-checkable certificate; 2305.01301 flagged as the nearest conceptual competitor. The note (§3) draws the distinction as certificate vs. analytic bound. |
| S7 | Novelty: "MaxSAT" label imprecise (L3) | **Reviewer right.** Veri-QEC uses SMT; Lean-QEC a verified SAT reduction; neither is MaxSAT. | NOTES drops "MaxSAT"; the note (§3) describes both as machine-checked distance / correction-condition verifiers, a different object from a P_L bracket. |

## NITs

| # | Finding (lens) | Verdict | Action |
|---|---|---|---|
| N1 | `C(77,7)` misstated twice as 2.28e9; `C(77,8)` as 2.0e10 (L1) | **Reviewer right.** `C(77,7)=2,404,808,340 (~2.40e9)`, `C(77,8)=21,042,072,975 (~2.10e10)`, recomputed. Affects no certified quantity; makes the wall marginally harder. | NOTES lines corrected (both occurrences); derived w=7 enumeration time 24→26 min. The note (§6) uses the correct C(77,7). |
| N2 | Decoder is minimum-*cardinality*, not minimum-likelihood / ML / MWPM (L1) | **Reviewer right.** BFS ranks fault sets by mechanism count, ignoring the differing p_i. The bracket is valid for THIS lookup-table decoder only. | The note (§2) states plainly the decoder is the minimum-cardinality coset-leader lookup table (Tomita–Svore), not the ML/MWPM decoder, and does not bound the optimal-decoder rate. |
| N3 | w6 certificate not fully replayed by L1 | **Resolved by L2**, which replayed `certificate_d5_r1_p1over1000_w6.json` end to end to CHECK PASS (>10 min). Kept as an optional, tighter WMAX=6 point; not part of the released WMAX=5 core. | The note (§6) presents WMAX=6 as the optional tighter run and states its checker cost honestly. |

## Corrections to the reviewers

- None material. L2's note that the d=5 unseen-syndrome guard is reached only in
  narrow constructed cases (the WMAX-underscoping tamper trips the distance
  guard first) is accepted as a defense-in-depth observation, not a defect; no
  change.
- L2's suggestion that `kill_condition_eval*.json` may not belong in the public
  set is honoured in the staging: the shipped public unit
  (`wedge-certificates/`) is **certificate JSON + stdlib checker only**. The
  kill-eval JSONs are results-only prose+numbers and are NOT staged into the
  certificate directory; their content is reported in the note instead.

## Build

`/opt/homebrew/bin/tectonic note.tex` — see the note's compile line below /
Part H staging record. Page count target 6–9pp.

## Spot-replay (staged location)

Both shipped d=5 WMAX=5 certificates and both d=3 certificates were re-checked
by the shipped stdlib checkers **from the staged `wedge-certificates/`
directory** after staging; all `CHECK PASS` (recorded in the SWEEP-RECORD and
the return summary).

## Post-release correction pass, 2026-08-12

One claim-level correction landed in the note after release (W-2); recorded here because the
Engine 2 referee found this log untouched while the paper had changed. W-1 records a defect
this round introduced and closed before release.

**W-1. Round-internal: the d = 3 uncorrectable-set count was written unqualified, and was
scoped before release.** Correcting W-2 required a new paragraph contrasting the two checkers.
As first drafted in this round, that paragraph gave the d = 3 count as "the uncorrectable sets
number 4823" with no weight bound. 4823 is the count of uncorrectable fault sets of weight at
most WMAX = 4 (55 + 690 + 4078 from `certificate_d3_r1_p1over100.json`); the total is
2^22 = 4,194,304, per Part K's certificate for the same object. The Engine 2 referee caught the
unqualified form and it was scoped in both twins before release.

No released note ever carried the unqualified form. `4823` appears in no Part H note at any tag
v0.8.0 through v0.13.0 — not in `.tex`, not in `.md`, not in extracted PDF text — under any of
the renderings `4823`, `4{,}823`, `4,823`, `4 823`, and not in the superseded `drafts/` tree.
An earlier version of this entry, written 2026-08-12, described this as a post-release
correction of released text. That was false. Corrected 2026-08-13.

Propagation grep (`4823`): 3 prose sites — this log, `note.tex`, `note.md`; both twins scoped,
the PDF rebuilt and verified by text extraction. The 23 further tracked files matching `4823`
are certificate, CNF and LRAT data in which it occurs as an incidental digit substring, not as
a claim.

**W-2. The checker descriptions (ii)-(iii) were stated as if uniform across distances.** They
describe `check_wedge_d5.py`; `check_wedge.py` at d = 3 runs a full untruncated BFS over all 256
syndromes and compares against an embedded decoder table. Corrected in both twins.
Propagation grep (`depth-truncated`, `WMAX`): checked across note twins and README; no further
site asserts uniformity.


## 2026-08-14 — independence-claim round (Part H, v0.15.0)

The front-matter "shares no code with the enumeration engine" was replaced by a
measured disclosure: 58 of `check_wedge.py`'s 141 executable lines appear in the
private engine and `151-166 == 124-139` is byte-identical, the tail dynamic program
among them; the d=5 checker shares 77 of 143. The tail backstop at all five
certificates and the whole-bracket backstop at d=3, established 2026-08-14, are
stated, as is the limit that L at d=5 is not backstopped. The tamper-control layer
is shown by enumeration to share no text with either engine. No certified value
changed.

## Correction round, 2026-11-17

**W-3. The note framed its own operating points as beyond direct Monte Carlo.** Mullan,
Weippert and Brown say the deep sub-threshold regime is not amenable to direct Monte Carlo
simulation; that statement is theirs and stays theirs, quoted as such in §1. But at this note's
operating points the pre-registered `10^7`-shot run of Table 2 resolves `P_L`: at d = 5,
p = 10^-3 its 95% interval is about 626 times the bracket width 9.93e-9, so about 6.2e-6 wide on
a value of 2.61e-5, about 12 percent either side (about 3.4 percent at d = 3). What the
certificate adds there is exactness and an interval about 626 times narrower. The 12 percent is
derived from the note's own Table 2 ratio; the binomial 95% half-width at 10^7 shots, 1.96
sqrt(P(1-P)/N) with P = 2.614e-5, gives 12.1 percent and a width ratio of 638, consistent with
the recorded 626 (the run record itself is not in this repository). Found by our own reading
of 2026-11-17. Corrected in the abstract (dated note), §1 ("defeats", "blocks"), §4 (the
sentence "it is exactly the regime [MWB] call inaccessible to sampling" goes) and the
acknowledgments, in both twins; the README section (added sentence); the August sweep record
(dated note). Part K carries the matching correction (its FIXLOG, K-5). No certified value
changed.
Propagation grep (`inaccessible`): Part H hits are §1's attributed quotation of [MWB], the
README's attributed sentence, the sweep record (followed by its note) and the dated notes.
(`defeats`): Part H and K hits are the dated notes, one in each twin of each part (Part K's
attributed credit sentence says "defeat"); Part L's use is about a different matter. (`exactly the regime`): 2, the dated notes.
[Amended after the referee of 2026-11-17: the dated notes now say that Mullan, Weippert and Brown's
statement concerns the low error rates needed for utility-scale computation (their abstract) and
that this note's operating points are not in that regime, instead of "kept here as theirs".
Propagation grep (`kept here as theirs`): 0.]
[Addition after the release gate of 2026-11-17: the acknowledgments, corrected in this round, carried no dated note; each twin now has one. Propagation grep (`The question this note answers`): 0 outside the dated notes.]

**W-4. The reference to the Lean-QEC paper gave wrong initials and a wrong title.** The entry
[LeanQEC] read "K. Ehatamm, S. Lee, Y. Wu and R. Tao, *Lean-QEC: machine-checked quantum
error-correcting code distances via a verified SAT reduction*". arXiv:2605.16523 is M. Ehatamm,
Y. Lee, X. Wu and R. Tao, *End-to-End Formalization of Quantum Error Correction* (arXiv listing
and the repository's CITATION.bib, read 2026-11-17); Part N cites it correctly. Corrected with a
dated note in both twins. Found by the referee of the 2026-11-17 round. Part K carries the same
correction (K-6).
Propagation grep (`K. Ehatamm`, `K.~Ehatamm`): 0 outside this log. (`verified SAT reduction`): 3,
§3 of each twin, which describes Lean-QEC's method in those words (Part B describes it the same
way, a SAT encoding whose refutation is replayed in the Lean kernel), and the August sweep record;
in this log, S7 and this entry. (Re-measured by the fix session of 2026-11-17; the first version
of this line said the hits were the dated notes.)
