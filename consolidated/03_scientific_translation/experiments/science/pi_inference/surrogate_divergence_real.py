#!/usr/bin/env python3
"""Benchmark B10 (hypothesis H11), real instances -- coordinator's script.

On the enumerated rotamer grids of workstream P2 (ff14SB vacuum energy f as known part, GBn2 polarisation
energy gb as residual, one rotamer variable per residue on a fixed backbone; read-only from
experiments/science/ws_P2/data/): the truth is g = f + gb at 300 K.  For three surrogates m whose remainder
r = beta (g - m) is

   m0 = f                      (the known part alone: remainder = the whole solvent term)
   m1 = f + A1[gb]             (plus the best one-body fit of gb: uniform least squares = ANOVA order 1)
   m2 = f + A2[gb]             (plus the best pairwise fit: ANOVA order 2; m2 is a pairwise model)

compute by exact sums over the grid the numbers addendum A17 says matter and the ones a fit reports:

   rms_m   root-mean-square of r under the surrogate's own Gibbs measure pi_m   (what a fit reports)
   osc     sup r - inf r                                                        (sup-norm width)
   gapV    D_1(pi_m || pi_g)   the Gibbs-Bogoliubov gap (cheap side)
   D1, D2, Dinf   Renyi divergences of the TRUE ensemble from the surrogate     (the certified cost:
           e^{D2}/eps^2 without a hint, e^{Dinf}/eps with one)
   K/2     sum_i c_i^2 / 2, c_i the one-site oscillations of r: the bound of A17.6 IF pi_m were a product
           measure (it is not: f is pairwise) -- reported to see whether the bound is of the right size.

Only instances whose domain is the full product grid are used (Val, Leu, Ser homopeptides; P2 report 2.0).
Units: k_BT at 300 K.  Nothing is sampled.
"""
import os, sys, math, json, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ws_P2"))
import anlib                                           # read-only use of P2's loader and ANOVA fit

BETA = anlib.BETA

def gibbs(E):
    w = np.exp(-BETA * (E - E.min())); return w / w.sum()

def renyi(pg, pm, p):
    w = pg / pm
    if p == 1:
        nz = pg > 0
        return float(np.sum(pg[nz] * np.log(w[nz])))
    if math.isinf(p): return float(np.log(w.max()))
    return float(np.log(np.sum(pm * w**p)) / (p - 1))

def one_site_osc(r):
    """c_i = max over the other coordinates of (max - min) of r along axis i."""
    return np.array([float((r.max(axis=i) - r.min(axis=i)).max()) for i in range(r.ndim)])

def analyse(tag, eps=0.1, max_states=3_000_000):
    d = anlib.load_fb(tag)
    size = int(np.prod(d["shape"]))
    if size > max_states: return None
    f = d["tors"] + d["lj"] + d["coul"]
    gb = d["gb"]
    g = f + gb
    pg = gibbs(g)
    rows = []
    for name, fit in (("m0 = f", np.zeros_like(gb)), ("m1 = f + A1[gb]", anlib.anova_fit(gb, 1)),
                      ("m2 = f + A2[gb]", anlib.anova_fit(gb, 2))):
        m = f + fit
        pm = gibbs(m)
        r = BETA * (g - m)                       # remainder in k_BT
        rc = r - float(np.sum(pm * r))
        rms = math.sqrt(float(np.sum(pm * rc * rc)))
        osc = float(r.max() - r.min())
        gapV = float(np.sum(pm * np.log(pm / pg)))
        D1, D2, Dinf = renyi(pg, pm, 1), renyi(pg, pm, 2.0), renyi(pg, pm, math.inf)
        c = one_site_osc(r)
        rows.append(dict(tag=tag, seq=d["seq"], bb=d["bb"], n=d["n"], states=size, surrogate=name, rms_under_surrogate=rms,
                         osc=osc, gapV=gapV, D1=D1, D2=D2, Dinf=Dinf, K_half=float(c @ c) / 2, c_max=float(c.max()),
                         log10_cost_nohint=(D2 - 2 * math.log(eps)) / math.log(10),
                         log10_cost_hint=(Dinf - math.log(eps)) / math.log(10),
                         log10_states=math.log10(size)))
    return rows

if __name__ == "__main__":
    tags = []
    for aa, ns in (("V", (2, 4, 6, 8, 10, 12)), ("L", (2, 4, 6, 8)), ("S", (2, 3, 4, 5, 6))):
        for bb in ("E", "P2", "H"):
            for n in ns:
                t = f"fb_{aa}{n}_{bb}_R3_t0.60"
                if os.path.exists(os.path.join(HERE, "..", "ws_P2", "data", t + ".npz")): tags.append(t)
    out = []; t0 = time.time()
    print(f"{'instance':<12}{'states':>9}  {'surrogate':<16}{'RMS(pi_m)':>10}{'osc':>8}{'gapV':>9}{'D1':>9}{'D2':>9}{'Dinf':>8}{'K/2':>9}"
          f"{'lg e^D2/eps^2':>15}{'lg e^Dinf/eps':>15}{'lg states':>10}")
    for t in tags:
        rows = analyse(t)
        if rows is None:
            print(f"{t[3:].split('_R3')[0]:<12} skipped (too large)"); continue
        for r in rows:
            print(f"{r['seq'][:1] + str(r['n']) + '_' + r['bb']:<12}{r['states']:>9}  {r['surrogate']:<16}{r['rms_under_surrogate']:>10.3f}{r['osc']:>8.2f}"
                  f"{r['gapV']:>9.4f}{r['D1']:>9.4f}{r['D2']:>9.4f}{r['Dinf']:>8.3f}{r['K_half']:>9.2f}"
                  f"{r['log10_cost_nohint']:>15.2f}{r['log10_cost_hint']:>15.2f}{r['log10_states']:>10.2f}")
        out += rows
    json.dump(out, open(os.path.join(HERE, "surrogate_divergence_real.json"), "w"), indent=1)
    print(f"# {len(out)} rows, {time.time() - t0:.0f} s; energies in k_BT at 300 K; eps = 0.1")
