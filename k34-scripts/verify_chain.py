#!/usr/bin/env python3
"""Whole-chain check for the r(I_3,L_4) result.

A driver of the same pipeline, not an independent check: it runs verify_witness.py,
audit_cnf.py and lrat_check.py from its own folder by subprocess. (Until the correction
of 2026-11-17 this line read "FINAL INDEPENDENT VERIFICATION ORCHESTRATOR".)

Re-derives the entire proof obligation from first principles and checks that
every required artifact exists, audits cleanly, and is certified:

Theorem chain for the upper bound r(I_3,L_4) <= 21+delta (whichever layers are
present and fully UNSAT):
  T1. r(I_3,L_3)=9: pure (3,3,9) UNSAT [validation/t339] + witness_bermond8.
  T2. r(I_2,L_4)=8: pure (2,4,8) UNSAT [validation/t248] + witness_qr7.
  T3. In any {I_3,L_4}-free D, for each v: N+(v)/N-(v) induce {I_3,L_3}-free
      graphs, I(v) induces an {I_2,L_4}-free graph (tournament, TT_4-free).
      With T1,T2: d+(v)<=8, d-(v)<=8, |I(v)|<=7.   [Lemma 3.1 of the note, k34-paper/]
  T4. Hence on N vertices, vertex 0 has a type (p,q,s), p+q+s=N-1, p,q<=8, s<=7.
      Arc reversal preserves the family and maps type (p,q,s) to (q,p,s), so
      types with p<=q suffice.
  T5. Block inventories (complete up to isomorphism, doubly enumerated):
      {I_3,L_3}-free: 8 vertices: 1 class (Bermond); 7: 7; 6: 31; 5: 25.
      TT_4-free tournaments: 7: 1 (QR_7); 6: 1; 5: 3; 4: 3.
  T6. For layer N: for EVERY type (p<=q) and EVERY choice of block classes, the
      cube CNF (pure encoding + units fixing the blocks) is UNSAT (certified).
      => no {I_3,L_4}-free graph on N vertices.
Lower bound: verified witness JSON on N0 vertices => r >= N0+1.

This script: (1) verifies the witnesses via verify_witness.py; (2) audits every
cube CNF via audit_cnf.py (which rebuilds the expected clause set itself, importing
nothing from the generators, and re-checks each block's defining property); (3) confirms CERTLOG.txt has
VERIFIED for every cube with matching SHA256 of the CNF, and that the gzipped
proof's SHA256 matches the log; (4) re-derives the required cube list and fails
if any expected cube is missing. Exit 0 = entire chain verified.
"""
import gzip, hashlib, os, subprocess, sys

H = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable

I3L3 = {8: ["witness_bermond8.json"],
        7: ["blocks_i3l3_7_class%d.json" % i for i in range(7)],
        6: ["blocks_i3l3_6_class%d.json" % i for i in range(31)],
        5: ["blocks_i3l3_5_class%d.json" % i for i in range(25)]}
TT4F = {7: ["witness_qr7.json"],
        6: ["blocks_tt4f_6_class0.json"],
        5: ["blocks_tt4f_5_class%d.json" % k for k in range(3)],
        4: ["blocks_tt4f_4_class%d.json" % k for k in range(3)]}


def cube_name(N, p, q, s, i, j, k):
    if N == 24:
        return "s2434"
    if N == 23:
        if (p, q, s) == (7, 8, 7):
            return "s23_a%d" % i
        if (p, q, s) == (8, 8, 6):
            return "s23_c"
    if N == 22:
        if (p, q, s) == (6, 8, 7):
            return "s22_A%d" % i
        if (p, q, s) == (7, 7, 7):
            return "s22_B%d_%d" % (i, j)
        if (p, q, s) == (7, 8, 6):
            return "s22_C%d" % i
        if (p, q, s) == (8, 8, 5):
            return "s22_D%d" % k
    if N == 21:
        if (p, q, s) == (8, 8, 4):
            return "s21_884_%d" % k
        if (p, q, s) == (7, 8, 5):
            return "s21_785_%d_%d" % (i, k)
        if (p, q, s) == (6, 8, 6):
            return "s21_686_%d" % i
        if (p, q, s) == (7, 7, 6):
            return "s21_776_%d_%d" % (i, j)
        if (p, q, s) == (5, 8, 7):
            return "s21_587_%d" % i
        if (p, q, s) == (6, 7, 7):
            return "s21_677_%d_%d" % (i, j)
    raise KeyError((N, p, q, s))


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def sha_gz(path):
    h = hashlib.sha256()
    with gzip.open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def certlog():
    recs = {}
    for line in open(os.path.join(H, "CERTLOG.txt")):
        t = line.split()
        if not t:
            continue
        base = t[0]
        ok = "VERIFIED:" in line
        fields = dict(p.strip().split("=") for p in line.split("|")[1:]
                      if "=" in p)
        recs[base] = (ok, fields.get("cnf_sha256", "").strip(),
                      fields.get("lrat_sha256", "").strip())
    return recs


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout or r.stderr) else ""


def main():
    layers = [int(x) for x in sys.argv[1:]] or [24, 23, 22]
    fails = []
    log = certlog()

    # foundational certs T1,T2 (verify anew from disk)
    for name, cnf, lrat, args in [
            ("T1 r(I_3,L_3)<=9", "validation/t339.cnf", "validation/t339.lrat", ["pure", "3", "3", "9"]),
            ("T2 r(I_2,L_4)<=8", "validation/t248.cnf", "validation/t248.lrat", ["pure", "2", "4", "8"])]:
        ok1, m1 = run([PY, os.path.join(H, "audit_cnf.py")] + args + [os.path.join(H, cnf)])
        ok2, m2 = run([PY, os.path.join(H, "lrat_check.py"), os.path.join(H, cnf), os.path.join(H, lrat)])
        print("%s: audit=%s lrat=%s" % (name, "PASS" if ok1 else "FAIL", m2[:60]))
        if not (ok1 and ok2):
            fails.append(name)
    for w in ["witness_bermond8.json", "witness_qr7.json"]:
        ok, m = run([PY, os.path.join(H, "verify_witness.py"), os.path.join(H, w)])
        print("%s: %s" % (w, m[:70]))
        if not ok:
            fails.append(w)

    for N in layers:
        total = 0
        for p in range(max(0, N - 16), 9):
            for q in range(p, 9):
                s = N - 1 - p - q
                if not (0 <= s <= 7):
                    continue
                if p not in I3L3 or q not in I3L3 or s not in TT4F:
                    fails.append("layer %d: missing inventory for type %s" % (N, (p, q, s)))
                    continue
                for i, pf in enumerate(I3L3[p]):
                    for j, qf in enumerate(I3L3[q]):
                        for k, sf in enumerate(TT4F[s]):
                            base = cube_name(N, p, q, s, i, j, k)
                            total += 1
                            cnf = os.path.join(H, base + ".cnf")
                            if not os.path.exists(cnf):
                                fails.append(base + ": cnf missing")
                                continue
                            ok, m = run([PY, os.path.join(H, "audit_cnf.py"), "cube",
                                         str(N), str(p), str(q), str(s),
                                         os.path.join(H, pf), os.path.join(H, qf),
                                         os.path.join(H, sf), cnf])
                            if not ok:
                                fails.append(base + ": AUDIT " + m)
                                continue
                            rec = log.get(base)
                            if not rec or not rec[0]:
                                fails.append(base + ": no VERIFIED certlog entry")
                                continue
                            if rec[1] != sha(cnf):
                                fails.append(base + ": cnf sha mismatch vs certlog")
                                continue
                            gz = os.path.join(H, base + ".lrat.gz")
                            if os.path.exists(gz):
                                if sha_gz(gz) != rec[2]:
                                    fails.append(base + ": lrat sha mismatch")
                            elif os.path.exists(os.path.join(H, base + ".lrat")):
                                if sha(os.path.join(H, base + ".lrat")) != rec[2]:
                                    fails.append(base + ": lrat sha mismatch")
                            else:
                                fails.append(base + ": proof file missing")
        print("layer N=%d: %d cubes required, %d problems" %
              (N, total, len([f for f in fails if f.startswith("s")])))

    if fails:
        print("CHAIN INCOMPLETE / FAILURES:")
        for f in fails:
            print("  -", f)
        return 1
    print("CHAIN FULLY VERIFIED for layers %s" % layers)
    return 0


if __name__ == "__main__":
    sys.exit(main())
