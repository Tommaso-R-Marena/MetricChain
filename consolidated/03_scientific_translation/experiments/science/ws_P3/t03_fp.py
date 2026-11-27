"""
P3 test 3: floating-point error budget, measured.  g and the descreening tables recomputed with
mpmath at 40 significant digits from the SAME double-precision inputs (coordinates, parameters;
converted exactly), compared with the double-precision values used everywhere.
usage: python3 -B t03_fp.py SEQ BB TAU nstates
"""
import sys, time
import numpy as np
import mpmath as mp
from p3core import GBModel, KAPPA, KCAL, NECK_SCALE, NECK_CUT

mp.mp.dps = 40
seq, bb, tau, nst = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
G = GBModel(seq, bb, tau=tau)
rng = np.random.default_rng(77)
st = np.stack([rng.integers(0, k, nst) for k in G.k], axis=1)
ef = G.energy(st)
M = mp.mpf
orr = [M(float(v)) for v in G.orr]; sr = [M(float(v)) for v in G.sr]; q = [M(float(v)) for v in G.q]
al = [M(float(v)) for v in G.al]; be = [M(float(v)) for v in G.be]; ga = [M(float(v)) for v in G.ga]
off = M(G.off)


def H(p, qq, r):
    U = r + sr[qq]; D = abs(r - sr[qq]); L = max(orr[p], D)
    v = M(0)
    if r + sr[qq] - orr[p] >= 0:
        v = M(1) / 2 * (1 / L - 1 / U + M(1) / 4 * (r - sr[qq] ** 2 / r) * (1 / U ** 2 - 1 / L ** 2) + M(1) / 2 * mp.log(L / U) / r)
    if G.kind == "gbn2":
        cut = orr[p] + off + orr[qq] + off + M(NECK_CUT)
        if cut - r >= 0:
            dr = r - M(float(G.d0[p, qq]))
            v += M(NECK_SCALE) * M(float(G.m0[p, qq])) / (1 + 100 * dr ** 2 + M("0.3e6") * dr ** 6)
    return v


worst = 0.0; worstI = 0.0
t0 = time.time()
for m in range(nst):
    X = G.coords(st[m:m + 1])[0]
    Xm = [[M(float(c)) for c in row] for row in X]
    nat = G.nat
    r = [[None] * nat for _ in range(nat)]
    for p in range(nat):
        for s in range(p + 1, nat):
            d2 = sum((Xm[p][c] - Xm[s][c]) ** 2 for c in range(3))
            r[p][s] = r[s][p] = mp.sqrt(d2)
    I = [sum(H(p, s, r[p][s]) for s in range(nat) if s != p) for p in range(nat)]
    If = G.descreening(st[m:m + 1])[0]
    worstI = max(worstI, max(abs(float(I[p] - M(float(If[p])))) for p in range(nat)))
    ib = []
    for p in range(nat):
        psi = I[p] * orr[p]
        ib.append(1 / orr[p] - mp.tanh(al[p] * psi - be[p] * psi ** 2 + ga[p] * psi ** 3) / (orr[p] + off))
    e = sum(q[p] ** 2 * ib[p] for p in range(nat)) / 2
    for p in range(nat):
        for s in range(p + 1, nat):
            BB = 1 / (ib[p] * ib[s])
            e += q[p] * q[s] / mp.sqrt(r[p][s] ** 2 + BB * mp.exp(-r[p][s] ** 2 / (4 * BB)))
    e = -M(KAPPA) * e / M(KCAL)
    err = abs(float(e - M(float(ef[m]))))
    worst = max(worst, err)
    print(f"   state {m}: g(double) = {ef[m]:.12f}, |double - mpmath(40 digits)| = {err:.2e} kcal/mol  [{time.time() - t0:.0f}s]", flush=True)
print(f"{seq} {bb} tau {tau} ({G.nat} atoms): worst |g(double) - g(mpmath)| = {worst:.2e} kcal/mol (allowance used: 1e-7); "
      f"worst |I_p(tables, double) - I_p(mpmath)| = {worstI:.2e} nm^-1 (allowance used for a table difference: 2e-10)")
