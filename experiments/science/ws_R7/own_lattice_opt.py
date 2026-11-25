"""R7 OWN test of the sentences "all published covering numbers are solver-proved optima" and "two solvers
agree on every cover" (ENG-RES-0002) on a sample of lattice cells.

For each requested cell (n, key):
  1. tolerance-free LP-duality lower bound (own_lattice_cert.certified_lb);
  2. if it is below the published N_cov: HiGHS (scipy.optimize.milp, my own formulation on the UNREDUCED matrix,
     mip_rel_gap = 0) and CP-SAT (OR-Tools, one worker, my own formulation on the UNREDUCED matrix), each with a
     time limit; the incumbent of each solver is re-checked against the boolean matrix.
Nothing from the engineering code is imported; the engineering class tables and published numbers are read.

  PYTHONPATH=<dir with ortools> python3 own_lattice_opt.py TIME_LIMIT n:key [n:key ...]
  key examples: "L=1,eps=0"  "L=1,eps=1/4*N"   ;  "all" for the 12 cells of that n
"""
import json
import math
import sys
import time

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csr_matrix

import own_lattice_cert as lc


def highs_cover(M, time_limit):
    C = M.shape[0]
    res = milp(c=np.ones(C), constraints=LinearConstraint(csr_matrix(M.T.astype(float)), lb=np.ones(M.shape[1]), ub=np.inf),
               integrality=np.ones(C), bounds=Bounds(0, 1), options=dict(time_limit=time_limit, mip_rel_gap=0.0))
    out = dict(status=int(res.status))
    if res.x is not None:
        ch = np.nonzero(res.x > 0.5)[0]
        out.update(primal=int(len(ch)), feasible=bool(M[ch].any(axis=0).all()))
    out["bound"] = float(getattr(res, "mip_dual_bound", float("nan")))
    return out


def cpsat_cover(M, time_limit):
    from ortools.sat.python import cp_model
    model = cp_model.CpModel()
    x = [model.NewBoolVar(f"x{a}") for a in range(M.shape[0])]
    for c in range(M.shape[1]):
        model.AddBoolOr([x[int(a)] for a in np.nonzero(M[:, c])[0]])
    model.Minimize(sum(x))
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = 1
    s.parameters.max_time_in_seconds = time_limit
    st = s.Solve(model)
    out = dict(status=s.StatusName(st))
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        ch = [a for a in range(M.shape[0]) if s.Value(x[a])]
        out.update(primal=len(ch), feasible=bool(M[ch].any(axis=0).all()), bound=float(s.BestObjectiveBound()))
    return out


if __name__ == "__main__":
    tl = float(sys.argv[1])
    res = json.loads((lc.ENG / "results" / "lattice_Sc12.json").read_text())
    rows = {r["n_torsions"]: r for r in res["rows"]}
    out = []
    tag = "_".join(a.replace("/", "o").replace("*", "").replace(",", "").replace("=", "").replace(":", "-") for a in sys.argv[2:])[:80]
    for arg in sys.argv[2:]:
        ns, key = arg.split(":", 1)
        n = int(ns)
        hist, count, gmin = lc.read_table(n)
        D = lc.l1_matrix(hist)
        keys = list(rows[n]["cover"]) if key == "all" else [key]
        for k in keys:
            cell = rows[n]["cover"][k]
            L, eps = lc.parse_key(k, n + 3)
            M = lc.cover_matrix(D, gmin, L, eps)
            t0 = time.time()
            lb, lp, _ = lc.certified_lb(M)
            rec = dict(n=n, key=k, classes=int(M.shape[0]), published=cell["N_cov"], published_proved=cell["proved_optimal"],
                       eng_solvers=cell["solvers"], certified_lb=lb, lp=lp)
            if lb < cell["N_cov"]:
                t1 = time.time(); rec["highs"] = highs_cover(M, tl); rec["highs"]["seconds"] = round(time.time() - t1, 1)
                t1 = time.time(); rec["cpsat"] = cpsat_cover(M, tl); rec["cpsat"]["seconds"] = round(time.time() - t1, 1)
            rec["seconds"] = round(time.time() - t0, 1)
            out.append(rec)
            print(rec, flush=True)
            json.dump(out, open(f"out_own_lattice_opt_{tag}.json", "w"), indent=1)
