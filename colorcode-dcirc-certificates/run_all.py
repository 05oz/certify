#!/usr/bin/env python3
"""run_all.py -- single entry point for the colour-code circuit-distance certificates.
Python standard library only; runs the same way on Linux, macOS and Windows.  The commands are
written with python3; on Windows use py (or python) instead.

    python3 run_all.py           full check (a few minutes on a laptop)
    python3 run_all.py --fast    every witness, the one-round and extended-code objects and the
                                 proofs under 5 MB (under half a minute)

Measured times and their logs are in README.md, section "Run it".

What it runs, in order, all from certs/:
  1. check_dcirc.py object   for every object m_*.json: the mechanism list is re-derived from the
                             hash-pinned circuit text without Stim and compared.
  2. check_dcirc.py witness  for every witness_*.json: the listed mechanisms are XORed against the
                             object; they must flip no detector and flip the observable.
  3. check_dcirc.py lower    for every lower_*.json whose proof file is present: the CNF is
                             regenerated from the object, its SHA-256 compared with the recorded
                             one, and the LRAT proof replayed.  Proofs that are not shipped are
                             reported as NOT PRESENT with a pointer to REGENERATE.md; they are
                             not counted as checked.
  4. lemma_b_check.py        the two list hypotheses that carry the extended-code lower bound to
                             the d-round detector error model.
  5. tamper_demo.py          (full mode only) fifteen corruptions of the d = 3 direct certificate,
                             each of which must be rejected by the check its label names.  This
                             negative-control battery starts the checker in child processes;
                             nothing on the verification path does.
Exit status is 0 only if nothing failed.  A missing proof is not a failure, but the summary then
lists the lower bounds that this run did not check.  Under python -O (or with PYTHONOPTIMIZE set),
which strips assert statements, this script and every checker it runs refuse to run.
"""
import json, os, runpy, sys, time
if not __debug__: sys.exit("run_all.py: refusing to run with Python optimisation on (-O, -OO or PYTHONOPTIMIZE): its checks rely on assert statements, which optimisation strips. Run it without -O and with PYTHONOPTIMIZE unset.")
HERE = os.path.dirname(os.path.abspath(__file__))
CERTS = os.path.join(HERE, "certs")
sys.path.insert(0, CERTS)
import check_dcirc as cd          # noqa: E402
import lemma_b_check as lb        # noqa: E402

FAST_OBJECT_MAX_BYTES = 400_000
FAST_PROOF_MAX_BYTES = 5_000_000


def main():
    fast = "--fast" in sys.argv[1:]
    t0 = time.perf_counter()
    fails, missing, done = [], [], {"object": 0, "witness": 0, "lower": 0, "lemma": 0}
    names = sorted(os.listdir(CERTS))

    print("== 1. objects re-derived from circuit text ==")
    for f in names:
        if not (f.startswith("m_") and f.endswith(".json")):
            continue
        p = os.path.join(CERTS, f)
        if fast and os.path.getsize(p) > FAST_OBJECT_MAX_BYTES:
            print(f"SKIP (--fast) object {f}")
            continue
        rec = json.load(open(p))
        cp = os.path.join(CERTS, rec.get("circuit_file", "c_" + f[2:-5] + ".stim"))
        try:
            cd.check_object(p, cp); done["object"] += 1
        except Exception as e:                      # noqa: BLE001
            print(f"FAIL object {f}: {type(e).__name__}: {e}"); fails.append(f)

    print("== 2. witnesses (upper bounds) ==")
    for f in names:
        if f.startswith("witness_") and f.endswith(".json"):
            try:
                cd.check_witness(os.path.join(CERTS, f)); done["witness"] += 1
            except Exception as e:                  # noqa: BLE001
                print(f"FAIL witness {f}: {type(e).__name__}: {e}"); fails.append(f)

    print("== 3. LRAT refutations (lower bounds) ==")
    for f in names:
        if not (f.startswith("lower_") and f.endswith(".json")):
            continue
        c = json.load(open(os.path.join(CERTS, f)))
        proof = os.path.join(CERTS, c["lrat_file"])
        if not os.path.exists(proof):
            print(f"NOT PRESENT {c['lrat_file']} (lower bound of {f} not checked here; see REGENERATE.md)")
            missing.append(f)
            continue
        if fast and os.path.getsize(proof) > FAST_PROOF_MAX_BYTES:
            print(f"SKIP (--fast) {f}")
            continue
        try:
            cd.check_lower(os.path.join(CERTS, f)); done["lower"] += 1
        except Exception as e:                      # noqa: BLE001
            print(f"FAIL lower {f}: {type(e).__name__}: {e}"); fails.append(f)

    print("== 4. list hypotheses of the extended-code reduction ==")
    for d, r in lb.PAIRS:
        need = [f"m_d{d}_r{r}.json", f"c_d{d}_r{r}.stim", f"m_Xext_d{d}.json"]
        if not all(os.path.exists(os.path.join(CERTS, x)) for x in need):
            continue
        if fast and os.path.getsize(os.path.join(CERTS, need[0])) > FAST_OBJECT_MAX_BYTES:
            print(f"SKIP (--fast) hypotheses d={d} r={r}")
            continue
        try:
            if lb.run(CERTS, d, r):
                done["lemma"] += 1
            else:
                fails.append(f"hypotheses d={d} r={r}")
        except Exception as e:                      # noqa: BLE001
            print(f"FAIL hypotheses d={d} r={r}: {type(e).__name__}: {e}"); fails.append(f"hypotheses d={d} r={r}")

    if not fast:
        print("== 5. tamper battery (negative controls, d3_r3) ==")
        argv = sys.argv
        try:
            sys.argv = [os.path.join(CERTS, "tamper_demo.py"), "d3_r3"]
            runpy.run_path(sys.argv[0], run_name="__main__")
        except SystemExit as e:
            if e.code not in (0, None):
                fails.append("tamper battery")
        finally:
            sys.argv = argv

    s = time.perf_counter() - t0
    print("== summary ==")
    print(f"objects re-derived: {done['object']}, witnesses checked: {done['witness']}, "
          f"proofs replayed: {done['lower']}, hypothesis checks: {done['lemma']}")
    if missing:
        print("lower bounds NOT checked by this run (proof not present; see REGENERATE.md): " + ", ".join(missing))
    if fails:
        print(f"FAILED ({len(fails)}): " + ", ".join(fails) + f"   [{s:.1f} s]")
        sys.exit(1)
    print(f"ALL PRESENT CERTIFICATES PASSED{' (fast subset)' if fast else ''} in {s:.1f} s")


if __name__ == "__main__":
    main()
