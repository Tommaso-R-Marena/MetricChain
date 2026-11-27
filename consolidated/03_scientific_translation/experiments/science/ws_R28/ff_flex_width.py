"""R28 — item 101 (c) also says rigid bond geometry makes "the wells narrower than they are in a molecule".
Measured here on the adiabatic relaxed maps written by ff_flex.py --map 5 (leucine, helix; 5-degree step):
for the two main wells, the effective area  A = sum over the 120-degree cell of exp(-(E - E_cellmin)) x step^2
(deg^2; for a harmonic well A = 2 pi sigma_1 sigma_2), for the relaxed energy and for the rigid energy
on the SAME points.  Control: the rigid effective area on the 5-degree sub-grid against the full 2.5-degree grid.
"""
import r28_common as rc
rc.cap()
import time
import numpy as np

t0 = time.time()
print("R28 ff_flex_width.py  start", rc.utc())
D = "/home/user/MetricChain/experiments/science/ws_R28/"
KT = 0.596
G = np.load(D + "grid_L_H_144.npz", allow_pickle=True)
Eg = (G["vac"] + G["gbn2"]) / KT
Eg = Eg - Eg.min()
cells = {"mt cell (240-360, 120-240)": ((240, 360), (120, 240)), "tp cell (120-240, 0-120)": ((120, 240), (0, 120))}


def area(E, ax1, ax2, cell, step):
    (a0, a1), (b0, b1) = cell
    m1 = (ax1 >= a0) & (ax1 < a1)
    m2 = (ax2 >= b0) & (ax2 < b1)
    sub = E[np.ix_(m1, m2)]
    fin = np.isfinite(sub)
    emin = sub[fin].min()
    return float(np.exp(-(sub[fin] - emin)).sum() * step * step), float(emin)


ax_full = np.arange(144) * 2.5
for var in ("A", "B"):
    z = np.load(D + f"flexmap_L_H_{var}.npz")
    ax, Em = z["ax"], z["Em"]
    Em = Em - Em[np.isfinite(Em)].min()
    Er = np.array([[Eg[int(round(c1 / 2.5)) % 144, int(round(c2 / 2.5)) % 144] for c2 in ax] for c1 in ax])
    Er_masked = np.where(np.isfinite(Em), Er, np.inf)
    print(f"variant {var}: {int(np.isfinite(Em).sum())} relaxed points")
    for nm, cell in cells.items():
        a_rel, e_rel = area(Em, ax, ax, cell, 5.0)
        a_rig, e_rig = area(Er_masked, ax, ax, cell, 5.0)
        a_full, _ = area(Eg, ax_full, ax_full, cell, 2.5)
        print(f"   {nm}: effective area relaxed {a_rel:7.1f} deg^2 (sqrt {np.sqrt(a_rel):.1f} deg), rigid on the same points {a_rig:7.1f} (sqrt {np.sqrt(a_rig):.1f});"
              f" ratio relaxed/rigid {a_rel / a_rig:.2f}   [control: rigid on the full 2.5-deg grid {a_full:7.1f}; 5-deg/2.5-deg {a_rig / a_full:.3f}]"
              f"   cell minimum above the map minimum: relaxed {e_rel:.3f}, rigid {e_rig:.3f} kT")
rc.finish(t0)
