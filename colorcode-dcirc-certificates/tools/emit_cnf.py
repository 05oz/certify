#!/usr/bin/env python3
"""emit_cnf.py -- write the canonical CNF of a lower-bound certificate, for regenerating its proof.
Python standard library only.  Uses check_dcirc.py's own regeneration, so the file it writes is
byte for byte the formula the checker replays the proof against; it prints the SHA-256 and compares
it with the certificate's recorded `cnf_sha256`.

Usage:  python3 tools/emit_cnf.py certs/lower_Xext_d15_K11.json  out.cnf
        (on Windows: py tools/emit_cnf.py ...)
"""
import hashlib, json, os, sys
if not __debug__: sys.exit("emit_cnf.py: refusing to run with Python optimisation on (-O, -OO or PYTHONOPTIMIZE): its checks rely on assert statements, which optimisation strips. Run it without -O and with PYTHONOPTIMIZE unset.")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "certs"))
import check_dcirc as cd          # noqa: E402


def main():
    low, out = sys.argv[1], sys.argv[2]
    c = json.load(open(low))
    rec = cd.load_object(os.path.join(os.path.dirname(os.path.abspath(low)), c["mechanism_file"]))
    assert rec["mechanism_list_sha256"] == c["mechanism_list_sha256"], "certificate bound to a different object"
    g = cd.regenerate(rec, c["K"])
    data = (f"p cnf {g.nv} {len(g.cl)}\n" + "".join(" ".join(map(str, cl)) + " 0\n" for cl in g.cl)).encode()
    open(out, "wb").write(data)
    h = hashlib.sha256(data).hexdigest()
    ok = h == c.get("cnf_sha256")
    print(f"{out}: p cnf {g.nv} {len(g.cl)}  sha256 {h}  {'matches' if ok else 'DOES NOT MATCH'} the certificate")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
