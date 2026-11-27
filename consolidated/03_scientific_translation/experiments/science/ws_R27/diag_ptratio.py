#!/usr/bin/env python3
"""R27 diagnostic: the per-point ratios > 1 printed by item2_adv_fixedX_run1 (stopped run) -- real violation or rounding noise?
For reflected tails the windows before the reflection have e_j = 0 exactly up to rounding, so local_k ~ 1e-15 and dist_k ~ 1e-15."""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np, resource, time
from r27lib import cap_memory, peak_mb, now, helix, chain_consts, pair_arrays, eta_vec, window_pair_index, procrustes, local_weights
from thmL_steps import check_pair
cap_memory(2.0)
def reflect(X, i, tail=True):
    nrm = np.cross(X[i + 2] - X[i + 1], X[i + 3] - X[i + 1]); nrm /= np.linalg.norm(nrm)
    Y = X.copy(); sl = slice(i + 4, None) if tail else slice(0, i + 1)
    Y[sl] = X[sl] - 2 * ((X[sl] - X[i + 1]) @ nrm)[:, None] * nrm[None, :]
    return Y
for n in (8, 20):
    X = helix(n, 2.3, 1.5, 100.0)
    tau, s, b = chain_consts(X); J, K = pair_arrays(n); widx = window_pair_index(n, J, K)
    M = local_weights(X, tau, s)
    for i in range(n - 4):
        Y = reflect(X, i, True)
        et = eta_vec(X, Y, J, K)
        e = np.array([np.linalg.norm(et[ix]) for ix in widx])
        loc = M @ e
        R1, t1, _ = procrustes(X[:5], Y[:5])
        dist = np.linalg.norm(Y - X @ R1 - t1, axis=1)
        bad = [(k, dist[k], loc[k]) for k in range(n) if dist[k] > loc[k]]
        out, viol, ctl = check_pair(X, Y)
        print(f"n={n} reflection at window {i}: points with dist_k > local_k: " + (", ".join(f"k={k}: dist {d:.2e} local {l:.2e}" for k, d, l in bad) or "none")
              + f"   | checker with noise floor: violations {len(viol)}, max per-point ratio {out['S3  (local) |y_k - g x_k| <= local_k']:.4f}")
print(f"ALL DONE {now()} peak memory {peak_mb():.0f} MB")
