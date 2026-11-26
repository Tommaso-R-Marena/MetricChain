#!/usr/bin/env python3
"""RA08 -- the exponent-level inequality inside Proposition Z3 of Z_REPORT, on the ENVELOPE curves, at finite d and
at accuracies from logarithmic to EXTENSIVE (what Theorem Z'' needs of Lemma A1 + Lemma Z1a + the discretisation of phi):

    min over 1 <= n_o <= d - d_min + 1  of   Pi_j(n_o) := max_{(B, sigma) in L_j} [ (d - n_o) B + (1 - sigma) n_o theta_na(y/n_o) ]
        <=   d M_{W_{j+1}, b_{j+1}}(y/d)  +  1 + a d_min ,

L_j the grid family of W_j (B a multiple of 1/N in [0, b_j], and B = b_j; N = d), y = xhat - X_0(d) >= 1.
Negative control: W_{j+2} in place of W_{j+1}.   theta_na from its definition (vectorised bisection), curves from the
referee's structural envelope sequence.  This is check (C) of the author's z1_onelevel.py, re-done independently and
extended to rates up to u (the largest accuracy rate that means anything on the cube).
Usage: python3 -B ra08_z3_exponent.py
"""
import math

import numpy as np

import ra_lib as R

u = 1.0
P = R.Cube(u).setup()
a, h, es = P.a, P.h, P.epsstar
pu = P.pu
S = R.EnvSeq(P, 24)
dmin = int(math.floor(1.0 / (2 * u))) + 2


def klv(x, y):
    return x * np.log(x / y) + (1 - x) * np.log((1 - x) / (1 - y))


def theta(e):
    e = np.asarray(e, dtype=float)
    lo = np.full(e.shape, pu)
    hi = np.full(e.shape, 0.5)
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        ok = klv(mid, pu) <= e
        lo = np.where(ok, mid, lo)
        hi = np.where(ok, hi, mid)
    return np.where(e >= es, 0.0, klv(0.5 * (lo + hi), 0.5))


def grid_family(j, N):
    Bs = np.arange(0, int(math.floor(N * S.b[j] + 1e-12)) + 1) / N
    if Bs[-1] < S.b[j]:
        Bs = np.append(Bs, S.b[j])
    sig = np.clip(S.Wvec(j, Bs), 0.0, 1.0)
    if j >= 1:
        sig[-1] = 1.0 if Bs[-1] == S.b[j] else sig[-1]
    return Bs, sig


print("# cube u = 1; d_min = %d; allowance 1 + a d_min = %.4f nats" % (dmin, 1 + a * dmin))
print("#     d    j     g = y/d        y      min Pi_j     d M_{j+1}(g)   slack = d M + 1 + a d_min - min Pi    n_o*/d    [control with W_{j+2}: slack]")
worst, ncase, ctrl_fail, tight = math.inf, 0, 0, 0
for d in (300, 1000, 3000, 10000):
    N = d
    nos = np.arange(1, d - dmin + 2)
    for j in (0, 1, 2, 3, 5, 8, 12, 20):
        Bs, sig = grid_family(j, N)
        for g in (0.03 * h, 0.3 * h, h, 2 * h, 0.9 * es, 1.5 * es, 0.5 * u, u):
            y = g * d
            if y < 1.0:
                continue
            th = theta(y / nos)
            # max over lines of (d - n_o) B + (1 - sigma) n_o theta: for each n_o (chunked)
            Pi = np.empty(len(nos))
            for c0 in range(0, len(nos), 2000):
                sl = slice(c0, c0 + 2000)
                Pi[sl] = np.max((d - nos[sl])[:, None] * Bs[None, :] + (nos[sl] * th[sl])[:, None] * (1.0 - sig)[None, :], axis=1)
            k = int(np.argmin(Pi))
            M1 = d * S.M(j + 1, g)[0]
            M2 = d * S.M(j + 2, g)[0]
            slack = M1 + 1 + a * dmin - Pi[k]
            slack2 = M2 + 1 + a * dmin - Pi[k]
            ncase += 1
            worst = min(worst, slack)
            if slack2 < 0:
                ctrl_fail += 1
            if abs(Pi[k] - M1) < 1e-2:
                tight += 1
            if d in (1000, 10000) and j in (0, 2, 8) and g in (0.3 * h, 2 * h, 0.9 * es, u):
                print("  %6d  %2d   %9.5f  %8.1f   %10.4f   %10.4f        %9.4f                        %.4f       %9.4f"
                      % (d, j, g, y, Pi[k], M1, slack, nos[k] / d, slack2))
print("%d cases: least slack %.4f nats (must be >= 0);  |min Pi - d M_{j+1}| < 0.01 nats in %d cases;  the control fails in %d cases"
      % (ncase, worst, tight, ctrl_fail))
