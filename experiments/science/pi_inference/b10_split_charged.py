#!/usr/bin/env python3
"""Benchmark B10 / addendum A17 (12), item 25: THE SPLIT FOR CHARGED AND AROMATIC SIDE CHAINS -- coordinator's script.

The 29 instances of surrogate_divergence_real2.py (poly-Lys 2-4, poly-Phe 4-8, the mixed sequence LKSELK 3-6; three
backbones), on their clash-free domains X_tau = {two-site clash score > 0.6} -- NOT products, taken by mask (not the
greedily pruned products of workstream P2).  All laws live on X_tau.  Models of the solvated ensemble pi_g
(g = ff14SB vacuum energy f + GBn2 term), by exact sums:
    m0, m1, m2      from the stored results of surrogate_divergence_real2.py (f alone; f + one-body fit of gb; f + pairwise
                    fit of gb), with m0 recomputed here as a check;
    product, chain  exponential families on X_tau,  q(x) proportional to exp(sum_i a_i(x_i) [+ sum_i b_i(x_i, x_{i+1})]) for x in X_tau,
                    fitted to the solvated energy by maximum likelihood (least KL(pi_g || q): convex, L-BFGS) and, for the
                    instances with at most FLOOR_MAX states, by the floor fit (least D_p, p = 2 ... 256, convex).
(On a masked domain these families are not exactly sampleable by transfer matrices -- the mask couples the sites.  The
numbers say how far the solvated ensemble is from "independent residues given the clash constraints", i.e. what the
split costs; they are not a recipe.)
Run:  python3 -u b10_split_charged.py > b10_split_charged.log      (one core)
"""
import os, sys, math, json, time
import numpy as np
from scipy.optimize import minimize
from scipy.special import logsumexp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ws_P2")); sys.path.insert(0, HERE)
import anlib
from b10_fit_directions import Family, BETA
from b10_floor_fit import fit_dp, divs
TAU = 0.6; FLOOR_MAX = 60000


def masked_family(shape, chain, maskflat):
    fam = Family(shape, chain)
    fam.cols = [c[maskflat] for c in fam.cols]; fam.N = int(maskflat.sum()); fam._A = None
    return fam


def fit_ml(fam, lpg):
    pg = np.exp(lpg); mg = fam.moments(pg)
    def fun(th):
        s = fam.score(th); lz = logsumexp(s); q = np.exp(s - lz)
        return float(lz - pg @ s), fam.moments(q) - mg          # = KL(pi_g || q) - const
    res = minimize(fun, np.zeros(fam.P), jac=True, method="L-BFGS-B", options=dict(maxiter=1500, maxfun=3000, ftol=1e-15, gtol=1e-10))
    v, g = fun(res.x)
    return res.x, float(np.max(np.abs(g)))


if __name__ == "__main__":
    t0 = time.time()
    old = json.load(open(os.path.join(HERE, "surrogate_divergence_real2.json")))
    oldd = {(r["tag"], r["surrogate"].split(" ")[0]): r for r in old}
    tags = [f"fb_K{n}_{bb}_R3_t0.60" for bb in ("E", "P2", "H") for n in (2, 3, 4)]
    tags += [f"fb_F{n}_{bb}_R3_t0.60" for bb in ("E", "P2", "H") for n in (4, 6, 8)]
    tags += [f"fb_LKSEc{n}_{bb}_R3_t0.60" for bb in ("E", "P2", "H") for n in (3, 4, 5, 6)]
    tags = [t for t in tags if os.path.exists(os.path.join(HERE, "..", "ws_P2", "data", t + ".npz"))]
    assert len(tags) == 29, len(tags)
    rows = []
    print("# instance states | D_2 [D_inf]: m0 = vacuum f alone | m1 = f + one-body fit of gb | independent residues on X_tau, ML fit of g | chain on X_tau, ML fit of g | m2 = f + pairwise fit of gb"
          " || floor fits (<= %d states): product D_inf, chain D_inf | check: m0 recomputed - stored | max |grad| of the ML fits" % FLOOR_MAX, flush=True)
    for tag in tags:
        d = anlib.load_fb(tag); mask = d["s2min"] > TAU; mf = mask.ravel()
        f = (d["tors"] + d["lj"] + d["coul"])[mask]; gb = d["gb"][mask]; g = f + gb
        bg = BETA * (g - g.min()); lpg = -bg - logsumexp(-bg)
        bf = BETA * (f - f.min()); lpf = -bf - logsumexp(-bf)
        d2_m0 = float(logsumexp(2 * lpg - lpf)); dinf_m0 = float(np.max(lpg - lpf))
        o0, o1, o2 = oldd[(tag, "m0")], oldd[(tag, "m1")], oldd[(tag, "m2")]
        chk = max(abs(d2_m0 - o0["D2"]), abs(dinf_m0 - o0["Dinf"]))
        assert chk < 1e-6 * max(1.0, abs(o0["D2"])), (tag, d2_m0, o0["D2"])
        res = dict(tag=tag, seq=d["seq"], bb=d["bb"], n=d["n"], states=int(mf.sum()), D2_m0=d2_m0, Dinf_m0=dinf_m0,
                   D2_m1=o1["D2"], Dinf_m1=o1["Dinf"], D2_m2=o2["D2"], Dinf_m2=o2["Dinf"])
        gr = 0.0
        for famname, chain in (("product", False), ("chain", True)):
            fam = masked_family(d["shape"], chain, mf)
            th, gn = fit_ml(fam, lpg); gr = max(gr, gn)
            d2, di = divs(fam, lpg, th); res["D2_" + famname] = d2; res["Dinf_" + famname] = di
            if fam.N <= FLOOR_MAX:
                thp = th.copy(); v = None
                for p in (2, 4, 8, 16, 32, 64, 128, 256):
                    thp, v, _ = fit_dp(fam, lpg, p, thp)
                d2f, dif = divs(fam, lpg, thp); res["Dinf_floor_" + famname] = dif; res["D2_floor_" + famname] = d2f; res["minD256_" + famname] = v
        res["grad_ml"] = gr; rows.append(res)
        name = ("K" if d["seq"][0] == "K" else "F" if d["seq"][0] == "F" else "LKSE:") + str(d["n"]) + "_" + d["bb"]
        res["name"] = name
        fl = (f"{res['Dinf_floor_product']:.3f}, {res['Dinf_floor_chain']:.3f}" if "Dinf_floor_product" in res else "--")
        print(f"{name:9s} {res['states']:7d} | {d2_m0:8.3f} [{dinf_m0:7.2f}] | {o1['D2']:8.3f} [{o1['Dinf']:6.2f}] | {res['D2_product']:8.4f} [{res['Dinf_product']:6.2f}] | "
              f"{res['D2_chain']:9.2e} [{res['Dinf_chain']:6.2f}] | {o2['D2']:9.2e} [{o2['Dinf']:5.2f}] || {fl} | {chk:.1e} | {gr:.1e}", flush=True)
    for fam_label, sel in (("poly-Lys", lambda r: r["seq"][0] == "K" and set(r["seq"]) == {"K"}), ("poly-Phe", lambda r: set(r["seq"]) == {"F"}), ("LKSELK", lambda r: len(set(r["seq"])) > 1)):
        rr = [r for r in rows if sel(r)]
        if not rr: continue
        f = lambda key: f"{min(r[key] for r in rr):.3g}..{max(r[key] for r in rr):.3g}"
        print(f"# {fam_label} ({len(rr)} instances): D_2  m0 {f('D2_m0')} | m1 {f('D2_m1')} | product {f('D2_product')} | chain {f('D2_chain')} | m2 {f('D2_m2')};   "
              f"D_2(m1)/D_2(product): {min(r['D2_m1'] / r['D2_product'] for r in rr):.2f}..{max(r['D2_m1'] / r['D2_product'] for r in rr):.2f};  D_2(m0)/D_2(product): {min(r['D2_m0'] / r['D2_product'] for r in rr):.1f}..{max(r['D2_m0'] / r['D2_product'] for r in rr):.1f}")
    json.dump(rows, open(os.path.join(HERE, "b10_split_charged.json"), "w"))
    print(f"ALL DONE {len(rows)} instances, {time.time() - t0:.0f} s")
