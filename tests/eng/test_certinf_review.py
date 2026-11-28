"""Tests added in answer to the independent review of Phase II (docs/engineering/phase2/REVIEW_A.md): one test per
finding that concerns the library, with the referee's counterexamples kept as tests, and tests of Theorem 5.4
(draws from the extremal ensemble)."""
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from metricchain_eng import certinf as ci  # noqa: E402


# ------------------------------------------------------------------------------------------------ C1, K2
def _gap_instance(seed=0, n=8, gamma=5.0):
    rng = np.random.default_rng(seed)
    pi = rng.dirichlet(np.ones(n))
    f, phi = rng.uniform(-1, 1, n), rng.uniform(-1, 1, (n, 1))
    l, u = pi, gamma * pi
    b = l @ np.column_stack([np.ones(n), phi, f])
    G = float((u - l).sum())
    region = ci.Box([float(pi @ phi[:, 0])], 0.05)
    exact = ci.interval(ci.box_problem(l, u, f, phi, region))["hi"]
    idx = rng.choice(n, size=2000, p=(u - l) / G)
    return b, G, f[idx], phi[idx], region, exact


def test_gap_certificate_honours_the_declaration():
    b, G, f, phi, region, exact = _gap_instance()
    tr, va = slice(0, 1000), slice(1000, None)
    plain = ci.Declared(-1, 1, [-1], [1], U_max=math.inf)
    run = lambda d, bb=b, gg=G, ff=f: ci.certify_upper_gap(bb, gg, ff[tr], phi[tr], ff[va], phi[va], region, d, 0.05)  # noqa: E731
    base = run(plain)
    assert base.status == "certified" and exact - 1e-9 <= base.value < exact + 0.25
    assert run(ci.Declared(-1, 1, [-1], [1], U_max=math.inf, iid=False)).status == "abstain"
    assert run(ci.Declared(-0.2, 0.2, [-1], [1], U_max=math.inf)).status == "void"            # a draw outside the range
    assert run(ci.Declared(-1, 1, [-1], [1], U_max=math.inf, beta=0.5)).status == "void"       # not a declaration
    assert abs(run(ci.Declared(-1, 1, [-1], [1], U_max=math.inf, f_err=0.1)).value - base.value - 0.1) < 1e-12
    for d in (ci.Declared(-1, 1, [-1], [1], U_max=math.inf, eps_tv=0.2), ci.Declared(-1, 1, [-1], [1], U_max=math.inf, beta=3.0),
              ci.Declared(-1, 1, [-1], [1], U_max=math.inf, phi_err=0.1)):
        out = run(d)
        assert out.status in ("certified", "trivial") and out.value >= base.value - 1e-12     # an allowance never tightens
    bad = f.copy()
    bad[1500] = math.nan
    assert run(plain, ff=bad).status == "void"
    assert run(plain, gg=-1.0).status == "void"


def test_gap_zero_is_handled_explicitly():
    b, G, f, phi, region, _ = _gap_instance()
    d = ci.Declared(-1, 1, [-1], [1], U_max=math.inf)
    out = ci.certify_upper_gap(b, 0.0, f[:10], phi[:10], f[10:20], phi[10:20], region, d, 0.05)
    assert out.status == "certified" and out.n_valid == 0 and abs(out.value - b[-1] / b[0]) < 1e-15
    zero = ci.certify_upper_gap(np.zeros(3), 0.0, f[:10], phi[:10], f[10:20], phi[10:20], region, d, 0.05)
    assert zero.status == "abstain"
    assert ci.s3_interval(b, 0.0, f[:50], phi[:50], region, 0.05)["status"] == "abstain"


# ------------------------------------------------------------------------------------------------ C2, K3
def test_inconsistency_of_a_class_with_l_zero():
    # the referee's instance: X = {0, 1}, l = 0, u = 1, phi = (0, 1), R = [2, 3]: Phi <= 0 identically, I is empty
    region = ci.Box([2.5], 0.5)
    P = ci.box_problem([0, 0], [1, 1], [0.0, 1.0], [[0.0], [1.0]], region)
    assert ci.interval(P)["empty"]
    val, eta = ci.find_inconsistency(P)
    assert val > 0.9 and eta[0] < 0
    assert ci.find_inconsistency(ci.box_problem([1e-3, 1e-3], [1, 1], [0.0, 1.0], [[0.0], [1.0]], region))[0] > 0
    ok = ci.box_problem([0, 0], [1, 1], [0.0, 1.0], [[0.0], [1.0]], ci.Box([0.5], 0.1))
    assert not ci.interval(ok)["empty"] and ci.find_inconsistency(ok)[0] <= 1e-12
    assert ci.find_inconsistency(ci.box_problem([1, 1], [2, 2], [0.0, 1.0], np.zeros((2, 0)), ci.Box()))[0] == 0.0
    # from a sample: the declared range decides with certainty, or the certificate abstains
    s = ci.Sample(f=[0, 1, 0, 1], phi=[[0], [1], [0], [1]], L=0.0, U=1.0)
    out = ci.certify_inconsistent(s, s, region, ci.Declared(0, 1, [0], [1], U_max=1.0), 0.05)
    assert out.status == "certified" and "deterministic" in out.note
    out = ci.certify_inconsistent(s, s, region, ci.Declared(0, 1, [0], [3], U_max=1.0), 0.05)
    assert out.status == "abstain" and "l = 0" in out.note
    # a disc and a declared square that do not meet, separated only along a diagonal
    d2 = ci.Declared(0, 1, [0, 0], [1, 1], U_max=1.0)
    assert ci.range_excludes_region(ci.Ellipsoid([1.8, 1.8], np.eye(2), 1.0), d2) is not None
    assert ci.range_excludes_region(ci.Ellipsoid([1.6, 1.6], np.eye(2), 1.0), d2) is None


# ------------------------------------------------------------------------------------------------ C3
def test_sequential_bound_is_not_exact_for_monotone_targets_on_three_state_sites():
    """The referee's counterexample: two sites with three ordered states, g = 1{x1 + x2 >= 3}."""
    pis = [np.array([0.0401, 0.5001, 0.4598]), np.array([0.3815, 0.4694, 0.1491])]
    us = [1.0038, 1.0722]
    states = [(a, b) for a in range(3) for b in range(3)]
    pi = np.array([pis[0][a] * pis[1][b] for a, b in states])
    edges, C = [], []
    for i, x in enumerate(states):
        for j, y in enumerate(states):
            if i != j and (x[0] == y[0]) != (x[1] == y[1]):          # the two configurations differ at one site
                edges.append((i, j))
                C.append(math.exp(us[0 if x[0] != y[0] else 1]))
    g = np.array([1.0 if a + b >= 3 else 0.0 for a, b in states])
    _, exact = ci.lp_ratio_class(pi, edges, C, g)
    terminal = (np.arange(5) >= 3).astype(float)
    seq = ci.sequential_upper(pis, us, [[0, 1, 2], [0, 1, 2]], terminal)
    rev = ci.sequential_upper(pis[::-1], us[::-1], [[0, 1, 2], [0, 1, 2]], terminal)
    assert abs(exact - 0.632638) < 1e-3 and abs(seq - 0.671526) < 1e-3 and abs(rev - 0.634084) < 1e-3
    assert seq > exact + 0.03 and rev > exact + 1e-4                 # sound, and strictly above the supremum


# ------------------------------------------------------------------------------------------------ K1
def test_non_finite_draws_void_the_certificate():
    rng = np.random.default_rng(1)
    s = ci.Sample(f=rng.uniform(0, 1, 200), phi=np.zeros((200, 0)), L=1.0, U=2.0)
    d = ci.Declared(0, 1, [], [], U_max=2.0)
    tr, va = slice(0, 100), slice(100, None)
    good = ci.certify_upper(s.part(tr), s.part(va), ci.Box(), d, 0.05)
    assert good.status == "certified" and good.value < 1.0
    for field in ("f", "U", "L"):
        vals = dict(f=s.f.copy(), phi=s.phi, L=s.L.copy(), U=s.U.copy())
        vals[field][150] = math.nan
        bad = ci.Sample(**vals)
        assert ci.certify_upper(bad.part(tr), bad.part(va), ci.Box(), d, 0.05).status == "void"
        assert ci.certified_interval(bad, ci.Box(), d, 0.1)["status"] == "void"
    assert ci.certify_upper(s.part(tr), s.part(va), ci.Box(), d, 1.5).status == "void"            # not a level
    assert ci.certify_upper(s.part(tr), s.part(va), ci.Box(), ci.Declared(0, 1, [], [], U_max=math.nan), 0.05).status == "void"


# ------------------------------------------------------------------------------------------------ K4
def _polygon_primal(f, phi, centre, radius, sign):
    """max of sign * p.f over probabilities p with p.phi in the regular 720-gon of inradius ``radius``."""
    ang = 2 * math.pi * np.arange(720) / 720
    dirs = np.column_stack([np.cos(ang), np.sin(ang)])
    res = linprog(-sign * f, A_ub=dirs @ phi.T, b_ub=radius + dirs @ centre, A_eq=np.ones((1, f.size)), b_eq=[1.0],
                  bounds=[(0, None)] * f.size, method="highs")
    assert res.status == 0
    return -res.fun


def test_model_free_interval_on_a_disc():
    """l = 0 and a region that is not a box: the descent route alone used to stall (errors up to 0.25)."""
    rng = np.random.default_rng(5)
    for _ in range(8):
        n = 40
        f, phi = rng.uniform(-1, 1, n), rng.uniform(-1, 1, (n, 2))
        centre, rad = phi[rng.choice(n, 3, replace=False)].mean(axis=0), 0.15
        out = ci.interval(ci.Problem(f, phi, Lw=0.0, Gw=1.0, region=ci.Ellipsoid(centre, np.eye(2), rad)))
        hi_in, hi_out = (_polygon_primal(f, phi, centre, r, 1.0) for r in (rad * math.cos(math.pi / 720), rad))
        lo_in, lo_out = (-_polygon_primal(f, phi, centre, r, -1.0) for r in (rad * math.cos(math.pi / 720), rad))
        assert hi_out - hi_in < 1e-4 and lo_in - lo_out < 1e-4      # the two polygons bracket the disc tightly
        assert hi_in - 1e-7 <= out["hi"] <= hi_out + 1e-7
        assert lo_out - 1e-7 <= out["lo"] <= lo_in + 1e-7
        assert not out["empty"]
    far = ci.interval(ci.Problem(f, phi, Lw=0.0, Gw=1.0, region=ci.Ellipsoid([5.0, 5.0], np.eye(2), 0.15)))
    assert far["empty"]


def test_cutting_planes_agree_with_the_programme():
    rng = np.random.default_rng(6)
    for lw in (0.0, 0.3):
        f, phi = rng.uniform(-1, 1, 60), rng.uniform(-1, 1, (60, 2))
        P = ci.Problem(f, phi, Lw=lw, Gw=1.0, region=ci.Box(phi.mean(axis=0), 0.1))
        assert abs(ci.solve_upper(P, "lp")[0] - ci.solve_upper(P, "polish")[0]) < 1e-7
    g = ci.tau_grad(ci.Problem(f, phi, Lw=0.0, Gw=1.0, region=ci.Ellipsoid([0.0, 0.0], 0.01 * np.eye(2))), np.array([0.3, -0.2]))
    assert np.all(np.isfinite(g))


# ------------------------------------------------------------------------------------------------ Theorem 5.4
def _tilt_instance(seed=11, n=30):
    rng = np.random.default_rng(seed)
    pi = rng.dirichlet(np.ones(n))
    f, phi = rng.uniform(-1, 1, n), rng.uniform(-1, 1, (n, 1))
    rho = rng.uniform(0.5, 2.0, n)
    l, u = pi * np.exp(-rho), pi * np.exp(rho)
    region = ci.Box([float(pi @ phi[:, 0])], 0.05)
    P = ci.box_problem(l, u, f, phi, region)
    out = ci.interval(P)
    return rng, l, u, f, phi, region, P, out["eta_hi"], out["hi"]


def test_tilted_score_identity():
    """Theorem 5.4(i): (sum of the extremal weights) x E_{p0}[tilted score] = Psi(tau, eta), at every tau."""
    _, l, u, f, phi, region, P, eta, vplus = _tilt_instance()
    for tau0 in (vplus + 0.03, vplus - 0.2):
        om = np.where(ci.tilt_indicator(f, phi, region, eta, tau0), u, l)
        for tau in (tau0, tau0 + 0.1, tau0 + 0.7, tau0 - 0.15, tau0 - 0.6):
            assert abs(om @ ci.tilted_score(f, phi, l / u, region, eta, tau0, tau) - ci.psi(P, tau, eta)) < 1e-12
        for a, b in ((tau0, tau0 + 0.05), (tau0 + 0.05, tau0 + 0.4)):                           # non-increasing in tau
            assert np.all(ci.tilted_score(f, phi, l / u, region, eta, tau0, b) <= ci.tilted_score(f, phi, l / u, region, eta, tau0, a) + 1e-15)


def test_tilted_certificate_is_valid_and_needs_no_bound_on_the_envelope():
    rng, l, u, f, phi, region, P, eta, vplus = _tilt_instance()
    d = ci.Declared(-1, 1, [-1], [1], U_max=math.inf)                 # no bound on u/pi is declared
    tau0 = vplus + 0.03
    om = np.where(ci.tilt_indicator(f, phi, region, eta, tau0), u, l)
    p0 = om / om.sum()
    vals = []
    for _ in range(200):
        idx = rng.choice(f.size, size=4000, p=p0)
        out = ci.certify_upper_tilted(f[idx], phi[idx], (l / u)[idx], region, eta, tau0, d, 0.05)
        assert out.status in ("certified", "trivial") and out.value >= tau0 - 1e-12
        vals.append(out.value)
    vals = np.array(vals)
    assert np.sum(vals < vplus - 1e-9) <= 20                          # at most delta, up to the binomial spread
    assert np.median(vals) < vplus + 0.15
    # a pilot below the root is still valid; the estimate of the root from tilted draws is close
    low = vplus - 0.1
    om = np.where(ci.tilt_indicator(f, phi, region, eta, low), u, l)
    idx = rng.choice(f.size, size=20000, p=om / om.sum())
    root, sd = ci.tilted_root(f[idx], phi[idx], (l / u)[idx], region, eta, low)
    assert abs(root - vplus) < 0.05 and 0 < sd < 4
    misses = 0
    for _ in range(100):
        idx = rng.choice(f.size, size=2000, p=om / om.sum())
        misses += ci.certify_upper_tilted(f[idx], phi[idx], (l / u)[idx], region, eta, low, d, 0.05).value < vplus - 1e-9
    assert misses <= 12
    # guards
    assert ci.certify_upper_tilted(f[idx], phi[idx], 1.5, region, eta, low, d, 0.05).status == "void"
    assert ci.certify_upper_tilted(f[idx], phi[idx], (l / u)[idx], region, eta, low,
                                   ci.Declared(-1, 1, [-1], [1], U_max=math.inf, iid=False), 0.05).status == "abstain"
    assert ci.certify_upper_tilted(f[idx], phi[idx], (l / u)[idx], region, eta, 2.0, d, 0.05).status == "trivial"
    lo = ci.certify_lower_tilted(f[idx], phi[idx], (l / u)[idx], region, eta, 0.0, d, 0.05)
    assert lo.status in ("certified", "trivial") and lo.value <= 0.0 + 1e-12


def test_tilted_draws_do_not_pay_the_envelope_ratio():
    """The hard instance of Theorem 6.1(a) at ratio 1000: reference draws certify nothing useful from 2000 draws,
    draws from the extremal ensemble come within a few hundredths of V+."""
    gamma = 1000.0
    a = 1.0 / gamma
    vplus = gamma * a / (1 + (gamma - 1) * a)
    rng = np.random.default_rng(3)
    n = 2000
    d = ci.Declared(0, 1, [], [], U_max=gamma)
    nothing = np.zeros((n, 0))
    ref, til = [], []
    for _ in range(100):
        s = ci.Sample(f=(rng.random(n) < a).astype(float), phi=nothing, L=1.0, U=gamma)
        ref.append(ci.certify_upper(s.part(slice(0, 1)), s, ci.Box(), d, 0.05).value)        # no multiplier to train
        y = (rng.random(n) < vplus).astype(float)                                            # the extremal ensemble
        til.append(ci.certify_upper_tilted(y, nothing, 1.0 / gamma, ci.Box(), np.zeros(0), 0.5, d, 0.05).value)
    ref, til = np.array(ref), np.array(til)
    assert np.sum(ref < vplus) <= 12 and np.sum(til < vplus) <= 12
    assert np.median(til) - vplus < 0.08
    assert np.median(ref) - vplus > 0.3


def test_training_helper_for_pilots():
    rng, l, u, f, phi, region, P, eta, vplus = _tilt_instance()
    pi = np.sqrt(l * u)
    pi = pi / pi.sum()
    idx = rng.choice(f.size, size=5000, p=pi)
    s = ci.Sample(f[idx], phi[idx], (l / pi)[idx], (u / pi)[idx])
    d = ci.Declared(-1, 1, [-1], [1], U_max=float((u / pi).max()))
    tau, eta_hat, se = ci.train_multipliers(s, region, d)
    assert math.isfinite(tau) and eta_hat.shape == (1,) and 0 < se < 1
    assert abs(tau - vplus) < 10 * se + 0.2
