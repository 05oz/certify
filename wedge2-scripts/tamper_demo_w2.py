#!/usr/bin/env python3
"""Tamper controls for check_wedge2.py.  Python 3 standard library only.

Takes a certificate that passes, applies eight distinct corruptions -- each
targeting a different verification gate -- and confirms the checker rejects
every one (nonzero exit / CHECK FAIL) while the pristine certificate still
passes.  Runs the checker IN PROCESS (no subprocesses, no signals).

Usage:  python3 tamper_demo_w2.py check_wedge2.py certificate.json
"""
import copy
import io
import json
import sys
import contextlib


def run_checker(checker_path, cert_obj, tmpname):
    json.dump(cert_obj, open(tmpname, "w"))
    src = open(checker_path).read()
    glb = {"__name__": "__main__", "__file__": checker_path}
    argv0 = sys.argv
    sys.argv = [checker_path, tmpname]
    buf = io.StringIO()
    code = 0
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(src, checker_path, "exec"), glb)
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else 1
    finally:
        sys.argv = argv0
    out = buf.getvalue()
    passed = (code == 0 and out.rstrip().endswith("CHECK PASS"))
    return passed, out


def main():
    checker, certf = sys.argv[1], sys.argv[2]
    base = json.load(open(certf))
    tmp = certf + ".tamper.tmp.json"

    ok, _ = run_checker(checker, base, tmp)
    if not ok:
        print("BASELINE FAILED -- pristine certificate does not pass")
        sys.exit(1)
    print("baseline: pristine certificate -> CHECK PASS")

    def t1(c):  # flip one A_w count
        c["A_w_full_spectrum"]["5"] = str(int(c["A_w_full_spectrum"]["5"]) + 1)
    def t2(c):  # perturb one mechanism probability
        c["mechanisms"][3]["p_num"] += 1
    def t3(c):  # and with a recomputed hash, so the hash gate alone is bypassed
        import hashlib
        c["mechanisms"][3]["p_num"] += 1
        lines = ["%d:%d:%d/%d" % (mm["det"], mm["obs"], mm["p_num"], mm["p_den"])
                 for mm in c["mechanisms"]]
        c["mechanism_list_sha256"] = hashlib.sha256(
            ("\n".join(lines) + "\n").encode()).hexdigest()
    def t4(c):  # alter the exact P_L numerator's last digit
        nn = c["P_L_exact"]["num"]
        c["P_L_exact"]["num"] = nn[:-1] + ("0" if nn[-1] != "0" else "1")
    def t5(c):  # swap the observable bit of one mechanism (breaks order/hash/counts)
        c["mechanisms"][7]["obs"] ^= 1
    def t6(c):  # claim a different circuit-level distance
        c["circuit_level_distance"] += 1
    def t7(c):  # corrupt one N_w entry
        c["N_w_logical_spectrum"]["6"] = str(int(c["N_w_logical_spectrum"]["6"]) + 2)
    def t8(c):  # shift the cited v1 bracket so containment fails
        L = c["v1_reference"]["bracket_L"].split("/")
        c["v1_reference"]["bracket_L"] = "%d/%s" % (int(L[0]) * 3, L[1])
        c["v1_reference"]["bracket_U"] = "%d/%s" % (int(L[0]) * 4, L[1])

    tampers = [("A_w count flipped", t1),
               ("probability perturbed (hash gate)", t2),
               ("probability perturbed, hash recomputed (count/P_L gate)", t3),
               ("P_L numerator altered", t4),
               ("observable bit swapped", t5),
               ("distance overstated", t6),
               ("N_w entry corrupted", t7),
               ("v1 bracket shifted (containment gate)", t8)]
    rejected = 0
    for name, t in tampers:
        c = copy.deepcopy(base)
        t(c)
        ok, out = run_checker(checker, c, tmp)
        verdict = "REJECTED" if not ok else "ACCEPTED (BAD!)"
        line = [l for l in out.splitlines() if l.startswith("CHECK FAIL")]
        print("tamper: %-55s -> %s  %s" % (name, verdict, line[0] if line else ""))
        rejected += (not ok)
    import os
    os.remove(tmp)
    if rejected == len(tampers):
        print("ALL %d TAMPER CONTROLS REJECTED" % len(tampers))
    else:
        print("TAMPER DEMO FAILED: %d/%d rejected" % (rejected, len(tampers)))
        sys.exit(1)


if __name__ == "__main__":
    main()
