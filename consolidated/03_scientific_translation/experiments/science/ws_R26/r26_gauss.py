#!/usr/bin/env python3
"""r26_gauss.py -- workstream R26, Item 4 (light): numerical checks of the formulas used in N_REPORT 5.1.

G1  closed forms of Theorem N9 against quadrature:   Xi_L(q) = int_0^inf L e^{Lr} Phi(-t-r) dr,
    Theta_L(p) = int_0^inf L e^{-Lr} Phi(c+r) dr,   t = Phi^{-1}(1-q), c = Phi^{-1}(p).
G2  attainment: for V = e^{L(x-t)_+} at s = 1:  E(V-1)_+ = Xi_L(Phi(-t));  for V = e^{-L(x-c)_+}: E min(V,1) ...
G3  the two inequalities of Proposition N10(b):  E min(e^{Lx}, e^{Lt}) <= e^{L^2/2} e^{-(L-t)^2/2} (0 <= t <= L),
    Phi(-t) <= e^{-t^2/2}/2 (t >= 0).
G4  Proposition N10(b) / remark (R7) in runs of my Algorithm A (no-cap variant) on V = e^{L x_1}: the largest
    sample of every run against (2K/(1+eta)) exp((L - sqrt(2 x_out))^2/2), and against the sharper form of (R7),
    K/((1+eta) p(t_x)), t_x = inf{t : E min(V,t) >= e^{-x_out} A}.
"""
import math
import sys
import time

import numpy as np
from scipy import integrate
from scipy.special import ndtr, ndtri

import r26_alg as A
import r26_n1 as N1


def main(runs):
    viol = 0
    worst = 0.0
    for L in (0.5, 1.5, 3.0, 6.0):
        for q in (1e-6, 1e-3, 0.05, 0.3, 0.7, 0.95):
            G = N1.GaussLine(L)
            t = -ndtri(q)
            num, _ = integrate.quad(lambda r: L * math.exp(L * r) * ndtr(-t - r), 0, 60, limit=400, epsabs=0,
                                    epsrel=1e-12)
            worst = max(worst, abs(num - G.Xi(q)) / num)
            c = ndtri(q)
            num2, _ = integrate.quad(lambda r: L * math.exp(-L * r) * ndtr(c + r), 0, 200 / L, limit=400, epsabs=0,
                                     epsrel=1e-12)
            closed2 = q + math.exp(L * c + L * L / 2) * ndtr(-c - L)
            worst = max(worst, abs(num2 - closed2) / num2)
            # attainment
            ex, _ = integrate.quad(lambda x: (math.exp(L * (x - t)) - 1) * math.exp(-x * x / 2) / math.sqrt(2 * math.pi),
                                   t, t + 60, limit=400, epsabs=0, epsrel=1e-12)
            worst = max(worst, abs(ex - G.Xi(q)) / ex)
    print(f"G1/G2: closed forms of Xi_L, Theta_L against quadrature and attainment by the half-line dip, 24 pairs: "
          f"largest relative difference {worst:.1e}")
    viol += worst > 1e-8
    v3 = 0
    for L in np.linspace(0.2, 8, 40):
        for t in np.linspace(0, L, 60):
            lhs = ndtr(t - L) + math.exp(L * t - L * L / 2) * ndtr(-t)
            if lhs > math.exp(-(L - t) ** 2 / 2) * (1 + 1e-12):
                v3 += 1
    for t in np.linspace(0, 12, 400):
        if ndtr(-t) > 0.5 * math.exp(-t * t / 2) * (1 + 1e-12):
            v3 += 1
    print(f"G3: the two inequalities of Proposition N10(b) on grids (2400 + 400 points): violations {v3}")
    viol += v3
    print(f"G4: runs (seeds default_rng(6000000 + 1000*cell + r), r < {runs})")
    cell = 0
    for L, theta, etap in ((3.0, 1.0, 1.0), (3.5, 1.0, 1.0), (3.5, 0.3, 1.0), (4.0, 1.0, 1.0)):
        G = N1.GaussLine(L)
        P = A.Params(lam=1.0, eta=0.5, etap=etap, theta=theta, nu1=1.0, b=0.25, delta=0.05, kappa0=1.0,
                     x=(6.0, 2.0, 0.25), C=(1.0, 5.0, 25.0))
        xo = P.x_out()
        pi_star = N1.closing_level_numeric(G.Xi, G.Theta, theta, P.eta, 1.0)
        cst = A.constants(P, G.ell0, pi_star, u0=G.u0)
        bound = 2 * cst["K"] / (1 + P.eta) * math.exp((L - math.sqrt(2 * xo)) ** 2 / 2) if xo < L * L / 2 else None
        # sharper form: t_x in the variable x: E min(V, e^{L t}) = A [Phi(t-L) + e^{Lt-L^2/2} Phi(-t)] >= e^{-x_out} A
        lo, hi = -10.0, L + 10.0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            val = ndtr(mid - L) + math.exp(L * mid - L * L / 2) * ndtr(-mid)
            if val >= math.exp(-xo):
                hi = mid
            else:
                lo = mid
        sharp = cst["K"] / ((1 + P.eta) * ndtr(-hi))
        ratios, ratios2, nr, bad = [], [], 0, 0
        for r in range(runs):
            rng = np.random.default_rng(6000000 + 1000 * cell + r)
            rec = A.run_A(P, G.V, lambda m_: G.sample(rng, m_), G.Xi, G.Theta, G.ell0, pi_star, rng, u0=G.u0,
                          max_points=6_000_000)
            if rec["stop"] != "closure":
                continue
            chk = A.check_core(rec, P, G.A, G.p_gt, G.excess, G.V(rec["idx"]))
            nr += 1
            bad += not chk["valid"]
            if bound is not None:
                ratios.append(chk["maxM"] / bound)
            ratios2.append(chk["maxM"] / sharp)
        cell += 1
        cond = "x_out < L^2/2" if bound is not None else "x_out >= L^2/2: N10(b) does not apply"
        print(f"   L = {L}, theta = {theta}: x_out = {xo:.3f}, L^2/2 = {L * L / 2:.3f} ({cond}); K = {cst['K']}; runs "
              f"closed {nr}, invalid {bad}; smallest M_max / N10(b) bound: "
              f"{min(ratios) if ratios else float('nan'):.2f}; smallest M_max / (R7) bound: "
              f"{min(ratios2) if ratios2 else float('nan'):.2f}")
        if ratios and min(ratios) < 1:
            viol += 1
        if ratios2 and min(ratios2) < 1:
            viol += 1
        viol += bad
    print(f"total violations: {viol}")
    return viol


if __name__ == "__main__":
    t0 = time.time()
    runs = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    print(f"r26_gauss.py runs {runs}; started {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    v = main(runs)
    print(f"finished {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}; elapsed {time.time() - t0:.1f} s; "
          f"peak memory {A.peak_mb():.0f} MB")
    sys.exit(1 if v else 0)
