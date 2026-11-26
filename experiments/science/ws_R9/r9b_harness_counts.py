#!/usr/bin/env python3
"""R9 follow-up (b): THE THEORY DIVISION'S CODE with a driver of mine — not a replication.

The theory report says that "both implementations" give 4, 8, 16, 40, 96, 256, 636, 1680 clean bridges among
4, 8, 20, 48, 116, 312, 804, 2144 bridges with 3..10 beads.  Their published outputs show these numbers for one
implementation (out_t4_semigroup.txt: mylat.py / concat_check.py) and, for the other (the harness), only the totals for
3..8 beads (falsification_output.txt, XVIII.7: bridges=508, clean=420).  This driver counts with the harness helpers
(ls_enum, ls_concat, ls_profile) and the function `clean` copied verbatim from their t4_lattice_index.py.
The harness module is executed exactly as t4_lattice_index.py does it (importlib, no bytecode written).

usage: r9b_harness_counts.py [path of the export]
"""
import sys, importlib.util, os
E2 = sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_24a3c27"
sys.argv = ['x']
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("harness", os.path.join(E2, "experiments", "falsify_conjectures.py"))
H = importlib.util.module_from_spec(spec)
spec.loader.exec_module(H)
z3 = H.ls_enum(3, bridge=True)[0]
diff = lambda a, b: tuple(a[k] - b[k] for k in range(4))


def clean(w):                                   # verbatim from their t4_lattice_index.py
    if w[-2][1] - w[-3][1] != 1:
        return False
    top, _, _ = H.ls_concat(w, z3, 0); bot, _, _ = H.ls_concat(z3, w, 0)
    return diff(H.ls_profile(top), H.ls_profile(w)) == (0,0,0,0) and diff(H.ls_profile(bot), H.ls_profile(w)) == (0,0,0,0)


published = {3: (4, 4), 4: (8, 8), 5: (16, 20), 6: (40, 48), 7: (96, 116), 8: (256, 312), 9: (636, 804), 10: (1680, 2144)}
mine_fixed = {3: (1, 1), 4: (2, 2), 5: (4, 5), 6: (10, 12), 7: (24, 29), 8: (64, 78), 9: (159, 201), 10: (420, 536), 11: (1115, 1433)}
print("harness helpers (their code): N, bridges returned by ls_enum(N, bridge=True), clean among them (their function), distinct first-two-bond pairs")
tb = tc = 0
for N in range(3, 12):
    br = H.ls_enum(N, bridge=True)
    nc = sum(1 for w in br if clean(w))
    starts = len({(tuple(w[1][k] - w[0][k] for k in range(3)), tuple(w[2][k] - w[1][k] for k in range(3))) for w in br})
    if N <= 8:
        tb += len(br); tc += nc
    note = ""
    if N in published:
        note = "  = published (clean, bridges)" if published[N] == (nc, len(br)) else f"  published: {published[N]}"
    m = mine_fixed[N]
    note += f";  my first-round counts with the first two bonds fixed: {m}, times {starts}: {(m[0] * starts, m[1] * starts)}"
    print(f"  N = {N:2d}: bridges {len(br):5d}, clean {nc:5d}, first-two-bond pairs {starts}{note}")
print(f"totals for 3..8 beads: bridges {tb}, clean {tc}   (their harness line XVIII.7: bridges=508, clean=420)")
