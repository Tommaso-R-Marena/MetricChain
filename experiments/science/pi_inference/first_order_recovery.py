#!/usr/bin/env python3
"""Addendum A17 (19): the certified bracket after FIRST-ORDER RECOVERY of the known slack (slack_recovery.py).

Sandwich m_- <= E <= m_+ : the coordinator's window models (exact in-window evaluated terms, occupancy-aware
reductions, far pairs split around the anchor), workstream P6's floating-point allowances, and workstream P9's
state-resolved penalty in the window form (every subset T charged in full to one in-window sub-tuple K(T), through
the maximum of P9's raw table Theta_T over the given-up sites).

Known slack, as tables ("items") on site sets that do not fit a window:
  far    a pair beyond the band:              (ceiling's part) - P    and    P - (floor's part)            two sites
  term   an evaluated term d_U out of window:  max over the given-up sites - d_U    and    d_U - min       the sites of U
  alloc  a subset T out of window:             [max over the given-up sites of Theta_T](x_K) - Theta_T(x_T) [T off the anchor]
                                               (the same item on both sides)                               the sites of T
Every item is given to the group of one HELD site and one window (held_site_laws.assign_routes: the last or first w
sites where that serves, as in slack_recovery.route, else a window inside the chain -- needed for chains longer than
2w); where both ends of an item could be held, the end that the reduction keeps is taken, so that slacks that occur
together are treated exactly together.
The floating-point allowance of the evaluated terms (EPS_G per value of g, 2^|U| values per term) is attached to each
term's own table (floor: d_U - 2^|U| EPS_G where all sites of U are off the anchor; ceiling: +), not allocated to sites
and in-band pairs as in workstream P6's form, which charges a pair's share of every term through it whenever the pair
is off the anchor; the sandwich with P6's allocation -- the one workstream P9 reports -- is printed for comparison.
With r = g - I_{m-1} g and |r| <= envelope(x) = sum_{T subset S(x)} Theta_T(x_T) (P9's Theorem R):
  m_+ - E = far_+ + term_+ + (pen - r) + (allowances - rounding) >= far_+ + term_+ + (pen - envelope) = s_+ ,
and the same below.  Proposition A17.19 (slack_recovery.py) then gives two lower ends (LJ), (LP) and two upper ends
(UE), (UP), all from exact means under the ceiling model, computed by the transfer matrix with one site held at each
of its states in turn; the corrected bracket is [max of the lower ends, min of the upper ends].
Every item is lowered by 1e-9 kcal/mol and clipped at zero before use, every mean multiplied by 1 - 1e-9.

Checks.  --enum: the two hypotheses at EVERY state, the exact means by enumeration, the exact ln Z inside every
corrected bracket; controls that must fail (every item doubled; the sign of the far items exchanged).  Without
--enum: the hypotheses at Gibbs states, at exact samples of floor and ceiling, at uniformly random states and at
states with exactly m and m + 1 sites off the anchor, with new evaluations of the energy; the means against exact
samples of the ceiling; the same controls; and P9's raw tables entry by entry against the exact anchored term at random
states with exactly m sites off (--nshell N, default 5000), with a control that must fail.
The raw tables are workstream P9's (ws_P9/cache/theta2_*.npz; for the small instances p9_verification/cache/, written
by p9_verification/dump_theta2.py); K(T) is P9's stored choice where there is one, else the rule below.

Run: python3 -B first_order_recovery.py K5 4 2 --enum   > first_order_recovery_K5_m4_w2_enum.log
     python3 -B first_order_recovery.py K12 4 7          > first_order_recovery_K12_m4_w7.log
"""
import os, sys, math, time, glob, itertools, functools, resource
import numpy as np
import nested_sampler as NS
from window_model_occ import build_window_models_occ, gibbs_sample
import slack_recovery as SR
import held_site_laws as HS
L, pw = NS.L, NS.pw
BETA, RND, SAFE = L.BETA, 1.0 + 1e-9, 1e-9
HERE = os.path.dirname(os.path.abspath(__file__)); SCI = os.path.normpath(os.path.join(HERE, ".."))
P8, P9, MYT = os.path.join(SCI, "ws_P8"), os.path.join(SCI, "ws_P9"), os.path.join(SCI, "p9_verification", "cache")


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
    a = sys.argv[1:]; seq, m, w = a[0], int(a[1]), int(a[2]); ENUM = "--enum" in a; bb = "H"; M = m - 1; t0 = time.time()
    tau = 0.60 if ":" in seq else dict(S=0.70, V=0.70, K=0.70, L=0.60, F=0.60)[seq[0]]
    tag = f"{seq.replace(':', 'c')}_{bb}_{tau:.2f}"
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau); n, k = G.ns, list(G.k); x0 = [int(v) for v in x0]; X0 = np.array(x0)
    subs = list(itertools.combinations(range(n), m)); non = [[b for b in range(k[i]) if b != x0[i]] for i in range(n)]
    # ---------------------------------------------------------------- P9's raw tables
    files = sorted(glob.glob(os.path.join(P9, "cache", f"theta2_{tag}_m{m}*.npz"))) or sorted(glob.glob(os.path.join(MYT, f"theta2_{tag}_m{m}*.npz")))
    tabs = [None] * len(subs)
    for fn in files:
        z = np.load(fn)
        for j in z["idx"]: tabs[int(j)] = np.array(z[f"t{int(j)}"], dtype=float)
    assert all(t is not None for t in tabs), "raw tables of P9 missing (p9_verification/dump_theta2.py writes them for small instances)"
    for T, tab in zip(subs, tabs): assert tab.shape == tuple(len(non[i]) for i in T) and (tab > 0).all()
    log(f"=== {seq} on {bb}, tau {tau}: {n} sites, states per site {k}, {float(np.prod([float(v) for v in k])):.6g} states, anchor {x0}; order m = {m}, band {w}; "
        f"{len(subs)} raw stage-2 tables of workstream P9 from {os.path.relpath(os.path.dirname(files[0]), SCI)} (sum of their maxima {BETA * sum(float(t.max()) for t in tabs):.5g} kT)")

    def full(sites, red):
        out = np.zeros([k[i] for i in sites]); out[np.ix_(*[non[i] for i in sites])] = red
        return out

    def energy(X):
        X = np.atleast_2d(X); return pw.f_energy(X, c0, h, J) + np.concatenate([G.bulk_energy(X[s:s + 256]) for s in range(0, len(X), 256)])
    # ---------------------------------------------------------------- the ball and the anchored terms
    blocks, tot = pw.ball_states(k, x0, M); allst = np.concatenate([b for _, b in blocks], axis=0); vals = None; srcb = "evaluated now"
    for f in sorted(os.listdir(os.path.join(P8, "cache"))):
        if f.startswith(f"ball_{tag}_M") and f.endswith(".npz") and "ckpt" not in f:
            z = np.load(os.path.join(P8, "cache", f))
            if z["states"].shape[0] >= tot and np.array_equal(z["states"][:tot], allst): vals = np.array(z["vals"][:tot], dtype=float); srcb = f"ws_P8/cache/{f}"; break
    fmy = os.path.join(NS.CACHE, f"ball_{tag}_M{M}.npz")                 # the coordinator's cache (ball_cache.py)
    if vals is None and os.path.exists(fmy):
        z = np.load(fmy)
        if z["states"].shape[0] == tot and np.array_equal(z["states"], allst): vals = np.array(z["vals"], dtype=float); srcb = f"pi_inference/serine_helix_reach_cache/{os.path.basename(fmy)}"
    if vals is None: vals = np.concatenate([G.bulk_energy(allst[s:s + 256]) for s in range(0, tot, 256)])
    radix = np.array([int(np.prod(k[i + 1:])) for i in range(n)], dtype=np.int64)
    code = allst.astype(np.int64) @ radix; order = np.argsort(code); code_s = code[order]; vals_s = vals[order]

    def lookup(st):
        c = np.atleast_2d(st).astype(np.int64) @ radix; p = np.searchsorted(code_s, c); assert np.array_equal(code_s[p], c)
        return vals_s[p]
    d, nb, _ = pw.anchored_terms(G, x0, M, energy=lookup, cache_file=None); assert nb == tot
    del allst, code, order
    XGo = gibbs_sample(pw, G, c0, h, J, x0, k, BETA, np.random.default_rng(4242))
    log(f"(0) ball of radius {M}: {tot} values ({srcb}); guiding Gibbs sample (seed 4242, uncertified): {float((XGo != X0[None]).sum(1).mean()):.2f} sites off the anchor on average [{time.time() - t0:.0f}s]")
    # ---------------------------------------------------------------- K(T): P9's stored choice, else the least expected reduced table under the product of the sample's one-site marginals
    fst = os.path.join(P9, "out", f"tables_{tag}_m{m}_w{w}.npz"); keepK = None
    if os.path.exists(fst):
        ZS = np.load(fst)
        if [tuple(int(v) for v in T) for T in ZS["s2_subs"]] == subs and [int(v) for v in ZS["x0"]] == x0:
            keepK = [tuple(int(v) for v in str(s).split("_")) for s in ZS["s2_keep"]]; srck = "workstream P9's stored choice"
    if keepK is None:
        pm = [((np.bincount(XGo[:, i], minlength=k[i]) + 0.5) / (len(XGo) + 0.5 * k[i]))[non[i]] for i in range(n)]; keepK = []
        for T, tab in zip(subs, tabs):
            best = None
            for keep in ([tuple(range(m))] if T[-1] - T[0] <= w else maximal_windows(T, w)):
                other = tuple(p for p in range(m) if p not in keep); red = tab.max(axis=other) if other else tab; sc = red
                for p in reversed(keep): sc = sc @ pm[T[p]]
                if best is None or (float(sc), float(red.max())) < best[0]: best = ((float(sc), float(red.max())), tuple(T[p] for p in keep))
            keepK.append(best[1])
        srck = "the least mean of the reduced table under the product of the guiding sample's one-site marginals"
    W = {}; alloc = []
    for T, tab, K in zip(subs, tabs, keepK):
        assert set(K) <= set(T) and K[-1] - K[0] <= w
        other = tuple(p for p in range(m) if T[p] not in K); red = tab.max(axis=other) if other else tab
        W[K] = W.get(K, 0.0) + full(K, red)
        if other:                                                        # allocation slack: [max over the given-up sites](x_K) - Theta_T(x_T) [T off the anchor]
            fk = full(K, red); sh = [k[i] if i in K else 1 for i in T]
            alloc.append((T, fk.reshape(sh) - full(T, tab), K))
    g1 = [W.get((i,), np.zeros(k[i])) for i in range(n)]; g2 = {K: v for K, v in W.items() if len(K) == 2}; g3 = {K: v for K, v in W.items() if len(K) >= 3}

    def pen(X):
        X = np.atleast_2d(X); out = np.zeros(len(X))
        for i in range(n): out += g1[i][X[:, i]]
        for K, v in list(g2.items()) + list(g3.items()): out += v[tuple(X[:, u] for u in K)]
        return out
    # ---------------------------------------------------------------- the models
    t1 = time.time(); phi1, psi1, psi2 = L.fp_tables(n, k, x0, M); zn, znn = np.zeros(n), np.zeros((n, n))
    gsA, g2A = L.banded_pair_form(n, m, w, zn, znn, psi1, psi2, 0.0)

    def add_pen(lo_, up_):
        for i in range(n):
            lo_.one[i] = lo_.one[i] - g1[i] * RND; up_.one[i] = up_.one[i] + g1[i] * RND
        for (i, j), v in g2.items(): lo_.add_pair(i, j, -v * RND); up_.add_pair(i, j, v * RND)
        for U, v in g3.items(): lo_.add_multi(U, -v * RND); up_.add_multi(U, v * RND)

    def build(dd, gs_, g2_, out=None):
        return build_window_models_occ(NS.WindowModel, k, x0, c0, h, J, dd, w, L.EPS_G, M, gs_, g2_, None, XG=XGo, far_pairs="anchored", out=out)
    # (1a) the sandwich as workstream P9 built it: P6's allocation of the floating-point allowance to sites and in-band pairs
    lo, up, info = build(d, gsA, g2A); add_pen(lo, up); b0 = (up.lnZ(), lo.lnZ()); del lo, up
    # (1b) the allowance ATTACHED TO EACH EVALUATED TERM: d_U is an alternating sum of 2^|U| values of g, each within EPS_G, and vanishes
    #      exactly unless all sites of U are off the anchor; so d_U -/+ 2^|U| EPS_G [x_U off the anchor] is a minorant / majorant of the
    #      true term, on the term's own table -- charged when U is off the anchor and not, as in the pair allocation, whenever a pair is.
    offm = [np.ones(k[i]) for i in range(n)]
    for i in range(n): offm[i][x0[i]] = 0.0

    def with_allowance(sense):
        dd = {}
        for U, arr in d.items():
            dd[U] = arr if len(U) == 0 else arr + sense * (2 ** len(U)) * L.EPS_G * functools.reduce(np.multiply.outer, [offm[u] for u in U])
        return dd
    d_lo, d_up = with_allowance(-1), with_allowance(+1); ch_lo, ch_up = {}, {}
    lo, _, info = build(d_lo, zn, znn, ch_lo); _, up, _ = build(d_up, zn, znn, ch_up); del _
    add_pen(lo, up)
    lnZlo, lnZup = lo.lnZ(), up.lnZ(); D = lnZlo - lnZup
    log(f"(1) sandwich (window form of P9's stage 2; K(T): {srck}); {info['exact']} evaluated terms exact in a window, {info['reduced']} reduced, {info['far_pairs']} pairs beyond the band.  "
        f"With workstream P6's allocation of the floating-point allowance (as P9 built it): [{b0[0]:.6f}, {b0[1]:.6f}], width {b0[1] - b0[0]:.6g}; "
        f"with the allowance attached to each evaluated term: certified bracket [{lnZup:.6f}, {lnZlo:.6f}], width D = {D:.6g} nats [{time.time() - t1:.0f}s, peak RSS {rss():.0f} MB]")
    # ---------------------------------------------------------------- the items
    def clean(t, name):
        assert float(t.min()) > -1e-9, f"negative slack in {name}: {float(t.min())}"
        return np.maximum(t - SAFE, 0.0)
    items = []; kind = []                                                # kind: (class, side)  side +1: ceiling, -1: floor, 0: both
    for side, chs, dd in ((+1, ch_up, d_up), (-1, ch_lo, d_lo)):          # the ceiling's choices and tables for the ceiling's slack, the floor's for the floor's
        for (i, j), (A, B, which, (cmin, cmax)) in chs["fchoice"].items():
            P = J[(i, j)] + dd.get((i, j), 0.0); base = A[:, None] + B[None, :]
            red = (cmax if side > 0 else cmin); red = red[:, None] if which == "i" else red[None, :]
            pref = "fwd" if which == "i" else "rev"                       # hold the site the reduction KEEPS: its slack occurs when that site is off the anchor
            items.append(((i, j), clean((base + red - P) if side > 0 else (P - base - red), "far"), pref)); kind.append(("far", side))

    def pref_of(U, kept):                                                 # the same rule for terms and subsets: hold a kept end site if one end is kept and the other given up
        return "fwd" if (U[0] in kept and U[-1] not in kept) else "rev" if (U[-1] in kept and U[0] not in kept) else None
    for side, chs, dd in ((+1, ch_up, d_up), (-1, ch_lo, d_lo)):
        for U, (sc, sl, keep, rlo, rup) in chs["choice"].items():
            other = tuple(p for p in range(len(U)) if p not in keep); arr = dd[U]; pref = pref_of(U, [U[p] for p in keep])
            items.append((U, clean((np.expand_dims(rup, other) - arr) if side > 0 else (arr - np.expand_dims(rlo, other)), "term"), pref)); kind.append(("term", side))
    for T, t, K in alloc:
        items.append((T, clean(t, "alloc"), pref_of(T, K))); kind.append(("alloc", 0))
    # ---------------------------------------------------------------- exact group means under the ceiling
    def idx(cls, side): return [j for j in range(len(items)) if kind[j][0] in cls and kind[j][1] in (side, 0)]

    def sel(cls, side): return [items[j] for j in idx(cls, side)]
    stages = (("far pairs", ("far",)), ("far pairs and out-of-window terms", ("far", "term")), ("far pairs, terms and the allocation of the penalty", ("far", "term", "alloc")))
    variants = {name: (sel(cls, +1), sel(cls, -1)) for name, cls in stages}; CL = ("far", "term", "alloc")
    t1 = time.time(); GL, RT = HS.group_stats(NS.WindowModel, up, [(sel((c,), +1), sel((c,), -1)) for c in CL], BETA, lnZup)
    GS = {name: GL[q] for q, (name, cls) in enumerate(stages)}
    rts = [None] * len(items)                                           # per item: (direction, held site, window start), in the chain's own numbering of sites
    for c, (rp, rm_) in zip(CL, RT):
        for js, rr in ((idx((c,), +1), rp), (idx((c,), -1), rm_)):
            for j, r in zip(js, rr):
                if r is not None: rts[j] = (r[0], r[1] if r[0] == "fwd" else n - 1 - r[1], r[2])
    worst = max(abs(g["mass"] - 1.0) for gs in GS.values() for g in gs.values())
    old = [r is not None and r[2] == n - w for r in rts]                 # the last (first) w sites: the routes of slack_recovery.py
    log(f"(2) exact means under the CEILING model, by the transfer matrix with one site held at each of its states in turn: {len(items)} items, {sum(r is not None and r[0] == 'fwd' for r in rts)} by the forward route, "
        f"{sum(r is not None and r[0] == 'rev' for r in rts)} on the mirrored chain ({sum(1 for r, o in zip(rts, old) if r is not None and not o)} of the two through a window inside the chain), "
        f"{sum(r is None for r in rts)} without a route; {len(GS[stages[-1][0]])} groups (direction, held site, first site of the window): {', '.join(f'{d_}{i}@{s_}' for d_, i, s_ in sorted(GS[stages[-1][0]]))}; "
        f"largest deviation of a clamped total mass from one: {worst:.1e} [{time.time() - t1:.0f}s, peak RSS {rss():.0f} MB]")
    assert worst < 1e-8
    gmean = lambda q: BETA * sum(float(items[j][1][tuple(XGo[:, u] for u in items[j][0])].mean()) for j in q)                  # first-order estimate on the Gibbs sample of the true ensemble
    log("| class | side | items | with a route | beta x mean on the Gibbs sample of the true ensemble (nats): items with a route; without |")
    log("|---|---|---|---|---|")
    for cls in ("far", "term", "alloc"):
        for side in ((+1, -1) if cls != "alloc" else (0,)):
            q = [j for j in range(len(items)) if kind[j] == (cls, side)]; qr = [j for j in q if rts[j] is not None]
            log(f"| {cls} | {'ceiling' if side > 0 else 'floor' if side < 0 else 'both'} | {len(q)} | {len(qr)} | {gmean(qr):.6g}; {gmean([j for j in q if rts[j] is None]):.6g} |")
    log("| recovered | lower end by (LJ) | by (LP) | upper end by (UE) | by (UP) | corrected bracket: best lower, best upper | width (nats) | D / width |")
    log("|---|---|---|---|---|---|---|---|")
    res = {"nothing (the sandwich)": (lnZup, lnZlo)}
    log(f"| nothing (the sandwich) | — | — | — | — | [{lnZup:.7f}, {lnZlo:.7f}] | **{D:.4g}** | 1.0 |")
    for name, cls in stages:
        B = SR.bounds(lnZlo, lnZup, GS[name], BETA); lo_ = max(B["LJ"], B["LP"]); up_ = min(B["UE"], B["UP"]); res[name] = (lo_, up_)
        log(f"| {name} | {B['LJ']:.7f} | {B['LP']:.7f} | {B['UE']:.7f} | {B['UP']:.7f} | [{lo_:.7f}, {up_:.7f}] | **{up_ - lo_:.4g}** | {D / (up_ - lo_):.1f} |")
    # ---------------------------------------------------------------- checks
    Ip, Im = sel(("far", "term", "alloc"), +1), sel(("far", "term", "alloc"), -1); Ipf, Imf = sel(("far",), +1), sel(("far",), -1)

    def hyp(X, E):
        """violations of m_+ - E >= s_+ and E - m_- >= s_- (ALL items, with or without a route), smallest margin; two controls."""
        mp, mm = up.energy(X), lo.energy(X); sp, sm = SR.items_value(Ip, X), SR.items_value(Im, X)
        v = int((mp - E < sp - 1e-9).sum() + (E - mm < sm - 1e-9).sum())
        c1 = int((mp - E < 2 * sp - 1e-9).sum() + (E - mm < 2 * sm - 1e-9).sum())                                     # control 1: every item doubled
        fp_, fm_ = SR.items_value(Ipf, X), SR.items_value(Imf, X)
        c2 = int((mp - E < sp - fp_ + fm_ - 1e-9).sum() + (E - mm < sm - fm_ + fp_ - 1e-9).sum())                     # control 2: far items of floor and ceiling exchanged
        return v, c1, c2, float(min((mp - E - sp).min(), (E - mm - sm).min()))
    if ENUM:
        t1 = time.time(); st = np.stack(np.meshgrid(*[np.arange(v) for v in k], indexing="ij"), axis=-1).reshape(-1, n)
        EE = energy(st); lnZ = float(-BETA * EE.min() + math.log(np.exp(-BETA * (EE - EE.min())).sum()))
        v, c1, c2, mg = hyp(st, EE)
        eu, el = up.energy(st), lo.energy(st); wu = np.exp(-BETA * (eu - eu.min())); wu /= wu.sum(); devm = 0.0
        name = stages[-1][0]; jp, jm = idx(CL, +1), idx(CL, -1); spu = np.zeros(len(st)); smu = np.zeros(len(st))
        for gk, gv in GS[name].items():
            Sp = SR.items_value([items[j] for j in jp if rts[j] == gk], st); Sm = SR.items_value([items[j] for j in jm if rts[j] == gk], st); spu += Sp; smu += Sm
            ex = dict(a=float((wu * Sp).sum()), e=float((wu * np.expm1(BETA * Sp)).sum()), b=float((wu * Sm).sum()), c=float((wu * Sm * np.exp(BETA * Sp)).sum()),
                      cp=float((wu * np.expm1(BETA * Sm) * np.exp(BETA * Sp)).sum()))
            devm = max(devm, max(abs(ex[q] - gv[q]) / max(abs(ex[q]), 1e-300) for q in ("a", "e", "b", "c", "cp") if abs(ex[q]) > 1e-12))
        lz = lambda e: float(-BETA * e.min() + math.log(np.exp(-BETA * (e - e.min())).sum()))
        best = (lz(eu - spu), lz(el + smu))                                                                             # what an exact treatment of the same items would give
        log(f"(3) EVERY state ({len(st)}): hypotheses m_+ - E >= s_+ and E - m_- >= s_- violated at {v} states (smallest margin {mg:.2e} kcal/mol); controls that must fail: every item doubled: {c1} violations; "
            f"far items of floor and ceiling exchanged: {c2} violations; the group means (a, e, b, c, cp) by enumeration against the transfer matrix: largest relative deviation {devm:.1e}")
        log(f"    exact ln Z = {lnZ:.7f}: inside every corrected bracket: {all(lo_ <= lnZ <= up_ for lo_, up_ in res.values())}; distances to the ends of the last one: {lnZ - res[name][0]:.3e}, {res[name][1] - lnZ:.3e}; "
            f"for comparison, ln Z of the models with the routed items put back exactly (by enumeration; no band model can hold them): [{best[0]:.7f}, {best[1]:.7f}], width {best[1] - best[0]:.4g} [{time.time() - t1:.0f}s]")
        assert v == 0 and c1 > 0 and all(lo_ <= lnZ <= up_ for lo_, up_ in res.values()) and devm < 1e-8
    else:
        t1 = time.time(); rs = np.random.default_rng(1618 + m)

        def random_states(s_, N, rng):
            X = np.tile(X0, (N, 1))
            for r in range(N):
                for i in rng.choice(n, size=s_, replace=False): X[r, i] = non[i][rng.integers(len(non[i]))]
            return X
        sets = {"Gibbs (seed 20261126)": gibbs_sample(pw, G, c0, h, J, x0, k, BETA, np.random.default_rng(20261126), nchain=8, nsweep=75, burn=15),
                "exact samples of the floor": lo.sample(1000, rs), "exact samples of the ceiling": up.sample(1000, rs),
                "uniformly random": np.stack([rs.integers(0, k[i], size=300) for i in range(n)], axis=1),
                f"exactly {m} sites off": random_states(m, 1000, rs), f"exactly {min(m + 1, n)} sites off": random_states(min(m + 1, n), 1000, rs),
                "one or two sites off (inside the ball)": np.concatenate([random_states(1, 300, rs), random_states(2, 300, rs)])}
        cells = []; V = C1 = C2 = 0; N = 0
        for nm, X in sets.items():
            v, c1, c2, mg = hyp(X, energy(X)); V += v; C1 += c1; C2 += c2; N += len(X); cells.append(f"{nm}: {len(X)}, {v} ({mg:.1e})")
        log(f"(3) hypotheses m_+ - E >= s_+ and E - m_- >= s_- with new evaluations of the energy — states, violations (smallest margin, kcal/mol): " + "; ".join(cells)
            + f" — total {N} states, {V} violations; controls that must fail on the same states: every item doubled: {C1} violations; far items of floor and ceiling exchanged: {C2} violations [{time.time() - t1:.0f}s]")
        t1 = time.time(); XS = up.sample(20000, np.random.default_rng(4)); name = stages[-1][0]
        plr = [items[j] for j in idx(CL, +1) if rts[j] is not None]; mir = [items[j] for j in idx(CL, -1) if rts[j] is not None]
        for lab, its, ex in (("sum <S+>", plr, sum(g["a"] for g in GS[name].values())), ("sum <S->", mir, sum(g["b"] for g in GS[name].values()))):
            vals_ = SR.items_value(its, XS); se = float(vals_.std() / math.sqrt(len(XS)))
            log(f"    {lab} against 20000 exact samples of the ceiling: exact {BETA * ex:.6g}, sampled {BETA * float(vals_.mean()):.6g} ± {BETA * se:.2g} nats ({(float(vals_.mean()) - ex) / max(se, 1e-300):+.1f} standard errors) [{time.time() - t1:.0f}s]")
        assert V == 0 and C1 > 0
        # P9's raw tables, entry by entry, at random states with exactly m sites off the anchor: there g - I_{m-1} g is the anchored term of T = S(x),
        # and I_{m-1} g is the sum of the evaluated terms on the subsets of T -- the per-entry check that exists wherever the ball of radius m - 1 does
        t1 = time.time(); NSH = int(a[a.index("--nshell") + 1]) if "--nshell" in a else 5000
        XM = random_states(m, NSH, np.random.default_rng(271828)); gX = np.concatenate([G.bulk_energy(XM[q:q + 256]) for q in range(0, NSH, 256)])
        I = np.full(NSH, float(d[()]))
        for U, arr in d.items():
            if len(U) >= 1: I += arr[tuple(XM[:, u] for u in U)]
        rem = np.abs(gX - I); where = {T: j for j, T in enumerate(subs)}; posn = [np.full(k[i], -1) for i in range(n)]
        for i in range(n): posn[i][non[i]] = np.arange(len(non[i]))
        th = np.empty(NSH); thmin = np.empty(NSH)
        for r in range(NSH):
            T = tuple(int(i) for i in np.nonzero(XM[r] != X0)[0]); tb = tabs[where[T]]
            th[r] = tb[tuple(posn[i][XM[r, i]] for i in T)]; thmin[r] = tb.min()
        nz = rem > 1e-9
        log(f"(4) P9's raw tables entry by entry at {NSH} random states with exactly {m} sites off the anchor (new evaluations of g; the remainder there is the exact anchored term of the changed set): "
            f"violations of abs(remainder) <= table entry: {int((rem > th * RND + 1e-10).sum())}; largest remainder {rem.max():.4g} kcal/mol; ratio entry / remainder: smallest {float((th[nz] / rem[nz]).min()):.3f}, "
            f"median {float(np.median(th[nz] / rem[nz])):.1f}; control that must fail (every table replaced by its minimum): {int((rem > thmin * RND + 1e-10).sum())} violations [{time.time() - t1:.0f}s]")
        assert int((rem > th * RND + 1e-10).sum()) == 0
    log(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {rss():.0f} MB")


if __name__ == "__main__":
    main()
