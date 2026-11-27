#!/usr/bin/env python3
"""R19, item 2: the held-site passes (held_site_laws.py, slack_recovery.py) against BRUTE-FORCE ENUMERATION with my own code,
on random band models -- and the four bounds of Proposition A17.19 end to end on random sandwiches with a known truth.

What is the coordinator's: the model class (window_model.make(pwmodel) -- the class nested_sampler.WindowModel is), the
routing and the group statistics (held_site_laws.assign_routes / group_stats / _stats_dir, slack_recovery.group_stats),
slack_recovery.bounds.  What is mine: the random instances, the enumeration of every state, the evaluation of a model
from its tables, the grouping of items by route and the five statistics by direct summation, the legality test of a
route, the bounds recomputed from my statistics, the exact ln Z of the truth.

Part A (random instances):  n in 4..9 sites, 1..4 states per site (different per site), band w in 1..4, random one-site,
  pair and multi-site (3-4 sites, span <= w) tables; "sources": random tables on 2-4 sites; each is replaced in the ceiling
  by its maximum, in the floor by its minimum over a random set of given-up sites (the kept sub-tuple fits a window); the
  items are (max - source) and (source - min) with random preferred direction; three classes (the driver's cumulative
  stages).  The truth is E = base + sum of sources + rho, |rho| <= c, ceiling/floor constants +-c: the hypotheses of the
  proposition hold by construction, with an unrecoverable part 2c.
  Checks: (A1) every route legal (window holds all sites but the held one, starts after it, inside the chain); an item that
  fits no window has no route iff neither end can be held; (A2) total mass of every group one; (A3) the five statistics
  a, e, b, c, cp of every group and every cumulative stage against enumeration; (A4) slack_recovery.group_stats (the older
  module: last/first w sites only) the same; (A5) LJ, LP <= ln Z(E) <= UE, UP from the coordinator's numbers and from mine;
  every iterate of (UE), (UP) an upper bound; (A6) the loss against "the same items put back exactly", as a multiple of D^2/4.
  Controls that must fail: (C1) the statistics of a group compared with the enumeration of the group with one item left
  out; (C2) the law computed with the backward message left out (B := 0) -- a wrong three-way split; (C3) every item
  doubled in the bounds: the hypotheses fail and the "bracket" must exclude the truth in some instances.
Part B (windows chosen by me, not by assign_routes): for random items, EVERY legal window start, including the window
  right after the held site and the last window of the chain, through held_site_laws._stats_dir in both directions.
Part C: fuzz of assign_routes alone on long chains (n up to 40, w up to 8): legality, completeness, and that no two items
  with different (direction, held site) share a group key.
Part D: slack_recovery.bounds at the edges: zero means, huge C', nan, 60 iterations without convergence.

Run: python3 -B r19_heldsite_fuzz.py [number of instances, default 600] [seed] > r19_heldsite_fuzz.log
"""
import os, sys, math, time, itertools, resource, warnings
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "NUMEXPR_MAX_THREADS"):
    os.environ[v] = "1"
sys.dont_write_bytecode = True
SCI = "/home/user/MetricChain/experiments/science"
sys.path.insert(0, os.path.join(SCI, "ws_P3")); sys.path.insert(0, os.path.join(SCI, "pi_inference"))
import numpy as np
import pwmodel as pw                                               # workstream P3's module (BandModel)
import window_model                                                # the coordinator's WindowModel
import slack_recovery as SR
import held_site_laws as HS
WindowModel, _bw, _dw = window_model.make(pw)
t00 = time.time()
NINST = int(sys.argv[1]) if len(sys.argv) > 1 else 600
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 20261126


def all_states(k):
    return np.stack(np.meshgrid(*[np.arange(v) for v in k], indexing="ij"), axis=-1).reshape(-1, len(k))


def energy_of(mdl, X):
    e = np.full(len(X), float(mdl.const))
    for i in range(mdl.n): e += np.asarray(mdl.one[i])[X[:, i]]
    for (i, j), t in mdl.pair.items(): e += np.asarray(t)[X[:, i], X[:, j]]
    for U, t in mdl.multi.items(): e += np.asarray(t)[tuple(X[:, u] for u in U)]
    return e


def lnz(e, beta):
    m = e.min(); return float(-beta * m + math.log(np.exp(-beta * (e - m)).sum()))


def rand_model(rng, n, w, k, scale):
    mdl = WindowModel(k, w); mdl.const = float(rng.normal())
    for i in range(n): mdl.one[i] = rng.normal(0, scale, k[i])
    for i in range(n):
        for j in range(i + 1, min(i + w, n - 1) + 1):
            if rng.random() < 0.75: mdl.add_pair(i, j, rng.normal(0, scale, (k[i], k[j])))
    if w >= 2:
        for _ in range(int(rng.integers(0, 2 * n))):
            a = int(rng.integers(0, n - 2)); cand = list(range(a, min(a + w, n - 1) + 1)); s = int(rng.integers(3, 5))
            if len(cand) < s: continue
            U = tuple(sorted(int(v) for v in rng.choice(cand, s, replace=False)))
            mdl.add_multi(U, rng.normal(0, scale, [k[u] for u in U]))
    return mdl


def add_reduced(mdl, V, red):
    if len(V) == 1: mdl.one[V[0]] = mdl.one[V[0]] + red
    elif len(V) == 2: mdl.add_pair(V[0], V[1], red)
    else: mdl.add_multi(V, red)


def legal(U, r, n, w):
    d, held, s = r
    V = U if d == "fwd" else tuple(n - 1 - u for u in reversed(U))
    return V[0] == held and s >= held + 1 and s + w - 1 <= n - 1 and all(s <= v <= s + w - 1 for v in V[1:])


def key_of(r, n):
    return (r[0], r[1] if r[0] == "fwd" else n - 1 - r[1], r[2])


def enum_stats(wgt, Sp, Sm, beta):
    return dict(a=float(wgt @ Sp), e=float(wgt @ np.expm1(beta * Sp)), b=float(wgt @ Sm), c=float(wgt @ (Sm * np.exp(beta * Sp))),
                cp=float(wgt @ (np.expm1(beta * Sm) * np.exp(beta * Sp))))


def reldev(ex, got):
    return max((abs(ex[q] - got[q]) / abs(ex[q]) if abs(ex[q]) > 1e-13 else abs(ex[q] - got[q])) for q in ("a", "e", "b", "c", "cp"))


def my_bounds(L, U, st, beta, iters=60):
    a = sum(g["a"] for g in st.values()); e = sum(g["e"] for g in st.values()); c = sum(g["c"] for g in st.values()); cp = sum(g["cp"] for g in st.values())
    LJ = U + beta * a; LP = U + math.log1p(e); u = v = L; its_u, its_v = [], []
    for _ in range(iters):
        u = L - beta * c * math.exp(U - u); v = L - math.log1p(cp * math.exp(U - v)); its_u.append(u); its_v.append(v)
    return LJ, LP, u, v, its_u, its_v


def main():
    rng = np.random.default_rng(SEED)
    tot = dict(inst=0, states=0, items=0, routed=0, noroute=0, inner=0, fwd=0, rev=0, groups=0, stats=0, shared=0, inwin_items=0, inwin_assert=0, multi_terms=0,
               k1sites=0, old_groups=0)
    worst = dict(stat=0.0, mass=0.0, old=0.0, lnZ=0.0); bad = dict(route=0, complete=0, stat=0, old=0, bound=0, iter=0, mine_bound=0, keycol=0)
    ctrl = dict(c1=0, c1_n=0, c2=0, c2_n=0, c3=0, c3_n=0); loss_ratio = []; gaps = []; tight = []
    hist_n = {}; hist_w = {}
    inst = 0
    while inst < NINST:
        n = int(rng.integers(4, 10)); w = int(rng.integers(1, min(4, n - 2) + 1))
        k = [int(v) for v in rng.choice([1, 2, 2, 3, 3, 4], n)]
        while np.prod([float(v) for v in k]) > 150000:
            k[int(rng.integers(n))] = 2
        if np.prod(k) < 8: continue
        beta = float(rng.choice([0.5, 1.0, 1.6775]))
        scale = float(rng.choice([0.3, 1.0, 2.0]))
        base = rand_model(rng, n, w, k, scale)
        up = WindowModel(k, w); lo = WindowModel(k, w)
        for mdl in (up, lo):
            mdl.const = base.const; mdl.one = [np.array(v, dtype=float) for v in base.one]
            for (i, j), t in base.pair.items(): mdl.add_pair(i, j, np.array(t, dtype=float))
            for U, t in base.multi.items(): mdl.add_multi(U, np.array(t, dtype=float))
        X = all_states(k); N = len(X); E = energy_of(base, X)
        nsrc = int(rng.integers(2, 13)); classes = [([], []), ([], []), ([], [])]; allow_inwin = rng.random() < 0.25
        sscale = float(rng.choice([0.01, 0.03, 0.1, 0.3, 1.0]))
        for _ in range(nsrc):
            s = int(rng.integers(2, 5)); U = tuple(sorted(int(v) for v in rng.choice(n, min(s, n), replace=False)))
            fits = U[-1] - U[0] <= w
            if fits and not allow_inwin: continue
            T = rng.normal(0, sscale, [k[u] for u in U])
            if rng.random() < 0.5:                                  # anchored structure: the source vanishes when one of its sites is in state 0
                p = int(rng.integers(len(U))); sl = [slice(None)] * len(U); sl[p] = 0; T[tuple(sl)] = 0.0
            a = int(rng.integers(len(U))); keep = [p for p in range(len(U)) if U[a] <= U[p] <= U[a] + w]
            if len(keep) > 1 and rng.random() < 0.3:
                keep = sorted(int(v) for v in rng.choice(keep, int(rng.integers(1, len(keep))), replace=False))
            other = tuple(p for p in range(len(U)) if p not in keep)
            E = E + T[tuple(X[:, u] for u in U)]
            if not other:                                           # kept whole: exact in both models
                add_reduced(up, U, T); add_reduced(lo, U, T); continue
            rmax, rmin = T.max(axis=other), T.min(axis=other); V = tuple(U[p] for p in keep)
            add_reduced(up, V, rmax); add_reduced(lo, V, rmin)
            pref = [None, "fwd", "rev", "fwd" if (0 in keep and len(U) - 1 not in keep) else "rev" if (len(U) - 1 in keep and 0 not in keep) else None][int(rng.integers(4))]
            c = int(rng.integers(3))
            pref_m = pref if rng.random() < 0.7 else [None, "fwd", "rev"][int(rng.integers(3))]      # the floor's item may prefer another end (the driver's choices are made per side)
            classes[c][0].append((U, np.expand_dims(rmax, other) - T, pref)); classes[c][1].append((U, T - np.expand_dims(rmin, other), pref_m))
            tot["inwin_items"] += int(fits)
        if sum(len(pl) for pl, mi in classes) == 0: continue
        cc = float(rng.choice([0.0, 0.02, 0.2])); rho = cc * np.sin(1.7 * (X * (1 + np.arange(n))[None]).sum(1) + 0.3)      # the unrecoverable part: |rho| <= cc
        E = E + rho; up.const += cc; lo.const -= cc
        eu, el = energy_of(up, X), energy_of(lo, X)
        allp = [it for pl, mi in classes for it in pl]; allm = [it for pl, mi in classes for it in mi]
        sp = sum(it[1][tuple(X[:, u] for u in it[0])] for it in allp); sm = sum(it[1][tuple(X[:, u] for u in it[0])] for it in allm)
        assert (eu - E - sp > -1e-9).all() and (E - el - sm > -1e-9).all() and min(float(it[1].min()) for it in allp + allm) > -1e-12      # my construction satisfies the hypotheses
        lnZup, lnZlo, lnZE = up.lnZ(beta), lo.lnZ(beta), lnz(E, beta)
        worst["lnZ"] = max(worst["lnZ"], abs(lnZup - lnz(eu, beta)), abs(lnZlo - lnz(el, beta)))
        wu = np.exp(-beta * (eu - eu.min())); wu /= wu.sum()
        try:
            stats, routes = HS.group_stats(WindowModel, up, classes, beta, lnZup)
        except AssertionError:
            # only allowed when an item that fits a window was passed (the module's precondition is violated by MY instance)
            assert allow_inwin, "assertion in group_stats on items that fit no window"
            tot["inwin_assert"] += 1; continue
        inst += 1; tot["inst"] += 1; tot["states"] += N; tot["multi_terms"] += len(up.multi); tot["k1sites"] += sum(1 for v in k if v == 1)
        hist_n[n] = hist_n.get(n, 0) + 1; hist_w[w] = hist_w.get(w, 0) + 1
        # ---- (A1) routes
        keyinfo = {}
        for c, ((pl, mi), (rp, rm_)) in enumerate(zip(classes, routes)):
            for its, rts in ((pl, rp), (mi, rm_)):
                for it, r in zip(its, rts):
                    U = it[0]; tot["items"] += 1; fits = U[-1] - U[0] <= w
                    can = (U[-1] - U[1] <= w - 1) or (U[-2] - U[0] <= w - 1)
                    if r is None:
                        tot["noroute"] += 1
                        if not fits and can: bad["complete"] += 1
                        continue
                    tot["routed"] += 1; tot[r[0]] += 1; tot["inner"] += int(r[2] != n - w)
                    if not legal(U, r, n, w): bad["route"] += 1
                    if not fits and not can: bad["complete"] += 1
                    kk = key_of(r, n); hs = (r[0], U[0] if r[0] == "fwd" else U[-1])
                    if keyinfo.setdefault(kk, hs) != hs: bad["keycol"] += 1
        # ---- (A2), (A3) statistics of every group at every cumulative stage
        Sp = {}; Sm = {}; members = {}
        for q in range(3):
            pl, mi = classes[q]; rp, rm_ = routes[q]
            for it, r in zip(pl, rp):
                if r is not None:
                    kk = key_of(r, n); Sp[kk] = Sp.get(kk, 0.0) + it[1][tuple(X[:, u] for u in it[0])]; Sm.setdefault(kk, np.zeros(N)); members.setdefault(kk, []).append(it)
            for it, r in zip(mi, rm_):
                if r is not None:
                    kk = key_of(r, n); Sm[kk] = Sm.get(kk, 0.0) + it[1][tuple(X[:, u] for u in it[0])]; Sp.setdefault(kk, np.zeros(N))
            if set(stats[q]) != set(Sp): bad["stat"] += 1; continue
            for kk in Sp:
                ex = enum_stats(wu, Sp[kk] + np.zeros(N), Sm[kk] + np.zeros(N), beta); got = stats[q][kk]
                dv = reldev(ex, got); worst["stat"] = max(worst["stat"], dv); worst["mass"] = max(worst["mass"], abs(got["mass"] - 1.0)); tot["stats"] += 5
                if dv > 1e-8: bad["stat"] += 1
        tot["groups"] += len(Sp); tot["shared"] += sum(1 for kk in members if len(members[kk]) > 1)
        # ---- control C1: one item left out of the enumeration of its group
        for kk, its in members.items():
            it = its[0]; v = it[1][tuple(X[:, u] for u in it[0])]
            if float(wu @ v) < 1e-6 * max(float(wu @ Sp[kk]), 1e-300) or float(wu @ v) < 1e-12: continue      # the item must carry at least 1e-6 of its group's mean
            ex = enum_stats(wu, Sp[kk] - v, Sm[kk] + np.zeros(N), beta); ctrl["c1_n"] += 1
            ctrl["c1"] += int(abs(ex["a"] - stats[2][kk]["a"]) > 1e-7 * abs(stats[2][kk]["a"]))          # the mean <S+_g> must differ by more than 1e-7 of itself
        # ---- control C2: the law WITHOUT the backward message (a wrong three-way split), by my enumeration: weights without the terms whose
        #      last site lies beyond the window.  "Live" when it changes a statistic of the group by more than 1e-6 (relative); then the
        #      coordinator's numbers must agree with the right law and not with the wrong one.
        for kk in list(Sp):
            d, held, s = kk
            if d != "fwd" or s + w > n - 1: continue                 # the last window of the chain has no backward message
            eb = np.zeros(N)                                         # the terms of the ceiling whose last site is >= s + w
            for i in range(s + w, n): eb += np.asarray(up.one[i])[X[:, i]]
            for (i, j), t in up.pair.items():
                if j >= s + w: eb += np.asarray(t)[X[:, i], X[:, j]]
            for U, t in up.multi.items():
                if U[-1] >= s + w: eb += np.asarray(t)[tuple(X[:, u] for u in U)]
            wb = np.exp(-beta * (eu - eb - (eu - eb).min())); wb /= wb.sum()
            right = enum_stats(wu, Sp[kk] + np.zeros(N), Sm[kk] + np.zeros(N), beta); wrong = enum_stats(wb, Sp[kk] + np.zeros(N), Sm[kk] + np.zeros(N), beta)
            if reldev(right, wrong) < 1e-6: continue
            ctrl["c2_n"] += 1; ctrl["c2"] += int(reldev(wrong, stats[2][kk]) > 1e-8 and reldev(right, stats[2][kk]) < 1e-8)
        # ---- (A4) the older module (last / first w sites only)
        old = SR.group_stats(WindowModel, up, classes, beta, lnZup)
        So = {}
        for q in range(3):
            pl, mi = classes[q]
            for its, sd in ((pl, 0), (mi, 1)):
                for it in its:
                    r = SR.item_route(it, n, w)
                    if r is None: continue
                    kk = (r, it[0][0] if r == "fwd" else it[0][-1]); g = So.setdefault(kk, [np.zeros(N), np.zeros(N)]); g[sd] += it[1][tuple(X[:, u] for u in it[0])]
            if set(old[q]) != set(So): bad["old"] += 1; continue
            for kk in So:
                dv = reldev(enum_stats(wu, So[kk][0], So[kk][1], beta), old[q][kk]); worst["old"] = max(worst["old"], dv)
                if dv > 1e-8: bad["old"] += 1
        tot["old_groups"] += len(So)
        # ---- (A5) the four bounds, the coordinator's and mine
        B = SR.bounds(lnZlo, lnZup, stats[2], beta)
        if not (B["LJ"] <= lnZE + 1e-10 and B["LP"] <= lnZE + 1e-10 and B["UE"] >= lnZE - 1e-10 and B["UP"] >= lnZE - 1e-10): bad["bound"] += 1
        mine = {kk: enum_stats(wu, Sp[kk] + np.zeros(N), Sm[kk] + np.zeros(N), beta) for kk in Sp}
        LJ, LP, UE, UP, iu, iv = my_bounds(lnz(el, beta), lnz(eu, beta), mine, beta)
        if not (LJ <= lnZE + 1e-10 and LP <= lnZE + 1e-10): bad["mine_bound"] += 1
        if min(iu) < lnZE - 1e-10 or min(iv) < lnZE - 1e-10: bad["iter"] += 1
        if any(iu[t + 1] > iu[t] + 1e-12 for t in range(len(iu) - 1)) or any(iv[t + 1] > iv[t] + 1e-12 for t in range(len(iv) - 1)): bad["iter"] += 1
        # ---- (A6) loss against the same items put back exactly
        spr = sum(v for v in Sp.values()) + np.zeros(N); smr = sum(v for v in Sm.values()) + np.zeros(N)
        best = (lnz(eu - spr, beta), lnz(el + smr, beta)); D = lnZlo - lnZup
        corr = min(B["UE"], B["UP"]) - max(B["LJ"], B["LP"])
        if D > 1e-6:
            loss_ratio.append(((corr - (best[1] - best[0])) / (D * D / 4.0), D, len(Sp), cc, beta, n, w, corr, best[1] - best[0])); gaps.append(D); tight.append(corr / D)
        # ---- control C3: every item doubled (hypotheses violated): does the "bracket" exclude the truth?
        st2 = {}
        for kk in Sp:
            st2[kk] = enum_stats(wu, 2 * (Sp[kk] + np.zeros(N)), 2 * (Sm[kk] + np.zeros(N)), beta)
        B2 = SR.bounds(lnZlo, lnZup, st2, beta); ctrl["c3_n"] += 1
        with np.errstate(all="ignore"):
            ctrl["c3"] += int(not (max(B2["LJ"], B2["LP"]) <= lnZE <= min(B2["UE"], B2["UP"])))
    print(f"PART A: {tot['inst']} random instances (seed {SEED}); sites n: {dict(sorted(hist_n.items()))}; band w: {dict(sorted(hist_w.items()))}; {tot['states']} states enumerated in all; "
          f"{tot['multi_terms']} multi-site terms in the ceilings; {tot['k1sites']} sites with a single state; {tot['items']} items ({tot['inwin_items']} of the sources fit a window: precondition deliberately violated; "
          f"{tot['inwin_assert']} such instances stopped by the module's own assertion and were skipped)")
    print(f"  (A1) routes: {tot['routed']} items routed ({tot['fwd']} forward, {tot['rev']} on the mirrored chain; {tot['inner']} through a window inside the chain), {tot['noroute']} without a route; "
          f"ILLEGAL routes: {bad['route']}; items that fit no window with a wrong route/no-route decision: {bad['complete']}; group keys shared by items with different (direction, held site): {bad['keycol']}")
    print(f"  (A2,A3) {tot['groups']} groups ({tot['shared']} with more than one plus item), {tot['stats']} statistics (a, e, b, c, cp; three cumulative stages) against enumeration: largest relative deviation {worst['stat']:.2e}; "
          f"groups off by more than 1e-8: {bad['stat']}; largest |mass - 1|: {worst['mass']:.1e}; ln Z of the models, transfer matrix against enumeration: {worst['lnZ']:.1e}")
    print(f"  (A4) slack_recovery.group_stats (older module): {tot['old_groups']} groups, largest relative deviation {worst['old']:.2e}; off by more than 1e-8: {bad['old']}")
    print(f"  (A5) LJ, LP <= ln Z(E) <= UE, UP from slack_recovery.bounds: violated in {bad['bound']} instances; from my statistics and formulas: {bad['mine_bound']}; "
          f"an iterate of (UE)/(UP) below ln Z(E), or an iteration that increases: {bad['iter']} instances")
    lr = np.array([v[0] for v in loss_ratio]); Dv = np.array(gaps); tg = np.array(tight)
    print(f"  (A6) {len(lr)} instances with D > 1e-6: D from {Dv.min():.3g} to {Dv.max():.3g} (median {np.median(Dv):.3g}); corrected width / D: median {np.median(tg):.3g}, largest {tg.max():.3g}; "
          f"loss against the same items put back exactly, in units of D^2/4: min {lr.min():.3g}, quartiles {np.percentile(lr, 25):.3g}, {np.median(lr):.3g}, {np.percentile(lr, 75):.3g}, max {lr.max():.3g}")
    ng = np.array([v[2] for v in loss_ratio])
    top = sorted((v for v in loss_ratio if v[1] < 0.3), reverse=True)[:5]
    print("       the five largest ratios with D < 0.3 (ratio, D, groups, unrecoverable constant c, beta, n, w, corrected width, width with the routed items put back exactly): "
          + "; ".join(f"({v[0]:.3g}, {v[1]:.4g}, {v[2]}, {v[3]}, {v[4]}, {v[5]}, {v[6]}, {v[7]:.4g}, {v[8]:.4g})" for v in top))
    for cut in (0.3, 0.05):
        sm_ = Dv < cut
        if sm_.sum() > 5:
            print(f"       restricted to D < {cut} ({int(sm_.sum())} instances): loss / (D^2/4): min {lr[sm_].min():.3g}, quartiles {np.percentile(lr[sm_], 25):.3g}, {np.median(lr[sm_]):.3g}, {np.percentile(lr[sm_], 75):.3g}, "
                  f"max {lr[sm_].max():.3g}; with at least 6 groups ({int((sm_ & (ng >= 6)).sum())} instances): median {np.median(lr[sm_ & (ng >= 6)]) if (sm_ & (ng >= 6)).sum() else float('nan'):.3g}, "
                  f"max {lr[sm_ & (ng >= 6)].max() if (sm_ & (ng >= 6)).sum() else float('nan'):.3g}")
    print(f"  controls that must fail: (C1) one item left out of the enumeration of its group: detected in {ctrl['c1']} of {ctrl['c1_n']} groups; (C2) the law without the backward message differs (by enumeration) in {ctrl['c2_n']} groups; the transfer-matrix numbers agree with the right law "
          f"and not with the wrong one in {ctrl['c2']} of them; (C3) every item doubled: the 'bracket' excludes the exact ln Z in {ctrl['c3']} of {ctrl['c3_n']} instances")

    # ------------------------------------------------------------------------------------------ PART B
    nB = 0; worstB = 0.0; badB = 0; right_after = 0; lastwin = 0; cases = 0
    rngB = np.random.default_rng(SEED + 1)
    while cases < max(60, NINST // 4):
        n = int(rngB.integers(4, 10)); w = int(rngB.integers(1, min(4, n - 2) + 1)); k = [int(v) for v in rngB.choice([1, 2, 3, 3, 4], n)]
        while np.prod([float(v) for v in k]) > 60000: k[int(rngB.integers(n))] = 2
        if np.prod(k) < 8: continue
        beta = 1.0; mdl = rand_model(rngB, n, w, k, 1.0); X = all_states(k); N = len(X); e = energy_of(mdl, X); wgt = np.exp(-beta * (e - e.min())); wgt /= wgt.sum()
        lnZ = mdl.lnZ(beta); rmodel = SR.reverse_model(WindowModel, mdl); msgs = HS.forward_messages(mdl, -beta); rmsgs = HS.forward_messages(rmodel, -beta)
        for d, m_, fm, bm in (("fwd", mdl, msgs, rmsgs), ("rev", rmodel, rmsgs, msgs)):
            pl = []; mi = []; exp_ = {}
            for _ in range(int(rngB.integers(1, 7))):
                held = int(rngB.integers(0, n - w)); s = int(rngB.integers(held + 1, n - w + 1))
                ns = int(rngB.integers(1, min(3, w) + 1)); others = tuple(sorted(int(v) for v in rngB.choice(np.arange(s, s + w), ns, replace=False)))
                V = (held,) + others; kd = [m_.k[v] for v in V]
                tp = rngB.exponential(0.4, kd) * (rngB.random(kd) < 0.7); tm = rngB.exponential(0.4, kd) * (rngB.random(kd) < 0.7)
                pl.append((V, tp, s)); mi.append((V, tm, s)); right_after += int(s == held + 1); lastwin += int(s == n - w)
                Xd = X if d == "fwd" else X[:, ::-1]                # state of the direction's chain: site v of the mirrored chain is site n-1-v
                g = exp_.setdefault((held, s), [np.zeros(N), np.zeros(N)]); g[0] += tp[tuple(Xd[:, v] for v in V)]; g[1] += tm[tuple(Xd[:, v] for v in V)]
            got = HS._stats_dir(m_, fm, bm, [(pl, mi)], beta, lnZ)[0]
            if set(got) != set(exp_): badB += 1; continue
            for kk in exp_:
                dv = reldev(enum_stats(wgt, exp_[kk][0], exp_[kk][1], beta), got[kk]); worstB = max(worstB, dv, abs(got[kk]["mass"] - 1.0)); nB += 1
                if dv > 1e-8: badB += 1
        cases += 1
    print(f"PART B: {cases} random models, windows chosen by me (every legal start allowed): {nB} groups in both directions, {right_after} items with the window right after the held site, {lastwin} with the last window "
          f"of the chain: largest relative deviation of a statistic or of a mass from one: {worstB:.2e}; groups off by more than 1e-8: {badB}")

    # ------------------------------------------------------------------------------------------ PART C
    rngC = np.random.default_rng(SEED + 2); nit = 0; ill = 0; incomplete = 0; keycol = 0; nrt = 0; samewin_diff = 0; runs = 0; pm_diff = 0
    for _ in range(20000):
        n = int(rngC.integers(3, 41)); w = int(rngC.integers(1, min(8, n - 1) + 1)); items = []
        for _ in range(int(rngC.integers(1, 30))):
            s = int(rngC.integers(2, 6)); U = tuple(sorted(int(v) for v in rngC.choice(n, min(s, n), replace=False)))
            if U[-1] - U[0] <= w: continue
            items.append((U, None, [None, "fwd", "rev"][int(rngC.integers(3))]))
        if not items: continue
        runs += 1; out = HS.assign_routes(items, n, w); seen = {}
        for it, r in zip(items, out):
            U = it[0]; nit += 1; can = (U[-1] - U[1] <= w - 1) or (U[-2] - U[0] <= w - 1)
            if r is None:
                incomplete += int(can); continue
            nrt += 1; ill += int(not legal(U, r, n, w)); incomplete += int(not can)
            hs = (r[0], U[0] if r[0] == "fwd" else U[-1])
            if seen.setdefault(key_of(r, n), hs) != hs: keycol += 1
        # the same items in another order must get legal routes too (the greedy sweep sorts them); count how often the grouping changes
        perm = rngC.permutation(len(items)); out2 = HS.assign_routes([items[p] for p in perm], n, w)
        for p, r2 in zip(perm, out2):
            if (out[p] is None) != (r2 is None) or (r2 is not None and not legal(items[p][0], r2, n, w)): ill += 1
            if out[p] is not None and r2 is not None and out[p] != r2: pm_diff += 1
    print(f"PART C: assign_routes alone, {runs} random item lists on chains of 3..40 sites, band 1..8: {nit} items, {nrt} routed; illegal routes: {ill}; wrong route / no-route decisions: {incomplete}; "
          f"group keys shared by different (direction, held site): {keycol}; items whose route changes when the list is permuted: {pm_diff}")

    # ------------------------------------------------------------------------------------------ PART D
    print("PART D: slack_recovery.bounds at the edges (ln Z(m_-) = 10, ln Z(m_+) = 9.9 unless said otherwise)")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        z = dict(a=0.0, e=0.0, b=0.0, c=0.0, cp=0.0)
        print(f"  all means zero: {SR.bounds(10.0, 9.9, {'g': z}, 1.0)}   (expected: both lower ends 9.9, both upper ends 10)")
        print(f"  no group at all: {SR.bounds(10.0, 9.9, {}, 1.0)}")
        for cp in (1e3, 1e300, float('inf'), float('nan')):
            g = dict(a=0.01, e=0.0101, b=0.01, c=0.0102, cp=cp); B = SR.bounds(10.0, 9.9, {'g': g}, 1.0)
            print(f"  C' = {cp}: {B}; the driver's choice min(UE, UP) = {min(B['UE'], B['UP'])}, max(LJ, LP) = {max(B['LJ'], B['LP'])}")
        for e_ in (float('inf'), float('nan')):
            g = dict(a=0.01, e=e_, b=0.01, c=0.0102, cp=0.0103); B = SR.bounds(10.0, 9.9, {'g': g}, 1.0)
            print(f"  <e^(beta S+) - 1> = {e_}: {B}; the driver's choice max(LJ, LP) = {max(B['LJ'], B['LP'])}")
        # slow convergence: a wide sandwich.  two states, beta = 1: E = (0, 0) = ceiling; floor m- = (0, -Lg): one group, S+ = 0, S- = (0, Lg) -- (UP) is exact in the limit
        for Lg in (0.1, 0.5, 1.0, 3.0, 8.0):
            lnZE = math.log(2.0); lnZlo = math.log(1.0 + math.exp(Lg)); lnZup = lnZE
            c = 0.5 * Lg; cp = 0.5 * math.expm1(Lg); g = dict(a=0.0, e=0.0, b=c, c=c, cp=cp)
            B = SR.bounds(lnZlo, lnZup, {'g': g}, 1.0, safe=0.0); u = v = lnZlo; iu = []; iv = []
            for t in range(20000):
                u = lnZlo - c * math.exp(lnZup - u); v = lnZlo - math.log1p(cp * math.exp(lnZup - v)); iu.append(u); iv.append(v)
            print(f"  two states, floor low by {Lg} at one of them (D = {lnZlo - lnZup:.4f}): exact ln Z = {lnZE:.6f}; UE: bounds() {B['UE']:.9f}, my step 60 {iu[59]:.9f}, step 20000 {iu[-1]:.9f}; "
                  f"UP: bounds() {B['UP']:.9f}, my step 60 {iv[59]:.9f}, step 20000 {iv[-1]:.9f} (60 steps short of the limit by {iv[59] - iv[-1]:.2e}); every iterate >= exact: {min(iu) >= lnZE - 1e-12 and min(iv) >= lnZE - 1e-12}")
        # hypotheses violated (C far too large): the iteration runs away
        g = dict(a=0.0, e=0.0, b=5.0, c=5.0, cp=200.0); B = SR.bounds(10.0, 9.9, {'g': g}, 1.0)
        print(f"  inconsistent input (C = 5 for D = 0.1): {B}  -> lower end {max(B['LJ'], B['LP'])} > upper end {min(B['UE'], B['UP'])}: an EMPTY bracket; nothing in slack_recovery.bounds or in the driver (without --enum) tests for it")
    print(f"ALL DONE {time.time() - t00:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")


if __name__ == "__main__":
    main()
