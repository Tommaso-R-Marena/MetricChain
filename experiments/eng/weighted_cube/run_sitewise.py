"""Site-wise labels on blocks of L = 1 .. Lmax sites: what longer blocks could give (results/sitewise.json).

The 2^L site-wise labels phi_sigma(x) = sum_i w_i [x_i != sigma_i] are vertices of the weighted cube for every
slope ratio (every edge is tight), so

    sw_L := capacity of the block restricted to these labels  <=  cap_L        for every L,

without any enumeration.  Two uses:

* RIGOROUS (up to floating point; the values are primal values I(M) of explicit weights M): if sw_L / L >= the
  cube's capacity exponent, the Markov recursion with blocks of L sites cannot show that the chain's exponent
  is below the cube's.  This gives, per cell, the shortest block length that could possibly decide.
* NUMERICAL, conditional: for L <= 4 the exact vertex lists show sw_L = cap_L in most cells (all cells with
  p >= 0.3).  IF that persisted for all L, the increments sw_L - sw_{L-1} would converge to a_inf itself; they
  are reported as an indication, exactly like increments of finite chains, and are not bounds.

Usage (repository root):   python experiments/eng/weighted_cube/run_sitewise.py [--Lmax 8]     # about 10 minutes
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fractions import Fraction  # noqa: E402

from metricchain_eng.weighted_cube import exponents as EX  # noqa: E402
from run_bounds import P_GRID, U_GRID, load_chambers  # noqa: E402

RES = Path(__file__).resolve().parent / "results"


def sitewise_rows(L: int, p: float, u: float) -> np.ndarray:
    us = EX.ustar(p, u)
    n = 1 << L
    logpi = EX.block_law_log(L, p)
    x = np.arange(n)
    bits = (x[:, None] >> np.arange(L)[None, :]) & 1
    w = np.array([u] * (L - 1) + [us])
    D = (bits[:, None, :] != bits[None, :, :]) @ w        # D[sigma, x] = phi_sigma(x)
    lw = logpi[None, :] - D
    lw -= lw.max(axis=1, keepdims=True)
    W = np.exp(lw)
    return W / W.sum(axis=1, keepdims=True)


def sitewise_capacity(L: int, p: float, u: float, tol: float = 1e-12):
    """(lower, upper) for the capacity over the site-wise labels: lower = I(M) for explicit weights M,
    upper = the largest KL(W_sigma || Q_M) over the site-wise labels (NOT over all vertices).
    Up to L = 8 the dual solver of ``exponents.capacity_solve`` is used; beyond (or if it fails) Blahut-Arimoto
    iterations locate the support and Newton's method on "equal values on the support" with an active-set loop
    finishes."""
    W = sitewise_rows(L, p, u)
    if L <= 8:
        s = EX.capacity_solve(W)
        if s["upper"] - s["lower"] <= 1e-10 or L <= 6:
            return s["lower"], s["upper"]
    m = W.shape[0]
    negH = np.einsum("ij,ij->i", W, np.log(W))

    def residual_jac(S, Ms):
        Ws = W[S]
        Q = Ms @ Ws
        return negH[S] - Ws @ np.log(Q), -(Ws / Q) @ Ws.T

    best = EX.capacity_iterate(W, iters=400)
    for _round in range(60):
        if best["upper"] - best["lower"] <= tol * max(1.0, best["lower"]):
            break
        M = best["M"]
        S = np.flatnonzero(M > 1e-7 * M.max())
        improved = False
        for _inner in range(30):
            Ms = EX._equalise(list(S), M[S] / M[S].sum(), residual_jac)
            if Ms is None:
                break
            full = np.zeros(m)
            full[S] = Ms
            Q, kl, lo, up = EX._capacity_eval(W, negH, full)
            if up - lo < best["upper"] - best["lower"]:
                best = dict(lower=lo, upper=up, M=full, Q=Q)
                improved = True
            viol = np.flatnonzero(kl > lo + tol)
            viol = viol[~np.isin(viol, S)]
            if len(viol) == 0:
                break
            add = viol[np.argsort(-kl[viol])[:8]]
            M = full.copy()
            M[add] = 1e-6
            S = np.concatenate([S, add])
        if not improved:
            nxt = EX.capacity_iterate(W, np.maximum(best["M"], 1e-12), iters=3000)
            if nxt["upper"] - nxt["lower"] < best["upper"] - best["lower"]:
                best = nxt
            else:
                break
    return best["lower"], best["upper"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--Lmax", type=int, default=8)
    ap.add_argument("--p", type=str, nargs="*", default=P_GRID)
    ap.add_argument("--u", type=str, nargs="*", default=U_GRID)
    args = ap.parse_args()
    cells = []
    t_all = time.time()
    for p_str in args.p:
        for u_str in args.u:
            p, u = float(p_str), float(u_str)
            ac = EX.cube_exponents(u)[2]
            t0 = time.time()
            rows = []
            for L in range(1, args.Lmax + 1):
                lo, up = sitewise_capacity(L, p, u)
                rows.append(dict(L=L, lower=lo, upper=up, gap=up - lo, per_site=lo / L, ratio_to_cube=lo / L / ac))
            inc = [rows[k]["lower"] - rows[k - 1]["lower"] for k in range(1, len(rows))]
            rate = inc[-1]
            intercept = rows[-1]["lower"] - args.Lmax * rate
            first_below = next((r["L"] for r in rows if r["per_site"] < ac), None)
            est = None
            if first_below is None and rate < ac:
                est = int(np.floor(intercept / (ac - rate))) + 1
            cells.append(dict(p=p_str, u=u_str, cube_a=ac, blocks=rows, largest_gap=max(r["gap"] for r in rows), increments=inc,
                              increment_ratio_to_cube=[v / ac for v in inc],
                              last_increment_ratio_to_cube=rate / ac, first_L_with_sitewise_below_cube=first_below,
                              extrapolated_first_L=est, seconds=round(time.time() - t0, 1)))
            print(f"p={p_str} u={u_str}: sw_L/(L cube) = " + " ".join(f"{r['ratio_to_cube']:.4f}" for r in rows)
                  + f" | last increment/cube {rate / ac:.5f} | first L below: {first_below} (extrapolated {est})"
                  + f" | largest gap {max(r['gap'] for r in rows):.1e}", flush=True)
    # numerical estimates of the slope at which the INCREMENT of the block capacity crosses the cube
    crossing = []
    chambers = {L: load_chambers(L)[0] for L in (3, 4)}

    def exact_cap(L, p, u):
        us = EX.ustar(p, u)
        c = next(c for c in chambers[L] if c.contains(Fraction(us / u)))
        return EX.capacity_bound(EX.BlockProblem(c, p, u))["lower"]

    def root(f, lo, hi, tol=5e-4):
        flo = f(lo)
        if (flo > 0) == (f(hi) > 0):
            return None
        while hi - lo > tol:
            mid = 0.5 * (lo + hi)
            if (f(mid) > 0) == (flo > 0):
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    for p_str in args.p:
        p = float(p_str)
        f_exact = lambda u: exact_cap(4, p, u) - exact_cap(3, p, u) - EX.cube_exponents(u)[2]
        f_sw = lambda u: sitewise_capacity(7, p, u)[0] - sitewise_capacity(6, p, u)[0] - EX.cube_exponents(u)[2]
        r_exact = root(f_exact, 1.0, 3.0)
        r_sw = root(f_sw, 1.0, 3.0)
        crossing.append(dict(p=p_str, increment_exact_L3_to_L4=None if r_exact is None else round(r_exact, 3),
                             increment_sitewise_L6_to_L7=None if r_sw is None else round(r_sw, 3)))
        print("crossing of the increment with the cube:", crossing[-1], flush=True)
    out = dict(Lmax=args.Lmax, note="floating point; lower = I(M) for explicit weights on the 2^L site-wise labels", cells=cells,
               increment_crossings=crossing, seconds_total=round(time.time() - t_all, 1))
    (RES / "sitewise.json").write_text(json.dumps(out, indent=1) + "\n")
    print("wrote", (RES / "sitewise.json").relative_to(ROOT))


if __name__ == "__main__":
    main()
