#!/usr/bin/env python3
"""Counterexamples to two 'exactly when' sentences of the report (Section 3.2 after E6, Section 3.3 after E8):
    'identification of finite ensembles = absence of chimeras'
    'the ensemble is identified exactly when [the set of realisable splices] contains nothing but the conformers'.
(1) a three-point toy; (2) the graph K4 + a vertex of degree two in the plane, two conformers, on an OPEN set of
pairs: three chimeras are realisable, yet every nu with the same edge-length laws has F_# nu = F_# mu.
Also: (3) 'exposed' without affine independence is not identified; (4) E1.3(b); (5) E8 Vandermonde step."""
import itertools
import numpy as np
from scipy.optimize import linprog, least_squares

rng = np.random.default_rng(777)


def marginal_lp(real, w, m):
    """real: list of realisable colourings a in {0,1}^m (constant ones included).  Max mass on non-constant
    colourings subject to: for every feature e and conformer i, sum_{a: a(e)=i} v_a = w_i."""
    A = []; b = []
    for e in range(m):
        for i in (0, 1):
            A.append([1.0 if a[e] == i else 0.0 for a in real]); b.append(w[i])
    c = [-(0.0 if len(set(a)) == 1 else 1.0) for a in real]
    res = linprog(c, A_eq=np.array(A), b_eq=np.array(b), bounds=[(0, None)] * len(real), method="highs")
    return -res.fun


def toy():
    # X = {x1, x2, y}, F(x1) = (0,0), F(x2) = (1,1), F(y) = (0,1): y is a chimera (colouring (1,2))
    real = [(0, 0), (1, 1), (0, 1)]
    out = []
    for w in ((0.5, 0.5), (0.3, 0.7)):
        out.append(marginal_lp(real, w, 2))
    return out


E = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (4, 0), (4, 1)]


def sq(p):
    return np.array([np.sum((p[i] - p[j]) ** 2) for i, j in E])


def cm4(q6):
    D = np.zeros((4, 4)); k = 0
    for i in range(4):
        for j in range(i + 1, 4):
            D[i, j] = D[j, i] = q6[k]; k += 1
    M = np.ones((5, 5)); M[0, 0] = 0; M[1:, 1:] = D
    return np.linalg.det(M)


def conformer(b, l7, l8, jitter):
    """K4 on vertices 0..3 with |x0 - x1| = b, vertex 4 at distances l7, l8 from x0, x1."""
    x0 = np.array([0.0, 0.0]); x1 = np.array([b, 0.0])
    x2 = np.array([0.3 * b, 1.1]) + jitter[0]; x3 = np.array([0.8 * b, -0.9]) + jitter[1]
    a = (b * b + l7 * l7 - l8 * l8) / (2 * b); h = np.sqrt(l7 * l7 - a * a)
    return np.array([x0, x1, x2, x3, np.array([a, h])])


def realise(q, seeds, starts=40):
    best = np.inf
    for s in range(starts):
        x0 = seeds[s % len(seeds)].ravel() + (0 if s < len(seeds) else 1.0) * rng.normal(size=10)
        res = least_squares(lambda x: sq(x.reshape(5, 2)) - q, x0, xtol=1e-14, ftol=1e-14, gtol=1e-14)
        best = min(best, np.linalg.norm(res.fun))
        if best < 1e-10:
            break
    return best


def k4_pendant(trials=20):
    out = []
    ident_all = True; n_chim = []
    for t in range(trials):
        jit = 0.05 * rng.normal(size=(4, 2))
        pert = 0.02 * rng.normal(size=6)
        x1 = conformer(2.0 + pert[0], 1.5 + pert[1], 1.5 + pert[2], jit[:2])
        x2 = conformer(5.0 + pert[3], 3.0 + pert[4], 2.5 + pert[5], jit[2:])
        L = np.array([sq(x1), sq(x2)])
        real = []
        for a in itertools.product((0, 1), repeat=8):
            q = L[list(a), range(8)]
            if len(set(a[:6])) > 1:
                # K4 block not monochromatic: realisable only if the Cayley-Menger determinant vanishes
                assert abs(cm4(q[:6])) > 1e-6
                continue
            bb = np.sqrt(q[0]); r0 = np.sqrt(q[6]); r1 = np.sqrt(q[7])
            if abs(r0 - r1) < bb < r0 + r1:
                real.append(a)
        chim = [a for a in real if len(set(a)) > 1]
        n_chim.append(len(chim))
        if t == 0:
            for a in chim:
                out.append(f"   chimera {a}: least-squares residual {realise(L[list(a), range(8)], (x1, x2)):.1e}")
            a = (1, 1, 1, 1, 1, 1, 0, 0)
            out.append(f"   non-realisable splice {a}: least-squares residual {realise(L[list(a), range(8)], (x1, x2)):.1e}")
        for w in ((0.5, 0.5), (0.2, 0.8), (0.9, 0.1)):
            if marginal_lp(real, w, 8) > 1e-9:
                ident_all = False
    out.insert(0, f"K4 + degree-2 vertex, {trials} pairs in an open set: realisable chimeras per pair: {sorted(set(n_chim))}; "
                  f"max mass any same-law ensemble can put on chimeras (3 weightings each) is 0 in all cases: {ident_all}")
    # control: a pair for which the two complementary chimeras are both realisable -> not identified
    x1 = conformer(2.0, 1.5, 1.5, np.zeros((2, 2))); x2 = conformer(2.1, 1.6, 1.4, 0.05 * np.ones((2, 2)))
    L = np.array([sq(x1), sq(x2)]); real = []
    for a in itertools.product((0, 1), repeat=8):
        if len(set(a[:6])) > 1:
            continue
        q = L[list(a), range(8)]; bb = np.sqrt(q[0]); r0 = np.sqrt(q[6]); r1 = np.sqrt(q[7])
        if abs(r0 - r1) < bb < r0 + r1:
            real.append(a)
    out.append(f"control (nearby conformers): {len(real) - 2} realisable chimeras; max chimera mass with the same laws, "
               f"w = (0.5,0.5): {marginal_lp(real, (0.5, 0.5), 8):.3f}")
    return out


def exposed_not_identified():
    # X = {a,b,c}, Phi = (0,0,1): f = Phi >= 0 exposes {a,b}; the uniform ensemble on {a,b} is not identified
    Phi = np.array([[0.0, 0.0, 1.0]])
    A = np.vstack([np.ones((1, 3)), Phi]); mu = np.array([0.5, 0.5, 0.0])
    res = linprog([-1, 0, 0], A_eq=A, b_eq=A @ mu, bounds=[(0, None)] * 3, method="highs")
    return f"exposed support without independence: another ensemble with the same data: nu = {np.round(res.x, 3).tolist()}"


def e13b():
    # E1.3(b): nu = law of R p, R^2 in {0,2}: same mean squared lengths, different law of Q
    p = rng.normal(size=(200000, 4, 2))
    R = np.sqrt(2.0 * rng.integers(0, 2, size=200000))[:, None, None]
    q = R * p
    d2 = lambda z: np.sum((z[:, 0] - z[:, 1]) ** 2, axis=1)
    return (f"E1.3(b) (Monte Carlo, Gaussian mu): E|p0-p1|^2 = {d2(p).mean():.3f} vs {d2(q).mean():.3f} under nu; "
            f"P(Q = 0) = {np.mean(d2(p) == 0):.3f} vs {np.mean(d2(q) == 0):.3f}")


def e8_moments():
    # a measure carried by K known atoms with the same moments 0..K-1 has the same weights (Vandermonde);
    # and the polynomial g(t) = prod (t - t_i)^2 has degree 2K: moments 1..2K are needed to integrate it.
    K = 4; t = np.sort(rng.random(K) * 3 + 0.5); w = rng.dirichlet(np.ones(K))
    V = np.vander(t, K, increasing=True).T
    w2 = np.linalg.solve(V, V @ w)
    g = np.poly(np.concatenate([t, t]))
    return f"E8: Vandermonde recovery error {np.max(np.abs(w2 - w)):.1e}; degree of prod (t - t_i)^2 = {len(g) - 1} = 2K"


if __name__ == "__main__":
    print("toy (3 points, 2 features, one chimera): max chimera mass with the same laws, w=(.5,.5) and (.3,.7):", toy())
    for line in k4_pendant():
        print(line)
    print(exposed_not_identified())
    print(e13b())
    print(e8_moments())
