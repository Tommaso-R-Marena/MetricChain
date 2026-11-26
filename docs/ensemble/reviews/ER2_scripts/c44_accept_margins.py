#!/usr/bin/env python3
"""ER2: at the moment the repository's is_face answers "face", how good is the certificate it holds?
Recorded in float64 for the last coupling matrix the script evaluated: the spread of the conformers' energies
(should be 0) and the gap between the lowest non-conformer and the highest conformer (must be > 0)."""
import sys, importlib.util
import numpy as np
import sys as _sys; _sys.dont_write_bytecode = True      # nothing is written next to the repository scripts
from er2_common import repo_root
REPO = repo_root()
spec = importlib.util.spec_from_file_location("ccp", REPO + "/experiments/ensemble/capacity_cutting_plane.py")
ccp = importlib.util.module_from_spec(spec); spec.loader.exec_module(ccp)
last = {}
_orig = ccp.energies
def _wrapped(Yall, Qm, *a, **k):
    last["Qm"] = Qm.copy()
    return _orig(Yall, Qm, *a, **k)
ccp.energies = _wrapped

n = int(sys.argv[1]); trials = int(sys.argv[2]); Ks = [int(k) for k in sys.argv[3:]]
rng = np.random.default_rng(4500 + n)
Yall = ccp.all_states(n); N = len(Yall); Yf = Yall.astype(float)
gaps = []; spreads = []; its = []
for K in Ks:
    for _ in range(trials):
        idx = rng.choice(N, size=K, replace=False)
        X = Yall[idx].astype(np.int64)
        last.clear()
        ans, it = ccp.is_face(X, Yall)
        if ans:
            E = 0.5 * np.einsum("ij,ij->i", Yf @ last["Qm"], Yf)
            mask = np.ones(N, dtype=bool); mask[idx] = False
            gaps.append(E[mask].min() - E[idx].max()); spreads.append(E[idx].max() - E[idx].min()); its.append(it)
gaps = np.array(gaps); spreads = np.array(spreads)
print(f"n = {n}: {len(gaps)} 'face' answers of the script (K in {Ks}, {trials} instances each)")
print(f"   float64 gap (lowest non-conformer) - (highest conformer) at acceptance: min {gaps.min():.3e}, 5% quantile {np.quantile(gaps, 0.05):.3e}, median {np.median(gaps):.3e}")
print(f"   spread of the conformers' energies at acceptance: max {spreads.max():.2e}")
print(f"   answers with a non-positive float64 gap: {int(np.sum(gaps <= 0))}")
