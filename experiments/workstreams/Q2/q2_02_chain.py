#!/usr/bin/env python3
"""Workstream Q2, check 2: the chain T, exactly.  The certified cost of T[G'; alpha, m] in dimension d is computed by
the recursion over the chain (levels in dimensions d, d - m, d - 2m, ..., each with the exact constants of
Theorem 11.56 for its own failure probability; below d_0 the base family at the accuracy alpha_low) and compared
with the closed bound  d B' + E_T(d; Lam)  of Proposition T.

Part A  G' saturating: cost exactly d B' + E (E = 0 and three error functions).  u in {1/2, 1, 2}; exponents B'
        along the epoch schedule (and a, for the base); alpha in {1, 0.1, 0.001}; horizons N = 10^3 ... 10^6;
        d = N and smaller; delta from 0.5 to e^{-d}; the block of the design, and half / twice that block.
Part B  the real base family under the chain: G_0 = T[base at accuracy X_B(N); alpha]  against  d a + E_T with E = E_frakB.
Part C  drop and chain together: T[D'[F; phi, X_D]; alpha] with F saturating of slope one on (0, R]
        (cost exactly d B - min(x, R d)), against  d B' + c_D' + A_T  (Propositions D' and T composed).

usage: python3 q2_02_chain.py A > out_q2_02_chain_A.txt          (4 minutes)
       python3 q2_02_chain.py B C > out_q2_02_chain_BC.txt      (about 15 minutes)
"""
import math
import sys
import time

import numpy as np

import q2lib as L

Q = L.Q
LN2 = L.LN2
INF = L.INF
t0 = time.time()

EFUNS = {
    'E=0': None,
    'E=3sqrt(d)': lambda d, x, Lam: 3 * math.sqrt(d),
    'E=Lam/7': lambda d, x, Lam: Lam / 7,
    'E=5/x+ln(Lam)': lambda d, x, Lam: 5 / x + math.log(Lam),
}

PARTS = [a.upper() for a in sys.argv[1:]] or ['A', 'B', 'C']
print("# Workstream Q2, check 2: the chain T by exact recursion against the closed bound of Proposition T   (parts %s)" % ", ".join(PARTS))

# ------------------------------------------------------------------------------------------------ Part A
if 'A' in PARTS:
    print("\n# Part A: chain on a saturating flat family G' (cost d B' + E)")
    print("#  u  e  B'/a  alpha   N   block m (design)  levels j(N)  d_0  c   | exact - N B'   A_T   bound - exact (delta = 0.05, E = 0, d = N)"
          "   | least slack over all (d, delta, E, block)   chains evaluated   levels evaluated")
    tot_ch = tot_lev = tot_viol = ninside = 0
    gmin = (INF, None)
    for u in (0.5, 1.0, 2.0):
        ev = L.Ev(u)
        cu = ev.cu
        seq = Q.epoch_seq(cu, 13)
        for e in (0, 1, 2, 4, 8, 12):
            Bp = seq['B'][e] if e >= 1 else cu.a
            for alpha in (1.0, 0.1, 0.001):
                for N in (1000, 10000, 100000, 1000000):
                    calX = L.X_D(cu, N, seq['phi'][e - 1]) if e >= 1 else L.X_B(cu, N)
                    m0 = L.Chain.design_m(cu, N, Bp, calX, alpha, math.log(20.0) + N * LN2)
                    rowmin = (INF, None)
                    nch = nlev = 0
                    show = None
                    for m in sorted(set([m0, max(1, m0 // 2), 2 * m0])):
                        ch = L.Chain(cu, N, Bp, calX, alpha, m)
                        if ch.d0 > N:
                            continue
                        ds = sorted(set([N, N - 1, (N + ch.d0) // 2, ch.d0 + 3 * m + 1, ch.d0 + 1, ch.d0]))
                        ds = [d for d in ds if ch.d0 <= d <= N]
                        for d in ds:
                            for ld in (math.log(0.5), math.log(0.05), -float(d)):
                                for ename, ef in EFUNS.items():
                                    if ename != 'E=0' and (ld != -float(d) or d != ds[-1]):
                                        continue
                                    Gp = L.SatLines([(Bp, 0.0)], INF, ef)
                                    t, recs, bottom = ch.exact(ev, d, ld, Gp)
                                    Lam = -ld + d * LN2
                                    bound = d * Bp + ch.E_T(d, Lam, Efun=ef)
                                    nch += 1
                                    nlev += len(recs)
                                    sl = bound - t
                                    if sl < rowmin[0]:
                                        rowmin = (sl, (m, d, round(ld, 2), ename))
                                    if sl < -1e-9:
                                        tot_viol += 1
                                        print("   VIOLATION u=%g e=%d alpha=%g N=%d m=%d d=%d ld=%.4g %s: exact %.4f bound %.4f" % (u, e, alpha, N, m, d, ld, ename, t, bound))
                                    # also: levels inside the chain against the bound at their own (d, delta)
                                    # (the last three and about twenty evenly spaced ones: the bound iterates Lam -> Lam + q_T)
                                    step = max(1, len(recs) // 20)
                                    for ir, r in enumerate(recs):
                                        if ir % step != 0 and ir < len(recs) - 3:
                                            continue
                                        Lr = -r['ld'] + r['d'] * LN2
                                        ninside += 1
                                        if r['t'] > r['d'] * Bp + ch.E_T(r['d'], Lr, Efun=ef) + 1e-9:
                                            tot_viol += 1
                                            print("   VIOLATION inside the chain at d=%d" % r['d'])
                                    if m == m0 and d == N and ld == math.log(0.05) and ename == 'E=0':
                                        show = (ch, t, bound)
                    tot_ch += nch
                    tot_lev += nlev
                    if rowmin[0] < gmin[0]:
                        gmin = (rowmin[0], (u, e, alpha, N) + rowmin[1])
                    if show is not None and (alpha == 1.0 or N == 1000000):
                        ch, t, bound = show
                        print("  %.1f %2d %.3f %5g %7d  %6d  %5d  %6d  %.2e | %9.2f  %9.2f  %8.2f | %8.2f at %s  %4d  %6d"
                              % (u, e, Bp / cu.a, alpha, N, ch.m, ch.j(N), ch.d0, ch.c, t - N * Bp, ch.A_T(N, ch.Lam_star(N, math.log(20.0) + N * LN2)),
                                 bound - t, rowmin[0], rowmin[1], nch, nlev))
            sys.stdout.flush()
        print("#  u = %.1f done [%.0f s]; the two evaluators on %d levels: largest difference %.2e, r_dagger/J/K differ on %d"
              % (u, time.time() - t0, ev.nlev, ev.maxdiff, ev.rdag_diff))
    print("# Part A total: %d chains (%d levels) evaluated, %d levels inside chains also compared with the bound at their own (d, delta), %d violations;"
          " least slack %.3f at (u, e, alpha, N, m, d, ln delta, E) = %s" % (tot_ch, tot_lev, ninside, tot_viol, gmin[0], gmin[1]))

# ------------------------------------------------------------------------------------------------ Part B
if 'B' in PARTS:
    print("\n# Part B: the real base family at the accuracy X_B(N) under the chain: G_0 = T[base; alpha]")
    # the two implementations of the base family (qlib.BaseTable, r12lib.Base) at the accuracies X_B: largest difference
    dmax = 0.0
    for u in (0.5, 1.0, 2.0):
        cu = Q.Cube(u)
        st = L.Stat()
        for N in (500, 3000, 20000):
            hb = L.HiBase(cu, N, st, fast=True)
            hq = L.HiBase(cu, N, st, fast=False)
            for d in (1, 2, 7, N // 9, N // 2, N):
                for ld in (math.log(0.05), -float(N)):
                    for x in (hb.xmin, 2 * hb.xmin, 0.3 * u * d + hb.xmin):
                        dmax = max(dmax, abs(float(hb.costs(d, np.array([x]), ld)[0]) - float(hq.costs(d, np.array([x]), ld)[0])))
    print("#  base family: qlib.BaseTable against r12lib.Base on 324 cases: largest difference %.2e" % dmax)
    print("#  u  alpha   N    X_B   m    j(N)  | exact/(N a)   (exact - N a)   bound - exact (delta = 0.05)   | node checks   least slack: induction T, base   viol")
for u in ((0.5, 1.0, 2.0) if 'B' in PARTS else ()):
    ev = L.Ev(u)
    cu = ev.cu
    for alpha in (1.0, 0.01):
        for N in (1000, 4000, 16000, 64000, 256000, 1000000):
            if N == 1000000 and alpha != 1.0:
                continue
            st = L.Stat()
            base = L.HiBase(cu, N, st)
            Lam0 = math.log(20.0) + N * LN2
            G0 = L.ChainFam(ev, base, alpha, N, st, Lam0)
            lds = (math.log(0.05),) if N >= 256000 else (math.log(0.05), -float(N))
            res = []
            for ld in lds:
                v = float(G0.costs(N, np.array([alpha]), ld)[0])
                res.append((v, N * cu.a + G0.Ebound(N, alpha, -ld + N * LN2)))
            v, b = res[0]
            print("  %.1f  %5g %7d  %.2f  %5d  %5d | %.4f  %9.2f  %8.2f | %6d  %8.2f, %8.2f  %d  [%.0f s]"
                  % (u, alpha, N, base.xmin, G0.ch.m, G0.ch.j(N), v / (N * cu.a), v - N * cu.a, b - v, st.total(),
                     st.minslack.get('induction T', (INF,))[0], st.minslack.get('induction base at log accuracy', (INF,))[0], len(st.viol),
                     time.time() - t0))
            for vv in st.viol[:5]:
                print("     VIOLATION:", vv)
            sys.stdout.flush()

# ------------------------------------------------------------------------------------------------ Part C
if 'C' in PARTS:
    print("\n# Part C: T[D'[F; phi_m, X_D]; alpha] with F saturating of slope one on (0, R_m] (cost d B_m - min(x, R_m d))")
    print("#  u  m  alpha   N   X_D   block  j(N) | exact - N B_{m+1}   c_D' + A_T (bound - N B_{m+1})   slack | D' levels built / passed through"
          "   least slack: D' as built, induction T   node checks  viol")


class SatFam(L.SatLines):
    """SatLines with the attributes of a family of type H(B, sigma, R; 0)"""

    def __init__(self, B, s, Rr):
        L.SatLines.__init__(self, [(B, s)], Rr)
        self.B, self.sigma = B, s

    def Ebound(self, d, x, Lam):
        return 0.0


for u in ((0.5, 1.0, 2.0) if 'C' in PARTS else ()):
    ev = L.Ev(u)
    cu = ev.cu
    seq = Q.epoch_seq(cu, 13)
    for m in (0, 2, 6, 11):
        for alpha in (1.0, 0.01):
            for N in (1000, 10000, 100000, 1000000):
                if N == 1000000 and (alpha != 1.0 or m != 6 or u == 2.0):
                    continue
                st = L.Stat()
                F = SatFam(seq['B'][m], 1.0, seq['R'][m])
                D = L.DprimeFam(ev, F, seq['phi'][m], N, st)
                Lam0 = math.log(20.0) + N * LN2
                G = L.ChainFam(ev, D, alpha, N, st, Lam0)
                lds = (math.log(0.05),) if N >= 1000000 else (math.log(0.05), -float(N))
                first = None
                for ld in lds:
                    v = float(G.costs(N, np.array([alpha]), ld)[0])
                    b = N * G.B + G.Ebound(N, alpha, -ld + N * LN2)
                    if first is None:
                        first = (v, b)
                v, b = first
                print("  %.1f %2d %5g %7d  %.2f  %5d %5d | %9.2f  %9.2f  %8.2f | %d / %d   %.2f, %.2f   %d  %d  [%.0f s]"
                      % (u, m, alpha, N, D.calX, G.ch.m, G.ch.j(N), v - N * G.B, b - N * G.B, b - v, D.wins['level'], D.wins['passthrough'],
                         st.minslack.get("D' as built", (INF,))[0], st.minslack.get('induction T', (INF,))[0], st.total(), len(st.viol), time.time() - t0))
                for vv in st.viol[:5]:
                    print("     VIOLATION:", vv)
                sys.stdout.flush()
print("\n# done in %.0f s" % (time.time() - t0))
