"""
P8 step 3 -- validation of the sharper forms of the bound (p8sr.SRBound.total_T, variants P3 / S / AH / SA) on an
enumerated instance, against EXACT constants.

For every subset T of order 3..maxorder (those of out/m1_<tag>.npz) and every atom / atom pair:
  C0  variant 'P3' of my vectorised evaluation reproduces P3's own summands (GFDecomp = gfbound.GFBound) -- consistency;
  C1  'S'  summand >= exact anchored constant c_T(t_pq)            (all contexts; PP of p8_01_measure.py)     [Proposition S]
  C2  'SA' and 'AH' summands >= exact RESTRICTED constant          (hosts outside T at the anchor; PPA of p8_01b) [Theorem AH]
  C3  SA <= S <= P3 and SA <= AH <= P3, summand by summand;
  C4  per atom pair and order m:  sum_T summand >= sup_x |t_pq - I_{m-1} t_pq|(x)   (REM; all four variants);
  C5  at EVERY state x:  |g_s(x) - I_{m-1} g_s(x)| <= sum_{T subset S(x), |T| = m} chat_T   for the true charges, for all
      charges positive and for the sign patterns of p8_02_signblind.py (the bounds are sign-blind: they must hold for all);
  C6  the closed form AHBound.total_ah(m) equals the sum over the subsets of the 'AH' constants.
Reports per order the sums over the subsets, and the breakdown by host pattern and atom class.

usage: python3 -B p8_03_sr_validate.py SEQ BB TAU
needs out/m1_<tag>.npz, out/m1b_<tag>.npz; uses out/sb_<tag>.npz if present.  Writes logs/sr_<tag>.log, out/sr_<tag>.json, .npz
"""
import sys, os, json, time
import numpy as np
from p8lib import *
from p8sr import AHBound, VARIANTS

a = sys.argv[1:]
seq, bb, tau = a[0], a[1], float(a[2])
tag = tagname(seq, bb, tau)
log = Log(os.path.join(HERE, "logs", f"sr_{tag}.log"))
t0 = time.time()
Z = np.load(os.path.join(HERE, "out", f"m1_{tag}.npz"))
Zb = np.load(os.path.join(HERE, "out", f"m1b_{tag}.npz"))
G = GBModel(seq, bb, tau=tau)
n, N = G.ns, G.nat
shape = tuple(G.k)
x0 = tuple(int(v) for v in Z["anchor"])
assert tuple(Z["shape"]) == shape
Tlist = [tuple(int(v) for v in row if v >= 0) for row in Z["Tlist"]]
orders = np.array([len(T) for T in Tlist]); maxorder = int(orders.max()); nT = len(Tlist)
PP = Z["PP"]; PPA = Zb["PPA"]; REM = Z["REM"]; PBs = Z["PBs"]; PBp = Z["PBp"]; cls = Z["cls"]; site_of = Z["site_of"]
log(f"=== p8_03_sr_validate: {seq} on {bb}, tau {tau}: atoms {N}, sites {n}, domain {list(G.k)}, anchor {x0}; {nT} subsets of order 3..{maxorder}")
sup = EnvelopeSup(G)
SR = AHBound(G, x0, sup, K=maxorder)
iu = np.triu_indices(N, 1); dvec = np.arange(N)
Vs = {v: np.zeros((nT, N)) for v in VARIANTS}; Vp = {v: np.zeros((nT, N, N)) for v in VARIANTS}; VT = {v: np.zeros(nT) for v in VARIANTS}
for ti, T in enumerate(Tlist):
    out = SR.total_T(len(T), T, decomp=True)
    for v in VARIANTS:
        se, cr, sv, pm = out[v]
        Vs[v][ti] = sv; Vp[v][ti] = pm; VT[v][ti] = se + cr
log(f"    bounds of {nT} subsets in the variants {VARIANTS} done, {time.time() - t0:.0f} s")
ex_s = PP[:, dvec, dvec]; ex_p = PP[:, iu[0], iu[1]]; exa_s = PPA[:, dvec, dvec]; exa_p = PPA[:, iu[0], iu[1]]
vp = {v: Vp[v][:, iu[0], iu[1]] for v in VARIANTS}
p3_p = PBp[:, iu[0], iu[1]]
nsum = int(ex_s.size + ex_p.size)
checks = {}
# C0
dev = max(float(np.abs(Vs["P3"] - PBs).max() / max(PBs.max(), 1e-300)), float(np.abs(vp["P3"] - p3_p).max() / max(p3_p.max(), 1e-300)))
rel = np.abs(vp["P3"] - p3_p) / np.maximum(p3_p, 1e-300)
devrel = float(rel[p3_p > 1e-14].max()) if (p3_p > 1e-14).any() else 0.0
log(f"    C0 variant 'P3' against P3's own summands: {nsum} summands, largest deviation relative to the largest summand {dev:.1e}, largest relative deviation of a summand {devrel:.1e}")
checks["C0"] = dict(n=nsum, dev=dev, devrel=devrel)
assert dev < 1e-10 and devrel < 1e-8
tol = 1e-12


def cmp(bs, bp, es, ep, name, label):
    v = int((bs < es - tol).sum() + (bp < ep - tol).sum())
    ms = es > 1e-10; mp = ep > 1e-10
    rs = bs[ms] / es[ms]; rp = bp[mp] / ep[mp]
    log(f"    {name} {label}: {nsum} comparisons, {v} violations; smallest ratio bound/exact (exact > 1e-10): self {rs.min():.4f}, pair {rp.min():.4f}; medians {np.median(rs):.2f}, {np.median(rp):.2f}")
    return dict(n=nsum, violations=v, min_ratio_self=float(rs.min()), min_ratio_pair=float(rp.min()), median_self=float(np.median(rs)), median_pair=float(np.median(rp)))


checks["C1_S"] = cmp(Vs["S"], vp["S"], ex_s, ex_p, "C1", "'S' summand >= exact anchored constant (all contexts), every (T, atom), (T, atom pair)")
checks["C2_SA"] = cmp(Vs["SA"], vp["SA"], exa_s, exa_p, "C2", "'SA' summand >= exact restricted constant (hosts outside T at the anchor)")
checks["C2_AH"] = cmp(Vs["AH"], vp["AH"], exa_s, exa_p, "C2", "'AH' summand >= exact restricted constant")
# is the restriction needed?  how often would 'SA' fail against the all-context constants
vfail = int((Vs["SA"] < ex_s - tol).sum() + (vp["SA"] < ex_p - tol).sum())
log(f"    (for information: 'SA' summand < exact ALL-context constant in {vfail} of {nsum} cases -- 'SA' is a bound of the restricted constants only)")
checks["SA_below_allcontext"] = vfail
# C3
n3 = v3 = 0
for lo_, hi_ in (("SA", "S"), ("S", "P3"), ("SA", "AH"), ("AH", "P3")):
    n3 += nsum
    v3 += int((Vs[lo_] > Vs[hi_] * (1 + 1e-9) + 1e-300).sum() + (vp[lo_] > vp[hi_] * (1 + 1e-9) + 1e-300).sum())
log(f"    C3 chains SA <= S <= P3 and SA <= AH <= P3, summand by summand: {n3} comparisons, {v3} violations")
checks["C3"] = dict(n=n3, violations=v3)
# C4
n4 = 0; v4 = {v: 0 for v in VARIANTS}; r4 = {v: np.inf for v in VARIANTS}
for m in range(3, maxorder + 1):
    sel = np.flatnonzero(orders == m)
    if not len(sel):
        continue
    rem_s = REM[m][dvec, dvec]; rem_p = REM[m][iu[0], iu[1]]
    n4 += len(rem_s) + len(rem_p)
    for v in VARIANTS:
        bs = Vs[v][sel].sum(axis=0); bp = vp[v][sel].sum(axis=0)
        v4[v] += int((bs < rem_s - tol).sum() + (bp < rem_p - tol).sum())
        mk = rem_p > 1e-10
        if mk.any():
            r4[v] = min(r4[v], float((bp[mk] / rem_p[mk]).min()))
        mk = rem_s > 1e-10
        if mk.any():
            r4[v] = min(r4[v], float((bs[mk] / rem_s[mk]).min()))
log(f"    C4 per atom pair and order: sum_T summand >= sup_x |t_pq - I_(m-1) t_pq|: {n4} comparisons per variant; violations " +
    ", ".join(f"{v}: {v4[v]}" for v in VARIANTS) + "; smallest ratio " + ", ".join(f"{v}: {r4[v]:.3f}" for v in VARIANTS))
checks["C4"] = dict(n=n4, violations=v4, min_ratio=r4)
# C5 state level
st = G.product_states(); S = len(st)
chg = (st != np.array(x0)[None, :])
systems = [("true charges", Z["g"]), ("all charges positive", Z["gabs"])]
sbf = os.path.join(HERE, "out", f"sb_{tag}.npz")
if os.path.exists(sbf):
    sb = np.load(sbf)
    for k, m_ in enumerate(sb["orders"]):
        systems.append((f"sign pattern found for order {int(m_)}", sb["gp"][:, k]))
n5 = 0; v5 = {v: 0 for v in VARIANTS}; r5 = {v: np.inf for v in VARIANTS}
for m in range(3, maxorder + 1):
    sel = np.flatnonzero(orders == m)
    if not len(sel):
        continue
    inS = np.stack([chg[:, list(Tlist[ti])].all(axis=1) for ti in sel], axis=1).astype(float)      # (S, nsub)
    env = {v: inS @ VT[v][sel] for v in VARIANTS}
    for name, arr in systems:
        gg = arr.reshape(shape)
        r = np.abs(gg - anchored_interp(gg, x0, m - 1)).reshape(-1)
        n5 += S
        for v in VARIANTS:
            v5[v] += int((r > env[v] + 1e-9).sum())
            mk = r > 1e-9
            if mk.any():
                r5[v] = min(r5[v], float((env[v][mk] / r[mk]).min()))
log(f"    C5 at every state, |g_s - I_(m-1) g_s|(x) <= envelope sum_(T in S(x)) chat_T, for {len(systems)} charge systems ({', '.join(nm for nm, _ in systems)}): "
    f"{n5} state checks per variant; violations " + ", ".join(f"{v}: {v5[v]}" for v in VARIANTS) + "; smallest ratio envelope/|remainder| " + ", ".join(f"{v}: {r5[v]:.2f}" for v in VARIANTS))
checks["C5"] = dict(n=n5, violations=v5, min_ratio=r5, systems=[nm for nm, _ in systems])
# C6
dev6 = 0.0
for m in range(3, maxorder + 1):
    sel = np.flatnonzero(orders == m)
    if len(sel):
        cf = sum(SR.total_ah(m)); ex = float(VT["AH"][sel].sum())
        dev6 = max(dev6, abs(cf - ex) / ex)
log(f"    C6 closed form total_ah(m) against the sum over subsets of the 'AH' constants: largest relative deviation {dev6:.1e}")
checks["C6"] = dev6
assert dev6 < 1e-10

res = dict(seq=seq, bb=bb, tau=tau, natoms=N, n=n, nstates=S, orders={}, checks=checks)
hostT = np.zeros((nT, N), dtype=bool)
for ti, T in enumerate(Tlist):
    hostT[ti] = np.isin(site_of, T)
mov2 = (site_of[iu[0]] >= 0).astype(int) + (site_of[iu[1]] >= 0).astype(int)
nc = len(CLASSES)
for m in range(3, maxorder + 1):
    sel = np.flatnonzero(orders == m)
    if not len(sel):
        continue
    tr = float(Z["C_total"][sel].sum()); pp = float(Z["C_PP"][sel].sum()); ppa = float(exa_s[sel].sum() + exa_p[sel].sum())
    tv = {v: float(VT[v][sel].sum()) for v in VARIANTS}
    row = dict(nsub=int(len(sel)), truth=tr, PP=pp, PPA=ppa, **tv)
    log(f"--- order {m}: {len(sel)} subsets; sums (kcal/mol): truth {tr:.4e} | best pair-by-pair {pp:.4e} (restricted contexts {ppa:.4e}) | P3 {tv['P3']:.4e} | S {tv['S']:.4e} | AH {tv['AH']:.4e} | SA {tv['SA']:.4e}")
    log(f"    P3/S = {tv['P3'] / tv['S']:.2f};  P3/AH = {tv['P3'] / tv['AH']:.2f};  P3/SA = {tv['P3'] / tv['SA']:.2f};   to the truth: P3 {tv['P3'] / tr:.0f}, S {tv['S'] / tr:.1f}, SA {tv['SA'] / tr:.1f};  "
        f"to the best pair-by-pair: P3 {tv['P3'] / pp:.2f}, S {tv['S'] / pp:.2f}, SA/restricted {tv['SA'] / ppa:.2f}")
    hp = hostT[sel][:, iu[0]].astype(int) + hostT[sel][:, iu[1]].astype(int)
    tab = []
    log("    cross part by host pattern:   best pair-by-pair (all contexts; restricted) | P3 | S | AH | SA | P3/PP | S/PP | SA/PPA")
    for nm_ in range(3):
        for nh_ in range(nm_ + 1):
            mk = (mov2[None, :] == nm_) & (hp == nh_)
            e_, ea_ = float(ex_p[sel][mk].sum()), float(exa_p[sel][mk].sum())
            vv = {v: float(vp[v][sel][mk].sum()) for v in VARIANTS}
            tab.append(dict(moving=nm_, hosts_in_T=nh_, PP=e_, PPA=ea_, **vv))
            if vv["P3"] > 0:
                log(f"      {nm_} moving, {nh_} host(s) in T: {e_:10.4e}; {ea_:10.4e} | {vv['P3']:10.4e} | {vv['S']:10.4e} | {vv['AH']:10.4e} | {vv['SA']:10.4e} | "
                    f"{vv['P3'] / e_ if e_ > 0 else float('nan'):7.2f} | {vv['S'] / e_ if e_ > 0 else float('nan'):6.2f} | {vv['SA'] / ea_ if ea_ > 0 else float('nan'):6.2f}")
    row["by_host"] = tab
    tabc = []
    log("    by atom class:   best pair-by-pair (all contexts; restricted) | P3 | S | SA | P3/PP | S/PP | SA/PPA")
    for a1 in range(nc):
        for b1 in range(a1, nc):
            mk = ((cls[iu[0]] == a1) & (cls[iu[1]] == b1)) | ((cls[iu[0]] == b1) & (cls[iu[1]] == a1))
            e_, ea_ = float(ex_p[sel][:, mk].sum()), float(exa_p[sel][:, mk].sum())
            vv = {v: float(vp[v][sel][:, mk].sum()) for v in VARIANTS}
            tabc.append(dict(name=f"{CLASSES[a1]}-{CLASSES[b1]}", PP=e_, PPA=ea_, **vv))
            if vv["P3"] > 0:
                log(f"      {CLASSES[a1] + '-' + CLASSES[b1]:12s} {e_:10.4e}; {ea_:10.4e} | {vv['P3']:10.4e} | {vv['S']:10.4e} | {vv['SA']:10.4e} | {vv['P3'] / e_:7.2f} | {vv['S'] / e_:6.2f} | {vv['SA'] / ea_:6.2f}")
    for a1 in range(nc):
        mk = cls == a1
        e_, ea_ = float(ex_s[sel][:, mk].sum()), float(exa_s[sel][:, mk].sum())
        vv = {v: float(Vs[v][sel][:, mk].sum()) for v in VARIANTS}
        tabc.append(dict(name=f"self:{CLASSES[a1]}", PP=e_, PPA=ea_, **vv))
        if vv["P3"] > 0:
            log(f"      {'self:' + CLASSES[a1]:12s} {e_:10.4e}; {ea_:10.4e} | {vv['P3']:10.4e} | {vv['S']:10.4e} | {vv['SA']:10.4e} | {vv['P3'] / e_:7.2f} | {vv['S'] / e_:6.2f} | {vv['SA'] / ea_:6.2f}")
    row["by_class"] = tabc
    res["orders"][str(m)] = row
res["per_subset"] = {v: {"-".join(map(str, T)): float(VT[v][ti]) for ti, T in enumerate(Tlist)} for v in VARIANTS}
np.savez_compressed(os.path.join(HERE, "out", f"sr_{tag}.npz"), **{f"T_{v}": VT[v] for v in VARIANTS}, **{f"s_{v}": Vs[v] for v in ("S", "SA")}, **{f"p_{v}": Vp[v] for v in ("S", "SA")})
with open(os.path.join(HERE, "out", f"sr_{tag}.json"), "w") as fh:
    json.dump(res, fh, indent=1)
log.done()
