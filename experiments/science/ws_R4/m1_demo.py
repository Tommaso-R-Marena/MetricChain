#!/usr/bin/env python3
"""R4 -- finding m1 made concrete: without the stopping rule, Claim B of Theorem 11.84
("|C_l| <= N_l in every run") fails in runs where inner brackets are wider than promised.

A bracket procedure may return a bracket wider than e^{x} with probability delta' (e.g. its own
trivial bracket after an abort).  Here ALL rung-1 calls return the trivial bracket of the fibre
(valid, ratio e^{2 u n_i} instead of e^{x_1}); the candidate set C_2 is then computed exactly as
in Theorem 11.84 (my batched_sim.Run.batched) and compared with N_2.
"""
import numpy as np
from batched_sim import Run

rng = np.random.default_rng(5)
print("# n_o n_i  x_1   kind      M_max     |C_2| honest   |C_2| with wide rung-1 brackets    N_2     violated")
for (n_o, n_i, x1, kind) in [(10, 4, 1.0, "flat"), (11, 4, 1.5, "cone"), (10, 5, 0.8, "flathist"),
                              (11, 3, 2.0, "walk"), (10, 6, 1.2, "dip")]:
    R = Run(1.0, n_o, n_i, 1.0, 0.5, 100.0, 3.0, 1.0, [x1, 0.5 * x1], 6, kind, "uniform", 0.05, rng)
    assert R.ok
    C_honest = R.batched()
    honest = int(C_honest[2].sum())
    orig = R.inner

    def wide(idx, l, orig=orig, R=R):
        if l == 1:
            return R.L0[idx], R.U0[idx]          # the trivial bracket: valid, but ratio e^{2 u n_i}
        return orig(idx, l)

    R.inner = wide
    C_wide = R.batched()
    wide_n = int(C_wide[2].sum())
    N2 = R.N_bound(2)
    print(f"  {n_o}  {n_i}   {x1:.1f}  {kind:8s} {R.M_max:8d}  {honest:10d}   {wide_n:12d}                 {int(N2):8d}   {wide_n > N2}")
