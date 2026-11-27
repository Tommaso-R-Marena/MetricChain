"""Test harness of the Geometric Inference division (cycle 1: second-moment rigidity).

Every test checks a statement of docs/geometry/ENSEMBLE_RIGIDITY.md on synthetic instances, in
exact arithmetic where the statement is an exact computation.  A test returns (ok, message).
`GEOM_MUT=<name>` plants one error (see mutation_checks.py): the corresponding test must fail.

Usage:  python3 run_checks.py [--quick] [--only NAME]
"""
import os
import sys
import time
import itertools
import numpy as np
from fractions import Fraction

from geomlib import (chain, edm, stack, sym_index, quad_row, sym_from_vec, edge_vectors,
                     conic_matrix, kabsch_rmsd)
import exact_conic_rank
import exact_jacobian_rank
import exact_4d_extreme
import demix as demix_mod
import hierarchy_example
import exact_nonlinear_threshold
import explore_below
import matroid_connectivity
import torsion_sharpness
import local_data_bounds
import third_moment

MUT = os.environ.get("GEOM_MUT", "")
QUICK = "--quick" in sys.argv
TESTS = []


def test(f):
    TESTS.append(f)
    return f


def rand_ensemble(K, n, rng, theta=np.deg2rad(111.0)):
    w = rng.dirichlet(np.ones(K) * 3)
    Xs = [chain(n, rng.uniform(-np.pi, np.pi, n - 3), theta=theta) for _ in range(K)]
    return w, Xs


def nullity(A, ncols, tol=1e-9):
    s = np.linalg.svd(A, compute_uv=False)
    return ncols - int((s > tol * s[0]).sum())


# ------------------------------------------------------------------ section 2, 3
@test
def stacking_identity():
    """Lemma 2.1: M(mu) = EDM of the stacked configuration."""
    rng = np.random.default_rng(1)
    worst = 0.0
    for K, n in [(1, 6), (2, 9), (3, 14), (5, 20)]:
        w, Xs = rand_ensemble(K, n, rng)
        M = sum(wk * edm(X) for wk, X in zip(w, Xs))
        Z = np.hstack([(wk if MUT == "stack_no_sqrt" else np.sqrt(wk)) * X for wk, X in zip(w, Xs)])
        worst = max(worst, np.abs(M - edm(Z)).max())
    return worst < 1e-10, f"max deviation {worst:.2e}"


@test
def obstruction_collinear():
    """Proposition 3.1(a): D(X) is the mean of the three scaled collinear coordinate configurations."""
    rng = np.random.default_rng(2)
    X = rng.normal(size=(9, 3))
    scale = 1.0 if MUT == "collinear_no_scale" else np.sqrt(3)
    M = sum(edm(scale * X[:, [c]]) for c in range(3)) / 3
    dev = np.abs(M - edm(X)).max()
    return dev < 1e-10, f"deviation {dev:.2e}"


@test
def obstruction_rotation():
    """Proposition 3.1(b),(c): a rotated stack has the same M; its blocks violate the bond
    constraints (generically), so the rotated mixture is not an ensemble of chains."""
    rng = np.random.default_rng(3)
    w, Xs = rand_ensemble(2, 12, rng)
    Z = stack(Xs, w)
    Q, _ = np.linalg.qr(rng.normal(size=(6, 6)))
    Z2 = Z @ Q
    same = np.abs(edm(Z) - edm(Z2)).max()
    blocks = [Z2[:, :3], Z2[:, 3:]]
    # bond lengths of block k would have to be constant (= sqrt(w'_k)) along the chain
    spread = max(np.ptp(np.linalg.norm(B[1:] - B[:-1], axis=1)) for B in blocks)
    return same < 1e-10 and spread > 1e-2, f"M deviation {same:.1e}; bond-length spread of rotated blocks {spread:.3f}"


@test
def four_atom_mixture():
    """Example 3.3: a non-planar 4-atom chain has the M of a cis/trans mixture."""
    theta = np.deg2rad(111.0)
    t = 1.1
    D = edm(chain(4, [t], theta=theta))
    Dcis, Dtrans = edm(chain(4, [0.0], theta=theta)), edm(chain(4, [np.pi], theta=theta))
    wc = (1 + np.cos(t)) / 2
    if MUT == "four_atom_weights":
        wc = 1 - wc
    dev = np.abs(wc * Dcis + (1 - wc) * Dtrans - D).max()
    return dev < 1e-10, f"deviation {dev:.2e}"


@test
def bcc_example():
    """Example 3.2: a freely jointed chain with bond vectors (+-1,+-1,+-1)/sqrt 3 is a mixture of
    three collinear freely jointed chains."""
    rng = np.random.default_rng(4)
    U = rng.choice([-1.0, 1.0], size=(10, 3)) / np.sqrt(3)
    X = np.vstack([np.zeros(3), np.cumsum(U, axis=0)])
    rods = [np.sqrt(3) * X[:, [c]] for c in range(3)]
    unit = all(np.allclose(np.abs(R[1:] - R[:-1]), 1.0) for R in rods)
    dev = np.abs(sum(edm(R) for R in rods) / 3 - edm(X)).max()
    return unit and dev < 1e-10, f"rods have unit bonds: {unit}; deviation {dev:.2e}"


# ------------------------------------------------------------------ section 4
@test
def affine_flex_midpoint():
    """Theorem A (iii)=>(ii): a quadric through the edge directions gives two chains with the same
    bond data whose squared distances average to those of X (4 atoms: 5 edges, dim Sym(3) = 6)."""
    rng = np.random.default_rng(5)
    X = chain(4, [0.8])
    A = conic_matrix(X)
    idx = sym_index(3)
    S = sym_from_vec(np.linalg.svd(A)[2][-1], 3, idx)
    t = 0.5 / np.abs(np.linalg.eigvalsh(S)).max()
    def image(tt):
        lam, Q = np.linalg.eigh(np.eye(3) + tt * S)
        return X @ (Q * np.sqrt(lam)) @ Q.T
    Xp, Xm = image(t), image(-2 * t if MUT == "midpoint_asymmetric" else -t)
    E0 = [(0, 1), (1, 2), (2, 3), (0, 2), (1, 3)]
    keep = max(abs(edm(Y)[i, j] - edm(X)[i, j]) for Y in (Xp, Xm) for (i, j) in E0)
    mid = np.abs((edm(Xp) + edm(Xm)) / 2 - edm(X)).max()
    moved = abs(edm(Xp)[0, 3] - edm(X)[0, 3])
    return keep < 1e-10 and mid < 1e-10 and moved > 1e-3, \
        f"bond data preserved to {keep:.1e}; midpoint deviation {mid:.1e}; d14^2 moved by {moved:.3f}"


@test
def conic_threshold_float():
    """Theorem C(b),(d): dim N(z) = max(K-1, dim Sym(3K) - (2n-3)) at bond angle 111 degrees."""
    rng = np.random.default_rng(6)
    bad = []
    for K in (1, 2, 3) if QUICK else (1, 2, 3, 4):
        n0 = -(-(9 * K * K + K + 8) // 4)
        if MUT == "threshold_minus_one":
            n0 -= 1
        dim = 3 * K * (3 * K + 1) // 2
        for n in (n0 - 1, n0, n0 + 2):
            w, Xs = rand_ensemble(K, n, rng)
            Z = stack(Xs, w)
            A = conic_matrix(Z, angles=(MUT != "drop_angle_edges"))
            nul = nullity(A, dim)
            want = (K - 1) if n >= n0 else dim - (2 * n - 3)
            if nul != want:
                bad.append((K, n, nul, want))
    return not bad, f"mismatches {bad}" if bad else "nullities as predicted"


@test
def conic_threshold_exact():
    """Theorem C(b): exact rank D_K at n0(K), two bond geometries, bond+angle and bonds only."""
    Kmax = 4 if QUICK else 8
    bad = []
    for geometry in ("rational", "tetrahedral"):
        for angles in (True, False):
            for K in range(1, Kmax + 1):
                n, dim, r, s, good = exact_conic_rank.check(K, geometry, angles)
                if not good:
                    bad.append((geometry, angles, K, r))
    return not bad, f"failures {bad}" if bad else f"rank D_K attained for K <= {Kmax}"


@test
def trivial_quadrics_only():
    """Theorem B, hypothesis (CC) made explicit: at the threshold the null space of the conic
    system is spanned by sum_k s_k E_k with sum_k w_k s_k = 0."""
    rng = np.random.default_rng(7)
    K, n = 3, 23
    w, Xs = rand_ensemble(K, n, rng)
    Z = stack(Xs, w)
    idx = sym_index(3 * K)
    A = conic_matrix(Z)
    null = np.linalg.svd(A)[2][len(idx) - (K - 1):]
    worst = 0.0
    for v in null:
        S = sym_from_vec(v, 3 * K, idx)
        s = [S[3 * k, 3 * k] for k in range(K)]
        T = np.kron(np.diag(s), np.eye(3))
        worst = max(worst, np.abs(S - T).max(), abs(sum(wk * sk for wk, sk in zip(w, s))))
    return worst < 1e-7, f"distance of the null space from the trivial quadrics {worst:.1e}"


@test
def demix_recovers():
    """Proposition 6.1: DEMIX returns the ensemble at and above the threshold (exact data)."""
    rng = np.random.default_rng(8)
    worst = 0.0
    for K, n in [(2, 12), (3, 23), (3, 28)] + ([] if QUICK else [(4, 39)]):
        w, Xs = rand_ensemble(K, n, rng)
        M = sum(wk * edm(X) for wk, X in zip(w, Xs))
        edges, lengths = demix_mod.chain_edges(n)
        out = demix_mod.demix(M, edges, lengths)
        if not out["ok"]:
            return False, f"K={K} n={n}: {out['reason']}"
        if MUT == "demix_wrong_block":
            out["states"] = [np.roll(S, 1, axis=1) * np.array([1.0, 1.0, 1.3]) for S in out["states"]]
        e, dw = demix_mod.match_error(Xs, w, out)
        worst = max(worst, e, dw)
    return worst < 1e-5, f"max state RMSD / weight error {worst:.2e}"


@test
def demix_refuses_below_threshold():
    """Below the threshold the certificate (nullity = K - 1) fails and DEMIX refuses."""
    rng = np.random.default_rng(9)
    w, Xs = rand_ensemble(2, 11, rng)
    M = sum(wk * edm(X) for wk, X in zip(w, Xs))
    edges, lengths = demix_mod.chain_edges(11)
    out = demix_mod.demix(M, edges, lengths)
    return (not out["ok"]) and out["certificate"]["nullity"] == 2, str(out.get("reason"))


# ------------------------------------------------------------------ section 5.3, 5.4
@test
def jacobian_exact():
    """Theorem H: exact full column rank at n = 2K+3 (complete) and w = K+3, n = (K^2+3K+4)/2."""
    Kmax = 4 if QUICK else 7
    bad = []
    for geometry in ("rational", "tetrahedral"):
        for K in range(2, Kmax + 1):
            P, D, r, good = exact_jacobian_rank.check(K, 2 * K + 3, 2 * K + 3, geometry)
            if not good:
                bad.append(("complete", geometry, K, r, P))
        for K in range(1, Kmax + 1):
            w = K + 2 if MUT == "band_K_plus_2" else K + 3
            n = (K * K + 3 * K + 4) // 2
            P, D, r, good = exact_jacobian_rank.check(K, n, w, geometry)
            if not good:
                bad.append(("band", geometry, K, r, P))
    return not bad, f"failures {bad[:4]}" if bad else f"full column rank for K <= {Kmax}"


@test
def band_K_plus_2_never():
    """Theorem H(b), necessity: for w = K+2 (K >= 2) the data are fewer than the parameters."""
    bad = []
    for K in range(2, 12):
        w = K + 2
        for n in range(w + 1, 400):
            data = sum(n - s for s in range(3, w + 1))
            if data >= K * (n - 2) - 1:
                bad.append((K, n))
                break
    return not bad, f"counterexamples to the count {bad}" if bad else "data < parameters for all n < 400"


@test
def trilateration_band():
    """Theorem F': with separation 3K+1 the stacked configuration is determined by trilateration
    in R^{3K} (K = 2: every 7 consecutive stacked points affinely independent; the next point is
    then determined by its distances to them)."""
    rng = np.random.default_rng(10)
    K, n = 2, 14
    w, Xs = rand_ensemble(K, n, rng)
    Z = stack(Xs, w)
    m = 3 * K
    worst_gap, worst_err = np.inf, 0.0
    for i in range(n - m - 1):
        P = Z[i:i + m + 1]
        B = (P[1:] - P[0]).T                      # m x m
        worst_gap = min(worst_gap, np.linalg.svd(B, compute_uv=False)[-1])
        d2 = ((P - Z[i + m + 1]) ** 2).sum(1)
        # solve for the point from its squared distances to the m+1 points
        rhs = 0.5 * ((P[1:] ** 2).sum(1) - (P[0] ** 2).sum() - d2[1:] + d2[0])
        y = np.linalg.solve((P[1:] - P[0]), rhs)
        worst_err = max(worst_err, np.abs(y - Z[i + m + 1]).max())
    return worst_gap > 1e-4 and worst_err < 1e-7, f"min simplex singular value {worst_gap:.2e}; reconstruction error {worst_err:.1e}"


@test
def lemma_R_reachability():
    """Lemma R: m0 = max(2, ceil(pi/beta)) steps of angle alpha reach every point of the sphere,
    and m0 - 1 steps do not (checked on the interval recursion for the angular distance)."""
    def reach(alpha, m, grid=20001):
        rho = np.linspace(0, np.pi, grid)
        cur = np.abs(rho - alpha) < np.pi / (grid - 1)          # J_1 = {alpha}
        for _ in range(m - 1):
            nxt = np.zeros(grid, bool)
            for r in rho[cur]:
                lo, hi = abs(r - alpha), min(r + alpha, 2 * np.pi - r - alpha)
                nxt |= (rho >= lo - 1e-9) & (rho <= hi + 1e-9)
            cur = nxt
        return cur.mean()
    bad = []
    for deg in (40.0, 69.0, 70.53, 90.0, 100.0, 125.0, 150.0):
        alpha = np.deg2rad(deg)
        beta = min(alpha, np.pi - alpha)
        m0 = max(2, int(np.ceil(np.pi / beta - 1e-12)))
        if MUT == "lemma_R_minus_one":
            m0 -= 1
        full = reach(alpha, m0) > 0.999
        short = reach(alpha, m0 - 1) > 0.999 if m0 > 1 else False
        if not full or short:
            bad.append((deg, m0, full, short))
    return not bad, f"failures {bad}" if bad else "full sphere exactly from m0 steps on"


@test
def conic_rank_profile():
    """Theorem C(c): the rank r_N of the conic system of K generic chains with N bonds is
    2N - 1 for N <= 3K, has non-increasing increments, and grows strictly until it is D_K
    (numerically it is min(2N - 1, D_K): the sharp profile of (b), (d))."""
    rng = np.random.default_rng(11)
    bad = []
    for K in (1, 2) if QUICK else (1, 2, 3):
        dim = 3 * K * (3 * K + 1) // 2
        DK = dim - (K - 1)
        nmax = -(-(9 * K * K + K + 8) // 4) + 3
        w, Xs = rand_ensemble(K, nmax, rng, theta=np.deg2rad(rng.uniform(95.0, 125.0)))
        Z = stack(Xs, w)
        ranks = []
        for n in range(2, nmax + 1):                    # N = n - 1 bonds
            A = conic_matrix(Z[:n], angles=(MUT != "profile_drop_angle_edges"))
            ranks.append(dim - nullity(A, dim))
        inc = [b - a for a, b in zip(ranks, ranks[1:])]
        free = all(ranks[N - 1] == 2 * N - 1 for N in range(1, min(3 * K, len(ranks)) + 1))
        concave = all(x >= y for x, y in zip(inc, inc[1:]))
        strict = all(d >= 1 for r, d in zip(ranks, inc) if r < DK)
        sharp = all(r == min(2 * N - 1, DK) for N, r in enumerate(ranks, start=1))
        if not (free and concave and strict and sharp and ranks[-1] == DK):
            bad.append((K, ranks))
    return not bad, f"profiles violate (i)-(iii) or min(2N-1, D_K): {bad}" if bad else \
        "r_N = min(2N - 1, D_K); increments non-increasing"


@test
def general_position_exact():
    """Hypothesis of Theorem F': every 3K + 1 consecutive stacked points of generic chains are
    affinely independent (exact, modulo a prime, at n0(K), together with (CC))."""
    import exact_general_position as G
    bad = []
    for geometry in ("rational", "tetrahedral"):
        for K in (1, 2) if QUICK else (1, 2, 3):
            n, s, good = G.check(K, geometry, extra=(1 if MUT == "general_position_one_more" else 0))
            if not good:
                bad.append((geometry, K, n))
    return not bad, f"failures {bad}" if bad else "every window of 3K + 1 stacked points affinely independent"


@test
def demix4_below_conic():
    """Proposition 6.2: the degree-4 certificate HF = K holds, and DEMIX-4 recovers the states by
    linear algebra, below the conic threshold (K = 2 at n = 11; K = 3 at n = 21); it refuses at
    K = 2, n = 10, where the rank-3 locus has a structural point at infinity (HF = 7)."""
    import demix4 as D4
    msgs, ok = [], True
    for K, n in ((2, 11), (3, 21)):
        good, info, errs = D4.demo(K, n, seed=7 * K + n, principal_only=(MUT == "demix4_principal_only"))
        ok &= good and info["HF"] == K
        msgs.append(f"K={K}, n={n}: HF={info['HF']}" + (f", RMSD {errs[0]:.0e}" if errs else ""))
    good, info, _ = D4.demo(2, 10, seed=3)
    ok &= (not good) and info["HF"] == 7
    msgs.append(f"K=2, n=10: HF={info['HF']} (refused)")
    return ok, "; ".join(msgs)


# ------------------------------------------------------------------ section 5.5

@test
def demix4_exact_witness():
    """Theorem I' (section 6.2): at rational witnesses, modulo a prime, the 4 x 4 minors span all
    quartic forms on L through the K states (K = 2, n = 11; K = 3, n = 17), or all those that
    are also singular at the structural point (K = 2, n = 10) -- Proposition 6.2 (b), (h)."""
    import exact_demix4 as X4
    mut = MUT == "demix4_exact_ignore_structural"       # planted error: claim h_4 = K at n = 6K - 2
    cases = [(2, 10, "rational"), (2, 10, "tetrahedral"), (2, 11, "rational"), (2, 11, "tetrahedral")]
    cases += [] if QUICK else [(3, 17, "rational")]
    ok, out = X4.self_test(), []
    for K, n, g in cases:
        proved, info = X4.certify(K, n, g, structural=not mut)
        ok &= proved
        out.append(f"K={K} n={n} {g[:3]}: rank_p {info['rank']} + jets {info['jets']} of {info['nmon']}")
    return ok, "; ".join(out)

@test
def nonlinear_threshold_exact():
    """Theorem I: for K = 2, n = 10 the rank <= 3 locus of P(L) has degree 7 = 1 + 1 + 5 (the two
    block projectors and the structural rank-2 point at infinity); for n = 11 degree 2.
    Groebner bases over F_32003 with Singular (the computation over Q is the proof; 80 s)."""
    import shutil
    if shutil.which("Singular") is None:
        return True, "SKIPPED: Singular is not installed (apt-get install singular)"
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        n10 = 11 if MUT == "threshold_I_at_eleven" else 10
        r10 = [exact_nonlinear_threshold.main(n10, seed, 32003) for seed in (0, 1)]
        r11 = exact_nonlinear_threshold.main(11, 0, 32003)
    want10 = [0, 0]
    # at n = 10 the script expects degree 7; planting n = 11 in its place still returns 0 there
    # (degree 2), so the mutation flips the expected degree instead
    if MUT == "threshold_I_at_eleven":
        ok = "DEG': '7'" in buf.getvalue()
    else:
        ok = r10 == want10 and r11 == 0 and buf.getvalue().count("'DEG': '7'") == 2
    return ok, "degree 7 at n = 10 (two witnesses), degree 2 at n = 11" if ok else buf.getvalue()[-300:]


@test
def two_states_below_threshold():
    """Section 5.5 [N]: at n = 8 a mixture of other chains reproduces the averaged data of a
    two-state ensemble (not identifiable among all ensembles); at n = 9 no such mixture is found."""
    r8 = explore_below.run(8, 0, 120 if QUICK else 200)
    r9 = explore_below.run(9, 0, 150 if QUICK else 250)
    mass8 = r8["max_mass_on_others"]
    if MUT == "below_claims_identifiable":
        ok = mass8 < 1e-6
    else:
        ok = (mass8 > 0.99 and r8.get("M_dev", 1) < 1e-9 and r8.get("bond_dev", 1) < 1e-9
              and abs(r9["max_mass_on_others"]) < 1e-9 and r9["others"] >= 1)
    return ok, (f"n=8: {r8.get('states')} other chains carry mass {mass8:.3f}, data deviation {r8.get('M_dev', float('nan')):.1e}; "
                f"n=9: {r9['others']} further chains, none can carry mass")


# ------------------------------------------------------------------ section 5.6, responses
@test
def matroid_patterns():
    """Theorem J: separations {3,4} give a connected matroid of full rank (exact witness), single
    separations are free; two rigid bodies: K_{3,3} bars connected, K_{2,2} free."""
    n = 11
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        seps = [3] if MUT == "single_separation_connected" else [3, 4]
        rk34, comps34 = matroid_connectivity.report("S", n, matroid_connectivity.pattern(n, seps))
        rk3, comps3 = matroid_connectivity.report("S", n, matroid_connectivity.pattern(n, [3]))
        rk5, comps5 = matroid_connectivity.report("S", n, matroid_connectivity.pattern(n, [5]))
    m33 = matroid_connectivity.two_body(3, 3)
    m22 = matroid_connectivity.two_body(2, 2)
    ok = (rk34 == n - 3 and len(comps34) == 1 and rk3 == n - 3 and len(comps3) == n - 3
          and rk5 == n - 5 and len(comps5) == n - 5 and m33 == (9, 6, 1) and m22[1] == 4 and m22[2] == 4)
    return ok, f"S={{3,4}}: rank {rk34}, {len(comps34)} component(s); S={{3}}: {len(comps3)} components; two triangles: {m33}"


@test
def kink_formula():
    """GEOMETRY-RES-0002: the small-angle Kabsch cost of a kink in the middle of an all-trans
    chain is a quarter of the coaxial cost I_red phi^2 (rod model), an eighth of min(I) phi^2."""
    a, b = torsion_sharpness.kink_test(400)
    target = 0.5 if MUT == "kink_half" else 0.25
    return abs(a - target) < 2e-3 and abs(b - target / 2) < 2e-3, f"cost / (I_red phi^2) = {a:.4f}, cost / (min I phi^2) = {b:.4f}"


# ------------------------------------------------------------------ section 7
def certificate_setup(K, n, rng):
    w, Xs = rand_ensemble(K, n, rng)
    Z = stack(Xs, w)
    B = np.hstack([np.ones((n, 1)), Z])
    Qb, _ = np.linalg.qr(B)
    Pi = Qb @ Qb.T
    Pperp = np.eye(n) - Pi
    return w, Xs, Z, (Pi if MUT == "certificate_wrong_projector" else Pperp)


@test
def dual_certificate():
    """Theorem G(a),(c): phi(X) = ||Pi_perp X||^2 = -1/2 <Pi_perp, D(X)> vanishes on the states, is
    positive on other chains, and its ensemble average is a linear function of M."""
    rng = np.random.default_rng(11)
    K, n = 2, 14
    w, Xs, Z, Pp = certificate_setup(K, n, rng)
    phi = lambda X: np.trace(X.T @ Pp @ X)
    at_states = max(abs(phi(X)) for X in Xs)
    others = [chain(n, rng.uniform(-np.pi, np.pi, n - 3)) for _ in range(200)]
    vals = np.array([phi(X) for X in others])
    lin = max(abs(phi(X) + 0.5 * (Pp * edm(X)).sum()) for X in others[:20])
    return at_states < 1e-9 and vals.min() > 1e-4 and lin < 1e-9, \
        f"phi at states {at_states:.1e}; min over 200 random chains {vals.min():.3f}; linearity defect {lin:.1e}"


@test
def quadratic_growth_local():
    """Theorem G(b), local part: under (CC), Pi_perp is positive definite on the flexes of each
    state modulo isometries (so phi grows quadratically away from the states)."""
    rng = np.random.default_rng(12)
    K, n = 2, 14
    w, Xs, Z, Pp = certificate_setup(K, n, rng)
    out = []
    for X in Xs:
        # tangent vectors: torsional velocity fields
        T = []
        for m in range(n - 3):
            ax = X[m + 2] - X[m + 1]
            ax /= np.linalg.norm(ax)
            V = np.zeros((n, 3))
            V[m + 3:] = np.cross(ax, X[m + 3:] - X[m + 2])
            T.append(V)
        # remove infinitesimal isometries
        iso = [np.tile(e, (n, 1)) for e in np.eye(3)] + [np.cross(e, X) for e in np.eye(3)]
        Bi = np.array([v.flatten() for v in iso]).T
        Qi, _ = np.linalg.qr(Bi)
        Tm = np.array([v.flatten() - Qi @ (Qi.T @ v.flatten()) for v in T]).T        # 3n x (n-3)
        Gm = Tm.T @ Tm
        Hm = sum((Tm.reshape(n, 3, -1)[:, c, :]).T @ Pp @ Tm.reshape(n, 3, -1)[:, c, :] for c in range(3))
        ev = np.linalg.eigvals(np.linalg.solve(Gm, Hm)).real
        out.append(ev.min())
    return min(out) > 1e-6, f"local growth constants {np.round(out, 5).tolist()}"


@test
def infinitesimal_identifiability_under_CC():
    """Theorem G(d), the bracketed step: under (CC) the Jacobian of the K-state parametrisation
    has full column rank (complete data)."""
    import explore_jacobian as ej
    K, n = 2, 12
    pairs = ej.band_pairs(n, n)
    Jm = ej.jac(K, n, pairs, seed=13)
    r = ej.rank(Jm)
    return r == K * (n - 3) + K - 1, f"rank {r} of {K * (n - 3) + K - 1}"


@test
def w2_exponent_is_sharp():
    """Theorem G(e): splitting a state symmetrically by eps changes M at order eps^2."""
    rng = np.random.default_rng(14)
    n = 14
    w = np.array([0.4, 0.6])
    t1, t2 = rng.uniform(-np.pi, np.pi, n - 3), rng.uniform(-np.pi, np.pi, n - 3)
    v = rng.normal(size=n - 3)
    M0 = w[0] * edm(chain(n, t1)) + w[1] * edm(chain(n, t2))
    ratios = []
    for eps in (1e-2, 5e-3, 2.5e-3):
        M = w[0] / 2 * (edm(chain(n, t1 + eps * v)) + edm(chain(n, t1 - eps * v))) + w[1] * edm(chain(n, t2))
        ratios.append(np.linalg.norm(M - M0) / eps ** 2)
    spread = np.ptp(ratios) / np.mean(ratios)
    return spread < 0.01, f"||dM||/eps^2 = {np.round(ratios, 4).tolist()}"


# ------------------------------------------------------------------ section 8
@test
def extreme_4d_witness():
    """Theorem D(b): exact rational 7-atom chain in R^4 with no quadric through its edge directions."""
    return exact_4d_extreme.main() == 0, "rank 10 of the quadric system, bond vectors span R^4"


@test
def six_atoms_have_a_quadric_in_4d():
    """Theorem D(a) at n = 6: a 4D chain has 9 edge directions and dim Sym(4) = 10, so it is never
    an extreme point (it decomposes into chains of lower rank)."""
    rng = np.random.default_rng(15)
    natoms = 7 if MUT == "six_atoms_is_seven" else 6
    gamma = -np.cos(np.deg2rad(111.0))
    U = [rng.normal(size=4)]
    U[0] /= np.linalg.norm(U[0])
    for a in range(1, natoms - 1):
        v = rng.normal(size=4)
        v -= (v @ U[-1]) * U[-1]
        v /= np.linalg.norm(v)
        U.append(gamma * U[-1] + np.sqrt(1 - gamma ** 2) * v)
    Y = np.vstack([np.zeros(4), np.cumsum(U, axis=0)])
    nul = nullity(conic_matrix(Y), 10)
    return nul >= 1, f"dimension of the space of quadrics {nul}"


@test
def hierarchy_instance():
    """Theorem E(d): globally rigid 6-atom chain, not second-moment rigid (two-state ensemble with the
    same averaged data on F)."""
    ok, checks = hierarchy_example.main(0, verbose=False)
    return ok, f"mixture deviation on F {checks['max_dev_mixture_vs_X_on_F']:.1e}; states differ from X on F by {checks['Xp_differs_from_X_on_F']:.2f}, {checks['Xm_differs_from_X_on_F']:.2f}"


@test
def hinge_conic_dimensions():
    """HINGE_ENSEMBLES.md, Proposition M3: dim N(z) = 10, 6, 3, 1 for two states that differ in
    1, 2, 3, 4 torsions (the Science division's count; (CC) only from four hinges on)."""
    import hinge_pairs as H
    rng = np.random.default_rng(21)
    want = {1: 10, 2: 6, 3: 3, 4: 1}
    if MUT == "hinge_cc_from_two":
        want[2] = 1
    bad = []
    for s in (1, 2, 3, 4):
        hinges = [4 + 5 * j for j in range(s)]
        n = hinges[-1] + 8
        X1, X2, _, _ = H.hinge_states(n, hinges, rng)
        dimN = nullity(conic_matrix(stack([X1, X2], [0.4, 0.6])), 21)
        if dimN != want[s]:
            bad.append((s, dimN, want[s]))
    return not bad, f"mismatches (s, dim, expected) {bad}" if bad else "dim N(z) = 10, 6, 3, 1"


@test
def hinge_cube():
    """HINGE_ENSEMBLES.md, Theorem M(b): two states that differ in two torsions; the eight chains
    of the cube are conformations and affine images of the stack, satisfy the parity relation
    and no other, and the linear programme leaves only the two states."""
    import hinge_pairs as H
    rng = np.random.default_rng(22)
    n, hinges = 11, [2, 5]
    X1, X2, _, _ = H.hinge_states(n, hinges, rng)
    w = np.array([0.3, 0.7])
    zc = stack([X1, X2], w)
    zc = zc - zc.mean(0)
    cand, ident, _ = H.cube_candidates(X1, X2, hinges, wrong_mirror=(MUT == "hinge_wrong_mirror"))
    keys = list(cand)
    Ds = {k: edm(Y) for k, Y in cand.items()}
    valid = all(H.e0_ok(Y) for Y in cand.values())
    aff = max(H.affine_residual(Y - Y.mean(0), zc) for Y in cand.values())
    parity = np.abs(sum((-1) ** sum(k) * Ds[k] for k in keys)).max()
    iu = np.triu_indices(n, 1)
    rank_aff = np.linalg.matrix_rank(np.array([Ds[k][iu] - Ds[keys[0]][iu] for k in keys[1:]]), tol=1e-8)
    M = w[0] * edm(X1) + w[1] * edm(X2)
    rngs = H.lp_unique([Ds[k] for k in keys], M, None, w)
    if rngs is None:
        return False, "linear programme infeasible"
    off = max(hi for k, (lo, hi) in zip(keys, rngs) if k not in ((0, 0, 0), (1, 1, 1)))
    w1 = rngs[keys.index((0, 0, 0))]
    ok = (ident < 1e-9 and valid and aff < 1e-8 and parity < 1e-8 and rank_aff == 6 and off < 1e-7
          and abs(w1[0] - w[0]) < 1e-7 and abs(w1[1] - w[0]) < 1e-7
          and np.abs(Ds[(1, 1, 1)] - edm(X2)).max() < 1e-8)
    return ok, (f"identities {ident:.0e}, affine images {aff:.0e}, parity {parity:.0e}, affine rank {rank_aff}, "
                f"weight off the states <= {off:.0e}, w1 in [{w1[0]:.4f}, {w1[1]:.4f}]")


@test
def hinge_candidates_exact():
    """HINGE_ENSEMBLES.md, Theorem M (b)(i) and (c): the scheme of candidate assemblies has degree
    8 (reduced) for two hinges and degree 2 for three, over Q (Singular)."""
    import shutil
    import subprocess
    if shutil.which("Singular") is None:
        return True, "SKIPPED: Singular is not installed (apt-get install singular)"
    here = os.path.dirname(os.path.abspath(__file__))
    cmd = [sys.executable, os.path.join(here, "exact_hinge_candidates.py")]
    if MUT == "hinge_two_candidates":
        cmd.append("--mutate")
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=here)
    return r.returncode == 0 and "ALL OK" in r.stdout, "degree 8 (two hinges, three instances), degree 2 (three hinges)" \
        if r.returncode == 0 else r.stdout[-300:]


@test
def hinge_halfturns():
    """HINGE_ENSEMBLES.md, Theorem M (b)(iii), (d) (the Science division's R22-1 (d)): the mixture
    is identifiable for generic torsion changes and for one half-turn, and not for two."""
    import hinge_halfturns as HH
    rng = np.random.default_rng(41)
    n, hinges = 14, [3, 7]
    w = np.array([0.37, 0.63])
    t1 = rng.uniform(-np.pi, np.pi, n - 3)
    res = {}
    for name, a, b in (("generic", 1.1, -1.9), ("one", np.pi, 1.3), ("two", np.pi, np.pi)):
        res[name] = HH.off_state_weight(n, t1, hinges, a, b, w)[0]
    want_two = 0.0 if MUT == "halfturns_identifiable" else 2 * w.min()
    ok = abs(res["generic"]) < 1e-6 and abs(res["one"]) < 1e-6 and abs(res["two"] - want_two) < 1e-4
    return ok, f"largest weight off the states: generic {res['generic']:.4f}, one half-turn {res['one']:.4f}, two {res['two']:.4f}"


@test
def hierarchy_exact_witness():
    """Theorem E(d): the exact rational witness (rigidity rank 12, indefinite stress matrix of
    rank 2, no conic through the constrained edge directions)."""
    import subprocess
    here = os.path.dirname(os.path.abspath(__file__))
    cmd = [sys.executable, os.path.join(here, "exact_hierarchy_witness.py")]
    if MUT == "hierarchy_semidefinite_neighbour":
        cmd.append("--mutate")
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=here)
    line = [l for l in r.stdout.splitlines() if l.startswith("sum of principal")]
    return r.returncode == 0 and "WITNESS OK" in r.stdout, (line[0] if line else r.stdout[-200:])


@test
def second_moment_of_rotated_data():
    """Corollary 9.1: E[(g x_i)(g x_j)^T] = <x_i, x_j>/3 * I for Haar-random g in O(3)
    (Monte Carlo, 2e5 rotations, tolerance 1e-2)."""
    rng = np.random.default_rng(16)
    a, b = rng.normal(size=3), rng.normal(size=3)
    N = 40000 if QUICK else 200000
    A = rng.normal(size=(N, 3, 3))
    Q, R = np.linalg.qr(A)
    Q = Q * np.sign(np.einsum("nii->ni", R))[:, None, :]
    ga, gb = Q @ a, Q @ b
    Mom = np.einsum("ni,nj->ij", ga, gb) / N
    dev = np.abs(Mom - (a @ b) / 3 * np.eye(3)).max()
    return dev < 2e-2, f"deviation {dev:.1e}"


# ------------------------------------------------------------------ LOCAL_DATA_STABILITY.md
@test
def local_data_bound_a():
    """Theorem K(a): s_7 <= pi sqrt(5 K(K+1)(2K+1)/3)/n for random configurations and patterns."""
    w = local_data_bounds.check_a(trials=20 if QUICK else 60)
    if MUT == "bound_a_too_strong":
        w *= 40.0          # pretend the bound were 40 times smaller
    return w <= 1.0, f"max of s_7 / bound = {w:.3f}"


@test
def local_data_bound_b():
    """Theorem K(b): one torsion move changes the range-K distances by at most
    2 sin(delta/2) b sqrt(T_K) in l2, and T_K <= K^4/48."""
    w, ex = local_data_bounds.check_b(trials=80 if QUICK else 200)
    tk = all(local_data_bounds.T(K) <= K ** 4 / 48 for K in range(3, 400))
    if MUT == "bound_b_too_strong":
        w *= 2.0           # pretend the bound were half as large
    return w <= 1.0 and tk, f"max ratio {w:.3f}; T_K <= K^4/48 for K < 400: {tk}; largest d_P/||dd|| seen {ex:.0f}"


@test
def helix_beam_law():
    """Theorem K(c) [N]: s_7 ~ c/n^2 on a helix (exponent within 0.1 of -2)."""
    e, c = local_data_bounds.helix_exponent()
    target = -1.0 if MUT == "helix_exponent_one" else -2.0
    return abs(e - target) < 0.1, f"exponent {e:.3f}, s_7 n^2 = {c:.1f}"


@test
def tube_bound_helix():
    """LOCAL_DATA_STABILITY.md, Theorem K(c): for an ideal helix (radius rho, rise h, L = n h)
    s_7(R)^2 <= 196 pi^4 rho^2 sum_F |x_j - x_k|^2 / (n L^4) for every pattern F."""
    import local_data_upper as U
    from local_data_bounds import rigidity_matrix
    bad, tight = [], []
    for tors, K in ((np.deg2rad(60.0), 4), (np.deg2rad(150.0), 5)):
        for n in (30, 60) if QUICK else (30, 60, 120):
            X = U.helix(n, tors)
            ax, h, rho, spread = U.helix_axis_frame(X)
            edges = [(i, j) for i in range(n) for j in range(i + 1, min(n, i + K + 1))]
            s7 = np.sort(np.linalg.svd(rigidity_matrix(X, edges), compute_uv=False))[6]
            sumsq = sum(((X[i] - X[j]) ** 2).sum() for i, j in edges)
            bound = np.sqrt(196 * np.pi ** 4 * rho ** 2 * sumsq / (n * (n * h) ** 4))
            if MUT == "tube_bound_too_strong":
                bound /= 50.0
            tight.append(bound / s7)
            if not (s7 <= bound and spread < 1e-8):
                bad.append((round(float(np.rad2deg(tors))), K, n, float(s7), float(bound)))
    return not bad, f"violations {bad}" if bad else f"s_7 <= bound; bound/s_7 between {min(tight):.0f} and {max(tight):.0f}"


@test
def local_procrustes_lemma():
    """Theorem L, Step 1: for two four-point windows with edge matrices P, Q and squared-distance
    errors eta, ||Q^T Q - P^T P||_F <= 2 ||eta|| and ||Q P^{-1} - R|| <= 2 ||eta|| / tau^2 with R the
    orthogonal polar factor; thin and thick windows, random and adversarial perturbations."""
    rng = np.random.default_rng(31)
    worst_gram, worst_polar = 0.0, 0.0
    for trial in range(400):
        U_, _ = np.linalg.qr(rng.normal(size=(3, 3)))
        V_, _ = np.linalg.qr(rng.normal(size=(3, 3)))
        sv = np.sort(rng.uniform(0.02, 2.5, 3))[::-1]
        if trial % 2 == 0:
            sv[2] = rng.uniform(0.01, 0.1)                      # a thin window
        P = U_ @ np.diag(sv) @ V_.T
        tau, D = sv[2], sv[0]
        X = np.vstack([np.zeros(3), P.T])                       # the four points
        if trial % 4 < 2:
            E = rng.normal(size=(4, 3))
        else:                                                   # displace along the thin direction
            E = np.outer(rng.normal(size=4), U_[:, 2])
        Y = X + 1e-3 * tau ** 2 / D * E / np.abs(E).max()
        Y = Y @ np.linalg.qr(rng.normal(size=(3, 3)))[0]        # an arbitrary orthogonal map
        Q = (Y[1:] - Y[0]).T
        eta = [((Y[a] - Y[b]) ** 2).sum() - ((X[a] - X[b]) ** 2).sum() for a in range(4) for b in range(a + 1, 4)]
        e = float(np.linalg.norm(eta))
        M = Q @ np.linalg.inv(P)
        Uu, _, Vt = np.linalg.svd(M)
        R = Uu @ Vt
        bound = 2 * e / (tau * D) if MUT == "procrustes_first_power" else 2 * e / tau ** 2
        worst_gram = max(worst_gram, np.linalg.norm(Q.T @ Q - P.T @ P) / (2 * e))
        worst_polar = max(worst_polar, np.linalg.norm(M - R, 2) / bound)
    ok = worst_gram <= 1 + 1e-9 and worst_polar <= 1 + 1e-9
    return ok, f"largest ||dG||_F / (2||eta||) = {worst_gram:.3f}, largest ||M - R|| / bound = {worst_polar:.3f}"


@test
def theorem_L0_instances():
    """Proposition L0 (the earlier form of Theorem L): ||Y - gX||_F <= 6.9 (b/tau^2) n (n+1) ||eta||_2,
    eta over separations <= 3, for every Y satisfying the pointwise condition (S) on the squared
    distances of separation <= 4; and (S) is needed for this form: a tail reflected in the plane
    of three consecutive atoms keeps the separation-3 data."""
    import local_data_upper as U
    rng = np.random.default_rng(32)
    worst, used = 0.0, 0
    for trial in range(30 if QUICK else 80):
        n = int(rng.integers(10, 60))
        X = U.helix(n, 1.3) if trial % 3 == 0 else U.thick_chain(n, rng)[0]
        tau, D = U.thickness(X)
        V = rng.normal(size=X.shape) if trial % 2 == 0 else U.softest_mode(X)[0]
        Y = X + 0.05 * tau ** 4 / (73 * D ** 2) * V / np.abs(V).max()
        S, left, right, _, _ = U.theorem_L0_sides(X, Y)
        if S:
            used += 1
            worst = max(worst, left / right)
    X, _ = U.thick_chain(30, rng)
    i = 12
    p0 = X[i + 1]
    nrm = np.cross(X[i + 2] - p0, X[i + 3] - p0)
    nrm /= np.linalg.norm(nrm)
    Y = X.copy()
    Y[i + 4:] = X[i + 4:] - 2 * np.outer((X[i + 4:] - p0) @ nrm, nrm)
    S, left, right, _, _ = U.theorem_L0_sides(X, Y)
    if MUT == "theorem_L_without_S":
        S = True                                            # planted error: the hypothesis is dropped
    if S:
        used += 1
        worst = max(worst, left / right if right > 0 else np.inf)
    ok = worst <= 1.0 and used >= 20 and not S and left > 0.5
    return ok, (f"{used} pairs satisfying (S): largest left/right = {worst:.4f}; reflected tail: (S) "
                f"{'holds' if S else 'fails'}, d_P = {left:.1f}")


@test
def procrustes_gram_lemma():
    """Lemmas P and Q of LOCAL_DATA_STABILITY.md: min_R ||U - XR||_F^2 <= ||UU^T - XX^T||_F^2 /
    (2 (sqrt 2 - 1) sigma_r(X)^2) for arbitrary U; and a five-point window with squared-distance
    errors of norm e is within kappa e / s of a congruent copy -- for any competitor, including
    one tetrahedron mirrored against the other and collapsed windows."""
    import local_data_upper as U
    rng = np.random.default_rng(33)
    c = 1.0 if MUT == "procrustes_gram_constant" else np.sqrt(2) - 1      # planted error: the factor dropped
    worst = U.procrustes_gram_ratio(rng, 3000 if QUICK else 12000) * (np.sqrt(2) - 1) / c
    kappa = 1 / (2 * np.sqrt(c))
    worst_w = 0.0
    for trial in range(300):
        X = rng.normal(size=(5, 3)) * rng.uniform(0.2, 2, size=3)
        kind = trial % 4
        if kind == 0:
            Y = rng.normal(size=(5, 3)) * rng.uniform(0.05, 4)
        elif kind == 1:                                   # last point mirrored in the plane of points 1, 2, 3
            nrm = np.cross(X[2] - X[1], X[3] - X[1])
            nrm /= np.linalg.norm(nrm)
            Y = X.copy()
            Y[4] = X[4] - 2 * ((X[4] - X[1]) @ nrm) * nrm
        elif kind == 2:                                   # collapsed towards a plane
            Y = X * np.array([1, 1, rng.uniform(-1, 1)])
        else:
            Y = X + rng.normal(size=(5, 3)) * 10 ** rng.uniform(-5, 0)
        e = float(np.linalg.norm(U.sq_errors(X, Y, [(a, b) for a in range(5) for b in range(a + 1, 5)])))
        res = U.best_fit(X, Y)[2]
        if e > 0:
            worst_w = max(worst_w, res / (kappa * e / U.csig3(X)))
    ok = worst <= 1 + 1e-9 and worst_w <= 1 + 1e-9
    return ok, f"largest ratio to the bound: Lemma P {worst:.3f}, five-point windows {worst_w:.3f}"


@test
def theorem_L_any_Y():
    """Theorem L (no threshold): for every configuration Y, d_P(X, Y) <= local bound <= 1.2 (b/(s tau))
    (n+2)^2 ||eta||_2 with eta over separations <= 4, and every step of the proof holds (windows,
    consecutive frames, telescoping); competitors of any size, reflected tails, unrelated chains,
    random points, mirror images, rotated heads; local form also for separations <= 5, 6."""
    import local_data_upper as U
    rng = np.random.default_rng(34)
    sep = 3 if MUT == "theorem_L_drop_sep4" else None      # planted error: separation-4 errors not counted
    nviol, wl, wg, tot = 0, 0.0, 0.0, 0
    for K, trials in ((4, 42 if QUICK else 140), (5, 14 if QUICK else 35), (6, 14 if QUICK else 35)):
        for trial in range(trials):
            n = int(rng.integers(K + 2, 50))
            X = U.helix(n, 1.3) if trial % 3 == 0 else U.thick_chain(n, rng)[0]
            Y = U.competitor(X, trial % 7, rng)
            r = U.theorem_L_bounds(X, Y, K=K, sep_in_eta=(sep if K == 4 else None), check_steps=True)
            tot += 1
            tol = lambda x: x * (1 + 1e-9) + 1e-12
            bad = bool(r["viol"]) or r["left"] > tol(r["right_local"])
            if K == 4:
                bad |= r["right_local"] > tol(r["right"])
                wg = max(wg, r["left"] / r["right"] if r["right"] > 0 else (np.inf if r["left"] > 1e-9 else 0.0))
            nviol += bad
            if r["right_local"] > 0:
                wl = max(wl, r["left"] / r["right_local"])
    return nviol == 0, f"{tot} pairs (X, Y): violations {nviol}; largest left/local bound = {wl:.3f}, left/uniform bound = {wg:.4f}"


@test
def theorem_L_sharp_constant():
    """Theorem L+: inside the range ||eta|| <= mu / (Lambda C_L), d_P(X, Y) <= ||eta|| / (mu +
    sqrt(mu^2 - Lambda ||eta||)); along the softest mode the first-order constant 1/(2 mu) is
    attained in the limit and exceeded at finite amplitude (so the quadratic term is needed)."""
    import local_data_upper as U
    rng = np.random.default_rng(35)
    first_order = MUT == "theorem_Lplus_first_order"       # planted error: the bound eta / (2 mu)
    worst, attained, used = 0.0, 0.0, 0
    for trial in range(10 if QUICK else 24):
        n = int(rng.integers(8, 30))
        X = U.helix(n, [1.0, 1.3, 2.0][trial % 3]) if trial % 2 == 0 else U.thick_chain(n, rng)[0]
        mu, Lam, CL = U.sharp_constants(X)
        pairs = U.band_pairs(n)
        A = U.sq_rigidity(X, pairs)
        Vt = np.linalg.svd(A)[2]
        for V in (Vt[3 * n - 7].reshape(n, 3), rng.normal(size=X.shape)):
            V = V / np.linalg.norm(V)
            for frac in (0.95, 0.2):
                amp = frac * mu / (Lam * CL) / (2 * np.linalg.norm(A @ V.ravel()))
                for sign in (1, -1):
                    Y = X + sign * amp * V
                    eta = float(np.linalg.norm(U.sq_errors(X, Y, pairs)))
                    bound = U.theorem_Lplus_bound(mu, Lam, CL, eta, quadratic=not first_order)
                    if bound is None:
                        continue
                    used += 1
                    dP = U.d_procrustes(X, Y)
                    worst = max(worst, dP / bound)
                    attained = max(attained, dP / (eta / (2 * mu)))
    ok = worst <= 1 + 1e-9 and used >= 40 and attained > 1 + 1e-7
    return ok, (f"{used} pairs in range: largest d_P / bound = {worst:.6f}; largest d_P / (||eta|| / 2mu) = "
                f"{attained:.6f} (above 1: the first-order constant alone is not a bound)")


@test
def label_patterns_linear():
    """LABEL_PATTERNS.md, Theorem P2: when only a subset S of the points is observed, the linear
    certificate holds and DEMIX recovers the labelled-site states exactly when the number c(S) of
    labelled pairs at chain separation 1 or 2 is at least (9K^2 + K + 2)/2; nullity max(K-1, D_K - c)."""
    import label_patterns as LP
    shift = 1 if MUT == "label_count_off_by_one" else 0       # planted error: one constrained pair fewer suffices
    ok, out = True, []
    pats = LP.PATTERNS[:11] if QUICK else LP.PATTERNS
    for name, K, n, S in pats:
        Xs, w = LP.random_mixture(K, n, seed=K * 100 + len(S))
        nul, c = LP.conic_nullity(Xs, w, S)
        cert, rmsd = LP.demix_pattern(Xs, w, S)
        D = 3 * K * (3 * K + 1) // 2
        ok &= (cert == (c >= LP.needed(K) - shift)) and nul == max(K - 1, D - c) and (not cert or rmsd < 1e-5)
        out.append(f"{c}:{'yes' if cert else 'no'}")
    return ok, f"{len(pats)} patterns (c : certified) " + " ".join(out)


@test
def label_patterns_exact():
    """LABEL_PATTERNS.md: exact conic ranks min(c, D_K - K + 1) on random label patterns and subsets
    (K <= 3), the one-state exception (two labelled triples: rank 5), and the quartic certificate
    for patterns of two states (h_4 = K from c = 17; K + dim L when two hyperplanes cover)."""
    import subprocess
    here = os.path.dirname(os.path.abspath(__file__))
    cmd = [sys.executable, os.path.join(here, "exact_label_patterns.py")]
    if MUT == "label_quartic_one_fewer":
        cmd.append("--mutate")
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=here)
    return r.returncode == 0 and "ALL OK" in r.stdout, "100 exact ranks, 0 exceptions; 7 quartic cases" if r.returncode == 0 else r.stdout[-200:]


@test
def sparse_labels_second_solution():
    """LABEL_PATTERNS.md, Proposition P3: with labels every fourth point (no two labelled points at
    chain separation 1 or 2) a rotation of the stacked labelled configuration gives labelled sites of
    two OTHER chains (fitted to rounding) with the same averaged squared distances."""
    import label_patterns as LP
    r = LP.second_solution(gap=4, eps=0.03, orthogonal=(MUT != "labels_rotation_not_orthogonal"))
    ok = r["fit_residual"] < 1e-9 and r["data_difference"] < 1e-9 and r["moved"] > 1e-2
    return ok, (f"chains fitted to {r['fit_residual']:.0e}; data differ by {r['data_difference']:.0e}; "
                f"labelled sites moved by RMSD {r['moved']:.2f}")


@test
def chain_affine_hull():
    """ENSEMBLE_RIGIDITY.md Lemma 8.0: over chains with a fixed bond angle the squared distances at
    chain separation >= 3 are affinely independent (rank of [1 | squared distances] is full), for
    several bond angles including the right angle; and the top Fourier coefficient of <b_k, b_l>
    has modulus (sin^2 a / 2) ((1 + cos a)/2)^(p-1), a = pi - theta."""
    rng = np.random.default_rng(36)
    minsep = 2 if MUT == "affine_hull_separation_two" else 3       # planted error: separation 2 claimed free
    ok, worst = True, np.inf
    for theta_deg in (60.0, 90.0, 111.0, 150.0):
        n = 9
        prs = [(i, j) for i in range(n) for j in range(i + minsep, n)]
        F = np.ones((4 * len(prs) + 20, len(prs) + 1))
        for s in range(len(F)):
            X = chain(n, rng.uniform(-np.pi, np.pi, n - 3), theta=np.deg2rad(theta_deg))
            F[s, 1:] = [np.sum((X[i] - X[j]) ** 2) for i, j in prs]
        sv = np.linalg.svd(F, compute_uv=False)
        ok &= int((sv > 1e-9 * sv[0]).sum()) == len(prs) + 1
        worst = min(worst, sv[-1] / sv[0])
    a = np.pi - np.deg2rad(111.0)
    m, p_t = 12, 2
    grid = 2 * np.pi * np.arange(m) / m
    acc = 0j
    for i1 in range(m):
        for i2 in range(m):
            X = chain(5, [grid[i1], grid[i2]], theta=np.deg2rad(111.0))
            acc += ((X[1] - X[0]) @ (X[4] - X[3])) * np.exp(-1j * (grid[i1] + grid[i2]))
    coef = abs(acc) / m ** 2
    pred = np.sin(a) ** 2 / 2 * (1 + np.cos(a)) / 2
    ok &= abs(coef - pred) < 1e-9
    return ok, f"full rank at four bond angles (smallest relative singular value {worst:.0e}); top coefficient {coef:.6f} = formula {pred:.6f}"


@test
def benchmark_suite_labels():
    """docs/geometry/BENCHMARKS.md: the 23 pinned instances of benchmark_suite/ are what MANIFEST.json
    says (SHA-256); the truth of every instance with averaged data reproduces the data; every
    'second solution' satisfies the statewise constraints, differs from the truth, and has the
    same data (averaged squared distances, or distances of separation <= 3 for C5)."""
    import hashlib
    import json
    from geomlib import edm, kabsch_rmsd
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "benchmark_suite")
    manifest = json.load(open(os.path.join(here, "MANIFEST.json")))
    ok, nsec, worst = len(manifest) == 23, 0, 0.0
    for entry in manifest:
        raw = open(os.path.join(here, entry["id"] + ".json")).read()
        ok &= hashlib.sha256(raw.encode()).hexdigest() == entry["sha256"]
        d = json.loads(raw)
        Xs = [np.array(X) for X in d["truth"]["states"]]
        w = np.array(d["truth"]["weights"])
        c = d["chain"]["second_neighbour_distance"]
        lab = d["data"].get("labelled_sites")                    # partial labelling: data among these sites only
        sub = (lambda X: X[lab]) if lab else (lambda X: X)
        if "matrix" in d["data"] and d["id"] not in ("G2", "G4"):
            ok &= np.abs(sum(wk * edm(sub(X)) for wk, X in zip(w, Xs)) - np.array(d["data"]["matrix"])).max() < 1e-9
        for key in ("second_solution", "second_solution_variant_a"):
            if key not in d:
                continue
            nsec += 1
            S = [np.array(X) for X in d[key]["states"]]
            v = np.array(d[key]["weights"])
            if MUT == "benchmark_second_solution_weights" and len(v) > 1:
                v = v[::-1].copy() if abs(v[0] - v[-1]) > 1e-6 else v * np.linspace(0.9, 1.1, len(v)) / (v * np.linspace(0.9, 1.1, len(v))).sum()
            if d["id"] == "C5":
                gap = max(abs(np.linalg.norm(Xs[0][j] - Xs[0][k]) - np.linalg.norm(S[0][j] - S[0][k])) for j, k in d["data"]["pairs_a"])
            else:
                gap = np.abs(sum(vk * edm(sub(X)) for vk, X in zip(v, S)) - np.array(d["data"]["matrix"])).max()
            worst = max(worst, gap)
            ok &= gap < 1e-9 and abs(v.sum() - 1) < 1e-9 and v.min() > 0
            if d["id"] != "C4":                             # C4's second solution deliberately violates the constraints
                ok &= all(max(abs(np.linalg.norm(Y[i + 1] - Y[i]) - 1) for i in range(len(Y) - 1)) < 1e-8 for Y in S)
                ok &= all(max(abs(np.linalg.norm(Y[i + 2] - Y[i]) - c) for i in range(len(Y) - 2)) < 1e-8 for Y in S)
            ok &= max(min(kabsch_rmsd(sub(X), sub(Y)) for X in Xs) for Y in S) > 1e-2
    return ok and nsec == 6, f"23 instances match the manifest; {nsec} second solutions reproduce the data to {worst:.0e}"


@test
def third_moment_blocks():
    """Proposition 9.2: the 3-form of mean triple products is determined by the data and its
    contractions have rank 2 exactly on block vectors."""
    r = third_moment.run(2, seed=3)
    want_generic = 2 if MUT == "third_moment_generic_rank" else 4
    ok = (r["fit_residual"] < 1e-9 and r["rank_of_system"] == 20 and set(map(int, r["block_ranks"])) == {2}
          and set(map(int, r["two_block_ranks"])) == {4} and set(map(int, r["generic_ranks"])) == {want_generic})
    return ok, f"block ranks {sorted(set(map(int, r['block_ranks'])))}, generic ranks {sorted(set(map(int, r['generic_ranks'])))}"


def main():
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]
    failed = []
    t0 = time.time()
    for f in TESTS:
        if only and f.__name__ != only:
            continue
        t = time.time()
        try:
            ok, msg = f()
        except Exception as e:                       # a crash is a failure of the harness
            ok, msg = False, f"EXCEPTION {type(e).__name__}: {e}"
        print(f"{'PASS' if ok else 'FAIL'}  {f.__name__:38s} {msg}   [{time.time() - t:.1f}s]", flush=True)
        if not ok:
            failed.append(f.__name__)
    n = len([f for f in TESTS if not only or f.__name__ == only])
    print(f"{n - len(failed)} of {n} tests passed in {time.time() - t0:.0f}s" + (f"; FAILED: {failed}" if failed else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
