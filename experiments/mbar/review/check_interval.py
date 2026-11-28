"""Referee A -- can LRRegion.interval return an interval that is too NARROW?

For each awkward data set we build the region with the division's code, ask it for intervals, and
then look for a *witness*: a point f with Phi(f) <= level (Phi evaluated by this script, directly
from the definition) whose contrast value c.f lies strictly outside the returned interval.  Such a
point proves that the returned interval is not the projection of the region.  We also check the
truth: if Phi(f*) <= level but c.f* is outside the interval, the interval is wrong.
"""
import sys, time, warnings
import numpy as np
from scipy.special import logsumexp
from scipy.optimize import minimize
from scipy.linalg import null_space

sys.path.insert(0, "../src")
from d9mbar.certificates import lr_confidence_region   # noqa: E402

warnings.filterwarnings("ignore")
rng = np.random.default_rng(424242)


def phi_def(A, y, f):
    return float(np.sum(logsumexp(A + f, axis=1) - f[y]))


def grad_def(A, y, f):
    Z = A + f
    p = np.exp(Z - logsumexp(Z, axis=1)[:, None])
    return p.sum(axis=0) - np.bincount(y, minlength=A.shape[1])


def my_profile(A, y, c, theta, f_start):
    """An upper bound on min{Phi(f): c.f = theta} together with the feasible point attaining it."""
    K = len(c)
    C = np.vstack([c, np.ones(K)])
    f_part = np.linalg.lstsq(C, np.array([theta, 0.0]), rcond=None)[0]
    Nsp = null_space(C)
    if Nsp.shape[1] == 0:
        return phi_def(A, y, f_part), f_part
    fun = lambda v: phi_def(A, y, f_part + Nsp @ v)
    jac = lambda v: Nsp.T @ grad_def(A, y, f_part + Nsp @ v)
    best_v, best = None, np.inf
    v0 = Nsp.T @ (f_start - f_part)
    for meth in ("BFGS", "Nelder-Mead", "BFGS"):
        start = v0 if best_v is None else best_v
        try:
            if meth == "BFGS":
                res = minimize(fun, start, jac=jac, method="BFGS", options=dict(gtol=1e-10, maxiter=2000))
            else:
                res = minimize(fun, start, method="Nelder-Mead",
                               options=dict(xatol=1e-10, fatol=1e-12, maxiter=4000 * len(start)))
        except Exception:
            continue
        if np.isfinite(res.fun) and res.fun < best:
            best, best_v = float(res.fun), res.x
    if best_v is None:
        return fun(v0), f_part + Nsp @ v0
    return best, f_part + Nsp @ best_v


def my_endpoint(A, y, c, level, fhat, sgn, start_step):
    """Largest t >= 0 such that (my upper bound of) the profile at c.fhat + sgn t is <= level."""
    th0 = float(c @ fhat)
    lo_t, f_lo = 0.0, fhat
    step = max(start_step, 1e-6)
    hi_t = None
    for _ in range(60):
        v, fx = my_profile(A, y, c, th0 + sgn * step, f_lo)
        if v > level:
            hi_t = step
            break
        lo_t, f_lo = step, fx
        step *= 1.6
    if hi_t is None:
        return np.inf, f_lo
    for _ in range(50):
        mid = 0.5 * (lo_t + hi_t)
        v, fx = my_profile(A, y, c, th0 + sgn * mid, f_lo)
        if v <= level:
            lo_t, f_lo = mid, fx
        else:
            hi_t = mid
    return lo_t, f_lo           # f_lo is a witness: Phi(f_lo) <= level, c.f_lo = th0 + sgn lo_t


def harmonic(K, spread, n, kpow=2.0, off_scale=0.0):
    ks = kpow ** np.arange(K)
    x0 = spread * np.arange(K)
    off = off_scale * rng.normal(size=K)
    x = np.concatenate([rng.normal(x0[k], 1 / np.sqrt(ks[k]), n[k]) for k in range(K)])
    y = np.repeat(np.arange(K), n)
    U = 0.5 * ks[None, :] * (x[:, None] - x0[None, :]) ** 2 + off[None, :]
    return U, y, -0.5 * np.log(2 * np.pi / ks) + off


def discrete(K, J, zero_prob, n, off_scale=0.0, alpha=1.0):
    while True:
        P = rng.dirichlet(np.ones(J) * alpha, size=K)
        P = np.where(rng.random((K, J)) < zero_prob, 0.0, P)
        if np.all(P.sum(axis=1) > 0):
            break
    P /= P.sum(axis=1, keepdims=True)
    off = off_scale * rng.normal(size=K)
    xs = np.concatenate([rng.choice(J, size=n[k], p=P[k]) for k in range(K)])
    y = np.repeat(np.arange(K), n)
    with np.errstate(divide="ignore"):
        U = -np.log(P[:, xs].T) + off[None, :]
    return U, y, off.copy()


def contrasts(K):
    out = []
    for i in range(K):
        for j in range(i + 1, K):
            c = np.zeros(K); c[i], c[j] = -1.0, 1.0
            out.append(c)
    if K >= 3:
        c = np.zeros(K); c[0], c[1], c[2] = 1.0, -2.0, 1.0
        out.append(c)
        c = rng.normal(size=K); out.append(c - c.mean())
    return out[:7]


cases = []
for K in (3, 4, 5):
    for spread in (0.5, 1.5, 3.0, 4.5):
        for npk in (6, 16, 60):
            for off in (0.0, 300.0):
                cases.append(("harm", K, spread, npk, off))
for K in (2, 3, 4):
    for J in (3, 6):
        for zp in (0.0, 0.4):
            for npk in (5, 20, 120):
                cases.append(("disc", K, J, zp, npk))

t_start = time.time()
stats = dict(datasets=0, ok=0, abstain=0, reject=0, intervals=0, crashes=0, narrow=0, truth_bad=0,
             nonfinite=0)
worst = []
crash_msgs = {}
for case in cases:
    for rep in range(2):
        nb = int(rng.choice([2, 4, 8]))
        if case[0] == "harm":
            _, K, spread, npk, off = case
            n = np.full(K, npk) + rng.integers(0, 3, K)
            U, y, ftrue = harmonic(K, spread, n, off_scale=off)
        else:
            _, K, J, zp, npk = case
            n = np.full(K, npk) + rng.integers(0, 3, K)
            U, y, ftrue = discrete(K, J, zp, n, off_scale=float(rng.choice([0.0, 50.0])))
        stats["datasets"] += 1
        try:
            reg = lr_confidence_region(U, y, alpha=0.05, n_batches=nb)
        except Exception as e:
            stats["crashes"] += 1
            crash_msgs[type(e).__name__ + ": " + str(e)[:80]] = case
            continue
        if reg.status == "REJECT_MODEL":
            stats["reject"] += 1
            continue
        if reg.status != "OK":
            stats["abstain"] += 1
            continue
        stats["ok"] += 1
        A, yy, level = reg.A, reg.labels, reg.level
        truth_in = phi_def(A, yy, ftrue) <= level
        for c in contrasts(K):
            try:
                lo, hi = reg.interval(c)
            except Exception as e:
                stats["crashes"] += 1
                crash_msgs[type(e).__name__ + ": " + str(e)[:80]] = case
                continue
            stats["intervals"] += 1
            if not (np.isfinite(lo) and np.isfinite(hi)):
                stats["nonfinite"] += 1
            th = float(c @ ftrue)
            if truth_in and not (lo <= th <= hi):
                stats["truth_bad"] += 1
                worst.append(("TRUTH in region but outside interval", case, nb, lo, hi, th))
            width = hi - lo if np.isfinite(hi - lo) else 1.0
            for sgn, end in ((1.0, hi), (-1.0, lo)):
                if not np.isfinite(end):
                    continue
                t_mine, fw = my_endpoint(A, yy, c, level, reg.fhat, sgn, 0.25 * abs(end - c @ reg.fhat))
                mine = float(c @ reg.fhat) + sgn * t_mine
                excess = sgn * (mine - end)         # > 0: my witness lies outside their interval
                if excess > 1e-7 * max(1.0, abs(width)) and phi_def(A, yy, fw) <= level:
                    stats["narrow"] += 1
                    worst.append(("WITNESS outside interval", case, nb, float(excess), float(width),
                                  float(level - phi_def(A, yy, fw))))
    if time.time() - t_start > 1500:
        print("time limit reached at case", case)
        break

print(stats)
print("crash messages:", crash_msgs)
worst.sort(key=lambda w: -w[3] if w[0].startswith("WITNESS") else 0)
for w in worst[:25]:
    print(w)
print("elapsed", round(time.time() - t_start, 1))
