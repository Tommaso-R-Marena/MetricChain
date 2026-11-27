#!/usr/bin/env python3
"""R13 / item 2, remark (1a) after Theorem 11.58: "C_max < LB holds first at n = 1370, 518, 4524 (u = 1, 2, 1/2; n_o = floor(n/2)),
fails again at some larger sizes, and holds at every n from 1398, 538, 4566".

RE-RUN of our own division's code for C_max (workstream R6: byte-identical copies of ws_R6/everyn.py and ws_R6/r6lib.py in
ws_R13/r6_copy/, imported from there so that nothing is written into ws_R6; everyn.two_level writes no file), with phi = 0.5
(n_o = floor(n/2)), design K64 (b = 0.5, lam = 0.2, eta = eta' = theta = 0.05, delta = 0.05, inner rates eps* 0.85^i).
OWN LINES for the non-adaptive lower bound (Theorem 11.45(b), from its statement): D_R = n ln(1+e^-u) - ln sum_j C(n,j) e^{-u max(j,R)},
R = least radius with D_R > eps, LB = (1 - 2 delta) 2^n/|B(n, R-1)|, at eps = x_out of the design; exact integer binomials, mpmath 40 digits.
Usage: python3 r13_09_separation_scan.py <u> <n_from> <n_to> [step]
"""
import sys, os, math, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "r6_copy"))
sys.dont_write_bytecode = True
import mpmath as mp
import everyn as EV
mp.mp.dps = 40

def own_ln_LB(n, u, eps, delta):
    u = mp.mpf(u)
    binom = [1] * (n + 1)
    for j in range(1, n + 1):
        binom[j] = binom[j - 1] * (n - j + 1) // j
    w = [mp.mpf(binom[j]) * mp.e ** (-u * j) for j in range(n + 1)]        # C(n,j) e^{-u j}
    tail = [mp.mpf(0)] * (n + 2)                                           # tail[R] = sum_{j >= R} C(n,j) e^{-u j}
    for j in range(n, -1, -1):
        tail[j] = tail[j + 1] + w[j]
    ball = [0] * (n + 1)                                                   # ball[R] = |B(n,R)|
    acc = 0
    for j in range(n + 1):
        acc += binom[j]
        ball[j] = acc
    base = n * mp.log(1 + mp.e ** (-u))
    def D(R):                                                              # sum_j C e^{-u max(j,R)} = e^{-uR} |B(R-1)| + tail[R]
        s = (mp.e ** (-u * R)) * (mp.mpf(ball[R - 1]) if R >= 1 else 0) + tail[R]
        return base - mp.log(s)
    lo, hi = 0, n
    while lo < hi:                                                         # D_R is nondecreasing in R
        mid = (lo + hi) // 2
        if D(mid) > eps:
            hi = mid
        else:
            lo = mid + 1
    R = lo
    return mp.log(1 - 2 * mp.mpf(delta)) + n * mp.log(2) - mp.log(mp.mpf(ball[R - 1])), R

if __name__ == "__main__":
    u = float(sys.argv[1]); n1 = int(sys.argv[2]); n2 = int(sys.argv[3]); step = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    print(f"# r13_09_separation_scan.py u={u} n={n1}..{n2} step {step}; phi = 0.5 (n_o = floor(n/2)), design K64")
    print("#     n   n_o   x_out    lnCmax(R6 code)  lnLB_na(R6 code)  lnLB_na(own lines)  R   lnLB-lnCmax   Cmax<LB")
    holds = []
    for n in range(n1, n2 + 1, step):
        t0 = time.time()
        o, P, xs, lnC = EV.two_level(n, u, 0.5, "K64")
        own, R = own_ln_LB(n, u, mp.mpf(P.x_out), 0.05)
        ok = o["lnCmax"] < float(own)
        holds.append((n, ok))
        print(f"  {n:6d} {o['n_o']:5d} {o['x_out']:.6f}   {o['lnCmax']:12.4f}     {o['ln_na']:12.4f}      {float(own):12.4f}    {R:4d}  {float(own) - o['lnCmax']:+9.4f}   {'yes' if ok else 'NO'}"
              f"   ({time.time()-t0:.1f}s){'   [own LB differs from R6 code!]' if abs(float(own) - o['ln_na']) > 1e-6 else ''}", flush=True)
    first = next((n for n, ok in holds if ok), None)
    lastfail = max((n for n, ok in holds if not ok), default=None)
    print(f"# in this window: first n with C_max < LB: {first};  last n with C_max >= LB: {lastfail};  "
          f"n with C_max >= LB after the first success: {[n for n, ok in holds if not ok and first is not None and n > first]}")
    print("# END")
