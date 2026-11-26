"""(b) Attempt to FALSIFY Theorem B by a direct search in torsion space (no use of the stacking
theory): given the mean squared-distance matrix M of a random 2-state ensemble of chains with n
atoms, look for a K'-state ensemble of chains (K' = 2, 3, 4) with the same bond data whose mean
squared-distance matrix equals M to 1e-10 and which is NOT the true ensemble.

usage: python3 b_direct.py n Kfit nstart [seed] [angle_deg] [kind]
"""
import sys
import time
import numpy as np
from multiprocessing import Pool
from scipy.optimize import least_squares
from mylib import build_chain, sqdist, free_pairs, procrustes_dist


def dD_dtors(X):
    """Derivative of the squared distances on the free pairs w.r.t. each torsion.
    torsion t rotates atoms j >= t+3 about the axis x_{t+1} -> x_{t+2}."""
    n = len(X)
    P = free_pairs(n)
    I = np.array([p[0] for p in P])
    Jx = np.array([p[1] for p in P])
    out = np.zeros((len(P), n - 3))
    for t in range(n - 3):
        u = X[t + 2] - X[t + 1]
        u = u / np.linalg.norm(u)
        mask = (I < t + 3) & (Jx >= t + 3)
        dxj = np.cross(u, X[Jx[mask]] - X[t + 2])
        out[mask, t] = 2 * np.einsum("ij,ij->i", X[Jx[mask]] - X[I[mask]], dxj)
    return out


class Problem:
    def __init__(self, n, K, rng, angle_deg=97.0, kind="homog"):
        self.n = n
        if kind == "homog":
            self.bonds = np.ones(n - 1)
            self.alphas = np.full(n - 2, np.pi - np.deg2rad(angle_deg))
        else:
            self.bonds = rng.uniform(0.8, 1.6, n - 1)
            self.alphas = np.pi - np.deg2rad(rng.uniform(85, 140, n - 2))
        self.w = rng.dirichlet(np.ones(K) * 4)
        self.tors = [rng.uniform(-np.pi, np.pi, n - 3) for _ in range(K)]
        self.Xs = [self.chain(t) for t in self.tors]
        self.Ds = [sqdist(X) for X in self.Xs]
        self.M = sum(wk * D for wk, D in zip(self.w, self.Ds))
        P = free_pairs(n)
        self.I = np.array([p[0] for p in P])
        self.J = np.array([p[1] for p in P])
        self.target = self.M[self.I, self.J]

    def chain(self, t):
        return build_chain(t, self.bonds, self.alphas)

    def unpack(self, p, Kf):
        n = self.n
        T = p[:Kf * (n - 3)].reshape(Kf, n - 3)
        s = np.concatenate([[0.0], p[Kf * (n - 3):]])
        s = s - s.max()
        v = np.exp(s)
        v /= v.sum()
        return T, v

    def residual(self, p, Kf):
        T, v = self.unpack(p, Kf)
        r = -self.target.copy()
        for a in range(Kf):
            D = sqdist(self.chain(T[a]))
            r += v[a] * D[self.I, self.J]
        return r

    def jac(self, p, Kf):
        n = self.n
        T, v = self.unpack(p, Kf)
        cols = []
        dvals = []
        for a in range(Kf):
            X = self.chain(T[a])
            cols.append(v[a] * dD_dtors(X))
            dvals.append(sqdist(X)[self.I, self.J])
        dvals = np.array(dvals).T                       # pairs x Kf
        mean = dvals @ v
        # d r / d s_b = v_b (D_b - mean),  b = 1..Kf-1
        ws = (dvals[:, 1:] - mean[:, None]) * v[None, 1:]
        return np.hstack(cols + [ws])

    def classify(self, p, Kf):
        """Distance of the fitted ensemble from the true one as a distribution on shapes:
        Q = sum_a v_a min_k d_P(Y_a, X_k)^2  (the quantity bounded in Theorem G(c)) and the
        deviation of the weights aggregated on the nearest true state."""
        T, v = self.unpack(p, Kf)
        agg = np.zeros(len(self.w))
        Q = 0.0
        for a in range(Kf):
            Y = self.chain(T[a])
            d = [procrustes_dist(Y, Xk) for Xk in self.Xs]
            k = int(np.argmin(d))
            Q += v[a] * d[k] ** 2
            agg[k] += v[a]
        return Q, np.abs(agg - self.w).max()


def one_start(args):
    prob, Kf, seed = args
    rng = np.random.default_rng(seed)
    n = prob.n
    p0 = np.concatenate([rng.uniform(-np.pi, np.pi, Kf * (n - 3)), rng.normal(size=Kf - 1)])
    try:
        sol = least_squares(prob.residual, p0, jac=prob.jac, args=(Kf,), method="lm",
                            xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=4000)
    except Exception as e:                               # LM needs residuals >= params
        sol = least_squares(prob.residual, p0, jac=prob.jac, args=(Kf,), method="trf",
                            xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=4000)
    r = np.abs(sol.fun).max()
    nontrue_mass, wdev = prob.classify(sol.x, Kf)
    return r, nontrue_mass, wdev, sol.x


def main():
    n = int(sys.argv[1])
    Kf = int(sys.argv[2])
    nstart = int(sys.argv[3])
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    angle = float(sys.argv[5]) if len(sys.argv) > 5 else 97.0
    kind = sys.argv[6] if len(sys.argv) > 6 else "homog"
    rng = np.random.default_rng(1000 + seed)
    prob = Problem(n, 2, rng, angle, kind)
    # sanity: analytic Jacobian against finite differences
    p = np.concatenate([rng.uniform(-np.pi, np.pi, Kf * (n - 3)), rng.normal(size=Kf - 1)])
    Jn = np.array([(prob.residual(p + 1e-6 * e, Kf) - prob.residual(p - 1e-6 * e, Kf)) / 2e-6
                   for e in np.eye(len(p))]).T
    jerr = np.abs(Jn - prob.jac(p, Kf)).max()
    t0 = time.time()
    with Pool(4) as pool:
        res = pool.map(one_start, [(prob, Kf, 7919 * seed + s) for s in range(nstart)], chunksize=8)
    zero = [r for r in res if r[0] < 1e-10]
    # a zero-residual solution is "the true ensemble" if all its mass sits (within the accuracy
    # allowed by Theorem G for a residual of 1e-10) on the true shapes with the true weights
    true_hits = [r for r in zero if r[1] < 1e-6 and r[2] < 1e-3]
    alt = [r for r in zero if not (r[1] < 1e-6 and r[2] < 1e-3)]
    nonzero = sorted(r[0] for r in res if r[0] >= 1e-10)
    print(f"n={n} true K=2 (w={np.round(prob.w, 4).tolist()}), fit K'={Kf}, kind={kind}, angle={angle}, seed={seed}: "
          f"{nstart} starts, jac err {jerr:.1e}, {time.time() - t0:.0f}s")
    print(f"   converged to max|dM| < 1e-10: {len(zero)}   of which the true ensemble: {len(true_hits)}   "
          f"ALTERNATIVES (not the true ensemble): {len(alt)}")
    if zero:
        print(f"   among converged runs: max Q = sum_a v_a min_k d_P^2 = {max(r[1] for r in zero):.2e}, max weight deviation {max(r[2] for r in zero):.2e}")
    if nonzero:
        print(f"   smallest max|dM| among non-converged local minima: {nonzero[0]:.3e} (median {np.median(nonzero):.2e})")
    # empirical test of Theorem G(c): Q <= C * ||M(nu) - M(mu)||_F for every ensemble nu
    rat = []
    for r in res:
        if r[0] > 1e-7:
            T, v = prob.unpack(r[3], Kf)
            Mfit = sum(va * sqdist(prob.chain(Ta)) for va, Ta in zip(v, T))
            rat.append(r[1] / np.linalg.norm(Mfit - prob.M))
    if rat:
        print(f"   largest Q/||M(nu)-M(mu)||_F over the non-converged end points: {max(rat):.3f}")
    for r in alt[:5]:
        T, v = prob.unpack(r[3], Kf)
        print(f"   ALT: max|dM|={r[0]:.2e} weights={np.round(v, 5).tolist()} Q={r[1]:.3e} weight dev={r[2]:.2e}")
        for a in range(Kf):
            Y = prob.chain(T[a])
            print(f"        state {a}: weight {v[a]:.5f}, d_P to true states = "
                  + ", ".join(f"{procrustes_dist(Y, Xk):.3e}" for Xk in prob.Xs))
    return prob, res


if __name__ == "__main__":
    main()
