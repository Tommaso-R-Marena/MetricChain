#!/usr/bin/env python3
"""R17, item 1(ii): the OUTER LOOP of the slope-step level of Q_REPORT section 4.1, run literally (grouped by
classes of equal fibre average) with the science division's own engine of Algorithm 2L+ (ws_R6/r6lib.py:
written from the specification of K_REPORT 2.2, exact constants, 40-digit control flow) and a SIMULATED inner
oracle, and checked run by run against every claim of Theorem K1 = Theorem 11.56 (ws_R6/checks.py).

Why: Q_REPORT section 8 item 1 and the referee R12 (section 4 item 1) say that Theorem 11.56 is used by the slope
step "far from the parameters at which it was simulated" and that "it cannot be simulated in this regime".  With
real inner procedures that is so (a run costs e^{36} evaluations at least).  With an inner oracle that answers
from the known fibre averages - valid answers of every shape the contract C3 allows, and invalid ones, among
them the trivial bracket that an aborted inner run returns - the outer loop CAN be run: thresholds
theta = e^{xhat-1} - (3e+1) - (2p_u)^n/e, unit ladders from ceil(xhat) down to x_L = b = 1, lam = 1, eta = 1/2,
eta' = 1, nu_1 = 1, exactly as the level is built.  What this does NOT cover: real nested inner runs, extensive
outer blocks beyond the sizes below, the failure probabilities e^{-Theta(n)} (delta enters only through K here).

The level (Q_REPORT l.386-391):  n_o = floor((xhat - 1 - c_log(n))/h), lam = 1, eta = 1/2, eta' = 1, nu_1 = 1, b = 1,
theta = e^{xhat-1} - (3e+1) - (2p_u)^n/e,  ladder x_0 = 2 u n_i > x_1 = min(ceil(xhat), ceil(2 u n_i) - 1) > ... > 1.
Inner costs charged per call: the saturating family C_l = exp(n_i a) (sigma = 0), as numbers (40 digits).

usage: python3 r17_sim_slope.py <budget seconds> [seed] [which: all|u1|u2|uhalf|tiny|smoke]
"""
import math
import os
import resource
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "ws_R6"))      # the science division's own R6 engine
import numpy as np            # noqa: E402
import mpmath as mp           # noqa: E402
import r6lib as R6            # noqa: E402
import instances as I         # noqa: E402
import checks as CK           # noqa: E402
import r17_formula as F       # noqa: E402

mp.mp.dps = 40


def slope_level(u, n, xhat, delta):
    """Params2LP of the level as built at accuracy xhat (must be >= X_0(n) and <= h n), and the design checks."""
    C = F.Cube(u)
    X0 = 1 + F.c_log(C, n) + C.h
    assert xhat >= X0 and xhat <= C.h * n + 1e-12, (xhat, X0, C.h * n)
    n_o = math.floor((xhat - 1 - F.c_log(C, n)) / C.h)
    n_i = n - n_o
    e = mp.e
    um = mp.mpf(u)
    xh = mp.mpf(xhat)
    theta = e ** (xh - 1) - (3 * e + 1) - (2 / (1 + e ** um)) ** n / e
    x1 = min(math.ceil(xhat), math.ceil(2 * u * n_i) - 1)
    xs = [2 * um * n_i] + [mp.mpf(v) for v in range(x1, 0, -1)]
    cost = e ** (mp.mpf(n_i) * mp.mpf(C.a))
    P = R6.Params2LP(n, n_o, u, lam=1, eta=Fraction(1, 2), etap=1, theta=theta, nu1=1, b=1, delta=delta,
                     xs=xs, costs=[cost] * (len(xs) - 1))
    chk = {}
    chk['xout_err'] = float(abs(P.x_out - xh))
    r1 = min(n_o - 1, math.floor(C.rho_h * n_o) + 1)
    chk['rdag'] = P.rdag
    chk['r1'] = r1
    chk['Q4_radius_ok'] = P.rdag >= r1
    chk['Q4_slack'] = float(n_o * C.h + math.log(n_o + 1) + mp.log(P.pidag))      # ln(1/pi) <= n_o h + ln(n_o+1)
    PM = math.log(P.J + 1) + math.log(24 * math.e * (math.e - 1)) + math.log(P.K)
    chk['s41'] = float(xhat - 1 + PM - mp.log(2 * P.Mbar))                        # (4.1)
    Lam = float(mp.log(1 / mp.mpf(delta))) + n * math.log(2)
    chk['K_le_Kbar'] = P.K <= F.Kbar_S(C, n, Lam)
    chk['J1_le_An'] = P.J + 1 <= F.A_n(C, n)
    chk['mmax_ok'] = P.m_max + 1 <= F.mbar_S(C, n)
    # Proposition Q6 with the saturating family (B = a, sigma = 0, R = inf, E = 0):
    # ln C_max <= n a - (a/h - 1) xhat + c_S(n, Lam; a)
    chk['Q6_slack'] = float(n * C.a - (C.a / C.h - 1) * xhat + F.c_S(C, n, Lam, C.a) - mp.log(P.Cmax))
    return C, P, chk


def profiles(n_o, u, rng, rho_h):
    k = max(0, min(n_o, int(round(rho_h * n_o))))
    out = [("flat", I.prof_flat(n_o, u)),
           ("cone", I.prof_cone(n_o, u)),
           ("dip_rho_h", I.prof_dip(n_o, u, k + 1)),
           ("dip_small", I.prof_dip(n_o, u, max(1, k // 2))),
           ("dip_large", I.prof_dip(n_o, u, min(n_o, 2 * k + 2))),
           ("plateau_cone", I.prof_plateau_cone(n_o, u, k)),
           ("flattened_cone", I.prof_flattened_cone(n_o, u, k)),
           ("equal_mass", I.prof_equal_mass(n_o, u)),
           ("rw_uniform", I.prof_random_walk(n_o, u, rng, "uniform")),
           ("rw_pm", I.prof_random_walk(n_o, u, rng, "pm")),
           ("rw_down", I.prof_random_walk(n_o, u, rng, "down")),
           ("half_cone", I.prof_cone(n_o, u, slope=u / 2))]
    return out


VALID = [("center", (R6.S_CENTER,)), ("top", (R6.S_TOP,)), ("bottom", (R6.S_BOTTOM,)), ("adv_hi", (R6.S_ADV_HI,)),
         ("adv_lo", (R6.S_ADV_LO,)), ("exact", (R6.S_EXACT,)), ("random", (R6.S_RANDOM,)), ("narrow", (R6.S_NARROW,)),
         ("mix", (R6.S_CENTER, R6.S_ADV_HI, R6.S_RANDOM, R6.S_BOTTOM))]
INVALID = [("some_trivial", (R6.S_CENTER, R6.S_TRIVIAL), [mp.mpf("0.99"), mp.mpf("0.01")]),
           ("all_trivial", (R6.S_TRIVIAL,), None),
           ("lazy", (R6.S_LAZY,), None),
           ("inv_above", (R6.S_CENTER, R6.S_INV_ABOVE), [mp.mpf("0.9"), mp.mpf("0.1")]),
           ("inv_below", (R6.S_CENTER, R6.S_INV_BELOW), [mp.mpf("0.9"), mp.mpf("0.1")]),
           ("too_wide", (R6.S_CENTER, R6.S_TOO_WIDE), [mp.mpf("0.9"), mp.mpf("0.1")])]


def main():
    t0 = time.time()
    budget = float(sys.argv[1])
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 17
    which = sys.argv[3] if len(sys.argv) > 3 else "all"
    rng = np.random.default_rng(seed)
    grid = []
    # (u, n, n_o, thin): thin = k keeps every k-th case of the list (12 profiles x (3 valid + 1 invalid oracle))
    if which in ("all", "u1", "smoke"):
        # u = 1: the smallest slope-step level exists at n = 470
        grid += [(1.0, 470, 1, 1), (1.0, 600, 3, 1), (1.0, 1000, 20, 2), (1.0, 1000, 60, 2), (1.0, 2000, 120, 3),
                 (1.0, 2000, 400, 4), (1.0, 600, 8, 2), (1.0, 1000, 5, 3), (1.0, 2000, 30, 4), (1.0, 3000, 1000, 6)]
    if which in ("all", "u2"):
        grid += [(2.0, 202, 1, 1), (2.0, 300, 4, 1), (2.0, 300, 12, 2), (2.0, 600, 25, 2), (2.0, 600, 100, 2),
                 (2.0, 600, 250, 3), (2.0, 1200, 600, 4)]
    if which in ("all", "uhalf"):
        grid += [(0.5, 1700, 1, 2), (0.5, 2500, 3, 3), (0.5, 2500, 40, 3), (0.5, 2500, 250, 4), (0.5, 1700, 6, 4)]
    if which == "tiny":
        # failure probabilities of the kind that is handed down in a nest: delta = 2^-n (K is about 12.5 n);
        # and the outer block of ONE coordinate at u = 1
        grid += [(1.0, 480, 1, 2, None), (1.0, 600, 8, 4, 'tiny'), (1.0, 1000, 60, 6, 'tiny'), (2.0, 300, 12, 4, 'tiny'),
                 (2.0, 600, 100, 6, 'tiny'), (1.0, 2000, 400, 8, 'tiny')]
    if which == "smoke":
        grid = grid[:2]
    grid = [g if len(g) == 5 else g + (None,) for g in grid]
    tot = dict(runs=0, closed=0, abort=0, G=0, det_viol=0, good_viol=0, design_viol=0, skipped=0, valid_runs=0,
               invalid_runs=0, good_and_valid=0, closed_LgtU=0)
    worst = dict(M_over_Mbar=0.0, M_over_Mdag=0.0, calls_over_bound=0.0, used_over_cnt=0.0, count_ineq=0.0,
                 q_over_Cvi=0.0, width_over_xhat=0.0, lnq_over_lnCmax=0.0)
    print("# u n n_o xhat theta=e^... L K J r_dag(r1) ln2Mbar | profile d0 s_in oracle | status G det good | "
          "width/xhat maxM/Mbar maxM/Mdag calls/bound used/cnt q/Cvi lnq/lnCmax levels t")
    stop = False
    for (u, n, no_target, thin, dmode) in grid:
        C0 = F.Cube(u)
        xhat = 1 + F.c_log(C0, n) + C0.h * (no_target + 0.5)
        if xhat > C0.h * n:
            print("# skipped (xhat > h n): u=%g n=%d n_o=%d" % (u, n, no_target))
            tot['skipped'] += 1
            continue
        for delta in ((mp.mpf(2) ** (-n),) if dmode == 'tiny' else (0.05,)):
            C, P, chk = slope_level(u, n, xhat, delta)
            if dmode == 'tiny':
                print("## delta = 2^-%d" % n)
            assert P.n_o == no_target, (P.n_o, no_target)
            design_ok = (chk['xout_err'] < 1e-30 and chk['Q4_radius_ok'] and chk['Q4_slack'] >= -1e-12
                         and chk['s41'] >= -1e-12 and chk['K_le_Kbar'] and chk['J1_le_An'] and chk['mmax_ok']
                         and chk['Q6_slack'] >= -1e-9)
            if not design_ok:
                tot['design_viol'] += 1
            print("## level u=%g n=%d n_o=%d n_i=%d xhat=%.4f ln(theta)=%.3f L=%d K=%d J=%d m_max=%d r_dag=%d (r1=%d, "
                  "rho_h n_o=%.2f, p_u n_o=%.2f) ln(1/pi)=%.3f (<= n_o h + ln(n_o+1) = %.3f) ln 2Mbar=%.2f (4.1) slack %.2f "
                  "|x_out - xhat|=%.1e ln C_max=%.2f Q6 slack %.2f  design ok: %s"
                  % (u, n, P.n_o, P.n_i, xhat, float(mp.log(P.theta)), P.L, P.K, P.J, P.m_max, P.rdag, chk['r1'],
                     C.rho_h * P.n_o, C.p * P.n_o, float(-mp.log(P.pidag)), P.n_o * C.h + math.log(P.n_o + 1),
                     float(mp.log(2 * P.Mbar)), chk['s41'], chk['xout_err'], float(mp.log(P.Cmax)), chk['Q6_slack'],
                     design_ok))
            profs = profiles(P.n_o, u, rng, C.rho_h)
            cases = []
            for pi, (pname, Fp) in enumerate(profs):
                for oi, (oname, strats) in enumerate(VALID):
                    # a spread, not the full product: every profile with 3 valid oracles (rotating)
                    if (pi + oi) % 3 != 0:
                        continue
                    d0 = 0 if (pi + oi) % 2 == 0 else P.n_o // 2
                    s_in = 0.0 if (pi + oi) % 4 < 2 else u / 2
                    cases.append((pname, Fp, d0, s_in, oname, strats, None, True))
                ii = pi % len(INVALID)
                oname, strats, wts = INVALID[ii]
                cases.append((pname, Fp, 0, u / 3, oname, strats, wts, False))
            cases = cases[::thin]
            for (pname, Fp, d0, s_in, oname, strats, wts, valid) in cases:
                if time.time() - t0 > budget:
                    stop = True
                    break
                inst = I.radial(n, P.n_o, u, Fp, d0=d0, s_in=s_in, strats=strats, weights=wts, name=pname)
                tr = time.time()
                try:
                    run = R6.Run(P, inst, R6.SimOracle(P.xs, rng), rng).run()
                except AssertionError as ex:      # the engine's sampler refuses blocks beyond 2^83 points
                    print("# skipped (%s): %s %s" % (ex, pname, oname))
                    tot['skipped'] += 1
                    continue
                ck = CK.check_2LP(run)
                tot['runs'] += 1
                tot['valid_runs' if valid else 'invalid_runs'] += 1
                tot['closed'] += run.status == "closed"
                tot['closed_LgtU'] += run.status == "closed_L>U"
                tot['abort'] += run.status == "abort"
                tot['G'] += bool(ck['G'])
                tot['good_and_valid'] += bool(ck['G']) and valid
                tot['det_viol'] += len(ck['det']) > 0
                tot['good_viol'] += (len(ck['good']) > 0) if ck['G'] else 0
                width = float(run.result[1] - run.result[0]) if run.status == "closed" else float('nan')
                rr = ck['ratios']
                if run.status == "closed":
                    worst['width_over_xhat'] = max(worst['width_over_xhat'], width / xhat)
                for key in ('M_over_Mbar', 'M_over_Mdag', 'calls_over_bound', 'used_over_cnt', 'count_ineq',
                            'q_over_Cvi', 'lnq_over_lnCmax'):
                    if key in rr and (ck['G'] or key in ('M_over_Mbar', 'M_over_Mdag', 'lnq_over_lnCmax')):
                        worst[key] = max(worst[key], rr[key])
                print("%g %d %d | %-14s d0=%-3d s_in=%-5.3g %-12s | %-10s G=%d det=%d good=%d | %.4f %.3e %.3e %s %s %s %.4f "
                      "lev=%d %.1fs%s"
                      % (u, n, P.n_o, pname, d0, s_in, oname, run.status, ck['G'], len(ck['det']),
                         len(ck['good']) if ck['G'] else -1, width / xhat if width == width else float('nan'),
                         rr['M_over_Mbar'], rr['M_over_Mdag'],
                         ("%.3e" % rr['calls_over_bound']) if 'calls_over_bound' in rr else "-",
                         ("%.3e" % rr['used_over_cnt']) if 'used_over_cnt' in rr else "-",
                         "%.3e" % rr['q_over_Cvi'], rr['lnq_over_lnCmax'], len(run.levels), time.time() - tr,
                         ("  ABORT: " + str(run.abort_reason)) if run.status == "abort" else ""))
                if ck['det']:
                    print("   DET VIOLATION: %s" % (ck['det'][:3],))
                if ck['G'] and ck['good']:
                    print("   GOOD-EVENT VIOLATION: %s" % (ck['good'][:3],))
                sys.stdout.flush()
            if stop:
                break
        if stop:
            print("# time budget reached; remaining configurations not run")
            break
    print("\nSUMMARY: runs %d (valid inner oracle %d, invalid %d); closed %d, closed with L>U %d, aborted %d; the events "
          "(V1)-(V3) held in %d runs (%d of them with a valid oracle); violations of statements claimed for EVERY run: %d; "
          "violations of statements claimed on the good event: %d; design-level violations (x_out, Lemma Q4, (4.1), "
          "constants, Prop Q6): %d; skipped %d"
          % (tot['runs'], tot['valid_runs'], tot['invalid_runs'], tot['closed'], tot['closed_LgtU'], tot['abort'],
             tot['G'], tot['good_and_valid'], tot['det_viol'], tot['good_viol'], tot['design_viol'], tot['skipped']))
    print("WORST RATIOS: " + ", ".join("%s=%.4g" % kv for kv in worst.items()))
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
    print("LAST LINE r17_sim_slope.py %s seed %d: completed%s; wall %.1f s; peak RSS %.1f MB"
          % (which, seed, " (budget reached)" if stop else "", time.time() - t0, rss))


if __name__ == "__main__":
    main()
