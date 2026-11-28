"""Referee A -- what if the same sample is used twice?  lr_confidence_region(batches=...) accepts any
list of index arrays; nothing checks that they are disjoint.  A natural mistake is to pass cumulative
prefixes ('the data so far') as rounds: batch b then contains samples on which its plug-in was fitted."""
import sys, warnings
import numpy as np
from scipy.special import logsumexp
sys.path.insert(0, "../src")
from d9mbar.certificates import lr_confidence_region
warnings.filterwarnings("ignore")


def run(mode, trials=1500, seed=11, K=3, overlap=0.3, per=12, rounds=8, alpha=0.05):
    r = np.random.default_rng(seed)
    P = np.full((K, K), overlap / (K - 1)); np.fill_diagonal(P, 1 - overlap)
    ftrue = np.array([0.0, 1.0, -0.5])
    Ut = -np.log(P).T + ftrue[None, :]
    miss = 0
    for tr in range(trials):
        comp = np.full(K, per // K)
        xs = np.concatenate([r.choice(K, size=comp[k] * rounds, p=P[k]) for k in range(K)])
        y = np.repeat(np.arange(K), comp * rounds)
        perm = np.concatenate([np.where(y == k)[0].reshape(rounds, -1) for k in range(K)], axis=1)   # rounds x per
        U = Ut[xs]
        if mode == "disjoint":
            batches = [perm[b] for b in range(rounds)]
        elif mode == "cumulative":
            batches = [perm[:b + 1].ravel() for b in range(rounds)]
        else:   # 'overlap1': each round re-uses the last round's samples as well
            batches = [perm[max(b - 1, 0):b + 1].ravel() for b in range(rounds)]
        reg = lr_confidence_region(U, y, alpha=alpha, batches=batches)
        if reg.status == "REJECT_MODEL":
            miss += 1
        elif reg.status == "OK":
            miss += int(float(np.sum(logsumexp(reg.A + ftrue, axis=1) - ftrue[reg.labels])) > reg.level)
    return miss / trials


for mode in ("disjoint", "overlap1", "cumulative"):
    print(f"batches = {mode:10s}: P(f* not in region) = {run(mode):.4f}   (nominal <= 0.05)")
