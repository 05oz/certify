#!/usr/bin/env python3
"""dem_from_circuit.py -- INDEPENDENT re-derivation of the fault-mechanism signatures of a
Stim circuit, Python standard library only, no Stim.

Fault model: every DEPOLARIZE2(p) a b instruction is a fault location; the 15 non-identity
two-qubit Paulis at that location are the faults.  (Other noise instructions abort: the
objects of this target carry DEPOLARIZE2 only.)  A fault's signature is the set of
detectors whose parity it flips together with the set of observables it flips.  The
mechanism list is the set of DISTINCT non-empty signatures, sorted.

Method: one reverse pass with per-qubit bitmasks.  Dx[q] (Dz[q]) is the set of
detectors/observables flipped by an X (Z) error on qubit q at the current point of the
circuit, encoded as an integer bitmask (bit i = detector i, bit n_det + k = observable k).
Reverse rules, exact Pauli-frame algebra:
  CX c t :  Dx[c] ^= Dx[t]   (X on control also flips target)
            Dz[t] ^= Dz[c]   (Z on target also flips control)
  M q     :  Dx[q] ^= mask(record) ;  Dz[q] = 0   (Z before a Z-measurement is absorbed)
  MX q    :  Dz[q] ^= mask(record) ;  Dx[q] = 0
  R q / RX q :  Dx[q] = Dz[q] = 0   (a reset erases everything before it)
  DEPOLARIZE2 a b :  emit signatures of the 15 Paulis from Dx[a], Dz[a], Dx[b], Dz[b]
                    (Y = X.Z, so its mask is Dx ^ Dz)
Records are indexed by a forward pass; DETECTOR/OBSERVABLE_INCLUDE resolve rec[-k] there.
Usage:  dem_from_circuit.py circuit.stim [m.json]   -> prints counts and canonical hash;
        with m.json, compares mechanism sets and exits nonzero on mismatch.
"""
import hashlib, json, re, sys
if not __debug__: sys.exit("dem_from_circuit.py: refusing to run with Python optimisation on (-O, -OO or PYTHONOPTIMIZE): its checks rely on assert statements, which optimisation strips. Run it without -O and with PYTHONOPTIMIZE unset.")
def parse(path):
    insts = []
    for raw in open(path):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        m = re.match(r"^([A-Z_0-9]+)(?:\(([^)]*)\))?\s*(.*)$", line)
        assert m, f"unparsed line: {line!r}"
        name, args, rest = m.group(1), m.group(2), m.group(3)
        assert name != "REPEAT", "REPEAT blocks are not supported by this re-derivation"
        toks = rest.split()
        insts.append((name, args, toks))
    return insts

def signatures(path):
    insts = parse(path)
    # forward pass: number records, resolve detectors and observables
    n_rec = 0
    detectors = []          # list of lists of absolute record indices
    observables = {}        # obs id -> set of record indices (XOR-accumulated)
    rec_index_of = []       # per instruction: list of record indices it produces (for M/MX)
    for name, args, toks in insts:
        if name in ("M", "MX", "MZ"):
            idx = []
            for t in toks:
                assert not t.startswith("!"), "inverted measurement targets not supported"
                idx.append(n_rec); n_rec += 1
            rec_index_of.append(idx)
        elif name in ("MR", "MRX", "MRZ", "MY", "MRY", "MPP"):
            raise SystemExit(f"unsupported measurement instruction {name}")
        elif name == "DETECTOR":
            recs = []
            for t in toks:
                mm = re.match(r"rec\[-(\d+)\]$", t); assert mm, t
                recs.append(n_rec - int(mm.group(1)))
            detectors.append(recs); rec_index_of.append(None)
        elif name == "OBSERVABLE_INCLUDE":
            k = int(float(args)) if args else 0
            s = observables.setdefault(k, set())
            for t in toks:
                mm = re.match(r"rec\[-(\d+)\]$", t); assert mm, t
                r = n_rec - int(mm.group(1))
                s ^= {r}
            rec_index_of.append(None)
        else:
            rec_index_of.append(None)
    n_det = len(detectors)
    obs_ids = sorted(observables)
    mask_of_rec = [0] * n_rec
    for i, recs in enumerate(detectors):
        for r in recs:
            mask_of_rec[r] ^= 1 << i
    for k in obs_ids:
        for r in observables[k]:
            mask_of_rec[r] ^= 1 << (n_det + obs_ids.index(k))
    # reverse pass
    nq = 0
    for name, args, toks in insts:
        if name in ("CX", "M", "MX", "MZ", "R", "RX", "RZ", "DEPOLARIZE2", "QUBIT_COORDS"):
            for t in toks:
                if t.lstrip("-").isdigit():
                    nq = max(nq, int(t) + 1)
    Dx = [0] * nq; Dz = [0] * nq
    sigs = set()
    for (name, args, toks), recs in zip(reversed(insts), reversed(rec_index_of)):
        if name == "CX":
            assert len(toks) % 2 == 0
            for i in range(len(toks) - 2, -1, -2):        # pairs are applied in order; reverse them
                c, t = int(toks[i]), int(toks[i + 1])
                Dx[c] ^= Dx[t]; Dz[t] ^= Dz[c]
        elif name in ("M", "MZ"):
            for q, r in zip(map(int, toks), recs):
                Dx[q] ^= mask_of_rec[r]; Dz[q] = 0
        elif name == "MX":
            for q, r in zip(map(int, toks), recs):
                Dz[q] ^= mask_of_rec[r]; Dx[q] = 0
        elif name in ("R", "RZ", "RX"):
            for q in map(int, toks):
                Dx[q] = 0; Dz[q] = 0
        elif name == "DEPOLARIZE2":
            assert len(toks) % 2 == 0
            for i in range(0, len(toks), 2):
                a, b = int(toks[i]), int(toks[i + 1])
                pa = [0, Dx[a], Dz[a], Dx[a] ^ Dz[a]]     # I X Z Y on a
                pb = [0, Dx[b], Dz[b], Dx[b] ^ Dz[b]]
                for ia in range(4):
                    for ib in range(4):
                        if ia == 0 and ib == 0:
                            continue
                        msk = pa[ia] ^ pb[ib]
                        if msk:
                            sigs.add(msk)
        elif name in ("TICK", "DETECTOR", "OBSERVABLE_INCLUDE", "QUBIT_COORDS", "SHIFT_COORDS"):
            pass
        else:
            raise SystemExit(f"unsupported instruction in circuit: {name}")
    out = []
    for msk in sigs:
        dets = [i for i in range(n_det) if msk >> i & 1]
        obs = [obs_ids[k] for k in range(len(obs_ids)) if msk >> (n_det + k) & 1]
        out.append((tuple(dets), tuple(obs)))
    out.sort()
    return n_det, obs_ids, out

def canon_hash(mechs):
    h = hashlib.sha256()
    for dets, obs in mechs:
        h.update((",".join(map(str, dets)) + ":" + ",".join(map(str, obs)) + "\n").encode())
    return h.hexdigest()

if __name__ == "__main__":
    n_det, obs_ids, mechs = signatures(sys.argv[1])
    print(f"detectors={n_det} observables={len(obs_ids)} distinct_signatures={len(mechs)} sha256={canon_hash(mechs)}")
    if len(sys.argv) > 2:
        rec = json.load(open(sys.argv[2]))
        theirs = sorted((tuple(m["dets"]), tuple(m["obs"])) for m in rec["mechanisms"])
        same = theirs == mechs and rec["num_detectors"] == n_det
        print("MATCH" if same else "MISMATCH", "against", sys.argv[2],
              f"(json: {len(theirs)} mechs, hash {rec['mechanism_list_sha256'][:16]}; ours {canon_hash(mechs)[:16]})")
        if not same:
            a, b = set(theirs), set(mechs)
            print("only in stim:", len(a - b), "only in ours:", len(b - a))
            for x in list(a - b)[:3]: print("  stim-only", x)
            for x in list(b - a)[:3]: print("  ours-only", x)
            sys.exit(1)
