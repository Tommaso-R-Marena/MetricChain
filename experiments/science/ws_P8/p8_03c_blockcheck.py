"""
P8 step 3 -- validation of the BLOCK-WISE state-resolved bounds 'Sb' and 'SAb' (p8sr.BlockBound) on an enumerated
instance, against exact block constants.

A block is a set of terms that share their hosts (and therefore their host states in every context):
    ('self', l)   self terms of side chain l (l = -1: fixed atoms);   ('cross1', l)   pairs fixed-l and inside l
    (l = -1: pairs of fixed atoms);   ('cross2', l, l2)   pairs between the side chains l < l2.
For a block Bk and a subset T the exact quantity that the block bound has to dominate is

    PPB_all[T, Bk] = sup over contexts z and states y_T of  sum_{tau in Bk} |Delta_T tau(z; y_T)|          ('Sb')
    PPB_res[T, Bk] = the same with every host of the block that is not in T held at its anchor state         ('SAb')

(absolute values term by term: no cancellation between the terms of a block is used by the bound, so none is allowed
on the exact side).  Checks:
  B1  Sb[T, Bk]  >= PPB_all[T, Bk]      for every subset and block;
  B2  SAb[T, Bk] >= PPB_res[T, Bk];
  B3  at every state x, every block, every order m:  sum_{tau in Bk} |tau(x) - I_{m-1} tau(x)| <= sum_{T in S(x), |T| = m} SAb[T, Bk]
      (and the same for Sb) -- the block-wise form of the inequality the certificate uses (Theorem AH);
  B4  at every state, |g_s - I_{m-1} g_s|(x) <= sum_{T in S(x)} chat_T for the true charges, all charges positive and the
      sign patterns of p8_02_signblind.py (variants Sb, SAb);
  B5  the sum over blocks of 'Sb' equals P3's own per-subset bound termwise.TermBound in anchored mode (an independent
      code path of workstream P3), and Sb <= S, SAb <= SA, SAb <= Sb.

usage: python3 -B p8_03c_blockcheck.py SEQ BB TAU [--budget SECONDS]
needs out/m1_<tag>.npz, out/sr_<tag>.npz; uses out/sb_<tag>.npz if present.  Writes logs/bc_<tag>.log, out/bc_<tag>.json
"""
import sys, os, json, time, itertools
import numpy as np
from p8lib import *
from p8sr import AHBound
from termwise import TermBound                         # P3 (read-only)

a = sys.argv[1:]
seq, bb, tau = a[0], a[1], float(a[2])
BUDGET = float(a[a.index("--budget") + 1]) if "--budget" in a else 1e18
tag = tagname(seq, bb, tau)
if os.path.exists(os.path.join(HERE, "out", f"bc_{tag}.json")) and "--force" not in a:
    print(f"out/bc_{tag}.json exists: this run is complete; nothing done"); sys.exit(0)
ckpt = os.path.join(MYCACHE, f"bc_{tag}_ckpt.npz")
resume = os.path.exists(ckpt)
log = Log(os.path.join(HERE, "logs", f"bc_{tag}.log"), append=resume)
t0 = time.time()
Z = np.load(os.path.join(HERE, "out", f"m1_{tag}.npz")); Zs = np.load(os.path.join(HERE, "out", f"sr_{tag}.npz"))
G = GBModel(seq, bb, tau=tau)
n, N = G.ns, G.nat
shape = tuple(G.k)
st = G.product_states(); S = len(st)
x0 = tuple(int(v) for v in Z["anchor"])
Tlist = [tuple(int(v) for v in row if v >= 0) for row in Z["Tlist"]]
orders = np.array([len(T) for T in Tlist]); maxorder = int(orders.max()); nT = len(Tlist)
tindex = {T: ti for ti, T in enumerate(Tlist)}
site_of = Z["site_of"]
blocks = [("self", -1), ("cross1", -1)] + [(kind, l) for l in range(n) for kind in ("self", "cross1")] + [("cross2", l, l2) for l in range(n) for l2 in range(l + 1, n)]
bindex = {b: i for i, b in enumerate(blocks)}
nB = len(blocks)


def block_of(p, q):
    hp, hq = int(site_of[p]), int(site_of[q])
    if p == q:
        return bindex[("self", hp)]
    hs = sorted({hp, hq} - {-1})
    if len(hs) == 0:
        return bindex[("cross1", -1)]
    if len(hs) == 1:
        return bindex[("cross1", hs[0])]
    return bindex[("cross2", hs[0], hs[1])]


mlist = [m for m in range(3, maxorder + 1) if (orders == m).any()]
need = nT * nB * S * 8 / 1e9
log(f"=== p8_03c_blockcheck: {seq} on {bb}, tau {tau}: atoms {N}, sites {n}, {S} states, anchor {x0}; {nT} subsets, {nB} blocks; accumulators at most {need:.2f} GB" + ("; RESUMING" if resume else ""))
assert need < 1.6, "accumulators too large for the memory limit of this workstream"
B = 1.0 / G.invB(G.descreening(st))
if resume:
    z = np.load(ckpt, allow_pickle=True); p_next = int(z["p_next"]); ACC = z["ACC"].item(); ACCR = z["ACCR"]
    log(f"    checkpoint read: rows 0..{p_next - 1} done")
else:
    p_next = 0; ACC = {}; ACCR = np.zeros((len(mlist), nB, S))
tlast = time.time(); stopped = False
for p in range(p_next, N):
    cols = np.arange(p, N)
    M = kernel_row(G, st, p, B, cols)
    M *= pair_coef(G, p, cols)[None, :]
    F = M.reshape(shape + (len(cols),))
    bcol = np.array([block_of(p, q) for q in cols])
    groups = [(b_, np.flatnonzero(bcol == b_)) for b_ in np.unique(bcol)]

    def cb(T, D):
        ti = tindex[T]
        A = np.abs(D)
        for b_, sel in groups:
            v = A[..., sel].sum(axis=-1)
            key = (ti, int(b_))
            if key in ACC:
                ACC[key] += v
            else:
                ACC[key] = v

    anch_walk(F, x0, n, maxorder, cb)
    acc = np.zeros_like(F)
    for r in range(0, maxorder):
        for U in itertools.combinations(range(n), r):
            if any(shape[i] < 2 for i in U):
                continue
            idx = tuple(slice(None) if i in U else x0[i] for i in range(n))
            dd = F[idx].copy()
            for a_, i in enumerate(U):
                dd = dd - np.take(dd, [x0[i]], axis=a_)
            acc += dd.reshape([shape[i] if i in U else 1 for i in range(n)] + [len(cols)])
        if (r + 1) in mlist:
            R = np.abs(F - acc).reshape(S, len(cols))
            mi = mlist.index(r + 1)
            for b_, sel in groups:
                ACCR[mi, int(b_)] += R[:, sel].sum(axis=1)
            del R
    del M, F, acc
    now = time.time()
    if now - tlast > 120 or p == N - 1 or now - t0 > BUDGET:
        tmp = ckpt + ".tmp.npz"
        np.savez(tmp, p_next=p + 1, ACC=np.array(ACC, dtype=object), ACCR=ACCR); os.replace(tmp, ckpt); tlast = now
        log(f"    row {p + 1}/{N} done, checkpoint written, {now - t0:.0f} s, RSS {rss_mb():.0f} MB")
    if now - t0 > BUDGET and p < N - 1:
        stopped = True
        break
if stopped:
    log(f"BUDGET REACHED at row {p + 1}/{N}: checkpoint on disk, run the same command again to continue (not a complete run)")
    log.f.close(); sys.exit(0)

# exact block constants: all contexts, and hosts outside T at the anchor
PPB_all = np.zeros((nT, nB)); PPB_res = np.zeros((nT, nB))
for (ti, b_), v in ACC.items():
    T = Tlist[ti]
    PPB_all[ti, b_] = float(v.max()) if v.size else 0.0
    w = v
    for h in blocks[b_][1:]:
        if h >= 0 and h not in T:
            w = np.take(w, [x0[h]], axis=h)
    PPB_res[ti, b_] = float(w.max()) if w.size else 0.0
del ACC
SR = AHBound(G, x0, EnvelopeSup(G), K=maxorder)
Sb = np.zeros((nT, nB)); SAb = np.zeros((nT, nB))
for ti, T in enumerate(Tlist):
    out = SR.total_T_blocks(len(T), T)
    for key, v in out["Sb"].items():
        Sb[ti, bindex[key]] = v
    for key, v in out["SAb"].items():
        SAb[ti, bindex[key]] = v
tol = 1e-12
res = dict(seq=seq, bb=bb, tau=tau, natoms=N, nstates=S, nblocks=nB, checks={})


def rep(name, bnd, ex, text):
    v = int((bnd < ex - tol).sum()); mk = ex > 1e-10
    r = bnd[mk] / ex[mk]
    log(f"    {name} {text}: {bnd.size} comparisons, {v} violations; ratio bound/exact (exact > 1e-10): min {r.min():.4f}, median {np.median(r):.2f}, max {r.max():.1f}")
    res["checks"][name] = dict(n=int(bnd.size), violations=v, min_ratio=float(r.min()), median_ratio=float(np.median(r)))


rep("B1", Sb, PPB_all, "'Sb' block bound >= exact block constant (all contexts; absolute values term by term)")
rep("B2", SAb, PPB_res, "'SAb' block bound >= exact block constant with the hosts outside T at the anchor")
vfail = int((SAb < PPB_all - tol).sum())
log(f"    (for information: 'SAb' < exact ALL-context block constant in {vfail} of {SAb.size} cases)")
# B3 state level per block
chg = (st != np.array(x0)[None, :])
n3 = 0; v3 = {"Sb": 0, "SAb": 0}; r3 = {"Sb": np.inf, "SAb": np.inf}
envT = {}
for mi, m in enumerate(mlist):
    sel = np.flatnonzero(orders == m)
    inS = np.stack([chg[:, list(Tlist[ti])].all(axis=1) for ti in sel], axis=1).astype(float)
    envT[m] = (sel, inS)
    for name, arr in (("Sb", Sb), ("SAb", SAb)):
        env = inS @ arr[sel]                           # (S, nB)
        R = ACCR[mi].T                                 # (S, nB)
        v3[name] += int((R > env + 1e-11).sum())
        mk = R > 1e-9
        if mk.any():
            r3[name] = min(r3[name], float((env[mk] / R[mk]).min()))
    n3 += S * nB
log(f"    B3 every state, block and order: sum over the terms of the block of |tau - I_(m-1) tau|(x) <= block envelope: {n3} comparisons per variant; violations Sb: {v3['Sb']}, SAb: {v3['SAb']}; "
    f"smallest ratio envelope/exact: Sb {r3['Sb']:.4f}, SAb {r3['SAb']:.4f}")
res["checks"]["B3"] = dict(n=n3, violations=v3, min_ratio=r3)
# B4 state level, whole function, sign patterns
systems = [("true charges", Z["g"]), ("all charges positive", Z["gabs"])]
sbf = os.path.join(HERE, "out", f"sb_{tag}.npz")
if os.path.exists(sbf):
    sb = np.load(sbf)
    for k_, m_ in enumerate(sb["orders"]):
        systems.append((f"sign pattern of order {int(m_)}", sb["gp"][:, k_]))
n4 = 0; v4 = {"Sb": 0, "SAb": 0}; r4 = {"Sb": np.inf, "SAb": np.inf}
for m in mlist:
    sel, inS = envT[m]
    for name, arr in (("Sb", Sb), ("SAb", SAb)):
        env = inS @ arr[sel].sum(axis=1)
        for nm, garr in systems:
            gg = garr.reshape(shape)
            r = np.abs(gg - anchored_interp(gg, x0, m - 1)).reshape(-1)
            v4[name] += int((r > env + 1e-9).sum())
            mk = r > 1e-9
            if mk.any():
                r4[name] = min(r4[name], float((env[mk] / r[mk]).min()))
    n4 += S * len(systems)
log(f"    B4 every state, {len(systems)} charge systems ({', '.join(nm for nm, _ in systems)}): |g_s - I_(m-1) g_s| <= envelope: {n4} state checks per variant; violations Sb: {v4['Sb']}, SAb: {v4['SAb']}; "
    f"smallest ratio envelope/|remainder|: Sb {r4['Sb']:.2f}, SAb {r4['SAb']:.2f}")
res["checks"]["B4"] = dict(n=n4, violations=v4, min_ratio=r4)
# B5 consistency with P3's termwise (anchored) and with the pair-wise variants
TB = TermBound(G, sup=EnvelopeSup(G), anchor=x0, kmax=maxorder, pad_I=G.ns * PAD_TAB)
tw = np.array([(TB.self_bound(T, mode="anchored") + TB.cross_bound(T, mode="anchored")) * RND for T in Tlist])
SbT = Sb.sum(axis=1); SAbT = SAb.sum(axis=1)
dev = float(np.abs(SbT - tw).max() / tw.max()); devrel = float((np.abs(SbT - tw) / tw).max())
v5 = int((SbT > Zs["T_S"] * (1 + 1e-9)).sum() + (SAbT > Zs["T_SA"] * (1 + 1e-9)).sum() + (SAbT > SbT * (1 + 1e-9)).sum())
log(f"    B5 'Sb' against P3's termwise.TermBound in anchored mode ({nT} subsets): largest relative deviation {devrel:.1e};  Sb <= S, SAb <= SA, SAb <= Sb: {3 * nT} comparisons, {v5} violations")
res["checks"]["B5"] = dict(n=nT, devrel=devrel, chain_violations=v5)
for m in mlist:
    sel = np.flatnonzero(orders == m)
    tr = float(Z["C_total"][sel].sum()); p3 = float(Z["C_P3"][sel].sum())
    row = dict(truth=tr, P3=p3, S=float(Zs["T_S"][sel].sum()), SA=float(Zs["T_SA"][sel].sum()), Sb=float(SbT[sel].sum()), SAb=float(SAbT[sel].sum()),
               PPB_all=float(PPB_all[sel].sum()), PPB_res=float(PPB_res[sel].sum()), PP=float(Z["C_PP"][sel].sum()))
    res.setdefault("orders", {})[str(m)] = row
    log(f"--- order {m}: sums over {len(sel)} subsets (kcal/mol): truth {tr:.4e} | exact block constants {row['PPB_all']:.4e} (restricted {row['PPB_res']:.4e}) | pair-by-pair {row['PP']:.4e} | "
        f"SAb {row['SAb']:.4e} | Sb {row['Sb']:.4e} | SA {row['SA']:.4e} | S {row['S']:.4e} | P3 {p3:.4e};  P3/SAb = {p3 / row['SAb']:.2f}, S/Sb = {row['S'] / row['Sb']:.3f}, SAb/truth = {row['SAb'] / tr:.1f}")
res["per_subset"] = dict(Sb={"-".join(map(str, T)): float(SbT[ti]) for ti, T in enumerate(Tlist)}, SAb={"-".join(map(str, T)): float(SAbT[ti]) for ti, T in enumerate(Tlist)})
with open(os.path.join(HERE, "out", f"bc_{tag}.json"), "w") as fh:
    json.dump(res, fh, indent=1)
np.savez_compressed(os.path.join(HERE, "out", f"bc_{tag}.npz"), Sb=Sb, SAb=SAb, PPB_all=PPB_all, PPB_res=PPB_res, blocks=np.array([str(b) for b in blocks]))
log.done()
