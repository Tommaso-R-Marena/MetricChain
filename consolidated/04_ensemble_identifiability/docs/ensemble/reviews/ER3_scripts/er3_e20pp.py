#!/usr/bin/env python3
"""ER3 review, Propositions E20' and E20'' (two states on a torus).  Reviewer's own code.

G.  Growth constant.  For a pair (p, q) the best constant is  c_true = inf_phi f(phi) / min(d_p^2, d_q^2);
    E20''(a) claims c_true >= c* = min(1, c_D).  c_true is computed on dense grids (|D| = 2: 1201^2 points,
    |D| = 3: 161^3 points; shared angles add nothing but the limit 1, see below) followed by local minimisation,
    together with the limits at the two states (the ratio is discontinuous there):
        lim inf at p or q  =  min( 1 if E is non-empty,  min_k sum_{l in D, l != k} beta_l ).
    Families: random; nearly coincident angles (beta down to 1e-6); antipodal; mixed.
    Reported: the smallest c_true / c* found (must be >= 1) and where; and separately the smallest value of
    c_true^D / c_D for the differing angles alone (how sharp the proved constant is where it is not trivial).
S.  Stability, part (b): on the 2-torus (|D| = 2) and on the 3-torus (|D| = 2, |E| = 1; |D| = 3) the largest
    int min(d_p^2, d_q^2) dnu over measures on a grid (refined around p and q so that scales down to 1e-3 are
    resolved) whose data are within tau: a linear programme; compared with Lambda tau / c*, Lambda the actual l1
    norm of the coefficients of f, and with the stated bound on Lambda.
W.  Weights, part (c): on the same grids the largest |nu(N_q) - w_q| (two linear programmes) against
    (4 sqrt(eps) + eps + 2 sqrt(2) tau) / beta_max.
I.  E20' itself on a 12^3 grid of the 3-torus: pairs of grid states differing in 2 or 3 angles are identified by
    the products over at most two angles; pairs differing in one angle are not, even with all 27 multilinear
    observables.
"""
import itertools, sys
import numpy as np
from scipy.optimize import linprog, minimize

rng = np.random.default_rng(31104)
TWO_PI = 2 * np.pi


def constants(p, q, D):
    beta = 2 - 2 * np.cos(p[D] - q[D])
    cD = beta.min() / 4 if len(D) >= 3 else beta[0] * beta[1] / (4 * (beta[0] + beta[1]))
    return beta, cD, min(1.0, cD)


def F_and_sums(phi, p, q):
    """phi: (..., d) on the differing angles.  Returns F, A, B."""
    a = 2 - 2 * np.cos(phi - p); b = 2 - 2 * np.cos(phi - q)
    A = a.sum(axis=-1); B = b.sum(axis=-1)
    F = A * B - (a * b).sum(axis=-1)
    return F, A, B


def ctrue_D(p, q, grid):
    """inf of F / min(A, B) over the torus of the differing angles (p, q of length d = 2 or 3)."""
    d = len(p)
    ax = TWO_PI * (np.arange(grid) + 0.37) / grid            # offset: the states are not grid points
    mesh = np.stack(np.meshgrid(*([ax] * d), indexing="ij"), axis=-1).reshape(-1, d)
    F, A, B = F_and_sums(mesh, p, q)
    R = F / np.minimum(A, B)
    order = np.argsort(R)[:12]
    best = R[order[0]]; arg = mesh[order[0]]
    def ratio(x):
        F, A, B = F_and_sums(x, p, q)
        m = min(A, B)
        return F / m if m > 1e-12 else 1e9
    for i in order:
        res = minimize(ratio, mesh[i], method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-14, "maxiter": 3000})
        if res.fun < best:
            best, arg = res.fun, res.x
    beta = 2 - 2 * np.cos(p - q)
    lim = min(beta.sum() - beta[k] for k in range(d))        # limit at the states along coordinate k
    return min(best, lim), best, lim, arg


def test_G():
    print("G. growth constant of E20''(a)")
    ok = True
    rows = []
    # |D| = 2
    fam2 = []
    for _ in range(60):
        fam2.append(("random", rng.uniform(0, TWO_PI, 2), rng.uniform(0, TWO_PI, 2)))
    for d1 in (1e-3, 1e-2, 0.1, 0.5, 1.0, 2.0, np.pi):
        for d2 in (1e-3, 1e-2, 0.1, 0.5, 1.0, 2.0, np.pi):
            p = rng.uniform(0, TWO_PI, 2); fam2.append((f"gaps {d1:g},{d2:g}", p, p + np.array([d1, d2])))
    worst2 = (np.inf, None)
    for name, p, q in fam2:
        beta, cD, cs = constants(np.r_[p], np.r_[q], np.arange(2))
        ct, interior, lim, arg = ctrue_D(p, q, 1201)
        ok &= ct >= cD * (1 - 1e-9)
        rows.append((2, name, beta.min(), beta.max(), ct / cD))
        if ct / cD < worst2[0]:
            worst2 = (ct / cD, (name, p, q, beta, ct, cD, arg, interior, lim))
    r2 = np.array([r[4] for r in rows if r[0] == 2])
    print(f"   |D| = 2, E empty: {len(r2)} pairs (random, and gaps from 1e-3 to pi in each angle): "
          f"c_true / c_D between {r2.min():.3f} and {r2.max():.1f}; (a) violated: {int((r2 < 1 - 1e-9).sum())}")
    name, p, q, beta, ct, cD, arg, interior, lim = worst2[1]
    print(f"      sharpest case: {name}, beta = ({beta[0]:.4g}, {beta[1]:.4g}), c_D = {cD:.5g}, c_true = {ct:.5g} "
          f"(interior infimum {interior:.5g} at phi - p = ({(arg[0] - p[0]) % TWO_PI:.4f}, {(arg[1] - p[1]) % TWO_PI:.4f}); limit at the states {lim:.5g})")
    # |D| = 3
    fam3 = []
    for _ in range(12):
        fam3.append(("random", rng.uniform(0, TWO_PI, 3), rng.uniform(0, TWO_PI, 3)))
    for gaps in ((1e-2, 1e-2, 1e-2), (1e-2, 1.0, 2.0), (0.3, 0.3, 3.0), (np.pi, np.pi, np.pi), (1e-2, np.pi, np.pi),
                 (3.0, 3.0, 3.0), (1.0, 1.0, 1.0), (2.5, 2.8, 3.1)):
        p = rng.uniform(0, TWO_PI, 3); fam3.append((f"gaps {gaps}", p, p + np.array(gaps)))
    r3 = []; worst3 = (np.inf, None)
    for name, p, q in fam3:
        beta, cD, cs = constants(p, q, np.arange(3))
        ct, interior, lim, arg = ctrue_D(p, q, 161)
        ok &= ct >= cD * (1 - 1e-9)
        r3.append(ct / cD)
        if ct / cD < worst3[0]:
            worst3 = (ct / cD, (name, beta, ct, cD))
    r3 = np.array(r3)
    print(f"   |D| = 3, E empty: {len(r3)} pairs: c_true / c_D between {r3.min():.3f} and {r3.max():.1f}; (a) violated: "
          f"{int((r3 < 1 - 1e-9).sum())}; sharpest: {worst3[1][0]}, beta = {np.round(worst3[1][1], 4)}, "
          f"c_true = {worst3[1][2]:.4g}, c_D = {worst3[1][3]:.4g}")
    # shared angles: f = sum_E a + F, d^2 = sum_E a + (A or B); inf of the ratio = min(1, c_true^D) exactly
    #   (>=: (x + F)/(x + m) >= min(1, F/m); <=: move only the shared angles, or only the differing ones)
    print("   shared angles (E non-empty): inf f/min(d^2) = min(1, c_true^D) exactly, so c_true/c* = min(1, c_true^D)/min(1, c_D);")
    print("      this equals 1/c_D whenever c_true^D >= 1, e.g. |D| = 3 with all beta_k = 3.2: c_D = 0.8, ratio 1.25 -- the")
    print("      division's 'worst case found' is of this kind (the trivially tight direction of the shared angles):")
    for gaps in ((2.214, 2.3, 2.5), (3.0, 3.1, 3.14)):
        p = rng.uniform(0, TWO_PI, 3); q = p + np.array(gaps)
        beta, cD, cs = constants(p, q, np.arange(3)); ct, interior, lim, arg = ctrue_D(p, q, 161)
        print(f"      |D| = 3 gaps {gaps}: beta_min = {beta.min():.3f}, c_D = {cD:.3f}, c_true^D = {ct:.3f}; with one shared "
              f"angle: c* = {min(1, cD):.3f}, best constant {min(1, ct):.3f}, ratio {min(1, ct) / min(1, cD):.3f}")
    # direct check with shared angles on random points (r = 3..5), including tiny beta
    viol = 0; cases = 0; smallest = np.inf
    for _ in range(300):
        r = int(rng.integers(3, 6)); nE = int(rng.integers(1, r - 1)); D = np.sort(rng.choice(r, size=r - nE, replace=False))
        Emask = np.ones(r, bool); Emask[D] = False
        p = rng.uniform(0, TWO_PI, r); q = p.copy()
        q[D] = p[D] + (rng.uniform(0, TWO_PI, len(D)) if rng.random() < 0.6 else 10 ** rng.uniform(-3, 0, len(D)))
        beta, cD, cs = constants(p, q, D)
        X = rng.uniform(0, TWO_PI, size=(40000, r))
        # half of the points near the states and near chimeras of the two states
        mix = np.where(rng.random((20000, r)) < 0.5, p, q) + rng.normal(scale=10 ** rng.uniform(-3, -0.5, (20000, 1)), size=(20000, r))
        X = np.vstack([X, mix])
        a = 2 - 2 * np.cos(X - p); b = 2 - 2 * np.cos(X - q)
        F = a[:, D].sum(1) * b[:, D].sum(1) - (a[:, D] * b[:, D]).sum(1)
        f = a[:, Emask].sum(1) + F
        m = np.minimum(a.sum(1), b.sum(1))
        keep = m > 1e-12
        ratio = (f[keep] / m[keep]).min() / cs
        smallest = min(smallest, ratio); viol += ratio < 1 - 1e-9; cases += 1
    print(f"      random check with shared angles, r = 3..5, {cases} pairs, 60000 points each (half near the states and "
          f"their chimeras, beta down to 1e-6): smallest f/(c* min d^2) = {smallest:.3f}; violations: {viol}")
    ok &= viol == 0
    return ok


def refined_grid(r, base, centres):
    ax = TWO_PI * np.arange(base) / base
    pts = [np.array(x) for x in itertools.product(ax, repeat=r)]
    for c in centres:
        pts.append(np.array(c))
        for rad in np.geomspace(1e-3, 0.7, 14):
            for _ in range(10 if r == 2 else 14):
                u = rng.normal(size=r); u /= np.linalg.norm(u)
                pts.append(c + rad * u)
            for k in range(r):                               # along the axes
                for s in (1, -1):
                    e = np.zeros(r); e[k] = s; pts.append(c + rad * e)
    return np.mod(np.array(pts), TWO_PI)


def certificate_coefficients(p, q, D, Emask, r):
    """Feature list and coefficients of f = sum_E a_k + sum_{k != l in D} a_k b_l  (constant dropped)."""
    names = []; funcs = []
    for k in range(r):
        names += [("c", k), ("s", k)]
    for k, l in itertools.combinations(D.tolist(), 2):
        names += [("cc", k, l), ("cs", k, l), ("sc", k, l), ("ss", k, l)]
    idx = {nm: i for i, nm in enumerate(names)}
    lam = np.zeros(len(names)); const = 0.0
    for k in np.nonzero(Emask)[0]:
        const += 2; lam[idx[("c", k)]] += -2 * np.cos(p[k]); lam[idx[("s", k)]] += -2 * np.sin(p[k])
    for k in D:
        for l in D:
            if k == l:
                continue
            # a_k b_l = (2 - 2 cos p_k c_k - 2 sin p_k s_k)(2 - 2 cos q_l c_l - 2 sin q_l s_l)
            const += 4
            lam[idx[("c", k)]] += -4 * np.cos(p[k]); lam[idx[("s", k)]] += -4 * np.sin(p[k])
            lam[idx[("c", l)]] += -4 * np.cos(q[l]); lam[idx[("s", l)]] += -4 * np.sin(q[l])
            for (u, fu) in (("c", np.cos(p[k])), ("s", np.sin(p[k]))):
                for (v, fv) in (("c", np.cos(q[l])), ("s", np.sin(q[l]))):
                    if k < l:
                        lam[idx[(u + v, k, l)]] += 4 * fu * fv
                    else:
                        lam[idx[(v + u, l, k)]] += 4 * fu * fv
    return names, lam, const


def feature_matrix(names, X):
    cols = []
    for nm in names:
        if len(nm) == 2:
            cols.append(np.cos(X[:, nm[1]]) if nm[0] == "c" else np.sin(X[:, nm[1]]))
        else:
            f1 = np.cos if nm[0][0] == "c" else np.sin; f2 = np.cos if nm[0][1] == "c" else np.sin
            cols.append(f1(X[:, nm[1]]) * f2(X[:, nm[2]]))
    return np.array(cols)                                     # m x N


def test_S_W():
    print("S, W. stability (b) and weights (c) by linear programmes on refined grids")
    ok = True
    cases = [(2, [0, 1], 36), (2, [0, 1], 36), (2, [0, 1], 36), (3, [0, 1], 14), (3, [0, 1, 2], 14)]
    for ci, (r, Dl, base) in enumerate(cases):
        D = np.array(Dl); Emask = np.ones(r, bool); Emask[D] = False
        p = rng.uniform(0, TWO_PI, r); q = p.copy()
        gaps = rng.uniform(0.8, np.pi, len(D)) if ci != 1 else np.array([0.35, 2.6])
        q[D] = p[D] + gaps
        beta, cD, cs = constants(p, q, D)
        X = refined_grid(r, base, [p, q])
        names, lam, const = certificate_coefficients(p, q, D, Emask, r)
        Fm = feature_matrix(names, X)
        a = 2 - 2 * np.cos(X - p); b = 2 - 2 * np.cos(X - q)
        Fv = a[:, D].sum(1) * b[:, D].sum(1) - (a[:, D] * b[:, D]).sum(1)
        f = a[:, Emask].sum(1) + Fv
        ok &= np.allclose(f, const + Fm.T @ lam, atol=1e-9)                     # the expansion of f
        Lam = np.abs(lam).sum(); Lam_bound = 2 * np.sqrt(2) * Emask.sum() + (8 + 8 * np.sqrt(2)) * len(D) * (len(D) - 1)
        ok &= Lam <= Lam_bound + 1e-9
        dp2 = a.sum(1); dq2 = b.sum(1); target = np.minimum(dp2, dq2)
        Nq = (dq2 < dp2).astype(float)
        ip = int(np.argmin(dp2)); iq = int(np.argmin(dq2))
        wq = 0.35; mu = np.zeros(len(X)); mu[ip] = 1 - wq; mu[iq] = wq
        y = Fm @ mu
        line = (f"   case {ci + 1}: r = {r}, |D| = {len(D)}, |E| = {Emask.sum()}, beta = {np.round(beta, 3)}, c* = {cs:.4f}, "
                f"Lambda = {Lam:.2f} (stated bound {Lam_bound:.2f}), {len(X)} grid points")
        print(line)
        for tau in (1e-4, 1e-3, 1e-2):
            A_ub = np.vstack([Fm, -Fm]); b_ub = np.concatenate([y + tau, -(y - tau)])
            kw = dict(A_ub=A_ub, b_ub=b_ub, A_eq=np.ones((1, len(X))), b_eq=[1.0], bounds=[(0, None)] * len(X), method="highs")
            res = linprog(-target, **kw); val = -res.fun
            eps = Lam * tau / cs
            up = -linprog(-Nq, **kw).fun; lo = linprog(Nq, **kw).fun
            dev = max(up - wq, wq - lo)
            wbound = (4 * np.sqrt(eps) + eps + 2 * np.sqrt(2) * tau) / beta.max()
            # reviewer's linear bound: h = 1 - (1 - a_k/beta_k)(1 - a_l/beta_l) for the two largest beta in D:
            #   h(p) = 0, h(q) = 1, both critical;  |h - 1_{N_q}| <= 12 min(d_p^2, d_q^2) / (beta_k beta_l);
            #   l1 norm of the non-constant coefficients of h <= 2 sqrt2 (1/beta_k + 1/beta_l) + (8 + 8 sqrt2)/(beta_k beta_l)
            bs = np.sort(beta)[::-1][:2]
            lin = 12 * eps / (bs[0] * bs[1]) + (2 * np.sqrt(2) * (1 / bs[0] + 1 / bs[1]) + (8 + 8 * np.sqrt(2)) / (bs[0] * bs[1])) * tau
            ok &= res.status == 0 and val <= eps * (1 + 1e-7) and dev <= wbound * (1 + 1e-7) and dev <= lin * (1 + 1e-7)
            print(f"      tau = {tau:g}: sup int min(d^2) dnu = {val:.3e}, bound Lambda tau / c* = {eps:.3e} (ratio {val / eps:.3f}); "
                  f"sup |nu(N_q) - w_q| = {dev:.3e}, bound (c) = {wbound:.3e} (ratio {dev / wbound:.3f}"
                  f"{'; bound vacuous' if wbound >= 1 else ''}); reviewer's linear bound {lin:.3e}")
    return ok


def test_I():
    print("I. E20' on a 12 x 12 x 12 grid of the 3-torus")
    g = 12; ax = TWO_PI * np.arange(g) / g
    X = np.array(list(itertools.product(ax, repeat=3)))
    one = lambda t: np.ones_like(t)
    fs = (one, np.cos, np.sin)
    cols2 = []; cols3 = []
    for f1, f2, f3 in itertools.product(range(3), repeat=3):
        col = fs[f1](X[:, 0]) * fs[f2](X[:, 1]) * fs[f3](X[:, 2])
        cols3.append(col)
        if (f1 > 0) + (f2 > 0) + (f3 > 0) <= 2:
            cols2.append(col)
    F2 = np.array(cols2).T; F3 = np.array(cols3).T          # N x 19, N x 27 (constant included)

    def identified(F, idx, w):
        N = F.shape[0]; mu = np.zeros(N); mu[idx] = w
        c = -np.ones(N); c[idx] = 0
        res = linprog(c, A_eq=F.T, b_eq=F.T @ mu, bounds=[(0, None)] * N, method="highs")
        return res.status == 0 and -res.fun < 1e-8 and np.linalg.matrix_rank(F[idx]) == len(idx)
    stats = {1: [0, 0], 2: [0, 0], 3: [0, 0]}; ok = True; adjacent = [0, 0]
    while min(v[0] for v in stats.values()) < 12 or adjacent[0] < 4:
        i, j = rng.choice(len(X), size=2, replace=False)
        diff = np.abs(X[i] - X[j]) > 1e-9
        differ = int(np.sum(diff))
        if differ == 1:
            # on a GRID the competitors live on the 12 grid points of one circle: if the two angle values are
            # neighbours on the grid, the chord is an edge of the 12-gon and the pair is identified *on the grid*
            # (a discretisation artefact; on the circle it is not).  Counted separately.
            k = int(np.nonzero(diff)[0][0]); step = int(round(abs(X[i][k] - X[j][k]) / (TWO_PI / g)))
            res = identified(F3, np.array([i, j]), np.array([0.3, 0.7]))       # all 27 multilinear functions
            if step in (1, g - 1):
                adjacent[0] += 1; adjacent[1] += res; ok &= res
            elif stats[1][0] < 12:
                stats[1][0] += 1; stats[1][1] += res; ok &= not res
            continue
        if stats[differ][0] >= 12:
            continue
        stats[differ][0] += 1
        res = identified(F2, np.array([i, j]), np.array([0.3, 0.7]))           # products over at most two angles
        stats[differ][1] += res; ok &= res
    print(f"   pairs differing in 3 angles: identified by the 18 observables of order <= 2 in {stats[3][1]}/{stats[3][0]}; "
          f"in 2 angles: {stats[2][1]}/{stats[2][0]}; in 1 angle (values not neighbours on the grid), all 26 multilinear "
          f"observables: identified in {stats[1][1]}/{stats[1][0]} (must be 0)")
    print(f"   (grid artefact: pairs differing in one angle by ONE grid step are identified among measures on the grid "
          f"in {adjacent[1]}/{adjacent[0]} cases -- the chord is an edge of the polygon of grid points; a grid check of "
          f"non-identification must use non-neighbouring values)")
    return ok


if __name__ == "__main__":
    part = sys.argv[1] if len(sys.argv) > 1 else "all"
    res = True
    if part in ("G", "all"):
        res &= test_G()
    if part in ("S", "all"):
        res &= test_S_W()
    if part in ("I", "all"):
        res &= test_I()
    print("PASS" if res else "FAIL")
