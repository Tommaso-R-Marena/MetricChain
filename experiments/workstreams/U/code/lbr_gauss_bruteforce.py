#!/usr/bin/env python3
"""Independent brute-force check of the nested construction behind lbr_gauss.py (small-slope limit).

Types Y in prod_j [0, sigma_j] on a grid; rate sum Y_j^2; metric rho(Y, Y') = 2 sum_j sigma_j |Y_j - Y'_j|.
A function Psi(Y) is "Lipschitz" if |Psi(Y) - Psi(Y')| <= rho.  Lower McShane envelopes are computed exactly on the
grid by separable max-plus sweeps (the metric is a sum over the axes).
Construction for r rounds (r = 2, 3), budget theta:
   V_t = {sum_{j >= t} Y_j^2 <= theta};
   Psi_1 = -Y_1^2 on V_1;  for t = 2..r:  Psi_t = max( lower McShane envelope of Psi_{t-1} from V_{t-1},
                                                       -(Y_1^2 + ... + Y_t^2) )   on V_t   (a function of Y_1..Y_t);
   deep twin = lower McShane envelope of Psi_r from V_r;  hidden gain = max_{Y not in V_r} [ -deep(Y) - |Y|^2 ],
   visible maximum = max_{Y in V_r} [ -Psi_r(Y) - |Y|^2 ]  (= 0 by the cap).
Checks: Psi_t is independent of Y_{>t} on V_t (by construction), Lipschitz (verified), equal to Psi_{t-1} on V_{t-1}.
Output: hidden gain against the formulas Xi_2, Xi_3 of lbr_gauss.py.
usage: lbr_gauss_bruteforce.py
"""
import math, sys
import numpy as np
from lbr_gauss import xi2, xi3


def envelope(vals, mask, steps):
    """lower McShane envelope max_a [vals(a) - rho(x, a)] over anchors a in mask; steps[j] = 2 sigma_j * grid spacing."""
    F = np.where(mask, vals, -np.inf)
    for ax, st in enumerate(steps):
        F = np.moveaxis(F, ax, 0)
        for i in range(1, F.shape[0]):
            np.maximum(F[i], F[i - 1] - st, out=F[i])
        for i in range(F.shape[0] - 2, -1, -1):
            np.maximum(F[i], F[i + 1] - st, out=F[i])
        F = np.moveaxis(F, 0, ax)
    return F


def lipschitz_ok(F, steps, tol=1e-9):
    return all(np.max(np.abs(np.diff(F, axis=ax))) <= st + tol for ax, st in enumerate(steps))


def run(theta, phi, N):
    r = len(phi)
    sig = [math.sqrt(p) for p in phi]
    axes = [np.linspace(0, s, N) for s in sig]
    steps = [2 * s * (s / (N - 1)) for s in sig]
    Y = np.meshgrid(*axes, indexing="ij")
    rate_from = [sum(Y[j] ** 2 for j in range(t, r)) for t in range(r)]      # sum_{j >= t} Y_j^2
    V = [rf <= theta + 1e-12 for rf in rate_from]
    Psi = -Y[0] ** 2                                                         # Psi_1 (used on V_1)
    ok = True
    for t in range(1, r):
        env = envelope(Psi, V[t - 1], steps)
        cap = -sum(Y[j] ** 2 for j in range(t + 1))
        new = np.maximum(env, cap)
        # the function used on V_t must not depend on Y_{>t}: take the slice Y_{>t} = 0 (typical) and broadcast
        sl = tuple([slice(None)] * (t + 1) + [0] * (r - t - 1))
        new_t = new[sl]
        new_b = np.broadcast_to(new_t.reshape(new_t.shape + (1,) * (r - t - 1)), new.shape)
        ok &= bool(np.all(np.abs(new_b[V[t - 1]] - Psi[V[t - 1]]) < 1e-9))   # extends Psi_{t-1} on V_{t-1}
        Psi = np.array(new_b)
        ok &= lipschitz_ok(Psi, steps)
    deep = envelope(Psi, V[r - 1], steps)
    mass = -deep - rate_from[0]
    hidden = float(np.max(mass[~V[r - 1]])) if np.any(~V[r - 1]) else float("-inf")
    visible = float(np.max((-Psi - rate_from[0])[V[r - 1]]))
    return hidden, visible, ok


if __name__ == "__main__":
    print("r = 2:  phi, theta | brute force hidden gain (N=400), visible max | formula Xi_2")
    for phi in ((0.5, 0.5), (0.65, 0.35), (0.3, 0.7)):
        for theta in (0.25, 0.30):
            if theta >= phi[1]:
                continue
            hid, vis, ok = run(theta, phi, 400)
            print(f"  {phi} {theta}: {hid:+.5f} {vis:+.5f} checks {ok} | {xi2(theta, phi):+.5f}")
    print("r = 3:  phi, theta | brute force hidden gain (N=90), visible max | formula Xi_3 (N=241)")
    for phi in ((0.1, 0.5, 0.4), (0.2, 0.54, 0.26), (0.2, 0.3, 0.5), (0.05, 0.35, 0.6), (0.3, 0.3, 0.4)):
        for theta in (0.15, 0.25):
            if theta >= phi[2]:
                continue
            hid, vis, ok = run(theta, phi, 90)
            print(f"  {phi} {theta}: {hid:+.5f} {vis:+.5f} checks {ok} | {xi3(theta, phi, N=241):+.5f}")
