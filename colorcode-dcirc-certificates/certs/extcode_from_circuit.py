#!/usr/bin/env python3
"""extcode_from_circuit.py -- the EXTENDED CODE of arXiv:2603.05481 (Strikis, Browne, Beverland,
Def. "Extended code" and Thm. "Circuit distance bounds") built from the circuit text alone.
Python standard library only; no Stim.

For a single-ancilla CNOT syndrome-extraction circuit, the X-sector extended code (Z-basis
memory, X-type logical failures) has one row per Z-check and one column per data qubit plus one
column per X-type residual error E_l = {i_l, ..., i_w} (l = 2..w), where i_1..i_w is the CNOT
order of the X-check on that ancilla; a residual column is the mod-2 sum of its data columns.
The Z-sector code is the mirror image (rows = X-checks, residuals from Z-check CNOT orders).
Output: a mechanism list in the same format as the DEM objects (detector-set, observable-bit
per column, distinct signatures, sorted, hashed), so check_dcirc.py verifies its certificates
unchanged.  d_ext = min weight in ker(H^ext) minus ker(L^ext) is a LOWER bound on the circuit-level
distance for any noise model (Prop. "Extended-code distance bound") and EQUALS it for
non-interleaved circuits whose faults can realise every column inside one partition (Cor.).

Circuit conventions parsed (build_parallel_circuit of the paper companion code): first round =
R; six CX layers data->anc (Z checks); M anc; RX anc; six CX layers anc->data (X checks); MX;
...; final M data; OBSERVABLE_INCLUDE(0) rec[...] over the final data measurement.
Usage: extcode_from_circuit.py circuit.stim {X|Z} out_m.json
"""
import hashlib, json, os, re, sys
if not __debug__: sys.exit("extcode_from_circuit.py: refusing to run with Python optimisation on (-O, -OO or PYTHONOPTIMIZE): its checks rely on assert statements, which optimisation strips. Run it without -O and with PYTHONOPTIMIZE unset.")
def parse(path):
    out = []
    for raw in open(path):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        m = re.match(r"^([A-Z_0-9]+)(?:\(([^)]*)\))?\s*(.*)$", line)
        out.append((m.group(1), m.group(2), m.group(3).split()))
    return out

def build(path, sector):
    insts = parse(path)
    # ancillas = targets of the first M; data = all qubits in R that are not ancillas
    first_M = next(t for n, a, t in insts if n == "M")
    anc = [int(q) for q in first_M]
    anc_idx = {q: i for i, q in enumerate(anc)}
    reset = next(t for n, a, t in insts if n == "R")
    data = sorted(int(q) for q in reset if int(q) not in anc_idx)
    # first round: CX layers before first M (Z checks, data->anc), CX layers between RX and MX (X checks, anc->data)
    z_order = {q: [] for q in anc}; x_order = {q: [] for q in anc}
    phase = "Z"; seen_M = False
    for n, a, t in insts:
        if n == "M" and not seen_M:
            seen_M = True; phase = "X"; continue
        if n == "MX":
            break
        if n == "CX":
            for i in range(0, len(t), 2):
                c, tg = int(t[i]), int(t[i + 1])
                if phase == "Z":
                    assert tg in anc_idx and c not in anc_idx
                    z_order[tg].append(c)
                else:
                    assert c in anc_idx and tg not in anc_idx
                    x_order[c].append(tg)
    # observable: top row via the final data measurement records
    final_M = [t for n, a, t in insts if n == "M"][-1]
    final_M = [int(q) for q in final_M]
    obs = None
    for n, a, t in insts:
        if n == "OBSERVABLE_INCLUDE":
            obs = set()
            for tok in t:
                k = int(re.match(r"rec\[-(\d+)\]$", tok).group(1))
                obs ^= {final_M[len(final_M) - k]}
    assert obs is not None
    # check supports (Z-check support == X-check support: same ancilla, same plaquette)
    for q in anc:
        assert sorted(z_order[q]) == sorted(x_order[q]), "Z/X supports differ on an ancilla"
    checks_of = {d: [anc_idx[q] for q in anc if d in z_order[q]] for d in data}
    order = x_order if sector == "X" else z_order      # residuals come from the OTHER-type check's CNOT order
    # X-sector (Z memory): failures are X errors; residuals from X-check (anc->data) orders; rows = Z checks.
    # Z-sector (X memory): failures are Z errors; residuals from Z-check (data->anc) orders; rows = X checks.
    cols = {}
    def add(sig, label):
        cols.setdefault(sig, []).append(label)
    for d in data:
        add((tuple(sorted(checks_of[d])), (0,) if d in obs else ()), f"data:{d}")
    for q in anc:
        seq = order[q]; w = len(seq)
        for l in range(2, w + 1):
            suffix = seq[l - 1:]
            dets = set(); ob = 0
            for d in suffix:
                dets ^= set(checks_of[d]); ob ^= (1 if d in obs else 0)
            add((tuple(sorted(dets)), (0,) if ob else ()), f"residual:anc{anc_idx[q]}:l{l}:{suffix}")
    sigs = sorted(s for s in cols if s[0] or s[1])
    mechs = [{"dets": list(s[0]), "obs": list(s[1]), "columns": cols[s]} for s in sigs]
    h = hashlib.sha256()
    for m in mechs:
        h.update((",".join(map(str, m["dets"])) + ":" + ",".join(map(str, m["obs"])) + "\n").encode())
    n_res = sum(max(0, len(order[q]) - 1) for q in anc)
    return {"kind": "extended_code", "sector": sector, "num_detectors": len(anc), "num_observables": 1,
            "num_data": len(data), "num_residuals": n_res, "num_columns": len(data) + n_res,
            "num_mechanisms": len(mechs), "mechanism_list_sha256": h.hexdigest(),
            "mechanism_hash_spec": "sha256 over newline-terminated lines 'd1,d2,...:o1,...' (detector ids ascending, observable ids ascending), mechanisms sorted by (dets, obs), UTF-8",
            "circuit_file": os.path.basename(path), "circuit_sha256": hashlib.sha256(open(path, "rb").read()).hexdigest(),
            "definition": "arXiv:2603.05481 Def. extended code; rows = checks of the type that detects the sector's errors; columns = data qubits + residual suffix sets of the opposite-type check CNOT orders (l=2..w); identical signatures merged (column labels kept)",
            "mechanisms": mechs}

if __name__ == "__main__":
    rec = build(sys.argv[1], sys.argv[2])
    if len(sys.argv) > 3:
        json.dump(rec, open(sys.argv[3], "w"))
    print(f"{sys.argv[2]}-sector extended code: rows={rec['num_detectors']} data={rec['num_data']} residuals={rec['num_residuals']} "
          f"distinct columns={rec['num_mechanisms']} sha256={rec['mechanism_list_sha256'][:16]}")
