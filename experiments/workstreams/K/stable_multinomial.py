"""Workstream K -- multinomial sampling that stays accurate for sample sizes up to 2^62 and cell probabilities down to
10^-300 (needed by sim_grouped.py).

SECOND VERSION (coordinator's check of the review SCI-REV-0007 of the Scientific Discovery Division, section 4 and
request R6-T5; 2026-11-26).  The first version sent every node of the splitting tree with n p > 30 (or p >= 1e-6) to
numpy's `Generator.binomial`, whatever the count n of the node.  The division found that sampler biased low for
n >~ 10^17 with means n p between about 60 and 10^4.  Our own measurement (numpy 2.5.3; part 3 of `selftest` and
experiments/coordinator_checks/nested_review_R6/t5_numpy_binomial_scan.py) confirms it and widens it: the law is
measurably wrong from n ~ 10^15 on, for means above 44 -- low by 0.8 % at n = 2^61, n p = 92 (91.28 instead of 92),
HIGH by 0.06 % at n = 2^53, n p = 500, and with a wrong variance and shape where the mean is right (n = 10^17,
n p = 92: variance low by 6 %) -- while nothing is detected for n <= 3 10^14 or when n is a power of two up to 2^52.
The lower end of the window is sharp: nothing at n p = 43.9, a wrong mean and variance at n p = 44.1.  The cause (the
source of numpy's BTPE branch, n p > 30, as we remember it; consistent with every measurement): its last acceptance
test, reached only for 20 < |y - m| < n p q/2 - 1 and therefore only if n p q > 44, evaluates
log((n + 1 - m)/(n - y + 1)) in floating point, and the rounding error of the quotient, multiplied by n, is of order
n 2^-53 -- a tenth at n = 10^15 -- and above 2^53 the integers themselves are rounded.  For means of 10^6 and more
nothing is detected with 4 10^6 draws (a relative error of the mean above 2 10^-6 would be).
Class name and interface are unchanged (`StableMultinomial(probs).sample(rng, n)`); `sample` has one new optional
argument, `legacy=True`, which restores the rule of the first version for the self-test.

Unchanged: binary splitting over the cells sorted by probability.  Every conditional probability is a ratio of sums of
positive terms (relative accuracy ~1e-15), always <= 1/2; a node with n p <= 30 and p < 1e-6 is sampled by inversion
with log1p (exact up to rounding).  numpy's own multinomial is not usable at this size (it conditions on
1 - p_1 - ... - p_j, which is rounding noise in the far tail).

New: numpy's binomial is called only with n <= 2^31, where every integer of its acceptance test is exact and the
rounding error just described is below 2^-22.  A node with a larger count is first reduced EXACTLY (`_reduce_exact`):
if V is the a-th smallest of n independent uniform numbers, a = ceil(n/2), then V ~ Beta(a, n + 1 - a), and given V
the a - 1 smaller ones are independent and uniform on (0, V) and the n - a larger ones independent and uniform on
(V, 1); so, for X = #{uniform numbers <= p} ~ Bin(n, p):
        V <= p :   X = a + Bin(n - a, (p - V)/(1 - V)),            V > p :   X = Bin(a - 1, p/V).
(The recursive beta method for the binomial law -- Relles 1972, Ahrens-Dieter 1974, Knuth, The Art of Computer
Programming 2, section 3.4.1; cited from memory -- the proof is the sentence above.)  Each step halves n: at most 31
steps.  There is NO Poisson or normal approximation: the law is exact up to the rounding of the beta variates
(relative 1e-16 on a variable whose relative fluctuation is at least 2^-31).  For comparison, replacing Bin(n, p) by
Poisson(n p) for small p -- the remedy the division proposes -- costs a total-variation error of at most
p (1 - e^{-n p}) <= min(p, n p^2) per draw (Le Cam; Barbour-Hall 1984, cited from memory).
"""
import math
import numpy as np

N_DIRECT = 2 ** 31                                     # largest number of trials handed to numpy's binomial


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


def _reduce_exact(rng, n, p):
    """Arrays n (int64, any size), p (float64 in [0, 1]).  Returns (base, n2, p2) with n2 <= N_DIRECT such that
    base + Bin(n2, p2) has exactly the law Bin(n, p) (order statistics of n uniform numbers; see the module text)."""
    n = np.array(n, dtype=np.int64)
    p = np.array(p, dtype=np.float64)
    base = np.zeros(len(n), dtype=np.int64)
    while True:
        idx = np.nonzero(n > N_DIRECT)[0]
        if len(idx) == 0:
            return base, n, p
        nn = n[idx]
        a = (nn + 1) // 2                                # V = the a-th smallest of nn uniform numbers ~ Beta(a, nn + 1 - a)
        V = rng.beta(a.astype(np.float64), (nn + 1 - a).astype(np.float64))
        pp = p[idx]
        le = V <= pp
        # V <= p: the a smallest numbers are <= p, the other nn - a are uniform on (V, 1)
        base[idx[le]] += a[le]
        n[idx[le]] = nn[le] - a[le]
        p[idx[le]] = (pp[le] - V[le]) / (1.0 - V[le])
        # V > p: the a-th smallest and all larger numbers exceed p, the a - 1 smaller ones are uniform on (0, V)
        gt = ~le
        n[idx[gt]] = a[gt] - 1
        p[idx[gt]] = pp[gt] / V[gt]


def binomial_exact(rng, n, p):
    """Bin(n, p) for arrays n (int64 up to 2^62) and p (float64 in [0, 1/2]); never calls numpy's binomial with more
    than N_DIRECT trials."""
    n = np.asarray(n, dtype=np.int64)
    p = np.asarray(p, dtype=np.float64)
    base, n2, p2 = _reduce_exact(rng, n, p)
    p2 = np.clip(p2, 0.0, 1.0)
    out = np.zeros(len(n), dtype=np.int64)
    small = (p2 < 1e-6) & (n2.astype(np.float64) * p2 <= 30.0)
    if small.any():
        out[small] = _binomial_small(rng, n2[small], p2[small])
    if (~small).any():
        out[~small] = rng.binomial(n2[~small], p2[~small])
    return base + out


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

    def sample(self, rng, n, legacy=False):
        """Counts of n points over the cells.  legacy=True: the rule of the first version (numpy's binomial for every
        node that is not `small`, whatever its count) -- kept only so that the self-test can exhibit its defect."""
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
            if legacy:
                if big.any():
                    cl[big] = rng.binomial(cnt[big], pl[big])
            else:
                direct = big & (cnt <= N_DIRECT)
                huge = big & (cnt > N_DIRECT)
                if direct.any():
                    cl[direct] = rng.binomial(cnt[direct], pl[direct])
                if huge.any():
                    cl[huge] = binomial_exact(rng, cnt[huge], pl[huge])
            cl = np.minimum(cl, cnt)
            new = np.empty(2 * len(cnt), dtype=np.int64)
            new[0::2] = cl
            new[1::2] = cnt - cl
            cnt = new
        out = np.zeros(self.S, dtype=np.int64)
        out[self.order] = cnt[self.size - self.S:]
        return out


# ---------------------------------------------------------------------------------------------------------------------
# self-test
# ---------------------------------------------------------------------------------------------------------------------
def _zmean_zvar(x, mu, var):
    """z-scores of the sample mean and of the sample variance of x against the exact mean and variance of a law that
    is close to normal (fourth central moment 3 var^2 + var: Poisson/binomial with small p)."""
    N = len(x)
    x = x.astype(np.float64)
    zm = (x.mean() - mu) / math.sqrt(var / N)
    zv = (((x - mu) ** 2).mean() - var) / math.sqrt((2 * var ** 2 + var) / N)
    return zm, zv


def _poisson_chi2(x, mu):
    """Pearson statistic of the sample x against the Poisson(mu) law on cells of expected count >= 50, as a z-score
    (chi2 - dof)/sqrt(2 dof)."""
    from math import lgamma
    N = len(x)
    lo, hi = int(mu - 6 * math.sqrt(mu)), int(mu + 6 * math.sqrt(mu))
    ks = np.arange(max(lo, 0), hi + 1)
    pm = np.exp(-mu + ks * math.log(mu) - np.array([lgamma(k + 1) for k in ks]))
    keep = N * pm >= 50
    ks, pm = ks[keep], pm[keep]
    obs = np.array([(x == k).sum() for k in ks], dtype=float)
    rest_p = 1.0 - pm.sum()
    rest_o = N - obs.sum()
    chi2 = float(((obs - N * pm) ** 2 / (N * pm)).sum() + (rest_o - N * rest_p) ** 2 / (N * rest_p))
    dof = len(ks)
    return (chi2 - dof) / math.sqrt(2 * dof)


def selftest(verbose=True):
    """(1) small n: chi-square against the exact multinomial law; (2) n = 2^59, radial law of Q_200: mean and variance of
    far-tail counts (tail mass 1e-17 ... 1e-12) for this sampler and for numpy's multinomial [(1), (2): the self-test of
    the first version]; (3) the defect of numpy's binomial at large n and its absence in `binomial_exact`: mean,
    variance and a chi-square test of the whole law; (4) the same through the class, first version (legacy=True)
    against second, on a two-cell law and on the shells of Q_250 in a block of 2^59 points; (5) `binomial_exact`
    against numpy's binomial at sizes where numpy is exact (n = 2^33 ... 2^40, reduced to 2^31 trials).  About one
    minute."""
    rng = np.random.default_rng(5)
    ok = True
    say = print if verbose else (lambda *a, **k: None)
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
    say(f"(1) small case: z-scores of the cell means {np.round(z, 2)}, variance ratios {np.round(var / (n * p * (1 - p)), 3)}: {okm}")
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
        say(f"(2) tail mass {tail[i]:.2e} (expected count {mu:9.1f}): stable sampler mean/expected {a.mean() / mu:.4f}, var/expected "
            f"{a.var() / mu:.3f}  [{okt}];   numpy multinomial mean/expected {b.mean() / mu:.4f}")
    # (3) numpy's binomial against binomial_exact, 200 000 draws each
    N = 200000
    say("(3) Bin(n, mu/n), 200 000 draws: mean, z-score of the mean, z-score of the variance, chi-square z-score against Poisson(mu)")
    say(f"    {'n':>22} {'mu':>6} | numpy.Generator.binomial: {'mean':>10} {'z_mean':>8} {'z_var':>8} {'z_chi2':>8} | binomial_exact: {'mean':>10} {'z_mean':>8} {'z_var':>8} {'z_chi2':>8}")
    power = False
    for (nn, mu) in ((2 ** 61, 92.0), (10 ** 18, 500.0), (2 ** 62 - 1, 5000.0), (10 ** 17, 92.0), (2 ** 53, 500.0), (2 ** 53 - 1, 500.0),
                     (2 ** 50, 92.0)):
        pp = mu / nn
        x = rng.binomial(nn, pp, size=N)
        y = binomial_exact(rng, np.full(N, nn, dtype=np.int64), np.full(N, pp))
        zx = _zmean_zvar(x, mu, mu) + (_poisson_chi2(x, mu),)
        zy = _zmean_zvar(y, mu, mu) + (_poisson_chi2(y, mu),)
        good = all(abs(v) < 4.5 for v in zy)
        ok = ok and good
        if nn == 2 ** 61:
            power = zx[0] < -15                                     # the first version's defect is seen by this test
        say(f"    {nn:22d} {mu:6.0f} | {'':25s} {x.mean():10.4f} {zx[0]:8.2f} {zx[1]:8.2f} {zx[2]:8.2f} | {'':15s} {y.mean():10.4f} {zy[0]:8.2f} {zy[1]:8.2f} {zy[2]:8.2f}  [{good}]")
    ok = ok and power
    say(f"    numpy's sampler fails at n = 2^61, n p = 92 (z of the mean below -15): {power}")
    # (4) through the class
    say("(4) through StableMultinomial.sample: first version (legacy=True) against second version")
    nn = 2 ** 61
    sm2 = StableMultinomial(np.array([92.0 / nn, 1.0]))
    reps = 20000
    a = np.array([sm2.sample(rng, nn, legacy=True)[0] for _ in range(reps)], dtype=float)
    b = np.array([sm2.sample(rng, nn)[0] for _ in range(reps)], dtype=float)
    za, zb = (a.mean() - 92) / math.sqrt(92 / reps), (b.mean() - 92) / math.sqrt(92 / reps)
    good = abs(zb) < 4.5 and za < -6
    ok = ok and good
    say(f"    two cells (92/2^61, rest), n = 2^61, {reps} draws: first version mean {a.mean():.3f} (z = {za:.1f}); second version mean {b.mean():.3f} (z = {zb:.1f})  [{good}]")
    n_o = 250
    probs = np.array([math.comb(n_o, k) for k in range(n_o + 1)], dtype=float) / 2.0 ** n_o
    smq = StableMultinomial(probs)
    lefthalf = np.zeros(n_o + 1, dtype=bool)
    lefthalf[smq.order[: smq.size // 2 - (smq.size - smq.S)]] = True          # the cells in the left half of the root
    size = 2 ** 59
    mu = size * float(probs[lefthalf].sum())
    reps = 4000
    a = np.array([smq.sample(rng, size, legacy=True)[lefthalf].sum() for _ in range(reps)], dtype=float)
    b = np.array([smq.sample(rng, size)[lefthalf].sum() for _ in range(reps)], dtype=float)
    za, zb = (a.mean() - mu) / math.sqrt(mu / reps), (b.mean() - mu) / math.sqrt(mu / reps)
    se = math.sqrt(2.0 / reps)                                      # standard error of a variance ratio
    wa, wb = (a.var() / mu - 1) / se, (b.var() / mu - 1) / se
    good = abs(zb) < 4.5 and abs(wb) < 4.5 and (abs(za) > 6 or abs(wa) > 6)   # here the first version has the right mean and a wrong variance
    ok = ok and good
    say(f"    shells of Q_250, block of 2^59 points, the {int(lefthalf.sum())} rarest shells together (expected count {mu:.2f}), {reps} draws: "
        f"first version mean {a.mean():.3f} (z = {za:.1f}), var/expected {a.var() / mu:.3f} (z = {wa:.1f}); second version mean {b.mean():.3f} (z = {zb:.1f}), "
        f"var/expected {b.var() / mu:.3f} (z = {wb:.1f})  [{good}]")
    # (5) the reduction against numpy where numpy is exact
    say("(5) binomial_exact (reduction to 2^31 trials) against numpy's binomial at sizes where numpy is exact, 200 000 draws each: z of the difference of the means, ratio of the variances")
    for (nn, pp) in ((2 ** 35, 3e-9), (2 ** 38 + 12345, 1.7e-9), (2 ** 40, 0.3), (2 ** 36, 0.5), (2 ** 33, 2e-5)):
        x = rng.binomial(nn, pp, size=N).astype(float)
        y = binomial_exact(rng, np.full(N, nn, dtype=np.int64), np.full(N, pp)).astype(float)
        var = nn * pp * (1 - pp)
        zd = (y.mean() - x.mean()) / math.sqrt(2 * var / N)
        zm = (y.mean() - nn * pp) / math.sqrt(var / N)
        vr = y.var() / x.var()
        good = abs(zd) < 4.5 and abs(zm) < 4.5 and abs(vr - 1) < 0.02
        ok = ok and good
        say(f"    n = {nn}, p = {pp:g}: z(mean_exact - mean_numpy) = {zd:.2f}, z(mean_exact - n p) = {zm:.2f}, var_exact/var_numpy = {vr:.4f}  [{good}]")
    say(f"stable multinomial self-test passed: {ok}")
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if selftest() else 1)
