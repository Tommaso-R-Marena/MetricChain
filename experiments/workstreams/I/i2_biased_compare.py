#!/usr/bin/env python3
"""Workstream I, experiment 2: the inductive growth bound on the p-biased cube against candidate
extremal sets: balls around the rare vertex (up-sets {|x| >= n - r} when ones are rare), balls
around the likely vertex, and 'layers' {a <= |x| <= b}.  Floating point; nothing certified."""
import sys, math
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from i1_dp_growth import make_index, step

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    hd = float(sys.argv[2]) if len(sys.argv) > 2 else 0.01
    q1 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.2
    q0 = 1 - q1
    dmax = n * math.log(1 / min(q0, q1)) + 1.0
    K = int(math.ceil(dmax / hd))
    T = n
    idx, idx_e0 = make_index(K, hd, q0, q1)
    G = np.ones((T + 1, K + 2)); G[:, K + 1] = 0.0
    for i in range(1, n + 1):
        G = step(G, idx, idx_e0, q0, q1, 1, 1)
    pmf = [math.comb(n, j) * q1 ** j * q0 ** (n - j) for j in range(n + 1)]
    def layer(a, b):      # measure of {a <= |x| <= b}
        a = max(a, 0); b = min(b, n)
        return sum(pmf[a:b + 1]) if a <= b else 0.0
    print(f"n={n} q1={q1} hd={hd} (grid slack about n*hd = {n*hd:.3f} in -ln m)")
    print("candidate sets E = {a <= |x| <= b}; E_t = {a - t <= |x| <= b + t};  loss = -ln DP(m(E), t) + ln mu(E_t) >= 0 up to the slack")
    print("  a   b   t   -ln mu(E)  -ln mu(E_t)   -ln DP   loss")
    worst = (0, None)
    rows = []
    for a in range(0, n + 1):
        for b in range(a, n + 1):
            mE = layer(a, b)
            if mE >= 1 - 1e-12: continue
            k = int(math.ceil(-math.log(mE) / hd - 1e-9))
            if k > K: continue
            for t in range(1, n + 1):
                mEt = layer(a - t, b + t)
                val = G[t, k]
                loss = -math.log(val) + math.log(mEt)
                rows.append((loss, a, b, t, -math.log(mE), -math.log(mEt), -math.log(val)))
    rows.sort()
    print("ten smallest losses (the sets that come closest to the bound):")
    for (loss, a, b, t, dE, dEt, dv) in rows[:10]:
        print(f" {a:3d} {b:3d} {t:3d}  {dE:9.4f}  {dEt:10.4f}  {dv:9.4f}  {loss:8.4f}")
    # per (measure class, t): the best candidate
    print("for up-balls {|x| >= n-r} (rare side), down-balls {|x| <= r}, and the best layer of comparable measure:")
    print("  r   t  | up-ball: -ln m, loss | down-ball: -ln m, loss")
    for r in range(0, n, max(1, n // 8)):
        for t in (1, 2, max(1, n // 4)):
            mu_u = layer(n - r, n); mu_d = layer(0, r)
            out = f" {r:3d} {t:3d}  |"
            for (mE, mEt) in ((mu_u, layer(n - r - t, n)), (mu_d, layer(0, r + t))):
                if mE >= 1 - 1e-12 or -math.log(mE) / hd > K:
                    out += "      -          -   |"; continue
                k = int(math.ceil(-math.log(mE) / hd - 1e-9))
                loss = -math.log(G[t, k]) + math.log(mEt)
                out += f" {-math.log(mE):8.4f} {loss:9.4f} |"
            print(out)
    neg = [r for r in rows if r[0] < -1e-9]
    print(f"candidates below the bound (must be none): {len(neg)}")
    assert not neg

if __name__ == "__main__":
    main()
