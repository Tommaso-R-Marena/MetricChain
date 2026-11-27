"""w12: every optimum of the tables of w04 (six chains, ten accuracies) re-evaluated with the primal solver
(wprimal.py: minimisation over couplings; landscape v by a second-stage coupling) at the generalised-dip profile
of the optimum, and the non-adaptive value through the primal cone formula at x = e + R(e)."""
import time

import numpy as np

from wlib import *
from wprimal import *
from wsites import chains

t00 = time.time()
C = chains()
worst = worst_c = 0.0
for name in ("bin", "path", "tri", "asym", "mix", "mix2"):
    ch = C[name]
    E = ch.E()
    row = []
    for fr in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9):
        e = fr * E
        R, ts = ch.R(e, return_t=True)
        prof, phis, Ms, gam = dip_profile(ch, ts)
        vH = r_primal(ch, prof, e, landscape="H", starts=2)
        vc = cone_primal(ch, prof.P, phis, e + R, starts=2)
        worst = max(worst, abs(vH - R))
        worst_c = max(worst_c, abs(vc - R))
        row.append(f"{fr:.1f}: {vH - R:+.1e}/{vc - R:+.1e}")
    print(f"{ch.name:14s} (primal r_mu*(e;H) - R) / (primal cone value at x = e + R, minus R):  " + "  ".join(row))
print(f"60 optima: largest |primal - R^max| = {worst:.1e}; largest |cone formula at e + R - R| = {worst_c:.1e}; time {time.time()-t00:.0f} s")
