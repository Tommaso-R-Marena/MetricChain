"""N1/N2 — falsification tests for the aliasing (coset) formula of the posterior on linear designs.

Checks, for random (non-isotropic) spectra and random linear designs on F_2^n, n <= 8:
  (a) posterior variance from cosets == dense GP posterior variance;
  (b) posterior mean from cosets  == dense GP posterior mean;
  (c) sup_x var <= 4 * NL (non-leader mass);  avg_x var >= eigenvalue tail T(N);
  (d) for BCH designs of designed distance 2m+1: min distance verified, sup_x var <= 4 tau_m^2;
  (e) sharpness of the constant 4: record max over trials of sup var / NL.
Run:  python3 n1_coset_formula.py
"""
import json
import math

import numpy as np

import cube as cb

rng = np.random.default_rng(20261125)
out = {"random": [], "bch": []}
worst = {"var": 0.0, "mean": 0.0, "ratio_sup_over_NL": 0.0, "min_avg_over_tail": math.inf}

for trial in range(300):
    n = int(rng.integers(3, 9))
    size = 1 << n
    kind = trial % 3
    if kind == 0:      # arbitrary positive spectrum, heavy-tailed
        v = rng.exponential(1.0, size) ** 3
    elif kind == 1:    # sparse spectrum (rank-deficient prior)
        v = np.where(rng.random(size) < 0.3, rng.exponential(1.0, size), 0.0)
    else:              # isotropic decaying
        s2 = [rng.exponential(1.0) * 0.5 ** m for m in range(n + 1)]
        v = cb.iso_spectrum(n, s2)
    r = int(rng.integers(1, n + 1))
    rows = [int(rng.integers(1, size)) for _ in range(r)]
    rk = cb.gf2_rank(rows)
    A = cb.span(rows, n)
    assert len(A) == 1 << rk
    g = cb.sample_gp(v, rng)
    mean_c, var_c, info = cb.posterior_linear(v, rows, n, g)
    mean_d, var_d, _ = cb.posterior_direct(v, A, g[A])
    scale = max(1.0, v.sum())
    e_var = float(np.max(np.abs(var_c - var_d)) / scale)
    e_mean = float(np.max(np.abs(mean_c - mean_d)) / max(1.0, np.max(np.abs(g))))
    worst["var"] = max(worst["var"], e_var)
    worst["mean"] = max(worst["mean"], e_mean)
    NL = info["NL"]
    sup = float(var_c.max())
    avg = float(var_c.mean())
    tail = cb.eig_tail(v, len(A))
    assert sup <= 4 * NL + 1e-9 * scale, (sup, NL)
    assert avg >= tail - 1e-9 * scale, (avg, tail)
    if NL > 1e-12:
        worst["ratio_sup_over_NL"] = max(worst["ratio_sup_over_NL"], sup / NL)
    if tail > 1e-12:
        worst["min_avg_over_tail"] = min(worst["min_avg_over_tail"], avg / tail)
    # interpolation at the design points
    assert np.max(np.abs(mean_c[A] - g[A])) < 1e-7 * max(1.0, np.max(np.abs(g)))
    assert np.max(var_c[A]) < 1e-9 * scale

out["random_summary"] = worst
print("random designs:", worst)
# NB: the dense comparison uses a pseudo-inverse of K_AA, which truncates tiny eigenvalues for the
# heavy-tailed spectra (relative error ~1e-7).  The structural check below is independent of that.
assert worst["var"] < 1e-5 and worst["mean"] < 1e-5

# ---- structural check, independent of conditioning: the coset covariance K_A vanishes on A and
#      K - K_A lies in span{K(.,a)} -- these two properties characterise the Schur complement.
serr = 0.0
for trial in range(150):
    n = int(rng.integers(3, 8))
    size = 1 << n
    kind = trial % 3
    if kind == 0:
        v = rng.exponential(1.0, size) ** 3
    elif kind == 1:
        v = np.where(rng.random(size) < 0.3, rng.exponential(1.0, size), 0.0)
    else:
        v = cb.iso_spectrum(n, [rng.exponential(1.0) * 0.5 ** m for m in range(n + 1)])
    rows = [int(rng.integers(1, size)) for _ in range(int(rng.integers(1, n + 1)))]
    A = cb.span(rows, n)
    _, var_c, _ = cb.posterior_linear(v, rows, n)
    syn = cb.syndromes(rows, n)
    ncos = 1 << len(rows)
    X = np.arange(size)
    chim = 1 - 2 * (cb.popcount((X[:, None] & X[None, :]).astype(np.uint64)) & 1)
    Kfull = (chim * v[None, :]) @ chim.T
    KA = np.zeros_like(Kfull)
    V = np.bincount(syn, weights=v, minlength=ncos)
    for T in range(ncos):
        if V[T] <= 0:
            continue
        sel = syn == T
        s_ = chim[:, sel] @ v[sel]
        KA += (chim[:, sel] * v[sel][None, :]) @ chim[:, sel].T - np.outer(s_, s_) / V[T]
    sc = max(1.0, v.sum())
    coef = np.linalg.lstsq(Kfull[:, A], Kfull - KA, rcond=None)[0]
    serr = max(serr, np.max(np.abs(KA[:, A])) / sc,
               np.max(np.abs(Kfull[:, A] @ coef - (Kfull - KA))) / sc,
               np.max(np.abs(np.diag(KA) - var_c)) / sc)
print("structural check, max relative error:", serr)
assert serr < 1e-10
out["structural_check_max_rel_err"] = float(serr)

# ---- BCH designs
for n, m in [(7, 1), (6, 1), (5, 1), (15, 1), (15, 2), (12, 2), (10, 2), (7, 2), (15, 3)]:
    rows = cb.bch_rows(n, m)
    rk = cb.gf2_rank(rows)
    ok = cb.min_distance_at_least(rows, n, 2 * m + 1)
    w = cb.weights(n)
    M = sum(math.comb(n, j) for j in range(m + 1))
    res = {"n": n, "m": m, "N": 1 << rk, "M_m": M, "dist>=2m+1": bool(ok)}
    # isotropic spectrum: unit variance on each order 0..m, tail on orders > m
    for name, s2 in [("geometric", [0.5 ** j for j in range(n + 1)]),
                     ("flat_tail", [1.0] * (m + 1) + [0.05] * (n - m)),
                     ("exact_order_m", [1.0] * (m + 1) + [0.0] * (n - m))]:
        v = cb.iso_spectrum(n, s2)
        tau2 = float(v[w > m].sum())
        if n <= 12:
            _, var, info = cb.posterior_linear(v, rows, n)
            sup, avg, NL = float(var.max()), float(var.mean()), info["NL"]
        else:  # n = 15: 2^15 points, up to 2^rk cosets -> still fine for rk <= 8, else bound only
            if rk <= 8:
                _, var, info = cb.posterior_linear(v, rows, n)
                sup, avg, NL = float(var.max()), float(var.mean()), info["NL"]
            else:
                sup = avg = float("nan")
                NL = cb.non_leader_mass(v, rows, n)
        res[name] = {"tau_m^2": tau2, "NL": NL, "sup_var": sup, "avg_var": avg,
                     "eig_tail(N)": cb.eig_tail(v, 1 << rk), "eig_tail(M_m)": cb.eig_tail(v, M)}
        if ok:
            assert NL <= tau2 + 1e-9
            if not math.isnan(sup):
                assert sup <= 4 * tau2 + 1e-9
    out["bch"].append(res)
    print(res)

with open("n1_coset_formula.json", "w") as fh:
    json.dump(out, fh, indent=1)
print("N1 OK")
