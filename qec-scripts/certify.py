#!/usr/bin/env python3
"""certify.py -- certificate-producing pipeline.

For a target code and sector, produce:
  UPPER bound: a witness JSON (explicit logical operator + co-witness),
    found via a cadical SAT call at weight K = d_target.
  LOWER bound: cadical UNSAT run at weight K = d_target - 1 with
    --lrat --no-binary, yielding an LRAT proof + certificate JSON.
All artifacts land in certificates/<name>/. Timings recorded in meta.json.
"""
import json, os, subprocess, sys, time
import numpy as np
import qec_lib as Q

HERE = os.path.dirname(os.path.abspath(__file__))
CERTS = os.path.join(HERE, "certificates")
CADICAL = "/opt/homebrew/bin/cadical"


def run_cadical(cnf_path, lrat_path=None, timeout=None):
    cmd = [CADICAL, "-q"]
    if lrat_path:
        cmd += ["--unsat", "--lrat", "--no-binary", cnf_path, lrat_path]
    else:
        cmd += ["--sat", cnf_path]
    t0 = time.perf_counter()
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    dt = time.perf_counter() - t0
    return r.returncode, r.stdout, dt      # 10 SAT, 20 UNSAT


def parse_model(stdout):
    lits = []
    for line in stdout.splitlines():
        if line.startswith("v "):
            lits += [int(t) for t in line[2:].split()]
    return {abs(l): l > 0 for l in lits if l != 0}


def prep_dir(name):
    d = os.path.join(CERTS, name)
    os.makedirs(d, exist_ok=True)
    return d


def log_event(certdir, ev):
    mp = os.path.join(certdir, "meta.json")
    meta = json.load(open(mp))
    meta["events"].append(ev)
    with open(mp, "w") as f:
        json.dump(meta, f, indent=1)


def css_init(name, HX, HZ, d_published=None):
    d = prep_dir(name)
    Q.save_matrix(HX, os.path.join(d, "HX.txt"))
    Q.save_matrix(HZ, os.path.join(d, "HZ.txt"))
    n = HX.shape[1]
    k = n - Q.rank(HX) - Q.rank(HZ)
    LX, LZ = Q.css_logical_reps(HX, HZ)
    Q.save_matrix(LZ, os.path.join(d, "pairing_X.txt"))   # X-logicals pair vs Z-reps
    Q.save_matrix(LX, os.path.join(d, "pairing_Z.txt"))
    with open(os.path.join(d, "meta.json"), "w") as f:
        json.dump(dict(name=name, n=int(n), k=int(k),
                       d_published=d_published, events=[]), f, indent=1)
    print(f"[{name}] n={n} k={k} (published d={d_published})", flush=True)


def load_pairing(certdir, sector):
    path = os.path.join(certdir, f"pairing_{sector}.txt")
    with open(path) as fh:
        rows, cols = map(int, fh.readline().split())
        return np.array([[int(c) for c in fh.readline().strip()]
                         for _ in range(rows)], np.uint8)


def css_upper(name, HX, HZ, sector, K, timeout=None):
    """SAT call at weight K; emit witness JSON if satisfiable."""
    d = prep_dir(name)
    Hc = HZ if sector == "X" else HX
    L = load_pairing(d, sector)
    cnf = Q.build_css_cnf(Hc, L, K)
    cnfp = os.path.join(d, f"upper_{sector}_K{K}.cnf")
    Q.write_dimacs(cnf, cnfp)
    rc, out, dt = run_cadical(cnfp, timeout=timeout)
    if rc != 10:
        print(f"[{name}] upper {sector} K={K}: NOT SAT (rc={rc}) in {dt:.1f}s", flush=True)
        return None
    model = parse_model(out)
    n = HX.shape[1]
    x = np.array([1 if model.get(i + 1) else 0 for i in range(n)], np.uint8)
    z = None
    for row in L:
        if int(x @ row.astype(int)) % 2 == 1:
            z = row
            break
    assert z is not None, "model does not pair with any pairing row?!"
    w = int(x.sum())
    cert = dict(kind="css_upper", sector=sector, HX_file="HX.txt",
                HZ_file="HZ.txt", weight=w,
                x=[int(v) for v in x], z=[int(v) for v in z])
    wp = os.path.join(d, f"witness_{sector}.json")
    with open(wp, "w") as f:
        json.dump(cert, f)
    log_event(d, dict(what=f"upper_{sector}", K=K, weight=w, solver_s=round(dt, 3)))
    print(f"[{name}] upper {sector}: weight-{w} logical in {dt:.1f}s -> {os.path.basename(wp)}", flush=True)
    return w


def css_lower(name, HX, HZ, sector, K, symmetry=None, timeout=None):
    """UNSAT proof that no nontrivial logical of weight <= K exists.
    symmetry: None or dict(perms=[perm_arrays], block=lm)."""
    d = prep_dir(name)
    Hc = HZ if sector == "X" else HX
    L = load_pairing(d, sector)
    instances = []
    if symmetry is None:
        forced_sets = [[]]
    else:
        block = symmetry["block"]
        forced_sets = [[1], [-(i + 1) for i in range(block)] + [block + 1]]
        for gi, p in enumerate(symmetry["perms"]):
            with open(os.path.join(d, f"perm_{gi}.txt"), "w") as f:
                f.write(" ".join(map(str, p)) + "\n")
    total = 0.0
    for idx, forced in enumerate(forced_sets):
        tag = f"lower_{sector}_K{K}" + (f"_i{idx}" if symmetry else "")
        cnf = Q.build_css_cnf(Hc, L, K, forced)
        cnfp = os.path.join(d, tag + ".cnf")
        lratp = os.path.join(d, tag + ".lrat")
        Q.write_dimacs(cnf, cnfp)
        rc, out, dt = run_cadical(cnfp, lratp, timeout=timeout)
        total += dt
        if rc != 20:
            print(f"[{name}] lower {sector} K={K} inst{idx}: rc={rc} after {dt:.1f}s -- ABORT", flush=True)
            return False
        print(f"[{name}] lower {sector} K={K} inst{idx}: UNSAT in {dt:.1f}s, "
              f"LRAT {os.path.getsize(lratp)} bytes", flush=True)
        instances.append(dict(forced=forced, cnf_file=os.path.basename(cnfp),
                              lrat_file=os.path.basename(lratp)))
    cert = dict(kind="css_lower", sector=sector, K=K, HX_file="HX.txt",
                HZ_file="HZ.txt", pairing_file=f"pairing_{sector}.txt",
                instances=instances,
                symmetry=(dict(perm_files=[f"perm_{i}.txt" for i in
                                           range(len(symmetry["perms"]))],
                               block=symmetry["block"]) if symmetry else None))
    cp = os.path.join(d, f"lower_{sector}_K{K}" + ("_sym" if symmetry else "") + ".json")
    with open(cp, "w") as f:
        json.dump(cert, f, indent=1)
    log_event(d, dict(what=f"lower_{sector}", K=K, solver_s=round(total, 3),
                      lrat_bytes=[os.path.getsize(os.path.join(d, i["lrat_file"]))
                                  for i in instances]))
    print(f"[{name}] lower {sector}: d_{sector} >= {K + 1} certified "
          f"(solver {total:.1f}s) -> {os.path.basename(cp)}", flush=True)
    return True


def stab_target_five_qubit():
    name = "five_qubit"
    d = prep_dir(name)
    S, L, n = Q.five_qubit()
    Q.save_matrix(S, os.path.join(d, "S.txt"))
    Q.save_matrix(L, os.path.join(d, "pairing.txt"))
    with open(os.path.join(d, "meta.json"), "w") as f:
        json.dump(dict(name=name, n=n, k=1, d_published=3, events=[]), f, indent=1)
    # upper: SAT at K=3
    cnf = Q.build_stab_cnf(S, L, 3)
    cnfp = os.path.join(d, "upper_K3.cnf")
    Q.write_dimacs(cnf, cnfp)
    rc, out, dt = run_cadical(cnfp)
    assert rc == 10
    model = parse_model(out)
    e = [1 if model.get(i + 1) else 0 for i in range(n)] + \
        [1 if model.get(n + i + 1) else 0 for i in range(n)]

    def omega(p, q):
        return (sum(p[i] & q[n + i] for i in range(n)) +
                sum(p[n + i] & q[i] for i in range(n))) % 2
    f = None
    for row in L:
        r = [int(v) for v in row]
        if omega(e, r) == 1:
            f = r
            break
    assert f is not None
    w = sum(e[i] | e[n + i] for i in range(n))
    with open(os.path.join(d, "witness.json"), "w") as fh:
        json.dump(dict(kind="stab_upper", S_file="S.txt", weight=w, e=e, f=f), fh)
    log_event(d, dict(what="upper", K=3, weight=w, solver_s=round(dt, 3)))
    print(f"[{name}] upper: weight-{w} logical in {dt:.2f}s", flush=True)
    # lower: UNSAT at K=2
    cnf = Q.build_stab_cnf(S, L, 2)
    cnfp = os.path.join(d, "lower_K2.cnf")
    lratp = os.path.join(d, "lower_K2.lrat")
    Q.write_dimacs(cnf, cnfp)
    rc, out, dt = run_cadical(cnfp, lratp)
    assert rc == 20, f"expected UNSAT, rc={rc}"
    with open(os.path.join(d, "lower_K2.json"), "w") as fh:
        json.dump(dict(kind="stab_lower", K=2, S_file="S.txt",
                       pairing_file="pairing.txt",
                       instances=[dict(forced=[], cnf_file="lower_K2.cnf",
                                       lrat_file="lower_K2.lrat")]), fh, indent=1)
    log_event(d, dict(what="lower", K=2, solver_s=round(dt, 3),
                      lrat_bytes=[os.path.getsize(lratp)]))
    print(f"[{name}] lower: d >= 3 certified in {dt:.2f}s, "
          f"LRAT {os.path.getsize(lratp)} B", flush=True)


def get_code(name):
    if name == "steane":
        HX, HZ = Q.steane()
        return HX, HZ, 3
    if name == "golay":
        HX, HZ = Q.golay()
        return HX, HZ, 7
    if name.startswith("surface"):
        dd = int(name[len("surface"):])
        HX, HZ = Q.rotated_surface(dd)
        return HX, HZ, dd
    if name in Q.BB_PARAMS:
        p = Q.BB_PARAMS[name]
        HX, HZ = Q.bb_code(p["l"], p["m"], p["a"], p["b"])
        return HX, HZ, p["nkd"][2]
    raise SystemExit(f"unknown code {name}")


def bb_translation_perms(name):
    p = Q.BB_PARAMS[name]
    l, m = p["l"], p["m"]
    lm = l * m

    def shift(di, dj):
        perm = [0] * (2 * lm)
        for blk in (0, 1):
            for r in range(l):
                for s in range(m):
                    src = blk * lm + r * m + s
                    dst = blk * lm + ((r + di) % l) * m + ((s + dj) % m)
                    perm[src] = dst
        return perm
    return [shift(1, 0), shift(0, 1)]


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "five_qubit":
        stab_target_five_qubit()
    else:
        name = sys.argv[2]
        HX, HZ, dpub = get_code(name)
        if cmd == "init":
            css_init(name, HX, HZ, dpub)
        elif cmd == "upper":
            sector, K = sys.argv[3], int(sys.argv[4])
            css_upper(name, HX, HZ, sector, K)
        elif cmd == "lower":
            sector, K = sys.argv[3], int(sys.argv[4])
            sym = None
            if len(sys.argv) > 5 and sys.argv[5] == "sym":
                p = Q.BB_PARAMS[name]
                sym = dict(perms=bb_translation_perms(name), block=p["l"] * p["m"])
            css_lower(name, HX, HZ, sector, K, symmetry=sym)
        else:
            raise SystemExit(f"unknown cmd {cmd}")
