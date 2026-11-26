#!/usr/bin/env python3
"""
r16_flat_own_fast.py -- workstream R16, Item 4: the same replication as r16_flat_own.py (exact two-level cost at the
flat instance with the science division's R6 engine and the base bracket's own answer on the zero fibre), for sizes at
which the pass-by-pass engine would need millions of passes (n = 16 000: about 2.6 million; over the 20-minute limit).
The engine's method Run._run_2LP is COPIED here from experiments/science/ws_R6/r6lib.py (our own code) with TWO changes:
 (1) of the passes of a level only the last record is kept;
 (2) an EXACT shortcut at the levels at which no point can be high (ln s_j >= b: every lower end is <= W = 1 <= s_j e^{-b}).
     There N = 0 at every pass, the running bound does not change, q = min{1, 1/((1-eta) 2^t)} decreases with the pass
     index t, hence the closing radius and the tail are nonincreasing in t: the closure test is monotone in t, and so is
     the negligibility test M >= M_j^neg.  The level therefore ends at t* = min(t_close, t_neg); t_close is found by
     bisection with the same exact arithmetic as the test itself, t_neg by exact comparison.  The engine then runs its
     ordinary pass at t* (blocks drawn, all points of blocks <= t* classified and charged, the test evaluated) and the
     script asserts that this pass ends the level.  Classification at t* refines exactly the points that the passes
     0..t* would have refined (a point is called at most once per rung), so the number of evaluations is the same.
Checked against the unmodified engine at (4000, 0.5) and (8000, 0.59): same number of evaluations, levels, populated and
negligible levels, last sample, closing radius and width.
usage: python3 -B r16_flat_own_fast.py <n> <phi | n_o=<int>> [rstar|int]
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


class FastRun(X.Run):
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
        self.nshort = 0
        self.t_close_prev = 0
        for j in range(0, P.J + 1):
            sj = e ** (j * P.lam)
            M = K
            t = 0
            rec = dict(j=j, passes=[], calls=[0] * (P.L + 1), status=None, Mneg=P.nu * sj / (ell * e ** P.b))
            self.levels.append(rec)
            jumped = False
            if self.ln_s(j) - self.b_f >= 0.0:
                # exact shortcut (see the header): the last pass index of this level
                def closes(tt):
                    qq = Fraction(K, 1) / ((1 - eta) * (K << tt))
                    if qq > 1:
                        qq = Fraction(1)
                    if qq * two_m < 1:
                        return True
                    rr = tab.least_ball_ge(qq * two_m)
                    if rr > m - 1:
                        return False
                    return sj * tab.E[rr] / two_m <= P.theta * e ** P.b * ell
                t_neg = 0
                while (K << t_neg) < rec["Mneg"]:
                    t_neg += 1
                lo_t = self.t_close_prev          # t_close is nondecreasing in j at these levels (s_j grows, ell is constant)
                if closes(min(lo_t, t_neg)):
                    # make sure lo_t is really the least closing index: step down while the previous one closes too
                    tc = min(lo_t, t_neg)
                    while tc > 0 and closes(tc - 1):
                        tc -= 1
                    t_close = tc
                elif closes(t_neg):
                    a_, b_ = min(lo_t, t_neg), t_neg       # closes(b_) and not closes(a_)
                    while b_ - a_ > 1:
                        mid = (a_ + b_) // 2
                        if closes(mid):
                            b_ = mid
                        else:
                            a_ = mid
                    t_close = b_
                else:
                    t_close = None                           # no closing pass up to t_neg: the level is left as negligible
                self.t_close_prev = t_close if t_close is not None else t_neg
                t = t_close if t_close is not None else t_neg
                assert t <= P.m_max
                M = K << t
                jumped = True
                self.nshort += 1
            while True:
                self._ensure_blocks(t)
                N = self._classify(j, t, rec)
                self.npasses += 1
                assert not (jumped and N != 0), "a point is high at a level of the shortcut"
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
                assert not jumped, "the shortcut pass did not end its level"
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
print("# r16_flat_own_fast.py started %s; n = %d, n_o = %d, variant %s" % (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), n, n_o, VARIANT), flush=True)
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
run = FastRun(P, inst, K0FlatOracle(), rng).run()
st = [r["status"] for r in run.levels]
na = n * a
lcost = float(mp.log(run.queries()))
last = run.levels[-1]["passes"][-1]
print("variant %s (engine with the exact shortcut): n = %d n_o = %d (phi = %.4f): status %s; ln(evaluations)/(n a) = %.4f; ln C_max/(n a) = %.4f;"
      " levels %d (populated %d, negligible %d); passes run %d (levels ended by the shortcut: %d); last sample K 2^%d; closing radius %d (r-dagger %d); returned width"
      " %.4f <= x_out %.4f: %s   [%.0f s]"
      % (VARIANT, n, n_o, n_o / n, run.status, lcost / na, float(mp.log(P.Cmax)) / na, len(st), st.count("populated"),
         st.count("negligible"), run.npasses, run.nshort, last["t"], int(last["r"]), P.rdag, float(run.result[1] - run.result[0]),
         float(P.x_out), float(run.result[1] - run.result[0]) <= float(P.x_out) + 1e-9, time.time() - t0))
print("# finished %s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
print("peak RSS MB", R.peak_rss_mb())
