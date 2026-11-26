#!/usr/bin/env python3
"""Referee checks for Part I (E1, E1.1, E1.2, E2, E3).  Independent implementations."""
import itertools, sys
import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(987654321)


def LP(c, **kw):
    return linprog(c, method="highs", **kw)


# ------------------------------------------------------------------ E1(a)
def cone_T_trivial(Phi, S):
    """T = {h : h _|_ span{1,Phi}, h >= 0 off S} == {0} ?  (definition used in the proof of E1(a)).
    Test: (1) max sum_{x not in S} h(x) over T intersected with a box is 0, and
          (2) (1,Phi) restricted to S has full column rank."""
    m, N = Phi.shape
    F = np.vstack([np.ones((1, N)), Phi])
    comp = [x for x in range(N) if x not in S]
    if np.linalg.matrix_rank(F[:, S], tol=1e-9) < len(S):
        return False
    if not comp:
        return True
    c = np.zeros(N); c[comp] = -1.0
    bounds = [(-1, 1) if x in S else (0, 1) for x in range(N)]
    res = LP(c, A_eq=F, b_eq=np.zeros(m + 1), bounds=bounds)
    assert res.status == 0
    return -res.fun < 1e-9


def direct_identified(Phi, mu):
    """Direct: is mu the only probability vector with data Phi mu?  max |nu - mu|_1-type LPs."""
    m, N = Phi.shape
    F = np.vstack([np.ones((1, N)), Phi])
    b = F @ mu
    for x in range(N):
        for s in (1, -1):
            c = np.zeros(N); c[x] = s
            res = LP(c, A_eq=F, b_eq=b, bounds=[(0, None)] * N)
            assert res.status == 0
            if abs(res.x[x] - mu[x]) > 1e-7:
                return False
    return True


def certificate(Phi, S):
    """(i) rank and (ii) f in span{1,Phi}, f = 0 on S, f >= 1 off S."""
    m, N = Phi.shape
    F = np.vstack([np.ones((1, N)), Phi])
    if np.linalg.matrix_rank(F[:, S], tol=1e-9) < len(S):
        return False, None
    comp = [x for x in range(N) if x not in S]
    if not comp:
        return True, np.zeros(m + 1)
    res = LP(np.zeros(m + 1), A_ub=-F[:, comp].T, b_ub=-np.ones(len(comp)), A_eq=F[:, S].T,
             b_eq=np.zeros(len(S)), bounds=[(None, None)] * (m + 1))
    return res.status == 0, (res.x if res.status == 0 else None)


def test_E1(trials=3000):
    agree = 0; ident = 0; weights_matter = 0
    for _ in range(trials):
        N = int(rng.integers(3, 9)); m = int(rng.integers(1, 5))
        Phi = rng.integers(-1, 2, size=(m, N)).astype(float)
        k = int(rng.integers(1, min(N, 4) + 1))
        if rng.random() < 0.5:
            lam = rng.integers(-1, 2, size=m).astype(float); v = lam @ Phi
            S = [x for x in range(N) if v[x] == v.min()]
        else:
            S = sorted(rng.choice(N, size=k, replace=False).tolist())
        mu = np.zeros(N); w = rng.random(len(S)) + 0.1; mu[S] = w / w.sum()
        mu2 = np.zeros(N); w = rng.random(len(S)) ** 3 + 0.01; mu2[S] = w / w.sum()
        a = direct_identified(Phi, mu); a2 = direct_identified(Phi, mu2)
        b, _ = certificate(Phi, S); c = cone_T_trivial(Phi, S)
        agree += (a == b == c); ident += a; weights_matter += (a != a2)
    print(f"E1(a): direct LP == certificate == cone test in {agree}/{trials}; identified {ident}; "
          f"cases where identification depended on the weights: {weights_matter}")
    return agree == trials and weights_matter == 0


# ------------------------------------------------------------------ E1.1
def test_E11(trials=1500):
    """Both bounds of Proposition E1.1 with data norm l_inf (dual l_1) and with data norm l_1 (dual l_inf)."""
    worst1 = worst2 = -np.inf; used = 0
    for _ in range(trials):
        N = int(rng.integers(4, 9)); m = int(rng.integers(2, 5))
        Phi = rng.normal(size=(m, N))
        k = int(rng.integers(1, 3)); S = sorted(rng.choice(N, size=k, replace=False).tolist())
        f = rng.random(N) + 0.2; f[S] = 0; Phi[0] = f
        ok, a = certificate(Phi, S)
        if not ok:
            continue
        used += 1
        c0, lam = 0.0, np.zeros(m); lam[0] = 1.0          # f = Phi_0 itself is a certificate
        comp = [x for x in range(N) if x not in S]
        gamma = f[comp].min()
        mu = np.zeros(N); w = rng.random(k) + 0.1; mu[S] = w / w.sum()
        for dual, prim in ((1, np.inf), (np.inf, 1)):
            # sigma: min over |h|_1 = 1 on S of |sum h| + |sum h Phi|_prim  (brute force over a fine sample + vertices)
            FS = Phi[:, S]
            cand = []
            if k == 1:
                cand = [np.array([1.0])]
            else:
                for t in np.linspace(-1, 1, 4001):
                    cand.append(np.array([t, 1 - abs(t)])); cand.append(np.array([t, -(1 - abs(t))]))
            sigma = min(abs(h.sum()) + np.linalg.norm(FS @ h, prim) for h in cand)
            R = max(np.linalg.norm(Phi[:, x], prim) for x in range(N))
            lam_dual = np.linalg.norm(lam, dual)
            for _ in range(20):
                nu = rng.dirichlet(np.ones(N) * rng.choice([0.2, 1.0]))
                if rng.random() < 0.5:
                    nu = (1 - 1e-3) * mu + 1e-3 * nu
                err = np.linalg.norm(Phi @ nu - Phi @ mu, prim)
                lhs1 = nu[comp].sum(); rhs1 = lam_dual * err / gamma
                lhs2 = np.abs(nu - mu).sum()
                rhs2 = ((1 + (1 + R) / sigma) * lam_dual / gamma + 1 / sigma) * err
                worst1 = max(worst1, lhs1 - rhs1); worst2 = max(worst2, lhs2 - rhs2 * (1 + 1e-3))
    print(f"E1.1: {used} instances; max (lhs - rhs) mass bound: {worst1:.2e}; TV bound: {worst2:.2e}  (both must be <= 0)")
    return worst1 <= 1e-12 and worst2 <= 1e-9


# ------------------------------------------------------------------ E1.2
def test_E12_example():
    """omega(tau) for the segment+arc example on a fine grid: ratio omega/sqrt(tau) should tend to 2 sqrt 2 (l_inf data norm)."""
    t = np.concatenate([np.linspace(-1, 0, 2001), np.linspace(0, np.pi / 2, 20001)[1:]])
    Phi = np.vstack([np.where(t <= 0, 1.0, np.cos(t)), np.where(t <= 0, t, np.sin(t))])
    rho = np.abs(t)
    out = []
    for tau in (1e-2, 1e-3, 1e-4, 1e-5):
        D = Phi - np.array([[1.0], [0.0]])
        res = LP(-rho, A_ub=np.vstack([D, -D]), b_ub=tau * np.ones(4), A_eq=np.ones((1, len(t))), b_eq=[1.0],
                 bounds=[(0, None)] * len(t))
        out.append((tau, -res.fun, -res.fun / np.sqrt(tau)))
    print("E1.2: tau, omega(tau), omega/sqrt(tau)  [2*sqrt(2) = 2.828]:")
    for o in out:
        print("      %.0e  %.5f  %.4f" % o)
    return abs(out[-1][2] - 2 * np.sqrt(2)) < 0.3


# ------------------------------------------------------------------ E2
def omega_primal(Phi, rho, xs, tau, norm):
    m, N = Phi.shape; D = Phi - Phi[:, [xs]]
    if norm == "inf":
        res = LP(-rho, A_ub=np.vstack([D, -D]), b_ub=tau * np.ones(2 * m), A_eq=np.ones((1, N)), b_eq=[1.0],
                 bounds=[(0, None)] * N)
    else:  # l1 data norm: |D nu|_1 <= tau with slack u >= |D nu|
        c = np.concatenate([-rho, np.zeros(m)])
        A_ub = np.vstack([np.hstack([D, -np.eye(m)]), np.hstack([-D, -np.eye(m)]),
                          np.concatenate([np.zeros(N), np.ones(m)])[None, :]])
        b_ub = np.concatenate([np.zeros(2 * m), [tau]])
        res = LP(c, A_ub=A_ub, b_ub=b_ub, A_eq=np.concatenate([np.ones(N), np.zeros(m)])[None, :], b_eq=[1.0],
                 bounds=[(0, None)] * (N + m))
    assert res.status == 0
    return -res.fun


def omega_dual(Phi, rho, xs, tau, norm):
    """inf_lam tau |lam|_* + max_y [rho(y) - lam.(Phi(y)-Phi(xs))]"""
    m, N = Phi.shape; D = Phi - Phi[:, [xs]]
    if norm == "inf":       # dual norm l1: lam = p - q
        c = np.concatenate([tau * np.ones(2 * m), [1.0]])
        A_ub = np.hstack([-D.T, D.T, -np.ones((N, 1))])
        res = LP(c, A_ub=A_ub, b_ub=-rho, bounds=[(0, None)] * (2 * m) + [(None, None)])
    else:                   # dual norm l_inf: |lam_i| <= s
        c = np.concatenate([np.zeros(m), [tau, 1.0]])
        A1 = np.hstack([-D.T, np.zeros((N, 1)), -np.ones((N, 1))])
        A2 = np.hstack([np.eye(m), -np.ones((m, 1)), np.zeros((m, 1))])
        A3 = np.hstack([-np.eye(m), -np.ones((m, 1)), np.zeros((m, 1))])
        res = LP(c, A_ub=np.vstack([A1, A2, A3]), b_ub=np.concatenate([-rho, np.zeros(2 * m)]),
                 bounds=[(None, None)] * m + [(0, None), (None, None)])
    if res.status != 0:
        return None
    return res.fun


def kappa(Phi, rho, xs, norm):
    m, N = Phi.shape; D = Phi - Phi[:, [xs]]
    if norm == "inf":
        res = LP(np.ones(2 * m), A_ub=np.hstack([-D.T, D.T]), b_ub=-rho, bounds=[(0, None)] * (2 * m))
    else:
        c = np.concatenate([np.zeros(m), [1.0]])
        A1 = np.hstack([-D.T, np.zeros((N, 1))])
        A2 = np.hstack([np.eye(m), -np.ones((m, 1))]); A3 = np.hstack([-np.eye(m), -np.ones((m, 1))])
        res = LP(c, A_ub=np.vstack([A1, A2, A3]), b_ub=np.concatenate([-rho, np.zeros(2 * m)]),
                 bounds=[(None, None)] * m + [(0, None)])
    return res.fun if res.status == 0 else np.inf


def test_E2(trials=600):
    gap = 0.0; lin = 0.0; fin = 0; viol = 0; mism = 0; attained_fail = 0
    for _ in range(trials):
        N = int(rng.integers(3, 10)); m = int(rng.integers(1, 5))
        P = rng.random((N, 2)); d = np.linalg.norm(P[:, None] - P[None], axis=2)
        xs = int(rng.integers(N))
        kind = rng.integers(3)
        if kind == 0:
            Phi = rng.normal(size=(m, N))
        elif kind == 1:
            Phi = rng.integers(-1, 2, size=(m, N)).astype(float)
        else:
            Phi = rng.normal(size=(m, N)); Phi[0] = d[xs] * (0.5 + rng.random(N))
        rho = d[xs].copy()
        if rng.random() < 0.3:      # a non-metric loss: any continuous rho >= 0 with rho(xs) = 0
            rho = rng.random(N); rho[xs] = 0
        for norm in ("inf", "l1"):
            for tau in (0.0, 1e-3, 0.05, 0.7):
                a = omega_primal(Phi, rho, xs, tau, norm); b = omega_dual(Phi, rho, xs, tau, norm)
                if b is None:
                    attained_fail += (tau > 0)     # for tau > 0 the dual must be solvable
                    continue
                gap = max(gap, abs(a - b))
            kap = kappa(Phi, rho, xs, norm)
            # kappa finite  <=>  delta_xs identified (rho > 0 off xs here) ?
            mu = np.zeros(N); mu[xs] = 1
            idt = direct_identified(Phi, mu)
            if (rho[np.arange(N) != xs] > 0).all():
                mism += (np.isfinite(kap) != idt)
            if np.isfinite(kap):
                fin += 1
                for tau in (1e-5, 1e-3, 1e-1, 1.0, 10.0):
                    w = omega_primal(Phi, rho, xs, tau, norm)
                    viol += (w > kap * tau + 1e-8)
                lin = max(lin, abs(omega_primal(Phi, rho, xs, 1e-6, norm) / 1e-6 - kap) / max(kap, 1e-9))
            else:
                # kappa = inf: sup omega/tau must be infinite; on a finite X this means omega(0) > 0
                if omega_primal(Phi, rho, xs, 0.0, norm) < 1e-9:
                    mism += 1
    print(f"E2: duality gap {gap:.2e}; dual infeasible at tau>0: {attained_fail}; kappa finite {fin}; "
          f"omega <= kappa tau violated {viol}; |omega(1e-6)/1e-6 - kappa|/kappa {lin:.2e}; "
          f"(kappa finite) != (delta identified) or kappa=inf with omega(0)=0: {mism}")
    return gap < 1e-7 and viol == 0 and lin < 1e-5 and mism == 0 and attained_fail == 0


def test_E21():
    n = 4; X = np.array(list(itertools.product((0, 1), repeat=n)), dtype=float).T
    rho = X.sum(axis=0); xs = 0
    k_inf = kappa(X, rho, xs, "inf"); k_l1 = kappa(X, rho, xs, "l1")
    print(f"E2.1: cube n=4: kappa (l_inf errors) = {k_inf:.3f} (claim n = 4); kappa (l_1 errors) = {k_l1:.3f} (claim 1)")
    return abs(k_inf - n) < 1e-8 and abs(k_l1 - 1) < 1e-8


# ------------------------------------------------------------------ E3
def kr_norm(d, h):
    N = len(h); rows = []; rhs = []
    for i in range(N):
        for j in range(N):
            if i != j:
                r = np.zeros(N); r[i] = 1; r[j] = -1; rows.append(r); rhs.append(d[i, j])
    res = LP(-h, A_ub=np.array(rows), b_ub=np.array(rhs), A_eq=np.eye(N)[[0]], b_eq=[0.0], bounds=[(None, None)] * N)
    assert res.status == 0
    return -res.fun, res.x


def polytope_vertices(Aeq, beq, Aub, bub, N):
    """all vertices of {x : Aeq x = beq, Aub x <= bub} in R^N by brute force."""
    V = []
    ne = Aeq.shape[0]
    for act in itertools.combinations(range(Aub.shape[0]), N - ne):
        A = np.vstack([Aeq, Aub[list(act)]]); b = np.concatenate([beq, bub[list(act)]])
        if abs(np.linalg.det(A)) < 1e-10:
            continue
        x = np.linalg.solve(A, b)
        if (Aub @ x <= bub + 1e-9).all():
            V.append(x)
    return V


def kappa_g(Phi, S, g):
    m, N = Phi.shape; comp = [x for x in range(N) if x not in S]
    c = np.concatenate([np.ones(2 * m), [0.0]])
    A_eq = np.hstack([Phi[:, S].T, -Phi[:, S].T, np.ones((len(S), 1))])
    A_ub = -np.hstack([Phi[:, comp].T, -Phi[:, comp].T, np.ones((len(comp), 1))]) if comp else None
    res = LP(c, A_ub=A_ub, b_ub=(-g[comp] if comp else None), A_eq=A_eq, b_eq=g[S],
             bounds=[(0, None)] * (2 * m) + [(None, None)])
    return res.fun if res.status == 0 else np.inf


def test_E3(trials=80):
    """omega_mu(tau) computed DIRECTLY (vertices of the feasible set of nu, convex objective W1) against kappa_mu*tau."""
    worst_eq = 0.0; worst_ub = -np.inf; worst_b = 0.0; strict_beyond = 0; done = 0; wdep = 0.0; exceed = 0
    while done < trials:
        N = int(rng.integers(4, 7)); m = int(rng.integers(1, 4))
        P = rng.random((N, 2)); d = np.linalg.norm(P[:, None] - P[None], axis=2)
        k = int(rng.integers(1, 3)); S = sorted(rng.choice(N, size=k, replace=False).tolist())
        Phi = rng.normal(size=(m, N)); f = rng.random(N) + 0.3; f[S] = 0; Phi[0] = f
        if not cone_T_trivial(Phi, S):
            continue
        comp = [x for x in range(N) if x not in S]
        # T_1 = {sum h = 0, h >= 0 off S, |Phi h|_inf <= 1}
        Aub = np.vstack([-np.eye(N)[comp], Phi, -Phi]); bub = np.concatenate([np.zeros(len(comp)), np.ones(2 * m)])
        VT = polytope_vertices(np.ones((1, N)), np.zeros(1), Aub, bub, N)
        if not VT:
            continue
        vals = [kr_norm(d, h) for h in VT]
        kmu = max(v for v, _ in vals); gstar = vals[int(np.argmax([v for v, _ in vals]))][1]
        hinf = max(np.abs(h).max() for h in VT)
        worst_b = max(worst_b, abs(kappa_g(Phi, S, gstar) - kmu) / kmu)
        for _ in range(40):                                  # random 1-Lipschitz g must not exceed kappa_mu
            a = rng.integers(N, size=3)
            g = rng.choice([-1, 1]) * np.minimum.reduce([d[a[0]] + rng.random(), d[a[1]] + rng.random(), d[a[2]] + 2])
            exceed += (kappa_g(Phi, S, g) > kmu + 1e-7)
        ratios = []
        for rep in range(2):
            mu = np.zeros(N); w = rng.random(k) ** (1 + 2 * rep) + 0.05; mu[S] = w / w.sum()
            tau0 = mu[S].min() / hinf
            for mult in (0.3, 1.0, 3.0, 30.0):
                tau = mult * tau0
                # feasible set of nu directly
                Aub2 = np.vstack([-np.eye(N), Phi, -Phi])
                bub2 = np.concatenate([np.zeros(N), Phi @ mu + tau, -(Phi @ mu) + tau])
                Vn = polytope_vertices(np.ones((1, N)), np.ones(1), Aub2, bub2, N)
                om = max(kr_norm(d, nu - mu)[0] for nu in Vn)
                worst_ub = max(worst_ub, om - kmu * tau)
                if mult <= 1.0:
                    worst_eq = max(worst_eq, abs(om - kmu * tau) / (kmu * tau))
                    ratios.append(om / tau)
                elif om < kmu * tau * (1 - 1e-6):
                    strict_beyond += 1
        wdep = max(wdep, (max(ratios) - min(ratios)) / kmu)
        done += 1
    print(f"E3: {trials} identified supports; max rel |omega - kappa tau| for tau <= tau0: {worst_eq:.2e}; "
          f"max (omega - kappa tau) over all tau: {worst_ub:.2e}; (b) sup-min at KR potential: {worst_b:.2e}; "
          f"random g exceeding kappa_mu: {exceed}; weight dependence of the slope: {wdep:.2e}; "
          f"strict inequality beyond tau0 in {strict_beyond} cases")
    return worst_eq < 1e-6 and worst_ub < 1e-8 and worst_b < 1e-6 and exceed == 0 and wdep < 1e-6


if __name__ == "__main__":
    ok = True
    for fn in (test_E1, test_E11, test_E12_example, test_E2, test_E21, test_E3):
        r = fn(); ok &= bool(r)
        print("   ->", "ok" if r else "FAILED")
    print("ALL OK" if ok else "SOME FAILED")
