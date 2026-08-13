# Regenerating the Erdős #112 (k(3,4)) certificate corpus

**The small artifacts are the record; the multi-gigabyte `.lrat` proofs are a cache.** Every
proof can be regenerated from the generator scripts plus the queue files, and every regenerated
proof is checkable against the SHA-256 recorded in `CERTLOG.txt`. Do not treat proof loss as
result loss (the program's internal preservation policy, PRESERVATION.md §3, which is not part
of this deposit).

That record is split between this public deposit and a private regeneration kit held by the
author. **What is in this directory:** `CERTLOG.txt`, this file, and the two lower-bound
witnesses `witness_sat_3_4_20.json` and `witness_cayley_6_3_n28_3_8_10_12_17.json`. **What is
in `k34-scripts/` beside it:** `gen_cnf.py`, `make_structured.py`, `lrat_check.py`,
`verify_witness.py`, `audit_cnf.py`, `audit_multiset.py`. Everything else in the table below —
the queue files, the 70 block-class representatives, `make_structured24.py`, `verify_one.py`,
`verify_and_pack.py`, `verify_chain.py`, `witness_c3_irw22_25.json`, `NOTES.md` — belongs to
the kit and is **not** in this repository. The table records what must be preserved, not what
is distributed; the procedure below runs inside the kit, not from this deposit. From the
deposit alone a reader can verify both witnesses and replay any certificate whose `.cnf` and
`.lrat` they hold, but cannot regenerate a `.cnf` to its recorded `cnf_sha256` (the
representatives are missing) and cannot run `audit_multiset.py` (it imports `verify_chain.py`).

## What must never be lost (small; keep and back up — kit contents, only partly deposited)

| Artifact | Size | In this deposit | Role |
|---|---|---|---|
| `CERTLOG.txt` | KB | yes | the verification record: per-certificate verdict, checked-step count, `cnf_sha256`, `lrat_sha256`, proof byte count |
| `q*.jsonl` + `q*.jsonl.state.jsonl` | KB | no | the exact job definitions (solver command line per cube) and their outcomes. **Covers 444 of the 445 bases: the single N=24 instance `s2434` has no queue line; regenerate it with `make_structured24.py`** |
| `gen_cnf.py`, `make_structured.py` | KB | yes | CNF/cube generators — the seed of every `.cnf` |
| `make_structured24.py` | KB | no | the generator for the single N=24 instance `s2434` |
| `blocks_i3l3_*.json`, `blocks_tt4f_*.json`, `witness_bermond8.json`, `witness_qr7.json` | KB | no | **the 70 block-class representatives the generators consume.** Without these no `.cnf` can be regenerated, and re-enumerating will not reproduce the recorded `cnf_sha256` (representative choice depends on enumeration order) |
| `lrat_check.py`, `audit_cnf.py`, `audit_multiset.py` | KB | yes | the deposited part of the checking and completeness-audit pipeline. `audit_multiset.py` imports `verify_chain.py` and therefore runs only inside the kit |
| `verify_one.py`, `verify_and_pack.py`, `verify_chain.py` | KB | no | the rest of that pipeline: the per-base verify-and-pack driver and `verify_chain.py`, which is also the only written-down cube-name ↔ block-class mapping |
| `verify_witness.py` | KB | yes | the checker for the entire lower-bound half |
| `witness_sat_3_4_20.json`, `witness_cayley_6_3_n28_3_8_10_12_17.json` | KB | yes | the two published lower-bound witnesses (independently checkable in milliseconds) |
| `witness_c3_irw22_25.json` | KB | no | a third lower-bound witness, not published with the note |
| `NOTES.md` | KB | no | the running record of what was run and why |

The kit assembled from this table has been tested end to end — it regenerates
`s21_587_1.cnf` to its recorded `cnf_sha256`, runs the completeness audit, and
verifies both witnesses — but that test was run on the kit, which is not this
deposit. Of those three, only the witness verification replays from this deposit.

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

## Procedure (runs inside the kit; steps 1–3 are not executable from this deposit)

1. Regenerate a cube's CNF with the generator and the block-class representatives; confirm
   `cnf_sha256` against `CERTLOG.txt`.
2. Re-run its solver command from the matching `q*.jsonl` line (CaDiCaL with proof logging).
3. `python3 verify_one.py <base>` — appends the verdict to `CERTLOG.txt` and packs the proof.

## What this deposit alone supports

* `python3 k34-scripts/verify_witness.py k34-certificates/witness_sat_3_4_20.json 3 4`, and the
  same for `witness_cayley_6_3_n28_3_8_10_12_17.json` with arguments `6 3` — the whole
  lower-bound half, in milliseconds.
* `python3 k34-scripts/lrat_check.py <base>.cnf <base>.lrat[.gz]` on any formula and proof the
  reader holds or has regenerated, checked against the digests and step count in `CERTLOG.txt`.
* `python3 k34-scripts/audit_cnf.py pure 3 4 <N> <file>.cnf` — re-derives the base encoding from
  the definitions and compares clause sets; the `cube` mode additionally needs the block JSONs
  its cube was built from, so it belongs to the kit.

Verification requires only CPython: the whole checking path is standard-library only, with no
external binary anywhere on it. `lrat_check.py` reads `<base>.lrat` and `<base>.lrat.gz`
interchangeably, and packing uses the `gzip` module, not a `gzip`/`gunzip` executable
(PROTOCOL §10). Regeneration additionally requires CaDiCaL 3.0.1, which is POSIX/WSL-friendly.
