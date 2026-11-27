import math, random, sys
from fractions import Fraction as Fr
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "rerun_copy" / "src")); sys.path.insert(0, str(HERE))
import numpy as np, mpmath as mp
import r18_mean as mine, r18_xcheck as X
from metricchain_eng.twolevel import meanrun as their
from metricchain_eng.twolevel.alg2l import Params, constants, inner_costs, lC_max
from metricchain_eng.twolevel.tables import CubeTables, LN2
rng = random.Random(1)
found = 0
while found < 2:
    dd = X.draw_design(rng)
    if dd is None: continue
    u, n, n_o = dd["u"], dd["n"], dd["n_o"]; n_i = n - n_o; xs = dd["xs"]
    P = Params(n=n, n_o=n_o, u=float(u), lam=float(dd["lam"]), eta=float(dd["eta"]), etap=dd["etap"], theta=dd["theta"], nu1=dd["nu1"], b=float(dd["b"]), delta=dd["delta"], xs=tuple(float(x) for x in xs))
    tabs = CubeTables(n_o, float(u)); C = constants(P, tabs); lC = inner_costs(P, C)
    D = mine.Design(n, n_o, u, dd["lam"], dd["eta"], dd["etap"], dd["theta"], dd["nu1"], dd["b"], dd["delta"], xs, lC=[None] + [float(x) for x in lC[1:]])
    Lam1 = math.log(2 / (1 + math.exp(-float(u))))
    for _ in range(2):
        F = X.draw_profile(rng, u, n_o); d0 = rng.randint(0, n_o); psi0 = F[d0]
        c_in = Fr(rng.randint(math.ceil(-n_i * Lam1 * 64), math.floor(n_i * (float(u) - Lam1) * 64)), 64); t0 = u * n_i + c_in
        Ff = [float(x) for x in F]
        for orc in ("bottom", "top"):
            pos = mine.uniform_positions(D, orc)
            atoms, den = mine.radial_atoms(D, F, c_in, pos=pos)
            Rm = mine.mean_run(D, atoms, den, psi0)
            Rt = X.their_run(P, tabs, C, lC, Ff, float(c_in), float(psi0), float(t0), orc)
            lM_m = np.array([math.log(D.K) + mm * math.log(2) for mm in Rm.ms])
            if Rm.j_stop == Rt.j_stop and np.max(np.abs(lM_m - Rt.lM)) > 1e-9 and found < 2:
                found += 1
                bad = np.flatnonzero(np.abs(lM_m - Rt.lM) > 1e-9)
                print(f"design n={n} n_o={n_o} u={u} lam={dd['lam']} eta={dd['eta']} etap={dd['etap']} theta={dd['theta']} nu1={dd['nu1']} b={dd['b']} L={D.L} K={D.K} m_max={D.m_max} {orc}")
                print(" levels differing:", bad[:10], "count", len(bad), "j_stop", Rm.j_stop)
                for j in bad[:3]:
                    mt = round((Rt.lM[j] - math.log(D.K)) / LN2)
                    print(f"  level {j}: mine m={Rm.ms[j]} kind={Rm.kinds[j]} P(HIGH)={Rm.high_num[j]/Rm.den:.6e} 2^m*P={(2**Rm.ms[j])*Rm.high_num[j]/Rm.den:.6f} ; theirs m={mt} kind={Rt.kind[j]} lq={Rt.lq[j]:.6f} lMneg-lK={(Rt.lMneg[j]-C.lK)/LN2:.6f}")
                    # neighbours
                    for jj in (j-1, j+1):
                        if 0 <= jj <= Rm.j_stop:
                            mt2 = round((Rt.lM[jj] - math.log(D.K)) / LN2)
                            print(f"     level {jj}: mine m={Rm.ms[jj]} kind={Rm.kinds[jj]} P={Rm.high_num[jj]/Rm.den:.6e}; theirs m={mt2} kind={Rt.kind[jj]} lMneg-lK={(Rt.lMneg[jj]-C.lK)/LN2:.6f}")
