#!/usr/bin/env python3
"""purex_from_object.py -- the X-PART SUB-LIST of a detector-error-model object (standard library).

For a CSS memory experiment with Z-type detectors (which see X errors and the Z observable) and X-type
detectors (which see Z errors), the X-part of any fault flips only Z-type detectors and the observable,
and its Z-part flips only X-type detectors.  Replacing every fault of an undetectable logical fault set
by its X-part gives an undetectable logical fault set of no greater weight (Z-detector flips and the
observable flip are unchanged, X-detector flips vanish).  Hence the minimum is attained on the sub-list
M_Z = { m in M : dets(m) subset of Z-type detectors }, and d_circ(M) = d_circ(M_Z).
HYPOTHESIS the checker verifies: for every m in M, its projection (dets(m) restricted to Z-type
detectors, obs(m)) is a member of M_Z or is empty; and M_Z is exactly that subset of M.
Z-type detectors are read from the circuit text: DETECTOR(x, y, t, 2, c) (pauli coordinate 2); X-type
have pauli coordinate 4.  Detector index = order of DETECTOR instructions.
Usage: purex_from_object.py m_dX_rY.json c_dX_rY.stim out.json
"""
import hashlib, json, os, re, sys
if not __debug__: sys.exit("purex_from_object.py: refusing to run with Python optimisation on (-O, -OO or PYTHONOPTIMIZE): its checks rely on assert statements, which optimisation strips. Run it without -O and with PYTHONOPTIMIZE unset.")
def z_detectors(circuit_path):
    zs = set(); i = 0
    for raw in open(circuit_path):
        line = raw.split("#", 1)[0].strip()
        if not line.startswith("DETECTOR"):
            continue
        m = re.match(r"^DETECTOR\(([^)]*)\)", line)
        args = [float(a) for a in m.group(1).split(",")] if m else []
        if len(args) >= 4 and int(args[3]) == 2:
            zs.add(i)
        i += 1
    return zs, i

def build(mpath, cpath):
    rec = json.load(open(mpath))
    zs, n = z_detectors(cpath)
    assert n == rec["num_detectors"], "detector count mismatch between object and circuit text"
    sub = [m for m in rec["mechanisms"] if all(d in zs for d in m["dets"])]
    keys = {(tuple(m["dets"]), tuple(m["obs"])) for m in sub}
    bad = 0
    for m in rec["mechanisms"]:
        proj = (tuple(d for d in m["dets"] if d in zs), tuple(m["obs"]))
        if (proj[0] or proj[1]) and proj not in keys:
            bad += 1
    h = hashlib.sha256()
    for m in sub:
        h.update((",".join(map(str, m["dets"])) + ":" + ",".join(map(str, m["obs"])) + "\n").encode())
    out = {"kind": "purex_sublist", "d": rec["d"], "rounds": rec["rounds"], "noise_model": rec["noise_model"],
           "p": rec.get("p"), "parent_object": os.path.basename(mpath), "parent_mechanism_list_sha256": rec["mechanism_list_sha256"],
           "circuit_file": rec.get("circuit_file", "c_d%d_r%d.stim" % (rec["d"], rec["rounds"])), "circuit_sha256": rec["circuit_sha256"],
           "num_detectors": rec["num_detectors"], "num_z_detectors": len(zs), "num_observables": 1,
           "num_parent_mechanisms": len(rec["mechanisms"]), "num_mechanisms": len(sub),
           "projections_outside_sublist": bad, "mechanism_list_sha256": h.hexdigest(),
           "mechanism_hash_spec": rec["mechanism_hash_spec"],
           "definition": "mechanisms of the parent object whose detector sets lie within the Z-type detectors (pauli coordinate 2); d_circ(parent) = d_circ(sub-list) by the X-part lemma, whose hypothesis (every parent mechanism's Z-projection is in the sub-list or empty) is checked here and by check_dcirc.py",
           "mechanisms": sub}
    return out

if __name__ == "__main__":
    out = build(sys.argv[1], sys.argv[2])
    if len(sys.argv) > 3:
        json.dump(out, open(sys.argv[3], "w"))
    print(f"pure-X sub-list: d={out['d']} rounds={out['rounds']} {out['num_mechanisms']}/{out['num_parent_mechanisms']} mechanisms, "
          f"Z-detectors {out['num_z_detectors']}/{out['num_detectors']}, projections outside sub-list: {out['projections_outside_sublist']}, sha256 {out['mechanism_list_sha256'][:16]}")
