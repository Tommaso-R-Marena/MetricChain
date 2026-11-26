"""O-3, numerical instance: a 7-atom chain that is (numerically) second-moment rigid on a set F
of 5 measured pairs without being universally rigid.

Steps for a candidate (torsions, F):
 1. equilibrium stress omega of (F u E0, X) (one-dimensional), stress matrix Omega: INDEFINITE;
 2. c = s * omega|_F; the constrained Hessian of H_c on the 4 flexes is negative definite:
    X is a strict local maximiser of H_c = sum_F c_ij |x_i - x_j|^2 over chains in R^3;
 3. global maximality over the 4-torus: a grid of 36^4 points plus 2000 local searches -- no
    value above H_c(X), and every maximiser found is X or its mirror image  [numerical, not a
    certificate];
 4. a realisation in R^4 with the lengths of X on F u E0 and affine dimension 4 (so the
    framework is not universally rigid), found by continuation into the fourth dimension.
If 3 holds exactly, D_F(X) is an exposed point of the set of F-averaged data of ensembles of
chains: no ensemble of other chains reproduces the averaged data of X on F, although a
four-dimensional framework has exactly the lengths of X.
"""
import sys
import itertools
import numpy as np
from scipy.optimize import minimize, least_squares
from geomlib import chain, edm
from explore_er3 import stress, flexes, E0, n

CANDIDATES = {
    # found by explore_er3.py (seed 1, trials 10641 and 427)
    "A": ([1.517404361415525, -1.046332870741514, 2.7119835539236874, -1.6743919325698102],
          [(0, 4), (0, 5), (1, 4), (1, 6), (2, 6)]),
    "B": ([1.1977164412277705, 1.1465226973558638, -2.9886139428782164, -1.1097536827938672],
          [(0, 4), (0, 5), (1, 4), (1, 6), (3, 6)]),
}


def verify(tors, F, ngrid=36, nlocal=2000, seed=0, verbose=True):
    rng = np.random.default_rng(seed)
    tors = np.array(tors, float)
    X = chain(n, tors)
    om, Om, sv = stress(X, E0 + F)
    ev = np.linalg.eigvalsh(Om)
    scale = np.abs(ev).max()
    T = flexes(X)
    Hq = np.array([[np.trace(a.T @ Om @ b) for b in T] for a in T])
    hv = np.linalg.eigvalsh((Hq + Hq.T) / 2)
    s = -1.0 if hv.min() > 0 else 1.0
    c = s * om[len(E0):]
    def Hc(tt):
        Xt = chain(n, tt)
        return sum(cij * ((Xt[i] - Xt[j]) ** 2).sum() for (i, j), cij in zip(F, c))
    h0 = Hc(tors)
    # grid
    g = np.linspace(-np.pi, np.pi, ngrid, endpoint=False)
    best_grid = -np.inf
    for t in itertools.product(g, repeat=n - 3):
        v = Hc(np.array(t))
        if v > best_grid:
            best_grid = v
    # local searches
    tops, worst = [], -np.inf
    DX = edm(X)
    other_max = -np.inf
    for _ in range(nlocal):
        r = minimize(lambda tt: -Hc(tt), rng.uniform(-np.pi, np.pi, n - 3), method="BFGS", options=dict(gtol=1e-10))
        v = -r.fun
        worst = max(worst, v)
        same = np.abs(edm(chain(n, r.x)) - DX).max() < 1e-5
        if not same:
            other_max = max(other_max, v)
    out = dict(stress_gap=float(sv[-2]), stress_eig=(ev / scale).round(5).tolist(), flex_hessian_eig=(s * hv / scale).round(5).tolist(),
               H_at_X=float(h0), best_grid=float(best_grid), best_local=float(worst), best_other_local_max=float(other_max),
               margin=float(h0 - other_max))
    # 4D realisation
    target = np.array([((X[i] - X[j]) ** 2).sum() for (i, j) in E0 + F])
    lam, vec = np.linalg.eigh(Om)
    ip, im = np.argmax(lam), np.argmin(lam)
    q = vec[:, ip] / np.sqrt(lam[ip]) + vec[:, im] / np.sqrt(-lam[im])
    res4 = None
    for h in (0.05, 0.1, 0.2, 0.4, -0.05, -0.1, -0.2, -0.4):
        Y0 = np.hstack([X, h * q[:, None]])
        def res(y):
            Y = y.reshape(n, 4)
            r = [((Y[i] - Y[j]) ** 2).sum() - t for (i, j), t in zip(E0 + F, target)]
            r += list(Y[0])
            r.append((Y[:, 3] - Y[:, 3].mean()).std() - abs(h) * q.std())
            return np.array(r)
        sol = least_squares(res, Y0.flatten(), xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=40000)
        if np.abs(sol.fun).max() < 1e-11:
            Y = sol.x.reshape(n, 4)
            s4 = np.linalg.svd(Y - Y.mean(0), compute_uv=False)
            if s4[3] > 1e-3:
                res4 = (float(np.abs(sol.fun).max()), s4.round(4).tolist(),
                        float(np.abs(edm(Y) - DX).max()))
                break
    out["fourD"] = res4
    ok = (out["margin"] > 1e-6 and best_grid <= h0 + 1e-9 and worst <= h0 + 1e-8 and res4 is not None
          and min(abs(e) for e in out["stress_eig"] if abs(e) > 1e-7) > 0 and
          (np.array(out["stress_eig"]) > 1e-7).any() and (np.array(out["stress_eig"]) < -1e-7).any())
    if verbose:
        for k, v in out.items():
            print(f"  {k}: {v}")
        print("  couplings c on F:", dict(zip(F, np.round(c, 6).tolist())))
        print("  CONSISTENT with: unique global maximiser in R^3, indefinite stress, 4D realisation" if ok else "  NOT confirmed")
    return ok, out


if __name__ == "__main__":
    for name in (sys.argv[1:] or ["A"]):
        tors, F = CANDIDATES[name]
        print(f"candidate {name}: torsions {tors}, F = {F}")
        verify(tors, F, ngrid=int(24))
