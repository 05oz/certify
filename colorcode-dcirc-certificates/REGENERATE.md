# Regenerating the five proofs that are not shipped

Five LRAT proofs are not carried in this directory. Each is larger than the repository's 50 MB
per-file limit.

| certificate | proves | proof file | gzip bytes | SHA-256 of the original gzip file | solver wall (build laptop) |
|---|---|---|---|---|---|
| `lower_d5_r5_K3.json` | d_circ(5,5) ≥ 4, direct | `d5_r5_K3.lrat.gz` | 70,625,863 | `ca61f84722d5e935db12945d95233870d025221a7433f636b31e0f0a87a6a5bf` | 56 s |
| `lower_pxd7_r7_K5.json` | d_circ(7,7) ≥ 6, X-part | `pxd7_r7_K5.lrat.gz` | 181,187,589 | `d078a0c2e4caa151d1a01aa39776c2aa3b14cf6108f1ee8062138aed4fc667f5` | 87 s |
| `lower_pxd9_r9_K6.json` | d_circ(9,9) ≥ 7, X-part | `pxd9_r9_K6.lrat.gz` | 4,057,166,967 | `b1bcaee2eaf2432d7315c11934684ef8beeb3fba6d930f00b9fe3c46679aa31f` | 686 s |
| `lower_Xext_d13_K10.json` | d_circ(13, r) ≥ 11, extended code | `Xext_d13_K10.lrat.gz` | 1,165,006,138 | `42df3115d67ff3eeb4610292bdd3b6802a39b9b277872bce48a33f358eec5e65` | 1,396 s |
| `lower_Xext_d15_K11.json` | d_circ(15, r) ≥ 12, extended code | `Xext_d15_K11.lrat.gz` | 8,945,210,112 | `8ca35d6c8147feacb5c65a000e256b6890d544cf4d9aa8cf0257190375939daf` | 15,724 s |

The d = 15 proof was produced in CaDiCaL's binary LRAT format: 14,062,531,915 bytes, SHA-256
`117a39f81e185a1b9302c6ae781891bb3d194caab6f61c5ed84853f5ddf53e92`. The gzip text file above
was converted from it. The same list is in `PROOFS-NOT-IN-GIT.sha256`.

**Values not covered by a shipped proof.** The values at d = 5, 7, 9 are also proved by shipped
proofs: the extended-code proofs `Xext_d{5,7,9}` and the X-part proof `pxd5`. Only **d = 13 and
d = 15** have no shipped lower-bound proof. For those two, regeneration is the way to check the
lower bound.

## Downloading the original proofs

The five files in the table above are attached to the GitHub release v0.16.0 of this repository
(https://github.com/05oz/certify/releases/tag/v0.16.0). They are not part of the Zenodo archive of
that release, which holds the repository snapshot. The two files larger than 2 GiB are attached in
parts of 1,900,000,000 bytes, the last part smaller: `pxd9_r9_K6.lrat.gz.part-a` to `.part-c`,
and `Xext_d15_K11.lrat.gz.part-a` to `.part-e`. The binary original of the d = 15 proof is not
attached. `check_dcirc.py` replays the gzip text proof, and drat-trim's `lrat-check` read the same
text, byte for byte (`logs/d15_proof_text_identity_2026-10-20.log`).

Download the files into this directory. Move the three whole files into `certs/` unchanged, then
join the parts, in order, into `certs/`. POSIX:

```
mv d5_r5_K3.lrat.gz pxd7_r7_K5.lrat.gz Xext_d13_K10.lrat.gz certs/
cat pxd9_r9_K6.lrat.gz.part-a pxd9_r9_K6.lrat.gz.part-b pxd9_r9_K6.lrat.gz.part-c > certs/pxd9_r9_K6.lrat.gz
cat Xext_d15_K11.lrat.gz.part-a Xext_d15_K11.lrat.gz.part-b Xext_d15_K11.lrat.gz.part-c Xext_d15_K11.lrat.gz.part-d Xext_d15_K11.lrat.gz.part-e > certs/Xext_d15_K11.lrat.gz
```

Windows (cmd):

```
move d5_r5_K3.lrat.gz certs\
move pxd7_r7_K5.lrat.gz certs\
move Xext_d13_K10.lrat.gz certs\
copy /b pxd9_r9_K6.lrat.gz.part-a + pxd9_r9_K6.lrat.gz.part-b + pxd9_r9_K6.lrat.gz.part-c certs\pxd9_r9_K6.lrat.gz
copy /b Xext_d15_K11.lrat.gz.part-a + Xext_d15_K11.lrat.gz.part-b + Xext_d15_K11.lrat.gz.part-c + Xext_d15_K11.lrat.gz.part-d + Xext_d15_K11.lrat.gz.part-e certs\Xext_d15_K11.lrat.gz
```

Compare each file's SHA-256 with the table. POSIX: `shasum -a 256 certs/NAME.lrat.gz` or
`sha256sum certs/NAME.lrat.gz`. Windows cmd: `certutil -hashfile certs\NAME.lrat.gz SHA256`.
PowerShell: `(Get-FileHash certs\NAME.lrat.gz -Algorithm SHA256).Hash`, which prints upper-case
hex. Then run `python3 certs/check_dcirc.py lower certs/lower_NAME.json` for each, or
`python3 run_all.py`, which replays every proof present in `certs/`; on Windows, type `py` (or
`python`) in place of `python3`. The hash authenticates the copy; the check is
`check_dcirc.py lower`.

## Why a regenerated proof is as good as the original

The solver sits in the production of a proof, which is where a solver has always been allowed. The
check does not trust it. `check_dcirc.py lower` regenerates the CNF from the hash-pinned object
and refuses a formula whose SHA-256 differs from the certificate's `cnf_sha256`. It then replays
the proof clause by clause. A proof made by another solver or another CaDiCaL version is
different but equally valid, so a SHA-256 mismatch against the table above is expected and is not
a failure. The hashes are there so that a reader with the identical toolchain can confirm
bit-for-bit reproduction, and so that copies of the original files can be authenticated. On
2026-10-20, re-solving five of the shipped instances (`d3_r3_K1`, `d5_r1_K3`, `d7_r1_K5`,
`Xext_d7_K5`, `Xext_d9_K6`) with CaDiCaL 3.0.1 reproduced their shipped proofs byte for byte
(`logs/converter_identity_2026-10-20.log`).

## Steps (any platform with Python ≥ 3.9 and a CaDiCaL build)

From this directory, with `NAME` the certificate stem, for example `Xext_d13_K10`. The commands
are written with `python3`; on Windows, type `py` (or `python`) in its place.

1. **Write the CNF the checker will use.**

   ```
   python3 tools/emit_cnf.py certs/lower_NAME.json NAME.cnf
   ```

   It prints the SHA-256 and exits non-zero unless it matches the certificate. On 2026-10-20 the
   regenerated CNF had the same SHA-256 as the solver's input file for all five certificates. For
   d = 15 the two files were also compared byte by byte (`VERIFY.log`).

2. **Solve with LRAT output.** CaDiCaL 3.0.1 was used; on Windows, use WSL or a native build.

   ```
   cadical --lrat --no-binary NAME.cnf NAME.lrat
   python3 -m gzip NAME.lrat
   ```

   Then move `NAME.lrat.gz` into `certs/`. CaDiCaL exits with code 20 (UNSATISFIABLE).

   **For d = 15 the text proof is large.** The original run wrote binary LRAT and converted it in
   a stream:

   ```
   cadical --lrat NAME.cnf NAME.blrat
   cc -O2 -o blrat2lrat tools/blrat2lrat.c
   ./blrat2lrat 13932 < NAME.blrat | gzip -1 > certs/Xext_d15_K11.lrat.gz
   ```

   Here 13932 is the CNF's clause count. These three lines need a POSIX shell and a C compiler
   (on Windows, WSL). The converter is a format converter, not a checker: a faulty conversion can
   only make the check fail. On 2026-10-20 its output was byte-identical to CaDiCaL's own text
   LRAT on five shipped instances (`logs/converter_identity_2026-10-20.log`). Do not pipe
   CaDiCaL's text output through a pipe into gzip on a memory-starved machine; on the build laptop
   that deadlocked. Write the file to disk first.

3. **Check.**

   ```
   python3 certs/check_dcirc.py lower certs/lower_NAME.json
   ```

   Or run `python3 run_all.py`, which picks up any proof present in `certs/`.

## Expected cost

Measured on the build laptop (Apple, 10 cores, 16 GB). Solver times are single runs; replay times
are `check_dcirc.py`.

- **d = 13:** about 23 minutes to solve, 1.2 GB gzip, and 5–12 minutes to replay (316 s and
  503 s on 2026-09-01; 706.7 s on 2026-10-20, whose log records no load figure). A replay on
  2026-10-21 took 1,465.3 s of wall-clock time and 708.4 s of CPU time; its log records one-minute
  load averages of 69.5 at its start and 127.3 at its end
  (`logs/replay_out_of_git_proofs_round4_2026-10-21.log`).
- **d = 15:** about 4.4 hours to solve. The binary proof is 14 GB; the gzip text is 9 GB. Replay
  took about 1.7 hours in `check_dcirc.py` and 20 minutes in drat-trim's `lrat-check`.

Allow about 25 GB of free disk for the d = 15 run.

## Optional second checker for any regenerated proof

drat-trim's `lrat-check` (github.com/marijnheule/drat-trim) accepts the same text proof against
the emitted CNF:

```
lrat-check NAME.cnf NAME.lrat
```

The d = 15 proof was checked by `lrat-check` on 2026-10-07 (`c VERIFIED`, 1,168.4 s;
`logs/2026-10-07/drat-trim_lrat-check_Xext_d15_K11.log`). It was not given the stored gzip file:
the converter's output for the binary proof was fed to it on standard input, against the CNF
whose SHA-256 its log records (`2b471a0f…83fde`, the formula `tools/emit_cnf.py` emits). That text is byte-identical to the decompressed `Xext_d15_K11.lrat.gz`, which
`check_dcirc.py` replayed (both 30,547,997,901 bytes, SHA-256 `d1220b7e…77fb84`;
`logs/d15_proof_text_identity_2026-10-20.log`).
