"""Tests of metricchain_eng.certinf.multistate (docs/engineering/phase2/MBAR_INTEGRATION.md)."""
import itertools
import math
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from metricchain_eng.certinf.multistate import (bridge_intervals, certify_upper_pooled, closure, kl_bounds, mbar_fit,
                                                shared_error_bound, shared_error_extremes, total_variation,
                                                weight_envelopes)  # noqa: E402


def ladder(M=300, K=4, seed=0):
    """A small family of overlapping states on M points: log-densities, normalised laws, f* = -ln Z."""
    rng = np.random.default_rng(seed)
    x = (np.arange(M) + 0.5) / M
    base = -8.0 * (x - 0.3) ** 2 + 0.3 * rng.standard_normal(M)
    lq = np.stack([base - 0.5 * 60.0 * j * (x - (0.3 + 0.12 * j)) ** 2 for j in range(K)], axis=1)
    Z = np.exp(lq).sum(axis=0)
    return x, lq, np.exp(lq) / Z, -np.log(Z)


def kl(y, mu):
    a = 0.0 if y <= 0 else y * math.log(y / mu)
    b = 0.0 if y >= 1 else (1 - y) * math.log((1 - y) / (1 - mu))
    return a + b


def test_kl_bounds_are_the_level_set():
    for y, n, t in ((0.3, 50, 3.0), (0.01, 400, 5.0), (0.97, 120, 2.0)):
        lo, hi = kl_bounds(y, n, t)
        assert lo < y < hi
        assert n * kl(y, lo) == pytest.approx(t, rel=1e-6) and n * kl(y, hi) == pytest.approx(t, rel=1e-6)
    lo, hi = kl_bounds(0.0, 100, 3.0)
    assert lo == 0.0 and hi == pytest.approx(1 - math.exp(-0.03), rel=1e-9)
    lo, hi = kl_bounds(1.0, 100, 3.0)
    assert hi == 1.0 and lo == pytest.approx(math.exp(-0.03), rel=1e-9)
    assert kl_bounds(0.4, 0, 3.0) == (0.0, 1.0)


def test_kl_bounds_cover_at_the_stated_rate():
    rng = np.random.default_rng(1)
    mu, n, t = 0.07, 200, math.log(2 / 0.1)
    y = rng.beta(0.7, 0.7 * (1 - mu) / mu, size=(4000, n)).mean(axis=1)        # values in [0, 1], not Bernoulli
    miss = sum(not (a <= mu <= b) for a, b in (kl_bounds(float(v), n, t) for v in y))
    assert miss <= 0.1 * 4000


def test_bridge_identity_is_exact_at_the_population():
    _, lq, P, f = ladder()
    a = np.array([0.4, -1.0, 2.0, 0.3])
    w = np.exp(a + lq)
    w /= w.sum(axis=1, keepdims=True)
    for i, j in itertools.combinations(range(4), 2):
        A, B = P[:, i] @ w[:, j], P[:, j] @ w[:, i]
        assert a[j] - a[i] + math.log(B) - math.log(A) == pytest.approx(f[j] - f[i], abs=1e-12)


def test_bridge_intervals_and_closure_cover_the_truth():
    _, lq, P, f = ladder()
    rng = np.random.default_rng(2)
    K, n, miss = 4, 300, 0
    for _ in range(200):
        idx = np.concatenate([rng.choice(len(lq), size=n, p=P[:, j]) for j in range(K)])
        lab = np.repeat(np.arange(K), n)
        a = f + rng.normal(0, 0.5, K)                       # an imperfect centre, independent of the draws
        lo, hi = bridge_intervals(lq[idx], lab, a, 0.1)
        cl = closure(lo, hi)
        if cl is None:
            miss += 1
            continue
        d = f[None, :] - f[:, None]
        miss += int(np.any(d < cl[0] - 1e-12) or np.any(d > cl[1] + 1e-12))
        assert np.all(cl[0] >= lo - 1e-12) and np.all(cl[1] <= hi + 1e-12)      # the closure only tightens
    assert miss <= 20


def test_closure_detects_contradiction_and_propagates():
    lo = np.array([[0, 1.0, -np.inf], [-2.0, 0, 0.5], [np.inf * -1, -1.0, 0]])
    hi = np.array([[0, 2.0, np.inf], [-1.0, 0, 1.0], [np.inf, -0.5, 0]])
    l, h = closure(lo, hi)
    assert l[0, 2] == pytest.approx(1.5) and h[0, 2] == pytest.approx(3.0)       # sums along the path 0 - 1 - 2
    assert l[2, 0] == pytest.approx(-3.0) and h[2, 0] == pytest.approx(-1.5)
    lo[0, 2], hi[0, 2], lo[2, 0], hi[2, 0] = 5.0, 6.0, -6.0, -5.0                # contradicts the path
    assert closure(lo, hi) is None


def test_weight_envelopes_enclose_the_true_density_ratio():
    _, lq, P, f = ladder()
    rng = np.random.default_rng(3)
    K = 4
    for trial in range(60):
        counts = rng.integers(1, 50, K).astype(float)
        if trial % 3 == 0:
            counts[rng.integers(1, K)] = 0.0                # a sub-mixture
        k = 0
        s = counts / counts.sum()
        m = P @ s
        truth = P[:, k] / m
        f0 = f + rng.normal(0, 1.0, K)
        d = f[None, :] - f[:, None]
        lo, hi = d - rng.uniform(0, 1.5, (K, K)), d + rng.uniform(0, 1.5, (K, K))
        if trial % 4 == 0:
            hi[0, 2] = np.inf                               # an unbounded side
            lo[0, 3] = -np.inf
        L, U = weight_envelopes(lq, counts, f0, k, lo, hi, 0.7, 1.9)
        assert np.all(L <= 0.7 * truth * (1 + 1e-10)) and np.all(1.9 * truth <= U * (1 + 1e-10))
        assert np.all(U <= 1.9 / s[k] * (1 + 1e-10))
        Lp, Up = weight_envelopes(lq, counts, f0, k, d, d)  # exact free energies: no slack, whatever the centre
        assert np.allclose(Lp, truth, rtol=1e-9) and np.allclose(Up, truth, rtol=1e-9)
    with pytest.raises(ValueError):
        weight_envelopes(lq, np.array([0.0, 1, 1, 1]), f, 0, d, d)


def test_mbar_fit_recovers_the_free_energies():
    _, lq, P, f = ladder()
    rng = np.random.default_rng(4)
    n = 4000
    idx = np.concatenate([rng.choice(len(lq), size=n, p=P[:, j]) for j in range(4)])
    f0 = mbar_fit(lq[idx], np.full(4, n))
    assert np.allclose(f0 - f0[0], f - f[0], atol=0.08)
    f1 = mbar_fit(lq[idx[: 2 * n]], np.array([n, n, 0, 0]))
    assert np.isnan(f1[2]) and np.isnan(f1[3]) and abs((f1[1] - f1[0]) - (f[1] - f[0])) < 0.08


def test_pooled_certificate_refuses_what_it_cannot_use():
    s0 = np.array([0.2, 0.9, 0.5])
    one = np.ones(3)
    assert certify_upper_pooled(s0, one, one, 1.0, 0.0, 1.0, 0.0).status == "void"
    assert certify_upper_pooled(s0, one, one, math.inf, 0.0, 1.0, 0.05).status == "void"
    assert certify_upper_pooled(s0, one, one, 0.5, 0.0, 1.0, 0.05).status == "void"          # a draw above the bound
    assert certify_upper_pooled(s0, 2 * one, one, 1.0, 0.0, 1.0, 0.05).status == "void"      # L > U
    assert certify_upper_pooled(np.array([0.2, np.nan]), one[:2], one[:2], 1.0, 0.0, 1.0, 0.05).status == "void"
    assert certify_upper_pooled(s0, one, one, 1.0, 0.0, 1.0, 0.05).status == "trivial"       # three draws certify nothing


def test_pooled_certificate_is_valid_and_gains_on_a_rare_event():
    """End to end: target state 0, an event of probability below 1e-6 under it, a ladder of five windows up to it.
    The event is a thin slice: the density ratio of the target against the mixture varies little on it (on a
    whole tail the largest ratio, not the average, sets the sample size; see MBAR_INTEGRATION.md, section 4)."""
    M, K = 400, 6
    x = (np.arange(M) + 0.5) / M
    lq = np.stack([-80.0 * (x - 0.3) ** 2] + [-80.0 * (x - 0.3) ** 2 - 200.0 * (x - c) ** 2 for c in (0.4, 0.5, 0.6, 0.7, 0.8)], axis=1)
    P = np.exp(lq) / np.exp(lq).sum(axis=0)
    A = ((x > 0.68) & (x <= 0.70)).astype(float)
    lam, ups = math.exp(-0.3), math.exp(0.3)
    p = P[:, 0] @ A
    truth = ups * p / (ups * p + lam * (1 - p))
    assert p < 1e-6 and P[:, 5] @ A > 0.1
    rng = np.random.default_rng(5)
    n, wrong, abstain, ratios, ratios_t = 1500, 0, 0, [], []
    for _ in range(30):
        draws = [rng.choice(M, size=2 * n, p=P[:, j]) for j in range(K)]
        pil, val = np.concatenate([d[:n] for d in draws]), np.concatenate([d[n:] for d in draws])
        lab, cnt = np.repeat(np.arange(K), n), np.full(K, float(n))
        f0 = mbar_fit(lq[pil], cnt)
        a = f0 + math.log(1 / K)
        point = f0[None, :] - f0[:, None]
        cl = closure(*bridge_intervals(lq[val], lab, a, 0.02))              # certified: validation half
        rehearsal = closure(*bridge_intervals(lq[pil], lab, a, 0.02))       # pilot half: only sizes the bound
        assert cl is not None and rehearsal is not None
        _, U0 = weight_envelopes(lq, cnt, f0, 0, point, point, lam, ups)
        c = 2.0 * math.exp(max(0.0, float(np.max(-(rehearsal[0][0] - point[0])))))
        big = c * float(np.max(U0 * A))                                     # from the pilot and the grid only
        Lg, Ug = weight_envelopes(lq, cnt, f0, 0, cl[0], cl[1], lam, ups)
        if float(np.max(Ug * A)) > big:
            abstain += 1
            continue
        b = certify_upper_pooled(A[val], Lg[val], Ug[val], big, 0.0, 1.0, 0.03)
        assert b.status == "certified"
        wrong += int(b.value < truth)
        ratios.append(b.value / truth)
        v0 = rng.choice(M, size=K * n, p=P[:, 0])                          # the same number of draws, target only
        t = certify_upper_pooled(A[v0], np.full(K * n, lam), np.full(K * n, ups), ups, 0.0, 1.0, 0.05)
        ratios_t.append(t.value / truth)
    assert abstain <= 3 and wrong <= 2
    assert 1.0 <= np.median(ratios) < 0.05 * np.median(ratios_t)


def test_shared_error_extremes_against_enumeration():
    rng = np.random.default_rng(6)
    n = 8
    signs = np.array(list(itertools.product((-1.0, 1.0), repeat=n)))
    for _ in range(50):
        p_i, p_j = rng.dirichlet(np.ones(n)), rng.dirichlet(np.ones(n))
        for eps in (0.1, 1.0):
            w = np.exp(-eps * signs)
            val = -np.log((w @ p_j) / (w @ p_i))
            lo, hi = shared_error_extremes(p_i, p_j, eps)
            assert lo == pytest.approx(val.min(), abs=1e-12) and hi == pytest.approx(val.max(), abs=1e-12)
            assert max(hi, -lo) <= shared_error_bound(total_variation(p_i, p_j), eps) + 1e-12
    p = rng.dirichlet(np.ones(n))
    assert shared_error_extremes(p, p, 1.0) == pytest.approx((0.0, 0.0), abs=1e-12)          # identical states: no effect
    a, b = np.array([1.0, 0.0]), np.array([0.0, 1.0])
    assert shared_error_extremes(a, b, 0.7) == pytest.approx((-1.4, 1.4), abs=1e-12)          # disjoint states: 2 eps
    assert shared_error_bound(1.0, 0.7) == pytest.approx(1.4)


# ------------------------------------------------------------------------------------------------
# The likelihood-ratio region of the label likelihood (added after reading the certified-MBAR division's
# Theorem B1) and the multiplicity form of the pooled certificate
# ------------------------------------------------------------------------------------------------
def _label_loss(f, lq, counts, w):
    s = counts / counts.sum()
    a = np.log(s) + f + lq
    m = a.max(axis=1)
    return float(w @ (m + np.log(np.exp(a - m[:, None]).sum(axis=1))) / w.sum() - s @ f)


def test_lr_region_covers_and_its_intervals_are_outer_bounds():
    from metricchain_eng.certinf.multistate import lr_intervals
    _, lq, P, f = ladder()
    rng = np.random.default_rng(7)
    K, n, alpha = 4, 400, 0.1
    cnt = np.full(K, float(n))
    d = f[None, :] - f[:, None]
    outside = bad = 0
    width_lr, width_br = [], []
    for rep in range(150):
        pil = np.concatenate([rng.choice(len(lq), size=n, p=P[:, j]) for j in range(K)])
        val = np.concatenate([rng.choice(len(lq), size=n, p=P[:, j]) for j in range(K)])
        f_ref = mbar_fit(lq[pil], cnt)
        w = np.bincount(val, minlength=len(lq)).astype(float)
        level = _label_loss(f_ref, lq, cnt, w) + math.log(1 / alpha) / (K * n)
        inside = _label_loss(f, lq, cnt, w) <= level
        outside += int(not inside)
        lo, hi = lr_intervals(lq, cnt, f_ref, alpha, 0, weights=w)
        assert np.all(lo[0] <= hi[0])
        if inside:                                   # the truth is in the region: every interval must contain it
            bad += int(np.any(d[0] < lo[0] - 1e-9) or np.any(d[0] > hi[0] + 1e-9))
        if rep < 20:                                 # no point of the region exceeds the dual bounds
            g = rng.standard_normal((200, K))
            f_hat = mbar_fit(lq, cnt, weights=w)
            for v in g:
                t_lo, t_hi = 0.0, 4.0
                for _ in range(40):                  # the point of the region farthest along the ray f_hat + t v
                    t = 0.5 * (t_lo + t_hi)
                    if _label_loss(f_hat + t * v, lq, cnt, w) <= level:
                        t_lo = t
                    else:
                        t_hi = t
                pt = f_hat + t_lo * v
                diff = pt - pt[0]
                assert np.all(diff <= hi[0] + 1e-7) and np.all(diff >= lo[0] - 1e-7)
        lo2, hi2 = lr_intervals(lq[val], cnt, f_ref, alpha, 0)                      # per-draw form: the same numbers
        assert np.allclose(lo2[0], lo[0], atol=1e-8) and np.allclose(hi2[0], hi[0], atol=1e-8)
        cl = closure(*bridge_intervals(lq[val], np.repeat(np.arange(K), n), f_ref + math.log(1 / K), alpha))
        width_lr.append(hi[0, K - 1] - lo[0, K - 1])
        width_br.append(cl[1][0, K - 1] - cl[0][0, K - 1])
    assert outside <= alpha * 150 and bad == 0
    assert np.median(width_lr) < 0.7 * np.median(width_br)       # tighter than bridge intervals with path sums


def test_lr_region_is_exhausted_by_its_bounds():
    """The dual bound is attained: a point of the region reaches each end to within the search tolerance."""
    from metricchain_eng.certinf.multistate import lr_intervals
    from scipy.optimize import minimize
    _, lq, P, f = ladder()
    rng = np.random.default_rng(8)
    K, n, alpha = 4, 600, 0.05
    cnt = np.full(K, float(n))
    pil = np.concatenate([rng.choice(len(lq), size=n, p=P[:, j]) for j in range(K)])
    val = np.concatenate([rng.choice(len(lq), size=n, p=P[:, j]) for j in range(K)])
    f_ref = mbar_fit(lq[pil], cnt)
    w = np.bincount(val, minlength=len(lq)).astype(float)
    level = _label_loss(f_ref, lq, cnt, w) + math.log(1 / alpha) / (K * n)
    lo, hi = lr_intervals(lq, cnt, f_ref, alpha, 0, weights=w)
    x0 = mbar_fit(lq, cnt, weights=w)
    for j in (1, 3):
        res = minimize(lambda g: -(g[j] - g[0]), x0, method="SLSQP",
                       constraints=[dict(type="ineq", fun=lambda g: level - _label_loss(g, lq, cnt, w))],
                       options=dict(ftol=1e-12, maxiter=500))
        assert res.success and _label_loss(res.x, lq, cnt, w) <= level + 1e-9
        primal = res.x[j] - res.x[0]
        assert primal <= hi[0, j] + 1e-7 and hi[0, j] - primal < 2e-3 * max(1.0, abs(hi[0, j] - lo[0, j]))


def test_multiplicities_give_the_same_certificate():
    rng = np.random.default_rng(9)
    grid = rng.uniform(0, 1, 50)
    U, L = rng.uniform(1.0, 3.0, 50), rng.uniform(0.2, 1.0, 50)
    idx = rng.integers(0, 50, 5000)
    big = float(np.max(U * np.maximum(grid - 0.2, 0)))
    a = certify_upper_pooled(grid[idx], L[idx], U[idx], big, 0.2, 1.0, 0.05)
    b = certify_upper_pooled(grid, L, U, big, 0.2, 1.0, 0.05, weights=np.bincount(idx, minlength=50).astype(float))
    assert a.status == b.status == "certified" and a.value == pytest.approx(b.value, abs=1e-10) and a.n_valid == b.n_valid
    assert certify_upper_pooled(grid, L, U, big, 0.2, 1.0, 0.05, weights=-np.ones(50)).status == "void"


def test_lr_intervals_on_small_samples_regression():
    """Regression for a defect of the first implementation: with few draws the search over multipliers reached a
    nearly infeasible inner problem, the Newton iteration ran off to a saturated point with a numerically
    singular Hessian, a negative Newton decrement passed the convergence test, and the 'upper bound' came out
    as -2.9e13 (found because the certificate refused the resulting L > U as 'void').  Same model, sizes and
    seed as the failing run of experiments/eng/phase2_mbar."""
    from metricchain_eng.certinf.multistate import lr_intervals
    M, n = 1000, 285
    x = (np.arange(M) + 0.5) / M
    V = 10.0 * ((x - 0.25) * (x - 0.75) / 0.0625) ** 2 + 2.0 * x
    lq = np.stack([-V] + [-V - 750.0 * (x - c) ** 2 for c in (0.30, 0.35, 0.40, 0.44, 0.47, 0.50)], axis=1)
    P = np.exp(lq - lq.max(axis=0))
    P /= P.sum(axis=0)
    f = -(np.log(np.exp(lq - lq.max(axis=0)).sum(axis=0)) + lq.max(axis=0))
    d = f - f[0]
    cnt = np.full(7, float(n))
    children = np.random.SeedSequence([20261128, 8]).spawn(200)
    outside = bad = unbounded = 0
    for child in [children[3]] + children[40:100]:               # repetition 3 is the one that failed
        rng = np.random.default_rng(child)
        rng.choice(M, size=4000, p=P[:, 0])
        draws = [rng.choice(M, size=2 * n, p=P[:, j]) for j in range(7)]
        pil = np.concatenate([q[:n] for q in draws])
        w = np.bincount(np.concatenate([q[n:] for q in draws]), minlength=M).astype(float)
        f_ref = mbar_fit(lq[pil], cnt)
        lo, hi = lr_intervals(lq, cnt, f_ref, 0.02, 0, weights=w)
        assert np.all(lo[0] <= hi[0]) and np.all(hi[0] > -1e6) and np.all(lo[0] < 1e6)
        unbounded += int(not np.all(np.isfinite(hi[0])) or not np.all(np.isfinite(lo[0])))
        level = _label_loss(f_ref, lq, cnt, w) + math.log(1 / 0.02) / (7 * n)
        if _label_loss(f, lq, cnt, w) <= level:
            bad += int(np.any(d < lo[0] - 1e-9) or np.any(d > hi[0] + 1e-9))
        else:
            outside += 1
    assert bad == 0 and outside <= 4 and unbounded <= 6
