#!/usr/bin/env python3
"""Identified against certified at degree 2, for pair data on small cubes (report §4.2, §4c.5).

For K random conformers on {-1,1}^n modulo the global flip, two exact decisions:
  face      : they are exactly the ground states of some pair energy and their pair features are affinely
              independent (a simplicial face of the cut polytope; linear programme over all 2^(n-1) states) —
              every ensemble on them is determined by its pair correlations (Theorem E1);
  degree 2  : the only sign vectors in their linear span are the conformers and their flips — equivalently
              (Theorem E10(a) and the Complexity division's Proposition 13, COMPLEXITY-RES-0008) some exposing
              pair energy has a sum-of-squares certificate of degree 2, namely the projection energy.
The difference "face and not degree 2" is the set of identified supports for which every exposing pair energy
needs a certificate of degree at least 4.

Usage: python3 degree2_vs_face.py [n trials ...]      default: 10 300 12 200
Numerical evidence only [N]; exact decisions, random supports (seed fixed).
"""
import sys, time
import numpy as np
from capacity_threshold import cube_mod_flip, pair_features, is_simplicial_face, psd_certificate


def main():
    args = [int(a) for a in sys.argv[1:]] or [10, 300, 12, 200]
    rng = np.random.default_rng(20261130)
    for n, trials in zip(args[0::2], args[1::2]):
        X = cube_mod_flip(n); F = pair_features(X); N = X.shape[0]
        print(f"n = {n}, {trials} random supports per K (distinct modulo the flip); columns: K, P(face), "
              f"P(degree-2 certificate), P(face without degree-2 certificate), P(degree-2 certificate but not a face)")
        for K in range(3, n):
            t0 = time.time(); face = deg2 = gap = bad = 0
            for _ in range(trials):
                idx = rng.choice(N, size=K, replace=False)
                _, fc = is_simplicial_face(F, idx)
                d2 = psd_certificate(X, idx)
                face += fc; deg2 += d2; gap += fc and not d2; bad += d2 and not fc
            print(f"   K = {K:3d}  K/n = {K / n:.2f}   {face / trials:.3f}   {deg2 / trials:.3f}   {gap / trials:.3f}   "
                  f"{bad / trials:.3f}   ({time.time() - t0:.0f} s)", flush=True)


if __name__ == "__main__":
    main()
