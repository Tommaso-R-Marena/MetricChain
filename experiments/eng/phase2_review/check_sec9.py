"""Review checks for sections 8 and 9 of CERTIFIED_INFERENCE.md.

Proposition 8.1 (lumping); Theorem 9.1 (flow duality: both alternatives by linear programming, and the
second part on graphs that are NOT strongly connected); Proposition 9.2 (closure under marginalisation,
and its failure for a correlated reference); Corollary 9.3 (formula against a brute-force programme over
the whole cone, binary and ternary sites, with a region); section 9.4 (box hull; every box containing
the class); Proposition 9.4.

Run:  python check_sec9.py
"""
from __future__ import annotations

import itertools

import numpy as np
from scipy.optimize import linprog, minimize, minimize_scalar

import ref

rng = np.random.default_rng(9090)


# ---------------------------------------------------------------- ratio-constrained classes

def cone_extreme(pi, edges, C, f, phi=None, A=None, c=None, sense=+1):
    """sup/inf of E_p f over p ~ pi r, r >= 0, r(x) <= C_xy r(y) on edges, with A E_p phi <= c."""
    N = len(pi)
    rows, rhs = [], []
    for (x, y), cxy in zip(edges, C):
        r = np.zeros(N)
        r[x] += 1.0
        r[y] -= cxy
        rows.append(r)
        rhs.append(0.0)
    if A is not None:
        phi = np.asarray(phi, float).reshape(N, -1)
        for k in range(len(c)):
            rows.append(pi * (phi @ A[k]))
            rhs.append(c[k])
    res = linprog(-sense * pi * f, A_ub=np.array(rows) if rows else None, b_ub=np.array(rhs) if rows else None,
                  A_eq=pi[None, :], b_eq=[1.0], bounds=[(0, None)] * N, method="highs")
    if res.status == 2:
        return None
    if res.status != 0:
        raise RuntimeError(res.message)
    return float(-sense * res.fun)


def product_space(sizes):
    return list(itertools.product(*[range(k) for k in sizes]))


def hamming_edges(states, slopes):
    idx = {s: i for i, s in enumerate(states)}
    edges, C = [], []
    for s in states:
        for i in range(len(s)):
            for v in range(max(t[i] for t in states) + 1):
                if v != s[i]:
                    t = s[:i] + (v,) + s[i + 1:]
                    if t in idx:
                        edges.append((idx[s], idx[t]))
                        C.append(np.exp(slopes[i]))
    return edges, np.array(C)


# ---------------------------------------------------------------- Proposition 8.1

def check_lumping():
    worst = 0.0
    for _ in range(100):
        ncell = int(rng.integers(2, 5))
        sizes = rng.integers(1, 4, ncell)
        cell = np.repeat(np.arange(ncell), sizes)
        N = len(cell)
        u = rng.uniform(0.2, 1, N)
        l = u * rng.uniform(0, 1, N)
        fc = rng.uniform(-1, 1, ncell)
        phic = rng.uniform(-1, 1, (ncell, 1))
        f, phi = fc[cell], phic[cell]
        lc = np.array([l[cell == k].sum() for k in range(ncell)])
        uc = np.array([u[cell == k].sum() for k in range(ncell)])
        w = rng.uniform(l, u)
        y = (w @ phi) / w.sum()
        A, c = ref.box_region(y - 0.05, y + 0.05)
        a = ref.primal_interval(l, u, phi, f, A, c)
        b = ref.primal_interval(lc, uc, phic, fc, A, c)
        worst = max(worst, abs(a[0] - b[0]), abs(a[1] - b[1]))
    print(f"[8.1] interval on X vs interval on the cells: max abs diff = {worst:.2e}")


# ---------------------------------------------------------------- Theorem 9.1

def check_flow_duality():
    agree = tot = 0
    nontrivial = 0
    for _ in range(600):
        N = int(rng.integers(2, 7))
        pairs = [(x, y) for x in range(N) for y in range(N) if x != y]
        k = int(rng.integers(0, len(pairs) + 1))
        sel = rng.choice(len(pairs), size=k, replace=False)
        edges = [pairs[i] for i in sel]
        C = np.exp(rng.normal(0, 1.0, len(edges)))        # includes C < 1: cycles can force r = 0
        a = rng.normal(size=N)
        if rng.random() < 0.3:
            a = -np.abs(a)
            a[rng.integers(N)] *= -0.2
        # verdict 1: is a.r <= 0 on the cone?   max a.r s.t. r in cone, sum r <= 1
        rows = []
        for (x, y), cxy in zip(edges, C):
            r = np.zeros(N)
            r[x] += 1
            r[y] -= cxy
            rows.append(r)
        rows.append(np.ones(N))
        res = linprog(-a, A_ub=np.array(rows), b_ub=np.r_[np.zeros(len(edges)), 1.0],
                      bounds=[(0, None)] * N, method="highs")
        nonpos = (-res.fun) <= 1e-9
        # verdict 2: a flow theta >= 0 with a(x) <= sum_y theta_xy - sum_y C_yx theta_yx
        if len(edges) == 0:
            flow = bool(np.all(a <= 1e-12))
        else:
            M = np.zeros((N, len(edges)))
            for j, ((x, y), cxy) in enumerate(zip(edges, C)):
                M[x, j] += 1.0
                M[y, j] -= cxy
            res2 = linprog(np.zeros(len(edges)), A_ub=-M, b_ub=-a, bounds=[(0, None)] * len(edges), method="highs")
            flow = res2.status == 0
        tot += 1
        agree += int(nonpos == flow)
        nontrivial += int(nonpos and np.any(a > 0))
    print(f"[9.1] 'a.r <= 0 on the cone' <=> 'a flow exists': agree in {agree}/{tot} random graphs"
          f" ({nontrivial} with the property holding and a not <= 0)")

    # second part: V+ = inf{tau : flow exists for some eta} on graphs that are not strongly connected
    worst = 0.0
    cases = 0
    for _ in range(200):
        N = int(rng.integers(3, 7))
        # a DAG-like edge set (x < y only): never strongly connected
        edges = [(x, y) for x in range(N) for y in range(x + 1, N) if rng.random() < 0.5]
        C = np.exp(rng.uniform(0, 1.5, len(edges)))
        pi = rng.dirichlet(np.ones(N))
        f = rng.uniform(-1, 1, N)
        phi = rng.uniform(-1, 1, (N, 1))
        r0 = np.ones(N)
        # a member of the class to place the region: r = 1 is in the class iff all C >= 1 (true here)
        y0 = (pi * r0) @ phi / (pi * r0).sum()
        ylo, yhi = y0 - 0.05, y0 + 0.05
        A, c = ref.box_region(ylo, yhi)
        vp = cone_extreme(pi, edges, C, f, phi, A, c, +1)
        if vp is None:
            continue
        # dual LP: variables tau, eta+, eta-, theta
        E = len(edges)
        nv = 3 + E
        obj = np.zeros(nv)
        obj[0] = 1.0
        rows = np.zeros((N, nv))
        rhs = np.zeros(N)
        for x in range(N):
            # pi(x) (f - tau - (e+ - e-) phi + e+ yhi - e- ylo) - (A^T theta)(x) <= 0
            rows[x, 0] = -pi[x]
            rows[x, 1] = pi[x] * (-phi[x, 0] + yhi[0])
            rows[x, 2] = pi[x] * (phi[x, 0] - ylo[0])
            rhs[x] = -pi[x] * f[x]
        for j, ((x, y), cxy) in enumerate(zip(edges, C)):
            rows[x, 3 + j] -= 1.0
            rows[y, 3 + j] += cxy
        res = linprog(obj, A_ub=rows, b_ub=rhs, bounds=[(None, None)] + [(0, None)] * (2 + E), method="highs")
        if res.status != 0:
            worst = np.inf
            continue
        cases += 1
        worst = max(worst, abs(res.fun - vp))
    print(f"[9.1] second part on graphs that are NOT strongly connected (edges x<y only): primal vs flow dual,"
          f" {cases} instances, max abs diff = {worst:.2e}  (compactness comes from pi > 0, r >= 0)")


# ---------------------------------------------------------------- Proposition 9.2

def check_marginal_closure():
    worst = 0.0
    for _ in range(60):
        sizes = [int(rng.integers(2, 4)) for _ in range(3)]
        states = product_space(sizes)
        pis = [rng.dirichlet(np.ones(k) * 2) for k in sizes]
        pi = np.array([np.prod([pis[i][s[i]] for i in range(3)]) for s in states])
        slopes = rng.uniform(0, 1.5, 3)
        if rng.random() < 0.3:
            slopes[rng.integers(3)] = 0.0
        edges, C = hamming_edges(states, slopes)
        Bsites = sorted(rng.choice(3, size=int(rng.integers(1, 3)), replace=False).tolist())
        statesB = product_space([sizes[i] for i in Bsites])
        piB = np.array([np.prod([pis[i][s[j]] for j, i in enumerate(Bsites)]) for s in statesB])
        edgesB, CB = hamming_edges(statesB, slopes[Bsites])
        idxB = {s: i for i, s in enumerate(statesB)}
        for _ in range(4):
            gB = rng.normal(size=len(statesB))
            g = np.array([gB[idxB[tuple(s[i] for i in Bsites)]] for s in states])
            big = cone_extreme(pi, edges, C, g)
            small = cone_extreme(piB, edgesB, CB, gB)
            worst = max(worst, abs(big - small))
    print(f"[9.2] product reference: sup of random functionals of the B-marginal, whole class vs class on the B sites:"
          f" max abs diff = {worst:.2e}")
    # failure for a correlated reference
    states = product_space([2, 2])
    pi = np.array([0.49, 0.01, 0.01, 0.49])
    slopes = np.array([0.2, 2.0])
    edges, C = hamming_edges(states, slopes)
    g = np.array([s[0] for s in states], float)
    big = cone_extreme(pi, edges, C, g)
    small = cone_extreme(np.array([0.5, 0.5]), [(0, 1), (1, 0)], np.exp([0.2, 0.2]), np.array([0.0, 1.0]))
    print(f"[9.2] correlated reference pi = (.49,.01,.01,.49), slopes (0.2, 2.0): sup p_1(1) over the class = {big:.4f},"
          f" over the one-site class with slope 0.2 = {small:.4f}  -> closure fails, as the note says")


# ---------------------------------------------------------------- Corollary 9.3

def D_plus(pi_i, u_i, g):
    return ref.threshold_max(pi_i, np.exp(u_i) * pi_i, g)


def check_cor93():
    print("[9.3] additive observables: formula vs programme over the whole cone (sites with 2 and 3 states)")
    worst = {1: 0.0, 2: 0.0}
    worst_low = 0.0
    cases = {1: 0, 2: 0}
    for trial in range(80):
        m = 1 if trial % 2 == 0 else 2
        sizes = [int(rng.integers(2, 4)) for _ in range(3)]
        states = product_space(sizes)
        pis = [rng.dirichlet(np.ones(k) * 2) for k in sizes]
        pi = np.array([np.prod([pis[i][s[i]] for i in range(3)]) for s in states])
        slopes = rng.uniform(0.0, 1.5, 3)
        if rng.random() < 0.25:
            slopes[rng.integers(3)] = 0.0
        edges, C = hamming_edges(states, slopes)
        fi = [rng.uniform(-1, 1, k) / 3 for k in sizes]
        phii = [rng.uniform(-1, 1, (k, m)) / 3 for k in sizes]
        f = np.array([sum(fi[i][s[i]] for i in range(3)) for s in states])
        phi = np.array([sum(phii[i][s[i]] for i in range(3)) for s in states])
        # region around the mean of a member of the class
        rho = np.array([np.prod([np.exp(rng.uniform(0, slopes[i])) if s[i] else 1.0 for i in range(3)]) for s in states])
        y0 = (pi * rho) @ phi / (pi * rho).sum()
        half = rng.uniform(0.0, 0.1, m) if rng.random() < 0.8 else np.zeros(m)
        ylo, yhi = y0 - half, y0 + half
        A, c = ref.box_region(ylo, yhi)
        vp = cone_extreme(pi, edges, C, f, phi, A, c, +1)
        vm = cone_extreme(pi, edges, C, f, phi, A, c, -1)
        if vp is None:
            continue

        def dual(eta, sign=+1):
            eta = np.atleast_1d(eta)
            return ref.h_box(eta, ylo, yhi) + sum(D_plus(pis[i], slopes[i], sign * fi[i] - phii[i] @ eta) for i in range(3))

        best = np.inf
        best_low = np.inf
        if m == 1:
            for H in (5.0, 50.0, 500.0, 5000.0):
                best = min(best, minimize_scalar(lambda e: dual([e]), bounds=(-H, H), method="bounded",
                                                 options={"xatol": 1e-12}).fun)
                best_low = min(best_low, minimize_scalar(lambda e: dual([e], -1), bounds=(-H, H), method="bounded",
                                                         options={"xatol": 1e-12}).fun)
        else:
            for x0 in [np.zeros(2)] + [rng.normal(size=2) * s for s in (1, 5, 25)]:
                for sign in (+1, -1):
                    res = minimize(lambda e: dual(e, sign), x0, method="Nelder-Mead",
                                   options={"xatol": 1e-11, "fatol": 1e-13, "maxiter": 20000})
                    for _ in range(3):
                        res = minimize(lambda e: dual(e, sign), res.x, method="Nelder-Mead",
                                       options={"xatol": 1e-12, "fatol": 1e-14, "maxiter": 20000})
                    if sign > 0:
                        best = min(best, res.fun)
                    else:
                        best_low = min(best_low, res.fun)
        cases[m] += 1
        worst[m] = max(worst[m], abs(best - vp))
        worst_low = max(worst_low, abs(-best_low - vm))
    print(f"   m = 1: {cases[1]} instances, max |formula - programme| = {worst[1]:.2e};"
          f"   m = 2: {cases[2]} instances, {worst[2]:.2e};   lower end (formula for -f): {worst_low:.2e}")
    # binary sites: achievable one-site marginals
    worst = 0.0
    for _ in range(40):
        n = 4
        states = product_space([2] * n)
        p1 = rng.uniform(0.1, 0.9, n)
        pi = np.array([np.prod([p1[i] if s[i] else 1 - p1[i] for i in range(n)]) for s in states])
        slopes = rng.uniform(0, 2, n)
        edges, C = hamming_edges(states, slopes)
        i = int(rng.integers(n))
        g = np.array([s[i] for s in states], float)
        hi = cone_extreme(pi, edges, C, g, sense=+1)
        lo = cone_extreme(pi, edges, C, g, sense=-1)
        th = np.log(p1[i] / (1 - p1[i]))
        sig = lambda z: 1 / (1 + np.exp(-z))
        worst = max(worst, abs(hi - sig(th + slopes[i])), abs(lo - sig(th - slopes[i])))
    print(f"   binary sites: range of p_i(1) over the class vs [sigma(theta-u), sigma(theta+u)]: max abs diff = {worst:.2e}")


# ---------------------------------------------------------------- section 9.4

def check_sec94():
    print("[9.4] uniform cube, slope u, target x_1, no observations")
    print("   n    u    V+ class (LP)   sigma(u)    box hull ratio (LP)   e^{un}     V+ box hull   e^{un}/(1+e^{un})"
          "   min over ALL containing boxes of u(A)/l(A^c)")
    for n, u in ((2, 0.5), (3, 0.5), (4, 0.5), (4, 1.0), (5, 0.3)):
        states = product_space([2] * n)
        N = len(states)
        pi = np.full(N, 1.0 / N)
        edges, C = hamming_edges(states, [u] * n)
        g = np.array([s[0] for s in states], float)
        v_class = cone_extreme(pi, edges, C, g)
        # box hull of the normalised ensembles: l(x) = min p(x), u(x) = max p(x)
        lo = np.array([cone_extreme(pi, edges, C, np.eye(N)[x], sense=-1) for x in range(N)])
        hi = np.array([cone_extreme(pi, edges, C, np.eye(N)[x], sense=+1) for x in range(N)])
        v_box = ref.threshold_max(lo, hi, g)
        # every box containing the class: beta(x) - alpha(y) >= u d(x,y); minimise u(A)/l(A^c) = sum_{x in A} max_y m(y) e^{u d(x,y)}
        Aset = [i for i, s in enumerate(states) if s[0] == 1]
        Ac = [i for i, s in enumerate(states) if s[0] == 0]
        dist = lambda a, b: sum(p != q for p, q in zip(states[a], states[b]))
        nv = len(Aset) + len(Ac)        # z_x (x in A), m_y (y in Ac)
        rows, rhs = [], []
        for ix, x in enumerate(Aset):
            for iy, y in enumerate(Ac):
                r = np.zeros(nv)
                r[ix] = -1.0
                r[len(Aset) + iy] = np.exp(u * dist(x, y))
                rows.append(r)
                rhs.append(0.0)
        Aeq = np.zeros((1, nv))
        Aeq[0, len(Aset):] = 1.0
        res = linprog(np.r_[np.ones(len(Aset)), np.zeros(len(Ac))], A_ub=np.array(rows), b_ub=np.array(rhs),
                      A_eq=Aeq, b_eq=[1.0], bounds=[(0, None)] * nv, method="highs")
        print(f"   {n}  {u:.1f}    {v_class:.6f}      {1 / (1 + np.exp(-u)):.6f}    {np.max(hi / lo):10.4f}        {np.exp(u * n):9.4f}"
              f"   {v_box:.6f}      {np.exp(u * n) / (1 + np.exp(u * n)):.6f}          {res.fun:.4f} (= e^(un): {np.exp(u * n):.4f})")
    print("   -> the box hull has ratio e^{un} and V+ = e^{un}/(1+e^{un}); moreover NO box class containing the bounded-influence")
    print("      class does better for this target (last column), which is stronger than the note's statement about 'the smallest'.")


# ---------------------------------------------------------------- Proposition 9.4

def check_prop94():
    worst = -np.inf
    impl_viol = 0
    fired = 0
    for _ in range(400):
        n = int(rng.integers(2, 5))
        states = product_space([2] * n)
        N = len(states)
        idx = {s: i for i, s in enumerate(states)}
        pi = rng.dirichlet(np.ones(N) * 2)
        slopes = rng.uniform(0, 1.0, n)
        # a member of the class: exp of a function with site-wise increments within the slopes
        coef = rng.uniform(-1, 1, n) * slopes
        h = np.array([sum(coef[i] * s[i] for i in range(n)) for s in states])
        # add a non-additive Lipschitz perturbation: min with a constant keeps the Lipschitz property
        h = np.minimum(h, np.quantile(h, rng.uniform(0.3, 1.0)))
        r = np.exp(h)
        Gglob = r.max() / r.min() * float(rng.uniform(1.0, 1.5))
        s = rng.normal(size=N) - rng.uniform(0, 1.5)
        sp, sm = np.maximum(s, 0), np.maximum(-s, 0)
        beta = -pi * sm
        for x in range(N):
            if sp[x] <= 0:
                continue
            # kernel: stay with prob q0, else move to a uniformly chosen neighbour
            q0 = rng.random()
            beta[x] += pi[x] * sp[x] * q0 * 1.0
            for i in range(n):
                t = list(states[x])
                t[i] = 1 - t[i]
                y = idx[tuple(t)]
                beta[y] += pi[x] * sp[x] * (1 - q0) / n * np.exp(slopes[i])
        lhs = float(np.sum(pi * r * s))
        mid = float(np.sum(r * beta))
        rhs = r.max() * np.maximum(beta, 0).sum() - r.min() * np.maximum(-beta, 0).sum()
        worst = max(worst, lhs - mid, mid - rhs)
        cond = Gglob * np.maximum(beta, 0).sum() - np.maximum(-beta, 0).sum() <= 0
        if cond:
            fired += 1
            if lhs > 1e-12:
                impl_viol += 1
    print(f"[9.4 prop] chain of inequalities sum(pi r s) <= sum(r beta) <= max r sum(beta+) - min r sum(beta-):"
          f" max violation = {worst:.2e}; condition held in {fired} cases, implication violated in {impl_viol}")


if __name__ == "__main__":
    check_lumping()
    check_flow_duality()
    check_marginal_closure()
    check_cor93()
    check_sec94()
    check_prop94()
