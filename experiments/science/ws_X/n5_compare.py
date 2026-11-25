"""N5 — the same toy problem under both paradigms: cost in evaluations of g as a function of n.

Toy problem.  X = {0,1}^n, known part f(x) = e*|x| (ground state 0, excitation energy e per site),
residual g drawn from the centred Gaussian field with isotropic ANOVA spectrum
   sigma_1^2 = n*s1, sigma_2^2 = n*s2  (orders 1 and 2 only; optionally an order-3 tail n*s3).
Target: min(f+g) within eps (a width), delta = 0.05 where a probability is involved.

Paradigm W (theory division; first-order envelope, worst case).  The class is
   {g : |g(x)-g(y)| <= sum_i c_i [x_i != y_i]}   with the SMALLEST valid constants
   c_i = max_x |g(x) - g(x + e_i)|  (an oracle choice: the best case for W).
   * exp-weights lower bound on the certificate size (theory report Thm 11.6(c), machine-checked
     `partition_bound`), valid for every algorithm up to the factor (1-2 delta) (Thm 11.23(b));
   * fractional covering number (LP), greedy cover (upper bound on N_cov), for small n;
   * best-first search (Piyavskii-Shubert), an actual hint-free algorithm of paradigm W.
Paradigm H (this report; Walsh-ellipsoid, worst case).  Class {||g||_v <= B}, B = 1.1*||g||_v
   (again an oracle-flavoured choice).  Hint-free algorithm: evaluate the minimiser of the lower
   confidence bound  f + ghat_A - B_A P_A  until  UB - LB <= eps  ("kernel best-first").
Paradigm B (this report; Gaussian prior, 1-delta credible).  Same algorithm with B_A replaced by
   z_t = sqrt(2 ln(|X| t^2 pi^2 / (3 delta)))  (union bound over points and steps).

Run:  python3 n5_compare.py [quick]
"""
import json
import math
import sys
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

import cube as cb

QUICK = len(sys.argv) > 1 and sys.argv[1] == "quick"
DELTA = 0.05


# ------------------------------------------------------------------ paradigm W helpers
def flip_constants(g, n):
    idx = np.arange(1 << n)
    return np.array([np.max(np.abs(g - g[idx ^ (1 << i)])) for i in range(n)])


def hamming_dist_table(c, n):
    """D[z] = sum_i c_i z_i for every bitmask z."""
    D = np.zeros(1)
    for i in range(n):
        D = np.concatenate([D, D + c[i]])
    return D


def product_transform(h, w, n):
    """(T h)(a) = sum_y prod_i w_i^{[a_i != y_i]} h(y)."""
    h = np.array(h, dtype=float)
    size = h.shape[0]
    for i in range(n):
        blk = 1 << i
        h = h.reshape(-1, 2, blk)
        h = np.stack([h[:, 0, :] + w[i] * h[:, 1, :], h[:, 1, :] + w[i] * h[:, 0, :]], axis=1)
        h = h.reshape(size)
    return h


def expw_lower_bound(f, g, c, eps, n):
    """max_t  e^{-t eps} sum_y e^{-t gap(y)} / max_a sum_y e^{-t s(a,y)},  s = d - g(a) + g(y)."""
    E = f + g
    gap = E - E.min()
    best = 1.0
    for t in np.concatenate([np.linspace(0.05, 3, 60), np.linspace(3.2, 12, 45)]):
        num = math.exp(-t * eps) * np.sum(np.exp(-t * gap))
        gm = g - g.mean()
        den = np.max(np.exp(t * gm) * product_transform(np.exp(-t * gm), np.exp(-t * c), n))
        best = max(best, num / den)
    return best


def cover_matrix(f, g, c, eps, n):
    size = 1 << n
    E = f + g
    gap = E - E.min()
    D = hamming_dist_table(c, n)
    idx = np.arange(size)
    xor = idx[:, None] ^ idx[None, :]
    s = D[xor] - g[:, None] + g[None, :]          # s[a, y]
    return s <= gap[None, :] + eps + 1e-12


def greedy_cover(cov):
    size = cov.shape[0]
    uncovered = np.ones(size, dtype=bool)
    count = 0
    covf = cov.astype(np.float32)
    while uncovered.any():
        gains = covf @ uncovered.astype(np.float32)
        a = int(np.argmax(gains))
        uncovered &= ~cov[a]
        count += 1
    return count


def fractional_cover(cov):
    size = cov.shape[0]
    A = csr_matrix(-cov.T.astype(float))           # for each y: -sum_{a covers y} z_a <= -1
    res = linprog(np.ones(size), A_ub=A, b_ub=-np.ones(size), bounds=(0, None), method="highs")
    return float(res.fun)


def best_first_W(f, g, c, eps, n, max_steps=None):
    size = 1 << n
    D = hamming_dist_table(c, n)
    idx = np.arange(size)
    L = np.full(size, -np.inf)
    UB = np.inf
    steps = 0
    max_steps = max_steps or size
    while steps < max_steps:
        if steps == 0:
            a = int(np.argmin(f))
        else:
            lower = f + L
            a = int(np.argmin(lower))
            if UB - lower[a] <= eps + 1e-12:
                break
        steps += 1
        L = np.maximum(L, g[a] - D[idx ^ a])
        UB = min(UB, f[a] + g[a])
    return steps


# ------------------------------------------------------------------ paradigms H and B
def kernel_best_first(f, g, v, n, eps, mode, B=None, delta=DELTA, max_steps=None):
    """Sequential lower-confidence-bound minimisation with exact (noise-free) kernel updates.
    mode = "H": band B_A * P_A (hypercircle);  mode = "B": band z_t * P_A (Gaussian credible)."""
    size = 1 << n
    kap = cb.fwht(v)
    idx = np.arange(size)
    var = np.full(size, kap[0])
    mean = np.zeros(size)
    cols = []
    norm2 = 0.0
    UB = np.inf
    steps = 0
    max_steps = max_steps or size
    truth = float(np.min(f + g))
    valid = True
    a = int(np.argmin(f))
    while True:
        # evaluate a
        steps += 1
        va = var[a]
        if va > 1e-12 * kap[0]:
            col = kap[idx ^ a].copy()
            for l in cols:
                col -= l * l[a]
            col /= math.sqrt(va)
            alpha = (g[a] - mean[a]) / math.sqrt(va)
            mean = mean + alpha * col
            var = np.maximum(var - col ** 2, 0.0)
            cols.append(col)
            norm2 += alpha ** 2
        UB = min(UB, f[a] + g[a])
        P = np.sqrt(var)
        if mode == "H":
            band = math.sqrt(max(B ** 2 - norm2, 0.0)) * P
        else:
            z = math.sqrt(2 * math.log(size * (steps + 1) ** 2 * math.pi ** 2 / (3 * delta)))
            band = z * P
        lower = f + mean - band
        a = int(np.argmin(lower))
        LB = float(lower[a])
        if not (LB - 1e-9 <= truth <= UB + 1e-9):
            valid = False
        if UB - LB <= eps + 1e-12 or steps >= max_steps:
            break
    return steps, valid, UB - LB


# ------------------------------------------------------------------ experiment, part I
def run_cell(n, e, s, eps, seed, kappa, do_cover, do_lp, do_bf, do_kernel):
    rng = np.random.default_rng(seed)
    v = cb.iso_spectrum(n, [0.0] + [n * sj for sj in s])
    g = cb.sample_gp(v, rng)
    w = cb.weights(n)
    f = e * w.astype(float)
    c = flip_constants(g, n) / kappa
    out = {"n": n, "e": e, "seed": seed, "kappa": kappa, "c_mean": float(c.mean()),
           "sharp_sites": int(np.sum(c <= e)), "M": int(np.sum(v > 0))}
    out["W_expw_lb"] = float(expw_lower_bound(f, g, c, eps, n))
    if do_cover:
        cov = cover_matrix(f, g, c, eps, n)
        out["W_greedy"] = greedy_cover(cov)
        if do_lp:
            out["W_frac"] = fractional_cover(cov)
        del cov
    if do_bf:
        out["W_bestfirst"] = best_first_W(f, g, c, eps, n)
    if do_kernel:
        B = math.sqrt(cb.rkhs_norm2(g, v)) / kappa
        st, ok, _ = kernel_best_first(f, g, v, n, eps, "H", B=B)
        out["H_kbf"], out["H_valid"], out["H_B"] = st, bool(ok), B
        st, ok, _ = kernel_best_first(f, g, v, n, eps, "B")
        out["B_kbf"], out["B_valid"] = st, bool(ok)
    return out


def part_one(eps, s):
    ns = [6, 8, 10] if QUICK else [6, 7, 8, 9, 10, 11, 12]
    es = [0.5] if QUICK else [0.0, 0.5, 1.0, 2.0]
    kappas = [1.0, 0.5]
    seeds = range(2) if QUICK else range(5)
    rows = []
    t0 = time.time()
    for kappa in kappas:
        for e in es:
            for n in ns:
                for seed in seeds:
                    rows.append(run_cell(n, e, s, eps, 1000 * n + seed, kappa, do_cover=n <= 11,
                                         do_lp=n <= 9, do_bf=True, do_kernel=True))
                sub = [r for r in rows if r["n"] == n and r["e"] == e and r["kappa"] == kappa]
                med = lambda k: float(np.median([r[k] for r in sub])) if k in sub[0] else float("nan")
                print(f"kappa={kappa:3.1f} e={e:3.1f} n={n:2d} |X|={1<<n:5d} c~{med('c_mean'):.2f} "
                      f"sharp={med('sharp_sites'):.0f} | W: expw>={med('W_expw_lb'):7.1f} "
                      f"frac={med('W_frac'):7.1f} greedy={med('W_greedy'):6.0f} "
                      f"bestfirst={med('W_bestfirst'):6.0f} | H: kbf={med('H_kbf'):4.0f} | "
                      f"B: kbf={med('B_kbf'):4.0f} | M={med('M'):.0f} valid H/B="
                      f"{sum(r['H_valid'] for r in sub)}/{sum(r['B_valid'] for r in sub)} of {len(sub)}"
                      f"  [{time.time()-t0:.0f}s]", flush=True)
    return rows


# ------------------------------------------------------------------ experiment, part II
def site_rate(t, e, gam, c, ratios):
    """max over site weights v=(1, ratio) of r(t; v) for a two-state site with total energies
    E(0)=0, E(1)=e+gam, residual gam*s, envelope constant c  (theory report Thm 11.8)."""
    Es = np.array([0.0, e + gam])
    gap = Es - Es.min()
    gs = np.array([0.0, gam])
    # rho[a, s] = c [a != s] - g(a) + g(s) - gap(s)
    rho = np.array([[c * (a != s_) - gs[a] + gs[s_] - gap[s_] for s_ in (0, 1)] for a in (0, 1)])
    v = np.stack([np.ones_like(ratios), ratios], axis=1)              # (R, 2)
    num = np.log(v.sum(axis=1))
    den = np.log(np.max(v @ np.exp(-t * rho).T, axis=1))              # max over a
    return float(np.max(num - den))


def product_lower_bound(e, gam, c, eps):
    """ln N_cov >= max_t [ sum_i max_v r_i(t; v) - t eps ]   (common slope t)."""
    ratios = np.concatenate([[0.0], np.exp(np.linspace(-12, 12, 481))])
    best = 0.0
    for t in np.concatenate([np.linspace(0.02, 2, 100), np.linspace(2.1, 20, 180)]):
        tot = sum(site_rate(t, e, gam[i], c[i], ratios) for i in range(len(gam))) - t * eps
        best = max(best, tot)
    return best


def part_two(eps, s1):
    """Additive toy: g = sum_i gam_i x_i, gam_i ~ N(0, 4 s1) (the order-1 part of the prior).
    W: machine-checked product lower bound (Thm 11.8) with c_i = |gam_i|/kappa.
    H/B: the kernel has rank n+1 (constant + n main effects): n+1 evaluations determine g."""
    rows = []
    for kappa in (1.0, 0.5):
        for e in (0.0, 0.1, 0.2, 0.4):
            for n in (10, 20, 50, 100, 200, 500, 1000):
                vals = []
                for seed in range(5):
                    rng = np.random.default_rng(7_000_000 + 1000 * n + seed)
                    gam = rng.standard_normal(n) * 2 * math.sqrt(s1)
                    c = np.abs(gam) / kappa
                    vals.append(product_lower_bound(e, gam, c, eps))
                rows.append({"kappa": kappa, "e": e, "n": n, "lnN_W_lb_median": float(np.median(vals)),
                             "lnN_W_lb_min": float(np.min(vals)), "N_HB": n + 1})
                print(f"additive toy kappa={kappa} e={e:4.2f} n={n:4d}: ln N_W >= "
                      f"{np.median(vals):8.2f} (min {np.min(vals):7.2f}; log10 N >= "
                      f"{np.median(vals)/math.log(10):6.1f})   N_H = N_B = {n+1}", flush=True)
    return rows


def validate_product_bound(eps, s1):
    """Sanity: on small additive instances the product bound is below the fractional cover."""
    worst = 0.0
    for seed in range(12):
        rng = np.random.default_rng(99 + seed)
        n = int(rng.integers(5, 10))
        gam = rng.standard_normal(n) * 2 * math.sqrt(s1)
        kappa = [1.0, 0.5][seed % 2]
        e = [0.0, 0.1, 0.2][seed % 3]
        c = np.abs(gam) / kappa
        idx = np.arange(1 << n)
        bits = ((idx[:, None] >> np.arange(n)[None, :]) & 1).astype(float)
        g = bits @ gam
        f = e * bits.sum(axis=1)
        cov = cover_matrix(f, g, c, eps, n)
        frac = fractional_cover(cov)
        lb = product_lower_bound(e, gam, c, eps)
        worst = max(worst, lb - math.log(frac))
        assert lb <= math.log(frac) + 1e-6, (lb, math.log(frac))
    print("product lower bound <= ln N_frac on 12 small additive instances; max(lb - ln N_frac) =",
          worst)
    return worst


def main():
    eps = 0.25
    s = (0.04, 0.02)                  # (s1, s2): exact order <= 2
    rows1 = part_one(eps, s)
    slack = validate_product_bound(eps, s[0])
    rows2 = [] if QUICK else part_two(eps, s[0])
    with open("n5_compare_quick.json" if QUICK else "n5_compare.json", "w") as fh:
        json.dump({"eps": eps, "s": s, "delta": DELTA, "part_one": rows1,
                   "product_bound_validation_max_slack": slack, "part_two": rows2}, fh, indent=1)


if __name__ == "__main__":
    main()
