#!/usr/bin/env python3
"""R9, item 4 (consequence): exact points of K^br from the explicit bridges behind Theorem 11.71(c).

The nine box-64 bridges are RE-GENERATED with the authors' builder (experiments/workstreams/S/code/build.py at 5ed4072,
imported read-only, no bytecode written; the call sequence parse -> strands_in_box -> link -> make_bridge is the one
R2 used, keys from experiments/workstreams/S/out/witnesses.txt).  Everything else is MY code (r9_lat.py): lattice walk,
self-avoidance, bridge, (h,g) from coordinates, the end corrections A(x,c1) and B(x), cleanliness, and the check
that head 2 + x + tail 3 is a clean bridge with (h,g) + A + B.
Result: for each bridge the exact point qhat/(N+3) of K^br (Theorem R9.1(d)); then the hull volume of the exact
profile points (no erosion)."""
import sys, json, time
sys.dont_write_bytecode = True
sys.path.append("/home/user/MetricChain/experiments/workstreams/S/code")
import build as B                      # the authors' generator (someone else's code)
import r9_lat as L
import numpy as np
from scipy.spatial import ConvexHull

WIT = {
 "W3 woodpile (0,3,4;0)": "hnf rows (1 0 0) (0 1 2) (0 0 3); path bonds A(n)-type: A(0,0,1):a2,a3 A(0,0,2):a0,a1",
 "checkerboard (0,1,3;0)": "hnf rows (1 0 0) (0 1 1) (0 0 2); path bonds A(n)-type: A(0,0,1):a0,a1",
 "coplanar sheets (0,0,1;0)": "hnf rows (1 0 0) (0 1 1) (0 0 3); path bonds A(n)-type: A(0,0,2):a0,a1",
 "rods (1/2,2,5/2;0)": "hnf rows (1 0 0) (0 1 1) (0 0 4); path bonds A(n)-type: A(0,0,2):a0,a1 A(0,0,3):a0,a1",
 "crossed rods (1/2,4,9/2;0)": "hnf rows (1 0 0) (0 1 4) (0 0 5); path bonds A(n)-type: A(0,0,1):a2,a3 A(0,0,2):a2,a3 A(0,0,3):a0,a1 A(0,0,4):a0,a1",
 "crystal (1,5,6;0)": "hnf rows (1 0 0) (0 1 0) (0 0 1); path bonds A(n)-type: A(0,0,0):a0,a1",
 "gauche-rich (0,12/5,22/5;4/5)": "hnf rows (1 0 1) (0 1 4) (0 0 8); path bonds A(n)-type: A(0,0,2):a0,a3 A(0,0,4):a0,a2 A(0,0,5):a2,a3 A(0,0,6):a1,a2 A(0,0,7):a0,a1",
 "gauche-rich (1/3,5/3,3;2/3)": "hnf rows (1 0 2) (0 1 3) (0 0 6); path bonds A(n)-type: A(0,0,2):a0,a1 A(0,0,4):a0,a2 A(0,0,5):a1,a2",
 "all-gauche (0,1/2,9/4;1)": "hnf rows (1 0 4) (0 1 5) (0 0 10); path bonds A(n)-type: A(0,0,4):a0,a1 A(0,0,6):a0,a2 A(0,0,7):a1,a3 A(0,0,9):a2,a3",
}
W = int(sys.argv[1]) if len(sys.argv) > 1 else 64
ONLY = sys.argv[2] if len(sys.argv) > 2 else None      # optional: a substring of the system's name (e.g. "12/5" with W = 128)
stored = {r["N"]: tuple(r["hg"]) for r in json.load(open(
    "/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_658b77f/experiments/coordinator_checks/limit_shape_review/wit/verified.json")).values()}
rows = []
for name, w in WIT.items():
    if ONLY is not None and ONLY not in name:
        continue
    t0 = time.time()
    hnf, ch = B.parse(w)
    strands = B.strands_in_box(hnf, ch, (W, W, W))
    walk, nlink, dropped, ns = B.link(strands)
    b = B.make_bridge(walk)
    x = [tuple(int(c) for c in p) for p in b]
    N = len(x)
    assert L.check_walk(x) is None, L.check_walk(x)
    assert L.is_bridge(x)
    hg = L.profile(x)
    assert stored.get(N) == hg, (N, hg, stored.get(N))
    idx = {p: i for i, p in enumerate(x)}
    Bv = L.B_part(x, idx)
    out = []
    for c1 in L.admissible_c1(x):
        Av = L.A_part(x, c1, idx)
        y = L.extend(x, c1, 2, 3)
        assert L.check_walk(y) is None and L.is_bridge(y) and L.is_clean(y)
        assert L.profile(y) == tuple(hg[i] + Av[i] + Bv[i] for i in range(4))
        out.append((c1, Av))
    Av = out[0][1]
    q = tuple(hg[i] + Av[i] + Bv[i] for i in range(4))
    rows.append((name, N, hg, Av, Bv, q))
    print(f"{name:32s} N = {N:6d}  (h,g) = {hg} (= the stored counts)  A = {Av}  B = {Bv}  clean as built: {L.is_clean(x)}"
          f"  -> exact point of K^br: {tuple(round(c/(N+3), 5) for c in q)}   [{time.time()-t0:.0f} s]", flush=True)
json.dump([(n, N, list(hg), list(a), list(b), list(q)) for n, N, hg, a, b, q in rows], open(f"out/witness_ends_W{W}{'_only' if ONLY else ''}.json", "w"))
if ONLY is not None:
    sys.exit(0)
exact = [(0, 0, 0), (0.5, 2, 1.5), (1, 5, 6), (0, 0, 1)]
pts = np.array(exact + [[q[i] / (N + 3) for i in range(3)] for _, N, _, _, _, q in rows])
print(f"hull of the 4 exact points and the {len(rows)} exact points qhat/(N+3) (profile part): volume {ConvexHull(pts).volume:.6f}"
      f"   (report: 1.5632 after erosion of the hull of ten bridge densities, among them the 166 199-bead bridge, which is not rebuilt here)")
