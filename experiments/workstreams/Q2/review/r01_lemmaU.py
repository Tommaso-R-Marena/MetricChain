#!/usr/bin/env python3
"""r01_lemmaU.py -- referee's test of Lemma U (inequality (U) and parts (b), (c)) with own evaluator rlib.

Levels: lambda = 1, eta = 1/2, eta' = 1, nu1 = 1, tolerance b, ladder of step one below the cap Xi,
inner family SATURATING (certified cost = the majorant of its type).
Families:  one line / maxima of lines with a finite common range R;
           R = infinity with POSITIVE slopes (the coordinator's question), with a flat line ("flat"),
           without a flat line but nonnegative on [0, 2u d] ("steep-B"),
           and a negative control: R = infinity, positive slope, majorant cut at 0 where it is negative
           (the family then does NOT have the type).
"""
import math, sys, time
sys.dont_write_bytecode = True
import numpy as np
import rlib
from rlib import LN2, INF

t0 = time.time()


def Efuns():
    return [("E=0", None),
            ("3sqrt(d)", lambda d, x, Lam: 3 * math.sqrt(d) + 0 * x),
            ("Lam/7", lambda d, x, Lam: Lam / 7 + 0 * x),
            ("5/x+lnLam", lambda d, x, Lam: 5 / x + math.log(Lam))]


def costs(fam, d, xs, ld):
    xs = np.asarray(xs, dtype=np.float64)
    xx = np.minimum(xs, fam.R * d) if fam.R < INF else xs
    mj = np.max(np.stack([d * B - s * xx for (B, s) in fam.lines]), axis=0)
    if fam.floor0:
        mj = np.maximum(mj, 0.0)
    Lam = -ld + d * LN2
    if fam.Efun is None:
        return mj
    return mj + fam.Efun(d, xs, Lam)


class Stat:
    def __init__(self):
        self.n = 0; self.viol = 0; self.minslack = INF; self.arg = None

    def add(self, slack, tag):
        self.n += 1
        if slack < -1e-9:
            self.viol += 1
        if slack < self.minslack:
            self.minslack = slack; self.arg = tag


stats = {}
aux = Stat()          # parts (b), (c)
auxfail = []


def run_level(cu, n, n_o, e, lth_extra, b, Xi, ld, fam, cat, tagx):
    u = cu.u
    n_i = n - n_o
    theta = cu.theta_na(e)
    lth = math.log(3.0) + math.log(n_o + 1.0) + 2 * u + math.exp(u) + n_o * e + lth_extra
    xs = rlib.ladder_U(cu, n_i, b, Xi)
    L = len(xs)
    lev = rlib.Level(u, n, n_o, 1.0, 0.5, 1.0, lth, 1.0, b, ld, L)
    lc = costs(fam, n_i, xs, lev.ldp)
    lcm = lev.lcmax(xs, lc)
    Lam = -ld + n * LN2
    # (b)
    Ab = rlib.A_nb(cu, n, b)
    chk = [("J+1<=A", lev.J + 1 <= Ab + 1e-9),
           ("mmax", lev.m_max + 1 <= rlib.mbar_b(cu, n, b) + 1e-9),
           ("L", L + 2 <= n + 3),
           ("K", lev.K <= rlib.Kbar_b(cu, n, -ld, b) + 1e-9),
           ("PM", lev.P_M + math.log(n_o + 1.0) <= 1 + lev.P_cnt + 1e-9),
           ("2.1", -lev.ldp + n_i * LN2 <= Lam + rlib.q_b(cu, n, Lam, b) + 1e-9),
           # (c)
           ("pi", -lev.lpi <= n_o * theta + math.log(n_o + 1.0) + 1e-9),
           ("rdag", lev.rd >= min(n_o - 1, math.floor(cu.rho_of(e) * n_o + 1e-12) + 1)),
           ("G", max(lev.Lam_lev - 1 - lev.P_cnt, 0.0) <= n_o * theta + 1e-9)]
    for name, ok in chk:
        aux.n += 1
        if not ok:
            aux.viol += 1; auxfail.append((name, u, n, n_o, e, b, ld))
    # (d)
    Lamp = Lam + rlib.q_b(cu, n, Lam, b)
    E1 = fam.E(n, b, Lamp)
    bound = max(n_i * B + (1 - s) * n_o * theta for (B, s) in fam.lines) + rlib.ell0_b(cu, n, Lam, b) + E1
    st = stats.setdefault(cat, Stat())
    st.add(bound - lcm, (u, n, n_o, round(e / cu.h, 3), round(lth_extra, 1), b, round(Xi, 2), round(ld, 2), tagx,
                         round(lcm, 3), round(bound, 3)))
    return bound - lcm, lev


def main(quick=False):
    for u in (0.5, 1.0, 2.0):
        cu = rlib.Cube(u)
        a, h, es = cu.a, cu.h, cu.eps_star
        sizes = [2, 3, 5, 12, 40, 150, 600, 2500, 10000, 40000] if not quick else [5, 150, 2500]
        rates = [0.0, 0.5 * h, h, 2 * h, 0.97 * es, 1.4 * es]
        for n in sizes:
            nos = sorted(set(max(1, min(n - 1, int(round(f * n)))) for f in (0.0, 0.03, 0.12, 0.3, 0.55, 0.8)))
            lds = [math.log(0.5), math.log(0.05), -12 * math.log(10), -float(n)]
            big = n >= 10000
            if big:
                lds = [math.log(0.05), -float(n)]
            for n_o in nos:
                n_i = n - n_o
                for e in rates:
                    th = cu.theta_na(e)
                    for b in ((1.0, 12.0) if big else (1.0, 3.7, 12.0)):
                        if 2 * u * n_i <= b:
                            continue
                        for lth_extra in ((0.0,) if big else (0.0, 7.0)):
                            for ild, ld in enumerate(lds):
                                # rotate the error functions to keep the run short
                                for (en, Ef) in [Efuns()[(ild + n_o) % 4], Efuns()[0]]:
                                    # ---- finite range: one line and maxima of lines
                                    for R in (h / 3, h, min(1.0, 6 * h)):
                                        if n_o * th > R * n_i or R * n_i > n:
                                            continue
                                        for lines, nm in (([(a, 1.0)], "1line"), ([(h, 0.0)], "1line"), ([(3 * a, 0.7)], "1line"),
                                                          ([(a, 0.3)], "1line"),
                                                          ([(a, 1.0), (0.8 * a, 0.5), (0.6 * a, 0.0)], "max3"),
                                                          ([(1.5 * h, 1.0), (h, 0.2)], "max2")):
                                            if any(B < s * R for (B, s) in lines):
                                                continue
                                            fam = rlib.SatFamily(lines, R, Ef, floor0=True)
                                            for Xi in (n_o * th, R * n_i):
                                                run_level(cu, n, n_o, e, lth_extra, b, Xi, ld, fam, "finite R: " + nm, (R / h, en, str(lines)))
                                    # ---- R = infinity, positive slopes, with a flat line
                                    for lines in ([(0.5 * a, 0.0), (0.9 * a, 0.4), (1.6 * a, 1.0)],
                                                  [(h, 0.0), (a, 1.0)],
                                                  [(0.2 * h, 0.0), (h, 0.15), (a, 0.6), (2 * a, 1.0)]):
                                        fam = rlib.SatFamily(lines, INF, Ef, floor0=False)
                                        for Xi in (n_o * th, min(n, 2 * n_o * th + 5), float(n)):
                                            if Xi < n_o * th:
                                                continue
                                            run_level(cu, n, n_o, e, lth_extra, b, Xi, ld, fam, "R=inf, positive slopes, flat line", (en, str(lines)))
                                    # ---- R = infinity, positive slopes, no flat line, majorant >= 0 on [0, 2u d]
                                    for lines in ([(2 * u * 1.0, 1.0)], [(2 * u * 0.3, 0.3), (2 * u, 1.0)]):
                                        fam = rlib.SatFamily(lines, INF, Ef, floor0=False)
                                        for Xi in (n_o * th, float(n)):
                                            run_level(cu, n, n_o, e, lth_extra, b, Xi, ld, fam, "R=inf, positive slopes, no flat line, B_i >= 2u sigma_i", (en, str(lines)))
                                    # ---- negative control: R = infinity, slope 1, B = a/2, cut at 0  (NOT a family of the type)
                                    if Ef is None:
                                        fam = rlib.SatFamily([(0.5 * a, 1.0)], INF, None, floor0=True)
                                        run_level(cu, n, n_o, e, lth_extra, b, n_o * th, ld, fam, "CONTROL (type violated): R=inf, slope 1, cut at 0", ("-",))
        print("u = %.1f done, %.0f s" % (u, time.time() - t0), flush=True)
    print()
    print("parts (b), (c): %d checks, %d violations %s" % (aux.n, aux.viol, auxfail[:5]))
    tot = 0
    for cat in sorted(stats):
        st = stats[cat]
        tot += st.n
        print("%-70s levels %7d  violations %6d  least slack of (U) %10.3f" % (cat, st.n, st.viol, st.minslack))
        print("      at (u, n, n_o, e/h, extra ln theta, b, Xi, ln delta, family, ln C_max, bound) = %s" % (st.arg,))
    print("total levels: %d;  time %.0f s" % (tot, time.time() - t0))


if __name__ == "__main__":
    main(quick=("quick" in sys.argv))
