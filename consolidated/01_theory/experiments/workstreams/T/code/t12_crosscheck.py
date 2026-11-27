#!/usr/bin/env python3
"""t12 -- cross-checks of the single-letter solvers by brute force (no clipping lemma, no monotonicity, no optimiser):
 (i)   V(mu, B; v) = min{ MI(nu) : u dist(nu,mu) + v(type) <= B } on a full grid of nu in [0,1]^2 (two blocks) and
       [0,1]^3 (three blocks), against the clipping solver;  the same with I in place of v (Lemma T7);
 (ii)  the brief's definition of the dip exponent of H for a centre of type m,
          R_m(e) = sup{ theta : max_{z in P_theta} min_{z' not in P_theta} [-MI(z) - I(kappa_z) + u dist(z,z') + v(kappa_z')] >= e },
       P_theta = {MI >= theta}, by an l1 distance transform on a (a,b)-grid of G^2 points (grid error O(1/G)), against the
       sup-min value;
 (iii) n_mu by the robust solver against the direct two-dimensional search, at random profiles.
usage: python3 t12_crosscheck.py bJ bB u e [G]
"""
import sys, time, math
import numpy as np
import tlib as T

bJ, bB, u, e = [float(x) for x in sys.argv[1:5]]
G = int(sys.argv[5]) if len(sys.argv) > 5 else 1001
t0 = time.time()
K = T.Known(T.phi_cw(bJ, bB), u)
rng = np.random.default_rng(99)

print("(i) inner problem by brute force")
worst2 = 0.0
for trial in range(12):
    m, a, b = rng.uniform(0.2, 0.8), rng.uniform(0.02, 0.45), rng.uniform(0.02, 0.45)
    if trial == 0:
        m, a, b = 0.5, 0.298, 0.298
    lams, mus = T.bin_blocks(m, a, b)
    B = e + T.alpha_blocks(K, lams, mus) + (rng.uniform(-0.01, 0.03) if trial else 0.0)
    Vc = T.V_clip(K, lams, mus, B, K.v, ng=2001, zoom=6)
    g = np.linspace(0, 1, 2001)
    N0, N1 = np.meshgrid(g, g, indexing="ij")
    kap = lams[0] * N0 + lams[1] * N1
    mi = np.maximum(T.hbf(kap) - lams[0] * T.hbf(N0) - lams[1] * T.hbf(N1), 0.0)
    dist = lams[0] * np.abs(N0 - mus[0]) + lams[1] * np.abs(N1 - mus[1])
    okv = u * dist + K.v(kap) <= B
    okI = u * dist + K.I(kap) <= B
    Vv = float(mi[okv].min()) if okv.any() else float("inf")
    VI = float(mi[okI].min()) if okI.any() else float("inf")
    worst2 = max(worst2, abs(Vv - Vc))
    print(f"  2 blocks (m,a,b)=({m:.3f},{a:.3f},{b:.3f}) B={B:.4f}: clipping {Vc:.6f} | grid, v: {Vv:.6f} | grid, I: {VI:.6f}")
worst3 = 0.0
for trial in range(6):
    lams = rng.dirichlet(np.ones(3) * 2)
    mus = rng.uniform(0.05, 0.95, 3)
    B = e + T.alpha_blocks(K, lams, mus) + rng.uniform(-0.005, 0.02)
    if B < float(K.v(np.array([float(lams @ mus)]))[0]):
        continue
    Vc = T.V_clip(K, lams, mus, B, K.v, ng=2001, zoom=6)
    g = np.linspace(0, 1, 181)
    N0, N1, N2 = np.meshgrid(g, g, g, indexing="ij")
    kap = lams[0] * N0 + lams[1] * N1 + lams[2] * N2
    mi = np.maximum(T.hbf(kap) - lams[0] * T.hbf(N0) - lams[1] * T.hbf(N1) - lams[2] * T.hbf(N2), 0.0)
    dist = lams[0] * np.abs(N0 - mus[0]) + lams[1] * np.abs(N1 - mus[1]) + lams[2] * np.abs(N2 - mus[2])
    ok = u * dist + K.v(kap) <= B
    Vv = float(mi[ok].min()) if ok.any() else float("inf")
    worst3 = max(worst3, abs(Vv - Vc))
    print(f"  3 blocks lams={np.round(lams,3)} mus={np.round(mus,3)} B={B:.4f}: clipping {Vc:.6f} | grid (181^3) {Vv:.6f}")
print(f"  largest |grid - clipping|: 2 blocks {worst2:.1e} (grid step 5e-4), 3 blocks {worst3:.1e} (grid step 5.6e-3; the grid value is an upper bound)   [{time.time()-t0:.0f}s]", flush=True)

print(f"(ii) the brief's definition of the dip exponent of H (P_theta = {{MI >= theta}}), centre type m, grid {G}^2")
for m in (0.5, 0.45):
    g = np.linspace(0, 1, G)
    A_, B_ = np.meshgrid(g, g, indexing="ij")
    kap = m * (1 - A_) + (1 - m) * B_
    mi = np.maximum(T.hbf(kap) - m * T.hbf(A_) - (1 - m) * T.hbf(B_), 0.0)
    Ik = K.I(kap)
    vk = K.v(kap)
    da = g[1] - g[0]
    wa, wb = u * m * da, u * (1 - m) * da

    def Eof(theta):
        inside = mi >= theta
        if inside.all() or not inside.any():
            return np.inf if inside.all() else -np.inf
        Tt = np.where(inside, np.inf, vk)
        for i in range(1, G):
            np.minimum(Tt[i], Tt[i - 1] + wa, out=Tt[i])
        for i in range(G - 2, -1, -1):
            np.minimum(Tt[i], Tt[i + 1] + wa, out=Tt[i])
        for j in range(1, G):
            np.minimum(Tt[:, j], Tt[:, j - 1] + wb, out=Tt[:, j])
        for j in range(G - 2, -1, -1):
            np.minimum(Tt[:, j], Tt[:, j + 1] + wb, out=Tt[:, j])
        return float((-mi - Ik + Tt)[inside].max())
    lo, hi = 0.0, 0.2
    for _ in range(22):
        mid = 0.5 * (lo + hi)
        if Eof(mid) >= e:
            lo = mid
        else:
            hi = mid
    # sup-min restricted to this centre type
    from scipy.optimize import minimize
    f = lambda x: -T.obj_bin(K, e, K.v, (m, x[0], x[1]))
    best = 0.0
    for s in ((0.298, 0.298), (0.27, 0.33), (0.33, 0.27), (0.2, 0.2)):
        r = minimize(f, np.array(s), method="Nelder-Mead", options={"xatol": 1e-8, "fatol": 1e-13, "maxiter": 600})
        best = max(best, -r.fun)
    print(f"  m = {m}: definition on the grid {lo:.5f} | sup-min over (a,b) at this m {best:.7f}   [{time.time()-t0:.0f}s]", flush=True)

print("(iii) n_mu: robust solver against the direct 2-d search")
worst = 0.0
for trial in range(10):
    m, a, b = rng.uniform(0.3, 0.7), rng.uniform(0.15, 0.4), rng.uniform(0.15, 0.4)
    lams, mus = T.bin_blocks(m, a, b)
    X = rng.uniform(0.005, 0.05)
    n1 = T.n_mu(K, lams, mus, X, K.v)
    n2 = T.n_mu_grid(K, lams, mus, X, K.v, G=1201, zoom=6)
    worst = max(worst, abs(n1 - n2))
print(f"  10 random profiles: largest difference {worst:.1e}")
print(f"time {time.time()-t0:.0f}s")
