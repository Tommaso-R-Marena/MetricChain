"""R28 — leucine, helix: the two wells on 1-degree windows (my own grids from ff_grid.py --window).

 W1  minima of the two wells at 1 deg against the 2.5 deg grid: positions, energy difference, strains
     of the ideal rotamers;  total energy and vacuum part alone.
 W2  the knife edge: sign of  E(180+d1, 60+d2) - E(300+d1, 180+d2)  for offsets |d1|, |d2| <= 5 deg
     in 1-deg steps (negative: the two-state rigid table prefers (180,60), the 'wrong' state).
 W3  slopes of the energy at the ideal rotamers and curvatures at the minima (thermal widths).
Control: the window energies at the points shared with the 2.5-deg grid must equal the grid's.
"""
import r28_common as rc
rc.cap()
import sys
import time
import numpy as np
import ff_lib as fl

t0 = time.time()
print("R28 ff_window.py  start", rc.utc())
D = "/home/user/MetricChain/experiments/science/ws_R28/"
G = np.load(D + "grid_L_H_144.npz", allow_pickle=True)
Wm = np.load(D + "win_L_H_mt_1deg.npz", allow_pickle=True)
Wt = np.load(D + "win_L_H_tp_1deg.npz", allow_pickle=True)
KT = fl.KT


def tot(z, part):
    return (z["vac"] + (z["gbn2"] if part == "total" else 0.0)) / KT


def at(z, a, b, part="total"):
    ax1, ax2 = z["axes"][0], z["axes"][1]
    i = int(np.argmin(np.abs(np.asarray(ax1, float) - a)))
    j = int(np.argmin(np.abs(np.asarray(ax2, float) - b)))
    assert abs(ax1[i] - a) < 1e-9 and abs(ax2[j] - b) < 1e-9, (a, b)
    return tot(z, part)[i, j]


# control: shared points
worst = 0.0
nsh = 0
for z in (Wm, Wt):
    for a in np.asarray(z["axes"][0], float):
        for b in np.asarray(z["axes"][1], float):
            if (a / 2.5) % 1 == 0 and (b / 2.5) % 1 == 0:
                g = (G["vac"] + G["gbn2"])[int(round(a / 2.5)), int(round(b / 2.5))] / KT
                worst = max(worst, abs(g - at(z, a, b)))
                nsh += 1
print(f"control: {nsh} points shared between the 1-deg windows and the 2.5-deg grid; largest energy difference {worst:.2e} kT -> {'ok' if worst < 1e-9 else 'FAILED'}")

for part in ("total", "vac"):
    Em, Et = tot(Wm, part), tot(Wt, part)
    im = np.unravel_index(Em.argmin(), Em.shape)
    it = np.unravel_index(Et.argmin(), Et.shape)
    pm = (float(Wm["axes"][0][im[0]]), float(Wm["axes"][1][im[1]]))
    pt = (float(Wt["axes"][0][it[0]]), float(Wt["axes"][1][it[1]]))
    g = (G["vac"] + (G["gbn2"] if part == "total" else 0.0)) / KT
    g_mt = g[int(round(287.5 / 2.5)), int(round(157.5 / 2.5))]
    cells_g = {"mt": g[96:145, 48:97].min(), "tp": g[48:97, 0:49].min()}
    print(f"\nW1 [{part}] 1-deg windows: mt-well minimum at {pm} deg; tp-well minimum at {pt} deg;"
          f" E(tp min) - E(mt min) = {Et.min() - Em.min():+.4f} kT   (2.5-deg grid: {cells_g['tp'] - cells_g['mt']:+.4f})")
    print(f"   lowering of the minima by the finer grid: mt {cells_g['mt'] - Em.min():.4f} kT, tp {cells_g['tp'] - Et.min():.4f} kT")
    e300, e180 = at(Wm, 300, 180, part), at(Wt, 180, 60, part)
    print(f"   strains of the ideal rotamers above the 1-deg well minima: (300,180): {e300 - Em.min():.4f} kT; (180,60): {e180 - Et.min():.4f} kT;"
          f" rigid two-state gap E(300,180) - E(180,60) = {e300 - e180:+.4f} kT")
    # W2 knife edge
    print(f"W2 [{part}] E(180+d1, 60+d2) - E(300+d1, 180+d2) [kT]; negative = the table prefers (180,60).  rows d1 = -5..5, columns d2 = -5..5")
    neg = 0
    for d1 in range(-5, 6):
        row = []
        for d2 in range(-5, 6):
            v = at(Wt, 180 + d1, 60 + d2, part) - at(Wm, 300 + d1, 180 + d2, part)
            neg += v < 0
            row.append(f"{v:+7.2f}")
        print(f"   d1 = {d1:+d}: " + " ".join(row))
    print(f"   negative (table prefers the tp state) at {neg} of 121 offsets")
    # W3 slopes and curvatures
    for (nm, z, a, b) in (("(300,180)", Wm, 300, 180), ("(180,60)", Wt, 180, 60)):
        s1 = (at(z, a + 1, b, part) - at(z, a - 1, b, part)) / 2
        s2 = (at(z, a, b + 1, part) - at(z, a, b - 1, part)) / 2
        print(f"W3 [{part}] slope of the energy at the ideal rotamer {nm}: dE/dchi1 = {s1:+.3f}, dE/dchi2 = {s2:+.3f} kT per degree")
    for (nm, z, p) in (("mt", Wm, pm), ("tp", Wt, pt)):
        a, b = p
        try:
            h11 = at(z, a + 1, b, part) - 2 * at(z, a, b, part) + at(z, a - 1, b, part)
            h22 = at(z, a, b + 1, part) - 2 * at(z, a, b, part) + at(z, a, b - 1, part)
            h12 = (at(z, a + 1, b + 1, part) - at(z, a + 1, b - 1, part) - at(z, a - 1, b + 1, part) + at(z, a - 1, b - 1, part)) / 4
            Hm = np.array([[h11, h12], [h12, h22]])
            ev = np.linalg.eigvalsh(Hm)
            print(f"W3 [{part}] curvature at the {nm} minimum {p}: Hessian eigenvalues {ev[0]:.4f}, {ev[1]:.4f} kT/deg^2 -> thermal widths (std) {1/np.sqrt(ev[1]):.1f} and {1/np.sqrt(ev[0]):.1f} deg")
        except AssertionError:
            print(f"W3 [{part}] {nm} minimum on the window edge")
rc.finish(t0)
