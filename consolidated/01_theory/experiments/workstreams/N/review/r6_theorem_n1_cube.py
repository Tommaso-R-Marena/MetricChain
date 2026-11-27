#!/usr/bin/env python3
"""Referee: Theorem N1 in a VALID setting with the referee's own implementation of Algorithm A (the one of
r1_n12_false_bracket.py): outer space Q_m uniform, outer integrand V(a) = e^{-f(|a|)} radial with |f(w+1) - f(w)| <= u
(so -ln V is in L_u(Q_m) and Harper's functions are tail functions of V), oracle brackets in four placements.

Checked in every run: no abort; L <= A <= U; U <= e^{x_out} L; every sampled certificate true; the Chernoff events
on the realised sample; claim (iii) q_j >= pi_* at every level that is left; claim (iv) every sample <= Mbar; stop
at a level <= J.  Parameter sets include small theta with nu_1 = 1, so that levels are left as negligible.
"""
import math
import sys
import time
from fractions import Fraction

import numpy as np

import r1_n12_false_bracket as r1


def set_instance(m, f):
    r1.m = m
    r1.NN = 2 ** m
    r1.binom = [math.comb(m, w) for w in range(m + 1)]
    r1.Vw = [math.exp(-f[w]) for w in range(m + 1)]
    r1.A = sum(r1.binom[w] * r1.Vw[w] for w in range(m + 1)) / r1.NN


def instances(m, u, rng):
    out = []
    out.append(("flat", [0.0] * (m + 1)))
    out.append(("cone", [u * w for w in range(m + 1)]))
    out.append(("anticone", [-u * w for w in range(m + 1)]))
    r = m // 3
    out.append(("dip r=%d" % r, [-u * max(r - w, 0) for w in range(m + 1)]))
    out.append(("far dip", [-u * max(w - (m - r), 0) for w in range(m + 1)]))
    f = [0.0]
    for w in range(m):
        f.append(f[-1] + rng.uniform(-u, u))
    out.append(("random radial", f))
    f = [0.0]
    for w in range(m):
        f.append(f[-1] + (u if rng.random() < 0.5 else -u))
    out.append(("random +-u", f))
    f = [0.0]
    for w in range(m):
        f.append(f[-1] + (-u if w >= m - 3 else 0.2 * u * rng.uniform(-1, 1)))
    out.append(("bulk + spike", f))
    return out


def main():
    t0 = time.time()
    rng = np.random.default_rng(99)
    half = Fraction(1, 2)
    psets = [("bounded th=.3", dict(lam=0.5, eta=half, etap=0.5, theta=0.3, nu1='b', b=0.3)),
             ("small th, nu1=1", dict(lam=0.5, eta=half, etap=0.5, theta=0.05, nu1=1.0, b=0.3)),
             ("extensive th=40", dict(lam=1.0, eta=half, etap=1.0, theta=40.0, nu1=1.0, b=1.0)),
             ("eta=1/4 th=.2", dict(lam=0.25, eta=Fraction(1, 4), etap=0.25, theta=0.2, nu1='b', b=0.2))]
    tot = dict(runs=0, closed=0, cap=0, abort=0, invalid=0, width=0, cert=0, chern=0, iii=0, iv=0, lev=0, pop=0, neg=0, v=0, cnt=0, nv=0)
    print("m   u    parameters        | pi_*      r_dag  J    K    Mbar     | runs  closed cap abort | invalid width cert chernoff (iii) (iv) | levels left pop/neg | largest sample")
    for (m, u) in [(10, 1.0), (12, 0.5), (11, 2.0), (13, 0.7)]:
        H = r1.Harper(m, u)
        for (pname, P) in psets:
            nu1 = 2 * math.exp(u) * m / P['theta'] if P['nu1'] == 'b' else P['nu1']
            row = dict(runs=0, closed=0, cap=0, abort=0, invalid=0, width=0, cert=0, chern=0, iii=0, iv=0, pop=0, neg=0, maxM=0, v=0, cnt=0, nv=0)
            for (iname, f) in instances(m, u, rng):
                set_instance(m, f)
                psi0 = f[0]
                ell0 = math.exp(-psi0) * ((1 + math.exp(-u)) / 2) ** m
                Vmax = math.exp(-psi0 + u * m)
                xs = [2 * u * 4, u * 2, P['b']] if u * 2 > P['b'] else [2 * u * 4, P['b']]
                for kappa0 in (1.0, (2 / (1 + math.exp(u))) ** m):
                    C = r1.Consts(P['lam'], P['eta'], P['etap'], P['theta'], nu1, P['b'], xs, 0.05, kappa0, ell0, Vmax, H)
                    for rep in range(2):
                        res = r1.run_A(rng, C, H, (rep + int(kappa0 < 1) * 2) % 4)
                        row['runs'] += 1
                        if res['stop'].startswith('abort'):
                            row['abort'] += 1
                            continue
                        row['closed'] += res['stop'] == 'closed'
                        row['cap'] += res['stop'] == 'cap'
                        ch = r1.check(res, C)
                        row['invalid'] += not ch['valid']
                        row['width'] += not ch['width']
                        row['cert'] += not ch['cert']
                        row['chern'] += not ch['chernoff']
                        for (j, kind, M, Nh, q, plow) in res['levels']:
                            row['pop'] += kind == 'pop'
                            row['neg'] += kind == 'neg'
                            row['iii'] += float(q) < C.pi_star * (1 - 1e-12)
                            row['iv'] += M > C.Mbar
                            row['maxM'] = max(row['maxM'], M)
                        if res['last'] is not None:
                            row['maxM'] = max(row['maxM'], res['last'][1])
                            row['iv'] += res['last'][1] > C.Mbar
                        # claim (v): for every level reached and x > 0:  M_j^neg p(s_j e^-x) <= c_eta^-1 e^lam nu e^x, and for
                        # x in {x_0..x_{L-1}} at most cnt(x) of the points used at level j have V > s_j e^-x
                        lastM = {j: M for (j, kind, M, Nh, q, plow) in res['levels']}
                        if res['last'] is not None:
                            lastM[res['last'][0]] = res['last'][1]
                        e = float(C.eta)
                        Vv = res['V']
                        for (j, ell_j, Mneg) in r1.ENTRIES:
                            sj = C.s0 * math.exp(j * C.lam)
                            for x in (0.05, 0.3, 1.0, 2.5, 6.0) + tuple(C.xs[:-1]):
                                row['v'] += Mneg * r1.p_exact(sj * math.exp(-x)) > (1 + e) / (1 - e) * math.exp(C.lam) * C.nu * math.exp(x) * (1 + 1e-9)
                            if j in lastM:
                                for x in C.xs[:-1]:
                                    row['cnt'] += int(np.count_nonzero(Vv[:lastM[j]] > sj * math.exp(-x))) > C.cnt(x)
                            row['nv'] += 1
                        # a stop at level J+1 counts only if level J was genuinely below the cap: with kappa0 = (2p_u)^m
                        # and 2um/lambda an integer, s_J = V_max exactly and rule (c0) at level J is a floating-point tie
                        if res['j'] > C.J:
                            sJ = C.s0 * math.exp(C.J * C.lam)
                            if res['j'] > C.J + 1 or sJ < C.Vmax * (1 - 1e-9):
                                tot['lev'] += 1
                            else:
                                tot['tie'] = tot.get('tie', 0) + 1
            print("%-3d %-4g %-17s | %-9.3g %-6d %-4d %-4d %-8.3g | %-5d %-6d %-3d %-5d | %-7d %-5d %-4d %-8d %-5d %-4d | %d / %d | %d"
                  % (m, u, pname, C.pi_star, C.rdag, C.J, C.K, C.Mbar, row['runs'], row['closed'], row['cap'], row['abort'],
                     row['invalid'], row['width'], row['cert'], row['chern'], row['iii'], row['iv'], row['pop'], row['neg'], row['maxM']))
            for k_ in ('runs', 'closed', 'cap', 'abort', 'invalid', 'width', 'cert', 'chern', 'iii', 'iv', 'pop', 'neg', 'v', 'cnt', 'nv'):
                tot[k_] += row[k_]
    print("TOTAL: runs %d, closed %d, stopped by (c0) %d, aborts %d | invalid %d, width violations %d, false certificates %d, "
          "Chernoff events violated %d, (iii) violated %d, (iv) violated %d, stops above J %d | levels left: %d populated, %d negligible; floating-point ties s_J = V_max resolved at level J+1: %d   (%.0f s)"
          % (tot['runs'], tot['closed'], tot['cap'], tot['abort'], tot['invalid'], tot['width'], tot['cert'], tot['chern'], tot['iii'], tot['iv'],
             tot['lev'], tot['pop'], tot['neg'], tot.get('tie', 0), time.time() - t0))
    print("claim (v), the count: %d levels reached; M_j^neg p(s_j e^-x) above the bound: %d;  points above s_j e^{-x_l} more than cnt(x_l): %d"
          % (tot['nv'], tot['v'], tot['cnt']))
    # Theorem N1 allows invalid brackets and false certificates only off the good event
    viol = tot['width'] + tot['iii'] + tot['iv'] + tot['lev'] + tot['abort']
    viol += (tot['invalid'] + tot['cert'] + tot['v'] + tot['cnt']) if tot['chern'] == 0 else 0
    return 1 if viol else 0


if __name__ == "__main__":
    sys.exit(main())
