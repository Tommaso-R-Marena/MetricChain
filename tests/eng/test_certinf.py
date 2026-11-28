"""Tests of src/metricchain_eng/certinf (Phase II): the statements of docs/engineering/phase2/CERTIFIED_INFERENCE.md
that can be checked by exhaustive computation on small instances, and the validity of the sampled certificates."""
import math
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from metricchain_eng import certinf as ci  # noqa: E402


def instance(rng, n, m, ratio=4.0):
    l = rng.uniform(0.2, 1.0, n)
    u = l * rng.uniform(1.0, ratio, n)
    return l, u, rng.uniform(-1, 1, n), rng.uniform(-1, 1, (n, m))


def reachable(rng, l, u, phi):
    w = l + rng.uniform(0, 1, len(l)) * (u - l)
    return (w @ phi) / w.sum()


# ------------------------------------------------------------------------------------------ exact side
def test_tau_root_is_the_root_of_psi():
    rng = np.random.default_rng(1)
    for _ in range(50):
        l, u, f, phi = instance(rng, 40, 2)
        P = ci.box_problem(l, u, f, phi, ci.Box(rng.uniform(-0.2, 0.2, 2), 0.1))
        eta = rng.normal(size=2)
        t = ci.tau_root(P, eta)
        assert abs(ci.psi(P, t, eta)) < 1e-9
        assert ci.psi(P, t - 1e-6, eta) > 0 > ci.psi(P, t + 1e-6, eta)


@pytest.mark.parametrize("m", [0, 1, 2, 3])
def test_dual_equals_primal_programme(m):
    """Theorem 4.1(b): the dual with m multipliers gives the ends of the primal programme over all weights."""
    rng = np.random.default_rng(10 + m)
    for _ in range(6):
        l, u, f, phi = instance(rng, 30, m)
        box = ci.Box(reachable(rng, l, u, phi), 0.03)
        lo, hi = ci.lp_primal_box(l, u, f, phi, box)
        out = ci.interval(ci.box_problem(l, u, f, phi, box))
        assert abs(out["hi"] - hi) < 1e-6 and abs(out["lo"] - lo) < 1e-6 and not out["empty"]
        assert ci.psi(ci.box_problem(l, u, f, phi, box), out["hi"] + 1e-9, out["eta_hi"]) <= 0     # soundness, 4.1(a)


def test_threshold_rule_without_data():
    rng = np.random.default_rng(3)
    l, u, f, _ = instance(rng, 25, 0)
    order = np.argsort(-f)
    best = max((np.where(np.isin(np.arange(25), order[:k]), u, l) @ f) / np.where(np.isin(np.arange(25), order[:k]), u, l).sum() for k in range(26))
    assert abs(ci.interval(ci.box_problem(l, u, f, np.zeros((25, 0)), ci.Box()))["hi"] - best) < 1e-12


def test_descent_route_and_ellipsoid():
    rng = np.random.default_rng(4)
    l, u, f, phi = instance(rng, 60, 2)
    y, e = reachable(rng, l, u, phi), np.array([0.04, 0.07])
    box_in, box_out = ci.Box(y, e / math.sqrt(2)), ci.Box(y, e)
    P = ci.box_problem(l, u, f, phi, box_out)
    t_lp, t_de = ci.solve_upper(P, "lp")[0], ci.solve_upper(P, "descent")[0]
    assert -1e-9 <= t_de - t_lp < 1e-5
    ell = ci.interval(ci.box_problem(l, u, f, phi, ci.Ellipsoid(y, np.diag(e ** 2), 1.0)))
    inner, outer = ci.interval(ci.box_problem(l, u, f, phi, box_in)), ci.interval(P)
    assert outer["lo"] - 1e-6 <= ell["lo"] <= inner["lo"] + 1e-5 and inner["hi"] - 1e-5 <= ell["hi"] <= outer["hi"] + 1e-6


def test_inconsistency_certificate():
    """Theorem 4.1(e)."""
    rng = np.random.default_rng(5)
    l, u, f, phi = instance(rng, 30, 2)
    far = ci.Box([0.95, 0.95], 0.02)
    assert ci.lp_primal_box(l, u, f, phi, far) is None
    P = ci.box_problem(l, u, f, phi, far)
    val, eta = ci.find_inconsistency(P)
    assert val > 0 and abs(ci.phi_value(P, eta) - val) < 1e-12 and ci.interval(P)["empty"]
    ok = ci.box_problem(l, u, f, phi, ci.Box(reachable(rng, l, u, phi), 0.02))
    assert ci.find_inconsistency(ok)[0] <= 1e-9


def test_instances_of_the_lower_bound():
    """The two families in the proof of Theorem 6.1."""
    gam = 10.0
    for a in (0.05, 0.1, 0.2):
        out = ci.interval(ci.box_problem([1 - a, a], [gam * (1 - a), gam * a], [0, 1], np.zeros((2, 0)), ci.Box()))
        assert abs(out["hi"] - gam * a / (1 + (gam - 1) * a)) < 1e-12
    m = 1 / gam
    for t in (0.0, 0.02, 0.05):
        pi = np.array([1 - 2 * m + t, 2 * (m - t), t])
        out = ci.interval(ci.box_problem(pi, gam * pi, [0, 0.5, 1], np.zeros((3, 0)), ci.Box()))
        assert abs(out["hi"] - 1 / (1 + (gam - 1) * (2 / gam - t))) < 1e-12
        assert abs(pi @ [0, 0.5, 1] - m) < 1e-15


def test_lumping_and_level_counts():
    """Proposition 8.1: a product reference, additive lattice-valued observables, any number of sites."""
    rng = np.random.default_rng(6)
    n, gam = 10, 3.0
    p1 = rng.uniform(0.2, 0.8, n)
    states = ((np.arange(1 << n)[:, None] >> np.arange(n)) & 1).astype(float)
    pi = np.prod(np.where(states == 1, p1, 1 - p1), axis=1)
    f, phi = states.mean(axis=1), states[:, :5].sum(axis=1, keepdims=True) / 5
    box = ci.Box([0.55], 0.02)
    full = ci.box_problem(pi, gam * pi, f, phi, box)
    law = ci.product_joint_law([[1 - p, p] for p in p1], [[[0, 0], [1, int(i < 5)]] for i in range(n)])
    cells, prob = ci.cells_from_law(law)
    small = ci.Problem(cells[:, 0] / n, cells[:, 1:2] / 5, Lw=prob, Gw=(gam - 1) * prob, region=box)
    a, b, c = ci.interval(full), ci.interval(ci.lump(full)), ci.interval(small)
    assert len(prob) <= 66 and abs(prob.sum() - 1) < 1e-12
    for key in ("lo", "hi"):
        assert abs(a[key] - b[key]) < 1e-7 and abs(a[key] - c[key]) < 1e-7


# ------------------------------------------------------------------------------------------ S3 as proposed
def test_s3_concentration_and_soundness():
    rng = np.random.default_rng(7)
    l, u, f, phi = instance(rng, 300, 2, ratio=2.0)
    v = np.column_stack([np.ones(300), phi, f])
    g = u - l
    b, G = l @ v, g.sum()
    box = ci.Box(reachable(rng, l, u, phi), 0.05)
    exact = ci.interval(ci.box_problem(l, u, f, phi, box))
    n = 4000
    lam = rng.normal(size=(2000, 4))
    lam /= np.abs(lam).sum(axis=1, keepdims=True)
    h_true = np.maximum(lam @ v.T, 0) @ g
    for rep in range(5):
        x = rng.choice(300, size=n, p=g / G)
        dev = np.abs(G * np.maximum(lam @ v[x].T, 0).mean(axis=1) - h_true).max() / G
        assert dev <= ci.s3_eps_rademacher(n, 4, 0.05) <= ci.s3_eps_net(n, 4, 0.05)
        for bound in ("net", "rademacher"):
            out = ci.s3_interval(b, G, f[x], phi[x], box, 0.05, bound)
            assert out["status"] == "certified" and out["lo"] <= exact["lo"] + 1e-9 and out["hi"] >= exact["hi"] - 1e-9


# ------------------------------------------------------------------------------------------ sampled certificates
def reference_model(rng, n_states, m, rho_max):
    pi = rng.dirichlet(np.ones(n_states))
    rho = rng.uniform(0, rho_max, n_states)
    f, phi = rng.uniform(-1, 1, n_states), rng.uniform(-1, 1, (n_states, m))
    l, u = pi * np.exp(-rho), pi * np.exp(rho)
    dec = ci.Declared(-1.0, 1.0, -np.ones(m), np.ones(m), math.exp(rho_max))
    return pi, rho, f, phi, l, u, dec


def draw(rng, pi, rho, f, phi, n):
    x = rng.choice(len(pi), size=n, p=pi)
    return ci.Sample(f[x], phi[x], np.exp(-rho[x]), np.exp(rho[x]))


def test_sampled_interval_is_valid_and_tightens():
    """Theorem 5.1: failures of the certified ends are rarer than delta; the excess shrinks with the sample."""
    rng = np.random.default_rng(8)
    pi, rho, f, phi, l, u, dec = reference_model(rng, 200, 2, 0.5)
    box = ci.Box(reachable(rng, l, u, phi), 0.05)
    exact = ci.interval(ci.box_problem(l, u, f, phi, box))
    fails, widths = 0, []
    for _ in range(120):
        out = ci.certified_interval(draw(rng, pi, rho, f, phi, 1200), box, dec, 0.1)
        fails += (out["hi"] < exact["hi"] - 1e-9) or (out["lo"] > exact["lo"] + 1e-9)
        widths.append(out["hi"] - out["lo"])
    assert fails <= 20                                   # at most delta = 0.1 of 120 in expectation; Markov is not tight
    big = ci.certified_interval(draw(rng, pi, rho, f, phi, 60000), box, dec, 0.1)
    assert big["status"] == "certified" and big["lo"] <= exact["lo"] and big["hi"] >= exact["hi"]
    assert (big["hi"] - exact["hi"]) < 0.5 * (np.median(widths) - (exact["hi"] - exact["lo"])) and big["hi"] - exact["hi"] < 0.05


def test_abstention_and_void():
    rng = np.random.default_rng(9)
    pi, rho, f, phi, l, u, dec = reference_model(rng, 50, 1, 0.3)
    s, box = draw(rng, pi, rho, f, phi, 400), ci.Box([0.0], 0.5)
    free = ci.Declared(-1, 1, [-1], [1], math.inf)
    assert ci.certified_interval(s, box, free, 0.1)["status"] == "abstain"
    chain = ci.Declared(-1, 1, [-1], [1], dec.U_max, iid=False)
    assert ci.certified_interval(s, box, chain, 0.1)["status"] == "abstain"
    wrong = ci.Declared(-0.5, 0.5, [-1], [1], dec.U_max)
    assert ci.certified_interval(s, box, wrong, 0.1)["status"] == "void"
    tiny = ci.certified_interval(draw(rng, pi, rho, f, phi, 6), box, dec, 0.01)
    assert tiny["status"] == "trivial" and tiny["lo"] == -1 and tiny["hi"] == 1


def test_inconsistency_from_samples():
    rng = np.random.default_rng(11)
    pi, rho, f, phi, l, u, dec = reference_model(rng, 100, 2, 0.4)
    far, near = ci.Box([0.9, 0.9], 0.02), ci.Box(reachable(rng, l, u, phi), 0.05)
    assert ci.lp_primal_box(l, u, f, phi, far) is None
    s = draw(rng, pi, rho, f, phi, 4000)
    assert ci.certify_inconsistent(s.part(slice(0, 2000)), s.part(slice(2000, None)), far, dec, 0.01).status == "certified"
    alarms = 0
    for _ in range(40):
        s = draw(rng, pi, rho, f, phi, 1000)
        alarms += ci.certify_inconsistent(s.part(slice(0, 500)), s.part(slice(500, None)), near, dec, 0.1).status == "certified"
    assert alarms <= 8


def test_gap_sampling_certificate():
    rng = np.random.default_rng(12)
    pi, rho, f, phi, l, u, dec = reference_model(rng, 150, 1, 0.6)
    v = np.column_stack([np.ones(150), phi, f])
    g = u - l
    b, G = l @ v, g.sum()
    box = ci.Box(reachable(rng, l, u, phi), 0.05)
    exact = ci.interval(ci.box_problem(l, u, f, phi, box))
    fails, vals = 0, []
    for _ in range(60):
        x = rng.choice(150, size=4000, p=g / G)
        out = ci.certify_upper_gap(b, G, f[x[:2000]], phi[x[:2000]], f[x[2000:]], phi[x[2000:]], box, dec, 0.1)
        fails += out.value < exact["hi"] - 1e-9
        vals.append(out.value)
    assert fails <= 12 and np.median(vals) - exact["hi"] < 0.1


def test_interval_arithmetic_confirmation():
    rng = np.random.default_rng(13)
    pi, rho, f, phi, l, u, dec = reference_model(rng, 80, 1, 0.3)
    s, box = draw(rng, pi, rho, f, phi, 300), ci.Box(reachable(rng, l, u, phi), 0.1)
    tr, va = s.part(slice(0, 150)), s.part(slice(150, None))
    plain, checked = ci.certify_upper(tr, va, box, dec, 0.1), ci.certify_upper(tr, va, box, dec, 0.1, rigorous=True)
    assert checked.status == plain.status == "certified" and 0 <= checked.value - plain.value < 1e-9


# ------------------------------------------------------------------------------------------ ratio-constrained classes
def test_complete_graph_is_the_box_class():
    rng = np.random.default_rng(14)
    n, gam = 12, 3.0
    pi, f, phi = rng.dirichlet(np.ones(n)), rng.uniform(-1, 1, n), rng.uniform(-1, 1, (n, 1))
    box = ci.Box(reachable(rng, pi, gam * pi, phi), 0.05)
    edges = [(i, j) for i in range(n) for j in range(n) if i != j]
    lo, hi = ci.lp_ratio_class(pi, edges, gam, f, phi, box)
    out = ci.interval(ci.box_problem(pi, gam * pi, f, phi, box))
    assert abs(out["lo"] - lo) < 1e-6 and abs(out["hi"] - hi) < 1e-6


def test_bounded_influence_closure_additive_and_separation():
    """Proposition 9.2, Corollary 9.3 and the example of section 9.4, against the programme on the whole cube."""
    rng = np.random.default_rng(15)
    n = 6
    states, edges, site = ci.hypercube(n)
    p1, slope = rng.uniform(0.2, 0.8, n), rng.uniform(0.2, 1.0, n)
    pi = np.prod(np.where(states == 1, p1, 1 - p1), axis=1)
    C = np.exp(slope[site])
    fs, ps = rng.uniform(-1, 1, (n, 2)), rng.uniform(-1, 1, (n, 2, 1))
    f = sum(fs[i][states[:, i].astype(int)] for i in range(n))
    phi = sum(ps[i][states[:, i].astype(int)] for i in range(n))
    box = ci.Box([float(pi @ phi[:, 0]) + 0.1], 0.05)
    lo, hi = ci.lp_ratio_class(pi, edges, C, f, phi, box)
    add = ci.additive_interval([[1 - p, p] for p in p1], slope, list(fs), list(ps), box)
    assert abs(add["lo"] - lo) < 1e-6 and abs(add["hi"] - hi) < 1e-6
    # closure: a target on sites {0, 1} is decided on the two-site cube
    g = states[:, 0] * states[:, 1] - 0.3 * states[:, 0]
    s2, e2, site2 = ci.hypercube(2)
    pi2 = np.prod(np.where(s2 == 1, p1[:2], 1 - p1[:2]), axis=1)
    whole, block = ci.lp_ratio_class(pi, edges, C, g), ci.lp_ratio_class(pi2, e2, np.exp(slope[site2]), s2[:, 0] * s2[:, 1] - 0.3 * s2[:, 0])
    assert abs(whole[0] - block[0]) < 1e-7 and abs(whole[1] - block[1]) < 1e-7
    # separation: one spin, uniform reference and slope u; the box hull of the class has ratio exp(u n)
    u = 0.7
    one = ci.lp_ratio_class(np.full(1 << n, 2.0 ** -n), edges, math.exp(u), states[:, 0])
    hull = ci.interval(ci.box_problem(np.full(1 << n, 1.0), np.full(1 << n, math.exp(u * n)), states[:, 0], np.zeros((1 << n, 0)), ci.Box()))
    assert abs(one[1] - 1 / (1 + math.exp(-u))) < 1e-7 and abs(hull["hi"] - 1 / (1 + math.exp(-u * n))) < 1e-9


def test_stress_observable():
    rng = np.random.default_rng(16)
    z = rng.normal(size=(6, 3))
    om = ci.projection_stress(z)
    assert np.allclose(om @ np.ones(6), 0) and np.linalg.eigvalsh(om).min() > -1e-12
    affine = np.stack([z @ rng.normal(size=(3, 3)) + rng.normal(size=3) for _ in range(4)])
    other = rng.normal(size=(4, 6, 3))
    assert np.allclose(ci.stress_values(affine, om), 0, atol=1e-10) and ci.stress_values(other, om).min() > 1e-3
    d2 = ci.sq_distances(other)
    off = om - np.diag(np.diag(om))
    assert np.allclose(ci.stress_values(other, om), -0.5 * np.einsum("ij,kij->k", off, d2))
