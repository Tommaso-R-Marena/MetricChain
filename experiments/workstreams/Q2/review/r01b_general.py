#!/usr/bin/env python3
"""r01b_general.py -- referee: (1) the generalised form of (U) WITHOUT the range condition (review note N2):
   ln C_max <= max_i [ n_i B_i + n_o theta - sigma_i min(n_o theta, R n_i) ] + ell_0^b + E_1,   cap Xi = n_o theta,
   tested on levels with n_o theta > R n_i (where Lemma U as stated does not apply), and for lines with DIFFERENT ranges R_i;
(2) the least slack of (U) by failure probability (how sharp ell_0^b is)."""
import math, sys, time
sys.dont_write_bytecode = True
import numpy as np
import rlib
from rlib import LN2, INF

t0 = time.time()


def costs_lines(lines, d, xs, ld, Ef):
    """lines: (B, sigma, R_i);  cost = max(0, max_i[d B_i - sigma_i min(x, R_i d)]) + E"""
    xs = np.asarray(xs, dtype=np.float64)
    mj = np.max(np.stack([d * B - s * (np.minimum(xs, R * d) if R < INF else xs) for (B, s, R) in lines]), axis=0)
    mj = np.maximum(mj, 0.0)
    return mj if Ef is None else mj + Ef(d, xs, -ld + d * LN2)


tot = viol = 0
gmin = (INF, None)
bydelta = {}
Efs = [None, lambda d, x, Lam: 3 * math.sqrt(d) + 0 * x, lambda d, x, Lam: 5 / x + math.log(Lam)]
for u in (0.5, 1.0, 2.0):
    cu = rlib.Cube(u)
    a, h, es = cu.a, cu.h, cu.eps_star
    for n in (2, 3, 5, 12, 40, 120, 300, 900, 2500, 8000, 20000, 60000):
        for n_o in sorted(set(max(1, min(n - 1, int(round(f * n)))) for f in (0.0, 0.03, 0.1, 0.2, 0.35, 0.5, 0.6, 0.75, 0.85, 0.95))):
            n_i = n - n_o
            for e in (0.0, 0.25 * h, 0.5 * h, h, 2 * h, 0.97 * es, 1.5 * es):
                th = cu.theta_na(e)
                for b in (1.0, 4.3, 15.0):
                    if 2 * u * n_i <= b:
                        continue
                    for ild, (ldn, ld) in enumerate((("0.5", math.log(0.5)), ("0.05", math.log(0.05)), ("1e-12", -27.63), ("e^-n", -float(n)))):
                        Ef = Efs[(ild + n_o) % 3]
                        for lines in ([(a, 1.0, h / 3)], [(a, 1.0, h / 50), (0.7 * a, 0.3, h)], [(3 * a, 0.7, 0.02 * h)],
                                      [(a, 1.0, h / 10), (0.8 * a, 0.5, 2 * h), (0.5 * a, 0.0, INF)],
                                      [(1.5 * h, 1.0, h / 4), (h, 0.2, INF)]):
                            if any(R < INF and B < s * R for (B, s, R) in lines):
                                continue
                            xs = rlib.ladder_U(cu, n_i, b, n_o * th)
                            lth = math.log(3.0) + math.log(n_o + 1.0) + 2 * u + math.exp(u) + n_o * e
                            lev = rlib.Level(u, n, n_o, 1.0, 0.5, 1.0, lth, 1.0, b, ld, len(xs))
                            lcm = lev.lcmax(xs, costs_lines(lines, n_i, xs, lev.ldp, Ef))
                            Lam = -ld + n * LN2
                            E1 = 0.0 if Ef is None else float(Ef(n, b, Lam + rlib.q_b(cu, n, Lam, b)))
                            bound = max(n_i * B + n_o * th - s * min(n_o * th, R * n_i) for (B, s, R) in lines) \
                                + rlib.ell0_b(cu, n, Lam, b) + E1
                            sl = bound - lcm
                            tot += 1
                            if sl < -1e-9:
                                viol += 1
                            beyond = any(R < INF and n_o * th > R * n_i for (B, s, R) in lines)
                            key = ("n >= 2500" if n >= 2500 else "n < 2500 ", ldn, "range condition violated" if beyond else "range condition holds")
                            if sl < bydelta.get(key, (INF,))[0]:
                                bydelta[key] = (sl, (u, n, n_o, round(e / h, 2), b, str(lines)))
print("generalised (U) without range condition, lines with different ranges: levels %d, violations %d" % (tot, viol))
for key in sorted(bydelta):
    print("   %s delta = %-6s %-26s least slack %8.3f at %s" % (key[0], key[1], key[2], bydelta[key][0], bydelta[key][1]))
print("time %.0f s" % (time.time() - t0))
