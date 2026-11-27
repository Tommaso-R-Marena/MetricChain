#!/usr/bin/env python3
"""Coordinator's check of workstream U, Theorem U3 (two rounds do not reach the hinted exponent).

(A) asymptotic: Xi(theta, phi1) = min_c [ phi1 x_na(c/phi1) + phi2 D((theta - c)/phi2) ],  theta2*(u) = sup{theta : Xi > 0, theta < phi2 a}.
(B) exact finite n (own implementation of the twins from the statement of the theorem; types (d1, d2) on two blocks):
    W1 = {c1(d1) + c2(d2) <= T},  W2 = {c2(d2) <= T},  g_j = -(largest u-Lipschitz minorant of t_j), t_j = ln P_j(mode) - ln P_j,
    F_deep = lower McShane envelope of g1 from W1,  F_cap = max(F_deep, g1 + g2),  F_D / F_S = F_cap continued at slope -u / +u outside W2.
    Checks: u-Lipschitz in each argument; F_D = F_S on V2; = g1 on W1; then gap = ln A(F_D) - ln A(F_S), p1 = P(not W1), p2 = P(not W2)."""
import numpy as np, math, sys, time
from scipy.special import gammaln, logsumexp
from scipy.optimize import brentq

def setup(u):
    pu = 1/(1+math.exp(u)); L1 = math.log(2/(1+math.exp(-u)))
    f = lambda r: r*np.log(2*r) + (1-r)*np.log(2*(1-r))
    rho = np.linspace(1e-9, 0.5, 2000001)
    fr = f(rho)                                   # decreasing from ln 2 to 0
    finv = lambda th: np.interp(th, fr[::-1], rho[::-1])
    k = lambda r: f(r) + u*r - L1
    a = float(f(pu)); h = float(f(L1/u))
    D = lambda th: u*finv(th) - L1                # accuracy rate certified with a hint by e^{n theta} evaluations
    xna = lambda th: D(th) + th                   # the same for a non-adaptive sample (shear law)
    return pu, L1, f, finv, k, a, h, D, xna

def Xi(theta, phi1, S):
    pu, L1, f, finv, k, a, h, D, xna = S
    phi2 = 1 - phi1
    c = np.linspace(0, min(theta, phi1*a), 20001)
    E = phi1*xna(c/phi1) + phi2*D((theta - c)/phi2)
    return float(E.min())

def theta2(u):
    S = setup(u); a, h = S[5], S[6]
    best = (0, None)
    for phi1 in np.linspace(0.30, 0.80, 101):
        phi2 = 1 - phi1
        hi = min(phi2*a, phi2*math.log(2)*0.999)
        if Xi(h, phi1, S) <= 0: continue
        if Xi(hi, phi1, S) > 0: root = hi
        else: root = brentq(lambda th: Xi(th, phi1, S), h, hi, xtol=1e-10)
        val = min(root, phi2*a)
        if val > best[0]: best = (val, phi1)
    return best, a, h

def logbinom(n):
    d = np.arange(n+1)
    return gammaln(n+1) - gammaln(d+1) - gammaln(n-d+1) - n*math.log(2)

def lip_minorant(t, u):
    v = t.copy()
    for i in range(1, len(v)): v[i] = min(v[i], v[i-1] + u)
    for i in range(len(v)-2, -1, -1): v[i] = min(v[i], v[i+1] + u)
    return v

def twins(n, n1, T, u):
    n2 = n - n1
    lp1, lp2 = logbinom(n1), logbinom(n2)
    c1, c2 = -lp1, -lp2
    g1 = -lip_minorant(lp1.max() - lp1, u); g2 = -lip_minorant(lp2.max() - lp2, u)
    W1 = (c1[:, None] + c2[None, :]) <= T
    W2 = c2 <= T
    if not W1.any() or W2.all(): return None
    # lower McShane envelope of g1 from W1:  F_deep(d) = max_{e in W1} [g1(e1) - u|d1-e1| - u|d2-e2|]   (two-pass l1 transform of a max)
    F = np.where(W1, g1[:, None] * np.ones((1, n2+1)), -np.inf)
    for axis in (0, 1):
        F = np.moveaxis(F, axis, 0)
        for i in range(1, F.shape[0]): F[i] = np.maximum(F[i], F[i-1] - u)
        for i in range(F.shape[0]-2, -1, -1): F[i] = np.maximum(F[i], F[i+1] - u)
        F = np.moveaxis(F, 0, axis)
    Fcap = np.maximum(F, g1[:, None] + g2[None, :])
    idx = np.flatnonzero(W2); lo, hi = idx[0], idx[-1]
    d2 = np.arange(n2+1)
    b = np.clip(d2, lo, hi)                           # nearest end point of W2 (or the point itself)
    dist = np.abs(d2 - b)
    FD = Fcap[:, b] - u*dist[None, :]
    FS = Fcap[:, b] + u*dist[None, :]
    # checks
    for G_ in (FD, FS):
        assert np.abs(np.diff(G_, axis=0)).max() <= u + 1e-9 and np.abs(np.diff(G_, axis=1)).max() <= u + 1e-9, "not Lipschitz"
    assert np.all(FD[:, W2] == FS[:, W2]) and np.all(FS >= FD - 1e-12)
    inter = W1 & W2[None, :]
    assert np.abs((FD - g1[:, None])[inter]).max() <= 1e-9, "not g1 on W1 ∩ V2"
    assert np.all(W1 <= W2[None, :]), "W1 not inside V2"
    lw = lp1[:, None] + lp2[None, :]
    gap = float(logsumexp(lw - FD) - logsumexp(lw - FS))
    lp_out1 = float(logsumexp(lw[~W1])); lp_out2 = float(logsumexp(lp2[~W2]))
    return gap, lp_out1, lp_out2, float(logsumexp(lw - FS))

def hinted_exponent(n, u, eps=1.0):
    """Theorem 11.25(a) at the zero residual: the smallest dip radius k with ln(1 + Phi(k)) > eps, Phi(k) = 2^-n sum_{d<k} C(n,d)(e^{u(k-d)} - 1);
    every algorithm needs (1-2 delta) 2^n/|B(n, k-1)| evaluations."""
    lp = logbinom(n); d = np.arange(n+1)
    for k in range(1, n):
        x = u*(k - d[:k])
        lphi = float(logsumexp(lp[:k] + x + np.log1p(-np.exp(-x))))      # ln Phi(k), in logs (no overflow)
        if np.logaddexp(0.0, lphi) > eps:
            return -float(logsumexp(lp[:k]))/n, k
    return None

if __name__ == "__main__":
    t0 = time.time()
    print("== A. asymptotic formula")
    for u in ((0.25, 0.5, 1.0, 2.0, 3.0) if len(sys.argv) < 2 else ()):
        (val, phi1), a, h = theta2(u)
        print(f"   u={u}: a={a:.6f} h={h:.6f}  theta2* = {val:.6f} = {val/a:.4f} a = {val/h:.4f} h  at phi1 = {phi1:.3f}   [{time.time()-t0:.0f}s]", flush=True)
    S = setup(1.0); h = S[6]
    print("   Xi(h, phi1) at u = 1:", [round(Xi(h, p, S), 6) for p in (0.1, 0.3, 0.5, 0.65)], " (must be positive)")
    print("== B. exact twins (accuracy 1): the largest T with gap > 1, over a few splits")
    for u, ns in ((1.0, (400, 800, 1600, 3200)), (2.0, (200, 400, 1600))):
        for n in ns:
            best = None
            for frac in (0.45, 0.5, 0.55, 0.6, 0.65):
                n1 = int(round(frac*n))
                # scan T upwards; keep the last T with gap > 1, then bisect between it and the next grid point
                Ts = np.linspace(0.01*n, 0.12*n if u < 1.5 else 0.3*n, 45)
                last = None
                for j, T in enumerate(Ts):
                    r = twins(n, n1, float(T), u)
                    if r is not None and r[0] > 1: last = j
                if last is None: continue
                lo_T, hi_T = float(Ts[last]), float(Ts[min(last+1, len(Ts)-1)])
                for _ in range(16):
                    mid = 0.5*(lo_T + hi_T); r = twins(n, n1, mid, u)
                    if r is not None and r[0] > 1: lo_T = mid
                    else: hi_T = mid
                r = twins(n, n1, lo_T, u)
                E = -float(np.logaddexp(r[1], r[2]))/n
                if best is None or E > best[0]: best = (E, n1, r[0], lo_T/n, r[3])
            he, k = hinted_exponent(n, u)
            print(f"   u={u} n={n}: n1={best[1]} gap={best[2]:.2f} T/n={best[3]:.5f}  E = -ln(p1+p2)/n = {best[0]:.5f};  hinted bound {he:.5f} (k*={k});  ratio {best[0]/he:.3f};  ln A(F_S) = {best[4]:.2f}   [{time.time()-t0:.0f}s]", flush=True)
