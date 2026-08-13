#!/usr/bin/env python3
"""Tamper battery for Part M (certified ZEFOZ brackets).  Standard library only.

Runs the shipped checker (zefoz-certificates/zefoz_checker2.py) against six
corrupted copies of the certificate and confirms each is rejected with a
nonzero exit code.  An untampered control (same slimming, no corruption) must
pass.  For speed each copy keeps the time-reversal object plus one Krawczyk
point; every corruption targets material the checker re-derives from first
principles, so rejection happens at the mathematical layer (there is no hash
layer in this certificate).

Battery:
  T1  Hessian eigenvalue bracket shifted off the recomputed enclosure
  T2  gradient enclosure shifted (both endpoints, width preserved) so the
      recomputed one escapes
  T3  LDL^T inertia count corrupted at one shift
  T4  one sign of the time-reversal matrix M16 flipped
  T5  gradient-norm bound eps understated below the recomputed bound
  T6  Krawczyk box radius inflated so the contraction genuinely fails

Usage:  python3 tamper_demo.py [path/to/certificate2.json]
"""
import copy
import json
import os
import subprocess
import sys
from fractions import Fraction as F

_here = os.path.dirname(os.path.abspath(__file__))
CERTDIR = None
for cand in (os.path.join(_here, "..", "zefoz-certificates"), _here):
    if os.path.exists(os.path.join(cand, "zefoz_checker2.py")):
        CERTDIR = cand
        break
CHECKER = os.path.join(CERTDIR, "zefoz_checker2.py")
CERT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(CERTDIR, "certificate2.json")
TMP = os.path.join(_here, "_tamper_tmp.json")


def fs(x):
    return "%d/%d" % (x.numerator, x.denominator)


def slim(cert):
    tr = next(p for p in cert["points"] if p.get("kind") == "time_reversal_identity")
    zp = next(p for p in cert["points"] if p.get("kind") == "zefoz_point")
    out = {k: cert[k] for k in ("meta", "constants", "sqrt_enclosures", "sites")}
    out["points"] = [copy.deepcopy(tr), copy.deepcopy(zp)]
    return out


def run(cert, label, expect_pass=False):
    json.dump(cert, open(TMP, "w"))
    r = subprocess.run([sys.executable, CHECKER, TMP], capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip().splitlines()
    verdict = out[-1] if out else "(no output)"
    ok = (r.returncode == 0) if expect_pass else (r.returncode != 0)
    print("[%s] %-44s exit=%d  %s" % ("OK" if ok else "BAD", label, r.returncode,
                                      verdict[:90]))
    return ok


def main():
    full = json.load(open(CERT))
    results = []

    c = slim(full)
    results.append(run(c, "control (untampered, slimmed)", expect_pass=True))

    c = slim(full)
    q = c["points"][1]["pairs"][0]
    lo, hi = q["hessian_eig_brackets_MHz_per_mT2"][0]
    q["hessian_eig_brackets_MHz_per_mT2"][0] = [fs(F(lo) + F(1, 10**5)),
                                               fs(F(hi) + F(1, 10**5))]
    results.append(run(c, "T1 Hessian eigenvalue bracket shifted"))

    c = slim(full)
    ge = c["points"][1]["pairs"][0]["gradient_enclosure_MHz_per_mT"]
    ge[0] = [fs(F(ge[0][0]) + F(1, 10**30)), fs(F(ge[0][1]) + F(1, 10**30))]
    results.append(run(c, "T2 gradient enclosure shifted"))

    c = slim(full)
    c["points"][1]["shifts"][5]["neg_count"] += 1
    results.append(run(c, "T3 inertia count corrupted"))

    c = slim(full)
    M = c["points"][0]["M16"]
    for a in range(16):
        if M[0][a] != 0:
            M[0][a] = -M[0][a]
            break
    results.append(run(c, "T4 time-reversal sign flipped"))

    c = slim(full)
    c["points"][1]["pairs"][0]["grad_norm_upper_MHz_per_mT"] = "1/" + str(10**60)
    results.append(run(c, "T5 gradient-norm bound understated"))

    c = slim(full)
    c["points"][1]["pairs"][0]["krawczyk"]["box_radius_mT"] = "1/1024"
    results.append(run(c, "T6 Krawczyk radius inflated"))

    try:
        os.remove(TMP)
    except OSError:
        pass
    if all(results):
        print("TAMPER BATTERY PASS (control passes; all six tampers rejected)")
        return 0
    print("TAMPER BATTERY FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
