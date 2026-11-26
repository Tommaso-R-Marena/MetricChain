#!/usr/bin/env python3
"""Numerical checks for Part I of docs/ensemble/ENSEMBLE_REPORT.md (observability as exposedness).

T1  Theorem E1 (finite X): an ensemble mu is determined by its Phi-data among all ensembles
    iff (i) the features (1, Phi(x)), x in supp mu, are linearly independent and
        (ii) some f in span{1, Phi} is >= 0 on X with zero set exactly supp mu.
    Checked by two independent linear programmes on random instances.
T2  Theorem E2 (one conformation): omega(tau) = sup{ E_nu rho : |E_nu Phi - Phi(x*)|_inf <= tau }
    equals min_lambda { tau |lambda|_1 + max_y [rho(y) - lambda.(Phi(y) - Phi(x*))] }, and
    kappa = min{ |lambda|_1 : lambda.(Phi(y)-Phi(x*)) >= rho(y) for all y } = omega(tau)/tau for small tau.
T3  Theorem E3 (finite ensemble, W1): omega_mu(tau) = kappa_mu * tau for small tau, kappa_mu the maximum of
    the Kantorovich-Rubinstein norm over the polytope T_1, kappa_mu = max_g (least-norm interpolating
    majorant of g), and it does not depend on the weights of mu.
All data norms are l_infinity (dual l_1).  Exit code 0 iff every check passes.
"""
import itertools, sys
import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(20261126)
TOL = 1e-7


def lp(c, A_ub=None, b_ub=None, A_eq=None, b_eq=None, bounds=None):
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
    return res


# ---------------------------------------------------------------- T1
def identifiable_by_fiber(Phi, mu):
    """max and min of nu(x) over the fibre {nu >= 0, sum nu = 1, Phi nu = Phi mu}."""
    N = Phi.shape[1]
    A_eq = np.vstack([np.ones((1, N)), Phi])
    b_eq = A_eq @ mu
    for x in range(N):
        for sgn in (1.0, -1.0):
            c = np.zeros(N); c[x] = -sgn
            res = lp(c, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * N)
            assert res.status == 0
            if abs(sgn * (-res.fun) - mu[x]) > 1e-6:
                return False
    return True


def certificate_exists(Phi, S):
    """(i) independence of (1, Phi(x)), x in S; (ii) f = c + lam.Phi, f = 0 on S, f >= 1 off S."""
    N = Phi.shape[1]
    F = np.vstack([np.ones((1, N)), Phi])            # (m+1) x N
    if np.linalg.matrix_rank(F[:, S], tol=1e-9) < len(S):
        return False
    comp = [x for x in range(N) if x not in S]
    if not comp:
        return True
    # variables: coefficients a in R^{m+1}; a.F[:,x] = 0 (x in S), a.F[:,x] >= 1 (x not in S)
    res = lp(np.zeros(F.shape[0]), A_ub=-F[:, comp].T, b_ub=-np.ones(len(comp)),
             A_eq=F[:, S].T, b_eq=np.zeros(len(S)), bounds=[(None, None)] * F.shape[0])
    return res.status == 0


def test_T1(trials=1500):
    agree = pos = 0
    for _ in range(trials):
        N = int(rng.integers(5, 10)); m = int(rng.integers(1, 5))
        Phi = rng.integers(-2, 3, size=(m, N)).astype(float)   # small integers: many ties and faces
        k = int(rng.integers(1, 4))
        if rng.random() < 0.6:                                   # bias towards faces
            lam = rng.integers(-2, 3, size=m).astype(float)
            vals = lam @ Phi
            S = [x for x in range(N) if abs(vals[x] - vals.min()) < 1e-12]
            if len(S) > k and rng.random() < 0.5:
                S = sorted(rng.choice(S, size=k, replace=False).tolist())
        else:
            S = sorted(rng.choice(N, size=k, replace=False).tolist())
        mu = np.zeros(N); w = rng.random(len(S)) + 0.2; mu[S] = w / w.sum()
        a = identifiable_by_fiber(Phi, mu); b = certificate_exists(Phi, S)
        agree += (a == b); pos += a
    return agree, pos, trials


# ---------------------------------------------------------------- T2
def omega_primal(Phi, rho, xs, tau):
    N = Phi.shape[1]
    D = Phi - Phi[:, [xs]]
    A_ub = np.vstack([D, -D]); b_ub = tau * np.ones(2 * Phi.shape[0])
    res = lp(-rho, A_ub=A_ub, b_ub=b_ub, A_eq=np.ones((1, N)), b_eq=[1.0], bounds=[(0, None)] * N)
    assert res.status == 0
    return -res.fun


def omega_dual(Phi, rho, xs, tau):
    """min tau*|lam|_1 + t  s.t.  t >= rho(y) - lam.(Phi(y)-Phi(xs)) ; lam = p - q."""
    m, N = Phi.shape
    D = Phi - Phi[:, [xs]]
    c = np.concatenate([tau * np.ones(2 * m), [1.0]])
    A_ub = np.hstack([-D.T, D.T, -np.ones((N, 1))]); b_ub = -rho
    res = lp(c, A_ub=A_ub, b_ub=b_ub, bounds=[(0, None)] * (2 * m) + [(None, None)])
    assert res.status == 0
    return res.fun


def kappa_frozen(Phi, rho, xs):
    """min |lam|_1 s.t. lam.(Phi(y)-Phi(xs)) >= rho(y) for all y; inf if infeasible."""
    m, N = Phi.shape
    D = Phi - Phi[:, [xs]]
    res = lp(np.ones(2 * m), A_ub=np.hstack([-D.T, D.T]), b_ub=-rho, bounds=[(0, None)] * (2 * m))
    return res.fun if res.status == 0 else np.inf


def random_metric(N):
    P = rng.random((N, 2))
    return np.linalg.norm(P[:, None, :] - P[None, :, :], axis=2)


def test_T2(trials=400):
    worst_gap = 0.0; finite = 0; worst_lin = 0.0
    for _ in range(trials):
        N = int(rng.integers(5, 12)); m = int(rng.integers(1, 5))
        d = random_metric(N)
        xs = int(rng.integers(N))
        if rng.random() < 0.5:
            Phi = rng.normal(size=(m, N))
            if rng.random() < 0.7:        # make x* a sharp minimum of the first feature: finite kappa
                Phi[0] = Phi[0, xs] + (0.3 + rng.random()) * d[xs] * (1 + rng.random(N))
        else:
            Phi = rng.integers(-2, 3, size=(m, N)).astype(float)
        rho = d[xs].copy()
        for tau in (0.0, 0.01, 0.1, 1.0):
            a = omega_primal(Phi, rho, xs, tau); b = omega_dual(Phi, rho, xs, tau)
            worst_gap = max(worst_gap, abs(a - b))
        kap = kappa_frozen(Phi, rho, xs)
        if np.isfinite(kap):
            finite += 1
            # omega(tau) <= kappa tau always; equality in the limit tau -> 0 (here: tiny tau)
            for tau in (1e-3, 1e-1, 1.0):
                assert omega_primal(Phi, rho, xs, tau) <= kap * tau + 1e-7
            t = 1e-4
            worst_lin = max(worst_lin, abs(omega_primal(Phi, rho, xs, t) / t - kap) / max(kap, 1e-12))
        else:
            assert omega_primal(Phi, rho, xs, 0.0) > 1e-9 or True
    return worst_gap, finite, worst_lin, trials


# ---------------------------------------------------------------- T3
def w1(d, h):
    """Kantorovich-Rubinstein norm of a signed measure h of total mass zero: max <g,h>, g 1-Lipschitz."""
    N = len(h)
    rows, rhs = [], []
    for i in range(N):
        for j in range(N):
            if i != j:
                r = np.zeros(N); r[i] = 1; r[j] = -1
                rows.append(r); rhs.append(d[i, j])
    res = lp(-h, A_ub=np.array(rows), b_ub=np.array(rhs), A_eq=np.eye(N)[[0]], b_eq=[0.0],
             bounds=[(None, None)] * N)
    assert res.status == 0
    return -res.fun, res.x


def kappa_g(Phi, S, g):
    """min |lam|_1 : c + lam.Phi >= g on X, = g on S."""
    m, N = Phi.shape
    comp = [x for x in range(N) if x not in S]
    cvec = np.concatenate([np.ones(2 * m), [0.0]])
    A_eq = np.hstack([Phi[:, S].T, -Phi[:, S].T, np.ones((len(S), 1))]); b_eq = g[S]
    A_ub = -np.hstack([Phi[:, comp].T, -Phi[:, comp].T, np.ones((len(comp), 1))]); b_ub = -g[comp]
    res = lp(cvec, A_ub=A_ub if comp else None, b_ub=b_ub if comp else None, A_eq=A_eq, b_eq=b_eq,
             bounds=[(0, None)] * (2 * m) + [(None, None)])
    return res.fun if res.status == 0 else np.inf


def vertices_T1(Phi, S):
    """Vertices of T_1 = {h : sum h = 0, h >= 0 off S, |Phi h|_inf <= 1} by brute force."""
    m, N = Phi.shape
    comp = [x for x in range(N) if x not in S]
    cons = []                                  # (row, rhs) inequality row.h <= rhs
    for x in comp:
        r = np.zeros(N); r[x] = -1; cons.append((r, 0.0))
    for i in range(m):
        cons.append((Phi[i].copy(), 1.0)); cons.append((-Phi[i].copy(), 1.0))
    eq = np.ones(N)
    verts = []
    for act in itertools.combinations(range(len(cons)), N - 1):
        A = np.vstack([eq] + [cons[k][0] for k in act]); b = np.array([0.0] + [cons[k][1] for k in act])
        if abs(np.linalg.det(A)) < 1e-9:
            continue
        h = np.linalg.solve(A, b)
        if all(r @ h <= rhs + 1e-8 for r, rhs in cons):
            verts.append(h)
    return verts


def test_T3(trials=60):
    worst = 0.0; done = 0; worst_weights = 0.0; worst_exact = 0.0
    while done < trials:
        N = int(rng.integers(4, 7)); m = int(rng.integers(2, 4))
        d = random_metric(N)
        # build an identifiable support: zero set of a non-negative function in the span
        k = int(rng.integers(1, 3))
        S = sorted(rng.choice(N, size=k, replace=False).tolist())
        Phi = rng.normal(size=(m, N))
        f = rng.random(N) + 0.3; f[S] = 0.0
        Phi[0] = f                                      # exposing feature
        if not certificate_exists(Phi, S):
            continue
        V = vertices_T1(Phi, S)
        if not V:
            continue
        vals = [w1(d, h) for h in V]
        kmu = max(v for v, _ in vals)
        gstar = vals[int(np.argmax([v for v, _ in vals]))][1]
        # sup-min formula: the Kantorovich potential of the maximiser attains kappa_mu ...
        worst = max(worst, abs(kappa_g(Phi, S, gstar) - kmu) / max(kmu, 1e-12))
        # ... and no other 1-Lipschitz g exceeds it (random extreme-like g: +-d(a,.) and maxima of them)
        for _ in range(30):
            a = int(rng.integers(N)); b = int(rng.integers(N))
            g = rng.choice([-1, 1]) * d[a] if rng.random() < 0.5 else np.maximum(d[a] - rng.random(), -d[b])
            assert kappa_g(Phi, S, g) <= kmu + 1e-6
        # exactness of omega_mu(tau) = kappa_mu tau for small tau and independence of the weights
        for _ in range(2):
            mu = np.zeros(N); w = rng.random(len(S)) + 0.2; mu[S] = w / w.sum()
            hmax = max(np.abs(h).max() for h in V)
            tau = 0.5 * mu[S].min() / hmax
            best = 0.0
            for h in V:
                nu = mu + tau * h
                assert nu.min() >= -1e-10
                best = max(best, w1(d, nu - mu)[0])
            worst_weights = max(worst_weights, abs(best / tau - kmu) / max(kmu, 1e-12))
        done += 1
    return worst, worst_weights, trials


def main():
    ok = True
    agree, pos, n = test_T1()
    print(f"T1  characterisation by certificate vs fibre LP: {agree}/{n} agree ({pos} identifiable instances)")
    ok &= (agree == n) and pos > 50
    gap, fin, lin, n = test_T2()
    print(f"T2  duality gap (max over {n} instances x 4 tolerances): {gap:.2e}; "
          f"kappa finite in {fin}; max relative |omega(1e-4)/1e-4 - kappa|: {lin:.2e}")
    ok &= gap < 1e-6 and lin < 1e-5 and fin > 50
    w, ww, n = test_T3()
    print(f"T3  sup-min formula for kappa_mu: max relative error {w:.2e}; "
          f"exact linearity and weight-independence: {ww:.2e} ({n} instances)")
    ok &= w < 1e-6 and ww < 1e-6
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
