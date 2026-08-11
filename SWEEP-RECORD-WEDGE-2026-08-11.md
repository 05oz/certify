# Dated novelty and verification sweep — certified sub-threshold logical error brackets (Part H)

All searches run 2026-08-11 (arXiv + web, 24-month window). Three-lens
adversarial review the same day. This record is the priority-and-replay
provenance for the wedge note; the decision log is `wedge-paper/FIXLOG.md`.

## Primary source (the market gap), confirmed verbatim

* **arXiv:2607.27153**, Mullan, Weippert, Brown (Northrop Grumman), *Improved
  Methods for Determining Quantum Error Correcting Code Performance and Fault
  Tolerance*, submitted 29 Jul 2026 — CONFIRMED real; resolves at
  arxiv.org/abs/2607.27153. Gap passage quoted verbatim in the note:
  performance "is not amenable to direct Monte Carlo simulation". Their answer
  is a sampler (a "pruning algorithm" plus "subregion MCMC" Metropolis–Hastings
  family), not a certificate; the Bravyi–Vargo antecedent is arXiv:1308.6270.
  This supports the note's framing exactly: the sub-threshold regime is named
  Monte-Carlo-inaccessible and answered with an estimator, not a re-verifiable
  bracket.

## Nearest neighbours — none produces the certified object

* **arXiv:2605.03054** (Regev, Dilley, Nutaro, Delgado, Bennink): closed-form
  LER approximations; analytic, includes measurement errors / a
  locally-correlated model; no machine-checkable certificate.
* **arXiv:2305.01301 / Quantum 9, 1950 (2025)** (Forlivesi, Valentini, Chiani):
  MacWilliams weight enumerators; analytic bounds/asymptotics extending to
  noisy syndrome-extraction circuits; undetectable-error enumerators, NOT a
  certified two-sided P_L bracket. Nearest conceptual competitor.
* **Lean-QEC arXiv:2605.16523** (verified SAT reduction) and **Veri-QEC,
  arXiv:2504.07732 = ACM 10.1145/3729293** (SMT): machine-checked code
  DISTANCE / correction-condition certificates, not logical-error-probability
  brackets.

The intersection the note occupies — exact integer uncorrectable-set counts
A_w by weight AND a two-sided exact-rational P_L bracket under a stated decoder
at circuit-level noise AND independent stdlib re-verification — is unoccupied.
**Verdict: PRIORITY-CLEAN.** Two novelty wording corrections required by the
sweep (2605.03054 / 2305.01301 are not "code-capacity only"; drop the "MaxSAT"
label for the two verifiers) were applied to NOTES.md and reflected in the note
(§3); see FIXLOG S6, S7.

## Verification summary

* Both d=3 certificates and both d=5 WMAX=5 certificates: `CHECK PASS` under
  system `python3` 3.9.6, stdlib only, replayed from the staged
  `wedge-certificates/` directory (2026-08-11). The d=5 WMAX=6 certificate:
  `CHECK PASS` (heavy, order ten-plus minutes; exceeds a 600 s foreground
  budget on a stock laptop).
* Independent re-derivation (separate code from the shipped checker) reproduced
  the d=3 counts A_1..A_3 = {0,55,690} and the truncation-equivalence; the
  Poisson-binomial tail T matched string-for-string at the d=5 points; every
  Monte Carlo ratio (18,500×, 626×, 20.5×, 2.33×) and E[W] recomputed from
  scratch. Seven tamper controls rejected nonzero.
* IP boundary: grep of the staged `wedge-certificates/` for engine/generator/MC
  tokens returned zero; the staged public unit is certificate JSON + stdlib
  checker only. The generator (`gen_dem_dN.py`), enumeration engine
  (`enum_engine_d5.py`), Stim-driven DEM, private MC, and kill-eval builders
  remain private and are NOT staged.

## Staged file pins (SHA-256, 2026-08-11)

```
cb6e617132a11e293045b877440eb08b552eff0d674e9c9971cd992aad433e60  certificate_d3_r1_p1over100.json
706bda319896764604da8c622f744d3a1e65a6657e5d2218466d3ff62e571d23  certificate_d3_r1_p1over1000.json
65a2d51e91267d1d612348b314ae56c2d06f3cc18ae6abb80b69bfe415772a82  certificate_d5_r1_p1over100.json
8013beace863b4e9c5ecd7f4eaf94756d6cc35068f80e9a7b712ed1e858bb850  certificate_d5_r1_p1over1000.json
4d071f7165ed0d16d1d9fce09074af071e0d6cb15fcfd63f5bbfd00546feb2dc  certificate_d5_r1_p1over1000_w6.json
62ff4a1438b1907c6aeae5cdcacd822008f4cb766bcff47c265f4f07fe4b1974  check_wedge.py
046dbeb1223a4df49c266af52d928d677d0ab41a5a30254a396366e38a119f3b  check_wedge_d5.py
```

Staged for release, not committed: awaiting Daniel's go.
