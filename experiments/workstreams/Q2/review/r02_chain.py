#!/usr/bin/env python3
"""r02_chain.py -- referee's exact recursion over a chain of Proposition T (own evaluator rlib).

For a chain T[G'; alpha, m] with horizon N started at (d = N, delta): the constants of Theorem 11.56 of every
level are computed top-down (each level has its own delta), the certified costs bottom-up (below d_0 the real
base bracket at the accuracy alpha_low; the coarse rung is served by a SATURATING flat family G' with cost
(d-m) B' + E).  Checked at EVERY level of the chain, at that level's own (d, delta):
  (i)   accuracy of the level <= a_d <= alpha;
  (ii)  ln(1/pi_dagger) <= varpi(m; c), P_cnt <= Pbar_cnt, P_M <= Pbar_M, (2.1) with q_T;
  (iii) ln cost <= d B' + E_T(d; Lam),  Lam = ln(1/delta) + d ln 2  (the claim of the proposition);
and (iv) for the block of the design: Delta_T = 0 and Lam* < Lam + d B'.
"""
import math, sys, time
sys.dont_write_bytecode = True
import numpy as np
import rlib
from rlib import LN2, INF

t0 = time.time()


def run_chain(cu, N, Bp, calX, alpha, m, ld_top, Efun, label, check_every=1, verbose=True):
    u = cu.u
    ch = rlib.Chain(cu, N, Bp, calX, alpha, m)
    c = ch.c
    assert ch.alow > 0 and calX > 1 and Bp <= LN2 and c <= 1 / 13 + 1e-15
    # top-down
    recs = []
    d, ld = N, ld_top
    tab = rlib.tables(u, m, c) if N >= ch.d0 else None
    while d >= ch.d0:
        jd = ch.j(d)
        a_d = ch.alow + jd * ch.w
        b_d = a_d - ch.w
        lev = rlib.Level(u, d, m, c, c, c, math.log(c), 2 * math.exp(u) * m / c, b_d, ld, 2, tab=tab)
        recs.append((d, ld, lev, a_d, b_d))
        d, ld = d - m, lev.ldp
    # bottom
    t, rstar = rlib.base_lcost(cu, d, ch.alow, ld) if d >= 1 else (0.0, -1)
    bottom = (d, ld, t)
    stat = dict(viol=0, minslack=INF, argmin=None, min_varpi=INF, n=0, maxacc=-INF)
    Lam_b = -ld + d * LN2
    # bottom against  d B' + e0
    if d >= 1:
        sl = d * Bp + ch.e0(Lam_b) - t
        stat['bottom_slack'] = sl
        if sl < -1e-9:
            stat['viol'] += 1
    # bottom-up
    for idx in range(len(recs) - 1, -1, -1):
        d, ld, lev, a_d, b_d = recs[idx]
        E1 = 0.0 if Efun is None else Efun(d - m, calX, -lev.ldp + (d - m) * LN2)
        lc1 = (d - m) * Bp + E1
        xs = [calX, b_d]
        t = lev.lcmax(xs, [lc1, t])
        Lam = -ld + d * LN2
        ok = True
        # (i)
        ok &= lev.x_out <= a_d + 1e-12 and a_d <= alpha + 1e-12 and b_d >= ch.alow - 1e-12
        stat['maxacc'] = max(stat['maxacc'], lev.x_out - a_d)
        # (ii)
        vp = rlib.varpi(cu, m, c)
        ok &= -lev.lpi <= vp + 1e-9
        stat['min_varpi'] = min(stat['min_varpi'], vp + lev.lpi)
        ok &= lev.P_cnt <= rlib.Pbar_cnt(cu, d, Lam, c) + 1e-9 and lev.P_M <= rlib.Pbar_M(cu, d, Lam, c) + 1e-9
        ok &= -lev.ldp + (d - m) * LN2 <= Lam + ch.qT(d, Lam) + 1e-9
        ok &= lev.J + 1 <= rlib.A_n(cu, d) / c + 1e-6 and lev.nu0 <= rlib.nubar_D(cu, d, c) * (1 + 1e-12)
        ok &= lev.m_max + 1 <= rlib.mbar_D(cu, d, c) + 1e-9 and lev.K <= rlib.Kbar_D(cu, d, -ld, c) + 1e-6
        # (iii)
        if idx % check_every == 0 or idx >= len(recs) - 3:
            bound = d * Bp + ch.E_T(d, Lam, Efun)
            sl = bound - t
            stat['n'] += 1
            if sl < stat['minslack']:
                stat['minslack'] = sl; stat['argmin'] = (d, round(ld, 2))
            ok &= sl >= -1e-9
        if not ok:
            stat['viol'] += 1
    Lam = -ld_top + N * LN2
    Ls = ch.Lam_star(N, Lam)
    res = dict(m=m, levels=len(recs), c=c, d0=ch.d0, alow=ch.alow, exact=t - N * Bp, A_T=ch.A_T(N, Ls),
               Delta=ch.Delta_T(N, Ls), jDelta=ch.j(N) * ch.Delta_T(N, Ls), bound=ch.E_T(N, Lam, Efun),
               Lam_growth=(Ls - Lam) / (N * Bp), stat=stat, bottom=bottom, varpi=rlib.varpi(cu, m, c),
               lpi_top=-recs[0][2].lpi if recs else None, rd_top=recs[0][2].rd if recs else None)
    if verbose:
        print("%-44s m=%5d levels=%5d c=%.2e d0=%5d | exact-NB'=%9.2f  A_T=%9.2f  j*Delta_T=%8.2f  E_T=%9.2f  slack(top)=%8.2f"
              " | min slack over %d levels checked %8.2f at %s; bottom d=%d slack %.2f; violations %d; varpi=%.1f ln(1/pi)=%.1f"
              % (label, m, len(recs), c, ch.d0, res['exact'], res['A_T'], res['jDelta'], res['bound'], res['bound'] - res['exact'],
                 stat['n'], stat['minslack'], stat['argmin'], bottom[0], stat.get('bottom_slack', float('nan')), stat['viol'],
                 res['varpi'], res['lpi_top'] if res['lpi_top'] is not None else float('nan')), flush=True)
    return res


def main():
    print("# referee: chains of Proposition T by exact recursion (own evaluator)")
    tot_lev = tot_viol = 0
    gmin = INF
    Efs = {"E=0": None, "E=3sqrt(d)": lambda d, x, Lam: 3 * math.sqrt(d), "E=Lam/7": lambda d, x, Lam: Lam / 7}
    for (u, e, alpha, N, ldname, En) in [
            (1.0, 0, 1.0, 10 ** 4, "0.05", "E=0"),
            (1.0, 0, 1.0, 10 ** 6, "0.05", "E=0"),            # the report's row: m = 1099, 909 levels, 126.6 / 230.7
            (2.0, 12, 1.0, 10 ** 6, "0.05", "E=0"),           # the report's row: m = 1119, 893 levels, 426.5 / 729.5
            (0.5, 0, 1.0, 10 ** 6, "0.05", "E=0"),            # the report's row: m = 3759, 266 levels, 111.7 / 181.1
            (1.0, 4, 0.01, 10 ** 5, "e^-N", "E=3sqrt(d)"),
            (0.5, 2, 0.001, 10 ** 5, "0.5", "E=Lam/7"),
            (2.0, 0, 0.1, 3 * 10 ** 4, "e^-N", "E=0"),
            (1.0, 8, 1.0, 10 ** 5, "e^-N", "E=Lam/7")]:
        cu = rlib.Cube(u)
        seq = rlib.epochs(cu, 13)
        Bp = seq['B'][e] if e >= 1 else cu.a
        calX = rlib.X_D(cu, N, seq['phi'][e - 1]) if e >= 1 else rlib.X_B(cu, N)
        ld = {"0.05": math.log(0.05), "0.5": math.log(0.5), "e^-N": -float(N)}[ldname]
        m0 = rlib.Chain.design_m(cu, N, Bp, calX, alpha, -ld + N * LN2)
        for (mm, tag) in ((m0, "design"), (max(1, m0 // 2), "half"), (2 * m0, "double"), (max(1, m0 // 7), "1/7")):
            ch = rlib.Chain(cu, N, Bp, calX, alpha, mm)
            if ch.d0 > N:
                continue
            nlev = ch.j(N)
            r = run_chain(cu, N, Bp, calX, alpha, mm, ld, Efs[En],
                          "u=%.1f B'/a=%.3f a=%g N=%g d=%s %s %s" % (u, Bp / cu.a, alpha, N, ldname, En, tag),
                          check_every=max(1, nlev // 150))
            tot_lev += r['levels']; tot_viol += r['stat']['viol']; gmin = min(gmin, r['stat']['minslack'])
            if tag == "design":
                Lam = -ld + N * LN2
                ok4 = r['Delta'] == 0.0 and ch.Lam_star(N, Lam) < Lam + N * Bp
                print("      (iv) for the block of the design: Delta_T = %.3f, (Lam* - Lam)/(N B') = %.4f  -> %s"
                      % (r['Delta'], r['Lam_growth'], "ok" if ok4 else "VIOLATED"))
                if not ok4:
                    tot_viol += 1
    print("# total: %d levels in the chains evaluated, %d violations, least slack of the claim %.2f nats; %.0f s"
          % (tot_lev, tot_viol, gmin, time.time() - t0))


if __name__ == "__main__":
    main()
