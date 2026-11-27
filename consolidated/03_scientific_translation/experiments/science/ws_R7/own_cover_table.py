"""R7 OWN: the 12 cells (L in {1, 1/5}) x (eps in {0, 1, N/20, N/10, N/4, N/2}) of the generic-chain cover table.
Own code (own_gen / own_cover), written before reading engineering code."""
import json, math, sys, time
import numpy as np
import own_cover as oc

def cells(N):
    return [(L, name, eps) for L in (1.0, 0.2) for name, eps in
            (("0", 0.0), ("1", 1.0), ("N/20", N / 20.0), ("N/10", N / 10.0), ("N/4", N / 4.0), ("N/2", N / 2.0))]

if __name__ == "__main__":
    n0, n1, tl = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
    only = sys.argv[4].split(",") if len(sys.argv) > 4 else None
    res = []
    for n in range(n0, n1 + 1):
        cd = oc.class_data(n)
        D = oc.dist_matrix(cd["Srep"])
        N = n + 3
        for (L, name, eps) in cells(N):
            if only and f"{L}:{name}" not in only:
                continue
            t0 = time.time()
            # optional 5th argument: time limit for the L = 1 cells (0 = bounds only)
            tl_cell = float(sys.argv[5]) if (len(sys.argv) > 5 and L == 1.0) else tl
            r = oc.run(n, L, eps, time_limit=tl_cell, cd=cd, D=D)
            r["eps_name"] = name
            r["seconds"] = time.time() - t0
            res.append(r)
            print(f"n={n} L={L} eps={name}: classes={r['classes']} greedy={r['greedy']} LP={r['lp']:.4f} "
                  f"certLB={r['lp_certified_ceil']} MILP primal={r.get('primal')} dual={r['dual_bound']} "
                  f"feas={r.get('primal_feasible_checked')} margin={r['min_margin']:.3e} status={r['status']} "
                  f"t={r['seconds']:.1f}s", flush=True)
            json.dump(res, open(f"out_own_cover_table_{n0}_{n1}.json", "w"), indent=1, default=str)
