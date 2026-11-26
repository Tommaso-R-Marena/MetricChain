#!/usr/bin/env python3
"""Addendum A17 (15): A COMPACT ENSEMBLE THAT IS NOT FROZEN -- serine on the helix: do pair or triple shares, or ANY share
allocation, rescue the certificate?  -- coordinator's script.

For Ace-Ser_n-NMe on the helix (n = 4, 5, 6; enumerated: 2 916, 17 496, 104 976 assignments; 9 or 6 rotamer states per
site) and, for comparison, on the strand, at the orders for which workstream P6 left pair sums and balls on disk:
  (1) the widths ln Z(m_-) - ln Z(m_+) of the banded sandwiches of workstreams P3 (site form) and P6 (pair form, triple
      form), all pairs and triples in band -- the models a certificate can actually use (pairwise / three-site, exactly
      solvable; they contain P3's reduction of the evaluated three-site terms);
  (2) by enumeration, with the evaluated terms kept EXACT (no reduction): the brackets from f + I_{m-1} g -/+ penalty for
      the site, pair and triple penalties and for the ENVELOPE  sum_{T subset of S(x)} chat_T  itself -- the pointwise
      smallest penalty that the certified constants allow, hence a lower limit for every share allocation;
  (3) the exact ln Z, the mean number of side chains off the anchor under the true ensemble, and the true remainder.
Inputs taken as given: P3's certified constants, the enumerated energies (P6's caches).  Model-relative.
Inputs that are NOT tracked in the repository (regenerable; see experiments/science/.gitignore):
  ../ws_P6/out/pairsums_<SEQ>_<BB>_t0.70_gbn2_m<m>.npz   -- regenerate with   cd ../ws_P6 && python3 -B p6_01_pairsums.py SEQ BB 0.70 m
  ../ws_P6/cache/enum_*.npy, ball_*.npz                  -- computed by p6lib when absent (needs OpenMM; minutes)
A row whose pair sums are absent is skipped with a message, not guessed.
Run:  python3 -B serine_helix_shares.py > serine_helix_shares.log     (one core; 8 s with the caches present)
"""
import os, sys, math, json, time, itertools, importlib
import numpy as np
from scipy.special import logsumexp
HERE = os.path.dirname(os.path.abspath(__file__))
P6 = os.path.normpath(os.path.join(HERE, "..", "ws_P6"))
sys.path.insert(0, P6)
import p6lib as L
T9 = importlib.import_module("p6_09_triple")
pw = L.pw; BETA = L.BETA


def log(s): print(s, flush=True)


t0 = time.time(); out = []
log("# instance m | off-anchor sites (mean under the true ensemble) | Gamma_m (kT) | true remainder sup (kcal/mol) | banded models, width in nats: site, pair, triple | "
    "exact evaluated terms, width: site, pair, triple, ENVELOPE | exact ln Z inside all")
for seq, bb, tau, ms in (("S4", "H", 0.70, (3, 4)), ("S5", "H", 0.70, (3, 4, 5)), ("S6", "H", 0.70, (4,)),
                         ("S4", "E", 0.70, (3, 4)), ("S5", "E", 0.70, (3, 4, 5)), ("S6", "E", 0.70, (3, 4))):
    sd = L.setup(seq, bb, tau); G, c0, h, J, x0, E0 = sd; n, k = G.ns, list(G.k); w = n - 1
    st, g, src = L.enumerate_g(G, seq, bb, tau, verbose=False)
    f = pw.f_energy(st, c0, h, J); E = f + g
    lnZE = float(logsumexp(-BETA * E)); pE = np.exp(-BETA * E - lnZE)
    nch = (st != np.array(x0)[None]).sum(1); noff = float(pE @ nch)
    for m in ms:
        fn = os.path.join(P6, "out", f"pairsums_{L.tagname(seq, bb, tau)}_m{m}.npz")
        if not os.path.exists(fn):
            log(f"{seq}/{bb} m={m}: no pair sums of workstream P6 on disk -- skipped"); continue
        z = np.load(fn)
        if list(z["anchor"]) != [int(v) for v in x0]:
            log(f"{seq}/{bb} m={m}: anchor differs -- skipped"); continue
        Gam, S, Gp = float(z["Gamma"]), z["S"], z["G"]
        val = {tuple(int(v) for v in e if v >= 0): float(t) for e, t in zip(z["excl"], z["tot"])}
        GF = L.GFBound2(G, x0, L.EnvelopeSup(G), K=m)
        tris = T9.window_triples(n, w)
        H = {}
        if tris:
            se, cr = L.GFBatch(GF).totals(m, tris)
            H = {tr: (val[()] - val[(tr[0],)] - val[(tr[1],)] - val[(tr[2],)] + val[(tr[0], tr[1])] + val[(tr[0], tr[2])] + val[(tr[1], tr[2])]) - float(t3)
                 for tr, t3 in zip(tris, se + cr)}
        d, nball, srcb = L.ball_terms(G, x0, m - 1, seq, bb, tau, verbose=False)
        phi1, psi1, psi2 = L.fp_tables(n, k, x0, m - 1)
        # (1) the banded models
        wid = {}
        gsS, g2S = L.site_form(n, m, S, phi1), np.zeros((n, n))
        gsB, g2B = L.banded_pair_form(n, m, w, S, Gp, psi1, psi2, 5e-9 * Gam)
        for form, (gs, g2) in (("S", (gsS, g2S)), ("B", (gsB, g2B))):
            lo, up = L.build_models(k, x0, c0, h, J, d, w, m - 1, gs, g2)
            ml, mu = lo.energy(st), up.energy(st); assert (ml <= E + 1e-9).all() and (E <= mu + 1e-9).all()
            wid[form] = lo.lnZ() - up.lnZ(); assert up.lnZ() <= lnZE <= lo.lnZ()
        if m >= 3 and tris:
            gsT, g2T, eta = T9.triple_form(n, m, w, Gp, H, psi1, psi2, 5e-9 * Gam, 1e-8 * Gam)
            lo, up = T9.build_triple_models(k, x0, c0, h, J, d, w, m - 1, gsT, g2T, eta)
            ml, mu = lo.energy(st), up.energy(st); assert (ml <= E + 1e-9).all() and (E <= mu + 1e-9).all()
            wid["T"] = lo.lnZ() - up.lnZ(); assert up.lnZ() <= lnZE <= lo.lnZ()
        # (2) exact evaluated terms, penalties without allowances, by enumeration
        Ig = pw.expansion_value(d, st); rem = g - Ig
        z1 = np.zeros(n); z2 = np.zeros((n, n))
        pens = {"site": L.penalty_value(st, x0, L.site_form(n, m, S, z1), z2)}
        gb0, g2b0 = L.banded_pair_form(n, m, w, S, Gp, z1, z2, 0.0); pens["pair"] = L.penalty_value(st, x0, gb0, g2b0)
        if tris:
            g0, g20, eta0 = T9.triple_form(n, m, w, Gp, H, z1, z2, 0.0, 0.0); pens["triple"] = T9.penalty_value3(st, x0, g0, g20, eta0)
        if math.comb(n, m) <= 500:
            chat = L.enum_chat(GF, m); pens["envelope"] = L.envelope_value(st, x0, chat)
        ex = {}
        for key, p in pens.items():
            assert (np.abs(rem) <= p + 1e-8).all(), (seq, bb, m, key)
            a, b = float(logsumexp(-BETA * (f + Ig + p))), float(logsumexp(-BETA * (f + Ig - p)))
            assert a - 1e-9 <= lnZE <= b + 1e-9
            ex[key] = b - a
        row = dict(seq=seq, bb=bb, m=m, states=int(len(st)), n_off=noff, Gamma_kT=BETA * Gam, rem_sup=float(np.abs(rem).max()), banded=wid, exact_terms=ex, lnZ=lnZE, nball=int(nball))
        out.append(row)
        log(f"{seq}/{bb} m={m} ({len(st)} states, ball {nball}) | {noff:.2f} of {n} | {BETA * Gam:8.3f} | {np.abs(rem).max():.2e} | "
            + ", ".join(f"{wid.get(kf, float('nan')):.4g}" for kf in ("S", "B", "T")) + " | "
            + ", ".join(f"{ex.get(kf, float('nan')):.4g}" for kf in ("site", "pair", "triple", "envelope")) + f" | True   [{time.time() - t0:.0f}s]")
json.dump(out, open(os.path.join(HERE, "serine_helix_shares.json"), "w"), indent=1)
log(f"ALL DONE {time.time() - t0:.0f} s")
