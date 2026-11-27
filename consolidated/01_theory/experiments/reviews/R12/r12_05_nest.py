#!/usr/bin/env python3
"""Referee R12, check 5: the nested design G_M of Q_REPORT 5.1, evaluated exactly with own code (r12lib), against
(i) the bound  n B_M + E_M  of Theorem Q8 (own evaluator of (5.2)), (ii) the induction inequality H(B, sigma, R; E^(t))
at every node visited, (iii) the bounds of Propositions Q6 / Q7 at every level built with the real families inside,
(iv) Lemma Q3 / Lemma Q4 at every level built, and (v) the numbers printed in Q_REPORT 7.3 (typed in below).

'proof': every level is the level as built (slope step where xhat >= X_0, drop with shift where it is defined) and
         nothing else;   'min': the design as defined (the cheapest admissible procedure at every node).

modes (argv[1]):
  A      u = 1, eps = 0.8715, delta = 0.05, n = 1000 ... 64000: M = 0, 1 (both variants), M = 2 up to n = 8000
  B      awkward sizes: every n from 2 to 200, M = 0..3, u in {0.1, 1, 4}, eps in {1e-6, 0.01, 0.8715, 50},
         delta in {0.999, 0.05, 1e-9, e^-n}; and the first sizes at which slope steps are built
  D      seven levels (M = 3) at n = 1000, 2000, 4000 (u = 1) and n = 1000, 2000 (u = 2); u = 2, n = 16000, M <= 1;
         u = 1/2, n = 16000, 64000, M <= 1
  E      extremes at medium sizes: eps from 1e-4 to 50, delta from 0.999 to e^{-100 n}, u in {0.1, 1, 4}
  big    u = 1, n = 16000, M = 2 (min only; about a quarter of an hour)
usage: python3 r12_05_nest.py A > out_05_nest_A.txt ;  likewise B, D, E, big  (A: 3 min, B: 0.5 min, D: 2.5 min, E: see output, big: see output)
"""
import sys, os, math, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r12lib import Cube, Formula, Stats, TabCache, build_design, LN2, INF

mode = sys.argv[1] if len(sys.argv) > 1 else 'A'
t00 = time.time()
tot_nodes = 0
tot_viol = 0


def run(cu, n, eps, ld, M, only_built=False, tabs=None):
    """returns dict(cost, bound, nodes, viol, slacks, top)"""
    global tot_nodes, tot_viol
    t0 = time.time()
    fam, fams, fm, st = build_design(cu, eps, M, only_built=only_built, tabs=tabs)
    eh = min(eps, 1.0)
    cost = fam.cost(n, eh, ld)
    E, B, k = fm.E_total(n, eps, ld, M)
    bound = n * B + E
    if cost > bound + 1e-9:
        st.bad("Theorem Q8: cost %.4f > bound %.4f at n=%d M=%d" % (cost, bound, n, M))
    top = ''
    if M >= 1:
        which, cands = fam.info[(n, ld)]
        top = which + ' {' + ', '.join('%s: %.1f' % (kk, vv) for kk, vv in cands.items()) + '}'
    tot_nodes += st.nodes
    tot_viol += len(st.viol)
    return dict(cost=cost, bound=bound, B=B, k=k, nodes=st.nodes, viol=list(st.viol), st=st, top=top, time=time.time() - t0)


def fmt_slack(st):
    f = lambda v: ('%7.2f' % v) if v < INF else '    inf'
    return "%s /%s /%s /%s /%s /%s" % (f(st.min_ind), f(st.min_q6), f(st.min_q7), f(st.min_q7ns), f(st.min_q3), f(st.min_q4))


print("# Referee R12, check 5 (mode %s): exact certified cost of the design G_M against Theorem Q8 and the induction" % mode)

if mode == 'A':
    rep = {  # n: (base exact, base bound, M=1 proof, min, bound, M=2 proof, min, bound)   [Q_REPORT 7.3, units of n a]
        1000: (1.349, 1.928, 1.349, 1.349, 3.910, 1.361, 1.361, 5.771), 1400: (1.287, 1.725, 1.287, 1.287, 3.107, 1.288, 1.288, 4.413),
        2000: (1.230, 1.561, 1.230, 1.196, 2.486, 1.231, 1.196, 3.369), 4000: (1.152, 1.348, 1.152, 1.033, 1.726, 1.154, 1.014, 2.103),
        8000: (1.101, 1.221, 1.093, 0.938, 1.322, 1.120, 0.849, 1.437), 16000: (1.069, 1.143, 0.974, 0.883, 1.110, 0.918, 0.756, 1.102),
        32000: (1.047, 1.095, 0.906, 0.850, 0.987, None, None, None), 64000: (1.033, 1.064, 0.864, 0.830, 0.915, None, None, None)}
    cu = Cube(1.0)
    eps, ld = 0.8715, math.log(0.05)
    print("# u = 1, eps = %.4f, delta = 0.05;  a = %.6f, h = %.6f" % (eps, cu.a, cu.h))
    print("#      n  M  levels | in units of n a:  proof     min      bound    | report: proof, min, bound | agree | nodes checked (proof+min)  violations |"
          " least slack: induction / Q6 level / Q7 shift / Q7 no shift / Lemma Q3 / Lemma Q4 | top drop of 'min' | time")
    ndiff = 0
    for n in (1000, 1400, 2000, 4000, 8000, 16000, 32000, 64000):
        for M in (0, 1, 2):
            if M == 2 and n > 8000:
                continue
            rp = run(cu, n, eps, ld, M, only_built=True)
            rm = run(cu, n, eps, ld, M, only_built=False)
            na = n * cu.a
            r = rep[n]
            want = (r[0], r[0], r[1]) if M == 0 else ((r[2], r[3], r[4]) if M == 1 else (r[5], r[6], r[7]))
            got = (rp['cost'] / na, rm['cost'] / na, rm['bound'] / na)
            ok = all(abs(g - w) <= 1.001e-3 for g, w in zip(got, want))
            ndiff += (not ok)
            st = rm['st']
            stp = rp['st']
            for attr in ('min_ind', 'min_q6', 'min_q7', 'min_q7ns', 'min_q3', 'min_q4'):
                setattr(st, attr, min(getattr(st, attr), getattr(stp, attr)))
            print("  %6d  %d  %3d    |                 %.4f   %.4f   %.4f   | %s | %s | %8d  %d | %s | %s | %.0f s"
                  % (n, M, rm['k'], got[0], got[1], got[2], want, 'yes' if ok else 'NO', rp['nodes'] + rm['nodes'],
                     len(rp['viol']) + len(rm['viol']), fmt_slack(st), rm['top'], rp['time'] + rm['time']))
            for v in (rp['viol'] + rm['viol'])[:5]:
                print("       VIOLATION: " + v)
            sys.stdout.flush()
    print("# rows that differ from the report by more than one unit of the last digit: %d" % ndiff)

elif mode == 'big':
    cu = Cube(1.0)
    eps, ld = 0.8715, math.log(0.05)
    n, M = 16000, 2
    rm = run(cu, n, eps, ld, M, only_built=False)
    na = n * cu.a
    print("  u = 1, n = %d, M = %d: min %.4f, bound %.4f (report: 0.756, 1.102); nodes %d, violations %d; slacks %s; top: %s; %.0f s"
          % (n, M, rm['cost'] / na, rm['bound'] / na, rm['nodes'], len(rm['viol']), fmt_slack(rm['st']), rm['top'], rm['time']))
    for v in rm['viol'][:5]:
        print("       VIOLATION: " + v)

elif mode == 'D':
    print("#   u      n  M  levels | min/(na)  bound/(na) | report: min, bound | agree | nodes  violations | least slack: induction / Q6 / Q7 shift / Q7 no shift / Q3 / Q4"
          " | levels built: S, D shift, D no shift, D passed | time")
    cases = [(1.0, 1000, 2, (1.361, 5.771)), (1.0, 1000, 3, (1.361, 7.489)), (1.0, 2000, 2, (1.196, 3.369)), (1.0, 2000, 3, (1.202, 4.195)),
             (1.0, 4000, 3, (1.015, 2.466)), (2.0, 1000, 2, (1.113, 5.208)), (2.0, 1000, 3, (1.113, 6.379)), (2.0, 2000, 2, (0.907, 2.925)),
             (2.0, 2000, 3, (0.889, 3.453)), (2.0, 16000, 1, (0.826, 1.009)), (0.5, 16000, 1, None), (0.5, 64000, 1, None)]
    ndiff = 0
    for (u, n, M, want) in cases:
        cu = Cube(u)
        rm = run(cu, n, 0.8715, math.log(0.05), M)
        na = n * cu.a
        got = (rm['cost'] / na, rm['bound'] / na)
        ok = want is None or all(abs(g - w) <= 1.001e-3 for g, w in zip(got, want))
        ndiff += (not ok)
        b = rm['st'].built
        print("  %.1f  %6d  %d  %3d    | %.4f    %.4f    | %s | %s | %8d  %d | %s | %d, %d, %d, %d | %.0f s"
              % (u, n, M, rm['k'], got[0], got[1], want, 'yes' if ok else 'NO', rm['nodes'], len(rm['viol']), fmt_slack(rm['st']),
                 b['S'], b['Dshift'], b['Dnoshift'], b['Dpass'], rm['time']))
        for v in rm['viol'][:5]:
            print("       VIOLATION: " + v)
        sys.stdout.flush()
    # the 'proof' variant of u = 2, n = 16000, M = 1 (report: 0.914)
    cu = Cube(2.0)
    rp = run(cu, 16000, 0.8715, math.log(0.05), 1, only_built=True)
    print("  u = 2, n = 16000, M = 1, 'proof': %.4f (report: 0.914); violations %d" % (rp['cost'] / (16000 * cu.a), len(rp['viol'])))
    print("# rows that differ from the report by more than one unit of the last digit: %d" % ndiff)

elif mode == 'B':
    print("# Part B1: every n from 2 to 200; M = 0..3; eps in {1e-6, 0.01, 0.8715, 50}; delta in {0.999, 0.05, 1e-9, e^-n}")
    print("#   u    designs   nodes    violations   least slack of Theorem Q8 [nats] at (n, M, eps, ln delta)   least slack of the induction"
          "   levels built and checked: S / D shift / D no shift   designs whose top drop chose a level   least Q7(no shift) slack   least Lemma Q3 slack"
          "   largest cost - n ln 2 (must be <= 0)")
    for u in (0.1, 1.0, 4.0):
        cu = Cube(u)
        tabs = TabCache(u, 64)
        nd = 0
        nodes = 0
        viol = []
        mins = (INF, None)
        minind = INF
        built = [0, 0, 0]
        chosen = 0
        minq7ns = INF
        minq3 = INF
        maxover = -INF
        for n in range(2, 201):
            for M in (0, 1, 2, 3):
                for eps in (1e-6, 0.01, 0.8715, 50.0):
                    for ld in (math.log(0.999), math.log(0.05), math.log(1e-9), -float(n)):
                        r = run(cu, n, eps, ld, M, tabs=tabs)
                        nd += 1
                        nodes += r['nodes']
                        viol += r['viol']
                        sl = r['bound'] - r['cost']
                        if sl < mins[0]:
                            mins = (sl, (n, M, eps, round(ld, 3)))
                        st = r['st']
                        minind = min(minind, st.min_ind)
                        built[0] += st.built['S']
                        built[1] += st.lev['Dshift']
                        built[2] += st.lev['Dnoshift']
                        chosen += (M >= 1 and not r['top'].startswith('pass'))
                        minq7ns = min(minq7ns, st.min_q7ns)
                        minq3 = min(minq3, st.min_q3)
                        maxover = max(maxover, r['cost'] - n * LN2)
        print("  %.1f   %6d   %7d   %4d   %9.3f at %s   %9.3f   %d / %d / %d   %d   %9.3f   %9.3f   %.2e   [%.0f s]"
              % (u, nd, nodes, len(viol), mins[0], mins[1], minind, built[0], built[1], built[2], chosen, minq7ns, minq3, maxover, time.time() - t00))
        for v in viol[:5]:
            print("       VIOLATION: " + v)
        sys.stdout.flush()

    print("#\n# Part B2: the first sizes at which the slope step S[G_0] is built (x-hat = h n >= X_0(n)), called directly at")
    print("#          x in {X_0(n), (X_0 + h n)/2, h n, 3 h n}, delta in {0.999, 0.05, e^-n}; and the design G_1, G_2 at the top around these sizes")
    print("#   u    first n   sizes   levels built (S)   violations   least slack: induction / Q6 level / Lemma Q4   least n_o   | G_1, G_2 at the top: designs, violations, least slack of Theorem Q8")
    for u in (0.5, 1.0, 2.0, 4.0):
        cu = Cube(u)
        fm0 = Formula(cu)
        n1 = 2
        while cu.h * n1 < fm0.X0(n1):
            n1 += 1
        tabs = TabCache(u, 64)
        fam, fams, fm, st = build_design(cu, 1.0, 1, tabs=tabs)
        S = fams[1]
        sizes = list(range(n1 - 2, n1 + 60)) + [2 * n1, 3 * n1 + 1]
        min_no = INF
        for n in sizes:
            X0 = fm.X0(n)
            for x in (X0, 0.5 * (X0 + cu.h * n), cu.h * n, 3 * cu.h * n):
                for ld in (math.log(0.999), math.log(0.05), -float(n)):
                    S.cost(n, x, ld)
                    xh = min(x, cu.h * n)
                    if xh >= X0:
                        min_no = min(min_no, math.floor((xh - 1 - fm.clog(n)) / cu.h + 1e-12))
        nd = 0
        viol2 = []
        mins = INF
        # the top call is a drop whose inner dimension is about (1 - phi_0) n: take n so that n_i runs through the first sizes
        for n in [int(n1 / (1 - cu.epochs(1)['phi'][0])) + k for k in range(-5, 80, 5)]:
            for M in (1, 2):
                for ld in (math.log(0.05), -float(n)):
                    r = run(cu, n, 1.0, ld, M, tabs=tabs)
                    nd += 1
                    viol2 += r['viol']
                    mins = min(mins, r['bound'] - r['cost'])
        print("  %.1f   %6d   %4d   %6d   %4d   %8.3f / %8.3f / %7.4f   %s   | %d, %d, %.2f   [%.0f s]"
              % (u, n1, len(sizes), st.built['S'], len(st.viol), st.min_ind, st.min_q6, st.min_q4, min_no, nd, len(viol2), mins, time.time() - t00))
        for v in (st.viol + viol2)[:5]:
            print("       VIOLATION: " + v)
        tot_viol += len(st.viol)
        tot_nodes += st.nodes
        sys.stdout.flush()

elif mode == 'E':
    print("# extremes at medium sizes: accuracies 1e-4 ... 50, failure probabilities 0.999 ... e^{-100 n}, slopes 0.1, 1, 4")
    print("#   u       n   M     eps      ln delta    | min/(na)   bound/(na)   bound - exact [nats] | nodes   violations | least slack: induction / Q6 / Q7 shift / Q7 no shift / Q3 / Q4"
          " | slope levels built, drop levels built (shift / no shift) | top | time")
    cases = []
    for n in (2000, 8000):
        for M in (1, 2):
            for (eps, ldf) in ((1e-4, math.log(0.05)), (50.0, math.log(0.05)), (0.8715, math.log(0.999)), (0.8715, -float(n)), (0.8715, -100.0 * n)):
                cases.append((1.0, n, M, eps, ldf))
    for (n, Ms) in ((400, (1, 2)), (1000, (1, 2)), (2000, (1,))):
        for M in Ms:
            for (eps, ldf) in ((1.0, math.log(0.05)), (0.01, -float(n))):
                cases.append((4.0, n, M, eps, ldf))
    cases.append((4.0, 2000, 2, 1.0, math.log(0.05)))          # 1.5 10^8 nodes, twelve minutes
    for n in (60000, 200000):
        for (eps, ldf) in ((1.0, math.log(0.05)), (0.01, -float(n))):
            cases.append((0.1, n, 1, eps, ldf))
    for (u, n, M, eps, ld) in cases:
        cu = Cube(u)
        rm = run(cu, n, eps, ld, M)
        na = n * cu.a
        st = rm['st']
        print("  %.1f  %6d  %d  %8.1e  %10.1f   | %.4f    %.4f    %9.1f | %8d  %d | %s | %d, %d / %d | %s | %.0f s"
              % (u, n, M, eps, ld, rm['cost'] / na, rm['bound'] / na, rm['bound'] - rm['cost'], rm['nodes'], len(rm['viol']), fmt_slack(st),
                 st.built['S'], st.lev['Dshift'], st.lev['Dnoshift'], rm['top'].split(' ')[0], rm['time']))
        for v in rm['viol'][:5]:
            print("       VIOLATION: " + v)
        sys.stdout.flush()

print("# total: %d node checks, %d violations of proved inequalities   [%.0f s]" % (tot_nodes, tot_viol, time.time() - t00))
