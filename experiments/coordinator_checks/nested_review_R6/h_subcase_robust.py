"""Harness remark of SCI-REV-0007, supplement: the proposed fixed sub-case for the Harper step -- outer landscape
'plateau of radius 4, then a cone of slope u' on Q_24, u = 1/2, lambda = 1/2, eta = 1/4, eta' = 1/2, theta = 2, b = 1/2,
nu_1 = 1 -- over 1000 seeds and the three inner behaviours of the harness: in how many runs does the Harper term decide
the closure, does condition [P] hold through Gamma'' only at a populated pass with r <= r_dagger, and is the
algorithm without the Harper term caught by the check of the closing radius?

Usage: python3 h_subcase_robust.py <falsify_conjectures.py> [seeds=1000]          (35 s)
"""
import sys, os, math, time
import numpy as np
import h_harper_usage as hh
from h_harper_usage import outfile

mod = hh.install(os.path.abspath(sys.argv[1]))
NSEEDS = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
n_o, u, d0 = 24, 0.5, 4
binom = [math.comb(n_o, j) for j in range(n_o + 1)]
f = u * np.maximum(np.arange(n_o + 1, dtype=float) - d0, 0.0)
vals, probs, lnw = np.exp(-f), np.array(binom, dtype=float) / 2 ** n_o, float(-f[0])
par = dict(lam=0.5, eta=0.25, etap=0.5, theta=2.0, b=0.5, delta=0.01, nu1=1.0)
lines = [f"fixed sub-case: plateau of radius {d0}, then a cone of slope u, n_o = {n_o}, n = {n_o + 2}, u = {u}, {par}; {NSEEDS} seeds per inner behaviour"]
print(lines[0])
ok = True
for mode in (0, 1, 2):
    hh.RUNS.clear()
    t0 = time.time()
    for seed in range(NSEEDS):
        mod.ba_two_level_plus(np.random.default_rng(50000 + seed), vals, probs, lnw, n_o, n_o + 2, u, par, mode, max_points=1_500_000)
    done = [r for r in hh.RUNS if r["error"] is None]
    dec, pg2, det = (sum(bool(r[k]) for r in done) for k in ("decisive", "P_by_Gamma2", "mutant_detected"))
    ok = ok and len(done) == NSEEDS == dec == pg2 == det
    lines.append(f"  inner behaviour {mode}: completed {len(done)}/{NSEEDS}; Harper term decides the closure in {dec}; "
                 f"[P] through Gamma'' only at a populated pass with r <= r_dagger in {pg2}; "
                 f"without the Harper term a level is left with r <= r_dagger (caught) in {det}   ({time.time() - t0:.0f} s)")
    print(lines[-1]); sys.stdout.flush()
lines.append(f"the sub-case exercises the Harper step in every run: {ok}")
print(lines[-1])
open(outfile("h_subcase_robust.txt"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if ok else 1)
