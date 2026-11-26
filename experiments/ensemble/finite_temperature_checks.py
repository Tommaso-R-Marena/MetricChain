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


def test_F2():
    """Three-letter sites, random symmetric site envelopes (metrics), non-uniform product reference."""
    out = []; ok = True; worst = -np.inf; cnt = 0
    for n in (2, 3):
        for _ in range(12):
            q = 3
            states = list(itertools.product(range(q), repeat=n)); N = len(states)
            index = {s: k for k, s in enumerate(states)}
            # site metrics: random points on a line scaled
            deltas = []
            for i in range(n):
                pts = np.sort(rng.random(q)) * rng.uniform(0.5, 2.5)
                deltas.append(np.abs(pts[:, None] - pts[None, :]))
            pis = [rng.dirichlet(np.ones(q) * 3) for _ in range(n)]
            pi = np.array([np.prod([pis[i][s[i]] for i in range(n)]) for s in states])
            # class in normalised weights v = pi * w / Z : v(y)/pi(y) <= exp(delta_i) v(x)/pi(x)
            rows = []
            for k, s in enumerate(states):
                for i in range(n):
                    for t in range(q):
                        if t == s[i]:
                            continue
                        y = list(s); y[i] = t; ky = index[tuple(y)]
                        r = np.zeros(N); r[ky] = 1.0 / pi[ky]; r[k] = -np.exp(deltas[i][s[i], t]) / pi[k]
                        rows.append(r)
            A = np.array(rows)
            for _ in range(4):
                # random member
                ptsm = []
                for _ in range(3):
                    res = linprog(rng.normal(size=N), A_ub=A, b_ub=np.zeros(len(A)), A_eq=np.ones((1, N)),
                                  b_eq=[1.0], bounds=[(0, None)] * N, method="highs")
                    ptsm.append(res.x)
                mu = sum(wi * p for wi, p in zip(rng.dirichlet(np.ones(3)), ptsm))
                a = tuple(rng.integers(q, size=n))
                # most polarised product member towards a
                star = []
                for i in range(n):
                    v = pis[i] * np.exp(-deltas[i][a[i]]); star.append(v / v.sum())
                mustar = np.array([np.prod([star[i][s[i]] for i in range(n)]) for s in states])
                tv = 0.5 * np.abs(mu - mustar).sum()
                bound = 0.0
                for i in range(n):
                    marg = sum(mu[k] for k, s in enumerate(states) if s[i] == a[i])
                    assert marg <= star[i][a[i]] + 1e-9          # the marginal bound
                    bound += 1 - marg / star[i][a[i]]
                worst = max(worst, tv - bound); cnt += 1
    out.append(f"    three-letter heterogeneous sites: {cnt} cases, max of TV - sum_i (1 - mu_i(a_i)/mu*_i(a_i)) = {worst:+.2e}")
    ok &= worst < 1e-9
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
    return worst < 1e-7, [f"    modulus duality (200 instances x 4 tolerances): largest gap {worst:.2e}"]


def ising_reference_case(n, Jm, h, b, a, exact=True, samples=25):
    """Class around the Ising reference pi ∝ exp(sum_{i<j} Jm[i,j] x_i x_j + h.x) with slope b; centre a.
    Variables are the weights w = mu / pi (well scaled: w(y) <= e^b w(x), sum pi w = 1).
    Returns (max of TV(mu, mu*_a) - sum_j deficits, max of mu(x_j = a_j) - mu*_a(x_j = a_j)); exact
    maximisation by one LP per sign pattern if `exact`, otherwise over vertices and mixtures of the polytope
    (solver tolerances repaired by the least Lipschitz majorant of -log w)."""
    X = cube(n); N = len(X)
    logpi = X @ h + sum(Jm[i, j] * X[:, i] * X[:, j] for i in range(n) for j in range(i + 1, n))
    pi = np.exp(logpi); pi /= pi.sum()
    index = {tuple(x): k for k, x in enumerate(X)}
    rows = []
    for k, x in enumerate(X):
        for i in range(n):
            y = x.copy(); y[i] = -y[i]; ky = index[tuple(y)]
            r = np.zeros(N); r[ky] = 1.0; r[k] = -np.exp(b)
            rows.append(r)
    A = np.array(rows)
    mustar = pi * np.exp(-b * np.sum(X != a, axis=1)); mustar /= mustar.sum()
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
                g = np.max(g[None, :] - b * dH, axis=1)        # least b-Lipschitz majorant: exact membership
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
    # (iii) the obstruction: a chain of three sites with one bond violated
    wv = []
    for _ in range(5):
        n = 3; a = rng.choice((-1, 1), size=n)
        Jm = random_couplings(n, a, "chain", floor=0.3); Jm[0, 1] = -Jm[0, 1]
        wv.append(ising_reference_case(n, Jm, 0.7 * rng.normal(size=n), rng.uniform(0.4, 2.0), a)[0])
    out.append("    chains of three sites with one bond violated by the centre (5 cases, exact): max of TV - sum of deficits = "
               + ", ".join(f"{v:+.3f}" for v in wv))
    ok &= max(wv) > 1e-3
    return ok, out


def main():
    allok = True
    for name, fn in (("F1 one-body data, cube (Theorem E15)", test_F1), ("F2 general alphabets (Theorem E15)", test_F2),
                     ("F3 members identified by one-body data", test_F3), ("F4 the double cone (Theorem E16)", test_F4),
                     ("F5 modulus duality (Theorem E17)", test_F5),
                     ("F6 an interacting reference (Theorem E15T)", test_F6)):
        ok, out = fn()
        print(f"{name}: {'ok' if ok else 'FAILED'}")
        for line in out:
            print(line)
        allok &= ok
    print("PASS" if allok else "FAIL")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
