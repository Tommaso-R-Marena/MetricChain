#!/usr/bin/env python3
"""Workstream R27 -- two small computations for the report.

 (1) Lemma Q as a usable bound for ONE five-point window (all ten distances measured), idealised traces: the RMSD bound
        kappa ||eta||_2 / (s sqrt(5)),   ||eta||_2 <= sigma sqrt(sum (2 d_jk + sigma)^2)   (every |distance error| <= sigma: worst allocation),
     against the worst RMSD actually found by maximising d_P of the window under the same constraint (SLSQP from many starts; a lower bound for the
     true worst case) -- so that the reader sees how much of the bound is real.
 (2) A variant of (local): the proof of Step 3 works with ANY window containing k; with the EARLIEST one, i-(k) = max(1, k-4), the sum has four
     fewer terms.  Checked on arbitrary Y:  |y_k - g1 x_k| <= delta_{i-} + sum_{j < i-} (delta_j + delta_{j+1}) (|x_k - c_{j+1}|/tau_{j+1} + 1/2).
     Control: the same with one further term dropped (i- replaced by i- - 1) must fail somewhere.
Run:  OMP_NUM_THREADS=1 python3 -B item4_extras.py > item4_extras_<stamp>.log
"""
import os, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import minimize
from r27lib import (cap_memory, peak_mb, now, KAPPA, helix, angle_chain, random_unit_chain, chain_consts, pair_arrays, eta_vec,
                    window_pair_index, procrustes, sigma3)

cap_memory(2.0)
t0 = time.time()
rng = np.random.default_rng(27125)
print(f"R27 item4_extras.py started {now()}")

print("\n(1) one five-point window with complete distances; every distance error at most sigma in absolute value (lengths in angstrom)")
print("    columns: trace | s | sigma | Lemma Q bound on the RMSD of the window | worst RMSD found under the same constraint | found/bound")
iu = np.triu_indices(5, 1)
for name, W in (("helix-like (2.3, 1.5, 100)", helix(5, 2.3, 1.5, 100.0)), ("strand-like 160", helix(5, 0.94, 3.3, 160.0)), ("strand-like 175", helix(5, 0.94, 3.3, 175.0))):
    d0 = np.linalg.norm(W[iu[0]] - W[iu[1]], axis=1)
    s = sigma3(W)
    for sig in (0.05, 0.1, 0.3, 0.5):
        bound = KAPPA * sig * np.sqrt(((2 * d0 + sig) ** 2).sum()) / s / np.sqrt(5)

        def neg(y):
            res = procrustes(W, y.reshape(5, 3))[2]
            return -(res * res).sum(), (-2 * res).ravel()

        cons = []
        for q in range(10):
            a, b = iu[0][q], iu[1][q]
            cons.append(dict(type="ineq", fun=lambda y, a=a, b=b, q=q: sig - (np.linalg.norm(y.reshape(5, 3)[a] - y.reshape(5, 3)[b]) - d0[q])))
            cons.append(dict(type="ineq", fun=lambda y, a=a, b=b, q=q: sig + (np.linalg.norm(y.reshape(5, 3)[a] - y.reshape(5, 3)[b]) - d0[q])))
        best = 0.0
        for trial in range(30):
            Y0 = W + sig * rng.normal(size=W.shape) * (0.3 if trial % 2 else 1.0)
            res = minimize(neg, Y0.ravel(), jac=True, method="SLSQP", constraints=cons, options=dict(maxiter=300, ftol=1e-12))
            Y = res.x.reshape(5, 3)
            de = np.linalg.norm(Y[iu[0]] - Y[iu[1]], axis=1) - d0
            if np.abs(de).max() <= sig * (1 + 1e-6):
                best = max(best, np.linalg.norm(procrustes(W, Y)[2]) / np.sqrt(5))
        print(f"    {name:28s} | {s:.4f} | {sig:4.2f} | {bound:7.3f} | {best:7.3f} | {best / bound:.3f}")

print("\n(2) (local) with the earliest window containing k")
tot = viol = ctl = 0; worst = 0.0
for rep in range(400):
    n = int(rng.integers(6, 25))
    X = [angle_chain, random_unit_chain][rep % 2](n, rng) if rep % 5 else helix(n, 0.94, 3.3, 170.0)
    tau, s, b = chain_consts(X)
    if tau.min() < 1e-6:
        continue
    J, K = pair_arrays(n); widx = window_pair_index(n, J, K)
    cW = np.array([X[i:i + 4].mean(0) for i in range(n - 3)])
    for q in range(12):
        kind = q % 6
        if kind == 0:
            Y = X + 10.0 ** rng.uniform(-4, 1) * rng.normal(size=X.shape)
        elif kind == 1:
            Y = rng.normal(size=X.shape) * 10.0 ** rng.uniform(-1, 1)
        elif kind == 2:
            i = int(rng.integers(0, n - 4))
            nrm = np.cross(X[i + 2] - X[i + 1], X[i + 3] - X[i + 1]); nrm /= np.linalg.norm(nrm)
            Y = X.copy(); Y[i + 4:] = X[i + 4:] - 2 * ((X[i + 4:] - X[i + 1]) @ nrm)[:, None] * nrm[None, :]
        elif kind == 3:
            Y = X.copy(); k0 = int(rng.integers(n)); Y[k0] += rng.normal(size=3) * 10.0 ** rng.uniform(-1, 3)
        elif kind == 4:
            Q, _ = np.linalg.qr(rng.normal(size=(3, 3))); k0 = int(rng.integers(1, n - 1))
            Y = X.copy(); Y[k0:] = (X[k0:] - X[k0]) @ Q + X[k0]
        else:
            u = rng.normal(size=3); u /= np.linalg.norm(u); Y = X @ (np.eye(3) - np.outer(u, u))
        et = eta_vec(X, Y, J, K)
        e = np.array([np.linalg.norm(et[ix]) for ix in widx])
        delta = KAPPA * e / s
        R1, t1, _ = procrustes(X[:5], Y[:5])
        dist = np.linalg.norm(Y - X @ R1 - t1, axis=1)
        scale = max(1.0, np.abs(X).max(), np.abs(Y).max())
        for k in range(n):
            im = max(0, k - 4)
            bound = delta[im] + sum((delta[j] + delta[j + 1]) * (np.linalg.norm(X[k] - cW[j + 1]) / tau[j + 1] + 0.5) for j in range(im))
            tot += 1
            if bound > 1e-7 * scale:
                worst = max(worst, dist[k] / bound)
                viol += int(dist[k] > bound * (1 + 1e-9))
            else:
                viol += int(dist[k] > 1e-9 * scale)
            if im >= 1:
                im2 = im - 1
                b2 = delta[im2] + sum((delta[j] + delta[j + 1]) * (np.linalg.norm(X[k] - cW[j + 1]) / tau[j + 1] + 0.5) for j in range(im2))
                ctl += int(dist[k] > b2 * (1 + 1e-9) + 1e-9 * scale)
print(f"    point-wise checks: {tot}   violations: {viol}   largest ratio: {worst:.4f}   CONTROL (one more term dropped: window i- - 1, which does not contain k): violated {ctl} times")
print(f"ALL DONE {now()}  {time.time() - t0:.1f} s  peak memory {peak_mb():.0f} MB")
