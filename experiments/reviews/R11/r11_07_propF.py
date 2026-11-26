"""R11 / 07 -- Proposition F (the Markov recursion).

(1) the inequality  sum_x pi_phi^t Q^(1-t) >= prod_i c_i  and the Lipschitz claim for -ln V_i
    on random inhomogeneous binary chains with random members of C_d and random Markov Q;
(2) the fixed point u* and the bounds  h, a, E <= (values of the one-site problem with law
    (1-p, p) and slope u*)  [report: h <= 0.04053, 0.05484, 0.07202, 0.09157;
    E <= 0.16935, 0.23419, 0.31886, 0.43245], and the block versions L = 2, 3 with all vertices;
(3) necessary condition: the exact values over site-wise labels (lower bounds on F*_n) are
    below n * (one-site bound).

Run:  python3 r11_07_propF.py       (about 2 minutes)
"""
import time, itertools
import numpy as np
from r11lib import *

T0 = time.time()
rng = np.random.default_rng(11)
u = 1.0

# ------------------------------------------------------------------------------------------ (1)
print("== (1) the inequality of Proposition F on random inhomogeneous binary chains ==")


def all_configs01(n):
    idx = np.arange(2 ** n)
    return (idx[:, None] >> np.arange(n)[None, :]) & 1          # letters 0/1, site i = bit i


worst_ratio = np.inf
worst_lip = -np.inf
worst_c_end = 0.0
ncase = 0
for rep in range(150):
    n = int(rng.integers(3, 8))
    t = float(rng.uniform(0.05, 0.95))
    X = all_configs01(n)
    N = 2 ** n
    pi1 = rng.dirichlet(np.ones(2))
    Ps = [None] + [rng.dirichlet(np.ones(2) * rng.choice([0.5, 2.0]), size=2) for _ in range(n - 1)]   # Ps[i][a, b], i = 1..n-1
    ds = [np.array([[0.0, rng.uniform(0.2, 2.0)], [rng.uniform(0.2, 2.0), 0.0]]) for _ in range(n)]   # asymmetric envelopes
    pi = pi1[X[:, 0]].copy()
    for i in range(1, n):
        pi *= Ps[i][X[:, i - 1], X[:, i]]
    D = np.zeros((N, N))
    for i in range(n):
        D += ds[i][X[:, i][:, None], X[:, i][None, :]]
    # random member of C_d
    g = rng.normal(0, rng.uniform(0.5, 3.0), size=N)
    phi = (g[None, :] + D).min(axis=1)
    if rng.uniform() < 0.3:
        g2 = rng.normal(0, 2.0, size=N)
        phi = np.maximum(phi, (g2[None, :] + D).min(axis=1))
    assert (phi[:, None] - phi[None, :] - D).max() < 1e-9
    # random Markov Q
    q1 = rng.dirichlet(np.ones(2))
    qs = [None] + [rng.dirichlet(np.ones(2), size=2) for _ in range(n - 1)]
    Q = q1[X[:, 0]].copy()
    for i in range(1, n):
        Q *= qs[i][X[:, i - 1], X[:, i]]
    w = pi * np.exp(-phi)
    piphi = w / w.sum()
    lhs = float((piphi ** t * Q ** (1 - t)).sum())
    # envelopes d*_i backwards (sites 0..n-1)
    dstar = [None] * n
    dstar[n - 1] = ds[n - 1].copy()
    for i in range(n - 2, -1, -1):
        Gi = np.zeros((2, 2))
        Pn = Ps[i + 1]
        # w = (1, e^y):  w(b') <= w(b) e^{d*(b,b')}  <=>  -d*(1,0) <= y <= d*(0,1)
        ys = (-dstar[i + 1][1, 0], dstar[i + 1][0, 1])
        for a in range(2):
            for a2 in range(2):
                if a != a2:
                    Gi[a, a2] = max(np.log((Pn[a2, 0] + Pn[a2, 1] * np.exp(y)) / (Pn[a, 0] + Pn[a, 1] * np.exp(y))) for y in ys)
        dstar[i] = ds[i] + Gi
    # Lipschitz claim: -ln V_i(x_<=i) is d*_i-Lipschitz in x_i
    wfull = pi * np.exp(-phi)
    for i in range(n):
        # V_i(x_{<=i}) = E_pi[e^{-phi} | x_{<=i}]
        key = X[:, : i + 1] @ (1 << np.arange(i + 1))
        num = np.bincount(key, weights=wfull, minlength=2 ** (i + 1))
        den = np.bincount(key, weights=pi, minlength=2 ** (i + 1))
        V = num / den
        pre = np.arange(2 ** i)
        l0, l1 = -np.log(V[pre]), -np.log(V[pre + 2 ** i])               # x_i = 0 / 1
        worst_lip = max(worst_lip, float((l0 - l1 - dstar[i][0, 1]).max()), float((l1 - l0 - dstar[i][1, 0]).max()))
    # c_i = min_b min_{gamma in Lip(d*_i)} sum_a q_i(b,a)^{1-t} (P_i(b,a) e^{-gamma(a)}/Z)^t
    def cval(qrow, Prow, dst):
        best = np.inf
        grid = np.linspace(-dst[1, 0], dst[0, 1], 201)                   # gamma(0) - gamma(1) in [-d*(1,0), d*(0,1)]
        vals = []
        for dlt in grid:
            ww = Prow * np.exp(-np.array([dlt, 0.0]))
            ww /= ww.sum()
            vals.append(float((qrow ** (1 - t) * ww ** t).sum()))
        vals = np.array(vals)
        return vals.min(), min(vals[0], vals[-1])
    prod = 1.0
    c, ce = cval(q1, pi1, dstar[0])
    worst_c_end = max(worst_c_end, ce - c)
    prod *= c
    for i in range(1, n):
        cb = []
        for b in range(2):
            c, ce = cval(qs[i][b], Ps[i][b], dstar[i])
            worst_c_end = max(worst_c_end, ce - c)
            cb.append(c)
        prod *= min(cb)
    worst_ratio = min(worst_ratio, lhs / prod)
    ncase += 1
print(f"{ncase} random chains (n = 3..7, asymmetric envelopes, random t): smallest [sum pi_phi^t Q^(1-t)] / [prod c_i] = {worst_ratio:.6f}  (must be >= 1)")
print(f"   -ln V_i is d*_i-Lipschitz in x_i: largest violation {worst_lip:.2e};  the minimum defining c_i is at an end of the segment: largest (end value - grid minimum) = {worst_c_end:.2e}")

# ------------------------------------------------------------------------------------------ (2)
print("\n== (2) fixed point u* and the one-site bounds (L = 1); block versions L = 2, 3 ==")


def ustar(p):
    g = lambda x: np.log(((1 - p) * np.exp(x) + p) / (p * np.exp(x) + 1 - p))
    x = u
    for _ in range(500):
        x = u + g(x)
    return x, g(x)


def site_logP(law, slope):
    """two-letter site (+1, -1) with law = (law[+], law[-]) and Hamming slope: the two vertices."""
    hh = slope / 2
    phis = np.array([[-hh, hh], [hh, -hh]])
    return gibbs_logs(np.log(np.asarray(law)), phis)


def block_logP_cond(L, p, slopes):
    """block of L sites with the law P^(L)(. | previous letter = +1) and the given slopes: all vertices."""
    s, pi = chain_law(L, p)
    first = s[:, 0]
    law = pi * np.where(first == 1, (1 - p), p) / 0.5          # P(x_1 | prev = +) * rest
    law /= law.sum()
    V = lipschitz_vertices(L, slopes)
    return gibbs_logs(np.log(law), V), V.shape[0]


rep_h = {0.4: (0.04053, 0.03889, 0.03736), 0.3: (0.05484, 0.05180, 0.04902), 0.2: (0.07202, 0.06672, 0.06197), 0.1: (0.09157, 0.08299, 0.07542)}
rep_E = {0.4: (0.16935, 0.16921, 0.16917), 0.3: (0.23419, 0.23324, 0.23285), 0.2: (0.31886, 0.31554, 0.31376), 0.1: (0.43245, 0.42378, 0.41799)}
rep_a3 = {0.4: 0.12970, 0.3: 0.15401, 0.2: 0.17747, 0.1: 0.19678}
rep_us = {0.4: 1.218, 0.3: 1.526, 0.2: 1.981, 0.1: 2.750}
for p in (0.4, 0.3, 0.2, 0.1):
    us, gus = ustar(p)
    K = np.log((1 - p) / p)
    hs, Es, As = [], [], []
    for L in (1, 2, 3):
        if L == 1:
            logP = site_logP((1 - p, p), us)
            nv = 2
        else:
            logP, nv = block_logP_cond(L, p, [u] * (L - 1) + [us])
        tt, v = golden_max(lambda t: maximise_G_fast(logP, t)[0], 0.1, 0.9, tol=1e-5)
        lo, up, _ = maximise_G_fast(logP, tt)
        hs.append(up / L)
        Es.append(maximise_E_fast(logP)[1] / L)
        As.append(maximise_a(logP)[1] / L)
    print(f"p={p}: u* = {us:.4f} (report {rep_us[p]}), slack g(u*) = {gus:.4f} < K = {K:.4f}")
    print(f"      h <= " + ", ".join(f"{v:.5f}" for v in hs) + "   report: " + ", ".join(f"{v:.5f}" for v in rep_h[p]))
    print(f"      E <= " + ", ".join(f"{v:.5f}" for v in Es) + "   report: " + ", ".join(f"{v:.5f}" for v in rep_E[p]))
    print(f"      a <= " + ", ".join(f"{v:.5f}" for v in As) + f"   report (L=3): {rep_a3[p]:.5f}")

# ------------------------------------------------------------------------------------------ (3)
print("\n== (3) necessary condition: exact optimum over site-wise labels (n = 8) <= 8 * one-site DP bound ==")
h = u / 2
for p in (0.4, 0.3, 0.1):
    us, _ = ustar(p)
    for t in (0.3, 0.45, 0.7):
        s, pi = chain_law(8, p)
        phis = -h * configs(8).astype(float) @ s.T.astype(float)
        logP = gibbs_logs(np.log(pi), phis)
        lo, up, M = maximise_G_fast(logP, t)
        dp = maximise_G_fast(site_logP((1 - p, p), us), t)[1]
        print(f"p={p} t={t}: site-wise optimum n=8: {lo:.6f} (per site {lo/8:.6f});  8 * DP = {8*dp:.6f};  cube 8 F_c = {8*cube_F(t):.6f};  ok: {lo <= 8*dp + 1e-9}")
print(f"{time.time()-T0:.1f} s")
