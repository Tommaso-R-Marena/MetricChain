"""Unit tests of the sample-based code (estimators and certificates).  Fast; run with pytest or
`python experiments/mbar/tests/test_certificates.py`.  Coverage at scale is in bench/."""
import itertools
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from d9mbar import population as pop  # noqa: E402
from d9mbar.certificates import (asymptotic_interval, classifier_evalue, kl_interval,  # noqa: E402
                                 lr_confidence_region, observable_interval, pmf_difference_interval,
                                 restricted_interval)
from d9mbar.estimators import (fitted_distributions, mbar, pilot_allocation, plugin_variance,  # noqa: E402
                               support_strongly_connected)


def harmonic(rng, n, K=4, spread=0.7):
    ks = 2.0 ** np.arange(K)
    x0 = spread * np.arange(K)
    f = -0.5 * np.log(2 * np.pi / ks)
    x = np.concatenate([rng.normal(x0[k], 1 / np.sqrt(ks[k]), n) for k in range(K)])
    y = np.repeat(np.arange(K), n)
    p = rng.permutation(len(y))
    return 0.5 * ks[None, :] * (x[p][:, None] - x0[None, :]) ** 2, y[p], f - f[0], x[p]


def test_evalue_exact_enumeration():
    """Theorem B1 by brute force: E[e-value] <= 1 for arbitrary predictors and tilts, and equal to
    exp(-N KL(s || a)) for the reverse-logistic likelihood ratio."""
    rng = np.random.default_rng(1)
    worst, maxE = 0.0, 0.0
    for trial in range(120):
        K, J = int(rng.integers(2, 4)), int(rng.integers(2, 5))
        n = [int(rng.integers(1, 3)) for _ in range(K)]
        if sum(n) > 5:
            continue
        P = rng.dirichlet(np.ones(J) * rng.uniform(0.3, 2), size=K)
        if trial % 3 == 0:
            P[0, 0] = 0
            P[0] /= P[0].sum()
        N = sum(n)
        s = np.array(n) / N
        m = s @ P
        if trial % 2 == 0:
            delta = rng.normal(0, 1.5, K)
            lam = s[:, None] * np.exp(delta)[:, None] * P
            lam = lam / lam.sum(axis=0)
            w = s
        else:
            lam = rng.dirichlet(np.ones(K), size=J).T
            w = rng.dirichlet(np.ones(K))
        pi = s[:, None] * P / m
        fac = np.where(P > 0, lam / np.where(pi > 0, pi, 1) * ((w @ P) / m), 0.0)
        labels = [k for k in range(K) for _ in range(n[k])]
        tot = 0.0
        for xs in itertools.product(range(J), repeat=N):
            pr = np.prod([P[labels[i], xs[i]] for i in range(N)])
            if pr > 0:
                tot += pr * np.prod([fac[labels[i], xs[i]] for i in range(N)])
        maxE = max(maxE, tot)
        assert tot <= 1 + 1e-12
        if trial % 2 == 0:
            a = (lam * m).sum(axis=1)
            worst = max(worst, abs(tot / np.exp(-N * np.sum(s * np.log(s / a))) - 1))
    assert worst < 1e-12
    return maxE, worst


def test_mbar_against_closed_form_and_plugin():
    rng = np.random.default_rng(2)
    U, y, ftrue, _ = harmonic(rng, 4000)
    f, info = mbar(U, y)
    assert info["converged"] and np.max(np.abs(f - ftrue)) < 0.08
    c = np.array([-1.0, 0, 0, 1.0])
    v = plugin_variance(U, y, c, f=f)
    P = fitted_distributions(U, y, f)
    assert np.allclose(P.sum(axis=1), 1) and 0 < v < 0.01
    # plug-in variance is homogeneous of degree -1 in the counts
    n = np.bincount(y).astype(float)
    assert abs(plugin_variance(U, y, c, counts=2 * n, P=P) * 2 - v) < 1e-9 * v


def test_region_basic_properties():
    rng = np.random.default_rng(3)
    U, y, ftrue, _ = harmonic(rng, 500)
    c = np.array([-1.0, 0, 0, 1.0])
    r05 = lr_confidence_region(U, y, alpha=0.05)
    r20 = lr_confidence_region(U, y, alpha=0.20)
    lo5, hi5 = r05.interval(c)
    lo2, hi2 = r20.interval(c)
    assert r05.status == "OK" and r05.contains(r05.fhat)
    assert lo5 <= lo2 <= c @ r05.fhat <= hi2 <= hi5            # nested in alpha, contains the centre
    assert abs(r05.phi(r05.fhat + 3.0) - r05.phi(r05.fhat)) < 1e-8      # gauge invariance
    # endpoints are on the boundary of the region (up to the outward tolerance)
    val, _, ok = r05._profile(c, hi5, r05.fhat)
    assert ok and val >= r05.level - 1e-6 and val - r05.level < 1e-2 * max(1.0, r05.level)
    # restriction to the two end states is a valid (wider or narrower) interval and contains the truth here
    lo, hi, _ = restricted_interval(U, y, c, [0, 3])
    assert lo <= ftrue[3] - ftrue[0] <= hi


def test_abstention_when_supports_are_separated():
    U = np.array([[0.0, np.inf], [np.inf, 0.0]] * 40)
    y = np.array([0, 1] * 40)
    assert not support_strongly_connected(U, y)
    reg = lr_confidence_region(U, y)
    lo, hi = reg.interval(np.array([-1.0, 1.0]))
    assert reg.status != "OK" and lo == -np.inf and hi == np.inf
    try:
        mbar(U, y)
        raise AssertionError("mbar must refuse")
    except ValueError:
        pass


def test_small_coverage_simulation():
    """300 small data sets: the joint region must miss the truth in at most a few of them
    (expected <= 15 at level 0.05; in practice none), and the observable interval likewise."""
    rng = np.random.default_rng(4)
    miss_region = miss_obs = 0
    for _ in range(300):
        U, y, ftrue, x = harmonic(rng, 60, K=3)
        reg = lr_confidence_region(U, y, alpha=0.05, n_batches=4)
        if reg.status == "OK" and not reg.contains(ftrue):
            miss_region += 1
    for _ in range(40):
        U, y, ftrue, x = harmonic(rng, 150, K=3)
        reg = lr_confidence_region(U, y, alpha=0.05, n_batches=4)
        A = (x > 0.7).astype(float)                     # P_1(x > 0.7) for state 1: N(0.7, 1/2) -> 0.5
        lo, hi = observable_interval(reg, U, y, 1, A)
        miss_obs += not (lo <= 0.5 <= hi)
        assert hi - lo < 1.0 or reg.status != "OK"
        # free-energy difference between the two halves of state 1: exactly 0
        dlo, dhi = pmf_difference_interval(reg, U, y, 1, x > 0.7, x <= 0.7)
        miss_obs += not (dlo <= 0.0 <= dhi)
    assert miss_region <= 15 and miss_obs <= 4, (miss_region, miss_obs)
    return miss_region, miss_obs


def test_kl_interval_and_pilot_allocation():
    lo, hi = kl_interval(0.3, 100, np.log(40))
    assert 0 < lo < 0.3 < hi < 1
    assert kl_interval(0.0, 50, 3.0)[0] == 0.0 and kl_interval(1.0, 50, 3.0)[1] == 1.0
    rng = np.random.default_rng(5)
    U, y, ftrue, _ = harmonic(rng, 50)
    extra, info = pilot_allocation(U, y, np.array([-1.0, 0, 0, 1.0]), total_budget=1000)
    assert extra.sum() == 800 and info["fallback"] is None and extra.min() >= 0.25 * 200 - 1


def test_model_check_is_quiet_under_the_model():
    rng = np.random.default_rng(6)
    U, y, ftrue, x = harmonic(rng, 300, K=3)

    def uniform_predictor(b, prev, cur):
        return np.full((len(cur), 3), 1 / 3)
    logE, info = classifier_evalue(U, y, uniform_predictor, n_batches=4)
    assert logE < 0 and info["converged"]


def test_equivariance_under_energy_offsets():
    """Referee finding E1.  Adding a constant off_k to the energies of state k, and any constant to all
    energies of a sample, must move every free energy by off_k and nothing else: estimates, region
    status, intervals and the model check must be unaffected, for offsets from 10 to 1000 kT."""
    rng = np.random.default_rng(11)
    K = 3
    worst_f = worst_int = 0.0
    for sd in (10.0, 100.0, 1000.0):
        for _ in range(25):
            U0, y, ftrue, x = harmonic(rng, 60, K=K)
            off = rng.normal(0, sd, K)
            U = U0 + off[None, :] + rng.normal(0, 30 * sd, len(y))[:, None]
            f0, i0 = mbar(U0, y)
            f, i1 = mbar(U, y)
            assert i1["converged"]
            worst_f = max(worst_f, np.max(np.abs((f - f[0]) - (f0 - f0[0]) - (off - off[0]))))
            r0 = lr_confidence_region(U0, y, n_batches=4)
            r = lr_confidence_region(U, y, n_batches=4)
            assert r.status == r0.status
            if r.status == "OK":
                c = np.array([-1.0, 0.0, 1.0])
                a0, a = r0.interval(c), r.interval(c)
                sh = off[2] - off[0]
                worst_int = max(worst_int, abs(a[0] - sh - a0[0]), abs(a[1] - sh - a0[1]))
                assert abs((r.level - r.phi_min) - (r0.level - r0.phi_min)) < 1e-6
            lE0, _ = classifier_evalue(U0, y, lambda b, prev, cur: np.full((len(cur), K), 1 / K), n_batches=4)
            lE, info = classifier_evalue(U, y, lambda b, prev, cur: np.full((len(cur), K), 1 / K), n_batches=4)
            assert info["converged"] and abs(lE - lE0) < 1e-6 and lE < np.log(20)
    assert worst_f < 1e-7 and worst_int < 1e-4, (worst_f, worst_int)
    return worst_f, worst_int


def test_solver_never_claims_convergence_at_a_saturated_start():
    """The exact failure the referee found: energies offset by tens of kT, solver started anywhere."""
    from d9mbar.estimators import minimize_lse
    rng = np.random.default_rng(12)
    bad = 0
    for _ in range(100):
        U0, y, ftrue, x = harmonic(rng, 50, K=4)
        off = rng.normal(0, 30.0, 4)
        n = np.bincount(y)
        A = np.log(n / n.sum())[None, :] - (U0 + off[None, :])
        for start in (None, np.zeros(4), rng.normal(0, 50, 4)):
            f, v, info = minimize_lse(A, n / n.sum(), f0=start)
            if info["converged"]:
                err = np.max(np.abs((f - f[0]) - (ftrue - ftrue[0]) - (off - off[0])))
                bad += err > 1.0                        # statistical error is ~0.1; 1.0 would be a wrong fit
            else:
                bad += 1                                 # with overlapping supports the fit must also succeed
    assert bad == 0, bad


def test_overlapping_rounds_are_refused():
    rng = np.random.default_rng(13)
    U, y, ftrue, x = harmonic(rng, 40, K=3)
    idx = np.arange(len(y))
    try:
        lr_confidence_region(U, y, batches=[idx[:40], idx[:80], idx])      # cumulative prefixes
        raise AssertionError("overlapping batches must be refused")
    except ValueError:
        pass
    reg = lr_confidence_region(U, y, batches=[idx[:40], idx[40:80], idx[80:]])
    assert reg.status == "OK"


if __name__ == "__main__":
    print("exact e-value enumeration (max E, identity error):", test_evalue_exact_enumeration())
    test_mbar_against_closed_form_and_plugin()
    test_region_basic_properties()
    test_abstention_when_supports_are_separated()
    print("small coverage simulation (misses of 300 regions, of 40 observable intervals):", test_small_coverage_simulation())
    test_kl_interval_and_pilot_allocation()
    test_model_check_is_quiet_under_the_model()
    print("equivariance under offsets up to 1000 kT (max error of f, of interval ends):", test_equivariance_under_energy_offsets())
    test_solver_never_claims_convergence_at_a_saturated_start()
    test_overlapping_rounds_are_refused()
    print("ALL CERTIFICATE TESTS PASSED")
