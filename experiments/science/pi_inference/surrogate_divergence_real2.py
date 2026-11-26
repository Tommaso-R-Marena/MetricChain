#!/usr/bin/env python3
"""Benchmark B10 (hypothesis H11), real instances, part 2 -- coordinator's script.

The same quantities as surrogate_divergence_real.py on the instances of workstream P2 whose domain is NOT a product
(pairs of rotamers that clash are excluded: X_tau = {two-site clash score > tau}, tau = 0.6, P2 report section 2.0):
poly-lysine (charged), poly-phenylalanine, and the mixed sequence LKSELK.  Surrogates: m0 = f (ff14SB vacuum energy),
m1 = f + best one-body least-squares fit of the GBn2 term on the domain, m2 = f + best pairwise fit (sparse least
squares, P2's design/fit_ls).  All Gibbs measures live on X_tau.  Energies in k_BT at 300 K.  Exact sums; nothing sampled.
"""
import os, sys, math, json, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ws_P2"))
import anlib
BETA = anlib.BETA; TAU = 0.6

def gibbs_vec(E):
    w = np.exp(-BETA * (E - E.min())); return w / w.sum()

def renyi(pg, pm, p):
    w = pg / pm
    if p == 1:
        nz = pg > 0; return float(np.sum(pg[nz] * np.log(w[nz])))
    if math.isinf(p): return float(np.log(w.max()))
    return float(np.log(np.sum(pm * w**p)) / (p - 1))

def analyse(tag, eps=0.1):
    d = anlib.load_fb(tag)
    mask = d["s2min"] > TAU
    st = np.argwhere(mask)
    f = (d["tors"] + d["lj"] + d["coul"])[mask]
    gb = d["gb"][mask]
    g = f + gb
    pg = gibbs_vec(g)
    rows = []
    fits = [("m0 = f", np.zeros_like(gb))]
    for order, name in ((1, "m1 = f + LS1[gb]"), (2, "m2 = f + LS2[gb]")):
        if order == 2 and d["n"] < 2: continue
        A = anlib.design(st, d["shape"], anlib.subsets_of_order(d["n"], order))
        fits.append((name, anlib.fit_ls(A, gb)))
    for name, fit in fits:
        m = f + fit
        pm = gibbs_vec(m)
        r = BETA * (g - m)
        rc = r - float(pm @ r)
        rows.append(dict(tag=tag, seq=d["seq"], bb=d["bb"], n=d["n"], states=int(mask.sum()), clash_free=float(mask.mean()),
                         surrogate=name, rms_under_surrogate=math.sqrt(float(pm @ (rc * rc))), osc=float(r.max() - r.min()),
                         gapV=float(np.sum(pm * np.log(pm / pg))), D1=renyi(pg, pm, 1), D2=renyi(pg, pm, 2.0),
                         Dinf=renyi(pg, pm, math.inf)))
    return rows

if __name__ == "__main__":
    tags = [f"fb_K{n}_{bb}_R3_t0.60" for bb in ("E", "P2", "H") for n in (2, 3, 4)]
    tags += [f"fb_F{n}_{bb}_R3_t0.60" for bb in ("E", "P2", "H") for n in (4, 6, 8)]
    tags += [f"fb_LKSEc{n}_{bb}_R3_t0.60" for bb in ("E", "P2", "H") for n in (3, 4, 5, 6)]
    out = []; t0 = time.time()
    print(f"{'instance':<12}{'states':>9}{'free':>6}  {'surrogate':<18}{'RMS(pi_m)':>10}{'osc':>9}{'gapV':>9}{'D1':>9}{'D2':>9}{'Dinf':>9}")
    for t in tags:
        if not os.path.exists(os.path.join(HERE, "..", "ws_P2", "data", t + ".npz")): continue
        rows = analyse(t)
        for r in rows:
            print(f"{r['seq'] + '_' + r['bb']:<12}{r['states']:>9}{r['clash_free']:>6.2f}  {r['surrogate']:<18}{r['rms_under_surrogate']:>10.3f}{r['osc']:>9.2f}"
                  f"{r['gapV']:>9.3f}{r['D1']:>9.3f}{r['D2']:>9.3f}{r['Dinf']:>9.2f}", flush=True)
        out += rows
    json.dump(out, open(os.path.join(HERE, "surrogate_divergence_real2.json"), "w"), indent=1)
    print(f"# {len(out)} rows, {time.time() - t0:.0f} s; energies in k_BT at 300 K; domain = pair-clash-free states")
