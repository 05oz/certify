# Regenerating the Erdős #112 (k(3,4)) certificate corpus

The small artifacts are the record. The multi-gigabyte `.lrat` proofs are a cache. Every proof
can be regenerated from the generator scripts, the block-class representatives and the queue
files, and every regenerated proof can be checked against its line in `CERTLOG.txt`. Losing a
proof file does not lose a result (the program's internal preservation policy, PRESERVATION.md
§3, which is not part of this deposit).

Every file the procedure below needs is in this repository. The block-class representatives,
the queue files and `verify_chain.py` were added after release v0.17.0. Releases up to v0.17.0
and their Zenodo records do not contain them, and texts written before the addition describe
them as held back in a private kit.

**In this directory:** `CERTLOG.txt`, this file, the two lower-bound witnesses
`witness_sat_3_4_20.json` and `witness_cayley_6_3_n28_3_8_10_12_17.json`, the 70 block files
`blocks_i3l3_*.json` and `blocks_tt4f_*.json`, the two further representatives
`witness_bermond8.json` and `witness_qr7.json`, and the queue files `q2.jsonl`, `q3.jsonl`,
`q5.jsonl` and `q5b.jsonl`. **In `k34-scripts/` beside it:** `gen_cnf.py`, `make_structured.py`,
`lrat_check.py`, `verify_witness.py`, `audit_cnf.py`, `audit_multiset.py`, `verify_chain.py`.

Held by the author and not in this repository: `make_structured24.py`, `verify_one.py`,
`verify_and_pack.py`, the job runner's state files, the queue files that hold no certificate
run, `witness_c3_irw22_25.json` and `NOTES.md`. The procedure below needs none of them.

## What must never be lost (small; keep and back up)

| Artifact | Size | In this repository | Role |
|---|---|---|---|
| `CERTLOG.txt` | KB | yes | the verification record: per-certificate verdict, checked-step count, `cnf_sha256`, `lrat_sha256`, proof byte count |
| `q2.jsonl`, `q3.jsonl`, `q5.jsonl`, `q5b.jsonl` | KB | yes | the solver command line of every cube of the N=23, N=22 and N=21 layers. **Covers 444 of the 445 bases: the single N=24 instance `s2434` has no queue line.** Published form: see "The queue files" below |
| `q*.jsonl.state.jsonl` and the other `q*.jsonl` | KB | no | the job runner's records of each job (status, time stamp, exit code, run time, peak memory), and the queues that hold no certificate run |
| `gen_cnf.py`, `make_structured.py` | KB | yes | CNF/cube generators, the seed of every `.cnf` |
| `make_structured24.py` | KB | no | the script that first wrote the single N=24 instance `s2434.cnf`. Not needed: `make_structured.py` with the two witness files writes the same bytes (last row of the table of cube names) |
| `blocks_i3l3_*.json`, `blocks_tt4f_*.json`, `witness_bermond8.json`, `witness_qr7.json` | KB | yes | **the 72 block-class representatives the generator consumes:** the 70 block files, and the representatives on 8 and on 7 vertices, which are stored as witness files. Without these no cube `.cnf` can be regenerated, and re-enumerating will not reproduce the recorded `cnf_sha256` (representative choice depends on enumeration order) |
| `lrat_check.py`, `audit_cnf.py`, `audit_multiset.py` | KB | yes | the proof checker and the two completeness audits |
| `verify_chain.py` | KB | yes | the cube-name ↔ block-class mapping as code, imported by `audit_multiset.py`; run by itself it checks a whole layer (see "The whole chain" below) |
| `verify_one.py`, `verify_and_pack.py` | KB | no | the drivers that wrote `CERTLOG.txt` during the original run: check one proof with `lrat_check.py`, append its ledger line, pack the proof. Not needed to regenerate or to check |
| `verify_witness.py` | KB | yes | the checker for the entire lower-bound half |
| `witness_sat_3_4_20.json`, `witness_cayley_6_3_n28_3_8_10_12_17.json` | KB | yes | the two published lower-bound witnesses (independently checkable in milliseconds) |
| `witness_c3_irw22_25.json` | KB | no | a third lower-bound witness, not published with the note |
| `NOTES.md` | KB | no | the running record of what was run and why |

## What is regenerable (large; delete freely once `CERTLOG.txt` records it)

* all cube `.cnf` files (2.07 GB for the 445; the 346 `s21_*.cnf` alone are 1.53 GB). Each must
  match the `cnf_sha256` recorded in `CERTLOG.txt`.
* all `.lrat` proofs (281 GB uncompressed across the 445 certificates; the 346 of the N=21
  layer alone are 245 GB; sum the `lrat_bytes` field of `CERTLOG.txt` to confirm). A
  regenerated proof need not be byte-identical (solvers are not required to be deterministic
  across builds). What must hold is that `lrat_check.py` accepts it against the same `.cnf`.

## The queue files

Each line is one job: an `id`, the shell command `cmd`, the job runner's limits `timeout`
(seconds) and `mem_mb`, and an empty `meta` field. `q5.jsonl` holds the 346 cubes of the N=21 layer, `q3.jsonl` the 90
cubes of N=22 and `q2.jsonl` the 8 cubes of N=23 (its ids are written without the underscore,
`s23a0` for `s23_a0`). `q5b.jsonl` repeats 24 lines of `q5.jsonl` with a longer `timeout`: in
the first pass the job runner stopped those 24 jobs at its own time limit, and they were run
again. The command is the same in both files.

The published files are the original job lines with two edits, both made by script: the
absolute path of the run directory was removed in front of every file name, and the directory
in front of the solver's name was removed. So each file is named as it sits in the working
directory, and the command reads `cadical`. Lines for jobs that are not certificate runs were
left out: six lines of `q2.jsonl` and six of `q3.jsonl`.

Every command has one shape:

```
cadical --lrat --no-binary -t 1500 '<base>.cnf' '<base>.lrat' > '<base>.sol'; grep -m1 '^s ' '<base>.sol'
```

`-t 1500` is CaDiCaL's time limit in seconds. It does not change the proof: for `s21_587_1`
the proofs written with and without it are byte-identical. On a slower machine, raise it or
leave it out. `s2434` has no queue line; the solver's log of that run records the same options
with `-t 170`.

## Cube names and their blocks

A cube formula is written by `make_structured.py N p q s <p-block> <q-block> <s-block> <name>.cnf`.
Vertex 0 has p out-neighbours, q in-neighbours and s non-neighbours, and the three blocks are
fixed to the named class representatives. The index in a block file's name is the index in the
cube's name. `verify_chain.py` holds the same rule as code (`I3L3`, `TT4F`, `cube_name`); the
table below was printed from it.

| cube name | indices | cubes | arguments of `make_structured.py` before `<name>.cnf` |
|---|---|---|---|
| `s21_587_<i>` | i = 0..24 | 25 | `21 5 8 7 blocks_i3l3_5_class<i>.json witness_bermond8.json witness_qr7.json` |
| `s21_677_<i>_<j>` | i = 0..30, j = 0..6 | 217 | `21 6 7 7 blocks_i3l3_6_class<i>.json blocks_i3l3_7_class<j>.json witness_qr7.json` |
| `s21_686_<i>` | i = 0..30 | 31 | `21 6 8 6 blocks_i3l3_6_class<i>.json witness_bermond8.json blocks_tt4f_6_class0.json` |
| `s21_776_<i>_<j>` | i = 0..6, j = 0..6 | 49 | `21 7 7 6 blocks_i3l3_7_class<i>.json blocks_i3l3_7_class<j>.json blocks_tt4f_6_class0.json` |
| `s21_785_<i>_<k>` | i = 0..6, k = 0..2 | 21 | `21 7 8 5 blocks_i3l3_7_class<i>.json witness_bermond8.json blocks_tt4f_5_class<k>.json` |
| `s21_884_<k>` | k = 0..2 | 3 | `21 8 8 4 witness_bermond8.json witness_bermond8.json blocks_tt4f_4_class<k>.json` |
| `s22_A<i>` | i = 0..30 | 31 | `22 6 8 7 blocks_i3l3_6_class<i>.json witness_bermond8.json witness_qr7.json` |
| `s22_B<i>_<j>` | i = 0..6, j = 0..6 | 49 | `22 7 7 7 blocks_i3l3_7_class<i>.json blocks_i3l3_7_class<j>.json witness_qr7.json` |
| `s22_C<i>` | i = 0..6 | 7 | `22 7 8 6 blocks_i3l3_7_class<i>.json witness_bermond8.json blocks_tt4f_6_class0.json` |
| `s22_D<k>` | k = 0..2 | 3 | `22 8 8 5 witness_bermond8.json witness_bermond8.json blocks_tt4f_5_class<k>.json` |
| `s23_a<i>` | i = 0..6 | 7 | `23 7 8 7 blocks_i3l3_7_class<i>.json witness_bermond8.json witness_qr7.json` |
| `s23_c` | one cube | 1 | `23 8 8 6 witness_bermond8.json witness_bermond8.json blocks_tt4f_6_class0.json` |
| `s2434` | one cube | 1 | `24 8 8 7 witness_bermond8.json witness_bermond8.json witness_qr7.json` |

## Procedure

Regeneration needs CPython 3 and CaDiCaL (`cadical` on the path) and assumes a POSIX shell.
`audit_multiset.py` and `verify_chain.py` look for their files beside themselves, so work in
one directory that holds the scripts and the data together. From the root of the repository:

```
mkdir work
cp k34-scripts/*.py k34-certificates/*.json k34-certificates/*.jsonl k34-certificates/CERTLOG.txt work/
cd work
```

1. Regenerate a cube's formula with the arguments from the table of names, and compare its
   SHA-256 with the `cnf_sha256` field of its line in `CERTLOG.txt`.

```
python3 make_structured.py 21 5 8 7 blocks_i3l3_5_class1.json witness_bermond8.json witness_qr7.json s21_587_1.cnf
python3 -c "import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" s21_587_1.cnf
grep "^s21_587_1 " CERTLOG.txt
```

2. Find its solver command in the queue file of its layer and run it.

```
grep "'s21_587_1.cnf'" q5.jsonl
cadical --lrat --no-binary -t 1500 's21_587_1.cnf' 's21_587_1.lrat' > 's21_587_1.sol'; grep -m1 '^s ' 's21_587_1.sol'
```

3. Check the proof. The checker must print `VERIFIED`. When the proof is byte-identical to the
   original, its size and SHA-256 equal `lrat_bytes` and `lrat_sha256` of the ledger line, and
   the step count printed equals the ledger's.

```
python3 lrat_check.py s21_587_1.cnf s21_587_1.lrat
```

The two audits of a formula:

```
python3 audit_cnf.py cube 21 5 8 7 blocks_i3l3_5_class1.json witness_bermond8.json witness_qr7.json s21_587_1.cnf
python3 audit_multiset.py 21
```

`audit_cnf.py` takes the same arguments as the generator. `audit_multiset.py N` checks every
cube of layer N and needs all of them in the working directory. To write all cubes of a layer,
save these lines as `regen_layer.py` in the working directory and run `python3 regen_layer.py 21`
(or 22, 23, 24):

```python
import subprocess, sys
from verify_chain import I3L3, TT4F, cube_name

N = int(sys.argv[1])
for p in range(max(0, N - 16), 9):
    for q in range(p, 9):
        s = N - 1 - p - q
        if not 0 <= s <= 7:
            continue
        for i, pf in enumerate(I3L3[p]):
            for j, qf in enumerate(I3L3[q]):
                for k, sf in enumerate(TT4F[s]):
                    name = cube_name(N, p, q, s, i, j, k)
                    subprocess.run([sys.executable, "make_structured.py", str(N), str(p),
                                    str(q), str(s), pf, qf, sf, name + ".cnf"], check=True)
```

## The whole chain

`python3 verify_chain.py 21` re-derives the list of cubes of the layer and, for each cube,
runs `audit_cnf.py`, looks up its `VERIFIED` line in `CERTLOG.txt`, and compares the SHA-256
of the formula and of the proof file in the working directory with that line. It needs every
proof of the layer on disk (245 GB for N=21) and accepts a proof only if it is byte-identical
to the original. Before the layers it checks `witness_bermond8.json` and `witness_qr7.json`
with `verify_witness.py` and replays two small certificates, for the two statements of
Lemma 3.2 of the note (no {I₃,TT₃}-free oriented graph on 9 vertices, no TT₄-free tournament
on 8 vertices). It expects them under `validation/`. They are made by:

```
mkdir validation
python3 gen_cnf.py 3 3 9 validation/t339.cnf
cadical --lrat --no-binary validation/t339.cnf validation/t339.lrat > validation/t339.sol
python3 gen_cnf.py 2 4 8 validation/t248.cnf
cadical --lrat --no-binary validation/t248.cnf validation/t248.lrat > validation/t248.sol
```

The header of `verify_chain.py` points to Lemma 3.1 of the note in `k34-paper/` for the argument
about the three neighbourhoods of a vertex. (Updated 2026-11-17: until then the header pointed to
`NOTES`, a file that is not in this repository.)

## What was tested on 2026-11-17

The procedure above was run from a clean export of `k34-scripts/` and `k34-certificates/` at
commit dd60711 with the added files in place, with CPython 3.15.2 and with the CaDiCaL build
that wrote the original proofs (version 3.0.1, Homebrew build for macOS on Apple silicon).

* Formulas. All 445 were regenerated. Each SHA-256 equals its `cnf_sha256` in `CERTLOG.txt`.
  `audit_multiset.py` passed for N = 21, 22, 23 and 24.
* Proofs. 17 proofs were regenerated with the recorded commands: `s2434`, the eight cubes of
  N=23, and eight cubes of N=21 (the three cubes with the smallest proofs of the layer,
  `s21_587_1`, `s21_587_15`, `s21_587_0`, and the cube with the smallest proof of each of the
  other five types, `s21_884_2`, `s21_677_30_0`, `s21_785_3_1`, `s21_686_25`, `s21_776_3_1`).
  Each came out byte-identical to the original: `lrat_bytes` and `lrat_sha256` equal the
  ledger's. `lrat_check.py` accepted each with the ledger's step count. A second checker,
  `lrat-check` of drat-trim (commit 2e3b2dc), accepted each as well.
* `python3 verify_chain.py 24 23` printed `CHAIN FULLY VERIFIED for layers [24, 23]`.

The N=22 layer and the rest of the N=21 layer were not solved again in this test.

## Without a solver

* `python3 k34-scripts/verify_witness.py k34-certificates/witness_sat_3_4_20.json 3 4`, and the
  same for `witness_cayley_6_3_n28_3_8_10_12_17.json` with arguments `6 3`: the whole
  lower-bound half, in milliseconds.
* `python3 k34-scripts/lrat_check.py <base>.cnf <base>.lrat[.gz]` on any formula and proof the
  reader holds, checked against the digests and step count in `CERTLOG.txt`.
* `python3 k34-scripts/audit_cnf.py pure 3 4 <N> <file>.cnf` re-derives the base encoding from
  the definitions and compares clause sets.
* Step 1 of the procedure and both audits need no solver.

Verification requires only CPython: the whole checking path is standard-library only, with no
external binary anywhere on it. `lrat_check.py` reads `<base>.lrat` and `<base>.lrat.gz`
interchangeably. Regenerating proofs additionally requires CaDiCaL. The original proofs were
written by CaDiCaL 3.0.1, which is POSIX/WSL-friendly.
