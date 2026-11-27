"""R7 OWN: certified branch and bound (own_certified_bb.py) on every lattice cell whose published optimum is not already
certified by the LP bound (22 cells), and optionally on the bracket lower ends that are solver bounds (10 cells).
Identical instances (e.g. eps = 0 and eps = N/20 for N < 20) are solved once.
   python3 own_certified_bb_all.py optima|brackets MAX_SECONDS [nmin nmax]
"""
import hashlib, json, sys, time
import numpy as np
import own_lattice_cert as lc
from own_certified_bb import CertifiedBB, reduce_instance

mode, max_seconds = sys.argv[1], float(sys.argv[2])
nmin = int(sys.argv[3]) if len(sys.argv) > 3 else 1
nmax = int(sys.argv[4]) if len(sys.argv) > 4 else 24
dual = json.load(open("out_own_lattice_dual_1_18.json")) + json.load(open("out_own_lattice_dual_19_24.json"))
if mode == "optima":
    todo = [(r["n"], r["key"], r["N_cov"]) for r in dual if r["eng_proved"] and not r["certified_optimal"]]
else:
    todo = [(r["n"], r["key"], r["eng_lower_solver"]) for r in dual if (not r["eng_proved"]) and r["eng_lower_solver"] > r["own_certified_lb"]]
todo = [t for t in todo if nmin <= t[0] <= nmax]
sys.setrecursionlimit(10000)
done = {}
out = []
for n, key, target in todo:
    hist, count, gmin = lc.read_table(n)
    L, eps = lc.parse_key(key, n + 3)
    M = lc.cover_matrix(lc.l1_matrix(hist), gmin, L, eps)
    h = (n, target, hashlib.sha256(np.packbits(M).tobytes()).hexdigest())
    if h in done:
        rec = dict(done[h]); rec.update(key=key, same_instance_as=done[h]["key"])
    else:
        R, rows, cols = reduce_instance(M)
        bb = CertifiedBB(R, target, max_nodes=10 ** 7, max_seconds=max_seconds)
        bb.solve([], np.zeros(R.shape[0], dtype=bool), np.zeros(R.shape[1], dtype=bool))
        rec = dict(n=n, key=key, target=target, reduced=list(R.shape), nodes=bb.nodes, pruned_by_certified_bound=bb.pruned_bound,
                   pruned_infeasible=bb.pruned_infeasible, max_depth=bb.max_depth, complete=not bb.incomplete,
                   smaller_cover_found=bb.found_cover is not None, seconds=round(time.time() - bb.t0, 1))
        done[h] = rec
    out.append(rec)
    print(rec, flush=True)
    json.dump(out, open(f"out_own_certified_bb_{mode}_{nmin}_{nmax}.json", "w"), indent=1)
