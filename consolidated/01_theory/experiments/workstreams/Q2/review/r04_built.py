#!/usr/bin/env python3
"""r04_built.py -- referee: the levels AS BUILT of Proposition D' and of Proposition Q6(e) / Corollary Q6(e)-max,
with own evaluator rlib and saturating inner families.  Checks the checklists (hypotheses of Lemma U for the level
as built), the accuracy, Lemma Q4(b) on the outer block, and the final type inequality of each proposition
(level and pass-through).  Also: Q6(e)-max for R = infinity with POSITIVE slopes and a flat line (R' = e) --
not stated in the report; the coordinator's case."""
import math, sys, time
sys.dont_write_bytecode = True
import numpy as np
import rlib
from rlib import LN2, INF, C3

t0 = time.time()


def costs(fam, d, xs, ld):
    xs = np.asarray(xs, dtype=np.float64)
    xx = np.minimum(xs, fam.R * d) if fam.R < INF else xs
    mj = np.max(np.stack([d * B - s * xx for (B, s) in fam.lines]), axis=0)
    if fam.floor0:
        mj = np.maximum(mj, 0.0)
    if fam.Efun is None:
        return mj
    return mj + fam.Efun(d, xs, -ld + d * LN2)


class Stat:
    def __init__(self):
        self.n = 0; self.viol = 0; self.min = INF; self.arg = None; self.aux = 0; self.auxviol = 0; self.pt = 0

    def add(self, sl, tag):
        self.n += 1
        if sl < -1e-9:
            self.viol += 1
        if sl < self.min:
            self.min, self.arg = sl, tag

    def chk(self, ok):
        self.aux += 1
        if not ok:
            self.auxviol += 1


def Dprime(cu, n, N, phi, b, lines, R, Ef, ld, st):
    u, a = cu.u, cu.a
    fam = rlib.SatFamily(lines, R, Ef, floor0=True)
    calX = rlib.X_D(cu, N, phi, b)
    Lam = -ld + n * LN2
    Bp = max((1 - phi) * B + (1 - s) * phi * a for (B, s) in lines)
    Bt = max(1.0, b * phi / (2 * u * (1 - phi))) * max(max(B - (1 - s) * a, 0.0) for (B, s) in lines)
    Lamp = Lam + rlib.q_b(cu, n, Lam, b)
    Eterm = fam.E(n, b, Lamp)
    typ = n * Bp + Bt + rlib.ell0_b(cu, n, Lam, b) + Eterm
    # pass-through
    pt = float(costs(fam, n, [calX], ld)[0])
    n_o = math.floor(phi * n + 1e-12)
    built = n_o >= 1 and 2 * u * (n - n_o) > b
    if not built:
        st.pt += 1
        st.add(typ - pt, ("pass-through", u, n, phi, b, str(lines)))
        return None
    n_i = n - n_o
    lth = rlib.ltheta_for_accuracy(cu, n, calX, b)
    Xi = R * n_i
    xs = rlib.ladder_U(cu, n_i, b, Xi)
    lev = rlib.Level(u, n, n_o, 1.0, 0.5, 1.0, lth, 1.0, b, ld, len(xs))
    st.chk(abs(lev.x_out - calX) < 1e-9)
    st.chk(lth >= math.log(3.0 * (n_o + 1)) + 2 * u + math.exp(u) - 1e-12)
    st.chk(n_o * a <= Xi + 1e-9 and Xi <= n + 1e-9)
    st.chk(-lev.lpi <= n_o * a + math.log(n_o + 1.0) + 1e-9)
    st.chk(lev.rd >= min(n_o - 1, math.floor(cu.p * n_o + 1e-12) + 1))
    st.chk(-lev.ldp + n_i * LN2 <= Lamp + 1e-9)
    lcm = lev.lcmax(xs, costs(fam, n_i, xs, lev.ldp))
    st.add(typ - min(lcm, pt), ("level", u, n, n_o, round(phi, 4), b, round(ld, 1), str(lines), round(R / cu.h, 3)))
    return lev


def Q6e(cu, n, x, e, b, lines, R, Ef, ld, st, Rp=None):
    u = cu.u
    th = cu.theta_na(e)
    fam = rlib.SatFamily(lines, R, Ef, floor0=(R < INF))
    if Rp is None:
        Rp = R * e / (th + R) if R < INF else e
    xh = min(x, Rp * n)
    Lam = -ld + n * LN2
    sig = [(B - (1 - s) * th) / e for (B, s) in lines]
    loss = max(max(sg, 0.0) for sg in sig) * (b + rlib.c_log(cu, n) + e) + rlib.ell0_b(cu, n, Lam, b)
    Lamp = Lam + rlib.q_b(cu, n, Lam, b)
    typ = max(n * B - sg * xh for ((B, s), sg) in zip(lines, sig)) + loss + fam.E(n, min(x, b), Lamp)
    pt = float(costs(fam, n, [x], ld)[0])
    X0 = b + rlib.c_log(cu, n) + e
    if xh < X0:
        st.pt += 1
        st.add(typ - pt, ("pass-through", u, n, x, e / cu.h, b, str(lines)))
        return None
    n_o = math.floor((xh - b - rlib.c_log(cu, n)) / e + 1e-12)
    n_i = n - n_o
    st.chk(1 <= n_o <= n - 1 and 2 * u * n_i > b)
    lth = rlib.ltheta_for_accuracy(cu, n, xh, b)
    st.chk(lth >= math.log(3.0 * (n_o + 1)) + 2 * u + math.exp(u) + n_o * e - 1e-9)
    if R < INF:
        st.chk(n_o * th <= R * n_i + 1e-9)
    xs = rlib.ladder_U(cu, n_i, b, n_o * th)
    lev = rlib.Level(u, n, n_o, 1.0, 0.5, 1.0, lth, 1.0, b, ld, len(xs))
    st.chk(abs(lev.x_out - xh) < 1e-9)
    st.chk(-lev.lpi <= n_o * th + math.log(n_o + 1.0) + 1e-9)
    st.chk(lev.rd >= min(n_o - 1, math.floor(cu.rho_of(e) * n_o + 1e-12) + 1))
    st.chk(-lev.ldp + n_i * LN2 <= Lamp + 1e-9)
    lcm = lev.lcmax(xs, costs(fam, n_i, xs, lev.ldp))
    st.add(typ - min(lcm, pt), ("level", u, n, n_o, round(xh, 2), round(e / cu.h, 3), b, round(ld, 1), str(lines),
                                "inf" if R == INF else round(R / cu.h, 3)))
    return lev


def main():
    Efl = [None, lambda d, x, Lam: 3 * math.sqrt(d) + 0 * x, lambda d, x, Lam: Lam / 7 + 0 * x,
           lambda d, x, Lam: 5 / x + math.log(Lam)]
    sD, sQ, sQinf = Stat(), Stat(), Stat()
    us = [float(x) for x in sys.argv[1:]] or [0.5, 1.0, 2.0]
    for u in us:
        cu = rlib.Cube(u)
        a, h = cu.a, cu.h
        seq = rlib.epochs(cu, 13)
        # ------------------------------------------------ Proposition D'
        typesD = [([(seq['B'][m], 1.0)], seq['R'][m], seq['phi'][m]) for m in range(0, 13, 2)]
        for (B, s, R) in ((h, 0.0, h), (a, 0.3, h), (a, 0.7, h / 3), (3 * a, 1.0, min(1.0, 6 * h)), (a, 1.0, h / 50), (h, 0.3, h / 3)):
            if B >= s * R:
                for f in (1.0, 0.5):
                    typesD.append(([(B, s)], R, f * R / (a + R)))
        typesD.append(([(a, 1.0), (0.8 * a, 0.5), (0.6 * a, 0.0)], h, h / (a + h)))
        typesD.append(([(1.5 * h, 1.0), (h, 0.2)], h / 3, 0.5 * (h / 3) / (a + h / 3)))
        for (lines, R, phi) in typesD:
            first = max(2, math.ceil(1 / phi))
            ns = sorted(set([2, 3, first - 1, first, first + 1, 2 * first, 7 * first, 30 * first, 1000, 10 ** 4, 10 ** 5]))
            for n in ns:
                if n < 1:
                    continue
                for ild, ld in enumerate((math.log(0.5), math.log(0.05), -27.6, -float(n)) if n < 10 ** 5 else (math.log(0.05), -float(n))):
                    for b in ((1.0, 2.5, 17.3) if n < 10 ** 5 else (1.0, 17.3)):
                        for N in ((n, 3 * n) if n < 10 ** 5 else (n,)):
                            Dprime(cu, n, N, phi, b, lines, R, Efl[(ild + n) % 4], ld, sD)
        # the number quoted in section 3: ln(1/pi) - n_o a at n = 1e6, phi_0  (u = 1)
        if u == 1.0:
            lev = Dprime(cu, 10 ** 6, 10 ** 6, seq['phi'][0], 1.0, [(seq['B'][0], 1.0)], seq['R'][0], None, math.log(0.05), Stat())
            print("u = 1, n = 1e6, phi_0 = %.4f: n_o = %d, r_dagger = %d, p_u n_o = %.1f, ln(1/pi) - n_o a = %.1f   (report: -959)"
                  % (seq['phi'][0], lev.n_o, lev.rd, cu.p * lev.n_o, -lev.lpi - lev.n_o * a))
        # ------------------------------------------------ Proposition Q6(e) and Corollary Q6(e)-max
        typesQ = [([(seq['B'][m], j / seq['d'][m])], h / j) for m in (0, 3, 8) for j in range(1, seq['J'][m]) if j / seq['d'][m] <= 1][:8]
        typesQ += [([(seq['B'][m], 0.0)], INF) for m in (0, 5)]
        for (B, s, R) in ((h, 0.0, INF), (1.5 * h, 0.2, h), (a, 0.5, 2 * h), (3 * a, 1.0, h / 3), (a, 1.0, h / 20), (a, 0.7, h), (h, 0.3, h / 3)):
            if R == INF or B >= s * R:
                typesQ.append(([(B, s)], R))
        typesQ.append(([(a, 1.0), (0.8 * a, 0.5), (0.6 * a, 0.0)], h))
        typesQ.append(([(1.5 * h, 1.0), (h, 0.2)], h / 4))
        typesQ.append(([(a, 1.0), (1.2 * h, 0.6), (h, 0.3), (0.9 * h, 0.0)], 2 * h))
        typesInf = [[(0.5 * a, 0.0), (0.9 * a, 0.4), (1.6 * a, 1.0)], [(h, 0.0), (a, 1.0)],
                    [(0.2 * h, 0.0), (h, 0.15), (a, 0.6), (2 * a, 1.0)]]
        rates = [0.2 * h, 0.5 * h, h, 2 * h, 3 * h, 0.97 * cu.eps_star]
        for e in rates:
            th = cu.theta_na(e)
            for b in (1.0, 2.5, 17.3):
                for n in (30, 200, 1500, 10 ** 4, 10 ** 5):
                    if n == 10 ** 5 and b == 2.5:
                        continue
                    X0 = b + rlib.c_log(cu, n) + e
                    for ild, ld in enumerate((math.log(0.5), math.log(0.05), -27.6, -float(n)) if n < 10 ** 5 else (math.log(0.05), -float(n))):
                        Ef = Efl[(ild + n) % 4]
                        for (lines, R) in typesQ:
                            Rp = R * e / (th + R) if R < INF else e
                            top = Rp * n
                            for x in sorted(set([0.5 * X0, X0, X0 + e, 0.5 * (X0 + top), top, 1.7 * top])):
                                if x >= b:
                                    Q6e(cu, n, x, e, b, lines, R, Ef, ld, sQ)
                        for lines in typesInf:
                            top = e * n
                            for x in sorted(set([X0, X0 + e, 0.3 * top, top, 1.7 * top])):
                                if x >= b:
                                    Q6e(cu, n, x, e, b, lines, INF, Ef, ld, sQinf)
        print("u = %.1f done, %.0f s" % (u, time.time() - t0), flush=True)
    for (nm, st) in (("Proposition D' (levels as built and pass-through)", sD),
                     ("Proposition Q6(e) / Corollary Q6(e)-max (finite R, or R = inf with sigma = 0)", sQ),
                     ("Q6(e)-max with R = inf, POSITIVE slopes, a flat line, R' = e (referee's extension)", sQinf)):
        print("%s:\n    cases %d (of which pass-through only %d), violations %d, least slack %.3f at %s;\n    checklist items %d, violations %d"
              % (nm, st.n, st.pt, st.viol, st.min, st.arg, st.aux, st.auxviol))
    print("time %.0f s" % (time.time() - t0))


if __name__ == "__main__":
    main()
