#!/usr/bin/env python3
"""Tamper battery for Part K (certified demag tensor).  Standard library only.

Runs the shipped checker (demag-certificates/check_demag.py) against six
corrupted copies of the certificate and confirms each is rejected nonzero, at
the hash layer and -- when the hash is recomputed to match -- at the
mathematical re-derivation layer.  A control (untampered) must pass.

Usage:  python3 tamper_demo.py [path/to/demag_certificate.json]
"""
import os
import sys
import json
import copy
import hashlib
import subprocess
from fractions import Fraction as Fr

_here = os.path.dirname(os.path.abspath(__file__))
CERTDIR = None
for cand in (os.path.join(_here, "..", "demag-certificates"), _here,
             os.path.join(_here, "..", "certificates")):
    if os.path.exists(os.path.join(cand, "check_demag.py")):
        CERTDIR = cand
        break
CHECKER = os.path.join(CERTDIR, "check_demag.py")
CERT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(CERTDIR, "demag_certificate.json")
TMP = os.path.join(_here, "_tamper_tmp.json")


def canon(e):
    return "|".join([e["cell"], e["direction"], str(e["sep_cells"]), e["component"],
                     e["N_lo"], e["N_hi"], e["naive_double"], e.get("asymp_oommf", "-")])


def rehash(cert):
    lines = [canon(e) for e in cert["entries"]]
    cert["entries_sha256"] = hashlib.sha256(("\n".join(lines) + "\n").encode()).hexdigest()


# Each checker run uses a small deterministic sample for speed; the stride
# sample always includes entry index 0, so all mutating tampers below target
# entry 0 and are re-derived.  The hash and the consistency-identity checks
# always scan every entry regardless of the sample.
SAMPLE = ["--sample", "24"]


def run(cert, label, expect_pass=False):
    json.dump(cert, open(TMP, "w"))
    r = subprocess.run([sys.executable, CHECKER, TMP] + SAMPLE, capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip().splitlines()
    verdict = out[-1] if out else "(no output)"
    ok = (r.returncode == 0) if expect_pass else (r.returncode != 0)
    print("[%s] %-40s exit=%d  %s" % ("OK" if ok else "BAD", label, r.returncode, verdict))
    return ok


def frs(f):
    return "%d/%d" % (f.numerator, f.denominator)


def main():
    base = json.load(open(CERT))
    allok = True
    allok &= run(base, "0. control (untampered)", expect_pass=True)

    def fr_of(e, k):
        return Fr(*map(int, e[k].split("/")))

    # 1. narrow to exclude truth + rehash
    c = copy.deepcopy(base); e = c["entries"][0]
    lo, hi = fr_of(e, "N_lo"), fr_of(e, "N_hi")
    e["N_hi"] = frs(lo + (hi - lo) / 4); rehash(c)
    allok &= run(c, "1. narrow enclosure + rehash")

    # 2. shift off truth + rehash
    c = copy.deepcopy(base); e = c["entries"][0]
    lo, hi = fr_of(e, "N_lo"), fr_of(e, "N_hi")
    sh = Fr(1, 1000)
    e["N_lo"] = frs(lo + sh); e["N_hi"] = frs(hi + sh); rehash(c)
    allok &= run(c, "2. shift enclosure + rehash")

    # 3. widen grossly + rehash
    c = copy.deepcopy(base); e = c["entries"][0]
    lo, hi = fr_of(e, "N_lo"), fr_of(e, "N_hi")
    e["N_lo"] = frs(lo - 1); e["N_hi"] = frs(hi + 1); rehash(c)
    allok &= run(c, "3. widen enclosure + rehash")

    # 4. corrupt naive double + rehash
    c = copy.deepcopy(base)
    c["entries"][0]["naive_double"] = (0.999).hex(); rehash(c)
    allok &= run(c, "4. corrupt naive double + rehash")

    # 5. corrupt hash only
    c = copy.deepcopy(base); c["entries_sha256"] = "0" * 64
    allok &= run(c, "5. corrupt entries_sha256")

    # 6. tamper a digit-loss claim (not in hash)
    c = copy.deepcopy(base)
    c["entries"][0]["naive_digits"]["correct_digits_lo"] = 99.0
    allok &= run(c, "6. tamper correct-digit claim")

    if os.path.exists(TMP):
        os.remove(TMP)
    print("TAMPER BATTERY", "PASS" if allok else "FAIL",
          "(control passes; all six corruptions rejected)" if allok else "")
    sys.exit(0 if allok else 1)


if __name__ == "__main__":
    main()
