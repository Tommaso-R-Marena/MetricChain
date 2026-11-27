#!/usr/bin/env python3
"""Workstream Q, check 3 -- the nested design G_M of Q_REPORT.md section 4 (epoch schedule): its EXACT certified cost
(Theorem 11.56 applied level by level, every constant from the referee's tables; base brackets of Proposition K0)
against the bound of Theorem Q8,   ln C <= n B_M + E_M(n, eps, delta).

For M epochs the design has k_M nested levels (base + J_m slope steps + one drop per epoch; at u = 1: k_1 = 3,
k_2 = 5).  Two variants are evaluated:
   'proof'  every level is the one built in the proof and nothing else;
   'min'    at every node the procedure with the smallest certified cost among those the proof allows (the level as
            built, the level without the shift of its outer block, the inner procedure itself) -- the rule of
            theory report 11.19, remark (1b).  Its cost is at most that of 'proof', and Theorem Q8 holds for both.
On every node visited the inequality of the induction (cost <= d B - sigma min(x, R d) + error term) is checked, and
Lemma Q3 / Lemma Q4 at every level built.  For comparison: the base family alone and the two-level design of
K_REPORT 6.4 (r8_flat.flat_run, n_o = n/2), whose certified accuracy 0.8715 is the accuracy asked for here.

usage: python3 q3_scheme_exact.py [quick] > out_q3_scheme_exact.txt      (about 40 minutes; 'quick': 4 minutes, no M = 2 above n = 4000)
       python3 q3_scheme_exact.py deep > out_q3_deep.txt                 (M = 3: seven nested levels, n <= 4000)
"""
import math
import sys
import time

import numpy as np

import qlib as Q
import qscheme as S

F = Q.F
EPS = 0.8715
DELTA = 0.05


def one(cu, seq, n, M, minrule):
    t0 = time.time()
    S.reset_check()
    Q._tabs.clear(); Q._tab_order.clear()
    G, levels, alpha = S.build_G(cu, M, EPS, seq, minrule)
    v = float(G.costs(n, np.array([alpha[M]]), math.log(DELTA))[0])
    ck = S.CHECK
    return v, ck, levels, time.time() - t0


def main(quick):
    t00 = time.time()
    print("# Workstream Q, check 3: exact certified cost of the design G_M against Theorem Q8.  eps = %.4f, delta = %.2f" % (EPS, DELTA))
    tot_viol = 0
    for u, ns, Ms in ((1.0, (1000, 1400, 2000, 4000, 8000, 16000, 32000, 64000), (0, 1, 2)),
                      (2.0, (1000, 4000, 16000), (0, 1)),
                      (0.5, (4000, 16000, 64000), (0, 1))):
        cu = Q.Cube(u)
        seq = Q.epoch_seq(cu, 3)
        a = cu.a
        print()
        print("# u = %.1f: a = %.6f, h = %.6f, h/a = %.4f;  B_M/a = %s;  levels k_M = %s;  J_m = %s"
              % (u, a, cu.h, cu.h / a, ", ".join("%.4f" % (b / a) for b in seq['B'][:3]), seq['k'][:3], seq['J'][:2]))
        print("#      n   M  levels   exact 'proof'   exact 'min'    Theorem Q8     n B_M     | in units of n a: proof    min     bound    B_M/a  |  bound - exact(min)   nodes checked   violations   least slack: induction / Lemma Q3 / Lemma Q4   time")
        for n in ns:
            ref2 = F.flat_run(u, n, 0.5)['lCmax'] if u == 1.0 else float('nan')
            for M in Ms:
                if M == 2 and (n > 16000 or (quick and n > 4000)):
                    continue
                E = Q.E_total(cu, n, EPS, math.log(1 / DELTA), M, seq)
                bound = n * seq['B'][M] + E
                res = {}
                for minrule in (False, True):
                    if M == 0 and not minrule:
                        continue
                    v, ck, levels, dt = one(cu, seq, n, M, minrule)
                    ind = min([s[1] for k, s in ck.by.items() if 'Lemma' not in k] + [float('inf')])
                    q3 = ck.by.get('D: Lemma Q3', [0, float('inf'), 0])[1]
                    q4 = ck.by.get('S: Lemma Q4', [0, float('inf'), 0])[1]
                    res[minrule] = (v, ck.n, ck.viol, ind, q3, q4, dt, levels)
                    tot_viol += ck.viol
                    assert v <= bound + 1e-9
                vm = res[True][0]
                vp = res[False][0] if False in res else vm
                nodes = sum(r[1] for r in res.values())
                nv = sum(r[2] for r in res.values())
                ind = min(r[3] for r in res.values())
                q3 = min(r[4] for r in res.values())
                q4 = min(r[5] for r in res.values())
                dt = sum(r[6] for r in res.values())
                print("%8d   %d   %3d    %10.2f     %10.2f    %10.2f   %9.2f   |              %.4f   %.4f   %.4f   %.4f  |     %9.2f        %8d        %3d          %8.2f / %8.2f / %6.2f        %5.0f s"
                      % (n, M, seq['k'][M], vp, vm, bound, n * seq['B'][M], vp / (n * a), vm / (n * a), bound / (n * a), seq['B'][M] / a,
                         bound - vm, nodes, nv, ind, q3, q4, dt), flush=True)
                # which candidate the top level uses, and where its maximum sits
                if M >= 1:
                    D = res[True][7][-1]
                    for key, inf in D.info.items():
                        if key[0] == n and 'n_o' in inf:
                            am = inf['argmax']
                            where = "outer sample" if am == 0 else "rung %d of %d at accuracy %.2f" % (am, inf['L'], inf['x_argmax'])
                            print("#            top drop ('min'): %s; n_o = %d, r_dag = %d, K = %d, ln 2Mbar = %.1f, ln(1/delta') = %.1f; largest term: %s; candidates %s"
                                  % (inf['winner'], inf['n_o'], inf['rdag'], inf['K'], inf['lMbar'] + Q.LN2, -inf['ldeltap'], where,
                                     {k: round(v, 1) for k, v in inf['cands'].items()}))
                        elif key[0] == n:
                            print("#            top drop ('min'): pass-through (%s)" % {k: round(v, 1) for k, v in inf['cands'].items()})
            if u == 1.0:
                print("#            [two-level design of K_REPORT 6.4 at n_o = n/2 (r8_flat.flat_run): ln C_max = %.2f = %.4f n a]" % (ref2, ref2 / (n * a)))
    print()
    print("violations of proved inequalities: %d   [%.0f s]" % (tot_viol, time.time() - t00))


def deep():
    """three epochs: seven nested levels at u = 1 and u = 2 (J_0 = J_1 = J_2 = 1), at the sizes where the direct
    recursion is still feasible"""
    t00 = time.time()
    print("# Workstream Q, check 3 (deep): exact certified cost of G_3 (seven nested levels) against Theorem Q8.  eps = %.4f, delta = %.2f" % (EPS, DELTA))
    tot_viol = 0
    for u, ns in ((1.0, (1000, 2000, 4000)), (2.0, (1000, 2000))):
        cu = Q.Cube(u)
        seq = Q.epoch_seq(cu, 4)
        a = cu.a
        print()
        print("# u = %.1f: a = %.6f, h = %.6f;  B_M/a = %s;  levels k_M = %s;  J_m = %s"
              % (u, a, cu.h, ", ".join("%.4f" % (b / a) for b in seq['B'][:4]), seq['k'][:4], seq['J'][:3]))
        print("#      n   M  levels   exact 'min'    Theorem Q8     n B_M   | in units of n a:  min     bound    B_M/a  |  nodes checked   violations   least slack: induction / Lemma Q3 / Lemma Q4   levels built (S, D with shift, D without shift, pass-through of drops)   time")
        for n in ns:
            for M in (2, 3):
                E = Q.E_total(cu, n, EPS, math.log(1 / DELTA), M, seq)
                bound = n * seq['B'][M] + E
                v, ck, levels, dt = one(cu, seq, n, M, True)
                tot_viol += ck.viol
                assert v <= bound + 1e-9
                ind = min([s[1] for k, s in ck.by.items() if 'Lemma' not in k] + [float('inf')])
                q3 = ck.by.get('D: Lemma Q3', [0, float('inf'), 0])[1]
                q4 = ck.by.get('S: Lemma Q4', [0, float('inf'), 0])[1]
                nS = sum(l.nconstruct for l in levels if isinstance(l, S.SLevel))
                wins = [0, 0, 0]
                for l in levels:
                    if isinstance(l, S.DLevel):
                        wins[0] += l.wins['shift']; wins[1] += l.wins['noshift']; wins[2] += l.wins['passthrough']
                print("%8d   %d   %3d    %10.2f    %10.2f   %9.2f |                %.4f   %.4f   %.4f  |   %9d        %3d          %8.2f / %8.2f / %6.2f          %d, %d, %d, %d      %5.0f s"
                      % (n, M, seq['k'][M], v, bound, n * seq['B'][M], v / (n * a), bound / (n * a), seq['B'][M] / a, ck.n, ck.viol, ind, q3, q4,
                         nS, wins[0], wins[1], wins[2], dt), flush=True)
    print()
    print("violations of proved inequalities: %d   [%.0f s]" % (tot_viol, time.time() - t00))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'deep':
        deep()
    else:
        main(len(sys.argv) > 1 and sys.argv[1] == 'quick')
