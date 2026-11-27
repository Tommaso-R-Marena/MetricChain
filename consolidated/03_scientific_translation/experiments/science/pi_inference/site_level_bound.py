#!/usr/bin/env python3
"""THE A-PRIORI BOUND FOR THE SITE LEVEL, in its sharper form, beyond enumeration -- coordinator's script.
For the penalty-free solvable minorant B of f + I_{m-1} g (workstream P3's banded model) and any covering vector of
site penalties gamma:   ln Z(B - sum_i gamma_i s_i) - ln Z(B) >= ln(1 + sum_i p_i (e^{beta gamma_i} - 1)),
p_i the off-anchor marginal of site i under B (exact, by transfer matrix), because e^{g.s} = prod(1 + s_i(e^{g_i} - 1))
>= 1 + sum s_i (e^{g_i} - 1); and sum_i beta gamma_i >= beta (Gamma_m + Phi(all sites)) -- the constants and the
floating-point allowance of the evaluated terms, which is a convex game as well (site_allocation_fw.py).  Minimum: water-filling (site_allocation_fw.py,
waterfill_bound).  Printed: the bound with the marginals, the weaker one with the single-change states, and the
water-filling penalties.  No ball beyond the one on disk, no sampling; one closed-form sum (Gamma_m).
Run:  python3 -B site_level_bound.py SEQ BB m w
"""
import os, sys, math, time, json, resource
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import nested_sampler as NS
from site_allocation_fw import waterfill_bound, GammaOracle
L, pw, BETA = NS.L, NS.pw, NS.BETA

seq, bb, m, w = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
tau = 0.60 if ":" in seq else dict(S=0.70, V=0.70, K=0.70, L=0.60, F=0.60)[seq[0]]
t0 = time.time(); M = m - 1
G, c0, h, J, x0, E0 = L.setup(seq, bb, tau); n, k = G.ns, list(G.k); x0 = np.array(x0)
GF = L.GFBound2(G, x0, L.EnvelopeSup(G), K=m); Gam = float(GammaOracle(GF, m, n).get([(1 << n) - 1])[0])
d, nball, srcb = L.ball_terms(G, x0, M, seq, bb, tau, verbose=False)
lo0, up0 = L.build_models(k, x0, c0, h, J, d, w, M, np.zeros(n), np.zeros((n, n)))
lnZ_base = lo0.lnZ()
p = np.zeros(n); a = np.zeros(n)
for i in range(n):
    ind = pw.BandModel(k, w); v = np.ones(k[i]); v[x0[i]] = 0.0; ind.one[i] = v
    p[i] = lo0.moments(ind)[0]
    stt = np.tile(x0, (k[i], 1)); stt[:, i] = np.arange(k[i]); e = np.delete(lo0.energy(stt), x0[i]); a[i] = math.exp(-BETA * float(e.min()) - lnZ_base)
assert (p >= a * (1 - 1e-9)).all()
PhiN = NS.EPS_G * sum(math.comb(n, s_) * 2 ** s_ for s_ in range(1, M + 1))      # the floating-point game on the full set (site_allocation_fw.py)
Gtot = BETA * (Gam + PhiN)
wf_p, g_p, lam_p = waterfill_bound(np.maximum(p, 1e-300), Gtot); wf_a, g_a, lam_a = waterfill_bound(a, Gtot)
print(f"=== a-priori bound for the site level: {seq}/{bb}, order {m}, band {w}: {n} sites, ball {nball}; Gamma_{m} = {BETA * Gam:.4f} kT; "
      f"floating-point allowance on the full set {BETA * PhiN:.4f} kT; penalty-free minorant ln Z(B) = {lnZ_base:.6f} [{time.time() - t0:.0f}s]")
print("    off-anchor marginals under B, -ln p_i: " + " ".join(f"{-math.log(max(v, 1e-300)):.1f}" for v in p))
print(f"    WITH THE MARGINALS: every covering vector of site penalties has ln Z(m_-) >= {lnZ_base + wf_p:.6f}, at least {wf_p:.6g} nats above ln Z(B); "
      f"water-filling penalties, kT: " + " ".join(f"{v:.2f}" for v in g_p))
print(f"    with the single-change states only (the weaker form printed by site_allocation_fw.py): at least {wf_a:.6g} nats above ln Z(B)")
lnZ_maj = up0.lnZ()
print(f"    for comparison, the penalty-free MAJORANT has ln Z = {lnZ_maj:.6f}: minorant and majorant are {lnZ_base - lnZ_maj:.6g} nats apart -- the part of "
      f"every bracket of this model class that no allocation can remove (workstream P3's reduction of evaluated terms to pair tables)")
json.dump(dict(seq=seq, bb=bb, m=m, w=w, Gamma_kT=BETA * Gam, lnZ_base=lnZ_base, lnZ_majorant=lnZ_maj, bound_marginals=wf_p, bound_single=wf_a, minus_ln_p=[float(-math.log(max(v, 1e-300))) for v in p],
               g_kT=[float(v) for v in g_p]), open(os.path.join(HERE, f"site_level_bound_{seq}_{bb}_m{m}_w{w}.json"), "w"), indent=1)
print(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")
