"""Independent numerical verification of the allocation theory (Priority A).

Run:  python experiments/mbar/tests/test_population.py   (also collected by pytest)
Every check is a claim of docs/mbar/MATHEMATICS.md, part A; the names in brackets are the theorems.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from d9mbar.population import (  # noqa: E402
    contrast_measure, efficiency_lower_bound, efficient_rounding, elfving_value, laplacian,
    observable_measure, optimal_allocation, state_variances as _state_variances, variance,
    variance_dual, variance_formula, variance_qp,
)


def variance_primal(P, s, c):          # the stable route, for a contrast
    return variance(P, s, contrast_measure(P, c))


def state_variances(P, s, c):
    return _state_variances(P, s, contrast_measure(P, c))


def random_model(rng, K=None, J=None, sparse=False):
    K = K or int(rng.integers(2, 8))
    J = J or int(rng.integers(K, 16))
    P = rng.dirichlet(np.full(J, rng.uniform(0.2, 3.0)), size=K)
    if sparse:  # chain-like supports with exact zeros, still connected
        P = np.zeros((K, J))
        width = max(2, J // K + 1)
        for k in range(K):
            lo = int(round(k * (J - width) / max(K - 1, 1)))
            P[k, lo:lo + width] = rng.dirichlet(np.ones(width))
    c = rng.normal(size=K)
    c -= c.mean()
    return P, c


def test_four_routes_agree():
    """[A1, A2, A3] formula = primal minimiser value = dual value = independent QP."""
    rng = np.random.default_rng(1)
    worst = 0.0
    for trial in range(400):
        P, c = random_model(rng, sparse=(trial % 4 == 0))
        s = rng.dirichlet(np.ones(len(c))) + 0.02
        try:
            a = variance_formula(P, s, c)
        except ValueError:      # disconnected sparse instance: every route must refuse or be infinite
            assert not np.isfinite(variance_dual(P, s, c))
            continue
        vals = [a, variance_primal(P, s, c), variance_dual(P, s, c), variance_qp(P, s, c)]
        worst = max(worst, np.ptp(vals) / max(1e-12, abs(a)))
    assert worst < 1e-6, worst
    return worst


def test_gradient_and_euler():
    """[A2] dV/ds_k = -Var_k(z); Euler: sum s_k Var_k(z) = V (degree -1)."""
    rng = np.random.default_rng(2)
    worst = 0.0
    for _ in range(300):
        P, c = random_model(rng)
        s = rng.dirichlet(np.ones(len(c))) + 0.05
        g = -state_variances(P, s, c)
        h = rng.normal(size=len(c))
        h /= np.linalg.norm(h)
        e = 1e-6
        fd = (variance_formula(P, s + e * h, c) - variance_formula(P, s - e * h, c)) / (2 * e)
        worst = max(worst, abs(fd - g @ h) / (1 + abs(fd)))
        assert abs(variance_formula(P, 3.7 * s, c) * 3.7 - variance_formula(P, s, c)) < 1e-8 * (1 + abs(fd))
    assert worst < 1e-5, worst
    return worst


def test_convexity_and_concave_precision():
    """[A1] V convex;  [A4] 1/V concave and superadditive;  monotone in each s_k."""
    rng = np.random.default_rng(3)
    wj = ws = wm = 0.0
    for _ in range(600):
        P, c = random_model(rng)
        K = len(c)
        s, t = rng.dirichlet(np.ones(K)) + 0.03, rng.dirichlet(np.ones(K)) + 0.03
        lam = rng.random()
        Vs, Vt = variance_formula(P, s, c), variance_formula(P, t, c)
        Vm = variance_formula(P, lam * s + (1 - lam) * t, c)
        if min(Vs, Vt, Vm) < 1e-12:
            continue
        wj = max(wj, (Vm - lam * Vs - (1 - lam) * Vt) / Vm)                 # convexity defect
        ws = max(ws, (lam / Vs + (1 - lam) / Vt - 1 / Vm) * Vm)             # concavity defect of 1/V
        Vsum = variance_formula(P, s + t, c)
        ws = max(ws, (1 / Vs + 1 / Vt - 1 / Vsum) * Vsum)                   # superadditivity defect
        k = int(rng.integers(K))
        e = np.zeros(K)
        e[k] = rng.random()
        wm = max(wm, (variance_formula(P, s + e, c) - Vs) / Vs)             # monotonicity defect
    assert wj < 1e-9 and ws < 1e-9 and wm < 1e-9, (wj, ws, wm)
    return wj, ws, wm


def test_boundary_extension():
    """[A3] the dual value on the closed orthant is the radial limit of V from the interior, and is
    +inf exactly when the contrast is not estimable from the sampled states."""
    rng = np.random.default_rng(4)
    worst = 0.0
    for _ in range(100):
        P, c = random_model(rng, K=5, J=9)
        s = rng.dirichlet(np.ones(5)) + 0.05
        s0 = s.copy()
        s0[2] = 0.0                     # state 2 unsampled; full supports, so still estimable
        # Numerical caveat (recorded in docs/mbar/DEAD_ENDS.md, N1): as s_k -> 0 both Laplacian
        # routes lose accuracy (v_k ~ c_k/s_k, condition number ~ 1/s_k); the dual and QP routes
        # do not.  The radial limit is therefore taken with the independent QP route.
        limit = variance_qp(P, np.where(s0 > 0, s0, 1e-8), c)
        worst = max(worst, abs(variance_dual(P, s0, c) - limit) / limit)
        worst = max(worst, abs(variance_primal(P, s0, c) - variance_dual(P, s0, c)) / limit)
    assert worst < 1e-4, worst
    # not estimable: the unsampled state has mass where no sampled state has any
    P = np.array([[0.5, 0.5, 0.0], [0.0, 0.5, 0.5], [0.2, 0.3, 0.5]])
    c = np.array([1.0, 0.0, -1.0])
    assert np.isfinite(variance_dual(P, np.array([0.5, 0.5, 0.0]), c))       # state 2 covered
    P2 = np.array([[1.0, 0.0, 0.0], [0.5, 0.5, 0.0], [0.2, 0.3, 0.5]])
    assert not np.isfinite(variance_dual(P2, np.array([0.5, 0.5, 0.0]), c))  # point 2 never sampled
    return worst


def test_elfving_identity_and_equivalence():
    """[A5, A6] min_s V = primal group norm = dual; KKT of the equivalence theorem; costs."""
    rng = np.random.default_rng(5)
    worst = 0.0
    for trial in range(40):
        P, c = random_model(rng, K=int(rng.integers(2, 6)), J=int(rng.integers(6, 12)))
        K = len(c)
        cost = np.exp(rng.normal(0, 1.0, K)) if trial % 2 else np.ones(K)
        B = 1.0
        s, V, info = optimal_allocation(P, c, cost=cost, budget=B, kind="contrast")
        pv, dv, sp = elfving_value(P, c, cost=cost, budget=B)
        worst = max(worst, abs(pv - V) / V, abs(dv - V) / V)
        assert info["kkt_gap"] < 1e-6, info["kkt_gap"]
        assert abs(efficiency_lower_bound(P, s, contrast_measure(P, c), cost=cost) - 1) < 1e-5
        # no competitor allocation beats it
        for _ in range(20):
            t = rng.dirichlet(np.ones(K)) + 1e-3
            t *= B / (cost @ t)
            assert variance_primal(P, t, c) >= V * (1 - 1e-7)
        # the allocation read off the group-norm solution attains the same value
        assert abs(variance_primal(P, np.where(sp > 1e-6, sp, 0.0), c) - V) / V < 1e-3
    assert worst < 1e-4, worst
    return worst


def test_rounding_and_safeguard():
    """[A8] integer rounding loses at most B/(B - sum a);  [A9] V(s) <= max_k(t_k/s_k) V(t)."""
    rng = np.random.default_rng(6)
    for _ in range(100):
        P, c = random_model(rng, K=4, J=8)
        cost = np.exp(rng.normal(0, 0.7, 4))
        N = int(rng.integers(40, 400))
        B = float(N) * cost.mean()
        s, V, _ = optimal_allocation(P, c, cost=cost, budget=B, kind="contrast")
        n = efficient_rounding(s, B, cost=cost)
        assert cost @ n <= B + 1e-9
        assert variance_primal(P, n.astype(float), c) <= V * B / (B - cost.sum()) * (1 + 1e-9)
        u, t = rng.dirichlet(np.ones(4)) + 0.02, rng.dirichlet(np.ones(4)) + 0.02
        assert variance_formula(P, u, c) <= np.max(t / u) * variance_formula(P, t, c) * (1 + 1e-9)
        gam = 0.3
        mix = gam * u + (1 - gam) * t
        assert variance_formula(P, mix, c) <= min(variance_formula(P, u, c) / gam,
                                                  variance_formula(P, t, c) / (1 - gam)) * (1 + 1e-9)


def test_laplacian_is_a_laplacian():
    rng = np.random.default_rng(7)
    for _ in range(50):
        P, c = random_model(rng)
        s = rng.dirichlet(np.ones(len(c))) + 0.02
        L = laplacian(P, s)
        assert np.allclose(L, L.T) and np.allclose(L.sum(axis=1), 0, atol=1e-12)
        assert np.all(L - np.diag(np.diag(L)) <= 1e-15)


def test_observables_and_multiple_targets():
    """[A3] expectation targets: single state reduces to Var_k(A); self-normalised importance
    sampling value; [A10] sum and max criteria are solved to their KKT conditions."""
    rng = np.random.default_rng(8)
    for _ in range(50):
        P, c = random_model(rng, K=3, J=10)
        A = rng.normal(size=10)
        nu = observable_measure(P, 0, A)
        var0 = P[0] @ A**2 - (P[0] @ A) ** 2
        assert abs(variance(P, np.array([1.0, 0, 0]), nu) - var0) < 1e-9 * (1 + var0)
        w = P[0] / P[1]
        snis = P[1] @ (w**2 * (A - P[0] @ A) ** 2)       # delta-method variance of self-normalised IS
        assert abs(variance(P, np.array([0, 1.0, 0]), nu) - snis) < 1e-8 * (1 + snis)
        # more samples anywhere never hurt, and sampling all three beats either alone per unit
        assert variance(P, np.array([1.0, 1.0, 1.0]), nu) <= min(var0, snis) + 1e-12
        cs = [np.array([1.0, -1, 0]), np.array([0, 1.0, -1]), np.array([1.0, 0, -1])]
        s, V, info = optimal_allocation(P, cs, objective="sum", kind="contrast")
        assert info["kkt_gap"] < 1e-6
        s2, V2, info2 = optimal_allocation(P, cs, objective="max", iters=4000, kind="contrast")
        for _ in range(30):
            t = rng.dirichlet(np.ones(3))
            assert max(variance_primal(P, t, ci) for ci in cs) >= V2 * (1 - 2e-3)


def test_neyman_step_monotone_and_efficiency_bound():
    """[A7] one step of iterated Neyman allocation never increases V;  [A6] the efficiency bound is a
    true lower bound on V*/V(s), also in its version with lower limits on the allocation."""
    rng = np.random.default_rng(9)
    worst_step, worst_bound = -np.inf, -np.inf
    for trial in range(150):
        P, c = random_model(rng, K=int(rng.integers(2, 6)), J=int(rng.integers(5, 11)))
        K = len(c)
        nu = contrast_measure(P, c)
        a = np.exp(rng.normal(0, 0.8, K))
        s = rng.dirichlet(np.ones(K)) + 0.02
        s /= a @ s                                      # budget 1
        V = variance(P, s, nu)
        g = _state_variances(P, s, nu)
        sp = s * np.sqrt(g / a)
        sp /= a @ sp
        if sp.min() > 0:
            worst_step = max(worst_step, (variance(P, sp, nu) - V) / V)
        _, Vopt, _ = optimal_allocation(P, nu, cost=a, budget=1.0, tol=1e-9, kind="measure")
        worst_bound = max(worst_bound, efficiency_lower_bound(P, s, nu, cost=a, budget=1.0) - Vopt / V)
        lo = 0.3 * s
        _, Vlo, _ = optimal_allocation(P, nu, cost=a, budget=1.0, lower=lo, tol=1e-9, kind="measure")
        worst_bound = max(worst_bound, efficiency_lower_bound(P, s, nu, cost=a, budget=1.0, lower=lo) - Vlo / V)
    assert worst_step < 1e-9 and worst_bound < 1e-6, (worst_step, worst_bound)
    return worst_step, worst_bound


if __name__ == "__main__":
    print("four routes, max relative spread      :", test_four_routes_agree())
    print("gradient, max relative error          :", test_gradient_and_euler())
    print("convexity / 1/V concavity / monotone  :", test_convexity_and_concave_precision())
    print("boundary extension, max relative error:", test_boundary_extension())
    print("Elfving identity, max relative gap    :", test_elfving_identity_and_equivalence())
    test_rounding_and_safeguard()
    test_laplacian_is_a_laplacian()
    test_observables_and_multiple_targets()
    print("Neyman step (max increase), efficiency bound (max excess):", test_neyman_step_monotone_and_efficiency_bound())
    print("ALL POPULATION CHECKS PASSED")
