#!/usr/bin/env python3
"""Referee's check of what Algorithm A does with the transport tail function of N_REPORT Lemma N16 on the cube
(sections 3.1 and 4(e) of the report say: "does not close with it before the atom at every accuracy rate below
0.589 u" and "the exponent of the level is ln 2").

Own implementation of Algorithm A (N_REPORT 2.2), outer space Q_m uniform, n_i = 0 (V evaluated exactly: every
bracket is [V, V]), Theta = id, tail function
    Xi_T(q) = int_0^R e^r min{ q, exp(-2 (r - r0(q))_+^2 / sigma^2) } dr,   sigma^2 = m u^2, R = m u,
    r0(q) = sigma sqrt(ln(1/(1-q))/2),   Xi_T(1) := +infinity,   Xi_T := 0 below the atom 2^-m.
The threshold is theta = e^{m X}.  Reported: the closing level pi_* of Theorem N1 (sup over ALL smaller q), the
bound Mbar, and what the run does (largest sample, level, validity).
"""
import math
import sys
import time

import numpy as np
from scipy.special import ndtr

INF = float("inf")


def XiT(q, m, u):
    if q >= 1:
        return INF
    if q * 2.0 ** m < 1 - 1e-12:
        return 0.0
    sig = u * math.sqrt(m)
    R = m * u
    r0 = sig * math.sqrt(math.log(1 / (1 - q)) / 2)
    r1 = r0 + sig * math.sqrt(math.log(1 / q) / 2)
    val = q * math.expm1(min(r1, R))
    if r1 < R:
        c = r0 + sig * sig / 4
        val += math.exp(r0 + sig * sig / 8) * (sig / 2) * math.sqrt(2 * math.pi) * (ndtr(2 * (R - c) / sig) - ndtr(2 * (r1 - c) / sig))
    return val


def harper_E(m, u):
    c = [math.comb(m, j) for j in range(m + 1)]
    return [sum(c[j] * math.expm1(u * (r + 1 - j)) for j in range(r + 1)) for r in range(m + 1)], [sum(c[:r + 1]) for r in range(m + 1)]


def run(rng, m, u, X, inst, lam=1.0, eta=0.5, etap=1.0, nu1=1.0, b=0.1, delta=0.05, maxM=3e7):
    binom = np.array([math.comb(m, w) for w in range(m + 1)], dtype=float)
    w = np.arange(m + 1)
    if inst == 'flat':
        psi = np.zeros(m + 1)
    elif inst == 'cone':
        psi = u * w
    else:                                   # dip on the ball of radius r around 0^m
        r = int(inst[3:])
        psi = -u * np.maximum(r - w, 0)
    Vw = np.exp(-psi)
    A = float((binom * Vw).sum() / 2.0 ** m)
    psi0 = psi[0]
    ell0 = math.exp(-psi0) * ((1 + math.exp(-u)) / 2) ** m
    Vmax = math.exp(-psi0 + u * m)
    theta = math.exp(m * X)
    ceta = (1 - eta) / (1 + eta)
    J = math.ceil(math.log(Vmax / ell0) / lam)
    nu0 = max((J + 1) * math.expm1(lam) / etap, nu1) / (1 - eta)
    # closing level of the theorem: conditions for ALL q < pi_*  (scan a log grid from the atom upwards)
    atom = 2.0 ** -m
    pi_star = atom
    for q in np.exp(np.linspace(math.log(atom), 0, 2001))[:-1]:
        x = XiT(q, m, u)
        if x <= theta * (1 - eta) * nu0 * q and x <= theta * ceta * q:
            pi_star = q
        else:
            break
    # the set of q at which both conditions hold (not only an initial segment)
    good = [q for q in np.exp(np.linspace(math.log(atom), 0, 2001))[:-1]
            if XiT(q, m, u) <= theta * (1 - eta) * nu0 * q and XiT(q, m, u) <= theta * ceta * q]
    m_max = math.ceil(math.log2(2 * (1 + eta) * math.exp(lam) * nu0 / ((1 - eta) * pi_star)))
    K = math.ceil(3 * (1 + eta) / eta ** 2 * math.log(2 * (J + 1) * (m_max + 1) * 3 / delta))
    nu = K * nu0
    Mbar = 2 * (1 + eta) * math.exp(lam) * nu0 * K / ((1 - eta) * pi_star)
    x_out = math.log(1 + math.exp(b) * (math.exp(lam) * (1 + eta) / (1 - eta) + etap + theta))
    V = np.empty(0)
    ell, Sig, usum, j, Mmax = ell0, 0.0, 0.0, 0, 0
    stop = None
    while stop is None:
        sj = ell0 * math.exp(j * lam)
        if sj >= Vmax:
            stop, Lr, Ur = 'cap', max(ell, Sig), ell0 + usum
            break
        Mneg = nu * sj / (ell * math.exp(b))
        M = K
        while True:
            if M > maxM:
                stop, Lr, Ur = 'not closed up to M = %.3g' % (M / 2), float('nan'), float('nan')
                break
            if len(V) < M:
                V = np.concatenate([V, Vw[rng.binomial(m, 0.5, M - len(V))]])
            Mmax = max(Mmax, M)
            Nh = int(np.count_nonzero(V[:M] > sj))
            q = min(1.0, max(Nh, K) / ((1 - eta) * M))
            pop = Nh >= K
            if pop:
                plow = Nh / ((1 + eta) * M)
                ell = max(ell, sj * math.exp(-b) * plow)
            tl = sj * XiT(q, m, u)
            if tl <= theta * math.exp(b) * ell:
                Lr = max(ell, Sig + ((1 - math.exp(-lam)) * math.exp(-b) * sj * plow if pop else 0.0))
                Ur = ell0 + usum + tl
                stop = 'closed (%s pass, q = %.3g)' % ('populated' if pop else 'unpopulated', q)
                break
            if pop:
                Sig += (1 - math.exp(-lam)) * math.exp(-b) * sj * plow
                usum += sj * math.expm1(lam) * q
                break
            if M >= Mneg:
                usum += sj * math.expm1(lam) * q
                break
            M *= 2
        j += 1
    valid = (Lr <= A * (1 + 1e-12) and A <= Ur * (1 + 1e-12)) if Lr == Lr else None
    return dict(pi_star=pi_star, Mbar=Mbar, K=K, J=J, Mmax=Mmax, stop=stop, level=j - 1, valid=valid,
                width_ok=(Ur <= math.exp(x_out) * Lr * (1 + 1e-9)) if Lr == Lr else None, atom=atom,
                good=(min(good), max(good)) if good else None, x_out=x_out)


def main():
    t0 = time.time()
    rng = np.random.default_rng(5)
    bad = 0
    u = 1.0
    print("transport tail function on Q_m, u = 1:  u^2/8 = 0.125,  0.589 u = %.3f,  eps* = ln cosh(u/2) = %.4f" % (math.sqrt(math.log(2) / 2), math.log(math.cosh(0.5))))
    # validity of Xi_T against Harper (it must dominate the exact tail function at ball sizes)
    for m in (16, 30, 60):
        E, ball = harper_E(m, u)
        worst = max((E[r] / 2.0 ** m) / XiT(ball[r] / 2.0 ** m, m, u) for r in range(m))
        print("  m = %d: Harper's exact function / Xi_T at ball sizes: largest ratio %.4f (must be <= 1)" % (m, worst))
        bad += worst > 1 + 1e-9
    print("  m   X      instance | pi_* of Theorem N1 (atom)        Mbar      | {q: [N],[P] hold} (min, max) | run: largest sample   stop                                  level  valid  width")
    for (m, X, inst) in [(30, 0.50, 'flat'), (30, 0.50, 'dip8'), (60, 0.50, 'cone'), (60, 0.50, 'dip15'), (30, 0.30, 'flat'), (30, 0.30, 'cone'), (30, 0.30, 'dip8'), (30, 0.20, 'flat'), (30, 0.20, 'dip8'),
                         (60, 0.30, 'flat'), (60, 0.30, 'dip15'), (60, 0.14, 'dip15'),
                         (16, 0.05, 'flat'), (16, 0.05, 'dip4'), (16, 0.10, 'dip4')]:
        r = run(rng, m, u, X, inst)
        print("  %-3d %-6.2f %-8s | %.3e (%.3e)        %.3e | %-28s | %-21d %-37s %-6d %-6s %s"
              % (m, X, inst, r['pi_star'], r['atom'], r['Mbar'], ("(%.2e, %.2e)" % r['good']) if r['good'] else "none above the atom",
                 r['Mmax'], r['stop'], r['level'], r['valid'], r['width_ok']))
        if r['valid'] is False or r['width_ok'] is False:
            bad += 1
    print("violations: %d  (%.1f s)" % (bad, time.time() - t0))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
