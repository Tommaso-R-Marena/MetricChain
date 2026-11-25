"""Model-free identified interval of the gauche fraction given the mean three-shell profile,
for diamond-lattice chains up to 24 torsions (27 beads), from the engineering division's exact
class tables (research/ubuntu-engineering at db56d05, experiments/eng/chain_cover/data/).

Each table row is a profile class: (c3, c8, c11), number of conformations, least and largest
number of gauche torsions in the class.  For a truth whose weight depends on the profile only
(athermal; attractive exp(eps*c3)), the mean profile m is computable from the table, and the
exact range of the mean gauche fraction over ALL ensembles with mean profile m is

    [ min sum_k p_k gmin_k ,  max sum_k p_k gmax_k ]   s.t.  sum_k p_k prof_k = m,  p a probability vector

(the vertical chord, at m, of the convex hull of {(profile, #gauche)} -- at finite N the object
whose normalised limit is the convex body of theory report section 11.22).
"""
import sys, json, glob, os
import os
import numpy as np
from scipy.optimize import linprog
from dia_chain import load_eng_table

ENG = os.environ.get("MC_ENG_DATA", "eng_ro/experiments/eng/chain_cover/data")   # see experiments/science/README.md

def chord(prof, gmin, gmax, m):
    K = len(prof)
    A = np.vstack([prof.T.astype(float), np.ones(K)]); b = np.concatenate([m, [1.0]])
    sc = np.maximum(np.abs(A).max(axis=1), 1.0); A = A / sc[:, None]; b = b / sc
    lo = linprog(gmin.astype(float), A_eq=A, b_eq=b, bounds=(0, None), method="highs")
    hi = linprog(-gmax.astype(float), A_eq=A, b_eq=b, bounds=(0, None), method="highs")
    assert lo.status == 0 and hi.status == 0
    return lo.fun, -hi.fun

rows = []
print(" n   N   classes   truth        mean profile/N (c3,c8,c11)        identified gauche fraction     width")
for n in range(2, 25):
    meta, tab = load_eng_table(f"{ENG}/dia_Sc12_n{n}.txt")
    prof = tab[:, :3]; cnt = tab[:, 3].astype(float); gmin = tab[:, 4]; gmax = tab[:, 6]
    N = n + 3
    for name, w in (("athermal", cnt), ("attract0.5", cnt * np.exp(0.5 * prof[:, 0]))):
        p = w / w.sum(); m = p @ prof
        lo, hi = chord(prof, gmin, gmax, m)
        rows.append(dict(n=n, N=N, classes=len(tab), truth=name, mean_profile=m.tolist(),
                         lo=lo / n, hi=hi / n, width=(hi - lo) / n))
        print(f"{n:2d}  {N:2d}  {len(tab):6d}   {name:11s}  ({m[0]/N:.4f}, {m[1]/N:.4f}, {m[2]/N:.4f})   "
              f"[{lo/n:.4f}, {hi/n:.4f}]   {(hi-lo)/n:.4f}")
json.dump(rows, open("identified_from_eng_tables.json", "w"), indent=1)
