# Regenerating the four proofs that do not fit in git

Four LRAT proofs in this corpus are between 79 MB and 646 MB compressed and are
not carried in this repository. Everything needed to recreate them byte-for-byte
*is* here: the CNF input, the certificate descriptor, and the SHA-256 the result
must have.

Recreating a proof puts a SAT solver back in the loop for the **production** of
the proof. That is where a solver has always been allowed to sit. The **check**
that follows still does not trust it: `check_lower.py` regenerates the CNF from
`HX.txt` / `HZ.txt` / `pairing_*.txt` itself and never reads the shipped `.cnf`.
So a regenerated proof is exactly as trustworthy as one downloaded from the
author, and both are exactly as trustworthy as the checker.

## Solver

CaDiCaL 3.0.1 (Biere, Fazekas, Fleury, Heisinger). Any CaDiCaL >= 3.0 with
`--lrat` should do; a different version, or a different solver emitting LRAT,
will produce a *different but equally valid* proof, so the SHA-256 below will
not match. That is expected and is not a failure — the check is
`check_lower.py`, not the hash. The hashes are recorded so that a reader who
uses the identical toolchain can confirm bit-for-bit reproduction.

The invocation, in every case:

```sh
cadical -q --unsat --lrat --no-binary <input.cnf> <output.lrat>
```

## The four proofs

Run each command from inside the relevant code directory.

### 1. `bb144/lower_X_K11.lrat` — gross code, X sector, symmetry-FREE

```sh
cd bb144
cadical -q --unsat --lrat --no-binary lower_X_K11.cnf lower_X_K11.lrat
python3 ../../qec-scripts/check_lower.py lower_X_K11.json
```

* certifies: `d_X >= 12` for [[144,12,12]] with **no symmetry lemma** in the trusted base
* expected size: 867,803,294 bytes
* expected SHA-256: `017747040f2f6c74681b276b7f15df768ee2781bc3f53d1380ca46c2a01e8508`
* solver time on one Apple M4 laptop: 342.3 s
* pure-Python replay: 176.4 s, 51 MB peak RSS

### 2. `bb144/lower_Z_K11.lrat` — gross code, Z sector, symmetry-FREE

```sh
cd bb144
cadical -q --unsat --lrat --no-binary lower_Z_K11.cnf lower_Z_K11.lrat
python3 ../../qec-scripts/check_lower.py lower_Z_K11.json
```

* certifies: `d_Z >= 12` for [[144,12,12]] with **no symmetry lemma** in the trusted base
* expected size: 671,988,205 bytes
* expected SHA-256: `a95ab0e17453a4088dc09c092fd4d0bee11245f0fb148aa35d336e4784850b6b`
* solver time: 227.3 s
* pure-Python replay: 72.9 s, 49 MB peak RSS

### 3. `bb288/lower_X_K11_i0.lrat` — [[288,12,18]], K = 11, orbit instance 0

```sh
cd bb288
cadical -q --unsat --lrat --no-binary lower_X_K11_i0.cnf lower_X_K11_i0.lrat
python3 ../../qec-scripts/check_lower.py lower_X_K11_sym.json
```

* certifies (with the shipped instance 1, `lower_X_K11_i1.lrat`): `d_X >= 12`
* expected size: 350,776,168 bytes
* expected SHA-256: `ee582993882e2cacc54e85664e7225d15d332ae8c67ffd542bef7471c4005f3a`
* solver time for the rung (both instances): 85.6 s
* pure-Python replay of the rung: 30.6 s, 49 MB peak RSS

### 4. `bb288/lower_X_K13_i0.lrat` — [[288,12,18]], K = 13, orbit instance 0 (the headline)

```sh
cd bb288
cadical -q --unsat --lrat --no-binary lower_X_K13_i0.cnf lower_X_K13_i0.lrat
python3 ../../qec-scripts/check_lower.py lower_X_K13_sym.json
```

* certifies (with the shipped instance 1, `lower_X_K13_i1.lrat`): **`d_X >= 14`**
* expected size: 2,941,958,076 bytes
* expected SHA-256: `1e5904a006b572a5defda9c2bc9f8f2ec39bee14b557f27671405affd0b80503`
* solver time for the rung (both instances): 512.6 s
* pure-Python replay of the rung: 413.6 s, **79 MB peak RSS** — the proof is
  more than thirty times larger than the memory needed to check it
* free disk required: ~3 GB

## What ships, and what it already proves

Nothing else is missing. With only what is in this repository, and nothing but
CPython, a reader can replay:

| code | certified from the shipped artifacts alone |
|---|---|
| Steane, five-qubit, rotated surface d=3 | `d = 3` |
| rotated surface d=5 | `d = 5` |
| rotated surface d=7, Golay | `d = 7` |
| BB [[72,12,6]] | `d = 6` |
| BB [[90,8,10]] | `d = 10` |
| BB [[108,8,10]] | `d = 10` |
| BB [[144,12,12]] (gross) | `d = 12` — weight-12 witnesses, the symmetry-broken X certificate, and the duality certificate |
| BB [[288,12,18]] | `10 <= d`, and `d <= 18` from the weight-18 witness plus duality |

The four regenerable proofs upgrade that to: `d = 12` for the gross code with
**no symmetry lemma at all** in the trusted base, and `14 <= d <= 18` at
n = 288.

## Compressed files

Proofs that do ship and are larger than a few MB ship gzipped. The certificate
descriptors name the uncompressed file, so decompress first:

```sh
gunzip bb90/*.lrat.gz bb108/*.lrat.gz bb144/*.lrat.gz bb288/*.lrat.gz
```

`manifest.json` hashes the **uncompressed** bytes, so a successful `manifest.py`
run after decompression also confirms the archives were intact.

## Integrity

`manifest.json` in this directory carries the SHA-256 and byte count of all 182
artifacts of the audited corpus, including the four proofs listed above, and
`../qec-scripts/manifest.py` re-checks them. Two known gaps, both documented in
the paper: the manifest predates `bb288/duality.json` and does not list it, and
the manifest covers files that this repository does not carry.
