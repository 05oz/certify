# Regenerating the Erdős #112 (k(3,4)) certificate corpus

**The small artifacts in this directory are the record; the multi-gigabyte `.lrat` proofs are a
cache.** Every proof can be regenerated from the generator scripts plus the queue files, and every
regenerated proof is checkable against the SHA-256 recorded in `CERTLOG.txt`. Do not treat proof
loss as result loss (PRESERVATION.md §3).

## What must never be lost (small; keep, back up, and publish with any paper)

| Artifact | Size | Role |
|---|---|---|
| `CERTLOG.txt` | KB | the verification record: per-certificate verdict, checked-step count, `cnf_sha256`, `lrat_sha256`, proof byte count |
| `q*.jsonl` + `q*.jsonl.state.jsonl` | KB | the exact job definitions (solver command line per cube) and their outcomes. **Covers 444 of the 445 bases: the single N=24 instance `s2434` has no queue line; regenerate it with `make_structured24.py`** |
| `gen_cnf.py`, `make_structured.py`, `make_structured24.py` | KB | CNF/cube generators — the seed of every `.cnf` |
| `blocks_i3l3_*.json`, `blocks_tt4f_*.json`, `witness_bermond8.json`, `witness_qr7.json` | KB | **the 70 block-class representatives the generators consume.** Without these no `.cnf` can be regenerated, and re-enumerating will not reproduce the recorded `cnf_sha256` (representative choice depends on enumeration order) |
| `lrat_check.py`, `verify_one.py`, `verify_and_pack.py`, `audit_multiset.py`, `audit_cnf.py`, `verify_chain.py` | KB | the checking and completeness-audit pipeline. `audit_multiset.py` imports `verify_chain.py`, which is also the only written-down cube-name ↔ block-class mapping |
| `verify_witness.py` | KB | the checker for the entire lower-bound half |
| `witness_sat_3_4_20.json`, `witness_cayley_6_3_n28_3_8_10_12_17.json`, `witness_c3_irw22_25.json` | KB | the explicit lower-bound witnesses (independently checkable in milliseconds) |
| `NOTES.md` | KB | the running record of what was run and why |

A kit assembled from this table has been tested end to end: it regenerates
`s21_587_1.cnf` to its recorded `cnf_sha256`, runs the completeness audit, and
verifies both witnesses.

## What is regenerable (large; delete freely once `CERTLOG.txt` records it)

* all cube `.cnf` files (≈ 2.1 GB total; the 346 `s21_*.cnf` alone are ≈ 1.5 GB) — regenerate
  with the generator scripts; each must match the `cnf_sha256` recorded in `CERTLOG.txt`.
* `s21_*.lrat(.gz)`, `s22_*.lrat(.gz)` (**281 GB uncompressed across all 445 certificates; the
  346-certificate N=21 layer alone is 245 GB** — sum the `lrat_bytes` field of `CERTLOG.txt` to
  confirm) — regenerate by re-running the
  solver command stored in the corresponding `q*.jsonl` entry, then re-verify with
  `python3 verify_one.py <base>`. A regenerated proof need not be byte-identical (solvers are not
  required to be deterministic across builds); what must hold is that `lrat_check.py` accepts it
  against the same `.cnf`.

## Procedure

1. Regenerate a cube's CNF with the generator; confirm `cnf_sha256` against `CERTLOG.txt`.
2. Re-run its solver command from the matching `q*.jsonl` line (CaDiCaL with proof logging).
3. `python3 verify_one.py <base>` — appends the verdict to `CERTLOG.txt` and packs the proof.

Verification requires only CPython: the whole checking path is standard-library only, with no
external binary anywhere on it. `lrat_check.py` reads `<base>.lrat` and `<base>.lrat.gz`
interchangeably, and packing uses the `gzip` module, not a `gzip`/`gunzip` executable
(PROTOCOL §10). Regeneration additionally requires CaDiCaL 3.0.1, which is POSIX/WSL-friendly.
