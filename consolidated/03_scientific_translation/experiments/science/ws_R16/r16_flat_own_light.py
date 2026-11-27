#!/usr/bin/env python3
"""
r16_flat_own_light.py -- workstream R16, Item 4: the same replication as r16_flat_own.py (exact two-level cost at the
flat instance with the science division's R6 engine and the base bracket's own answer on the zero fibre), for sizes at
which the R6 engine's per-pass records would not fit into 2 GB.  The engine's method Run._run_2LP is COPIED here from
experiments/science/ws_R6/r6lib.py (our own code) with ONE change: of the passes of a level only the last record is
kept (the loop, the arithmetic and the order of operations are unchanged; mutations removed).  At n = 4000 it is
checked against the unmodified engine (same number of evaluations, levels, closing radius).
usage: python3 -B r16_flat_own_light.py <n> <phi | n_o=<int>> [rstar|int]
"""
import os
import sys
import time
import math
from fractions import Fraction

import numpy as np
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ws_R6"))
import r6lib as X            # noqa: E402
import everyn as EV          # noqa: E402
sys.path.pop(0)
import r16lib as R           # noqa: E402

Fr = Fraction
mp.mp.dps = 40


class LightRun(X.Run):
    def _run_2LP(self):          # copied from r6lib.Run._run_2LP; only the storage of the pass records differs
        P, tab = self.P, self.tab
        m = self.n_o
        eta = P.eta
        e = mp.e
        K = P.K
        two_m = tab.two_m
        s0 = mp.mpf(1)
        ell = e ** (self.ln_ell - self.ln_s0)
        Sigma = mp.mpf(0)
        upper_terms = mp.mpf(0)
        self.npasses = 0
        for j in range(0, P.J + 1):
            sj = e ** (j * P.lam)
            M = K
            t = 0
            rec = dict(j=j, passes=[], calls=[0] * (P.L + 1), status=None, Mneg=P.nu * sj / (ell * e ** P.b))
            self.levels.append(rec)
            while True:
                self._ensure_blocks(t)
                N = self._classify(j, t, rec)
                self.npasses += 1
                qF = Fraction(max(N, K), 1) / ((1 - eta) * M)
                if qF > 1:
                    qF = Fraction(1)
                q = mp.mpf(qF.numerator) / qF.denominator
                populated = N >= K
                plow = None
                if populated:
                    plowF = Fraction(N, 1) / ((1 + eta) * M)
                    plow = mp.mpf(plowF.numerator) / plowF.denominator
                    bound = plowF * two_m
                    if bound < 1:
                        bound = Fraction(1)
                    kH = tab.largest_ball_le(bound)
                    ell = max(ell, sj * e ** (-P.b) * plow, sj * e ** (-P.b) * tab.T[kH] / two_m)
                if qF * two_m < 1:
                    tail = mp.mpf(0)
                    r = -1
                else:
                    r = tab.least_ball_ge(qF * two_m)
                    tail = sj * tab.E[r] / two_m if r <= m - 1 else mp.inf
                closed = tail <= P.theta * e ** P.b * ell
                rec["passes"] = [dict(M=M, t=t, N=N, r=r, populated=populated, closed=closed)]      # last pass only
                if closed:
                    Lo = max(ell, Sigma + ((1 - e ** (-P.lam)) * e ** (-P.b) * sj * plow if populated else 0))
                    Up = s0 + upper_terms + tail
                    rec["status"] = "closed"
                    self.status = "closed"
                    self.result = (self.ln_s0 + mp.log(Lo), self.ln_s0 + mp.log(Up))
                    if Lo > Up:
                        self.status = "closed_L>U"
                    return
                if populated:
                    rec["status"] = "populated"
                    Sigma += (1 - e ** (-P.lam)) * e ** (-P.b) * sj * plow
                    upper_terms += (e ** P.lam - 1) * sj * q
                    break
                if M >= rec["Mneg"]:
                    rec["status"] = "negligible"
                    upper_terms += (e ** P.lam - 1) * sj * q
                    break
                if t + 1 > P.m_max:
                    raise X.Abort("M would exceed K 2^m_max")
                M *= 2
                t += 1
        raise X.Abort("level J left")


u = 1.0
n = int(sys.argv[1])
VARIANT = sys.argv[3] if len(sys.argv) > 3 else "rstar"
assert VARIANT in ("rstar", "int")
t0 = time.time()
a = R.a_of(u)
if sys.argv[2].startswith("n_o="):
    n_o = int(sys.argv[2][4:])
    phi = n_o / n
else:
    phi = float(sys.argv[2])
    n_o = R.n_outer(phi, n)
print("# r16_flat_own_light.py started %s; n = %d, n_o = %d, variant %s" % (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), n, n_o, VARIANT), flush=True)
n_i = n - n_o
b = 0.5
xs = [mp.mpf(v) for v in R.geometric_ladder(2 * u * n_i, b, 40)]
tab_o = X.Tables(n_o, u)
tab_i = X.Tables(n_i, u)
P0 = X.Params2LP(n, n_o, u, 0.2, Fr(1, 20), 0.05, 0.05, 2 * math.exp(u) * n_o / 0.05, b, 0.05, xs, [1] * 40, tables=tab_o)
costs = []
lnL = [None]
lnU = [None]
two_d = mp.mpf(2) ** n_i
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
    num = K * (1 << n_i) * eta.denominator
    den = (eta.denominator - eta.numerator) * tab_i.ball[rs]
    M_int = -(-num // den)
    target = Fr(num, (eta.denominator - eta.numerator) * M_int)
    rhat_int = tab_i.least_ball_ge(target) if target >= 1 else None
    assert rhat_int is not None and rhat_int <= rs
    rhat = rs if VARIANT == "rstar" else rhat_int
    lnL.append(float(-mp.log(1 + ef)))
    lnU.append(float(mp.log(1 / (1 - ef) + tab_i.E[rhat] / two_d)))
P = X.Params2LP(n, n_o, u, 0.2, Fr(1, 20), 0.05, 0.05, 2 * math.exp(u) * n_o / 0.05, b, 0.05, xs, costs, tables=tab_o)
print("# tables and constants ready after %.0f s" % (time.time() - t0), flush=True)


class K0FlatOracle:
    def __call__(self, run, idx, l, j):
        return np.full(len(idx), lnL[l]), np.full(len(idx), lnU[l])


inst = X.ClassInstance(n, n_o, u, [0.0], [1], 0.0, [X.S_BOTTOM], 0, name="flat")
rng = np.random.default_rng(0)
run = LightRun(P, inst, K0FlatOracle(), rng).run()
st = [r["status"] for r in run.levels]
na = n * a
lcost = float(mp.log(run.queries()))
last = run.levels[-1]["passes"][-1]
print("variant %s (light engine): n = %d n_o = %d (phi = %.4f): status %s; ln(evaluations)/(n a) = %.4f; ln C_max/(n a) = %.4f;"
      " levels %d (populated %d, negligible %d); passes %d; last sample K 2^%d; closing radius %d (r-dagger %d); returned width"
      " %.4f <= x_out %.4f: %s   [%.0f s]"
      % (VARIANT, n, n_o, n_o / n, run.status, lcost / na, float(mp.log(P.Cmax)) / na, len(st), st.count("populated"),
         st.count("negligible"), run.npasses, last["t"], int(last["r"]), P.rdag, float(run.result[1] - run.result[0]),
         float(P.x_out), float(run.result[1] - run.result[0]) <= float(P.x_out) + 1e-9, time.time() - t0))
print("# finished %s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
print("peak RSS MB", R.peak_rss_mb())
