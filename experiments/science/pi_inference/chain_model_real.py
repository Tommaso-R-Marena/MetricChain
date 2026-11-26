#!/usr/bin/env python3
"""Addendum A17 (9): is a NEAREST-NEIGHBOUR CHAIN enough as the tractable model? -- coordinator's script.

On the enumerated product-domain instances of workstream P2 (Val, Leu, Ser homopeptides): total energy g = f + gb
(ff14SB vacuum + GBn2), ANOVA decomposition of g on the grid (uniform weights):
      g = g0 + sum_i g_i + sum_{i<j} g_ij + (beyond pairwise).
Models (all have exactly computable partition functions at any length by transfer matrices):
      mc(w) = g0 + sum_i g_i + sum_{0 < j-i <= w} g_ij          w = 1: nearest-neighbour chain; w = 2: next-nearest
      m2    = the full pairwise part (w = n-1; tractable only for small tree-width)
For each: remainder r = beta (g - m); under pi_m: floor b = E r - min r, sigma, the Jensen gap K (error of first-order
perturbation theory), the Bennett bracket W(b, sigma^2), and D_2, D_inf of the true ensemble from the model.
Exact sums; b and sigma are the instance's exact values (a test of what a certificate would cost, not a certificate).
"""
import os, sys, math, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ws_P2"))
import anlib
BETA = anlib.BETA

def anova_terms(g):
    n = g.ndim; mu = g.mean()
    main = [g.mean(axis=tuple(a for a in range(n) if a != i), keepdims=True) - mu for i in range(n)]
    pair = {}
    for i in range(n):
        for j in range(i + 1, n):
            pair[(i, j)] = g.mean(axis=tuple(a for a in range(n) if a not in (i, j)), keepdims=True) - mu - main[i] - main[j]
    return mu, main, pair

def W_sharp(b, s2):
    if b < 1e-12 or s2 < 1e-300: return 0.0
    if b > 700.0: return b + math.log(s2 / (b * b + s2))
    return math.log1p((b * b * math.expm1(-s2 / b) + s2 * math.expm1(b)) / (b * b + s2))

def analyse(tag):
    d = anlib.load_fb(tag)
    g = d["tors"] + d["lj"] + d["coul"] + d["gb"]
    n = g.ndim
    mu, main, pair = anova_terms(g)
    pg = np.exp(-BETA * (g - g.min())); pg /= pg.sum()
    rows = []
    for w in (1, 2, n - 1):
        if w > n - 1 or (w == 2 and n < 4): continue
        m = np.full(g.shape, mu)
        for t in main: m = m + t
        for (i, j), t in pair.items():
            if j - i <= w: m = m + t
        pm = np.exp(-BETA * (m - m.min())); pm /= pm.sum()
        r = BETA * (g - m); Er = float(np.sum(pm * r)); rc = r - Er
        s2 = float(np.sum(pm * rc * rc)); b = float(-rc.min())
        K = float(np.log1p(np.sum(pm * np.expm1(-rc))))
        ww = pg / pm
        rows.append(dict(tag=tag, seq=d["seq"], bb=d["bb"], n=n, model=("pairwise" if w == n - 1 else f"chain w={w}"), b=b, sigma=math.sqrt(s2),
                         width=float(r.max() - r.min()), K=K, W=W_sharp(b, s2), D2=float(np.log(np.sum(pm * ww * ww))), Dinf=float(np.log(ww.max()))))
    return rows

if __name__ == "__main__":
    out = []
    print(f"{'instance':<10}{'model':<12}{'floor b':>9}{'sigma':>8}{'width':>8} | {'K':>10}{'Bennett W':>11}{'D2':>10}{'Dinf':>8}")
    for aa, ns in (("V", (6, 8, 10, 12)), ("L", (6, 8)), ("S", (4, 5, 6))):
        for bb in ("E", "P2", "H"):
            for nres in ns:
                t = f"fb_{aa}{nres}_{bb}_R3_t0.60"
                if not os.path.exists(os.path.join(HERE, "..", "ws_P2", "data", t + ".npz")): continue
                for r in analyse(t):
                    print(f"{aa + str(nres) + '_' + bb:<10}{r['model']:<12}{r['b']:>9.3f}{r['sigma']:>8.4f}{r['width']:>8.2f} | {r['K']:>10.3e}{r['W']:>11.3e}{r['D2']:>10.3e}{r['Dinf']:>8.3f}", flush=True)
                    out.append(r)
    json.dump(out, open(os.path.join(HERE, "chain_model_real.json"), "w"), indent=1)
    print(f"# {len(out)} rows; energies in k_BT at 300 K")
