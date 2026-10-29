#!/usr/bin/env python3
"""tamper_demo.py -- negative controls for check_dcirc.py.  Standard library only.
Usage: python3 tamper_demo.py STEM   (e.g. d3_r3; needs m_STEM.json, c_STEM.stim, one witness and
one lower certificate for STEM in this directory).  Each corruption is written to a temp copy of
the certificate directory and must be REJECTED by the checker; the pristine copy must PASS.
Fifteen corruptions.  Each one names the check that must reject it, and the battery matches the
checker's output against that check: a corruption that is rejected by a different check from the
one its label names fails the battery, so every label is tested, not only every rejection.
The two CX-reversal cases reverse a pair in the third CX layer: once with the circuit hash left
stale, and once with the object rebound to the edited circuit's hash.  The last three lower-bound
cases remove one mechanism from the object and rehash it; they then rebind, in turn, nothing,
the certificate's object hash, and also its recorded CNF hash, so that they are rejected by the
certificate-to-object binding, by the regenerated CNF's hash, and by the LRAT replay itself.
The last case repeats the dropped-mechanism witness with the checker started under python -O,
which strips assert statements: the checker's optimisation guard must refuse to run (without the
guard, -O accepts that witness).
"""
import gzip, hashlib, json, os, re, shutil, subprocess, sys, tempfile
if not __debug__: sys.exit("tamper_demo.py: refusing to run with Python optimisation on (-O, -OO or PYTHONOPTIMIZE): its checks rely on assert statements, which optimisation strips. Run it without -O and with PYTHONOPTIMIZE unset.")
stem = sys.argv[1]
here = os.path.dirname(os.path.abspath(__file__))
wit = [f for f in os.listdir(here) if f.startswith(f"witness_{stem}_w") and "stimheur" not in f][0]
low = [f for f in os.listdir(here) if f.startswith(f"lower_{stem}_K")][0]
_rec = json.load(open(os.path.join(here, f"m_{stem}.json")))
CIRC = _rec.get("circuit_file", f"c_{stem}.stim")
files = [f"m_{stem}.json", CIRC, wit, low, json.load(open(os.path.join(here, low)))["lrat_file"],
         "check_dcirc.py", "dem_from_circuit.py", "extcode_from_circuit.py", "purex_from_object.py"]

def run(d, mode, arg, extra=None, pyflags=()):
    cmd = [sys.executable, *pyflags, os.path.join(d, "check_dcirc.py"), mode, os.path.join(d, arg)] + ([os.path.join(d, extra)] if extra else [])
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip()
    last = out.splitlines()[-1] if out else ""
    if r.returncode != 0 and ": " not in last:     # a bare exception: say where it was raised
        frames = re.findall(r'File "([^"]+)", line (\d+)', out)
        if frames:
            last += f" (raised at {os.path.basename(frames[-1][0])}:{frames[-1][1]})"
    return r.returncode == 0, last, out

def fresh():
    d = tempfile.mkdtemp(prefix="tamper_")
    _tmpdirs.append(d)
    for f in files:
        shutil.copy(os.path.join(here, f), d)
    return d

def edit_json(d, name, fn):
    p = os.path.join(d, name); j = json.load(open(p)); fn(j); json.dump(j, open(p, "w"))

results = []
_tmpdirs = []
# pristine
d = fresh()
for mode, a, b in (("object", f"m_{stem}.json", CIRC), ("witness", wit, None), ("lower", low, None)):
    ok, msg, _ = run(d, mode, a, b); results.append((f"pristine {mode}", ok, msg))
    assert ok, f"pristine {mode} FAILED: {msg}"

def corrupt(label, mode, a, b, fn, expect, pyflags=()):
    """expect: substrings of the checker's output, any one of which identifies the check named in
    the label.  The case passes only if the checker rejects AND the rejection comes from that check.
    pyflags: interpreter options for the checker's process (the last case passes -O)."""
    d = fresh(); fn(d)
    ok, msg, out = run(d, mode, a, b, pyflags)
    if ok:
        results.append((label, False, "ACCEPTED: " + msg))
    elif not any(e in out for e in expect):
        results.append((label, False, "rejected by a different check: " + msg))
    else:
        results.append((label, True, msg))

m, c = f"m_{stem}.json", CIRC
def drop_mech(d): edit_json(d, m, lambda j: j["mechanisms"].pop(0))
def drop_mech_rehash(d):
    def f(j):
        j["mechanisms"].pop(len(j["mechanisms"]) // 2)
        h = hashlib.sha256()
        for mm in j["mechanisms"]:
            h.update((",".join(map(str, mm["dets"])) + ":" + ",".join(map(str, mm["obs"])) + "\n").encode())
        j["mechanism_list_sha256"] = h.hexdigest()
    edit_json(d, m, f)
def flip_circuit(d):
    p = os.path.join(d, c); s = open(p).read().replace("DEPOLARIZE2(0.001)", "DEPOLARIZE2(0.002)", 1); open(p, "w").write(s)
CX_LAYER = 2     # reverse a pair in the third CX instruction: faults of earlier layers pass through it.
                 # (Reversing a pair in the FIRST CX layer is not a valid control for the re-derivation:
                 # no fault precedes that gate, so the mechanism list can stay the same.)
def swap_cx(d, rehash=False):
    p = os.path.join(d, c); lines = open(p).read().split("\n")
    seen = 0
    for i, l in enumerate(lines):
        if l.startswith("CX "):
            if seen == CX_LAYER:
                t = l.split(); t[1], t[2] = t[2], t[1]; lines[i] = " ".join(t); break
            seen += 1
    open(p, "w").write("\n".join(lines))
    if rehash:      # bind the object to the edited circuit, so that only the re-derivation can reject it
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        edit_json(d, m, lambda j: j.__setitem__("circuit_sha256", h))
def swap_cx_rehash(d): swap_cx(d, rehash=True)
def wit_drop(d): edit_json(d, wit, lambda j: (j["mechanism_indices"].pop(), j["mechanisms"].pop(), j.__setitem__("weight", j["weight"] - 1)))
def wit_weight(d): edit_json(d, wit, lambda j: j.__setitem__("weight", j["weight"] - 1))
def wit_hash(d): edit_json(d, wit, lambda j: j.__setitem__("mechanism_list_sha256", "0" * 64))
def low_K(d): edit_json(d, low, lambda j: j.__setitem__("K", j["K"] + 1))
def low_hash(d): edit_json(d, low, lambda j: j.__setitem__("mechanism_list_sha256", "0" * 64))
def low_trunc(d):
    p = os.path.join(d, json.load(open(os.path.join(d, low)))["lrat_file"])
    data = gzip.open(p, "rt").read().split("\n"); data = data[: max(1, len(data) // 2)]
    gzip.open(p, "wt").write("\n".join(data) + "\n")
def low_obj(d):          # the object loses a mechanism and is rehashed; the certificate still names the old object
    drop_mech_rehash(d)
def low_obj_rebind(d):   # ... and the certificate is rebound to the new object hash: the regenerated CNF changes
    drop_mech_rehash(d)
    h = json.load(open(os.path.join(d, m)))["mechanism_list_sha256"]
    edit_json(d, low, lambda j: j.__setitem__("mechanism_list_sha256", h))
def low_obj_rebind_cnf(d):   # ... and its recorded CNF hash is set to the regenerated CNF's: only the replay is left
    low_obj_rebind(d)
    sys.path.insert(0, d)
    import check_dcirc as cd        # the checker's own CNF regeneration (byte-identical copy in d)
    sys.path.remove(d)
    rec = cd.load_object(os.path.join(d, m))
    g = cd.regenerate(rec, json.load(open(os.path.join(d, low)))["K"])
    data = (f"p cnf {g.nv} {len(g.cl)}\n" + "".join(" ".join(map(str, cl)) + " 0\n" for cl in g.cl)).encode()
    edit_json(d, low, lambda j: j.__setitem__("cnf_sha256", hashlib.sha256(data).hexdigest()))

REDERIVATION = ("re-derived", "dem_from_circuit.py", "extcode_from_circuit.py", "purex_from_object.py")
corrupt("object: mechanism removed (hash mismatch)", "object", m, c, drop_mech,
        ("mechanism list hash mismatch",))
corrupt("object: mechanism removed, hash recomputed (rejected by the re-derivation)", "object", m, c, drop_mech_rehash,
        REDERIVATION)
corrupt("object: circuit noise strength edited (circuit hash mismatch)", "object", m, c, flip_circuit,
        ("circuit text hash mismatch",))
corrupt("object: CX pair in 3rd CX layer reversed, hash left (circuit hash mismatch)", "object", m, c, swap_cx,
        ("circuit text hash mismatch",))
corrupt("object: CX pair in 3rd CX layer reversed, circuit hash recomputed (rejected by the re-derivation)", "object", m, c,
        swap_cx_rehash, REDERIVATION)
corrupt("witness: one mechanism dropped (XOR check)", "witness", wit, None, wit_drop,
        ("witness flips detectors", "witness does not flip the observable"))
corrupt("witness: declared weight wrong", "witness", wit, None, wit_weight,
        ("declared weight wrong",))
corrupt("witness: bound to wrong object hash", "witness", wit, None, wit_hash,
        ("witness bound to a different object",))
corrupt("lower: K overstated by one (regenerated CNF hash mismatch)", "lower", low, None, low_K,
        ("regenerated CNF differs from the certificate's recorded hash",))
corrupt("lower: bound to wrong object hash", "lower", low, None, low_hash,
        ("certificate bound to a different object",))
corrupt("lower: LRAT truncated to half (replay: no empty clause)", "lower", low, None, low_trunc,
        ("proof ended without the empty clause",))
corrupt("lower: mechanism removed, object rehashed, certificate not rebound (certificate-to-object binding)", "lower", low, None,
        low_obj, ("certificate bound to a different object",))
corrupt("lower: same, certificate rebound to the new object (regenerated CNF hash mismatch)", "lower", low, None,
        low_obj_rebind, ("regenerated CNF differs from the certificate's recorded hash",))
corrupt("lower: same, certificate and CNF hash rebound (LRAT replay fails)", "lower", low, None,
        low_obj_rebind_cnf, ("Bad: line ", "Bad: proof ended"))
corrupt("witness: one mechanism dropped, checker run under python -O (refused by the optimisation guard)", "witness", wit,
        None, wit_drop, ("refusing to run with Python optimisation on",), pyflags=("-O",))
allok = True
for label, ok, msg in results:
    print(("PASS" if ok else "FAIL"), "|", label, "|", msg[:110]); allok &= ok
for _d in _tmpdirs:
    shutil.rmtree(_d, ignore_errors=True)
print("TAMPER BATTERY", "PASS" if allok else "FAIL",
      f"({len(results)-3} corruptions, each rejected by the check its label names)" if allok else "")
sys.exit(0 if allok else 1)
