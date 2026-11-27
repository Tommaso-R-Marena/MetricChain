#!/usr/bin/env python3
"""ER4 (internal AI review) -- the paragraph "What survives the displacement" after Proposition E20c
(report b654396, lines 2251-2260).  Own code.

Claim: for a six-tuple at distance eps from a special one, "all its twins are concentrated within O(sqrt(eps)) of
its own states".  What the argument gives is a bound on the second moment,  int min_k d(x, p_k)^2 dnu = O(eps).
Test: take the special six-tuple of the report's check S4 (recomputed here), displace its sixth state by eps, and
solve, over all measures on the (sampled) curve Z_eps of the displaced six-tuple with the 27 data of the uniform
ensemble on the displaced states (every twin lives on Z_eps: g_1^2 + g_2^2 is in the span and has mean zero):
   LP1  maximise  int min_k d(x, p_k)^2 dnu                       (second moment of the distance to the states)
   LP2  maximise  nu{ x : min_k d(x, p_k) > 0.5 }                 (mass far away from every state)
   LP3  for the curve point farthest from all states: the largest mass a twin can put within 0.05 of it.
If the twins were SUPPORTED within O(sqrt(eps)) of the states, LP2 and LP3 would be zero for small eps.
"""
import sys

import numpy as np
from scipy.optimize import linprog

from er4_torus import (Fmat, I0_basis, curve_components, lift, null2, project, refine_loop, tangent, torus_dist,
                       wrap, Rmatrix)
from er4_e20c_special import special_positions


def special_tuple():
    P0 = np.random.default_rng(2).uniform(-np.pi, np.pi, size=(6, 3))
    N, _ = null2(P0)
    loops = [refine_loop(N, c, hmax=0.01) for c in curve_components(N, M=4000)]
    I0, Bc, _ = I0_basis(N)
    for ci, p in special_positions(N, Bc, P0[:5], loops):
        P = np.vstack([P0[:5], p])
        if np.linalg.svd(np.array([lift(q) for q in P]), compute_uv=False)[-1] > 1e-3:
            return P
    raise RuntimeError("no special six-tuple found")


def twins_lp(P, hmax=0.006, M=5000):
    N, s = null2(P)
    loops = [refine_loop(N, c, hmax=hmax) for c in curve_components(N, M=M)]
    pts = np.vstack(loops)
    # extra sample points on the curve close to every state (arc lengths 1e-6 ... 1e-1 on both sides): the twins of a
    # slightly displaced six-tuple carry most of their mass there
    extra = []
    for p in P:
        t, _ = tangent(N, p)
        for sarc in np.logspace(-6, -1, 150):
            for sgn in (1.0, -1.0):
                extra.append(wrap(project(N, p + sgn * sarc * t)))
    pts = np.vstack([pts, np.array(extra)])
    d = torus_dist(pts, P)
    keep = d > 5e-7
    pts, d = pts[keep], d[keep]
    cols = np.vstack([Fmat(pts), Fmat(P)]).T
    y = Fmat(P).mean(0)
    n = cols.shape[1]
    bounds = [(0, None)] * n
    out = {"npts": len(pts), "sv12": np.linalg.svd(Rmatrix(N, P), compute_uv=False)[11]}
    # LP1
    c1 = -np.concatenate([d ** 2, np.zeros(6)])
    r1 = linprog(c1, A_eq=cols, b_eq=y, bounds=bounds, method="highs")
    out["M2"] = -r1.fun if r1.status == 0 else np.nan
    if r1.status == 0:
        w = r1.x[:len(pts)]
        out["mass_off_states_LP1"] = w.sum()
        out["support_max_dist_LP1"] = d[w > 1e-9].max() if (w > 1e-9).any() else 0.0
    # LP2
    c2 = -np.concatenate([(d > 0.5).astype(float), np.zeros(6)])
    r2 = linprog(c2, A_eq=cols, b_eq=y, bounds=bounds, method="highs")
    out["far_mass"] = -r2.fun if r2.status == 0 else np.nan
    # LP3
    i0 = int(np.argmax(d))
    near = np.linalg.norm(wrap(pts - pts[i0]), axis=1) < 0.05
    c3 = -np.concatenate([near.astype(float), np.zeros(6)])
    r3 = linprog(c3, A_eq=cols, b_eq=y, bounds=bounds, method="highs")
    out["mass_at_farthest"] = -r3.fun if r3.status == 0 else np.nan
    out["farthest_dist"] = d[i0]
    # least mass on the states (is the displaced ensemble determined on the sample?)
    c4 = np.concatenate([np.zeros(len(pts)), np.ones(6)])
    r4 = linprog(c4, A_eq=cols, b_eq=y, bounds=bounds, method="highs")
    out["least_mass_states"] = r4.fun if r4.status == 0 else np.nan
    return out


def main():
    Ps = special_tuple()
    print("special six-tuple (recomputed): sixth state", ", ".join(f"{x:.6f}" for x in Ps[5]))
    o = twins_lp(Ps)
    print(f"eps = 0 (the special six-tuple): smallest singular value of (R) {o['sv12']:.1e}; curve points {o['npts']}; "
          f"largest second moment over twins {o['M2']:.2e}; least mass on the states {o['least_mass_states']:.6f}")
    rng = np.random.default_rng(99)
    dirs = rng.normal(size=(3, 3))
    dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
    print("displacement of the sixth state by eps in a random direction (three directions per eps)")
    print("   eps      sv12(R)   max int min d^2 dnu   (that)/eps   sqrt(that)   far mass (d > 0.5)  far mass/eps   "
          "mass within 0.05 of the farthest curve point (its distance)   least mass on states")
    for eps in (1e-1, 3e-2, 1e-2, 3e-3):          # below 3e-3 the masses (of order eps^2) reach the LP tolerances
        for u in dirs:
            P = Ps.copy()
            P[5] = P[5] + eps * u
            o = twins_lp(P)
            print(f"   {eps:7.0e}  {o['sv12']:.2e}   {o['M2']:.4e}          {o['M2'] / eps:8.4f}    {np.sqrt(max(o['M2'], 0.0)):.4f}       "
                  f"{o['far_mass']:.4e}       {o['far_mass'] / eps:8.4f}      {o['mass_at_farthest']:.3e} "
                  f"({o['farthest_dist']:.2f})                                   {o['least_mass_states']:.6f}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
