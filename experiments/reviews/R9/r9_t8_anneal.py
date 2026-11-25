# R9 test 8: shape-agnostic search for a counterexample to Theorem F6 among ALL unions of profile classes around one
# centre (2-group grid, any mask): annealing on the mask, objective omega(D) = least omega with
# theta <= R^max(e - omega) + omega  (theta = -ln mu_H(D)/n, e = ln Phi_H^+(D)/n).  F6 predicts sup_D omega(D) -> 0.
# usage: python3 r9_t8_anneal.py p u n m steps seed
import numpy as np, sys, time
from math import log, exp
from r9lib import Par
from r9prof import Grid
p, u, n, m, steps, seed = float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
rng = np.random.default_rng(seed); t0 = time.time()
P = Par(p, u); a = -P.ec(); E = P.E()[0]; ts, Fs, _ = P.table()
def R1(e): return max(float(np.max(Fs - ts * e)), 0.0, -e)
def omega(theta, e):
    if theta <= R1(e): return 0.0
    lo, hi = 0.0, 10.0
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if theta <= R1(e - mid) + mid: hi = mid
        else: lo = mid
    return hi
k = int(round(m * n)); gr = Grid(P, (k, n - k)); lnn = log(n)
lncum, d = gr.density_ball_order((1, 0))
def val(D):
    if D.all() or not D.any(): return -1.0, 0, 0
    ln_mu, ln_pp, ln_phi, ln_md = gr.stats(D)
    th = -ln_mu / n; e = ln_pp / n
    return omega(th, e), th, e
# reference: the best density ball
best_ball = max((val(lncum <= -th * n) + (th,) for th in np.linspace(0.02, 1.2 * a, 60)), key=lambda r: r[0])
print(f"p={p} u={u} n={n} centre type {k/n:.3f}: best density ball: omega = {best_ball[0]:.5f} = {best_ball[0]*n/lnn:.3f} ln n/n (theta={best_ball[1]:.3f}, e={best_ball[2]:+.3f})")
overall = (best_ball[0], 'density ball')
for start in ('ball', 'ball2', 'random', 'hamming', 'empty'):
    if start == 'ball': D = lncum <= -best_ball[3] * n
    elif start == 'ball2': D = lncum <= -0.5 * a * n
    elif start == 'random': D = rng.uniform(size=gr.shape) < 0.3
    elif start == 'hamming': D = d <= int(0.2 * n)
    else:
        D = np.zeros(gr.shape, dtype=bool); D[k, 0] = True      # the centre alone
    cur = val(D); best = cur; T = 0.2 * lnn / n
    for it in range(steps):
        D2 = D.copy()
        mv = rng.integers(0, 4)
        i = int(rng.integers(0, gr.shape[0])); j = int(rng.integers(0, gr.shape[1]))
        if mv == 0: D2[i, j] = ~D2[i, j]
        elif mv == 1:
            w = int(rng.integers(1, 4)); D2[i:i + w, j:j + w] = rng.uniform() < 0.5
        elif mv == 2:    # grow / shrink along the boundary
            nb = np.zeros_like(D); nb[1:] |= D[:-1]; nb[:-1] |= D[1:]; nb[:, 1:] |= D[:, :-1]; nb[:, :-1] |= D[:, 1:]
            cand = np.argwhere(nb & ~D) if rng.uniform() < 0.5 else np.argwhere(D & ~(np.pad(D, 1)[2:, 1:-1] & np.pad(D, 1)[:-2, 1:-1] & np.pad(D, 1)[1:-1, 2:] & np.pad(D, 1)[1:-1, :-2]))
            if len(cand) == 0: continue
            c = cand[rng.integers(0, len(cand))]; D2[c[0], c[1]] = ~D2[c[0], c[1]]
        else:           # a whole anti-diagonal segment (one type class shell range)
            D2[i, :] = D2[i, :] | (rng.uniform(size=gr.shape[1]) < 0.02)
        new = val(D2)
        if new[0] >= cur[0] or rng.uniform() < exp((new[0] - cur[0]) / T):
            D, cur = D2, new
            if cur[0] > best[0]: best = cur
        T = max(T * 0.9995, 1e-5)
    print(f"  start '{start}': best omega found = {best[0]:.5f} = {best[0]*n/lnn:.3f} ln n/n (theta={best[1]:.3f}, e={best[2]:+.3f})   [{time.time()-t0:.0f}s]")
    sys.stdout.flush()
    if best[0] > overall[0]: overall = (best[0], start)
print(f"  overall: {overall[0]:.5f} = {overall[0]*n/lnn:.3f} ln n/n  ({overall[1]});   best density ball: {best_ball[0]*n/lnn:.3f} ln n/n")
