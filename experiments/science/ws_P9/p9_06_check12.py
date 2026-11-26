#!/usr/bin/env python3
"""P9 step 6 -- checks of the RESOLVED bound (stage 2) at twelve residues, where nothing can be enumerated.

(a) EVERY state with exactly m sites off the anchor (needs the ball of radius m; order 4 for the peptides whose ball
    of radius 4 exists).  For such a state x, with T = S(x):  g(x) - I_{m-1} g(x) = d_T(x_T), the anchored term of order
    m, which the ball gives exactly; Theorem R reads  |d_T(x_T)| <= Theta^2_T(x_T).  Checked for all subsets T and all
    states x_T; with the two controls of the validation (W1: the minimum of Theta_T over the states in place of the
    value; W2: the table rolled by one position along each state axis), which must fail.
(b) UNIFORMLY RANDOM states with s = m .. n sites off the anchor (250 per s; new evaluations of g):
    |g(x) - I_{m-1} g(x)| <= sum_{T subset S(x)} Theta^2_T(x_T), with I_{m-1} g from the ball by my own formula
        I_M g(x) = sum_{v <= M} (-1)^(M-v) C(s-v-1, M-v) sum_{U subset S(x), |U| = v} g(x_U, x0)        (s > M),
    self-tested against the grid recursion on a random table; and the same with rolled tables (control).
Needs cache/theta2_<tag>_m<M>*.npz (p9_03_tables.py --keeptabs) and P8's cached ball (read-only).
(c) with --shell N: N random states with EXACTLY m sites off the anchor (subset and rotamers uniform): there the
    remainder is the anchored term d_T(x_T), from one new evaluation and the ball of radius m - 1; |d_T| <= Theta^2_T(x_T),
    with the two controls of (a).  The substitute for (a) at an order whose ball of radius m does not exist.
usage: python3 -B p9_06_check12.py SEQ M [--noa] [--nob] [--shell N]      writes logs/check12_<tag>_m<M>[_shell].log, out/check12_....json
"""
import sys
from p9lib import *

a = sys.argv[1:]; seq, m = a[0], int(a[1]); bb = "H"; tau = tau_of(seq); tag = tagname(seq, bb, tau); M = m - 1
log = Log(os.path.join(LOGS, f"check12_{tag}_m{m}" + ("_shell" if "--shell" in a else "") + ".log"))
log(f"=== p9_06_check12 {seq} on {bb}, tau {tau}, order {m}; started {now()}")
G, c0, h, J, x0, E0 = setup(seq, bb, tau); n, k = G.ns, list(G.k); t0 = time.time()
subs = list(itertools.combinations(range(n), m)); non = nonanchor(k, x0, range(n))
tabs = [None] * len(subs)
for fn in sorted(glob.glob(os.path.join(MYCACHE, f"theta2_{tag}_m{m}*.npz"))):
    z = np.load(fn)
    for j in z["idx"]:
        tabs[int(j)] = np.array(z[f"t{int(j)}"])
assert all(t is not None for t in tabs)
log(f"    {n} sites, states per site {k}, anchor {x0}; {len(subs)} stage-2 tables Theta_T read from ws_P9/cache")


def roll_tab(tab):
    out = tab
    for ax in range(tab.ndim):
        if tab.shape[ax] > 1:
            out = np.roll(out, 1, axis=ax)
    return out


def load_ball(Mb):
    blocks, tot = pw.ball_states(k, x0, Mb); allst = np.concatenate([b for _, b in blocks], axis=0)
    for f in sorted(os.listdir(os.path.join(P8DIR, "cache"))):
        if f.startswith(f"ball_{tag}_M") and f.endswith(".npz") and "ckpt" not in f:
            z = np.load(os.path.join(P8DIR, "cache", f))
            if z["states"].shape[0] >= tot and np.array_equal(z["states"][:tot], allst):
                return allst, np.array(z["vals"][:tot], dtype=float), f
    return None, None, None


def make_lookup(allst, vals):
    radix = np.array([int(np.prod(k[i + 1:])) for i in range(n)], dtype=np.int64)
    code = allst.astype(np.int64) @ radix; order = np.argsort(code); code_s = code[order]; vals_s = vals[order]

    def lookup(st):
        c = np.atleast_2d(st).astype(np.int64) @ radix; p = np.searchsorted(code_s, c); assert np.array_equal(code_s[np.minimum(p, len(code_s) - 1)], c), "state outside the ball"
        return vals_s[p]
    return lookup


res = dict(seq=seq, m=m)
# ---------------------------------------------------------------- (a)
if "--noa" not in a:
    allst, vals, fb = load_ball(m)
    if allst is None:
        log(f"(a) no cached ball of radius {m} for this peptide: check (a) not available at this order")
    else:
        lookup = make_lookup(allst, vals)
        d, nb, _ = pw.anchored_terms(G, x0, m, energy=lookup, cache_file=None)
        nst = 0; viol = 0; vmin = 0; vroll = 0; rmin = np.inf; worst = None; big = 0; ratios = []
        for T, tab in zip(subs, tabs):
            dT = np.abs(d[T][np.ix_(*[non[i] for i in T])])
            nst += dT.size; viol += int((dT > tab * (1 + 1e-12) + 1e-10).sum())
            vmin += int((dT > tab.min() * (1 + 1e-12) + 1e-10).sum()); vroll += int((dT > roll_tab(tab) * (1 + 1e-12) + 1e-10).sum())
            mk = dT > 1e-9
            if mk.any():
                r = tab[mk] / dT[mk]; ratios.append(r)
                if r.min() < rmin:
                    rmin = float(r.min()); worst = T
        ratios = np.concatenate(ratios) if ratios else np.zeros(0)
        log(f"(a) ball of radius {m} from ws_P8/cache/{fb}; every state with exactly {m} sites off the anchor: {nst} states in {len(subs)} subsets: "
            f"|d_T(x_T)| <= Theta^2_T(x_T) violated at {viol}; smallest ratio bound / exact term {rmin:.3f} (subset {worst}); median ratio {np.median(ratios):.1f} over the {len(ratios)} states with |d_T| > 1e-9 kcal/mol; "
            f"CONTROLS: minimum over the states in place of the value: {vmin} violations; table rolled by one rotamer: {vroll} violations  -> {'both FAIL as intended' if vmin and vroll else 'A CONTROL DOES NOT FAIL'} [{time.time() - t0:.0f}s]")
        res["a"] = dict(states=int(nst), viol=viol, min_ratio=rmin, median_ratio=float(np.median(ratios)), ctl_min=vmin, ctl_roll=vroll)
        del d, allst, vals
# ---------------------------------------------------------------- (b)
if "--nob" not in a:
    def interp(X, lookup):
        out = np.empty(len(X))
        for a_, row in enumerate(X):
            Sx = [i for i in range(n) if row[i] != x0[i]]; s = len(Sx)
            if s <= M:
                out[a_] = lookup(row[None])[0]; continue
            tot = 0.0
            for v in range(0, M + 1):
                c = (-1) ** (M - v) * math.comb(s - v - 1, M - v)
                sts = np.tile(np.asarray(x0), (math.comb(s, v), 1))
                for b_, U in enumerate(itertools.combinations(Sx, v)):
                    sts[b_, list(U)] = row[list(U)]
                tot += c * float(lookup(sts).sum())
            out[a_] = tot
        return out

    # self-test of the formula on a random table
    rngt = np.random.default_rng(3); shp = (3, 2, 4, 3, 2, 3); xt = [1, 0, 2, 1, 1, 0]; Ft = rngt.standard_normal(shp)
    gridt = np.stack(np.meshgrid(*[np.arange(v) for v in shp], indexing="ij"), axis=-1).reshape(-1, len(shp))
    n_, x0_, M_ = n, x0, M
    devt = 0.0
    for Mt in (1, 2, 3, 4):
        n, x0, M = len(shp), xt, Mt
        It = interp(gridt, lambda st_: Ft[tuple(np.atleast_2d(st_).T)])
        devt = max(devt, float(np.abs((Ft.reshape(-1) - It) - remainder_grid(Ft, xt, Mt + 1).reshape(-1)).max()))
    n, x0, M = n_, x0_, M_
    allst, vals, fb = load_ball(M); assert allst is not None, "no cached ball"
    lookup = make_lookup(allst, vals); del allst
    rng = np.random.default_rng(777); mob = [i for i in range(n) if k[i] > 1]; XR = []; NR = 250
    for s in range(m, n + 1):
        for _ in range(NR):
            x = np.array(x0); Sx = rng.choice(mob, size=s, replace=False)
            for i in Sx:
                x[i] = rng.choice(non[i])
            XR.append(x)
    XR = np.array(XR); gR = np.concatenate([G.bulk_energy(XR[s:s + 250]) for s in range(0, len(XR), 250)])
    R = np.abs(gR - interp(XR, lookup)); sR = (XR != np.array(x0)[None]).sum(1)
    pos = [np.full(k[i], -1) for i in range(n)]
    for i in range(n):
        pos[i][non[i]] = np.arange(len(non[i]))
    P = np.stack([pos[i][XR[:, i]] for i in range(n)], axis=1)
    env = np.zeros(len(XR)); envr = np.zeros(len(XR))
    for T, tab in zip(subs, tabs):
        I = P[:, list(T)]; inS = (I >= 0).all(axis=1)
        if inS.any():
            env[inS] += tab[tuple(I[inS].T)]; envr[inS] += roll_tab(tab)[tuple(I[inS].T)]
    LD = Loaded(os.path.join(OUT, f"tables_{tag}_m{m}_w7.npz")); envA = const_envelope(subs, LD.TB[1].sab, XR, x0)
    log(f"(b) self-test of the interpolation formula against the grid recursion (random table, M = 1..4): largest deviation {devt:.1e}; ball of radius {M} from ws_P8/cache/{fb}; "
        f"{len(XR)} uniformly random states, {NR} for each number s of sites off the anchor, g evaluated here [{time.time() - t0:.0f}s]")
    log("| s | states | largest |g - I g| (kcal/mol) | violations of |g - I g| <= resolved envelope | smallest envelope / |g - I g| | median envelope (kcal/mol): resolved stage 2; P8's constants | control (tables rolled by one rotamer): violations |")
    log("|---|---|---|---|---|---|---|")
    rb = {}
    for s in range(m, n + 1):
        sel = sR == s; v = int((R[sel] > env[sel] * (1 + 1e-12) + 1e-9).sum()); vr = int((R[sel] > envr[sel] * (1 + 1e-12) + 1e-9).sum())
        ratio = float((env[sel] / np.maximum(R[sel], 1e-300)).min())
        rb[s] = dict(viol=v, min_ratio=ratio, maxR=float(R[sel].max()), ctl_roll=vr, med_env=float(np.median(env[sel])), med_envA=float(np.median(envA[sel])))
        log(f"| {s} | {int(sel.sum())} | {R[sel].max():.4g} | {v} | {ratio:.2f} | {np.median(env[sel]):.3g}; {np.median(envA[sel]):.3g} | {vr} |")
    res["b"] = dict(states=int(len(XR)), viol=int(sum(r["viol"] for r in rb.values())), min_ratio=float(min(r["min_ratio"] for r in rb.values())), ctl_roll=int(sum(r["ctl_roll"] for r in rb.values())), by_s=rb)
    log(f"    in all: {res['b']['viol']} violations at {len(XR)} random states; smallest ratio {res['b']['min_ratio']:.2f}; control: {res['b']['ctl_roll']} violations")
# ---------------------------------------------------------------- (c)
if "--shell" in a:
    NC = int(a[a.index("--shell") + 1])
    allst, vals, fb = load_ball(M); assert allst is not None, "no cached ball"
    lookup = make_lookup(allst, vals); del allst
    rng = np.random.default_rng(4321); XS = np.tile(np.array(x0), (NC, 1)); which = rng.integers(0, len(subs), size=NC)
    for a_ in range(NC):
        for i in subs[which[a_]]:
            XS[a_, i] = rng.choice(non[i])
    t1 = time.time(); gS = np.concatenate([G.bulk_energy(XS[s_:s_ + 250]) for s_ in range(0, NC, 250)])
    # with exactly m sites off the anchor: g - I_{m-1} g = d_T(x_T) = sum over U subset T of (-1)^(m-|U|) g(x_U, x0)
    dT = gS.copy()
    for v in range(0, m):
        sgn = (-1) ** (m - v)
        for pos_ in itertools.combinations(range(m), v):
            sts = np.tile(np.array(x0), (NC, 1))
            for a_ in range(NC):
                T = subs[which[a_]]
                for p_ in pos_:
                    sts[a_, T[p_]] = XS[a_, T[p_]]
            dT += sgn * lookup(sts)
    dT = np.abs(dT)
    pos = [np.full(k[i], -1) for i in range(n)]
    for i in range(n):
        pos[i][non[i]] = np.arange(len(non[i]))
    th = np.empty(NC); thmin = np.empty(NC); throll = np.empty(NC)
    for a_ in range(NC):
        T = subs[which[a_]]; idx = tuple(pos[i][XS[a_, i]] for i in T); tab = tabs[which[a_]]
        th[a_] = tab[idx]; thmin[a_] = tab.min(); throll[a_] = roll_tab(tab)[idx]
    viol = int((dT > th * (1 + 1e-12) + 1e-9).sum()); vmin = int((dT > thmin * (1 + 1e-12) + 1e-9).sum()); vroll = int((dT > throll * (1 + 1e-12) + 1e-9).sum())
    mk = dT > 1e-9; ratio = th[mk] / dT[mk]
    log(f"(c) {NC} random states with EXACTLY {m} sites off the anchor (subset and rotamers uniformly at random; g evaluated here, {time.time() - t1:.0f} s; lower orders from the ball of radius {M}): "
        f"|d_T(x_T)| <= Theta^2_T(x_T) violated at {viol}; smallest ratio {ratio.min():.2f}, median {np.median(ratio):.0f} over the {int(mk.sum())} states with |d_T| > 1e-9 kcal/mol; largest |d_T| {dT.max():.3g} kcal/mol; "
        f"CONTROLS: minimum over the states in place of the value: {vmin} violations; table rolled by one rotamer: {vroll} violations  -> {'both FAIL as intended' if vmin and vroll else 'A CONTROL DOES NOT FAIL'}")
    res["c"] = dict(states=NC, viol=viol, min_ratio=float(ratio.min()), median_ratio=float(np.median(ratio)), ctl_min=vmin, ctl_roll=vroll, n_nonzero=int(mk.sum()))
json.dump(res, open(os.path.join(OUT, f"check12_{tag}_m{m}" + ("_shell" if "--shell" in a else "") + ".json"), "w"), indent=1)
log.done()
