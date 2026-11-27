"""N7 — spectrum => exponent.  Two-sided bounds on the sup-norm design complexity
        n_p(eta) = min{ N : exists design A, |A| = N, max_x P_A(x) <= eta }
for the brief's product covariance k(x,y) = sigma^2 rho^{d_H(x,y)} on {0,1}^n:

   M(eta)  <=  n_p(eta)  <=  2 * ceil( 8 sigma^2 M(eta/sqrt 8) / eta^2 )        (Theorem A)

with M(eta) = min{M : T(M) <= eta^2}, T(M) = sum of all but the M largest eigenvalues.
Eigenvalues: sigma^2 a^{n-m} b^m with multiplicity C(n,m), a=(1+rho)/2, b=(1-rho)/2.

Part 1: fixed rho  -> exponent h(b) (binary entropy in nats), for every fixed relative tolerance.
Part 2: rho = 1 - 2 lam / n -> polynomial, degree = a Poisson(lam) quantile.
Part 3: random linear codes (the existence argument of Theorem A) on small cubes:
        E[NL] <= T(M) + sigma^2 M / N0, and sup_x P_A^2 <= 4 NL.
Run: python3 n7_exponent.py
"""
import json
import math

import numpy as np
from scipy.special import gammaln, logsumexp

import cube as cb


def log_comb(n, k):
    return gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)


def M_of_eta(n, b, theta2):
    """ln M(eta) for relative tolerance theta^2 = eta^2/sigma^2: eigenvalues are decreasing in the
    order m when b < 1/2, so the top-M set is a union of layers plus part of one layer."""
    m = np.arange(n + 1)
    logmass = log_comb(n, m) + m * math.log(b) + (n - m) * math.log(1 - b)   # ln of layer variance
    logcount = log_comb(n, m)
    # tail[j] = variance of layers j..n
    tail = np.array([logsumexp(logmass[j:]) for j in range(n + 1)] + [-np.inf])
    lt = math.log(theta2)
    # smallest j such that tail[j+1] <= theta2: keep layers 0..j entirely is enough; refine inside j
    j = 0
    while tail[j + 1] > lt:
        j += 1
    # layers 0..j-1 are needed entirely; of layer j we need a fraction
    need = math.exp(tail[j]) - theta2                 # variance still to be removed from layer j
    frac = max(0.0, min(1.0, need / math.exp(logmass[j])))
    parts = [logcount[i] for i in range(j)]
    if frac > 0:
        parts.append(logcount[j] + math.log(frac))
    return float(logsumexp(parts)) if parts else 0.0, j


def h(b):
    return -b * math.log(b) - (1 - b) * math.log(1 - b)


out = {"fixed_rho": [], "scaled_rho": [], "random_codes": []}
print("Part 1: fixed rho, relative tolerance theta = eta/sigma")
for rho in (0.5, 0.9, 0.99):
    b = (1 - rho) / 2
    for theta in (0.5, 0.1):
        for n in (50, 100, 200, 500, 1000, 2000):
            lo, j = M_of_eta(n, b, theta ** 2)
            up_M, _ = M_of_eta(n, b, theta ** 2 / 8)
            up = math.log(2) + math.log(8 / theta ** 2) + up_M
            up = min(up, n * math.log(2))
            rec = {"rho": rho, "theta": theta, "n": n, "lnN_lower": lo, "lnN_upper": up,
                   "rate_lower": lo / n, "rate_upper": up / n, "h(b)": h(b), "order_needed": j}
            out["fixed_rho"].append(rec)
            print(f"rho={rho:4.2f} theta={theta:3.1f} n={n:5d}: {lo/n:.4f} <= (1/n) ln n_p <= {up/n:.4f}"
                  f"   h((1-rho)/2) = {h(b):.4f}   order needed ~ {j} (nb = {n*b:.1f})")

print("Part 2: rho = 1 - 2 lam/n  (bounded effective order)")
for lam in (0.5, 2.0):
    for theta in (0.5, 0.1):
        for n in (50, 100, 200, 500, 1000, 2000):
            b = lam / n
            lo, j = M_of_eta(n, b, theta ** 2)
            up_M, j2 = M_of_eta(n, b, theta ** 2 / 8)
            up = math.log(2) + math.log(8 / theta ** 2) + up_M
            rec = {"lam": lam, "theta": theta, "n": n, "lnN_lower": lo, "lnN_upper": up,
                   "deg_lower": lo / math.log(n), "deg_upper": up / math.log(n), "order_lo": j,
                   "order_up": j2}
            out["scaled_rho"].append(rec)
            print(f"lam={lam:3.1f} theta={theta:3.1f} n={n:5d}: ln n_p in [{lo:7.2f}, {up:7.2f}] "
                  f"= n^[{lo/math.log(n):.2f}, {up/math.log(n):.2f}]   orders {j}..{j2}")

print("Part 3: random linear designs on small cubes")
rng = np.random.default_rng(3)
for n, rho in ((10, 0.9), (12, 0.9), (12, 0.8), (14, 0.9)):
    v = cb.product_spectrum(n, 1.0, rho)
    order = np.argsort(-v, kind="stable")
    rank_of = np.empty(1 << n, dtype=np.int64)
    rank_of[order] = np.arange(1 << n)
    sorted_v = v[order]
    tailsum = np.concatenate([np.cumsum(sorted_v[::-1])[::-1], [0.0]])       # T(M) = tailsum[M]
    for r in (4, 6, 8):
        if r >= n:
            continue
        N0 = 1 << r
        NLs, sups = [], []
        ntr = 2000 if n <= 12 else 300
        for trial in range(ntr):
            rows = [int(x) for x in rng.integers(1, 1 << n, size=r)]
            NL = cb.non_leader_mass(v, rows, n)
            NLs.append(NL)
            if trial < 3 and n <= 12:
                _, var, _ = cb.posterior_linear(v, rows, n)
                sups.append(float(var.max()))
                assert var.max() <= 4 * NL + 1e-9
        # bound: min over M of T(M) + sum_{U in top-M} v_U * rank(U)/N0  (sharper form) and
        #        the simple form T(M) + sigma^2 M / N0
        cum_rank = np.cumsum(sorted_v * np.arange(1 << n)) / N0
        sharp = float(np.min(tailsum[1:] + cum_rank))
        Ms = np.arange(1, (1 << n) + 1)
        simple = float(np.min(tailsum[1:] + Ms / N0))
        se = float(np.std(NLs) / math.sqrt(len(NLs)))
        rec = {"n": n, "rho": rho, "N0": N0, "trials": ntr, "mean_NL": float(np.mean(NLs)), "se": se,
               "median_NL": float(np.median(NLs)), "min_NL": float(np.min(NLs)),
               "bound_sharp": sharp, "bound_simple": simple, "eig_tail_T(N0)": float(tailsum[N0]),
               "sup_var_examples": sups}
        out["random_codes"].append(rec)
        print(rec)
        assert np.mean(NLs) <= sharp + 4 * se + 1e-9   # the expectation bound, 4 standard errors

with open("n7_exponent.json", "w") as fh:
    json.dump(out, fh, indent=1)
print("N7 done")
