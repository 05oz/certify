#!/usr/bin/env python3
"""check_dcirc.py -- certificate checker for circuit-level distance claims.  Python standard
library only (json, gzip, hashlib, sys, time, os).  No Stim, no solver, no numpy.

A certificate directory holds, per object (d, rounds):
  m_dX_rY.json          the OBJECT: canonical mechanism list M (distinct fault signatures of the
                        circuit's detector error model), with its SHA-256 and the circuit's SHA-256
  witness_dX_rY_wW.json UPPER bound: W mechanisms of M whose detector sets XOR to empty and whose
                        observable bits XOR to 1   =>  d_circ <= W
  lower_dX_rY_KK.json   LOWER bound: K and the name of an LRAT refutation of the canonical CNF
                        "some F subset M with |F| <= K has XOR dets = 0 and XOR obs = 1"
                        =>  d_circ >= K+1.   The CNF is REGENERATED here from M by the spec below;
                        the solver's own CNF file is never read.
Optionally the circuit text itself (c_dX_rY.stim) is re-derived into M by dem_from_circuit.py
(standard library, no Stim) and compared, so that Stim is not in the trusted base either.
Extended-code objects (kind 'extended_code', m_Xext_dX.json) are re-derived from the same circuit
text by extcode_from_circuit.py (the extended code of arXiv:2603.05481) and compared likewise.

CANONICAL CNF SPEC (must reproduce the solved instance byte-for-byte or the LRAT check fails):
  variables x_j = j+1 for mechanism j = 0..m-1 in the certificate's order; auxiliary variables
  allocated sequentially from m+1 in visitation order.
  XOR gate u = a xor b emits, in order: (-u a b) (-u -a -b) (u -a b) (u a -b).
  XOR chain over [l_1..l_t]: cur = l_1; for k = 2..t: fresh u, gate u = cur xor l_k, cur = u.
  (1) for each detector i = 0..n-1 ascending: S_i = ascending mechanisms containing i; if empty
      emit nothing; else chain over x_{S_i} and emit unit (-cur).
  (2) observable: O = ascending mechanisms with non-empty obs; chain; emit unit (+cur).
  (3) Sinz sequential at-most-K over x_1..x_m: registers s(i,j), i = 1..m-1 outer, j = 1..K inner;
      clauses: (-x_1 s(1,1)); (-s(1,j)) j=2..K; for i=2..m-1: (-x_i s(i,1)), (-s(i-1,1) s(i,1)),
      for j=2..K: (-x_i -s(i-1,j-1) s(i,j)), (-s(i-1,j) s(i,j)); then (-x_i -s(i-1,K));
      finally (-x_m -s(m-1,K)).  Nothing if K >= m.
LRAT replay: text LRAT (optionally gzip), RUP steps with hints: every hint clause must be unit or
falsified under the current assignment (a non-unit hint aborts; a hint already satisfied under the
current assignment propagates nothing and is skipped and counted), ids strictly increasing,
deletions honoured, negative (RAT) hints abort, a hint that is not a live clause aborts.
Success = the empty clause is derived.

Usage:
  check_dcirc.py witness  witness_dX_rY_wW.json
  check_dcirc.py lower    lower_dX_rY_KK.json
  check_dcirc.py object   m_dX_rY.json c_dX_rY.stim      (re-derive M from the circuit, no Stim)
  check_dcirc.py all      DIR                            (every certificate in DIR)
"""
import gzip, hashlib, json, os, sys, time
if not __debug__: sys.exit("check_dcirc.py: refusing to run with Python optimisation on (-O, -OO or PYTHONOPTIMIZE): its checks rely on assert statements, which optimisation strips. Run it without -O and with PYTHONOPTIMIZE unset.")

# ----------------------------------------------------------------- object hash

def mech_hash(mechs):
    h = hashlib.sha256()
    for m in mechs:
        h.update((",".join(map(str, m["dets"])) + ":" + ",".join(map(str, m["obs"])) + "\n").encode())
    return h.hexdigest()


def load_object(path):
    rec = json.load(open(path))
    mechs = rec["mechanisms"]
    keys = [(tuple(m["dets"]), tuple(m["obs"])) for m in mechs]
    assert keys == sorted(keys), "mechanism list is not in canonical sorted order"
    assert len(set(keys)) == len(keys), "duplicate mechanism"
    for m in mechs:
        assert all(0 <= i < rec["num_detectors"] for i in m["dets"]), "detector id out of range"
        assert all(o == 0 for o in m["obs"]), "only observable 0 is supported"
        assert m["dets"] or m["obs"], "empty signature"
    assert mech_hash(mechs) == rec["mechanism_list_sha256"], "mechanism list hash mismatch"
    return rec


# ----------------------------------------------------------------- witness

def check_witness(path):
    t0 = time.perf_counter()
    w = json.load(open(path))
    base = os.path.dirname(os.path.abspath(path))
    rec = load_object(os.path.join(base, w["mechanism_file"]))
    assert rec["mechanism_list_sha256"] == w["mechanism_list_sha256"], "witness bound to a different object"
    mechs = rec["mechanisms"]
    idx = w["mechanism_indices"]
    assert len(set(idx)) == len(idx), "repeated mechanism in witness"
    dets = set(); obs = 0
    for j in idx:
        mm = mechs[j]
        assert mm == w["mechanisms"][idx.index(j)], "witness mechanism copy disagrees with object"
        dets ^= set(mm["dets"]); obs ^= (1 if mm["obs"] else 0)
    assert not dets, f"witness flips detectors {sorted(dets)}"
    assert obs == 1, "witness does not flip the observable"
    assert len(idx) == w["weight"], "declared weight wrong"
    ms = (time.perf_counter() - t0) * 1000
    print(f"OK upper bound: d_circ(d={rec['d']}, rounds={rec['rounds']}) <= {len(idx)}   [{ms:.1f} ms]")
    return len(idx)


# ----------------------------------------------------------------- CNF regeneration

class Regen:
    def __init__(self, nv):
        self.nv = nv
        self.cl = []

    def fresh(self):
        self.nv += 1
        return self.nv

    def chain(self, lits):
        cur = lits[0]
        for l in lits[1:]:
            u = self.fresh()
            self.cl.append((-u, cur, l)); self.cl.append((-u, -cur, -l))
            self.cl.append((u, -cur, l)); self.cl.append((u, cur, -l))
            cur = u
        return cur

    def sinz(self, xs, K):
        m = len(xs)
        if K >= m:
            return
        s = {}
        for i in range(1, m):
            for j in range(1, K + 1):
                s[(i, j)] = self.fresh()
        self.cl.append((-xs[0], s[(1, 1)]))
        for j in range(2, K + 1):
            self.cl.append((-s[(1, j)],))
        for i in range(2, m):
            self.cl.append((-xs[i - 1], s[(i, 1)]))
            self.cl.append((-s[(i - 1, 1)], s[(i, 1)]))
            for j in range(2, K + 1):
                self.cl.append((-xs[i - 1], -s[(i - 1, j - 1)], s[(i, j)]))
                self.cl.append((-s[(i - 1, j)], s[(i, j)]))
            self.cl.append((-xs[i - 1], -s[(i - 1, K)]))
        self.cl.append((-xs[m - 1], -s[(m - 1, K)]))


def regenerate(rec, K):
    mechs = rec["mechanisms"]; m = len(mechs); n = rec["num_detectors"]
    g = Regen(m)
    touch = [[] for _ in range(n)]; obs = []
    for j, mm in enumerate(mechs):
        for i in mm["dets"]:
            touch[i].append(j)
        if mm["obs"]:
            obs.append(j)
    for i in range(n):
        if touch[i]:
            g.cl.append((-g.chain([j + 1 for j in touch[i]]),))
    assert obs, "no mechanism flips the observable"
    g.cl.append((g.chain([j + 1 for j in obs]),))
    g.sinz(list(range(1, m + 1)), K)
    return g


# ----------------------------------------------------------------- LRAT replay

class Bad(Exception):
    pass


def replay_lrat(clauses, path, progress=None):
    """Strict RUP-with-hints replay.  clauses: list of tuples, ids 1..len."""
    live = {i + 1: c for i, c in enumerate(clauses)}
    maxvar = max((abs(l) for c in clauses for l in c), default=0)
    val = [0] * (maxvar + 1)          # signed epoch: +e true, -e false, else unassigned
    epoch = 0
    last_id = len(clauses)
    empty = False
    skipped = 0
    opener = gzip.open if path.endswith(".gz") else open
    with opener(path, "rt") as fh:
        for ln, line in enumerate(fh, 1):
            parts = line.split()
            if not parts:
                continue
            cid = int(parts[0])
            if len(parts) > 1 and parts[1] == "d":
                for t in parts[2:]:
                    i = int(t)
                    if i == 0:
                        break
                    live.pop(i, None)
                continue
            nums = list(map(int, parts[1:]))
            z = nums.index(0)
            lits, hints = nums[:z], nums[z + 1:]
            if not hints or hints[-1] != 0:
                raise Bad(f"line {ln}: malformed hint list")
            hints = hints[:-1]
            if cid <= last_id:
                raise Bad(f"line {ln}: clause id {cid} not increasing")
            last_id = cid
            epoch += 1
            for l in lits:
                v = abs(l)
                if v > maxvar:
                    val.extend([0] * (v - maxvar)); maxvar = v
                val[v] = -epoch if l > 0 else epoch       # falsify the lemma's literals
            conflict = False
            for h in hints:
                if h < 0:
                    raise Bad(f"line {ln}: RAT hint {h} (RUP-only checker)")
                c = live.get(h)
                if c is None:
                    raise Bad(f"line {ln}: hint {h} is not a live clause")
                unit = None; nfree = 0; satisfied = False
                for l in c:
                    v = abs(l)
                    if v > maxvar:
                        val.extend([0] * (v - maxvar)); maxvar = v
                    s = val[v]
                    if s == epoch or s == -epoch:
                        if (s > 0) == (l > 0):
                            satisfied = True
                            break
                        continue
                    nfree += 1; unit = l
                    if nfree > 1:
                        raise Bad(f"line {ln}: hint {h} is not unit")
                if satisfied:
                    skipped += 1          # a satisfied hint propagates nothing; skipping it is sound
                    continue
                if nfree == 0:
                    conflict = True
                    break
                val[abs(unit)] = epoch if unit > 0 else -epoch
            if not conflict:
                raise Bad(f"line {ln}: no conflict for lemma {cid}")
            live[cid] = tuple(lits)
            if not lits:
                empty = True
                break
            if progress and epoch % progress == 0:
                print(f"    ... {epoch:,} lemmas, {len(live):,} live clauses", flush=True)
    if not empty:
        raise Bad("proof ended without the empty clause")
    if skipped:
        print(f"    (skipped {skipped} hint clause(s) already satisfied under the running assignment; sound, contributes nothing)")
    return epoch


def check_lower(path, progress=200000):
    t0 = time.perf_counter()
    c = json.load(open(path))
    base = os.path.dirname(os.path.abspath(path))
    rec = load_object(os.path.join(base, c["mechanism_file"]))
    assert rec["mechanism_list_sha256"] == c["mechanism_list_sha256"], "certificate bound to a different object"
    K = c["K"]
    g = regenerate(rec, K)
    if "cnf_sha256" in c:       # informational: the solved instance's hash, recomputed here
        data = (f"p cnf {g.nv} {len(g.cl)}\n" + "".join(" ".join(map(str, cl)) + " 0\n" for cl in g.cl)).encode()
        h = hashlib.sha256(data).hexdigest()
        assert h == c["cnf_sha256"], "regenerated CNF differs from the certificate's recorded hash"
    n = replay_lrat(g.cl, os.path.join(base, c["lrat_file"]), progress)
    s = time.perf_counter() - t0
    print(f"OK lower bound: d_circ(d={rec['d']}, rounds={rec['rounds']}) >= {K + 1}   "
          f"[{n:,} lemmas replayed, {len(g.cl):,} clauses regenerated, {s:.1f} s]")
    return K + 1


def check_object(mpath, cpath):
    """Re-derive the object's mechanism list from the circuit text (no Stim) and compare.
    kind absent/'dem': detector-error-model signatures (dem_from_circuit);
    kind 'extended_code': the extended code of arXiv:2603.05481 (extcode_from_circuit)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    rec = load_object(mpath)
    data = open(cpath, "rb").read()
    assert hashlib.sha256(data).hexdigest() == rec["circuit_sha256"], "circuit text hash mismatch"
    theirs = [(tuple(m["dets"]), tuple(m["obs"])) for m in rec["mechanisms"]]
    if rec.get("kind") == "purex_sublist":
        import purex_from_object as pfo, dem_from_circuit as dfc
        # re-derive the PARENT list from the circuit text, then the sub-list and the lemma hypothesis
        n_det, obs_ids, mechs = dfc.signatures(cpath)
        parent = {"d": rec["d"], "rounds": rec["rounds"], "noise_model": rec["noise_model"], "num_detectors": n_det,
                  "circuit_sha256": rec["circuit_sha256"], "mechanism_list_sha256": rec["parent_mechanism_list_sha256"],
                  "mechanism_hash_spec": rec["mechanism_hash_spec"],
                  "mechanisms": [{"dets": list(a), "obs": list(b)} for a, b in mechs]}
        assert mech_hash(parent["mechanisms"]) == rec["parent_mechanism_list_sha256"], "parent list re-derived from circuit differs"
        import tempfile, os as _os
        tp = _os.path.join(tempfile.mkdtemp(), "parent.json"); json.dump(parent, open(tp, "w"))
        r2 = pfo.build(tp, cpath)
        ours = [(tuple(m["dets"]), tuple(m["obs"])) for m in r2["mechanisms"]]
        assert r2["projections_outside_sublist"] == 0, "X-part lemma hypothesis fails: a Z-projection is not in the sub-list"
        assert ours == theirs, "re-derived pure-X sub-list differs from the object"
        print(f"OK object (pure-X sub-list): d={rec['d']} rounds={rec['rounds']}: parent list ({len(mechs)} mechanisms) re-derived from the "
              f"circuit text (no Stim), sub-list {len(ours)} identical, lemma hypothesis holds; sha256 {rec['mechanism_list_sha256'][:16]}")
        return
    if rec.get("kind") == "extended_code":
        import extcode_from_circuit as efc
        r2 = efc.build(cpath, rec["sector"])
        ours = [(tuple(m["dets"]), tuple(m["obs"])) for m in r2["mechanisms"]]
        assert r2["num_detectors"] == rec["num_detectors"], "check count differs"
        assert ours == theirs, "re-derived extended code differs from the object"
        print(f"OK object (extended code, {rec['sector']} sector): d={rec['d']}: {len(ours)} distinct columns "
              f"re-derived from the circuit text (no Stim) and identical to the object; sha256 {rec['mechanism_list_sha256'][:16]}")
        return
    import dem_from_circuit as dfc
    n_det, obs_ids, mechs = dfc.signatures(cpath)
    ours = [(tuple(a), tuple(b)) for a, b in mechs]
    assert n_det == rec["num_detectors"], "detector count differs"
    assert ours == theirs, "re-derived mechanism list differs from the object"
    print(f"OK object: d={rec['d']} rounds={rec['rounds']}: {len(ours)} mechanisms re-derived from the circuit text "
          f"(no Stim) and identical to the object; sha256 {rec['mechanism_list_sha256'][:16]}")


def main():
    mode = sys.argv[1]
    if mode == "witness":
        check_witness(sys.argv[2])
    elif mode == "lower":
        check_lower(sys.argv[2])
    elif mode == "object":
        check_object(sys.argv[2], sys.argv[3])
    elif mode == "all":
        d = sys.argv[2]
        names = sorted(os.listdir(d))
        for f in names:
            p = os.path.join(d, f)
            if f.startswith("m_") and f.endswith(".json"):
                rec = json.load(open(p))
                cp = os.path.join(d, rec.get("circuit_file", "c_" + f[2:-5] + ".stim"))
                if os.path.exists(cp):
                    check_object(p, cp)
                else:
                    print(f"SKIP object {f}: circuit file {os.path.basename(cp)} not present")
        for f in names:
            p = os.path.join(d, f)
            if f.startswith("witness_"):
                check_witness(p)
        for f in names:
            p = os.path.join(d, f)
            if f.startswith("lower_"):
                check_lower(p)
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
