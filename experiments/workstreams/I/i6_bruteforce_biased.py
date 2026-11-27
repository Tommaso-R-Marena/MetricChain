#!/usr/bin/env python3
"""Workstream I, experiment 6: exhaustive test on the biased cube Q_n (n <= 4, all 2^(2^n) subsets) of

    'for p = P(x_i = 1) <= 1/2 and every r, t: among all sets E with mu(E) >= mu(U_r) the up-ball
     U_r = {|x| >= n - r} around the rare vertex minimises mu(E_t)'.

Exact rational arithmetic."""
import itertools, sys
from fractions import Fraction as Fr

def run(n, p):
    N = 1 << n
    q = 1 - p
    w = [p ** bin(x).count('1') * q ** (n - bin(x).count('1')) for x in range(N)]
    nb = [[x] + [x ^ (1 << i) for i in range(n)] for x in range(N)]
    # neighbourhood masks of single points, then sets as bitmasks over the N points
    nbmask = [sum(1 << y for y in nb[x]) for x in range(N)]
    def measure(mask):
        return sum(w[x] for x in range(N) if mask >> x & 1)
    def grow(mask):
        out = 0
        m = mask; x = 0
        while m:
            if m & 1: out |= nbmask[x]
            m >>= 1; x += 1
        return out
    # measures of all subsets by Gray-code style DP on the lowest set bit
    meas = [Fr(0)] * (1 << N)
    for mask in range(1, 1 << N):
        low = (mask & -mask).bit_length() - 1
        meas[mask] = meas[mask & (mask - 1)] + w[low]
    gr = [0] * (1 << N)
    for mask in range(1, 1 << N):
        low = (mask & -mask).bit_length() - 1
        gr[mask] = gr[mask & (mask - 1)] | nbmask[low]
    full = (1 << N) - 1
    ok = True
    for r in range(0, n):
        ball = sum(1 << x for x in range(N) if bin(x).count('1') >= n - r)
        mb = meas[ball]
        cur = list(range(1 << N))
        # t-step neighbourhoods by iterating the one-step map
        g = list(range(1 << N))
        for t in range(1, n - r + 1):
            g = [gr[m] for m in g]
            ball_t = sum(1 << x for x in range(N) if bin(x).count('1') >= n - r - t)
            target = meas[ball_t]
            best = min(meas[g[mask]] for mask in range(1, 1 << N) if meas[mask] >= mb)
            flag = (best == target)
            ok &= flag
            print(f"  n={n} p={p} r={r} t={t}: mu(U_r)={float(mb):.6f}  min mu(E_t)={float(best):.6f}  up-ball value={float(target):.6f}  {'EXTREMAL' if flag else 'NOT EXTREMAL (min is smaller)'}")
    return ok

if __name__ == "__main__":
    res = []
    for n in (2, 3, 4):
        for p in (Fr(1, 10), Fr(1, 5), Fr(1, 3), Fr(2, 5), Fr(1, 2)):
            res.append(((n, p), run(n, p)))
    print("summary:", "; ".join(f"n={n},p={p}: {'ok' if o else 'FAILS'}" for ((n, p), o) in res))
