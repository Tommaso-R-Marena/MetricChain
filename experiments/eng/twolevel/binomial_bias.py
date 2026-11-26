"""X-006b, part 1: the defect of numpy's binomial sampler at large counts, and the exact replacement.

Reported by the Scientific Discovery Division (SCI-REV-0007 §4, request R6-E3).  This script
measures, in the environment of the engineering runs,

  * numpy's ``Generator.binomial(n, p)`` on a grid of ``n`` and of means ``n p``: z-scores of the sample
    mean and of the sample variance against the exact values;
  * ``metricchain_eng.twolevel.sampling.binomial_exact`` on the same grid;
  * the exact sampler against the exact probability mass function (chi-square) in the three
    regimes of its collision step (dense, thinning with many collisions, thinning with few).

    python experiments/eng/twolevel/binomial_bias.py --draws 400000 --out experiments/eng/twolevel/results/x006b_binomial_bias.json

Every cell uses its own stream, seeded by (seed, cell index), so a cell can be recomputed alone.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from metricchain_eng.twolevel import sampling  # noqa: E402

NS = (10 ** 9, 2 ** 31, 10 ** 12, 10 ** 14, 10 ** 15, 2 ** 53, 10 ** 16, 10 ** 17, 10 ** 18, 2 ** 61)
MEANS = (5.0, 29.0, 60.0, 92.0, 500.0, 5000.0, 1e5, 1e7, 1e10, 1e13)       # the last two only where n >= 1e15


def zscores(x: np.ndarray, n: int, mean: float) -> tuple[float, float, float]:
    """z of the sample mean, z of the sample variance, relative error of the sample mean."""
    p = mean / n
    var = mean * (1 - p)
    N = len(x)
    xm = float(x.mean())
    zm = (xm - mean) / math.sqrt(var / N)
    # variance of the sample variance: (mu4 - var^2)/N, mu4 = var (1 + 3 var (1 - 2p ... )) ~ 3 var^2 + var for small p
    zv = (float(x.var()) - var) / math.sqrt((2 * var * var + var) / N)
    return zm, zv, xm / mean - 1


def grid(draws: int, seed: int) -> list[dict]:
    rows = []
    for i, n in enumerate(NS):
        for j, mean in enumerate(MEANS):
            if mean > 1e7 and n < 10 ** 15:
                continue
            p = mean / n
            rng = np.random.default_rng([seed, 1, i, j])
            x = rng.binomial(n, p, size=draws).astype(np.float64)
            zm, zv, rel = zscores(x, n, mean)
            rng = np.random.default_rng([seed, 2, i, j])
            lp, lq = math.log(p), math.log1p(-p)
            # the exact sampler is a Python loop: fewer draws where it is slow (large means)
            m = draws if mean <= 5000 else max(2000, draws // 20)
            y = np.array([sampling.binomial_exact(rng, n, lp, lq) for _ in range(m)], dtype=np.float64)
            branch = sampling.branch(n, lp, lq)
            ezm, ezv, erel = zscores(y, n, mean)
            rows.append(dict(n=n, mean=mean, draws=draws, numpy_z_mean=zm, numpy_z_var=zv, numpy_rel_mean=rel,
                             exact_draws=m, exact_branch=branch, exact_z_mean=ezm, exact_z_var=ezv, exact_rel_mean=erel))
            print(f"n={n:.3g} mean={mean:g}: numpy z=({zm:+.1f},{zv:+.1f}) rel={rel:+.2e} | exact[{branch}] z=({ezm:+.1f},{ezv:+.1f})", flush=True)
    return rows


def chi_square(draws: int, seed: int) -> list[dict]:
    """The Poissonisation branch against the exact law, forced by calling it below N_SAFE."""
    out = []
    cases = [("dense: n=12, p=0.3", 12, 0.3), ("dense: n=40, p=0.5", 40, 0.5), ("thinning, many collisions: n=2000, p=0.05", 2000, 0.05),
             ("thinning, many collisions: n=10^5, p=0.004", 10 ** 5, 0.004), ("thinning, few collisions: n=10^8, p=3e-7", 10 ** 8, 3e-7),
             ("thinning, few collisions: n=2^40, p=92/2^40", 2 ** 40, 92 / 2 ** 40), ("n=2^61, p=92/2^61", 2 ** 61, 92 / 2 ** 61),
             ("n=2^61, p=500/2^61", 2 ** 61, 500 / 2 ** 61)]
    for c, (name, n, p) in enumerate(cases):
        rng = np.random.default_rng([seed, 3, c])
        mu = -math.log1p(-p)
        x = np.array([sampling._distinct(rng, int(rng.poisson(n * mu)), n) for _ in range(draws)])
        mean, sd = n * p, math.sqrt(n * p * (1 - p))
        lo, hi = max(0, int(mean - 4.5 * sd)), min(n, int(mean + 4.5 * sd) + 1)
        ks = np.arange(lo, hi + 1)
        pmf = stats.binom.pmf(ks, n, p)
        obs = np.array([(x == k).sum() for k in ks], dtype=float)
        exp_ = pmf * draws
        # pool the cells with small expectation into the two ends
        keep = exp_ >= 5
        o = np.concatenate([[obs[~keep & (ks < mean)].sum() + (x < lo).sum()], obs[keep], [obs[~keep & (ks >= mean)].sum() + (x > hi).sum()]])
        e = np.concatenate([[exp_[~keep & (ks < mean)].sum() + stats.binom.cdf(lo - 1, n, p) * draws], exp_[keep],
                            [exp_[~keep & (ks >= mean)].sum() + stats.binom.sf(hi, n, p) * draws]])
        ok = e > 0
        chi2 = float(((o[ok] - e[ok]) ** 2 / e[ok]).sum())
        dof = int(ok.sum()) - 1
        out.append(dict(case=name, n=n, p=p, draws=draws, chi2=chi2, dof=dof, p_value=float(stats.chi2.sf(chi2, dof))))
        print(f"{name}: chi2 = {chi2:.1f} on {dof} dof, p = {out[-1]['p_value']:.3f}", flush=True)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--draws", type=int, default=400000)
    ap.add_argument("--seed", type=int, default=20261126)
    ap.add_argument("--out", type=str, default="")
    args = ap.parse_args()
    t0 = time.time()
    res = dict(numpy=np.__version__, scipy=__import__("scipy").__version__, seed=args.seed,
               thresholds=dict(N_SAFE=sampling.N_SAFE, P_SMALL=sampling.P_SMALL, LAM_MAX=sampling.LAM_MAX, CAND_PER_TRIAL=sampling.CAND_PER_TRIAL),
               chi_square=chi_square(max(20000, args.draws // 4), args.seed), grid=grid(args.draws, args.seed))
    res["seconds"] = time.time() - t0
    if args.out:
        Path(args.out).write_text(json.dumps(res, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
