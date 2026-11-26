"""
P8 step 1 -- the measurement for charged side chains (P5's step 1, extended).

For an enumerated instance (anchor x0 = argmin E by enumeration, as in P5) and every subset T of
sites of order 3..maxorder, by EXACT ENUMERATION of all states (kcal/mol):

  truth      c_T(g)                                 anchored constant of the GBn2 energy
  self/cross c_T(sum_p t_pp), c_T(sum_{p<q} t_pq)   P3's split
  PP         c_T(t_pq) for EVERY atom pair p <= q   -> stored per (T, p, q); their sum over pairs is the least value any
                                                      term-by-term bound can have ("best pair-by-pair bound", P5's PP_T)
  class x class   c_T(F_ab), F_ab = sum of the pair terms between atom classes a, b (bb, nsc, chain, head), and the
                  SIGNED value of Delta_T F_ab at the (context, states) where |Delta_T g| is largest (these add up to c_T(g))
  fine groups     sum over pairs of groups (per residue: fixed part, neutral side chain, chain, head) of c_T(F_PQ)
  all-plus   c_T(g_|q|)                             the same atoms with all charges positive (a sign-blind bound must cover it)
  P3         P3's certified bound per (T, atom) and per (T, atom pair) (my GFDecomp = P3's GFBound with the summands
             exposed), its closed-form sum Gamma_m, and the check  P3 summand >= exact constant  for every (T, p <= q).

usage: python3 -B p8_01_measure.py SEQ BB TAU [maxorder=6] [--budget SECONDS]
  --budget: stop at a row boundary after that many seconds (a checkpoint is on disk; run the same command again to
            continue).  A checkpoint is written every 60 s in any case.
writes logs/m1_<tag>.log (complete when its last line is 'DONE in ... s'), out/m1_<tag>.npz, out/m1_<tag>.json
"""
import sys, os, json, time, itertools
import numpy as np
from p8lib import *

a = sys.argv[1:]
seq, bb, tau = a[0], a[1], float(a[2])
maxorder = int(a[3]) if len(a) > 3 and not a[3].startswith("--") else 6
BUDGET = float(a[a.index("--budget") + 1]) if "--budget" in a else 1e18
tag = tagname(seq, bb, tau)
if os.path.exists(os.path.join(HERE, "out", f"m1_{tag}.npz")) and "--force" not in a:
    print(f"out/m1_{tag}.npz exists: this run is complete (use --force to redo it); nothing done"); sys.exit(0)
ckpt = os.path.join(MYCACHE, f"m1_{tag}_ckpt.npz")
resume = os.path.exists(ckpt)
log = Log(os.path.join(HERE, "logs", f"m1_{tag}.log"), append=resume)
t0 = time.time()
G, st, shape, f, g, E, x0 = build(seq, bb, tau)
n, N, S = G.ns, G.nat, len(st)
maxorder = min(maxorder, n)
Tlist = subsets(n, shape, 3, maxorder)
nT = len(Tlist)
cls, letter = atom_classes(G)
fg, fgnames = fine_groups(G)
nc = len(CLASSES); nf = fg.max() + 1
cidx, cpairs = pair_index(nc)
fidx, fpairs = pair_index(nf)
log(f"=== p8_01_measure: {seq} ({G.seq}) on {bb}, tau {tau}: atoms {N}, sites {n}, domain {list(shape)} = {S} states; anchor x0 = argmin E = {x0}; "
    f"{nT} subsets of order 3..{maxorder}" + ("; RESUMING from checkpoint" if resume else ""))
for c in range(nc):
    m = cls == c
    log(f"    class {CLASSES[c]:5s}: {int(m.sum()):3d} atoms, net charge {G.q[m].sum():+.4f} e, sum |q| {np.abs(G.q[m]).sum():.4f} e")
log("    fine groups (net charge): " + ", ".join(f"{nm} {G.q[fg == k].sum():+.3f}" for k, nm in enumerate(fgnames)))
B = 1.0 / G.invB(G.descreening(st))
ia = int(np.ravel_multi_index(x0, shape))
Xa = G.coords(st[ia:ia + 1])[0]
Ba = B[ia]

if resume:
    z = np.load(ckpt)
    p_next = int(z["p_next"]); PP = z["PP"]; REM = z["REM"]; FC = z["FC"]; FS = z["FS"]; FGp = z["FGp"]; gabs = z["gabs"]; gsum = z["gsum"]
    Dmin = z["Dmin"]; Dmax = z["Dmax"]; rmin = z["rmin"]; rmax = z["rmax"]
    assert list(z["anchor"]) == list(x0) and PP.shape == (nT, N, N)
    log(f"    checkpoint read: rows 0..{p_next - 1} done")
else:
    p_next = 0
    PP = np.zeros((nT, N, N))                         # exact c_T(t_pq), stored for p <= q
    REM = np.zeros((maxorder + 1, N, N))              # REM[m, p, q] = sup_x |t_pq - I_{m-1} t_pq|(x), m = 3..maxorder, p <= q
    FC = np.zeros((S, len(cpairs)))                   # class-pair functions (pairs p < q only), kcal/mol
    FS = np.zeros((S, nc))                            # self terms by class
    FGp = np.zeros((S, len(fpairs)))                  # fine-group pair functions (self terms inside the diagonal groups)
    gabs = np.zeros(S); gsum = np.zeros(S)
    Dmin = np.full((N, N), np.inf); Dmax = np.zeros((N, N)); rmin = np.full((N, N), np.inf); rmax = np.zeros((N, N))


def save_ckpt(p_next):
    tmp = ckpt + ".tmp.npz"
    np.savez(tmp, p_next=p_next, PP=PP, REM=REM, FC=FC, FS=FS, FGp=FGp, gabs=gabs, gsum=gsum, Dmin=Dmin, Dmax=Dmax, rmin=rmin, rmax=rmax, anchor=np.array(x0))
    os.replace(tmp, ckpt)


tlast = time.time()
stopped = False
for p in range(p_next, N):
    cols = np.arange(p, N)
    # kernel row with distances (chunked over states)
    M = np.empty((S, len(cols)))
    for s0 in range(0, S, 20000):
        sub = st[s0:s0 + 20000]
        X = G.coords(sub)
        d = X[:, p, None, :] - X[:, cols, :]
        r2 = (d * d).sum(-1)
        BB = B[s0:s0 + 20000, p, None] * B[s0:s0 + 20000][:, cols]
        Dv = r2 / (4.0 * BB)
        M[s0:s0 + 20000] = 1.0 / np.sqrt(r2 + BB * np.exp(-Dv))
        Dmin[p, cols] = np.minimum(Dmin[p, cols], Dv.min(axis=0)); Dmax[p, cols] = np.maximum(Dmax[p, cols], Dv.max(axis=0))
        rr = np.sqrt(r2)
        rmin[p, cols] = np.minimum(rmin[p, cols], rr.min(axis=0)); rmax[p, cols] = np.maximum(rmax[p, cols], rr.max(axis=0))
        del X, d, r2, BB, Dv, rr
    coef = pair_coef(G, p, cols)
    gabs -= M @ np.abs(coef)                           # g_|q|: PRE < 0, so every pair term of the all-plus system is -|coef| M
    M *= coef[None, :]                                 # now t_pq, q >= p
    gsum += M.sum(axis=1)
    FS[:, cls[p]] += M[:, 0]
    for c in range(nc):
        sel = np.flatnonzero(cls[cols[1:]] == c) + 1
        if len(sel):
            FC[:, cidx[cls[p], c]] += M[:, sel].sum(axis=1)
    for k in range(nf):
        sel = np.flatnonzero(fg[cols] == k)
        if len(sel):
            FGp[:, fidx[fg[p], k]] += M[:, sel].sum(axis=1)
    c_ = anch_consts(M.reshape(shape + (len(cols),)), x0, n, maxorder)
    for ti, T in enumerate(Tlist):
        PP[ti, p, p:] = c_[T]
    del c_
    rr_ = anchored_remainders(M.reshape(shape + (len(cols),)), x0, n, list(range(3, maxorder + 1)))
    for m_, v_ in rr_.items():
        REM[m_, p, p:] = v_
    del rr_, M
    now = time.time()
    if now - tlast > 60 or p == N - 1 or now - t0 > BUDGET:
        save_ckpt(p + 1); tlast = now
        log(f"    row {p + 1}/{N} done, checkpoint written, {now - t0:.0f} s, RSS {rss_mb():.0f} MB")
    if now - t0 > BUDGET and p < N - 1:
        stopped = True
        break
if stopped:
    log(f"BUDGET REACHED at row {p + 1}/{N}: checkpoint on disk, run the same command again to continue (this log part is not a complete run)")
    log.f.close()
    sys.exit(0)

err = float(np.abs(gsum - g.reshape(-1)).max())
log(f"    check: sum of the pair terms equals P3's evaluator G.energy at all {S} states to {err:.2e} kcal/mol")
assert err < 1e-8
iu = np.triu_indices(N, 1)
dvec = np.arange(N)

# ------------------------------------------------------------------ exact constants of the aggregated functions
C = {}
gflat = g.reshape(-1)
selfp = FS.sum(axis=1); crossp = gflat - selfp
for nm, arr in (("total", gflat), ("self", selfp), ("cross", crossp), ("allplus", gabs)):
    c_ = anch_consts(arr.reshape(shape), x0, n, maxorder)
    C[nm] = np.array([float(c_[T]) for T in Tlist])
# class pairs: constants and signed contributions at the argmax of |Delta_T g|
Fall = np.concatenate([FC, FS], axis=1)               # (S, 10 + 4): F_ab (pairs p<q), then self by class
ncomp = Fall.shape[1]
cls_const = np.zeros((nT, ncomp)); cls_signed = np.zeros((nT, ncomp))
tindex = {T: ti for ti, T in enumerate(Tlist)}


def cb(T, D):
    ti = tindex[T]
    A = D.reshape(-1, ncomp)
    if A.shape[0] == 0:
        return
    cls_const[ti] = np.maximum(A.max(axis=0), -A.min(axis=0))
    tot = A.sum(axis=1)
    k = int(np.argmax(np.abs(tot)))
    cls_signed[ti] = A[k] * np.sign(tot[k])
    assert abs(abs(tot[k]) - C["total"][ti]) < 1e-9


anch_walk(Fall.reshape(shape + (ncomp,)), x0, n, maxorder, cb)
# fine groups, column blocks (memory)
C["fine"] = np.zeros(nT)
for c0_ in range(0, FGp.shape[1], 24):
    blk = np.ascontiguousarray(FGp[:, c0_:c0_ + 24])
    c_ = anch_consts(blk.reshape(shape + (blk.shape[1],)), x0, n, maxorder)
    for ti, T in enumerate(Tlist):
        C["fine"][ti] += float(c_[T].sum())
C["PP_self"] = PP[:, dvec, dvec].sum(axis=1)
C["PP_cross"] = PP[:, iu[0], iu[1]].sum(axis=1)
C["PP"] = C["PP_self"] + C["PP_cross"]
log(f"    exact constants done, {time.time() - t0:.0f} s")

# ------------------------------------------------------------------ P3's bound, pair by pair
t1 = time.time()
sup = EnvelopeSup(G)
GF = GFDecomp(G, x0, sup, K=maxorder)
dev, devsum, ncmp = check_against_base(G, x0, sup, maxorder, range(3, maxorder + 1), Tlist[:6])
log(f"    GFDecomp against P3's GFBound ({ncmp} totals): largest relative deviation {dev:.1e}; summands add up to the totals to {devsum:.1e}")
assert dev < 1e-12 and devsum < 1e-10
PBs = np.zeros((nT, N)); PBp = np.zeros((nT, N, N))
C["P3_self"] = np.zeros(nT); C["P3_cross"] = np.zeros(nT)
for ti, T in enumerate(Tlist):
    se, cr, sv, pm = GF.decomp(len(T), list(T))
    PBs[ti] = sv; PBp[ti] = pm
    C["P3_self"][ti] = se; C["P3_cross"][ti] = cr
C["P3"] = C["P3_self"] + C["P3_cross"]
Gam = {m: GF.total(m) for m in range(3, maxorder + 1)}
log(f"    P3 bounds done, {time.time() - t1:.0f} s")

# checks: P3 summand >= exact constant, for every (T, atom) and (T, atom pair)
tol = 1e-12
ex_s = PP[:, dvec, dvec]; ex_p = PP[:, iu[0], iu[1]]; bd_p = PBp[:, iu[0], iu[1]]
viol = int((PBs < ex_s - tol).sum() + (bd_p < ex_p - tol).sum())
ncheck = int(ex_s.size + ex_p.size)
msk_s = ex_s > 1e-10; msk_p = ex_p > 1e-10
ratio_s = PBs[msk_s] / ex_s[msk_s]; ratio_p = bd_p[msk_p] / ex_p[msk_p]
log(f"    CHECK P3 summand >= exact constant for every (T, atom) and (T, atom pair): {ncheck} comparisons, {viol} violations; "
    f"smallest ratio bound/exact (exact > 1e-10): self {ratio_s.min():.4f}, pair {ratio_p.min():.4f}; medians {np.median(ratio_s):.2f}, {np.median(ratio_p):.2f}")
nagg = 0; vagg = 0
for ti in range(nT):
    for lo_, hi_ in ((C["total"][ti], C["fine"][ti]), (C["fine"][ti], C["PP"][ti]), (C["PP"][ti], C["P3"][ti]), (C["self"][ti], C["P3_self"][ti]),
                     (C["cross"][ti], C["P3_cross"][ti]), (C["allplus"][ti], C["P3"][ti]), (C["allplus"][ti], C["PP"][ti]), (C["total"][ti], cls_const[ti].sum())):
        nagg += 1
        if hi_ < lo_ - 1e-9:
            vagg += 1; log(f"    VIOLATION of a chain at T = {Tlist[ti]}: {lo_} > {hi_}")
log(f"    chains truth <= fine groups <= PP <= P3; self <= P3_self; cross <= P3_cross; all-plus <= PP <= P3; truth <= sum of class-pair constants: {nagg} checks, {vagg} violations")

# per-pair remainders: sup_x |t_pq - I_{m-1} t_pq| <= sum over T of order m of c_T(t_pq)   (Proposition 1 applied to the pair term)
nrem = vrem = 0
for m in range(3, maxorder + 1):
    selm = np.flatnonzero(np.array([len(T) for T in Tlist]) == m)
    bound = PP[selm].sum(axis=0)
    nrem += N * (N + 1) // 2
    vrem += int((np.triu(REM[m]) > np.triu(bound) + 1e-10).sum())
log(f"    per-pair remainders against the sums of their own anchored constants (Proposition 1 for each pair term): {nrem} checks, {vrem} violations")
# true remainder
rem = {}
for m in range(3, maxorder + 1):
    r = g - anchored_interp(g, x0, m - 1)
    rem[m] = (float(r.min()), float(r.max()))

# ------------------------------------------------------------------ report
orders = np.array([len(T) for T in Tlist])
res = dict(seq=seq, bb=bb, tau=tau, natoms=N, n=n, shape=list(shape), anchor=list(x0), nstates=S, maxorder=maxorder,
           classes=CLASSES, class_pairs=[[CLASSES[a_], CLASSES[b_]] for a_, b_ in cpairs], orders={})
hostT = np.zeros((nT, N), dtype=bool)                 # is the host of atom p in T?
site_of = -np.ones(N, dtype=int)
for i in range(n):
    site_of[G.mov[i]] = i
for ti, T in enumerate(Tlist):
    hostT[ti] = np.isin(site_of, T)
for m in range(3, maxorder + 1):
    sel = np.flatnonzero(orders == m)
    if not len(sel):
        continue
    tr = C["total"][sel].sum()
    log(f"--- order {m}: {len(sel)} subsets; sums over the subsets (kcal/mol) and ratio to the truth")
    row = dict(nsub=int(len(sel)))
    for k in ("total", "self", "cross", "fine", "allplus", "PP_self", "PP_cross", "PP", "P3_self", "P3_cross", "P3"):
        v = float(C[k][sel].sum()); row[k] = v
        log(f"    {k:9s} {v:11.4e}   /truth {v / tr:9.2f}")
    row["Gamma"] = [float(Gam[m][0]), float(Gam[m][1])]
    log(f"    Gamma_{m} (closed form over all subsets): self {Gam[m][0]:.4e} + cross {Gam[m][1]:.4e} = {sum(Gam[m]):.4e}  (sum of the per-subset bounds: {row['P3']:.4e})")
    log(f"    true remainder g - I_{m - 1} g over all states: [{rem[m][0]:.4e}, {rem[m][1]:.4e}];  Gamma_{m} / sup|remainder| = {sum(Gam[m]) / max(abs(rem[m][0]), abs(rem[m][1])):.0f}")
    row["remainder"] = list(rem[m])
    # by class pair
    log(f"    by atom class (sums over the {len(sel)} subsets):   signed share of the truth | exact constant of the class-pair function | best pair-by-pair | P3 | P3 / pair-by-pair")
    tab = []
    for k in range(ncomp):
        if k < len(cpairs):
            a_, b_ = cpairs[k]; name = f"{CLASSES[a_]}-{CLASSES[b_]}"
            mk = ((cls[iu[0]] == a_) & (cls[iu[1]] == b_)) | ((cls[iu[0]] == b_) & (cls[iu[1]] == a_))
            ppv = float(ex_p[sel][:, mk].sum()); p3v = float(bd_p[sel][:, mk].sum())
        else:
            a_ = k - len(cpairs); name = f"self:{CLASSES[a_]}"
            mk = cls == a_
            ppv = float(ex_s[sel][:, mk].sum()); p3v = float(PBs[sel][:, mk].sum())
        sg_, cc_ = float(cls_signed[sel, k].sum()), float(cls_const[sel, k].sum())
        tab.append(dict(name=name, signed=sg_, const=cc_, PP=ppv, P3=p3v))
        if ppv > 0 or p3v > 0:
            log(f"      {name:12s} {sg_:+11.4e} ({100 * sg_ / tr:+7.1f} %) | {cc_:10.4e} | {ppv:10.4e} | {p3v:10.4e} | {p3v / ppv if ppv > 0 else float('nan'):7.2f}")
    row["by_class"] = tab
    # by host pattern (number of hosts of the pair that lie in T), pairs p < q
    hp = hostT[sel][:, iu[0]].astype(int) + hostT[sel][:, iu[1]].astype(int)
    mov2 = (site_of[iu[0]] >= 0).astype(int) + (site_of[iu[1]] >= 0).astype(int)
    tabh = []
    log("    cross part by host pattern (moving atoms of the pair; of which with their site in T):   best pair-by-pair | P3 | ratio")
    for nm_ in range(3):
        for nh_ in range(nm_ + 1):
            mk = (mov2[None, :] == nm_) & (hp == nh_)
            ppv = float(ex_p[sel][mk].sum()); p3v = float(bd_p[sel][mk].sum())
            tabh.append(dict(moving=nm_, hosts_in_T=nh_, PP=ppv, P3=p3v))
            if p3v > 0:
                log(f"      {nm_} moving, {nh_} host(s) in T: {ppv:10.4e} | {p3v:10.4e} | {p3v / ppv if ppv > 0 else float('nan'):7.2f}")
    row["by_host"] = tabh
    # by the smallest D = r^2/(4 B_p B_q) over ALL states (pairs p < q)
    Danch = Dmin[iu[0], iu[1]]
    edges = [0.0, 0.1, 0.3, 1.0, 2.0, 4.0, 8.0, 16.0, np.inf]
    tabd = []
    log("    cross part by Dmin = min over all states of r^2/(4 B_p B_q):   pairs | best pair-by-pair | P3 | ratio")
    for lo_, hi_ in zip(edges[:-1], edges[1:]):
        mk = (Danch >= lo_) & (Danch < hi_)
        ppv = float(ex_p[sel][:, mk].sum()); p3v = float(bd_p[sel][:, mk].sum())
        tabd.append(dict(lo=lo_, hi=hi_ if np.isfinite(hi_) else None, npairs=int(mk.sum()), PP=ppv, P3=p3v))
        log(f"      Dmin in [{lo_:4.1f}, {hi_:4.1f}): {int(mk.sum()):5d} | {ppv:10.4e} | {p3v:10.4e} | {p3v / ppv if ppv > 0 else float('nan'):7.2f}")
    row["by_D"] = tabd
    res["orders"][str(m)] = row
res["checks"] = dict(p3_vs_exact=dict(n=ncheck, violations=viol, min_ratio_self=float(ratio_s.min()), min_ratio_pair=float(ratio_p.min())),
                     chains=dict(n=nagg, violations=vagg), gfdecomp_dev=dev, energy_dev=err)
res["per_subset"] = {k: {"-".join(map(str, T)): float(C[k][ti]) for ti, T in enumerate(Tlist)} for k in C}
np.savez_compressed(os.path.join(HERE, "out", f"m1_{tag}.npz"), Tlist=np.array([list(T) + [-1] * (maxorder - len(T)) for T in Tlist]), PP=PP, PBs=PBs, PBp=PBp,
                    REM=REM, cls=cls, fine=fg, site_of=site_of, q=G.q, anchor=np.array(x0), shape=np.array(shape), g=gflat, gabs=gabs, FC=FC, FS=FS,
                    cls_const=cls_const, cls_signed=cls_signed, Dmin=Dmin, Dmax=Dmax, rmin=rmin, rmax=rmax, Xa=Xa, Ba=Ba,
                    **{f"C_{k}": v for k, v in C.items()})
with open(os.path.join(HERE, "out", f"m1_{tag}.json"), "w") as fh:
    json.dump(res, fh, indent=1)
log.done()
