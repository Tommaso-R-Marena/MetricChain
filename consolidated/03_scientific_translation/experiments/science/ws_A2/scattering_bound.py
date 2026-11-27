#!/usr/bin/env python3
"""Workstream A2 — check of Proposition A2.1: the sorted-squared-distance transport distance bounds differences of
Debye scattering intensities.  For point sets x, y with N unit scatterers,
    I_x(q) = N + 2 sum_{p<q'} sinc(q r_pq'),   sinc(t) = sin(t)/t,
    |I_x(q) - I_y(q)| <= (q^2/3) * W(x,y),     W = sum_k |s^x_(k) - s^y_(k)|  (sorted squared distances, all pairs),
because d/ds sinc(q sqrt(s)) = (q^2/2) (t cos t - sin t)/t^3 has absolute value <= q^2/6.
Also: equal distance multisets (homometric sets) => identical I(q) for all q (checked on the 6-bead lattice pair)."""
import numpy as np

rng = np.random.default_rng(7)


def sqd(X):
    d = X[:, None, :] - X[None, :, :]
    s = (d ** 2).sum(-1)
    return np.sort(s[np.triu_indices(len(X), 1)])


def debye(s, q, n):
    t = q * np.sqrt(s)
    return n + 2 * np.sinc(t / np.pi).sum()   # np.sinc(x) = sin(pi x)/(pi x)


def random_chain(n):
    steps = rng.normal(size=(n - 1, 3))
    steps /= np.linalg.norm(steps, axis=1)[:, None]
    return np.vstack([np.zeros(3), np.cumsum(steps, 0)])


worst = 0.0
viol = 0
for _ in range(4000):
    n = rng.integers(4, 40)
    x, y = random_chain(n), random_chain(n)
    sx, sy = sqd(x), sqd(y)
    W = np.abs(sx - sy).sum()
    for q in (0.05, 0.2, 0.5, 1.0, 2.0, 5.0):
        lhs = abs(debye(sx, q, n) - debye(sy, q, n))
        rhs = q * q / 3 * W
        worst = max(worst, lhs / rhs)
        viol += lhs > rhs * (1 + 1e-12)
print(f"random freely jointed chains: violations {viol}; max |dI|/((q^2/3) W) = {worst:.4f}")

# sup of |(t cos t - sin t)/t^3|
t = np.linspace(1e-4, 60, 2_000_000)
print("sup_t |(t cos t - sin t)/t^3| =", np.abs((t * np.cos(t) - np.sin(t)) / t ** 3).max(), "(1/3 expected, at t -> 0)")

A = np.array([(0, 0), (0, 1), (0, 2), (1, 2), (1, 3), (2, 3)], float)
B = np.array([(0, 0), (0, 1), (1, 1), (1, 2), (1, 3), (2, 3)], float)
sa, sb = sqd(A), sqd(B)
print("6-bead homometric pair: sorted squared distances equal:", np.array_equal(sa, sb),
      "; max_q |I_A - I_B| on a grid:", max(abs(debye(sa, q, 6) - debye(sb, q, 6)) for q in np.linspace(0.01, 20, 500)))
