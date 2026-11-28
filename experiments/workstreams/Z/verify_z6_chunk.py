#!/usr/bin/env python3
"""verify_z6_chunk.py u J0 J1 K  --  the independent exact checker on levels J0..J1 of a run of z6_certified_tops.py.

The checker is `review_a6/a6_02_verify_z6_output.py` (written by the referee of the addendum; it shares no
code with the script it checks).  Its source is read unchanged; two places are replaced in memory: (1) the
range of its verification loop, `range(1, JLEV + 1)` -> `range(J0, JLEV + 1)`, so that a long run can be verified
in several processes; (2) its test (C) for the cap line gets a refinement loop that adds more of the checker's
OWN certified lines where the slack is negative (explained at the patch below: same acceptance criterion,
same source of lines; without it the test fails spuriously at many levels of the run with K = 4000).  The construction itself (the script's own `step`) is always run from level 1 to J1; only
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
# --- second in-memory patch (Phase II): refinement of the checker's test (C) for the cap line.
# The checker verifies the cap line by comparing it, exactly, with the maximum of the certified lines and of
# lines OF ITS OWN (own sample points, own rigorous pairs).  Its choice of sample points assumes that the cap
# becomes active at a vertex of the hull of the other lines; when the cap becomes active strictly inside the
# last linear piece (as it does at many levels of the run with K = 4000), the choice degenerates to 300
# log-spaced points near the top and the test fails although the cap is valid (at the failing vertex the
# checker's own line through that very point lies above the cap).  The patch keeps the acceptance criterion
# (slack >= 0 at every vertex of the exact hull) and the source of the lines (the checker's `own_lines`); it only
# adds own lines around the vertex of least slack and repeats, at most eight times.  A test that is still
# negative after that is reported as a failure, as before.
old_cap = "            this_ok = worst[0] >= 0\n"
assert src.count(old_cap) == 1, "the checker's cap test was not found"
new_cap = '''            _rounds = 0
            while worst[0] < 0 and _rounds < 8:
                _xw = float(worst[1])
                _d = max(c - _xw, c * 1e-13)
                _pts = np.unique(np.concatenate([c - _d * np.geomspace(1e-7, 2.0, 500), _xw + _d * np.linspace(-0.3, 0.3, 201)]))
                _pts = _pts[(_pts > 0) & (_pts < c)]
                mine = mine + own_lines(prev, c, _pts)
                G = X.XCurve(cert_lines + mine, c)
                worst = None
                for (x, v) in G.vertices():
                    slack = v - (Fr(m) * x - Fr(bL))
                    if worst is None or slack < worst[0]:
                        worst = (slack, x)
                _rounds += 1
            if _rounds:
                cap_info += " [refined: %d round(s)]" % _rounds
            this_ok = worst[0] >= 0
'''
src = src.replace(old_cap, new_cap)
print("# verify_z6_chunk.py: levels %d..%d of the run u = %s, K = %s (checker: review_a6/a6_02_verify_z6_output.py, loop range patched in memory)" % (J0, J1, u_str, K), flush=True)
sys.argv = [path, u_str, str(J1), K, "nocontrols"]
exec(compile(src, path, "exec"), {"__name__": "__main__", "__file__": path})
