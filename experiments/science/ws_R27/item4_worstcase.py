#!/usr/bin/env python3
"""Workstream R27, Item 4 (numbers for the paragraph a software author can act on) -- a LOWER bound, by search, for the worst-case
reconstruction error at a given accuracy of the measured distances, on the idealised traces:

    maximise  d_P(X, Y)   subject to   sum over the 4n-10 pairs of separation <= 4 of ( |y_j - y_k| - |x_j - x_k| )^2  <=  N sigma^2

(sigma = root-mean-square error of the DISTANCES, in angstrom).  SLSQP with analytic gradients from many starts (softest modes of both
signs, random directions, reflected tails pulled back onto the constraint set, random clouds).  What is found is a configuration Y that fits the
local distances of X to rms sigma and lies at RMSD d_P/sqrt(n) from X after the best superposition (mirror images allowed): any valid error
bar at that accuracy must be at least this large.  Compared with: the first-order worst case  sigma sqrt(N/n)/s_7  and the bound of Theorem L.

Nothing here is a statement about real structures.  Run:  OMP_NUM_THREADS=1 python3 -B item4_worstcase.py [budget] > item4_worstcase_<stamp>.log
"""
import os, sys, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import minimize
from r27lib import (cap_memory, peak_mb, now, helix, chain_consts, pair_arrays, eta_vec, procrustes, uniform_constant,
                    half_jacobian, mu_and_mode)

cap_memory(2.0)
t0 = time.time()
BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 500.0
rng = np.random.default_rng(27118)
print(f"R27 item4_worstcase.py started {now()}  budget {BUDGET:.0f} s")


def reflect_tail(X, i):
    nrm = np.cross(X[i + 2] - X[i + 1], X[i + 3] - X[i + 1]); nrm /= np.linalg.norm(nrm)
    Y = X.copy()
    Y[i + 4:] = X[i + 4:] - 2 * ((X[i + 4:] - X[i + 1]) @ nrm)[:, None] * nrm[None, :]
    return Y


class Prob:
    def __init__(self, X):
        self.X = X; self.n = n = len(X)
        self.J, self.K = pair_arrays(n)
        self.d = np.linalg.norm(X[self.J] - X[self.K], axis=1)
        self.N = len(self.J)
        A = half_jacobian(X, self.J, self.K)
        Rg = A / self.d[:, None]
        U, S, Vt = np.linalg.svd(Rg, full_matrices=True)
        S = np.concatenate([S, np.zeros(max(0, 3 * n - len(S)))])
        self.s7 = S[3 * n - 7]
        self.soft = [Vt[3 * n - 7 - q].reshape(n, 3) for q in range(4)]
        self.C = uniform_constant(X)
        self.rg = np.sqrt(((X - X.mean(0)) ** 2).sum() / n)
        self.diam = np.linalg.norm(X - X.mean(0), axis=1).max()

    def dist_err(self, Y):
        return np.linalg.norm(Y[self.J] - Y[self.K], axis=1) - self.d

    def neg_d2(self, y):
        Y = y.reshape(self.n, 3)
        res = procrustes(self.X, Y)[2]
        return -(res * res).sum(), (-2 * res).ravel()

    def con(self, y, sig):
        de = self.dist_err(y.reshape(self.n, 3))
        return 1.0 - (de @ de) / (self.N * sig * sig)

    def con_jac(self, y, sig):
        Y = y.reshape(self.n, 3)
        dv = Y[self.J] - Y[self.K]
        L = np.linalg.norm(dv, axis=1)
        de = L - self.d
        v = (2 * de / np.maximum(L, 1e-300))[:, None] * dv
        G = np.zeros_like(Y)
        np.add.at(G, self.J, v); np.add.at(G, self.K, -v)
        return (-G / (self.N * sig * sig)).ravel()

    def pull_back(self, Y, sig):
        """reduce the distance misfit of a start (descent on the stress, a few L-BFGS steps at a time) until it satisfies the constraint"""
        y = Y.ravel().copy()

        def fg(z):
            de = self.dist_err(z.reshape(self.n, 3))
            return de @ de, -self.con_jac(z, 1.0) * self.N

        for _ in range(100):
            de = self.dist_err(y.reshape(self.n, 3))
            if np.sqrt((de @ de) / self.N) <= 0.95 * sig:
                break
            y = minimize(fg, y, jac=True, method="L-BFGS-B", options=dict(maxiter=4)).x
        return y.reshape(self.n, 3)

    def solve(self, Y0, sig):
        res = minimize(self.neg_d2, Y0.ravel(), jac=True, method="SLSQP",
                       constraints=[dict(type="ineq", fun=self.con, jac=self.con_jac, args=(sig,))], options=dict(maxiter=400, ftol=1e-12))
        Y = res.x.reshape(self.n, 3)
        de = self.dist_err(Y)
        rms = np.sqrt((de @ de) / self.N)
        if rms > sig * (1 + 1e-6):
            return None
        return np.sqrt(-res.fun), Y, rms


cases = [("helix-like n=12", helix(12, 2.3, 1.5, 100.0)), ("helix-like n=20", helix(20, 2.3, 1.5, 100.0)),
         ("strand-like 160 n=12", helix(12, 0.94, 3.3, 160.0)), ("strand-like 160 n=20", helix(20, 0.94, 3.3, 160.0))]
sigmas = (0.01, 0.03, 0.1, 0.2, 0.3, 0.5, 1.0)
per_case = BUDGET / len(cases)
print("\ncolumns: sigma (rms distance error, A) | worst RMSD found (A) [which start] | first-order worst case sigma sqrt(N/n)/s_7 | ratio found/first-order |"
      " bound of Theorem L as an RMSD (uniform constant, ||eta|| computed from the Y found) | radius of gyration | max |distance error| of the Y found")
store = {}
for name, X in cases:
    tcase = time.time()
    P = Prob(X)
    n = P.n
    print(f"\n{name}: N = {P.N} pairs, s_7 = {P.s7:.4f}, first-order RMSD per unit rms distance error = {np.sqrt(P.N / n) / P.s7:.3f}, C_L = {P.C:.4g}, R_g = {P.rg:.2f} A")
    prev_best = None
    for sig in sigmas:
        if time.time() - tcase > per_case:
            print(f"   sigma = {sig}: skipped (time budget)")
            continue
        tsig = time.time()
        best = (0.0, None, None, "")
        starts = []
        amp = sig * np.sqrt(P.N) / P.s7                    # first-order amplitude of the softest mode
        for q in range(4):
            for sg in (1, -1):
                starts.append((f"soft mode {q + 1}", X + sg * 0.9 * amp * P.soft[q]))
        for _ in range(6):
            c = rng.normal(size=4)
            starts.append(("mixture of soft modes", X + 0.7 * amp * sum(ci * m for ci, m in zip(c, P.soft)) / np.linalg.norm(c)))
        for _ in range(4):
            starts.append(("random direction", X + sig * rng.normal(size=X.shape)))
        if sig >= 0.1:
            for i in range(0, n - 4, max(1, (n - 4) // 6)):
                starts.append(("reflected tail, pulled back", P.pull_back(reflect_tail(X, i), sig)))
            for _ in range(3):
                starts.append(("random cloud, pulled back", P.pull_back(X + P.diam * 0.5 * rng.normal(size=X.shape), sig)))
        if prev_best is not None:
            starts.append(("continuation from the previous sigma", prev_best))
        for kind, Y0 in starts:
            if time.time() - tsig > per_case / len(sigmas) * 1.5:
                break
            out = P.solve(Y0, sig)
            if out is not None and out[0] > best[0]:
                best = (out[0], out[1], out[2], kind)
        if best[1] is None:
            print(f"   sigma = {sig}: no feasible end point")
            continue
        dP_, Y, rms, kind = best
        prev_best = Y
        et = eta_vec(X, Y, P.J, P.K)
        fo = sig * np.sqrt(P.N / n) / P.s7
        de = P.dist_err(Y)
        print(f"   {sig:5.2f} | {dP_ / np.sqrt(n):8.3f} [{kind}] | {fo:8.3f} | {dP_ / np.sqrt(n) / fo:6.2f} | {P.C * np.linalg.norm(et) / np.sqrt(n):10.4g} | {P.rg:6.2f} | {np.abs(de).max():.3f}"
              f"   (rms achieved {rms:.4f}; d_P/||eta|| = {dP_ / np.linalg.norm(et):.3f})")
        store[(name, sig)] = Y
        sys.stdout.flush()
np.savez(os.path.join(os.path.dirname(os.path.abspath(__file__)), "item4_worstcase_found.npz"),
         **{f"{k[0]}|{k[1]}": v for k, v in store.items()})
print("\ncontrol: every reported Y satisfies the constraint (rms distance misfit <= sigma) by construction; the first-order prediction must be recovered at the smallest sigma "
      "(ratio ~ 1): see the first row of each case.")
print(f"ALL DONE {now()}  {time.time() - t0:.1f} s  peak memory {peak_mb():.0f} MB")
