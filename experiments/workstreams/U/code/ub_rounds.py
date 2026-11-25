#!/usr/bin/env python3
"""Upper bounds: the round-limited ladder recursion T^(r) (Theorem U1 + Theorems 11.52/11.56 of the theory report).

T^(1) = theta_na on (0, inf), T^(1)(0) = a.  An r-round bracket family is obtained from a ladder with rungs
l = 1..L whose inner procedures use r_1 + ... + r_L <= r rounds (Theorem U1: the rungs are processed one after the
other, all fibres of a rung in parallel).  With outer fraction phi, tolerance rate beta (0 at bounded accuracy),
mu = phi*theta_na((g-beta)/phi) (phi*a at g = 0), rates xi_1 > ... > xi_L, xi_L = beta/(1-phi) (0 at g = 0):

  cost(g) = max{ mu + (1-phi) T^(r_1)(xi_1),  max_{l>=2} [ min(mu, (1-phi) xi_{l-1}) + (1-phi) T^(r_l)(xi_l) ] }.

T^(r)(g) = min( T^(r-1)(g), inf over phi, beta, ladders ).  Everything is evaluated on grids with *conservative*
rounding (a requested accuracy is rounded down to a grid point, costs are step functions), so every printed number
is an upper bound for the recursion and hence (up to the arbitrarily small losses of the theorems) for tau^(r).
Necessary conditions checked:  T^(1) = theta_na is not improved by one-round ladders;  T^(r) >= theta_hint;
T^(r) nonincreasing in r.
usage: ub_rounds.py mode r1,r2,... [K]      mode = gauss | u-value (e.g. 1.0); the list of round numbers must be increasing;
       ladders for r use inner procedures with round numbers among {1} and the earlier entries of the list
"""
import sys, math, time
import numpy as np


class Model:
    def __init__(self, mode):
        if mode == "gauss":
            self.a, self.h, self.eps = 1.0, 0.25, 1.0
            self.th_na = lambda x: np.where(x >= 1.0, 0.0, (1 - np.sqrt(np.clip(x, 0, 1))) ** 2)
            self.th_hint = lambda e: np.where(e >= 1.0, 0.0, (1 - np.clip(e, 0, 1)) ** 2 / 4)
        else:
            from ulib import Cube, f
            u = float(mode)
            c = Cube(u)
            self.a, self.h, self.eps = c.a, c.h, c.eps_star
            rr = np.linspace(c.pu, 0.5, 200001)
            kk = c.kl_pu(rr); kk[0] = 0.0
            ff = f(rr)
            self.th_na = lambda x: np.where(np.asarray(x) >= c.eps_star, 0.0, np.interp(np.clip(x, 0, c.eps_star), kk, ff))
            self.th_hint = lambda e: np.where(np.asarray(e) >= c.eps_star, 0.0, f(np.clip((c.Lam1 + np.asarray(e)) / u, 0, 0.5)))


def run(mode, rs, K=160, nphi=79, nbeta=24, verbose=True):
    M = Model(mode)
    a, h, eps = M.a, M.h, M.eps
    # accuracy grid: xi_0 = 0 (bounded accuracy), xi_k = eps*(k/K)^2, k = 1..K  (xi_K = eps: cost 0)
    grid = eps * (np.arange(0, K + 1) / K) ** 2
    T = {1: np.concatenate([[a], np.asarray(M.th_na(grid[1:]), dtype=float)])}
    T[1][-1] = 0.0
    phis = np.linspace(0.0125, 0.9875, nphi)
    best_info = {}

    def inv(tab, y):
        """smallest grid index k with tab[k] <= y (tab nonincreasing); K+1 (infeasible) cannot occur since tab[K] = 0."""
        # tab is nonincreasing: search on reversed array
        y = np.asarray(y)
        idx = len(tab) - np.searchsorted(tab[::-1], y, side="right")
        return np.clip(idx, 0, len(tab) - 1), (y >= 0)

    for r in rs:
        t0 = time.time()
        parts = sorted(T.keys())
        prev = T[parts[-1]]
        new = prev.copy()
        info = [None] * (K + 1)
        for gi in range(0, K):                       # target accuracy index (K: cost 0 anyway)
            g = grid[gi]
            # candidate tolerances beta: grid points xi_b with (1-phi) xi_b < g  (g = 0: only beta = 0)
            if gi == 0:
                betas_idx = np.array([0])
            else:
                betas_idx = np.unique(np.round(np.linspace(1, gi, min(nbeta, gi))).astype(int))
            PH, BI = np.meshgrid(phis, betas_idx, indexing="ij")
            xiL = grid[BI]                            # last rung accuracy rate (inner dimension)
            beta = (1 - PH) * xiL
            ok0 = beta < g if gi > 0 else np.ones_like(beta, dtype=bool)
            if gi == 0:
                mu = PH * a
            else:
                mu = PH * np.asarray(M.th_na(np.maximum(g - beta, 0) / PH))
            lo = np.full(PH.shape, h * 0.5)
            hi = np.full(PH.shape, float(prev[gi]) + 1e-12)
            for _ in range(26):
                v = 0.5 * (lo + hi)
                # DP over rounds: cur[rho] = smallest reachable accuracy index with rho rounds used (K+1: nothing yet)
                reach = [None] * (r + 1)
                feas = np.zeros(PH.shape, dtype=bool)
                for rho in range(1, r + 1):
                    bestk = np.full(PH.shape, K + 5)
                    for r1 in parts:
                        if r1 > rho:
                            break
                        if rho - r1 == 0:
                            c = mu
                            valid = np.ones(PH.shape, dtype=bool)
                        else:
                            pk = reach[rho - r1]
                            valid = pk <= K
                            c = np.minimum(mu, (1 - PH) * grid[np.clip(pk, 0, K)])
                        y = (v - c) / (1 - PH)
                        k, pos = inv(T[r1], y)
                        k = np.where(valid & pos, k, K + 5)
                        bestk = np.minimum(bestk, k)
                    reach[rho] = bestk
                    feas |= bestk <= BI
                feas &= ok0
                hi = np.where(feas, v, hi)
                lo = np.where(feas, lo, v)
            val = np.where(ok0, hi, np.inf)
            j = np.unravel_index(np.argmin(val), val.shape)
            if val[j] < new[gi]:
                new[gi] = val[j]
                info[gi] = (float(PH[j]), float(xiL[j]))
        # monotone hull in the accuracy (a procedure for a smaller accuracy serves a larger one)
        new = np.minimum.accumulate(new)
        T[r] = new
        best_info[r] = info
        if verbose:
            viol = float(np.max(np.asarray(M.th_hint(grid)) - new))
            print(f"r={r}: T(0)/a={new[0]/a:.4f}  [phi={info[0][0] if info[0] else float('nan'):.3f}]  "
                  f"T(eps*/16)/a={new[K//4]/a:.4f} T(eps*/4)/a={new[K//2]/a:.4f}  max(theta_hint - T)={viol:+.2e}  "
                  f"monotone in r: {bool(np.all(new <= prev + 1e-12))}  ({time.time()-t0:.0f}s)", flush=True)
    return M, grid, T


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "gauss"
    rs = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [2, 3, 4, 5, 6]
    K = int(sys.argv[3]) if len(sys.argv) > 3 else 160
    M = Model(mode)
    print(f"mode={mode}: a={M.a:.6f} h={M.h:.6f} h/a={M.h/M.a:.4f} eps*={M.eps:.6f}; grid K={K} (conservative rounding)")
    # necessary condition: one-round ladders do not beat theta_na
    worst = 0.0
    for g in np.linspace(0.02, 0.9, 23) * M.eps:
        ph = np.linspace(0.01, 0.99, 197)[:, None]
        be = np.linspace(0.001, 0.999, 500)[None, :] * g
        val = ph * M.th_na((g - be) / ph) + (1 - ph) * M.th_na(be / (1 - ph))
        worst = min(worst, float(np.min(val) - M.th_na(g)))
    print(f"one-round product samples: min over (g, phi, beta) of [phi th_na((g-beta)/phi) + (1-phi) th_na(beta/(1-phi)) - th_na(g)] = {worst:+.2e} (must be >= 0)")
    Mm, grid, T = run(mode, rs, K)
    print("table  T^(r)(0)/a :", "  ".join(f"r={r}:{T[r][0]/M.a:.4f}" for r in sorted(T)))
    print("(T^(r)(0) - h)/a   :", "  ".join(f"r={r}:{(T[r][0]-M.h)/M.a:.4f}" for r in sorted(T)))
