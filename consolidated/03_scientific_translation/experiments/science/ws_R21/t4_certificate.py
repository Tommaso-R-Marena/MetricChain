"""T4 — Corollary E8 in numbers (own code): the certificate
        f(p) = sum_e prod_i ( t_e(p) - t_e(x_i) )^2 ,   t_e = squared length of edge e,
its mean under the ensemble, under perturbed ensembles, and what error of the 2K moments per edge
it tolerates.

Quantities (lengths in units in which conformer coordinates are standard normal):
  C_abs   = sum_{e, j=1..2K} |c_{e,j}| m_{e,j}(mu)      (c: monomial coefficients of the certificate)
            if every moment is known to relative accuracy eps, the mean of f is known to eps*C_abs.
  gamma*(r) = min{ f(p) : D(p) >= r },  D(p) = min_i || t_full(p) - t_full(x_i) ||_2 over ALL pairs
            (the value of the certificate at the best "near-chimera" at shape distance >= r).
  guarantee (Markov, any nu):  nu(D >= r) <= eps * C_abs / gamma*(r).
  adversary (linear programme over an explicit finite candidate set): the largest mass at D >= r
            of an ensemble whose 2K|E| moments are within relative eps of those of mu.
usage: python3 -B t4_certificate.py <graph> <K> <seed> [n_inst]
"""
import sys
import numpy as np
from scipy.optimize import linprog, minimize
from r21_common import *

name = sys.argv[1]
K = int(sys.argv[2])
seed = int(sys.argv[3])
n_inst = int(sys.argv[4]) if len(sys.argv) > 4 else 3
rng = np.random.default_rng(seed)
N, E = graph_table()[name]
m = len(E)
EF = complete(N)
R = Realiser(N, E)
n = R.n
print(f"T4 certificate  graph={name} N={N} m={m} K={K} seed={seed} instances={n_inst}  start {now()}")
print(f"   number of means used by E8: 2K|E| = {2*K*m};  unknowns K(2N-3) + K - 1 = {K*(2*N-3) + K - 1}")


def make(X, w):
    Tc = sqlen(X, E)                                   # (K, m)
    Tfull = sqlen(X, EF)
    coef = np.zeros((m, 2 * K + 1))                    # lowest degree first
    for e in range(m):
        g = np.poly(Tc[:, e])
        coef[e] = np.polymul(g, g)[::-1]
    mom = np.array([[np.sum(w * Tc[:, e] ** j) for j in range(2 * K + 1)] for e in range(m)])   # (m, 2K+1)

    def fun(Z, want_jac):
        r, Jt = R.res_jac(Z, np.zeros((Z.shape[0], m)), want_jac)      # r = t(p)
        diff = r[:, None, :] - Tc[None, :, :]                             # (B, K, m)
        g = np.prod(diff, axis=1)
        if not want_jac:
            return g, None
        gp = np.zeros_like(g)
        for i in range(K):
            others = [j for j in range(K) if j != i]
            gp += np.prod(diff[:, others, :], axis=1) if others else 1.0
        return g, gp[:, :, None] * Jt

    def fval(Z):
        g, _ = fun(Z, False)
        return np.sum(g * g, axis=1)

    def D(Z):
        tf = sqlen(embed(Z, N), EF)
        return np.min(np.linalg.norm(tf[:, None, :] - Tfull[None, :, :], axis=2), axis=1)

    return Tc, Tfull, coef, mom, fun, fval, D


for inst in range(n_inst):
    X = rng.standard_normal((K, N, 2))
    w = rng.dirichlet(np.ones(K) * 3.0)
    Tc, Tfull, coef, mom, fun, fval, D = make(X, w)
    Zc = np.array([gauge(x) for x in X])
    print(f"--- instance {inst}: weights {np.round(w, 3)}; squared lengths range {Tc.min():.2f}..{Tc.max():.2f}; "
          f"min |t_e(x_i) - t_e(x_j)| = {(np.min(np.abs(Tc[:, None] - Tc[None])[np.triu_indices(K, 1)]) if K > 1 else np.nan):.3f}")
    # (1) mean of the certificate
    mean_direct = float(np.sum(w * fval(Zc)))
    mean_moments = float(np.sum(coef * mom))
    C_abs = float(np.sum(np.abs(coef[:, 1:]) * mom[:, 1:]))
    print(f"(1) mean of f under mu: direct {mean_direct:.2e}; from the moments sum c*m = {mean_moments:.2e} "
          f"(cancellation: C_abs = sum |c| m = {C_abs:.3e}; rounding floor about {C_abs*2e-16:.1e})")
    # (2) perturbed ensembles
    w2 = rng.dirichlet(np.ones(K) * 3.0)
    lowmom = max(abs(np.sum((w2 - w) * Tc[:, e] ** j) / mom[e, j]) for e in range(m) for j in range(1, 2 * K + 1))
    print(f"(2a) other weights {np.round(w2, 3)}: mean of f = {float(np.sum(w2 * fval(Zc))):.2e} (blind to weights); "
          f"largest relative change of a moment {lowmom:.3f}")
    V = rng.standard_normal((K, n))
    V /= np.linalg.norm(V, axis=1, keepdims=True)
    deltas = np.array([1e-1, 1e-2, 1e-3, 1e-4])
    vals = np.array([float(np.sum(w * fval(Zc + d * V))) for d in deltas])
    slope = np.polyfit(np.log(deltas[1:]), np.log(vals[1:]), 1)[0]
    print(f"(2b) every conformer displaced by delta (unit vector in the gauge chart): mean f = "
          + ", ".join(f"{v:.2e} (delta={d:g})" for d, v in zip(deltas, vals)) + f"; fitted exponent {slope:.3f}")
    # split of conformer 0: 1/2 delta(x+sv) + 1/2 delta(x-sv)
    ss = np.array([1e-1, 3e-2, 1e-2, 3e-3, 1e-3])
    errs = []
    for s in ss:
        Tp = sqlen(embed(np.stack([Zc[0] + s * V[0], Zc[0] - s * V[0]]), N), E)     # (2, m)
        e_rel = 0.0
        for e in range(m):
            for j in range(1, 2 * K + 1):
                mm = mom[e, j] - w[0] * Tc[0, e] ** j + w[0] * 0.5 * (Tp[0, e] ** j + Tp[1, e] ** j)
                e_rel = max(e_rel, abs(mm - mom[e, j]) / mom[e, j])
        errs.append(e_rel)
    errs = np.array(errs)
    sl = np.polyfit(np.log(ss), np.log(errs), 1)
    print(f"(2c) conformer 0 split into two at +-s: largest relative moment error = "
          + ", ".join(f"{v:.2e} (s={d:g})" for d, v in zip(ss, errs)) + f"; exponent {sl[0]:.3f}"
          f"  => moments within eps cannot exclude a spread s ~ {np.exp(-sl[1]/sl[0]):.2f} * eps^(1/{sl[0]:.2f})")
    # (3) near-chimeras: local minima of f
    nst = 6000
    Z0 = 1.5 * rng.standard_normal((nst, n))
    Z, cost, gn = batched_lm(fun, Z0, iters=300)
    d = D(Z)
    zero = cost < 1e-16
    conv = gn < 1e-6 * (1 + cost)
    zero_far = zero & (d > 1e-5)
    print(f"(3) {nst} LM runs on f: {int(zero.sum())} reach f < 1e-16; of these {int(zero_far.sum())} are NOT a conformer "
          f"(D > 1e-5) [E8: must be 0]; conformers reached: {[int(np.sum(zero & (np.linalg.norm(sqlen(embed(Z, N), EF) - Tfull[i], axis=1) < 1e-5))) for i in range(K)]}")
    loc = (~zero) & conv
    order = np.argsort(cost[loc])
    Zl, cl, dl = Z[loc][order], cost[loc][order], d[loc][order]
    if len(cl):
        print(f"    positive local minima found: {len(cl)} runs; lowest values f = {np.array2string(np.unique(np.round(cl, 12))[:5], precision=3)}; "
              f"lowest: f = {cl[0]:.3e} at shape distance D = {dl[0]:.3f}")
    for r in (0.3, 1.0):
        cand = cl[dl >= r]
        g_lm = cand.min() if len(cand) else np.inf
        # boundary / constrained refinement with SLSQP
        best_c = g_lm

        def obj(z):
            return float(fval(z[None])[0])

        cons = [{'type': 'ineq', 'fun': (lambda z, i=i: float(np.sum((sqlen(embed(z[None], N), EF)[0] - Tfull[i]) ** 2) - r * r))} for i in range(K)]
        starts = []
        for i in range(K):
            for _ in range(25):
                v = rng.standard_normal(n)
                v /= np.linalg.norm(v)
                # scale so that D ~ r
                lo, hi = 0.0, 5.0
                for _ in range(40):
                    mid = 0.5 * (lo + hi)
                    if D((Zc[i] + mid * v)[None])[0] < r:
                        lo = mid
                    else:
                        hi = mid
                starts.append(Zc[i] + hi * v)
        for z0 in starts:
            res = minimize(obj, z0, method='SLSQP', constraints=cons, options={'maxiter': 300, 'ftol': 1e-15})
            if res.success and all(c['fun'](res.x) >= -1e-9 for c in cons):
                best_c = min(best_c, res.fun)
        gam = best_c
        print(f"    r = {r}: gamma*(r) = {gam:.3e} (LM local minima with D >= r: {g_lm:.3e}; after boundary search: {best_c:.3e}); "
              f"guarantee nu(D >= r) <= eps * {C_abs / gam:.3e}  => for 10% of the mass: eps <= {0.1 * gam / C_abs:.2e}")
        # (4) adversary: linear programme over an explicit finite candidate set (two sizes, to see the dependence)
        def candidates(mult):
            cl_ = [Zc]
            for sc in (1e-3, 3e-3, 1e-2, 3e-2, 1e-1, 3e-1):
                for i in range(K):
                    cl_.append(Zc[i] + sc * rng.standard_normal((100 * mult, n)))
            if len(Zl):
                _, ui = np.unique(np.round(cl, 10), return_index=True)
                near = Zl[ui][:40]
                cl_.append(near)
                for sc in (1e-3, 1e-2, 1e-1):
                    for z in near[:20]:
                        cl_.append(z + sc * rng.standard_normal((10 * mult, n)))
            cl_.append(1.2 * rng.standard_normal((2000 * mult, n)))
            return np.vstack(cl_)

        def rows_of(Yc):
            Ty = sqlen(embed(Yc, N), E)
            return np.array([Ty[:, e] ** j / mom[e, j] for e in range(m) for j in range(1, 2 * K + 1)])

        for mult in (1, 3):
            Yc = candidates(mult)
            A = rows_of(Yc)
            keep = np.max(A, axis=0) <= 30.0          # drop candidates with huge normalised moments (useless to the adversary, bad for the LP)
            keep[:K] = True
            Yc, A = Yc[keep], A[:, keep]
            far = D(Yc) >= r
            out = []
            for eps in (1e-2, 1e-3, 1e-4, 1e-5):
                A_ub = np.vstack([A, -A])
                b_ub = np.concatenate([np.full(A.shape[0], 1 + eps), -np.full(A.shape[0], 1 - eps)])
                res = linprog(-far.astype(float), A_ub=A_ub, b_ub=b_ub, A_eq=np.ones((1, len(Yc))), b_eq=[1.0],
                              bounds=(0, None), method='highs', options={'time_limit': 60, 'primal_feasibility_tolerance': 1e-9, 'dual_feasibility_tolerance': 1e-9})
                if res.status != 0:
                    out.append((eps, np.nan, np.nan, res.status, 0))
                    continue
                nu = np.maximum(res.x, 0)
                nu /= nu.sum()
                actual = np.max(np.abs(A @ nu - 1))
                out.append((eps, float(nu[far].sum()), actual, 0, int(np.sum(nu > 1e-9))))
            print(f"    adversary LP, r = {r}, {len(Yc)} candidates ({int(far.sum())} far): mass at D >= r of an explicit ensemble whose "
                  f"{2*K*m} moments are within relative eps of mu's: "
                  + "; ".join((f"eps={e:g}: {mfar:.3e} (achieved err {a:.1e}, {ns} atoms; Markov bound {min(1.0, e * C_abs / gam):.1e})"
                               if st == 0 else f"eps={e:g}: LP status {st}") for e, mfar, a, st, ns in out))
print("DONE t4_certificate", name, K, now())
