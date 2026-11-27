#!/usr/bin/env python3
"""r03_formula.py -- referee: formula (A.1) of Theorem A, evaluated from the text of the report with own code,
for rows of the table of section 7.3 (u = 1, eps = 1, delta = 0.05; bound minimised over M)."""
import math, sys
sys.dont_write_bytecode = True
import rlib
from rlib import LN2


def E_A1(cu, n, eps, ldelta_inv, M, seq, detail=False):
    """(A.1): returns E'_M (and its parts: base, slope steps, drops, chains)."""
    u, a, h = cu.u, cu.a, cu.h
    epsh = min(eps, 1.0)
    Lam = ldelta_inv + n * LN2
    Lam0 = Lam
    parts = dict(base=0.0, slope=0.0, drop=0.0, chain=0.0, nslope=0, chains=[])
    for e in range(M, -1, -1):
        Bp = seq['B'][e] if e >= 1 else a
        calX = rlib.X_D(cu, n, seq['phi'][e - 1]) if e >= 1 else rlib.X_B(cu, n)
        alpha = epsh if e == M else 1.0
        m = rlib.Chain.design_m(cu, n, Bp, calX, alpha, Lam)
        ch = rlib.Chain(cu, n, Bp, calX, alpha, m)
        Lam = Lam + ch.j(n) * ch.qT(n, Lam + n * Bp)
        AT = ch.A_T(n, Lam)
        parts['chain'] += AT
        parts['chains'].append((e, m, ch.j(n), ch.c, AT))
        if e >= 1:
            me = e - 1
            Bt = max(1.0, seq['R'][me] / (2 * u * a)) * seq['B'][me]
            parts['drop'] += Bt + rlib.ell0_b(cu, n, Lam)
            Lam = Lam + rlib.q_b(cu, n, Lam)
            for j in range(seq['J'][me], 0, -1):
                sig = j / seq['d'][me]
                parts['slope'] += sig * (1 + rlib.c_log(cu, n) + h) + rlib.ell0_b(cu, n, Lam)
                parts['nslope'] += 1
                Lam = Lam + rlib.q_b(cu, n, Lam)
    parts['base'] = rlib.E_frakB(cu, n, Lam)
    parts['Lam_end_ratio'] = Lam / Lam0
    tot = parts['base'] + parts['slope'] + parts['drop'] + parts['chain']
    return (tot, parts) if detail else tot


def main():
    u, eps, delta = 1.0, 1.0, 0.05
    cu = rlib.Cube(u)
    seq = rlib.epochs(cu, 45)
    print("# referee: (A.1) at u = 1, eps = 1, delta = 0.05; minimised over M.   h/a = %.5f" % (cu.h / cu.a))
    print("# n | M  k_M | bound/(n a) | (bound - n h)/sqrt(n ln n) | E'_M = base + slope steps + drops + chains | report's row")
    rep = {10 ** 3: "0, 1, 2.320 [2.75]; 146 = 18 + 0 + 0 + 1x128",
           10 ** 4: "0, 1, 1.166 [3.30]; 184 = 23 + 0 + 0 + 1x161",
           10 ** 6: "9, 34, 0.3581 [2.85]; 6588 = 33 + 24x86 + 9x65 + 10x390",
           10 ** 8: "17, 268, 0.2690 [1.64]; 37122 = 42 + 250x99 + 17x84 + 18x613",
           10 ** 10: "25, 2868, 0.2632 [1.35]; 358401 = 51 + 2842x118 + 25x102 + 26x823",
           10 ** 12: "32, 23995, 0.2627 [1.29]; 3.35e6 = 61 + 23962x138 + 32x121 + 33x1023"}
    for n in (10 ** 3, 10 ** 4, 10 ** 6, 10 ** 8, 10 ** 10, 10 ** 12):
        best = None
        for M in range(0, 41):
            if seq['k'][M] > n:
                break
            E = E_A1(cu, n, eps, math.log(1 / delta), M, seq)
            val = n * (seq['B'][M] if M >= 1 else cu.a) + E
            if best is None or val < best[0]:
                best = (val, M)
        val, M = best
        E, p = E_A1(cu, n, eps, math.log(1 / delta), M, seq, detail=True)
        ns = p['nslope']
        print("%8.0e | %2d %6d | %.4f | %.3f | %.0f = %.0f + %dx%.0f + %dx%.0f + %dx%.0f | Lam_end/Lam_0 = %.3f | %s"
              % (n, M, seq['k'][M], val / (n * cu.a), (val - n * cu.h) / math.sqrt(n * math.log(n)), E, p['base'],
                 ns, p['slope'] / ns if ns else 0, M, p['drop'] / M if M else 0, M + 1, p['chain'] / (M + 1),
                 p['Lam_end_ratio'], rep[n]))
        if n in (10 ** 6,):
            print("      chains at n = 1e6 (e, block m, levels, c, A_T): " +
                  "; ".join("(%d, %d, %d, %.1e, %.0f)" % t for t in p['chains']))
    # accuracy enters additively: [bound(eps) - bound(1)] / ln(1/eps)
    for n in (10 ** 6, 10 ** 8):
        row = []
        for eps in (1e-1, 1e-6, 1e-32):
            b1 = min(n * (seq['B'][M] if M >= 1 else cu.a) + E_A1(cu, n, 1.0, math.log(20.0), M, seq) for M in range(0, 30) if seq['k'][M] <= n)
            b2 = min(n * (seq['B'][M] if M >= 1 else cu.a) + E_A1(cu, n, eps, math.log(20.0), M, seq) for M in range(0, 30) if seq['k'][M] <= n)
            row.append((b2 - b1) / math.log(1 / eps))
        print("n = %.0e: [bound(eps) - bound(1)]/ln(1/eps) at eps = 1e-1, 1e-6, 1e-32: %s   (report: 24.7 at 1e6, 27.0 at 1e8)" % (n, ", ".join("%.1f" % x for x in row)))


if __name__ == "__main__":
    main()
