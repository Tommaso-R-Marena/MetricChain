#!/usr/bin/env python3
"""ER2: the rows n = 10, 12 of the table of section 4.4.
(1) Independent replication with my own LP (max-margin form, float64, all states) on fresh instances.
(2) Attempt to reproduce the stored numbers with the driver that output_threshold.txt describes in words
    ("capacity_threshold.is_simplicial_face with numpy default_rng(777); n, trials = (10,400),(12,300),(14,120);
    K = round(a*n), a in 0.8..1.4") -- the driver itself is not in the repository, so its loop order is a guess.
"""
import sys, time, importlib.util
import numpy as np
import sys as _sys; _sys.dont_write_bytecode = True      # nothing is written next to the repository scripts
from er2_common import repo_root, face_maxmargin
REPO = repo_root()
from scipy.optimize import linprog

spec = importlib.util.spec_from_file_location("ct", REPO + "/experiments/ensemble/capacity_threshold.py")
ct = importlib.util.module_from_spec(spec); spec.loader.exec_module(ct)


my_face = face_maxmargin


stored = {10: {8: 0.875, 9: 0.787, 10: 0.613, 11: 0.383, 12: 0.253, 13: 0.072, 14: 0.022},
          12: {10: 0.890, 11: 0.773, 12: 0.677, 13: 0.537, 14: 0.323, 16: 0.060, 17: 0.020}}
for n, trials in ((10, 400), (12, 150)):
    X = ct.cube_mod_flip(n); F = ct.pair_features(X); N = len(X)
    rng = np.random.default_rng(9000 + n)
    print(f"n = {n}: my LP, {trials} fresh instances per K  (stored value in the repository output; binomial standard error of the difference)")
    for K, p0 in stored[n].items():
        f = sum(my_face(F, rng.choice(N, size=K, replace=False)) for _ in range(trials)) / trials
        n0 = 400 if n == 10 else 300
        se = np.sqrt(p0 * (1 - p0) / n0 + max(f * (1 - f), 1e-4) / trials)
        print(f"   K = {K:2d}: {f:.3f}   (stored {p0:.3f}; difference {f - p0:+.3f} = {(f - p0) / se:+.1f} s.e.)", flush=True)
# (2) guessed driver, n = 10 only
n, trials = 10, 400
X = ct.cube_mod_flip(n); F = ct.pair_features(X); N = len(X)
for label, order in (("K outer loop, alphas 0.8..1.4", "K"),):
    rng = np.random.default_rng(777); out = []
    for a in (0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4):
        K = int(round(a * n)); face = 0
        for _ in range(trials):
            idx = rng.choice(N, size=K, replace=False)
            ind, fc = ct.is_simplicial_face(F, idx); face += fc
        out.append(face / trials)
    print(f"guessed driver ({label}), n = 10: " + ", ".join(f"{v:.3f}" for v in out)
          + "   stored: 0.875, 0.787, 0.613, 0.383, 0.253, 0.072, 0.022")
