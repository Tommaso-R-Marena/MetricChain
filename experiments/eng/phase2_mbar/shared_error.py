#!/usr/bin/env python
"""Proposition M2 (docs/engineering/phase2/MBAR_INTEGRATION.md): an energy error shared by two states.

A  brute force on 10 points: every sign pattern of the error against the closed form and the bound.
B  a table on the model R10 of PREDICTIONS.md: exact range, bound, and the bound 2 eps that ignores sharing.
C  the composed statement from samples: bridge interval of the model's free-energy difference, widened by the
   bound with a certified upper bound of the total-variation distance; coverage with the error at its worst.

    PYTHONPATH=src python experiments/eng/phase2_mbar/shared_error.py
"""
from __future__ import annotations

import itertools
import json
import math
import os

import numpy as np

from metricchain_eng.certinf.multistate import (bridge_intervals, kl_bounds, shared_error_bound, shared_error_extremes,
                                                total_variation)

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20261128


def part_a(rng, cases=400, n=10):
    signs = np.array(list(itertools.product((-1.0, 1.0), repeat=n)))
    worst_formula = worst_interior = 0.0
    violations = 0
    tight = []
    for c in range(cases):
        conc = 10.0 ** rng.uniform(-1.0, 1.0)
        p_i, p_j = rng.dirichlet(np.full(n, conc)), rng.dirichlet(np.full(n, conc))
        if c % 5 == 0:                                   # some points outside the support of one state
            p_i[rng.integers(n)] = 0.0
            p_j[rng.integers(n)] = 0.0
            p_i, p_j = p_i / p_i.sum(), p_j / p_j.sum()
        tv = total_variation(p_i, p_j)
        for eps in (0.05, 0.3, 1.0, 2.0):
            w = np.exp(-eps * signs)                     # e^{-d} at the vertices of the box
            val = -np.log((w @ p_j) / (w @ p_i))
            lo, hi = shared_error_extremes(p_i, p_j, eps)
            worst_formula = max(worst_formula, abs(val.min() - lo), abs(val.max() - hi))
            d = rng.uniform(-eps, eps, size=(200, n))
            vi = -np.log((np.exp(-d) @ p_j) / (np.exp(-d) @ p_i))
            worst_interior = max(worst_interior, float(np.max(vi) - hi), float(lo - np.min(vi)))
            b = shared_error_bound(tv, eps)
            violations += int(max(hi, -lo) > b + 1e-12)
            tight.append(max(hi, -lo) / b if b > 0 else 1.0)
    return dict(cases=cases, points=n, eps=[0.05, 0.3, 1.0, 2.0], max_abs_difference_formula_vs_enumeration=worst_formula,
                max_excess_of_interior_errors=worst_interior, bound_violations=violations,
                exact_over_bound_min=float(np.min(tight)), exact_over_bound_median=float(np.median(tight)))


def model_r10():
    x = (np.arange(1000) + 0.5) / 1000
    V = 10.0 * ((x - 0.25) * (x - 0.75) / 0.0625) ** 2 + 2.0 * x
    lq = np.empty((1000, 7))
    lq[:, 0] = -V
    for j, c in enumerate((0.30, 0.35, 0.40, 0.44, 0.47, 0.50), 1):
        lq[:, j] = -V - 0.5 * 1500.0 * (x - c) ** 2
    P = np.exp(lq - lq.max(axis=0))
    P /= P.sum(axis=0)
    return x, lq, P


def part_b():
    _, _, P = model_r10()
    rows = []
    for i, j in ((1, 2), (1, 3), (1, 4), (0, 1), (0, 6), (5, 6)):
        tv = total_variation(P[:, i], P[:, j])
        for eps in (0.1, 0.5, 1.0):
            lo, hi = shared_error_extremes(P[:, i], P[:, j], eps)
            rows.append(dict(states=[i, j], tv=tv, eps=eps, exact_lo=lo, exact_hi=hi, bound=shared_error_bound(tv, eps),
                             unshared=2 * eps))
    return rows


def part_c(rng, reps=500, n=2000, eps=0.5, alpha=0.05):
    """States 1 and 2 of R10 are simulated; the truth carries the worst shared error (the one that raises f_2 - f_1 most)."""
    _, lq, P = model_r10()
    i, j = 1, 2
    p_i, p_j = P[:, i], P[:, j]
    lz = np.log(np.exp(lq - lq.max(axis=0)).sum(axis=0)) + lq.max(axis=0)
    df_model = -(lz[j] - lz[i])                                   # f_j - f_i of the simulated model
    ratio = p_j / p_i
    best, d_star = -math.inf, None
    for t in np.unique(ratio):                                    # f_j - f_i + (-ln R): largest when R is smallest
        d = np.where(ratio >= t, eps, -eps)                       # small weight e^{-d} where p_j/p_i is large
        v = -math.log((np.exp(-d) @ p_j) / (np.exp(-d) @ p_i))
        if v > best:
            best, d_star = v, d
    lo_x, hi_x = shared_error_extremes(p_i, p_j, eps)
    assert abs(best - hi_x) < 1e-10
    df_true = df_model + best
    tv = total_variation(p_i, p_j)
    a = np.array([0.0, df_model + 0.3])                           # an imperfect centre, fixed in advance
    miss = miss_naive = 0
    widths, widths_naive, tvs = [], [], []
    for _ in range(reps):
        xi, xj = rng.choice(1000, size=n, p=p_i), rng.choice(1000, size=n, p=p_j)
        logq = np.vstack([lq[xi][:, [i, j]], lq[xj][:, [i, j]]])
        lab = np.repeat([0, 1], n)
        blo, bhi = bridge_intervals(logq, lab, a, alpha / 2)
        l, u = blo[0, 1], bhi[0, 1]
        # 1 - TV = E_i min(1, e^{f_j - f_i} q_j/q_i) is non-decreasing in f_j - f_i: use its certified lower end
        y = float(np.mean(np.minimum(1.0, np.exp(l + lq[xi, j] - lq[xi, i]))))
        tv_up = 1.0 - kl_bounds(y, n, math.log(2.0 / (alpha / 2)))[0]
        b = shared_error_bound(tv_up, eps)
        miss += int(not (l - b <= df_true <= u + b))
        miss_naive += int(not (l - 2 * eps <= df_true <= u + 2 * eps))
        widths.append(u - l + 2 * b)
        widths_naive.append(u - l + 4 * eps)
        tvs.append(tv_up)
    return dict(reps=reps, draws_per_state=n, eps=eps, level=alpha, tv=tv, exact_change=[lo_x, hi_x],
                true_minus_model=best, misses=miss, misses_unshared_rule=miss_naive,
                median_width=float(np.median(widths)), median_width_unshared_rule=float(np.median(widths_naive)),
                median_bridge_width=float(np.median(np.array(widths_naive) - 4 * eps)), median_tv_upper=float(np.median(tvs)))


def main():
    rng = np.random.default_rng(SEED)
    out = dict(seed=SEED, A=part_a(rng), B=part_b(), C=part_c(rng))
    with open(os.path.join(HERE, "results", "shared_error.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("A", json.dumps(out["A"]))
    print("B  states   TV     eps   exact range of the change        bound    2 eps")
    for r in out["B"]:
        print(f"   {r['states']}  {r['tv']:.3f}  {r['eps']:.1f}   [{r['exact_lo']:+.4f}, {r['exact_hi']:+.4f}]   {r['bound']:.4f}   {r['unshared']:.1f}")
    print("C", json.dumps(out["C"]))


if __name__ == "__main__":
    main()
