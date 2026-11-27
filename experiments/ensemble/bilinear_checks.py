#!/usr/bin/env python3
"""Checks for Proposition E32 (bilinear data: unknown linear parameters of the forward model).

Data  y = B(nu) a,  B(nu) = sum_x nu_x Psi(x),  Psi(x) an m x p matrix, a in a box A of R^p unknown.

 U1  a planted instance: the local certificate in exact rational arithmetic, the explicit radius,
     and a subdivision of the box with an exact exclusion vector on every cell outside the
     neighbourhood: (mu, a_0) is the only compatible pair.  Cross-check on a grid of parameters.
 U2  a twin: two compatible pairs with different ensembles and different parameters, exactly;
     the subdivision leaves cells around both parameters.
 U3  outer bounds: the range of a target over the cells that are not excluded contains the range
     over a fine grid of parameters, and shrinks to it as the cells are refined.
 U4  the Gaussian count: the local criterion holds with the probability of Wendel's formula for
     n - K points in dimension m - p - K + 1.

Exact parts use fractions and sympy; linear programmes are solved in floating point (HiGHS) and
every exclusion vector is rounded to rationals and verified exactly before it is accepted.
"""
import sys
from fractions import Fraction as Fr
from math import comb

import numpy as np
import sympy as sp
from scipy.optimize import linprog


def rat(v, den=10**6):
    f = Fr(float(v)).limit_denominator(den)
    return sp.Rational(f.numerator, f.denominator)


def Bmat(Psi, nu):
    n, m, p = Psi.shape
    return [[sum(nu[x] * int(Psi[x, i, k]) for x in range(n)) for k in range(p)] for i in range(m)]


def matvec(M, v):
    return [sum(M[i][k] * v[k] for k in range(len(v))) for i in range(len(M))]


def local_certificate(Psi, mu, a0):
    """Exact.  Returns None, or U (U B(mu) = 0), c0, gamma, ell, g, Gn, foff and the radius rho0."""
    n, m, p = Psi.shape
    S = [x for x in range(n) if mu[x] != 0]
    K = len(S)
    B = sp.Matrix(Bmat(Psi, mu))
    if B.rank() < p:
        return None
    null = B.T.nullspace()
    if not null:
        return None
    U = sp.Matrix.hstack(*null).T
    d = U.rows
    G = [U * sp.Matrix(Psi[x].tolist()) for x in range(n)]
    a0s = sp.Matrix([sp.Rational(a.numerator, a.denominator) for a in a0])
    F = [G[x] * a0s for x in range(n)]
    M0 = sp.Matrix([[1] + list(F[x]) for x in S])
    if M0.rank() < K:
        return None
    Z = sp.Matrix([list(F[x]) for x in S]).nullspace()
    if not Z:
        return None
    Zm = sp.Matrix.hstack(*Z)
    off = [x for x in range(n) if x not in S]
    Hf = np.array([[float(v) for v in (F[x].T * Zm)] for x in off])
    z = Zm.cols
    res = linprog(c=[0] * z + [-1], A_ub=np.hstack([-Hf, np.ones((len(off), 1))]),
                  b_ub=np.zeros(len(off)), bounds=[(-1, 1)] * z + [(None, None)], method='highs')
    if res.status != 0 or res.x[-1] < 1e-9:
        return None
    c0 = Zm * sp.Matrix([rat(v) for v in res.x[:z]])
    q = [(F[x].T * c0)[0] for x in range(n)]
    if not all(q[x] == 0 for x in S) or not all(q[x] > 0 for x in off):
        return None
    gamma = min(q[x] for x in off)
    L = (M0 * M0.T).inv() * M0
    assert L * M0.T == sp.eye(K)
    ell = sum(abs(v) for v in L)
    g = max(sum(abs(v) for v in (G[x].T * c0)) for x in range(n))
    Gn = max(max(sum(abs(G[x][i, k]) for k in range(p)) for i in range(d)) for x in range(n))
    foff = max(max(abs(v) for v in F[x]) for x in off)
    rho0 = 1 / ((1 + ell * max(1, foff)) * g / gamma + ell * Gn)
    return dict(U=U, c0=c0, gamma=gamma, ell=ell, g=g, Gn=Gn, foff=foff, rho0=rho0)


def slice_range(Psi, a, y, target=None):
    """For a fixed parameter: is the slice non-empty, and the range of a linear target over it."""
    n, m, p = Psi.shape
    A_eq = np.vstack([np.ones((1, n)), np.array([Psi[x] @ a for x in range(n)]).T])
    b_eq = np.concatenate([[1.0], y])
    if target is None:
        res = linprog(np.zeros(n), A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * n, method='highs')
        return res.status == 0
    lo = linprog(target, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * n, method='highs')
    if lo.status != 0:
        return None
    hi = linprog(-np.asarray(target), A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * n, method='highs')
    return lo.fun, -hi.fun


def exclusion(Psi, y, lo, hi):
    """Floating point: maximise t with  lam.y - max_x sigma_cell(Psi(x)^T lam) >= t,  |lam|_inf <= 1."""
    n, m, p = Psi.shape
    nv = m + n * p + 1
    c = np.zeros(nv)
    c[-1] = -1
    A = []
    for x in range(n):
        row = np.zeros(nv)
        row[:m] = -y
        row[m + x * p: m + (x + 1) * p] = 1
        row[-1] = 1
        A.append(row)
        for k in range(p):
            for bd in (lo[k], hi[k]):
                row = np.zeros(nv)
                row[:m] = bd * Psi[x, :, k]
                row[m + x * p + k] = -1
                A.append(row)
    res = linprog(c, A_ub=np.array(A), b_ub=np.zeros(len(A)),
                  bounds=[(-1, 1)] * m + [(None, None)] * (n * p + 1), method='highs')
    if res.status != 0:
        return -1.0, None
    return res.x[-1], res.x[:m]


def exact_margin(Psi, yq, lo, hi, lam):
    """lam.y - max_x sigma_cell(Psi(x)^T lam), in rationals."""
    n, m, p = Psi.shape
    worst = None
    for x in range(n):
        s = Fr(0)
        for k in range(p):
            ck = sum(lam[i] * int(Psi[x, i, k]) for i in range(m))
            s += max(lo[k] * ck, hi[k] * ck)
        worst = s if worst is None else max(worst, s)
    return sum(lam[i] * yq[i] for i in range(m)) - worst


def subdivide(Psi, yq, lo, hi, maxdepth, centre=None, rho0=None, depth=0, out=None):
    """Leaves: ('local' | 'excluded' | 'open', lo, hi, exclusion vector or None)."""
    if out is None:
        out = []
    p = len(lo)
    if centre is not None and max(max(abs(lo[k] - centre[k]), abs(hi[k] - centre[k]))
                                  for k in range(p)) < rho0:
        out.append(('local', lo, hi, None))
        return out
    y = np.array([float(v) for v in yq])
    t, lam = exclusion(Psi, y, [float(v) for v in lo], [float(v) for v in hi])
    if t > 1e-9:
        lamq = [Fr(float(v)).limit_denominator(10**6) for v in lam]
        if exact_margin(Psi, yq, lo, hi, lamq) > 0:
            out.append(('excluded', lo, hi, lamq))
            return out
    if depth >= maxdepth:
        out.append(('open', lo, hi, None))
        return out
    k = max(range(p), key=lambda j: hi[j] - lo[j])
    mid = (lo[k] + hi[k]) / 2
    hi1 = list(hi)
    hi1[k] = mid
    lo2 = list(lo)
    lo2[k] = mid
    subdivide(Psi, yq, lo, hi1, maxdepth, centre, rho0, depth + 1, out)
    subdivide(Psi, yq, lo2, hi, maxdepth, centre, rho0, depth + 1, out)
    return out


def check_leaves(Psi, yq, lo, hi, leaves, centre, rho0):
    """Independent check of a certificate of uniqueness: the leaves tile the box (volumes add up,
    interiors disjoint), each is inside the open neighbourhood or carries a valid exclusion vector."""
    p = len(lo)
    vol = Fr(1)
    for k in range(p):
        vol *= hi[k] - lo[k]
    total = Fr(0)
    for kind, l, h, lam in leaves:
        v = Fr(1)
        for k in range(p):
            if not (lo[k] <= l[k] < h[k] <= hi[k]):
                return False
            v *= h[k] - l[k]
        total += v
        if kind == 'local':
            if not max(max(abs(l[k] - centre[k]), abs(h[k] - centre[k])) for k in range(p)) < rho0:
                return False
        elif kind == 'excluded':
            if not exact_margin(Psi, yq, l, h, lam) > 0:
                return False
        else:
            return False
    if total != vol:
        return False
    for i in range(len(leaves)):
        for j in range(i):
            if all(max(leaves[i][1][k], leaves[j][1][k]) < min(leaves[i][2][k], leaves[j][2][k])
                   for k in range(p)):
                return False
    return True


def planted(seed, n=12, m=8, p=2, K=2):
    rng = np.random.default_rng(seed)
    Psi = rng.integers(-3, 4, size=(n, m, p))
    mu = [Fr(0)] * n
    for i in range(K):
        mu[i] = Fr(i + 1, K * (K + 1) // 2)
    a0 = ([Fr(1), Fr(1, 2)] + [Fr(1, 3)] * p)[:p]
    return Psi, mu, a0


BOX = ([Fr(1, 2), Fr(0)], [Fr(3, 2), Fr(1)])


def u1():
    print('U1  planted instances (n = 12, m = 8, p = 2, two conformers, box [1/2,3/2] x [0,1])')
    done = 0
    for seed in range(1, 8):
        Psi, mu, a0 = planted(seed)
        cert = local_certificate(Psi, mu, a0)
        if cert is None:
            print('    seed %d: the local criterion fails' % seed)
            continue
        yq = matvec(Bmat(Psi, mu), a0)
        leaves = subdivide(Psi, yq, BOX[0], BOX[1], 40, a0, cert['rho0'])
        kinds = [l[0] for l in leaves]
        ok = check_leaves(Psi, yq, BOX[0], BOX[1], leaves, a0, cert['rho0'])
        # cross-check: slices on a grid of parameters
        y = np.array([float(v) for v in yq])
        feas = 0
        for i in range(41):
            for j in range(41):
                a = np.array([0.5 + i / 40, j / 40])
                if abs(a[0] - 1) + abs(a[1] - 0.5) > 1e-12 and slice_range(Psi, a, y):
                    feas += 1
        print('    seed %d: radius %.3e; cells %d (in the neighbourhood %d, excluded %d, open %d); '
              'certificate verified exactly: %s; grid parameters other than a_0 with a non-empty '
              'slice: %d of 1680' % (seed, float(cert['rho0']), len(leaves), kinds.count('local'),
                                     kinds.count('excluded'), kinds.count('open'), ok, feas))
        done += ok and feas == 0
    return done


def twin(seed=1):
    """Second compatible pair (nu2, a2): change Psi at one configuration outside the support."""
    Psi, mu, a0 = planted(seed)
    n, m, p = Psi.shape
    yq = matvec(Bmat(Psi, mu), a0)
    nu2 = [Fr(0)] * n
    nu2[5], nu2[6], nu2[7] = Fr(1, 4), Fr(1, 4), Fr(1, 2)
    a2 = [Fr(5, 4), Fr(1, 4)]
    # Psi(7) a2 * nu2(7) = y - sum_{x != 7} nu2(x) Psi(x) a2 ; choose Psi(7) = r a2^T / (nu2(7)|a2|^2)
    r = [yq[i] - sum(nu2[x] * sum(int(Psi[x, i, k]) * a2[k] for k in range(p)) for x in (5, 6))
         for i in range(m)]
    nrm = sum(v * v for v in a2)
    Psi7 = [[r[i] * a2[k] / (nu2[7] * nrm) for k in range(p)] for i in range(m)]
    return Psi, Psi7, mu, a0, nu2, a2, yq


def u2():
    print('U2  a twin')
    Psi, Psi7, mu, a0, nu2, a2, yq = twin()
    n, m, p = Psi.shape
    # exact verification with the rational Psi(7); then scale all data to integers for the LPs
    def B_exact(nu):
        out = []
        for i in range(m):
            row = []
            for k in range(p):
                s = Fr(0)
                for x in range(n):
                    s += nu[x] * (Psi7[i][k] if x == 7 else int(Psi[x, i, k]))
                row.append(s)
            out.append(row)
        return out
    y1 = matvec(B_exact(mu), a0)
    y2 = matvec(B_exact(nu2), a2)
    same = y1 == y2 == yq
    tv = sum(abs(mu[x] - nu2[x]) for x in range(n)) / 2
    print('    data of (mu, a_0) and of (nu_2, a_2) equal exactly: %s; total variation between the '
          'ensembles %s; a_0 = (1, 1/2), a_2 = (5/4, 1/4)' % (same, tv))
    Pf = Psi.astype(float).copy()
    Pf[7] = np.array([[float(v) for v in row] for row in Psi7])
    y = np.array([float(v) for v in yq])

    class P:  # exact margins need rational Psi: use a wrapper with Fractions
        pass
    leaves = subdivide_float(Pf, y, BOX[0], BOX[1], 9)
    open_cells = [l for l in leaves if l[0] == 'open']
    near0 = any(all(l[1][k] <= a0[k] <= l[2][k] for k in range(p)) for l in open_cells)
    near2 = any(all(l[1][k] <= a2[k] <= l[2][k] for k in range(p)) for l in open_cells)
    lo_hull = [min(float(l[1][k]) for l in open_cells) for k in range(p)]
    hi_hull = [max(float(l[2][k]) for l in open_cells) for k in range(p)]
    print('    subdivision to depth 9: %d cells excluded, %d not; cells not excluded contain a_0: %s, '
          'a_2: %s; hull of the cells not excluded: [%.3f, %.3f] x [%.3f, %.3f]'
          % (sum(l[0] == 'excluded' for l in leaves), len(open_cells), near0, near2,
             lo_hull[0], hi_hull[0], lo_hull[1], hi_hull[1]))
    return same and near0 and near2, (Pf, y, leaves)


def subdivide_float(Pf, y, lo, hi, maxdepth, depth=0, out=None, margin=1e-7):
    """As subdivide, for data that are not integers: exclusion accepted on a floating-point margin."""
    if out is None:
        out = []
    p = len(lo)
    t, lam = exclusion(Pf, y, [float(v) for v in lo], [float(v) for v in hi])
    if t > margin:
        out.append(('excluded', lo, hi, lam))
        return out
    if depth >= maxdepth:
        out.append(('open', lo, hi, None))
        return out
    k = max(range(p), key=lambda j: hi[j] - lo[j])
    mid = (lo[k] + hi[k]) / 2
    hi1 = list(hi)
    hi1[k] = mid
    lo2 = list(lo)
    lo2[k] = mid
    subdivide_float(Pf, y, lo, hi1, maxdepth, depth + 1, out, margin)
    subdivide_float(Pf, y, lo2, hi, maxdepth, depth + 1, out, margin)
    return out


def relaxed_range(Pf, y, lo, hi, target):
    """Range of a linear target over the relaxation of one cell (variables nu, W)."""
    n, m, p = Pf.shape
    nv = n + n * p
    A_eq = np.zeros((1 + m, nv))
    A_eq[0, :n] = 1
    for x in range(n):
        A_eq[1:, n + x * p: n + (x + 1) * p] = Pf[x]
    b_eq = np.concatenate([[1.0], y])
    A = []
    for x in range(n):
        for k in range(p):
            row = np.zeros(nv)
            row[x] = float(lo[k])
            row[n + x * p + k] = -1
            A.append(row)
            row = np.zeros(nv)
            row[x] = -float(hi[k])
            row[n + x * p + k] = 1
            A.append(row)
    c = np.zeros(nv)
    c[:n] = target
    bounds = [(0, None)] * n + [(None, None)] * (n * p)
    r1 = linprog(c, A_ub=np.array(A), b_ub=np.zeros(len(A)), A_eq=A_eq, b_eq=b_eq, bounds=bounds,
                 method='highs')
    if r1.status != 0:
        return None
    r2 = linprog(-c, A_ub=np.array(A), b_ub=np.zeros(len(A)), A_eq=A_eq, b_eq=b_eq, bounds=bounds,
                 method='highs')
    return r1.fun, -r2.fun


def u3(Pf, y):
    print('U3  outer bounds for the weight of configuration 0 on the twin instance')
    n, m, p = Pf.shape
    target = np.zeros(n)
    target[0] = 1
    inner = [1.0, 0.0]
    N = 240
    for i in range(N + 1):
        for j in range(N + 1):
            r = slice_range(Pf, np.array([0.5 + i / N, j / N]), y, target)
            if r is not None:
                inner = [min(inner[0], r[0]), max(inner[1], r[1])]
    print('    range over the slices of a %d x %d grid of parameters (an inner estimate): '
          '[%.4f, %.4f]' % (N + 1, N + 1, inner[0], inner[1]))
    ok = True
    widths = []
    for depth in (0, 3, 6, 9):
        leaves = subdivide_float(Pf, y, BOX[0], BOX[1], depth)
        outer = [1.0, 0.0]
        for kind, lo, hi, _ in leaves:
            if kind == 'open':
                r = relaxed_range(Pf, y, lo, hi, target)
                if r is not None:
                    outer = [min(outer[0], r[0]), max(outer[1], r[1])]
        widths.append(outer[1] - outer[0])
        ok = ok and outer[0] <= inner[0] + 1e-9 and outer[1] >= inner[1] - 1e-9
        print('    cells of depth %d: certified outer bound [%.4f, %.4f]' % (depth, outer[0], outer[1]))
    ok = ok and all(widths[i + 1] <= widths[i] + 1e-9 for i in range(len(widths) - 1))
    return ok


def wendel(N, D):
    if D <= 0:
        return 0.0
    return sum(comb(N - 1, k) for k in range(min(D, N))) / 2 ** (N - 1)


def criterion_float(Psi, mu, a0):
    n, m, p = Psi.shape
    S = [x for x in range(n) if mu[x] != 0]
    B = np.tensordot(mu, Psi, axes=1)
    u, s, vt = np.linalg.svd(B)
    if s[p - 1] < 1e-9 or m <= p:
        return False
    U = u[:, p:].T
    F = np.array([U @ Psi[x] @ a0 for x in range(n)])
    d = m - p
    FS = F[S]
    if np.linalg.matrix_rank(np.hstack([np.ones((len(S), 1)), FS])) < len(S):
        return False
    uu, ss, vv = np.linalg.svd(FS)
    Z = vv[np.sum(ss > 1e-9):].T
    if Z.shape[1] == 0:
        return False
    off = [x for x in range(n) if x not in S]
    H = F[off] @ Z
    z = Z.shape[1]
    res = linprog(c=[0] * z + [-1], A_ub=np.hstack([-H, np.ones((len(off), 1))]), b_ub=np.zeros(len(off)),
                  bounds=[(-1, 1)] * z + [(None, None)], method='highs')
    return res.status == 0 and res.x[-1] > 1e-9


def u4(trials=2000):
    print('U4  Gaussian forward models: frequency of the local criterion and Wendel\'s formula')
    rng = np.random.default_rng(7)
    ok = True
    for (n, m, p, K) in ((12, 7, 1, 2), (12, 8, 2, 2), (12, 10, 2, 2), (12, 9, 3, 2), (16, 11, 2, 3),
                         (12, 6, 2, 2)):
        hits = 0
        for _ in range(trials):
            Psi = rng.standard_normal((n, m, p))
            mu = np.zeros(n)
            mu[:K] = rng.dirichlet(np.ones(K))
            a0 = rng.standard_normal(p)
            hits += criterion_float(Psi, mu, a0)
        pw = wendel(n - K, m - p - K + 1)
        sd = (pw * (1 - pw) / trials) ** 0.5
        good = abs(hits / trials - pw) <= 4 * sd + 1e-12
        ok = ok and good
        print('    n = %2d, m = %2d, p = %d, K = %d: frequency %.4f, formula %.4f (%s)'
              % (n, m, p, K, hits / trials, pw, 'within four standard errors' if good else 'DISAGREES'))
    return ok


def main():
    done = u1()
    ok2, (Pf, y, _) = u2()
    ok3 = u3(Pf, y)
    ok4 = u4()
    print('SUMMARY  U1 unique compatible pair certified on %d instances; U2 twin: %s; '
          'U3 outer bounds nested and containing the inner estimate: %s; U4 Gaussian count: %s'
          % (done, ok2, ok3, ok4))
    good = done >= 4 and ok2 and ok3 and ok4
    print('PASS' if good else 'FAIL')
    return 0 if good else 1


if __name__ == '__main__':
    sys.exit(main())
