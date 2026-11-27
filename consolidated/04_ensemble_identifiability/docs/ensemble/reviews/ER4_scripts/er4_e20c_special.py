#!/usr/bin/env python3
"""ER4 (internal AI review) -- Proposition E20c and the paragraph "Where the special six-tuples are".
Own code (er4_torus.py); nothing imported from experiments/ensemble/.

For a six-tuple P (five fixed states and a sixth that moves on the curve Z through all six):
  1. all real components of Z (double cover over phi_3; no continuation);
  2. D(p) = det( R(P_1..P_5, p) restricted to a complement of I_0 ) along every component; its sign changes are
     the positions of the sixth state at which the twelve conditions drop rank (simple zeros);
  3. each such position is classified: lifts dependent (the sixth zero of the lifted certificate of the five) or
     independent (a "special six-tuple" of E20c);
  4. at a special six-tuple: singular values of (R); q_0; its range on every real component; number of states per
     component; second derivative along the curve at the states; case (a) / (b) / neither;
  5. a linear programme over measures on the sampled curve: least mass on the six states among measures with the
     same 27 data;
  6. in case (a): the certificate f_A = A (g_1^2 + g_2^2) + q_0 + i of the report with the least-norm i, its Hessians,
     the smallest A for which a minimisation over the normal planes all along the curve finds no negative value,
     and a global search for negative values of f_A:
       - a grid of G^3 points,
       - local minimisation (BFGS, analytic gradient) from the lowest grid points, from random points, and from
         points displaced off the curve all along the curve (the place where a thin negative tube would hide).

Usage: er4_e20c_special.py  [which]      which in {author_S4, author_S4b, own}
"""
import sys
import time

import numpy as np
from scipy.optimize import brentq, linprog, minimize

from er4_torus import (Fmat, Fvec, I0_basis, Rmatrix, curve_components, dFmat, ddFvec, gjac, gval, lift, null2,
                       prod_coeffs, project, refine_loop, tangent, torus_dist, wrap)


def D_along(N, Bc, P5, loop):
    """determinant of the 12 conditions (restricted to the complement of I_0) with the sixth state at each loop point"""
    base = Rmatrix(N, P5) @ Bc                    # 10 x 12
    Fl = Fmat(loop) @ Bc
    dFl = dFmat(loop)
    out = np.empty(len(loop))
    for i, p in enumerate(loop):
        t, _ = tangent(N, p)
        M = np.vstack([base, Fl[i], (t @ dFl[i]) @ Bc])
        out[i] = np.linalg.det(M)
    return out


def D_point(N, Bc, base, p):
    t, _ = tangent(N, p)
    M = np.vstack([base, Fvec(p) @ Bc, (t @ dFmat(p[None, :])[0]) @ Bc])
    return np.linalg.det(M)


def special_positions(N, Bc, P5, loops):
    """sign changes of D along every loop, refined"""
    base = Rmatrix(N, P5) @ Bc
    found = []
    for ci, loop in enumerate(loops):
        Dv = D_along(N, Bc, P5, loop)
        n = len(loop)
        near = torus_dist(loop, P5) < 4e-3          # D has a zero of order four where the sixth state meets another
        for i in range(n):                           # state: no sign change there, only rounding noise
            j = (i + 1) % n
            if near[i] or near[j]:
                continue
            if Dv[i] == 0.0 or Dv[i] * Dv[j] < 0:
                a, d = loop[i], wrap(loop[j] - loop[i])
                fun = lambda s: D_point(N, Bc, base, project(N, a + s * d))
                try:
                    s0 = brentq(fun, 0.0, 1.0, xtol=1e-15, rtol=1e-15, maxiter=200)
                except ValueError:
                    continue
                found.append((ci, wrap(project(N, a + s0 * d))))
    return found


def analyse_special(N, P, loops, label, do_cert=True, A=100.0, grid=96, verbose=True, rng=None):
    """P: six states with rank-11 conditions.  Returns a dict."""
    out = {}
    I0, Bc, _ = I0_basis(N)
    R = Rmatrix(N, P)
    sv = np.linalg.svd(R, compute_uv=False)
    out["sv11"], out["sv12"] = sv[10], sv[11]
    lifts_sv = np.linalg.svd(np.array([lift(p) for p in P]), compute_uv=False)
    out["lift_sv6"] = lifts_sv[-1]
    RB = R @ Bc
    q0 = Bc @ np.linalg.svd(RB)[2][-1]            # unit vector, orthogonal to I_0
    allpts = np.vstack(loops)
    vals = Fmat(allpts) @ q0
    q0 = q0 * np.sign(vals.sum())
    comp_of_state = [int(np.argmin([np.min(np.linalg.norm(wrap(c - p), axis=1)) for c in loops])) for p in P]
    out["states_per_component"] = [comp_of_state.count(ci) for ci in range(len(loops))]
    ranges = []
    for c in loops:
        v = Fmat(c) @ q0
        ranges.append((v.min(), v.max()))
    out["ranges"] = ranges
    tol = 1e-9
    signs = []
    for lo, hi in ranges:
        signs.append(1 if lo > -tol else (-1 if hi < tol else 0))     # +1: >= 0, -1: <= 0, 0: both signs
    out["signs"] = signs
    dist = torus_dist(allpts, P)
    vals = Fmat(allpts) @ q0
    out["q0_min_far"] = vals[dist > 0.1].min()
    out["q0_max"] = vals.max()
    out["q0_min"] = vals.min()
    # second derivative of q_0 along the curve at the states, through h = q_0 + i with grad h = 0 at the states
    rows, rhs = [], []
    for p in P:
        G = gjac(N, p)                                               # 2 x 3
        gq = dFmat(p[None, :])[0] @ q0                               # gradient of q_0 at p
        ab, res, _, _ = np.linalg.lstsq(G.T, gq, rcond=None)
        rows.append(np.concatenate([lift(p), np.zeros(8)]))
        rhs.append(-ab[0])
        rows.append(np.concatenate([np.zeros(8), lift(p)]))
        rhs.append(-ab[1])
    ell = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None)[0]
    ic = prod_coeffs(ell[:8], N[0]) + prod_coeffs(ell[8:], N[1])
    h = q0 + ic
    out["grad_h_states"] = max(np.linalg.norm(dFmat(p[None, :])[0] @ h) for p in P)
    d2 = []
    for p in P:
        t, _ = tangent(N, p)
        Hh = ddFvec(p) @ h
        d2.append(t @ Hh @ t)
    out["d2_states"] = d2
    if all(s == 1 for s in signs) and min(d2) > 1e-9 and out["q0_min_far"] > 0:
        case = "a"
    elif (0 in signs) or (1 in signs and -1 in signs):
        # both signs on Z overall?
        case = "b" if (vals.min() < -1e-7 and vals.max() > 1e-7) else "neither"
    else:
        case = "neither"
    out["case"] = case
    # linear programme: least mass on the states among measures on the sampled curve with the same data
    far = dist > 0.02
    sample = allpts[far][::2]
    cols = np.vstack([Fmat(sample), Fmat(P)]).T
    y = Fmat(P).mean(0)
    cost = np.concatenate([np.zeros(len(sample)), np.ones(6)])
    res = linprog(cost, A_eq=cols, b_eq=y, bounds=[(0, None)] * cols.shape[1], method="highs")
    out["lp_least_mass"] = res.fun if res.status == 0 else np.nan
    if verbose:
        print(f"  [{label}] singular values 11, 12 of (R): {sv[10]:.4f}, {sv[11]:.1e}; smallest singular value of the lifts "
              f"{lifts_sv[-1]:.4f}")
        print(f"      sixth state: {', '.join(f'{x:.6f}' for x in P[5])}")
        print(f"      real components: {len(loops)}; states per component: {out['states_per_component']}; range of q_0 on "
              f"each: {', '.join(f'[{lo:.2e}, {hi:.4f}]' for lo, hi in ranges)}")
        print(f"      q_0 on the curve: min {out['q0_min']:.2e}, min at distance > 0.1 from the states "
              f"{out['q0_min_far']:.4f}, max {out['q0_max']:.4f}; second derivatives along the curve at the states: "
              f"{', '.join(f'{x:.4f}' for x in d2)}")
        print(f"      case ({case}); least mass on the six states (LP over the sampled curve, {len(sample)} points): "
              f"{out['lp_least_mass']:.6f}")
    if not (do_cert and case == "a"):
        return out
    # ------------------------------------------------------------------ the certificate of E20c(a)
    Lc = prod_coeffs(N[0], N[0]) + prod_coeffs(N[1], N[1])
    if A == "auto":
        # the proposition says "A large": take 1.5 times the smallest A for which a minimisation over the normal
        # planes all along the curve finds no negative value
        a_min = minimal_A(N, P, loops, h, Lc, q0)
        out["A_min_tube"] = a_min
        A = 1.5 * a_min
        if verbose:
            print(f"      smallest A for which the normal-plane minimisation along the curve finds no negative value: "
                  f"{a_min:.3f}; the certificate is tested with A = {A:.3f}")
    fc = A * Lc + h
    eigs = [np.linalg.eigvalsh(ddFvec(p) @ fc)[0] for p in P]
    out["hess_min_eig"] = min(eigs)
    # smallest A for which all six Hessians are positive definite (bisection)
    def minhess(a):
        return min(np.linalg.eigvalsh(ddFvec(p) @ (a * Lc + h))[0] for p in P)
    lo_a, hi_a = 0.0, 1.0
    while minhess(hi_a) <= 0 and hi_a < 1e9:
        hi_a *= 2
    for _ in range(60):
        mid = 0.5 * (lo_a + hi_a)
        if minhess(mid) > 0:
            hi_a = mid
        else:
            lo_a = mid
    out["A_hess"] = hi_a
    # first-order requirement along the curve
    dFl = dFmat(allpts)
    gh = dFl @ h                                   # gradients of h at the curve points (n, 3)
    qv = Fmat(allpts) @ q0
    Areq = np.zeros(len(allpts))
    for i, p in enumerate(allpts):
        if dist[i] < 0.02:
            continue
        Jm = gjac(N, p)
        JTJp = np.linalg.pinv(Jm.T @ Jm)
        Areq[i] = gh[i] @ JTJp @ gh[i] / (4 * qv[i])
    out["A_req_first_order"] = Areq.max()
    out["A_req_where"] = allpts[np.argmax(Areq)]
    out["A_req_dist"] = dist[np.argmax(Areq)]

    def f(x):
        return Fvec(x) @ fc

    def df(x):
        return dFmat(np.asarray(x)[None, :])[0] @ fc

    # grid
    gr = -np.pi + 2 * np.pi * np.arange(grid) / grid
    v = np.stack([np.ones(grid), np.cos(gr), np.sin(gr)], axis=1)
    V0 = np.einsum("ai,bj,ck,ijk->abc", v, v, v, fc.reshape(3, 3, 3))
    out["grid_min"] = V0.min()
    flat = np.argsort(V0.ravel())[:400]
    starts = [np.array([gr[i // (grid * grid)], gr[(i // grid) % grid], gr[i % grid]]) for i in flat]
    rng = rng or np.random.default_rng(12345)
    starts += list(rng.uniform(-np.pi, np.pi, size=(1500, 3)))
    # points displaced off the curve, all along the curve
    step = max(1, len(allpts) // 1500)
    for p in allpts[::step]:
        Jm = gjac(N, p)
        for sgn in (1.0, -1.0):
            starts.append(p + sgn * 0.03 * Jm[0] / np.linalg.norm(Jm[0]))
        starts.append(p.copy())
    best, best_x = np.inf, None
    far_min, far_x = np.inf, None
    n_far = 0
    for x0 in starts:
        r = minimize(f, x0, jac=df, method="BFGS", options={"gtol": 1e-11})
        d = torus_dist(r.x[None, :], P)[0]
        if r.fun < best:
            best, best_x = r.fun, r.x
        if d > 1e-3:
            n_far += 1
            if r.fun < far_min:
                far_min, far_x = r.fun, r.x
    out["n_starts"] = len(starts)
    out["global_min"] = best
    out["far_min"] = far_min
    out["n_far"] = n_far
    out["far_x"] = far_x
    if verbose:
        print(f"      certificate f = {A:g} (g_1^2 + g_2^2) + h: |grad h| at the states {out['grad_h_states']:.1e}; smallest "
              f"Hessian eigenvalue of f at the states {out['hess_min_eig']:.4f}")
        print(f"      the six Hessians are positive definite from A = {out['A_hess']:.3f} on (a necessary condition on A)")
        print(f"      grid {grid}^3: minimum {out['grid_min']:.3e}; {len(starts)} local minimisations: lowest value "
              f"{best:.3e}; local minima at distance > 1e-3 from the states: {n_far}"
              + (f", lowest {far_min:.4e} at ({', '.join(f'{x:.4f}' for x in wrap(far_x))})" if n_far else ""))
    out["fc"], out["h"], out["Lc"], out["q0"] = fc, h, Lc, q0
    return out


def minimal_A(N, P, loops, h, Lc, q0, tol=1e-3):
    """smallest A (to relative accuracy tol) for which no negative value of f_A is found near the curve:
    for every sampled curve point, minimise f_A over the normal plane (2-dimensional BFGS from zero)."""
    allpts = np.vstack(loops)
    dist = torus_dist(allpts, P)
    step = max(1, len(allpts) // 800)
    pts = allpts[::step]

    def tube_min(a):
        fc = a * Lc + h
        worst = np.inf
        for p in pts:
            Jm = gjac(N, p)
            Q, _ = np.linalg.qr(Jm.T)             # 3 x 2 orthonormal basis of the normal plane
            fun = lambda c: Fvec(p + Q @ c) @ fc
            r = minimize(fun, np.zeros(2), method="BFGS", options={"gtol": 1e-10})
            worst = min(worst, r.fun)
        return worst

    lo, hi = 0.0, 1.0
    while tube_min(hi) < -1e-9 and hi < 1e7:
        lo, hi = hi, hi * 2
    while hi - lo > tol * hi:
        mid = 0.5 * (lo + hi)
        if tube_min(mid) < -1e-9:
            lo = mid
        else:
            hi = mid
    return hi


def run_instance(P0, label, do_cert=True, M=4000, hmax=0.01, A=100.0, compute_minA=False):
    t0 = time.time()
    N, s = null2(P0)
    loops = [refine_loop(N, c, hmax=hmax) for c in curve_components(N, M=M)]
    I0, Bc, _ = I0_basis(N)
    sv0 = np.linalg.svd(Rmatrix(N, P0), compute_uv=False)
    comp_of_state = [int(np.argmin([np.min(np.linalg.norm(wrap(c - p), axis=1)) for c in loops])) for p in P0]
    print(f"[{label}] starting six-tuple: smallest singular value of (R) {sv0[11]:.4f}; real components of the curve: "
          f"{len(loops)} ({', '.join(str(len(c)) for c in loops)} points); states per component: "
          f"{[comp_of_state.count(ci) for ci in range(len(loops))]}; the sixth state is on component {comp_of_state[5]}")
    pos = special_positions(N, Bc, P0[:5], loops)
    print(f"  positions of the sixth state at which the determinant of the twelve conditions changes sign: {len(pos)}")
    results = []
    for k, (ci, p) in enumerate(pos):
        P = np.vstack([P0[:5], p])
        lsv = np.linalg.svd(np.array([lift(q) for q in P]), compute_uv=False)[-1]
        if lsv < 1e-6:
            print(f"  [{label}/{k}] on component {ci}: the six lifts are dependent (smallest singular value {lsv:.1e}): "
                  f"the sixth zero of the lifted certificate of the five states, "
                  f"({', '.join(f'{x:.6f}' for x in p)})")
            results.append({"dependent": True, "component": ci})
            continue
        o = analyse_special(N, P, loops, f"{label}/{k}", do_cert=do_cert, A=A)
        o["dependent"] = False
        o["component"] = ci
        o["P"] = P
        if compute_minA and o["case"] == "a" and do_cert:
            amin = minimal_A(N, P, loops, o["h"], o["Lc"], o["q0"])
            o["A_min_tube"] = amin
            print(f"      smallest A for which the normal-plane minimisation along the curve finds no negative value: "
                  f"{amin:.3f}")
        results.append(o)
    print(f"  ({time.time() - t0:.0f} s)")
    return N, loops, results


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "author_S4"
    if which == "author_S4":
        # the starting six-tuple of the report's check S4 (numpy default_rng(2), uniform on (-pi, pi)^(6x3))
        P0 = np.random.default_rng(2).uniform(-np.pi, np.pi, size=(6, 3))
        run_instance(P0, "S4 start (seed 2)", compute_minA=True)
    elif which == "author_S4b":
        P0 = np.random.default_rng(0).uniform(-np.pi, np.pi, size=(6, 3))
        run_instance(P0, "S4b start (seed 0)", compute_minA=True)
    elif which == "own":
        # certificates (case (a)) for a few six-tuples of my own, with the global search
        for seed in (7001, 7002, 7004, 7005):
            P0 = np.random.default_rng(seed).uniform(-np.pi, np.pi, size=(6, 3))
            run_instance(P0, f"own seed {seed}", M=3000, hmax=0.015, compute_minA=False, A="auto")
    elif which == "stats":
        # statistics over random six-tuples: number of real components, number of special positions, cases
        import collections
        tally = collections.Counter()
        detail = []
        nseeds = int(sys.argv[2]) if len(sys.argv) > 2 else 40
        for seed in range(8000, 8000 + nseeds):
            P0 = np.random.default_rng(seed).uniform(-np.pi, np.pi, size=(6, 3))
            N, s = null2(P0)
            loops = [refine_loop(N, c, hmax=0.01) for c in curve_components(N, M=5000)]
            allp = np.vstack(loops)
            smooth = min(tangent(N, p)[1] for p in allp[::5])
            if smooth < 2e-3 or s[-1] < 1e-2:
                tally[("set aside: curve nearly singular or lifts nearly dependent",)] += 1
                print(f"  seed {seed}: set aside (min |grad g_1 x grad g_2| on the curve {smooth:.1e}, smallest singular "
                      f"value of the lifts {s[-1]:.1e})", flush=True)
                continue
            I0, Bc, _ = I0_basis(N)
            pos = special_positions(N, Bc, P0[:5], loops)
            ndep, cases, dep_comp, comps_of = 0, [], None, []
            for ci, p in pos:
                P = np.vstack([P0[:5], p])
                lsv = np.linalg.svd(np.array([lift(q) for q in P]), compute_uv=False)[-1]
                if lsv < 1e-6:
                    ndep += 1
                    dep_comp = ci
                    continue
                o = analyse_special(N, P, loops, "", do_cert=False, verbose=False)
                cases.append(o["case"])
                comps_of.append((ci, o["case"], o["lp_least_mass"], min(o["d2_states"]), o["sv11"], o["lift_sv6"]))
            key = (len(loops), len(pos), ndep, "".join(sorted(cases)))
            tally[key] += 1
            # consistency of the LP with the case (the LP leaves out curve points within 0.02 of a state: when the
            # special sixth state is that close to another state the LP is not conclusive and is not counted)
            lp_ok = all((c == "a") == (lm > 1 - 1e-6) for (_, c, lm, _, _, lsv6) in comps_of if lsv6 > 0.02)
            same = [c for (ci, c, _, _, _, _) in comps_of if ci == dep_comp]
            other = [c for (ci, c, _, _, _, _) in comps_of if ci != dep_comp]
            detail.append((seed, key, lp_ok, same, other))
            print(f"  seed {seed}: components {len(loops)}; sign changes {len(pos)}; dependent {ndep}; cases "
                  f"{[(ci, c, round(lm, 6)) for (ci, c, lm, _, _, _) in comps_of]}; LP agrees with the case: {lp_ok}; "
                  f"on the component of the dependent position: {same}; on the other: {other}", flush=True)
        print("tally (real components, sign changes of D, dependent positions, cases of the special positions):")
        for k, v in sorted(tally.items(), key=lambda kv: str(kv[0])):
            print("   ", k, v)
        pat = collections.Counter((d[1][0], tuple(sorted(d[3])), tuple(sorted(d[4]))) for d in detail)
        print("patterns (real components; cases on the component that carries the dependent position; cases on the other):")
        for k, v in sorted(pat.items(), key=lambda kv: -kv[1]):
            print("   ", k, v)
        print("LP agrees with the classification in all instances:", all(d[2] for d in detail))
    return 0


if __name__ == "__main__":
    sys.exit(main())
