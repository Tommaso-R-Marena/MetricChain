"""Continuous single-torsion scans: oscillation and torsion-space Lipschitz constants of the
residuals along one torsion (others fixed at conformations of ensemble C); the torus formula
of Theorem 11.34 with the measured numbers.  Values are maxima over a sample of base
conformations -> lower bounds on the suprema.
usage: python3 an8_scans.py n [n ...]"""
import sys, os, json, math
import numpy as np
from analysis_lib import *

np.set_printoptions(precision=1, suppress=True, linewidth=220)
beta = 1 / KT300
out = {}
for n in [int(a) for a in sys.argv[1:]]:
    d = dict(np.load(os.path.join(HERE, "data", f"scan_n{n}.npz")))
    step = math.radians(float(d["step"])); Nb, m, K = d["gbn2"].shape
    ok = d["clash"] > 0.7
    f = d["tors"] + d["lj"] + d["coul"]
    res = {"GB": d["gbn2"], "ff03-ff14SB": d["ff03_tors"] + d["ff03_lj"] + d["ff03_coul"] - f,
           "ff15ipq-ff14SB": d["ff15ipq_tors"] + d["ff15ipq_lj"] + d["ff15ipq_coul"] - f, "coul+GB": d["coul"] + d["gbn2"], "f": f}
    allowed = ok.mean(axis=2)                      # fraction of the circle that is clash-free
    print(f"\n=== n={n}: {Nb} base conformations x {m} torsions x {K} angles (step {math.degrees(step):.0f} deg); "
          f"mean clash-free fraction of a torsion circle: {allowed.mean():.2f}")
    for name, g in res.items():
        gm = np.where(ok, g, np.nan)
        with np.errstate(all="ignore"):
            osc = np.nanmax(gm, axis=2) - np.nanmin(gm, axis=2)            # (Nb, m)
        osc = np.where(ok.sum(axis=2) >= 2, osc, np.nan)
        dg = np.abs(np.roll(gm, -1, axis=2) - gm) / step                   # adjacent pairs incl. wrap-around
        with np.errstate(all="ignore"):
            lip = np.nanmax(dg, axis=2)
        cmax = np.nanmax(osc, axis=0); cmed = np.nanmedian(osc, axis=0)
        Lmax = np.nanmax(lip, axis=0); Lmed = np.nanmedian(lip, axis=0)
        b = beta * Lmax * math.pi / 2
        J = float(np.sum(np.log(np.sinh(np.minimum(b, 700)) / b))) if np.all(b < 700) else float(np.sum(b - np.log(2 * b)))
        print(f"{name:15s} oscillation along one torsion (kcal/mol): max over bases {cmax}  (median {np.round(np.nanmedian(cmed),1)})")
        print(f"{'':15s} Lipschitz constant L_i (kcal/mol/rad): max {Lmax}  (median {np.round(np.nanmedian(Lmed),1)});  "
              f"b_i = beta L_i pi/2 up to {b.max():.0f};  J = sum ln(sinh b_i / b_i) = {J:.0f} nats")
        out[f"{n}|{name}"] = dict(osc_max=cmax.tolist(), osc_med=cmed.tolist(), L_max=Lmax.tolist(), L_med=Lmed.tolist(), J=J)
p = os.path.join(HERE, "out", "an8_scans.json")
old = json.load(open(p)) if os.path.exists(p) else {}
old.update(out); json.dump(old, open(p, "w"), indent=0)
