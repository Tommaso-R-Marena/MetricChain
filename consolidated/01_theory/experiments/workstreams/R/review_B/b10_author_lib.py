"""Referee B, check 10: the author's library rlib.py against my definitions (blib.py), at random regular points.
rlib computes Sigma through J; blib computes it from theta (definition).  Also the kinked pair."""
import sys, math, random
sys.dont_write_bytecode = True          # do not leave a __pycache__ in the author's directory
sys.path.insert(0, "..")
import rlib
import blib

rng = random.Random(7)
for A, Bp in [(rlib.Gauss().setup(), blib.gauss()), (rlib.Cube(1.0).setup(), blib.cube(1.0)), (rlib.Cube(2.0).setup(), blib.cube(2.0)),
              (rlib.Kinked(), blib.kink_author())]:
    worst = 0.0
    for _ in range(400):
        s = rng.uniform(0, 0.95)
        B = rng.uniform(0.0, 0.97) * (1 - s) * A.a
        v1, v2 = A.sigma(B, s), Bp.sigma_direct(B, s)
        worst = max(worst, abs(v1 - v2) / max(1.0, abs(v2)))
    # theta_na of the author against mine
    wt = max(abs(A.theta_na(e) - Bp.theta(e)) for e in [1e-6, 1e-3, 0.02, 0.1, 0.3, 0.6])
    print("%-22s max relative |Sigma_rlib - Sigma_definition| over 400 points: %.2e;   max |theta_rlib - theta_mine| at 6 points: %.1e" % (A.name, worst, wt))
