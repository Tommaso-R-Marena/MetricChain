"""R28 — can the upper end (c) of Proposition A17.24 be kept a PAIR model?

As stated, the penalty of site i is c_i(s)^2 / 8 with c_i = sum over the terms T containing i of o_{T,i}(s_T):
a factor that couples all the sites of all the terms containing i (three sites on a chain; a whole neighbourhood
in a dense pair model).  By Cauchy-Schwarz, for weights w_T > 0 with sum 1,
        (sum_T o_T)^2  <=  sum_T o_T^2 / w_T ,
so  exp(-sum_T [ R_T - sum_{i in T, H} o_{T,i}^2 / (8 w_{T,i}) ])  is still an upper end and IS a model on the
interaction sets of V.  This script measures the price on the toy chain (their instance A), all coordinates in
mode H, equal weights (w = 1/2 at interior sites, 1 at the two ends).
Control: weights that sum to 2 (i.e. the penalty halved) must give a value BELOW the stated upper end somewhere
and can exclude the exact value; the relaxed end can never be below the stated end (asserted).
"""
import r28_common as rc
rc.cap()
import time
import numpy as np
from scipy.special import logsumexp
import toy_lib as tl

t0 = time.time()
print("R28 toy_pairwise.py  start", rc.utc())
n, N = 8, 1440
rng = np.random.default_rng(20261126)
phi = rng.uniform(0, 2 * np.pi, n)
theta = rng.uniform(0, 2 * np.pi, n - 1)
x = tl.grid(N)
e = [1.5 * (1.0 + np.cos(3.0 * x + phi[i])) for i in range(n)]
pair = [2.0 * np.cos(x[:, None] - x[None, :] - theta[i]) for i in range(n - 1)]
ch = tl.Chain([np.exp(-ee) for ee in e], pair, None)
ex = ch.lnZ_exact()
print(" k   all-H width per angle: stated (3-site penalty) | pair-model relaxation (equal weights) | ratio | relaxed >= stated | exact inside | control (weights summing to 2) below the stated end / excludes exact")
bad = 0
for k in (3, 6, 12, 24, 48, 96, 144, 288):
    idx, tw = tl.cell_index(N, k)
    cs = tl.Cells(ch, idx, tw)
    lj = cs.lnZ_jensen()
    lH = cs.lnZ_upper(cs.all_H())

    def pair_upper(wsum):
        tabs = []
        for i in range(n - 1):
            wl = 1.0 if i == 0 else 0.5 * wsum            # weight of term i at its left site i
            wr = 1.0 if i == n - 2 else 0.5 * wsum        # weight of term i at its right site i+1
            tabs.append(cs.A[i] - cs.oL[i] ** 2 / (8.0 * wl) - cs.oR[i] ** 2 / (8.0 * wr))
        return cs._lnZ_pairwise(tabs)
    lP = pair_upper(1.0)
    lC = pair_upper(2.0)
    ok = lP >= lH - 1e-10 and ex <= lP + 1e-10
    bad += not ok
    print(f"{k:4d}   {(lH - lj)/n:.4e} | {(lP - lj)/n:.4e} | {(lP - lj)/(lH - lj):.3f} | {lP >= lH - 1e-10} | {ex <= lP + 1e-10} | {lC < lH} / {ex > lC}")
print(f"violations: {bad} (must be 0)")
rc.finish(t0)
