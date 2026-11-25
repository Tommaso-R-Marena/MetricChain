"""N13 — the lever arm in ONE set of coordinates: first-order envelope vs spectral class.

Toy chain.  n+1 bond vectors u_0..u_n in {+1,-1} (a directed walk on the line); "torsion-like"
variables x_i = [u_i != u_{i-1}], i = 1..n, so that u_k u_l = chi_{(k,l]}(x) is the Walsh character
of the INTERVAL (k,l] — interaction order l-k in the variables x.  Every energy that is quadratic
in the positions p_j = sum_{k<j} u_k (squared radius of gyration, elastic networks, harmonic
restraints with arbitrary position-dependent stiffness) is therefore

      g(x) = sum_{0<=k<l<=n} w_kl chi_{(k,l]}(x):   orders up to n, but only n(n+1)/2 modes.

Residual: g = (lam/n) * sum_{k<l} (1 + 0.5 xi_kl) u_k u_l   (a noisy "R_g^2" term, lam = 1),
known part f = e * (number of flips), e = 0.5; target min(f+g) within eps = 0.25.

W: first-order envelope in the x-coordinates with the smallest valid constants
   c_i = max_x |g(x) - g(x + e_i)|  (kappa = 1, oracle).  These grow with the distance to the
   chain end (flipping x_i reverses every bond vector beyond i): the lever arm.
H: ball of the kernel whose spectrum is 1 on interval characters, B = ||g|| (kappa = 1) or 2||g||.
B: Gaussian prior with the second moments of the generating law (mis-centred on purpose: the
   true coefficients all have the same sign); validity is recorded, not assumed.
Run: OMP_NUM_THREADS=1 python3 n13_lever_arm.py
"""
import json
import math

import numpy as np

import cube as cb
from n5_compare import (best_first_W, cover_matrix, flip_constants, fractional_cover,
                        greedy_cover, kernel_best_first)

EPS, E_FLIP, LAM = 0.25, 0.5, 1.0
rows = []
for n in (6, 7, 8, 9, 10, 11, 12):
    size = 1 << n
    wts = cb.weights(n).astype(float)
    f = E_FLIP * wts
    # interval masks: (k,l] with 0 <= k < l <= n  <->  bits k..l-1
    masks = [sum(1 << b for b in range(k, l)) for k in range(n) for l in range(k + 1, n + 1)]
    M = len(masks)
    rec_n = []
    for seed in range(3):
        rng = np.random.default_rng(13_000 + 100 * n + seed)
        w = (LAM / n) * (1 + 0.5 * rng.standard_normal(M))
        ghat = np.zeros(size)
        ghat[masks] = w
        g = cb.fwht(ghat)
        c = flip_constants(g, n)
        r = {"n": n, "seed": seed, "M": M, "c_end": float(min(c[0], c[-1])), "c_mid": float(c[n // 2]),
             "c": [float(v) for v in c]}
        if n <= 11:
            cov = cover_matrix(f, g, c, EPS, n)
            r["W_greedy"] = greedy_cover(cov)
            if n <= 9:
                r["W_frac"] = fractional_cover(cov)
            del cov
        r["W_bestfirst"] = best_first_W(f, g, c, EPS, n)
        v = np.zeros(size)
        v[masks] = 1.0
        norm = math.sqrt(cb.rkhs_norm2(g, v))
        for kap in (1.0, 0.5):
            st, ok, _ = kernel_best_first(f, g, v, n, EPS, "H", B=norm / kap)
            r[f"H_kbf_kappa{kap}"], r[f"H_valid_kappa{kap}"] = st, bool(ok)
        vB = v * (LAM / n) ** 2 * 1.25
        st, ok, _ = kernel_best_first(f, g, vB, n, EPS, "B")
        r["B_kbf"], r["B_valid"] = st, bool(ok)
        rec_n.append(r)
        rows.append(r)
    med = lambda k: float(np.median([r[k] for r in rec_n])) if k in rec_n[0] else float("nan")
    print(f"n={n:2d} |X|={size:5d} M={M:3d} c(end)={med('c_end'):.2f} c(mid)={med('c_mid'):.2f} | "
          f"W: frac={med('W_frac'):7.1f} greedy={med('W_greedy'):6.0f} bestfirst={med('W_bestfirst'):6.0f}"
          f" | H: {med('H_kbf_kappa1.0'):4.0f} (B=||g||), {med('H_kbf_kappa0.5'):4.0f} (B=2||g||)"
          f" | B: {med('B_kbf'):4.0f}  valid H/H/B = "
          f"{sum(r['H_valid_kappa1.0'] for r in rec_n)}/{sum(r['H_valid_kappa0.5'] for r in rec_n)}/"
          f"{sum(r['B_valid'] for r in rec_n)} of 3", flush=True)
json.dump({"eps": EPS, "e": E_FLIP, "lam": LAM, "rows": rows}, open("n13_lever_arm.json", "w"), indent=1)
print("N13 done")
