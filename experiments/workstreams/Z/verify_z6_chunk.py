#!/usr/bin/env python3
"""verify_z6_chunk.py u J0 J1 K  --  the independent exact checker on levels J0..J1 of a run of z6_certified_tops.py.

The checker is `review_a6/a6_02_verify_z6_output.py` (written by the referee of the addendum; it shares no
code with the script it checks).  Its source is read unchanged; ONE line is replaced in memory — the range
of its verification loop, `range(1, JLEV + 1)` -> `range(J0, JLEV + 1)` — so that a long run can be verified in
several processes.  The construction itself (the script's own `step`) is always run from level 1 to J1; only
the exact verification of the levels below J0 is left to another chunk.  Negative controls are skipped
("nocontrols"): they are in the stored outputs of the short runs.

Used in Phase II for the 400-level run (u = 1, K = 4000), which two referees had left unchecked:
    python3 -B verify_z6_chunk.py 1 1 134 4000 ; ... 1 135 267 4000 ; ... 1 268 400 4000
Outputs: out_verify_z6_u1_K4000_levels_*.txt
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
u_str, J0, J1, K = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
path = os.path.join(HERE, "review_a6", "a6_02_verify_z6_output.py")
src = open(path).read()
old = 'for j in range(1, JLEV + 1):\n    verify_level(curves[j - 1], curves[j]'
assert src.count(old) == 1, "the checker's verification loop was not found"
src = src.replace(old, 'for j in range(%d, JLEV + 1):\n    verify_level(curves[j - 1], curves[j]' % J0)
print("# verify_z6_chunk.py: levels %d..%d of the run u = %s, K = %s (checker: review_a6/a6_02_verify_z6_output.py, loop range patched in memory)" % (J0, J1, u_str, K), flush=True)
sys.argv = [path, u_str, str(J1), K, "nocontrols"]
exec(compile(src, path, "exec"), {"__name__": "__main__", "__file__": path})
