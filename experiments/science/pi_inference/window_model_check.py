#!/usr/bin/env python3
"""Addendum A17 (16), part B: window_model.py against EXHAUSTIVE ENUMERATION -- coordinator's check.

For enumerable instances (serine on the helix and the strand, the orders for which workstream P6's pair sums are on
disk) and for several windows w, with the site, banded pair and banded triple penalties:
  (a) the energies of the floor and ceiling at EVERY state against a direct evaluation that does not use the model
      class:  f + [sum of the in-window d_U, exact] + [P3's minorant/majorant of the others] -/+ penalty -- for the full
      window (w = n - 1) this is  f + I_{m-1} g -/+ penalty -/+ const  with no reduction at all;
  (b) the sandwich  m_- <= E <= m_+  at every state;
  (c) ln Z by the transfer matrix against the sum over all states of the model's own energies;
  (d) for the full window: the bracket widths against the "exact evaluated terms" columns of serine_helix_shares.json
      (computed there by enumeration, without any model class and WITHOUT the two floating-point allowances and the
      constant allowance, which the models here carry: the difference in the last column is their cost);
  (e) P3's/P6's models (with reductions) for the same window, for the gain; both rules for the terms that do not fit
      a window: P3's ("pair"), P3's choice extended to a maximal sub-tuple that fits ("ext": its floor must be pointwise
      at least, its ceiling at most, P3's -- checked at every state), and the maximal sub-tuple of least sup-norm
      slack ("best"); the direct evaluation re-codes each rule independently of window_model.py;
  (f) Lemma A17.16 (the cost of a sandwich is its mean band): with a = beta (E - m_-), b = beta (m_+ - E), <.> the mean
      under the TRUE ensemble and A = sup a,
            <a + b> - <b^2>/2  <=  ln Z(m_-) - ln Z(m_+)  <=  <a + b> + e^A <a^2>/2,
      checked exactly on every sandwich (both the window models and the models with reductions);
  (g) the triple form with two windows (a narrower window w3 for the triples than the band w of the model): the
      sandwich at every state and the exact ln Z inside the bracket, for every w3; with w3 = w the tables of P6.
Run:  python3 -B window_model_check.py > window_model_check.log        (one core, about a minute)
"""
import os, sys, math, json, time, importlib, itertools
import numpy as np
from scipy.special import logsumexp
HERE = os.path.dirname(os.path.abspath(__file__))
P6 = os.path.normpath(os.path.join(HERE, "..", "ws_P6"))
sys.path.insert(0, P6); sys.path.insert(0, HERE)
import p6lib as L
T9 = importlib.import_module("p6_09_triple")
import window_model
pw = L.pw; BETA = L.BETA
WindowModel, build_window_models, diff_window = window_model.make(pw)


def log(s): print(s, flush=True)


t0 = time.time(); worst = dict(a=0.0, c=0.0, d=0.0); viol = 0; ncase = 0; dom_viol = 0; wider = dict(ext=0, best=0, best_vs_ext=0, n=0)
lem = dict(n=0, bad=0, rel_narrow=0.0, rel_all=0.0, slack_lo=float("inf"), slack_up=float("inf"), where_narrow="", rel_full=0.0, where_full="")


def lemma(E, elo, eup, pE, label="", full=False, m=0):
    """exact check of Lemma A17.16 on an enumerated sandwich; returns (D, mean band)."""
    a = BETA * (E - elo); b = BETA * (eup - E)
    D = float(logsumexp(-BETA * elo) - logsumexp(-BETA * eup)); mb = float(pE @ (a + b))
    lo_b = mb - 0.5 * float(pE @ (b * b)); up_b = mb + 0.5 * math.exp(float(a.max())) * float(pE @ (a * a))
    lem["n"] += 1; lem["bad"] += int(not (lo_b - 1e-10 <= D <= up_b + 1e-10))
    lem["slack_lo"] = min(lem["slack_lo"], D - lo_b); lem["slack_up"] = min(lem["slack_up"], up_b - D)
    rel = abs(D - mb) / D; lem["rel_all"] = max(lem["rel_all"], rel)
    if D < 0.5 and rel > lem["rel_narrow"]: lem["rel_narrow"] = rel; lem["where_narrow"] = f"{label}, D = {D:.4g}, <a + b> = {mb:.4g}"
    if m >= 4 and D < 0.5 and rel > lem["rel_full"]: lem["rel_full"] = rel; lem["where_full"] = f"{label}, D = {D:.4g}, <a + b> = {mb:.4g}"
    return D, mb
ref = {(r["seq"], r["bb"], r["m"]): r for r in json.load(open(os.path.join(HERE, "serine_helix_shares.json")))}
log("# instance m w | terms exact / reduced / far pairs | per form (S site, B pair, T triple): width with exact window terms and the rest reduced by the rule "
    "'best', 'ext', 'pair' [width of P3/P6's model, everything of order >= 3 reduced] | max |model energy - direct| | "
    "sandwich violations | |lnZ transfer - lnZ by enumeration| | full window: |width - enumerated exact-terms width|   (the last four for the pair rule; the summary covers all three)")
for seq, bb, tau, ms in (("S4", "H", 0.70, (3, 4)), ("S5", "H", 0.70, (4, 5)), ("S6", "H", 0.70, (4,)), ("S5", "E", 0.70, (4, 5)), ("S6", "E", 0.70, (3, 4))):
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau); n, k = G.ns, list(G.k)
    st, g, src = L.enumerate_g(G, seq, bb, tau, verbose=False)
    f = pw.f_energy(st, c0, h, J); E = f + g
    pE = np.exp(-BETA * E - logsumexp(-BETA * E))
    for m in ms:
        fn = os.path.join(P6, "out", f"pairsums_{L.tagname(seq, bb, tau)}_m{m}.npz")
        if not os.path.exists(fn):
            log(f"{seq}/{bb} m={m}: no pair sums of workstream P6 on disk -- skipped"); continue
        z = np.load(fn); assert list(z["anchor"]) == [int(v) for v in x0]
        Gam, S, Gp = float(z["Gamma"]), z["S"], z["G"]
        val = {tuple(int(v) for v in e if v >= 0): float(t) for e, t in zip(z["excl"], z["tot"])}
        GF = L.GFBound2(G, x0, L.EnvelopeSup(G), K=m)
        d, nball, srcb = L.ball_terms(G, x0, m - 1, seq, bb, tau, verbose=False)
        phi1, psi1, psi2 = L.fp_tables(n, k, x0, m - 1)
        s_ind = (st != np.array(x0)[None])
        for w in sorted({n - 1, max(2, n - 3), 2}):
            tris = T9.window_triples(n, w)
            H = {}
            if tris:
                se, cr = L.GFBatch(GF).totals(m, tris)
                H = {tr: (val[()] - val[(tr[0],)] - val[(tr[1],)] - val[(tr[2],)] + val[(tr[0], tr[1])] + val[(tr[0], tr[2])] + val[(tr[1], tr[2])]) - float(t3)
                     for tr, t3 in zip(tris, se + cr)}
            tabs = {"S": (L.site_form(n, m, S, phi1), np.zeros((n, n)), None)}
            tabs["B"] = tuple(L.banded_pair_form(n, m, w, S, Gp, psi1, psi2, 5e-9 * Gam)) + (None,)
            tabs["T"] = tuple(T9.triple_form(n, m, w, Gp, H, psi1, psi2, 5e-9 * Gam, 1e-8 * Gam))
            cells = []
            for form, rule in [(f_, r_) for f_ in "SBT" for r_ in ("best", "ext", "pair")]:
                gs, g2, eta = tabs[form]
                lo, up, info = build_window_models(k, x0, c0, h, J, d, w, L.EPS_G, m - 1, gs, g2, eta, reduce=rule)
                # (a) direct evaluation without the model class
                pen = L.penalty_value(st, x0, gs, g2) if eta is None else T9.penalty_value3(st, x0, gs, g2, eta)
                base_lo = np.full(len(st), float(d[()])); base_up = base_lo.copy()          # f already contains c0, h and J
                for U, arr in d.items():
                    s = len(U)
                    if s == 0: continue
                    if s == 1:
                        v = arr[st[:, U[0]]]; base_lo += v; base_up += v; continue
                    if U[-1] - U[0] <= w:
                        v = arr[tuple(st[:, u] for u in U)]; base_lo += v; base_up += v; continue
                    # outside the window: P3's reduction, re-coded here independently of the model class
                    for base, sense in ((base_lo, -1), (base_up, +1)):
                        if s == 2:
                            a, b = pw._additive_split(J[U] + arr, sense); base += a[st[:, U[0]]] + b[st[:, U[1]]] - J[U][st[:, U[0]], st[:, U[1]]]
                            continue
                        # P3's choice, re-coded: the in-band pair of least sup-norm slack, else the first site
                        best = None
                        for pa in range(s):
                            for pb in range(pa + 1, s):
                                if U[pb] - U[pa] > w: continue
                                other = tuple(p for p in range(s) if p not in (pa, pb))
                                red = arr.min(axis=other) if sense < 0 else arr.max(axis=other)
                                sl = float(np.abs(arr - np.expand_dims(red, other)).max())
                                if best is None or sl < best[0]: best = (sl, pa, pb, red)
                        if rule in ("best", "ext"):
                            # maximal sub-tuples that fit a window, by brute force over all subsets (independent of window_model.py)
                            fits = [kp for size in range(1, s) for kp in itertools.combinations(range(s), size) if U[kp[-1]] - U[kp[0]] <= w]
                            maxi = [kp for kp in fits if not any(set(kp) < set(k2) for k2 in fits)]
                            must = set() if rule == "best" else (set(best[1:3]) if best is not None else {0})
                            cand = []
                            for kp in maxi:
                                if not must <= set(kp): continue
                                other = tuple(p for p in range(s) if p not in kp)
                                red = arr.min(axis=other) if sense < 0 else arr.max(axis=other)
                                cand.append((float(np.abs(arr - np.expand_dims(red, other)).max()), kp, red))
                            sl_, kp, red = min(cand, key=lambda t_: t_[0])
                            base += red[tuple(st[:, U[p]] for p in kp)]
                            continue
                        if best is not None: base += best[3][st[:, U[best[1]]], st[:, U[best[2]]]]
                        else:
                            other = tuple(range(1, s)); red = arr.min(axis=other) if sense < 0 else arr.max(axis=other); base += red[st[:, U[0]]]
                dlo = f + base_lo - pen - L.EPS_G; dup = f + base_up + pen + L.EPS_G
                elo, eup = lo.energy(st), up.energy(st)
                da = float(max(np.abs(elo - dlo).max(), np.abs(eup - dup).max())); worst["a"] = max(worst["a"], da)
                v = int((elo > E + 1e-9).sum() + (eup < E - 1e-9).sum()); viol += v
                a, b = up.lnZ(), lo.lnZ()
                dc = float(max(abs(a - logsumexp(-BETA * eup)), abs(b - logsumexp(-BETA * elo)))); worst["c"] = max(worst["c"], dc)
                # (e) the models with reductions
                if eta is None: lo0, up0 = L.build_models(k, x0, c0, h, J, d, w, m - 1, gs, g2)
                else: lo0, up0 = T9.build_triple_models(k, x0, c0, h, J, d, w, m - 1, gs, g2, eta)
                w0 = lo0.lnZ() - up0.lnZ()
                lemma(E, elo, eup, pE, f"{seq}/{bb} m={m} w={w} form {form}, exact window terms", m=m)
                lemma(E, lo0.energy(st), up0.energy(st), pE, f"{seq}/{bb} m={m} w={w} form {form}, with reductions", m=m)
                dd = float("nan")
                if w == n - 1 and (seq, bb, m) in ref:
                    key = dict(S="site", B="pair", T="triple")[form]
                    dd = abs((b - a) - ref[(seq, bb, m)]["exact_terms"][key]); worst["d"] = max(worst["d"], dd)
                if rule == "best": wbest = b - a
                elif rule == "ext": wext = b - a; loext, upext = elo, eup
                else:
                    # the "ext" rule can only tighten: its floor is pointwise >= and its ceiling pointwise <= those of the "pair" rule
                    dom_viol += int((loext < elo - 1e-9).sum() + (upext > eup + 1e-9).sum())
                    wider["ext"] += int(wext > b - a + 1e-12); wider["best"] += int(wbest > b - a + 1e-12); wider["best_vs_ext"] += int(wbest > wext + 1e-12); wider["n"] += 1
                    cells.append(f"{form} best {wbest:.6g}, ext {wext:.6g}, pair {b - a:.6g} [{w0:.6g}] | {da:.1e} | {v} | {dc:.1e} | {dd:.1e}")
                ncase += 1
            log(f"{seq}/{bb} m={m} w={w} | {info['exact']} / {info['reduced']} / {info['far_pairs']} || " + " || ".join(cells) + f"  [{time.time() - t0:.0f}s]")
# ---- (g) the triple form with two windows (window_model.triple_form_two_windows) on enumerated domains
g_n = 0; g_viol = 0; g_dev = 0.0; g_out = 0; cells = []
for seq, bb, tau, m in (("S6", "H", 0.70, 4), ("S6", "E", 0.70, 4), ("S5", "H", 0.70, 5)):
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau); n, k = G.ns, list(G.k)
    st, g, src = L.enumerate_g(G, seq, bb, tau, verbose=False); f = pw.f_energy(st, c0, h, J); E = f + g; lnZE = float(logsumexp(-BETA * E))
    z = np.load(os.path.join(P6, "out", f"pairsums_{L.tagname(seq, bb, tau)}_m{m}.npz")); Gam, S, Gp = float(z["Gamma"]), z["S"], z["G"]
    val = {tuple(int(v) for v in e if v >= 0): float(t) for e, t in zip(z["excl"], z["tot"])}
    GF = L.GFBound2(G, x0, L.EnvelopeSup(G), K=m); d, nball, srcb = L.ball_terms(G, x0, m - 1, seq, bb, tau, verbose=False)
    phi1, psi1, psi2 = L.fp_tables(n, k, x0, m - 1); w = n - 1
    tris = T9.window_triples(n, w); se, cr = L.GFBatch(GF).totals(m, tris)
    H = {tr: (val[()] - val[(tr[0],)] - val[(tr[1],)] - val[(tr[2],)] + val[(tr[0], tr[1])] + val[(tr[0], tr[2])] + val[(tr[1], tr[2])]) - float(t3) for tr, t3 in zip(tris, se + cr)}
    ref_T = T9.triple_form(n, m, w, Gp, H, psi1, psi2, 5e-9 * Gam, 1e-8 * Gam)
    for w3 in range(2, w + 1):
        gs, g2, eta = window_model.triple_form_two_windows(T9.window_triples, L.RND, n, m, w, w3, Gp, H, psi1, psi2, 5e-9 * Gam, 1e-8 * Gam)
        if w3 == w:
            g_dev = max(g_dev, float(np.abs(gs - ref_T[0]).max()), float(np.abs(g2 - ref_T[1]).max()), max(abs(eta[t] - ref_T[2][t]) for t in eta))
        lo, up, info = build_window_models(k, x0, c0, h, J, d, w, L.EPS_G, m - 1, gs, g2, eta)
        elo, eup = lo.energy(st), up.energy(st); g_viol += int((elo > E + 1e-9).sum() + (eup < E - 1e-9).sum())
        a, b = up.lnZ(), lo.lnZ(); g_out += int(not (a - 1e-9 <= lnZE <= b + 1e-9)); g_n += 1
        cells.append(f"{seq}/{bb} m={m} w={w} w3={w3}: {b - a:.5g}")
log("TWO-WINDOW TRIPLE FORM (band w = n - 1 for pairs and evaluated terms, triples within w3; exact window terms): widths  " + ";  ".join(cells))
log(f"   {g_n} sandwiches: sandwich violations at enumerated states {g_viol}; exact ln Z outside the bracket {g_out} times; "
    f"with w3 = w the tables equal workstream P6's triple_form to {g_dev:.1e}")
log(f"REDUCTION RULES ({wider['n']} sandwiches each): states at which the floor of the 'ext' rule is below, or its ceiling above, that of P3's 'pair' rule: {dom_viol} (must be 0); "
    f"brackets wider than with the 'pair' rule: 'ext' {wider['ext']}, 'best' {wider['best']}; 'best' wider than 'ext': {wider['best_vs_ext']}")
assert dom_viol == 0
log(f"SUMMARY: {ncase} sandwiches on enumerated domains; largest |model energy - direct evaluation| = {worst['a']:.2e} kcal/mol; sandwich violations: {viol}; "
    f"largest |ln Z transfer - ln Z enumeration| = {worst['c']:.2e}; full window against the enumerated exact-terms widths of serine_helix_shares.json "
    f"(which carry no floating-point allowance): {worst['d']:.2e} nats")
log(f"LEMMA A17.16 on {lem['n']} sandwiches (window models and models with reductions), exact means under the true ensemble: violated {lem['bad']} times; "
    f"smallest slack of the lower bound {lem['slack_lo']:.2e}, of the upper bound {lem['slack_up']:.2e} nats; first-order error |D - <a + b>| / D: "
    f"at most {lem['rel_narrow']:.3f} where D < 0.5 nats (worst: {lem['where_narrow']}), at most {lem['rel_all']:.3f} overall; "
    f"at orders m >= 4 with D < 0.5 nats at most {lem['rel_full']:.3f} (worst: {lem['where_full']})")
log("ALL DONE")
