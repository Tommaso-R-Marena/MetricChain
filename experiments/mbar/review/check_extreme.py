"""Referee A -- LRRegion.interval on numerically extreme (but mathematically admissible) data."""
import sys, warnings, traceback
import numpy as np
sys.path.insert(0, "../src")
from d9mbar.certificates import lr_confidence_region
warnings.filterwarnings("ignore")
rng = np.random.default_rng(3)
for gap in (30.0, 200.0, 800.0, 2000.0):
    K, n = 3, 24
    y = np.repeat(np.arange(K), n)
    U = np.full((K * n, K), gap)
    U[np.arange(K * n), y] = 0.0
    U += rng.normal(scale=0.01, size=U.shape)          # all energies finite: support graph strongly connected
    perm = rng.permutation(K * n); U, y = U[perm], y[perm]
    try:
        reg = lr_confidence_region(U, y, alpha=0.05, n_batches=4)
        c = np.array([-1.0, 0.0, 1.0])
        out = reg.interval(c) if reg.status == "OK" else None
        # the true region contains every f with |f_i - f_j| <= gap - 5 (each sample keeps probability ~1)
        print(f"gap {gap}: status {reg.status}, interval {out}, level-phi_min = "
              f"{(reg.level - reg.phi_min) if reg.status == 'OK' else None}")
    except Exception as e:
        print(f"gap {gap}: EXCEPTION {type(e).__name__}: {e}")
