#!/usr/bin/env python3
"""r29_i5_level_of_nest.py [u] [N]  --  Item 5: ONE LEVEL of their exact nest (z3_nest.py, mode env, base sat) replicated.

The first level family of the nest is  Z_1 = Z[base]:  one level of Lemma Z2 over the base family that saturates the
flat type b_0 = a (certified cost exactly d a at every accuracy >= 1), the outer block chosen by the proxy Pi_0.
THEIR number: zetalib.ZLevelFam(...).costs(d, [x-hat], ln delta)   (their classes, their evaluators, imported in place).
MY number: r29level.level_Z2 (my evaluator from the statement of Theorem 11.56) with my own minimisation of the proxy
    Pi_0(n_o) = max_{lines of W_0} [(d - n_o) B + (1 - sigma) n_o theta_na(y/n_o)] = (d - n_o) a + n_o theta_na(y/n_o),
over ALL blocks 1 <= n_o <= d - d_min + 1, y = x-hat - X_0(d), and my own theta_na.
Then the stated bound of Theorem 11.58e(b) / Proposition Z3 is tested with MY envelope curve W_1 (semi-analytic):
    ln C_max  <=  max_{grid lines of W_1} [d B - sigma x-hat] + ell_0(d, Lambda) + X_0(d) + d_min ln 2 + 2,
    accuracy of the level <= x-hat,   ln(1/delta') + n_i ln 2 <= Lambda + q(d, Lambda)   (q from q2lib, taken as given).
Any discrepancy between my number and theirs, and any violation of the bound, is printed.
Control (must fail): the bound without its error term.
"""
import math
import sys
import time

import numpy as np

import r29lib as R
import r29env as E
import r29level as LV

R.cap_memory()
u = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
N = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
Z = "/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_07cde81/experiments/workstreams/Z"
sys.path.insert(0, Z)
sys.dont_write_bytecode = True
import zetalib as ZL  # noqa: E402   (theirs, read only)

Q2 = ZL.Q2
P = E.CubeF(u)
a = P.a
dm = LV.dmin(u)
env = E.EnvSA(P, 2)
C = ZL.make_chain("env", u, 4)                         # their curves (EnvZ, grid)
ev = Q2.Ev(u, both=True)
st = Q2.Stat()
zfam = ZL.ZLevelFam(ev, ZL.SatFlat(C.b[0]), C.grid(0, N), C.grid(1, N), C.b[1], N, st)
calX = LV.X0(u, N) + 1.0
print("# one level of the nest (mode env, base sat), cube u = %g, horizon N = %d: X = X_0(N) + 1 = %.4f;  a (mine) = %.15f, b_0 (theirs) = %.15f" % (u, N, calX, a, C.b[0]))
my_lines0 = [(i / N, 0.0) for i in range(int(math.floor(N * a + 1e-12)) + 1)] + [(a, 0.0)]
# grid lines of MY W_1 for the type
Bs = [i / N for i in range(int(math.floor(N * env.b[1] + 1e-12)) + 1)]
if Bs[-1] < env.b[1]:
    Bs.append(env.b[1])
W1 = np.array([min(1.0, max(0.0, float(env.W(1, B)))) for B in Bs])
Bs = np.array(Bs)

rows = []
maxdiff = 0.0
nviol = nctrl = ncase = 0
no_diff = 0
t0 = time.time()
print("#      d    x-hat   ln delta | n_o theirs  mine | ln C_max theirs      mine        diff | accuracy mine | type(W_1)+E+   slack | ln(1/d')+n_i ln2 <= Lam+q: slack")
for d in (N, N // 2, N // 5, 137):
    if d <= dm + 2:
        continue
    X0 = LV.X0(u, d)
    for xh in (calX, calX + 3, calX + 0.01 * d, calX + 0.05 * d, calX + 0.2 * d):
        for ldel in (math.log(0.05), -40.0, -0.5 * d):
            y = xh - X0
            # theirs
            lc_th = float(zfam.costs(d, np.array([xh]), ldel)[0])
            no_th = zfam.design(d, y)[0]
            # mine: proxy over all blocks
            best = (math.inf, None)
            for n_o in range(1, d - dm + 2):
                pi = (d - n_o) * a + n_o * P.theta(y / n_o)
                if pi < best[0]:
                    best = (pi, n_o)
            n_o = best[1]
            r = LV.level_Z2(u, d, n_o, y, P.theta, my_lines0, ldel)
            # if the blocks differ (ties, or their candidate list at large d), evaluate mine at their block for the comparison
            if n_o != no_th:
                no_diff += 1
                r_cmp = LV.level_Z2(u, d, no_th, y, P.theta, my_lines0, ldel)
            else:
                r_cmp = r
            diff = r_cmp["lC"] - lc_th
            maxdiff = max(maxdiff, abs(diff))
            Lam = -ldel + d * math.log(2)
            typ = float(np.max(d * Bs - W1 * xh))
            Eplus = LV.ell0(u, d, Lam) + X0 + dm * math.log(2) + 2
            slack = typ + Eplus - r["lC"]
            q = Q2.qSb(ev.cu, d, Lam)
            slack_d = Lam + q - (-r["ldeltap"] + (d - n_o) * math.log(2))
            ncase += 1
            if slack < -1e-9 or r["xout"] > xh + 1e-9 or slack_d < -1e-9:
                nviol += 1
            if r["lC"] - typ > 1e-9:
                nctrl += 1
            if ldel == math.log(0.05) or d == N:
                print("  %6d  %7.2f  %8.1f |  %6d  %6d | %12.6f  %12.6f  %+.1e |  %10.4f  | %10.2f  %8.2f | %8.2f"
                      % (d, xh, ldel, no_th, n_o, lc_th, r_cmp["lC"], diff, r["xout"], typ + Eplus, slack, slack_d))
print("# %d cases: largest |ln C_max mine - theirs| at the same block: %.2e;  cases in which my proxy block differs from theirs: %d" % (ncase, maxdiff, no_diff))
print("# violations of the stated bound (type of W_1 + E+, accuracy, delta'): %d  [must be 0];  control (bound without E+) fails in %d cases  [must be > 0]" % (nviol, nctrl))
print("# their own checks inside these calls: %d checks, %d violations" % (st.total(), len(st.viol)))
print("LEVEL-OF-NEST: %s" % ("replicated; no violation; control fails as it must" if (maxdiff < 1e-8 and nviol == 0 and nctrl > 0 and len(st.viol) == 0) else "CHECK FAILED"))
R.finish("r29_i5_level_of_nest u=%g N=%d" % (u, N))
