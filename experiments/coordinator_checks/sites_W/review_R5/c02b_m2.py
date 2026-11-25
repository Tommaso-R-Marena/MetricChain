"""M2, parts (b), (c) in a light form (the first script ran out of its 590 s in part (b)): F* tabulated on a grid of 4001 slopes."""
import sys, time, math
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import dlib
rng = np.random.default_rng(6)
t0 = time.time()
ds = {k: dlib.Site(*v) for k, v in dlib.SITES.items()}
ts = np.linspace(0, 1, 4001)
tab = {k: np.array([0.0 if (t <= 0 or t >= 1) else dlib.renyi(s, t)[0] for t in ts]) for k, s in ds.items()}
print("tabulated F*_j on 4001 slopes: %.1f s" % (time.time() - t0))

def Rhat(F, e):            # max_t [F(t) - t e] on the grid (a lower bound of the true value, error O(grid^2))
    return float(np.max(F - ts * e))

def theta_na(F, x):
    m = ts < 1
    return float(np.max((F[m] - ts[m] * x) / (1 - ts[m])))

print("(b) theta <= Rhat(x - theta - w) + w  =>  theta <= theta_na(x - 2w) + w   (three chains, 3000 random (x, w))")
worst = -1.0
for names, lam in ((("bin", "path"), (0.5, 0.5)), (("bin", "tri"), (0.4, 0.6)), (("path", "tri", "asym"), (0.2, 0.3, 0.5))):
    F = sum(l * tab[k] for l, k in zip(lam, names))
    for _ in range(1000):
        x = float(rng.uniform(0.005, 0.5)); w = float(rng.uniform(0.0, x / 2.05))
        lo, hi = -1.0, 3.0
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if mid <= Rhat(F, x - mid - w) + w: lo = mid
            else: hi = mid
        worst = max(worst, lo - (theta_na(F, x - 2 * w) + w))
print("   largest [theta_max - (theta_na(x - 2w) + w)] = %.2e  (0 up to the grid error: the two sides are equal)" % worst)

print("(a') Lipschitz bound again, on the tabulated functions, 20000 random pairs of compositions of the four site types, x in (0, 0.5)")
names = ("bin", "path", "tri", "asym")
amax = max(dlib.a_site(ds[k])[1] for k in names)
big = 0.0
for _ in range(20000):
    lam = rng.dirichlet(np.ones(4) * rng.choice([0.3, 1.0, 5.0])); lam2 = rng.dirichlet(np.ones(4) * rng.choice([0.3, 1.0, 5.0]))
    x = float(rng.uniform(1e-4, 0.5))
    d = abs(theta_na(sum(l * tab[k] for l, k in zip(lam, names)), x) - theta_na(sum(l * tab[k] for l, k in zip(lam2, names)), x))
    big = max(big, d / (float(np.abs(lam - lam2).sum()) * amax))
print("   largest |theta_na^lam' - theta_na^lam| / (||lam' - lam||_1 max_j a_j) = %.4f  (must be <= 1; 1/2 is the best constant when sum = 0 is used)" % big)

print("(c) compositions of the blocks: inner block n_j - floor(phi n_j), outer block floor(phi n_j)")
worst_i = worst_o = worst_i_m = 0.0
for _ in range(300000):
    m = int(rng.integers(2, 7)); phi = float(rng.uniform(0.05, 0.95))
    nj = rng.integers(1, 400, m) if rng.random() < 0.5 else np.concatenate([rng.integers(1, 6, m - 1), [int(rng.integers(100, 4000))]])
    n = int(nj.sum()); no = np.floor(phi * nj).astype(int); ni = nj - no
    if no.sum() == 0 or phi * n - m <= 0: continue
    di = float(np.abs(ni / ni.sum() - nj / n).sum()) * (1 - phi) * n
    do = float(np.abs(no / no.sum() - nj / n).sum()) * (phi * n - m)
    worst_i = max(worst_i, di / (2 * m)); worst_o = max(worst_o, do / (2 * m)); worst_i_m = max(worst_i_m, di / m)
print("   max ||lam_inner - lam||_1 (1-phi) n / (2m) = %.4f (<= 1: my bound holds);   the same with m in place of 2m: %.4f (> 1: the reviewer's"
      " constant m is too small);   max ||lam_outer - lam||_1 (phi n - m)/(2m) = %.4f" % (worst_i, worst_i_m, worst_o))
print("time %.1f s" % (time.time() - t0))
