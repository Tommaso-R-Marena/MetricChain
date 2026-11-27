#!/usr/bin/env python3
"""Checks for docs/ensemble/ENSEMBLE_REPORT.md, section 4c.4, Proposition E20e: thirteen states on a torus of four
angles, multilinear data (the 81 means of products of 1, cos, sin of the four angles).

The lifted certificate of K = 13 states vanishes on a real curve Z = {g_1 = g_2 = g_3 = 0} through them.  A function
of the data span that is non-negative and vanishes at the states has value zero and derivative zero along Z at each
state (26 linear conditions).  On Z the 81 functions span 36; so the candidates form a space of dimension 10 modulo
the functions that vanish on Z, and whether one of them is positive on Z away from the states (with positive second
derivative at the states) is a linear programme over a traced sample of Z.

  * If the programme finds one (q), the function f = A (g_1^2 + g_2^2 + g_3^2) + q + i, with i vanishing on Z and
    chosen so that the gradient of q + i vanishes at the states, is checked to be non-negative on the whole torus
    with the thirteen states as its only zeros (grid of 24^4 points, local refinements, Hessians at the states):
    then every ensemble on the thirteen states is determined.
  * If it finds none, the dual solution is reported (the zero functional as a strictly positive combination of the
    evaluation functionals: its margin) together with a second measure on the curve with the same 81 data and no
    mass on the states: the ensemble is not determined.

Default run (part of run_all.py): two instances, one of each kind.
    python3 torus_four_angles.py --survey A B     analyses the seeds A..B-1 and prints one line each and a tally
(not part of run_all.py; its output is stored in output_threshold.txt).
"""
import itertools
import sys

import numpy as np
from scipy.optimize import linprog, minimize

R4 = 4
K13 = 13
BASIS = np.array(list(itertools.product(range(3), repeat=R4)))          # 81 index vectors
ok = True


def check(name, cond):
    global ok
    ok &= bool(cond)
    print(f"  {name}: {'ok' if cond else 'FAILED'}")


def half(p):
    return np.array([np.cos(p / 2), np.sin(p / 2)])


def dhalf(p):
    return 0.5 * np.array([-np.sin(p / 2), np.cos(p / 2)])


def w(phi):
    v = np.array([1.0])
    for p in phi:
        v = np.kron(v, half(p))
    return v


def dw(phi, k):
    v = np.array([1.0])
    for j, p in enumerate(phi):
        v = np.kron(v, dhalf(p) if j == k else half(p))
    return v


def F(phi):
    tab = np.array([[1.0, np.cos(p), np.sin(p)] for p in phi])
    return np.prod(tab[np.arange(R4)[None, :], BASIS], axis=1)


def dF(phi):
    tab = np.array([[1.0, np.cos(p), np.sin(p)] for p in phi])
    dtab = np.array([[0.0, -np.sin(p), np.cos(p)] for p in phi])
    out = np.zeros((R4, len(BASIS)))
    for a in range(R4):
        t2 = tab.copy()
        t2[a] = dtab[a]
        out[a] = np.prod(t2[np.arange(R4)[None, :], BASIS], axis=1)
    return out


def wrap(d):
    return (d + np.pi) % (2 * np.pi) - np.pi


def gval(N, phi):
    return N @ w(phi)


def gjac(N, phi):
    return np.array([[N[j] @ dw(phi, k) for k in range(R4)] for j in range(N.shape[0])])


def tangent(N, phi):
    tv = np.linalg.svd(gjac(N, phi))[2][-1]
    return tv / np.linalg.norm(tv)


def project(N, phi):
    for _ in range(50):
        res = gval(N, phi)
        if np.linalg.norm(res) < 1e-13:
            break
        phi = phi - np.linalg.lstsq(gjac(N, phi), res, rcond=None)[0]
    return phi


def trace(N, start, h=0.02, maxsteps=20000):
    pts = [start.copy()]
    phi = start.copy()
    tprev = tangent(N, phi)
    for step in range(maxsteps):
        tv = tangent(N, phi)
        if tv @ tprev < 0:
            tv = -tv
        phi = project(N, phi + h * tv)
        tprev = tv
        pts.append(phi.copy())
        if step > 10 and np.linalg.norm(wrap(phi - start)) < 0.8 * h:
            return np.array(pts), True
    return np.array(pts), False


def second_derivative_rows(N, P, h=2e-3):
    rows = []
    for p in P:
        tau = tangent(N, p)
        a, b = project(N, p + h * tau), project(N, p - h * tau)
        rows.append((F(a) + F(b) - 2 * F(p)) / h ** 2)
    return np.array(rows)


def grid_values(coef, n=24):
    g = np.linspace(-np.pi, np.pi, n + 1)[:-1]
    tab = np.stack([np.ones(n), np.cos(g), np.sin(g)], axis=1)
    vals = np.einsum("abcd,ia,jb,kc,ld->ijkl", coef.reshape(3, 3, 3, 3), tab, tab, tab, tab)
    return vals, g


def analyse(seed, nstarts=200):
    rng = np.random.default_rng(seed)
    P = rng.uniform(-np.pi, np.pi, size=(K13, R4))
    N = np.linalg.svd(np.array([w(p) for p in P]))[2][K13:]              # three multilinear forms g_j = N_j . w
    comps, closed = [], True

    def known(pt):
        return any(np.min(np.linalg.norm(wrap(c - pt), axis=1)) < 0.05 for c in comps)

    for st in [p for p in P] + [project(N, rng.uniform(-np.pi, np.pi, R4)) for _ in range(nstarts)]:
        if np.linalg.norm(gval(N, st)) > 1e-9 or known(st):
            continue
        c, cl = trace(N, st)
        closed &= cl
        comps.append(c)
    pts = np.vstack(comps)
    dist = np.array([min(np.linalg.norm(wrap(pt - p)) for p in P) for pt in pts])
    Fz = np.array([F(pt) for pt in pts])
    sv = np.linalg.svd(Fz, compute_uv=False)
    dimR = int(np.sum(sv > 1e-8 * sv[0]))
    Rb = np.linalg.svd(Fz)[2][:dimR].T                                   # the data span on Z, modulo what vanishes on Z
    rows = []
    for p in P:
        rows.append(F(p))
        rows.append(tangent(N, p) @ dF(p))
    M = np.array(rows) @ Rb
    svM = np.linalg.svd(M, compute_uv=False)
    rankM = int(np.sum(svM > 1e-8 * svM[0]))
    cand = Rb @ np.linalg.svd(M)[2][rankM:].T
    nc = cand.shape[1]
    d2 = second_derivative_rows(N, P) @ cand
    far = dist > 0.15
    A_ub = np.vstack([-np.hstack([Fz[far] @ cand, -np.ones((far.sum(), 1))]), -np.hstack([d2, -np.ones((K13, 1))])])
    res = linprog(np.concatenate([np.zeros(nc), [-1.0]]), A_ub=A_ub, b_ub=np.zeros(A_ub.shape[0]),
                  bounds=[(-1, 1)] * nc + [(None, None)], method="highs")
    out = dict(seed=seed, components=len(comps), closed=closed, dimR=dimR, rank=rankM, candidates=nc,
               t=(-res.fun if res.status == 0 else float("nan")))
    if out["t"] > 1e-5:
        q = cand @ res.x[:-1]
        qz = Fz @ q
        rs = np.random.default_rng(999)
        smp = rs.uniform(-np.pi, np.pi, size=(600, R4))
        Fs = np.array([F(s) for s in smp])

        def coeffs(fun):
            return np.linalg.lstsq(Fs, np.array([fun(s) for s in smp]), rcond=None)[0]

        Lc = coeffs(lambda s: np.sum(gval(N, s) ** 2))
        rws, rhs = [], []
        for p in P:
            ab = np.linalg.lstsq(gjac(N, p).T, dF(p) @ q, rcond=None)[0]
            for j in range(3):
                row = np.zeros(48)
                row[16 * j:16 * (j + 1)] = w(p)
                rws.append(row)
                rhs.append(-ab[j])
        ell = np.linalg.lstsq(np.array(rws), np.array(rhs), rcond=None)[0]
        ic = coeffs(lambda s: sum((ell[16 * j:16 * (j + 1)] @ w(s)) * gval(N, s)[j] for j in range(3)))
        hfun = q + ic
        out.update(q_min_on_curve=float(qz.min()), q_min_far=float(qz[far].min()),
                   gradient_at_states=float(max(np.linalg.norm(dF(p) @ hfun) for p in P)), certificate=None)
        for A in (1e3, 1e4, 1e5, 1e6, 1e7):
            fc = A * Lc + hfun
            vals, g = grid_values(fc)
            fmin, away = float(vals.min()), np.inf
            for i in np.argsort(vals, axis=None)[:40]:
                x0 = np.array([g[k] for k in np.unravel_index(i, vals.shape)])
                rr = minimize(lambda s: F(s) @ fc, x0, jac=lambda s: dF(s) @ fc, method="BFGS", options={"gtol": 1e-11})
                fmin = min(fmin, rr.fun)
                if min(np.linalg.norm(wrap(rr.x - p)) for p in P) > 1e-3:
                    away = min(away, rr.fun)
            eig = []
            for p in P:
                H = np.zeros((R4, R4))
                for a in range(R4):
                    e = np.zeros(R4)
                    e[a] = 1e-4
                    H[:, a] = (dF(p + e) @ fc - dF(p - e) @ fc) / 2e-4
                eig.append(np.linalg.eigvalsh((H + H.T) / 2)[0])
            # values of size A are computed with a rounding error of order 1e-16 A times the number of terms
            if fmin > -1e-11 * A and min(eig) > 1e-6 and (not np.isfinite(away) or away > 1e-12 * A + 1e-9):
                out["certificate"] = dict(A=A, minimum=fmin, hessian=float(min(eig)), away=float(away))
                break
        out["verdict"] = "IDENTIFIED" if out["certificate"] else "UNDECIDED (a candidate on the curve; torus check failed)"
    else:
        Efun = np.vstack([Fz[far][::4] @ cand, d2])
        n = Efun.shape[0]
        c = np.concatenate([np.zeros(n), [-1.0]])
        A_eq = np.vstack([np.hstack([Efun.T, np.zeros((nc, 1))]), np.concatenate([np.ones(n), [0.0]])[None, :]])
        b_eq = np.concatenate([np.zeros(nc), [1.0]])
        A_ub2 = np.hstack([-np.eye(n), np.ones((n, 1)) / n])
        rs2 = linprog(c, A_ub=A_ub2, b_ub=np.zeros(n), A_eq=A_eq, b_eq=b_eq,
                      bounds=[(0, None)] * n + [(None, None)], method="highs")
        margin = -rs2.fun if rs2.status == 0 else float("nan")
        sel = pts[dist > 0.05][::3]
        cols = np.array([F(z) for z in sel] + [F(p) for p in P]).T
        y = np.mean([F(p) for p in P], axis=0)
        rt = linprog(np.concatenate([np.zeros(len(sel)), np.ones(K13)]), A_eq=cols, b_eq=y,
                     bounds=[(0, None)] * cols.shape[1], method="highs")
        least = rt.fun if rt.status == 0 else float("nan")
        out.update(dual_margin=float(margin), least_mass_on_states=float(least))
        out["verdict"] = "NOT IDENTIFIED" if (margin > 1e-6 and least < 1 - 1e-6) else "UNDECIDED (no candidate; no twin found)"
    return out


def line(o):
    head = (f"seed {o['seed']}: real components of the curve {o['components']}; functions on the curve {o['dimR']};"
            f" rank of the 26 conditions {o['rank']}; candidates {o['candidates']}; ")
    if o["verdict"] == "IDENTIFIED":
        c = o["certificate"]
        return head + (f"IDENTIFIED: a candidate with minimum {o['q_min_far']:.4f} on the curve at distance > 0.15 from the"
                       f" states; certificate with A = {c['A']:.0e}: smallest Hessian eigenvalue at the states"
                       f" {c['hessian']:.4f}, smallest local minimum away from the states {c['away']:.4f}")
    if o["verdict"] == "NOT IDENTIFIED":
        return head + (f"NOT IDENTIFIED: no candidate is positive on the curve (dual margin {o['dual_margin']:.4f});"
                       f" a twin on the curve with least mass {o['least_mass_on_states']:.6f} on the states")
    return head + o["verdict"]


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--survey":
        a, b = int(sys.argv[2]), int(sys.argv[3])
        tally = {}
        for seed in range(a, b):
            o = analyse(seed)
            tally[o["verdict"]] = tally.get(o["verdict"], 0) + 1
            print(line(o), flush=True)
        print(f"thirteen random states on T^4, seeds {a}..{b - 1}: " + "; ".join(f"{k}: {v}" for k, v in sorted(tally.items())))
        sys.exit(0)
    print("T1  thirteen random states on T^4 that are not determined (Proposition E20e (b))")
    o = analyse(0)
    print("    " + line(o))
    check("the curve carries 36 functions of the data span, the 26 conditions are independent, 10 candidates remain",
          o["dimR"] == 36 and o["rank"] == 26 and o["candidates"] == 10 and o["closed"])
    check("no candidate is positive on the curve, with a positive dual margin, and a twin exists",
          o["verdict"] == "NOT IDENTIFIED" and o["dual_margin"] > 1e-3 and o["least_mass_on_states"] < 1e-6)
    print("T2  thirteen random states on T^4 that are determined (Proposition E20e (a))")
    o = analyse(1)
    print("    " + line(o))
    check("36 functions, 26 independent conditions, 10 candidates", o["dimR"] == 36 and o["rank"] == 26
          and o["candidates"] == 10 and o["closed"])
    check("a candidate positive on the curve, and a certificate that is non-negative on the torus with non-degenerate"
          " zeros at the thirteen states and no other zero found",
          o["verdict"] == "IDENTIFIED" and o["q_min_far"] > 1e-4 and o["q_min_on_curve"] > -1e-9
          and o["gradient_at_states"] < 1e-9 and o["certificate"]["hessian"] > 1e-3)
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)
