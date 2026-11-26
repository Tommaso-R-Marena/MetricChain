#!/usr/bin/env python3
"""r10_nest_M1.py -- referee: the nested design of Theorem A with M = 1, EXACTLY, with own code (no caching tricks):

    G_1 = T[ D'[ S[ T[B; 1, m_0] ]; phi_0, X_0 ]; eps^, m_1 ]        (J_0 = 1 slope step in epoch 0 for u = 1/2, 1, 2)

Theorem 11.56 is applied level by level with the exact constants (each level with its own failure probability), the
real base brackets inside.  Two variants: "min" (the families as defined: S and D' are the cheaper of the level and the
pass-through) and "proof" (the level whenever it is built).  On EVERY node the inequality of the induction
    cost <= d B - sigma min(x, R d) + E(d, x; ln(1/delta) + d ln 2)
with the error functions of sections 2-5 is checked; the top is compared with n B_1 + E'_1 of (A.1).
usage: python3 r10_nest_M1.py u n [u n ...]"""
import math, sys, time
sys.dont_write_bytecode = True
import numpy as np
import rlib
from rlib import LN2, INF
import r03_formula as F

EPS = 0.8715
LD = math.log(0.05)


class Nest:
    def __init__(self, u, n, variant):
        self.cu = cu = rlib.Cube(u)
        self.u, self.n, self.variant = u, n, variant
        seq = self.seq = rlib.epochs(cu, 3)
        assert seq['J'][0] == 1
        a, h = cu.a, cu.h
        self.sig1 = 1.0 / seq['d'][0]                       # slope after the slope step (>= 1)
        self.phi0, self.R0, self.B1 = seq['phi'][0], seq['R'][0], seq['B'][1]
        self.X0D = rlib.X_D(cu, n, self.phi0)               # accuracy of the drop
        self.XB = rlib.X_B(cu, n)
        epsh = min(EPS, 1.0)
        Lam = -LD + n * LN2
        m1 = rlib.Chain.design_m(cu, n, self.B1, self.X0D, epsh, Lam)
        self.ch1 = rlib.Chain(cu, n, self.B1, self.X0D, epsh, m1)
        Lam += self.ch1.j(n) * self.ch1.qT(n, Lam + n * self.B1)
        Lam += rlib.q_b(cu, n, Lam)
        Lam += rlib.q_b(cu, n, Lam)
        m0 = rlib.Chain.design_m(cu, n, a, self.XB, 1.0, Lam)
        self.ch0 = rlib.Chain(cu, n, a, self.XB, 1.0, m0)
        self.Bt = max(1.0, self.R0 / (2 * u * a)) * seq['B'][0]
        self.nodes = dict(base=0, chain0=0, S=0, D=0, chain1=0)
        self.minslack = dict(base=INF, chain0=INF, S=INF, D=INF, chain1=INF)
        self.viol = 0
        self.built = dict(S=0, D=0)

    # ---------------- error functions of the induction
    def E_T0(self, d, Lam):
        return self.ch0.E_T(d, Lam, lambda dd, x, L: rlib.E_frakB(self.cu, dd, L))

    def E_S(self, d, Lam):
        cu = self.cu
        return self.E_T0(d, Lam + rlib.q_b(cu, d, Lam)) + self.sig1 * (1 + rlib.c_log(cu, d) + cu.h) + rlib.ell0_b(cu, d, Lam)

    def E_D(self, d, Lam):
        cu = self.cu
        return self.E_S(d, Lam + rlib.q_b(cu, d, Lam)) + self.Bt + rlib.ell0_b(cu, d, Lam)

    def E_T1(self, d, Lam):
        return self.ch1.E_T(d, Lam, lambda dd, x, L: self.E_D(dd, L))

    def note(self, kind, slack):
        self.nodes[kind] += 1
        if slack < self.minslack[kind]:
            self.minslack[kind] = slack
        if slack < -1e-9:
            self.viol += 1

    # ---------------- exact costs
    def base(self, d, ld):
        """the base family B at the accuracy X_B(n)"""
        t, _ = rlib.base_lcost(self.cu, d, self.XB, ld)
        self.note('base', d * self.cu.a + rlib.E_frakB(self.cu, d, -ld + d * LN2) - t)
        return t

    def chain(self, ch, d, ld, coarse, kind, Efn):
        cu, u, m, c = self.cu, self.u, ch.m, ch.c
        recs = []
        dd, l = d, ld
        while dd >= ch.d0:
            a_d = ch.alow + ch.j(dd) * ch.w
            lev = rlib.Level(u, dd, m, c, c, c, math.log(c), 2 * math.exp(u) * m / c, a_d - ch.w, l, 2, tab=rlib.tables(u, m, c))
            if lev.x_out > a_d + 1e-12:
                self.viol += 1
            recs.append((dd, l, lev, a_d))
            dd, l = dd - m, lev.ldp
        t, _ = rlib.base_lcost(cu, dd, ch.alow, l)
        self.note(kind, dd * ch.Bp + Efn(dd, -l + dd * LN2) - t)
        for (dd, l, lev, a_d) in reversed(recs):
            c1 = coarse(dd - m, lev.ldp)
            t = lev.lcmax([ch.calX, a_d - ch.w], [c1, t])
            self.note(kind, dd * ch.Bp + Efn(dd, -l + dd * LN2) - t)
        return t

    def chain0(self, d, ld):
        return self.chain(self.ch0, d, ld, self.base, 'chain0', self.E_T0)

    def S(self, d, x, ld):
        """the slope step S[G_0] of Proposition Q6 (inner type (a, 0, inf)), at accuracy x >= 1"""
        cu, u, h, a = self.cu, self.u, self.cu.h, self.cu.a
        xh = min(x, h * d)
        X0 = 1 + rlib.c_log(cu, d) + h
        lam = -ld + d * LN2
        typ = d * a - self.sig1 * xh + self.E_S(d, lam)
        if xh < X0:
            t = self.chain0(d, ld)
        else:
            n_o = math.floor((xh - 1 - rlib.c_log(cu, d)) / h + 1e-12)
            n_i = d - n_o
            lth = rlib.ltheta_for_accuracy(cu, d, xh, 1.0)
            x1 = min(math.ceil(xh - 1e-12), math.ceil(2 * u * n_i - 1e-12) - 1)
            xs = [float(x1 - i) for i in range(x1)]
            lev = rlib.Level(u, d, n_o, 1.0, 0.5, 1.0, lth, 1.0, 1.0, ld, len(xs))
            if abs(lev.x_out - xh) > 1e-9:
                self.viol += 1
            c0 = self.chain0(n_i, lev.ldp)
            t = lev.lcmax(xs, [c0] * len(xs))
            self.built['S'] += 1
            self.note('S', typ - t)                       # the level itself obeys the bound of Q6 / U1
            if self.variant == 'min':
                t = min(t, self.chain0(d, ld))
        self.note('S', typ - t)
        return t

    def D(self, d, ld):
        """the drop D'[S[G_0]; phi_0, X_0] at (d, delta); delivers the accuracy X_0"""
        cu, u = self.cu, self.u
        n_o = math.floor(self.phi0 * d + 1e-12)
        lam = -ld + d * LN2
        typ = d * self.B1 + self.E_D(d, lam)
        if n_o >= 1 and 2 * u * (d - n_o) > 1:
            n_i = d - n_o
            lth = rlib.ltheta_for_accuracy(cu, d, self.X0D, 1.0)
            xs = rlib.ladder_U(cu, n_i, 1.0, self.R0 * n_i)
            lev = rlib.Level(u, d, n_o, 1.0, 0.5, 1.0, lth, 1.0, 1.0, ld, len(xs))
            if abs(lev.x_out - self.X0D) > 1e-9:
                self.viol += 1
            lc = [self.S(n_i, x, lev.ldp) for x in xs]
            t = lev.lcmax(xs, lc)
            self.built['D'] += 1
            self.note('D', typ - t)
            if self.variant == 'min':
                t = min(t, self.S(d, self.X0D, ld))
        else:
            t = self.S(d, self.X0D, ld)
        self.note('D', typ - t)
        return t

    def top(self):
        return self.chain(self.ch1, self.n, LD, self.D, 'chain1', self.E_T1)


def main():
    args = sys.argv[1:] or ['1', '2000']
    rep = {(1.0, 1000): "1.995 / 1.887 / 4.475", (1.0, 2000): "1.609 / 1.521 / 2.763", (1.0, 4000): "1.263 / 1.196 / 1.844",
           (1.0, 8000): "1.015 / 0.989 / 1.354", (2.0, 2000): "1.106 / 1.075 / 1.454", (2.0, 4000): "0.922 / 0.902 / 1.135"}
    for i in range(0, len(args), 2):
        u, n = float(args[i]), int(args[i + 1])
        out = {}
        for variant in ('proof', 'min'):
            t0 = time.time()
            N = Nest(u, n, variant)
            t = N.top()
            cu = N.cu
            E = F.E_A1(cu, n, EPS, -LD, 1, rlib.epochs(cu, 45))
            bound = n * N.B1 + E
            out[variant] = t / (n * cu.a)
            print("u = %.1f n = %d  %-5s: ln cost/(n a) = %.4f   bound of Theorem A (M = 1) = %.4f   blocks m_1 = %d (%d levels), m_0 = %d"
                  % (u, n, variant, t / (n * cu.a), bound / (n * cu.a), N.ch1.m, N.ch1.j(n), N.ch0.m))
            print("      node checks: %s  (levels built: %s);  violations %d;  least slack of the induction by family: %s   [%.0f s]"
                  % (N.nodes, N.built, N.viol, {k: round(v, 1) for k, v in N.minslack.items()}, time.time() - t0), flush=True)
            if t > bound + 1e-9:
                print("      VIOLATION of Theorem A at the top")
        print("      report (section 7.4), proof / min / bound: %s" % rep.get((u, n), "-"))


if __name__ == "__main__":
    main()
