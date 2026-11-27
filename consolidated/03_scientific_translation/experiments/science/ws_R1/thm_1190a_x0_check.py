#!/usr/bin/env python3
"""R1: the one flagged cell of thm_1190a_blocks.py (n at X = 0 exactly, kappa=.3, u=1: k-block value exceeds the
two-block supremum by 6e-9).  Hypothesis: artefact of the degenerate accuracy X = 0, where n(mu;0) jumps from MI(mu)
(self-consistent shells) to a smaller value and my solver decides self-consistency with a 1e-12 cut-off.
Test: (1) repeat at X = 1e-8, 1e-6, 1e-4 (non-degenerate); (2) at X = 0 evaluate the best 3-block profile found
with the exact self-consistency test replaced by the limit X -> 0+."""
import math, sys
import numpy as np
from thm_1190a_blocks import outer_search, two_block_sup, n_inner, MI
kappa, u = 0.3, 1.0
print(f"{'X':>8} {'two-block sup':>16} {'best 3-block (primal)':>22} {'dual':>14} {'excess of dual':>15}")
worst = -1.0
for X in (1e-4, 1e-6, 1e-8, 0.0):
    ref = two_block_sup(kappa, u, "n", X)
    p, d, prof = outer_search(3, kappa, u, "n", X, 6)
    print(f"{X:8.1e} {ref:16.12f} {p:22.12f} {d:14.12f} {d-ref:15.3e}")
    if X > 0:
        worst = max(worst, d - ref)
    else:
        lam, mu = prof
        print("   best 3-block profile at X=0: lam =", [f"{l:.6f}" for l in lam], " mu =", [f"{m:.6f}" for m in mu], f" MI(mu) = {MI(lam, mu, kappa):.12f}")
        for Xs in (1e-12, 1e-10, 1e-8):
            pp, dd, _ = n_inner(lam, mu, kappa, u, Xs)
            print(f"   same profile at X = {Xs:.0e}: n = {pp:.12f}   (two-block sup at that X: {two_block_sup(kappa, u, 'n', Xs):.12f})")
print("max excess at X > 0:", f"{worst:.3e}", "->", "PASS" if worst <= 1e-9 else "FAIL")
