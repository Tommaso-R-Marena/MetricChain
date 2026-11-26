#!/usr/bin/env python3
"""Referee R12, check 7: Proposition Q1, Lemma Q2 and Corollary Q4a of Q_REPORT on real levels, and the tables of
its section 7.1 (parts A/B and C) recomputed with own code (numbers of the report typed in below).

Part A  the two-level design of K_REPORT 6.4 (u = 1, n_o = n/2, base brackets inside): ln C_max, M* = max{Lam, max_l t_l},
        ln C_max - M* (<= ln(L+2)), the largest term, Lam = ln 2Mbar, P_M, P_cnt, ln(1/delta'), over = ln(1/pi_dag) - n_o a,
        the bounds of Lemma Q3 (refined and uniform) and of Lemma K.4(d);  then the inequality (2.3) of Corollary Q4a.
Part B  Proposition Q1 and Lemma Q2(a)-(d) on 3000 random admissible levels (random lambda, eta, eta', theta, nu_1, b,
        ladders, inner costs, failure probabilities; n <= 3000).

usage: python3 r12_07_onelevel.py > out_07_onelevel.txt        (about 20 s)
"""
import sys, os, math, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r12lib import Cube, Tab, TabCache, Formula, Stats, Base, level_consts, level_cmax, LN2, INF

t0 = time.time()
print("# Referee R12, check 7: one level -- Proposition Q1, Lemma Q2, Corollary Q4a; tables of Q_REPORT 7.1 recomputed")

u = 1.0
cu = Cube(u)
fm = Formula(cu)
st = Stats()
tabs = TabCache(u, 8)
base = Base(cu, tabs, st, fm)
# tau_2 from the closed form  min_phi max{(1-phi) a, phi a + (1-phi) theta_na(phi a/(1-phi))}
lo, hi = 0.0, 1.0
for _ in range(100):
    mid = 0.5 * (lo + hi)
    if (1 - mid) * cu.a > mid * cu.a + (1 - mid) * cu.theta_na(mid * cu.a / (1 - mid)):
        lo = mid
    else:
        hi = mid
tau2 = (1 - lo) * cu.a
print("# u = 1: a = %.6f, tau_2/a = %.6f (report: 0.5004), at phi = %.6f" % (cu.a, tau2 / cu.a, lo))

rep_AB = {1000: (126.30, 0.91, 112.65, 22.86, 31.59, 120.0, 34.32, 1.535, 3.64, 4.75), 4000: (322.25, 2.41, 309.68, 24.35, 34.47, 317.1, 63.44, 1.418, 2.76, 4.59),
          16000: (1047.08, 1.00, 1033.09, 25.84, 37.34, 1040.5, 119.69, 1.338, 2.31, 4.49), 64000: (3839.07, 0.00, 3809.49, 27.33, 40.21, 3816.9, 231.95, 1.297, 2.08, 4.44)}
rep_C = {1000: (32.49, 107.89, 70.78, 2.24, 37.73, 104.46), 4000: (37.91, 151.65, 100.19, 1.58, 61.83, 129.66),
         16000: (51.57, 236.30, 158.82, 1.26, 107.31, 204.35), 64000: (92.35, 402.74, 286.02, 1.13, 195.85, 351.29)}
print("\n# Part A: K_REPORT 6.4 design, b = 0.5, lam = 0.2, eta = eta' = theta = 0.05, delta = 0.05, 40 rungs")
print("#      n   ln C_max  ln C_max - M*  largest term (rung: x_{l-1} -> x_l)  Lam      P_M     P_cnt   ln(1/delta')  over    over/sqrt(n_o)  Q3 refined/sqrt  K.4(d)/sqrt  Q3 uniform/sqrt | agrees with the report")
rowsC = []
nbad = 0
for n in (1000, 4000, 16000, 64000):
    n_o = n // 2
    n_i = n - n_o
    b, lam, eta, etap, theta, delta, Lr = 0.5, 0.2, 0.05, 0.05, 0.05, 0.05, 40
    x0 = 2 * u * n_i
    xs = [x0 * (b / x0) ** (l / Lr) for l in range(Lr + 1)]
    xs[-1] = b
    cs = level_consts(cu, tabs.get(n_o), n, n_o, lam, eta, etap, math.log(theta), 2 * math.exp(u) * n_o / theta, b, math.log(delta), Lr)
    lC = [base.raw(n_i, x, cs['ldeltap'])[0] for x in xs[1:]]
    lCmax, arg = level_cmax(cs, xs, lC)
    Lam, PM, Pc = cs['Lam'], cs['P_M'], cs['P_cnt']
    t = [min(Lam, xs[l - 1] + Pc) + lC[l - 1] for l in range(1, Lr + 1)]
    Mstar = max([Lam] + t)
    over = cs['l_inv_pi'] - n_o * cu.a
    lceta = math.log((1 - eta) / (1 + eta))
    m0 = math.ceil(-lceta / u)
    ell1 = LN2 + u * (m0 + 2) - math.log(theta)
    s = math.sqrt(n_o * ell1 / 2)
    assert s <= cu.p * n_o / 2 - 1
    q3ref = u * (1 + s) + (4 / (3 * cu.p)) * (ell1 + 2 / n_o) + math.log(n_o + 1)
    k4d = (u + math.log(4)) * (1 + s) + math.log(n_o + 1)
    q3uni = fm.cbar_pi(n_o, ell1)
    got = (lCmax, lCmax - Mstar, Lam, PM, Pc, -cs['ldeltap'], over, over / math.sqrt(n_o), q3ref / math.sqrt(n_o), k4d / math.sqrt(n_o))
    want = rep_AB[n]
    tol = (0.011, 0.011, 0.011, 0.011, 0.011, 0.11, 0.011, 0.0011, 0.011, 0.011)
    ok = all(abs(g - w) <= tl for g, w, tl in zip(got, want, tol))
    # Proposition Q1 and Lemma Q3 on this level
    ok1 = Mstar <= lCmax + 1e-9 and lCmax <= math.log(Lr + 2) + Mstar + 1e-9 and abs(Lam - (PM + cs['l_inv_pi'])) < 1e-9 and over <= q3ref and over <= q3uni
    nbad += (not ok) + (not ok1)
    print("  %6d  %8.2f   %5.2f        rung %2d: %8.1f -> %8.1f       %8.2f  %6.2f  %6.2f   %7.1f   %7.2f   %6.3f        %5.2f          %5.2f        %5.2f     | %s%s"
          % (n, lCmax, lCmax - Mstar, arg, xs[arg - 1] if arg else 0, xs[arg] if arg else 0, Lam, PM, Pc, -cs['ldeltap'], over, over / math.sqrt(n_o),
             q3ref / math.sqrt(n_o), k4d / math.sqrt(n_o), q3uni / math.sqrt(n_o), 'yes' if ok else 'NO', '' if ok1 else '  Q1/Q3 VIOLATED'))
    # (2.3): bounded theta: omega = a
    core = max([n_o * cu.a] + [min(n_o * cu.a, xs[l - 1]) + lC[l - 1] for l in range(1, Lr + 1)])
    err_ref = math.log(Lr + 2) + max(PM + q3ref, Pc)
    err_uni = math.log(Lr + 2) + max(PM + q3uni, Pc)
    cfin = base.raw(n_i, xs[-1], cs['ldeltap'])[0]
    eb = fm.Ebase(n_i, xs[-1], -cs['ldeltap'])
    rowsC.append((n, lCmax - core, err_ref, err_uni, lCmax - n * tau2, (lCmax - n * tau2) / math.sqrt(n), cfin - n_i * cu.a, eb))
print("#\n# Part A (continued): the inequality (2.3) of Corollary Q4a (bounded theta, omega = a)")
print("#      n   ln C_max - max{n_o a, max_l[min(n_o a, x_{l-1}) + ln C_l]}   Err of (2.3) with the refined Lemma Q3   with cbar_pi (as Corollary Q4a is stated)"
      "   ln C_max - n tau_2   /sqrt(n)   finest rung: ln cost - n_i a   E_base | agrees with the report (which uses the refined form)")
for (n, d, er, eu_, ex, exs, cf, eb) in rowsC:
    want = rep_C[n]
    got = (d, er, ex, exs, cf, eb)
    # the column 'ln C_max - n tau_2' depends on the fifth digit of tau_2/a (mine: bisection of the closed form): 0.1 nat allowed there
    ok = all(abs(g - w) <= tl for g, w, tl in zip(got, want, (0.011, 0.011, 0.1, 0.011, 0.011, 0.011)))
    ok1 = d <= er + 1e-9 and d <= eu_ + 1e-9 and cf <= eb + 1e-9
    nbad += (not ok) + (not ok1)
    print("  %6d   %7.2f                                                        %7.2f                               %7.2f                             %7.2f      %5.2f      %7.2f                %7.2f | %s%s"
          % (n, d, er, eu_, ex, exs, cf, eb, 'yes' if ok else 'NO', '' if ok1 else '  (2.3) VIOLATED'))
print("# rows that differ from the report or violate an inequality: %d" % nbad)

# -------------------------------------------------------------------------------------------- Part B
print("\n# Part B: Proposition Q1 and Lemma Q2 on random admissible levels")
rng = np.random.default_rng(2026)
nlev = 0
bad = 0
for trial in range(3000):
    uu = float(rng.choice([0.1, 0.5, 1.0, 2.0, 4.0]))
    c2 = Cube(uu)
    n = int(rng.integers(2, 3001))
    n_o = int(rng.integers(1, n))
    n_i = n - n_o
    lam = float(10 ** rng.uniform(-4, 0))
    eta = float(10 ** rng.uniform(-3, math.log10(0.5)))
    etap = float(10 ** rng.uniform(-3, 0))
    ltheta = float(rng.uniform(-12, 0.8 * n_o + 3))
    nu1 = float(10 ** rng.uniform(0, 6))
    L = int(rng.integers(1, 60))
    x0 = 2 * uu * n_i
    b = float(10 ** rng.uniform(-3, math.log10(x0 * 0.9)))
    cuts = np.sort(rng.uniform(0, 1, L - 1))[::-1] if L > 1 else np.array([])
    xL = b * float(rng.uniform(0.05, 1.0))
    xs = [x0] + [xL + (x0 - xL) * float(v) * 0.999 for v in cuts] + [xL]
    if any(xs[i] <= xs[i + 1] for i in range(L)):
        continue
    ld = -float(10 ** rng.uniform(-3, 4))
    t = Tab(n_o, uu)
    cs = level_consts(c2, t, n, n_o, lam, eta, etap, ltheta, nu1, b, ld, L)
    lC = [float(rng.uniform(0, n_i * LN2)) for _ in range(L)]
    lCmax, arg = level_cmax(cs, xs, lC)
    nlev += 1
    Lam, PM, Pc = cs['Lam'], cs['P_M'], cs['P_cnt']
    tl = [min(Lam, xs[l - 1] + Pc) + lC[l - 1] for l in range(1, L + 1)]
    Ms = max([Lam] + tl)
    J, K = cs['J'], cs['K']
    checks = [
        abs(Lam - (PM + cs['l_inv_pi'])) < 1e-8,                                   # Q1: Lam = P_M + ln(1/pi_dag)
        PM <= Pc + 1e-12,
        Ms <= lCmax + 1e-9 and lCmax <= math.log(L + 2) + Ms + 1e-9,               # Q1: the sandwich
        J <= (2 * uu * n + b + n_o * LN2) / lam + 1 + 1e-9,                        # Q2(a)
        cs['l_inv_pi'] <= (n_o + 1) * LN2 + 1e-9,                                  # Q2(b)
        cs['m_max'] <= math.log2(2 * (1 + eta) * math.exp(lam) * cs['nu0'] / (1 - eta)) + n_o + 2 + 1e-9,
        K <= 3 * (1 + eta) / eta ** 2 * (-ld + math.log(2.0 * (J + 1) * (cs['m_max'] + 1) * (L + 2))) + 1 + 1e-6,       # Q2(c)
        abs(-cs['ldeltap'] - (-ld + math.log(2 * L) + Lam)) < 1e-8,                # Q2(d)
        -cs['ldeltap'] + n_i * LN2 <= -ld + n * LN2 + math.log(4 * L) + PM + 1e-8,  # (2.1)
    ]
    bad += sum(1 for ck in checks if not ck)
print("  %d random levels, 9 relations each: %d failures" % (nlev, bad))
print("\n# done in %.0f s" % (time.time() - t0))
