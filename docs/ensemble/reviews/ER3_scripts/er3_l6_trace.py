#!/usr/bin/env python3
"""ER3 review: which of the 46 pairs of the division's check L6 gives the quoted worst ratio 1.25, and how many
pairs L6 skips.  The division's module is imported read-only and run in the order of its main() (so that its random
stream is the one of the stored output); two_state_setup is wrapped to log the pairs."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "experiments", "ensemble")))
sys.dont_write_bytecode = True
import lifted_checks as L                                     # noqa: E402

log = []
orig = L.two_state_setup


def wrapped(r, shared):
    out = orig(r, shared)
    p, q, E, D, beta, cstar = out
    log.append((r, shared, len(D), float(beta.min()), float(beta.max()), float(cstar)))
    return out


L.two_state_setup = wrapped
for fn in (L.test_L1, L.test_L2, L.test_L3, L.test_L4, L.test_L5):
    fn()
ok, out = L.test_L6()
print(out[0].strip())
skipped = [x for x in log if x[3] < 0.05]
print(f"pairs generated: {len(log)}; skipped because some beta < 0.05: {len(skipped)}; tested: {len(log) - len(skipped)}")
print("pairs with shared angles and |D| >= 3, for which the best possible constant is 1 as soon as c_true^D >= 1,")
print("so that  f/(c* min d^2)  has infimum 1/c_D = 4/beta_min:")
for r, shared, nD, bmin, bmax, cs in sorted(log, key=lambda x: 1 / x[5] if (x[1] > 0 and x[2] >= 3) else 1e9)[:5]:
    if shared > 0 and nD >= 3:
        print(f"   r = {r}, shared = {shared}, |D| = {nD}, beta_min = {bmin:.3f}, c* = {cs:.3f}, 1/c* = {1 / cs:.3f}")
