"""Follow-up to r3_R3_real_cube.py, test T2b: the one cell with |z| > 3 (radial dip on blocks (3,3,2), M = 1)
is re-run with 40 times more runs and three seeds, to separate a real bias from a heavy-tailed sample."""
import math
import sys
import numpy as np
from r3_R3_real_cube import Instance, R3, profiles

log = dict(T1_total=0, T1_two_values_fail=0, T1_cand_fail=0)
for seed in (1, 2, 3):
    rng = np.random.default_rng(seed)
    ns, u = (3, 3, 2), 1.0
    for name, F in profiles(ns, u, rng):
        if name not in ('radial-dip', 'flat+dip-at-rare-type', 'block2-only-deep-in-block1'):
            continue
        inst = Instance(ns, F, rng)
        for M in (1, 3):
            ests = np.array([R3(inst, M, rng, log)[0] for _ in range(20000)])
            sd = ests.std(ddof=1)
            z = (ests.mean() - inst.A) / (sd / math.sqrt(len(ests)))
            print('seed %d %-28s M=%d runs=%d A=%.6f mean=%.6f z=%+.2f' % (seed, name, M, len(ests), inst.A, ests.mean(), z), flush=True)
