"""
P8 -- exact RESTRICTED anchored constants of every pair term (validation target of Theorem AH).

For every subset T (order 3..maxorder) and every atom pair p <= q with hosts h1, h2:

    PPA[T, p, q] = sup { |Delta_T t_pq(z; x0_T -> y_T)| :  y_T in X_T,  z in X with z_h = x0_h for every host h of the pair
                                                             that is NOT in T }

(the other sites outside T run over all their states).  PPA <= PP (all contexts; p8_01_measure.py), with equality when
both hosts lie in T or the pair has no host.  By exact enumeration of all states.

usage: python3 -B p8_01b_restricted.py SEQ BB TAU [maxorder=6] [--budget SECONDS]
needs out/m1_<tag>.npz (anchor, subset list, PP for the cross-check).  Writes logs/m1b_<tag>.log, out/m1b_<tag>.npz
"""
import sys, os, time
import numpy as np
from p8lib import *

a = sys.argv[1:]
seq, bb, tau = a[0], a[1], float(a[2])
BUDGET = float(a[a.index("--budget") + 1]) if "--budget" in a else 1e18
tag = tagname(seq, bb, tau)
if os.path.exists(os.path.join(HERE, "out", f"m1b_{tag}.npz")) and "--force" not in a:
    print(f"out/m1b_{tag}.npz exists: this run is complete (use --force to redo it); nothing done"); sys.exit(0)
ckpt = os.path.join(MYCACHE, f"m1b_{tag}_ckpt.npz")
resume = os.path.exists(ckpt)
log = Log(os.path.join(HERE, "logs", f"m1b_{tag}.log"), append=resume)
t0 = time.time()
Z = np.load(os.path.join(HERE, "out", f"m1_{tag}.npz"))
G = GBModel(seq, bb, tau=tau)
n, N = G.ns, G.nat
shape = tuple(G.k)
assert tuple(Z["shape"]) == shape
st = G.product_states(); S = len(st)
x0 = tuple(int(v) for v in Z["anchor"])
Tlist = [tuple(int(v) for v in row if v >= 0) for row in Z["Tlist"]]
nT = len(Tlist); maxorder = max(len(T) for T in Tlist)
tindex = {T: ti for ti, T in enumerate(Tlist)}
site_of = Z["site_of"]
log(f"=== p8_01b_restricted: {seq} on {bb}, tau {tau}: atoms {N}, sites {n}, {S} states, anchor {x0}; {nT} subsets" + ("; RESUMING" if resume else ""))
B = 1.0 / G.invB(G.descreening(st))
if resume:
    z = np.load(ckpt); p_next = int(z["p_next"]); PPA = z["PPA"]
    log(f"    checkpoint read: rows 0..{p_next - 1} done")
else:
    p_next = 0; PPA = np.zeros((nT, N, N))
tlast = time.time(); stopped = False
CB = max(1, int(60e6 // (8 * S)))                    # columns per block: one block array is at most 60 MB
for p in range(p_next, N):
    l1 = int(site_of[p])
    for c0_ in range(p, N, CB):
        cols = np.arange(c0_, min(N, c0_ + CB))
        M = kernel_row(G, st, p, B, cols)
        M *= pair_coef(G, p, cols)[None, :]
        groups = [(int(h), np.flatnonzero(site_of[cols] == h)) for h in np.unique(site_of[cols])]

        def cb(T, D):
            ti = tindex[T]
            A = D
            if l1 >= 0 and l1 not in T:
                A = np.take(A, [x0[l1]], axis=l1)
            for l2, sel in groups:
                sub = A[..., sel]
                if l2 >= 0 and l2 not in T and l2 != l1:
                    sub = np.take(sub, [x0[l2]], axis=l2)
                PPA[ti, p, cols[sel]] = np.abs(sub).reshape(-1, len(sel)).max(axis=0) if sub.size else 0.0

        anch_walk(M.reshape(shape + (len(cols),)), x0, n, maxorder, cb)
        del M
    now = time.time()
    if now - tlast > 60 or p == N - 1 or now - t0 > BUDGET:
        tmp = ckpt + ".tmp.npz"
        np.savez(tmp, p_next=p + 1, PPA=PPA); os.replace(tmp, ckpt); tlast = now
        log(f"    row {p + 1}/{N} done, checkpoint written, {now - t0:.0f} s, RSS {rss_mb():.0f} MB")
    if now - t0 > BUDGET and p < N - 1:
        stopped = True
        break
if stopped:
    log(f"BUDGET REACHED at row {p + 1}/{N}: checkpoint on disk, run the same command again to continue (not a complete run)")
    log.f.close(); sys.exit(0)
PP = Z["PP"]
iu = np.triu_indices(N)
d = PP[:, iu[0], iu[1]] - PPA[:, iu[0], iu[1]]
nviol = int((d < -1e-12).sum())
# equality where no host of the pair is outside T
eq_ok = 0; eq_n = 0
for ti, T in enumerate(Tlist):
    inT = np.isin(site_of, T) | (site_of < 0)
    mk = inT[iu[0]] & inT[iu[1]]
    eq_n += int(mk.sum()); eq_ok += int((np.abs(d[ti][mk]) <= 1e-13).sum())
tot_pp = float(PP[:, iu[0], iu[1]].sum()); tot_ppa = float(PPA[:, iu[0], iu[1]].sum())
log(f"    checks: PPA <= PP for every (T, pair): {d.size} comparisons, {nviol} violations; equal where no host of the pair is outside T: {eq_ok} of {eq_n}")
for m in range(3, maxorder + 1):
    sel = [ti for ti, T in enumerate(Tlist) if len(T) == m]
    if sel:
        a_ = float(PP[sel][:, iu[0], iu[1]].sum()); b_ = float(PPA[sel][:, iu[0], iu[1]].sum())
        log(f"    order {m}: sum over subsets and pairs of the exact constants: all contexts {a_:.6e}, hosts outside T at the anchor {b_:.6e} (ratio {a_ / b_:.3f})")
np.savez_compressed(os.path.join(HERE, "out", f"m1b_{tag}.npz"), PPA=PPA)
log.done()
