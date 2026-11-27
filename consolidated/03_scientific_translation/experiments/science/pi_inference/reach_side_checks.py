#!/usr/bin/env python3
"""Addendum A17 (16), items 44 and 46: two side checks by exhaustive enumeration -- coordinator's script.

(1) Small helices of every residue type: the certified constant Gamma_m of workstream P3 against the largest TRUE
    remainder sup_x |g - I_{m-1} g| and its root mean square under the true ensemble, per order.  (The ratio is of the
    same size for all types; the truth is larger for the charged ones.)
(2) Ace-Leu12-NMe on the helix: why no cheap floor exists far from the anchor -- the range of the known part f and of
    the solvent term g by number of flipped side chains, against the certified constants of orders 1..4.
Inputs: workstream P6's library and caches (enumerations are computed by it when absent); P3's constants.
Run:  python3 -B reach_side_checks.py > reach_side_checks.log       (one core, under a minute with the caches)
"""
import os, sys, time
import numpy as np
from scipy.special import logsumexp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "ws_P6")))
import p6lib as L
pw = L.pw; BETA = L.BETA
CACHE = os.path.join(HERE, "serine_helix_reach_cache"); os.makedirs(CACHE, exist_ok=True)
L.MYCACHE = CACHE          # balls evaluated here are cached in this script's directory, not in a workstream's


def log(s): print(s, flush=True)


t0 = time.time()
log("# (1) instance | states | off the anchor (mean) | per order m: Gamma_m (kcal/mol) | sup |g - I_{m-1} g| (kcal/mol) | ratio | rms of the remainder under the true ensemble")
for seq, tau in (("K3", 0.70), ("K4", 0.70), ("LKSE:4", 0.60), ("LKSE:5", 0.60), ("S4", 0.70), ("S5", 0.70), ("L6", 0.60)):
    G, c0, h, J, x0, E0 = L.setup(seq, "H", tau); n, k = G.ns, list(G.k)
    st, g, src = L.enumerate_g(G, seq, "H", tau, verbose=False)
    f = pw.f_energy(st, c0, h, J); E = f + g; pE = np.exp(-BETA * E - logsumexp(-BETA * E))
    noff = float(pE @ (st != np.array(x0)[None]).sum(1)); cells = []
    for m in range(2, n + 1):
        d, nball, srcb = L.ball_terms(G, x0, m - 1, seq, "H", tau, verbose=False)
        rem = g - pw.expansion_value(d, st)
        GF = L.GFBound2(G, x0, L.EnvelopeSup(G), K=m); se, cr = L.GFBatch(GF).totals(m, [()]); Gam = float(se[0] + cr[0])
        assert np.abs(rem).max() <= Gam + 1e-9, (seq, m)
        cells.append(f"m={m}: {Gam:.4g} | {np.abs(rem).max():.3g} | {Gam / np.abs(rem).max():.3g} | {float(np.sqrt(pE @ rem ** 2)):.2g}")
    log(f"{seq}/H ({len(st)} states, k = {k}; {noff:.2f} of {n} off) || " + " || ".join(cells) + f"  [{time.time() - t0:.0f}s]")
log("# (2) Leu12 on the helix (4096 states, exact enumeration)")
G, c0, h, J, x0, E0 = L.setup("L12", "H", 0.60); n = G.ns
st, g, src = L.enumerate_g(G, "L12", "H", 0.60, verbose=False)
f = pw.f_energy(st, c0, h, J); E = f + g; t = (st != np.array(x0)[None]).sum(1); i0 = int(np.where(t == 0)[0][0])
log(f"exact ln Z = {float(logsumexp(-BETA * E)):.6f}; the solvent term over all states: g - g(anchor) in [{(g - g[i0]).min():.2f}, {(g - g[i0]).max():.2f}] kcal/mol; "
    f"all twelve flipped: E - E(anchor) = {float(E[t == n][0] - E[i0]):.2f} kcal/mol = {float(E[t == n][0] - E[i0]) * BETA:.1f} kT")
for tt in range(0, n + 1, 2):
    sel = t == tt
    log(f"   {tt:2d} flips ({int(sel.sum()):4d} states): f - f(anchor) in [{(f[sel] - f[i0]).min():7.2f}, {(f[sel] - f[i0]).max():7.2f}]   g - g(anchor) in "
        f"[{(g[sel] - g[i0]).min():6.2f}, {(g[sel] - g[i0]).max():6.2f}]   E - E(anchor) >= {(E[sel] - E[i0]).min():6.2f} kcal/mol")
cells = []
for m in (1, 2, 3, 4):
    GF = L.GFBound2(G, x0, L.EnvelopeSup(G), K=m); se, cr = L.GFBatch(GF).totals(m, [()])
    cells.append(f"Gamma_{m} = {se[0] + cr[0]:.4g} kcal/mol ({(se[0] + cr[0]) * BETA:.4g} kT)")
log("   certified constants: " + "; ".join(cells))
log(f"ALL DONE {time.time() - t0:.0f} s")
