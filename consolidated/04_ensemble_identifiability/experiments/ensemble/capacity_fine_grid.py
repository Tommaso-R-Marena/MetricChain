#!/usr/bin/env python3
"""Driver of the rows n = 10, 12, 14 of the table of §4.4 (docs/ensemble/ENSEMBLE_REPORT.md): face frequency of
K random conformers on a fine grid of K/n, by the full linear programme of capacity_threshold.py.

This is the script that produced the block "fine grid, full LP" of output_threshold.txt (the internal review
ER2 noted that it was described there in words only, and reproduced the n = 10 row from the description).
Usage: python3 capacity_fine_grid.py            (n = 16 takes long; it was stopped by hand for the stored block)
Numerical evidence only [N].
"""
import pathlib, sys, time
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import capacity_threshold as ct

rng = np.random.default_rng(777)
for n, trials in ((10, 400), (12, 300), (14, 120), (16, 40)):
    X = ct.cube_mod_flip(n); F = ct.pair_features(X); N = X.shape[0]
    print(f"n = {n}, trials = {trials}", flush=True)
    for K in sorted(set(int(round(a * n)) for a in (0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4))):
        t0 = time.time(); face = 0
        for _ in range(trials):
            idx = rng.choice(N, size=K, replace=False)
            face += ct.is_simplicial_face(F, idx)[1]
        print(f"   K = {K:3d}  K/n = {K/n:4.2f}  face frequency = {face/trials:5.3f}   ({time.time()-t0:.0f} s)", flush=True)
