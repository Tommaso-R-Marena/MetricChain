#!/usr/bin/env python3
"""Addendum A17 (16), item 41: THREE RULES for the evaluated terms that do not fit a window -- coordinator's script.

Ace-Ser12-NMe on the helix, triple shares, exact window terms; the terms of order >= 3 with max U - min U > w are
replaced by a minimum / maximum over some of their sites according to window_model.build_window_models(reduce=...):
"pair" (workstream P3's rule), "ext" (P3's choice extended to a maximal sub-tuple that fits a window; pointwise at
least as tight as P3's), "best" (the maximal sub-tuple of least sup-norm slack).  All three are valid sandwiches
(window_model_check.py checks them at every state of enumerated instances); this script measures what they gain at a
size that cannot be enumerated.  Needs the caches of serine_helix_reach.py (balls, pair and triple sums) for the
configurations below; a configuration whose caches are absent is skipped with a message.
Run:  python3 -B window_model_rules.py > window_model_rules.log        (one core, a minute)
"""
import os, sys, time, importlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "ws_P6"))); sys.path.insert(0, HERE)
import p6lib as L, window_model
T9 = importlib.import_module("p6_09_triple"); pw = L.pw
CACHE = os.path.join(HERE, "serine_helix_reach_cache"); L.encl.CACHE = CACHE; L.MYCACHE = CACHE
WindowModel, build_window_models, diff_window = window_model.make(pw)
seq, bb, tau = "S12", "H", 0.70
G, c0, h, J, x0, E0 = L.setup(seq, bb, tau); n, k = G.ns, list(G.k)
print("# S12 on the helix, triple form, exact window terms: bracket width in nats by rule for the terms that do not fit a window "
      "(in brackets: the sum of the sup-norm slacks of the reduced terms of the floor, kcal/mol)", flush=True)
for m, w in ((5, 6), (5, 7), (6, 6)):
    t0 = time.time(); M = m - 1
    fp, ft = os.path.join(CACHE, f"pairsums_{seq}_{bb}_m{m}.npz"), os.path.join(CACHE, f"triplesums_{seq}_{bb}_m{m}_w{w}.npz")
    if not (os.path.exists(fp) and os.path.exists(ft)):
        print(f"m = {m}, w = {w}: caches of serine_helix_reach.py absent -- skipped", flush=True); continue
    excl = L.exclusion_sets(n, None); tot_ex = np.load(fp)["tot"]
    Gam, S, Gp = L.assemble_pair_sums(n, m, excl, tot_ex); val = {tuple(e): float(t) for e, t in zip(excl, tot_ex)}
    tris = T9.window_triples(n, w); t3 = np.load(ft)["tot"]
    H = {tr: (val[()] - val[(tr[0],)] - val[(tr[1],)] - val[(tr[2],)] + val[(tr[0], tr[1])] + val[(tr[0], tr[2])] + val[(tr[1], tr[2])]) - float(v)
         for tr, v in zip(tris, t3)}
    phi1, psi1, psi2 = L.fp_tables(n, k, x0, M)
    gs, g2, eta = T9.triple_form(n, m, w, Gp, H, psi1, psi2, 5e-9 * Gam, 1e-8 * Gam)
    d, nball, srcb = L.ball_terms(G, x0, M, seq, bb, tau, verbose=False)
    out = []
    for rule in ("pair", "ext", "best"):
        lo, up, info = build_window_models(k, x0, c0, h, J, d, w, L.EPS_G, M, gs, g2, eta, reduce=rule)
        out.append(f"{rule} {lo.lnZ() - up.lnZ():.6g} [{info['reduced_sup']:.4g}; {info['reduced']} terms]")
    print(f"order {m}, band {w}: " + ";  ".join(out) + f"   [{time.time() - t0:.0f}s]", flush=True)
print("ALL DONE")
