#!/usr/bin/env python3
"""lemma_b_check.py -- machine check of the two list hypotheses that carry the extended-code
lower bound d_ext(d) to the detector error model of C(d, r).  Python standard library only.

This is a standard-library port (2026-10-20) of the build session's Stim-based script of the same
name.  The original read detector coordinates through stim.Circuit.get_detector_coordinates();
this version reads them from the circuit text (DETECTOR(x, y, t, pauli, colour) arguments plus the
running SHIFT_COORDS offset).  Its output lines are printed in the original's format so that the
two can be compared line by line.

Inputs, per (d, r), all in DIR: m_d{d}_r{r}.json (mechanism list M of C(d, r)), c_d{d}_r{r}.stim
(its circuit text, hash-checked against the object), m_Xext_d{d}.json (the X-sector extended code).

Hypothesis A (X-part closure).  For every mechanism m of M, its restriction to the Z-type
detectors and the observable is either empty or itself a mechanism of M_Z, the sub-list of
mechanisms that touch only Z-type detectors.  Consequence: from any undetectable logical fault set
F of M, replacing each member by its restriction and cancelling repeats gives an undetectable
logical subset of M_Z of size <= |F|.  So d_circ(M) >= d_circ(M_Z).

Hypothesis B (projection).  For every mechanism of M_Z, its projection -- for each Z check, the
parity, over all rounds, of that check's detectors it flips; together with its observable bit --
is either zero or a column of the extended code.  Consequence: for an undetectable logical subset S
of M_Z every per-check parity sum is 0 and the observable sum is 1, so the non-zero projections,
after cancelling repeats, are an undetectable logical set of extended-code columns of size <= |S|.
So d_circ(M_Z) >= d_ext.  Together: d_circ(C(d, r)) >= d_ext(d).

Also reported (the upper direction, for comparison with the build log; the shipped upper bounds
are explicit witnesses and do not use it): the rounds in which every extended-code column is
realised by a single mechanism of M_Z that lives in that round's detectors and flips each check's
detector at most once.

Usage:  lemma_b_check.py DIR            (every (d, r) whose three files are present)
        lemma_b_check.py DIR d r [d r ...]
Exit status 0 iff every checked (d, r) passes both hypotheses.
"""
import collections, hashlib, json, os, re, sys
if not __debug__: sys.exit("lemma_b_check.py: refusing to run with Python optimisation on (-O, -OO or PYTHONOPTIMIZE): its checks rely on assert statements, which optimisation strips. Run it without -O and with PYTHONOPTIMIZE unset.")
PAIRS = [(3, 3), (5, 5), (7, 7), (9, 9), (11, 11), (13, 13), (15, 15),
         (3, 1), (5, 1), (7, 1), (9, 1), (11, 1), (13, 1), (15, 1)]


def circuit_geometry(path):
    """Return (ancillas in the order of the first M instruction, qubit -> (x, y),
    list of detector coordinate tuples with SHIFT_COORDS applied)."""
    qc = {}
    dets = []
    shift = []
    first_m = None
    for raw in open(path):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        mm = re.match(r"^([A-Z_0-9]+)(?:\(([^)]*)\))?\s*(.*)$", line)
        name, args, rest = mm.group(1), mm.group(2), mm.group(3)
        vals = [float(a) for a in args.split(",")] if args else []
        if name == "QUBIT_COORDS":
            assert not any(shift), "QUBIT_COORDS after SHIFT_COORDS is not supported"
            qc[int(rest.split()[0])] = tuple(vals)
        elif name == "SHIFT_COORDS":
            if len(shift) < len(vals):
                shift += [0.0] * (len(vals) - len(shift))
            for i, v in enumerate(vals):
                shift[i] += v
        elif name == "DETECTOR":
            co = [v + (shift[i] if i < len(shift) else 0.0) for i, v in enumerate(vals)]
            dets.append(tuple(co))
        elif name == "M" and first_m is None:
            first_m = [int(t) for t in rest.split()]
        elif name == "REPEAT":
            raise SystemExit("REPEAT blocks are not supported")
    assert first_m is not None, "no M instruction"
    return first_m, qc, dets


def run(base, d, r):
    mpath = os.path.join(base, f"m_d{d}_r{r}.json")
    cpath = os.path.join(base, f"c_d{d}_r{r}.stim")
    epath = os.path.join(base, f"m_Xext_d{d}.json")
    rec = json.load(open(mpath))
    ext = json.load(open(epath))
    assert hashlib.sha256(open(cpath, "rb").read()).hexdigest() == rec["circuit_sha256"], "circuit text hash mismatch"
    cols = {(tuple(m["dets"]), tuple(m["obs"])) for m in ext["mechanisms"]}
    anc, qc, coords = circuit_geometry(cpath)
    assert len(coords) == rec["num_detectors"], "detector count differs between object and circuit text"
    check_of_xy = {qc[q][:2]: k for k, q in enumerate(anc)}
    assert len(check_of_xy) == len(anc) == ext["num_detectors"], "ancilla/check count mismatch"
    det_info = {}
    for i, co in enumerate(coords):
        if int(co[3]) == 2:                      # Z-type detector: (x, y, t, 2, colour)
            det_info[i] = (check_of_xy[(co[0], co[1])], int(co[2]))
    mechs = rec["mechanisms"]
    # Hypothesis A
    zkeys = {(tuple(m["dets"]), tuple(m["obs"])) for m in mechs if all(dd in det_info for dd in m["dets"])}
    bad_a = 0
    for m in mechs:
        proj = (tuple(dd for dd in m["dets"] if dd in det_info), tuple(m["obs"]))
        if (proj[0] or proj[1]) and proj not in zkeys:
            bad_a += 1
    # Hypothesis B and the realisation report
    n_pure = 0; bad = 0; img = set(); realised = collections.defaultdict(set)
    for m in mechs:
        if any(dd not in det_info for dd in m["dets"]):
            continue
        n_pure += 1
        par = collections.Counter(det_info[dd][0] for dd in m["dets"])
        static = (tuple(sorted(k for k, v in par.items() if v % 2)), tuple(m["obs"]))
        if not static[0] and not static[1]:
            continue
        if static not in cols:
            bad += 1
        img.add(static)
        layers = {det_info[dd][1] for dd in m["dets"]}
        if len(layers) == 1 and all(v == 1 for v in par.values()):
            realised[next(iter(layers))].add(static)
    full = sorted(L for L, s in realised.items() if cols <= s)
    ok_b = bool(bad == 0 and not (cols - img) and full)
    print(f"d={d} r={r}: ext columns={len(cols)} pure-Z-detector mechanisms={n_pure}/{len(mechs)} | "
          f"projections not a column: {bad} | columns outside projection image: {len(cols - img)} | "
          f"layers realising every column as a single-layer fault: {full} | {'PASS' if ok_b else 'FAIL'}", flush=True)
    print(f"d={d} r={r}: X-part closure: {len(mechs)} mechanisms, {len(zkeys)} in M_Z, "
          f"restrictions outside M_Z: {bad_a} | {'PASS' if bad_a == 0 else 'FAIL'}", flush=True)
    return ok_b and bad_a == 0


def main():
    base = sys.argv[1]
    rest = list(map(int, sys.argv[2:]))
    pairs = list(zip(rest[0::2], rest[1::2])) if rest else PAIRS
    allok = True; n = 0
    for d, r in pairs:
        need = [os.path.join(base, f) for f in (f"m_d{d}_r{r}.json", f"c_d{d}_r{r}.stim", f"m_Xext_d{d}.json")]
        if all(os.path.exists(p) for p in need):
            allok &= run(base, d, r); n += 1
        elif rest:
            raise SystemExit(f"missing input for d={d} r={r}")
    print("LEMMA-B HYPOTHESES", "PASS" if (allok and n) else "FAIL", f"({n} objects; hypotheses A and B)")
    sys.exit(0 if (allok and n) else 1)


if __name__ == "__main__":
    main()
