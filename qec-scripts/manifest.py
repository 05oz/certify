#!/usr/bin/env python3
"""manifest.py -- walk certificates/, hash every artifact, re-run every
checker, and write manifest.json with sizes, sha256, and check times."""
import hashlib, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
CERTS = os.path.join(HERE, "certificates")
PY = sys.executable
LRAT_CHECK = os.path.join(HERE, "tools-drat-trim", "lrat-check")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run_checker(script, args):
    t0 = time.perf_counter()
    r = subprocess.run([PY, os.path.join(HERE, script)] + args,
                       capture_output=True, text=True)
    dt = (time.perf_counter() - t0) * 1000
    return r.returncode == 0, round(dt, 1), r.stdout.strip()


def main():
    out = {}
    for code in sorted(os.listdir(CERTS)):
        cdir = os.path.join(CERTS, code)
        if not os.path.isdir(cdir):
            continue
        entry = dict(files={}, checks=[])
        for f in sorted(os.listdir(cdir)):
            p = os.path.join(cdir, f)
            entry["files"][f] = dict(bytes=os.path.getsize(p), sha256=sha256(p))
        for f in sorted(os.listdir(cdir)):
            p = os.path.join(cdir, f)
            if f.startswith("witness") and f.endswith(".json"):
                ok, ms, msg = run_checker("check_witness.py", [p])
                entry["checks"].append(dict(cert=f, checker="check_witness.py",
                                            ok=ok, ms=ms, msg=msg))
            elif f.startswith("lower") and f.endswith(".json"):
                big = any(entry["files"][i["lrat_file"]]["bytes"] > 5_000_000
                          for i in json.load(open(p))["instances"])
                args = ([ "--external", LRAT_CHECK, p] if big else [p])
                ok, ms, msg = run_checker("check_lower.py", args)
                entry["checks"].append(dict(cert=f,
                                            checker="check_lower.py" +
                                            (" +lrat-check" if big else " (pure python)"),
                                            ok=ok, ms=ms, msg=msg))
            elif f == "duality.json":
                ok, ms, msg = run_checker("check_duality.py", [p])
                entry["checks"].append(dict(cert=f, checker="check_duality.py",
                                            ok=ok, ms=ms, msg=msg))
        out[code] = entry
        for c in entry["checks"]:
            flag = "OK " if c["ok"] else "FAIL"
            print(f"{flag} {code:10s} {c['cert']:24s} {c['ms']:>9.1f} ms  {c['msg']}")
    with open(os.path.join(HERE, "manifest.json"), "w") as f:
        json.dump(out, f, indent=1)
    bad = [1 for e in out.values() for c in e["checks"] if not c["ok"]]
    print(f"\n{'ALL CHECKS PASSED' if not bad else str(len(bad)) + ' FAILURES'}")


if __name__ == "__main__":
    main()
