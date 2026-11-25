"""N5b — the additive toy for large n (vectorised re-implementation of part II of n5_compare.py).

Toy.  X = {0,1}^n, f(x) = e|x|, residual g(x) = sum_i gam_i x_i with gam_i ~ N(0, 4 s1), s1 = 0.04
(the order-1 part of the prior of n5_compare.py; flip increments of standard deviation 0.4).
Accuracy eps = 0.25.

Paradigm W: first-order class with constants c_i = |gam_i| / kappa.  Lower bound on the size of
EVERY eps-certificate, hence (times 1-2 delta) on the expected number of evaluations of every
algorithm that is correct on the class (theory report Thm 11.8 `product_exp_weights` [V] and
Thm 11.23(b) `expected_queries_ge_exp_weights_min` [V]):

      ln N  >=  max_{t >= 0} [ sum_i max_v r_i(t; v) - t eps ],
      r_i(t; v) = ln sum_s v(s) - ln max_a sum_s v(s) exp(-t rho_i(a,s)),
      rho_i(a,s) = c_i [a != s] - gam_i(a) + gam_i(s) - gap_i(s).

Paradigms H and B: the kernel of additive functions (constant + n main effects) has rank n+1;
n+1 evaluations on any unisolvent set (a star, or a Hadamard design when n+1 is a power of two)
determine g, so the minimum is known exactly: N = n + 1, for every instance and every eps.

Also reported: the same bound for the ZERO residual with a uniform constant c (the theory
division's own hard instance), and the kappa at which the envelope bound first exceeds n+1.
Run: python3 n5b_additive.py
"""
import json
import math

import numpy as np

EPS = 0.25
S1 = 0.04
RATIOS = np.concatenate([[0.0], np.exp(np.linspace(-14, 14, 281))])
TS = np.concatenate([np.linspace(0.01, 2, 80), np.linspace(2.1, 40, 220)])


def product_lower_bound(e, gam, c, eps):
    """Vectorised over sites and weight ratios.  Returns max_t [sum_i max_v r_i - t eps] (>= 0)."""
    E1 = e + gam                                  # energy of state 1 (state 0 has energy 0)
    gap0 = np.maximum(-E1, 0.0)                   # gap of state 0
    gap1 = np.maximum(E1, 0.0)                    # gap of state 1
    # rho[a][s]
    rho00 = -gap0
    rho01 = c + gam - gap1                        # a=0, s=1: c - g(0) + g(1) - gap(1)
    rho10 = c - gam - gap0                        # a=1, s=0
    rho11 = -gap1
    best = 0.0
    v1 = RATIOS[None, :]                          # (1, R)
    lognum = np.log1p(v1)
    for t in TS:
        a0 = np.exp(-t * rho00)[:, None] + v1 * np.exp(-t * rho01)[:, None]
        a1 = np.exp(-t * rho10)[:, None] + v1 * np.exp(-t * rho11)[:, None]
        r = lognum - np.log(np.maximum(a0, a1))   # (n, R)
        tot = float(np.sum(np.max(r, axis=1))) - t * eps
        best = max(best, tot)
    return best


rows = []
print("random additive residual, c_i = |gam_i|/kappa")
for kappa in (0.9, 0.7, 0.5, 0.25):
    for e in (0.0, 0.1, 0.2, 0.4):
        for n in (10, 20, 50, 100, 200, 500, 1000):
            vals = []
            for seed in range(5):
                rng = np.random.default_rng(7_000_000 + 1000 * n + seed)     # same draws as n5_compare
                gam = rng.standard_normal(n) * 2 * math.sqrt(S1)
                vals.append(product_lower_bound(e, gam, np.abs(gam) / kappa, EPS))
            med = float(np.median(vals))
            rows.append({"kind": "random", "kappa": kappa, "e": e, "n": n, "lnN_W_lb_median": med,
                         "lnN_W_lb_min": float(np.min(vals)), "rate_per_site": med / n,
                         "N_HB": n + 1})
            print(f"kappa={kappa:4.2f} e={e:4.2f} n={n:4d}: ln N_W >= {med:8.2f}"
                  f"  (N_W >= 10^{med/math.log(10):6.1f}; rate {med/n:.4f}/site)   N_H = N_B = {n+1}",
                  flush=True)

print("zero residual, uniform constant c (theory division's hard instance), f = e|x|, e = 0.2")
for c in (0.25, 0.4, 0.8):
    for n in (10, 20, 50, 100, 200, 500, 1000):
        lb = product_lower_bound(0.2, np.zeros(n), np.full(n, c), EPS)
        rows.append({"kind": "zero", "c": c, "e": 0.2, "n": n, "lnN_W_lb": lb, "N_HB": n + 1})
        print(f"c={c:4.2f} e=0.20 n={n:4d}: ln N_W >= {lb:8.2f}  (10^{lb/math.log(10):6.1f})"
              f"   N_H = N_B = {n+1}", flush=True)

# crossover: smallest n at which the envelope lower bound exceeds n+1
print("crossover n (smallest n in the grid with exp(lb) > n+1):")
cross = {}
for kappa in (0.9, 0.7, 0.5, 0.25):
    for e in (0.0, 0.1, 0.2, 0.4):
        sub = [r for r in rows if r["kind"] == "random" and r["kappa"] == kappa and r["e"] == e]
        hit = [r["n"] for r in sub if r["lnN_W_lb_median"] > math.log(r["n"] + 1)]
        cross[f"kappa={kappa},e={e}"] = min(hit) if hit else None
        print(f"  kappa={kappa} e={e}: {cross[f'kappa={kappa},e={e}']}")
with open("n5b_additive.json", "w") as fh:
    json.dump({"eps": EPS, "s1": S1, "rows": rows, "crossover": cross}, fh, indent=1)
print("N5b done")
