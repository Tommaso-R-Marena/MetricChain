"""(1) Random finite spaces with asymmetric envelopes: full LP = bipartite LP = dual LP; the closure of an optimal residual
(lower extension to A, then upper extension to B) is optimal, admissible on all of A u B, and a fixed point; Theorem 11.12
(one state against the rest) in closed form; weak duality for random feasible plans and random admissible residuals."""
import numpy as np, itertools, math
from ratio_lib import *
rng = np.random.default_rng(20261125)
worst = dict(full_vs_bip=0, bip_vs_dual=0, closed=0, single=0, weak=0.0, adm=0.0)
cases = 0
for rep in range(300):
    n = int(rng.integers(5, 10))
    D = rng.uniform(0.1, 3.0, size=(n, n))
    if rep % 3 == 0:
        D = (D + D.T) / 2
    D = closure(D)
    w = np.exp(rng.normal(0, 1.5, size=n))
    perm = rng.permutation(n)
    na = int(rng.integers(1, n - 1)); nb = int(rng.integers(1, n - na + 1))
    A = sorted(perm[:na].tolist()); B = sorted(perm[na:na + nb].tolist())
    vf, tf = lp_full(w, D, A, B)
    vb, tb = lp_bip(w, D, A, B)
    vd, psi = lp_dual(w, D, A, B)
    worst["full_vs_bip"] = max(worst["full_vs_bip"], abs(vf - vb) / vb)
    worst["bip_vs_dual"] = max(worst["bip_vs_dual"], abs(vd - vb) / vb)
    # closure of the bipartite optimum
    g = np.zeros(n)
    idx = A + B
    g[idx] = -np.log(np.maximum(tb[idx], 1e-300))
    g1 = lower_ext(g, D, A, B)
    g2 = upper_ext(g1, D, A, B)
    g3 = lower_ext(g2, D, A, B)
    worst["closed"] = max(worst["closed"], abs(ratio(w, g2, A, B) - vb) / vb, float(np.abs(g3[A] - g2[A]).max()))
    # admissibility of the closed pair on all of A u B (within A, within B, both cross directions)
    viol = max(g2[x] - g2[y] - D[x, y] for x in idx for y in idx)
    worst["adm"] = max(worst["adm"], viol)
    # weak duality with random admissible residuals
    for _ in range(5):
        c = rng.normal(0, 2, size=n)
        gg = np.array([min(c[y] + D[x, y] for y in range(n)) for x in range(n)])      # an admissible function (inf-convolution)
        assert max(gg[x] - gg[y] - D[x, y] for x in range(n) for y in range(n)) < 1e-9
        worst["weak"] = max(worst["weak"], ratio(w, gg, A, B) / vd - 1)
    if na == 1:
        y = A[0]
        closed = w[y] / sum(w[z] * math.exp(-D[z, y]) for z in B)
        worst["single"] = max(worst["single"], abs(closed - vb) / vb)
    cases += 1
print("cases", cases)
for k, v in worst.items():
    print(f"  {k:12s} {v:.3e}")
