#!/usr/bin/env python3
"""P9 step 0 -- probe: does the recording subclass reproduce P8's constants, and what do the per-state block arrays
look like?  usage: python3 -B p9_00_probe.py SEQ [BB]   (enumerated instances: K4, K5, LKSE:5)
writes logs/probe_<tag>.log"""
import sys
from p9lib import *

seq = sys.argv[1]; bb = sys.argv[2] if len(sys.argv) > 2 else "H"; tau = tau_of(seq); tag = tagname(seq, bb, tau)
log = Log(os.path.join(LOGS, f"probe_{tag}.log"))
log(f"=== p9_00_probe {seq} on {bb}, tau {tau}; started {now()}")
G, c0, h, J, x0, E0 = setup(seq, bb, tau); n, k = G.ns, list(G.k)
log(f"    {G.nat} atoms, {n} sites, states per site {k}, anchor {x0}")
fbc = os.path.join(P8DIR, "out", f"bc_{tag}.json")
Jd = json.load(open(fbc))["per_subset"] if os.path.exists(fbc) else None
SR = ResBound(G, tuple(x0), EnvelopeSup(G), K=n)
worst = 0.0
for m in range(3, n + 1):
    t1 = time.time(); TB = Tables(n, k, x0, m)
    for T in itertools.combinations(range(n), m):
        parts = theta_parts(SR, m, T)
        tab, non = theta_table(parts, k, x0)
        TB.add(T, tab, parts["sab"], parts["sb"])
        if Jd is not None:
            key = "-".join(map(str, T))
            for var, mine in (("SAb", parts["sab"]), ("Sb", parts["sb"])):
                ref = float(Jd[var][key]); worst = max(worst, abs(mine - ref) / ref)
        if m == 3 or T == tuple(range(m)):
            log(f"    m = {m}, T = {T}: P8's SAb {parts['sab']:.6g}, joint maximum over the states of T {tab.max():.6g} (ratio {tab.max() / parts['sab']:.4f}), "
                f"minimum {tab.min():.6g}, median {np.median(tab):.6g}, value at the first non-anchor states {tab.flat[0]:.6g}; constant part SC*C = {parts['C'] * SC:.6g}")
            for p, l in enumerate(T):
                ax = tuple(q for q in range(m) if q != p); c = tab.max(axis=ax)
                log(f"        site {l}: c_(T,i)(b) / SAb over the non-anchor states b: " + " ".join(f"{v / parts['sab']:.3f}" for v in c))
    TB.finish()
    log(f"--- m = {m}: {len(TB.subs)} subsets [{time.time() - t1:.1f}s]; Gamma (kT): Sb {BETA * TB.sb.sum():.5g}, SAb {BETA * TB.sab.sum():.5g}, joint max {BETA * TB.cJ.sum():.5g}, "
        f"joint min {BETA * TB.cmin.sum():.5g}; cJ <= SAb for every subset: {bool(np.all(TB.cJ <= TB.sab * (1 + 1e-12)))}")
if Jd is not None:
    log(f"    my recorded constants against P8's stored per-subset values (ws_P8/out/bc_{tag}.json), 'Sb' and 'SAb', all orders: largest relative deviation {worst:.2e}")
log.done()
