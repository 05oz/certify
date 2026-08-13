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

Two claim-level corrections landed in the note after release; recorded here because the
Engine 2 referee found this log untouched while the paper had changed.

**W-1. The d = 3 uncorrectable-set count was unqualified.** The note read "the uncorrectable
sets number 4823". 4823 is the count of uncorrectable fault sets of weight at most WMAX = 4
(55 + 690 + 4078 from `certificate_d3_r1_p1over100.json`); the total is 2^22 = 4,194,304, per
Part K's certificate for the same object. Corrected in both twins to name the weight bound.
Propagation grep (`4823`): 3 hits — note.tex, note.md, note.pdf; all three now scoped, the PDF
rebuilt and verified by text extraction.

**W-2. The checker descriptions (ii)-(iii) were stated as if uniform across distances.** They
describe `check_wedge_d5.py`; `check_wedge.py` at d = 3 runs a full untruncated BFS over all 256
syndromes and compares against an embedded decoder table. Corrected in both twins.
Propagation grep (`depth-truncated`, `WMAX`): checked across note twins and README; no further
site asserts uniformity.
