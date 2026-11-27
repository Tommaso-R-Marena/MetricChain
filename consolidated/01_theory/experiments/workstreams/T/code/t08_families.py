#!/usr/bin/env python3
"""t08 -- the isoperimetric statement for the flat-histogram instance H on families of sets at larger n that are NOT
unions of profile classes around one centre (exact sums on k-block profile grids, kfin.py):
  (a) neighbourhoods of a 3-block or 4-block profile class C:  D = { x : u d(x,C) + V_n(|x|) < n B }   (random blocks, types, budgets);
  (b) cylinders: a binary shell-neighbourhood on a fraction of the coordinates, the rest free;
  (c) unions of two shell-neighbourhoods around two different centres s1, s2 (4 blocks: the overlap pattern of s1, s2);
  (d) random unions of classes of a 3-block grid (small n);
  (e) the binary optimum itself (2 blocks), as a control.
For every set: e_D = ln Phi+_H(D)/n, theta_D = -ln maxdens(D)/n, and omega(D) = least omega >= 0 with
theta_D <= R(e_D - omega) + omega, where R is the BINARY single-letter function (table of t09).  The theorem of the report
(with the supremum over all block profiles in place of R) says omega -> 0; a family with omega(D) not tending to zero
would show that binary centres are not enough.
Part 0: KFin against brute force (n <= 10).
usage: python3 t08_families.py bJ bB u table_tag n [seed]
"""
import sys, time, math, itertools
import numpy as np
from scipy.special import logsumexp
import tlib as T
import kfin as KF

bJ, bB, u = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
tag = sys.argv[4]
n = int(sys.argv[5])
seed = int(sys.argv[6]) if len(sys.argv) > 6 else 11
phi = T.phi_cw(bJ, bB)
rng = np.random.default_rng(seed)
t0 = time.time()

tab = np.loadtxt(f"../out/Rtable_{tag}.txt")
te, tR = tab[:, 0], tab[:, 1]
slope_lo = (tR[1] - tR[0]) / (te[1] - te[0])


def Rfun(e):
    e = np.asarray(e, dtype=float)
    out = np.interp(e, te, tR)
    out = np.where(e < te[0], np.maximum(-e, tR[0] + slope_lo * (e - te[0])), out)
    out = np.where(e > te[-1], np.maximum(tR[-1] + (tR[-1] - tR[-2]) / (te[-1] - te[-2]) * (e - te[-1]), 0.0), out)
    return np.maximum(out, np.maximum(-e, 0.0))


def omega_of(eD, thD):
    if thD <= Rfun(eD):
        return 0.0
    lo, hi = 0.0, 2.0 * u + 2.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if thD <= Rfun(eD - mid) + mid:
            hi = mid
        else:
            lo = mid
    return hi


# ---- Part 0: brute force ----------------------------------------------------------------------------------------------
nb = 0
for sizes in ((3, 3, 3), (2, 4, 3), (2, 3, 2, 3)):
    f = KF.KFin(sizes, phi, u)
    nn = f.n
    X = np.array(list(itertools.product([0, 1], repeat=nn)), dtype=np.int8)
    wt = X.sum(axis=1)
    Dm = (X[:, None, :] != X[None, :, :]).sum(axis=2).astype(float)
    cuts = np.cumsum((0,) + sizes)
    prof = tuple(X[:, cuts[j]:cuts[j + 1]].sum(axis=1) for j in range(len(sizes)))
    pi = np.exp(-f.J[wt] - f.lCn[wt])
    psi = -f.Vn[wt]
    w = np.exp(-psi)
    A = float((pi * w).sum())
    mu = pi * w / A
    for trial in range(5):
        mask = rng.random(f.t.shape) < 0.3
        if mask.all() or not mask.any():
            continue
        inD = mask[prof]
        out = ~inD
        sx = (u * Dm[:, out] + psi[:, None] - psi[None, out]).min(axis=1)
        PhiP = float((mu[inD] * np.exp(sx[inD])).sum())
        muD = float(mu[inD].sum())
        md = max(inD[wt == t].mean() for t in range(nn + 1))
        lPhiP, lmu, lPhi, md2 = f.dip(mask, f.Vn)
        assert abs(math.exp(lPhiP) - PhiP) < 1e-9 * max(1, PhiP) and abs(math.exp(lmu) - muD) < 1e-9 and abs(md - md2) < 1e-12, (sizes, trial)
        nb += 3
print(f"Part 0: KFin against brute force on full cubes: {nb} checks passed   [{time.time()-t0:.0f}s]")

print(f"\nCurie-Weiss bJ={bJ} bB={bB} u={u}, n = {n}; ln n/n = {math.log(n)/n:.5f}; R from table '{tag}'")
stats = {}


def record(fam, f, mask, note=""):
    if mask.all() or not mask.any():
        return None
    lPhiP, lmu, lPhi, md = f.dip(mask, f.Vn)
    eD, thD = lPhiP / f.n, -math.log(md) / f.n
    om = omega_of(eD, thD)
    s = stats.setdefault(fam, [0, 0.0, None, -9.0])
    s[0] += 1
    if om > s[1]:
        s[1], s[2] = om, (eD, thD, float(Rfun(eD)), note)
    if -0.1 < eD < 0.06:                          # signed excess theta_D - R(e_D) on the range of the table
        s[3] = max(s[3], thD - float(Rfun(eD)))
    return eD, thD, om


def nbhd(f, cell, B):
    """D = { classes : u * l1(class, cell) + V_n(type) < n B }"""
    mask0 = np.zeros(f.t.shape, dtype=bool)
    mask0[cell] = True
    d = f.dist_to(mask0)
    return (f.u * d + f.Vn[f.t]) < f.n * B


def alpha_cell(f, cell):
    return (-f.ldens[cell] + f.J[f.t[cell]]) / f.n          # -ln pi(class)/n


# (e) control: 2 blocks, the binary optimum of the table at e = 0 and neighbours
f2 = KF.KFin((n // 2, n - n // 2), phi, u)
for erow in tab[::max(1, len(tab) // 12)]:
    e, R, m, a, b = erow[:5]
    k = int(round(m * n))
    f = KF.KFin((k, n - k), phi, u)
    cell = (int(round((1 - a) * k)), int(round(b * (n - k))))
    for de in (-0.01, 0.0, 0.01):
        B = e + de + alpha_cell(f, cell)
        r = record("(e) binary optimum of the table", f, nbhd(f, cell, B), note=f"e={e:+.3f}")
# (a) random 3- and 4-block neighbourhoods
for kk, ntr in ((3, 260), (4, 90)):
    for trial in range(ntr):
        lam = rng.dirichlet(np.ones(kk) * 1.5)
        sizes = np.maximum(np.round(lam * n).astype(int), 2)
        sizes[np.argmax(sizes)] += n - sizes.sum()
        if sizes.min() < 2:
            continue
        f = KF.KFin(sizes, phi, u)
        mus = rng.uniform(0.02, 0.98, kk)
        if trial % 3 == 0:                         # near the binary optimum: two groups of blocks around 0.70 and 0.30
            mus = np.where(rng.random(kk) < 0.5, 0.702, 0.298) + rng.normal(0, 0.03, kk)
            mus = np.clip(mus, 0.02, 0.98)
        cell = tuple(int(round(mu_ * s)) for mu_, s in zip(mus, sizes))
        al = alpha_cell(f, cell)
        for e in rng.uniform(-0.06, 0.05, 3):
            B = e + al
            if B * f.n <= f.Vn[f.t[cell]]:
                continue
            record(f"(a) neighbourhoods of a {kk}-block class", f, nbhd(f, cell, B), note=f"sizes={tuple(int(s) for s in sizes)} mus={np.round(mus,3)} e={e:+.3f}")
print(f"  (a),(e) done [{time.time()-t0:.0f}s]", flush=True)
# (b) cylinders: binary shell neighbourhood on a fraction lam of the coordinates, the rest free
for lamc in (0.5, 0.7, 0.85):
    n1 = int(round(lamc * n / 2))
    sizes = (n1, n1, n - 2 * n1)
    f = KF.KFin(sizes, phi, u)
    for x in (0.27, 0.30, 0.33):
        for fr in (0.3, 0.5, 0.7):
            cellc = (int(round((1 - x) * n1)), int(round(x * n1)))
            # cylinder over the free block: all values of the third coordinate
            mask0 = np.zeros(f.t.shape, dtype=bool)
            mask0[cellc[0], cellc[1], :] = True
            d = f.dist_to(mask0)
            for r in (0.03, 0.06, 0.1, 0.15):
                mask = d < r * n                                  # Hamming neighbourhood of the cylinder, any type
                record("(b) cylinders (radius, all types)", f, mask, note=f"lam={lamc} x={x} r={r}")
            cell = (cellc[0], cellc[1], int(round(fr * sizes[2])))
            al = alpha_cell(f, cell)
            for e in (-0.03, 0.0, 0.02):
                record("(b) cylinders (budget around one class)", f, nbhd(f, cell, e + al), note=f"lam={lamc} x={x} free={fr} e={e}")
print(f"  (b) done [{time.time()-t0:.0f}s]", flush=True)
# (c) unions of two shell neighbourhoods around centres s1, s2 of type 1/2 with overlap pattern (11, 10, 01, 00)
for ov in (0.25, 0.4, 0.1):
    n11 = int(round(ov * n))
    n10 = n // 2 - n11
    sizes = (n11, n10, n10, n - n11 - 2 * n10)
    if min(sizes) < 2:
        continue
    f = KF.KFin(sizes, phi, u)
    i11, i10, i01, i00 = f.idx
    k1 = n11 + n10
    # profile around s1: ones of s1 = blocks 11, 10
    a1 = (k1 - i11 - i10) / k1
    b1 = (i01 + i00) / (f.n - k1)
    a2 = (k1 - i11 - i01) / k1
    b2 = (i10 + i00) / (f.n - k1)
    for x in (0.28, 0.30):
        for e in (-0.03, 0.0, 0.02):
            masks = []
            for (aa, bb) in ((a1, b1), (a2, b2)):
                # distance (per site) from the profile (aa,bb) to the shell (x,x) around that centre, plus V_n
                dist = (k1 * np.abs(aa - x) + (f.n - k1) * np.abs(bb - x))
                alc = float(T.MI_bin(k1 / f.n, x, x)) + (f.J[f.n // 2] / f.n)
                masks.append((f.u * dist + f.Vn[f.t]) < f.n * (e + alc))
            record("(c) unions of two shell-neighbourhoods", f, masks[0] | masks[1], note=f"overlap={ov} x={x} e={e}")
            record("(c') one of the two (control)", f, masks[0], note=f"overlap={ov} x={x} e={e}")
print(f"  (c) done [{time.time()-t0:.0f}s]", flush=True)
# (d) random unions of classes on a 3-block grid, and random 'smooth' masks
n3 = min(n, 48)
f = KF.KFin((n3 // 3, n3 // 3, n3 - 2 * (n3 // 3)), phi, u)
for trial in range(200):
    g = rng.normal(size=3)
    c = rng.normal()
    val = sum(gi * (ix / s - 0.5) for gi, ix, s in zip(g, f.idx, f.sizes))
    q = rng.uniform(0.5, 2.5)
    mask = (np.abs(val - 0.2 * c) < 0.1 * q) if trial % 2 else (val > 0.2 * c + 0.15 * q)
    record("(d) slabs and half-spaces in a 3-block grid", f, mask, note=f"n={n3}")
print(f"  (d) done [{time.time()-t0:.0f}s]", flush=True)

print("\nfamily                                           sets   max omega   (in ln n/n)   max[theta_D - R(e_D)]   at (e_D, theta_D, R(e_D))")
for fam, (cnt, om, where, exc) in stats.items():
    nn_ = n3 if fam.startswith("(d)") else n
    w = "" if where is None else f"({where[0]:+.4f}, {where[1]:.4f}, {where[2]:.4f})  {where[3]}"
    print(f"{fam:48s} {cnt:5d}   {om:.5f}     {om/(math.log(nn_)/nn_):6.3f}      {exc:+.5f}             {w}")
print(f"time {time.time()-t0:.0f}s")
