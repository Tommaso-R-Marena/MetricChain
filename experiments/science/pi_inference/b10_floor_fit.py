#!/usr/bin/env python3
"""Benchmark B10 / addendum A17 (12), item 24: THE FLOOR HAS ITS OWN FIT -- coordinator's script.

For an exponential family q_theta (independent residues; nearest-neighbour chain) and every Renyi order p > 1,
    D_p(pi_g || q_theta) = (1/(p-1)) ln sum_x exp(p ln pi_g(x) - (p-1) s_theta(x)) + ln Z_theta
is CONVEX in theta (a log-sum-exp of affine functions plus a log-partition function).  So the least-D_p fits are convex
programmes for all p in (1, infinity], the maximum-likelihood fit is their limit p -> 1, and p = infinity is the fit that
minimises the floor D_inf = ln max pi_g/q.  (Only the variational fit, least KL(q || pi_g), is not convex.  The header of
b10_fit_directions.py calls the least-D_2 fit non-convex: that was wrong; its two starts agreed because it is convex.)

This script follows p = 2, 4, 8, ..., 256 with warm starts (L-BFGS, exact sums) on the enumerated instances with at most
BIG states, and reports for each (instance, family):
  D_inf and D_2 of the least-D_2 fit (CHI) and of the least-D_256 fit;
  a certified bracket for the least possible floor in the family:   min_q D_256  <=  min_q D_inf  <=  D_inf(least-D_256 fit)
  (the left inequality because D_p <= D_inf for every q; the minimisation of D_256 is convex, its value is that of a
  converged quasi-Newton run and is reported with the norm of the gradient).
Run:  python3 -u b10_floor_fit.py > b10_floor_fit.log        (one core)
"""
import os, sys, math, json, time
import numpy as np
from scipy.optimize import minimize
from scipy.special import logsumexp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ws_P2")); sys.path.insert(0, HERE)
import anlib
from b10_fit_directions import Family, BETA
BIG = 60000
PS = (2, 4, 8, 16, 32, 64, 128, 256)


def fit_dp(fam, lpg, p, th0, maxiter=600):
    def fun(th):
        s = fam.score(th); lz = logsumexp(s); q = np.exp(s - lz)
        a = p * lpg - (p - 1) * s
        la = logsumexp(a); w = np.exp(a - la)
        val = la / (p - 1) + lz
        grad = fam.moments(q) - fam.moments(w)
        return float(val), grad
    res = minimize(fun, th0, jac=True, method="L-BFGS-B", options=dict(maxiter=maxiter, maxfun=2 * maxiter, ftol=1e-15, gtol=1e-10))
    v, g = fun(res.x)
    return res.x, v, float(np.max(np.abs(g)))


def divs(fam, lpg, th):
    lq = fam.logq(th)
    return float(logsumexp(2 * lpg - lq)), float(np.max(lpg - lq))


if __name__ == "__main__":
    t0 = time.time(); rows = []
    tags = []
    for aa, ns in (("V", (2, 4, 6, 8, 10, 12)), ("L", (2, 4, 6, 8)), ("S", (2, 3, 4, 5, 6))):
        for bb in ("E", "P2", "H"):
            for n in ns:
                t = f"fb_{aa}{n}_{bb}_R3_t0.60"
                if os.path.exists(os.path.join(HERE, "..", "ws_P2", "data", t + ".npz")): tags.append(t)
    assert len(tags) == 45
    print("# instance family | least-D_2 fit: D_2, D_inf | least-D_256 fit: D_2, D_inf | least possible floor in the family: [min D_256, D_inf(fit)] | floor gained over least-D_2 | D_2 paid | max |grad| at p = 256", flush=True)
    skipped = []
    for tag in tags:
        d = anlib.load_fb(tag)
        g = (d["tors"] + d["lj"] + d["coul"] + d["gb"]).ravel()
        if g.size > BIG: skipped.append(tag); continue
        betag = BETA * (g - g.min()); lpg = -betag - logsumexp(-betag)
        for famname, chain in (("product", False), ("chain", True)):
            fam = Family(d["shape"], chain)
            th = np.zeros(fam.P); out = {}
            for p in PS:
                th, v, gn = fit_dp(fam, lpg, p, th)
                out[p] = (v, gn) + divs(fam, lpg, th)
            d2c, dic = out[2][2], out[2][3]; v256, g256, d2f, dif = out[256]
            name = d["seq"][:1] + str(d["n"]) + "_" + d["bb"]
            # orderings that must hold up to the optimiser's tolerance: min_q D_2 <= min_q D_256 <= D_inf(fit)
            order_defect = max(v256 - dif, out[2][0] - v256, 0.0)
            assert order_defect < 1e-5, (name, famname, order_defect)
            rows.append(dict(order_defect=order_defect, tag=tag, name=name, family=famname, N=fam.N, D2_chi=d2c, Dinf_chi=dic, D2_p256=d2f, Dinf_p256=dif, minD256=v256, grad256=g256,
                             path={str(p): out[p][:4] for p in PS}))
            print(f"{name:8s} {famname:7s} | {d2c:10.3e} {dic:8.4f} | {d2f:10.3e} {dif:8.4f} | [{v256:8.4f}, {dif:8.4f}] | {dic - dif:8.4f} | {d2f - d2c:10.3e} | {g256:.1e}", flush=True)
    nt = [r for r in rows if r["D2_chi"] >= 1e-3 or r["Dinf_chi"] >= 0.05]
    gain = np.array([r["Dinf_chi"] - r["Dinf_p256"] for r in nt]); pay = np.array([r["D2_p256"] - r["D2_chi"] for r in nt]); width = np.array([r["Dinf_p256"] - r["minD256"] for r in nt])
    rel = np.array([r["Dinf_p256"] / r["Dinf_chi"] for r in nt])
    print(f"# summary over the {len(nt)} (instance, family) pairs with D_2 >= 1e-3 or D_inf >= 0.05 for the least-D_2 fit ({len(rows)} pairs run; skipped above {BIG} states: {[t.split('_')[1] + '_' + t.split('_')[2] for t in skipped]})")
    print(f"#   floor of the least-D_256 fit / floor of the least-D_2 fit: min {rel.min():.3f} median {np.median(rel):.3f} max {rel.max():.3f}")
    print(f"#   floor gained (nats): median {np.median(gain):.3f}, max {gain.max():.3f};  D_2 paid: median {np.median(pay):.2e}, max {pay.max():.2e}")
    print(f"#   width of the bracket for the least possible floor: median {np.median(width):.3f}, max {width.max():.3f}")
    print(f"#   largest gradient norm at p = 256: {max(r['grad256'] for r in rows):.1e};  largest defect of the ordering min D_2 <= min D_256 <= D_inf(fit) (optimiser tolerance; families that contain the truth exactly): {max(r['order_defect'] for r in rows):.1e}")
    json.dump(rows, open(os.path.join(HERE, "b10_floor_fit.json"), "w"))
    print(f"ALL DONE {len(rows)} rows, {time.time() - t0:.0f} s")
