#!/usr/bin/env python3
"""Workstream I, experiment 5: the defect of the Chernoff potential in the growth recursion (uniform cube),
searched finely, including the corners: very small sets (d near n ln 2), very large sets (d near 0),
small radii t, and the edge Gamma = 0.  Prints n * sup defect by region.  Floating point exploration."""
import math, sys
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from i4_potential_defect import Gamma, LN2

def defect(n, d0, d1, t):
    g = lambda d, tt: Gamma(n, d, tt) if tt >= 0 else np.full(np.shape(d), np.inf)
    A0, A1 = g(d0, t), g(d1, t)
    B0, B1 = g(d0, t - 1), g(d1, t - 1)
    lhs = -np.log(0.5 * np.exp(-np.minimum(A0, B1)) + 0.5 * np.exp(-np.minimum(A1, B0)))
    d = -np.log(0.5 * np.exp(-d0) + 0.5 * np.exp(-d1))
    return lhs - Gamma(n + 1, d, t)

def region(n, name, dlo, dhi, ts, nd=600, spread=8.0, ns=161):
    best = (-1e9, None)
    for t in ts:
        dm = np.linspace(dlo, dhi, nd)[:, None]
        s = np.linspace(-spread, spread, ns)[None, :]
        d0 = np.clip(dm + s, 0, n * LN2); d1 = np.clip(dm - s, 0, n * LN2)
        df = defect(n, d0, d1, t)
        i = np.unravel_index(np.nanargmax(df), df.shape)
        if df[i] > best[0]:
            best = (float(df[i]), (t, float(d0[i]), float(d1[i])))
        # one fibre empty (d1 = inf): the set lives in one half
        dm1 = np.linspace(dlo, dhi, nd)
        A0 = Gamma(n, dm1, t); B0 = Gamma(n, dm1, t - 1) if t >= 1 else np.full(nd, np.inf)
        lhs = -np.log(0.5 * np.exp(-A0) + 0.5 * np.exp(-B0))
        df1 = lhs - Gamma(n + 1, dm1 + LN2, t)
        j = int(np.nanargmax(df1))
        if df1[j] > best[0]:
            best = (float(df1[j]), (t, float(dm1[j]), float('inf')))
    w, (t, d0, d1) = best
    print(f"  n={n:5d} {name:28s}: n*sup defect = {n*w:+8.3f}   at t={t}, d0={d0:.3f}, d1={d1:.3f}")
    return w

for n in (50, 200, 1000):
    top = n * LN2
    ts_small = [1, 2, 3, 5, 8]
    ts_mid = sorted(set(int(round(x * n)) for x in (0.02, 0.05, 0.1, 0.2, 0.3, 0.45)))
    region(n, "interior, mid radii", 0.05 * top, 0.95 * top, ts_mid)
    region(n, "interior, small radii", 0.05 * top, 0.95 * top, ts_small)
    region(n, "tiny sets (last 30 nats)", max(top - 30, 0), top, ts_small + ts_mid)
    region(n, "tiny sets (last 5 nats)", max(top - 5, 0), top, ts_small + ts_mid, spread=5.0)
    region(n, "large sets (d <= 3)", 0.0, 3.0, ts_small + ts_mid, spread=3.0)
