"""M2 numerical checks: (a) |theta_na^{lam'}(x) - theta_na^{lam}(x)| <= ||lam' - lam||_1 max_j a_j, with the harness helpers
(st_theta_na, st_a) and with my own code; (b) the implication of (G2) as a statement about functions;
(c) the composition of the inner/outer block against the composition of the chain."""
import sys, time, math
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import dlib
H = dlib.load_harness()
rng = np.random.default_rng(5)
t0 = time.time()

hs = {k: H.st_site(*v) for k, v in H.ST_SITES.items()}
ds = {k: dlib.Site(*v) for k, v in dlib.SITES.items()}
a_h = {k: H.st_a(s) for k, s in hs.items()}
a_d = {k: dlib.a_site(s) for k, s in ds.items()}
E_d = {k: dlib.E_site(s) for k, s in ds.items()}
print("capacities a_j  harness:", {k: round(v, 6) for k, v in a_h.items()}, " own (lower, upper):", {k: (round(v[0], 9), round(v[1], 9)) for k, v in a_d.items()})

print("(a) Lipschitz bound in the composition")
examples = [
    ("mix  (bin, path)", ("bin", "path"), (0.5, 0.5), [(0.45, 0.55), (0.55, 0.45), (0.3, 0.7), (0.52, 0.48)]),
    ("mix2 (bin, tri)", ("bin", "tri"), (0.4, 0.6), [(0.35, 0.65), (0.45, 0.55), (0.6, 0.4), (0.41, 0.59)]),
    ("three types (bin, path, asym)", ("bin", "path", "asym"), (0.3, 0.3, 0.4), [(0.25, 0.35, 0.4), (0.3, 0.2, 0.5), (0.34, 0.33, 0.33)]),
]
worst_ratio_h = worst_ratio_d = 0.0
for label, names, lam, others in examples:
    amax_h = max(a_h[k] for k in names); amax_d = max(a_d[k][1] for k in names)
    E = sum(l * E_d[k] for l, k in zip(lam, names))
    for lam2 in others:
        l1 = sum(abs(x - y) for x, y in zip(lam, lam2))
        dh = dd = 0.0
        for frac in (0.05, 0.15, 0.3, 0.5, 0.7, 0.9, 1.1):
            x = frac * E
            th1 = H.st_theta_na([(l, hs[k]) for l, k in zip(lam, names)], x)
            th2 = H.st_theta_na([(l, hs[k]) for l, k in zip(lam2, names)], x)
            dh = max(dh, abs(th1 - th2))
            td1 = dlib.theta_na([(l, ds[k]) for l, k in zip(lam, names)], x)
            td2 = dlib.theta_na([(l, ds[k]) for l, k in zip(lam2, names)], x)
            dd = max(dd, abs(td1 - td2))
        worst_ratio_h = max(worst_ratio_h, dh / (l1 * amax_h)); worst_ratio_d = max(worst_ratio_d, dd / (l1 * amax_d))
        print("   %-30s lam = %s, lam' = %s: ||.||_1 = %.3f, bound = %.6f; max_x |diff|: harness %.6f, own %.6f  -> %s" %
              (label, lam, lam2, l1, l1 * amax_d, dh, dd, "ok" if max(dh, dd) <= l1 * amax_d + 1e-9 else "VIOLATION"))
print("   largest |diff| / bound: harness helpers %.4f, own code %.4f (must be <= 1)" % (worst_ratio_h, worst_ratio_d))

# random compositions, own code, including x close to 0 (where the bound is nearly attained if a single type dominates)
viol = 0; big = 0.0; n = 0
names = ("bin", "path", "tri", "asym")
amax = max(a_d[k][1] for k in names)
for _ in range(60):
    lam = rng.dirichlet(np.ones(4)); lam2 = rng.dirichlet(np.ones(4)) if rng.random() < 0.5 else np.abs(lam + rng.normal(0, 0.02, 4))
    lam2 = lam2 / lam2.sum()
    l1 = float(np.abs(lam - lam2).sum())
    x = float(rng.choice([0.002, 0.01, 0.05, 0.1, 0.2, 0.3]))
    d = abs(dlib.theta_na([(l, ds[k]) for l, k in zip(lam, names)], x, tmax=0.9999, grid=120) - dlib.theta_na([(l, ds[k]) for l, k in zip(lam2, names)], x, tmax=0.9999, grid=120))
    n += 1; big = max(big, d / (l1 * amax))
    if d > l1 * amax + 1e-9: viol += 1
print("   60 random pairs of compositions of four site types (own code), x in [0.002, 0.3]: violations %d, largest |diff|/bound = %.4f" % (viol, big))

print("(b) the implication used in (G2):  theta <= Rhat(x - theta - w) + w   =>   theta <= theta_na(x - 2w) + w")
chain = [(0.5, ds["bin"]), (0.5, ds["path"])]
worst = -1.0; cnt = 0
for _ in range(40):
    x = float(rng.uniform(0.02, 0.3)); w = float(rng.uniform(0.0, x / 2.2))
    lo, hi = -1.0, 2.0                      # largest theta with theta <= Rhat(x - theta - w) + w (the left side minus the right is increasing)
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if mid <= dlib.Rhat(chain, x - mid - w, grid=40)[0] + w: lo = mid
        else: hi = mid
    rhs = dlib.theta_na(chain, x - 2 * w, tmax=0.9999, grid=120) + w
    worst = max(worst, lo - rhs); cnt += 1
print("   %d random (x, w): largest [theta_max - (theta_na(x - 2w) + w)] = %.2e (must be <= 0 up to solver error)" % (cnt, worst))

print("(c) compositions of the blocks: inner block n_j - floor(phi n_j), outer block floor(phi n_j)")
worst_i = worst_o = 0.0; worst_i_m = 0.0
for _ in range(200000):
    m = int(rng.integers(2, 6)); phi = float(rng.uniform(0.05, 0.95))
    nj = rng.integers(1, 400, m) if rng.random() < 0.5 else np.concatenate([rng.integers(1, 4, m - 1), [int(rng.integers(100, 4000))]])
    n = nj.sum(); no = np.floor(phi * nj).astype(int); ni = nj - no
    if no.sum() == 0 or phi * n - m <= 0: continue
    di = np.abs(ni / ni.sum() - nj / n).sum() * (1 - phi) * n
    do = np.abs(no / no.sum() - nj / n).sum() * (phi * n - m)
    worst_i = max(worst_i, di / (2 * m)); worst_o = max(worst_o, do / (2 * m)); worst_i_m = max(worst_i_m, di / m)
print("   ||lam_inner - lam||_1 (1-phi) n / (2m) <= %.4f;  the same divided by m instead of 2m: %.4f (reviewer's constant m fails if > 1);"
      "  ||lam_outer - lam||_1 (phi n - m)/(2m) <= %.4f" % (worst_i, worst_i_m, worst_o))
print("time %.1f s" % (time.time() - t0))
