#!/usr/bin/env python3
"""ER2: attack on Theorem E15T (thermal union bound with an interacting reference; binary sites).

Class: weights w = mu/pi with w(x^(i)) <= e^{b_i} w(x); centre a; e_i = 1[x_i != a_i];
mu* = pi e^{-sum_i b_i e_i} / Z.  All maxima are exact (one LP per subset of the state space).

U1  references that are log-supermodular in e (Ising, every bond satisfied by a, any fields; plus an
    attractive three-body term): population bound; TV - sum_i [mu*_i - mu_i] ; and the ordered bound
    TV - sum_i [E_mu h_i(x_<i) - mu_i]  for EVERY ordering of the sites.
U2  a violated bond: the smallest explicit counterexample (two sites), and three-site chains.
U3  is the bound false WHENEVER the centre violates a bond ("and only then")?  Triangles with two strong
    satisfied bonds and one weak violated bond.
"""
import itertools, sys, time
import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(1503)


def setup(n, logpi_e, bs):
    """States are e in {0,1}^n (disagreement variables).  logpi_e: function of e."""
    E = np.array(list(itertools.product((0, 1), repeat=n))); N = len(E)
    index = {tuple(e): k for k, e in enumerate(E)}
    lp = np.array([logpi_e(e) for e in E]); pi = np.exp(lp - lp.max()); pi /= pi.sum()
    rows = []
    for k, e in enumerate(E):
        for i in range(n):
            y = e.copy(); y[i] = 1 - y[i]; ky = index[tuple(y)]
            r = np.zeros(N); r[ky] = 1.0 / pi[ky]; r[k] = -np.exp(bs[i]) / pi[k]; rows.append(r)
    R = np.array(rows)
    mustar = pi * np.exp(-(E @ bs)); mustar /= mustar.sum()
    return E, pi, R, mustar


def log_supermodular(E, p, tol=1e-12):
    idx = {tuple(e): k for k, e in enumerate(E)}
    for x in E:
        for y in E:
            j = idx[tuple(np.maximum(x, y))]; m = idx[tuple(np.minimum(x, y))]
            if p[j] * p[m] < p[idx[tuple(x)]] * p[idx[tuple(y)]] * (1 - 1e-10) - tol:
                return False
    return True


def exact_max(R, N, mustar, lin, const):
    best = -np.inf; arg = None
    A_eq = np.ones((1, N)); bounds = [(0, None)] * N; b_ub = np.zeros(len(R))
    for mask in range(1 << N):
        ind = np.array([(mask >> k) & 1 for k in range(N)], dtype=float)
        res = linprog(-(ind + lin), A_ub=R, b_ub=b_ub, A_eq=A_eq, b_eq=[1.0], bounds=bounds, method="highs")
        if res.status != 0:
            raise RuntimeError("LP failed")
        val = -res.fun - ind @ mustar - const
        if val > best:
            best = val; arg = res.x.copy()
    return best, arg


def population_excess(E, R, mustar):
    """max over the class of mu(e_i = 0) - mu*(e_i = 0), for each site."""
    N = len(E); out = []
    for i in range(E.shape[1]):
        row = (E[:, i] == 0).astype(float)
        res = linprog(-row, A_ub=R, b_ub=np.zeros(len(R)), A_eq=np.ones((1, N)), b_eq=[1.0],
                      bounds=[(0, None)] * N, method="highs")
        out.append(-res.fun - row @ mustar)
    return np.array(out)


def ordered_lin(E, mustar, order):
    """Linear functional and constant such that sum_i [E_mu h_i(x_<i) - mu(e_i = 0)] = lin . mu  (const = 0),
    h_i = mu*(e_i = 0 | e_{order[:i]})."""
    N = len(E); lin = np.zeros(N)
    for pos, i in enumerate(order):
        prev = list(order[:pos])
        h = np.zeros(N)
        for k, e in enumerate(E):
            same = np.all(E[:, prev] == e[prev], axis=1) if prev else np.ones(N, dtype=bool)
            h[k] = mustar[same & (E[:, i] == 0)].sum() / mustar[same].sum()
        lin += h - (E[:, i] == 0)
    return lin


def analyse(n, logpi_e, bs, orders="all"):
    E, pi, R, mustar = setup(n, logpi_e, bs); N = len(E)
    pop = population_excess(E, R, mustar)
    agree = (1 - E).astype(float)                      # indicators of e_i = 0, columns = sites
    exc, arg = exact_max(R, N, mustar, agree.sum(axis=1), (agree.T @ mustar).sum())
    out = dict(lsm=log_supermodular(E, mustar), pop=pop.max(), excess=exc, arg=arg, E=E, mustar=mustar, pi=pi)
    if orders:
        ords = list(itertools.permutations(range(n))) if orders == "all" else orders
        worst = -np.inf
        for o in ords:
            lin = ordered_lin(E, mustar, o)
            v, _ = exact_max(R, N, mustar, -lin, 0.0)
            worst = max(worst, v)
        out["ordered"] = worst
    return out


def ising(n, J, h, extra=None):
    def f(e):
        v = sum(J[i][j] * e[i] * e[j] for i in range(n) for j in range(i + 1, n)) + float(np.dot(h, e))
        return v + (extra(e) if extra else 0.0)
    return f


def U1():
    print("U1  log-supermodular references (couplings K_ij e_i e_j with K_ij >= 0 = bonds satisfied by a; any fields)")
    worst = dict(pop=-np.inf, excess=-np.inf, ordered=-np.inf); cnt = 0; lsm_all = True
    for n, reps, graph in ((2, 12, "complete"), (3, 8, "chain"), (3, 8, "complete"), (3, 4, "three-body"), (4, 1, "complete")):
        for _ in range(reps):
            J = np.zeros((n, n))
            for i in range(n):
                for j in range(i + 1, n):
                    if graph != "chain" or j == i + 1:
                        J[i, j] = abs(rng.normal()) * 1.5
            h = rng.normal(size=n) * 1.2; bs = rng.uniform(0.2, 2.5, size=n)
            extra = (lambda e, c=abs(rng.normal()): c * e[0] * e[1] * e[2]) if graph == "three-body" else None
            out = analyse(n, ising(n, J, h, extra), bs, orders="all" if n <= 3 else None)
            lsm_all &= out["lsm"]; cnt += 1
            for k in worst:
                if k in out:
                    worst[k] = max(worst[k], out[k])
    print(f"    {cnt} references (n = 2, 3, 4; chains, triangles, K4, a three-body term), all log-supermodular: {lsm_all}")
    print(f"    largest over the class of mu(x_i=a_i) - mu*(x_i=a_i): {worst['pop']:+.2e}")
    print(f"    largest of TV - sum_i [mu*_i - mu_i]: {worst['excess']:+.2e};  largest of TV - sum_i [E_mu h_i - mu_i] over all orderings: {worst['ordered']:+.2e}")
    return worst["pop"] < 1e-8 and worst["excess"] < 1e-8 and worst["ordered"] < 1e-8


def U2():
    print("U2  a bond violated by the centre")
    # two sites, pi prop. to exp(J x1 x2) with J = -1/2 and a = (+,+): in e, log pi = K e1 e2 + const*(e1+e2), K = 4J = -2
    n = 2; K = -2.0; b = 1.0
    out = analyse(n, lambda e: K * e[0] * e[1] - (K / 2) * (e[0] + e[1]), np.array([b, b]))
    E, mustar, mu = out["E"], out["mustar"], out["arg"]
    print(f"    two sites, pi ~ exp(-x1 x2 / 2), a = (+,+), b = 1 (uniform slopes): log-supermodular in e: {out['lsm']}")
    print(f"      states e = (e1,e2): {[tuple(int(v) for v in e) for e in E]}")
    print(f"      mu*  = {np.round(mustar, 6)};  mu*(x_i = a_i) = {np.round([(mustar[E[:, i] == 0]).sum() for i in range(n)], 6)}")
    print(f"      max over the class of mu(x_1 = a_1) - mu*(x_1 = a_1) = {out['pop']:+.6f}")
    print(f"      max over the class of TV - sum_i [mu*_i - mu_i] = {out['excess']:+.6f}, attained at mu = {np.round(mu, 6)}")
    vals = []
    for _ in range(6):
        n = 3; J = np.zeros((n, n)); J[0, 1] = -(0.3 + abs(rng.normal())) * 1.2; J[1, 2] = (0.3 + abs(rng.normal())) * 1.2
        out = analyse(n, ising(n, J, rng.normal(size=n) * 0.7, None), rng.uniform(0.4, 2.0, size=n), orders=None)
        vals.append((out["excess"], out["pop"]))
    print("    three-site chains, first bond violated (6 cases): (max TV-excess, max population excess) = "
          + ", ".join(f"({a:+.3f}, {p:+.3f})" for a, p in vals))
    return True


def U3():
    print("U3  is the bound false whenever a bond is violated?  Triangles: K12 = K23 = K (satisfied), K13 = -kappa (violated)")
    found = None
    for K, kappa, th, b in ((4.0, 0.2, -2.0, 1.0), (3.0, 0.1, -1.5, 0.7), (6.0, 0.5, -3.0, 1.5), (2.0, 0.05, -1.0, 1.0),
                            (1.0, 0.5, 0.0, 1.0), (4.0, 1.5, -2.0, 1.0)):
        n = 3
        J = np.zeros((n, n)); J[0, 1] = K; J[1, 2] = K; J[0, 2] = -kappa
        h = np.array([th, th, th]); bs = np.array([b, b, b])
        out = analyse(n, ising(n, J, h, None), bs, orders="all")
        # ordered bound for the ordering (1, 3, 2) alone (the site between the two satisfied bonds last)
        E, mustar = out["E"], out["mustar"]
        Rr = setup(n, ising(n, J, h, None), bs)[2]
        v132, _ = exact_max(Rr, len(E), mustar, -ordered_lin(E, mustar, (0, 2, 1)), 0.0)
        print(f"    K = {K}, kappa = {kappa}, field {th}, b = {b}: mu* log-supermodular: {out['lsm']}; "
              f"max population excess {out['pop']:+.2e}; max TV-excess {out['excess']:+.2e}; "
              f"ordered bound, ordering (1,3,2): {v132:+.2e}; worst ordering: {out['ordered']:+.2e}")
        if not out["lsm"] and out["excess"] < 1e-9 and out["pop"] < 1e-9 and found is None:
            found = (K, kappa, th, b)
    if found:
        print(f"    => reference with a violated bond (not log-supermodular) for which BOTH statements of E15T(a) hold exactly: (K, kappa, field, b) = {found}")
    return True


def U4():
    print("U4  the counterexample of finding F1: pi ~ exp(x1 x2 + x2 x3 - x1 x3 / 2), no fields, a = (+,+,+), b = (1,1,1)")
    # in the disagreement variables: K12 = K23 = 4, K13 = -2, linear terms -2 sum_j J_ij = (-1, -4, -1)
    n = 3; J = np.zeros((n, n)); J[0, 1] = 4.0; J[1, 2] = 4.0; J[0, 2] = -2.0
    f = ising(n, J, np.array([-1.0, -4.0, -1.0]), None); bs = np.ones(n)
    out = analyse(n, f, bs, orders=None)
    E, pi, R, mustar = setup(n, f, bs)
    X = 1 - 2 * E
    chk = np.exp(X[:, 0] * X[:, 1] + X[:, 1] * X[:, 2] - 0.5 * X[:, 0] * X[:, 2]); chk /= chk.sum()
    print(f"    reference equals the spin form: {np.abs(chk - pi).max():.1e};  mu* log-supermodular in e: {out['lsm']}")
    print(f"    max over the class of mu(x_i=a_i) - mu*(x_i=a_i): {out['pop']:+.2e};  of TV - sum_i [mu*_i - mu_i]: {out['excess']:+.2e}")
    vals = []
    for o in itertools.permutations(range(n)):
        v, _ = exact_max(R, len(E), mustar, -ordered_lin(E, mustar, o), 0.0)
        vals.append((tuple(i + 1 for i in o), v))
    print("    ordered bound TV - sum_i [E_mu h_i - mu_i], by ordering: " + ", ".join(f"{o}: {v:+.2e}" for o, v in vals))
    return True


def main():
    t0 = time.time()
    ok = U1(); print(f"    -> {'no counterexample' if ok else 'COUNTEREXAMPLE'}  [{time.time() - t0:.0f} s]", flush=True)
    U2(); print(f"    [{time.time() - t0:.0f} s]", flush=True)
    U3(); print(f"    [{time.time() - t0:.0f} s]", flush=True)
    U4(); print(f"    [{time.time() - t0:.0f} s]", flush=True)


if __name__ == "__main__":
    main()
