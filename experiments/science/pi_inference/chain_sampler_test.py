#!/usr/bin/env python3
"""Unit test of the exact sampler and transfer matrix in beyond_enumeration_chain.py (class Chain): on random chain
models with n = 6 sites, alphabets of 2-3 letters and windows W = 1, 2, 3, 4, compare (i) ln Z with enumeration and
(ii) the empirical frequencies of 400 000 samples with the exact probabilities (total variation; a chi-square statistic
against its degrees of freedom)."""
import itertools, math, sys, os
import numpy as np
sys.argv = [sys.argv[0]]                       # the module reads sys.argv only under __main__
import importlib.util
spec = importlib.util.spec_from_file_location("bec", os.path.join(os.path.dirname(os.path.abspath(__file__)), "beyond_enumeration_chain.py"))
bec = importlib.util.module_from_spec(spec)
import types
sys.modules["fbmodel"] = types.SimpleNamespace(FBModel=None)   # the test does not need the molecular model
spec.loader.exec_module(bec)
rng = np.random.default_rng(12345)
ok = True
for W in (1, 2, 3, 4):
    for trial in range(3):
        n = 6; k = [int(rng.integers(2, 4)) for _ in range(n)]
        u = [rng.normal(0, 1.0, k[i]) for i in range(n)]
        v = {(i, j): rng.normal(0, 1.0, (k[i], k[j])) for i in range(n) for j in range(i + 1, min(n, i + W + 1))}
        ch = bec.Chain(0.7, u, v, W)
        lnZ = ch.solve()
        X = np.array(list(itertools.product(*[range(a) for a in k])))
        e = ch.energy(X); lnZ_enum = float(np.log(np.exp(-e).sum()))
        p = np.exp(-e - lnZ_enum)
        N = 400000
        x = ch.sample(N, rng)
        code = np.zeros(N, dtype=np.int64)
        for i in range(n): code = code * k[i] + x[:, i]
        cnt = np.bincount(code, minlength=len(X))
        tv = 0.5 * np.abs(cnt / N - p).sum()
        chi2 = float(((cnt - N * p) ** 2 / (N * p)).sum()); dof = len(X) - 1
        z = (chi2 - dof) / math.sqrt(2 * dof)
        good = abs(lnZ - lnZ_enum) < 1e-9 and abs(z) < 4.0
        ok &= good
        print(f"W={W} alphabets={k}: ln Z {lnZ:.9f} vs enumeration {lnZ_enum:.9f}; TV(empirical, exact) = {tv:.4f}; chi2 = {chi2:.0f} on {dof} dof (z = {z:+.2f})  {'ok' if good else 'FAIL'}")
print("ALL OK" if ok else "FAILURE")
