"""
P6 diagnostic (NOT a certificate): where does the width of the deterministic bracket come from?
For one instance, order and band: ln Z(m_-) - ln Z(m_+) of models built with
  (0) no penalty at all (P3's band reductions of the evaluated terms only),
  (1) the tail penalty only (no floating-point allowance),
  (2) the full certified penalty,
for the site form and the banded pair form.  Only (2) is a certified sandwich.
usage: python3 -B p6_07_decompose.py SEQ BB TAU m w
"""
import sys, time, math
import numpy as np
import p6lib as L
seq, bb, tau, m, w = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
t0 = time.time()
G, c0, h, J, x0, E0 = L.setup(seq, bb, tau)
n, k = G.ns, G.k
sup = L.EnvelopeSup(G); GF = L.GFBound2(G, x0, sup, K=m)
Gam, S, Gp, src = L.load_or_compute_pair_sums(G, GF, x0, seq, bb, tau, "gbn2", m, w=w)
M = m - 1
d, nball, srcb = L.ball_terms(G, x0, M, seq, bb, tau, verbose=False)
phi1, psi1, psi2 = L.fp_tables(n, k, x0, M)
z1 = np.zeros(n); z2 = np.zeros((n, n))
rows = []
def width(gs, g2, const):
    lo, up = L.build_models(k, x0, c0, h, J, d, w, M, gs, g2, const=const)
    return lo.lnZ() - up.lnZ()
w0 = width(z1, z2, 0.0)
S_tail = np.maximum(S, 0.0) / m * L.RND
gsB_tail, g2B_tail = L.banded_pair_form(n, m, w, S, Gp, z1, z2, 5e-9 * Gam)
gsB, g2B = L.banded_pair_form(n, m, w, S, Gp, psi1, psi2, 5e-9 * Gam)
print(f"=== decomposition (diagnostic): {seq} on {bb}, tau {tau}, m = {m}, band {w}; Gamma_{m} = {Gam:.4e} kcal/mol; ball {nball}")
print(f"    (0) no penalty, band reductions of the evaluated terms only: width {w0:.6f} nats")
print(f"    site form:        (1) tail only {width(S_tail, z2, 0.0):.6f}   (2) certified (with P3's site allocation of the fp allowance) {width(L.site_form(n, m, S, phi1), z2, L.EPS_G):.6f}")
print(f"    banded pair form: (1) tail only {width(gsB_tail, g2B_tail, 0.0):.6f}   (2) certified (pair allocation of the fp allowance) {width(gsB, g2B, L.EPS_G):.6f}"
      f"   [(2') banded pair tail with P3's SITE allocation of the fp allowance: {width(gsB_tail + phi1, g2B_tail, L.EPS_G):.6f}]")
print(f"    fp allowance: per changed site (P3's allocation) {phi1.max():.3e}; per changed pair (pair allocation) {psi2.max():.3e}; per changed site in the pair allocation {psi1.max():.1e} kcal/mol")
print(f"DONE p6_07_decompose {seq} {bb} {tau} m={m} w={w} [{time.time() - t0:.0f}s]")
