#!/usr/bin/env python3
"""Workstream R27, Item 4 -- what Theorem L guarantees in numbers on idealised traces (lengths in angstrom):
   helix-like  (radius 2.3, rise 1.5, 100 deg per point)       strand-like (radius 0.94, rise 3.3, 160 / 170 / 175 deg per point)
and a replication of the table of section 6 of the note (C_L, 1/(2 mu), certified range, first-order worst case).

For each trace and length n:
   C_L   = 1.2 b (n+2)^2/(s* tau*)                      (uniform constant of Theorem L; squared-distance errors)
   C_loc = 2 ||M||_2                                     (a constant read off the local form: d_P <= ||M e||_2 <= ||M||_2 ||e||_2 <= 2 ||M||_2 ||eta||_2)
   mu, 1/(2 mu)                                          (first-order constant for squared distances), s_7 of the rigidity matrix (distances)
   R_g (radius of gyration), d_max (largest measured distance), N = 4n - 10 measured pairs.
Distance errors delta_jk with root-mean-square sigma: ||eta||_2 <= (2 d_max + max|delta|) sigma sqrt(N)  (worst allocation; the delta^2 term is neglected
below because sigma << d).  The error bar of the theorem as an RMSD is  C ||eta||_2 / sqrt(n).
   sigma_obj(C) = R_g sqrt(n) / (C 2 d_max sqrt(N))      rms distance error below which the error bar is smaller than the radius of gyration
   sigma_1A(C)  =      sqrt(n) / (C 2 d_max sqrt(N))     ... smaller than 1 angstrom
Nothing here is a statement about real structures: idealised traces of constant radius, rise and turn.

Run:  OMP_NUM_THREADS=1 python3 -B item4_tables.py > item4_tables_<stamp>.log
"""
import os, sys, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from r27lib import (cap_memory, peak_mb, now, KAPPA, helix, chain_consts, pair_arrays, local_weights, uniform_constant,
                    half_jacobian, band_laplacian_max)

cap_memory(2.0)
t0 = time.time()
print(f"R27 item4_tables.py started {now()}")


def quantities(X, want_mu=True):
    n = len(X)
    tau, s, b = chain_consts(X)
    J, K = pair_arrays(n)
    d = np.linalg.norm(X[J] - X[K], axis=1)
    N = len(J)
    C = uniform_constant(X, (tau, s, b))
    Cloc = 2 * np.linalg.svd(local_weights(X, tau, s), compute_uv=False)[0]
    rg = np.sqrt(((X - X.mean(0)) ** 2).sum() / n)
    out = dict(n=n, b=b, tau=tau.min(), s=s.min(), C=C, Cloc=Cloc, rg=rg, dmax=d.max(), drms=np.sqrt((d * d).mean()), N=N)
    if want_mu:
        A = half_jacobian(X, J, K)
        S = np.linalg.svd(A, compute_uv=False)
        S = np.concatenate([S, np.zeros(max(0, 3 * n - len(S)))])
        mu = S[3 * n - 7]
        Rg_ = A / d[:, None]                                  # rigidity matrix for distances
        S2 = np.linalg.svd(Rg_, compute_uv=False)
        S2 = np.concatenate([S2, np.zeros(max(0, 3 * n - len(S2)))])
        s7 = S2[3 * n - 7]
        nz = S[:3 * n - 6]
        # Gaussian noise of the squared distances, least-squares estimator, first order: E d_P^2 = sig^2 sum 1/(4 mu_i^2);
        # worst case for the same l2 norm: N sig^2/(4 mu^2)
        typ_over_worst = np.sqrt((1.0 / nz ** 2).sum() / (N / mu ** 2))
        out.update(mu=mu, s7=s7, zero=S[3 * n - 6], Lam=band_laplacian_max(n), typ=typ_over_worst)
    return out


traces = [("helix-like (2.3, 1.5, 100)", lambda n: helix(n, 2.3, 1.5, 100.0)),
          ("strand-like (0.94, 3.3, 160)", lambda n: helix(n, 0.94, 3.3, 160.0)),
          ("strand-like (0.94, 3.3, 170)", lambda n: helix(n, 0.94, 3.3, 170.0)),
          ("strand-like (0.94, 3.3, 175)", lambda n: helix(n, 0.94, 3.3, 175.0))]

print("\n[T1] replication of the table of section 6 of the note.  Their numbers (n: C_L | 1/(2mu) | certified range as rms distance error | first-order RMSD per unit rms distance error):")
print("     helix-like 12: 185 | 0.23 | 2e-5 | 4.2;   20: 456 | 0.45 | 3e-6 | 9.0;   100: 9800 | 9.5 | 2e-9 | 207")
print("     strand-like 160: 12: 1780 | 3.3 | 9e-8 | 58;   20: 4410 | 7.3 | 1e-8 | 140;   100: 94700 | 168 | 9e-12 | 3460;      strand-like 175, 20: 65100 | 42 | 1e-10 | 753")
print("     mine (certified range = mu/(11.04 C_L) as a squared-distance l2 norm, converted to an rms distance error by /(2 d_rms sqrt(N)) and by /(2 d_max sqrt(N));")
print("           first-order worst case = sqrt(N/n)/s_7(rigidity matrix)):")
for name, gen, ns in ((traces[0][0], traces[0][1], (12, 20, 100)), (traces[1][0], traces[1][1], (12, 20, 100)), (traces[3][0], traces[3][1], (20,))):
    for n in ns:
        q = quantities(gen(n))
        rho = q["mu"] / (11.04 * q["C"])
        print(f"     {name:30s} n={n:4d}: C_L = {q['C']:9.4g} | 1/(2mu) = {1 / (2 * q['mu']):7.4g} | range {rho:.2e} A^2 -> rms {rho / (2 * q['drms'] * np.sqrt(q['N'])):.1e} (d_rms) / "
              f"{rho / (2 * q['dmax'] * np.sqrt(q['N'])):.1e} (d_max) A | first-order worst case {np.sqrt(q['N'] / n) / q['s7']:8.4g} | tau* = {q['tau']:.4f}, s* = {q['s']:.4f}, b = {q['b']:.4f}")

print("\n[T2] for which noise levels is the error bar of Theorem L smaller than the object?")
print("     columns: n | R_g  d_max | C_L  C_loc  1/(2mu) | rms distance error below which the RMSD bound is < R_g: with C_L, with C_loc | ... < 1 A: with C_L, with C_loc |")
print("              the same two thresholds for the first-order worst case (NOT a guarantee: the best any worst-case theorem could give) | typical/worst (Gaussian noise, first order)")
for name, gen in traces:
    print(f"   {name}")
    for n in (5, 8, 12, 20, 50, 100, 200):
        q = quantities(gen(n))
        f = np.sqrt(n) / (2 * q["dmax"] * np.sqrt(q["N"]))
        sU, sL = q["rg"] * f / q["C"], q["rg"] * f / q["Cloc"]
        s1 = q["rg"] / (np.sqrt(q["N"] / n) / q["s7"])
        print(f"     {n:4d} | {q['rg']:6.2f} {q['dmax']:6.2f} | {q['C']:10.4g} {q['Cloc']:10.4g} {1 / (2 * q['mu']):8.4g} | {sU:.1e} {sL:.1e} | {f / q['C']:.1e} {f / q['Cloc']:.1e} | "
              f"{s1:.1e} {s1 / q['rg']:.1e} | {q['typ']:.3f}")

print("\n[T3] for a given rms distance error sigma, the lengths n >= 5 for which the uniform error bar (RMSD) is below the radius of gyration")
print("     (RMSD bound = C_L 2 d_max sigma sqrt(N/n); 'none' = for no n in 5..300)")
for name, gen in traces:
    rows = []
    cache = []
    for n in list(range(5, 61)) + [80, 100, 150, 200, 300]:
        X = gen(n)
        tau, s, b = chain_consts(X)
        J, K = pair_arrays(n)
        d = np.linalg.norm(X[J] - X[K], axis=1)
        C = 1.2 * b * (n + 2) ** 2 / (s.min() * tau.min())
        rg = np.sqrt(((X - X.mean(0)) ** 2).sum() / n)
        cache.append((n, C * 2 * d.max() * np.sqrt(len(J) / n), rg))
    line = []
    for sig in (1.0, 0.1, 0.01, 1e-3, 1e-4, 1e-5):
        ok = [n for n, c, rg in cache if c * sig < rg]
        line.append(f"sigma = {sig:g} A: " + ("none" if not ok else f"n in {min(ok)}..{max(ok)}" + ("" if ok == [c[0] for c in cache if min(ok) <= c[0] <= max(ok)] else " (not an interval)")))
    print(f"   {name:30s} " + ";  ".join(line))
    n5 = cache[0]
    print(f"   {'':30s} at n = 5 the bar is below R_g iff sigma < {n5[2] / n5[1]:.2e} A;  the threshold decreases with n: " +
          ", ".join(f"n={n}: {rg / c:.1e}" for n, c, rg in cache if n in (5, 10, 20, 50, 100, 300)))

print("\n[T4] Corollary L.2 in practice: the constant computed from an ESTIMATE instead of the truth (helix-like n = 20; the estimate = truth + Gaussian noise of size s)")
rng = np.random.default_rng(27115)
X = helix(20, 2.3, 1.5, 100.0)
for sg in (0.0, 0.05, 0.2, 0.5):
    vals = []
    for _ in range(20):
        Yh = X + sg * rng.normal(size=X.shape)
        vals.append(uniform_constant(Yh))
    print(f"     s = {sg:4.2f} A: C(estimate) median {np.median(vals):9.4g}  range [{min(vals):9.4g}, {max(vals):9.4g}]   (C of the truth: {uniform_constant(X):.4g})")
print(f"ALL DONE {now()}  {time.time() - t0:.1f} s  peak memory {peak_mb():.0f} MB")
