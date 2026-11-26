"""P8 diagnostic (memory incident of 06:46): resident memory of the restricted enumeration pass, row by row, on a small
instance.  usage: python3 -B x05_memdiag.py SEQ BB TAU NROWS MODE   (MODE: 'old' = the callback of p8_01b as it was; 'new' = fixed)"""
import sys, os, time, gc
import numpy as np
from p8lib import *
seq, bb, tau, nrows, mode = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
tag = tagname(seq, bb, tau)
Z = np.load(os.path.join(HERE, "out", f"m1_{tag}.npz"))
G = GBModel(seq, bb, tau=tau)
n, N = G.ns, G.nat
shape = tuple(G.k)
st = G.product_states(); S = len(st)
x0 = tuple(int(v) for v in Z["anchor"])
Tlist = [tuple(int(v) for v in row if v >= 0) for row in Z["Tlist"]]
nT = len(Tlist); maxorder = max(len(T) for T in Tlist)
tindex = {T: ti for ti, T in enumerate(Tlist)}
site_of = Z["site_of"]
B = 1.0 / G.invB(G.descreening(st))
PPA = np.zeros((nT, N, N))
print(f"{seq}/{bb}: S = {S}, N = {N}, one row array = {S * N * 8 / 1e6:.0f} MB; RSS before the loop {rss_mb():.0f} MB", flush=True)
for p in range(nrows):
    cols = np.arange(p, N)
    M = kernel_row(G, st, p, B, cols)
    M *= pair_coef(G, p, cols)[None, :]
    l1 = int(site_of[p])
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
            PPA[ti, p, p + sel] = np.abs(sub).reshape(-1, len(sel)).max(axis=0) if sub.size else 0.0

    r0 = rss_mb()
    anch_walk(M.reshape(shape + (len(cols),)), x0, n, maxorder, cb)
    r1 = rss_mb()
    del M
    if mode == "new":
        gc.collect()
    print(f"  row {p}: RSS before walk {r0:.0f}, after walk {r1:.0f}, after del{'+gc' if mode == 'new' else ''} {rss_mb():.0f} MB; gc counts {gc.get_count()}", flush=True)
import resource
print(f"peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")
