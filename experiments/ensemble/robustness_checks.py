#!/usr/bin/env python3
"""Checks for docs/ensemble/ENSEMBLE_REPORT.md, Part VIII, section 4e.4 (graded answers; written in reply to the
Frontier Benchmarking division's mathematical feedback E-1 ... E-5): Propositions E23.1(d), E17.2, E30, E31, E4.1.

R1  Gains and offsets with tolerances (E23.1(d)): in the variables (nu, t = 1/gain, offset/gain) the compatible set
    is a polyhedron; the interval of a target from one linear programme against a scan over the gain.
R2  Error sets that are not boxes (E17.2): the tolerance term of a certificate is the support function of the error
    set -- low-rank-plus-box (two linear programmes, primal and dual) and ellipsoids (dual bound against a primal
    search).
R3  Refining the pool (E30): the interval on an h-net at tolerance tau + L h, widened by L_psi h, contains the
    interval on the full space, which contains the interval on the net; the pool-robust mass bound.
R4  The identifiability radius (E31): R_TV = the largest width of the interval of a population over all subsets;
    exact by enumeration on small spaces; the bounds max_x w_x <= R_TV <= (1/2) sum_x w_x; 'R_TV = 1' on the
    instances built from the partition problem.
R5  Quantitative Renyi-Heppes (E4.1): laws of m features on a grid known within eps in total variation; the largest
    mass off the K conformers against m eps / (m - K (r - 1)).

Random seeds are fixed.  Linear programmes: scipy HiGHS.  About one minute.
"""
import itertools
import sys

import numpy as np
from scipy.optimize import linprog, minimize

rng = np.random.default_rng(20261127)
ok = True


def check(name, cond):
    global ok
    ok &= bool(cond)
    print(f"  {name}: {'ok' if cond else 'FAILED'}")


def solve(c, A_ub=None, b_ub=None, A_eq=None, b_eq=None, bounds=None):
    return linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")


# ---------------------------------------------------------------------------------------------------------- R1
def test_R1():
    print("R1  one gain and one offset with tolerances (Proposition E23.1(d))")
    worst_in = worst_gap = 0.0
    cases = 0
    while cases < 60:
        N = int(rng.integers(5, 9))
        m = int(rng.integers(3, 6))
        Phi = rng.uniform(-1, 1, size=(N, m))
        psi = rng.normal(size=N)
        mu = rng.dirichlet(np.ones(N))
        s_true, b_true = rng.uniform(0.5, 2.0), rng.uniform(-0.5, 0.5)
        y = s_true * (mu @ Phi) + b_true
        tau = 0.02
        # variables: nu (N), t = 1/s, bp = b/s ;   t*y - bp*1 - Phi^T nu  in  t*[-tau, tau]
        # i.e.  Phi^T nu - t (y + tau) + bp <= 0   and   -Phi^T nu + t (y - tau) - bp <= 0 ;   gains in [1/3, 4]
        A_ub = np.vstack([np.hstack([Phi.T, -(y + tau)[:, None], np.ones((m, 1))]),
                          np.hstack([-Phi.T, (y - tau)[:, None], -np.ones((m, 1))])])
        b_ub = np.zeros(2 * m)
        A_eq = np.concatenate([np.ones(N), [0.0, 0.0]])[None, :]
        bounds = [(0, None)] * N + [(0.25, 3.0), (None, None)]
        lo = solve(np.concatenate([psi, [0, 0]]), A_ub, b_ub, A_eq, [1.0], bounds)
        hi = solve(-np.concatenate([psi, [0, 0]]), A_ub, b_ub, A_eq, [1.0], bounds)
        if lo.status != 0 or hi.status != 0:
            continue
        # scan over the gain s (t = 1/s in [0.25, 3]) and the offset eliminated by a free variable
        slo, shi = np.inf, -np.inf
        for tt in np.linspace(0.25, 3.0, 221):
            A2 = np.vstack([np.hstack([Phi.T, np.ones((m, 1))]), np.hstack([-Phi.T, -np.ones((m, 1))])])
            b2 = np.concatenate([tt * (y + tau), -tt * (y - tau)])
            Ae = np.concatenate([np.ones(N), [0.0]])[None, :]
            bd = [(0, None)] * N + [(None, None)]
            r1 = solve(np.concatenate([psi, [0]]), A2, b2, Ae, [1.0], bd)
            if r1.status == 0:
                r2 = solve(-np.concatenate([psi, [0]]), A2, b2, Ae, [1.0], bd)
                slo, shi = min(slo, r1.fun), max(shi, -r2.fun)
        cases += 1
        worst_in = max(worst_in, lo.fun - slo, shi + hi.fun)          # the scan must stay inside the LP interval
        worst_gap = max(worst_gap, slo - lo.fun, -hi.fun - shi)        # and approach it
        truth_in = lo.fun - 1e-9 <= mu @ psi <= -hi.fun + 1e-9
        if not truth_in:
            worst_in = 1.0
    print(f"    {cases} random instances (gain in [1/3, 4], free offset, tolerance 0.02): the scan over 221 values of the"
          f" gain never leaves the interval of the single linear programme (largest excess {max(worst_in, 0):.1e}) and"
          f" comes within {worst_gap:.4f} of its ends; the truth is inside in every case")
    check("one linear programme in (nu, 1/gain, offset/gain) gives the interval", worst_in < 1e-7 and worst_gap < 0.02)


# ---------------------------------------------------------------------------------------------------------- R2
def test_R2():
    print("R2  error sets that are not boxes (Proposition E17.2)")
    gap_lp = 0.0
    cases = 0
    while cases < 80:
        N = int(rng.integers(5, 10))
        m = int(rng.integers(3, 6))
        k = int(rng.integers(1, 3))
        Phi = rng.uniform(-1, 1, size=(N, m))
        psi = rng.normal(size=N)
        U = rng.normal(size=(m, k))
        mu = rng.dirichlet(np.ones(N))
        tau = rng.uniform(0.005, 0.05, size=m)
        y = mu @ Phi + U @ rng.normal(size=k) + rng.uniform(-1, 1, size=m) * tau
        # primal: max E psi  s.t.  y - Phi^T nu = U c + e, |e| <= tau, c free
        A_ub = np.vstack([np.hstack([Phi.T, U]), np.hstack([-Phi.T, -U])])
        b_ub = np.concatenate([y + tau, -(y - tau)])
        A_eq = np.concatenate([np.ones(N), np.zeros(k)])[None, :]
        pr = solve(-np.concatenate([psi, np.zeros(k)]), A_ub, b_ub, A_eq, [1.0], [(0, None)] * N + [(None, None)] * k)
        # dual: min  a + lam.y + sum tau |lam|   s.t.  a + lam.Phi(x) >= psi(x),  U^T lam = 0
        nv = 2 * m + 1                                               # lam = p - q, a
        cost = np.concatenate([y + tau, -(y - tau), [1.0]])
        A_ub2 = -np.hstack([Phi, -Phi, np.ones((N, 1))])
        A_eq2 = np.hstack([U.T, -U.T, np.zeros((k, 1))])
        du = solve(cost, A_ub2, -psi, A_eq2, np.zeros(k), [(0, None)] * (2 * m) + [(None, None)])
        if pr.status != 0 or du.status != 0:
            continue
        cases += 1
        gap_lp = max(gap_lp, abs(-pr.fun - du.fun))
    print(f"    low-rank-plus-box error sets, {cases} random instances: the dual bound with the certificate orthogonal to"
          f" the systematic directions equals the primal value (largest difference {gap_lp:.1e})")
    check("systematic directions: the certificate must be orthogonal to them, and then the bound is tight", gap_lp < 1e-7)
    # ellipsoid: dual bound  min_lam  max_x (psi - lam.Phi) + lam.y + rho |S^{1/2} lam|   against a primal search
    worst_weak, worst_gap, cases = 0.0, 0.0, 0
    for _ in range(25):
        N = int(rng.integers(4, 8))
        m = 3
        Phi = rng.uniform(-1, 1, size=(N, m))
        psi = rng.normal(size=N)
        Bm = rng.normal(size=(m, m))
        Sig = Bm @ Bm.T + 0.1 * np.eye(m)
        Sh = np.linalg.cholesky(Sig)
        rho = 0.05
        mu = rng.dirichlet(np.ones(N))
        y = mu @ Phi

        def dual(lam):
            return np.max(psi - Phi @ lam) + lam @ y + rho * np.linalg.norm(Sh.T @ lam)

        best = min((minimize(dual, rng.normal(size=m), method="Nelder-Mead",
                             options={"xatol": 1e-10, "fatol": 1e-12, "maxiter": 20000}).fun for _ in range(6)))
        Sinv = np.linalg.inv(Sig)
        cons = [{"type": "eq", "fun": lambda nu: nu.sum() - 1},
                {"type": "ineq", "fun": lambda nu: rho ** 2 - (y - nu @ Phi) @ Sinv @ (y - nu @ Phi)}]
        prim = -np.inf
        for _ in range(6):
            r = minimize(lambda nu: -(nu @ psi), mu, constraints=cons, bounds=[(0, 1)] * N, method="SLSQP",
                         options={"ftol": 1e-12, "maxiter": 500})
            if r.success:
                prim = max(prim, -r.fun)
        cases += 1
        worst_weak = max(worst_weak, prim - best)
        worst_gap = max(worst_gap, best - prim)
    print(f"    ellipsoidal error sets, {cases} random instances: the primal value never exceeds the dual bound"
          f" (largest excess {max(worst_weak, 0):.1e}) and the two agree within {worst_gap:.1e}")
    check("ellipsoids: the tolerance term is rho times the dual norm", worst_weak < 1e-6 and worst_gap < 1e-4)


# ---------------------------------------------------------------------------------------------------------- R3
def interval(Phi, y, tau, psi):
    N, m = Phi.shape
    A_ub = np.vstack([Phi.T, -Phi.T])
    b_ub = np.concatenate([y + tau, -(y - tau)])
    lo = solve(psi, A_ub, b_ub, np.ones((1, N)), [1.0], [(0, None)] * N)
    hi = solve(-psi, A_ub, b_ub, np.ones((1, N)), [1.0], [(0, None)] * N)
    if lo.status != 0 or hi.status != 0:
        return None
    return lo.fun, -hi.fun


def test_R3():
    print("R3  refining the pool (Proposition E30)")
    viol, cases, widen = 0.0, 0, []
    while cases < 40:
        # the 'full' space: 720 points of a circle; the pool: every q-th point; Lipschitz constants from the functions
        nfull = 720
        th = 2 * np.pi * np.arange(nfull) / nfull
        m = 4
        coef = rng.normal(size=(m, 3))
        Phi = np.stack([c[0] * np.cos(th) + c[1] * np.sin(th) + c[2] * np.cos(2 * th) for c in coef], axis=1)
        L = max(np.sqrt(c[0] ** 2 + c[1] ** 2) + 2 * abs(c[2]) for c in coef)          # sup-norm Lipschitz constant
        pc = rng.normal(size=3)
        psi = pc[0] * np.cos(th) + pc[1] * np.sin(th) + pc[2] * np.cos(2 * th)
        Lpsi = np.sqrt(pc[0] ** 2 + pc[1] ** 2) + 2 * abs(pc[2])
        q = int(rng.choice([12, 20, 30]))
        pool = np.arange(0, nfull, q)
        h = np.pi * q / nfull                                                              # half the spacing
        K = int(rng.integers(1, 4))
        S = rng.choice(pool, size=K, replace=False)
        mu = np.zeros(nfull)
        mu[S] = rng.dirichlet(np.ones(K))
        y = mu @ Phi
        tau = 0.01
        full = interval(Phi, y, tau, psi)
        inner = interval(Phi[pool], y, tau, psi[pool])
        outer = interval(Phi[pool], y, tau + L * h, psi[pool])
        if full is None or inner is None or outer is None:
            continue
        cases += 1
        viol = max(viol, inner[0] - full[0] if inner[0] < full[0] - 1e-9 else 0.0, full[1] - inner[1] if inner[1] > full[1] + 1e-9 else 0.0)
        viol = max(viol, (outer[0] - Lpsi * h) - full[0], full[1] - (outer[1] + Lpsi * h))
        widen.append(((outer[1] + Lpsi * h) - (outer[0] - Lpsi * h)) / max(full[1] - full[0], 1e-9))
    print(f"    {cases} random instances on a circle (720 points; pools of 60, 36 or 24 points): pool interval at tau within"
          f" the full interval within the pool interval at tau + L h widened by L_psi h, largest violation"
          f" {max(viol, 0):.1e}; the outer interval is {np.median(widen):.1f} times as wide as the exact one (median)")
    check("the two pool intervals bracket the exact one", viol < 1e-8)


# ---------------------------------------------------------------------------------------------------------- R4
def pop_interval(Phi, y, tau, mask):
    N = Phi.shape[0]
    A_ub = np.vstack([Phi.T, -Phi.T])
    b_ub = np.concatenate([y + tau, -(y - tau)])
    lo = solve(mask.astype(float), A_ub, b_ub, np.ones((1, N)), [1.0], [(0, None)] * N)
    hi = solve(-mask.astype(float), A_ub, b_ub, np.ones((1, N)), [1.0], [(0, None)] * N)
    return lo.fun, -hi.fun


def tv_radius_exact(Phi, y, tau):
    N = Phi.shape[0]
    best = 0.0
    for bits in range(1, 2 ** (N - 1)):                    # a set and its complement have the same width
        mask = np.array([(bits >> i) & 1 for i in range(N)], dtype=bool)
        lo, hi = pop_interval(Phi, y, tau, mask)
        best = max(best, hi - lo)
    return best


def tv_radius_vertices(Phi, y):
    """tau = 0: the compatible set is a polytope whose vertices have at most m + 1 atoms; R_TV is attained at a pair
    of vertices."""
    N, m = Phi.shape
    verts = []
    Aeq = np.vstack([Phi.T, np.ones((1, N))])
    beq = np.concatenate([y, [1.0]])
    for k in range(1, m + 2):
        for sub in itertools.combinations(range(N), k):
            Ak = Aeq[:, sub]
            sol, res, rank, _ = np.linalg.lstsq(Ak, beq, rcond=None)
            if rank == k and np.linalg.norm(Ak @ sol - beq) < 1e-9 and np.all(sol > 1e-10):
                v = np.zeros(N)
                v[list(sub)] = sol
                verts.append(v)
    best = 0.0
    for a, b in itertools.combinations(verts, 2):
        best = max(best, 0.5 * np.abs(a - b).sum())
    return best, len(verts)


def test_R4():
    print("R4  the identifiability radius (Proposition E31)")
    worst_def, bounds_ok, cases = 0.0, 0, 0
    ratio_up = []
    while cases < 30:
        N = int(rng.integers(5, 9))
        m = int(rng.integers(1, 4))
        Phi = rng.integers(-2, 3, size=(N, m)).astype(float)
        mu = rng.dirichlet(np.ones(N))
        y = mu @ Phi
        R_sets = tv_radius_exact(Phi, y, 0.0)
        R_vert, nv = tv_radius_vertices(Phi, y)
        w = []
        for x in range(N):
            mask = np.zeros(N, dtype=bool)
            mask[x] = True
            lo, hi = pop_interval(Phi, y, 0.0, mask)
            w.append(hi - lo)
        cases += 1
        worst_def = max(worst_def, abs(R_sets - R_vert))
        bounds_ok += (max(w) <= R_sets + 1e-8 and R_sets <= min(1.0, 0.5 * sum(w)) + 1e-8)
        ratio_up.append(min(1.0, 0.5 * sum(w)) / max(R_sets, 1e-12))
    print(f"    {cases} random instances (5 to 8 configurations, exact data): the largest width over all subsets equals the"
          f" largest total-variation distance between two vertices of the compatible polytope (largest difference"
          f" {worst_def:.1e}); max_x w_x <= R_TV <= min(1, (1/2) sum_x w_x) in {bounds_ok}/{cases}; the upper bound is"
          f" {np.median(ratio_up):.2f} times R_TV (median), at most {max(ratio_up):.2f}")
    check("R_TV is the largest width of a population interval; the cheap bounds hold", worst_def < 1e-7 and bounds_ok == cases)
    # hardness: X = {1..n} x {+,-};  data: nu(i,+) + nu(i,-) = 1/n, sum_i a_i nu(i,+) = sum(a)/(2n);  R_TV = 1 iff a splits
    agree = yes = 0
    fam = 40
    for _ in range(fam):
        n = int(rng.integers(3, 7))
        a = [int(v) for v in rng.integers(1, 9, size=n)]
        tot = sum(a)
        reach = {0}
        for v in a:
            reach |= {s + v for s in reach}
        split = (tot % 2 == 0) and (tot // 2 in reach)
        N = 2 * n
        Phi = np.zeros((N, n + 1))
        for i in range(n):
            Phi[2 * i, i] = Phi[2 * i + 1, i] = 1.0
            Phi[2 * i, n] = a[i]
        y = np.concatenate([np.ones(n) / n, [tot / (2 * n)]])
        R, _ = tv_radius_vertices(Phi, y)
        agree += ((R > 1 - 1e-7) == split)
        yes += split
    print(f"    the partition instances: 'two compatible ensembles with disjoint supports exist (R_TV = 1)' agrees with the"
          f" subset-sum table in {agree}/{fam} ({yes} with a split)")
    check("deciding R_TV = 1 encodes the partition problem", agree == fam and 0 < yes < fam)


# ---------------------------------------------------------------------------------------------------------- R5
def test_R5():
    print("R5  quantitative Renyi-Heppes (Proposition E4.1)")
    qp = 5                                                    # the grid F_5 x F_5; features: lines of m slopes
    pts = [(a, b) for a in range(qp) for b in range(qp)]
    N = len(pts)
    worst_ratio, viol, cases = 0.0, 0.0, 0
    for _ in range(40):
        m = int(rng.integers(3, 7))                           # slopes 0..m-1 (m <= 6 = number of directions of F_5^2)
        slopes = list(range(min(m, 5))) + (["inf"] if m == 6 else [])
        feats = []
        for s in slopes:
            feats.append([b if s == "inf" else (a + s * b) % qp for (a, b) in pts])
        feats = np.array(feats)                               # m x N, values in 0..4; two points agree on at most one
        K = int(rng.integers(1, m))                           # r = 2: need m >= K + 1
        S = rng.choice(N, size=K, replace=False)
        mu = np.zeros(N)
        mu[S] = rng.dirichlet(np.ones(K))
        eps = 0.01
        # maximise nu(X \ S) subject to  TV(law_j(nu), law_j(mu)) <= eps  for every feature j
        # variables: nu (N), slacks u_{j,v} >= |nu(T_j = v) - mu(T_j = v)|  (m*qp), with sum_v u_{j,v} <= 2 eps
        nvar = N + m * qp
        A_ub, b_ub = [], []
        for j in range(m):
            for v in range(qp):
                ind = (feats[j] == v).astype(float)
                row = np.zeros(nvar)
                row[:N] = ind
                row[N + j * qp + v] = -1.0
                A_ub.append(row)
                b_ub.append(mu @ ind)
                row2 = np.zeros(nvar)
                row2[:N] = -ind
                row2[N + j * qp + v] = -1.0
                A_ub.append(row2)
                b_ub.append(-(mu @ ind))
            row = np.zeros(nvar)
            row[N + j * qp:N + (j + 1) * qp] = 1.0
            A_ub.append(row)
            b_ub.append(2 * eps)
        cost = np.zeros(nvar)
        off = np.ones(N)
        off[S] = 0.0
        cost[:N] = -off
        A_eq = np.zeros((1, nvar))
        A_eq[0, :N] = 1.0
        res = solve(cost, np.array(A_ub), np.array(b_ub), A_eq, [1.0], [(0, None)] * nvar)
        bound = m * eps / (m - K)
        cases += 1
        viol = max(viol, -res.fun - bound)
        worst_ratio = max(worst_ratio, -res.fun / bound)
    print(f"    {cases} random instances on the 5 x 5 grid (3 to 6 directions of lines, 1 to m - 1 conformers, every law"
          f" within 0.01 in total variation): the largest mass off the conformers never exceeds m eps/(m - K)"
          f" (largest excess {max(viol, 0):.1e}) and reaches {worst_ratio:.3f} of it")
    check("the mass off the conformers is at most m eps / (m - K (r - 1))", viol < 1e-9 and worst_ratio > 0.3)


if __name__ == "__main__":
    test_R1()
    test_R2()
    test_R3()
    test_R4()
    test_R5()
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)
