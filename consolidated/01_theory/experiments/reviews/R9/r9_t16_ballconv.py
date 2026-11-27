# R9 test 16: Theorem F6 on density balls at FIXED theta, n = 250 ... 4000: the excess
#   raw = ln Phi_H^+(D)/n - (R^max)^{-1}(theta),  theta = -ln mu_H(D)/n,
# in units of ln n / n (must stay bounded if the exponent of the tail function of H is (R^max)^{-1}), maximised over
# centre types; and omega(D).   usage: python3 r9_t16_ballconv.py p u
import numpy as np, sys, time
from math import log
from r9lib import Par
from r9prof import Grid
p, u = float(sys.argv[1]), float(sys.argv[2]); t0 = time.time()
P = Par(p, u); a = -P.ec(); E = P.E()[0]; hh = P.Rmax(0.0); ts, Fs, _ = P.table()
def R1(e): return max(float(np.max(Fs - ts * e)), 0.0, -e)
def omega(theta, e):
    if theta <= R1(e): return 0.0
    lo, hi = 0.0, 10.0
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if theta <= R1(e - mid) + mid: hi = mid
        else: lo = mid
    return hi
print(f"p={p} u={u}: h={hh:.4f} a={a:.4f} E={E:.4f}")
targets = [0.5 * hh, hh, 0.5 * (hh + a), 0.9 * a]
for th in targets:
    row = []
    for n in (250, 500, 1000, 2000, 4000):
        best = (-np.inf, None)
        for m in (0.40, 0.45, 0.50, 0.55, 0.60):
            k = int(round(m * n)); gr = Grid(P, (k, n - k)); lncum, d = gr.density_ball_order((1, 0))
            D = lncum <= -th * n
            if not D.any() or D.all(): continue
            ln_mu, ln_pp, ln_phi, ln_md = gr.stats(D)
            theta = -ln_mu / n; e = ln_pp / n; raw = e - P.Rmax_inv(theta)
            if raw > best[0]: best = (raw, m, theta, e, omega(theta, e))
        row.append((n, best))
    print(f"  target theta = {th:.4f}: " + "; ".join(f"n={n}: raw={b[0]:+.5f} = {b[0]*n/log(n):+.2f} ln n/n (m={b[1]}, omega = {b[4]*n/log(n):.2f} ln n/n)" for n, b in row) + f"   [{time.time()-t0:.0f}s]")
    sys.stdout.flush()
