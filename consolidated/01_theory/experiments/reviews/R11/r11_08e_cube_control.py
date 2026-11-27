"""R11 / 08e -- control of my safe tilt-state recursion at p = 1/2 (uniform cube) and for p -> 1/2:
it must return the cube values from above:  F_c(t) = t ln cosh(u/2) - ln cosh(tu/2),  E = ln cosh(u/2),
a = (u/2) tanh(u/2) - ln cosh(u/2).

Run:  python3 r11_08e_cube_control.py      (about 1 minute)
"""
import numpy as np
from r11lib import *
from r11_08_propG import Grid, a_rate, u

hc, tc, ac, Ec = cube_constants(u)
for p in (0.5, 0.499, 0.49, 0.45):
    for G in (201, 801):
        gr = Grid(p, G)
        row = []
        for t in (0.3, 0.49, 0.7):
            v = min(gr.rate(t, q, iters=6000, tol=1e-11)[0] for q in (p, 0.5))
            row.append(f"F({t}) <= {v:.6f} [cube {cube_F(t):.6f}]")
        E, _, _ = gr.E_rate()
        a = min(a_rate(gr, q)[0] for q in (p, 0.5))
        print(f"p={p} G={G}: " + "  ".join(row) + f"  E <= {E:.6f} [cube {Ec:.6f}; E_F {E_F(p,u):.6f}]  a <= {a:.6f} [cube {ac:.6f}]", flush=True)
