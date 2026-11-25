"""Brute-force check of the log-tables of klib.Cube against direct sums (small n)."""
import math, numpy as np
from klib import Cube, consts
ok = True
for n in (1, 2, 5, 12, 30):
    for u in (0.3, 1.0, 2.5):
        c = Cube(n, u)
        binom = [math.comb(n, j) for j in range(n + 1)]
        ball = [sum(binom[: r + 1]) for r in range(n + 1)]
        for r in range(n + 1):
            E = sum(binom[j] * (math.exp(u * (r + 1 - j)) - 1) for j in range(r + 1))
            T = sum(binom[j] * math.exp(-u * max(j - r, 0)) for j in range(n + 1))
            Gt = (math.exp(u) - 1) if r == 0 else E / ball[r - 1]
            for name, val, ref in (("ball", c.lball_r(r), math.log(ball[r])), ("E", c.lE[r], math.log(E)), ("T", c.lT[r], math.log(T)), ("Gt", c.lGt[r], math.log(Gt))):
                if abs(val - ref) > 1e-9 * max(1, abs(ref)):
                    ok = False; print("MISMATCH", n, u, r, name, val, ref)
        # radius / kball
        for q in (1.0, 0.5, 0.1, 2.0 ** -n, 0.3 * 2.0 ** -n * 7):
            if q > 1: continue
            r = c.radius(math.log(q))
            r_ref = next(rr for rr in range(n + 1) if ball[rr] >= 2 ** n * q - 1e-9)
            if r != r_ref: ok = False; print("radius mismatch", n, u, q, r, r_ref)
        for cnt in (0.3, 1.0, 1.5, 7.0, 2.0 ** n * 0.4):
            k = c.kball(math.log(cnt))
            k_ref = max([kk for kk in range(n + 1) if ball[kk] <= max(1, cnt) + 1e-9] + [0])
            if k != k_ref: ok = False; print("kball mismatch", n, u, cnt, k, k_ref)
print("tables agree with brute force:", ok)
