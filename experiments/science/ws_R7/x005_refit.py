"""R7: refit of the X-005 trend ("excess of the worst case over the claimed exponent decays like 1/sqrt(n)").

Reads the engineering division's stored search results (experiments/eng/twolevel/results/x005_cost.jsonl at a2f6dc7)
and rebuilds, with my own code, the table TABLE:trend of ENG-RES-0008 section 3:
  for every (u, n): worst(phi) = max over {flat bottom, flat top, all cost searches} of ln(cost);
  phi* = argmin_phi worst(phi);  excess = worst(phi*)/(n a) - claimed_exponent(phi*)/a.
Then fits several laws to excess(n).
"""
import json, math, sys
from collections import defaultdict
from pathlib import Path
import numpy as np

P = Path(__file__).resolve().parent / "eng_copy" / "experiments" / "eng" / "twolevel" / "results" / "x005_cost.jsonl"
rows = [json.loads(l) for l in open(P)]
cells = defaultdict(dict)
for r in rows:
    worst = max([r["flat"]["bottom"]["lcost"], r["flat"]["top"]["lcost"]] +
                [s["best_value"] for s in r["searches"] if s["objective"] == "cost"])
    flat = max(r["flat"]["bottom"]["lcost"], r["flat"]["top"]["lcost"])
    cells[(r["u"], r["n"])][r["phi"]] = dict(worst=worst, flat=flat, flat_bottom=r["flat"]["bottom"]["lcost"], a=r["a"],
                                              claimed=r["claimed_exponent"], lCmax=r["constants"]["lCmax"])
trend = defaultdict(list)
for (u, n) in sorted(cells):
    c = cells[(u, n)]
    phi = min(c, key=lambda p: c[p]["worst"])
    x = c[phi]
    na = n * x["a"]
    trend[u].append(dict(n=n, phi=phi, worst=x["worst"] / na, claimed=x["claimed"] / x["a"],
                         diff=x["worst"] / na - x["claimed"] / x["a"], cap=x["lCmax"] / na, a=x["a"],
                         flat_at_phi=x["flat"] / na))
out = {}
for u, t in trend.items():
    print(f"\nu = {u}")
    print("   n     phi   worst/(na)  claimed/a   diff     diff*sqrt(n)  diff*n^0.75  local exponent")
    prev = None
    for x in t:
        loc = "" if prev is None else f"{-math.log(x['diff'] / prev['diff']) / math.log(x['n'] / prev['n']):.3f}"
        print(f"{x['n']:7d} {x['phi']:.2f}  {x['worst']:.4f}     {x['claimed']:.4f}   {x['diff']:+.4f}   "
              f"{x['diff'] * math.sqrt(x['n']):7.2f}      {x['diff'] * x['n'] ** 0.75:8.2f}    {loc}")
        prev = x
    n = np.array([x["n"] for x in t], float)
    d = np.array([x["diff"] for x in t], float)
    res = {}
    def fit(name, cols, mask=None, logspace=True):
        m = np.ones(len(n), bool) if mask is None else mask
        A = np.column_stack([c(n[m]) for c in cols])
        # relative least squares: minimise sum ((model - d)/d)^2
        Aw = A / d[m][:, None]
        coef, *_ = np.linalg.lstsq(Aw, np.ones(m.sum()), rcond=None)
        pred = A @ coef
        rel = (pred - d[m]) / d[m]
        res[name] = dict(coef=[float(c) for c in coef], rms_rel=float(np.sqrt((rel ** 2).mean())), max_rel=float(np.abs(rel).max()),
                         npts=int(m.sum()), npar=len(cols))
        return res[name]
    for label, mask in (("all 13 sizes", None), ("n >= 4000 (phi fixed at 0.50)", n >= 4000)):
        m = np.ones(len(n), bool) if mask is None else mask
        # (1) pure power law, free exponent: log-log linear regression
        X = np.column_stack([np.ones(m.sum()), np.log(n[m])])
        beta, *_ = np.linalg.lstsq(X, np.log(d[m]), rcond=None)
        r = np.log(d[m]) - X @ beta
        s2 = (r ** 2).sum() / (m.sum() - 2)
        se = math.sqrt(s2 * np.linalg.inv(X.T @ X)[1, 1])
        print(f"  [{label}] power law C n^-p: p = {-beta[1]:.3f} +- {se:.3f} (log-log OLS), rms rel residual {math.sqrt((r**2).mean()):.3f}")
        f1 = fit(f"A/sqrt(n) | {label}", [lambda x: x ** -0.5], mask)
        f2 = fit(f"A/sqrt(n) + B/n | {label}", [lambda x: x ** -0.5, lambda x: x ** -1.0], mask)
        f3 = fit(f"(A + B ln n)/sqrt(n) | {label}", [lambda x: x ** -0.5, lambda x: np.log(x) * x ** -0.5], mask)
        f4 = fit(f"A/n^(2/3) | {label}", [lambda x: x ** (-2 / 3)], mask)
        f5 = fit(f"A/n^(3/4) | {label}", [lambda x: x ** -0.75], mask)
        f6 = fit(f"A ln n / n | {label}", [lambda x: np.log(x) / x], mask)
        f7 = fit(f"A/sqrt(n) + B ln n/n | {label}", [lambda x: x ** -0.5, lambda x: np.log(x) / x], mask)
        for k, v in res.items():
            if k.endswith(label):
                print(f"     {k:55s} coef={['%.4g' % c for c in v['coef']]} rms rel {v['rms_rel']:.3f} max rel {v['max_rel']:.3f}")
    out[str(u)] = dict(trend=t, fits=res)
json.dump(out, open("out_x005_refit.json", "w"), indent=1)
