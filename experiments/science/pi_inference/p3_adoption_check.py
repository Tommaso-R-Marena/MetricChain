#!/usr/bin/env python3
"""Coordinator's own check of the combinatorial statements of workstream P3 that the division publishes.

Written independently of experiments/science/ws_P3 (nothing imported from it).

 (1) Proposition 1 (remainder identity of the anchored expansion): for every g on a finite product,
     every anchor x0, every x and every m >= 1, with the sites ordered,
         g(x) - I_{m-1} g(x) = sum over T subset S(x), |T| = m, of  Delta_T g(z^{T,x}; x_T),
     z^{T,x}_i = x_i for i < min T and x0_i otherwise;  S(x) = {i : x_i != x0_i};
     I_M g(x) = sum over U subset S(x), |U| <= M, of d_U(x_U),  d_U(x_U) = Delta_U g(x0; x_U).
 (2) The allocation lemma at order m: for non-negative c_T (|T| = m) and gamma_i = (1/m) sum_{T contains i} c_T,
         sum_{T subset S, |T| = m} c_T  <=  sum_{i in S} gamma_i     for every S.
 (3) Lemma R (sample-range bound): for i.i.d. W in [w_min, 1] with mean mu, eps_N = 1 - (delta/2)^(1/N),
         min_N - (min_N - w_min) eps_N  <=  mu  <=  max_N + (1 - max_N) eps_N    with probability >= 1 - delta.
     Coverage by simulation on four laws, two of them adversarial (a rare atom at an end point).
 (4) Lemma 2, Corollary L1 (one inner function additive in the sites of T):
         |Delta_T phi(u)| <= sup |phi^(|T|)| * prod_i |a_i(y_i) - a_i(z_i)|      (phi = tanh, exp; orders 1..4).

Run:  python3 p3_adoption_check.py > p3_adoption_check.log      (a few seconds)
"""
import itertools
import math

import numpy as np

rng = np.random.default_rng(20261126)


def mixed_difference(g, base, T, yT):
    """Delta_T g(base; y_T) = sum_{U subset T} (-1)^{|T|-|U|} g(y_U, base_{-U})."""
    T = list(T)
    tot = 0.0
    for r in range(len(T) + 1):
        for U in itertools.combinations(range(len(T)), r):
            x = list(base)
            for j in U:
                x[T[j]] = yT[j]
            tot += (-1) ** (len(T) - r) * g[tuple(x)]
    return tot


print("# (1) remainder identity of the anchored expansion")
worst = 0.0
cases = 0
for trial in range(40):
    n = int(rng.integers(2, 7))
    shape = tuple(int(rng.integers(2, 5)) for _ in range(n))
    g = rng.standard_normal(shape) * float(rng.choice([0.1, 1.0, 10.0]))
    x0 = tuple(int(rng.integers(0, k)) for k in shape)
    for _ in range(12):
        x = tuple(int(rng.integers(0, k)) for k in shape)
        S = [i for i in range(n) if x[i] != x0[i]]
        for m in range(1, n + 2):
            interp = 0.0
            for r in range(0, min(m - 1, len(S)) + 1):
                for U in itertools.combinations(S, r):
                    interp += mixed_difference(g, x0, U, [x[i] for i in U])
            lhs = g[x] - interp
            rhs = 0.0
            for T in itertools.combinations(S, m):
                z = list(x0)
                for i in range(min(T)):
                    z[i] = x[i]
                rhs += mixed_difference(g, z, T, [x[i] for i in T])
            worst = max(worst, abs(lhs - rhs) / (1.0 + abs(g).max()))
            cases += 1
print(f"   {cases} cases (40 random functions on random product grids with 2-6 sites and 2-4 states, 12 points each, every order m): largest |lhs - rhs| / (1 + max|g|) = {worst:.2e}")
assert worst < 1e-12

print("# (2) allocation lemma at order m")
worst = -1.0
cases = 0
for trial in range(300):
    n = int(rng.integers(3, 9))
    m = int(rng.integers(2, min(n, 5) + 1))
    c = {T: float(rng.exponential()) * float(rng.choice([0.0, 1.0, 1.0])) for T in itertools.combinations(range(n), m)}
    gamma = [sum(v for T, v in c.items() if i in T) / m for i in range(n)]
    for r in range(n + 1):
        for S in itertools.combinations(range(n), r):
            lhs = sum(v for T, v in c.items() if set(T) <= set(S))
            rhs = sum(gamma[i] for i in S)
            worst = max(worst, lhs - rhs)
            cases += 1
print(f"   {cases} pairs (constants, S): largest (sum over T inside S of c_T) - (sum of gamma_i over S) = {worst:.2e}  (must be <= 0 up to rounding)")
assert worst < 1e-9

print("# (3) Lemma R: coverage of the sample-range bracket")
delta = 0.05
for name, sampler, mu, wmin in [
    ("uniform on [0.2, 1]", lambda N: rng.uniform(0.2, 1.0, N), 0.6, 0.2),
    ("nearly constant 0.97 with a 1 % atom at 1", lambda N: np.where(rng.random(N) < 0.01, 1.0, 0.97), 0.97 + 0.01 * 0.03, 0.5),
    ("0.9 with an atom of mass 3/N at w_min = 0.1 (adversarial for the lower side)", None, None, 0.1),
    ("0.3 with an atom of mass 3/N at 1 (adversarial for the upper side)", None, None, 0.05),
]:
    for N in (50, 500, 5000):
        if sampler is None:
            q = 3.0 / N
            if "lower" in name:
                samp = lambda NN, q=q: np.where(rng.random(NN) < q, 0.1, 0.9)
                m_true = 0.9 - q * 0.8
            else:
                samp = lambda NN, q=q: np.where(rng.random(NN) < q, 1.0, 0.3)
                m_true = 0.3 + q * 0.7
        else:
            samp, m_true = sampler, mu
        eps = 1.0 - (delta / 2.0) ** (1.0 / N)
        reps = 4000
        miss = 0
        for _ in range(reps):
            w = samp(N)
            lo = w.min() - (w.min() - wmin) * eps
            hi = w.max() + (1.0 - w.max()) * eps
            if not (lo <= m_true <= hi):
                miss += 1
        print(f"   {name}, N = {N}: miss rate {miss/reps:.4f}  (must be <= {delta} up to the simulation error {1.96*math.sqrt(delta*(1-delta)/reps):.4f})")
        assert miss / reps <= delta + 3 * math.sqrt(delta * (1 - delta) / reps)

print("# (4) Corollary L1: mixed differences of phi(c + sum_i a_i(x_i))")
worst = -1e9
cases = 0
for trial in range(3000):
    order = int(rng.integers(1, 5))
    c = float(rng.normal())
    a_z = rng.normal(size=order) * 0.5
    a_y = a_z + rng.normal(size=order) * float(rng.choice([0.01, 0.2, 1.0]))
    for phi, dsup in (("tanh", None), ("exp", None)):
        # u ranges over [c + sum min, c + sum max]
        lo = c + np.minimum(a_z, a_y).sum()
        hi = c + np.maximum(a_z, a_y).sum()
        grid = np.linspace(lo, hi, 2001)
        if phi == "exp":
            f = math.exp
            sup = math.exp(hi)
        else:
            f = math.tanh
            # derivatives of tanh up to order 4 as polynomials in t = tanh(u)
            t = np.tanh(grid)
            d = [1 - t**2, -2 * t * (1 - t**2), -2 * (1 - t**2) * (1 - 3 * t**2), 8 * t * (1 - t**2) * (2 - 3 * t**2)][order - 1]
            sup = float(np.abs(d).max()) * (1 + 1e-6) + 1e-9      # grid maximum with a small allowance
        tot = 0.0
        for r in range(order + 1):
            for U in itertools.combinations(range(order), r):
                u = c + sum(a_y[i] if i in U else a_z[i] for i in range(order))
                tot += (-1) ** (order - r) * f(u)
        bound = sup * float(np.prod(np.abs(a_y - a_z)))
        worst = max(worst, abs(tot) - bound)
        cases += 1
print(f"   {cases} cases (tanh and exp, orders 1-4): largest |Delta| - bound = {worst:.2e}  (must be <= 0 up to the grid allowance)")
assert worst <= 1e-9
print("ALL OK")
