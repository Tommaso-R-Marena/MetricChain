#!/usr/bin/env python3
"""z7_exactness.py [u]  --  Is the envelope sequence EXACT?  (floating point [N]; cube pair)

The addendum proves tau_j <= b_j (the tops of the envelope sequence bound the exponent of j nested levels at
vanishing accuracy).  This script computes the level recursion itself to high accuracy for two and three levels,

    T_1 = theta_na,   T_{k+1} = min(T_k, R[T_k]),
    R[T](g) = inf_{0 < phi < 1, 0 <= beta <= g}  sup_{gamma >= beta} [ min(gamma, mu) + (1 - phi) T(gamma/(1 - phi)) ],
    mu = phi theta_na((g - beta)/phi)                                                   (theory report (11.18.2)),

and compares:  (1) tau_2 = T_2(0+) against the closed form a^2/(a + x), theta_na(x) = a - x, and against b_2;
(2) T_2(g) against the majorant M_2(g) = max_B (B - W_2(B) g) of the envelope curve at positive rates g;
(3) tau_3 = T_3(0+) against b_3.

For T = theta_na (convex) the supremum over gamma is at an end point: with mu = phi theta_na((g - beta)/phi),
    beta <= mu:  max( beta + (1 - phi) theta(beta/(1 - phi)),  mu + (1 - phi) theta(mu/(1 - phi)) );
    beta >  mu:  mu + (1 - phi) theta(beta/(1 - phi)).
For T = T_2 (not known to be convex) the supremum is taken over a fine grid of gamma.
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import zetalib   # noqa: E402

u = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
pu = 1 / (1 + math.exp(u))
a = pu * math.log(2 * pu) + (1 - pu) * math.log(2 * (1 - pu))
estar = 0.5 * math.log(0.5 / pu) + 0.5 * math.log(0.5 / (1 - pu))


def _theta_exact(e):
    """theta_na(e) = KL(rho || 1/2), KL(rho || p_u) = e, rho in [p_u, 1/2]; vectorised bisection"""
    e = np.asarray(e, dtype=float)
    lo = np.full(e.shape, pu)
    hi = np.full(e.shape, 0.5)
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        kl = mid * np.log(mid / pu) + (1 - mid) * np.log((1 - mid) / (1 - pu))
        big = kl > e
        hi = np.where(big, mid, hi)
        lo = np.where(big, lo, mid)
    r = 0.5 * (lo + hi)
    out = r * np.log(2 * r) + (1 - r) * np.log(2 * (1 - r))
    return np.where(e >= estar, 0.0, np.where(e <= 0, a, out))


_S = np.linspace(0.0, 1.0, 400001)                 # table in the variable s = sqrt(e/eps*): theta is smooth in s
_TH = _theta_exact(estar * _S * _S)
_TH[0], _TH[-1] = a, 0.0


def theta(e):
    """theta_na by linear interpolation of the table (error below 1e-11 a; checked in main)"""
    e = np.asarray(e, dtype=float)
    s_ = np.sqrt(np.clip(e, 0.0, estar) / estar)
    return np.where(e >= estar, 0.0, np.interp(s_, _S, _TH))


def R_theta(g, nphi=1500, nbeta=400):
    """R[theta_na](g), g > 0, by a grid over (phi, beta) refined twice around the minimiser"""
    best = (math.inf, None, None)
    plo, phi_hi, blo, bhi = 1e-4, 1 - 1e-4, 0.0, g
    for it in range(4):
        phi = np.linspace(plo, phi_hi, nphi)[:, None]
        beta = np.linspace(blo, bhi, nbeta)[None, :]
        mu = phi * theta((g - beta) / phi)
        v1 = beta + (1 - phi) * theta(beta / (1 - phi))
        v2 = mu + (1 - phi) * theta(mu / (1 - phi))
        v3 = mu + (1 - phi) * theta(beta / (1 - phi))
        val = np.where(beta <= mu, np.maximum(v1, v2), v3)
        i, j = np.unravel_index(np.argmin(val), val.shape)
        if val[i, j] < best[0]:
            best = (float(val[i, j]), float(phi[i, 0]), float(beta[0, j]))
        dp, db = (phi_hi - plo) / nphi, (bhi - blo) / nbeta
        plo, phi_hi = max(1e-6, best[1] - 4 * dp), min(1 - 1e-6, best[1] + 4 * dp)
        blo, bhi = max(0.0, best[2] - 4 * db), min(g, best[2] + 4 * db)
    return best


def main():
    E = zetalib.EnvZ(u, 4, NG=8000)
    h = E.h
    tt = np.random.default_rng(1).random(20000) * estar
    print("# cube u = %g: a = %.10f, h = %.10f, eps* = %.10f;  table error of theta_na: %.1e a" % (u, a, h, estar, float(np.max(np.abs(theta(tt) - _theta_exact(tt)))) / a), flush=True)
    # (1) two levels at vanishing accuracy
    lo, hi = 0.0, estar
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if float(theta(np.array([mid]))[0]) + mid < a else (lo, mid)
    # theta(x) + x is a - (steep) near 0 ... the root of theta(x) = a - x other than x = 0:
    x = 0.5 * (lo + hi)
    tau2_closed = a * a / (a + x)
    phis = np.linspace(1e-4, 1 - 1e-4, 200001)
    f = np.maximum((1 - phis) * a, phis * a + (1 - phis) * theta(phis * a / (1 - phis)))
    tau2_grid = float(f.min())
    print("(1) tau_2: closed form a^2/(a + x), theta(x) = a - x, x = %.10f:  %.12f;  grid minimum of the level formula: %.12f;  envelope top b_2: %.12f"
          % (x, tau2_closed, tau2_grid, E.b[2]))
    print("    (tau_2 - b_2)/a = %.2e   [the addendum proves tau_2 <= b_2; duality of the cap line gives equality]" % ((tau2_closed - E.b[2]) / a), flush=True)
    # (2) T_2 at positive rates against the majorant of the envelope curve W_2
    xs, W2 = E.curves[2]
    def M2(g):
        return float(np.max(xs - W2 * g))
    print("(2) T_2(g) = min(theta, R[theta])(g) against M_2(g) = max_B (B - W_2(B) g):")
    print("      g/eps*      theta_na(g)     R[theta](g)   (phi, beta/g)        M_2(g)       (M_2 - T_2)/a")
    worst = 0.0
    gs = np.array([0.001, 0.003, 0.01, 0.03, 0.06, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]) * estar
    T2tab = []
    for g in gs:
        r, p, b = R_theta(float(g))
        th = float(theta(np.array([g]))[0])
        t2 = min(th, r)
        m2 = M2(float(g))
        worst = max(worst, (m2 - t2) / a)
        T2tab.append(t2)
        print("    %8.4f   %.10f   %.10f   (%.4f, %.4f)   %.10f   %+.3e" % (g / estar, th, r, p, b / g, m2, (m2 - t2) / a), flush=True)
    print("    largest (M_2 - T_2)/a over these rates: %.3e   (zero would mean: the envelope majorant IS the second level)" % worst)
    # (3) three levels at vanishing accuracy: tau_3 = inf_phi sup_gamma [min(gamma, phi a) + (1 - phi) T_2(gamma/(1 - phi))]
    gg = np.concatenate([[0.0], np.geomspace(1e-7, 1.0, 420) * estar])
    T2 = np.empty(len(gg))
    T2[0] = tau2_closed
    for i in range(1, len(gg)):
        r, _, _ = R_theta(float(gg[i]), nphi=600, nbeta=200)
        T2[i] = min(float(theta(np.array([gg[i]]))[0]), r)
    T2 = np.minimum.accumulate(T2)
    def T2f(xx):
        return np.where(xx >= estar, 0.0, np.interp(xx, gg, T2))
    best3 = (math.inf, None)
    for phi in np.linspace(0.01, 0.99, 981):
        gam = np.concatenate([[0.0], np.geomspace(1e-8, 1.0, 1500) * max(phi * a, 1e-12) * 1.0, np.linspace(1.0, 6.0, 200) * phi * a])
        val = float(np.max(np.minimum(gam, phi * a) + (1 - phi) * T2f(gam / (1 - phi))))
        if val < best3[0]:
            best3 = (val, phi)
    tau3 = best3[0]
    # the same operator applied to the majorant M_2 instead of T_2 (what the envelope step bounds)
    best3m = math.inf
    for phi in np.linspace(0.01, 0.99, 981):
        gam = np.concatenate([[0.0], np.geomspace(1e-8, 1.0, 1500) * phi * a, np.linspace(1.0, 6.0, 200) * phi * a])
        m2v = np.max(xs[None, :] - W2[None, :] * (gam / (1 - phi))[:, None], axis=1)
        best3m = min(best3m, float(np.max(np.minimum(gam, phi * a) + (1 - phi) * m2v)))
    print("(3) tau_3 from T_2 (grid of 420 rates, linear interpolation): %.10f = %.6f a  (phi = %.3f);  the same operator on the majorant M_2: %.10f = %.6f a;  envelope top b_3: %.10f = %.6f a"
          % (tau3, tau3 / a, best3[1], best3m, best3m / a, E.b[3], E.b[3] / a))
    print("    (b_3 - tau_3)/a = %.3e;   (b_3 - R[M_2](0))/a = %.3e" % ((E.b[3] - tau3) / a, (E.b[3] - best3m) / a))


if __name__ == "__main__":
    main()
