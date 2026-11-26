#!/usr/bin/env python3
"""R17: the outer loop of a DROP level of Q_REPORT section 4.2 (the variant "without shift", n_o = floor(phi n)),
run literally with the science division's R6 engine and a simulated inner oracle, at small sizes.
The level (Q_REPORT l.455-465): phi = R/(a+R), lam = eta = eta' = theta = c, nu_1 = 2 e^u n_o / c, b = beta = alpha - w(c),
ladder x_0 = 2 u n_i > x_1 = ceil(R n_i) > ... > 1 > beta.  Here: epoch 0, i.e. R = h/J_0, c = c_0 = 1/26 (eps = 1),
alpha = 1.  This is a bounded level (the kind workstream K and our R6 simulated with other constants); it is run
here only so that both kinds of level of the schedule have been executed as built.
usage: python3 r17_sim_drop.py <budget seconds> [seed]"""
import math, os, resource, sys, time
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "ws_R6"))
import numpy as np
import mpmath as mp
import r6lib as R6
import instances as I
import checks as CK
import r17_formula as F
import r17_sim_slope as S

mp.mp.dps = 40


def drop_level(u, n, delta):
    C = F.Cube(u)
    d, J, k, B, Rm, phi = C.epochs(1)
    R, ph = Rm[0], phi[0]
    cF = Fraction(1, 26)
    c = 1.0 / 26
    alpha = 1.0
    beta = alpha - F.w_of_c(c)
    assert n >= F.nD_prime(C, c)
    n_o = math.floor(ph * n)
    assert n_o >= 1
    n_i = n - n_o
    x1 = math.ceil(R * n_i)
    xs = [mp.mpf(2 * u) * n_i] + [mp.mpf(v) for v in range(x1, 0, -1)] + [mp.mpf(beta)]
    cost = mp.e ** (mp.mpf(n_i) * mp.mpf(C.a))
    cm = mp.mpf(1) / 26
    P = R6.Params2LP(n, n_o, u, lam=cm, eta=cF, etap=cm, theta=cm, nu1=2 * mp.e ** mp.mpf(u) * n_o / cm, b=beta, delta=delta,
                     xs=xs, costs=[cost] * (len(xs) - 1))
    chk = dict(acc_ok=float(P.x_out) <= alpha + 1e-12, xout=float(P.x_out),
               Q3_slack=float(n_o * C.a + F.cpi_bar(C, n_o, F.ell_c(C, c)) + mp.log(P.pidag)))
    return C, P, chk, alpha


def main():
    t0 = time.time()
    budget = float(sys.argv[1])
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 21
    rng = np.random.default_rng(seed)
    tot = dict(runs=0, valid=0, closed=0, abort=0, G=0, det=0, good=0, design=0)
    worst = dict(M_over_Mbar=0.0, M_over_Mdag=0.0, calls_over_bound=0.0, used_over_cnt=0.0, count_ineq=0.0, width=0.0)
    stop = False
    for (u, n, thin) in ((1.0, 40, 3), (1.0, 100, 4), (2.0, 30, 3), (1.0, 250, 6), (2.0, 80, 6), (1.0, 600, 12)):
        C, P, chk, alpha = drop_level(u, n, 0.05)
        ok = chk['acc_ok'] and chk['Q3_slack'] >= -1e-12
        tot['design'] += not ok
        print("## drop level u=%g n=%d n_o=%d n_i=%d c=1/26 beta=%.4f x_out=%.4f (<= alpha = %g) L=%d K=%d J=%d m_max=%d r_dag=%d "
              "(p_u n_o=%.2f) ln(1/pi)=%.3f Lemma Q3 slack %.2f ln 2Mbar=%.2f ln C_max=%.2f design ok: %s"
              % (u, n, P.n_o, P.n_i, float(P.b), chk['xout'], alpha, P.L, P.K, P.J, P.m_max, P.rdag, C.p * P.n_o,
                 float(-mp.log(P.pidag)), chk['Q3_slack'], float(mp.log(2 * P.Mbar)), float(mp.log(P.Cmax)), ok))
        sys.stdout.flush()
        profs = S.profiles(P.n_o, u, rng, C.rho_h)
        cases = []
        for pi, (pname, Fp) in enumerate(profs):
            for oi, (oname, strats) in enumerate(S.VALID):
                if (pi + oi) % 3 != 0:
                    continue
                d0 = 0 if (pi + oi) % 2 == 0 else P.n_o // 2
                s_in = 0.0 if (pi + oi) % 4 < 2 else u / 2
                cases.append((pname, Fp, d0, s_in, oname, strats, None, True))
            oname, strats, wts = S.INVALID[pi % len(S.INVALID)]
            cases.append((pname, Fp, 0, u / 3, oname, strats, wts, False))
        for (pname, Fp, d0, s_in, oname, strats, wts, valid) in cases[::thin]:
            if time.time() - t0 > budget:
                stop = True
                break
            inst = I.radial(n, P.n_o, u, Fp, d0=d0, s_in=s_in, strats=strats, weights=wts, name=pname)
            tr = time.time()
            run = R6.Run(P, inst, R6.SimOracle(P.xs, rng), rng).run()
            ck = CK.check_2LP(run)
            tot['runs'] += 1
            tot['valid'] += valid
            tot['closed'] += run.status == "closed"
            tot['abort'] += run.status == "abort"
            tot['G'] += bool(ck['G'])
            tot['det'] += len(ck['det']) > 0
            tot['good'] += (len(ck['good']) > 0) if ck['G'] else 0
            width = float(run.result[1] - run.result[0]) if run.status == "closed" else float('nan')
            rr = ck['ratios']
            if run.status == "closed" and valid:
                worst['width'] = max(worst['width'], width)
            for key in ('M_over_Mbar', 'M_over_Mdag', 'calls_over_bound', 'used_over_cnt', 'count_ineq'):
                if key in rr:
                    worst[key] = max(worst[key], rr[key])
            print("%g %d %d | %-14s d0=%-3d s_in=%-5.3g %-12s | %-10s G=%d det=%d good=%d | width %.4f maxM/Mbar %.3e maxM/Mdag %.3e "
                  "lev=%d %.1fs%s" % (u, n, P.n_o, pname, d0, s_in, oname, run.status, ck['G'], len(ck['det']),
                                     len(ck['good']) if ck['G'] else -1, width, rr['M_over_Mbar'], rr['M_over_Mdag'],
                                     len(run.levels), time.time() - tr,
                                     ("  ABORT: " + str(run.abort_reason)) if run.status == "abort" else ""))
            if ck['det']:
                print("   DET VIOLATION: %s" % (ck['det'][:3],))
            if ck['G'] and ck['good']:
                print("   GOOD-EVENT VIOLATION: %s" % (ck['good'][:3],))
            sys.stdout.flush()
        if stop:
            print("# time budget reached; remaining configurations not run")
            break
    print("\nSUMMARY (drop levels): runs %(runs)d (valid oracle %(valid)d); closed %(closed)d, aborted %(abort)d; (V1)-(V3) held in "
          "%(G)d; runs violating an every-run claim: %(det)d; a good-event claim: %(good)d; design-level violations: %(design)d" % tot)
    print("WORST: " + ", ".join("%s=%.4g" % kv for kv in worst.items()) + "  (width is in nats; alpha = 1)")
    print("LAST LINE r17_sim_drop.py seed %d: completed%s; wall %.1f s; peak RSS %.1f MB"
          % (seed, " (budget reached)" if stop else "", time.time() - t0,
             resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))


if __name__ == "__main__":
    main()
