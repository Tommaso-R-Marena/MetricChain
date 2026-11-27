"""N11 — randomisation in a linear (additive) class: Monte Carlo over SITES.

Class (the theory division's box class with the features F_i(x) = x_i): g(x) = sum_i gam_i x_i,
gam_i in [-w, w]; known part f(x) = e|x|, 0 <= e < w.  Then
     min(f+g)     = sum_i min(0, e + gam_i),
     ln Z_beta    = sum_i ln( (1 + exp(-beta (e + gam_i))) / 2 )        (uniform reference).
Algorithm: evaluate g at 0 and at k single flips e_i, i in a uniform random k-subset of the sites
(k+1 evaluations; gam_i = g(e_i) - g(0)); return (n/k) * sum over the sample of the site terms.
Hoeffding (sampling without replacement): the error exceeds eps1*n with probability at most
2 exp(-2 k eps1^2 / R^2), R the range of a site term (R = w - e for the minimum).
A deterministic algorithm with error at most eps1*n on the class needs at least
n (1 - 4 eps1 / R) evaluations at the zero residual (the vertex argument of Proposition 11).

Check: empirical failure frequency for several adversarial coefficient patterns and n up to 10^5.
Run: python3 n11_site_mc.py
"""
import json
import math

import numpy as np

rng = np.random.default_rng(1111)
w, e, beta = 1.0, 0.2, 1.0
eps1, delta = 0.1, 0.05
R = w - e
k = math.ceil(R ** 2 / (2 * eps1 ** 2) * math.log(2 / delta))
Rz = math.log((1 + math.exp(-beta * (e - w))) / 2) - math.log((1 + math.exp(-beta * (e + w))) / 2)
kz = math.ceil(Rz ** 2 / (2 * eps1 ** 2) * math.log(2 / delta))
print(f"k = {k} sampled sites for the minimum (R = {R}),  k = {kz} for ln Z (range {Rz:.3f})")


def patterns(n):
    yield "uniform random", rng.uniform(-w, w, n)
    g = np.zeros(n); g[: n // 10] = -w
    yield "10% of sites at -w, rest 0", g
    g = np.full(n, -w); g[: n // 2] = w
    yield "half -w, half +w", g
    g = np.zeros(n); g[rng.choice(n, max(1, n // 50), replace=False)] = -w
    yield "2% of sites at -w (sparse)", g
    yield "all at -(e+0.01) (every site barely flips)", np.full(n, -(e + 0.01))


out = []
for n in (1000, 10_000, 100_000):
    for name, gam in patterns(n):
        site_min = np.minimum(0.0, e + gam)
        site_lnz = np.log((1 + np.exp(-beta * (e + gam))) / 2)
        truth_min, truth_lnz = site_min.sum(), site_lnz.sum()
        fails_min = fails_lnz = 0
        trials = 2000
        errs = []
        for _ in range(trials):
            idx = rng.choice(n, k, replace=False)
            est = n * site_min[idx].mean()
            errs.append(abs(est - truth_min) / n)
            fails_min += abs(est - truth_min) > eps1 * n
            idz = rng.choice(n, kz, replace=False)
            fails_lnz += abs(n * site_lnz[idz].mean() - truth_lnz) > eps1 * n
        rec = {"n": n, "pattern": name, "evaluations_min": k + 1, "evaluations_lnZ": kz + 1,
               "deterministic_lower_bound": n * (1 - 4 * eps1 / R),
               "fail_rate_min": fails_min / trials, "fail_rate_lnZ": fails_lnz / trials,
               "median_abs_err_per_site": float(np.median(errs)), "delta": delta}
        out.append(rec)
        print(rec)
        assert rec["fail_rate_min"] <= delta and rec["fail_rate_lnZ"] <= delta
with open("n11_site_mc.json", "w") as fh:
    json.dump({"w": w, "e": e, "beta": beta, "eps1": eps1, "delta": delta, "k_min": k, "k_lnZ": kz,
               "rows": out}, fh, indent=1)
print("N11 done")
