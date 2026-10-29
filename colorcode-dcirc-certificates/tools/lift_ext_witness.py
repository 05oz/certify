#!/usr/bin/env python3
"""lift_ext_witness.py -- GENERATOR (untrusted): turn an extended-code witness into an explicit fault
set of the detector error model of C(d, r).  Python standard library only.

For each column of the extended-code witness, pick the lowest-index mechanism of M(d, r) that
  * touches only Z-type detectors,
  * flips detectors of a single round L only, each check's detector at most once, and
  * projects (per-check parity over all rounds, observable bit) exactly onto that column.
All picks use the same round L (the smallest round in which every needed column is realised).
Within one round each check's detector is flipped once per picked mechanism whose column contains
that check, so the XOR of the picks flips no detector because the columns XOR to zero, and flips the
observable because the columns do.  This file only proposes the set; the claim is checked by
`check_dcirc.py witness`, which XORs the listed mechanisms against M(d, r) and trusts nothing here.

Usage:  python3 tools/lift_ext_witness.py CERTDIR d r ext_witness.json out_witness.json
        (on Windows: py tools/lift_ext_witness.py ...)
"""
import collections, json, os, re, sys


def geometry(path):
    qc = {}; dets = []; shift = []; first_m = None
    for raw in open(path):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        mm = re.match(r"^([A-Z_0-9]+)(?:\(([^)]*)\))?\s*(.*)$", line)
        name, args, rest = mm.group(1), mm.group(2), mm.group(3)
        vals = [float(a) for a in args.split(",")] if args else []
        if name == "QUBIT_COORDS":
            qc[int(rest.split()[0])] = tuple(vals)
        elif name == "SHIFT_COORDS":
            shift += [0.0] * max(0, len(vals) - len(shift))
            for i, v in enumerate(vals):
                shift[i] += v
        elif name == "DETECTOR":
            dets.append(tuple(v + (shift[i] if i < len(shift) else 0.0) for i, v in enumerate(vals)))
        elif name == "M" and first_m is None:
            first_m = [int(t) for t in rest.split()]
    return first_m, qc, dets


def main():
    base, d, r, wpath, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
    mfile = f"m_d{d}_r{r}.json"
    rec = json.load(open(os.path.join(base, mfile)))
    w = json.load(open(wpath))
    want = [(tuple(m["dets"]), tuple(m["obs"])) for m in w["mechanisms"]]
    anc, qc, coords = geometry(os.path.join(base, rec.get("circuit_file", f"c_d{d}_r{r}.stim")))
    check_of_xy = {qc[q][:2]: k for k, q in enumerate(anc)}
    zinfo = {i: (check_of_xy[(co[0], co[1])], int(co[2])) for i, co in enumerate(coords) if int(co[3]) == 2}
    pick = collections.defaultdict(dict)        # round -> column -> lowest mechanism index
    for j, m in enumerate(rec["mechanisms"]):
        if not m["dets"] or any(x not in zinfo for x in m["dets"]):
            continue
        par = collections.Counter(zinfo[x][0] for x in m["dets"])
        layers = {zinfo[x][1] for x in m["dets"]}
        if len(layers) != 1 or any(v != 1 for v in par.values()):
            continue
        col = (tuple(sorted(par)), tuple(m["obs"]))
        L = next(iter(layers))
        pick[L].setdefault(col, j)
    rounds = sorted(L for L in pick if all(c in pick[L] for c in want))
    assert rounds, "no single round realises every column of the witness"
    L = rounds[0]
    idx = sorted(pick[L][c] for c in want)
    assert len(set(idx)) == len(idx)
    mechs = [rec["mechanisms"][j] for j in idx]
    dx = set(); ob = 0
    for m in mechs:
        dx ^= set(m["dets"]); ob ^= 1 if m["obs"] else 0
    assert not dx and ob == 1, "lifted set is not an undetectable logical (generator bug)"
    res = {"kind": "dcirc_upper", "d": d, "rounds": r, "noise_model": rec["noise_model"],
           "mechanism_file": mfile, "mechanism_list_sha256": rec["mechanism_list_sha256"],
           "weight": len(idx), "mechanism_indices": idx, "mechanisms": mechs,
           "lifted_from": os.path.basename(wpath), "lift_round": L,
           "statement": f"d_circ <= {len(idx)}: the listed fault mechanisms flip no detector and flip observable 0"}
    json.dump(res, open(out, "w"), indent=1)
    print(f"lifted {os.path.basename(wpath)} -> {os.path.basename(out)}: weight {len(idx)}, round {L} "
          f"(rounds realising all columns: {rounds})")


if __name__ == "__main__":
    main()
