#!/usr/bin/env python3
"""a1_homog.py -- referee A1: the Remark "homogeneous spaces" added to section 2.3 after the review.

Claim of the remark: Lemma 2.5 and Theorem A' hold verbatim on every finite metric space with a uniform
reference in which the number of points at each distance from a point does not depend on the point
(|X| in place of 2^n, V(r-1) the size of a ball, m_r = E_pi e_r(d(., c))).

Exact enumeration of all L-tuples of centres (independent uniform, repetitions included) on
  the Petersen graph (vertex-transitive, not a Cayley graph), the Johnson scheme J(6,3),
  the ternary Hamming space H(3,3), the cycle C_9,
and, as a negative control, two spaces WITHOUT the property (a path, a star), where the mean of the bias
functional is not zero.  Checked on the homogeneous spaces: the dips and their maxima are admissible;
E_pi e_r(d(., c)) does not depend on c; mean of G_psi = 0; one-centre oscillation <= (sup psi - inf psi) m_r;
R - O_c <= A(w_c) - 1 <= R; E O_c <= C(L,2) m_r V/|X|; P(O_c >= R/2) <= (L-1) V/|X|; the hitting
probability of a point is <= L V/|X|; exact tails <= 2 exp(-2 t^2/(L d^2)), d = (sup psi - inf psi) m_r.
Own code; nothing imported from the repository.
"""
import itertools
import math
import numpy as np


def bfs_dist(adj):
    n = len(adj)
    D = np.full((n, n), -1, dtype=int)
    for s in range(n):
        D[s, s] = 0
        frontier = [s]
        while frontier:
            nxt = []
            for v in frontier:
                for w in adj[v]:
                    if D[s, w] < 0:
                        D[s, w] = D[s, v] + 1
                        nxt.append(w)
            frontier = nxt
    return D


def petersen():
    verts = list(itertools.combinations(range(5), 2))
    adj = [[j for j, b in enumerate(verts) if not set(a) & set(b)] for a in verts]
    return bfs_dist(adj)


def johnson(n, k):
    verts = list(itertools.combinations(range(n), k))
    return np.array([[k - len(set(a) & set(b)) for b in verts] for a in verts])


def hamming(q, n):
    verts = list(itertools.product(range(q), repeat=n))
    return np.array([[sum(x != y for x, y in zip(a, b)) for b in verts] for a in verts])


def cycle(n):
    return np.array([[min((a - b) % n, (b - a) % n) for b in range(n)] for a in range(n)])


def path(n):
    return np.array([[abs(a - b) for b in range(n)] for a in range(n)])


def star(n):
    return np.array([[0 if a == b else (1 if 0 in (a, b) else 2) for b in range(n)] for a in range(n)])


def run(name, D, u, r, L, rng, expect_homog=True):
    N = D.shape[0]
    E = np.where(D < r, np.expm1(u * (r - D)), 0.0)            # E[c, x] = e_r(d(x, c))
    masses = E.mean(axis=1)
    balls = (D < r).sum(axis=1)
    profile = [tuple(np.bincount(D[c], minlength=N)) for c in range(N)]
    homog = len(set(profile)) == 1
    # admissibility of the maximum of dips for one random tuple
    c0 = rng.integers(0, N, size=L)
    w = 1.0 + E[c0].max(axis=0)
    adm = bool(np.all(w[:, None] <= np.exp(u * D) * w[None, :] * (1 + 1e-12)))
    m_r, V = masses.max(), int(balls.max())
    R = L * m_r
    phis = [rng.uniform(-1, 1, size=N), rng.choice([-1.0, 1.0], size=N), (np.arange(N) == 0).astype(float),
            1.0 - 2.0 * (D[0] <= 1)]
    Psi = np.stack([p - p.mean() for p in phis], axis=1)
    osc_psi = Psi.max(axis=0) - Psi.min(axis=0)
    Pm = np.minimum(E[:, None, :], E[None, :, :]).mean(axis=2)
    G = np.empty((N,) * L + (Psi.shape[1],))
    A1 = np.empty((N,) * L)
    O = np.empty((N,) * L)
    hit = 0
    for c in itertools.product(range(N), repeat=L):
        mx = E[list(c)].max(axis=0)
        G[c] = mx @ Psi / N
        A1[c] = mx.mean()
        O[c] = sum(Pm[c[i], c[j]] for i in range(L) for j in range(i + 1, L))
        hit += mx[0] > 0
    ntot = N ** L
    meanG = np.abs(G.reshape(ntot, -1).mean(axis=0)).max()
    osc1 = max(float((G.max(axis=ax) - G.min(axis=ax)).reshape(-1, Psi.shape[1])[:, k].max() / max(osc_psi[k], 1e-300))
               for ax in range(L) for k in range(Psi.shape[1])) / m_r
    lower = float(((R - O) - A1).max())
    upper = float((A1 - R).max())
    EO, EOb = float(O.mean()), math.comb(L, 2) * m_r * V / N
    pO, pOb = float((O >= R / 2 - 1e-13).mean()), (L - 1) * V / N
    worst = 0.0
    for k in range(Psi.shape[1]):
        d = osc_psi[k] * m_r
        if d <= 0:                                  # constant observable: psi = 0, G = 0
            continue
        s = np.sort(np.abs(G[..., k].ravel()))
        p_ge = (ntot - np.arange(ntot)) / ntot
        worst = max(worst, float((p_ge / (2 * np.exp(-2 * s * s / (L * d * d)))).max()))
    ok = (adm and meanG < 1e-12 * max(1, R) and osc1 <= 1 + 1e-9 and lower <= 1e-12 and upper <= 1e-12
          and EO <= EOb + 1e-12 and pO <= pOb + 1e-12 and hit / ntot <= L * V / N + 1e-12 and worst <= 1 + 1e-9
          and masses.max() - masses.min() < 1e-12)
    print("   %-9s |X|=%-3d r=%d L=%d: same distance profile at every point: %-5s  m_r spread %.1e  admissible %s  |mean G| %.1e  osc/(osc(psi) m_r) %.4f  "
          "max[(R-O)-(A-1)] %+.1e  E O/bound %.3f  P(O>=R/2) %.4f<=%.4f  hit %.4f<=%.4f  tail/McDiarmid %.4f   %s"
          % (name, N, r, L, homog, masses.max() - masses.min(), adm, meanG, osc1, lower, EO / EOb if EOb > 0 else float("nan"),
             pO, pOb, hit / ntot, L * V / N, worst, ("ok" if ok else "FAIL") if expect_homog else ("(control: mean G != 0)" if meanG > 1e-6 else "control FAILED to show a bias")))
    return ok if expect_homog else meanG > 1e-6


def main():
    rng = np.random.default_rng(20261128)
    print("a1_homog.py -- referee A1 -- Lemma 2.5 / Theorem A' on homogeneous finite metric spaces (all tuples of centres)")
    allok = True
    for name, D in (("Petersen", petersen()), ("J(6,3)", johnson(6, 3)), ("H(3,3)", hamming(3, 3)), ("C_9", cycle(9))):
        diam = int(D.max())
        for r in range(1, min(3, diam + 1) + 1):
            for L in (1, 2, 3) + ((4,) if D.shape[0] <= 10 else ()):
                allok &= run(name, D, 1.0, r, L, rng)
    print("   negative controls (the number of points at a given distance depends on the point):")
    for name, D in (("path P_7", path(7)), ("star K_1,6", star(7))):
        for r, L in ((2, 1), (2, 2), (2, 3)):       # r >= 2: for r = 1 the dips are single points and nothing is lost
            allok &= run(name, D, 1.0, r, L, rng, expect_homog=False)
    print("all checks %s" % ("pass" if allok else "FAIL"))


if __name__ == "__main__":
    main()
