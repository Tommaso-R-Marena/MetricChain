"""Binomial and multinomial counts for samples of up to 2^61 points.

Why this module exists.  numpy's ``Generator.binomial(n, p)`` is not reliable for large ``n``:
from ``n`` of about 10^15 on, the mean and the variance of counts with mean between about 60 and
10^4 are wrong (mean -0.8 % at ``n = 2^61``, mean 92; variance -6 % at ``n = 2^53``).  The defect was
reported by the Scientific Discovery Division (SCI-REV-0007 §4) and is measured in this environment
by ``experiments/eng/twolevel/binomial_bias.py``.  The first version of the literal simulation
(experiment X-006) drew shell counts with that sampler from blocks of up to 5 10^17 points.

What replaces it.  ``binomial_exact`` draws Binomial(n, p)

* with numpy's sampler when ``n <= 2^31`` and ``min(p, 1-p) >= 1e-9`` (no defect was found there);
* otherwise by *Poissonisation*, which is exact: give every trial an independent Poisson(mu) number
  of events, ``mu = -ln(1 - p)``, so that a trial has at least one event with probability ``p``.  The
  total number of events is ``T ~ Poisson(n mu)`` and, given ``T``, the events fall on the trials
  independently and uniformly; the binomial count is the number of *distinct* trials hit.  That
  number is ``T`` minus the number of collisions, and the collisions are drawn by thinning: event
  ``t`` hits an occupied trial with probability ``D_{t-1}/n <= T/n`` (``D`` = occupied trials), so a
  Binomial(T, T/n) number of candidate events is placed uniformly among the ``T`` events and each is
  accepted with probability ``D_{t-1}/T``.  The cost is O(1 + T^2/n);
* with numpy's sampler again in the one regime where Poissonisation is too slow: ``n > 2^31`` and a
  mean above ``min(2^30, sqrt(1000 n))``.  There the count has a standard deviation above 1 200 (above
  30 000 when ``n >= 10^15``), numpy's defect touches a fraction of the draws of the order of one over
  the standard deviation and moves them within the bulk of the law; the relative effect on the count
  is below 10^-7.  Such counts enter the simulation only through sums that are compared at a
  relative tolerance ``eta``.  This branch is *not* exact and is named ``"bulk"`` in ``BRANCHES``.

Probabilities are passed as logarithms of ``p`` and of ``1 - p`` so that both tails keep their
relative precision.
"""
from __future__ import annotations

import math

import numpy as np

N_SAFE = 1 << 31            # numpy's sampler is used as it is up to this number of trials
P_SMALL = 1e-9              # ... and down to this success probability
LAM_MAX = float(1 << 30)    # largest Poisson mean drawn by Poissonisation
CAND_PER_TRIAL = 1000.0     # Poissonisation needs T^2/n candidates: allowed while lam^2 <= CAND_PER_TRIAL * n

BRANCHES = {"numpy": 0, "poisson": 0, "bulk": 0}     # how often each branch was taken (diagnostics only)


def _distinct(rng: np.random.Generator, T: int, n: int) -> int:
    """Number of distinct values among ``T`` independent uniform draws from ``n`` boxes (exact)."""
    if T <= 1:
        return T
    if 2 * T >= n:                                   # dense case, small n only: throw the balls literally
        return int(np.unique(rng.integers(0, n, size=T, dtype=np.int64)).size)
    pc = T / n
    nc = binomial_exact(rng, T, math.log(pc), math.log1p(-pc))
    if nc == 0:
        return T
    acc = 0
    for t0 in np.sort(rng.choice(T, size=nc, replace=False)):
        # candidate event number t0 + 1 (1-based); occupied boxes before it: t0 - acc
        if rng.random() * T < int(t0) - acc:
            acc += 1
    return T - acc


def branch(n: int, lp: float, lq: float) -> str:
    """Which branch ``binomial_exact`` takes for these arguments ("numpy", "poisson" or "bulk")."""
    p = math.exp(min(lp, lq))
    if n <= N_SAFE and p >= P_SMALL:
        return "numpy"
    lam = n * -math.log1p(-p)
    return "bulk" if (lam > LAM_MAX or lam * lam > CAND_PER_TRIAL * n) else "poisson"


def binomial_exact(rng: np.random.Generator, n: int, lp: float, lq: float) -> int:
    """Binomial(n, p) with ``lp = ln p`` and ``lq = ln(1 - p)``; see the module docstring."""
    n = int(n)
    if n <= 0 or lp == -math.inf:
        return 0
    if lq == -math.inf:
        return n
    if lp > lq:                                      # p > 1/2: count the failures
        return n - binomial_exact(rng, n, lq, lp)
    p = math.exp(lp)
    if n <= N_SAFE and p >= P_SMALL:
        BRANCHES["numpy"] += 1
        return int(rng.binomial(n, p))
    lam = n * -math.log1p(-p)                        # mean number of events
    if lam > LAM_MAX or lam * lam > CAND_PER_TRIAL * n:
        BRANCHES["bulk"] += 1
        return int(rng.binomial(n, p))
    BRANCHES["poisson"] += 1
    return _distinct(rng, int(rng.poisson(lam)), n)


def stable_multinomial(rng: np.random.Generator, size: int, lpmf: np.ndarray, sampler: str = "exact") -> np.ndarray:
    """Counts of ``size`` i.i.d. draws from the law with log-probabilities ``lpmf`` (int64).

    Sequential binomials with conditional probabilities p_j / (p_j + p_{j+1} + ...), the tail sums
    accumulated in the log domain from the far end, so that cells of mass 1e-18 are sampled
    correctly (numpy's ``multinomial`` loses them: K_REPORT §6.8, R8 ``r8_numpy_tail.py``).

    ``sampler="exact"`` draws each binomial with ``binomial_exact``; ``sampler="numpy"`` is the first
    version (numpy's binomial at every size), kept to reproduce the runs of job M-011."""
    ltail = np.logaddexp.accumulate(lpmf[::-1])[::-1]
    out = np.zeros(len(lpmf), dtype=np.int64)
    left = int(size)
    last = len(lpmf) - 1
    for j in range(len(lpmf)):
        if left == 0:
            break
        if j == last:
            out[j] = left
            break
        lp = min(0.0, float(lpmf[j] - ltail[j]))
        if sampler == "numpy":
            c = int(rng.binomial(left, math.exp(lp)))
        else:
            c = binomial_exact(rng, left, lp, float(ltail[j + 1] - ltail[j]))
        out[j] = c
        left -= c
    return out
