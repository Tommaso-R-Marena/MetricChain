#!/usr/bin/env python3
"""Addendum A17 (18): the occupancy-aware reduction rule (window_model_occ.py) against the rules of window_model.py.

For one instance, order m, band w and the three share forms: certified brackets of ln Z(E) with the evaluated terms
that do not fit the band reduced by
   "pair"  workstream P3's rule (the in-band pair of least sup-norm slack),
   "best"  the maximal sub-tuple that fits a window with the least sup-norm slack,
   "occ"   the maximal sub-tuple with the least sample mean of what is lost (window_model_occ.py), far pairs as P3,
   "occ+"  the same with the anchored split of the pairs beyond the band;
the width of the same models with all penalties zero (what the reductions cost by themselves; not a sandwich); the
first-order prediction beta x sample mean of m_+ - m_-; and the checks: the sandwich at the Gibbs states, at exact
samples of the floor, and with --enum at EVERY state, with the exact ln Z inside every bracket.
The Gibbs sample that guides rule "occ" (seed 4242) is NOT the one the sandwich is checked on (seed 777).
Constants: workstream P3's closed form (default; this script's caches), or with --chat VAR workstream P8's per-subset
constants (as nested_sampler_ext.py).

Options: --chat VAR, --enum, --rules pair,occ+ (default: all four).
Run:  python3 -B occ_reduction_test.py K5 H 4 2 --chat SAb --enum > occ_reduction_test_K5_H_m4_w2_SAb_enum.log
      python3 -B occ_reduction_test.py K12 H 5 7 --chat SAb    > occ_reduction_test_K12_H_m5_w7_SAb.log
      python3 -B occ_reduction_test.py S12 H 5 7               > occ_reduction_test_S12_H_m5_w7.log
"""
import os, sys, math, json, time, itertools, resource
import numpy as np
import nested_sampler as NS
import nested_sampler_ext as NX
from window_model_occ import build_window_models_occ, gibbs_sample
L, pw, T9, window_model = NS.L, NS.pw, NS.T9, NS.window_model
BETA = L.BETA
log = NS.log


def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024


def main():
    a = sys.argv[1:]; seq, bb, m, w = a[0], a[1], int(a[2]), int(a[3]); VAR = NS.opt(a, "--chat", None); ENUM = "--enum" in a
    M = m - 1; t0 = time.time()
    tau = 0.60 if ":" in seq else dict(S=0.70, V=0.70, K=0.70, L=0.60, F=0.60)[seq[0]]
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau); n, k = G.ns, list(G.k); x0 = [int(v) for v in x0]
    subs = list(itertools.combinations(range(n), m)); tris = T9.window_triples(n, w)
    phi1, psi1, psi2 = L.fp_tables(n, k, x0, M)
    if VAR:
        P8 = NX.P8; tag = f"{seq.replace(':', 'c')}_{bb}_{tau:.2f}"
        f12, f12b, fbc = (os.path.join(P8, "out", f) for f in (f"g12_{tag}_m{m}.npz", f"g12b_{tag}_m{m}.npz", f"bc_{tag}.json"))
        if os.path.exists(f12b):
            Z = np.load(f12); Zb = np.load(f12b); assert [int(v) for v in Zb["anchor"]] == x0 and [tuple(int(v) for v in T) for T in Zb["T"]] == subs
            V = [str(v) for v in Z["variants"]]; Vb = [str(v) for v in Zb["variants"]]
            chat = Zb["Cb"][:, Vb.index(VAR)] if VAR in Vb else Z["C"].sum(axis=2)[:, V.index(VAR)]
        else:
            Jd = json.load(open(fbc))["per_subset"][VAR]; chat = np.array([float(Jd["-".join(map(str, T))]) for T in subs])
        Gam = float(chat.sum()); S = np.zeros(n); Gp = np.zeros((n, n)); H = {tr: 0.0 for tr in tris}
        for T, v in zip(subs, chat):
            for i in T: S[i] += v
            for i, j in itertools.combinations(T, 2): Gp[i, j] += v; Gp[j, i] += v
            for tr in itertools.combinations(T, 3):
                if tr in H: H[tr] += v
        absG = absH = 1e-12 * Gam; srcc = f"workstream P8's per-subset constants '{VAR}'"
        blocks, tot = pw.ball_states(k, x0, M); allst = np.concatenate([b for _, b in blocks], axis=0); vals = None
        for f in sorted(os.listdir(os.path.join(P8, "cache"))):
            if f.startswith(f"ball_{tag}_M") and f.endswith(".npz") and "ckpt" not in f:
                z = np.load(os.path.join(P8, "cache", f))
                if z["states"].shape[0] >= tot and np.array_equal(z["states"][:tot], allst): vals = np.array(z["vals"][:tot], dtype=float); break
        if vals is None: vals = np.concatenate([G.bulk_energy(allst[s:s + 256]) for s in range(0, tot, 256)])
        radix = np.array([int(np.prod(k[i + 1:])) for i in range(n)], dtype=np.int64)
        code = allst.astype(np.int64) @ radix; order = np.argsort(code); code_s = code[order]; vals_s = vals[order]

        def lookup(st):
            c = np.atleast_2d(st).astype(np.int64) @ radix; p = np.searchsorted(code_s, c); assert np.array_equal(code_s[p], c)
            return vals_s[p]
        d, nb, _ = pw.anchored_terms(G, x0, M, energy=lookup, cache_file=None); nball = tot
    else:
        GF = L.GFBound2(G, x0, L.EnvelopeSup(G), K=m); excl = L.exclusion_sets(n, None)
        fps = os.path.join(NS.CACHE, f"pairsums_{seq}_{bb}_m{m}.npz")
        if os.path.exists(fps) and list(np.load(fps)["anchor"]) == x0: tot_ex = np.load(fps)["tot"]
        else:
            se, cr = L.GFBatch(GF).totals(m, excl); tot_ex = se + cr; np.savez(fps, tot=tot_ex, anchor=np.array(x0))
        Gam, S, Gp = L.assemble_pair_sums(n, m, excl, tot_ex); val = {tuple(e): float(t) for e, t in zip(excl, tot_ex)}
        fpt = os.path.join(NS.CACHE, f"triplesums_{seq}_{bb}_m{m}_w{w}.npz")
        if os.path.exists(fpt) and list(np.load(fpt)["anchor"]) == x0: t3 = np.load(fpt)["tot"]
        else:
            se, cr = L.GFBatch(GF).totals(m, tris); t3 = se + cr; np.savez(fpt, tot=t3, anchor=np.array(x0))
        H = {tr: (val[()] - val[(tr[0],)] - val[(tr[1],)] - val[(tr[2],)] + val[(tr[0], tr[1])] + val[(tr[0], tr[2])] + val[(tr[1], tr[2])]) - float(v) for tr, v in zip(tris, t3)}
        absG, absH = 5e-9 * Gam, 1e-8 * Gam; srcc = "workstream P3's closed form"
        d, nball, _ = L.ball_terms(G, x0, M, seq, bb, tau, verbose=False)
    tabs = {"S": (L.site_form(n, m, S, phi1), np.zeros((n, n)), None), "B": L.banded_pair_form(n, m, w, S, Gp, psi1, psi2, absG) + (None,),
            "T": window_model.triple_form_two_windows(T9.window_triples, L.RND, n, m, w, w, Gp, H, psi1, psi2, absG, absH)}
    dom = float(np.prod([float(v) for v in k]))
    log(f"=== {seq} on {bb}, tau {tau}: {n} sites, states per site {k}, {dom:.6g} assignments; anchor {x0}; order m = {m}, band {w}; constants: {srcc}, "
        f"Gamma_{m} = {BETA * Gam:.4g} kT; ball {nball} evaluations [{time.time() - t0:.0f}s]")
    XGo = gibbs_sample(pw, G, c0, h, J, x0, k, BETA, np.random.default_rng(4242))         # guides rule "occ"
    XGc = gibbs_sample(pw, G, c0, h, J, x0, k, BETA, np.random.default_rng(777))          # the sandwich is checked here
    EGc = pw.f_energy(XGc, c0, h, J) + G.bulk_energy(XGc)
    log(f"(0) two Gibbs samples of the true ensemble, 960 states each (uncertified): off-anchor frequencies by site (sample that guides 'occ'): "
        + " ".join(f"{v:.2f}" for v in (XGo != np.array(x0)[None]).mean(0)) + f" [{time.time() - t0:.0f}s]")
    if ENUM:
        st = np.stack(np.meshgrid(*[np.arange(v) for v in k], indexing="ij"), axis=-1).reshape(-1, n)
        gE = np.concatenate([G.bulk_energy(st[s:s + 256]) for s in range(0, len(st), 256)]); EE = pw.f_energy(st, c0, h, J) + gE
        lnZ = float(-BETA * EE.min() + math.log(np.exp(-BETA * (EE - EE.min())).sum()))
        log(f"    enumeration: {len(st)} states, exact ln Z = {lnZ:.6f}")
    zero = (np.zeros(n), np.zeros((n, n)), None); res = dict(seq=seq, bb=bb, m=m, w=w, chat=VAR, Gamma_kT=BETA * Gam, rules={})

    def build(rule, tab):
        if rule in ("pair", "best"): return NS.build_window_models(k, x0, c0, h, J, d, w, L.EPS_G, M, *tab, reduce=rule)
        return build_window_models_occ(NS.WindowModel, k, x0, c0, h, J, d, w, L.EPS_G, M, *tab, XG=XGo, far_pairs=("anchored" if rule == "occ+" else "p3"))
    log("| rule | reduced terms; sum of their sup-norm slacks (kcal/mol) | width with all penalties zero (nats) | form S: bracket, width | form B | form T | "
        "beta x mean of m_+ - m_- over the check sample (form T) | sandwich violated at Gibbs states (S, B, T) | " + ("violated at any state; exact ln Z inside (S, B, T) |" if ENUM else "2000 floor samples of form T: violations |"))
    log("|---|---|---|---|---|---|---|---|---|")
    for rule in NS.opt(a, "--rules", "pair,best,occ,occ+").split(","):
        t1 = time.time(); lo0, up0, info = build(rule, zero); w0 = lo0.lnZ() - up0.lnZ(); del lo0, up0
        cells = []; viol = []; extra = []; R = dict(width_zero=w0, info={kk: (float(v) if isinstance(v, float) else v) for kk, v in info.items()})
        for form in "SBT":
            lo, up, _ = build(rule, tabs[form]); a_, b_ = up.lnZ(), lo.lnZ(); l1, u1 = lo.energy(XGc), up.energy(XGc)
            viol.append(int((l1 > EGc + 1e-9).sum() + (u1 < EGc - 1e-9).sum())); cells.append(f"[{a_:.6f}, {b_:.6f}] **{b_ - a_:.4g}**")
            R[form] = dict(lnZ_lo=a_, lnZ_hi=b_, width=b_ - a_, viol_gibbs=viol[-1])
            if ENUM:
                le, ue = lo.energy(st), up.energy(st); ve = int((le > EE + 1e-9).sum() + (ue < EE - 1e-9).sum()); extra.append(f"{ve}; {a_ <= lnZ <= b_}"); R[form].update(viol_all=ve, inside=bool(a_ <= lnZ <= b_))
            if form == "T":
                fo = BETA * float((u1 - l1).mean())
                if not ENUM:
                    xs = lo.sample(2000, np.random.default_rng(99)); Ex = pw.f_energy(xs, c0, h, J) + G.bulk_energy(xs)
                    vf = int((lo.energy(xs) > Ex + 1e-9).sum() + (up.energy(xs) < Ex - 1e-9).sum()); extra.append(f"{vf}"); R["floor_viol"] = vf
            del lo, up
        res["rules"][rule] = R
        fk = ("; far pairs: " + ", ".join(f"{v} {kk}" for kk, v in info["far_kind"].items()) + f"; first-order cost of the reductions on the guiding sample: terms {BETA * info['first_order']:.3g}, far pairs {BETA * info['far_first_order']:.3g} nats") if "far_kind" in info and rule == "occ+" else (f"; first-order cost on the guiding sample: terms {BETA * info['first_order']:.3g} nats" if "first_order" in info else "")
        log(f"| {rule} | {info['reduced']}; {info['reduced_sup']:.4g}{fk} | {w0:.4g} | " + " | ".join(cells) + f" | {fo:.4g} | {', '.join(map(str, viol))} | {', '.join(extra)} |   [{time.time() - t1:.0f}s, peak RSS {rss():.0f} MB]")
    json.dump(res, open(os.path.join(NS.HERE, f"occ_reduction_test_{seq.replace(':', 'c')}_{bb}_m{m}_w{w}" + (f"_{VAR}" if VAR else "") + ("_enum" if ENUM else "") + ".json"), "w"), indent=1)
    log(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {rss():.0f} MB")


if __name__ == "__main__":
    main()
