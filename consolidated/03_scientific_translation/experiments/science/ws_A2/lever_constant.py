#!/usr/bin/env python3
"""Workstream A2 — how large can 2 sqrt(2 I_red)/(b m^{3/2}) be for a tetrahedral chain?  (Theorem 11.36 quotes 0.824.)
Arms all-trans; the three torsions next to the central bond on each side are scanned on a 20-degree grid, which orients
the arms relative to the central axis.  I_A depends only on the torsions on side A and I_B only on those on side B, and
I_red is increasing in both, so the two sides are maximised separately.  Own code."""
import itertools
import numpy as np
from torsion_checks import chain, inertia_about_axis

grid = np.deg2rad(np.arange(-180, 180, 20))
for N in (43, 83, 163):
    n = N - 3
    i = n // 2
    m = min(i + 1, n - i)
    bestA = (0, None)
    bestB = (0, None)
    for t1, t2, t3 in itertools.product(grid, repeat=3):
        tors = np.full(n, np.pi)
        tors[i - 3], tors[i - 2], tors[i - 1] = t1, t2, t3
        tors[i + 1], tors[i + 2], tors[i + 3] = t3, t2, t1
        X = chain(N, tors)
        a0, a1 = X[i + 1], X[i + 2]
        ax = a1 - a0
        IA = inertia_about_axis(X[: i + 2], a0, ax)
        IB = inertia_about_axis(X[i + 2:], a0, ax)
        lab = tuple(int(round(np.rad2deg(t))) for t in (t1, t2, t3))
        if IA > bestA[0]:
            bestA = (IA, lab)
        if IB > bestB[0]:
            bestB = (IB, lab)
    IA, IB = bestA[0], bestB[0]
    r = 2 * np.sqrt(2 * IA * IB / (IA + IB)) / m ** 1.5
    print(f"N={N} m={m}: sup I_A/m^3 = {IA / m**3:.4f} at {bestA[1]}, sup I_B/m^3 = {IB / m**3:.4f} at {bestB[1]}; "
          f"2 sqrt(2 I_red)/m^1.5 = {r:.4f}", flush=True)
