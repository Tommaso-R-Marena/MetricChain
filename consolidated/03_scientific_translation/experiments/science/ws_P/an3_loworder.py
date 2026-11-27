"""Analysis 3a: best approximation of each residual by low-order functions of the torsions
(sum of single-torsion terms; torsion pairs within a window; residue tables; residue pairs),
on the clash-free domain.  Least squares (RMS-optimal) and Chebyshev LP (sup-optimal).
usage: python3 an3_loworder.py alphabet n [--lp] [--names GB,...]"""
import sys, os, json, time
import numpy as np
from analysis_lib import *

alphabet, n = sys.argv[1], int(sys.argv[2])
do_lp = "--lp" in sys.argv
names = ["GB", "coul+GB", "ff03-ff14SB", "ff15ipq-ff14SB", "ff19SB-ff14SB", "ff99SB-ff14SB", "OBC2-GBn2", "GBSA"]
if "--names" in sys.argv:
    names = sys.argv[sys.argv.index("--names") + 1].split(",")
TAU = 0.7
d = load(alphabet, n); R = residuals(d); m = d["m"]; k = d["k"]
mask = d["clash"] > TAU
st = states_of(mask)
M = len(st)
rng = np.random.default_rng(7)
perm = rng.permutation(M); half = M // 2
tr, te = perm[:half], perm[half:]
models = [("1body", None), ("res1", None)]
for w in (1, 2, 3, 5, 7, None):
    if w is None or w < m - 1:
        models.append(("2body", w))
models += [("res2", 1), ("res2", None)]
if m <= 12:
    models += [("3body", 3), ("res3", 2)]
if m <= 8:
    models += [("3body", None)]
res_path = os.path.join(HERE, "out", "an3_loworder.json")
results = json.load(open(res_path)) if os.path.exists(res_path) else {}
print(f"=== {alphabet} n={n}: {M} clash-free conformations (tau={TAU}); kT = {KT300:.4f} kcal/mol")
print(f"{'residual':16s} {'model':12s} {'npar':>6s} {'std(g)':>7s} {'RMS_LS':>7s} {'max_LS':>7s} {'testRMS':>8s} {'testMax':>8s} {'eta_sup':>8s} {'eta_sup/kT':>10s}")
for name in names:
    if name not in R:
        continue
    y = R[name][mask]
    for kind, w in models:
        subs = model_subsets(m, kind, w)
        A, _ = design_subsets(st, k, subs)
        npar = A.shape[1]
        if npar > 0.8 * M:
            continue
        pred, th = fit_ls(A, y)
        r = y - pred
        # generalisation: fit on half, test on the other half
        ptr, thtr = fit_ls(A[tr], y[tr])
        rte = y[te] - A[te] @ thtr
        eta = float("nan")
        if do_lp and npar <= 3000 and M * len(subs) < 4e6:
            t0 = time.time()
            eta, _ = fit_sup(A, y, time_limit=900)
        tag = f"{kind}" + (f"(w={w})" if w is not None else "")
        print(f"{name:16s} {tag:12s} {npar:6d} {y.std():7.3f} {np.sqrt((r**2).mean()):7.3f} {np.abs(r).max():7.3f} {np.sqrt((rte**2).mean()):8.3f} {np.abs(rte).max():8.3f} {eta:8.3f} {eta/KT300:10.2f}", flush=True)
        results[f"{alphabet}|{n}|{name}|{tag}"] = dict(npar=int(npar), M=int(M), std=float(y.std()), rms=float(np.sqrt((r**2).mean())),
                                                     max_ls=float(np.abs(r).max()), test_rms=float(np.sqrt((rte**2).mean())),
                                                     test_max=float(np.abs(rte).max()), eta_sup=eta)
json.dump(results, open(res_path, "w"), indent=0)
