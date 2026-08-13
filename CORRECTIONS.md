# CORRECTIONS — v0.14.0 documentation-correction round

Dated 2026-08-13. This round changed documentation only.

**No certified value changed, and no checker's verification logic changed.** Of the
8 scripts touched, 7 change only comments, docstrings or printed messages; one
non-gating demonstration script had the rational point it queries corrected; and a
machine-specific symlink to an absolute path outside the repository was removed. Every
checker passes as before, and every mathematical result of Parts A through M stands.

This file is an index, not a record. It carries no restated counts, claims or
replacement text: those live in each part's note, and the reasoning behind them in that
part's build log, which are the places they are checked. It lists what changed and
where to find the reasoning.

## Where the corrections are recorded

| Part | Version | Note | Build log | Dated round entry added |
|---|---|---|---|---|
| A | v0.1.x | [`paper/preprint-dixmier-poisson.pdf`](paper/preprint-dixmier-poisson.pdf) | [`paper/FIXLOG.md`](paper/FIXLOG.md) | yes |
| B | v0.2.x | [`paper/preprint-qec-distances.pdf`](paper/preprint-qec-distances.pdf) | [`paper/FIXLOG-qec.md`](paper/FIXLOG-qec.md) | yes |
| C | v0.3.0 | [`tt3-paper/note.pdf`](tt3-paper/note.pdf) | [`tt3-paper/FIXLOG.md`](tt3-paper/FIXLOG.md) | yes |
| D | v0.4.0 | [`qec1435-paper/note.pdf`](qec1435-paper/note.pdf) | [`qec1435-paper/FIXLOG.md`](qec1435-paper/FIXLOG.md) | yes |
| E | v0.5.0 | [`cfr-paper/note.pdf`](cfr-paper/note.pdf) | [`cfr-paper/FIXLOG.md`](cfr-paper/FIXLOG.md) | yes |
| F | v0.6.0 | [`mps-paper/note.pdf`](mps-paper/note.pdf) | [`mps-paper/FIXLOG.md`](mps-paper/FIXLOG.md) | yes |
| G | v0.7.0 | [`k34-paper/note.pdf`](k34-paper/note.pdf) | [`k34-paper/FIXLOG.md`](k34-paper/FIXLOG.md) | yes |
| H | v0.8.0 | [`wedge-paper/note.pdf`](wedge-paper/note.pdf) | [`wedge-paper/FIXLOG.md`](wedge-paper/FIXLOG.md) | yes |
| I | v0.9.0 | [`kelmans-paper/note.pdf`](kelmans-paper/note.pdf) | [`kelmans-paper/FIXLOG.md`](kelmans-paper/FIXLOG.md) | yes |
| J | v0.10.0 | [`k34add-paper/note.pdf`](k34add-paper/note.pdf) | [`k34add-paper/FIXLOG.md`](k34add-paper/FIXLOG.md) | yes |
| K | v0.11.0 | [`wedge2-paper/note.pdf`](wedge2-paper/note.pdf) | [`wedge2-paper/FIXLOG.md`](wedge2-paper/FIXLOG.md) | yes |
| L | v0.12.x | [`demag-paper/note.pdf`](demag-paper/note.pdf) | [`demag-paper/FIXLOG.md`](demag-paper/FIXLOG.md) | yes |
| M | v0.13.0 | [`zefoz-paper/note.pdf`](zefoz-paper/note.pdf) | [`zefoz-paper/FIXLOG.md`](zefoz-paper/FIXLOG.md) | yes |

The last column is mechanical and says exactly one thing: this round's diff against `main`
added a dated line to that log which is not its title. It does not certify that the entry is
complete or correct — only that the log gained one.

Every part carries a build-log entry for this round. Part J's log was created on
2026-08-13 and records only this round's corrections: no build-time log was kept for
v0.10.0, and none has been reconstructed.

## Files changed

81 files. Regenerate this list with `git diff --name-status main`.

**Part A** (6)

- `paper/FIXLOG.md`
- `paper/preprint-dixmier-poisson.md`
- `paper/preprint-dixmier-poisson.pdf`
- `paper/preprint-dixmier-poisson.tex`
- `scripts/erratum-check/exhibit.py`
- `scripts/erratum-check/fibre_check.py`

**Part B** (7)

- `paper/FIXLOG-qec.md`
- `paper/preprint-qec-distances.md`
- `paper/preprint-qec-distances.pdf`
- `paper/preprint-qec-distances.tex`
- `qec-certificates/REGENERATE.md`
- `qec-certificates/bb288/bb288_prof_K16_exact.lrat.gz` — deleted
- `qec-scripts/verify_manifest.py`

**Part C** (4)

- `tt3-paper/FIXLOG.md`
- `tt3-paper/note.md`
- `tt3-paper/note.pdf`
- `tt3-paper/note.tex`

**Part D** (4)

- `qec1435-paper/FIXLOG.md`
- `qec1435-paper/note.md`
- `qec1435-paper/note.pdf`
- `qec1435-paper/note.tex`

**Part E** (4)

- `cfr-paper/FIXLOG.md`
- `cfr-paper/note.md`
- `cfr-paper/note.pdf`
- `cfr-paper/note.tex`

**Part F** (5)

- `mps-certificates/reverify.py`
- `mps-paper/FIXLOG.md`
- `mps-paper/note.md`
- `mps-paper/note.pdf`
- `mps-paper/note.tex`

**Part G** (5)

- `k34-certificates/REGENERATE.md`
- `k34-paper/FIXLOG.md`
- `k34-paper/note.md`
- `k34-paper/note.pdf`
- `k34-paper/note.tex`

**Part H** (4)

- `wedge-paper/FIXLOG.md`
- `wedge-paper/note.md`
- `wedge-paper/note.pdf`
- `wedge-paper/note.tex`

**Part I** (6)

- `kelmans-certificates/verdict-n04-20.md`
- `kelmans-certificates/verdict-n22-24.md`
- `kelmans-paper/FIXLOG.md`
- `kelmans-paper/note.md`
- `kelmans-paper/note.pdf`
- `kelmans-paper/note.tex`

**Part J** (5)

- `k34add-certificates/README.md`
- `k34add-paper/FIXLOG.md` — added
- `k34add-paper/note.md`
- `k34add-paper/note.pdf`
- `k34add-paper/note.tex`

**Part K** (5)

- `wedge2-paper/FIXLOG.md`
- `wedge2-paper/note.md`
- `wedge2-paper/note.pdf`
- `wedge2-paper/note.tex`
- `wedge2-scripts/identity_selftest.py`

**Part L** (6)

- `demag-paper/FIXLOG.md`
- `demag-paper/note.md`
- `demag-paper/note.pdf`
- `demag-paper/note.tex`
- `demag-scripts/anchor_check.py`
- `demag-scripts/tamper_demo.py`

**Part M** (6)

- `zefoz-paper/FIXLOG.md`
- `zefoz-paper/note.md`
- `zefoz-paper/note.pdf`
- `zefoz-paper/note.tex`
- `zefoz-scripts/kill-logs/KILL-STATS.md`
- `zefoz-scripts/tamper_demo.py`

**Repository-wide** (14)

- `.gitignore`
- `.zenodo.json`
- `CITATION.cff`
- `CORRECTIONS.md` — added
- `INDEPENDENT-VERIFICATION.md`
- `PROVENANCE.md`
- `README.md`
- `SWEEP-RECORD-CFR-2026-08-06.md`
- `SWEEP-RECORD-DEMAG-2026-08-12.md`
- `SWEEP-RECORD-K34ADD-2026-08-11.md`
- `SWEEP-RECORD-KELMANS-2026-08-11.md`
- `SWEEP-RECORD-MPS-2026-08-06.md`
- `SWEEP-RECORD-TT3-2026-08-05.md`
- `SWEEP-RECORD-ZEFOZ-2026-08-12.md`
