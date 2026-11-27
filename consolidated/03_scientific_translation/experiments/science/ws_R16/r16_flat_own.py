#!/usr/bin/env python3
"""
r16_flat_own.py -- workstream R16, Item 4: REPLICATION of the exact two-level cost at the flat instance psi = 0 with
the science division's own literal engine (workstream R6: experiments/science/ws_R6/r6lib.py -- exact integers,
Fractions and 40-digit mpmath; written from the algorithm text before any code of the theory division was read).
Nothing of the theory division is imported.

At psi = 0 every fibre is the zero function, and the base bracket of Proposition K0 on the zero function is
deterministic: every weight is 1, so t^ = 1, A^ = 1 and the bracket is
        [ 1/(1+eta_l) ,  1/(1-eta_l) + 2^{-d} E_{r^}(d) ]       (enumeration: [1, 1]),
r^ the least radius with |B(d, r^)| >= 2^d q_+, q_+ = K_l/((1-eta_l) M_l)  -- Proposition K0's statement.  With
M_l = K_l 2^d/((1-eta_l)|B(d, r*_l)|) (not rounded) this radius is r*_l; with the integer M_l of the proposition it can
be smaller (it is, at the coarsest rungs, where r*_l = d - 1): both variants are run, see VARIANT below.  The R6 engine is run unchanged on the
one-class instance with an oracle that returns this bracket at rung l; the outer design is the one of THY-RES-0013
section 4 (b = 0.5, lam = 0.2, eta = eta' = theta = 1/20, delta = 0.05, nu_1 = 2 e^u n_o/theta, geometric ladder of 40
rungs x_l = x_0 (b/x_0)^{l/40}  [RESOLVED-BY-READING, as in r16lib.py]).

usage: python3 -B r16_flat_own.py <n> <phi> [rstar|int]         (u = 1)
"""
import os
import sys
import time
import math
from fractions import Fraction as Fr

import numpy as np
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ws_R6"))
import r6lib as X            # noqa: E402   science division, workstream R6
import everyn as EV          # noqa: E402   science division, workstream R6 (Proposition K0 on exact tables)
sys.path.pop(0)
import r16lib as R           # noqa: E402   (only for the ladder, n_o and the constant a)

mp.mp.dps = 40
u = 1.0
n = int(sys.argv[1])
phi = float(sys.argv[2])
# variant "rstar": the tail radius of the base bracket is r* (M not rounded up: the convention of the theory division's
# flat evaluator, r8_flat.k0_plan_flat, "M taken without rounding up" [RESOLVED-BY-READING]);
# variant "int": M = ceil(...) an integer, as Proposition K0 states it, and r^ the least radius with |B(d,r^)| >= 2^d q_+.
VARIANT = sys.argv[3] if len(sys.argv) > 3 else "rstar"
assert VARIANT in ("rstar", "int")
t0 = time.time()
print("# r16_flat_own.py started %s; n = %d, phi = %g" % (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), n, phi), flush=True)
a = R.a_of(u)
n_o = R.n_outer(phi, n)
n_i = n - n_o
b = 0.5
xs = [mp.mpf(v) for v in R.geometric_ladder(2 * u * n_i, b, 40)]
tab_o = X.Tables(n_o, u)
tab_i = X.Tables(n_i, u)
theta = Fr(1, 20)
P0 = X.Params2LP(n, n_o, u, 0.2, Fr(1, 20), 0.05, 0.05, 2 * math.exp(u) * n_o / 0.05, b, 0.05, xs, [1] * 40, tables=tab_o)
# base brackets: cost and the deterministic answer on the zero fibre
costs = []
lnL = [None]
lnU = [None]
two_d = mp.mpf(2) ** n_i
nshift = 0
for l in range(1, 41):
    c, info = EV.k0_cost(n_i, u, xs[l], P0.deltap, tab_i)
    costs.append(mp.e ** c)
    if info["mode"] == "enum":
        lnL.append(0.0)
        lnU.append(0.0)
        continue
    eta = Fr(info["eta"])
    ef = mp.mpf(eta.numerator) / eta.denominator
    K, rs = info["K"], info["rstar"]
    # M = ceil(K 2^d/((1-eta)|B(d,r*)|)) as an exact integer; 2^d q_+ = K 2^d/((1-eta) M) as an exact fraction
    num = K * (1 << n_i) * eta.denominator
    den = (eta.denominator - eta.numerator) * tab_i.ball[rs]
    M_int = -(-num // den)
    target = Fr(num, (eta.denominator - eta.numerator) * M_int)
    rhat_int = tab_i.least_ball_ge(target) if target >= 1 else None          # the radius of the proposition, integer M
    assert rhat_int is not None and rhat_int <= rs, (l, rhat_int, rs)
    rhat = rs if VARIANT == "rstar" else rhat_int
    nshift += (rhat_int != rs)
    lnL.append(float(-mp.log(1 + ef)))
    lnU.append(float(mp.log(1 / (1 - ef) + tab_i.E[rhat] / two_d)))
    assert lnU[-1] - lnL[-1] <= float(xs[l]) + 1e-12
print("# variant %s: rungs at which the radius r^ of the proposition (integer M) is below r*: %d of 40" % (VARIANT, nshift), flush=True)
P = X.Params2LP(n, n_o, u, 0.2, Fr(1, 20), 0.05, 0.05, 2 * math.exp(u) * n_o / 0.05, b, 0.05, xs, costs, tables=tab_o)


class K0FlatOracle:
    """the base bracket's own (deterministic) answer on the zero fibre"""

    def __call__(self, run, idx, l, j):
        return np.full(len(idx), lnL[l]), np.full(len(idx), lnU[l])


inst = X.ClassInstance(n, n_o, u, [0.0], [1], 0.0, [X.S_BOTTOM], 0, name="flat")
rng = np.random.default_rng(0)
run = X.Run(P, inst, K0FlatOracle(), rng).run()
st = [r["status"] for r in run.levels]
na = n * a
lcost = float(mp.log(run.queries()))
last = run.levels[-1]["passes"][-1]
print("variant %s: n = %d phi = %g (n_o = %d): status %s; ln(evaluations)/(n a) = %.4f; ln C_max/(n a) = %.4f; levels %d (populated %d,"
      " negligible %d); last sample K 2^%d; closing radius %d (r-dagger %d); returned width %.4f <= x_out %.4f: %s;"
      " rungs used: deepest %d   [%.0f s]"
      % (VARIANT, n, phi, n_o, run.status, lcost / na, float(mp.log(P.Cmax)) / na, len(st), st.count("populated"), st.count("negligible"),
         last["t"], int(last["r"]), P.rdag, float(run.result[1] - run.result[0]), float(P.x_out),
         float(run.result[1] - run.result[0]) <= float(P.x_out) + 1e-9, int(run.rung.max()), time.time() - t0))
print("# finished %s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
print("peak RSS MB", R.peak_rss_mb())
