#!/usr/bin/env python3
"""r11_nest_M.py -- referee: the nested design of Theorem A for M epochs with ONE slope step per epoch (J_m = 1: true for
m = 0, 1, 2 at u = 1; m = 0, 1 at u = 1/2 and 2), exactly, with own code:

    F_0 = T[B; 1, m_0],     F_{e+1} = T[ D'[ S[F_e]; phi_e, X_e ]; alpha^(e+1), m_{e+1} ]

Variant "min" (the families as defined) or "proof" (the level whenever built).  Node checks of the induction on every
node with the error functions of sections 2-5; the top against n B_M + E'_M of (A.1).
usage: python3 r11_nest_M.py u n M [variant]"""
import math, sys, time
sys.dont_write_bytecode = True
import rlib
from rlib import LN2, INF
import r03_formula as F

EPS = 0.8715
LD = math.log(0.05)


class Nest:
    def __init__(self, u, n, M, variant):
        self.cu = cu = rlib.Cube(u)
        self.u, self.n, self.M, self.variant = u, n, M, variant
        seq = self.seq = rlib.epochs(cu, M + 2)
        assert all(seq['J'][m] == 1 for m in range(M)), "this script needs J_m = 1"
        a = cu.a
        self.XB = rlib.X_B(cu, n)
        self.XD = [rlib.X_D(cu, n, seq['phi'][m]) for m in range(M)]
        self.sig = [1.0 / seq['d'][m] for m in range(M)]
        self.Bt = [max(1.0, seq['R'][m] / (2 * u * a)) * seq['B'][m] for m in range(M)]
        self.ch = [None] * (M + 1)
        Lam = -LD + n * LN2
        for e in range(M, -1, -1):
            Bp = seq['B'][e] if e >= 1 else a
            calX = self.XD[e - 1] if e >= 1 else self.XB
            alpha = min(EPS, 1.0) if e == M else 1.0
            m = rlib.Chain.design_m(cu, n, Bp, calX, alpha, Lam)
            self.ch[e] = rlib.Chain(cu, n, Bp, calX, alpha, m)
            Lam += self.ch[e].j(n) * self.ch[e].qT(n, Lam + n * Bp)
            if e >= 1:
                Lam += rlib.q_b(cu, n, Lam)
                Lam += rlib.q_b(cu, n, Lam)
        self.count = 0
        self.viol = 0
        self.minslack = {}
        self.built = {}

    # ---- error functions
    def E_T(self, e, d, Lam):
        if e == 0:
            return self.ch[0].E_T(d, Lam, lambda dd, x, L: rlib.E_frakB(self.cu, dd, L))
        return self.ch[e].E_T(d, Lam, lambda dd, x, L: self.E_D(e - 1, dd, L))

    def E_S(self, e, d, Lam):
        cu = self.cu
        return self.E_T(e, d, Lam + rlib.q_b(cu, d, Lam)) + self.sig[e] * (1 + rlib.c_log(cu, d) + cu.h) + rlib.ell0_b(cu, d, Lam)

    def E_D(self, e, d, Lam):
        cu = self.cu
        return self.E_S(e, d, Lam + rlib.q_b(cu, d, Lam)) + self.Bt[e] + rlib.ell0_b(cu, d, Lam)

    def note(self, kind, slack):
        self.count += 1
        if slack < self.minslack.get(kind, INF):
            self.minslack[kind] = slack
        if slack < -1e-9:
            self.viol += 1

    # ---- exact costs
    def base(self, d, ld):
        t, _ = rlib.base_lcost(self.cu, d, self.XB, ld)
        self.note('base', d * self.cu.a + rlib.E_frakB(self.cu, d, -ld + d * LN2) - t)
        return t

    def chain(self, e, d, ld):
        ch = self.ch[e]
        cu, u, m, c = self.cu, self.u, ch.m, ch.c
        coarse = self.base if e == 0 else (lambda dd, l: self.D(e - 1, dd, l))
        recs = []
        dd, l = d, ld
        while dd >= ch.d0:
            a_d = ch.alow + ch.j(dd) * ch.w
            lev = rlib.Level(u, dd, m, c, c, c, math.log(c), 2 * math.exp(u) * m / c, a_d - ch.w, l, 2, tab=rlib.tables(u, m, c, keep=12))
            if lev.x_out > a_d + 1e-12:
                self.viol += 1
            recs.append((dd, l, lev, a_d))
            dd, l = dd - m, lev.ldp
        t, _ = rlib.base_lcost(cu, dd, ch.alow, l)
        self.note('chain%d' % e, dd * ch.Bp + self.E_T(e, dd, -l + dd * LN2) - t)
        for (dd, l, lev, a_d) in reversed(recs):
            c1 = coarse(dd - m, lev.ldp)
            t = lev.lcmax([ch.calX, a_d - ch.w], [c1, t])
            self.note('chain%d' % e, dd * ch.Bp + self.E_T(e, dd, -l + dd * LN2) - t)
        return t

    def S(self, e, d, x, ld):
        cu, u, h = self.cu, self.u, self.cu.h
        B = self.ch[e].Bp
        xh = min(x, h * d)
        X0 = 1 + rlib.c_log(cu, d) + h
        typ = d * B - self.sig[e] * xh + self.E_S(e, d, -ld + d * LN2)
        if xh < X0:
            t = self.chain(e, d, ld)
        else:
            n_o = math.floor((xh - 1 - rlib.c_log(cu, d)) / h + 1e-12)
            n_i = d - n_o
            lth = rlib.ltheta_for_accuracy(cu, d, xh, 1.0)
            x1 = min(math.ceil(xh - 1e-12), math.ceil(2 * u * n_i - 1e-12) - 1)
            xs = [float(x1 - i) for i in range(x1)]
            lev = rlib.Level(u, d, n_o, 1.0, 0.5, 1.0, lth, 1.0, 1.0, ld, len(xs))
            if abs(lev.x_out - xh) > 1e-9:
                self.viol += 1
            c0 = self.chain(e, n_i, lev.ldp)
            t = lev.lcmax(xs, [c0] * len(xs))
            self.built['S%d' % e] = self.built.get('S%d' % e, 0) + 1
            self.note('S%d' % e, typ - t)
            if self.variant == 'min':
                t = min(t, self.chain(e, d, ld))
        self.note('S%d' % e, typ - t)
        return t

    def D(self, e, d, ld):
        cu, u = self.cu, self.u
        phi, R = self.seq['phi'][e], self.seq['R'][e]
        n_o = math.floor(phi * d + 1e-12)
        typ = d * self.seq['B'][e + 1] + self.E_D(e, d, -ld + d * LN2)
        if n_o >= 1 and 2 * u * (d - n_o) > 1:
            n_i = d - n_o
            lth = rlib.ltheta_for_accuracy(cu, d, self.XD[e], 1.0)
            xs = rlib.ladder_U(cu, n_i, 1.0, R * n_i)
            lev = rlib.Level(u, d, n_o, 1.0, 0.5, 1.0, lth, 1.0, 1.0, ld, len(xs))
            if abs(lev.x_out - self.XD[e]) > 1e-9:
                self.viol += 1
            lc = [self.S(e, n_i, x, lev.ldp) for x in xs]
            t = lev.lcmax(xs, lc)
            self.built['D%d' % e] = self.built.get('D%d' % e, 0) + 1
            self.note('D%d' % e, typ - t)
            if self.variant == 'min':
                t = min(t, self.S(e, d, self.XD[e], ld))
        else:
            t = self.S(e, d, self.XD[e], ld)
        self.note('D%d' % e, typ - t)
        return t


def main():
    u, n, M = float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    variants = sys.argv[4:] or ['proof', 'min']
    for variant in variants:
        t0 = time.time()
        N = Nest(u, n, M, variant)
        t = N.chain(M, n, LD)
        cu = N.cu
        E = F.E_A1(cu, n, EPS, -LD, M, rlib.epochs(cu, 45))
        bound = n * (N.seq['B'][M] if M >= 1 else cu.a) + E
        print("u = %.1f n = %d M = %d %-5s: ln cost/(n a) = %.4f   bound of Theorem A = %.4f   blocks (top first): %s"
              % (u, n, M, variant, t / (n * cu.a), bound / (n * cu.a), [(c.m, c.j(n)) for c in reversed(N.ch)]))
        print("      node checks %d (levels built: %s); violations %d; least slack of the induction by family: %s   [%.0f s]"
              % (N.count, N.built, N.viol, {k: round(v, 1) for k, v in sorted(N.minslack.items())}, time.time() - t0), flush=True)
        if t > bound + 1e-9:
            print("      VIOLATION of Theorem A at the top")


if __name__ == "__main__":
    main()
