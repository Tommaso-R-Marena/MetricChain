#!/usr/bin/env python3
"""ER2: the rows n = 10, 12, 14 of the table of section 4.4 come from capacity_threshold.is_simplicial_face
(feasibility LP with unbounded couplings: 'face' iff status == 0).  Instance-wise comparison with my
max-margin LP (|Q_ij| <= 1, face iff t* > 1e-6) on the same instances."""
import importlib.util, sys
import numpy as np
import sys as _sys; _sys.dont_write_bytecode = True      # nothing is written next to the repository scripts
from er2_common import repo_root, face_maxmargin
REPO = repo_root()
from scipy.optimize import linprog
spec = importlib.util.spec_from_file_location("ct", REPO + "/experiments/ensemble/capacity_threshold.py")
ct = importlib.util.module_from_spec(spec); spec.loader.exec_module(ct)
my_face = face_maxmargin
tot = dis = 0
for n, trials, Ks in ((10, 60, (9, 10, 11, 12, 13)), (12, 25, (12, 13, 14, 15))):
    X = ct.cube_mod_flip(n); F = ct.pair_features(X); N = len(X); rng = np.random.default_rng(31 + n)
    for K in Ks:
        a = b = d = 0
        for _ in range(trials):
            idx = rng.choice(N, size=K, replace=False)
            ind, fc = ct.is_simplicial_face(F, idx); mine = my_face(F, idx)
            a += fc; b += mine; d += (bool(fc) != bool(mine))
        tot += trials; dis += d
        print(f"n = {n}, K = {K}: faces by capacity_threshold.is_simplicial_face {a}/{trials}, by my max-margin LP {b}/{trials}, disagreements {d}", flush=True)
print(f"total {tot} instances, disagreements {dis}")
