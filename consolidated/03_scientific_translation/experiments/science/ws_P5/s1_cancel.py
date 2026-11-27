"""
P5 step 1 -- is the cancellation there at the order that matters, and at which level of grouping?

For an enumerated instance and every subset T of sites of order 3..maxorder, EXACT anchored
constants c_T^anch (sup over all contexts and all non-anchor states of T; kcal/mol) of

  total     g                                   (the truth to be bounded)
  self      sum_p W_pp                          cross   sum_{p != q} W_pq
  pair      sum over atom pairs of c_T(term)    = the smallest value ANY bound can have that bounds
                                                  every atom-pair term (and self term) separately
  ag[G]     sum over (atom p, group Q) of c_T( sum_{q in Q} W_pq )     signs kept inside a group, for one atom
  gg[G]     sum over ordered group pairs of c_T( sum_{p in P, q in Q} W_pq )
  atom      sum over atoms p of c_T( sum_q W_pq )                      signs kept over ALL partners of one atom
  grp[G]    sum over groups P of c_T( sum_{p in P} sum_q W_pq )
  agx[G], ggx[G]   the same as ag, gg for the CROSS part alone (the diagonal p = q removed): "the cross part
            regrouped by groups"; cross <= ggx, agx <= pair_cross
  P3        P3's certified term-by-term bound chat_T (gfbound.GFBound.total(m, T)), self and cross parts

for the groupings G of p5lib.groupings.  W_pq = -(KAPPA/2) q_p q_q M_pq / KCAL, g = sum_{p,q} W_pq.
All of them are >= c_T^anch(g) (triangle inequality); 'pair' >= 'ag' >= 'atom' and 'pair' >= 'gg' >= 'grp'.

usage: python3 -B s1_cancel.py SEQ BB TAU [maxorder=5] [--nop3] [--blk DOUBLES_PER_BLOCK] [--gg name,name]
                                [--rows a:b]   only the atom rows a..b-1; partial sums -> out/tmp/s1_<tag>_rows<a>-<b>.npz
                                [--merge]      finish from the partial files of out/tmp/ (they must cover all rows)
                                [--p3max K]    P3's bound subset by subset only up to order K (it costs about a second
                                               per subset at order 6 and 240 atoms); above K only its closed-form sum Gamma_m
writes logs/s1_<SEQ>_<BB>_<TAU>.log and out/s1_<SEQ>_<BB>_<TAU>.json
"""
import sys, os, json, time, itertools, glob
import numpy as np
from p5lib import *

a = sys.argv[1:]
seq, bb, tau = a[0], a[1], float(a[2])
maxorder = int(a[3]) if len(a) > 3 and not a[3].startswith("--") else 5
nop3 = "--nop3" in a
BLK = float(a[a.index("--blk") + 1]) if "--blk" in a else 6e7
GGSEL = a[a.index("--gg") + 1].split(",") if "--gg" in a else None
ROWS = [int(v) for v in a[a.index("--rows") + 1].split(":")] if "--rows" in a else None
MERGE = "--merge" in a
P3MAX = int(a[a.index("--p3max") + 1]) if "--p3max" in a else 99
tag = f"{seq}_{bb}_{tau:.2f}"
TMP = os.path.join(HERE, "out", "tmp")
logname = f"s1_{tag}.log" if ROWS is None else f"s1_{tag}_rows{ROWS[0]}-{ROWS[1]}.log"
log = Tee(os.path.join(HERE, "logs", logname))
t0 = time.time()
G, st, shape, f, g, E, x0 = build(seq, bb, tau)
n, N, S = G.ns, G.nat, len(st)
maxorder = min(maxorder, n)
log(f"=== s1_cancel: {seq} on {bb}, tau {tau}: atoms {N}, sites {n}, domain {list(shape)} = {S} states; anchor x0 = argmin E = {x0}"
    + (f"; ROWS {ROWS}" if ROWS else "") + ("; MERGE" if MERGE else ""))
grp = groupings(G)
for nm, lab in grp.items():
    qc = group_charges(G, lab)
    log(f"    grouping '{nm}': {lab.max() + 1} groups; |group charge|: max {np.abs(qc).max():.4f}, mean {np.abs(qc).mean():.4f} e")
Tlist = subsets(n, shape, 3, maxorder)
ggnames = [nm for nm in grp if GGSEL is None or nm in GGSEL]
acckeys = ["pair_self", "pair_cross", "atom"] + [f"ag_{nm}" for nm in grp] + [f"agx_{nm}" for nm in grp]


def phase_A(r0, r1):
    """partial sums over the atom rows r0..r1-1."""
    B = 1.0 / G.invB(G.descreening(st))
    X = G.coords(st)
    R = max(1, min(N, int(BLK // (S * N))))
    blocks = [np.arange(s, min(r1, s + R)) for s in range(r0, r1, R)]
    log(f"    {len(Tlist)} subsets of order 3..{maxorder}; rows {r0}..{r1 - 1} in blocks of {R} atoms ({len(blocks)} blocks)")
    acc = {k: np.zeros(len(Tlist)) for k in acckeys}
    tot = np.zeros(S); sf = np.zeros(S)
    GG = {nm: np.zeros((S, grp[nm].max() + 1, grp[nm].max() + 1)) for nm in ggnames}
    GGx = {nm: np.zeros((S, grp[nm].max() + 1, grp[nm].max() + 1)) for nm in ggnames}
    ind = {nm: (lab[:, None] == np.arange(lab.max() + 1)[None, :]).astype(float) for nm, lab in grp.items()}   # (N, nG)
    for bi, rows in enumerate(blocks):
        W = weights(G, kernel_rows(G, st, rows, B, X), rows)                 # (S, R, N)
        tot += W.sum(axis=(1, 2))
        sf += W[:, np.arange(len(rows)), rows].sum(axis=1)
        c = anch_consts(W.reshape(shape + W.shape[1:]), x0, n, maxorder)     # pair level
        diag = (np.arange(len(rows)), rows)
        for ti, T in enumerate(Tlist):
            cs = float(c[T][diag].sum())
            acc["pair_self"][ti] += cs
            acc["pair_cross"][ti] += float(c[T].sum()) - cs
        del c
        U = W.sum(axis=2)                                                    # atom level
        c = anch_consts(U.reshape(shape + U.shape[1:]), x0, n, maxorder)
        for ti, T in enumerate(Tlist):
            acc["atom"][ti] += float(c[T].sum())
        for nm in grp:                                                       # atom x group; accumulate group x group
            V = W @ ind[nm]                                                  # (S, R, nG)
            c = anch_consts(V.reshape(shape + V.shape[1:]), x0, n, maxorder)
            for ti, T in enumerate(Tlist):
                acc[f"ag_{nm}"][ti] += float(c[T].sum())
            if nm in GG:
                GG[nm] += np.einsum("srg,rh->shg", V, ind[nm][rows])         # (S, P, Q): sum over p in P of V[p, Q]
            del V
        W[:, np.arange(len(rows)), rows] = 0.0                               # cross part alone from here on
        for nm in grp:
            V = W @ ind[nm]
            c = anch_consts(V.reshape(shape + V.shape[1:]), x0, n, maxorder)
            for ti, T in enumerate(Tlist):
                acc[f"agx_{nm}"][ti] += float(c[T].sum())
            if nm in GGx:
                GGx[nm] += np.einsum("srg,rh->shg", V, ind[nm][rows])
            del V
        del W
        if bi % 4 == 0 or bi == len(blocks) - 1:
            log(f"    block {bi + 1}/{len(blocks)} done, {time.time() - t0:.0f} s")
    return acc, tot, sf, GG, GGx


if ROWS is not None:
    acc, tot, sf, GG, GGx = phase_A(ROWS[0], ROWS[1])
    os.makedirs(TMP, exist_ok=True)
    np.savez(os.path.join(TMP, f"s1_{tag}_rows{ROWS[0]}-{ROWS[1]}.npz"), rows=np.array(ROWS), tot=tot, sf=sf,
             **{f"acc_{k}": v for k, v in acc.items()}, **{f"GG_{nm}": v for nm, v in GG.items()},
             **{f"GGx_{nm}": v for nm, v in GGx.items()})
    log.done()
    sys.exit(0)
if MERGE:
    files = sorted(glob.glob(os.path.join(TMP, f"s1_{tag}_rows*.npz")))
    cover = np.zeros(N, dtype=int)
    acc = {k: np.zeros(len(Tlist)) for k in acckeys}
    tot = np.zeros(S); sf = np.zeros(S)
    GG = {nm: np.zeros((S, grp[nm].max() + 1, grp[nm].max() + 1)) for nm in ggnames}
    GGx = {nm: np.zeros((S, grp[nm].max() + 1, grp[nm].max() + 1)) for nm in ggnames}
    for fn in files:
        z = np.load(fn)
        cover[z["rows"][0]:z["rows"][1]] += 1
        tot += z["tot"]; sf += z["sf"]
        for k in acckeys:
            acc[k] += z[f"acc_{k}"]
        for nm in ggnames:
            GG[nm] += z[f"GG_{nm}"]; GGx[nm] += z[f"GGx_{nm}"]
        log(f"    merged {os.path.basename(fn)}")
    assert np.all(cover == 1), "the partial files do not cover every atom row exactly once"
else:
    acc, tot, sf, GG, GGx = phase_A(0, N)

err = float(np.abs(tot - g.reshape(-1)).max())
log(f"    check: sum_pq W_pq equals P3's evaluator G.energy at all {S} states to {err:.2e} kcal/mol")
assert err < 1e-8
cr = tot - sf
res = dict(seq=seq, bb=bb, tau=tau, natoms=N, n=n, shape=list(shape), anchor=list(x0), nstates=S, maxorder=maxorder)
C = {}
for nm, arr in (("total", tot), ("self", sf), ("cross", cr)):
    c = anch_consts(arr.reshape(shape), x0, n, maxorder)
    C[nm] = {T: float(c[T]) for T in Tlist}
for k in acckeys:
    C[k] = {T: float(acc[k][ti]) for ti, T in enumerate(Tlist)}
for nm in GG:
    C[f"gg_{nm}"] = {T: 0.0 for T in Tlist}
    for Qc in range(GG[nm].shape[2]):                                     # column by column (memory)
        col = np.ascontiguousarray(GG[nm][:, :, Qc])
        c = anch_consts(col.reshape(shape + col.shape[1:]), x0, n, maxorder)
        for T in Tlist:
            C[f"gg_{nm}"][T] += float(c[T].sum())
    u = GG[nm].sum(axis=2)
    c = anch_consts(u.reshape(shape + u.shape[1:]), x0, n, maxorder)
    C[f"grp_{nm}"] = {T: float(c[T].sum()) for T in Tlist}
    C[f"ggx_{nm}"] = {T: 0.0 for T in Tlist}
    for Qc in range(GGx[nm].shape[2]):
        col = np.ascontiguousarray(GGx[nm][:, :, Qc])
        c = anch_consts(col.reshape(shape + col.shape[1:]), x0, n, maxorder)
        for T in Tlist:
            C[f"ggx_{nm}"][T] += float(c[T].sum())
C["pair"] = {T: C["pair_self"][T] + C["pair_cross"][T] for T in Tlist}
log(f"    exact constants done, {time.time() - t0:.0f} s")

# P3's certified bound, per subset and summed in closed form
if not nop3:
    t1 = time.time()
    sup = EnvelopeSup(G)
    GF = GFBound(G, x0, sup, K=maxorder)
    C["P3_self"] = {}; C["P3_cross"] = {}
    for T in Tlist:
        if len(T) > P3MAX:
            continue
        bs, bc = GF.total(len(T), T)
        C["P3_self"][T] = bs; C["P3_cross"][T] = bc
    C["P3"] = {T: C["P3_self"][T] + C["P3_cross"][T] for T in C["P3_self"]}
    Gam = {m: GF.total(m) for m in range(3, maxorder + 1)}
    log(f"    P3 bounds done, {time.time() - t1:.0f} s")

# true remainder of the anchored expansion
rem = {}
for m in range(3, maxorder + 1):
    r = g - anchored_interp(g, x0, m - 1)
    rem[m] = (float(r.min()), float(r.max()))

# ------------------------------------------------------------------ checks and report
keys = ["total", "self", "cross"] + [f"grp_{nm}" for nm in GG] + ["atom"] + [f"gg_{nm}" for nm in GG] + [f"ag_{nm}" for nm in grp] \
       + [f"ggx_{nm}" for nm in GG] + [f"agx_{nm}" for nm in grp] \
       + ["pair_self", "pair_cross", "pair"] + ([] if nop3 else ["P3_self", "P3_cross", "P3"])
nchk = nviol = 0
tol = 1e-9
for T in Tlist:
    t = C["total"][T]
    chains = [("atom", f"ag_{nm}") for nm in grp] + [(f"ag_{nm}", "pair") for nm in grp] \
           + [(f"grp_{nm}", f"gg_{nm}") for nm in GG] + [(f"gg_{nm}", "pair") for nm in GG]
    for k in keys:
        if k in ("self", "cross", "pair_self", "pair_cross", "P3_self", "P3_cross") or k.startswith("ggx_") or k.startswith("agx_"):
            continue
        if k == "P3" and T not in C["P3"]:
            continue
        nchk += 1
        if C[k][T] < t - tol:
            nviol += 1; log(f"    VIOLATION: {k} < total at T={T}: {C[k][T]} < {t}")
    chains += [("cross", f"ggx_{nm}") for nm in GG] + [(f"ggx_{nm}", "pair_cross") for nm in GG] \
            + [("cross", f"agx_{nm}") for nm in grp] + [(f"agx_{nm}", "pair_cross") for nm in grp]
    for lo_, hi_ in chains:
        nchk += 1
        if C[hi_][T] < C[lo_][T] - tol:
            nviol += 1; log(f"    VIOLATION: {hi_} < {lo_} at T={T}")
    if not nop3 and T in C["P3"]:
        for lo_, hi_ in (("self", "P3_self"), ("cross", "P3_cross"), ("pair_self", "P3_self"), ("pair_cross", "P3_cross")):
            nchk += 1
            if C[hi_][T] < C[lo_][T] - tol:
                nviol += 1; log(f"    VIOLATION: {hi_} < {lo_} at T={T}: {C[hi_][T]} < {C[lo_][T]}")
log(f"    inequality checks (triangle-inequality chains; P3 bound >= exact part constants and >= sum of exact term constants): {nchk} checks, {nviol} violations")
for m in range(3, maxorder + 1):
    Tm = [T for T in Tlist if len(T) == m]
    if not Tm:
        continue
    log(f"--- order {m}: {len(Tm)} subsets; sums over subsets of exact anchored constants (kcal/mol), and ratio to the total")
    base = sum(C["total"][T] for T in Tm)
    for k in keys:
        if k.startswith("P3") and m > P3MAX:                          # only the closed-form sum is available
            s = {"P3_self": Gam[m][0], "P3_cross": Gam[m][1], "P3": sum(Gam[m])}[k]
            log(f"    {k:12s} sum {s:11.4e}   /total {s / base:9.2f}   (closed form Gamma_{m}; not computed subset by subset)")
            continue
        s = sum(C[k][T] for T in Tm)
        rat = np.array([C[k][T] / C["total"][T] for T in Tm if C["total"][T] > 0])
        log(f"    {k:12s} sum {s:11.4e}   /total {s / base:9.2f}   per subset min/median/max {rat.min():8.2f} {np.median(rat):8.2f} {rat.max():9.2f}")
    if not nop3:
        log(f"    Gamma_{m} (P3, closed form over all subsets): self {Gam[m][0]:.4e} + cross {Gam[m][1]:.4e} = {sum(Gam[m]):.4e}; "
            f"sum over subsets of chat_T: {sum(C['P3'][T] for T in Tm if T in C['P3']):.4e}" + ("" if m <= P3MAX else " (not computed)"))
    log(f"    true remainder g - I_{m - 1} g over all states: [{rem[m][0]:.4e}, {rem[m][1]:.4e}]")
res["sums"] = {str(m): {k: sum(C[k][T] for T in Tlist if len(T) == m and T in C[k]) for k in keys} for m in range(3, maxorder + 1)}
if not nop3:
    for m in range(3, maxorder + 1):
        if m > P3MAX:
            res["sums"][str(m)].update(P3_self=Gam[m][0], P3_cross=Gam[m][1], P3=sum(Gam[m]))
res["nsubsets"] = {str(m): len([T for T in Tlist if len(T) == m]) for m in range(3, maxorder + 1)}
res["per_subset"] = {k: {"-".join(map(str, T)): C[k][T] for T in Tlist if T in C[k]} for k in keys}
res["remainder"] = {str(m): rem[m] for m in rem}
if not nop3:
    res["Gamma"] = {str(m): list(Gam[m]) for m in Gam}
res["checks"] = dict(n=nchk, violations=nviol)
res["states_enumerated"] = S
with open(os.path.join(HERE, "out", f"s1_{tag}.json"), "w") as fh:
    json.dump(res, fh, indent=1)
log.done()
