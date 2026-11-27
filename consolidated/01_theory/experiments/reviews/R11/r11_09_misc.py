"""R11 / 09 -- further replications.

(a) slope dependence at p = 0.3 (section 6.5): lower bound (Prop. H) / cube, upper bound (Prop. F, L=1) / cube, E_F / cube;
(b) lower ends of a from Prop. H at t = 0.999;
(c) optimum over ALL site-wise labels on the plain chain, n = 6, 8, 10 (section 6.4);
(d) strong coupling, u = 1: Prop. H lower bound at small p (section 6.5);
(e) section 8.3: Markov-type classes -- are the class-wise quantile LEVELS admissible, and is the
    truncated residual psi^{tr,q} itself admissible?  (the report's example concerns the levels);
(f) Proposition J: E_n >= ln Z_n(h)/Z_n(0); exact E_n over all vertices (n <= 3); ascent search for
    a member of the class with KL(pi || pi_phi) above the uniform field (n = 8, 10).

Run:  python3 r11_09_misc.py [a b c d e f]      (all parts: about 4 minutes)
"""
import sys, time, itertools
import numpy as np
from scipy.optimize import minimize, linprog
from scipy.sparse import coo_matrix
from r11lib import *

T0 = time.time()
parts = sys.argv[1:] or list("abcdef")


def G_inf(p, t, c, u, N=64):
    h = u / 2
    Kp = 0.5 * np.log((1 - p) / p)
    pc = 1.0 / (1.0 + np.exp(2 * c))
    return (L_moment(pc, Kp, h, t, N=N) - t * L_moment(p, c, t * h, 1.0 / t, N=N)
            - t * np.log(2 * np.cosh(Kp)) + np.log(2 * np.cosh(c)))


def best_G_inf(p, u, starts=((0.45, 0.8), (0.4, 0.4), (0.48, 0.1), (0.45, 1.5))):
    best = (-1, None, None)
    for t0, c0 in starts:
        res = minimize(lambda z: -G_inf(p, min(max(z[0], 0.02), 0.98), abs(z[1]), u), [t0, c0], method='Nelder-Mead',
                       options=dict(xatol=1e-6, fatol=1e-13, maxiter=3000))
        if -res.fun > best[0]:
            best = (-res.fun, min(max(res.x[0], 0.02), 0.98), abs(res.x[1]))
    return best


def site_bounds(p, slope):
    hh = slope / 2
    logP = gibbs_logs(np.log(np.array([1 - p, p])), np.array([[-hh, hh], [hh, -hh]]))
    tt, v = golden_max(lambda t: maximise_G_fast(logP, t)[0], 0.05, 0.95, tol=1e-6)
    return maximise_G_fast(logP, tt)[1], maximise_a(logP)[1], maximise_E_fast(logP)[1]


if 'a' in parts:
    print("== (a) slope dependence at p = 0.3 (report: lower/cube 2.271 2.209 2.022 1.736 1.328 0.994 0.925 0.928; upper/cube 2.33 2.33 2.29 2.17 1.88 1.46 1.26 1.16; E_F/cube 2.332 2.327 2.294 2.194 1.935 1.546 1.348 1.243) ==")
    p = 0.3
    for uu in (0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 3.0, 4.0):
        hc, tc, ac, Ec = cube_constants(uu)
        lo, ts, cs = best_G_inf(p, uu)
        x = uu
        g = lambda y: np.log(((1 - p) * np.exp(y) + p) / (p * np.exp(y) + 1 - p))
        for _ in range(2000):
            x = uu + g(x)
        up = site_bounds(p, x)[0]
        print(f"u={uu:5.2f}: cube h = {hc:.6e};  lower/cube = {lo/hc:.3f} (t={ts:.3f}, c={cs:.3f});  upper/cube = {up/hc:.3f};  E_F/cube = {E_F(p, uu)/Ec:.3f};  chi = (1-p)/p = {(1-p)/p:.3f}   [{time.time()-T0:.0f} s]", flush=True)

if 'b' in parts:
    print("\n== (b) a >= G_inf(t; c)/(1-t) at t = 0.999 (report: 0.116817 (p=0.4, c=0.42), 0.123875 (0.3, 0.52), 0.122445 (0.2, 0.51), 0.101876 (0.1, 0.42);  cube a = 0.110944) ==")
    for p in (0.4, 0.3, 0.2, 0.1):
        t = 0.999
        cs, v = golden_max(lambda c: G_inf(p, t, c, 1.0, N=96), 0.0, 1.5, tol=1e-4)
        print(f"p={p}: G_inf(0.999; c)/(0.001) = {v/(1-t):.6f} at c = {cs:.3f};  N=96 vs 160: {abs(G_inf(p,t,cs,1.0,N=96)-G_inf(p,t,cs,1.0,N=160))/(1-t):.1e}")

if 'c' in parts:
    print("\n== (c) all site-wise labels on the plain chain, p = 0.3, t = 0.431 (report: 0.039856, 0.040183, 0.040243 per site for n = 6, 8, 10) ==")
    u = 1.0
    h = u / 2
    prev = None
    for n in (6, 8, 10):
        s, pi = chain_law(n, 0.3)
        phis = -h * configs(n).astype(float) @ s.T.astype(float)
        logP = gibbs_logs(np.log(pi), phis)
        lo, up, M = maximise_G_fast(logP, 0.431)
        inc = "" if prev is None else f";  increment (F_n - F_(n-2))/2 = {(lo-prev)/2:.5f}"
        print(f"n={n}: F = [{lo:.7f}, {up:.7f}]  per site {lo/n:.6f}{inc};  labels with weight > 1e-6: {(M>1e-6).sum()};  cube {cube_F(0.431):.6f}   [{time.time()-T0:.0f} s]", flush=True)
        prev = lo

if 'd' in parts:
    print("\n== (d) strong coupling at u = 1: Prop. H lower bound (report: below the cube at p = 0.02: 0.0274) ==")
    hc = cube_constants(1.0)[0]
    for p in (0.05, 0.02, 0.01):
        lo, ts, cs = best_G_inf(p, 1.0, starts=((0.35, 0.8), (0.3, 1.2), (0.3, 0.5)))
        print(f"p={p}: max_(t,c) G_inf = {lo:.6f} (t={ts:.3f}, c={cs:.3f});  cube {hc:.6f};  E_F = {E_F(p,1.0):.4f}")

if 'e' in parts:
    print("\n== (e) section 8.3: quantile levels and truncated residuals for Markov-type classes, n = 8, u = 1 ==")
    rng = np.random.default_rng(3)
    n = 8
    N = 2 ** n
    idx = np.arange(N)
    bits = (idx[:, None] >> np.arange(n)[None, :]) & 1
    ham = np.zeros((N, N))
    for i in range(n):
        ham += bits[:, i][:, None] != bits[:, i][None, :]
    # Markov type: first letter and the four pair counts
    pairs = bits[:, :-1] * 2 + bits[:, 1:]
    key_m = bits[:, 0] + 2 * sum((pairs == k).sum(axis=1) * (n ** (k + 1)) for k in range(4))
    key_t = bits.sum(axis=1)
    out = {}
    for name, key in (("type classes", key_t), ("Markov-type classes", key_m)):
        classes = [np.where(key == k)[0] for k in np.unique(key)]
        viol_lev = viol_tr = 0
        ncase = 0
        worst_tr = 0.0
        for rep in range(100):
            g = rng.normal(0, rng.uniform(1, 4), size=N)
            psi = (g[None, :] + ham).min(axis=1)
            if rep % 4 == 0:
                psi = ham[:, rng.integers(0, N)].copy()                # a cone
            w = np.exp(-psi)
            for q in (0.05, 0.2, 0.5):
                tlev = np.empty(N)
                for C in classes:
                    ws = np.sort(w[C])[::-1]
                    # smallest value v of w on the class such that density{w > v} <= q
                    kq = int(np.floor(q * len(C)))                    # at most kq points may lie strictly above
                    v = ws[min(kq, len(C) - 1)]
                    tlev[C] = v
                lev = -np.log(tlev)
                psitr = np.maximum(psi, lev)                           # weight min(w, t)
                e1 = (lev[:, None] - lev[None, :] - ham).max()
                e2 = (psitr[:, None] - psitr[None, :] - ham).max()
                viol_lev += e1 > 1e-9
                viol_tr += e2 > 1e-9
                worst_tr = max(worst_tr, e2)
                ncase += 1
        print(f"{name} ({len(classes)} classes): {ncase} (residual, q) cases;  levels not admissible in {viol_lev};  truncated residual psi^tr not admissible in {viol_tr} (largest excess {worst_tr:.3f})")

if 'f' in parts:
    print("\n== (f) Proposition J ==")
    u = 1.0
    h = u / 2

    def lnZratio(n, p):
        s, pi = chain_law(n, p)
        return float(np.log((pi * np.exp(h * s.sum(axis=1))).sum()))

    print("exact E_n over ALL vertices (n = 2, 3) against ln Z_n(h)/Z_n(0):")
    for p in (0.4, 0.3, 0.1):
        for n in (2, 3):
            s, pi = chain_law(n, p)
            V = lipschitz_vertices(n, [u] * n)
            logP = gibbs_logs(np.log(pi), V)
            lo, up, M = maximise_E_fast(logP)
            print(f"   p={p} n={n}: E_n = [{lo:.9f}, {up:.9f}] ({V.shape[0]} vertices);  ln Z_n(h)/Z_n(0) = {lnZratio(n,p):.9f}")
    print("ascent search for a member with KL(pi || pi_phi) = E_pi phi + ln E_pi e^-phi above the uniform field (successive LPs):")
    rng = np.random.default_rng(1)
    for n in (8, 10):
        N = 2 ** n
        idx = np.arange(N)
        # constraints phi(x) - phi(x^i) <= u for all x, i
        rows, cols, vals = [], [], []
        r = 0
        for i in range(n):
            y = idx ^ (1 << i)
            rows += [np.arange(r, r + N)] * 2
            cols += [idx, y]
            vals += [np.ones(N), -np.ones(N)]
            r += N
        A = coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(r, N)).tocsr()
        b = np.full(r, u)
        bounds = [(0, 0)] + [(None, None)] * (N - 1)
        for p in (0.3, 0.1):
            s, pi = chain_law(n, p)
            target = lnZratio(n, p)
            best = -np.inf
            nstart = 6 if n == 8 else 3
            for st in range(nstart):
                # random admissible start
                g = rng.normal(0, 2.0, size=N)
                ham1 = None
                phi = g.copy()
                # project to the class by an inf-convolution along edges (Bellman-Ford style)
                for _ in range(n + 1):
                    for i in range(n):
                        phi = np.minimum(phi, phi[idx ^ (1 << i)] + u)
                f_old = -np.inf
                for it in range(60):
                    wgt = pi * np.exp(-phi)
                    grad = pi - wgt / wgt.sum()                         # gradient of E_pi phi + ln E_pi e^-phi
                    res = linprog(-grad, A_ub=A, b_ub=b, bounds=bounds, method='highs')
                    phi = res.x
                    f = float(pi @ phi + np.log((pi * np.exp(-phi)).sum()))
                    if f <= f_old + 1e-12:
                        break
                    f_old = f
                best = max(best, f)
            print(f"   n={n} p={p}: best KL found {best:.9f};  uniform field ln Z_n(h)/Z_n(0) = {target:.9f};  above the uniform field: {best > target + 1e-9}   [{time.time()-T0:.0f} s]", flush=True)
print(f"{time.time()-T0:.1f} s")
