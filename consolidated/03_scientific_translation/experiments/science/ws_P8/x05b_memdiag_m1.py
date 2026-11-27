"""P8 diagnostic (memory incident of 06:46): did the MAIN enumeration pass (p8_01_measure.py as it ran before the fix)
leak as well?  Reproduces its row loop on a small instance with P5's anch_consts called directly (no gc.collect) and
prints the resident memory row by row.  usage: python3 -B x05b_memdiag_m1.py SEQ BB TAU NROWS"""
import sys, os, gc
import numpy as np
from p8lib import *
seq, bb, tau, nrows = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
G, st, shape, f, g, E, x0 = build(seq, bb, tau)
n, N, S = G.ns, G.nat, len(st)
maxorder = n
Tlist = subsets(n, shape, 3, maxorder)
B = 1.0 / G.invB(G.descreening(st))
print(f"{seq}/{bb}: S = {S}, N = {N}, one row array = {S * N * 8 / 1e6:.0f} MB; RSS before the loop {rss_mb():.0f} MB", flush=True)
PP = np.zeros((len(Tlist), N, N)); REM = np.zeros((maxorder + 1, N, N))
for p in range(nrows):
    cols = np.arange(p, N)
    M = kernel_row(G, st, p, B, cols)
    M *= pair_coef(G, p, cols)[None, :]
    c_ = (P5.anch_consts if len(sys.argv) > 5 and sys.argv[5] == "old" else anch_consts)(M.reshape(shape + (len(cols),)), x0, n, maxorder)   # "old": as before the fix
    for ti, T in enumerate(Tlist):
        PP[ti, p, p:] = c_[T]
    del c_
    rr_ = anchored_remainders(M.reshape(shape + (len(cols),)), x0, n, list(range(3, maxorder + 1)))
    for m_, v_ in rr_.items():
        REM[m_, p, p:] = v_
    del rr_, M
    print(f"  row {p}: RSS {rss_mb():.0f} MB; gc counts {gc.get_count()}", flush=True)
import resource
print(f"peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")
