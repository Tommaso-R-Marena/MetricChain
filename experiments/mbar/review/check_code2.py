"""Referee A -- further tests of the CODE: classifier_evalue (is the statistic <= the e-value at the
truth?), observable_interval (coverage; union bound; division by s_k), kl_interval (exact binomial
check of the claimed failure probability 2 exp(-t)).
"""
import sys, warnings
import numpy as np
from scipy.special import logsumexp
from scipy.stats import binom

sys.path.insert(0, "../src")
from d9mbar.certificates import (classifier_evalue, make_batches, lr_confidence_region,     # noqa: E402
                                 observable_interval, kl_interval)

warnings.filterwarnings("ignore")
rng = np.random.default_rng(1618)

# ------------------------------------------------------------------ kl_interval: exact check
print("== kl_interval: exact failure probability for Bernoulli samples vs 2 exp(-t)")
worst = 0.0
for n in (5, 20, 80):
    for mu in (0.01, 0.1, 0.5, 0.93):
        for t in (0.5, 2.0, 4.0):
            fail = 0.0
            for k in range(n + 1):
                lo, hi = kl_interval(k / n, n, t)
                if not (lo <= mu <= hi):
                    fail += binom.pmf(k, n, mu)
            worst = max(worst, fail / (2 * np.exp(-t)))
print(f"  max over (n, mu, t) of P(mu not in interval) / (2 e^-t) = {worst:.4f}  (claim <= 1)")

# ------------------------------------------------------------------ classifier_evalue
print("== classifier_evalue: statistic vs log prod lambda/pi(f*) computed from the definition")
K, J = 3, 5
worst_gap, rej, nconv = -np.inf, 0, 0
trials = 400
for tr in range(trials):
    P = rng.dirichlet(np.ones(J), size=K)
    ftrue = rng.normal(size=K)
    n = rng.integers(30, 60, K)
    xs = np.concatenate([rng.choice(J, size=n[k], p=P[k]) for k in range(K)])
    y = np.repeat(np.arange(K), n)
    perm = rng.permutation(len(y)); xs, y = xs[perm], y[perm]
    U = -np.log(P[:, xs].T) + ftrue[None, :]

    def prob(b, prev, cur):
        # frequency classifier trained on earlier batches (uses the raw point, not the energies)
        cnt = np.ones((J, K)) * 0.5
        np.add.at(cnt, (xs[prev], y[prev]), 1.0)
        return (cnt / cnt.sum(axis=1, keepdims=True))[xs[cur]]
    logE, info = classifier_evalue(U, y, prob, n_batches=6)
    nconv += int(not info["converged"])
    # the same statistic at the true f, from the definition
    batches = make_batches(y, 6)
    tot = 0.0
    for b in range(1, 6):
        cur, prev = batches[b], np.concatenate(batches[:b])
        nb = np.bincount(y[cur], minlength=K); beta = nb / nb.sum()
        lam = prob(b, prev, cur)
        Z = np.log(beta)[None, :] + ftrue[None, :] - U[cur]
        logpi = Z - logsumexp(Z, axis=1)[:, None]
        idx = np.arange(len(cur))
        tot += float(np.sum(np.log(lam[idx, y[cur]]) - logpi[idx, y[cur]]))
    worst_gap = max(worst_gap, logE - tot)
    rej += int(logE >= np.log(20))
print(f"  max of (code statistic - value at the truth) = {worst_gap:.3e} (claim <= 0); "
      f"rejections at alpha=0.05: {rej}/{trials}; unconverged fits: {nconv}")

# ------------------------------------------------------------------ observable_interval
print("== observable_interval: coverage of E_k[A] (alpha = 0.05, alpha_obs = 0.025)")
miss, nontriv, widths = 0, 0, []
trials = 150
for tr in range(trials):
    K, J = 3, 6
    P = rng.dirichlet(np.ones(J) * 2, size=K)
    ftrue = rng.normal(size=K)
    n = np.array([int(v) for v in rng.integers(150, 400, K)])
    xs = np.concatenate([rng.choice(J, size=n[k], p=P[k]) for k in range(K)])
    y = np.repeat(np.arange(K), n)
    perm = rng.permutation(len(y)); xs, y = xs[perm], y[perm]
    U = -np.log(P[:, xs].T) + ftrue[None, :]
    Aobs = rng.random(J)
    k = int(rng.integers(K))
    reg = lr_confidence_region(U, y, alpha=0.05)
    lo, hi = observable_interval(reg, U, y, k, Aobs[xs], alpha_obs=0.025)
    truth = P[k] @ Aobs
    miss += int(not (lo <= truth <= hi))
    nontriv += int(hi - lo < 1)
    widths.append(hi - lo)
print(f"  misses {miss}/{trials} (claim: probability <= 0.075); nontrivial intervals {nontriv}; median width {np.median(widths):.3f}")
