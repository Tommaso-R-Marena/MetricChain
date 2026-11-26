#!/usr/bin/env python3
"""Coordinator's re-run of workstream P9's certified brackets with a driver that is not P9's (its request P9-E1),
from tables that are re-built here out of P9's RAW state-resolved tables.

What is P9's and what is mine.  P9's: the raw stage-2 tables Theta_T(x_T), one per m-subset T, read from
ws_P9/cache/theta2_<tag>_m<m>*.npz (checked against exact anchored terms by resolved_check12.py), and -- for form W
only -- the CHOICE of the sub-tuple K(T) each subset is charged to (read from ws_P9/out/tables_*.npz, key s2_keep;
every choice is valid, the choice only moves the number).  Mine: everything else --
 (1) TABLES, re-built from the raw tables with the code below and compared entry by entry with what P9 stored:
       form W   W_K(b_K) = sum over the subsets T with K(T) = K of  max{ Theta_T(y_T) : y_K = b_K };
       form T   equal shares on the triples: t_U(b_U) = (1 / C(m,3)) sum_{T contains U} max{ Theta_T(y_T) : y_U = b_U };
                a triple that fits a window (max U - min U <= w) is kept, any other goes in thirds to its three pairs
                (maximum over the third site); a pair in band is kept, any other goes in halves to its two sites.
     Tables are zero whenever one of their sites is at the anchor.
 (2) ENVELOPE <= TABLES at my own states:  sum_{T subset S(x)} Theta_T(x_T) <= pen_W(x), pen_T(x)  (the step from
     Theorem R to the tables -- P9's Proposition P), with controls that must fail.
 (3) MODELS: the coordinator's (window models with exact in-window terms, occupancy-aware reductions, the split of the
     far pairs around the anchor -- as occ_reduction_test.py, rule "occ+"), with zero penalties plus workstream P6's
     floating-point allowances, plus my tables of (1) times (1 + 1e-9); the certified bracket of ln Z.
 (4) SANDWICH m_- <= E <= m_+ with new evaluations of the energy at my own states: Gibbs states (my seed), exact samples
     of the floor AND of the ceiling (my seed), uniformly random states, random states with exactly m and m + 1 sites
     off the anchor.  Controls: the same models without the tables (must fail), with the tables divided by 10 and 100.
Run: python3 -B resolved_brackets.py K12 0.70 4 7 > resolved_brackets_K12_m4_w7.log
"""
import os, sys, math, time, glob, itertools, resource
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SCI = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(SCI, "pi_inference"))
import nested_sampler as NS
from window_model_occ import build_window_models_occ, gibbs_sample
L, pw = NS.L, NS.pw
BETA, RND = L.BETA, 1.0 + 1e-9
P8, P9 = os.path.join(SCI, "ws_P8"), os.path.join(SCI, "ws_P9")


def log(s): print(s, flush=True)


def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024


def maximal_windows(U, w):
    sets = []
    for a in range(len(U)):
        V = tuple(p for p in range(len(U)) if U[a] <= U[p] <= U[a] + w)
        if not any(set(V) <= set(V2) for V2 in sets):
            sets = [V2 for V2 in sets if not set(V2) <= set(V)] + [V]
    return sets


def main():
    a = sys.argv[1:]; seq, tau, m, w = a[0], float(a[1]), int(a[2]), int(a[3]); bb = "H"; M = m - 1; t0 = time.time()
    FORMS = (a[a.index("--forms") + 1] if "--forms" in a else "W,T").split(",")
    tag = f"{seq.replace(':', 'c')}_{bb}_{tau:.2f}"
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau); n, k = G.ns, list(G.k); x0 = [int(v) for v in x0]; X0 = np.array(x0)
    subs = list(itertools.combinations(range(n), m)); non = [[b for b in range(k[i]) if b != x0[i]] for i in range(n)]
    pos = [np.full(k[i], -1) for i in range(n)]
    for i in range(n): pos[i][non[i]] = np.arange(len(non[i]))
    # ---------------------------------------------------------------- P9's raw tables and its choice of sub-tuples
    tabs = [None] * len(subs); files = sorted(glob.glob(os.path.join(P9, "cache", f"theta2_{tag}_m{m}*.npz")))
    for fn in files:
        z = np.load(fn)
        for j in z["idx"]: tabs[int(j)] = np.array(z[f"t{int(j)}"], dtype=float)
    assert all(t is not None for t in tabs), "raw tables of P9 missing"
    for T, tab in zip(subs, tabs): assert tab.shape == tuple(len(non[i]) for i in T) and (tab > 0).all()
    fst = os.path.join(P9, "out", f"tables_{tag}_m{m}_w{w}.npz"); ZS = np.load(fst)
    assert [tuple(int(v) for v in T) for T in ZS["s2_subs"]] == subs and [int(v) for v in ZS["x0"]] == x0 and [int(v) for v in ZS["k"]] == k
    keepK = [tuple(int(v) for v in str(s).split("_")) for s in ZS["s2_keep"]]
    log(f"=== {seq} on {bb}, tau {tau}: {n} sites, states per site {k}, anchor {x0}; order m = {m}, band {w}; {len(subs)} raw stage-2 tables of workstream P9 "
        f"({sum(t.size for t in tabs)} entries, {len(files)} file(s)); sum of their maxima {BETA * sum(float(t.max()) for t in tabs):.5g} kT")

    def full(sites, red):
        out = np.zeros([k[i] for i in sites]); out[np.ix_(*[non[i] for i in sites])] = red
        return out
    # ---------------------------------------------------------------- (1) the tables, re-built
    t1 = time.time(); W = {}; nfit = 0; sizes = {}
    for T, tab, K in zip(subs, tabs, keepK):
        assert set(K) <= set(T) and K[-1] - K[0] <= w, "P9's sub-tuple is not an in-window sub-tuple of its subset"
        if T[-1] - T[0] <= w: assert K == T; nfit += 1
        else:                                                           # K must be one of the maximal in-window sub-tuples (not needed for validity)
            assert tuple(T.index(i) for i in K) in maximal_windows(T, w)
        other = tuple(p for p in range(m) if T[p] not in K)
        red = tab.max(axis=other) if other else tab
        W[K] = W.get(K, 0.0) + full(K, red); sizes[len(K)] = sizes.get(len(K), 0) + 1
    devW = 0.0; keysW = {tuple(int(v) for v in f[5:].split("_")) for f in ZS.files if f.startswith("s2_W_")}
    assert keysW == set(W), "the set of sub-tuples differs from P9's stored window form"
    for K, tabK in W.items():
        st = np.array(ZS["s2_W_" + "_".join(map(str, K))]); assert st.shape == tabK.shape
        devW = max(devW, float(np.abs(st - tabK).max() / tabK.max()))
        for ax, i in enumerate(K): assert not np.take(tabK, x0[i], axis=ax).any()
    log(f"(1) form W re-built from the raw tables: {len(W)} tables on {', '.join(f'{v} subsets -> {s} sites' for s, v in sorted(sizes.items()))} ({nfit} subsets fit a window and are kept whole); "
        f"largest deviation from P9's stored tables, relative to the table's maximum: {devW:.1e}")
    c3 = math.comb(m, 3); S3 = {}
    for T, tab in zip(subs, tabs):
        for tr in itertools.combinations(range(m), 3):
            other = tuple(p for p in range(m) if p not in tr); U = tuple(T[p] for p in tr)
            S3[U] = S3.get(U, 0.0) + full(U, tab.max(axis=other) if other else tab)
    devS = 0.0
    for U, v in S3.items():
        st = np.array(ZS["s2_S3_" + "_".join(map(str, U))]); devS = max(devS, float(np.abs(st - v).max() / v.max()))
    g1T = [np.zeros(k[i]) for i in range(n)]; pairT = {}; g3T = {}
    for (i, j, l), v in S3.items():
        t = v / c3
        if l - i <= w: g3T[(i, j, l)] = t
        else:
            for key, ax in (((i, j), 2), ((i, l), 1), ((j, l), 0)):
                pairT[key] = pairT.get(key, 0.0) + t.max(axis=ax) / 3.0
    g2T = {}
    for (i, j), v in pairT.items():
        if j - i <= w: g2T[(i, j)] = v
        else:
            g1T[i] = g1T[i] + 0.5 * v.max(axis=1); g1T[j] = g1T[j] + 0.5 * v.max(axis=0)
    log(f"    form T re-built: {len(g3T)} in-window triple tables, {len(S3) - len(g3T)} triples reduced to pairs, {len(g2T)} in-band pair tables, "
        f"{len(pairT) - len(g2T)} pairs reduced to sites; triple sums against P9's stored ones: largest relative deviation {devS:.1e} [{time.time() - t1:.0f}s]")
    FT = {"W": ([W.get((i,), np.zeros(k[i])) for i in range(n)], {K: v for K, v in W.items() if len(K) == 2}, {K: v for K, v in W.items() if len(K) >= 3}),
          "T": (g1T, g2T, g3T)}

    def pen(form, X):
        g1, g2, g3 = FT[form]; X = np.atleast_2d(X); out = np.zeros(len(X))
        for i in range(n): out += g1[i][X[:, i]]
        for (i, j), v in g2.items(): out += v[X[:, i], X[:, j]]
        for U, v in g3.items(): out += v[tuple(X[:, u] for u in U)]
        return out

    def envelope(X, tabs_=None):
        X = np.atleast_2d(X); P = np.stack([pos[i][X[:, i]] for i in range(n)], axis=1); out = np.zeros(len(X))
        for T, tab in zip(subs, tabs_ if tabs_ is not None else tabs):
            I = P[:, list(T)]; inS = (I >= 0).all(axis=1)
            if inS.any(): out[inS] += tab[tuple(I[inS].T)]
        return out

    def random_states(s, N, rng):
        X = np.tile(X0, (N, 1))
        for r in range(N):
            for i in rng.choice(n, size=s, replace=False): X[r, i] = non[i][rng.integers(len(non[i]))]
        return X
    # ---------------------------------------------------------------- (2) envelope <= tables
    rng = np.random.default_rng(20261126 + 10 * m)
    t1 = time.time(); rows = []
    for s in range(m, n + 1):
        X = random_states(s, 4000, rng); env = envelope(X)
        rows.append((s, env, {f: pen(f, X) for f in FT}))
    for f in FT:
        worst = min(float((p[f] / e).min()) for s, e, p in rows); viol = sum(int((p[f] < e * (1 - 1e-12)).sum()) for s, e, p in rows)
        at_m = rows[0]; eq = float((at_m[2][f] / at_m[1]).min())
        log(f"(2) envelope <= tables, form {f}: {sum(len(e) for s, e, p in rows)} random states (4000 for each number s = {m}..{n} of sites off the anchor): {viol} violations; smallest ratio table sum / envelope {worst:.6g} "
            f"(at s = {m}, where the envelope is one table entry: {eq:.6g})")
    # controls: (i) form W with the minimum over the given-up sites in place of the maximum; (ii) form W with every 20th table removed
    Wmin = {}
    for T, tab, K in zip(subs, tabs, keepK):
        other = tuple(p for p in range(m) if T[p] not in K)
        Wmin[K] = Wmin.get(K, 0.0) + full(K, tab.min(axis=other) if other else tab)

    def pen_tabs(Wd, X):
        out = np.zeros(len(X))
        for K, v in Wd.items(): out += v[tuple(X[:, u] for u in K)]
        return out
    c1 = sum(int((pen_tabs(Wmin, random_states(s, 4000, np.random.default_rng(5 + s))) < envelope(random_states(s, 4000, np.random.default_rng(5 + s))) * (1 - 1e-12)).sum()) for s in range(m, n + 1))
    Wdrop = {K: v for q, (K, v) in enumerate(sorted(W.items())) if q % 20 != 0}
    c2 = sum(int((pen_tabs(Wdrop, random_states(s, 4000, np.random.default_rng(5 + s))) < envelope(random_states(s, 4000, np.random.default_rng(5 + s))) * (1 - 1e-12)).sum()) for s in range(m, n + 1))
    log(f"    controls that must fail (same number of states): minimum in place of the maximum over the given-up sites: {c1} violations; every 20th table of form W removed ({len(W) - len(Wdrop)} of {len(W)}): {c2} violations "
        f"[{time.time() - t1:.0f}s]")
    assert c1 > 0 and c2 > 0, "a control did not fail"
    # ---------------------------------------------------------------- the ball and the anchored terms (as occ_reduction_test.py)
    t1 = time.time(); blocks, tot = pw.ball_states(k, x0, M); allst = np.concatenate([b for _, b in blocks], axis=0); vals = None
    for f in sorted(os.listdir(os.path.join(P8, "cache"))):
        if f.startswith(f"ball_{tag}_M") and f.endswith(".npz") and "ckpt" not in f:
            z = np.load(os.path.join(P8, "cache", f))
            if z["states"].shape[0] >= tot and np.array_equal(z["states"][:tot], allst): vals = np.array(z["vals"][:tot], dtype=float); srcb = f"ws_P8/cache/{f}"; break
    assert vals is not None, "no cached ball"
    pick = np.random.default_rng(31).choice(tot, size=600, replace=False)
    dev = float(np.abs(np.concatenate([G.bulk_energy(allst[pick[s:s + 200]]) for s in range(0, 600, 200)]) - vals[pick]).max()); assert dev < 1e-8
    radix = np.array([int(np.prod(k[i + 1:])) for i in range(n)], dtype=np.int64)
    code = allst.astype(np.int64) @ radix; order = np.argsort(code); code_s = code[order]; vals_s = vals[order]

    def lookup(st):
        c = np.atleast_2d(st).astype(np.int64) @ radix; p = np.searchsorted(code_s, c); assert np.array_equal(code_s[p], c)
        return vals_s[p]
    d, nb, _ = pw.anchored_terms(G, x0, M, energy=lookup, cache_file=None); assert nb == tot
    del allst, code, order
    log(f"(3) ball of radius {M}: {tot} values from {srcb}; 600 of them re-evaluated now (my seed): largest deviation {dev:.1e} kcal/mol [{time.time() - t1:.0f}s]")

    def energy(X):
        X = np.atleast_2d(X); return pw.f_energy(X, c0, h, J) + np.concatenate([G.bulk_energy(X[s:s + 256]) for s in range(0, len(X), 256)])
    XGo = gibbs_sample(pw, G, c0, h, J, x0, k, BETA, np.random.default_rng(4242))                      # guides the reductions (as in every run of the pipeline)
    t1 = time.time(); XGm = gibbs_sample(pw, G, c0, h, J, x0, k, BETA, np.random.default_rng(20261126), nchain=8, nsweep=75, burn=15)
    log(f"    Gibbs samples (uncertified): seed 4242 guides the reductions; my check sample: seed 20261126, {len(XGm)} states, {float((XGm != X0[None]).sum(1).mean()):.2f} sites off the anchor on average [{time.time() - t1:.0f}s]")
    phi1, psi1, psi2 = L.fp_tables(n, k, x0, M); zn, znn = np.zeros(n), np.zeros((n, n))
    gsA, g2A = L.banded_pair_form(n, m, w, zn, znn, psi1, psi2, 0.0)                                   # P6's floating-point allowances alone

    def base(gs, g2):
        return build_window_models_occ(NS.WindowModel, k, x0, c0, h, J, d, w, L.EPS_G, M, gs, g2, None, XG=XGo, far_pairs="anchored")
    t1 = time.time(); lo0, up0, info = base(zn, znn); w0 = lo0.lnZ() - up0.lnZ(); del lo0, up0
    log(f"    models with all penalties zero and no allowances (not a sandwich): width {w0:.6g} nats; {info['exact']} evaluated terms exact in a window, {info['reduced']} reduced, {info['far_pairs']} pairs beyond the band "
        f"[{time.time() - t1:.0f}s, peak RSS {rss():.0f} MB]")
    # ---------------------------------------------------------------- (3), (4): brackets and sandwiches
    states = {"Gibbs (my seed)": XGm, "uniformly random": np.stack([np.random.default_rng(77).integers(0, k[i], size=500) for i in range(n)], axis=1),
              f"exactly {m} sites off (random)": random_states(m, 1500, np.random.default_rng(78)), f"exactly {m + 1} sites off (random)": random_states(min(m + 1, n), 1500, np.random.default_rng(79))}
    loA, upA, _ = base(gsA, g2A)                                                                       # allowances only: the models every form starts from
    Ecache = {name: energy(X) for name, X in states.items()}                                           # new evaluations of the energy, once per state set
    log("| form | certified bracket of ln Z | width (nats) | states: number, violations of m_- <= E <= m_+, largest factor by which the tables could shrink before a violation | "
        "controls on the same states: violations without the tables; with the tables / 100; / 10 | model energies equal base -/+ my table sum (largest deviation, kcal/mol) |")
    log("|---|---|---|---|---|---|")
    for form in FORMS:
        t1 = time.time(); g1, g2, g3 = FT[form]
        lo, up, _ = base(gsA, g2A)
        for i in range(n):
            lo.one[i] = lo.one[i] - g1[i] * RND; up.one[i] = up.one[i] + g1[i] * RND
        for (i, j), v in g2.items(): lo.add_pair(i, j, -v * RND); up.add_pair(i, j, v * RND)
        for U, v in g3.items(): lo.add_multi(U, -v * RND); up.add_multi(U, v * RND)
        a_, b_ = up.lnZ(), lo.lnZ()
        rs = np.random.default_rng(2718 + m)
        sts = dict(states); sts["exact samples of the floor (my seed)"] = lo.sample(1500, rs); sts["exact samples of the ceiling (my seed)"] = up.sample(1500, rs)
        cells = []; ctl = [0, 0, 0]; devm = 0.0; ntot = 0; vtot = 0
        for name, X in sts.items():
            E = Ecache[name] if name in Ecache else energy(X); l0, u0 = loA.energy(X), upA.energy(X); P = pen(form, X) * RND; l1, u1 = lo.energy(X), up.energy(X)
            devm = max(devm, float(np.abs(l1 - (l0 - P)).max()), float(np.abs(u1 - (u0 + P)).max()))
            v = int((l1 > E + 1e-9).sum() + (u1 < E - 1e-9).sum()); need = np.maximum(np.maximum(l0 - E, E - u0), 0.0)
            fac = float((P[need > 1e-9] / need[need > 1e-9]).min()) if (need > 1e-9).any() else float("inf")
            for q, sc in enumerate((0.0, 0.01, 0.1)): ctl[q] += int((l0 - sc * P > E + 1e-9).sum() + (u0 + sc * P < E - 1e-9).sum())
            offm = float((X != X0[None]).sum(1).mean()); ntot += len(X); vtot += v
            cells.append(f"{name}: {len(X)} ({offm:.2f} sites off), {v}, {fac:.3g}")
        log(f"| {form} | [{a_:.6f}, {b_:.6f}] | **{b_ - a_:.4g}** | " + "; ".join(cells) + f" — total {ntot} states, {vtot} violations | {ctl[0]}; {ctl[1]}; {ctl[2]} | {devm:.1e} |   [{time.time() - t1:.0f}s, peak RSS {rss():.0f} MB]")
        assert vtot == 0, "SANDWICH VIOLATED"
        del lo, up
    log(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {rss():.0f} MB")


if __name__ == "__main__":
    main()
