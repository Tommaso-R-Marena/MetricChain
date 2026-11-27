"""
P8 -- the true ensemble of a peptide too large to enumerate, by heat-bath Gibbs sampling (UNCERTIFIED; a sample).

The same algorithm, chain count, sweep count and random seed as the coordinator's
`pi_inference/serine_helix_reach.gibbs` as called by `certificate_reach_table.py` (16 chains started at P3's anchor,
sites updated in order from their exact conditional law, states kept after every sweep past the burn-in; numpy
default_rng(20261126)), re-implemented here so that nothing of pi_inference is imported or written.  If the
re-implementation is faithful the off-anchor frequencies by site equal those of
`pi_inference/certificate_reach_table_H.json` exactly (compared at the end).

usage: python3 -B p8_05_gibbs.py SEQ BB TAU [--nsweep N] [--budget SECONDS]
writes logs/gibbs_<tag>.log, out/gibbs_<tag>.npz (X: states (chains * kept sweeps, n); chain index; anchor)
"""
import sys, os, time, json
import numpy as np
from p8lib import *
import pwmodel as pw                                  # P3 (read-only)

a = sys.argv[1:]
seq, bb, tau = a[0], a[1], float(a[2])
BUDGET = float(a[a.index("--budget") + 1]) if "--budget" in a else 1e18
tag = tagname(seq, bb, tau)
if os.path.exists(os.path.join(HERE, "out", f"gibbs_{tag}.npz")) and "--force" not in a:
    print(f"out/gibbs_{tag}.npz exists: this run is complete (use --force to redo it); nothing done"); sys.exit(0)
ckpt = os.path.join(MYCACHE, f"gibbs_{tag}_ckpt.npz")
resume = os.path.exists(ckpt)
log = Log(os.path.join(HERE, "logs", f"gibbs_{tag}.log"), append=resume)
t0 = time.time()
G = GBModel(seq, bb, tau=tau)
n = G.ns; k = list(G.k)
c0, h, J = pw.known_tables(G)
x0, E0, nev = pw.icm_anchor(G, c0, h, J)
x0 = np.array([int(v) for v in x0])
NCHAIN, BURN = 16, 50
NSWEEP = int(a[a.index("--nsweep") + 1]) if "--nsweep" in a else (250 if sum(k) <= 100 else 150)
log(f"=== p8_05_gibbs: {seq} on {bb}, tau {tau}: {G.nat} atoms, {n} sites, states per site {k}; anchor (ICM) {tuple(int(v) for v in x0)}, E = {E0:.6f}; "
    f"{NCHAIN} chains, {NSWEEP} sweeps, burn-in {BURN}" + ("; RESUMING" if resume else ""))
rng = np.random.default_rng(20261126)
if resume:
    z = np.load(ckpt, allow_pickle=True)
    sw0 = int(z["sw_next"]); X = z["X"]; keep = list(z["keep"]); rng.bit_generator.state = z["rng_state"].item()
    log(f"    checkpoint read: sweeps 0..{sw0 - 1} done")
else:
    sw0 = 0; X = np.tile(x0.astype(np.int64), (NCHAIN, 1)); keep = []
tlast = time.time(); stopped = False
for sw in range(sw0, NSWEEP):
    for i in range(n):
        C = np.repeat(X, k[i], axis=0); C[:, i] = np.tile(np.arange(k[i]), NCHAIN)
        E = (pw.f_energy(C, c0, h, J) + G.bulk_energy(C)).reshape(NCHAIN, k[i])
        P = np.exp(-BETA * (E - E.min(1, keepdims=True))); P /= P.sum(1, keepdims=True)
        u = rng.random(NCHAIN); X[:, i] = np.minimum((P.cumsum(1) < u[:, None]).sum(1), k[i] - 1)
    if sw >= BURN:
        keep.append(X.copy())
    now = time.time()
    if now - tlast > 60 or sw == NSWEEP - 1 or now - t0 > BUDGET:
        tmp = ckpt + ".tmp.npz"
        np.savez(tmp, sw_next=sw + 1, X=X, keep=np.array(keep).reshape(-1, NCHAIN, n), rng_state=np.array(rng.bit_generator.state, dtype=object))
        os.replace(tmp, ckpt); tlast = now
        log(f"    sweep {sw + 1}/{NSWEEP} done, checkpoint written, {now - t0:.0f} s")
    if now - t0 > BUDGET and sw < NSWEEP - 1:
        stopped = True
        break
if stopped:
    log(f"BUDGET REACHED at sweep {sw + 1}/{NSWEEP}: checkpoint on disk, run the same command again to continue (not a complete run)")
    log.f.close(); sys.exit(0)
K = np.array(keep).reshape(-1, NCHAIN, n)            # (kept sweeps, chains, n)
off = (K != x0[None, None, :])
fr_chain = off.mean(axis=0)                           # (chains, n)
psite = fr_chain.mean(axis=0)
noff = fr_chain.sum(axis=1)
log(f"    {K.shape[0] * NCHAIN} states kept; off the anchor: {noff.mean():.3f} +- {noff.std(ddof=1) / 4:.3f} of {n} (standard error over the 16 chains); by site: "
    + " ".join(f"{v:.3f}" for v in psite))
ref = os.path.join(SCI, "pi_inference", "certificate_reach_table_H.json")
if bb == "H" and os.path.exists(ref):
    for r in json.load(open(ref)):
        if r["seq"] == seq and abs(r["tau"] - tau) < 1e-9:
            d = float(np.abs(np.array(r["p_site"]) - psite).max())
            log(f"    against the coordinator's table (certificate_reach_table_H.json): largest difference of an off-anchor frequency {d:.2e}"
                + ("  -- the same sample" if d < 1e-12 else "  -- NOT the same sample (statistically comparable only)"))
Xall = K.transpose(1, 0, 2).reshape(-1, n)            # chain-major
np.savez_compressed(os.path.join(HERE, "out", f"gibbs_{tag}.npz"), X=Xall, chain=np.repeat(np.arange(NCHAIN), K.shape[0]), anchor=x0, k=np.array(k), psite=psite)
log.done()
