"""
P8 step 3 -- the new constants for peptides too large to enumerate: every subset T of order m, by explicit enumeration
of the subsets (the state-resolved maxima have no closed form over T), in the four variants of p8sr.py:

    P3  (P3's own bound; its sum must reproduce P3's closed form Gamma_m),   S  (state-resolved; bounds c_T^anch),
    AH  (anchored hosts, P3's types; sum must reproduce the closed form total_ah),   SA  (anchored hosts + state-resolved).

Anchor: P3's coordinate-descent anchor (pwmodel.icm_anchor), as in P3's pipeline and the coordinator's reach table.

usage: python3 -B p8_04_gamma12.py SEQ BB TAU M [--budget SECONDS] [--limit K]
  --budget: stop after that many seconds at a subset boundary (checkpoint on disk; run again to continue)
  --limit K: only the first K subsets (timing test; nothing is saved)
writes logs/g12_<tag>_m<M>.log, out/g12_<tag>_m<M>.npz (per-subset constants of the four variants, self and cross parts)
"""
import sys, os, time, itertools, json
import numpy as np
from p8lib import *
from p8sr import AHBound, VARIANTS
import pwmodel as pw                                  # P3 (read-only)

a = sys.argv[1:]
seq, bb, tau, m = a[0], a[1], float(a[2]), int(a[3])
BUDGET = float(a[a.index("--budget") + 1]) if "--budget" in a else 1e18
LIMIT = int(a[a.index("--limit") + 1]) if "--limit" in a else None
tag = tagname(seq, bb, tau) + f"_m{m}"
if os.path.exists(os.path.join(HERE, "out", f"g12_{tag}.npz")) and "--force" not in a and LIMIT is None:
    print(f"out/g12_{tag}.npz exists: this run is complete (use --force to redo it); nothing done"); sys.exit(0)
ckpt = os.path.join(MYCACHE, f"g12_{tag}_ckpt.npz")
resume = os.path.exists(ckpt) and LIMIT is None
log = Log(os.path.join(HERE, "logs", f"g12_{tag}.log" if LIMIT is None else f"g12_{tag}_timing.log"), append=resume)
t0 = time.time()
G = GBModel(seq, bb, tau=tau)
n, N = G.ns, G.nat
c0, h, J = pw.known_tables(G)
x0, E0, nev = pw.icm_anchor(G, c0, h, J)
x0 = tuple(int(v) for v in x0)
Tall = [T for T in itertools.combinations(range(n), m) if all(G.k[i] >= 2 for i in T)]
log(f"=== p8_04_gamma12: {seq} on {bb}, tau {tau}: atoms {N}, sites {n}, states per site {list(G.k)}; anchor (ICM) {x0}, E = {E0:.6f} kcal/mol; order {m}: {len(Tall)} subsets"
    + ("; RESUMING" if resume else ""))
SR = AHBound(G, x0, EnvelopeSup(G), K=m)
nT = len(Tall)
if resume:
    z = np.load(ckpt); i_next = int(z["i_next"]); C = z["C"]
    assert list(z["anchor"]) == list(x0) and C.shape == (nT, len(VARIANTS), 2)
    log(f"    checkpoint read: subsets 0..{i_next - 1} done")
else:
    i_next = 0; C = np.zeros((nT, len(VARIANTS), 2))  # [subset, variant, (self, cross)]
tlast = time.time(); stopped = False
for i in range(i_next, nT if LIMIT is None else min(nT, LIMIT)):
    out = SR.total_T(m, Tall[i])
    for vi, v in enumerate(VARIANTS):
        C[i, vi] = out[v]
    now = time.time()
    if LIMIT is not None:
        log(f"    subset {i} {Tall[i]}: " + ", ".join(f"{v} {sum(out[v]):.5g}" for v in VARIANTS) + f"  [{now - t0:.1f} s]")
        continue
    if now - tlast > 60 or i == nT - 1 or now - t0 > BUDGET:
        tmp = ckpt + ".tmp.npz"
        np.savez(tmp, i_next=i + 1, C=C, anchor=np.array(x0)); os.replace(tmp, ckpt); tlast = now
        log(f"    subset {i + 1}/{nT} done, checkpoint written, {now - t0:.0f} s")
    if now - t0 > BUDGET and i < nT - 1:
        stopped = True
        break
if LIMIT is not None:
    log.done(); sys.exit(0)
if stopped:
    log(f"BUDGET REACHED at subset {i + 1}/{nT}: checkpoint on disk, run the same command again to continue (not a complete run)")
    log.f.close(); sys.exit(0)
tot = C.sum(axis=2)                                   # (nT, variants)
Gam = tot.sum(axis=0)
t1 = time.time()
cf = SR.total(m); cfa = SR.total_ah(m)
dev_p3 = abs(Gam[VARIANTS.index("P3")] - sum(cf)) / sum(cf); dev_ah = abs(Gam[VARIANTS.index("AH")] - sum(cfa)) / sum(cfa)
log(f"    closed forms ({time.time() - t1:.0f} s): P3's Gamma_{m} = {sum(cf):.8g} kcal/mol, sum over the {nT} subsets of variant 'P3' = {Gam[0]:.8g} (relative deviation {dev_p3:.1e}); "
    f"anchored-hosts closed form {sum(cfa):.8g}, sum of variant 'AH' {Gam[VARIANTS.index('AH')]:.8g} (relative deviation {dev_ah:.1e})")
assert dev_p3 < 1e-9 and dev_ah < 1e-9
nviol = int((tot[:, VARIANTS.index("S")] > tot[:, 0] * (1 + 1e-9)).sum() + (tot[:, VARIANTS.index("SA")] > tot[:, VARIANTS.index("S")] * (1 + 1e-9)).sum()
            + (tot[:, VARIANTS.index("SA")] > tot[:, VARIANTS.index("AH")] * (1 + 1e-9)).sum() + (tot[:, VARIANTS.index("AH")] > tot[:, 0] * (1 + 1e-9)).sum())
log(f"    per-subset chains SA <= S <= P3, SA <= AH <= P3: {4 * nT} comparisons, {nviol} violations")
for vi, v in enumerate(VARIANTS):
    r = tot[:, 0] / tot[:, vi]
    log(f"    Gamma_{m}[{v:2s}] = {Gam[vi]:12.6g} kcal/mol = {Gam[vi] * BETA:12.6g} kT  (self {C[:, vi, 0].sum():.4g});  P3 / {v}: sums {Gam[0] / Gam[vi]:.3f}; per subset min {r.min():.2f}, median {np.median(r):.2f}, max {r.max():.2f}")
np.savez_compressed(os.path.join(HERE, "out", f"g12_{tag}.npz"), T=np.array(Tall), C=C, anchor=np.array(x0), variants=np.array(VARIANTS), k=np.array(G.k),
                    Gamma_closed=np.array(cf), Gamma_ah_closed=np.array(cfa))
log.done()
