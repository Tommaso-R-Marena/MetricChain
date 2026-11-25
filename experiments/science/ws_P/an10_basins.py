"""Reference conformations (all-helix, all-beta, all-PPII) on the A3 grids: energies of the
known part f and of E = f + g_GB, Gibbs weights, and the collective cost-to-distance ratio
lambda* = min_y (h(y) - h(x0)) / d(x0, y) for the per-torsion envelope of g_GB.
usage: python3 an10_basins.py"""
import numpy as np, json, os
from analysis_lib import *
beta = 1 / KT300
out = {}
for n in range(2, 7):
    d = load("A3", n); R = residuals(d); m = d["m"]; k = d["k"]
    mask = d["clash"] > 0.7
    f = np.where(mask, R["f"], np.inf); g = R["GB"]; E = f + g
    c, _, _ = first_order(g, mask)
    ref = {"helix": tuple([1, 0] * n), "beta": tuple([0, 2] * n), "PPII": tuple([1, 2] * n)}
    x0 = np.unravel_index(np.argmin(f), f.shape); xs = np.unravel_index(np.argmin(E), E.shape)
    name = lambda x: next((kk for kk, v in ref.items() if tuple(int(t) for t in x) == v), str(tuple(int(t) for t in x)))
    st = np.indices(f.shape).reshape(m, -1).T
    ff = f.reshape(-1); EE = E.reshape(-1); ok = np.isfinite(ff)
    piE = np.exp(-beta * (EE[ok] - EE[ok].min())); piE /= piE.sum()
    line = f"n={n}: argmin f = {name(x0)}, argmin E = {name(xs)};"
    for kk, v in ref.items():
        line += f"  {kk}: f-min f = {f[v]-f[x0]:6.2f}, E-min E = {E[v]-E[xs]:6.2f};"
    print(line)
    for label, h, xm in (("f", ff, x0), ("E", EE, xs)):
        xm_flat = np.ravel_multi_index(xm, f.shape)
        D = ((st != st[xm_flat]) * c[None, :]).sum(axis=1)
        with np.errstate(divide="ignore", invalid="ignore"):
            ratio = np.where(ok & (D > 0), (h - h[xm_flat]) / D, np.inf)
        y = int(np.argmin(ratio))
        nflip = int((st[y] != st[xm_flat]).sum())
        # single-flip neighbours
        nb = 0; sharp = 0
        for i in range(m):
            gaps = [h[np.ravel_multi_index(tuple(list(xm[:i]) + [s] + list(xm[i+1:])), f.shape)] - h[xm_flat] for s in range(k) if s != xm[i]]
            gaps = [v for v in gaps if np.isfinite(v)]
            if gaps:
                nb += 1; sharp += int(min(gaps) >= c[i])
        print(f"     landscape {label}: lambda* = {ratio[y]:.4f} at Hamming distance {nflip} (excitation {h[y]-h[xm_flat]:.2f} kcal/mol, envelope distance {D[y]:.1f}); "
              f"sites with a clash-free single-flip neighbour {nb}/{m}, sharp among them {sharp}")
        out[f"{n}|{label}"] = dict(lam=float(ratio[y]), ham=nflip, exc=float(h[y]-h[xm_flat]), nb=nb, sharp=sharp)
    print(f"     Gibbs weight (300 K, grid) of argmin E: {piE.max():.3f}; number of conformations within 1 / 2 / 5 kcal/mol of min E: "
          f"{int((EE[ok]-EE[ok].min() <= 1).sum())} / {int((EE[ok]-EE[ok].min() <= 2).sum())} / {int((EE[ok]-EE[ok].min() <= 5).sum())}")
json.dump(out, open(os.path.join(HERE, "out", "an10_basins.json"), "w"), indent=0)
J = json.load(open(os.path.join(HERE, "out", "an2_second_order.json")))
for key in ("A3|3|f", "A3|4|f", "A3|4|GB"):
    if key in J:
        C = np.array(J[key]["C"]); print(key, "max c_ij", C.max().round(2), "by separation", [round(v[0], 1) for v in J[key]["bysep"].values()])
