#!/usr/bin/env python3
"""
R1 (SCI-REV-0001) -- Theorem 11.90(a): "binary centres suffice on a slice".

For a profile mu with k blocks (fractions lam_j, densities mu_j, sum lam_j mu_j = kappa):
    r(mu; e) = min{ MI(nu) : nu-bar = kappa,  u dist(nu, mu) <= e + MI(mu) }
    n(mu; X) = min{ MI(nu) : nu-bar = kappa,  MI(nu) + u dist(nu, mu) - MI(mu) <= X }
with MI(nu) = sum lam_j KL(nu_j || kappa), dist = sum lam_j |nu_j - mu_j|.
Claim: sup over ALL block structures of r and of n equals the sup over two-block profiles (closed forms of 11.90(b)).

What this script does (own code):
  * inner problems solved by KKT root finding (clipping thresholds), and every reported value is SANDWICHED:
        dual value  <=  true minimum  <=  value of an exactly feasible nu
    (weak duality is elementary and independent of the proof under review);
  * a second, independent inner solver (SLSQP on the split variables) on a random sample;
  * outer maximisation over k = 3, 4, 5 blocks by random multistart + Nelder-Mead;
    the result is compared with the two-block supremum R^kappa(e), N^kappa(X) computed in thm_1190.py;
  * negative accuracies e < 0 (where the published proof of (a) has a gap: feasibility is a second linear
    constraint on the law of block densities) are included.
A violation would be a profile whose DUAL (certified lower) value exceeds the two-block supremum.
Run:  python3 thm_1190a_blocks.py [quick]
"""
import math
import sys
import time

import numpy as np
from scipy.optimize import brentq, minimize

from thm_1190 import Ray, best_centre, kl, Psi_c, R_unif

rng = np.random.default_rng(20261125)


def sig(x):
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    z = math.exp(x)
    return z / (1.0 + z)


def lgt(x):
    return math.log(x) - math.log1p(-x)


def MI(lam, mu, kappa):
    return sum(l * kl(m, kappa) for l, m in zip(lam, mu))


def dist(lam, nu, mu):
    return sum(l * abs(a - b) for l, a, b in zip(lam, nu, mu))


def clip_profile(mu, lo, hi):
    return [min(max(m, lo), hi) for m in mu]


def solve_type(lam, mu, kappa, half_width):
    """thresholds (c_lo, c_hi) with logit c_hi - logit c_lo = 2*half_width such that the clipped profile has type kappa.
    Returns (nu, centre) where logit c = centre -+ half_width."""
    lk = lgt(kappa)

    def typ(c):
        lo, hi = sig(c - half_width), sig(c + half_width)
        return sum(l * min(max(m, lo), hi) for l, m in zip(lam, mu)) - kappa

    a, b = lk - half_width - 1.0, lk + half_width + 1.0
    while typ(a) > 0:
        a -= 5.0
        if a < -700:
            break
    while typ(b) < 0:
        b += 5.0
        if b > 700:
            break
    c = brentq(typ, a, b, xtol=1e-15, rtol=1e-15, maxiter=300)
    lo, hi = sig(c - half_width), sig(c + half_width)
    return clip_profile(mu, lo, hi), c


def r_inner(lam, mu, kappa, u, e):
    """returns (primal, dual, nu): dual <= r(mu;e) <= primal.  -inf if infeasible."""
    mi_mu = MI(lam, mu, kappa)
    B = (e + mi_mu) / u
    if B < -1e-15:
        return -math.inf, -math.inf, None
    B = max(B, 0.0)
    d0 = sum(l * abs(kappa - m) for l, m in zip(lam, mu))
    if d0 <= B:
        return 0.0, 0.0, [kappa] * len(mu)
    lk = lgt(kappa)

    def excess(w):
        nu, _ = solve_type(lam, mu, kappa, w)
        return dist(lam, nu, mu) - B

    # half width w = t*u; excess decreasing in w; excess(0) = d0 - B > 0
    w_hi = 1.0
    while excess(w_hi) > 0:
        w_hi *= 2.0
        if w_hi > 1e3:
            break
    if excess(w_hi) > 0:            # B = 0 (or tiny): exit = mu
        return mi_mu, mi_mu, list(mu)
    w = brentq(excess, 0.0, w_hi, xtol=1e-15, rtol=1e-15, maxiter=300)
    # make the primal point exactly feasible: take w slightly larger if needed
    nu, c = solve_type(lam, mu, kappa, w)
    k_ = 0
    while dist(lam, nu, mu) > B and k_ < 60:
        w = w * (1 + 1e-15 * 2 ** k_) + 1e-300
        nu, c = solve_type(lam, mu, kappa, w)
        k_ += 1
    primal = MI(lam, nu, kappa)
    # dual value at (t, xi): t*u = w, xi = logit(kappa) - c
    xi = lk - c
    dual = sum(l * (kl(y, kappa) + xi * (y - kappa) + w * abs(y - m)) for l, y, m in zip(lam, nu, mu)) - w * B
    return primal, dual, nu


def n_inner(lam, mu, kappa, u, X):
    """n(mu;X) by KKT: nu = clip(mu, sigma(c - w'), sigma(c + w')), w' = tau u/(1+tau).  returns (primal, dual, nu)"""
    mi_mu = MI(lam, mu, kappa)
    C = X + mi_mu
    d0 = u * sum(l * abs(kappa - m) for l, m in zip(lam, mu))
    if d0 <= C:
        return 0.0, 0.0, [kappa] * len(mu)
    lk = lgt(kappa)

    def G(wp):
        nu, _ = solve_type(lam, mu, kappa, wp)
        return MI(lam, nu, kappa) + u * dist(lam, nu, mu) - C

    # wp in [0, u): G decreasing; G(0) = d0 - C > 0; at wp -> u: the Gibbs shell (minimiser of MI + u dist)
    if G(u * (1 - 1e-12)) > 0:
        if X < 0:
            return -math.inf, -math.inf, None
        return mi_mu, mi_mu, list(mu)       # only mu itself (X = 0, self-consistent shell)
    wp = brentq(G, 0.0, u * (1 - 1e-12), xtol=1e-15, rtol=1e-15, maxiter=300)
    nu, c = solve_type(lam, mu, kappa, wp)
    k_ = 0
    while MI(lam, nu, kappa) + u * dist(lam, nu, mu) > C and k_ < 60:
        wp = min(wp * (1 + 1e-15 * 2 ** k_) + 1e-300, u * (1 - 1e-13))
        nu, c = solve_type(lam, mu, kappa, wp)
        k_ += 1
    primal = MI(lam, nu, kappa)
    tau = wp / (u - wp)
    xi = (1 + tau) * (lk - c)
    dual = sum(l * ((1 + tau) * kl(y, kappa) + tau * u * abs(y - m) + xi * (y - kappa)) for l, y, m in zip(lam, nu, mu)) - tau * C
    return primal, dual, nu


# ---------------------------------------------------------------------------------------------------------------
# independent inner solver (SLSQP on nu = mu + p - q)
# ---------------------------------------------------------------------------------------------------------------
def r_inner_slsqp(lam, mu, kappa, u, e):
    lam = np.asarray(lam)
    mu = np.asarray(mu)
    k = len(mu)
    B = (e + MI(lam, mu, kappa)) / u

    def klv(y):
        y = np.clip(y, 1e-300, 1 - 1e-16)
        return y * np.log(y / kappa) + (1 - y) * np.log((1 - y) / (1 - kappa))

    def obj(z):
        nu = mu + z[:k] - z[k:]
        return float(np.sum(lam * klv(nu)))

    cons = [{"type": "eq", "fun": lambda z: float(np.sum(lam * (z[:k] - z[k:])))},
            {"type": "ineq", "fun": lambda z: B - float(np.sum(lam * (z[:k] + z[k:])))}]
    bnds = [(0.0, max(1 - m - 1e-12, 0.0)) for m in mu] + [(0.0, max(m - 1e-12, 0.0)) for m in mu]
    best = math.inf
    for trial in range(6):
        z0 = np.zeros(2 * k) if trial == 0 else rng.uniform(0, 1, 2 * k) * np.array([b[1] for b in bnds]) * 0.3
        res = minimize(obj, z0, method="SLSQP", bounds=bnds, constraints=cons,
                       options={"maxiter": 500, "ftol": 1e-15})
        z = res.x
        if abs(cons[0]["fun"](z)) < 1e-9 and cons[1]["fun"](z) > -1e-9:
            best = min(best, obj(z))
    return best


# ---------------------------------------------------------------------------------------------------------------
# profiles
# ---------------------------------------------------------------------------------------------------------------
def profile_from_params(x, k, kappa):
    a = np.asarray(x[:k], float)
    a = a - a.max()
    lam = np.exp(a)
    lam = lam / lam.sum()
    b = np.asarray(x[k:], float)

    def typ(c):
        return sum(l * sig(bb + c) for l, bb in zip(lam, b)) - kappa

    lo, hi = -50.0, 50.0
    c = brentq(typ, lo - abs(b).max(), hi + abs(b).max(), xtol=1e-15)
    mu = [min(max(sig(bb + c), 1e-300), 1 - 1e-16) for bb in b]
    return list(lam), mu


def outer_search(k, kappa, u, which, val, n_starts, maxiter=600):
    """maximise the inner value over k-block profiles; returns (best primal, its dual, profile)"""
    inner = (lambda lam, mu: r_inner(lam, mu, kappa, u, val)) if which == "r" else (lambda lam, mu: n_inner(lam, mu, kappa, u, val))

    def neg(x):
        lam, mu = profile_from_params(x, k, kappa)
        p, d, _ = inner(lam, mu)
        if p == -math.inf:
            return 1e3
        return -p

    best = (-math.inf, -math.inf, None)
    for s in range(n_starts):
        x0 = np.concatenate([rng.normal(0, 1.0, k), rng.normal(0, 1.5, k)])
        res = minimize(neg, x0, method="Nelder-Mead", options={"maxiter": maxiter, "xatol": 1e-9, "fatol": 1e-13})
        lam, mu = profile_from_params(res.x, k, kappa)
        p, d, _ = inner(lam, mu)
        if p > best[0]:
            best = (p, d, (lam, mu))
    return best


def two_block_sup(kappa, u, which, val):
    if which == "r":
        if val >= 0:
            return best_centre(kappa, u, val, "V")[0]
        # negative accuracy: game form, sup over m (the game form is the claimed value for all real e)
        from scipy.optimize import minimize_scalar
        ms = np.linspace(0.005, 0.995, 199)
        vals = [Ray(float(m), kappa).V_game(val, u) for m in ms]
        i = int(np.argmax(vals))
        res = minimize_scalar(lambda m: -Ray(float(m), kappa).V_game(val, u), bounds=(ms[max(i - 1, 0)], ms[min(i + 1, 198)]),
                              method="bounded", options={"xatol": 1e-12})
        return max(vals[i], -res.fun)
    return best_centre(kappa, u, None, "N", X=val)[0]


def main(quick=False):
    t0 = time.time()
    ok = True
    # ---- (0) the two inner solvers agree; sandwich gaps ----
    max_gap = 0.0
    max_dis = 0.0
    n_s = 0
    for _ in range(40 if quick else 150):
        k = int(rng.integers(2, 6))
        kappa = float(rng.uniform(0.1, 0.9))
        u = float(rng.choice([0.5, 1.0, 2.0]))
        lam, mu = profile_from_params(np.concatenate([rng.normal(0, 1, k), rng.normal(0, 1.5, k)]), k, kappa)
        e = float(rng.uniform(-0.5, 1.0)) * MI(lam, mu, kappa) * rng.choice([0.0, 1.0, 0.3])
        p, d, nu = r_inner(lam, mu, kappa, u, e)
        if p == -math.inf:
            continue
        max_gap = max(max_gap, p - d)
        assert d <= p + 1e-12
        if nu is not None:
            assert abs(sum(l * y for l, y in zip(lam, nu)) - kappa) < 1e-12
            assert u * dist(lam, nu, mu) <= e + MI(lam, mu, kappa) + 1e-12
        ps = r_inner_slsqp(lam, mu, kappa, u, e)
        if math.isfinite(ps):
            max_dis = max(max_dis, abs(ps - p))
            n_s += 1
    print(f"[{'PASS' if max_gap < 1e-9 and max_dis < 2e-6 else 'FAIL'}] inner solver: duality gap (primal - dual) <= {max_gap:.2e}; "
          f"KKT solver vs independent SLSQP on {n_s} random profiles: <= {max_dis:.2e}")
    ok &= max_gap < 1e-9 and max_dis < 2e-6
    sys.stdout.flush()

    # ---- (1) outer searches ----
    configs = [(0.5, 1.0, "r", 0.0), (0.3, 1.0, "r", 0.0), (0.3, 1.0, "r", 0.01), (0.2, 2.0, "r", 0.02),
               (0.3, 1.0, "r", -0.03), (0.5, 1.0, "r", -0.05), (0.2, 2.0, "r", -0.1),
               (0.3, 1.0, "n", 0.0), (0.3, 1.0, "n", 0.02), (0.5, 1.0, "n", 0.05), (0.2, 2.0, "n", 0.05)]
    if quick:
        configs = configs[:2] + configs[4:5] + configs[7:8]
    n_starts = 4 if quick else 12
    print(f"{'kappa':>6} {'u':>4} {'fn':>3} {'acc':>7} {'2-block sup':>13} | " + " | ".join(f"k={k}: best primal (dual)      " for k in (3, 4, 5)))
    worst_excess = -math.inf
    for (kappa, u, which, val) in configs:
        ref = two_block_sup(kappa, u, which, val)
        cells = []
        for k in (3, 4, 5):
            p, d, prof = outer_search(k, kappa, u, which, val, n_starts)
            worst_excess = max(worst_excess, d - ref)
            cells.append(f"{p:.9f} ({d:.9f}) {'<=' if d <= ref + 1e-9 else '>!'}")
        print(f"{kappa:6.2f} {u:4.1f} {which:>3} {val:7.3f} {ref:13.9f} | " + " | ".join(cells))
        sys.stdout.flush()
    print(f"[{'PASS' if worst_excess <= 1e-8 else 'FAIL'}] 11.90(a): max over all searches of (certified lower value of a k-block profile "
          f"- two-block supremum) = {worst_excess:.3e}  (a positive value would refute (a))")
    ok &= worst_excess <= 1e-8
    print(f"elapsed {time.time() - t0:.0f} s")
    print("SUMMARY:", "ALL PASS" if ok else "FAILURES")


if __name__ == "__main__":
    main(quick=(len(sys.argv) > 1 and sys.argv[1] == "quick"))
