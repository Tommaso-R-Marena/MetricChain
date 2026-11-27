#!/usr/bin/env python3
"""Driver of the single-flip stability numbers for n = 40 and n = 60 quoted in §4.4
(docs/ensemble/ENSEMBLE_REPORT.md), using symmetric_stability.feasible.

This is the script that produced the block "symmetric stability, n = 40 (10 trials), 60 (6 trials)" of
output_threshold.txt (the internal review ER2 noted that it was not in the repository).
Usage: python3 symmetric_stability_large.py          (about half an hour)
Numerical evidence only [N].
"""
import pathlib, sys, time
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import symmetric_stability as ss

rng = np.random.default_rng(4242)
for n, trials in ((40, 10), (60, 6)):
    print(f"n = {n}", flush=True)
    for alpha in (1.3, 1.5, 1.6, 1.7, 1.8, 1.9):
        K = int(round(alpha * n)); f = 0; t0 = time.time()
        for _ in range(trials):
            X = rng.choice((-1, 1), size=(K, n))
            f += ss.feasible(X, False)
        print(f"   K/n = {alpha:4.2f}: P(strictly stable, symmetric Q) = {f / trials:4.2f}  ({time.time() - t0:.0f} s)", flush=True)
