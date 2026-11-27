#!/usr/bin/env python3
"""Referee: the NEGLIGIBLE branch of the unbounded variant (Theorem N1' of N_REPORT), which the report says it did
not exercise (section 9).  Outer space (R, N(0,1)); instances with a bulk and a thin exponential tail:
    V(a) = e^{L (a - c)_+}       (the extremal dip; A = Phi(c) + e^{L^2/2 - Lc} Phi(L - c))
    V(a) = e^{L a}               (linear)
Tail functions Xi_L, Theta_L (exact for the class).  Own implementation of Algorithm A without rule (c0), with the
constants of Theorem N1' (J from the closing level, abort if level J+1 would be entered).  For every run: closed?,
valid?, width?, number of levels left as populated / as negligible, q_j >= pi_* at every level left (claim (iii)),
M <= Mbar (claim (iv)), levels <= J (claim (i)).
"""
import math
import sys
import time

import numpy as np
from scipy import stats

from r2_gauss import Xi, ThetaBar

Phi, Phinv = stats.norm.cdf, stats.norm.ppf


def consts(L, lam, eta, etap, theta, nu1, b, delta, ell0, u0, nrungs):
    ceta = (1 - eta) / (1 + eta)
    qs = np.exp(np.linspace(math.log(1e-13), 0, 6001))[:-1]
    pi_star = None
    for q in qs:
        x = Xi(L, q)
        if x <= theta * nu1 * q and x <= theta * ThetaBar(L, ceta * q):
            pi_star = q
        else:
            break
    if pi_star is None:
        return None
    pi_star *= 0.999
    J = math.floor((math.log(u0 / ell0) + b + lam + math.log((1 + eta) / ((1 - eta) * pi_star))) / lam)
    nu0 = max((J + 1) * math.expm1(lam) / etap, nu1) / (1 - eta)
    m_max = math.ceil(math.log2(2 * (1 + eta) * math.exp(lam) * nu0 / ((1 - eta) * pi_star)))
    K = math.ceil(3 * (1 + eta) / eta ** 2 * math.log(2 * (J + 1) * (m_max + 1) * (nrungs + 2) / delta))
    return dict(pi_star=pi_star, J=J, nu0=nu0, m_max=m_max, K=K, nu=K * nu0,
                Mbar=2 * (1 + eta) * math.exp(lam) * nu0 * K / ((1 - eta) * pi_star),
                x_out=math.log(1 + math.exp(b) * (math.exp(lam) * (1 + eta) / (1 - eta) + etap + theta)))


def run(rng, L, f, A, C, lam, eta, theta, b, ell0, mode, maxM=4e7):
    K, nu, J = C['K'], C['nu'], C['J']
    x0 = math.log(Phi(L) / Phi(-L))
    xs = [x0, b]
    V = np.empty(0); Lo = np.empty(0); Up = np.empty(0); rung = np.empty(0, dtype=np.int64)

    def bracket(vals, x):
        xi = rng.random(len(vals)) if mode == 0 else (np.ones(len(vals)) if mode == 1 else np.zeros(len(vals)))
        return vals * np.exp(-xi * x), vals * np.exp((1 - xi) * x)

    ell, Sig, usum, j, Mmax = ell0, 0.0, 0.0, 0, 0
    npop = nneg = 0
    qmin_left = 1.0
    while True:
        if j > J:
            return dict(stop='abort-J', npop=npop, nneg=nneg, Mmax=Mmax, level=j)
        sj = ell0 * math.exp(j * lam)
        Mneg = nu * sj / (ell * math.exp(b))
        M = K
        while True:
            if M > maxM:
                return dict(stop='too-large', npop=npop, nneg=nneg, Mmax=Mmax, level=j)
            if len(V) < M:
                nv = f(rng.standard_normal(M - len(V)))
                l0, u0_ = bracket(nv, xs[0])
                V = np.concatenate([V, nv]); Lo = np.concatenate([Lo, l0]); Up = np.concatenate([Up, u0_])
                rung = np.concatenate([rung, np.zeros(len(nv), dtype=np.int64)])
            Mmax = max(Mmax, M)
            idx = np.nonzero((Up[:M] > sj) & (Lo[:M] <= sj * math.exp(-b)) & (rung[:M] == 0))[0]
            if len(idx):
                rung[idx] = 1
                nl, nu_ = bracket(V[idx], xs[1])
                Lo[idx] = np.maximum(Lo[idx], nl); Up[idx] = np.minimum(Up[idx], nu_)
            Nh = int(np.count_nonzero(Up[:M] > sj))
            q = min(1.0, max(Nh, K) / ((1 - eta) * M))
            pop = Nh >= K
            if pop:
                plow = Nh / ((1 + eta) * M)
                ell = max(ell, sj * math.exp(-b) * ThetaBar(L, plow))
            tl = sj * Xi(L, q)
            if tl <= theta * math.exp(b) * ell:
                Lr = max(ell, Sig + ((1 - math.exp(-lam)) * math.exp(-b) * sj * plow if pop else 0.0))
                Ur = ell0 + usum + tl
                return dict(stop='closed', npop=npop, nneg=nneg, Mmax=Mmax, level=j, valid=bool(Lr <= A <= Ur),
                            width=bool(Ur <= math.exp(C['x_out']) * Lr * (1 + 1e-12)), qmin=qmin_left, ratio=Ur / Lr)
            if pop:
                npop += 1
                qmin_left = min(qmin_left, q)
                Sig += (1 - math.exp(-lam)) * math.exp(-b) * sj * plow
                usum += sj * math.expm1(lam) * q
                break
            if M >= Mneg:
                nneg += 1
                qmin_left = min(qmin_left, q)
                usum += sj * math.expm1(lam) * q
                break
            M *= 2
        j += 1


def main():
    t0 = time.time()
    rng = np.random.default_rng(3)
    bad = 0
    print("L    instance      theta  nu1   | pi_*       J    K    Mbar      x_out | runs closed invalid width-bad | levels left: populated, negligible | min q_j/pi_* | max M/Mbar | max level")
    cases = []
    for (L, c) in [(1.0, 3.0), (1.0, 3.3), (0.7, 3.0), (2.0, 2.5)]:
        cases.append((L, 'dip c=%.1f' % c, (lambda a, L=L, c=c: np.exp(L * np.maximum(a - c, 0))), Phi(c) + math.exp(L * L / 2 - L * c) * Phi(L - c)))
    cases.append((2.0, 'linear', (lambda a: np.exp(2.0 * a)), math.exp(2.0)))
    psets = {1.0: [(0.5, 0.5, 0.5, 0.005, 60.0, 0.1), (0.5, 0.5, 0.5, 0.006, 50.0, 0.1)],
             0.7: [(0.5, 0.5, 0.5, 0.002, 100.0, 0.1), (0.5, 0.5, 0.5, 0.003, 80.0, 0.1)],
             2.0: [(0.5, 0.5, 0.5, 0.05, 100.0, 0.1), (1.0, 0.5, 1.0, 0.1, 40.0, 0.25)]}
    totneg = 0
    for (L, name, f, A) in cases:
        ell0 = 2 * math.exp(L * L / 2) * Phi(-L)             # reference point 0, psi(0) = 0:  E e^{-L|x|} <= A
        u0 = 2 * math.exp(L * L / 2) * Phi(L)
        for (lam, eta, etap, theta, nu1, b) in psets[L]:
            C = consts(L, lam, eta, etap, theta, nu1, b, 0.05, ell0, u0, 1)
            if C is None:
                print("%-4g %-13s %-6g %-5g | no closing level" % (L, name, theta, nu1))
                continue
            res = [run(rng, L, f, A, C, lam, eta, theta, b, ell0, rep % 3) for rep in range(6)]
            closed = [r for r in res if r['stop'] == 'closed']
            inval = sum(not r['valid'] for r in closed)
            wbad = sum(not r['width'] for r in closed)
            npop = sum(r['npop'] for r in res)
            nneg = sum(r['nneg'] for r in res)
            totneg += nneg
            qr = min([r['qmin'] for r in closed], default=float('nan')) / C['pi_star']
            mr = max(r['Mmax'] for r in res) / C['Mbar']
            lev = max(r['level'] for r in res)
            print("%-4g %-13s %-6g %-5g | %-10.3g %-4d %-4d %-9.3g %-5.3f | %-4d %-6d %-7d %-9d | %-9d %-23d | %-12.3g | %-10.3g | %d (J = %d)"
                  % (L, name, theta, nu1, C['pi_star'], C['J'], C['K'], C['Mbar'], C['x_out'], len(res), len(closed), inval, wbad, npop, nneg, qr, mr, lev, C['J']))
            bad += inval + wbad + (len(closed) < len(res)) + (qr < 1) + (mr > 1) + (lev > C['J'])
    print("levels left as negligible in the unbounded variant, all runs: %d" % totneg)
    print("violations: %d   (%.1f s)" % (bad, time.time() - t0))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
