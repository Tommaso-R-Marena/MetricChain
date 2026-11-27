"""R7 RE-RUN of the engineering division's own two solvers on its own REDUCED instances (functions of
src/metricchain_eng/chains/profile_cover.py at a2f6dc7, imported from the exported work tree given as argv[1]).

Question: does each of the two solvers PROVE the published optimum on its own?  The stored rows for n <= 18 record only
the size found by each solver ({'highs': k, 'cpsat': k}) and one flag `proved_optimal`.
Here: one worker for CP-SAT (this machine allows one core; engineering used 8 workers on 4 cores).
   PYTHONPATH=<ortools dir> python3 rerun_eng_two_solvers.py <eng work tree> TIME_LIMIT n:key [n:key ...]
"""
import json, sys, time
from fractions import Fraction as Fr
from pathlib import Path
W = Path(sys.argv[1]); sys.path.insert(0, str(W / "src"))
from metricchain_eng.chains.profile_cover import (parse_enum_output, cover_matrix_P, reduce_cover, min_cover_highs,
                                                   min_cover_cpsat, certified_lower_bound, greedy_cover)
tl = float(sys.argv[2])
stored = {r["n_torsions"]: r for r in json.load(open(W / "experiments/eng/chain_cover/results/lattice_Sc12.json"))["rows"]}
out = []
for arg in sys.argv[3:]:
    ns, key = arg.split(":", 1); n = int(ns)
    tab = parse_enum_output((W / f"experiments/eng/chain_cover/data/dia_Sc12_n{n}.txt").read_text())
    L = Fr(key.split(",")[0].split("=")[1]); e = key.split("=")[-1]
    eps = Fr(e[:-2]) * tab.n_beads if e.endswith("*N") else Fr(e)
    M = cover_matrix_P(tab, L, eps)
    R, rows, cols = reduce_cover(M)
    rec = dict(n=n, key=key, published=stored[n]["cover"][key]["N_cov"], stored_solvers=stored[n]["cover"][key]["solvers"],
               reduced=list(R.shape), certified=certified_lower_bound(M, R, cols), greedy=len(greedy_cover(R)))
    t0 = time.time(); size, chosen, ok, bound = min_cover_highs(R, time_limit=tl)
    rec["highs"] = dict(size=size, proved=ok, bound=bound, seconds=round(time.time() - t0, 1))
    t0 = time.time(); size, chosen, ok, bound = min_cover_cpsat(R, time_limit=tl, workers=1)
    rec["cpsat_1_worker"] = dict(size=size, proved=ok, bound=bound, seconds=round(time.time() - t0, 1))
    out.append(rec); print(rec, flush=True)
json.dump(out, open("out_rerun_eng_two_solvers.json", "w"), indent=1)
