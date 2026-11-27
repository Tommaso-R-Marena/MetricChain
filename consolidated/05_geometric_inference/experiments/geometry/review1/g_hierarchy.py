"""(g) Theorem E(d): a globally rigid but not universally rigid 6-point framework on
G = E0 u F = K6 minus {15, 26} (1-based), F = {14, 25, 36, 16}.

 1. statistics over random 6-point configurations: stress space dimension, rank and signature
    of the stress matrix;
 2. EXACT rational witness (fractions): 1-dimensional stress space, stress matrix of rank
    2 = n - 4 and INDEFINITE, and rank 6 of the E0 conic system (N(X) = 0).  Open conditions =>
    they hold at generic configurations nearby, to which Connelly / Gortler-Healy-Thurston
    (globally rigid) and Gortler-Thurston (not universally rigid) apply;
 3. a chain instance (unit bonds, bond angle 97 deg): indefinite stress -> realisation in R^4
    with the same 13 lengths -> two-state ensemble of 3D chains with the averaged data of X on F;
 4. numerical check that this (non-generic) instance is globally rigid: all zeros of the
    4 equations D(X(theta))_F = D(X)_F on the 3-torus of torsions.
"""
from fractions import Fraction as Fr
import itertools
import numpy as np
from scipy.optimize import least_squares
from mylib import build_chain, sqdist, e0_pairs, conic_system, nullspace, unvech

n = 6
E0 = e0_pairs(n)
F = [(0, 3), (1, 4), (2, 5), (0, 5)]
G = E0 + F
assert len(set(G)) == 13 and (0, 4) not in G and (1, 5) not in G


def rigidity_matrix(X, edges):
    dim = X.shape[1]
    R = np.zeros((len(edges), X.size))
    for r, (i, j) in enumerate(edges):
        R[r, dim * i:dim * i + dim] = X[i] - X[j]
        R[r, dim * j:dim * j + dim] = X[j] - X[i]
    return R


def stress(X, edges):
    R = rigidity_matrix(X, edges)
    U, s, Vt = np.linalg.svd(R.T, full_matrices=True)       # R^T omega = 0
    sfull = np.concatenate([s, np.zeros(len(edges) - len(s))])
    nul = int((sfull < 1e-9 * sfull[0]).sum())
    om = Vt[-1]
    Om = np.zeros((len(X), len(X)))
    for wgt, (i, j) in zip(om, edges):
        Om[i, i] += wgt; Om[j, j] += wgt; Om[i, j] -= wgt; Om[j, i] -= wgt
    return Om, nul


def part1(rng):
    sig = {}
    for rep in range(2000):
        X = rng.normal(size=(n, 3))
        Om, nul = stress(X, G)
        ev = np.linalg.eigvalsh(Om)
        big = np.abs(ev) > 1e-8 * np.abs(ev).max()
        key = (nul, int(big.sum()), "indefinite" if ev[big].min() * ev[big].max() < 0 else "semidefinite")
        sig[key] = sig.get(key, 0) + 1
    print("1. 2000 Gaussian 6-point configurations: (stress dim, rank of stress matrix, signature) -> count")
    for k, v in sorted(sig.items()):
        print("     ", k, v)


# ---------------------------------------------------------------- exact part
def frac_nullspace(rows):
    """Basis of the right null space of a rational matrix (list of rows)."""
    A = [list(r) for r in rows]
    nr, nc = len(A), len(A[0])
    piv, r = [], 0
    for c in range(nc):
        p = next((i for i in range(r, nr) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        A[r] = [x / A[r][c] for x in A[r]]
        for i in range(nr):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        piv.append(c); r += 1
        if r == nr:
            break
    free = [c for c in range(nc) if c not in piv]
    basis = []
    for f in free:
        v = [Fr(0)] * nc
        v[f] = Fr(1)
        for i, c in enumerate(piv):
            v[c] = -A[i][f]
        basis.append(v)
    return basis, r


def part2():
    cands = [
        [(0, 0, 0), (1, 0, 0), (1, 2, 0), (3, 1, 2), (2, -1, 3), (4, 2, 1)],
        [(0, 0, 0), (2, 0, 1), (1, 3, 0), (-1, 1, 2), (3, 2, 4), (1, -2, 3)],
        [(0, 0, 0), (1, 1, 0), (3, 0, 1), (2, 2, 3), (0, 3, 1), (1, 4, 4)],
        [(0, 0, 0), (1, 0, 0), (2, 1, 0), (2, 2, 1), (3, 2, 3), (1, 3, 4)],
        [(0, 0, 0), (3, 0, 0), (4, 2, 0), (2, 3, 2), (5, 5, 1), (3, 6, 4)],
    ]
    print("2. exact rational witnesses (all arithmetic in Q):")
    for X in cands:
        X = [tuple(Fr(c) for c in p) for p in X]
        # R^T omega = 0  <=>  for each vertex i and coordinate c: sum_{edges at i} omega_e (x_i - x_j)_c = 0
        rows = []
        for i in range(n):
            for c in range(3):
                row = [Fr(0)] * len(G)
                for e, (a, b) in enumerate(G):
                    if a == i:
                        row[e] = X[a][c] - X[b][c]
                    elif b == i:
                        row[e] = X[b][c] - X[a][c]
                rows.append(row)
        basis, rk = frac_nullspace(rows)
        if len(basis) != 1:
            print("     stress space dimension", len(basis), "-> skip")
            continue
        om = basis[0]
        Om = [[Fr(0)] * n for _ in range(n)]
        for wgt, (i, j) in zip(om, G):
            Om[i][i] += wgt; Om[j][j] += wgt; Om[i][j] -= wgt; Om[j][i] -= wgt
        _, rank_Om = frac_nullspace(Om)
        # signature of a rank-2 symmetric matrix: sign of the sum of its 2x2 principal minors
        # (= e_2 of the eigenvalues = product of the two non-zero eigenvalues)
        e2 = sum(Om[i][i] * Om[j][j] - Om[i][j] * Om[j][i] for i in range(n) for j in range(i + 1, n))
        # conic system of the E0 edges
        idx = [(a, b) for a in range(3) for b in range(a, 3)]
        crow = []
        for (i, j) in E0:
            e = [X[j][c] - X[i][c] for c in range(3)]
            crow.append([e[a] * e[b] * (1 if a == b else 2) for (a, b) in idx])
        _, crank = frac_nullspace(crow)
        # affine span
        _, arank = frac_nullspace([[X[i][c] - X[0][c] for c in range(3)] for i in range(1, n)])
        # non-degenerate bond angles: consecutive bond vectors not parallel
        nondeg = all(any(v != 0 for v in np.cross([float(X[i + 1][c] - X[i][c]) for c in range(3)],
                                                  [float(X[i + 2][c] - X[i + 1][c]) for c in range(3)])) for i in range(n - 2))
        print(f"     X = {[tuple(int(c) for c in p) for p in X]}: rank rigidity = {rk} (stress dim 1), "
              f"rank stress matrix = {rank_Om}, e2(eigenvalues) = {e2} -> {'INDEFINITE' if e2 < 0 else 'semidefinite'}; "
              f"rank E0 conic system = {crank} (of 6); affine rank {arank}; bond angles non-degenerate: {nondeg}")


def part3(rng, ang=97.0):
    bonds = np.ones(n - 1)
    alphas = np.full(n - 2, np.pi - np.deg2rad(ang))
    chain = lambda t: build_chain(t, bonds, alphas)
    for trial in range(10000):
        tors = rng.uniform(-np.pi, np.pi, n - 3)
        X = chain(tors)
        Om, nul = stress(X, G)
        ev = np.linalg.eigvalsh(Om)
        big = np.abs(ev) > 1e-8 * np.abs(ev).max()
        if nul == 1 and big.sum() == 2 and ev[big].min() < -0.2 * np.abs(ev).max() and ev[big].max() > 0.2 * np.abs(ev).max():
            break
    print(f"3. chain instance (unit bonds, {ang} deg), torsions (deg) {np.round(np.rad2deg(tors), 3).tolist()}")
    print(f"     stress space dim {nul}; stress matrix eigenvalues {np.round(ev, 5).tolist()} (rank 2, indefinite)")
    DX = sqdist(X)
    target = np.array([DX[i, j] for (i, j) in G])
    # realisation in R^4 with the same 13 lengths: start from X plus a 4th coordinate q with q^T Omega q = 0
    lam, vec = np.linalg.eigh(Om)
    q = vec[:, -1] / np.sqrt(lam[-1]) + vec[:, 0] / np.sqrt(-lam[0])
    best = None
    for hgt in (0.2, 0.4, 0.6, 0.8, -0.3, -0.6):
        def res(y):
            Y = y.reshape(n, 4)
            r = [((Y[i] - Y[j]) ** 2).sum() - t for (i, j), t in zip(G, target)]
            return np.array(r + list(Y[0]) + [np.std(Y[:, 3]) - abs(hgt) * np.std(q)])
        sol = least_squares(res, np.hstack([X, hgt * q[:, None]]).ravel(), xtol=1e-15, ftol=1e-15, gtol=1e-15)
        Y = sol.x.reshape(n, 4)
        sv = np.linalg.svd(Y - Y.mean(0), compute_uv=False)
        if np.abs(sol.fun).max() < 1e-12 and sv[3] > 1e-2:
            best = Y
            break
    assert best is not None, "no 4D realisation found"
    Y = best
    DY = sqdist(Y)
    print(f"     4D realisation: max length deviation on the 13 bars {max(abs(DY[i,j]-DX[i,j]) for i,j in G):.1e}; "
          f"singular values {np.round(sv, 4).tolist()}; unmeasured pairs differ from X by "
          f"{[round(float(DY[i,j]-DX[i,j]), 4) for (i,j) in [(0,4),(1,5)]]}  => not universally rigid")
    A = conic_system(Y, E0)
    N, s, rank = nullspace(A, 10)
    S = unvech(N[-1], 4)
    evS, Q = np.linalg.eigh(S)
    tp, tm = -1 / evS[0], -1 / evS[-1]
    lamw = -tm / (tp - tm)
    states = []
    for t in (tp, tm):
        l = np.clip(1 + t * evS, 0, None)
        l[np.argmin(l)] = 0
        Xt = Y @ (Q * np.sqrt(l))
        U, sv3, Vt = np.linalg.svd(Xt - Xt.mean(0), full_matrices=False)
        states.append(U[:, :3] * sv3[:3])
    Dmix = lamw * sqdist(states[0]) + (1 - lamw) * sqdist(states[1])
    print(f"     two-state ensemble: weights ({lamw:.5f}, {1-lamw:.5f}); bond/1-3 deviation of the states "
          f"{max(abs(sqdist(S_)[i,j]-DX[i,j]) for S_ in states for i,j in E0):.1e}; "
          f"max deviation of the averaged data from X on F: {max(abs(Dmix[i,j]-DX[i,j]) for i,j in F):.1e}")
    print(f"     the states differ from X on F by {[round(float(max(abs(sqdist(S_)[i,j]-DX[i,j]) for i,j in F)), 4) for S_ in states]}"
          f"  => X is NOT F-ensemble-rigid")
    N3, s3, r3 = nullspace(conic_system(X, E0), 6)
    print(f"     N(X): rank of the E0 conic system of X = {r3} (of 6), smallest singular value ratio {s3[5]/s3[0]:.2e}")
    # 4. global rigidity of the instance: zeros of D(X(theta))_F - D(X)_F on the 3-torus
    tF = np.array([DX[i, j] for (i, j) in F])
    fres = lambda t: np.array([sqdist(chain(t))[i, j] for (i, j) in F]) - tF
    sols = []
    grid = np.linspace(-np.pi, np.pi, 13)[:-1]
    for t0 in itertools.product(grid, repeat=3):
        sol = least_squares(fres, np.array(t0) + 0.01, xtol=1e-15, ftol=1e-15, gtol=1e-15)
        if np.abs(sol.fun).max() < 1e-11:
            t = (sol.x + np.pi) % (2 * np.pi) - np.pi
            if not any(np.abs(np.angle(np.exp(1j * (t - s_)))).max() < 1e-6 for s_ in sols):
                sols.append(t)
    print(f"4. zeros of the 4 measured-pair equations on the 3-torus (12^3 starts): {len(sols)}:")
    for t in sols:
        same = np.abs(sqdist(chain(t)) - DX).max()
        print(f"     torsions (deg) {np.round(np.rad2deg(t), 3).tolist()}  max|D - D(X)| = {same:.1e}  "
              f"({'congruent to X (itself or mirror image)' if same < 1e-8 else 'A DIFFERENT REALISATION'})")


if __name__ == "__main__":
    rng = np.random.default_rng(2718)
    part1(rng)
    part2()
    part3(rng)
