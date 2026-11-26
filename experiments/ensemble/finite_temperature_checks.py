#!/usr/bin/env python3
"""Numerical checks for Part IV of docs/ensemble/ENSEMBLE_REPORT.md (finite temperature: identification
inside a first-order class) and for Theorem E17 (noise).

The class: probability vectors mu > 0 on a product space with mu(x[i -> s]) <= exp(delta_i(x_i, s)) * mu(x)
(for the cube: mu(x^(i)) <= e^b mu(x)), i.e. Gibbs measures of residuals that are Lipschitz for a
site-additive envelope around the uniform reference.  In the normalised weights the class is a polytope.

F1  Theorem E15 on the cube: for every member mu and every a:  TV(mu, P_a) <= sum_i (sigma - mu(x_i = a_i)),
    P_a the product measure with P(x_i = a_i) = sigma = 1/(1+e^{-b}).  EXACT maximisation of
    TV - sum_i tau_i over the class polytope for n = 3 (one LP per sign pattern), vertices and random members
    for n = 4..6.  The maximum is 0 (attained).
F2  Theorem E15 for general alphabets and heterogeneous sites (three-letter sites, random symmetric
    site envelopes, non-uniform product reference): TV(mu, mu*_a) <= sum_i (1 - mu(x_i = a_i)/mu*_i(a_i)).
F3  Members identified by one-body data: for n = 3, the fibre of the one-body data inside the class is a
    point iff at most one marginal is unsaturated.
F4  Theorem E16: the double cone exp((b/2)|M|) is the unique maximiser of E[M^2] over the class for even n;
    for odd n the maximisers form a segment (the populations of the two basins are free within e^{+-b}).
F5  Theorem E17: omega(eps) = min_lam { eps |lam|_1 + osc(psi - lam.Phi) } (l_inf data norm; LP on both sides).
F6  Theorem E15T (an interacting reference): Ising references whose bonds are all satisfied by the centre a
    (chains, triangles: exact maximisation over the class polytope; complete graphs on 4..7 sites: vertices
    and mixtures) give max of TV(mu, mu*_a) - sum_j [mu*_a(x_j = a_j) - mu(x_j = a_j)] = 0; a chain with one
    violated bond gives a positive maximum (the obstruction).
Exit code 0 iff every check passes.
"""
import itertools, sys
import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(20261130)


def cube(n):
    return np.array(list(itertools.product((-1, 1), repeat=n)))


def class_constraints_cube(n, b):
    """A_ub mu <= 0 encoding mu(x^(i)) - e^b mu(x) <= 0 for all x, i."""
    X = cube(n); N = len(X)
    index = {tuple(x): k for k, x in enumerate(X)}
    rows = []
    for k, x in enumerate(X):
        for i in range(n):
            y = x.copy(); y[i] = -y[i]
            r = np.zeros(N); r[index[tuple(y)]] = 1.0; r[k] = -np.exp(b)
            rows.append(r)
    return X, np.array(rows)


def product_measure(X, a, sigma):
    agree = (X == a)
    return np.prod(np.where(agree, sigma, 1 - sigma), axis=1)


def random_member_cube(X, A, n, b):
    """A random member: optimum of a random linear objective mixed with random convex combinations."""
    N = len(X)
    pts = []
    for _ in range(3):
        res = linprog(rng.normal(size=N), A_ub=A, b_ub=np.zeros(len(A)), A_eq=np.ones((1, N)), b_eq=[1.0],
                      bounds=[(0, None)] * N, method="highs")
        pts.append(res.x)
    w = rng.dirichlet(np.ones(3))
    return sum(wi * p for wi, p in zip(w, pts))


def test_F1():
    out = []; ok = True
    # exact, n = 3
    for b in (0.5, 1.0, 2.0):
        n = 3; X, A = class_constraints_cube(n, b); N = len(X); sigma = 1 / (1 + np.exp(-b))
        a = np.ones(n, dtype=int); q = product_measure(X, a, sigma)
        # tau_i(mu) = sigma - mu(x_i = a_i): linear in mu
        tau_rows = np.array([-(X[:, i] == a[i]).astype(float) for i in range(n)])
        worst = -np.inf
        for s in itertools.product((-1.0, 1.0), repeat=N):
            s = np.array(s)
            # maximise 0.5 * s.(mu - q) - sum_i (sigma - mu(x_i=a_i)) ; TV = max over s
            c = -(0.5 * s - tau_rows.sum(axis=0))
            res = linprog(c, A_ub=A, b_ub=np.zeros(len(A)), A_eq=np.ones((1, N)), b_eq=[1.0],
                          bounds=[(0, None)] * N, method="highs")
            val = -res.fun - 0.5 * s @ q - n * sigma
            worst = max(worst, val)
        out.append(f"    n = 3, b = {b}: max over the class of TV(mu, P_a) - sum_i tau_i = {worst:+.2e} (exact, 256 LPs)")
        ok &= abs(worst) < 1e-9
    # sampled, n = 4..6
    worst = -np.inf; cnt = 0; tight = 0.0
    for n in (4, 5, 6):
        for b in (0.5, 1.5):
            X, A = class_constraints_cube(n, b); sigma = 1 / (1 + np.exp(-b))
            for _ in range(15):
                mu = random_member_cube(X, A, n, b)
                for _ in range(4):
                    a = rng.choice((-1, 1), size=n)
                    q = product_measure(X, a, sigma)
                    tv = 0.5 * np.abs(mu - q).sum()
                    tau = sum(sigma - mu[X[:, i] == a[i]].sum() for i in range(n))
                    worst = max(worst, tv - tau); cnt += 1
                    tight = max(tight, tv / max(tau, 1e-300))
    out.append(f"    n = 4..6: {cnt} (member, centre) pairs: max of TV - sum_i tau_i = {worst:+.2e}; largest ratio TV/sum tau = {tight:.4f}")
    ok &= worst < 1e-9
    return ok, out


def site_envelope(q, symmetric):
    """A random site envelope on q letters satisfying the triangle inequality: a metric (points on a line) if
    `symmetric`, otherwise a quasi-metric (shortest paths for random directed weights)."""
    if symmetric:
        pts = np.sort(rng.random(q)) * rng.uniform(0.5, 2.5)
        return np.abs(pts[:, None] - pts[None, :])
    W = rng.uniform(0.2, 2.5, size=(q, q)); np.fill_diagonal(W, 0.0)
    for k in range(q):                                           # Floyd-Warshall
        W = np.minimum(W, W[:, [k]] + W[[k], :])
    return W


def general_alphabet_case(n, q, symmetric):
    """Returns (states, class constraint matrix in the measure, site envelopes, site references, reference)."""
    states = list(itertools.product(range(q), repeat=n)); N = len(states)
    index = {st: k for k, st in enumerate(states)}
    deltas = [site_envelope(q, symmetric) for _ in range(n)]
    pis = [rng.dirichlet(np.ones(q) * 3) for _ in range(n)]
    pi = np.array([np.prod([pis[i][st[i]] for i in range(n)]) for st in states])
    rows = []                                                    # mu(y)/pi(y) <= exp(delta_i(x_i, y_i)) mu(x)/pi(x)
    for k, st in enumerate(states):
        for i in range(n):
            for t in range(q):
                if t == st[i]:
                    continue
                y = list(st); y[i] = t; ky = index[tuple(y)]
                r = np.zeros(N); r[ky] = 1.0 / pi[ky]; r[k] = -np.exp(deltas[i][st[i], t]) / pi[k]
                rows.append(r)
    return states, np.array(rows), deltas, pis, pi


def polarised_member(states, deltas, pis, a, into_centre=True):
    """mu*_a = product of pi_i(s) exp(-delta_i(s, a_i)) (cost INTO the centre); with into_centre=False the cost
    out of the centre, delta_i(a_i, s) — the same thing for symmetric envelopes, not a member otherwise."""
    star = []
    for i in range(len(deltas)):
        cost = deltas[i][:, a[i]] if into_centre else deltas[i][a[i], :]
        v = pis[i] * np.exp(-cost); star.append(v / v.sum())
    return star, np.array([np.prod([star[i][st[i]] for i in range(len(deltas))]) for st in states])


def test_F2():
    """Three-letter sites, random site envelopes, non-uniform product reference: Theorem E15 (a), (b); symmetric
    envelopes (metrics) and one-sided ones (quasi-metrics), with the control for the orientation."""
    out = []; ok = True
    for symmetric in (True, False):
        worst = -np.inf; cnt = 0; worst_marg = -np.inf; member = 0; wrong_member = 0; refs = 0
        for n in (2, 3):
            for _ in range(12):
                q = 3
                states, A, deltas, pis, pi = general_alphabet_case(n, q, symmetric); N = len(states)
                for _ in range(4):
                    ptsm = []
                    for _ in range(3):
                        res = linprog(rng.normal(size=N), A_ub=A, b_ub=np.zeros(len(A)), A_eq=np.ones((1, N)),
                                      b_eq=[1.0], bounds=[(0, None)] * N, method="highs")
                        ptsm.append(res.x)
                    mu = sum(wi * pt for wi, pt in zip(rng.dirichlet(np.ones(3)), ptsm))
                    a = tuple(rng.integers(q, size=n))
                    star, mustar = polarised_member(states, deltas, pis, a)
                    refs += 1
                    member += np.max(A @ mustar) < 1e-9
                    _, wrong = polarised_member(states, deltas, pis, a, into_centre=False)
                    wrong_member += np.max(A @ wrong) < 1e-9
                    tv = 0.5 * np.abs(mu - mustar).sum()
                    bound = 0.0
                    for i in range(n):
                        marg = sum(mu[k] for k, st in enumerate(states) if st[i] == a[i])
                        worst_marg = max(worst_marg, marg - star[i][a[i]])          # (a): the marginal bound
                        bound += 1 - marg / star[i][a[i]]
                    worst = max(worst, tv - bound); cnt += 1
        kind = "symmetric site envelopes (metrics)" if symmetric else "one-sided site envelopes (quasi-metrics)"
        out.append(f"    three-letter heterogeneous sites, {kind}: {cnt} cases; mu*_a (cost into the centre) is a member "
                   f"in {member}/{refs}; max of mu_i(a_i) - mu*_i(a_i) = {worst_marg:+.2e}; "
                   f"max of TV - sum_i (1 - mu_i(a_i)/mu*_i(a_i)) = {worst:+.2e}; "
                   f"with the cost out of the centre the measure is a member in {wrong_member}/{refs}")
        ok &= worst < 1e-9 and worst_marg < 1e-9 and member == refs
        ok &= (wrong_member == refs) if symmetric else (wrong_member < refs // 2)
    return ok, out


def test_F3():
    out = []; ok = True
    n = 3; b = 1.0; X, A = class_constraints_cube(n, b); N = len(X); sigma = 1 / (1 + np.exp(-b))
    onebody = np.array([(X[:, i] == 1).astype(float) for i in range(n)])

    def fibre_point(mu):
        Aeq = np.vstack([np.ones((1, N)), onebody]); beq = Aeq @ mu
        for k in range(N):
            for sgn in (1.0, -1.0):
                c = np.zeros(N); c[k] = -sgn
                res = linprog(c, A_ub=A, b_ub=np.zeros(len(A)), A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * N,
                              method="highs")
                if abs(sgn * (-res.fun) - mu[k]) > 1e-7:
                    return False
        return True

    agree = tot = 0
    for _ in range(60):
        kind = rng.integers(4)                     # number of unsaturated sites in a product member
        p = np.array([sigma if i >= kind else rng.uniform(1 - sigma + 0.05, sigma - 0.05) for i in range(n)])
        a_sign = rng.choice((-1, 1), size=n)
        probs = np.where(a_sign == 1, p, 1 - p)    # P(x_i = +1)
        mu = np.prod(np.where(X == 1, probs, 1 - probs), axis=1)
        if kind >= 2 and rng.random() < 0.5:       # a correlated member with the same marginals
            i, j = 0, 1
            h = (X[:, i] * X[:, j]).astype(float)
            mu = mu * (1 + 0.02 * h); mu = mu / mu.sum()
            if (A @ mu).max() > 1e-12:
                continue
        marg = onebody @ mu
        unsat = int(np.sum((np.abs(marg - sigma) > 1e-9) & (np.abs(marg - (1 - sigma)) > 1e-9)))
        tot += 1; agree += (fibre_point(mu) == (unsat <= 1))
    out.append(f"    n = 3, b = 1: identified by one-body data inside the class <=> at most one unsaturated marginal: {agree}/{tot}")
    ok &= agree == tot and tot > 30
    return ok, out


def test_F4():
    out = []; ok = True
    for n, b in ((4, 1.0), (6, 0.7), (5, 1.0)):
        X, A = class_constraints_cube(n, b); N = len(X)
        M = X.sum(axis=1).astype(float)
        res = linprog(-(M ** 2), A_ub=A, b_ub=np.zeros(len(A)), A_eq=np.ones((1, N)), b_eq=[1.0],
                      bounds=[(0, None)] * N, method="highs")
        D = np.exp(0.5 * b * np.abs(M)); D /= D.sum()
        opt = -res.fun; val = D @ M ** 2
        # dimension of the optimal face: maximise/minimise each coordinate on the optimal face
        Aeq = np.vstack([np.ones((1, N)), M ** 2]); beq = np.array([1.0, opt])
        spread = 0.0
        for k in range(N):
            lo = linprog(np.eye(N)[k], A_ub=A, b_ub=np.zeros(len(A)), A_eq=Aeq, b_eq=beq,
                         bounds=[(0, None)] * N, method="highs").fun
            hi = -linprog(-np.eye(N)[k], A_ub=A, b_ub=np.zeros(len(A)), A_eq=Aeq, b_eq=beq,
                          bounds=[(0, None)] * N, method="highs").fun
            spread = max(spread, hi - lo)
        out.append(f"    n = {n}, b = {b}: max E[M^2] over the class = {opt:.6f}; double cone: {val:.6f}; "
                   f"largest spread of a weight on the optimal face = {spread:.2e}")
        ok &= abs(opt - val) < 1e-7
        ok &= (spread < 1e-7) if n % 2 == 0 else (spread > 1e-4)
        if n % 2 == 1:
            # the predicted segment: D * (1 + theta sign M), |theta| <= tanh(b/2)
            th = np.tanh(b / 2)
            Dth = np.exp(0.5 * b * np.abs(M)) * (1 + th * np.sign(M)); Dth /= Dth.sum()
            ok &= (A @ Dth).max() < 1e-12 and abs(Dth @ M ** 2 - opt) < 1e-7
            k = int(np.argmax(M))
            pred = Dth[k] - (np.exp(0.5 * b * np.abs(M)) * (1 - th * np.sign(M)) / np.sum(np.exp(0.5 * b * np.abs(M)) * (1 - th * np.sign(M))))[k]
            out.append(f"        odd n: end points D_(+-theta), theta = tanh(b/2), are members and optimal; "
                       f"predicted spread at the all-plus state {pred:.6f}")
    return ok, out


def test_F5():
    out = []; worst = 0.0
    for _ in range(200):
        N = int(rng.integers(5, 11)); m = int(rng.integers(1, 4))
        Phi = rng.normal(size=(m, N)); psi = rng.normal(size=N)
        for eps in (0.0, 0.05, 0.3, 1.0):
            # primal: mu1, mu0 ensembles, |Phi (mu1 - mu0)|_inf <= eps, maximise psi.(mu1 - mu0)
            c = -np.concatenate([psi, -psi])
            Aub = np.vstack([np.hstack([Phi, -Phi]), np.hstack([-Phi, Phi])]); bub = eps * np.ones(2 * m)
            Aeq = np.zeros((2, 2 * N)); Aeq[0, :N] = 1; Aeq[1, N:] = 1
            pr = -linprog(c, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=[1, 1], bounds=[(0, None)] * (2 * N),
                          method="highs").fun
            # dual: min eps*|lam|_1 + (hi - lo), hi >= psi - lam.Phi >= lo ; lam = p - q
            cd = np.concatenate([eps * np.ones(2 * m), [1.0, -1.0]])
            A1 = np.hstack([-Phi.T, Phi.T, -np.ones((N, 1)), np.zeros((N, 1))])       # psi - lam.Phi <= hi
            A2 = np.hstack([Phi.T, -Phi.T, np.zeros((N, 1)), np.ones((N, 1))])        # lo <= psi - lam.Phi
            du = linprog(cd, A_ub=np.vstack([A1, A2]), b_ub=np.concatenate([-psi, psi]),
                         bounds=[(0, None)] * (2 * m) + [(None, None)] * 2, method="highs").fun
            worst = max(worst, abs(pr - du))
    out = [f"    modulus duality, l^infinity data norm, class of all ensembles (200 instances x 4 tolerances): "
           f"largest gap {worst:.2e}"]
    # the constant of E17(c): kappa = E sech^2(1 + Z), by two quadratures; and, without the closed form, the risk
    # of the Bayes rule p(z) = 1/(1 + exp(-2z)) for the two hypotheses z ~ N(+-1, 1), T in {0, 1}
    nodes, wts = np.polynomial.hermite_e.hermegauss(150)
    kappa_gh = float(wts @ (1 / np.cosh(1 + nodes)) ** 2 / np.sqrt(2 * np.pi))
    z = np.linspace(-14, 14, 560001); dz = z[1] - z[0]
    dens = lambda mean: np.exp(-(z - mean) ** 2 / 2) / np.sqrt(2 * np.pi)
    kappa_tr = float(np.sum(dens(0.0) / np.cosh(1 + z) ** 2) * dz)
    pz = 1 / (1 + np.exp(-2 * z))
    risk1 = float(np.sum(dens(1.0) * (pz - 1) ** 2) * dz); risk0 = float(np.sum(dens(-1.0) * pz ** 2) * dz)
    from math import erf, sqrt
    phi_m1 = 0.5 * (1 + erf(-1 / sqrt(2)))
    out.append(f"    constant of E17(c): kappa = E sech^2(1 + Z) = {kappa_gh:.6f} (Gauss-Hermite), {kappa_tr:.6f} (trapezoid); "
               f"risk of the Bayes rule under the two hypotheses = {risk1:.6f}, {risk0:.6f} = kappa/4 = {kappa_gh / 4:.6f}; "
               f"sqrt(kappa)/2 = {np.sqrt(kappa_gh) / 2:.4f}; the testing bound of version 2: Phi_N(-1) = {phi_m1:.4f}, "
               f"sqrt(Phi_N(-1))/2 = {np.sqrt(phi_m1) / 2:.4f}")
    ok = (worst < 1e-7 and abs(kappa_gh - kappa_tr) < 1e-8 and abs(risk1 - kappa_gh / 4) < 1e-8
          and abs(risk0 - kappa_gh / 4) < 1e-8 and abs(kappa_gh - 0.4496) < 1e-4 and phi_m1 < kappa_gh)
    return ok, out


def ising_reference_case(n, Jm, h, b, a, exact=True, samples=25, logpi=None):
    """Class around the Ising reference pi ∝ exp(sum_{i<j} Jm[i,j] x_i x_j + h.x) with slope b; centre a.
    (If `logpi` is given — a vector over cube(n) — it is used as the logarithm of the reference instead; `b` may
    be a scalar or, with `exact`, one slope per site.)
    Variables are the weights w = mu / pi (well scaled: w(y) <= e^b w(x), sum pi w = 1).
    Returns (max of TV(mu, mu*_a) - sum_j deficits, max of mu(x_j = a_j) - mu*_a(x_j = a_j)); exact
    maximisation by one LP per sign pattern if `exact`, otherwise over vertices and mixtures of the polytope
    (solver tolerances repaired by the least Lipschitz majorant of -log w)."""
    X = cube(n); N = len(X)
    if logpi is None:
        logpi = X @ h + sum(Jm[i, j] * X[:, i] * X[:, j] for i in range(n) for j in range(i + 1, n))
    pi = np.exp(logpi - np.max(logpi)); pi /= pi.sum()
    index = {tuple(x): k for k, x in enumerate(X)}
    bvec = np.broadcast_to(np.asarray(b, dtype=float), (n,))
    rows = []
    for k, x in enumerate(X):
        for i in range(n):
            y = x.copy(); y[i] = -y[i]; ky = index[tuple(y)]
            r = np.zeros(N); r[ky] = 1.0; r[k] = -np.exp(bvec[i])
            rows.append(r)
    A = np.array(rows)
    mustar = pi * np.exp(-((X != a).astype(float) @ bvec)); mustar /= mustar.sum()
    agree = np.array([(X[:, i] == a[i]).astype(float) for i in range(n)])
    mstar = agree @ mustar
    kw = dict(A_ub=A, b_ub=np.zeros(len(A)), A_eq=pi[None, :], b_eq=[1.0], bounds=[(0, None)] * N, method="highs")
    worst = -np.inf; worst_marg = -np.inf
    if exact:
        for sgn in itertools.product((-1.0, 1.0), repeat=N):
            sgn = np.array(sgn)
            c = -(0.5 * sgn + agree.sum(axis=0)) * pi           # objective in w
            res = linprog(c, **kw)
            worst = max(worst, -res.fun - 0.5 * sgn @ mustar - mstar.sum())
        for j in range(n):
            res = linprog(-agree[j] * pi, **kw)
            worst_marg = max(worst_marg, -res.fun - mstar[j])
    else:
        dH = (X[:, None, :] != X[None, :, :]).sum(axis=2)
        for _ in range(samples):
            pts = []
            for _ in range(3):
                w = linprog(rng.normal(size=N) * pi, **kw).x
                g = -np.log(np.maximum(w, 1e-300))
                g = np.max(g[None, :] - float(b) * dH, axis=1)  # least b-Lipschitz majorant: exact membership
                mu = pi * np.exp(-g); pts.append(mu / mu.sum())
            for mu in pts + [sum(wt * q for wt, q in zip(rng.dirichlet(np.ones(3)), pts))]:
                worst = max(worst, 0.5 * np.abs(mu - mustar).sum() - (mstar - agree @ mu).sum())
                worst_marg = max(worst_marg, (agree @ mu - mstar).max())
    return worst, worst_marg


def random_couplings(n, a, graph, scale=1.0, floor=0.0):
    Jm = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            if graph == "complete" or j == i + 1:
                Jm[i, j] = (floor + abs(rng.normal())) * scale * a[i] * a[j]     # bond satisfied by a
    return Jm


def test_F6():
    out = []; ok = True
    # (i) chains and triangles of three sites, every bond satisfied: exact
    w1 = wm1 = -np.inf
    for t in range(6):
        n = 3; a = rng.choice((-1, 1), size=n)
        Jm = random_couplings(n, a, "chain" if t < 3 else "complete")
        w, wm = ising_reference_case(n, Jm, 0.7 * rng.normal(size=n), rng.uniform(0.4, 2.0), a)
        w1 = max(w1, w); wm1 = max(wm1, wm)
    out.append(f"    three sites, chains and triangles, every bond satisfied (6 cases, exact): max of TV - sum of deficits = {w1:+.2e}; "
               f"max of mu(x_j = a_j) - mu*(x_j = a_j) = {wm1:+.2e}")
    ok &= abs(w1) < 1e-9 and wm1 < 1e-9
    # (ii) complete graphs on 4..7 sites, every bond satisfied: vertices and mixtures
    w2 = wm2 = -np.inf
    for n in (4, 5, 6, 7):
        for _ in range(3):
            a = rng.choice((-1, 1), size=n)
            w, wm = ising_reference_case(n, random_couplings(n, a, "complete", scale=0.6), 0.7 * rng.normal(size=n),
                                         rng.uniform(0.4, 2.0), a, exact=False)
            w2 = max(w2, w); wm2 = max(wm2, wm)
    out.append(f"    complete graphs on 4..7 sites, every bond satisfied (12 references, 1200 members): "
               f"max of TV - sum of deficits = {w2:+.2e}; max of mu(x_j = a_j) - mu*(x_j = a_j) = {wm2:+.2e}")
    ok &= w2 < 1e-9 and wm2 < 1e-9
    # (iii) a violated bond can break both bounds: chains of three sites with one bond violated
    wv = []; wp = []
    for _ in range(5):
        n = 3; a = rng.choice((-1, 1), size=n)
        Jm = random_couplings(n, a, "chain", floor=0.3); Jm[0, 1] = -Jm[0, 1]
        w, wm = ising_reference_case(n, Jm, 0.7 * rng.normal(size=n), rng.uniform(0.4, 2.0), a)
        wv.append(w); wp.append(wm)
    out.append("    chains of three sites with one bond violated by the centre (5 cases, exact): max of TV - sum of deficits = "
               + ", ".join(f"{v:+.3f}" for v in wv) + "; max of mu(x_j = a_j) - mu*(x_j = a_j) = "
               + ", ".join(f"{v:+.3f}" for v in wp))
    ok &= min(wv) > 1e-3 and min(wp) > 1e-3
    # (iv) the two examples of the internal review ER2 (F1):
    #      two sites, pi ~ exp(-x1 x2 / 2), centre (+,+), b = 1: both excesses equal 0.169599... (closed form);
    #      a triangle with one violated bond for which both bounds hold all the same.
    Jm = np.zeros((2, 2)); Jm[0, 1] = -0.5
    w, wm = ising_reference_case(2, Jm, np.zeros(2), 1.0, np.array([1, 1]))
    e2 = np.exp(2.0)
    # closed form of the excess: (mu(x1 = +) - mu*(x1 = +)) with mu = (1, e^2, 1, 1)/(3 + e^2) in the order
    # e = (00, 01, 10, 11), mu* = (1, 1, 1, e^-2)/(3 + e^-2): the excess equals the population excess
    pop = (1 + e2) / (3 + e2) - 2 / (3 + 1 / e2)
    out.append(f"    two sites, pi ~ exp(-x1 x2/2), centre (+,+), b = 1: max of TV - sum of deficits = {w:+.6f}, "
               f"max population excess = {wm:+.6f} (closed form {pop:+.6f})")
    ok &= abs(w - pop) < 1e-7 and abs(wm - pop) < 1e-7
    Jm = np.zeros((3, 3)); Jm[0, 1] = 1.0; Jm[1, 2] = 1.0; Jm[0, 2] = -0.5
    w, wm = ising_reference_case(3, Jm, np.zeros(3), 1.0, np.array([1, 1, 1]))
    out.append(f"    triangle pi ~ exp(x1 x2 + x2 x3 - x1 x3/2), centre (+,+,+), b = 1 (bond 1-3 violated): "
               f"max of TV - sum of deficits = {w:+.2e}, max population excess = {wm:+.2e}: both bounds hold")
    ok &= w < 1e-9 and wm < 1e-9
    # (v) the hypothesis of E15T(a): positive association of mu*_a in the disagreement variables, decided exactly by
    #     the covariances of the indicators of all pairs of up-sets (every monotone function is a positive
    #     combination of such indicators and a constant).  The triangle of (iv) is positively associated although it
    #     is not log-supermodular; the two-site example is not.
    def polarised_ising(n, Jm, b):
        es = list(itertools.product((0, 1), repeat=n))
        lw = np.array([sum(Jm[i, j] * (1 - 2 * e[i]) * (1 - 2 * e[j]) for i in range(n) for j in range(i + 1, n))
                       - b * sum(e) for e in es])
        p = np.exp(lw - lw.max())
        return es, p / p.sum()

    def association(es, p):
        n = len(es[0]); idx = {e: k for k, e in enumerate(es)}
        ups = []
        for mask in range(1 << len(es)):
            U = [k for k in range(len(es)) if mask >> k & 1]
            Uset = set(U)
            if all(idx[tuple(max(es[k][i], int(i == j)) for i in range(n))] in Uset for k in U for j in range(n)):
                ups.append(np.array([1.0 if k in Uset else 0.0 for k in range(len(es))]))
        worst = min(float(p @ (u * v) - (p @ u) * (p @ v)) for u in ups for v in ups)
        return len(ups), worst

    def log_supermodular(es, p):
        n = len(es[0]); idx = {e: k for k, e in enumerate(es)}
        worst = np.inf
        for e in es:
            for f in es:
                jn = tuple(max(x, y) for x, y in zip(e, f)); mt = tuple(min(x, y) for x, y in zip(e, f))
                worst = min(worst, p[idx[jn]] * p[idx[mt]] - p[idx[e]] * p[idx[f]])
        return worst

    Jm = np.zeros((3, 3)); Jm[0, 1] = 1.0; Jm[1, 2] = 1.0; Jm[0, 2] = -0.5
    es, p = polarised_ising(3, Jm, 1.0)
    nu, cov3 = association(es, p); ls3 = log_supermodular(es, p)
    Jm = np.zeros((2, 2)); Jm[0, 1] = -0.5
    es2, p2 = polarised_ising(2, Jm, 1.0)
    nu2, cov2 = association(es2, p2)
    out.append(f"    hypothesis of E15T(a): the triangle's mu*_a: least covariance of two up-set indicators ({nu} up-sets) "
               f"= {cov3:+.2e} (positively associated), least lattice defect = {ls3:+.3e} (not log-supermodular); "
               f"the two-site example: least covariance ({nu2} up-sets) = {cov2:+.4f} (not positively associated)")
    ok &= nu == 20 and nu2 == 6 and cov3 > -1e-12 and ls3 < -1e-6 and cov2 < -1e-3
    return ok, out


def proper_upsets(E):
    """Indicator vectors (rows) of all up-sets of the 0/1 vectors E (rows; coordinate-wise order) except the empty
    set and the whole set."""
    M, n = E.shape
    index = {tuple(int(v) for v in e): k for k, e in enumerate(E)}
    up = [[index[tuple(int(v) if i != j else 1 for i, v in enumerate(e))] for j in range(n) if e[j] == 0] for e in E]
    out = []
    for mask in range(1, (1 << M) - 1):
        if all(mask >> q & 1 for k in range(M) if mask >> k & 1 for q in up[k]):
            out.append([mask >> k & 1 for k in range(M)])
    return np.array(out, dtype=float)


def upset_criteria(nu, E, inds):
    """Slacks of the four conditions of Proposition E15U for a measure nu on the rows of E:
    (A) positive association: min over pairs of up-sets of Cov(1_U, 1_W);
    (B) min over up-sets U and sites i of Cov(1_U, e_i);
    (C) min over up-sets U of Cov(1_U, N) - Var(1_U), N the number of disagreements;
    (D) min over sites i of Cov(e_i, N - e_i)."""
    Nd = E.sum(axis=1); pU = inds @ nu; pe = nu @ E
    A = float(((inds * nu) @ inds.T - np.outer(pU, pU)).min())
    B = float(((inds * nu) @ E - np.outer(pU, pe)).min())
    C = float((inds @ (nu * Nd) - pU * (nu @ Nd) - pU * (1 - pU)).min())
    D = float(min(nu @ (E[:, i] * (Nd - E[:, i])) - pe[i] * (nu @ (Nd - E[:, i])) for i in range(E.shape[1])))
    return A, B, C, D


def test_F7():
    """Proposition E15U: exact criteria on up-sets."""
    out = []; ok = True
    # (i) the criteria against exact maximisation over the class polytope: three sites, couplings of both signs,
    #     random fields; equal slopes in half of the cases, one slope per site in the other half
    n = 3; agreeC = agreeB = holdC = holdB = holdA = 0; cases = 40
    for t in range(cases):
        a = rng.choice((-1, 1), size=n)
        Jm = np.zeros((n, n))
        for i in range(n):
            for j in range(i + 1, n):
                Jm[i, j] = rng.normal() * rng.choice((0.3, 1.0))
        h = 0.7 * rng.normal(size=n)
        b = rng.uniform(0.3, 2.0) if t % 2 == 0 else rng.uniform(0.3, 2.0, size=n)
        tv, pop = ising_reference_case(n, Jm, h, b, a)
        X = cube(n); E = (X != a).astype(float)
        logpi = X @ h + sum(Jm[i, j] * X[:, i] * X[:, j] for i in range(n) for j in range(i + 1, n))
        nu = np.exp(logpi - E @ np.broadcast_to(np.asarray(b, dtype=float), (n,))); nu /= nu.sum()
        cA, cB, cC, cD = upset_criteria(nu, E, proper_upsets(E))
        agreeC += (cC >= -1e-12) == (tv <= 1e-9); agreeB += (cB >= -1e-12) == (pop <= 1e-9)
        holdC += cC >= -1e-12; holdB += cB >= -1e-12; holdA += cA >= -1e-12
    out.append(f"    three sites, {cases} references with couplings of both signs (half with one slope per site): the up-set "
               f"criterion (C) agrees with the exact maximum of TV - sum of deficits in {agreeC}/{cases}, the criterion (B) with "
               f"the exact maximal population excess in {agreeB}/{cases}; (C) holds in {holdC}, (B) in {holdB}, positive "
               f"association in {holdA}")
    ok &= agreeC == cases and agreeB == cases and holdA <= holdB and holdA <= holdC and holdC < cases
    # (ii) a pure three-body known part: mu*_a(e) = (1 - lam (-1)^N(e)) / 8 on three sites.  All pair covariances
    #      vanish; the criterion (C) holds iff lam <= 1/2 (slack (1 - 2 lam)/16 at U = {e_2 = 1 or e_3 = 1}).
    a = np.array([1, 1, 1]); X = cube(3); E = (X != a).astype(float); Nd = E.sum(axis=1); inds = proper_upsets(E)
    line = []
    U23 = ((E[:, 1] + E[:, 2]) > 0).astype(float)                    # the up-set {e_2 = 1 or e_3 = 1}
    for lam, label in ((11 / 13, "11/13"), (1 / 2, "1/2"), (1 / 3, "1/3")):
        nu = (1 - lam * (-1.0) ** Nd) / 8
        cA, cB, cC, cD = upset_criteria(nu, E, inds)
        pair = max(abs(nu @ (E[:, i] * E[:, j]) - (nu @ E[:, i]) * (nu @ E[:, j])) for i in range(3) for j in range(i + 1, 3))
        pU = nu @ U23; s23 = nu @ (U23 * Nd) - pU * (nu @ Nd) - pU * (1 - pU)
        tv, pop = ising_reference_case(3, None, None, 1.0, a, logpi=np.log(nu) + 1.0 * Nd)
        line.append(f"lam = {label}: largest pair covariance {pair:.1e}; slack of (C) at U = {{e_2 or e_3}}: {s23:+.6f} "
                    f"(formula (1 - 2 lam)/16 = {(1 - 2 * lam) / 16:+.6f}), least slack over all up-sets {cC:+.6f}; exact max "
                    f"of TV - sum of deficits = {tv:+.6f}")
        ok &= pair < 1e-12 and abs(s23 - (1 - 2 * lam) / 16) < 1e-12 and abs(cC - min((1 - 2 * lam) / 16, 0.0)) < 1e-12
        ok &= (tv > 1e-6) == (lam > 0.5 + 1e-9) and abs(cD) < 1e-12
    out.append("    pure three-body known part on three sites, mu*_a = (1 - lam (-1)^N)/8, slope 1: " + "; ".join(line))
    # (iii) the n necessary conditions (D): Cov(e_i, N - e_i) >= 0 for every site.  They are not sufficient for
    #       pair-interaction known parts either: an explicit instance on four sites (found by an adversarial
    #       search; two strongly bound pairs {1,3}, {2,4} that repel each other), with the member of density
    #       proportional to 1 + (e^2 - 1) 1_U, U = {e_2 = e_4 = 1}, slopes 1, which violates the bound.
    n = 4; X = cube(n); E = (X != np.ones(n)).astype(float); Nd = E.sum(axis=1); inds = proper_upsets(E)
    K = np.zeros((n, n)); K[np.triu_indices(n, 1)] = [-1.4, 6.0, -2.6, -0.5, 3.3, 0.0]; lin = np.array([0.1, 0.5, -1.0, 1.4])
    lw = np.einsum("ki,ij,kj->k", E, K, E) + E @ lin
    nu = np.exp(lw - lw.max()); nu /= nu.sum()
    cA, cB, cC, cD = upset_criteria(nu, E, inds)
    U = E[:, 1] * E[:, 3]; pU = nu @ U
    sU = nu @ (U * Nd) - pU * (nu @ Nd) - pU * (1 - pU)
    gapU = (nu @ (U * Nd)) / pU - (nu @ ((1 - U) * Nd)) / (1 - pU)
    tt = np.exp(2.0) - 1; mu = (1 + tt * U) / (1 + tt * pU) * nu
    tv = 0.5 * np.abs(mu - nu).sum(); deficits = float((mu - nu) @ Nd)
    # the member: w = mu / pi with pi = nu e^{+N} must satisfy w(y) <= e^{d_H(x, y)} w(x) for all pairs
    w = mu / (nu * np.exp(Nd)); dH = (X[:, None, :] != X[None, :, :]).sum(axis=2)
    member = bool(np.all(np.log(w)[None, :] - np.log(w)[:, None] <= dH + 1e-12))
    out.append(f"    pair-interaction known part on four sites, K = (K12, K13, K14, K23, K24, K34) = (-1.4, 6, -2.6, -0.5, 3.3, 0), "
               f"fields (0.1, 0.5, -1, 1.4) in e: least Cov(e_i, N - e_i) = {cD:+.4f} (the conditions (D) hold); at "
               f"U = {{e_2 = e_4 = 1}}: E[N | U] - E[N | U^c] = {gapU:.4f} < 1, slack of (C) = {sU:+.4f}; the member with "
               f"density ~ 1 + (e^2 - 1) 1_U (in the class: {member}) has TV = {tv:.4f} > sum of deficits = {deficits:.4f}")
    ok &= cD > 1e-3 and sU < -1e-3 and gapU < 1 and member and tv > deficits + 1e-3 and abs(cC - sU) < 0.05
    line = []
    for n, trials in ((3, 2000), (4, 1000)):
        X = cube(n); E = (X != np.ones(n)).astype(float); inds = proper_upsets(E)
        differ = bothhold = assoc = 0
        for _ in range(trials):
            K = np.triu(rng.normal(size=(n, n)) * rng.choice((0.3, 1.0, 2.5)), 1); lin = rng.normal(size=n)
            lw = np.einsum("ki,ij,kj->k", E, K, E) + E @ lin
            nu = np.exp(lw - lw.max()); nu /= nu.sum()
            cA, cB, cC, cD = upset_criteria(nu, E, inds)
            differ += (cC >= -1e-12) != (cD >= -1e-12); bothhold += cC >= -1e-12; assoc += cA >= -1e-12
        line.append(f"n = {n} ({len(inds)} up-sets), {trials} random pair models: (C) and (D) differ in {differ}; (C) holds in "
                    f"{bothhold}, of which positively associated {assoc}")
        ok &= assoc < bothhold
    out.append("    how often (D) fails to decide (C) for random pair-interaction known parts (couplings of both signs): "
               + "; ".join(line) + " — rare, and not never (the instance above)")
    # (iv) weak coupling (consequence 1): pi = pi_0 exp(eps sum J_ij x_i x_j), centre all-plus, slopes b_i; to first
    #      order the bound holds iff s_i = sum_{j != i} J_ij v_j > 0 for every site, v_j = p_j (1 - p_j) under the
    #      polarised member of the product part.  Instances with min_i |s_i| < 0.05 are skipped (undecided at first order).
    n = 4; X = cube(n); E = (X != np.ones(n)).astype(float); inds = proper_upsets(E)
    eps = 0.02; agree = used = holds = 0
    for _ in range(400):
        Jm = np.triu(rng.normal(size=(n, n)), 1); Jm = Jm + Jm.T
        lin0 = rng.normal(size=n); bs = rng.uniform(0.3, 2.0, size=n)
        p0 = 1 / (1 + np.exp(-(lin0 - bs)))                      # nu_0(e_i = 1) for the product part pi_0 ~ exp(lin0.e)
        s1 = Jm @ (p0 * (1 - p0))
        if np.abs(s1).min() < 0.05:
            continue
        lw = E @ (lin0 - bs) + eps * 0.5 * np.einsum("ki,ij,kj->k", X, Jm, X)
        nu = np.exp(lw - lw.max()); nu /= nu.sum()
        cA, cB, cC, cD = upset_criteria(nu, E, inds)
        used += 1; agree += (cC >= -1e-13) == (s1.min() > 0); holds += cC >= -1e-13
    out.append(f"    weak coupling, four sites, eps = {eps}: the sign of min_i sum_j J_ij v_j decides the criterion (C) in "
               f"{agree}/{used} instances (the bound holds in {holds} of them)")
    ok &= agree == used and 0 < holds < used
    return ok, out


def main():
    allok = True
    for name, fn in (("F1 one-body data, cube (Theorem E15)", test_F1), ("F2 general alphabets (Theorem E15)", test_F2),
                     ("F3 members identified by one-body data", test_F3), ("F4 the double cone (Theorem E16)", test_F4),
                     ("F5 modulus duality (Theorem E17)", test_F5),
                     ("F6 an interacting reference (Theorem E15T)", test_F6),
                     ("F7 exact criteria on up-sets (Proposition E15U)", test_F7)):
        ok, out = fn()
        print(f"{name}: {'ok' if ok else 'FAILED'}")
        for line in out:
            print(line)
        allok &= ok
    print("PASS" if allok else "FAIL")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
