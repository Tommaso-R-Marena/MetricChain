#!/usr/bin/env python3
"""Physical reading of workstream R10's small-slope law (Propositions R10.1, R10.2; SCI-REV-0010) for the
helix-coil chain of FINITE length -- coordinator's script.

Zimm-Bragg chain of n residues, states c (coil) / h (helix); weights: a residue in h after h: s; in h after c (or at
the first position): sigma*s; in c: 1.  The pair weights [[1, sigma s], [1, s]] have determinant s (1 - sigma) > 0, so
the measure is log-supermodular (associated), and by R10.2 the largest variance of a function with one-residue
oscillation <= 1 is Var(N_h), N_h = number of helical residues.  By R10.1 the three exponents of the n-residue chain
are, to second order in the per-residue envelope u (in k_B T):   E_n, a_n = u^2 Var(N_h)/2,   h_n = u^2 Var(N_h)/8.
The factor relative to independent residues with the same one-residue marginals theta_i is
        S_n := Var(N_h) / sum_i theta_i (1 - theta_i);
for the infinite chain S = (1 + rho)/(1 - rho), rho = lambda_-/lambda_+, i.e.
        S_inf = (1 + s)/sqrt((1 - s)^2 + 4 sigma s)          (= sigma^(-1/2) at the midpoint s = 1).
This script (1) checks the transfer-matrix computation against brute-force enumeration for n <= 12, (2) checks the
bulk formula at n = 20 000, (3) tabulates S_n for peptide lengths, at s = 1 and at the chain's own transition
midpoint (largest Var(N_h)), (4) reports the range of validity suggested by u * sd(N_h) <= 1.
Model-relative: Zimm-Bragg weights only; nothing here is fitted to or compared with a measurement.
"""
import itertools, math
import numpy as np

def exact_stats(n, s, sigma):
    """Var(N_h), marginals theta_i by forward-backward with polynomial bookkeeping avoided: use first/second derivatives
    via a 3-component (value, d/dlambda, d2/dlambda2) transfer in lambda = ln s."""
    # generating function in z multiplying each helical residue: weights s*z; moments from derivatives at z = 1
    # forward vectors over (state) with (Z, Z', Z'') where ' = d/dz at z = 1
    # state 0 = c, 1 = h.  Start: virtual previous state c.
    Z = np.array([1.0, 0.0]); Z1 = np.zeros(2); Z2 = np.zeros(2)       # before any residue: "previous state c"
    for i in range(n):
        wc = np.array([1.0, 1.0])                 # to c from (c, h)
        wh = np.array([sigma * s, s])             # to h from (c, h); carries one factor z
        nZ = np.array([wc @ Z, wh @ Z]); nZ1 = np.array([wc @ Z1, wh @ Z1 + wh @ Z]); nZ2 = np.array([wc @ Z2, wh @ Z2 + 2 * (wh @ Z1)])
        scale = nZ.sum(); Z, Z1, Z2 = nZ / scale, nZ1 / scale, nZ2 / scale
    tot = Z.sum(); m1 = Z1.sum() / tot; m2f = Z2.sum() / tot          # E N, E N(N-1)
    var = m2f + m1 - m1 * m1
    # marginals by forward-backward
    F = np.zeros((n + 1, 2)); F[0] = [1.0, 0.0]
    T = np.array([[1.0, sigma * s], [1.0, s]])
    for i in range(n):
        F[i + 1] = F[i] @ T; F[i + 1] /= F[i + 1].sum()
    B = np.zeros((n + 1, 2)); B[n] = [1.0, 1.0]
    for i in range(n - 1, -1, -1):
        B[i] = T @ B[i + 1]; B[i] /= B[i].sum()
    theta = np.array([F[i + 1, 1] * B[i + 1, 1] / (F[i + 1] @ B[i + 1]) for i in range(n)])
    return var, m1, theta

def brute(n, s, sigma):
    Z = 0.0; m1 = 0.0; m2 = 0.0; th = np.zeros(n)
    for x in itertools.product((0, 1), repeat=n):
        w = 1.0; prev = 0
        for xi in x:
            if xi: w *= s * (1.0 if prev else sigma)
            prev = xi
        N = sum(x); Z += w; m1 += w * N; m2 += w * N * N; th += w * np.array(x)
    m1 /= Z; m2 /= Z
    return m2 - m1 * m1, m1, th / Z

def S_inf(s, sigma): return (1 + s) / math.sqrt((1 - s) ** 2 + 4 * sigma * s)

# (1) transfer matrix against brute force
worst = 0.0
for n in (3, 6, 9, 12):
    for s in (0.6, 1.0, 1.4):
        for sigma in (1e-3, 0.05, 0.5):
            v, m, th = exact_stats(n, s, sigma); vb, mb, thb = brute(n, s, sigma)
            worst = max(worst, abs(v - vb) / max(vb, 1e-300), abs(m - mb) / max(mb, 1e-300), float(np.abs(th - thb).max()))
assert worst < 1e-9, worst
print(f"(1) transfer matrix against brute-force enumeration, n = 3, 6, 9, 12, 9 parameter pairs each: largest deviation {worst:.1e}")
v5, _, _ = exact_stats(5, 1.0, 1e-3)
print(f"    n = 5, s = 1, sigma = 1e-3: Var(N_h) = {v5:.6f}   (workstream R10 reports V_5 = 0.102379 over all vertices)")

# (2) bulk formula
for s, sigma in ((1.0, 1e-3), (1.0, 1e-4), (1.1, 1e-3), (1.5, 1e-3), (0.8, 1e-3)):
    n = 20000; v, m, th = exact_stats(n, s, sigma)
    mid = slice(n // 4, 3 * n // 4)
    # per-site ratio in the bulk: d Var / dn against theta(1-theta)
    v2, _, _ = exact_stats(n + 2000, s, sigma)
    t = float(th[n // 2]); ratio = (v2 - v) / 2000 / (t * (1 - t))
    print(f"(2) n -> infinity, s = {s}, sigma = {sigma:g}: bulk helix fraction {t:.4f}; d Var(N_h)/dn / [theta(1-theta)] = {ratio:.3f};  formula (1+s)/sqrt((1-s)^2+4 sigma s) = {S_inf(s, sigma):.3f}")
    assert abs(ratio / S_inf(s, sigma) - 1) < 2e-3

# (3) finite peptides
print("(3) finite chains.  Columns: s; helix fraction <N_h>/n; Var(N_h); S_n = Var(N_h)/sum theta_i(1-theta_i); second-order")
print("    coefficients per residue  E_n/(n u^2) = a_n/(n u^2) = Var(N_h)/(2n)  [independent residues at theta = 1/2: 0.125];  u_max := 1/sd(N_h)")
for sigma in (1e-3, 1e-4):
    print(f"  sigma = {sigma:g}   (infinite chain at s = 1: S = {S_inf(1.0, sigma):.1f}; cooperative length sigma^(-1/2) = {sigma ** -0.5:.0f} residues)")
    for n in (10, 20, 30, 50, 100, 300, 1000):
        rows = []
        # at s = 1
        v, m, th = exact_stats(n, 1.0, sigma); rows.append(("s = 1", 1.0, v, m, th))
        # at the chain's own midpoint: largest Var(N_h) over s
        grid = np.exp(np.linspace(math.log(0.5), math.log(60.0), 2401))
        vs = [exact_stats(n, float(sv), sigma)[0] for sv in grid]
        k = int(np.argmax(vs)); sv = float(grid[k]); v, m, th = exact_stats(n, sv, sigma); rows.append(("largest Var", sv, v, m, th))
        out = []
        for name, sv, v, m, th in rows:
            prod = float((th * (1 - th)).sum())
            out.append(f"{name}: s = {sv:.3f}, <N_h>/n = {m / n:.3f}, Var = {v:.3f}, S_n = {v / prod:.2f}, Var/(2n) = {v / (2 * n):.4f}, u_max = {1 / math.sqrt(v):.3f}")
        print(f"    n = {n:5d} | " + " | ".join(out))
print("ALL OK")
