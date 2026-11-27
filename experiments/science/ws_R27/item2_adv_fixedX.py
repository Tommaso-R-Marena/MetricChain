#!/usr/bin/env python3
"""Workstream R27, Item 2 (ii) -- ADVERSARIAL search for a fixed reference chain X: optimise Y to maximise
   (U)  d_P(X, Y) / ||eta||_2            (the uniform bound of Theorem L says this is <= C_L = 1.2 b (n+2)^2/(s* tau*))
   (LF) d_P(X, Y) / ||local(Y)||_2       (the local bound in Frobenius form says this is <= 1)
   (PT) max_k |y_k - g1 x_k| / local_k   (the local bound per point, g1 = frame of the first window; <= 1)
by L-BFGS with analytic gradients for (U), (LF) and numerical gradients for (PT), from many starts: noise of all sizes around X,
reflected tails and heads at every position (+ noise), softest modes of both signs, random clouds, collapsed copies, X with one
point displaced, unrelated chains.

Also printed for every X: the first-order constant 1/(2 mu) (mu = (3n-6)-th singular value of the half-Jacobian A), a constant
C_loc = 2 ||M||_2 derived from the local form (d_P <= ||M e|| <= ||M||_2 ||e|| <= 2 ||M||_2 ||eta||), and the reflections.

Self-check of the gradients against finite differences (a control: a wrong gradient would show here).
Run:  OMP_NUM_THREADS=1 python3 -B item2_adv_fixedX.py > item2_adv_fixedX_<stamp>.log
"""
import os, time, sys
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import minimize
from r27lib import (cap_memory, peak_mb, now, KAPPA, helix, random_unit_chain, angle_chain, chain_consts, pair_arrays, eta_vec,
                    window_pair_index, procrustes, local_weights, uniform_constant, mu_and_mode)

cap_memory(2.0)
t0 = time.time()
BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 520.0
rng = np.random.default_rng(27112)
print(f"R27 item2_adv_fixedX.py started {now()}  budget {BUDGET:.0f} s")


class Ref:
    def __init__(self, X):
        self.X = X
        self.n = n = len(X)
        self.tau, self.s, self.b = chain_consts(X)
        self.J, self.K = pair_arrays(n)
        widx = window_pair_index(n, self.J, self.K)
        self.P = np.zeros((n - 4, len(self.J)))
        for i, ix in enumerate(widx):
            self.P[i, ix] = 1.0
        self.M = local_weights(X, self.tau, self.s)
        self.MtM = self.M.T @ self.M
        self.C = uniform_constant(X, (self.tau, self.s, self.b))
        self.Cloc = 2 * np.linalg.svd(self.M, compute_uv=False)[0]
        self.mu, self.nxt, self.V, _ = mu_and_mode(X, self.J, self.K)
        self.diam = np.linalg.norm(X - X.mean(0), axis=1).max()
        self.rg = np.sqrt(((X - X.mean(0)) ** 2).sum() / n)

    def eta(self, Y):
        return eta_vec(self.X, Y, self.J, self.K)

    def grad_from_eta(self, Y, g_eta):
        """gradient w.r.t. Y of a function of eta with partial derivatives g_eta"""
        v = 2 * g_eta[:, None] * (Y[self.J] - Y[self.K])
        G = np.zeros_like(Y)
        np.add.at(G, self.J, v)
        np.add.at(G, self.K, -v)
        return G

    def fU(self, y):
        """-log( d_P / ||eta|| ) and gradient"""
        Y = y.reshape(self.n, 3)
        et = self.eta(Y)
        en2 = et @ et
        res = procrustes(self.X, Y)[2]
        d2 = (res * res).sum()
        if en2 < 1e-300 or d2 < (1e-7 * self.diam) ** 2:          # below this amplitude both sides are rounding noise
            return 700.0, np.zeros_like(y)
        f = -0.5 * np.log(d2) + 0.5 * np.log(en2)
        G = -res / d2 + self.grad_from_eta(Y, et) / en2
        return f, G.ravel()

    def local(self, Y):
        et = self.eta(Y)
        e = np.sqrt(self.P @ (et * et))
        return self.M @ e, e, et

    def fLF(self, y):
        """-log( d_P / ||local||_2 ) and gradient"""
        Y = y.reshape(self.n, 3)
        loc, e, et = self.local(Y)
        l2 = loc @ loc
        res = procrustes(self.X, Y)[2]
        d2 = (res * res).sum()
        if l2 < 1e-300 or d2 < (1e-7 * self.diam) ** 2:
            return 700.0, np.zeros_like(y)
        w = self.MtM @ e
        with np.errstate(divide="ignore", invalid="ignore"):
            q = np.where(e > 0, w / e, 0.0)
        g_eta = 2 * et * (self.P.T @ q)            # d(l2)/d eta
        f = -0.5 * np.log(d2) + 0.5 * np.log(l2)
        G = -res / d2 + 0.5 * self.grad_from_eta(Y, g_eta) / l2
        return f, G.ravel()

    def pt_ratios(self, Y):
        loc, e, et = self.local(Y)
        R1, t1, _ = procrustes(self.X[:5], Y[:5])
        dist = np.linalg.norm(Y - self.X @ R1 - t1, axis=1)
        # noise floor: a ratio is formed only where the bound is above 1e-7 diam; below it both sides are rounding noise
        # (e.g. the points before a reflected tail: local_k = 0 exactly, dist_k ~ 1e-15) and the check is dist_k <= local_k + 1e-9 diam
        floor = 1e-7 * self.diam
        r = np.zeros(self.n)
        big = loc > floor
        r[big] = dist[big] / loc[big]
        r[(~big) & (dist > loc + 1e-9 * self.diam)] = np.inf
        return r, dist, loc

    def fPT(self, y):
        r = self.pt_ratios(y.reshape(self.n, 3))[0]
        m = r.max()
        return -np.log(m) if m > 1e-300 else 700.0

    def values(self, Y):
        et = self.eta(Y)
        en = np.linalg.norm(et)
        dp = np.linalg.norm(procrustes(self.X, Y)[2])
        loc = self.local(Y)[0]
        r = self.pt_ratios(Y)[0]
        return dp, en, np.linalg.norm(loc), r.max()


def reflect(X, i, tail=True):
    nrm = np.cross(X[i + 2] - X[i + 1], X[i + 3] - X[i + 1])
    nrm /= np.linalg.norm(nrm)
    Y = X.copy()
    sl = slice(i + 4, None) if tail else slice(0, i + 1)
    Y[sl] = X[sl] - 2 * ((X[sl] - X[i + 1]) @ nrm)[:, None] * nrm[None, :]
    return Y


def starts(ref, rng, nrand):
    X, n = ref.X, ref.n
    for i in range(n - 4):
        yield "reflection", reflect(X, i, True)
        yield "reflection", reflect(X, i, False) + 1e-3 * ref.diam * rng.normal(size=X.shape)
    for tt in (1e-3, 1e-2, 0.1, 0.5):
        for sg in (1, -1):
            yield "softest mode", X + sg * tt * ref.diam * ref.V
    for q in range(nrand):
        kind = q % 5
        if kind == 0:
            yield "noise", X + ref.diam * 10.0 ** rng.uniform(-4, -1) * rng.normal(size=X.shape)
        elif kind == 1:
            yield "noise", X + ref.diam * 10.0 ** rng.uniform(-1, 0.5) * rng.normal(size=X.shape)
        elif kind == 2:
            yield "cloud", ref.diam * rng.normal(size=X.shape)
        elif kind == 3:
            u = rng.normal(size=3); u /= np.linalg.norm(u)
            yield "collapsed", (X - X.mean(0)) @ (np.eye(3) - rng.uniform(0.5, 1.0) * np.outer(u, u)) + 1e-2 * ref.diam * rng.normal(size=X.shape)
        else:
            Y = X.copy(); k = rng.integers(n); Y[k] += ref.diam * rng.normal(size=3) * 10.0 ** rng.uniform(-1, 1)
            yield "one point", Y


def thin_window_chain(n, rng, pos, height):
    X = angle_chain(n, rng)
    a, b_, c_ = X[pos + 1], X[pos + 2], X[pos + 3]
    nrm = np.cross(b_ - a, c_ - a); nrm /= np.linalg.norm(nrm)
    h = (X[pos + 4] - a) @ nrm
    X[pos + 4:] += (height - h) * nrm
    return X


# ---- gradient self-check ---------------------------------------------------------------------------------------------
ref = Ref(angle_chain(9, rng))
worst = 0.0
for _ in range(20):
    y = (ref.X + 0.3 * rng.normal(size=ref.X.shape)).ravel()
    for fun in (ref.fU, ref.fLF):
        f, g = fun(y)
        d = rng.normal(size=y.size); d /= np.linalg.norm(d)
        h = 1e-6
        fd = (fun(y + h * d)[0] - fun(y - h * d)[0]) / (2 * h)
        worst = max(worst, abs(fd - g @ d) / max(1e-12, abs(fd) + abs(g @ d)))
print(f"gradient self-check (analytic vs central differences, 40 directions): worst relative error {worst:.2e}")
gbad = ref.fU(y)[1] * 1.3
fd = (ref.fU(y + 1e-6 * d)[0] - ref.fU(y - 1e-6 * d)[0]) / 2e-6
print(f"   control (gradient deliberately scaled by 1.3): relative error {abs(fd - gbad @ d) / (abs(fd) + abs(gbad @ d)):.2e}  (must be large)")

# ---- the reference chains ----------------------------------------------------------------------------------------------
a4 = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float)
refs = [("double regular tetrahedron n=5", np.vstack([a4[0], a4[1], a4[2], a4[3], 2 * a4[1:].mean(0) - a4[0]]))]
for n in (6, 8, 12, 20):
    refs.append((f"helix-like n={n}", helix(n, 2.3, 1.5, 100.0)))
for n in (8, 12, 20):
    refs.append((f"strand-like 160 n={n}", helix(n, 0.94, 3.3, 160.0)))
for n in (8, 12):
    refs.append((f"strand-like 175 n={n}", helix(n, 0.94, 3.3, 175.0)))
for n in (6, 8, 12):
    refs.append((f"random unit chain n={n} (a)", random_unit_chain(n, rng)))
    refs.append((f"angle-constrained chain n={n}", angle_chain(n, rng)))
for hgt in (1e-1, 1e-2, 1e-3):
    refs.append((f"thin interior window h={hgt:g} n=10", thin_window_chain(10, rng, 3, hgt)))

print("\ncolumns: n | tau* s* b | C_L (uniform) | C_loc = 2||M|| | 1/(2mu) | best d_P/||eta|| found [d_P/diam at the maximiser, start kind]"
      " | (best d_P/||eta||)/C_L | sup d_P/||local||_2 | sup per-point local ratio | starts | violations")
glob = dict(U=(0, None), LF=(0, None), PT=(0, None))
n_viol_total = 0
per_ref_budget = BUDGET / len(refs)
for name, X in refs:
    tref = time.time()
    ref = Ref(X)
    n = ref.n
    best = dict(U=(0.0, None, None), LF=(0.0, None, None), PT=(0.0, None, None))
    best_far = (0.0, None)          # best d_P/||eta|| among maximisers with d_P > 0.2 diam ("distant")
    nst = 0; viol = 0
    refl_best = (0.0, 0.0, 0.0)
    for i in range(n - 4):
        for tail in (True, False):
            Yr = reflect(X, i, tail)
            dp, en, lf, pt = ref.values(Yr)
            if dp / en > refl_best[0]:
                refl_best = (dp / en, dp, en)
    for kind, Y0 in starts(ref, rng, 60 if n <= 12 else 30):
        if time.time() - tref > per_ref_budget:
            break
        nst += 1
        for key, fun, jac in (("U", ref.fU, True), ("LF", ref.fLF, True)):
            res = minimize(fun, Y0.ravel(), jac=jac, method="L-BFGS-B", options=dict(maxiter=1500, maxfun=4000))
            Y = res.x.reshape(n, 3)
            dp, en, lf, pt = ref.values(Y)
            if not (np.isfinite(dp) and en > 0 and lf > 0 and dp > 1e-7 * ref.diam):
                continue
            vals = dict(U=dp / en, LF=dp / lf, PT=pt)
            for k2 in ("U", "LF", "PT"):
                if vals[k2] > best[k2][0]:
                    best[k2] = (vals[k2], kind, dp / ref.diam)
            if dp > 0.2 * ref.diam and dp / en > best_far[0]:
                best_far = (dp / en, kind, dp / ref.diam, en)
            if dp / en > ref.C * (1 + 1e-9) or dp / lf > 1 + 1e-9 or pt > 1 + 1e-9:
                viol += 1
        if n <= 8 and nst % 3 == 0:
            res = minimize(ref.fPT, Y0.ravel(), method="L-BFGS-B", options=dict(maxiter=300, maxfun=12000))
            res = minimize(ref.fPT, res.x, method="Nelder-Mead", options=dict(maxiter=3000, xatol=1e-10, fatol=1e-12))
            Y = res.x.reshape(n, 3)
            dp, en, lf, pt = ref.values(Y)
            if not (np.isfinite(dp) and dp > 1e-7 * ref.diam):
                continue
            if np.isfinite(pt) and pt > best["PT"][0]:
                best["PT"] = (pt, kind, dp / ref.diam)
            if pt > 1 + 1e-9:
                viol += 1
    n_viol_total += viol
    for k2 in ("U", "LF", "PT"):
        val = best[k2][0] / ref.C if k2 == "U" else best[k2][0]
        if val > glob[k2][0]:
            glob[k2] = (val, name)
    print(f"{name:36s} {n:3d} | {ref.tau.min():8.4f} {ref.s.min():8.4f} {ref.b:6.3f} | {ref.C:10.4g} | {ref.Cloc:10.4g} | {1 / (2 * ref.mu):9.4g} | "
          f"{best['U'][0]:9.4g} [{best['U'][2]:.1e}, {best['U'][1]}] | {best['U'][0] / ref.C:9.3e} | {best['LF'][0]:7.4f} [{best['LF'][1]}] | "
          f"{best['PT'][0]:7.4f} [{best['PT'][1]}] | {nst:3d} | {viol}")
    far = best_far
    print(f"{'':36s}       best reflection: d_P/||eta|| = {refl_best[0]:.4g} (d_P = {refl_best[1]:.3g}, ||eta|| = {refl_best[2]:.3g});"
          + (f"  best 'distant' maximiser (d_P > 0.2 diam): d_P/||eta|| = {far[0]:.4g} at d_P/diam = {far[2]:.2f}, ||eta|| = {far[3]:.3g} [{far[1]}]" if far[1] else "  no distant maximiser")
          + f";  (1/(2mu))/C_L = {1 / (2 * ref.mu) / ref.C:.2e}, C_loc/C_L = {ref.Cloc / ref.C:.3f}, mu^2/Lambda(11.04) = {ref.mu ** 2 / 11.04:.3g}")
    sys.stdout.flush()

print(f"\nlargest ratios over all reference chains:  d_P/(C_L ||eta||) = {glob['U'][0]:.6g} at {glob['U'][1]};  d_P/||local||_2 = {glob['LF'][0]:.6g} at {glob['LF'][1]};"
      f"  per-point local = {glob['PT'][0]:.6g} at {glob['PT'][1]}")
print(f"violations of a claimed bound found by the optimiser: {n_viol_total}")
print("control of the optimiser (it must be able to find a violation of a wrong bound): the uniform bound divided by 1000 is violated iff the first number above exceeds 1e-3: "
      f"{glob['U'][0] > 1e-3};  the local Frobenius bound divided by 10 is violated iff the second exceeds 0.1: {glob['LF'][0] > 0.1}")
print(f"ALL DONE {now()}  {time.time() - t0:.1f} s  peak memory {peak_mb():.0f} MB")
