#!/usr/bin/env python3
"""Independent LRAT proof checker (stdlib only, RUP steps with hints; RAT steps
per LRAT spec with negative-id hints). Shares no code with the generator/solver.

Usage: lrat_check.py formula.cnf proof.lrat
Prints VERIFIED iff the proof derives the empty clause from the formula with
every step checking out. Exit 0 on success, 1 on any failure.

Checking model:
- clauses stored by id; original clauses are 1..m in file order.
- addition step "<id> <lits> 0 <hints> 0": assume negation of <lits>; process
  hints in order: each positive hint id must reference a clause that is, under
  the current partial assignment, either falsified (-> conflict, step verified)
  or unit (-> extend assignment). If hints contain negative ids, the step is
  checked as a RAT step on the first literal of <lits>.
- deletion step "<id> d <ids> 0": remove clauses.
- The proof must contain an addition of the empty clause; everything after it is
  ignored.
"""
import gzip
import os
import sys


def _open_text(path):
    """Open a file that may be gzipped, without invoking any external tool.

    PROTOCOL section 10: the checker must be stdlib-only and OS-independent by
    construction, so packed proofs are read with the gzip module rather than by
    shelling out to gunzip. A .lrat and a .lrat.gz are interchangeable inputs.
    """
    if path.endswith(".gz"):
        return gzip.open(path, "rt")
    if not os.path.exists(path) and os.path.exists(path + ".gz"):
        return gzip.open(path + ".gz", "rt")
    return open(path)


def parse_cnf(path):
    clauses = {}
    idx = 0
    for line in _open_text(path):
        line = line.strip()
        if not line or line[0] in "pc%":
            continue
        lits = [int(t) for t in line.split()]
        if lits and lits[-1] == 0:
            lits = lits[:-1]
        if lits or line.startswith("0"):
            idx += 1
            clauses[idx] = tuple(lits)
    return clauses, idx


def unit_propagate_hints(clauses, assign, hints):
    """assign: dict lit->True for assigned-true literals. Process positive hints
    to a fixpoint. SOUNDNESS NOTE: hints are only guidance; we use a hint clause
    only when it is genuinely falsified (-> conflict) or unit (-> forced
    assignment) under the current assignment. Satisfied or not-yet-unit hints
    are skipped/retried; skipping cannot create unsound conclusions, it can only
    fail to reach a conflict. A missing (deleted/undefined) hint id fails hard.
    Returns 'conflict' on success, else an error/None after fixpoint."""
    pending = list(hints)
    while pending:
        progress = False
        nxt = []
        for h in pending:
            cl = clauses.get(h)
            if cl is None:
                return "missing:%d" % h
            unassigned = None
            state = "falsified"
            for lit in cl:
                if lit in assign:
                    state = "satisfied"
                    break
                if -lit in assign:
                    continue
                if unassigned is None:
                    unassigned = lit
                    state = "unit"
                else:
                    state = "non-unit"
                    break
            if state == "falsified":
                return "conflict"
            if state == "unit":
                assign[unassigned] = True
                progress = True
            elif state == "non-unit":
                nxt.append(h)
            # satisfied: drop
        if not progress:
            return None
        pending = nxt
    return None


def check_step(clauses, lits, hints):
    assign = {}
    for lit in lits:
        assign[-lit] = True
    if any(h < 0 for h in hints):
        # RAT step. Split: leading positive hints = RUP part.
        i = 0
        while i < len(hints) and hints[i] > 0:
            i += 1
        r = unit_propagate_hints(clauses, assign, hints[:i])
        if r == "conflict":
            return True
        if r is not None:
            return False
        if not lits:
            return False
        pivot = lits[0]
        # gather RAT groups: -cid followed by its positive hints
        groups = []
        j = i
        while j < len(hints):
            if hints[j] >= 0:
                return False
            cid = -hints[j]; j += 1
            hs = []
            while j < len(hints) and hints[j] > 0:
                hs.append(hints[j]); j += 1
            groups.append((cid, hs))
        listed = {cid for cid, _ in groups}
        # every clause containing -pivot must be listed (deleted ones excluded)
        for cid, cl in clauses.items():
            if -pivot in cl and cid not in listed:
                return False
        for cid, hs in groups:
            cl = clauses.get(cid)
            if cl is None:
                return False
            a2 = dict(assign)
            ok = False
            skip = False
            for lit in cl:
                if lit == -pivot:
                    continue
                if lit in a2:
                    skip = True  # resolvent tautological/satisfied
                    break
                if -lit not in a2:
                    a2[-lit] = True
            if skip:
                continue
            r = unit_propagate_hints(clauses, a2, hs)
            if r != "conflict":
                return False
        return True
    r = unit_propagate_hints(clauses, assign, hints)
    return r == "conflict"


def main():
    cnf_path, proof_path = sys.argv[1], sys.argv[2]
    clauses, top = parse_cnf(cnf_path)
    steps = 0
    empty_derived = False
    with _open_text(proof_path) as f:
        for line in f:
            toks = line.split()
            if not toks:
                continue
            if toks[1] == "d":
                for t in toks[2:-1]:
                    clauses.pop(int(t), None)
                continue
            ints = [int(t) for t in toks]
            cid = ints[0]
            rest = ints[1:]
            # split lits and hints on the first 0
            z = rest.index(0)
            lits = rest[:z]
            hints = rest[z + 1:]
            if hints and hints[-1] == 0:
                hints = hints[:-1]
            if not check_step(clauses, lits, hints):
                print("FAILED at step id %d (line: %s)" % (cid, line.strip()[:120]))
                return 1
            clauses[cid] = tuple(lits)
            steps += 1
            if not lits:
                empty_derived = True
                break
    if empty_derived:
        print("VERIFIED: empty clause derived after %d checked steps" % steps)
        return 0
    print("FAILED: proof ended without empty clause (%d steps)" % steps)
    return 1


if __name__ == "__main__":
    sys.exit(main())
