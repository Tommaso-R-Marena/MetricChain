#!/usr/bin/env python3
"""P9 step 0b -- consistency of the two-stage resolver (p9lib.Resolver) with workstream P8's code path.

For every subset T of every order m = 3..n of an enumerated instance (or for --sample N random subsets of order --m at
twelve residues):
  C1  stage 1, block by block: the maximum over the states of T of my block table equals P8's 'SAb' block constant
      (the table IS P8's array before `_c1`/`_c2`; this checks my reading of which entries they combine);
  C2  stage 2 with the actual increments replaced by P3's maxima ("maxmode") equals stage 1, block by block
      (checks my re-implementation of the sum over set partitions with the increments kept as functions of the state);
  C3  stage 2 <= stage 1 pointwise, block by block (monotonicity: every increment is at most its maximum);
  C4  stage 2 "lite" (blocks with all hosts outside T at stage 1) lies between stage 2 and stage 1;
  and prints how much stage 2 gains: maximum, median and minimum of Theta_T over the states of T, both stages.
usage: python3 -B p9_00b_consistency.py SEQ [--m M --sample N]     writes logs/consistency_<tag>[_m<M>].log"""
import sys
from p9lib import *

a = sys.argv[1:]; seq = a[0]; bb = "H"; tau = tau_of(seq); tag = tagname(seq, bb, tau)
MS = int(a[a.index("--m") + 1]) if "--m" in a else None
NS = int(a[a.index("--sample") + 1]) if "--sample" in a else None
log = Log(os.path.join(LOGS, f"consistency_{tag}" + (f"_m{MS}" if MS else "") + ".log"))
log(f"=== p9_00b_consistency {seq} on {bb}, tau {tau}; started {now()}")
G, c0, h, J, x0, E0 = setup(seq, bb, tau); n, k = G.ns, list(G.k)
log(f"    {G.nat} atoms, {n} sites, states per site {k}, anchor {x0}")
orders = [MS] if MS else list(range(3, n + 1))
SR = ResBound(G, tuple(x0), EnvelopeSup(G), K=max(orders))
R2 = Resolver(SR); R2m = Resolver(SR, maxmode=True); R2l = Resolver(SR, lite=True)
rng = np.random.default_rng(5)
for m in orders:
    subs = list(itertools.combinations(range(n), m))
    if NS and NS < len(subs):
        subs = [subs[j] for j in sorted(rng.choice(len(subs), size=NS, replace=False))]
    w1 = w2 = 0.0; v3 = v4 = 0; nb = 0; t = [0.0, 0.0, 0.0]; rows = []
    for T in subs:
        t0 = time.time(); out, b1 = R2.blocks(m, T, 1); t[0] += time.time() - t0
        t0 = time.time(); _, b2 = R2.blocks(m, T, 2); t[1] += time.time() - t0
        _, b2m = R2m.blocks(m, T, 2)
        t0 = time.time(); _, b2l = R2l.blocks(m, T, 2); t[2] += time.time() - t0
        shape = [len(R2.non[i]) for i in T]
        th1 = np.zeros(shape); th2 = np.zeros(shape); th2l = np.zeros(shape)
        for (key, t1), (_, t2), (_, t2m), (_, t2l) in zip(b1, b2, b2m, b2l):
            nb += 1
            ref = out["SAb"][key]
            w1 = max(w1, abs(float(t1.max()) - ref) / max(ref, 1e-300))
            f1 = np.broadcast_to(t1, shape); f2m = np.broadcast_to(t2m, shape)
            w2 = max(w2, float(np.abs(f2m - f1).max() / max(f1.max(), 1e-300)))
            f2 = np.broadcast_to(t2, shape); f2l = np.broadcast_to(t2l, shape)
            v3 += int((f2 > f1 * (1 + 1e-12)).sum()); v4 += int((f2l > f1 * (1 + 1e-12)).sum() + (f2 > f2l * (1 + 1e-12)).sum())
            th1 += t1; th2 += t2; th2l += t2l
        sab = sum(out["SAb"].values())
        rows.append((T, sab, th1.max(), np.median(th1), th1.min(), th2.max(), np.median(th2), th2.min(), th2l.max(), np.median(th2l), th2l.min()))
    log(f"--- m = {m}: {len(subs)} subsets, {nb} blocks; C1 stage-1 block maximum against P8's 'SAb' block constant: largest relative deviation {w1:.1e}; "
        f"C2 stage 2 in maxmode against stage 1: largest deviation relative to the block maximum {w2:.1e}; C3 stage 2 > stage 1 at {v3} table entries; "
        f"C4 lite outside [stage 2, stage 1] at {v4} entries; seconds per subset: stage 1 {t[0] / len(subs):.3f}, stage 2 {t[1] / len(subs):.3f}, lite {t[2] / len(subs):.3f}")
    R = np.array([r[1:] for r in rows])
    log(f"    sums over these subsets (kT): SAb {BETA * R[:, 0].sum():.5g} | stage 1: max {BETA * R[:, 1].sum():.5g}, median {BETA * R[:, 2].sum():.5g}, min {BETA * R[:, 3].sum():.5g} | "
        f"stage 2: max {BETA * R[:, 4].sum():.5g}, median {BETA * R[:, 5].sum():.5g}, min {BETA * R[:, 6].sum():.5g} | lite: max {BETA * R[:, 7].sum():.5g}, median {BETA * R[:, 8].sum():.5g}, min {BETA * R[:, 9].sum():.5g}")
    for r in rows[:6]:
        log(f"      T = {r[0]}: SAb {r[1]:.4g} | stage 1 max/med/min {r[2]:.4g} {r[3]:.4g} {r[4]:.4g} | stage 2 {r[5]:.4g} {r[6]:.4g} {r[7]:.4g} | lite {r[8]:.4g} {r[9]:.4g} {r[10]:.4g}")
log.done()
