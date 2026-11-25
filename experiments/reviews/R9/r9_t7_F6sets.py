# R9 test 7: Theorem F6 on set families that the author did not test: sets that are unions of cells of a 4-group
# profile grid (invariant under S_{n1} x S_{n2} x S_{n3} x S_{n4}), computed exactly:
#   U2   unions of two density balls with different centres (centre types m1, m2, relative distance dd)
#   I2   intersections (lenses) of two such balls
#   U16  unions of the 16 balls around the centres that are constant on each group (plain and with type-dependent radii)
#   HS   half-spaces {sum_g c_g w_g >= tau} and slabs, random coefficients (no centre)
#   EL   ellipsoids in profile space around a fractional profile point (no centre in the cube)
#   RB   random unions of boxes in profile space
# statistic:  theta = -ln mu_H(D)/n,  e = ln Phi_H^+(D)/n,  raw = e - (R^max)^{-1}(theta)   (F6: raw <= O(ln n / n)),
#             omega(D) = least omega with theta <= R^max(e - omega) + omega.
# usage: python3 r9_t7_F6sets.py p u nscale nsets seed      (group sizes are multiples of nscale)
import numpy as np, sys, time
from math import log
from r9lib import Par
from r9prof import Grid, lse
p, u, nscale, nsets, seed = float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
rng = np.random.default_rng(seed)
t0 = time.time()
P = Par(p, u); a = -P.ec(); E = P.E()[0]
ts, Fs, _ = P.table()
eg = np.linspace(-a, E, 20001)
def Rv(e):
    e = np.atleast_1d(np.asarray(e, dtype=float))
    return np.maximum((Fs[None, :] - ts[None, :] * e[:, None]).max(axis=1), np.maximum(0.0, -e))
Rgrid = Rv(eg)
def Rinv(th):
    return -th if th >= a else float(np.interp(th, Rgrid[::-1], eg[::-1]))
def omega(theta, e):
    if theta <= Rv(e)[0]: return 0.0
    lo, hi = 0.0, 10.0
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if theta <= Rv(e - mid)[0] + mid: hi = mid
        else: lo = mid
    return hi

results = {}
def record(fam, gr, D, tag):
    if D.all() or not D.any(): return
    n = gr.n
    ln_mu, ln_pp, ln_phi, ln_md = gr.stats(D)
    theta = -ln_mu / n; e = ln_pp / n
    raw = e - Rinv(theta) if theta > 0 else float('nan')
    om = omega(theta, e)
    results.setdefault((fam, n), []).append((theta, e, raw, om, tag))

def density_ball(gr, pattern, lnq):
    lncum, d = gr.density_ball_order(pattern)
    return lncum <= lnq

def run(sizes):
    gr = Grid(P, sizes); n = gr.n
    lnn = log(n)
    pats = [(1, 1, 0, 0), (1, 0, 1, 0)]         # two centres: s = 1 on groups 0,1 ; s' = 1 on groups 0,2
    cum = [gr.density_ball_order(pt) for pt in pats]
    # single balls (sanity) and unions / intersections of two
    for it in range(nsets):
        th1 = rng.uniform(0.3 * lnn / n * 10, a * 1.1); th2 = th1 * rng.choice([1.0, 1.0, rng.uniform(0.6, 1.6)])
        D1 = cum[0][0] <= -th1 * n; D2 = cum[1][0] <= -th2 * n
        if it < nsets // 4: record('B1 single density ball', gr, D1, (round(th1, 3),))
        record('U2 union of two density balls', gr, D1 | D2, (round(th1, 3), round(th2, 3)))
        if it % 2 == 0: record('I2 intersection of two balls', gr, D1 & D2, (round(th1, 3), round(th2, 3)))
    # Hamming balls (plain radii) around two centres and their union
    d1 = gr.dist_to(pats[0]); d2 = gr.dist_to(pats[1])
    for it in range(nsets // 2):
        r1 = rng.uniform(0.05, 0.45) * n; r2 = r1 * rng.choice([1.0, rng.uniform(0.7, 1.3)])
        record('U2h union of two Hamming balls', gr, (d1 <= r1) | (d2 <= r2), (round(r1 / n, 3), round(r2 / n, 3)))
    # 16 centres: the code {s constant on every group}
    dcode = sum(np.minimum(gr.w[g], gr.sizes[g] - gr.w[g]) for g in range(4))
    dcode = np.broadcast_to(dcode, gr.shape)
    key = gr.ti * (n + 1) + dcode.astype(np.int64)
    shell = np.zeros((n + 1) * (n + 1)); np.add.at(shell, key.ravel(), np.exp(gr.logdens).ravel())
    cumc = np.cumsum(shell.reshape(n + 1, n + 1), axis=1)[gr.ti, dcode.astype(np.int64)]
    for it in range(nsets // 2):
        r = rng.uniform(0.02, 0.4) * n
        record('U16 union of 16 Hamming balls', gr, dcode <= r, (round(r / n, 3),))
        th = rng.uniform(3 * lnn / n, a * 1.1)
        record('U16d union of 16 balls, type-dependent radii', gr, cumc <= np.exp(-th * n), (round(th, 3),))
    # half-spaces and slabs with random coefficients
    wfrac = [gr.w[g] / gr.sizes[g] for g in range(4)]
    for it in range(nsets):
        c = rng.normal(0, 1, 4)
        if it % 3 == 0: c = rng.choice([-1.0, 0.0, 1.0], 4) + rng.normal(0, 0.05, 4)
        lin = sum(c[g] * gr.w[g] for g in range(4)); lin = np.broadcast_to(lin, gr.shape)
        lo, hi = lin.min(), lin.max()
        tau = lo + rng.uniform(0.02, 0.6) * (hi - lo)
        record('HS half-space', gr, lin <= tau, tuple(c.round(2)))
        if it % 2 == 0:
            tau2 = lo + rng.uniform(0.1, 0.9) * (hi - lo); wd = rng.uniform(0.01, 0.15) * (hi - lo)
            record('SL slab', gr, np.abs(lin - tau2) <= wd, tuple(c.round(2)))
    # ellipsoids around a fractional profile point
    for it in range(nsets):
        z = rng.uniform(0.05, 0.95, 4); sc = rng.uniform(0.3, 3.0, 4); r = rng.uniform(0.03, 0.5)
        q = sum(sc[g] * (wfrac[g] - z[g]) ** 2 for g in range(4)); q = np.broadcast_to(q, gr.shape)
        record('EL ellipsoid around a fractional profile', gr, q <= r * r, tuple(z.round(2)))
        if it % 2 == 0:
            l1 = sum(sc[g] * np.abs(wfrac[g] - z[g]) for g in range(4)); l1 = np.broadcast_to(l1, gr.shape)
            record('L1 l1-ball around a fractional profile', gr, l1 <= r * 2, tuple(z.round(2)))
    # random unions of boxes in profile space
    for it in range(nsets // 2):
        D = np.zeros(gr.shape, dtype=bool)
        for b in range(int(rng.integers(1, 5))):
            sl = []
            for g in range(4):
                s = gr.sizes[g]; lo_ = int(rng.integers(0, s)); ln_ = int(rng.integers(1, max(2, s // 2)))
                sl.append(slice(lo_, min(lo_ + ln_, s + 1)))
            D[tuple(sl)] = True
        record('RB random union of boxes', gr, D, ())

for mult in ([1] if nscale > 0 else []):
    # two centres of type 1/2 at relative distance 1/2 (equal groups), and a skew configuration
    run((nscale, nscale, nscale, nscale))
    print(f"done sizes {(nscale,)*4}  [{time.time()-t0:.0f}s]"); sys.stdout.flush()
    s2 = (int(round(1.6 * nscale)), int(round(0.4 * nscale)), int(round(0.4 * nscale)), int(round(1.6 * nscale)))
    run(s2)
    print(f"done sizes {s2}  [{time.time()-t0:.0f}s]"); sys.stdout.flush()

print(f"p={p} u={u}: a={a:.4f} h={P.Rmax(0.0):.4f} E={E:.4f}")
for (fam, n) in sorted(results):
    rec = results[(fam, n)]; lnn = log(n)
    thmin = 3 * lnn / n
    sel = [r for r in rec if r[0] >= thmin]
    if not sel:
        print(f"  n={n} {fam}: {len(rec)} sets, none with theta >= 3 ln n/n"); continue
    raws = np.array([r[2] for r in sel]); oms = np.array([r[3] for r in rec])
    i = int(np.argmax(raws)); j = int(np.argmax(oms))
    print(f"  n={n} {fam}: {len(rec)} sets ({len(sel)} with theta >= 3 ln n/n = {thmin:.3f}); max raw = {raws[i]:+.4f} = {raws[i]*n/lnn:+.2f} ln n/n at theta={sel[i][0]:.3f} e={sel[i][1]:+.3f}; "
          f"max omega (all sets) = {oms[j]:.4f} = {oms[j]*n/lnn:.2f} ln n/n at theta={rec[j][0]:.3f} e={rec[j][1]:+.3f}")
allr = [r for k in results for r in results[k]]
print(f"  total {len(allr)} sets; overall max omega = {max(r[3] for r in allr):.4f}   [{time.time()-t0:.0f}s]")
