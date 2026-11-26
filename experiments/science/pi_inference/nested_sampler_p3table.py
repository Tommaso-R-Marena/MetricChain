#!/usr/bin/env python3
"""The nested sampler (nested_sampler.py, unchanged) with workstream P3's constants taken from a TABLE of all chat_T,
for instances where nested_sampler.py would compute one closed-form sum per distinct changed set -- coordinator's
script for the twenty-residue serine helix.

nested_sampler.Envelope uses a table of all chat_T only when C(n, m) <= 6000 and otherwise one closed-form sum per
distinct changed set among the proposals.  That is right for frozen ensembles (few distinct changed sets: 1 118 for
the twenty-residue valine instance) and wrong for a mobile one: at twenty residues of serine (p = 0.5) nearly every
one of 400 000 proposals has its own changed set, and 400 000 closed-form sums are hours (first run stopped).  Here:
all C(n, m) constants once (workstream P6's closed form with the complement of T excluded -- the same numbers the
table mode of nested_sampler.py uses; cached in serine_helix_reach_cache/chat_<tag>_m<m>.npz in its format), then
everything as in nested_sampler_ext.py: site, pair and in-window triple sums by plain summation (allowance 1e-12
Gamma), the envelope by subset sums over the table, the outer sandwich with the window models and, with
--reduce occ+, the split of the far pairs around the anchor (window_model_occ.py), P3's backward sampler with its
messages computed once.

Run: python3 -B nested_sampler_p3table.py S20 H 5 7 T window --reduce occ+ --N 1200 --Nf 400000 > nested_sampler_S20_H_m5_w7_T_window_p3table_occ.log
"""
import os, sys, math, time, itertools
import numpy as np
import nested_sampler as NS
import nested_sampler_ext as NX
L, pw, T9, window_model = NS.L, NS.pw, NS.T9, NS.window_model
RED = NS.opt(sys.argv, "--reduce", "pair"); assert RED in ("pair", "occ+")


def build_table(seq, bb, m, w, form, models, w3=None):
    assert models == "window" and "--enum" not in sys.argv
    tau = 0.60 if ":" in seq else dict(S=0.70, V=0.70, K=0.70, L=0.60, F=0.60)[seq[0]]
    w3 = w if w3 is None else w3; M = m - 1; t0 = time.time()
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau); n, k = G.ns, list(G.k); x0 = [int(v) for v in x0]
    subs = list(itertools.combinations(range(n), m))
    fn = os.path.join(NS.CACHE, f"chat_{seq.replace(':', 'c')}_{bb}_m{m}.npz")
    if os.path.exists(fn) and list(np.load(fn)["anchor"]) == x0 and len(np.load(fn)["chat"]) == len(subs):
        chat = np.load(fn)["chat"]; srcp = "this script's cache"
    else:
        GF = L.GFBound2(G, x0, L.EnvelopeSup(G), K=m); B = L.GFBatch(GF); out = []
        for s_ in range(0, len(subs), 256):
            ex = [tuple(i for i in range(n) if i not in T) for T in subs[s_:s_ + 256]]
            se, cr = B.totals(m, ex); out.append(se + cr)
            if s_ == 0: NS.log(f"--- table of constants: the first 256 of {len(subs)} closed-form sums took {time.time() - t0:.0f} s")
        chat = np.concatenate(out); np.savez(fn, chat=chat, anchor=np.array(x0)); srcp = f"computed now, {time.time() - t0:.0f} s"
    Gam = float(chat.sum()); S = np.zeros(n); Gp = np.zeros((n, n)); tris = T9.window_triples(n, w3); H = {tr: 0.0 for tr in tris}
    for T, v in zip(subs, chat):
        for i in T: S[i] += v
        for i, j in itertools.combinations(T, 2): Gp[i, j] += v; Gp[j, i] += v
        for tr in itertools.combinations(T, 3):
            if tr in H: H[tr] += v
    absA = 1e-12 * Gam
    d, nball, srcb = L.ball_terms(G, x0, M, seq, bb, tau, verbose=False)
    phi1, psi1, psi2 = L.fp_tables(n, k, x0, M)
    if form == "S": tabs = (L.site_form(n, m, S, phi1), np.zeros((n, n)), None)
    elif form == "B": tabs = L.banded_pair_form(n, m, w, S, Gp, psi1, psi2, absA) + (None,)
    else: tabs = window_model.triple_form_two_windows(T9.window_triples, L.RND, n, m, w, w3, Gp, H, psi1, psi2, absA, absA)
    if RED == "pair":
        lo, up, info = NS.build_window_models(k, x0, c0, h, J, d, w, L.EPS_G, M, *tabs); redtxt = "workstream P3's rule"
    else:
        from window_model_occ import build_window_models_occ, gibbs_sample
        XGo = gibbs_sample(pw, G, c0, h, J, x0, k, L.BETA, np.random.default_rng(4242))
        lo, up, info = build_window_models_occ(NS.WindowModel, k, x0, c0, h, J, d, w, L.EPS_G, M, *tabs, XG=XGo, far_pairs="anchored")
        redtxt = "occupancy-aware rule with the split of the far pairs around the anchor (window_model_occ.py; guiding Gibbs sample of 960 states, seed 4242)"
    diff = NS.diff_window(lo, up); lo.sample = NX.cached_sampler(lo)
    NS.log(f"--- CONSTANTS FROM A TABLE: {len(subs)} constants chat_T of workstream P3's closed form ({srcp}); Gamma_{m} = {L.BETA * Gam:.6g} kT; "
           f"reduction of what does not fit the band: {redtxt}; floor sampler with messages computed once")
    return dict(seq=seq, bb=bb, tau=tau, m=m, M=M, w=w, w3=w3, form=form, models=models, G=G, c0=c0, h=h, J=J, x0=np.array(x0), E0=E0, n=n, k=k,
                GF=None, Gam=Gam, d=d, nball=int(nball), srcb=srcb, srcp=srcp, lo=lo, up=up, diff=diff, info=info, env=NX.TableEnvelope(chat, m, n, x0))


if __name__ == "__main__":
    NS.build = build_table
    a = sys.argv[1:]; seq, bb, m, w, form, models = a[0], a[1], int(a[2]), int(a[3]), a[4], a[5]
    NS.main()
    tagj = f"{seq.replace(':', 'c')}_{bb}_m{m}_w{w}_{form}_{models}"
    os.replace(os.path.join(NS.HERE, f"nested_sampler_{tagj}.json"), os.path.join(NS.HERE, f"nested_sampler_{tagj}_p3table" + ("_occ" if RED != "pair" else "") + ".json"))
