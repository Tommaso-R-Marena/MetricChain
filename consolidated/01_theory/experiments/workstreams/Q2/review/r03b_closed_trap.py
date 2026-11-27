#!/usr/bin/env python3
"""r03b_closed_trap.py -- referee: (1) Proposition A' (closed form of (A.1)): hypothesis, Lam-bar <= Lam-hat, and the two
inequalities;  (2) the formula of section 5.4 (drops without chains, Proposition N) at a few sizes."""
import math, sys
sys.dont_write_bytecode = True
import rlib
from rlib import LN2, C3
import r03_formula as F


def ellT(cu, n, Lhat, Bp, calX, alpha):
    cl = alpha / (13.0 * n)
    mb = 1 + (calX + rlib.Pbar_cnt(cu, n, Lhat, cl) + math.log(4.0)) / Bp
    return (LN2 - Bp) * max(mb + calX / (2 * cu.u), math.log(78 * n / (5 * alpha)) / math.log((1 + math.exp(cu.u)) / 2)) \
        + rlib.Pbar_M(cu, n, Lhat, cl) + math.log(8.0)


def closed(cu, n, eps, ldi, M, seq):
    u, a, h = cu.u, cu.a, cu.h
    Lam0 = ldi + n * LN2
    Lhat = (M + 3) * Lam0
    kM = seq['k'][M]
    hyp = (kM - 1) * rlib.q_b(cu, n, Lhat) <= Lam0
    l0 = rlib.ell0_b(cu, n, Lhat)
    cl = 1 + rlib.c_log(cu, n) + h
    first = sum(seq['J'][m] * l0 + cl * seq['J'][m] * (seq['J'][m] + 1) / (2 * seq['d'][m]) for m in range(M))
    first += sum(max(1.0, seq['R'][m] / (2 * u * a)) * seq['B'][m] + l0 for m in range(M))
    lts = []
    for e in range(M + 1):
        Bp = seq['B'][e] if e >= 1 else a
        calX = rlib.X_D(cu, n, seq['phi'][e - 1]) if e >= 1 else rlib.X_B(cu, n)
        lts.append(ellT(cu, n, Lhat, Bp, calX, min(eps, 1.0) if e == M else 1.0))
    first += sum(lts) + rlib.E_frakB(cu, n, Lhat)
    lS = l0 + 0.5 * cl
    lD = l0 + (a / h) * cl + max(1.0, h / (2 * u * a)) * a
    second = (kM - 1 - M) * lS + M * lD + (M + 1) * max(lts) + rlib.E_frakB(cu, n, Lhat)
    return hyp, first, second


def E_trap(cu, n, eps, ldi, M, seq):
    u, a, h = cu.u, cu.a, cu.h
    b = [rlib.X_B(cu, n)]
    for m in range(M):
        b.append(b[m] + math.log(C3 + 1 + 3 * (seq['phi'][m] * n + 1) * math.exp(2 * u + math.exp(u))))
    Lam = ldi + n * LN2
    Bp = seq['B'][M] if M >= 1 else a
    mm = rlib.Chain.design_m(cu, n, Bp, b[M], min(eps, 1.0), Lam)
    ch = rlib.Chain(cu, n, Bp, b[M], min(eps, 1.0), mm)
    Lam += ch.j(n) * ch.qT(n, Lam + n * Bp)
    E = ch.A_T(n, Lam)
    for m in range(M - 1, -1, -1):
        bm = b[m]
        Bt = max(1.0, bm * seq['phi'][m] / (2 * u * (1 - seq['phi'][m]))) * seq['B'][m]
        E += Bt + rlib.ell0_b(cu, n, Lam, bm)
        Lam += rlib.q_b(cu, n, Lam, bm)
        for j in range(seq['J'][m], 0, -1):
            E += (j / seq['d'][m]) * (bm + rlib.c_log(cu, n) + h) + rlib.ell0_b(cu, n, Lam, bm)
            Lam += rlib.q_b(cu, n, Lam, bm)
    return E + rlib.E_frakB(cu, n, Lam), b[M]


def main():
    print("# (1) Proposition A': cases with the hypothesis; (A.1) <= first closed form <= second closed form")
    nc = nh = bad = 0
    worst = 0.0
    for u in (0.5, 1.0, 2.0):
        cu = rlib.Cube(u)
        seq = rlib.epochs(cu, 30)
        for n in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 8, 10 ** 10):
            for M in range(0, 26):
                if seq['k'][M] > n:
                    break
                for eps in (1.0, 1e-3):
                    nc += 1
                    hyp, f1, f2 = closed(cu, n, eps, math.log(20.0), M, seq)
                    if not hyp:
                        continue
                    nh += 1
                    E, p = F.E_A1(cu, n, eps, math.log(20.0), M, seq, detail=True)
                    if not (E <= f1 + 1e-9 <= f2 + 2e-9) or p['Lam_end_ratio'] > M + 3:
                        bad += 1
                    worst = max(worst, f1 / E)
    print("cases %d, with the hypothesis %d, violations %d; largest (closed form)/(A.1) = %.1f" % (nc, nh, bad, worst))
    print("# (2) section 5.4: drops without chains (formula E^N_M), u = 1, eps = 1, delta = 0.05, minimised over M")
    cu = rlib.Cube(1.0)
    seq = rlib.epochs(cu, 40)
    rep = {10 ** 5: "5, 0.576 [3.24]", 10 ** 6: "9, 0.3559 [2.78]", 10 ** 7: "12, 0.2900 [2.39]", 10 ** 8: "16, 0.2714 [2.27]"}
    for n in (10 ** 5, 10 ** 6, 10 ** 7, 10 ** 8):
        best = None
        for M in range(0, 36):
            if seq['k'][M] > n:
                break
            E, bM = E_trap(cu, n, 1.0, math.log(20.0), M, seq)
            val = n * (seq['B'][M] if M >= 1 else cu.a) + E
            if best is None or val < best[0]:
                best = (val, M, bM)
        newb = min(n * (seq['B'][M] if M >= 1 else cu.a) + F.E_A1(cu, n, 1.0, math.log(20.0), M, seq) for M in range(0, 36) if seq['k'][M] <= n)
        print("n = %.0e: no chain: M = %d, bound/(na) = %.4f [%.2f], top tolerance b_M = %.1f;  with chains (A.1): %.4f   (report: %s)"
              % (n, best[1], best[0] / (n * cu.a), (best[0] - n * cu.h) / math.sqrt(n * math.log(n)), best[2], newb / (n * cu.a), rep[n]))


if __name__ == "__main__":
    main()
