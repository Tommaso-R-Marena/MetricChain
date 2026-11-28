#!/usr/bin/env python3
"""Phase II, exploratory [N]: the flat hiding family (PHASE2_REPORT.md, Corollary A'') for a product
reference Bernoulli(p)^n around tilted baselines w0 = exp(-gamma |x|), against single-type dip
families, at the level of exponents (types on a grid of 121^3 points; crude: values are good to
about 1e-3).

For a query of type omega and a centre of type k obtained from it by i flips 0->1 and j flips
1->0 (fractions of n): the dip of the centre covers the query iff
(u+gamma) i + (u-gamma) j <= -(k ln s1 + (1-k) ln s0)   (masses of the relative cones under mu_{w0});
`flat`  = min over (omega,i,j) of -[ln #centres + ln q(centre)],  q = Bernoulli(theta)^n the hiding law;
`single-type` = max over k of min over (omega,i,j) with that k of [h(k) - ln #centres].
Not checked against Theorem 11.59 of the theory report.   Output: out_p2_field_flat.txt
"""
import numpy as np, math
def h2(x):
    x = np.clip(x, 1e-300, 1 - 1e-16)
    return -x*np.log(x) - (1-x)*np.log(1-x)
def setup(p, u, gam):
    lp = math.log(p/(1-p)) - gam                    # logit of p' = law of mu_{w0}, w0 = e^{-gam|x|}
    pp = 1/(1+math.exp(-lp))
    s1 = pp + (1-pp)*math.exp(-(u+gam)); s0 = (1-pp) + pp*math.exp(-(u-gam))
    lam = (1-math.exp(-(u+gam)))/(1-math.exp(-(u-gam)))      # lambda_1/lambda_0
    th = lam*s1/(lam*s1 + s0)
    return pp, s1, s0, th
def exps(p, u, gam, G=121):
    pp, s1, s0, th = setup(p, u, gam)
    W = np.linspace(0, 1, G)[:, None, None]          # omega: type of the query
    A = np.linspace(0, 1, G)[None, :, None]          # i = A*(1-omega)
    B = np.linspace(0, 1, G)[None, None, :]          # j = B*omega
    i = A*(1-W); j = B*W; k = W - j + i
    feas = (u+gam)*i + (u-gam)*j <= -(k*math.log(s1) + (1-k)*math.log(s0)) + 1e-12
    cnt = (1-W)*h2(A) + W*h2(B)                      # ln #centres (type k) at (i,j) from x, per site
    lq = k*math.log(th) + (1-k)*math.log(1-th)
    flat = np.where(feas, -(cnt + lq), np.inf).min()
    # single-type families: for each k, min over feasible (omega,i,j) with that k of h(k) - cnt
    kb = np.clip(np.rint(k*(G-1)).astype(int), 0, G-1)
    val = np.where(feas, h2(k) - cnt, np.inf)
    best_per_k = np.full(G, np.inf)
    np.minimum.at(best_per_k, kb.ravel(), val.ravel())
    best_per_k[~np.isfinite(best_per_k)] = 0.0
    kk = int(np.argmax(best_per_k))
    return flat, best_per_k[kk], kk/(G-1), th
for (p, u) in [(0.5, 1.0), (0.3, 1.0), (0.1, 2.0)]:
    print("p=%.2f u=%.1f   gamma, flat exponent, single-type exponent (best type), theta_flat" % (p, u))
    res = []
    for gam in np.linspace(-0.95*u, 0.95*u, 39):
        f, r, kk, th = exps(p, u, gam)
        res.append((gam, f, r, kk, th))
    for row in res[::3]:
        print("   %+.3f  %.5f  %.5f (%.3f)  %.3f" % row)
    bf = max(res, key=lambda t: t[1]); br = max(res, key=lambda t: t[2])
    print("  max flat  = %.5f at gamma=%+.3f (single-type there %.5f)" % (bf[1], bf[0], bf[2]))
    print("  max single-type = %.5f at gamma=%+.3f (flat there %.5f)" % (br[2], br[0], br[1]))
