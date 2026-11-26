"""R11 / 08b -- the remark of section 6.3: "With Q = pi the worst label is the uniform field and
the bound is the closed form t E_F(u) - E_F(tu)".  Safe tilt-state bound with q~ = p against the
closed form, for several grids; and the q~-dependence at p = 0.2.

Run:  python3 r11_08b_Qpi_check.py     (about 2-3 minutes)
"""
import time
import numpy as np
from r11lib import *
from r11_08_propG import Grid, u

T0 = time.time()
for p, t in ((0.4, 0.45), (0.3, 0.43), (0.2, 0.419), (0.1, 0.38)):
    cf = t * E_F(p, u) - E_F(p, t * u)
    row = []
    for G in (201, 401, 801, 1601):
        gr = Grid(p, G)
        val, low, w, it = gr.rate(t, p, iters=8000, tol=1e-11)
        row.append(f"G={G}: {val:.6f}")
    print(f"p={p} t={t}: closed form (uniform field, Q = pi) {cf:.6f};  safe relaxed value at q~ = p: " + "  ".join(row) + f"   [{time.time()-T0:.0f} s]", flush=True)
print()
p, t = 0.2, 0.419
gr = Grid(p, 801)
for q in (0.16, 0.17, 0.18, 0.19, 0.195, 0.2, 0.205, 0.21):
    print(f"p={p} t={t} G=801 q~={q}: safe bound {gr.rate(t, q, iters=8000, tol=1e-11)[0]:.6f}", flush=True)
print(f"{time.time()-T0:.1f} s")
