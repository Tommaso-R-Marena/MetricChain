"""Workstream K -- multinomial sampling that stays accurate for sample sizes up to 2^62 and cell probabilities down to
10^-300 (needed by sim_grouped.py).

numpy's Generator.multinomial conditions sequentially on `remaining_p = 1 - p_1 - ... - p_j`, which is rounding noise
once the remaining mass is below ~1e-14: for n ~ 2^60 the far-tail cells -- exactly the rare high levels the outer loop
is about -- then get wrong counts (checked in `selftest`: cells of total mass 1e-16 receive 0 points instead of ~50).
numpy's binomial is also wrong for p < 1e-16 with n p of order one (its inversion branch computes q = 1 - p = 1).

Here: binary splitting over the cells sorted by probability.  Every conditional probability is a ratio of sums of
positive terms (relative accuracy ~1e-15), always <= 1/2; a node with n p <= 30 and p < 1e-6 is sampled by inversion
with log1p (exact up to rounding), every other node by numpy's binomial (its inversion branch with p >= 1e-6, or BTPE).
"""
import math
import numpy as np


def _binomial_small(rng, n, p, kmax=400):
    """Bin(n, p) by inversion for arrays with n p <= 30 (p tiny); P(X = 0) = exp(n log1p(-p))."""
    n = n.astype(np.float64)
    u = rng.uniform(size=len(n))
    k = np.zeros(len(n), dtype=np.int64)
    pk = np.exp(n * np.log1p(-p))
    cdf = pk.copy()
    ratio = p / (1.0 - p)
    active = u > cdf
    while active.any() and int(k.max()) < kmax:
        idx = np.nonzero(active)[0]
        k[idx] += 1
        pk[idx] *= (n[idx] - k[idx] + 1) / k[idx] * ratio[idx]
        cdf[idx] += pk[idx]
        active[idx] = (u[idx] > cdf[idx]) & (pk[idx] > 0)
    return k


class StableMultinomial:
    def __init__(self, probs):
        probs = np.asarray(probs, dtype=np.float64)
        S = len(probs)
        self.order = np.argsort(probs, kind="stable")              # ascending
        size = 1
        while size < S:
            size *= 2
        leaf = np.zeros(size)
        leaf[size - S:] = probs[self.order]
        self.S, self.size = S, size
        self.levels = [leaf]                                        # levels[0] = leaves ... levels[-1] = root
        while len(self.levels[-1]) > 1:
            a = self.levels[-1]
            self.levels.append(a[0::2] + a[1::2])

    def sample(self, rng, n):
        cnt = np.array([int(n)], dtype=np.int64)
        for lev in range(len(self.levels) - 2, -1, -1):
            mass = self.levels[lev]
            left, right = mass[0::2], mass[1::2]
            tot = left + right
            pl = np.where(tot > 0, left / np.where(tot > 0, tot, 1.0), 0.0)        # <= 1/2 (cells sorted ascending)
            cl = np.zeros(len(cnt), dtype=np.int64)
            live = (cnt > 0) & (pl > 0)
            small = live & (pl < 1e-6) & (cnt.astype(np.float64) * pl <= 30.0)
            big = live & ~small
            if small.any():
                cl[small] = _binomial_small(rng, cnt[small], pl[small])
            if big.any():
                cl[big] = rng.binomial(cnt[big], pl[big])
            cl = np.minimum(cl, cnt)
            new = np.empty(2 * len(cnt), dtype=np.int64)
            new[0::2] = cl
            new[1::2] = cnt - cl
            cnt = new
        out = np.zeros(self.S, dtype=np.int64)
        out[self.order] = cnt[self.size - self.S:]
        return out


def selftest(verbose=True):
    """(1) small n: chi-square against the exact multinomial law; (2) n = 2^59, radial law of Q_200: mean and variance of
    far-tail counts (tail mass 1e-17 ... 1e-12) for this sampler and for numpy's multinomial."""
    rng = np.random.default_rng(5)
    ok = True
    # (1)
    p = np.array([0.5, 0.2, 0.2, 0.07, 0.02, 0.01])
    sm = StableMultinomial(p)
    reps, n = 40000, 50
    tot = np.zeros(len(p))
    sq = np.zeros(len(p))
    for _ in range(reps):
        c = sm.sample(rng, n)
        assert c.sum() == n
        tot += c; sq += c.astype(float) ** 2
    mean = tot / reps
    var = sq / reps - mean ** 2
    z = (mean - n * p) / np.sqrt(n * p * (1 - p) / reps)
    okm = bool(np.all(np.abs(z) < 4.5)) and bool(np.all(np.abs(var / (n * p * (1 - p)) - 1) < 0.05))
    ok = ok and okm
    if verbose:
        print(f"  small case: z-scores of the cell means {np.round(z, 2)}, variance ratios {np.round(var / (n * p * (1 - p)), 3)}: {okm}")
    # (2)
    n_o = 200
    probs = np.array([math.comb(n_o, k) for k in range(n_o + 1)], dtype=float) / 2.0 ** n_o
    pc = probs[np.arange(n_o, -1, -1)]                   # ascending W for a cone: rare small-d shells at the end
    tail = np.cumsum(pc[::-1])[::-1]
    sm = StableMultinomial(pc)
    size = 2 ** 59
    reps = 300
    for target in (1e-17, 1e-16, 1e-15, 1e-14, 1e-13, 1e-12):
        i = int(np.searchsorted(-tail, -target))
        mu = size * tail[i]
        a = np.array([float(sm.sample(rng, size)[i:].sum()) for _ in range(reps)])
        b = np.array([float(rng.multinomial(size, pc)[i:].sum()) for _ in range(reps)])
        za = (a.mean() - mu) / math.sqrt(mu / reps)
        okt = abs(za) < 4.5 and abs(a.var() / mu - 1) < 0.35
        ok = ok and okt
        if verbose:
            print(f"  tail mass {tail[i]:.2e} (expected count {mu:9.1f}): stable sampler mean/expected {a.mean() / mu:.4f}, var/expected "
                  f"{a.var() / mu:.3f}  [{okt}];   numpy multinomial mean/expected {b.mean() / mu:.4f}")
    if verbose:
        print(f"stable multinomial self-test passed: {ok}")
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if selftest() else 1)
