"""N6 — what a Bayesian certificate is worth when the prior is wrong, and what a population-level
(conformal) recalibration can and cannot repair.

Toy: X = {0,1}^10, f = 0.5|x|, target min(f+g).  ASSUMED prior: isotropic, sigma_1^2 = n*0.04,
sigma_2^2 = n*0.02 (orders 1,2) plus a constant of variance 1.  Design: dual BCH, m = 1 (N = 16 evaluations): main effects are
learned, the pair part is the unlearned tail.  Certificate: the 95% posterior interval of
min(f+g) under the assumed prior (posterior sampling, 400 samples) — exact up to Monte Carlo.

Truths:
  (a) well specified;
  (b) pair variance 4x the assumed one;
  (c) an order-3 component (variance n*0.02) that the prior does not contain;
  (d) heavy tails: Walsh coefficients ~ Student t_3 scaled to the assumed variances;
  (e) dips: in a fraction 0.2 of the instances a first-order dip  -(D - c d_H(x,y))_+  of depth
      D = 2, slope c = 1 (11 of 1024 configurations) centred at one of the 30 lowest states.
For each: coverage of the nominal interval; a goodness-of-fit check the user can run on the
SAME 16 evaluations (y^T K_AA^{-1} y ~ chi^2_15); a check with 32 extra random evaluations
(standardised residuals); split-conformal recalibration (300 calibration instances with known
truth, 300 test instances) with score |truth - centre| / halfwidth.

Also: the Lebesgue function of the designs (amplification of a sup-norm-bounded remainder).
Run: OMP_NUM_THREADS=1 python3 n6_misspec.py
"""
import json
import math

import numpy as np
from scipy import stats

import cube as cb
from n4_bayes import LinearPosterior

rng = np.random.default_rng(606)
n = 10
size = 1 << n
w = cb.weights(n)
f = 0.5 * w.astype(float)
v_assumed = cb.iso_spectrum(n, [1.0, n * 0.04, n * 0.02])
rows = cb.bch_rows(n, 1)
post = LinearPosterior(v_assumed, rows, n)
A = cb.span(rows, n)
KAA = cb.kernel_matrix(v_assumed, A, A)
KAA_pinv = np.linalg.pinv(KAA, hermitian=True)
rankA = int(np.linalg.matrix_rank(KAA))
res = np.stack([post.posterior_residual() for _ in range(400)])
ALPHA = 0.05
idx = np.arange(size)
NOT_A = np.setdiff1d(idx, A)
assert post.P[NOT_A].min() > 1e-6


def truth_sampler(kind):
    if kind == "a":
        v = v_assumed
        return cb.fwht(rng.standard_normal(size) * np.sqrt(v)), False
    if kind == "b":
        v = cb.iso_spectrum(n, [1.0, n * 0.04, n * 0.08])
        return cb.fwht(rng.standard_normal(size) * np.sqrt(v)), False
    if kind == "c":
        v = cb.iso_spectrum(n, [1.0, n * 0.04, n * 0.02, n * 0.02])
        return cb.fwht(rng.standard_normal(size) * np.sqrt(v)), False
    if kind == "d":
        t = stats.t.rvs(3, size=size, random_state=rng) / math.sqrt(3.0)   # unit variance
        return cb.fwht(t * np.sqrt(v_assumed)), False
    if kind == "e":
        g = cb.fwht(rng.standard_normal(size) * np.sqrt(v_assumed))
        if rng.random() < 0.2:
            low = np.argsort(f + g)[:30]                    # a low-lying state the model mispredicts
            y = int(low[rng.integers(30)])
            dist = cb.popcount((idx ^ y).astype(np.uint64))
            g = g - np.maximum(2.0 - 1.0 * dist, 0.0)       # depth 2, slope 1: 11 of 1024 points
            return g, True
        return g, False
    raise ValueError(kind)


def analyse(g):
    ghat = cb.fwht(g) / size
    mean = post.mean_from_ghat(ghat)
    truth = float(np.min(f + g))
    samp = np.min(f[None, :] + mean[None, :] + res, axis=1)
    lo, hi = np.quantile(samp, [ALPHA / 2, 1 - ALPHA / 2])
    centre, half = (lo + hi) / 2, (hi - lo) / 2
    y = g[A]
    chi2 = float(y @ KAA_pinv @ y)
    p_fit = float(stats.chi2.sf(chi2, rankA))              # upper tail: data too rough for the prior
    extra = rng.choice(NOT_A, 32, replace=False)           # extra evaluations off the design
    zres = (g[extra] - mean[extra]) / post.P[extra]
    zstat = float(np.mean(zres ** 2))                      # ~ 1 under the assumed prior
    return truth, centre, half, p_fit, zstat


out = {}
for kind, label in [("a", "well specified"), ("b", "pair variance x4"), ("c", "unmodelled order 3"),
                    ("d", "Student-t3 coefficients"), ("e", "dips in 20% of instances")]:
    recs = []
    for _ in range(600):
        g, dipped = truth_sampler(kind)
        recs.append(analyse(g) + (dipped,))
    truth, centre, half, pfit, zstat, dipped = map(np.array, zip(*recs))
    covered = np.abs(truth - centre) <= half
    cal, test = slice(0, 300), slice(300, 600)
    scores = np.abs(truth[cal] - centre[cal]) / half[cal]
    k = math.ceil((1 - ALPHA) * (300 + 1))
    q = float(np.sort(scores)[k - 1])
    cov_conf = np.abs(truth[test] - centre[test]) <= q * half[test]
    r = {"label": label, "nominal_coverage": float(covered.mean()),
         "mean_halfwidth": float(half.mean()),
         "conformal_factor_q": q, "conformal_coverage_test": float(cov_conf.mean()),
         "fit_test_reject_rate_at_5pct": float(np.mean(pfit < 0.05)),
         "heldout_z2_mean": float(zstat.mean()),
         "heldout_reject_rate": float(np.mean(zstat > stats.chi2.ppf(0.95, 32) / 32))}
    if kind == "e":
        d = dipped.astype(bool)
        r["nominal_coverage_dipped"] = float(covered[d].mean())
        r["nominal_coverage_clean"] = float(covered[~d].mean())
        dt = d[test]
        r["conformal_coverage_dipped"] = float(cov_conf[dt].mean()) if dt.any() else None
        r["conformal_coverage_clean"] = float(cov_conf[~dt].mean())
        r["fit_reject_rate_dipped"] = float(np.mean(pfit[d] < 0.05))
        r["heldout_reject_rate_dipped"] = float(np.mean(zstat[d] > stats.chi2.ppf(0.95, 32) / 32))
        r["mean_abs_error_dipped"] = float(np.mean(np.abs(truth[d] - centre[d])))
    out[kind] = r
    print(kind, r, flush=True)

# ---- Lebesgue functions: amplification of an adversarial sup-norm remainder
leb = []
for nn, m in [(7, 1), (7, 2), (10, 1), (10, 2), (12, 1)]:
    vv = cb.iso_spectrum(nn, [1.0] * (m + 1))             # exact order <= m (incl. constant)
    rws = cb.bch_rows(nn, m)
    AA = cb.span(rws, nn)
    _, var, W = cb.posterior_direct(vv, AA)
    lam = np.abs(W).sum(axis=1)
    M = sum(math.comb(nn, j) for j in range(m + 1))
    leb.append({"n": nn, "m": m, "N": len(AA), "M": M, "max_Lebesgue": float(lam.max()),
                "mean_Lebesgue": float(lam.mean()), "sqrt_M": math.sqrt(M),
                "max_l2_weights": float(np.sqrt((W ** 2).sum(axis=1)).max()),
                "sqrt(M/N)": math.sqrt(M / len(AA)), "max_var": float(var.max())})
    print(leb[-1], flush=True)
out["lebesgue"] = leb
with open("n6_misspec.json", "w") as fh:
    json.dump(out, fh, indent=1)
print("N6 done")
