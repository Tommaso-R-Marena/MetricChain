#!/usr/bin/env python3
"""Workstream R27, Item 2 (i) -- Step 2 of the proof of Theorem L, attacked on its own: six points (two five-point windows F_1, F_2 sharing the
four points W = {2,3,4,5}); maximise over BOTH configurations
      rho2 = ||R_1 - R_2||_F * tau / (delta_1 + delta_2),    tau = sigma_3 of the centred shared window,  delta_i = kappa e_i / s_i,
(the proof says rho2 <= 1 whatever the determinants of R_1, R_2) -- with starts in which the shared four points are nearly coplanar and the
two frames have opposite determinants (reflected sixth point), and generic starts.  L-BFGS with numerical gradients + Nelder-Mead.
Also: the same quantity with the residuals in place of their bounds, rho2' = ||R_1 - R_2||_F tau / (||eps_1|W|| + ||eps_2|W||) (<= 1 by the
same line of the proof).
Control (must fail): the five-point thickness s_1 in place of tau.
Run:  OMP_NUM_THREADS=1 python3 -B item2_adv_step2.py > item2_adv_step2_<stamp>.log
"""
import os, sys, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import minimize
from r27lib import cap_memory, peak_mb, now, KAPPA, angle_chain, random_unit_chain, sigma3, procrustes

cap_memory(2.0)
t0 = time.time()
rng = np.random.default_rng(27124)
print(f"R27 item2_adv_step2.py started {now()}")
iu = np.triu_indices(5, 1)


def e_win(P, Q):
    dx = P[iu[0]] - P[iu[1]]; dy = Q[iu[0]] - Q[iu[1]]
    return np.linalg.norm(np.einsum("ij,ij->i", dy - dx, dy + dx))


def ratios(X, Y):
    tau = sigma3(X[1:5]); s1 = sigma3(X[0:5]); s2 = sigma3(X[1:6])
    if tau < 1e-10:
        return None
    R1, t1, r1 = procrustes(X[0:5], Y[0:5]); R2, t2, r2 = procrustes(X[1:6], Y[1:6])
    d1 = KAPPA * e_win(X[0:5], Y[0:5]) / s1; d2 = KAPPA * e_win(X[1:6], Y[1:6]) / s2
    dR = np.linalg.norm(R1 - R2)
    if d1 + d2 < 1e-12:
        return None
    res = np.linalg.norm(r1[1:5]) + np.linalg.norm(r2[0:4])
    return dR * tau / (d1 + d2), (dR * tau / res if res > 1e-12 else 0.0), dR * s1 / (d1 + d2), np.linalg.det(R1) * np.linalg.det(R2), tau / s1, dR


def obj(z, which):
    r = ratios(z[:18].reshape(6, 3), z[18:].reshape(6, 3))
    if r is None or r[which] <= 0:
        return 50.0
    return -np.log(r[which])


best = {0: (0, None), 1: (0, None)}
ctl_best = 0.0
nst = 0
for which in (0, 1):
    for q in range(60):
        if time.time() - t0 > 240 * (which + 1):
            break
        X = angle_chain(6, rng) if q % 2 else random_unit_chain(6, rng)
        kind = q % 3
        if kind == 0:                               # shared window nearly coplanar, sixth point reflected in its plane (frames of opposite determinant)
            nrm = np.cross(X[2] - X[1], X[3] - X[1]); nrm /= np.linalg.norm(nrm)
            X[4:] += (10.0 ** rng.uniform(-3, -0.5) - (X[4] - X[1]) @ nrm) * nrm
            Y = X.copy(); Y[5] = X[5] - 2 * ((X[5] - X[1]) @ nrm) * nrm
            Y += 1e-3 * rng.normal(size=Y.shape)
        elif kind == 1:
            Y = X + 0.3 * rng.normal(size=X.shape)
        else:
            Y = rng.normal(size=X.shape)
        z0 = np.concatenate([X.ravel(), Y.ravel()])
        res = minimize(obj, z0, args=(which,), method="L-BFGS-B", options=dict(maxiter=300, maxfun=15000))
        res = minimize(obj, res.x, args=(which,), method="Nelder-Mead", options=dict(maxiter=4000, xatol=1e-10, fatol=1e-12))
        r = ratios(res.x[:18].reshape(6, 3), res.x[18:].reshape(6, 3))
        nst += 1
        if r is not None:
            if r[which] > best[which][0]:
                best[which] = (r[which], r)
            ctl_best = max(ctl_best, r[2])
for which, lab in ((0, "||R_1 - R_2||_F tau/(delta_1 + delta_2)"), (1, "||R_1 - R_2||_F tau/(||eps_1|W|| + ||eps_2|W||)")):
    v, r = best[which]
    print(f"sup found of {lab}: {v:.6f}   (at the maximiser: det R_1 det R_2 = {r[3]:+.0f}, tau/s_1 = {r[4]:.3e}, ||R_1 - R_2||_F = {r[5]:.4f})")
print(f"starts: {nst};  violations (ratio > 1): {sum(1 for w in (0, 1) if best[w][0] > 1 + 1e-9)}")
print(f"CONTROL (s_1 in place of tau): largest value of ||R_1 - R_2||_F s_1/(delta_1 + delta_2) met: {ctl_best:.3f}  (> 1 means the wrong statement is violated: {ctl_best > 1})")
print(f"ALL DONE {now()}  {time.time() - t0:.1f} s  peak memory {peak_mb():.0f} MB")
