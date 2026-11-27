#!/usr/bin/env python3
"""P9 step 1 -- VALIDATION BY ENUMERATION of the state-resolved bounds and of every table form built from them.

Instance: SEQ on the helix (P2's pruned product domain as workstreams P3 / P8 use it), every order m = 3..n.

LEFT SIDES (my own code; P3's evaluator only supplies coordinates and Born radii):
  g(x) at every state (P3's bulk evaluator, cached here; compared with P8's stored enumeration);
  every term tau = t_pq (p <= q) at every state from coordinates and Born radii; sum of the terms against g;
  R_m(x)      = |g(x) - I_{m-1} g(x)|                               (whole function)
  L_m[Bk](x)  = sum_{tau in block Bk} |tau(x) - I_{m-1} tau(x)|     (block by block, absolute values term by term)
  with I_{m-1} by inclusion-exclusion on the grid (remainders_all), self-tested against the successive-difference
  recursion (p9lib.remainder_grid) on a random table and on g.

RIGHT SIDES, stage s = 1 (hosts resolved) and s = 2 (hosts and non-host sites resolved):
  E^s[Bk](x) = sum_{T subset S(x), |T| = m} Theta^s_{Bk,T}(x_T)      (block envelope),      E^s = sum over blocks.

CHECKS (every one at EVERY state)
  V1  L_m[Bk] <= E^s[Bk]   for every block           -- the statement proved (Theorem AH before the maximum), sharp:
                                                        no cancellation between blocks can hide a block that is too small;
  V2  R_m <= E^s                                      -- the hypothesis the certificate needs, resolved;
  V3  E^s <= pen^{s,form}  and  R_m <= pen^{s,form}   -- every table form: site 'S'; pair 'B' and triple 'T' with all
                                                        pairs / triples in band, and with narrow bands w = 1, 2 (the
                                                        chains for what is out of band / out of window); the window
                                                        form 'W' with window 2 and with everything in the window
                                                        (then W is the envelope itself);
  V4  resolved <= state-independent, pointwise: pen^{s,form} <= the same form with the joint maxima cJ^s <= with P8's 'SAb'.
CONTROLS that must FAIL (a check that cannot fail checks nothing):
  W1  the MINIMUM over the states in place of the value at the state (block tables; site/pair/triple tables);
  W2  the value at a WRONG rotamer: every table rolled by one position along each of its state axes;
  W4  shares that do not add up: the banded forms with the out-of-band / out-of-window parts dropped.
  For each control: violations at block level (V1), of the whole function (V2 / V3), and of "tables dominate the
  envelope" (E^s <= pen), which is the sharp form of the table statement.

usage: python3 -B p9_01_validate.py SEQ      writes logs/validate_<tag>.log, out/validate_<tag>.json
"""
import sys
from p9lib import *

seq = sys.argv[1]; bb = "H"; tau = tau_of(seq); tag = tagname(seq, bb, tau)
log = Log(os.path.join(LOGS, f"validate_{tag}.log"))
log(f"=== p9_01_validate {seq} on {bb}, tau {tau}; started {now()}")
G, c0, h, J, x0, E0 = setup(seq, bb, tau); n, k = G.ns, list(G.k); shape = tuple(k); N = G.nat
st, g, src = enumerate_g(G, tag); S = len(st)
f = pw.f_energy(st, c0, h, J); E = f + g
wB = np.exp(-BETA * (E - E.min())); lnZ = float(-BETA * E.min() + math.log(wB.sum())); wB /= wB.sum()
chg = st != np.array(x0)[None]
log(f"    {N} atoms, {n} sites, states per site {k}, {S} states, anchor {x0}; g: {src}; exact ln Z = {lnZ:.6f}; "
    f"mean number of sites off the anchor in the true ensemble {float((wB * chg.sum(1)).sum()):.3f}")
fm = os.path.join(P8DIR, "out", f"m1_{tag}.npz")
if os.path.exists(fm):
    Z8 = np.load(fm)
    if "g" in Z8.files and Z8["g"].shape == g.shape:
        log(f"    P8's stored enumeration of g (ws_P8/out/m1_{tag}.npz) against mine: largest deviation {float(np.abs(Z8['g'] - g).max()):.2e} kcal/mol; its anchor equals mine: {[int(v) for v in Z8['anchor']] == x0}")
orders = list(range(3, n + 1)); TOL = 1e-10


def remainders_all(F, orders):
    """yields (m, |F - I_{m-1} F|) for m in orders; F of shape `shape` + trailing axes."""
    acc = np.zeros_like(F); extra = F.shape[n:]
    for r in range(0, max(orders)):
        for U in itertools.combinations(range(n), r):
            idx = tuple(slice(None) if i in U else x0[i] for i in range(n))
            dd = F[idx]
            for a_, i in enumerate(U):
                dd = dd - np.take(dd, [x0[i]], axis=a_)
            acc += dd.reshape([shape[i] if i in U else 1 for i in range(n)] + list(extra))
        if (r + 1) in orders:
            yield r + 1, np.abs(F - acc)


# ---- self-test of the remainder code
rng = np.random.default_rng(1); Fr = rng.standard_normal(shape) if S <= 20000 else None
dev = 0.0
for m, R in remainders_all((Fr if Fr is not None else g.reshape(shape)), orders):
    dev = max(dev, float(np.abs(R - np.abs(remainder_grid((Fr if Fr is not None else g.reshape(shape)), x0, m))).max()))
log(f"(0) self-test: inclusion-exclusion remainder against the successive-difference recursion on {'a random table' if Fr is not None else 'g'} of this shape, orders {orders}: largest deviation {dev:.1e}")
Rg = {m: R.reshape(-1) for m, R in remainders_all(g.reshape(shape), orders)}

# ---- blocks, exact block remainders at every state
site_of = -np.ones(N, dtype=int)
for l in range(n):
    site_of[G.mov[l]] = l
blocks = [("self", -1), ("cross1", -1)]
for l in range(n):
    blocks += [("self", l), ("cross1", l)] + [("cross2", l, l2) for l2 in range(l + 1, n)]
bindex = {b: i for i, b in enumerate(blocks)}; nB = len(blocks)


def block_of(p, q):
    hp, hq = int(site_of[p]), int(site_of[q])
    if p == q:
        return bindex[("self", hp)]
    hs = sorted({hp, hq} - {-1})
    return bindex[("cross1", -1)] if not hs else bindex[("cross1", hs[0])] if len(hs) == 1 else bindex[("cross2", hs[0], hs[1])]


t0 = time.time()
PRE = -KAPPA / KCAL
ib = np.empty((S, N)); X = np.empty((S, N, 3))
for s0 in range(0, S, 8192):
    sub = st[s0:s0 + 8192]; ib[s0:s0 + 8192] = G.invB(G.descreening(sub)); X[s0:s0 + 8192] = G.coords(sub)
Bo = 1.0 / ib
L = np.zeros((len(orders), nB, S)); gsum = np.zeros(S)
for p in range(N):
    cols = np.arange(p, N)
    d = X[:, p, None, :] - X[:, cols, :]; r2 = (d * d).sum(-1); del d
    BB = Bo[:, p, None] * Bo[:, cols]
    t = PRE * G.q[p] * G.q[cols][None, :] / np.sqrt(r2 + BB * np.exp(-r2 / (4.0 * BB)))
    t[:, 0] *= 0.5                                           # the self term t_pp = -(KAPPA/2) q_p^2 / B_p
    gsum += t.sum(axis=1)
    bcol = np.array([block_of(p, q) for q in cols])
    for m, R in remainders_all(t.reshape(shape + (len(cols),)), orders):
        R = R.reshape(S, len(cols))
        for b_ in np.unique(bcol):
            L[orders.index(m), b_] += R[:, bcol == b_].sum(axis=1)
    del t, r2, BB
del X, ib, Bo
log(f"(1) every term t_pq at every state ({N * (N + 1) // 2} terms x {S} states), my own evaluation from coordinates and Born radii: "
    f"sum of the terms against g: largest deviation {float(np.abs(gsum - g).max()):.2e} kcal/mol; exact block remainders L_m[Bk](x) for {nB} blocks, orders {orders} [{time.time() - t0:.0f}s, peak RSS {peak_rss():.0f} MB]")
fck = os.path.join(P8DIR, "cache", f"bc_{tag}_ckpt.npz")
if os.path.exists(fck):
    try:
        zc = np.load(fck)
        if int(zc["p_next"]) == N and zc["ACCR"].shape == L.shape:
            b8 = [("self", -1), ("cross1", -1)] + [(kind, l) for l in range(n) for kind in ("self", "cross1")] + [("cross2", l, l2) for l in range(n) for l2 in range(l + 1, n)]   # P8's order of the blocks (p8_03c_blockcheck.py)
            perm = [b8.index(b) for b in blocks]
            log(f"    P8's stored block remainders (ws_P8/cache/bc_{tag}_ckpt.npz, array ACCR; P8's own enumeration pass, blocks re-ordered to mine) against mine: largest deviation {float(np.abs(zc['ACCR'][:, perm] - L).max()):.2e} kcal/mol")
    except Exception as e:
        log(f"    (P8's checkpoint could not be compared: {type(e).__name__})")

# ---- right sides
SR = ResBound(G, tuple(x0), EnvelopeSup(G), K=n)
RES = Resolver(SR)
gshape = lambda T: [k[i] if i in T else 1 for i in range(n)]
non = RES.non


def embed(T, tab):
    """table on the non-anchor states of T (broadcastable) -> grid-broadcastable array, zero where a site of T is at the anchor."""
    full = np.zeros([k[t] for t in T])
    full[np.ix_(*[non[t] for t in T])] = np.broadcast_to(tab, [len(non[t]) for t in T])
    return full.reshape(gshape(T))


def roll_tab(tab):
    out = tab
    for ax in range(tab.ndim):
        if tab.shape[ax] > 1:
            out = np.roll(out, 1, axis=ax)
    return out


def transform_tables(TB, kind):
    """a copy of the top-level sums with every table replaced by a WRONG one: 'min' = its minimum over the non-anchor
    entries, 'roll' = rolled by one along every state axis (within the non-anchor states)."""
    W = Tables(TB.n, TB.k, TB.x0, TB.m, keep=False); W.subs = TB.subs
    def tr(tab, sites):
        sub = tab[np.ix_(*[non[i] for i in sites])]
        new = np.full(sub.shape, sub.min()) if kind == "min" else roll_tab(sub)
        out = np.zeros_like(tab); out[np.ix_(*[non[i] for i in sites])] = new
        return out
    W.S1 = [tr(TB.S1[i], [i]) for i in range(TB.n)]
    W.S2 = {key: tr(v, list(key)) for key, v in TB.S2.items()}
    W.S3 = {key: tr(v, list(key)) for key, v in TB.S3.items()}
    return W


def drop_far(TB, form, w):
    """control W4: the banded form WITHOUT the parts that the chain moves from out-of-band pairs / out-of-window triples."""
    g1, g2, g3 = form_tables(TB, form, n)          # everything in band: the top-level tables
    g2 = {key: v for key, v in g2.items() if key[1] - key[0] <= w}
    g3 = {key: v for key, v in g3.items() if key[2] - key[0] <= w}
    return [np.zeros(k[i]) for i in range(n)], g2, g3


def wpen(X, tabs):
    out = np.zeros(len(X))
    for part in tabs:
        for K, t in part.items():
            out += t[tuple(X[:, u] for u in K)]
    return out


def transform_W(W, kind):
    out = {}
    for K, tab in W.items():
        sub = tab[np.ix_(*[non[i] for i in K])]
        new = np.full(sub.shape, sub.min()) if kind == "min" else roll_tab(sub)
        t = np.zeros_like(tab); t[np.ix_(*[non[i] for i in K])] = new; out[K] = t
    return out


res = dict(seq=seq, tau=tau, lnZ=lnZ, orders={})
XG = st[np.random.default_rng(4242).choice(S, size=960, p=wB)]             # guides the choice of sub-tuples in the window form: exact samples of the true ensemble
poffG = off_frequencies(XG, k, x0)
FORMS = [("S", n)] + [("B", w) for w in sorted({n, 2, 1}, reverse=True)] + [("T", w) for w in sorted({n, 2}, reverse=True)] + [("W", w) for w in sorted({n, 2}, reverse=True)]
for mi, m in enumerate(orders):
    t1 = time.time(); subs = list(itertools.combinations(range(n), m)); R = Rg[m]; nz = R > 1e-9
    Eb = {s: np.zeros((nB,) + shape) for s in (1, 2)}; EbW = {(s, c): np.zeros((nB,) + shape) for s in (1, 2) for c in ("min", "roll")}
    ACC = {ww: Acc(n, k, x0, m, ww, {4242: XG}) for ww in (2, n)}          # window form with a narrow window and with everything in the window
    for jT, T in enumerate(subs):
        th = {}
        for s in (1, 2):
            out, blk = RES.blocks(m, T, s)
            tab = np.zeros([len(non[t]) for t in T])
            for key, t in blk:
                b_ = bindex[key]; Eb[s][b_] += embed(T, t); tab = tab + t
                EbW[(s, "min")][b_] += embed(T, np.full_like(t, t.min())); EbW[(s, "roll")][b_] += embed(T, roll_tab(t))
            th[s] = tab
        for ww in ACC:
            ACC[ww].add(jT, T, th[1], th[2], float(sum(out["SAb"].values())), float(sum(out["Sb"].values())))
    TB = ACC[n].TB
    row = dict(subsets=len(subs)); res["orders"][str(m)] = row
    log(f"--- order m = {m}: {len(subs)} subsets, {int((chg.sum(1) >= m).sum())} states with >= m sites off the anchor; largest R_m = {R.max():.4g} kcal/mol, Boltzmann mean of beta R_m = {BETA * (wB * R).sum():.3e} [{time.time() - t1:.0f}s]")
    for s in (1, 2):
        TB[s].finish(); Ebs = Eb[s].reshape(nB, S); Es = Ebs.sum(axis=0); Lm = L[mi]
        v1 = int((Lm > Ebs * (1 + 1e-12) + TOL).sum()); mk = Lm > 1e-9
        r1 = float((Ebs[mk] / Lm[mk]).min()) if mk.any() else float("nan")
        v2 = int((R > Es * (1 + 1e-12) + TOL).sum()); r2_ = float((Es[nz] / R[nz]).min())
        log(f"    stage {s}: V1 block level: {nB * S} comparisons, violations {v1}, smallest E[Bk]/L[Bk] {r1:.4f} | V2 whole function: {S} states, violations {v2}, smallest E/R {r2_:.3f} | "
            f"Boltzmann means (kT): envelope {BETA * (wB * Es).sum():.3e}, ratio to the remainder {(wB * Es).sum() / max((wB * R).sum(), 1e-300):.1f}; "
            f"Gamma (kT): SAb {BETA * TB[s].sab.sum():.5g}, joint maximum cJ {BETA * TB[s].cJ.sum():.5g}, minimum over states {BETA * TB[s].cmin.sum():.5g}")
        row[f"stage{s}"] = dict(V1_viol=v1, V1_min_ratio=r1, V2_viol=v2, V2_min_ratio=r2_, mean_env_kT=float(BETA * (wB * Es).sum()), mean_R_kT=float(BETA * (wB * R).sum()),
                                Gamma_SAb=float(BETA * TB[s].sab.sum()), Gamma_cJ=float(BETA * TB[s].cJ.sum()))
        for c, name in (("min", "W1 minimum over the states"), ("roll", "W2 value at a wrong rotamer")):
            Ew = EbW[(s, c)].reshape(nB, S); w1 = int((Lm > Ew * (1 + 1e-12) + TOL).sum()); w2 = int((R > Ew.sum(0) * (1 + 1e-12) + TOL).sum())
            log(f"        CONTROL {name} (block tables): violations at block level {w1}, of the whole function {w2}   -> {'FAILS as intended' if w1 > 0 else 'DOES NOT FAIL'}")
            row[f"stage{s}"][f"ctl_{c}_block"] = w1; row[f"stage{s}"][f"ctl_{c}_whole"] = w2
        cells = []
        for form, w in FORMS:
            if form == "W":
                pen = wpen(st, window_form(ACC[w].W[s]))
                penJ = wpen(st, window_form_const(subs, TB[s].cJ, k, x0, w, poffG)); penA = wpen(st, window_form_const(subs, TB[s].sab, k, x0, w, poffG))
            else:
                pen = pen_value(st, *form_tables(TB[s], form, w))
                penJ = pen_value(st, *form_tables(TB[s], form, w, resolved=False, const=TB[s].cJ))
                penA = pen_value(st, *form_tables(TB[s], form, w, resolved=False, const=TB[s].sab))
            va = int((Es > pen * (1 + 1e-12) + TOL).sum()); vb = int((R > pen * (1 + 1e-12) + TOL).sum())
            # W: the constant forms choose their sub-tuples by another rule than the resolved one, so only cJ <= SAb is a pointwise chain there
            vc = int(((pen > penJ * (1 + 1e-9) + TOL).sum() if form != "W" else 0) + (penJ > penA * (1 + 1e-9) + TOL).sum())
            if form == "W":
                EJ = const_envelope(subs, TB[s].cJ, st, x0); vc += int((EJ > penJ * (1 + 1e-12) + TOL).sum())
            ctl = []
            for c in ("min", "roll"):
                pw_ = wpen(st, window_form(transform_W(ACC[w].W[s], c))) if form == "W" else pen_value(st, *form_tables(transform_tables(TB[s], c), form, w))
                ctl.append((int((Es > pw_ * (1 + 1e-12) + TOL).sum()), int((R > pw_ * (1 + 1e-12) + TOL).sum())))
            if w < n and form in "BT":
                pd = pen_value(st, *drop_far(TB[s], form, w)); ctl.append((int((Es > pd * (1 + 1e-12) + TOL).sum()), int((R > pd * (1 + 1e-12) + TOL).sum())))
            lab = form + ("" if form == "S" else f"(w={w})" if w < n else "(all in band)")
            if form == "W" and w == n:
                row[f"stage{s}"]["W_equals_envelope"] = float(np.abs(pen - Es * RND).max())
            row[f"stage{s}"][lab] = dict(env_viol=va, R_viol=vb, chain_viol=vc, min_ratio=float((pen[nz] / R[nz]).min()), mean_kT=float(BETA * (wB * pen).sum()),
                                         mean_cJ_kT=float(BETA * (wB * penJ).sum()), mean_SAb_kT=float(BETA * (wB * penA).sum()), controls=ctl)
            cells.append(f"{lab}: E<=pen violated {va}, R<=pen violated {vb}, chain resolved<=cJ<=SAb violated {vc}, smallest pen/R {(pen[nz] / R[nz]).min():.2f}, "
                         f"Boltzmann mean beta pen {BETA * (wB * pen).sum():.3e} (cJ {BETA * (wB * penJ).sum():.3e}, SAb {BETA * (wB * penA).sum():.3e}); "
                         f"controls [E<=pen violated, R<=pen violated]: W1 min {list(ctl[0])}, W2 roll {list(ctl[1])}" + (f", W4 far parts dropped {list(ctl[2])}" if len(ctl) > 2 else ""))
        for c_ in cells:
            log("        " + c_)
json.dump(res, open(os.path.join(OUT, f"validate_{tag}.json"), "w"), indent=1)
log.done()
