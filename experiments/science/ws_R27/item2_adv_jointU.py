#!/usr/bin/env python3
"""Workstream R27, Item 2 (ii) -- ADVERSARIAL search over BOTH configurations for the UNIFORM bound of Theorem L, n = 5 ... 16:
maximise      rho(X, Y) = d_P(X, Y) s* tau* / ( 1.2 b (n+2)^2 ||eta||_2 )         (the theorem says rho <= 1).

rho is non-smooth in X (min over windows, max over bonds); the search maximises the smooth lower bound rho_p <= rho obtained by
replacing  s*, tau*  by the power means  (sum s_i^-p)^(-1/p)  (smaller)  and  b  by  (sum b_i^p)^(1/p)  (larger),  p = 12 -> 48 -> 200,
with analytic gradients (checked against finite differences), and reports the EXACT rho at the end points.
Starts: angle-constrained chains, perturbed tetrahelices, helix-like chains, chains with one flattened interior window; Y = X + noise,
a reflected tail, a collapsed copy, a random cloud; and continuation in n (the best pair for n-1, extended by one point).

Run:  OMP_NUM_THREADS=1 python3 -B item2_adv_jointU.py [budget seconds] [seed] [n1,n2,...] [pair.npy to continue from] > item2_adv_jointU_<stamp>.log
"""
import os, sys, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import minimize
from scipy.special import logsumexp, softmax
from r27lib import (cap_memory, peak_mb, now, helix, angle_chain, chain_consts, pair_arrays, eta_vec, procrustes)

cap_memory(2.0)
t0 = time.time()
BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 520.0
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 27116
rng = np.random.default_rng(SEED)
print(f"R27 item2_adv_jointU.py started {now()}  budget {BUDGET:.0f} s  seed {SEED}")
PA = {}


def pa(n):
    if n not in PA:
        PA[n] = pair_arrays(n)
    return PA[n]


def exact_rho(X, Y):
    n = len(X)
    J, K = pa(n)
    tau, s, b = chain_consts(X)
    et = eta_vec(X, Y, J, K)
    dp = np.linalg.norm(procrustes(X, Y)[2])
    en = np.linalg.norm(et)
    if en <= 0 or tau.min() <= 0:
        return 0.0
    return dp * s.min() * tau.min() / (1.2 * b * (n + 2) ** 2 * en)


def f_and_grad(z, n, p):
    """- log rho_p and its gradient"""
    X = z[:3 * n].reshape(n, 3); Y = z[3 * n:].reshape(n, 3)
    J, K = pa(n)
    R, t, res = procrustes(X, Y)
    d2 = (res * res).sum()
    dx = X[J] - X[K]; dy = Y[J] - Y[K]
    et = np.einsum("ij,ij->i", dy - dx, dy + dx)
    en2 = et @ et
    if d2 < 1e-24 or en2 < 1e-300:
        return 80.0, np.zeros_like(z)
    GX = -res @ R.T / d2
    GY = res / d2
    vx = (-2 * et)[:, None] * dx / en2            # d(1/2 log en2)/dx_j ;  minus at k
    vy = (2 * et)[:, None] * dy / en2
    gx = np.zeros_like(X); gy = np.zeros_like(Y)
    np.add.at(gx, J, vx); np.add.at(gx, K, -vx)
    np.add.at(gy, J, vy); np.add.at(gy, K, -vy)
    GX -= gx; GY -= gy                             # gradient of  1/2 log d2 - 1/2 log en2
    val = 0.5 * np.log(d2) - 0.5 * np.log(en2)
    for m in (4, 5):
        nw = n - m + 1
        sv = np.empty(nw); grads = []
        for i in range(nw):
            Xc = X[i:i + m] - X[i:i + m].mean(0)
            U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
            sv[i] = S[2]
            grads.append(np.outer(U[:, 2], Vt[2]))
        if sv.min() <= 1e-12:
            return 80.0, np.zeros_like(z)
        ls = np.log(sv)
        val += -logsumexp(-p * ls) / p
        w = softmax(-p * ls)
        for i in range(nw):
            GX[i:i + m] += (w[i] / sv[i]) * grads[i]
    bv = X[1:] - X[:-1]
    bl = np.linalg.norm(bv, axis=1)
    lb = np.log(bl)
    val -= logsumexp(p * lb) / p
    w = softmax(p * lb)
    gb = (w / bl ** 2)[:, None] * bv
    GX[1:] -= gb
    GX[:-1] += gb
    val -= np.log(1.2 * (n + 2) ** 2)
    return -val, -np.concatenate([GX.ravel(), GY.ravel()])


def tetrahelix(n):
    a = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float) / (2 * np.sqrt(2))
    pts = [a[0], a[1], a[2], a[3]]
    while len(pts) < n:
        c = (pts[-1] + pts[-2] + pts[-3]) / 3
        pts.append(2 * c - pts[-4])
    return np.array(pts[:n])


def reflect_tail(X, i):
    nrm = np.cross(X[i + 2] - X[i + 1], X[i + 3] - X[i + 1]); nrm /= np.linalg.norm(nrm)
    Y = X.copy()
    Y[i + 4:] = X[i + 4:] - 2 * ((X[i + 4:] - X[i + 1]) @ nrm)[:, None] * nrm[None, :]
    return Y


def start(n, q, rng):
    kx = q % 5
    if kx == 0:
        X = angle_chain(n, rng, th=(60.0, 120.0), ph=(40.0, 140.0))
    elif kx == 1:
        X = tetrahelix(n) + 0.08 * rng.normal(size=(n, 3))
    elif kx == 2:
        X = helix(n, 2.3, 1.5, 100.0) / 3.83 + 0.05 * rng.normal(size=(n, 3))
    elif kx == 3:
        X = angle_chain(n, rng, th=(70.0, 110.0), ph=(50.0, 130.0))
        if n >= 6:
            pos = rng.integers(0, n - 5)
            a, b_, c_ = X[pos + 1], X[pos + 2], X[pos + 3]
            nrm = np.cross(b_ - a, c_ - a); nrm /= np.linalg.norm(nrm)
            h = (X[pos + 4] - a) @ nrm
            X[pos + 4:] += (rng.choice([0.3, 0.1, 0.03]) - h) * nrm
    else:
        X = tetrahelix(n) * np.array([1.0, 1.0, rng.uniform(0.6, 1.6)]) + 0.05 * rng.normal(size=(n, 3))
    ky = (q // 5) % 4
    if ky == 0:
        Y = X + 0.3 * rng.normal(size=X.shape)
    elif ky == 1:
        Y = reflect_tail(X, rng.integers(0, n - 4)) + 0.02 * rng.normal(size=X.shape)
    elif ky == 2:
        Xc = X - X.mean(0)
        p = np.linalg.svd(Xc, full_matrices=False)[2][2]
        Y = Xc - rng.uniform(0.5, 1.0) * np.outer(Xc @ p, p) + 0.2 * rng.normal(size=X.shape)
    else:
        Y = rng.normal(size=X.shape)
    return np.concatenate([X.ravel(), Y.ravel()])


def optimise(z0, n):
    z = z0
    for p in (12.0, 48.0, 200.0):
        res = minimize(f_and_grad, z, args=(n, p), jac=True, method="L-BFGS-B", options=dict(maxiter=4000, maxfun=8000))
        z = res.x
    return z


# ---- gradient self-check -------------------------------------------------------------------------------------------------
n = 8
z = start(n, 0, rng)
f, g = f_and_grad(z, n, 12.0)
worst = 0.0
for _ in range(20):
    d = rng.normal(size=z.size); d /= np.linalg.norm(d)
    fd = (f_and_grad(z + 1e-6 * d, n, 12.0)[0] - f_and_grad(z - 1e-6 * d, n, 12.0)[0]) / 2e-6
    worst = max(worst, abs(fd - g @ d) / (abs(fd) + abs(g @ d) + 1e-12))
print(f"gradient self-check (20 directions, n = 8, p = 12): worst relative error {worst:.2e};  surrogate <= exact: "
      f"{np.exp(-f) <= exact_rho(z[:3 * n].reshape(n, 3), z[3 * n:].reshape(n, 3)) * (1 + 1e-12)}")

ns = [5, 6, 7, 8, 9, 10, 11, 12, 14, 16]
if len(sys.argv) > 3:
    ns = [int(v) for v in sys.argv[3].split(",")]
SEEDFILE = sys.argv[4] if len(sys.argv) > 4 else None       # optional .npy with a pair (X, Y) to continue from
wts = np.array([n ** 1.5 for n in ns], float)
shares = BUDGET * wts / wts.sum()
best = {}
prev = np.load(SEEDFILE) if SEEDFILE else None
print(f"lengths: {ns};  continuation from: {SEEDFILE}")
for n, share in zip(ns, shares):
    tsec = time.time()
    b = (0.0, None)
    q = 0
    cands = []
    if prev is not None:
        # continuation in n: extend the best pair by one more point (several random extensions) at either end
        m = len(prev) // 6
        Xp = prev[:3 * m].reshape(m, 3); Yp = prev[3 * m:].reshape(m, 3)
        for rep in range(6):
            Xn, Yn = Xp, Yp
            while len(Xn) < n:
                if rep % 2 == 0:
                    step = Xn[-1] - Xn[-4] if len(Xn) >= 4 else rng.normal(size=3)
                    xn = Xn[-1] + step / np.linalg.norm(step) * np.linalg.norm(Xn[-1] - Xn[-2]) + 0.2 * rng.normal(size=3)
                    yn = Yn[-1] + (xn - Xn[-1]) + 0.2 * rng.normal(size=3)
                    Xn = np.vstack([Xn, xn]); Yn = np.vstack([Yn, yn])
                else:
                    step = Xn[0] - Xn[3]
                    xn = Xn[0] + step / np.linalg.norm(step) * np.linalg.norm(Xn[0] - Xn[1]) + 0.2 * rng.normal(size=3)
                    yn = Yn[0] + (xn - Xn[0]) + 0.2 * rng.normal(size=3)
                    Xn = np.vstack([xn, Xn]); Yn = np.vstack([yn, Yn])
            cands.append(np.concatenate([Xn.ravel(), Yn.ravel()]))
    done = 0
    while time.time() - tsec < share:
        z0 = cands.pop() if cands else start(n, q, rng)
        q += 1
        z = optimise(z0, n)
        r = exact_rho(z[:3 * n].reshape(n, 3), z[3 * n:].reshape(n, 3))
        done += 1
        if np.isfinite(r) and r > b[0]:
            b = (r, z.copy())
    best[n] = b
    prev = b[1]
    X = b[1][:3 * n].reshape(n, 3); Y = b[1][3 * n:].reshape(n, 3)
    tau, s, bb = chain_consts(X)
    J, K = pa(n)
    et = eta_vec(X, Y, J, K)
    dp = np.linalg.norm(procrustes(X, Y)[2])
    diam = np.linalg.norm(X - X.mean(0), axis=1).max()
    bl = np.linalg.norm(np.diff(X, axis=0), axis=1)
    print(f"n = {n:2d}: largest rho found {b[0]:.6g}   ({done} starts, {time.time() - tsec:.0f} s; at the maximiser tau*/b = {tau.min() / bb:.3f}, s*/b = {s.min() / bb:.3f}, "
          f"tau max/min = {tau.max() / tau.min():.2f}, bonds min/max = {bl.min() / bl.max():.2f}, d_P/diam = {dp / diam:.2f}, "
          f"share of ||eta||^2 on separation 4: {np.sum(et[(K - J) == 4] ** 2) / (et @ et):.2f})")
    np.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"item2_adv_jointU_best_n{n}_seed{SEED}.npy"), b[1])
    sys.stdout.flush()

top = max(best.items(), key=lambda kv: kv[1][0])
print(f"\nlargest ratio d_P/(uniform bound) found: {top[1][0]:.6g} at n = {top[0]};  violations (rho > 1): {sum(1 for v in best.values() if v[0] > 1)}")
print(f"control of the optimiser: the uniform bound with the constant divided by 100 is violated iff this exceeds 0.01: {top[1][0] > 0.01};  divided by 1000: {top[1][0] > 0.001}")
print(f"ALL DONE {now()}  {time.time() - t0:.1f} s  peak memory {peak_mb():.0f} MB")
