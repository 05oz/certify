# PENDING

The independent certificate checker (`certify_check.py`) is not yet part of this snapshot; it lands here from the week-1 build. It will walk the schema (see `../schema/`), re-run every verifier, compare msolve outputs against the stored `certificates/out_*.txt` files, and exit nonzero on any mismatch.

Until it lands, run the verifiers by hand per the quickstart in `../README.md`.
