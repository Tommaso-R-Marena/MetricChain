#!/usr/bin/env python3
"""ER3 review, the torus row of the table of section 4c.5 ("identified up to: not known; not identified beyond: not
known (a count of double-point conditions suggests (3^r - 1)/(r+1))").  Reviewer's own code; numerical evidence.

Principle used: every measure with the data of an ensemble on S is carried by the zero set Z_S of the projector
certificate.  When Z_S is finite, identification is a finite linear-algebra question; when Z_S is a curve, it is
a linear programme over measures on the curve (one-dimensional, so a fine discretisation is adequate; unlike a
product grid of the torus it contains the candidate twins).

A.  r = 3, K = 6 generic states: Z_S is a real curve.  LP over measures on ~12000 points of the curve: largest mass
    off the six states with the same 26 data.  (If positive: generic six-state ensembles on the 3-torus are not
    identified, so the identified range for three angles is exactly K <= 5 = 2^r - r.)
    Also the number of linearly independent functions of the span on the curve (expected 12: sections of a line
    bundle of degree 12 on a curve of genus 1), against 2K = 12 conditions for six double zeros.
B.  r = 4, K = 12 (= 2^r - r) when all 24 solutions lie on the torus (about 5 % of random instances): the 24
    rank-one matrices satisfy one linear relation (Euler-Jacobi).  The ensemble on the 12 states is identified iff
    no relation has non-negative coefficients on the 12 extra zeros; decided from the relation.
C.  r = 4, K = 13: Z_S is a curve; the same LP as in A.
"""
import itertools, sys
import numpy as np
from scipy.optimize import linprog
import er3_e20_torus as T

rng = np.random.default_rng(31106)
TWO_PI = 2 * np.pi


def real_features(Z):
    """All products of (1, cos, sin) over the angles: real and imaginary parts of the monomials z^m, m in {-1,0,1}^r,
    one of each conjugate pair."""
    r = Z.shape[1]; cols = [np.ones(len(Z))]
    seen = set()
    for m in itertools.product((-1, 0, 1), repeat=r):
        if m == (0,) * r or tuple(-x for x in m) in seen:
            continue
        seen.add(m)
        mono = np.prod(Z ** np.array(m), axis=1)
        cols += [mono.real, mono.imag]
    return np.array(cols)                                    # 3^r x N


def curve_points_r3(C, n3):
    """Torus zeros of the two equations C v(z) = 0 (C: 2 x 8) for z3 on a grid of the unit circle."""
    A, B = C[:, :4], C[:, 4:]; pts = []
    q = lambda w: w[0] * w[3] - w[1] * w[2]
    for t in np.exp(2j * np.pi * (np.arange(n3) + 0.5) / n3):
        _, _, Vh = np.linalg.svd(A + t * B); N2 = Vh[2:].conj().T
        n0, n1 = N2[:, 0], N2[:, 1]
        qa, qc = q(n0), q(n1); qb = q(n0 + n1) - qa - qc
        for s_ in np.roots([qa, qb, qc]):
            w = s_ * n0 + n1
            z = np.array([w[1] / w[0], w[2] / w[0], t])
            if T.on_torus(z, 1e-7):
                pts.append(z / np.abs(z))
    return np.array(pts)


def lp_on_curve(Zc, Zs, w, delta):
    """Largest mass at angular distance > delta from every state, over measures on the curve points Zc and the states
    Zs, with exactly the data of sum w_i delta_{Zs_i}."""
    Z = np.vstack([Zc, Zs]); F = real_features(Z)
    mu = np.zeros(len(Z)); mu[len(Zc):] = w
    d = np.min(np.abs(np.angle(Z[:, None, :] / Zs[None, :, :])).max(axis=2), axis=1)
    c = -(d > delta).astype(float)
    res = linprog(c, A_eq=F, b_eq=F @ mu, bounds=[(0, None)] * len(Z), method="highs")
    rank = np.linalg.matrix_rank(F[:, : len(Zc)].T, tol=1e-8)
    return -res.fun, np.abs(F @ res.x - F @ mu).max(), rank, res.status


def part_A(n=10):
    print("A. three angles, six generic states: measures on the zero curve of the projector certificate")
    out = []
    for it in range(n):
        P = rng.uniform(0, TWO_PI, size=(6, 3)); C = T.complement(P)
        Zc = curve_points_r3(C, 6000)
        val, resid, rank, status = lp_on_curve(Zc, np.exp(1j * P), rng.dirichlet(2 * np.ones(6)), 0.05)
        out.append((len(Zc), val, resid, rank, status))
        print(f"   instance {it + 1}: {len(Zc)} points on the curve; dimension of the span of the 27 products on the curve: "
              f"{rank}; largest mass farther than 0.05 from the six states with the same data: {val:.3f} "
              f"(residual {resid:.1e}, LP status {status})", flush=True)
    return out


def part_B(target=5, max_instances=110):
    print("B. four angles, twelve states, instances in which all 24 solutions lie on the torus")
    found = tried = 0
    while found < target and tried < max_instances:
        tried += 1
        P = rng.uniform(0, TWO_PI, size=(12, 4)); C = T.complement(P)
        sols = T.newton_all_solutions(C, 4, seed=5000 + tried)
        if len(sols) != 24 or not all(T.on_torus(s, 1e-6) for s in sols):
            continue
        found += 1
        given = np.exp(1j * P)
        isS = np.array([np.abs(s[None, :] - given).max(axis=1).min() < 1e-6 for s in sols])
        V = T.lift(sols)
        mats = np.array([np.outer(v, v.conj()).ravel() for v in V])
        M = np.hstack([mats.real, mats.imag])                # 24 x 512, rows = Hermitian matrices
        U, sv, Vt = np.linalg.svd(M.T, full_matrices=False)  # relations: M^T h = 0
        h = Vt[-1]
        null_dim = int((sv < 1e-9 * sv[0]).sum())
        hx = h[~isS]
        same_sign = bool(np.all(hx > 1e-9) or np.all(hx < -1e-9))
        # direct LP on the 24 points: largest mass off the 12 states with the same data
        F = real_features(sols); mu = np.zeros(24); mu[isS] = rng.dirichlet(2 * np.ones(12))
        res = linprog(-(~isS).astype(float), A_eq=F, b_eq=F @ mu, bounds=[(0, None)] * 24, method="highs")
        print(f"   instance {found} (after {tried} tries): relations among the 24 rank-one matrices: {null_dim}; "
              f"coefficients on the 12 extra zeros: {int((hx > 0).sum())} positive, {int((hx < 0).sum())} negative "
              f"-> a twin exists: {same_sign}; LP on the 24 zeros, largest mass off the states: {-res.fun:.2e}", flush=True)
    print(f"   ({found} such instances in {tried} tries)")


def curve_points_r4(C, n4):
    pts = []
    for t in np.exp(2j * np.pi * (np.arange(n4) + 0.5) / n4):
        C3 = C[:, :8] + t * C[:, 8:]
        try:
            sols = T.solve_r3_K5(C3)
        except Exception:
            continue
        for s in sols:
            if T.on_torus(s, 1e-6) and np.abs(C3 @ T.lift(s)[0]).max() < 1e-8:
                z = np.append(s, t); pts.append(z / np.abs(z))
    return np.array(pts)


def part_C(n=4):
    print("C. four angles, thirteen generic states: measures on the zero curve of the projector certificate")
    for it in range(n):
        P = rng.uniform(0, TWO_PI, size=(13, 4)); C = T.complement(P)
        Zc = curve_points_r4(C, 2500)
        val, resid, rank, status = lp_on_curve(Zc, np.exp(1j * P), rng.dirichlet(2 * np.ones(13)), 0.05)
        print(f"   instance {it + 1}: {len(Zc)} points on the curve; dimension of the span of the 81 products on the curve: "
              f"{rank}; largest mass farther than 0.05 from the thirteen states with the same data: {val:.2e} "
              f"(residual {resid:.1e}, LP status {status})", flush=True)


def part_C_tolerance(n=4):
    """The instances of part C again (same random stream).  Where the LP with exact data finds no twin on the
    discretised curve, is that an artefact of the discretisation?  Allow the data to differ by tau: if the largest
    mass far from the states stays of order tau the absence of a twin is robust; if it jumps to order one it was
    an artefact."""
    print("C'. the instances of C with data matched up to tau (l_inf), mass farther than 0.05 from the states")
    for it in range(n):
        P = rng.uniform(0, TWO_PI, size=(13, 4)); C = T.complement(P)
        Zc = curve_points_r4(C, 2500); Zs = np.exp(1j * P)
        w = rng.dirichlet(2 * np.ones(13))
        Z = np.vstack([Zc, Zs]); F = real_features(Z)
        mu = np.zeros(len(Z)); mu[len(Zc):] = w
        d = np.min(np.abs(np.angle(Z[:, None, :] / Zs[None, :, :])).max(axis=2), axis=1)
        c = -(d > 0.05).astype(float); y = F @ mu
        vals = []
        for tau in (0.0, 1e-8, 1e-6, 1e-4, 1e-2):
            A_ub = np.vstack([F[1:], -F[1:]]); b_ub = np.concatenate([y[1:] + tau, -(y[1:] - tau)])
            res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=F[:1], b_eq=y[:1], bounds=[(0, None)] * len(Z), method="highs")
            vals.append(-res.fun if res.status == 0 else float("nan"))
        print(f"   instance {it + 1}: " + ", ".join(f"tau = {t:g}: {v:.2e}" for t, v in zip((0.0, 1e-8, 1e-6, 1e-4, 1e-2), vals)), flush=True)


if __name__ == "__main__":
    part = sys.argv[1] if len(sys.argv) > 1 else "A"
    if part == "A":
        part_A()
    elif part == "B":
        part_B()
    elif part == "C":
        part_C()
    else:
        part_C_tolerance()
