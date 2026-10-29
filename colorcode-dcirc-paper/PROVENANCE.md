# PROVENANCE — colour-code circuit distances (Kishony–Fowler circuit)

This file is the dated record behind the note's credit paragraph. Dates of other people's work
are public timestamps that they control. Dates of our own work are internal build-log times.
The external timestamp of everything we claim begins only at the public release of this
directory.

## Timeline

| Date (2026) | Event | Who | Evidence |
|---|---|---|---|
| Mar 5 | The extended code and the theorem "Circuit distance bounds" (d_ext ≤ d_circ for single-auxiliary CNOT circuits, with equality for non-interleaved ones) | Strikis, Browne, Beverland | arXiv:2603.05481v1. v2 of Sep 14 leaves the theorem statement unchanged. |
| Mar 30 | The single-auxiliary colour-code circuit, its schedules, the argument that the boundary distance is "asymptotically reduced by a factor of 5/6", and the sentence "we verify numerically that, up to d=13, the circuit-level distance is given by d_circ = d − ⌊(d+3)/6⌋". That sentence states the formula, and so the value 11, at d = 13. No per-d values, method, round count or noise model are given for it. | Kishony, Fowler | arXiv:2603.28852v1, main.tex:199–201 (still v1 only on Oct 27); companion code at Classiq/classiq-library |
| Sep 1 | **Our computation (unreleased).** Two-sided certificates at d = 3, …, 13 by three routes, a standard-library checker, a referee pass, and a novelty sweep. Nothing was made public. | this program | build logs `colorcode-dcirc-certificates/logs/2026-09-01/` |
| Oct 4 | **Earliest independent values for this circuit found in the sources read (as of Oct 29).** Exact branch-and-bound values: rounds = d at d = 3, 5, 7, 9; one round at d = 5, 7, 9, 11. Also the corner bound d_circ ≤ d − 1 for every single-auxiliary schedule, and DRAT-checked upper bounds over schedule spaces. | github.com/dylanneve1/qsim-lab | research/qec/qec-r4.md §2.3; research/theory/theory-colour.md; commits of Oct 4–5 |
| Oct 7 | **Our d = 15 computation (unreleased).** The extended-code refutation at K = 11 took 15,724 s. drat-trim `lrat-check` reported VERIFIED at 10:26 ET, and `check_dcirc.py` reported "OK lower bound … >= 12" at 17:53 ET. A same-day novelty sweep followed. | this program | `colorcode-dcirc-certificates/logs/2026-10-07/` |
| Oct 15 | A DRAT-checked circuit distance for IBM's depth-8 syndrome cycle of the [[72,12,6]] bivariate-bicycle code (= 6); for the larger codes, values whose DRAT-checked steps rest in part on enumerators. Also the projection check of every fault's key against the extended code, the device our Hypothesis B uses. | M. Kornstein | doi:10.5281/zenodo.23394575, depth8_cycle/DERIVATION.md:161–165, :222, :229 |
| Oct 13 / Oct 20 | Release v1.0 (a period-18 circuit): gross-code circuit-distance argument with DRAT-checked lift steps. In v1.0 its d_ext and logical lists rest on searches. Superseded by v2.0 (Oct 24). | G. Pan | github.com/GavinNull/gross-code-distance-12, release v1.0 |
| Oct 20 | Recency re-sweep. This directory staged: direct d-round witnesses at d = 11, 13, 15 lifted from the extended-code witnesses, a standard-library check of Hypotheses A and B on every object, and the checker re-run on the staged copies. | this program | `SWEEP-RECORD-COLORCODE-DCIRC-2026-10-20.md`; `colorcode-dcirc-certificates/VERIFY.log` |
| Oct 23 | Junction hook errors in the authors' schedule. On every non-corner plaquette, bulk included, a weight-2 hook error and d − 2 data errors form an undetected logical error of d − 1 faults, checked at d = 7, 9 and 11 in the authors' circuits (upper bounds); a counterexample to the authors' statement that, away from the corners, no single hook error alone reduces the distance. Integer-program values 6 at d = 7 and 8 at d = 9 when only the bulk CNOTs and the data qubits are noisy. No value at d = 13 or 15; no proof object. | S. Issa, M. Martonosi | arXiv:2610.33347v1 (submitted Oct 23, announced Oct 27), main.tex:31–32, :88–89, :203–209, :242–247, :265–268 |
| Oct 24 | Release v2.0: circuits of period 11 with circuit distance 12 (gross code) and 10 ([[90,8,10]]), every solver decision backed by a checked certificate: VeriPB for the extended-code distances and the completeness of the logical lists, DRAT checked by drat-trim and `cake_lpr` for the lifts. | G. Pan | github.com/GavinNull/gross-code-distance-12, release v2.0 notes; paper/draft.tex:262–267 |
| Oct 25 | Schedule C9, another single-auxiliary schedule of the authors' family: circuit distance 8 = d − 1 at d = 9 in Crocker's construction, Z and X memory. The extended-code step of the lower bound (d_ext ≥ 8) has a DRAT proof (kissat; drat-trim), regenerated from the shipped CNF and deleted after the check; the circuit step is a Stim-based single-fault check at 1–5, 9 and 25 rounds plus a hand lemma for every round count in a companion note that is not in the record. For the authors' colour rule: extended-code distances 2, 4, 6, 7 at d = 3, 5, 7, 9 by exhaustive search, and circuit distance 7 at d = 9 for one and three rounds, with no proof object. Nothing for d ≥ 11. | C. Crocker | doi:10.5281/zenodo.23633600 (v1.0), colour_c9_pack/README.md:5–22, colour_c9_pack/check_full.py:16–17, :179–196, colour_c9_pack/check_kf.py:8–15 |
| Oct 25 | Experiment E-037: VeriPB-checked lower bounds of 10 for IBM's depth-8 gross-code cycle, for every number of rounds up to 12, in both bases, in two fault models; the certificates are regenerable from the public code and are not in the repository. | G. Pan | research/journal/2026-10-25-E-037-ibm-cert.md:1–11 (commit 1f9757458f); paper/draft.tex:62–65, :899–905 |
| Oct 27–28 | Recency re-check of this record: the Crocker record of Oct 25 read in full; the third "not found" item replaced by a narrower one; credits for Issa–Martonosi, Crocker and Pan added. | this program | `SWEEP-RECORD-COLORCODE-DCIRC-2026-10-20.md` §7; `colorcode-dcirc-paper/FIXLOG.md`, round 7 |
| Oct 28–29 | Recency re-check of this record: the arXiv quant-ph mailing of Oct 28 read (submissions received before about Oct 27, 18:00 UTC); no mailing was issued on the evening of Oct 28 (arXiv's scheduled maintenance); the submissions received from 14:00 EDT on Oct 27 to 14:00 EDT on Oct 29, announced on Oct 29 at 20:00 EDT, are not covered (arXiv's status page; `SWEEP-RECORD-COLORCODE-DCIRC-2026-10-20.md` §7.8); the Zenodo records, repositories and repository searches of the re-check list, the Kishony–Fowler authors' repositories and the Error Correction Zoo colour pages checked after Oct 29, 00:00 UTC. Nothing found bears on this record's statements, and its as-of date moves to Oct 29. | this program | `SWEEP-RECORD-COLORCODE-DCIRC-2026-10-20.md` §7.8; `colorcode-dcirc-paper/FIXLOG.md`, round 8 |

## Consequences for credit

**Values at d ≤ 11.**
- Our certificates for these values predate qsim-lab's posting, but they were not public.
- The earliest independent values found in the sources read, as of 2026-10-29, are therefore
  qsim-lab's, and the note credits them as such. Our contribution at those points is the
  checkable proof, not the number.
- Two later results on the same CNOT schedule are credited as independent: Crocker's values for
  the authors' colour rule (Oct 25) and Issa–Martonosi's d − 1 upper bounds at d = 7, 9, 11
  (Oct 23). Neither ships a proof object for a lower bound on this schedule.
- A text search of a local copy of the files our program added on its public branch of
  2026-09-26 to 10-14 finds no colour-code term (colour code, color code, Kishony, Fowler, 6.6.6,
  plaquette: 0 hits).

**d = 13.** The authors' own statement is the one earlier statement found: their formula holds
numerically up to d = 13 (main.tex:201), which gives 11 there, with no per-d values, round count
or method. Our value agrees with it. An independent computation of that value, or a proof of it,
was not found in the sources read, as of 2026-10-29; this package gives both.

**d = 15.** No value appears in any source read as of 2026-10-29.

**Checkable proofs.** Crocker's record of Oct 25 has a DRAT proof for the extended-code step of a
lower bound for another schedule of the same family (C9, d = 9), so a checkable proof inside a
colour-code circuit-distance lower bound is not ours in general. Not found in the sources read,
as of 2026-10-29: a checkable proof (an LRAT, DRAT or formal proof object) of a lower bound on the
circuit distance of any circuit with the authors' schedule, at any d, or of any colour-code
syndrome-extraction circuit at d ≥ 11. The nearest items found are Crocker's record above and the
bundle of Shutty's arXiv:2609.21376 (doi:10.5281/zenodo.22820614, `distance/README.md`), which
ships a re-runnable, Stim-based exhaustive check of that paper's small-instance lower bounds for a
different circuit; that check is a search that trusts Stim, not a proof object.
