#!/usr/bin/env python3
"""Workstream Q -- the nested design of Q_REPORT.md section 4 ("epoch schedule") and its EXACT certified cost.

A family is an object with
    costs(d, xs, ld)        ln of the certified cost bound of its procedure for dimension d, accuracies xs (array),
                            failure probability e^ld  (the bound holds in every run: Theorem 11.56 / Proposition K0)
    B, sigma, R             the majorant  d B - sigma min(x, R d)  of Q_REPORT (R = inf, sigma = 0 for a flat bound)
    Ebound(d, x, Lam)       the error term proved in Q_REPORT:  costs <= d B - sigma min(x, R d) + Ebound
                            whenever ln(1/delta) + d ln 2 <= Lam
and every evaluation is checked against that inequality (`CHECK`), so a run of this file is a test of the whole
induction on every node it visits.

Families:  BaseFam (Proposition K0 or enumeration), Synthetic (cost equal to a majorant: the test of one step),
           SLevel (slope step, Proposition Q6), DLevel (drop, Proposition Q7), build_G (the family G_M).
All constants of a level come from qlib.level_consts, i.e. from the formulas of K_REPORT 2.2 with the referee's
tables; nothing about a level is approximated.
"""
import math

import numpy as np

import qlib as Q

LN2 = Q.LN2
INF = float('inf')


class Check:
    """collects the comparison  exact <= majorant + Ebound  over all nodes"""

    def __init__(self):
        self.n = 0
        self.viol = 0
        self.minslack = INF
        self.worst = None
        self.by = {}

    def add(self, name, exact, bound, tag=None):
        self.n += 1
        slack = bound - exact
        if slack < -1e-9:
            self.viol += 1
        if slack < self.minslack:
            self.minslack = slack
            self.worst = (name, tag, exact, bound)
        s = self.by.setdefault(name, [0, INF, 0])
        s[0] += 1
        s[1] = min(s[1], slack)
        if slack < -1e-9:
            s[2] += 1


CHECK = Check()


def reset_check():
    global CHECK
    CHECK = Check()
    return CHECK


class Family:
    name = '?'
    B = 0.0
    sigma = 0.0
    R = INF

    def majorant(self, d, x):
        if self.sigma == 0.0:
            return d * self.B
        return d * self.B - self.sigma * min(x, self.R * d)

    def _check(self, d, xs, ld, vals):
        Lam = -ld + d * LN2
        for x, v in zip(xs, vals):
            CHECK.add(self.name, float(v), self.majorant(d, float(x)) + self.Ebound(d, float(x), Lam), (d, float(x), ld))


class BaseFam(Family):
    """G_0: the two-sample bracket of Proposition K0 (design of K_REPORT 3.2) or enumeration, whichever is cheaper"""
    name = 'base'

    def __init__(self, cube):
        self.cube = cube
        self.B = cube.a
        self.ncalls = 0

    def Ebound(self, d, x, Lam):
        return Q.E_base(self.cube, d, x, Lam)

    def costs(self, d, xs, ld):
        xs = np.asarray(xs, dtype=float)
        bt = Q.BaseTable(self.cube.u, d)
        out = bt.costs(xs, ld)
        self.ncalls += xs.size
        # check a few (all would be slow in pure python): the two ends and the middle
        idx = sorted(set([0, xs.size // 2, xs.size - 1]))
        self._check(d, xs[idx], ld, out[idx])
        return out


class Synthetic(Family):
    """a family whose cost EQUALS the majorant d B - sigma min(x, R d) + E0: the worst case allowed by the hypothesis"""
    name = 'synthetic'

    def __init__(self, B, sigma, R, E0=0.0):
        self.B, self.sigma, self.R, self.E0 = B, sigma, R, E0

    def Ebound(self, d, x, Lam):
        return self.E0

    def costs(self, d, xs, ld):
        xs = np.asarray(xs, dtype=float)
        if self.sigma == 0.0:
            return np.full(xs.shape, d * self.B + self.E0)
        return d * self.B - self.sigma * np.minimum(xs, self.R * d) + self.E0


class SLevel(Family):
    """slope step S[inner] (Proposition Q6): Algorithm 2L+ with lam = 1, eta = 1/2, eta' = 1, nu_1 = 1, tolerance 1,
    theta = e^{x-1} - (3e+1) - (2p_u)^n/e (accuracy exactly x), outer block n_o = floor((x - 1 - c_log(n))/h),
    ladder 2u n_i > min(ceil(x), ceil(2u n_i) - 1) > ... > 2 > 1.  x is first lowered to R' n; below X0(n): pass-through."""
    name = 'S'

    def __init__(self, cube, inner, B, minrule=True):
        self.cube, self.inner = cube, inner
        assert inner.sigma <= 1 + 1e-12 and abs(inner.B - B) < 1e-12
        self.B = B
        self.sigma = inner.sigma + B / cube.h - 1
        self.R = cube.h if inner.R == INF else inner.R * cube.h / (cube.h + inner.R)
        self.memo = {}
        self.info = {}
        self.nconstruct = 0
        self.nwin = 0
        self.minrule = minrule

    def Ebound(self, d, x, Lam):
        cu = self.cube
        return self.inner.Ebound(d, min(x, 1.0), Lam + Q.qS(cu, d, Lam)) + Q.cS(cu, d, Lam, self.B)

    def costs(self, d, xs, ld):
        """the cheaper (by certified cost) of the level built for min(x, R'd) and of the inner procedure itself"""
        xs = np.asarray(xs, dtype=float)
        xh = np.minimum(xs, self.R * d)
        X0 = Q.X0(self.cube, d)
        out = self.inner.costs(d, xs, ld) if self.minrule else np.full(xs.shape, INF)
        pas = xh < X0
        if np.any(pas) and not self.minrule:
            out[pas] = self.inner.costs(d, xs[pas], ld)
        Lam = -ld + d * LN2
        for i in np.nonzero(~pas)[0]:
            v = self.construct(d, float(xh[i]), ld)
            # Proposition Q6 for the level as built
            CHECK.add('S as built', v, self.majorant(d, float(xs[i])) + self.Ebound(d, float(xs[i]), Lam), (d, float(xh[i]), ld))
            if v < out[i]:
                out[i] = v
                self.nwin += 1
        self._check(d, xs, ld, out)
        return out

    def construct(self, d, xh, ld):
        key = (d, xh, round(ld, 9))
        if key in self.memo:
            return self.memo[key]
        cu = self.cube
        u, h = cu.u, cu.h
        n_o = int(math.floor((xh - 1 - Q.c_log(cu, d)) / h))
        assert 1 <= n_o <= d - 1
        n_i = d - n_o
        ltheta = (xh - 1) + math.log1p(-(3 * math.e + 1 + (2 * cu.p) ** d / math.e) * math.exp(-(xh - 1)))
        x1 = min(int(math.ceil(xh)), int(math.ceil(2 * u * n_i)) - 1)
        assert x1 >= 1 and x1 < 2 * u * n_i
        L = x1
        c = Q.level_consts(u, d, n_o, 1.0, 0.5, 1.0, ltheta, 1.0, 1.0, ld, L)
        assert abs(c['xout'] - xh) < 1e-9, (c['xout'], xh)
        xs = np.concatenate(([2 * u * n_i], np.arange(x1, 0, -1, dtype=float)))
        lc = self.inner.costs(n_i, xs[1:], c['ldeltap'])
        lC, terms = Q.level_cmax(c, xs, np.concatenate(([0.0], lc)))
        # Lemma Q4 on this node: ln(1/pi_dag) <= n_o h + ln(n_o + 1)
        CHECK.add('S: Lemma Q4', -c['lpidag'], n_o * h + math.log(n_o + 1), (d, xh))
        self.nconstruct += 1
        self.memo[key] = lC
        self.info[key] = dict(n_o=n_o, n_i=n_i, L=L, K=c['K'], J=c['J'], rdag=c['rdag'], lMbar=c['lMbar'], ldeltap=c['ldeltap'],
                              argmax=int(np.argmax(terms)), P_cnt=c['P_cnt'], P_M=c['P_M'], lpidag=c['lpidag'])
        return lC


class DLevel(Family):
    """drop D[inner; c, alpha, beta] (Proposition Q7): Algorithm 2L+ with lam = eta = eta' = theta = c,
    nu_1 = 2 e^u n_o/c, tolerance beta = alpha - w(c), outer block n_o = floor(phi n - shift), phi = R/(a + R),
    ladder 2u n_i > ceil(R n_i) > ... > 1 > beta.  It ignores the accuracy asked for (>= alpha) and delivers alpha.
    Candidates (the cheapest by certified cost is used): the level with shift = shift_D(n) (the one of the proof),
    the level without shift, and the inner procedure at accuracy alpha (pass-through)."""
    name = 'D'

    def __init__(self, cube, inner, c, alpha, beta, R, phi, minrule=True):
        self.cube, self.inner = cube, inner
        assert inner.sigma >= 1 - 1e-12 and inner.R >= R - 1e-15
        self.c, self.alpha, self.beta, self.Rin, self.phi = c, alpha, beta, R, phi
        self.Bin = inner.B
        self.B = (1 - phi) * inner.B
        self.sigma = 0.0
        self.R = INF
        self.memo = {}
        self.info = {}
        self.minrule = minrule
        self.wins = dict(shift=0, noshift=0, passthrough=0)

    def Ebound(self, d, x, Lam):
        cu = self.cube
        return self.inner.Ebound(d, self.beta, Lam + Q.qD(cu, d, Lam, self.c)) + Q.cD(cu, d, Lam, self.c, self.phi, self.Rin, self.Bin)

    def Ebound_noshift(self, d, Lam):
        cu = self.cube
        c = self.c
        cD0 = self.Bin * (1 + self.phi * Q.n_Dp(cu, c)) + Q.cpi_bar(cu, int(math.floor(self.phi * d)), c) + math.log(d + 4) + 1 \
            + Q.PcntD(cu, d, Lam, c)
        return self.inner.Ebound(d, self.beta, Lam + Q.qD(cu, d, Lam, c)) + cD0

    def costs(self, d, xs, ld):
        xs = np.asarray(xs, dtype=float)
        assert np.all(xs >= self.alpha - 1e-12)
        v = self.best(d, ld)
        out = np.full(xs.shape, v)
        self._check(d, xs[:1], ld, out[:1])
        return out

    def best(self, d, ld):
        key = (d, round(ld, 9))
        if key in self.memo:
            return self.memo[key]
        cu = self.cube
        c = self.c
        Lam = -ld + d * LN2
        sh = Q.shift_D(cu, d, c, self.phi, self.Rin)
        cands = {}
        ok_dim = d >= Q.n_Dp(cu, c)
        n_o = int(math.floor(self.phi * d - sh))
        if ok_dim and n_o >= 1:
            v, inf = self.build(d, n_o, ld)
            inf['shift'] = sh
            cands['shift'] = (v, inf)
            CHECK.add('D as built (shift)', v, d * self.B + self.Ebound(d, self.alpha, Lam), (d, ld))
        n_o0 = int(math.floor(self.phi * d))
        if self.minrule and ok_dim and n_o0 >= 1:
            v, inf = self.build(d, n_o0, ld)
            inf['shift'] = 0.0
            cands['noshift'] = (v, inf)
            CHECK.add('D as built (no shift)', v, d * self.B + self.Ebound_noshift(d, Lam), (d, ld))
        if self.minrule or not cands:
            v = float(self.inner.costs(d, np.array([self.alpha]), ld)[0])
            cands['passthrough'] = (v, dict())
        win = min(cands, key=lambda kk: cands[kk][0])
        self.wins[win] += 1
        v, inf = cands[win]
        inf = dict(inf)
        inf['winner'] = win
        inf['cands'] = {kk: cands[kk][0] for kk in cands}
        self.memo[key] = v
        self.info[key] = inf
        return v

    def build(self, d, n_o, ld):
        cu = self.cube
        u = cu.u
        c = self.c
        n_i = d - n_o
        x1 = int(math.ceil(self.Rin * n_i))
        assert 1 <= x1 < 2 * u * n_i
        xs = np.concatenate(([2 * u * n_i], np.arange(x1, 0, -1, dtype=float), [self.beta]))
        L = x1 + 1
        k = Q.level_consts(u, d, n_o, c, c, c, math.log(c), 2 * math.exp(u) * n_o / c, self.beta, ld, L)
        assert k['xout'] <= self.alpha + 1e-12, (k['xout'], self.alpha)
        lc = self.inner.costs(n_i, xs[1:], k['ldeltap'])
        lC, terms = Q.level_cmax(k, xs, np.concatenate(([0.0], lc)))
        # Lemma Q3 on this node: ln(1/pi_dag) <= n_o a + cpi_bar(n_o, c)
        CHECK.add('D: Lemma Q3', -k['lpidag'], n_o * cu.a + Q.cpi_bar(cu, n_o, c), (d,))
        am = int(np.argmax(terms))
        inf = dict(n_o=n_o, n_i=n_i, L=L, K=k['K'], J=k['J'], rdag=k['rdag'], lMbar=k['lMbar'], ldeltap=k['ldeltap'],
                   argmax=am, x_argmax=(float(xs[am]) if am >= 1 else None), P_cnt=k['P_cnt'], P_M=k['P_M'], lpidag=k['lpidag'],
                   terms=(float(terms[0]), float(terms[1]), float(np.max(terms[2:]))))
        return lC, inf


def build_G(cube, M, eps, seq=None, minrule=True):
    """the family G_M of Q_REPORT section 4 for the target accuracy eps; returns (family, list of all levels from the
    base up, the accuracies alpha_m).  minrule=False: every level is the one of the proof and nothing else (no choice
    by certified cost; pass-through only where the proof prescribes it)."""
    if seq is None:
        seq = Q.epoch_seq(cube, max(M, 1))
    cs, alpha = Q.acc_schedule(eps, M)
    fam = BaseFam(cube)
    levels = [fam]
    for m in range(M):
        for j in range(seq['J'][m]):
            fam = SLevel(cube, fam, seq['B'][m], minrule)
            levels.append(fam)
        assert fam.sigma >= 1 - 1e-12 and abs(fam.R - seq['R'][m]) < 1e-12
        fam = DLevel(cube, fam, cs[m], alpha[m + 1], alpha[m], seq['R'][m], seq['phi'][m], minrule)
        assert abs(fam.B - seq['B'][m + 1]) < 1e-12
        levels.append(fam)
    return fam, levels, alpha
