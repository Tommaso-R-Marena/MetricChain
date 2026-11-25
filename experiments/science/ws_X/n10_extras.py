"""N10 — two small computations for the report.

(I) ln Z over the order-2 Walsh ellipsoid on the cube, after the main effects are known.
    Class: g = sum_{i<j} ghat_ij chi_i chi_j with sum ghat_ij^2 / v2 <= B^2, v2 = n s2 / C(n,2),
    B = b sqrt(n); f = 0 (uniform reference).  By Theorem B,
         U(beta) = sup_{||r|| <= B} ln E_unif exp(-beta r) = sup_pi [beta B sqrt(pi K pi) - KL(pi||unif)].
    Candidates: (i) the Curie-Weiss member r = -t sum_{i<j} chi_i chi_j (t fixed by the norm), whose
    value is a one-dimensional sum; (ii) numerical ascent from random, localised and CW starts.
    Mean-field prediction: U = O(1) for 2 beta b sqrt(s2) < 1 and
         U ~ n sup_m [beta b sqrt(s2) m^2 - I(m)] above.   Upper bound: beta B max_x P(x) = n beta b sqrt(s2).

(II) What it costs an ellipsoid to contain a dip.  RKHS norm of the first-order dip
         dip(x) = -(D - c d_H(x,y))_+ ,   D = 3, c = 1
     under the product spectrum sigma^2 rho^{d_H} with rho = 1 - 2 lam/n (bounded effective order),
     relative to the typical norm sqrt(2^n) of a prior draw and to the norm of an additive function
     of the same depth.
Run: OMP_NUM_THREADS=1 python3 n10_extras.py
"""
import itertools
import json
import math

import numpy as np
from scipy.special import gammaln, logsumexp

import cube as cb

rng = np.random.default_rng(1010)
out = {"cw": [], "dip": []}


def I_rate(m):
    m = min(max(m, -1 + 1e-15), 1 - 1e-15)
    return 0.5 * (1 + m) * math.log(1 + m) + 0.5 * (1 - m) * math.log(1 - m)


# ---------------------------------------------------------------- (I)
b, s2 = 1.0, 0.25
for n in (8, 10, 12):
    size = 1 << n
    pairs = list(itertools.combinations(range(n), 2))
    P2 = len(pairs)
    v2 = n * s2 / P2
    B = b * math.sqrt(n)
    idx = np.arange(size)
    spins = 1 - 2 * ((idx[:, None] >> np.arange(n)[None, :]) & 1)
    feats = np.stack([spins[:, i] * spins[:, j] for i, j in pairs], axis=1).astype(float)  # (2^n, P2)
    Khalf = feats * math.sqrt(v2)                    # K = Khalf Khalf^T
    lnu = -n * math.log(2)

    def value(w):
        a = -(Khalf @ w)
        m = a.max()
        return m + math.log(np.exp(a - m).sum()) + lnu

    def ascent(w, beta):
        w = w * (B / np.linalg.norm(w))
        val = value(beta * w)
        for _ in range(500):
            a = -beta * (Khalf @ w)
            p = np.exp(a - a.max())
            p /= p.sum()
            grad = -(Khalf.T @ p)
            ng = np.linalg.norm(grad)
            if ng < 1e-300:
                break
            w2 = B * grad / ng
            v2_ = value(beta * w2)
            if v2_ <= val + 1e-13:
                break
            w, val = w2, v2_
        return val

    M = n - 2 * np.arange(n + 1)
    logc = gammaln(n + 1) - gammaln(np.arange(n + 1) + 1) - gammaln(n - np.arange(n + 1) + 1)
    t = B * math.sqrt(v2 / P2)                       # CW member: r = -t sum_{i<j} s_i s_j, ||r|| = B
    for beta in (0.4, 0.8, 1.0, 1.2, 1.6, 2.4, 4.0):
        U_cw = float(logsumexp(logc + beta * t * (M ** 2 - n) / 2) + lnu)
        starts = [rng.standard_normal(P2) for _ in range(12)]
        starts.append(-np.ones(P2))                                   # CW direction
        for x in rng.integers(0, size, 4):                             # localised directions
            starts.append(-Khalf[x])
        U_num = max(ascent(w0, beta) for w0 in starts)
        mf = max(n * (beta * b * math.sqrt(s2) * m ** 2 - I_rate(m)) for m in np.linspace(0, 1, 2001))
        rec = {"n": n, "beta": beta, "2*beta*b*sqrt(s2)": 2 * beta * b * math.sqrt(s2),
               "U_numeric": U_num, "U_CurieWeiss": U_cw, "mean_field_extensive": mf,
               "sup_norm_bound": beta * B * math.sqrt(n * s2)}
        out["cw"].append(rec)
        print(rec, flush=True)
        assert U_num <= rec["sup_norm_bound"] + 1e-9

# ---------------------------------------------------------------- (II)
for n in (8, 10, 12, 14, 16):
    size = 1 << n
    idx = np.arange(size)
    dist = cb.popcount(idx.astype(np.uint64))
    dip = -np.maximum(3.0 - 1.0 * dist, 0.0)                       # centred at y = 0
    add = -3.0 * (1 - dist / n)                                    # additive function, same depth at 0
    for lam in (0.5, 2.0):
        v = cb.product_spectrum(n, 1.0, 1 - 2 * lam / n)
        nd = math.sqrt(cb.rkhs_norm2(dip, v))
        na = math.sqrt(cb.rkhs_norm2(add, v))
        rec = {"n": n, "lam": lam, "norm_dip": nd, "norm_additive_same_depth": na,
               "typical_prior_norm": math.sqrt(size), "ratio_dip_over_typical": nd / math.sqrt(size),
               "log10_norm_dip": math.log10(nd)}
        out["dip"].append(rec)
        print(rec, flush=True)

with open("n10_extras.json", "w") as fh:
    json.dump(out, fh, indent=1)
print("N10 done")
