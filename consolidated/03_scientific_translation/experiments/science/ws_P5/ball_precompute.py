"""
P5 -- checkpointed evaluation of the Hamming ball for workstream P3's pipeline (floor_p3copy.py), for instances whose
ball takes longer than one 20-minute run: the values of g on the ball of radius M about the pipeline's anchor are
computed in parts and stored in the pipeline's own cache format (cache/ball_*.npz: states, vals), which
pwmodel.anchored_terms reads back if and only if the state list is identical to the one it would evaluate.
The file name, the anchor (pw.icm_anchor), the state list (pw.ball_states) and the evaluator (G.bulk_energy) are
exactly those of run_floor.py.

usage: python3 -B ball_precompute.py SEQ BB TAU M part NPARTS     (part = 0 .. NPARTS-1)
       python3 -B ball_precompute.py SEQ BB TAU M merge NPARTS
log: logs/ball_<SEQ>_<BB>_M<M>_part<k>.log / ..._merge.log
"""
import sys, os, time, hashlib
import numpy as np
from p5lib import *
import pwmodel as pw

seq, bb, tau, M, what, nparts = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), sys.argv[5], int(sys.argv[6])
log = Tee(os.path.join(HERE, "logs", f"ball_{seq}_{bb}_M{M}_" + ("merge" if what == "merge" else f"part{what}") + ".log"))
G = GBModel(seq, bb, tau=tau, kind="gbn2")
c0, h, J = pw.known_tables(G)
x0, E0, nev = pw.icm_anchor(G, c0, h, J)
blocks, tot = pw.ball_states(G.k, x0, M)
allst = np.concatenate([b for _, b in blocks], axis=0)
ah = hashlib.sha1(str((tuple(x0), [list(map(int, dd)) for dd in G.dom])).encode()).hexdigest()[:10]
cache_file = os.path.join(HERE, "cache", f"ball_{seq.replace(':', 'c')}_{bb}_t{tau:.2f}_gbn2_M{M}_{ah}.npz")
edges = np.linspace(0, tot, nparts + 1).astype(int)
log(f"=== ball_precompute {seq}/{bb} tau {tau}: {G.nat} atoms, anchor E = {E0:.4f}, ball of radius {M}: {tot} states; cache file {os.path.basename(cache_file)}")
os.makedirs(os.path.join(HERE, "out", "tmp"), exist_ok=True)
pf = lambda k: os.path.join(HERE, "out", "tmp", f"ballpart_{seq}_{bb}_M{M}_{k}of{nparts}.npy")
if what == "merge":
    vals = np.concatenate([np.load(pf(k)) for k in range(nparts)])
    assert len(vals) == tot
    rng = np.random.default_rng(5)
    idx = rng.integers(0, tot, 24)
    dev = float(np.abs(G.energy(allst[idx]) - vals[idx]).max())          # P3's own evaluator on a subsample
    log(f"    merged {nparts} parts; 24 random ball states re-evaluated with P3's own evaluator: largest deviation {dev:.2e} kcal/mol")
    assert dev < 1e-8
    np.savez(cache_file, states=allst.astype(np.int16), vals=vals)
    for k in range(nparts):
        os.remove(pf(k))
else:
    k = int(what)
    lo, hi = edges[k], edges[k + 1]
    vals = np.empty(hi - lo)
    t0 = time.time()
    for s in range(lo, hi, 4096):
        e = min(hi, s + 4096)
        vals[s - lo:e - lo] = G.bulk_energy(allst[s:e])
        if ((s - lo) // 4096) % 5 == 0:
            log(f"    {e - lo}/{hi - lo} evaluations, {time.time() - t0:.0f} s")
    np.save(pf(k), vals)
log.done()
