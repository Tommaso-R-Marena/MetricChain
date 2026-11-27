#!/usr/bin/env python3
"""Workstream R27, Item 2 (ii) -- ADVERSARIAL search over BOTH configurations (X, Y), small n: maximise
   (U)  d_P(X, Y) / ( 1.2 (b/(s* tau*)) (n+2)^2 ||eta||_2 )      -- the uniform bound says <= 1
   (LF) d_P(X, Y) / ||local(X, Y)||_2                            -- the local bound, Frobenius form, says <= 1
   (PT) max_k |y_k - g1 x_k| / local_k                           -- the local bound per point says <= 1
L-BFGS with numerical gradients from many starts, then a Nelder-Mead polish (the objectives are non-smooth in X: min, max).

Control of the optimiser: the same code must find a violation of deliberately wrong bounds (uniform constant divided by 1000;
'kappa = 1/2' in the local bound).
Run:  OMP_NUM_THREADS=1 python3 -B item2_adv_joint.py [budget seconds] > item2_adv_joint_<stamp>.log
"""
import os, sys, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import minimize
from r27lib import (cap_memory, peak_mb, now, KAPPA, helix, random_unit_chain, angle_chain, chain_consts, pair_arrays, eta_vec,
                    window_pair_index, procrustes, local_weights)

cap_memory(2.0)
t0 = time.time()
BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 520.0
rng = np.random.default_rng(27113)
print(f"R27 item2_adv_joint.py started {now()}  budget {BUDGET:.0f} s")
PAIRS = {}
INF_HITS = [0]


def setup(n):
    if n not in PAIRS:
        J, K = pair_arrays(n)
        widx = window_pair_index(n, J, K)
        P = np.zeros((n - 4, len(J)))
        for i, ix in enumerate(widx):
            P[i, ix] = 1.0
        PAIRS[n] = (J, K, P)
    return PAIRS[n]


def all_ratios(X, Y):
    n = len(X)
    J, K, P = setup(n)
    tau, s, b = chain_consts(X)
    if tau.min() < 1e-9 * b or not np.isfinite(b):
        return None
    et = eta_vec(X, Y, J, K)
    en = np.linalg.norm(et)
    res = procrustes(X, Y)[2]
    dp = np.linalg.norm(res)
    diam = np.linalg.norm(X - X.mean(0), axis=1).max()
    if en < 1e-300 or dp < 1e-7 * diam:
        return None
    C = 1.2 * b * (n + 2) ** 2 / (s.min() * tau.min())
    M = local_weights(X, tau, s)
    loc = M @ np.sqrt(P @ (et * et))
    R1, t1, _ = procrustes(X[:5], Y[:5])
    dist = np.linalg.norm(Y - X @ R1 - t1, axis=1)
    # noise floor (see item2_adv_fixedX.py): ratio only where the bound is above 1e-7 diam
    big = loc > 1e-7 * diam
    pt = (dist[big] / loc[big]).max() if big.any() else 0.0
    if np.any((~big) & (dist > loc + 1e-9 * diam)):
        pt = np.inf
        INF_HITS[0] += 1          # a point farther than 1e-9 diam from g1(x_k) although its local bound is below the noise floor
    return dp / (C * en), dp / np.linalg.norm(loc), pt, dp / diam, tau.min() / b, s.min() / b


def obj(z, n, which):
    X = z[:3 * n].reshape(n, 3); Y = z[3 * n:].reshape(n, 3)
    r = all_ratios(X, Y)
    if r is None or not np.isfinite(r[which]) or r[which] <= 0:
        return 60.0
    return -np.log(r[which])


def obj_U_fast(z, n):
    """only the uniform ratio (cheaper)"""
    X = z[:3 * n].reshape(n, 3); Y = z[3 * n:].reshape(n, 3)
    J, K, P = setup(n)
    tau, s, b = chain_consts(X)
    if tau.min() < 1e-9 * b:
        return 60.0
    et = eta_vec(X, Y, J, K)
    en = np.linalg.norm(et)
    dp = np.linalg.norm(procrustes(X, Y)[2])
    if en < 1e-300 or dp < 1e-9:
        return 60.0
    C = 1.2 * b * (n + 2) ** 2 / (s.min() * tau.min())
    return -np.log(dp / (C * en))


def start_X(n, rng, q):
    kind = q % 4
    if kind == 0:
        return random_unit_chain(n, rng)
    if kind == 1:
        return angle_chain(n, rng, th=(60.0, 110.0), ph=(50.0, 130.0))
    if kind == 2:
        # compact: successive regular tetrahedra (Boerdijk-Coxeter helix): every 4 consecutive points a regular tetrahedron
        a = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float) / (2 * np.sqrt(2))
        pts = [a[0], a[1], a[2], a[3]]
        while len(pts) < n:
            c = (pts[-1] + pts[-2] + pts[-3]) / 3
            pts.append(2 * c - pts[-4])
        return np.array(pts[:n]) + 0.05 * rng.normal(size=(n, 3))
    return helix(n, 2.3, 1.5, 100.0) / 3.8 + 0.05 * rng.normal(size=(n, 3))


def start_Y(X, rng, q):
    n = len(X)
    kind = (q // 4) % 4
    if kind == 0:
        return X + 0.3 * rng.normal(size=X.shape)
    if kind == 1:
        Xc = X - X.mean(0)
        U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
        p = Vt[2]
        return Xc - rng.uniform(0.5, 1.0) * np.outer(Xc @ p, p) + 0.2 * rng.normal(size=X.shape)
    if kind == 2:
        return X + 0.02 * rng.normal(size=X.shape)
    return rng.normal(size=X.shape)


glob = {}
plan = [(5, "U", 60), (5, "LF", 40), (5, "PT", 40), (6, "U", 40), (6, "LF", 16), (6, "PT", 16), (7, "U", 30), (8, "U", 24), (7, "LF", 8), (8, "LF", 6)]
weights = {(n, w): (3 * n) ** 2 * ns * (1.0 if w == "U" else 3.0) for n, w, ns in plan}
tot = sum(weights.values())
for n, which, nstart in plan:
    tsec = time.time()
    share = BUDGET * weights[(n, which)] / tot
    idx = dict(U=0, LF=1, PT=2)[which]
    best = (0.0, None)
    done = 0
    for q in range(nstart):
        if time.time() - tsec > share:
            break
        X0 = start_X(n, rng, q)
        Y0 = start_Y(X0, rng, q)
        z0 = np.concatenate([X0.ravel(), Y0.ravel()])
        if which == "U":
            res = minimize(obj_U_fast, z0, args=(n,), method="L-BFGS-B", options=dict(maxiter=300, maxfun=20000))
            res = minimize(obj_U_fast, res.x, args=(n,), method="Nelder-Mead", options=dict(maxiter=4000, xatol=1e-9, fatol=1e-11))
        else:
            res = minimize(obj, z0, args=(n, idx), method="L-BFGS-B", options=dict(maxiter=200, maxfun=15000))
            res = minimize(obj, res.x, args=(n, idx), method="Nelder-Mead", options=dict(maxiter=3000, xatol=1e-9, fatol=1e-11))
        done += 1
        r = all_ratios(res.x[:3 * n].reshape(n, 3), res.x[3 * n:].reshape(n, 3))
        if r is not None and np.isfinite(r[idx]) and r[idx] > best[0]:
            best = (r[idx], r, res.x.copy())
    glob[(n, which)] = best
    r = best[1]
    print(f"n = {n}  objective {which:2s}: sup found {best[0]:.6g}   (starts done {done} of {nstart}; at the maximiser: uniform ratio {r[0]:.4g}, "
          f"d_P/||local||_2 {r[1]:.4g}, per-point {r[2]:.4g}, d_P/diam {r[3]:.3g}, tau*/b {r[4]:.3f}, s*/b {r[5]:.3f})   [{time.time() - tsec:.0f} s]")
    np.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"item2_adv_joint_best_n{n}_{which}.npy"), best[2])
    sys.stdout.flush()

bU = max(v[0] for (n, w), v in glob.items() if w == "U")
bLF = max(v[0] for (n, w), v in glob.items() if w == "LF")
bPT = max(v[0] for (n, w), v in glob.items() if w == "PT")
viol = sum(1 for v in glob.values() if v[0] > 1 + 1e-9) + INF_HITS[0]
print(f"evaluations in which a point violated a local bound that is below the noise floor (would be a real violation): {INF_HITS[0]}")
print(f"\nlargest ratios found (joint search): uniform {bU:.6g};  local, Frobenius form {bLF:.6g};  local, per point {bPT:.6g};  violations: {viol}")
print(f"control of the optimiser: uniform constant divided by 1000 violated: {bU > 1e-3};  divided by 100 violated: {bU > 1e-2};  "
      f"local bound with kappa -> 1/2 (per point) violated: {bPT > 0.5 / KAPPA}")
print(f"ALL DONE {now()}  {time.time() - t0:.1f} s  peak memory {peak_mb():.0f} MB")
