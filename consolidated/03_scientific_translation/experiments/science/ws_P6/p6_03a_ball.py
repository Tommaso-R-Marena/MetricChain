"""
P6 step 5a: values of g on the Hamming ball of radius M about P3's anchor for a LONG chain, in parts that can run as
separate processes (each part is its own checkpoint file).  With --merge the parts are concatenated into the cache
file that p6lib.ball_terms reads (same format as P3's ball cache: states in pwmodel.ball_states order, values).

usage: python3 -B p6_03a_ball.py SEQ BB TAU M --part i --of k      (evaluate part i of k, 0-based)
       python3 -B p6_03a_ball.py SEQ BB TAU M --merge --of k
"""
import sys, os, time, hashlib
import numpy as np
import p6lib as L
pw = L.pw

a = sys.argv[1:]
seq, bb, tau, M = a[0], a[1], float(a[2]), int(a[3])
K = int(a[a.index("--of") + 1])
t0 = time.time()
G, c0, h, J, x0, E0 = L.setup(seq, bb, tau)
blocks, tot = pw.ball_states(G.k, x0, M)
allst = np.concatenate([b for _, b in blocks], axis=0)
ah = hashlib.sha1(str((tuple(x0), [list(map(int, dd)) for dd in G.dom])).encode()).hexdigest()[:10]
stem = os.path.join(L.MYCACHE, f"ball_{seq.replace(':', 'c')}_{bb}_t{tau:.2f}_gbn2_M{M}_{ah}")
edges = np.linspace(0, tot, K + 1).astype(int)
print(f"=== ball: {seq} on {bb}, tau {tau}: atoms {G.nat}, sites {G.ns}, anchor E = {E0:.6f}; radius {M}: {tot} states; setup {time.time() - t0:.1f}s", flush=True)
if "--merge" in a:
    vals = np.concatenate([np.load(f"{stem}_part{i}of{K}.npy") for i in range(K)])
    assert len(vals) == tot and np.isfinite(vals).all()
    rng = np.random.default_rng(99)
    pick = rng.integers(0, tot, 24)
    dev = float(np.abs(vals[pick] - G.energy(allst[pick])).max())           # P3's own evaluator at 24 random ball states
    assert dev < 1e-8, dev
    np.savez(stem + ".npz", states=allst.astype(np.int16), vals=vals)
    print(f"    merged {K} parts -> {os.path.basename(stem)}.npz; bulk evaluator vs P3's own evaluator at 24 ball states: {dev:.1e}")
    print(f"DONE p6_03a_ball merge {seq} {bb} {tau} M={M} [{time.time() - t0:.0f}s]", flush=True)
    sys.exit(0)
i = int(a[a.index("--part") + 1])
lo, hi = int(edges[i]), int(edges[i + 1])
fn = f"{stem}_part{i}of{K}.npy"
vals = np.empty(hi - lo)
t1 = time.time()
for s in range(lo, hi, 2048):
    e = min(hi, s + 2048)
    vals[s - lo:e - lo] = G.bulk_energy(allst[s:e])
    if ((s - lo) // 2048) % 5 == 0:
        print(f"      part {i}/{K}: {e - lo}/{hi - lo} evaluations, {time.time() - t1:.0f}s", flush=True)
np.save(fn, vals)
print(f"    part {i} of {K}: states {lo}..{hi - 1}, {hi - lo} evaluations in {time.time() - t1:.1f}s ({1e3 * (time.time() - t1) / max(1, hi - lo):.2f} ms each) -> {os.path.basename(fn)}")
print(f"DONE p6_03a_ball part {i}/{K} {seq} {bb} {tau} M={M} [{time.time() - t0:.0f}s]", flush=True)
