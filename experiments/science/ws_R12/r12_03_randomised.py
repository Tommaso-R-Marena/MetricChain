#!/usr/bin/env python3
"""R12 item 2, second script — Proposition 11.18e(b) and (c).

(b) as written: "For randomised algorithms without a hint the same count holds in the worst case,
    sup_g E|Q(g)| >= (1 - delta) N_ball - o(1)", the task being that of (a): "returns a finite
    lower bound for min(E0 + g) or a bracket of finite width for ln Z, valid for every g in G".

    COUNTER-ALGORITHM (R12).  g = h + R with h of order < m (the anchored interpolant) and
    |R| <= C (the order-m constants).  Draw q uniformly random configurations, M = max |g(x^j)|.
    If some sample has |h(x^j)| >= c ||h||_inf then ||g||_inf <= B := (M + C)/c + C, hence
    min E0 - B <= min(E0 + g)  and  |ln Z(E0 + g) - ln Z(E0)| <= B.
    Binary cube, order below m = 2 (affine functions): c = 1/(n+1) and at least HALF of the
    points are good, for every h (pairing argument, see NOTES.md) - so q = ceil(log2(1/delta))
    evaluations give a valid finite bound with probability >= 1 - delta on EVERY g, against
    N_ball = n + 1.
    Binary cube, order below m = d + 1: c = 0.6 / (N_ball (3n)^d) and at least a fraction 2^{-d}
    of the points are good (weighted-maximal Fourier coefficient, see NOTES.md).

    The script computes, for many functions h (random, multi-scale, with cancellations, and
    the result of a hill-climbing adversary), the EXACT fraction of bad points by enumerating
    the cube, hence the exact failure probability (fraction bad)^q, and checks the bound B on
    the remaining samples directly.

(c) hinted refutation of a wrong hint of order < m by N = ceil(k^{m-1} ln(1/delta)) uniform
    samples: exact miss probability for the worst difference (a cylinder) and a simulation.

One command:  python3 r12_03_randomised.py
"""
import itertools
import math
import time

import numpy as np

T0 = time.time()
rng = np.random.default_rng(2026112603)


def cube_pm(n):
    """All 2^n points as +-1 rows."""
    idx = np.arange(1 << n)
    return 1 - 2 * ((idx[:, None] >> np.arange(n)[None, :]) & 1)


def affine_values(alpha, beta, S):
    return alpha + S @ beta


def bad_fraction_affine(alpha, beta, S, C):
    """Exact fraction of points x whose single observation would give an INVALID bound,
    i.e. (n+1)(|g(x)| + C) + C < ||g||_inf, for g = h + R with the worst R allowed (|R| <= C):
    a point is certainly good if |h(x)| >= ||h||_inf/(n+1).  We count the points that are not
    certainly good: |h(x)| < ||h||_inf/(n+1)."""
    n = len(beta)
    h = affine_values(alpha, beta, S)
    H = np.max(np.abs(h))
    if H == 0:
        return 0.0, h
    return float(np.mean(np.abs(h) < H / (n + 1) * (1 - 1e-12))), h


def families(n):
    out = []
    for _ in range(300):
        out.append(("gaussian", rng.normal(), rng.normal(size=n)))
    for _ in range(300):
        sc = 10.0 ** rng.uniform(-6, 6, size=n)
        out.append(("multi-scale", rng.normal() * 10.0 ** rng.uniform(-6, 6), rng.normal(size=n) * sc))
    for _ in range(100):
        b = np.zeros(n)
        i = rng.integers(n)
        b[i] = rng.choice([-1, 1]) * 10.0 ** rng.uniform(0, 9)
        out.append(("one huge coefficient", rng.normal(), b))
    for _ in range(200):
        b = np.zeros(n)
        k = rng.integers(2, n + 1)
        idx = rng.choice(n, size=k, replace=False)
        vals = rng.choice([-1.0, 1.0], size=k)
        b[idx] = vals
        out.append(("+-1 on a subset (cancellations)", float(rng.integers(-k, k + 1)), b))
    for _ in range(100):
        out.append(("constant dominates", 10.0 ** rng.uniform(0, 6), rng.normal(size=n)))
    for t in range(1, n + 1):
        b = np.zeros(n)
        b[:t] = 1.0
        for a in range(-t, t + 1):
            out.append(("equal weights, alpha integer (many exact zeros)", float(a), b.copy()))
    return out


print("=" * 110)
print("PART 1 — binary cube, order below m = 2: a valid finite bound from q = ceil(log2(1/delta)) random evaluations")
print("=" * 110)
delta = 0.05
q = math.ceil(math.log2(1 / delta))
for n in (8, 12, 16):
    S = cube_pm(n).astype(float)
    worst = (0.0, None)
    count = 0
    for name, alpha, beta in families(n):
        fb, _ = bad_fraction_affine(alpha, beta, S, 0.0)
        count += 1
        if fb > worst[0]:
            worst = (fb, name)
    # hill-climbing adversary on (alpha, beta): maximise the bad fraction
    best_adv = 0.0
    for start in range(30):
        alpha = float(rng.integers(-3, 4))
        beta = rng.integers(-3, 4, size=n).astype(float)
        cur, _ = bad_fraction_affine(alpha, beta, S, 0.0)
        for it in range(400):
            a2, b2 = alpha, beta.copy()
            j = rng.integers(n + 1)
            step = float(rng.choice([-2, -1, 1, 2])) * rng.choice([1.0, 0.5, 0.1])
            if j == n:
                a2 += step
            else:
                b2[j] += step
            val, _ = bad_fraction_affine(a2, b2, S, 0.0)
            if val >= cur:
                alpha, beta, cur = a2, b2, val
        best_adv = max(best_adv, cur)
    N_ball = n + 1
    print("n = %2d: N_ball = %d, claimed lower bound (1 - delta) N_ball = %.2f; q = %d random evaluations."
          % (n, N_ball, (1 - delta) * N_ball, q))
    print("        %d test functions: largest exact fraction of bad points %.4f (family: %s); hill-climbing adversary: %.4f; "
          "theory: <= 0.5" % (count, worst[0], worst[1], best_adv))
    wf = max(worst[0], best_adv)
    print("        hence exact failure probability of the q-sample bound <= %.5f  (delta = %g)   %s" % (
        wf ** q, delta, "OK" if wf ** q <= delta else "FAIL"))

# end-to-end check of the bound B on one instance with a known part and a remainder
n = 12
S = cube_pm(n).astype(float)
E0 = rng.normal(size=1 << n) * 2.0
C = 0.7
fails = 0
trials = 20000
worst_slack = math.inf
checked_g = 0
for name, alpha, beta in families(n)[:400]:
    h = affine_values(alpha, beta, S)
    R = rng.uniform(-C, C, size=1 << n)
    g = h + R
    true_min = float(np.min(E0 + g))
    m0 = float(np.max(-(E0 + g)))
    lnZ = m0 + math.log(float(np.sum(np.exp(-(E0 + g) - m0))))
    m1 = float(np.max(-E0))
    lnZ0 = m1 + math.log(float(np.sum(np.exp(-E0 - m1))))
    idx = rng.integers(0, 1 << n, size=(trials // 400, q))
    M = np.max(np.abs(g[idx]), axis=1)
    B = (n + 1) * (M + C) + C
    L = float(np.min(E0)) - B
    ok = (L <= true_min + 1e-9) & (np.abs(lnZ - lnZ0) <= B + 1e-9)
    fails += int(np.sum(~ok))
    checked_g += 1
print("end-to-end (n = 12, C = 0.7, random known part): %d functions x %d sample sets of q = %d points; the output "
      "'min E0 - B' was an invalid lower bound or 'ln Z0 +- B' an invalid bracket in %d of %d runs (%.4f; allowed %.2f)"
      % (checked_g, trials // 400, q, fails, checked_g * (trials // 400), fails / (checked_g * (trials // 400)), delta))

print()
print("=" * 110)
print("PART 2 — binary cube, order below m = 3 and 4: fraction of points with |h(x)| >= c ||h||_inf, c = 0.6/(N_ball (3n)^d)")
print("=" * 110)


def walsh_basis(n, d):
    S = cube_pm(n).astype(float)
    cols = [np.ones(1 << n)]
    sets = [()]
    for size in range(1, d + 1):
        for U in itertools.combinations(range(n), size):
            cols.append(np.prod(S[:, U], axis=1))
            sets.append(U)
    return np.stack(cols, axis=1), sets


for n, d in ((10, 2), (10, 3), (12, 2)):
    W, sets = walsh_basis(n, d)
    N_ball = W.shape[1]
    c = 0.6 / (N_ball * (3 * n) ** d)
    rho = 2.0 ** (-d)
    worst_good = 1.0
    worst_name = None
    tests = 0
    for trial in range(400):
        kind = trial % 4
        if kind == 0:
            coef = rng.normal(size=N_ball)
        elif kind == 1:
            coef = rng.normal(size=N_ball) * 10.0 ** rng.uniform(-5, 5, size=N_ball)
        elif kind == 2:
            coef = np.zeros(N_ball)
            idx = rng.choice(N_ball, size=rng.integers(1, 6), replace=False)
            coef[idx] = rng.choice([-1.0, 1.0], size=len(idx))
        else:
            # a cylinder indicator on d random sites: the least-support function
            U = rng.choice(n, size=d, replace=False)
            S = cube_pm(n)
            hv = np.all(S[:, U] == 1, axis=1).astype(float)
            coef = np.linalg.lstsq(W, hv, rcond=None)[0]
        h = W @ coef
        H = np.max(np.abs(h))
        good = float(np.mean(np.abs(h) >= c * H))
        tests += 1
        if good < worst_good:
            worst_good, worst_name = good, ("gaussian", "multi-scale", "sparse +-1", "cylinder")[kind]
    qd = math.ceil(math.log(1 / delta) / -math.log(1 - rho))
    print("n = %d, d = %d: N_ball = %d, (1 - delta) N_ball = %.1f; c = %.3g; least fraction of good points over %d functions: "
          "%.4f (%s); theory >= 2^-d = %.4f; q = ceil(ln(1/delta)/-ln(1 - 2^-d)) = %d evaluations  %s" % (
              n, d, N_ball, (1 - delta) * N_ball, c, tests, worst_good, worst_name, rho, qd,
              "OK" if worst_good >= rho - 1e-12 else "FAIL"))

print()
print("=" * 110)
print("PART 3 — (c): a wrong hint of order below m is refuted by N = ceil(k^{m-1} ln(1/delta)) uniform evaluations")
print("=" * 110)
for k, m, n in ((2, 2, 10), (2, 3, 10), (3, 2, 6), (3, 3, 6), (4, 2, 5), (4, 3, 5)):
    N = math.ceil(k ** (m - 1) * math.log(1 / delta))
    rho = k ** (-(m - 1))
    exact_miss = (1 - rho) ** N
    # simulation with the worst difference: the indicator of a cylinder on m - 1 sites
    X = rng.integers(0, k, size=(200000, N, m - 1))
    hit = np.any(np.all(X == 0, axis=2), axis=1)
    n_ball = sum(math.comb(n, j) * (k - 1) ** j for j in range(m))
    print("k = %d, m = %d: N = %d (N_ball at n = %d sites: %d); exact miss probability for a cylinder (1 - k^-(m-1))^N = %.5f; "
          "simulated %.5f; <= delta: %s" % (k, m, N, n, n_ball, exact_miss, 1 - hit.mean(), exact_miss <= delta))
print()
print("total elapsed %.1f s" % (time.time() - T0))
print("R12_03_DONE")
